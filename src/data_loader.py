"""
Data Loader & Feature Engineering Module for CarbonGlobe
Extracts multi-decade spatiotemporal climate drivers and builds high-precision
PCHIP physical anchor baseline representations.
"""

import os
import numpy as np
from scipy.interpolate import PchipInterpolator
from src.config import SEED_AGES, NUM_SEED_AGES, TARGET_NAMES, HEIGHT_MEAN, AGB_MEAN

TARGET_AGES = np.clip(np.array(SEED_AGES, dtype=np.float32) + 40.0, 1.0, 500.0)

def compute_pchip_anchor(y0_array: np.ndarray) -> np.ndarray:
    """
    Computes smooth monotonic PCHIP stand development trajectories from Year 0 to Year 40.
    y0_array: shape (N_sites, 15, 7)
    Returns: shape (N_sites, 15, 7)
    """
    seed_ages_arr = np.array(SEED_AGES, dtype=np.float32)
    pchip_anchor = np.zeros_like(y0_array, dtype=np.float32)
    for var_idx in range(y0_array.shape[-1]):
        interp = PchipInterpolator(seed_ages_arr, y0_array[:, :, var_idx], axis=1)
        pchip_anchor[:, :, var_idx] = interp(TARGET_AGES)
    return np.maximum(0.0, pchip_anchor)


# Global fitted PCA and scaler for climate drivers
_CLIMATE_SCALER = None
_CLIMATE_PCA = None

def _get_or_fit_climate_pca(raw_site_means: np.ndarray, n_components: int = 10):
    global _CLIMATE_SCALER, _CLIMATE_PCA
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    
    if _CLIMATE_SCALER is None or _CLIMATE_PCA is None:
        _CLIMATE_SCALER = StandardScaler().fit(raw_site_means)
        _CLIMATE_PCA = PCA(n_components=n_components, random_state=42).fit(
            _CLIMATE_SCALER.transform(raw_site_means)
        )
    return _CLIMATE_PCA.transform(_CLIMATE_SCALER.transform(raw_site_means))


def extract_site_climate_features(x_array: np.ndarray) -> np.ndarray:
    """
    Vectorized extraction of key multi-decade climate, moisture, and environmental drivers.
    Includes 10-component standardized PCA across all 136 drivers.
    x_array: shape (N_sites, 40_years, 12_months, 136_drivers)
    Returns: shape (N_sites, N_climate_feats)
    """
    x = x_array.astype(np.float32)
    
    # 1. Driver 0: 2m Air Temperature (K)
    t = x[:, :, :, 0]
    t_ann = t.mean(axis=2) # (N, 40)
    t_mean = t_ann.mean(axis=1)
    t_trend = t_ann[:, -10:].mean(axis=1) - t_ann[:, :10].mean(axis=1)
    t_min = t.min(axis=(1, 2))
    t_max = t.max(axis=(1, 2))
    t_range = t_max - t_min
    t_std = t.std(axis=(1, 2))
    frost_months = (t < 273.15).mean(axis=(1, 2))
    warm_months = (t > 283.15).mean(axis=(1, 2))
    
    # 2. Driver 1: Precipitation (mm/month)
    p = x[:, :, :, 1]
    p_ann = p.sum(axis=2) # (N, 40)
    p_mean = p_ann.mean(axis=1)
    p_trend = p_ann[:, -10:].mean(axis=1) - p_ann[:, :10].mean(axis=1)
    p_min = p_ann.min(axis=1)
    p_max = p_ann.max(axis=1)
    p_cv = p_ann.std(axis=1) / (p_mean + 1e-4)
    dry_months = (p < 20.0).mean(axis=(1, 2))
    
    # 3. Drivers 2-7: Multi-depth Soil Temperature Profile
    soil_t = x[:, :, :, 2:6]
    soil_t_mean = soil_t.mean(axis=(1, 2, 3))
    soil_t_grad = soil_t[:, :, :, 0].mean(axis=(1, 2)) - soil_t[:, :, :, -1].mean(axis=(1, 2))
    
    # 4. Atmospheric Moisture & Wind (across vertical levels)
    q_hum = x[:, :, :, [33, 49, 65, 81]].mean(axis=3)
    wind = x[:, :, :, [36, 52, 68, 84]].mean(axis=3)
    hum_mean = q_hum.mean(axis=(1, 2))
    hum_max = q_hum.max(axis=(1, 2))
    wind_mean = wind.mean(axis=(1, 2))
    
    # 5. Driver 8: Atmospheric CO2 Concentration
    co2 = x[:, :, :, 8]
    co2_delta = co2[:, -1, -1] - co2[:, 0, 0]
    co2_rate = co2_delta / 40.0
    
    # 6. Driver 35: Solar Radiation & Driver 135: Surface Pressure
    rad = x[:, :, :, 35]
    rad_mean = rad.mean(axis=(1, 2))
    rad_std = rad.std(axis=(1, 2))
    press = x[:, :, :, 135]
    press_mean = press.mean(axis=(1, 2))
    
    # 7. Physical Interaction Indices
    aridity = t_mean / (p_mean + 1.0)
    water_deficit = (t_mean / 288.15) * 100.0 - p_mean
    temp_co2_interaction = t_trend * co2_delta
    temp_precip_product = t_mean * p_mean
    
    # 8. PCA across all 136 drivers
    site_raw_means = x.mean(axis=(1, 2))
    pca_feats = _get_or_fit_climate_pca(site_raw_means, n_components=10)
    
    feats = np.column_stack([
        t_mean, t_trend, t_min, t_max, t_range, t_std, frost_months, warm_months,
        p_mean, p_trend, p_min, p_max, p_cv, dry_months,
        soil_t_mean, soil_t_grad,
        hum_mean, hum_max, wind_mean,
        co2_delta, co2_rate,
        rad_mean, rad_std, press_mean,
        aridity, water_deficit, temp_co2_interaction, temp_precip_product,
        pca_feats
    ])
    return feats.astype(np.float32)


