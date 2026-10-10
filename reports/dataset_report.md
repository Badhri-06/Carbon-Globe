# CarbonGlobe Dataset Report (Phase 3)

**Date**: 2026-10-07
**Source**: Hugging Face Repository (`zhwang1/CarbonGlobe`)

## Summary of Downloaded Dataset Files

| Local Relative Path | Remote File | Size | Description |
|---|---|---|---|
| `carbon_globe/README.md` | `README.md` | 8.8 KB | NeurIPS 2025 CarbonGlobe benchmark documentation |
| `carbon_globe/readme.txt` | `readme.txt` | 1.5 KB | Dataset schema and directory mapping |
| `carbon_globe/train.csv` | `train.csv` | 20.6 KB | 3,035 global training site indices |
| `carbon_globe/val.csv` | `val.csv` | 2.3 KB | 338 global validation site indices |
| `carbon_globe/test.csv` | `test.csv` | 345.1 KB | Global test site indices |
| `carbon_globe/data_stats/data_stats.npz` | `data_stats/data_stats.npz` | 4.2 KB | Feature & target global mean and standard deviation |
| `carbon_globe/data_stats/age_triplet.npz` | `data_stats/age_triplet.npz` | 2.5 KB | Seed forest ages & age-dependent state statistics |
| `carbon_globe/data_stats/mask2d.npy` | `data_stats/mask2d.npy` | 1.98 MB | Spatial 2D grid mapping mask (0.5° global resolution) |
| `carbon_globe/data_global/res_train4_test8.npz` | `data_global/res_train4_test8.npz` | 3,769.47 MB | Full 40-year multi-site environmental forcing and trajectories |

## Data Schemas & Features

### 1. Environmental Driver Features ($X$)
- **Monthly sequence shape**: `(N_sites, 40, 12, 136)`
- **Number of drivers**: 136 environmental covariates (meteorological forcing, radiation, CO2, soil properties, atmospheric pressure, precipitation, temperature).
- **Normalizing Statistics (`data_stats.npz`)**:
  - `x_mean`: shape `(136,)`
  - `x_std`: shape `(136,)`

### 2. Ecosystem State Targets ($Y$)
- **Target Ordering**: `['height', 'agb', 'soil', 'lai', 'gpp', 'npp', 'rh']`
- **Number of target state variables**: 7
- **Normalizing Statistics (`data_stats.npz`)**:
  - `y_mean`: shape `(7,)`
  - `y_std`: shape `(7,)`

### 3. Seed Forest Ages
- **15 Seed Forest Ages**: `[1, 10, 20, 30, 50, 70, 100, 150, 200, 250, 300, 350, 400, 450, 500]`
- **Linear growth trajectory**: Forest age at step $t$ ($t \in [0..39]$) equals $\text{seed\_age} + t$.

### 4. Official Competition Normalization Constants
$$\text{height}_{\text{submission}} = \frac{\text{height}_{\text{pred}}}{10.90645}$$
$$\text{agb}_{\text{submission}} = \frac{\text{agb}_{\text{pred}}}{3.39567}$$
