import numpy as np
import lightgbm as lgb
import xgboost as xgb
from catboost import CatBoostRegressor
from sklearn.model_selection import KFold
from src.config import HEIGHT_MEAN, AGB_MEAN

class AnchorDeltaTreeModel:
    """
    Anchor Delta Tree Predictor using 5-Fold GroupKFold Cross Validation.
    Supports model_type in ["lightgbm", "xgboost", "catboost"].
    
    Directly optimizes competition scaled loss:
    delta_h_scaled = (y40_h - anchor_h) / 10.90645
    delta_a_scaled = (y40_a - anchor_a) / 3.39567
    """
    def __init__(self, model_type="lightgbm", n_estimators=450, learning_rate=0.03, max_depth=6, random_state=42):
        self.model_type = model_type.lower()
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.random_state = random_state
        
        self.fold_models_h = []
        self.fold_models_a = []
        self.oof_preds_h = None
        self.oof_preds_a = None

    def fit_cv(self, X_mat, Y0_anchor_mat, Delta_Y_mat, site_ids, n_splits=5):
        """
        X_mat: (N_samples, N_features)
        Y0_anchor_mat: (N_samples, 2) [anchor_h, anchor_a] (unscaled)
        Delta_Y_mat: (N_samples, 2) [delta_h, delta_a] (unscaled)
        site_ids: (N_samples,) site index for GroupKFold
        """
        N_samples = X_mat.shape[0]
        site_uniques = np.unique(site_ids)
        kf = KFold(n_splits=n_splits, shuffle=True, random_state=self.random_state)
        
        self.oof_preds_h = np.zeros(N_samples, dtype=np.float32)
        self.oof_preds_a = np.zeros(N_samples, dtype=np.float32)
        
        self.fold_models_h = []
        self.fold_models_a = []
        
        # Scale deltas to align loss function directly with competition metric
        delta_h_scaled = Delta_Y_mat[:, 0] / HEIGHT_MEAN
        delta_a_scaled = Delta_Y_mat[:, 1] / AGB_MEAN
        
        anchor_h = Y0_anchor_mat[:, 0]
        anchor_a = Y0_anchor_mat[:, 1]
        
        for fold, (tr_sites_idx, val_sites_idx) in enumerate(kf.split(site_uniques)):
            tr_mask = np.isin(site_ids, site_uniques[tr_sites_idx])
            val_mask = np.isin(site_ids, site_uniques[val_sites_idx])
            
            X_tr, X_val = X_mat[tr_mask], X_mat[val_mask]
            
            if self.model_type == "lightgbm":
                m_h = lgb.LGBMRegressor(
                    n_estimators=self.n_estimators,
                    learning_rate=self.learning_rate,
                    num_leaves=63,
                    subsample=0.85,
                    colsample_bytree=0.80,
                    random_state=self.random_state + fold,
                    n_jobs=-1,
                    verbose=-1
                )
                m_a = lgb.LGBMRegressor(
                    n_estimators=self.n_estimators,
                    learning_rate=self.learning_rate,
                    num_leaves=63,
                    subsample=0.85,
                    colsample_bytree=0.80,
                    random_state=self.random_state + fold + 10,
                    n_jobs=-1,
                    verbose=-1
                )
            elif self.model_type == "xgboost":
                m_h = xgb.XGBRegressor(
                    n_estimators=self.n_estimators,
                    learning_rate=self.learning_rate,
                    max_depth=self.max_depth,
                    subsample=0.85,
                    colsample_bytree=0.85,
                    tree_method="hist",
                    random_state=self.random_state + fold,
                    n_jobs=-1,
                    verbosity=0
                )
                m_a = xgb.XGBRegressor(
                    n_estimators=self.n_estimators,
                    learning_rate=self.learning_rate,
                    max_depth=self.max_depth,
                    subsample=0.85,
                    colsample_bytree=0.85,
                    tree_method="hist",
                    random_state=self.random_state + fold + 10,
                    n_jobs=-1,
                    verbosity=0
                )
            elif self.model_type == "catboost":
                m_h = CatBoostRegressor(
                    iterations=self.n_estimators,
                    learning_rate=self.learning_rate,
                    depth=self.max_depth,
                    random_seed=self.random_state + fold,
                    verbose=0
                )
                m_a = CatBoostRegressor(
                    iterations=self.n_estimators,
                    learning_rate=self.learning_rate,
                    depth=self.max_depth,
                    random_seed=self.random_state + fold + 10,
                    verbose=0
                )
            else:
                raise ValueError(f"Unknown model_type {self.model_type}")
                
            m_h.fit(X_tr, delta_h_scaled[tr_mask])
            m_a.fit(X_tr, delta_a_scaled[tr_mask])
            
            # Predict unscaled physical targets
            pred_del_h_val = m_h.predict(X_val) * HEIGHT_MEAN
            pred_del_a_val = m_a.predict(X_val) * AGB_MEAN
            
            self.oof_preds_h[val_mask] = np.maximum(0.0, anchor_h[val_mask] + pred_del_h_val)
            self.oof_preds_a[val_mask] = np.maximum(0.0, anchor_a[val_mask] + pred_del_a_val)
            
            self.fold_models_h.append(m_h)
            self.fold_models_a.append(m_a)

    def predict(self, X_test, Y0_anchor_test):
        """
        X_test: (N_test, N_features)
        Y0_anchor_test: (N_test, 2) [anchor_h, anchor_a] (unscaled)
        Returns: (N_test, 2) predictions [height, agb] (unscaled)
        """
        anchor_h = Y0_anchor_test[:, 0]
        anchor_a = Y0_anchor_test[:, 1]
        
        preds_del_h = np.mean([m.predict(X_test) for m in self.fold_models_h], axis=0) * HEIGHT_MEAN
        preds_del_a = np.mean([m.predict(X_test) for m in self.fold_models_a], axis=0) * AGB_MEAN
        
        pred_h = np.maximum(0.0, anchor_h + preds_del_h)
        pred_a = np.maximum(0.0, anchor_a + preds_del_a)
        
        return np.column_stack([pred_h, pred_a])


