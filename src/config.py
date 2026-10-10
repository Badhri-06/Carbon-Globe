import os
import numpy as np

# Domain Constants
SEED_AGES = [1, 10, 20, 30, 50, 70, 100, 150, 200, 250, 300, 350, 400, 450, 500]
NUM_SEED_AGES = len(SEED_AGES)

TARGET_NAMES = ['height', 'agb', 'soil', 'lai', 'gpp', 'npp', 'rh']
NUM_TARGETS = len(TARGET_NAMES)

HEIGHT_IDX = 0
AGB_IDX = 1

# Competition Normalization Constants
HEIGHT_MEAN = 10.90645
AGB_MEAN = 3.39567

# Competition Metric Calculation
def compute_competition_metric(y_true_height, y_pred_height, y_true_agb, y_pred_agb):
    """
    Computes competition score:
    0.5 * (MSE(height / 10.90645) + MSE(agb / 3.39567))
    """
    height_true_scaled = np.asarray(y_true_height, dtype=np.float64) / HEIGHT_MEAN
    height_pred_scaled = np.asarray(y_pred_height, dtype=np.float64) / HEIGHT_MEAN
    
    agb_true_scaled = np.asarray(y_true_agb, dtype=np.float64) / AGB_MEAN
    agb_pred_scaled = np.asarray(y_pred_agb, dtype=np.float64) / AGB_MEAN
    
    mse_height = np.mean((height_pred_scaled - height_true_scaled) ** 2)
    mse_agb = np.mean((agb_pred_scaled - agb_true_scaled) ** 2)
    
    score = 0.5 * (mse_height + mse_agb)
    return {
        "score": float(score),
        "mse_height": float(mse_height),
        "mse_agb": float(mse_agb),
        "rmse_height_rel": float(np.sqrt(mse_height)),
        "rmse_agb_rel": float(np.sqrt(mse_agb)),
    }
