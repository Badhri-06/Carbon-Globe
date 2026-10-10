import os
import numpy as np
import pandas as pd
from src.config import compute_competition_metric, HEIGHT_MEAN, AGB_MEAN

def load_validation_splits(val_csv_path="carbon_globe/val.csv"):
    """
    Loads site indices for validation from val.csv.
    """
    if not os.path.exists(val_csv_path):
        raise FileNotFoundError(f"Validation file {val_csv_path} not found.")
    
    val_df = pd.read_csv(val_csv_path, header=None)
    val_sites = val_df.iloc[:, 0].values.astype(int)
    return val_sites


def evaluate_rollout(y_true_sequence, y_pred_sequence):
    """
    Evaluates long-horizon 40-step rollout performance.
    
    y_true_sequence: (N_samples, 41, 7) or (N_samples, 40, 7)
    y_pred_sequence: (N_samples, 41, 7) or (N_samples, 40, 7)
    
    Computes:
    - One-step MSE
    - Year-40 competition normalized metric
    """
    # Extract Year 40 (last time index)
    y_true_y40 = y_true_sequence[:, -1, :] # (N_samples, 7)
    y_pred_y40 = y_pred_sequence[:, -1, :] # (N_samples, 7)
    
    y_true_height = y_true_y40[:, 0]
    y_pred_height = y_pred_y40[:, 0]
    
    y_true_agb = y_true_y40[:, 1]
    y_pred_agb = y_pred_y40[:, 1]
    
    metrics = compute_competition_metric(y_true_height, y_pred_height, y_true_agb, y_pred_agb)
    
    # Compute step-by-step MSE across all 40 steps for height and agb
    step_mse_height = np.mean(((y_pred_sequence[:, :, 0] - y_true_sequence[:, :, 0]) / HEIGHT_MEAN) ** 2, axis=0)
    step_mse_agb    = np.mean(((y_pred_sequence[:, :, 1] - y_true_sequence[:, :, 1]) / AGB_MEAN) ** 2, axis=0)
    
    metrics["step_mse_height"] = step_mse_height.tolist()
    metrics["step_mse_agb"] = step_mse_agb.tolist()
    metrics["year1_score"] = float(0.5 * (step_mse_height[0] + step_mse_agb[0]))
    metrics["year20_score"] = float(0.5 * (step_mse_height[19] + step_mse_agb[19]))
    metrics["year40_score"] = metrics["score"]
    
    return metrics


def save_validation_report(model_name, metrics, output_path="reports/validation_results.md"):
    """
    Appends or creates validation summary report.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    content = f"""
## Model Validation: {model_name}
- **Year-40 Competition Normalized Score**: `{metrics['score']:.6f}`
- **Year-40 Height Normalized MSE**: `{metrics['mse_height']:.6f}` (Relative RMSE: `{metrics['rmse_height_rel']:.4f}`)
- **Year-40 AGB Normalized MSE**: `{metrics['mse_agb']:.6f}` (Relative RMSE: `{metrics['rmse_agb_rel']:.4f}`)
- **Year-1 Trajectory Score**: `{metrics.get('year1_score', 0.0):.6f}`
- **Year-20 Trajectory Score**: `{metrics.get('year20_score', 0.0):.6f}`

---
"""
    with open(output_path, "a") as f:
        f.write(content)
    print(f"Validation report saved to {output_path}")