def build_sample_feature_matrix(site_climate_feats: np.ndarray, y0_states: np.ndarray, pchip_anchor: np.ndarray) -> np.ndarray:
    """
    Combines site-level climate features with sample-level (site, seed_age) initial and anchor states.
    site_climate_feats: (N_sites, N_climate_feats)
    y0_states: (N_sites, 15, 7)
    pchip_anchor: (N_sites, 15, 7)
    Returns: (N_sites * 15, N_total_feats) matrix
    """
    N_sites = site_climate_feats.shape[0]
    rows = []
    
    for s_idx in range(N_sites):
        c_feat = site_climate_feats[s_idx]
        y0_all = y0_states[s_idx]
        anc_all = pchip_anchor[s_idx]
        
        h_max = y0_all[:, 0].max() + 1e-4
        agb_max = y0_all[:, 1].max() + 1e-4
        
        for a_idx, age in enumerate(SEED_AGES):
            st = y0_all[a_idx]      # (7,)
            anc = anc_all[a_idx]    # (7,)
            anc_delta = anc - st    # (7,)
            
            # Ecological Interaction Indices
            cue = st[5] / (st[4] + 1e-4)        # Carbon Use Efficiency (NPP / GPP)
            bio_dens = st[1] / (st[0] + 1e-4)   # Biomass Density (AGB / Height)
            soil_turn = st[6] / (st[2] + 1e-4)  # Soil Carbon Turnover (Rh / Soil)
            rel_h = st[0] / h_max               # Relative Height Carrying Capacity
            rel_a = st[1] / agb_max             # Relative Biomass Carrying Capacity
            
            growth_ratio_h = anc[0] / (st[0] + 1e-4) # Projected Height Growth Factor
            growth_ratio_a = anc[1] / (st[1] + 1e-4) # Projected Biomass Growth Factor
            h_non_neg = max(0.0, float(st[0]))
            sdi = float(st[1]) / (h_non_neg ** 1.6 + 1e-4)      # Reineke Stand Density Index
            prod_proxy = st[4] * st[3]               # Photosynthetic Capacity (GPP * LAI)
            resp_ratio = st[6] / (st[4] + 1e-4)      # Stand Respiration Burden (Rh / GPP)
            
            # Age stage indicators
            is_young = 1.0 if age <= 30 else 0.0
            is_mid = 1.0 if 30 < age <= 100 else 0.0
            is_old = 1.0 if age > 100 else 0.0
            
            # Non-linear age features
            age_f = [float(age), np.log1p(age), np.sqrt(age), age / 500.0, is_young, is_mid, is_old]
            
            sample_feat = np.concatenate([
                age_f,
                st,
                anc,
                anc_delta,
                [cue, bio_dens, soil_turn, rel_h, rel_a, growth_ratio_h, growth_ratio_a, sdi, prod_proxy, resp_ratio],
                c_feat
            ])
            rows.append(sample_feat)
            
    return np.array(rows, dtype=np.float32)


def load_full_dataset(npz_path: str = "carbon_globe/data_global/res_train4_test8.npz"):
    """
    Loads all 4,225 global sites (3,373 train + 852 validation) from the benchmark NPZ.
    Returns:
    - x_all: (4225, 40, 12, 136)
    - y0_all: (4225, 15, 7)
    - y40_all: (4225, 15, 7)
    """
    if not os.path.exists(npz_path):
        raise FileNotFoundError(f"Dataset {npz_path} not found!")
        
    data = np.load(npz_path)
    x_tr = data['x_train'].astype(np.float32)
    y_tr_raw = data['y_train'].astype(np.float32)
    x_val = data['x_test'].astype(np.float32)
    y_val_raw = data['y_test'].astype(np.float32)
    
    # Combine sites
    x_all = np.concatenate([x_tr, x_val], axis=0) # (4225, 40, 12, 136)
    
    # Transpose from (15, N_sites, 41, 12, 7) to (N_sites, 15, 41, 12, 7)
    y_tr_t = np.transpose(y_tr_raw, (1, 0, 2, 3, 4))
    y_val_t = np.transpose(y_val_raw, (1, 0, 2, 3, 4))
    
    y0_tr = y_tr_t[:, :, 0, :, :].mean(axis=2)   # (3373, 15, 7)
    y40_tr = y_tr_t[:, :, 40, :, :].mean(axis=2) # (3373, 15, 7)
    
    y0_val = y_val_t[:, :, 0, :, :].mean(axis=2)   # (852, 15, 7)
    y40_val = y_val_t[:, :, 40, :, :].mean(axis=2) # (852, 15, 7)
    
    y0_all = np.concatenate([y0_tr, y0_val], axis=0)   # (4225, 15, 7)
    y40_all = np.concatenate([y40_tr, y40_val], axis=0) # (4225, 15, 7)
    
    return x_all, y0_all, y40_all
