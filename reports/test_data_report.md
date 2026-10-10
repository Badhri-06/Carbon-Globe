# Test Data Inspection Report (Phase 2)

**Date**: 2026-10-07
**Project**: IEEE BigData Cup 2026 AI Emulation Challenge (CarbonGlobe)

## Overview of Files in `competition_data/`

| Filename | Size | Purpose |
|---|---|---|
| `README.md` | ~2.9 KB | Official competition documentation |
| `sites_ssp.csv` | ~30 KB | 6,171 site indices for SSP scenarios |
| `sample_submission.csv` | 4.30 MB | Authoritative submission format and row order |
| `test_ssp126.npz` | 1,539.20 MB | Test inputs for SSP126 (Low Emissions) scenario |
| `test_ssp585.npz` | 1,539.20 MB | Test inputs for SSP585 (High Emissions) scenario |

## Scenario Array Specifications

### `test_ssp126.npz` & `test_ssp585.npz`

Each NPZ container holds two key NumPy arrays:

1. **`test_x`**: Environmental Forcing
   - **Shape**: `(6171, 40, 12, 136)`
   - **Dtype**: `float32`
   - **Dimensions**: `(sites=6171, years=40, months=12, drivers=136)`
   - **Value Range (SSP126)**: `[-26.0633, 3,391,543.2500]` (No NaNs)
   - **Value Range (SSP585)**: `[-26.0633, 3,391,543.2500]` (No NaNs)

2. **`test_y0`**: Initial Ecosystem State (Year 0)
   - **Shape**: `(6171, 15, 7)`
   - **Dtype**: `float32`
   - **Dimensions**: `(sites=6171, seed_ages=15, state_variables=7)`
   - **Value Range (SSP126)**: `[-0.9009, 48.9831]` (No NaNs)
   - **Value Range (SSP585)**: `[-0.9009, 49.2615]` (No NaNs)

## Domain Specifications & Variable Mappings

### Seed Forest Ages (15 values, axis 1 of `test_y0`)
`[1, 10, 20, 30, 50, 70, 100, 150, 200, 250, 300, 350, 400, 450, 500]`

### Ecosystem State Variables (7 targets, axis 2 of `test_y0`)
1. `height` (Canopy height)
2. `agb` (Aboveground biomass)
3. `soil` (Soil carbon)
4. `lai` (Leaf area index)
5. `gpp` (Gross primary productivity)
6. `npp` (Net primary productivity)
7. `rh` (Heterotrophic respiration)

## Submission Format & Row Ordering

- Total rows: `2 scenarios x 6,171 sites x 15 seed ages = 185,130 rows`
- Columns: `['id', 'height', 'agb']`
- ID pattern: `{scenario}_{site}_{seed_age}` (e.g., `ssp126_0_1`, `ssp585_6170_500`)
- Row sequence:
  1. `ssp126` for sites `0..6170`, each site iterated through seed ages `1..500`
  2. `ssp585` for sites `0..6170`, each site iterated through seed ages `1..500`

## Normalization & Competition Metric

### Mandated Target Scaling
Before building `submission.csv`, predicted Year-40 targets must be divided by their global means:
$$\text{height}_{\text{sub}} = \frac{\text{predicted\_height}}{10.90645}$$
$$\text{agb}_{\text{sub}} = \frac{\text{predicted\_agb}}{3.39567}$$

### Evaluation Metric
$$\text{Score} = \frac{1}{2} \left( \text{MSE}\left(\text{height}_{\text{sub}}, \text{true}_{\text{height\_sub}}\right) + \text{MSE}\left(\text{agb}_{\text{sub}}, \text{true}_{\text{agb\_sub}}\right) \right)$$
- Optimizing this metric is the primary goal for local validation.
