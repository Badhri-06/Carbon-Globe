import os
import shutil
import zipfile
import numpy as np
import pandas as pd
from src.config import SEED_AGES, HEIGHT_MEAN, AGB_MEAN
from src.data_loader import extract_site_climate_features, compute_pchip_anchor, build_sample_feature_matrix

SUBMISSION_PATH = "outputs/submission.csv"
SAMPLE_SUB_PATH = "competition_data/sample_submission.csv"

def run_competition_inference(models_dict, ensemble_obj, output_csv=SUBMISSION_PATH):
    """
    Runs model inference on competition test data (SSP126 and SSP585).
    Produces year-40 normalized height and agb predictions for all 185,130 rows.
    """
    print("==================================================")
    print("      COMPETITION INFERENCE PIPELINE              ")
    print("==================================================")
    
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    scenarios = ["ssp126", "ssp585"]
    model_names = ensemble_obj.model_names
    
    # Store predictions in lookup dictionary: (scenario, site_idx, seed_age) -> (h_scaled, a_scaled)
    preds_lookup = {}
    
    for scenario in scenarios:
        npz_path = f"competition_data/test_{scenario}.npz"
        if not os.path.exists(npz_path):
            raise FileNotFoundError(f"Test file {npz_path} not found!")
            
        print(f"\n[Scenario] Processing {scenario.upper()} from {npz_path}...")
        test_data = np.load(npz_path)
        test_x = test_data["test_x"].astype(np.float32)   # (6171, 40, 12, 136)
        test_y0 = test_data["test_y0"].astype(np.float32) # (6171, 15, 7)
        N_sites = test_x.shape[0]
        
        # 1. Physical PCHIP Baseline
        print(f"  Computing vectorized PCHIP physical stand trajectory for {N_sites} sites...")
        pchip_anc = compute_pchip_anchor(test_y0) # (6171, 15, 7)
        
        # 2. Extract multi-decade climate features
        print("  Extracting climate summary features...")
        site_feats = extract_site_climate_features(test_x) # (6171, N_feats)
        
        # 3. Build sample feature matrix
        X_test = build_sample_feature_matrix(site_feats, test_y0, pchip_anc) # (6171 * 15, N_total_feats)
        Y0_anc_2d = np.column_stack([pchip_anc[:, :, 0].reshape(-1), pchip_anc[:, :, 1].reshape(-1)])
        
        # 4. Predict with candidate models
        h_preds_list = []
        a_preds_list = []
        for name in model_names:
            m = models_dict[name]
            p_m = m.predict(X_test, Y0_anc_2d)
            h_preds_list.append(p_m[:, 0])
            a_preds_list.append(p_m[:, 1])
            
        # 5. Blend using learned optimal age-adaptive ensemble weights
        sample_ages = np.tile(SEED_AGES, N_sites)
        pred_h_raw, pred_a_raw = ensemble_obj.predict(h_preds_list, a_preds_list, ages=sample_ages)
        pred_h_raw = np.maximum(0.0, pred_h_raw)
        pred_a_raw = np.maximum(0.0, pred_a_raw)
        
        # 6. Apply mandatory competition scaling
        pred_h_scaled = pred_h_raw / HEIGHT_MEAN
        pred_a_scaled = pred_a_raw / AGB_MEAN
        
        sample_idx = 0
        for s_idx in range(N_sites):
            for a_idx, age in enumerate(SEED_AGES):
                preds_lookup[(scenario, s_idx, age)] = (
                    float(pred_h_scaled[sample_idx]),
                    float(pred_a_scaled[sample_idx])
                )
                sample_idx += 1
                
    # 7. Format exactly according to sample_submission.csv
    print(f"\nBuilding final submission DataFrame matching {SAMPLE_SUB_PATH}...")
    sample_sub = pd.read_csv(SAMPLE_SUB_PATH)
    submission_rows = []
    
    for row_id in sample_sub['id']:
        parts = row_id.split('_')
        scen, site_id, age = parts[0], int(parts[1]), int(parts[2])
        h_val, a_val = preds_lookup[(scen, site_id, age)]
        submission_rows.append({
            'id': row_id,
            'height': h_val,
            'agb': a_val
        })
        
    sub_df = pd.DataFrame(submission_rows)
    sub_df.to_csv(output_csv, index=False)
    print(f"Submission saved to {output_csv} (Total rows: {len(sub_df):,})")
    
    # Auto-compress submission.zip
    zip_path = os.path.splitext(output_csv)[0] + ".zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(output_csv, arcname=os.path.basename(output_csv))
    print(f"Compressed submission saved to {zip_path}")
    
    return output_csv
