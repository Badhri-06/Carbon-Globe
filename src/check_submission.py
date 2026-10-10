import os
import sys
import pandas as pd
import numpy as np

SUBMISSION_PATH = "outputs/submission.csv"
SAMPLE_SUBMISSION_PATH = "competition_data/sample_submission.csv"
EXPECTED_ROWS = 185130

def check_submission_file(sub_path=SUBMISSION_PATH, sample_path=SAMPLE_SUBMISSION_PATH):
    print("==================================================")
    print("      AUTOMATED SUBMISSION CHECKER & VERIFIER     ")
    print("==================================================")
    
    if not os.path.exists(sub_path):
        print(f"[FAIL] Submission file not found at {sub_path}")
        return False
        
    print(f"[1/8] File existence confirmed: {sub_path}")
    
    try:
        sub_df = pd.read_csv(sub_path)
    except Exception as e:
        print(f"[FAIL] Unable to parse CSV file: {e}")
        return False
        
    # Check 1: Row count
    if len(sub_df) != EXPECTED_ROWS:
        print(f"[FAIL] Expected {EXPECTED_ROWS} rows, got {len(sub_df)}")
        return False
    print(f"[2/8] Row count verified: {EXPECTED_ROWS} rows")
    
    # Check 2: Columns
    expected_cols = ["id", "height", "agb"]
    if list(sub_df.columns) != expected_cols:
        print(f"[FAIL] Expected columns {expected_cols}, got {list(sub_df.columns)}")
        return False
    print(f"[3/8] Column header verified: {list(sub_df.columns)}")
    
    # Check 3: Missing/NaN/Inf values
    if sub_df.isnull().any().any():
        print(f"[FAIL] Submission contains NaN or missing values!")
        return False
    if np.isinf(sub_df["height"].values).any() or np.isinf(sub_df["agb"].values).any():
        print(f"[FAIL] Submission contains Infinite values!")
        return False
    print(f"[4/8] Null and Infinity checks passed")
    
    # Check 4: ID alignment with sample_submission
    if os.path.exists(sample_path):
        sample_df = pd.read_csv(sample_path)
        if not (sub_df["id"].values == sample_df["id"].values).all():
            print(f"[FAIL] Submission IDs do NOT match sample_submission.csv exact sequence!")
            mismatches = (sub_df["id"].values != sample_df["id"].values).sum()
            print(f"       Total mismatches: {mismatches}")
            return False
        print(f"[5/8] ID sequence matches sample_submission.csv perfectly")
    else:
        print(f"[WARNING] sample_submission.csv not found at {sample_path} to compare IDs.")
        
    # Check 5: Duplicate IDs
    if sub_df["id"].duplicated().any():
        print(f"[FAIL] Submission contains duplicate IDs!")
        return False
    print(f"[6/8] Duplicate ID check passed")
    
    # Check 6: Scenario distribution
    ssp126_count = sub_df["id"].str.startswith("ssp126_").sum()
    ssp585_count = sub_df["id"].str.startswith("ssp585_").sum()
    if ssp126_count != 92565 or ssp585_count != 92565:
        print(f"[FAIL] Scenario counts mismatched. Expected 92565 each, got ssp126={ssp126_count}, ssp585={ssp585_count}")
        return False
    print(f"[7/8] Scenario distribution verified (92,565 rows for ssp126, 92,565 rows for ssp585)")
    
    # Check 7: Value ranges and statistics
    h_min, h_max, h_mean = sub_df["height"].min(), sub_df["height"].max(), sub_df["height"].mean()
    a_min, a_max, a_mean = sub_df["agb"].min(), sub_df["agb"].max(), sub_df["agb"].mean()
    
    print(f"[8/8] Target Statistics:")
    print(f"       Height (scaled): min={h_min:.4f}, max={h_max:.4f}, mean={h_mean:.4f}")
    print(f"       AGB (scaled):    min={a_min:.4f}, max={a_max:.4f}, mean={a_mean:.4f}")
    
    if h_min < 0 or a_min < 0:
        print(f"[WARNING] Negative predicted values detected: min height={h_min}, min agb={a_min}")
    if h_mean < 0.1 or h_mean > 5.0 or a_mean < 0.1 or a_mean > 5.0:
        print(f"[WARNING] Unusually scaled mean values! Ensure height was divided by 10.90645 and agb by 3.39567.")
        
    print("\n>>> SUCCESS: Submission file passed all automated validation checks! <<<")
    return True

if __name__ == "__main__":
    success = check_submission_file()
    if not success:
        sys.exit(1)