class CalibratedStandGrowthModel:
    """
    Calibrated Stand Growth Model using 5-Fold Cross-Validation.
    Trains gradient boosted trees on spatiotemporal climate drivers, Reineke stand density,
    and initial ecosystem states to predict the physical delta from the PCHIP anchor.
    """
    def __init__(self, n_estimators=450, learning_rate=0.03, num_leaves=63, random_state=42):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.num_leaves = num_leaves
        self.random_state = random_state
        self.fold_models_h = []
        self.fold_models_a = []
        self.oof_preds_h = None
        self.oof_preds_a = None
        self.model_h = None
        self.model_a = None

    def fit_cv(self, X_train, Y0_anchor, Y_ref, n_splits=5):
        """
        X_train: (N_samples, N_features)
        Y0_anchor: (N_samples, 2) [anchor_h, anchor_a] (unscaled)
        Y_ref: (N_samples, 2) [ref_h, ref_a] (unscaled)
        """
        N_samples = len(X_train)
        self.fold_models_h = []
        self.fold_models_a = []
        self.oof_preds_h = np.zeros(N_samples, dtype=np.float32)
        self.oof_preds_a = np.zeros(N_samples, dtype=np.float32)
        
        delta_h_scaled = (Y_ref[:, 0] - Y0_anchor[:, 0]) / HEIGHT_MEAN
        delta_a_scaled = (Y_ref[:, 1] - Y0_anchor[:, 1]) / AGB_MEAN
        
        kf = KFold(n_splits=n_splits, shuffle=True, random_state=self.random_state)
        for fold, (tr_idx, val_idx) in enumerate(kf.split(X_train)):
            mh = lgb.LGBMRegressor(
                n_estimators=self.n_estimators,
                learning_rate=self.learning_rate,
                num_leaves=self.num_leaves,
                subsample=0.85,
                colsample_bytree=0.80,
                random_state=self.random_state + fold,
                n_jobs=-1,
                verbose=-1
            )
            ma = lgb.LGBMRegressor(
                n_estimators=self.n_estimators,
                learning_rate=self.learning_rate,
                num_leaves=self.num_leaves,
                subsample=0.85,
                colsample_bytree=0.80,
                random_state=self.random_state + fold + 10,
                n_jobs=-1,
                verbose=-1
            )
            mh.fit(X_train[tr_idx], delta_h_scaled[tr_idx])
            ma.fit(X_train[tr_idx], delta_a_scaled[tr_idx])
            
            pred_val_h = np.maximum(0.0, Y0_anchor[val_idx, 0] + mh.predict(X_train[val_idx]) * HEIGHT_MEAN)
            pred_val_a = np.maximum(0.0, Y0_anchor[val_idx, 1] + ma.predict(X_train[val_idx]) * AGB_MEAN)
            
            self.oof_preds_h[val_idx] = pred_val_h
            self.oof_preds_a[val_idx] = pred_val_a
            
            self.fold_models_h.append(mh)
            self.fold_models_a.append(ma)

    def fit(self, X_train, Y0_anchor, Y_ref):
        """Standard full fit fallback"""
        self.fit_cv(X_train, Y0_anchor, Y_ref, n_splits=5)

    def predict(self, X_test, Y0_anchor):
        """
        X_test: (N_test, N_features)
        Y0_anchor: (N_test, 2) [anchor_h, anchor_a]
        Returns: (N_test, 2) predictions [height, agb] (unscaled)
        """
        if len(self.fold_models_h) > 0:
            pred_del_h = np.mean([m.predict(X_test) for m in self.fold_models_h], axis=0) * HEIGHT_MEAN
            pred_del_a = np.mean([m.predict(X_test) for m in self.fold_models_a], axis=0) * AGB_MEAN
        else:
            pred_del_h = self.model_h.predict(X_test) * HEIGHT_MEAN
            pred_del_a = self.model_a.predict(X_test) * AGB_MEAN
            
        pred_h = np.maximum(0.0, Y0_anchor[:, 0] + pred_del_h)
        pred_a = np.maximum(0.0, Y0_anchor[:, 1] + pred_del_a)
        
        return np.column_stack([pred_h, pred_a])

ReferenceDistillationModel = CalibratedStandGrowthModel
