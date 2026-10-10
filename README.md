# CarbonGlobe AI Emulation Challenge (IEEE BigData Cup 2026)

Global-Scale Land Ecosystem Forecasting: 40-Year Canopy Height & Aboveground Biomass Emulation.

---

## 📌 Project Overview

This repository contains the complete, production-grade machine learning solution for the **IEEE BigData Cup 2026 AI Emulation Challenge**.

The challenge requires predicting global ecosystem state variables (**canopy height** and **aboveground biomass**) across **6,171 sites** and **15 seed forest ages** over a **40-year horizon** under **SSP126** and **SSP585** climate projections.

### 🏆 Key Validation & Optimization Highlights:
- **Baseline Heuristic**: `~0.181 – 0.300+` Normalized MSE
- **5-Fold Cross-Validation Score**: **`0.001393`** (Target `< 0.010` Passed by **86.1%**!)
  - Height Normalized MSE: `0.001241`
  - AGB Normalized MSE: `0.001545`
  - Height $R^2$: `0.9982`
  - AGB $R^2$: `0.9991`
- **Simulation Domain Models**: 5-Fold GroupKFold CV Score: **`0.032968`** (< 0.050)
- **Calibrated Multi-Scale Architecture**: PCHIP monotonic stand trajectories + 10-Component Climate PCA + Reineke Stand Density Index.
- **Total Runtime**: **~115 seconds**
- **Final Submission**: `outputs/submission.csv` & `outputs/submission.zip` (185,130 rows, verified)

---

## 📁 Repository Structure

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
│   ├── final_report.md          # Comprehensive technical report (Methodology, Math, Results)
│   ├── validation_results.md    # Detailed per-model validation breakdown
│   ├── experiment_summary.csv   # Tabular experimental ledger
│   ├── dataset_report.md        # Dataset schema and statistics report
│   ├── test_data_report.md      # Test set dimensions and scenario report
│   └── hardware_report.md       # Hardware compute specifications
│
├── outputs/                     # Final competition submission files
│   ├── submission.csv           # Final verified submission (185,130 rows)
│   └── submission.zip           # Compressed bundle ready for upload
│
├── competition_data/            # Official test sets & sample submission
└── carbon_globe/                # Hugging Face global benchmark data
```

---

## 🚀 Execution & Verification

### Run End-to-End Pipeline (~115s):
```bash
python train_all_models.py
```

### Verify Submission Integrity:
```bash
python -c "from src.check_submission import check_submission_file; check_submission_file('outputs/submission.csv')"
```

See [reports/final_report.md](file:///c:/Users/badhr/Desktop/Carbon%20Globe/reports/final_report.md) for full scientific formulations, mathematical proofs, and architectural details.
