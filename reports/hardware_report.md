# Hardware and System Environment Report

**Date & Time**: 2026-10-07
**Project**: IEEE BigData Cup 2026 AI Emulation Challenge (CarbonGlobe)

## System Hardware Specifications

| Property | Value |
|---|---|
| **OS Platform** | Windows 10 / 11 (Build 26200, 64-bit AMD64) |
| **CPU Model** | 12th Gen Intel(R) Core(TM) i7-12650H |
| **Physical Cores** | 10 cores (6 Performance + 4 Efficient) |
| **Logical Threads** | 16 threads |
| **Total System RAM** | 15.65 GB |
| **Available RAM** | ~0.76 - 4.00 GB (Dynamic) |
| **Disk Space Total** | 907.97 GB |
| **Disk Space Free** | 233.85 GB |

## GPU Acceleration Details

| Property | Value |
|---|---|
| **GPU Model** | NVIDIA GeForce RTX 3050 Laptop GPU |
| **VRAM Total** | 4.00 GB (GDDR6) |
| **Driver Version** | 592.82 |
| **CUDA System Driver** | 13.1 |
| **WDDM Mode** | Enabled |

## Software & Python Environment

| Property | Value |
|---|---|
| **Python Version** | 3.10.11 (64-bit) |
| **Executable Path** | `C:\Users\badhr\AppData\Local\Programs\Python\Python310\python.exe` |
| **PyTorch CUDA Target** | PyTorch 2.5.1 + CUDA 12.1 (`cu121`) |

## Operational Guidelines for Computational Constraints
1. **Memory Safety**: Given 16 GB system RAM and 4 GB GPU VRAM, large arrays (> 1 GB) must be loaded with `np.load(..., mmap_mode='r')` or streamed in float32 chunks.
2. **Hybrid Execution Strategy**: Use GPU acceleration for neural network forward/backward passes with small/medium batch sizes (e.g., batch_size 1024 - 4096), and CPU multiprocessing for tree models (LightGBM/XGBoost) and dataset feature extraction.
