import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import KFold

class PyTorchResTabularNN(nn.Module):
    """
    Deep Residual Tabular Neural Network for predicting ecosystem state deltas.
    Uses LayerNorm, SiLU activations, residual skip-connections, and dropout.
    """
    def __init__(self, in_features, hidden_dim=512, dropout=0.1, out_targets=2):
        super().__init__()
        self.input_layer = nn.Sequential(
            nn.Linear(in_features, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.SiLU()
        )
        
        self.res1 = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.SiLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim)
        )
        
        self.res2 = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.SiLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim)
        )
        
        self.head = nn.Sequential(
            nn.SiLU(),
            nn.Linear(hidden_dim, 256),
            nn.SiLU(),
            nn.Linear(256, out_targets)
        )

    def forward(self, x):
        h0 = self.input_layer(x)
        h1 = F.silu(h0 + self.res1(h0))
        h2 = F.silu(h1 + self.res2(h1))
        return self.head(h2)


class AnchorDeltaPyTorchModel:
    """
    Anchor Delta PyTorch Predictor using 5-Fold GroupKFold Cross Validation.
    """
    def __init__(self, hidden_dim=512, epochs=35, batch_size=256, lr=0.002, random_state=42):
        self.hidden_dim = hidden_dim
        self.epochs = epochs
        self.batch_size = batch_size
        self.lr = lr
        self.random_state = random_state
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.models = []
        self.x_means = []
        self.x_stds = []
        
        self.oof_preds_h = None
        self.oof_preds_a = None

    def fit_cv(self, X_mat, Y0_anchor_mat, Delta_Y_mat, site_ids, n_splits=5):
        N_samples = X_mat.shape[0]
        site_uniques = np.unique(site_ids)
        kf = KFold(n_splits=n_splits, shuffle=True, random_state=self.random_state)
        
        self.oof_preds_h = np.zeros(N_samples, dtype=np.float32)
        self.oof_preds_a = np.zeros(N_samples, dtype=np.float32)
        
        anchor_h = Y0_anchor_mat[:, 0]
        anchor_a = Y0_anchor_mat[:, 1]
        
        self.models = []
        self.x_means = []
        self.x_stds = []
        
        for fold, (tr_sites_idx, val_sites_idx) in enumerate(kf.split(site_uniques)):
            tr_sites = set(site_uniques[tr_sites_idx])
            val_sites = set(site_uniques[val_sites_idx])
            
            tr_mask = np.array([s in tr_sites for s in site_ids])
            val_mask = np.array([s in val_sites for s in site_ids])
            
            X_tr, X_val = X_mat[tr_mask], X_mat[val_mask]
            delta_tr, delta_val = Delta_Y_mat[tr_mask], Delta_Y_mat[val_mask]
            
            # Standardization
            mean_tr = X_tr.mean(axis=0, keepdims=True)
            std_tr = X_tr.std(axis=0, keepdims=True) + 1e-6
            
            X_tr_norm = (X_tr - mean_tr) / std_tr
            X_val_norm = (X_val - mean_tr) / std_tr
            
            self.x_means.append(mean_tr)
            self.x_stds.append(std_tr)
            
            model = PyTorchResTabularNN(X_mat.shape[1], hidden_dim=self.hidden_dim).to(self.device)
            optimizer = torch.optim.AdamW(model.parameters(), lr=self.lr, weight_decay=1e-4)
            scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=self.epochs)
            criterion = nn.MSELoss()
            
            train_ds = TensorDataset(torch.tensor(X_tr_norm, dtype=torch.float32), torch.tensor(delta_tr, dtype=torch.float32))
            train_loader = DataLoader(train_ds, batch_size=self.batch_size, shuffle=True)
            
            model.train()
            for epoch in range(self.epochs):
                for batch_x, batch_y in train_loader:
                    batch_x, batch_y = batch_x.to(self.device), batch_y.to(self.device)
                    optimizer.zero_grad()
                    out = model(batch_x)
                    loss = criterion(out, batch_y)
                    loss.backward()
                    optimizer.step()
                scheduler.step()
                
            model.eval()
            with torch.no_grad():
                val_x_t = torch.tensor(X_val_norm, dtype=torch.float32).to(self.device)
                pred_delta_val = model(val_x_t).cpu().numpy()
                
            self.oof_preds_h[val_mask] = np.maximum(0.0, anchor_h[val_mask] + pred_delta_val[:, 0])
            self.oof_preds_a[val_mask] = np.maximum(0.0, anchor_a[val_mask] + pred_delta_val[:, 1])
            self.models.append(model)

    def predict(self, X_test, Y0_anchor_test):
        anchor_h = Y0_anchor_test[:, 0]
        anchor_a = Y0_anchor_test[:, 1]
        
        preds_del_list = []
        for model, mean_tr, std_tr in zip(self.models, self.x_means, self.x_stds):
            model.eval()
            X_test_norm = (X_test - mean_tr) / std_tr
            with torch.no_grad():
                xt = torch.tensor(X_test_norm, dtype=torch.float32).to(self.device)
                pred_del = model(xt).cpu().numpy()
                preds_del_list.append(pred_del)
                
        avg_preds_del = np.mean(preds_del_list, axis=0) # (N_test, 2)
        
        pred_h = np.maximum(0.0, anchor_h + avg_preds_del[:, 0])
        pred_a = np.maximum(0.0, anchor_a + avg_preds_del[:, 1])
        
        return np.column_stack([pred_h, pred_a])
