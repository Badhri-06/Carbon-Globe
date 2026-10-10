import numpy as np
from scipy.optimize import minimize
from src.config import compute_competition_metric, HEIGHT_MEAN, AGB_MEAN

class EnsemblePredictor:
    """
    Ensemble model that optimizes weights to blend out-of-fold predictions
    from multiple candidate models (LightGBM, XGBoost, CatBoost, PyTorch NN).
    """
    def __init__(self, model_names=None):
        self.model_names = model_names or []
        self.weights_height = None
        self.weights_agb = None

    def fit_weights(self, preds_height_list, y_true_height, preds_agb_list, y_true_agb):
        """
        preds_height_list: list of (N_samples,) arrays from each candidate model
        preds_agb_list: list of (N_samples,) arrays from each candidate model
        """
        num_models = len(preds_height_list)
        if num_models == 1:
            self.weights_height = np.array([1.0])
            self.weights_agb = np.array([1.0])
            return

        H_mat = np.column_stack(preds_height_list)
        A_mat = np.column_stack(preds_agb_list)

        def loss_height(w):
            w = w / np.sum(w)
            pred = H_mat @ w
            return np.mean(((pred - y_true_height) / HEIGHT_MEAN) ** 2)

        def loss_agb(w):
            w = w / np.sum(w)
            pred = A_mat @ w
            return np.mean(((pred - y_true_agb) / AGB_MEAN) ** 2)

        init_w = np.ones(num_models) / num_models
        bounds = [(0.0, 1.0) for _ in range(num_models)]
        constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0})

        res_h = minimize(loss_height, init_w, method='SLSQP', bounds=bounds, constraints=constraints)
        res_a = minimize(loss_agb, init_w, method='SLSQP', bounds=bounds, constraints=constraints)

        self.weights_height = res_h.x / np.sum(res_h.x)
        self.weights_agb = res_a.x / np.sum(res_a.x)

        print("\nOptimized Ensemble Weights (Height):", dict(zip(self.model_names, self.weights_height)))
        print("Optimized Ensemble Weights (AGB):   ", dict(zip(self.model_names, self.weights_agb)))

    def predict(self, preds_height_list, preds_agb_list, ages=None):
        H_mat = np.column_stack(preds_height_list)
        A_mat = np.column_stack(preds_agb_list)

        opt_height = H_mat @ self.weights_height
        opt_agb = A_mat @ self.weights_agb
        return opt_height, opt_agb
