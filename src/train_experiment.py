import os
import time
import json
import numpy as np
import pandas as pd

EXPERIMENT_CSV = "reports/experiment_summary.csv"
MODELS_DIR = "models"
EXPERIMENTS_DIR = "experiments"

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(EXPERIMENTS_DIR, exist_ok=True)
os.makedirs("reports", exist_ok=True)

def log_experiment(experiment_name, model_type, features_used, hyperparams, val_score, height_err, agb_err, train_time):
    """
    Logs experiment metrics to reports/experiment_summary.csv
    """
    row = {
        "experiment": experiment_name,
        "model": model_type,
        "features": features_used,
        "hyperparameters": json.dumps(hyperparams),
        "validation_score": f"{val_score:.6f}",
        "height_error": f"{height_err:.6f}",
        "agb_error": f"{agb_err:.6f}",
        "training_time": f"{train_time:.2f}s"
    }
    df_row = pd.DataFrame([row])
    if not os.path.exists(EXPERIMENT_CSV):
        df_row.to_csv(EXPERIMENT_CSV, index=False)
    else:
        df_row.to_csv(EXPERIMENT_CSV, mode="a", header=False, index=False)
    print(f"Logged experiment {experiment_name} to {EXPERIMENT_CSV}")
