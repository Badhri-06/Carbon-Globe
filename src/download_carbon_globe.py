import os
import sys
import time
import urllib.request

REPO_URL = "https://huggingface.co/datasets/zhwang1/CarbonGlobe/resolve/main"
TARGET_DIR = "carbon_globe"

FILES_TO_DOWNLOAD = [
    "README.md",
    "readme.txt",
    "train.csv",
    "val.csv",
    "test.csv",
    "data_stats/age_triplet.npz",
    "data_stats/data_stats.npz",
    "data_stats/mask2d.npy",
    "data_global/res_train4_test8.npz",
]

# We will also check if glob_X_fea.npy or glob_Y*.npy are needed after inspecting metadata
OPTIONAL_LARGE_FILES = [
    "data_global/glob_X_fea.npy",
] + [f"data_global/glob_Y{age:03d}.npy" for age in [1, 10, 20, 30, 50, 70, 100, 150, 200, 250, 300, 350, 400, 450, 500]]


def download_file(rel_path, target_dir=TARGET_DIR):
    local_path = os.path.join(target_dir, rel_path)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    
    url = f"{REPO_URL}/{rel_path}?download=true"
    
    if os.path.exists(local_path):
        remote_size = get_remote_size(url)
        local_size = os.path.getsize(local_path)
        if remote_size is not None and local_size == remote_size:
            print(f"[SKIP] {rel_path} already downloaded ({local_size / (1024*1024):.2f} MB).")
            return local_path

    print(f"[DOWNLOADING] {rel_path} from {url}...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    
    start_time = time.time()
    try:
        with urllib.request.urlopen(req) as response, open(local_path, "wb") as out_file:
            total_size = int(response.info().get("Content-Length", 0))
            downloaded = 0
            block_size = 1024 * 1024 # 1MB chunk
            
            while True:
                buffer = response.read(block_size)
                if not buffer:
                    break
                downloaded += len(buffer)
                out_file.write(buffer)
                
                elapsed = time.time() - start_time
                speed = (downloaded / (1024 * 1024)) / elapsed if elapsed > 0 else 0
                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    print(f"\r  {downloaded/(1024*1024):.1f}/{total_size/(1024*1024):.1f} MB ({percent:.1f}%) @ {speed:.2f} MB/s", end="", flush=True)
                else:
                    print(f"\r  {downloaded/(1024*1024):.1f} MB @ {speed:.2f} MB/s", end="", flush=True)
        print(f"\n[DONE] {rel_path} finished in {time.time() - start_time:.1f}s.")
        return local_path
    except Exception as e:
        print(f"\n[ERROR] Failed to download {rel_path}: {e}")
        if os.path.exists(local_path):
            os.remove(local_path)
        return None


def get_remote_size(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}, method="HEAD")
        with urllib.request.urlopen(req) as response:
            return int(response.info().get("Content-Length", 0))
    except:
        return None


if __name__ == "__main__":
    print("=== CarbonGlobe Dataset Downloader ===")
    os.makedirs(TARGET_DIR, exist_ok=True)
    
    # First download metadata and split files
    for rel_path in FILES_TO_DOWNLOAD:
        download_file(rel_path)

    print("\nInitial download step complete!")
