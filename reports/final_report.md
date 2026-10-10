# CarbonGlobe AI Emulation Challenge: Technical & Validation Report

**Competition**: IEEE BigData Cup 2026 — AI Emulation Challenge: Global-Scale Land Ecosystem Forecasting  
**Author / Team**: Badhri Narayanan M ([@Badhri-06](https://github.com/Badhri-06)), Bavin ([@Bavin22](https://github.com/Bavin22)), Aswitha ([@aswitha570-ux](https://github.com/aswitha570-ux))  
**Validation Benchmark**: 5-Fold Cross-Validation (< 0.010 Target Achieved: **`0.001393`**)  
**Submission Status**: Verified (185,130 rows, formatted, scaled, and verified)  

---

## 1. Executive Summary

This report documents the machine learning, ecological modeling, and multi-scale spatiotemporal architecture developed for the **IEEE BigData Cup 2026 AI Emulation Challenge**.

The challenge requires forecasting forest canopy height and aboveground biomass (AGB) at Year 40 across **6,171 global sites** and **15 seed forest stand ages** under two distinct climate projection pathways: **SSP126** (sustainable, low-emissions) and **SSP585** (fossil-fueled, high-emissions).

### Key Performance Highlights:
- **Baseline Heuristic Score**: `~0.181 – 0.300+` Normalized MSE (due to static global gain assumptions and unanchored regressions)
- **Production Model 5-Fold Cross-Validation Score**: **`0.001393`** (Strictly beats the `< 0.010` target by **86.1%**!)
  - **Year-40 Height Normalized MSE**: `0.001241`
  - **Year-40 AGB Normalized MSE**: `0.001545`
  - **Height Fit Fidelity $R^2$**: **`0.9982`**
  - **AGB Fit Fidelity $R^2$**: **`0.9991`**
- **Simulation Domain Models (4,225 Global Sites)**: 5-Fold GroupKFold CV Score: **`0.032968`** (< 0.050)
- **Mean Calibration**:
  - `height`: Mean = `0.9356`, Min = `0.0000`, Max = `2.5593`
  - `agb`: Mean = `0.9336`, Min = `0.0000`, Max = `6.9167`
- **Verified Output**: `outputs/submission.csv` & `outputs/submission.zip` (185,130 rows, 0 nulls, strictly non-negative, identical format and row order to `sample_submission.csv`)

---

## 2. Methodology & Scientific Architecture

The core challenge in long-horizon forest ecosystem forecasting is modeling both **developmental stand aging** (ontogenetic growth from seed age $A$ to target age $A+40$) and **climate-driven environmental sensitivity** (multi-decade warming, precipitation seasonality, drought, and CO2 fertilization).

```
                         [40-Year Climate Drivers (X)]
                                      │
                         [Initial Stand State (Y0)]
                                      │
               ┌──────────────────────┴──────────────────────┐
               ▼                                             ▼
     [Empirical Physical Anchor]                  [Multi-Variate Climate PCA]
   Monotonic PCHIP stand development              10 Orthogonal Climate Modes
       (Preserves ontogenetic growth)                 (Captures >95% variance)
               │                                             │
               └──────────────────────┬──────────────────────┘
                                      ▼
                   [5-Fold CV Calibrated Stand Model]
                 Gradient Boosted Decision Tree Ensemble
                   Predicts Scaled Delta Across All Folds
                       CV Score: 0.00139 (< 0.010)
                                      │
                         [outputs/submission.csv]
```

### 2.1 Component 1: Monotonic PCHIP Physical Stand Allometric Anchor
Forest stand age advances linearly: at Year 40, a stand seeded at age $A$ reaches target age $A_{\text{target}} = \min(A + 40, 500)$.  
Because tree growth curves are monotonically increasing and allometrically bounded, we fit a monotonic cubic Hermite spline (**PCHIP**) along the stand age axis:
$$Y_{0,\text{anchor}}(A_{\text{target}}) = \text{PCHIP}\left(A_{\text{target}}, \; \text{SeedAges}, \; Y_0\right)$$

This anchors the baseline prediction in the site's empirical allometric trajectory, avoiding unconstrained extrapolation.

### 2.2 Component 2: 10-Component Standardized Multi-Variate Climate PCA
Across the 136 climate and environmental drivers in $X$, individual variables exhibit strong spatial collinearity. We standardize and compute orthogonal principal components across the multi-decade site climate summaries:
$$\mathbf{z}_{\text{climate}} = \mathbf{V}_{10}^\top \mathbf{\Sigma}^{-1} \left(\bar{\mathbf{x}} - \boldsymbol{\mu}\right)$$
This retains $>95\%$ of total climate variance while eliminating collinearity and high-frequency noise.

### 2.3 Component 3: Ecological Biophysical Interaction Indices
We construct domain-specific ecological indices from initial stand states:
- **Reineke's Stand Density Index (SDI)**: $\text{SDI} = \frac{\text{AGB}}{\text{Height}^{1.6} + 10^{-4}}$ (quantifies stand crowding and self-thinning limits)
- **Carbon Use Efficiency (CUE)**: $\text{CUE} = \frac{\text{NPP}}{\text{GPP} + 10^{-4}}$
- **Photosynthetic Capacity Proxy**: $\text{GPP} \times \text{LAI}$
- **Respiration Burden**: $\frac{\text{Rh}}{\text{GPP} + 10^{-4}}$
- **Soil Carbon Turnover**: $\frac{\text{Rh}}{\text{Soil} + 10^{-4}}$
- **Water Deficit & Aridity**: Potential evapotranspiration demand minus precipitation

### 2.4 Component 4: 5-Fold Cross-Validated Gradient Boosted Regressors
The model directly optimizes the competition normalized loss metric:
$$\Delta Y_{\text{scaled}} = \left[\frac{Y_{40,h} - Y_{0,\text{anchor},h}}{10.90645}, \; \frac{Y_{40,a} - Y_{0,\text{anchor},a}}{3.39567}\right]$$

By training across 5 folds and averaging predictions across fold models, the architecture eliminates point variance and decision-boundary jitter:
- **5-Fold Cross-Validation Score**: **`0.001393`** (< 0.010)
- **Height Normalized MSE**: **`0.001241`**
- **AGB Normalized MSE**: **`0.001545`**

---

## 3. Validation & Benchmark Comparison

| Model Architecture | Role | Benchmark Metric | Target Passed? |
|---|---|:---:|:---:|
| **Physical PCHIP Baseline** | Stand Maturation Anchor | 5-Fold CV: `0.180893` | ❌ Unoptimized |
| **Simulation LightGBM Model** | 4,225 Simulation Sites | 5-Fold CV: `0.032968` | ✅ Passed (< 0.05) |
| **Simulation XGBoost Model** | 4,225 Simulation Sites | 5-Fold CV: `0.034985` | ✅ Passed (< 0.05) |
| **Calibrated Stand Growth Model** | Production Model Deployment | **5-Fold CV: `0.001393`** | **✅ PASSED (< 0.010)** |

---

## 4. Automated Submission Verification

The final submission file `outputs/submission.csv` was verified using `src/check_submission.py`:
- **Total Rows**: Exactly **185,130** rows ($2 \text{ scenarios} \times 6,171 \text{ sites} \times 15 \text{ ages}$).
- **Columns**: `id`, `height`, `agb`
- **ID Sequence**: Identical row-by-row match with `competition_data/sample_submission.csv`
- **Missing / NaN / Inf**: **0**
- **Physical Non-negativity**: All values bounded $\ge 0$
- **Target Distribution Statistics (Pre-scaled)**:
  - `height`: Mean = `0.9356`, Min = `0.0000`, Max = `2.5593`
  - `agb`: Mean = `0.9336`, Min = `0.0000`, Max = `6.9167`

---

## 5. Codebase Layout

```
Carbon Globe/
│
├── train_all_models.py          # Master executable pipeline (Trains empirical + loads production model + generates verified submission)
├── README.md                    # Project overview & execution guide
│
├── src/                         # Core modular architecture
│   ├── config.py                # Competition constants, normalization factors, metric loss functions
│   ├── data_loader.py           # PCHIP anchor calculation, 10-PCA drivers, SDI features, full loader
│   ├── models/
│   │   └── tree_models.py       # AnchorDeltaTreeModel & CalibratedStandGrowthModel
│   ├── ensemble.py              # Production ensemble predictor
│   ├── inference.py             # Inference generator for test_ssp126 & test_ssp585
│   ├── validation.py            # Validation metric reporter & Markdown generator
│   ├── train_experiment.py      # Experiment tracker logging to CSV
│   └── check_submission.py      # Automated 8-point submission verifier
│
├── models/                      # Saved trained model artifacts
│   └── calibrated_stand_growth_model.joblib # Persisted 5-Fold CV production model
│
├── reports/                     # Formal technical reports
│   ├── final_report.md          # Comprehensive technical report (this document)
│   ├── validation_results.md    # Detailed per-model validation breakdown
│   ├── experiment_summary.csv   # Tabular experimental ledger
│   ├── dataset_report.md        # Dataset schema and statistics report
│   ├── test_data_report.md      # Test set dimensions and scenario report
│   └── hardware_report.md       # Hardware compute specifications
│
├── outputs/                     # Final competition submission files
│   ├── submission.csv           # Final verified submission (185,130 rows)
│   └── submission.zip           # Compressed bundle ready for direct upload
│
├── competition_data/            # Official test sets & sample submission
└── carbon_globe/                # Hugging Face global benchmark data
```

---

## 6. How to Reproduce

To reproduce the entire pipeline end-to-end:
```bash
python train_all_models.py
```
*(Runs in ~115 seconds, evaluates simulation domain models, deploys calibrated 5-Fold CV model with score = 0.00139, and produces `outputs/submission.csv` and `outputs/submission.zip`).*
