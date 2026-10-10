# Project Archive: Publication & Presentation Assets

This directory contains the academic research manuscript, technical presentation decks, and associated generation scripts for the **IEEE BigData Cup 2026 AI Emulation Challenge**.

---

## 📁 Archive Contents

### 1. Research Paper (LaTeX)
* **`paper.tex`**: Full publication-grade IEEE conference paper (*Physics-Guided Allometric Spline Anchoring and Multi-Decade Climate Emulation for Global Forest Carbon Forecasting*).
* **`figures/`**: Publication figures (300 DPI):
  * `system_architecture.png`: End-to-end physics-guided emulation pipeline.
  * `allometric_trajectories.png`: Monotonic PCHIP stand growth vs. polynomial Runge oscillations.
  * `correlation_matrix.png`: Biophysical, climate, and ecosystem state correlation heatmap.
  * `experiment_progression.png`: Cross-validation progression bar chart across 20+ runs.
  * `fit_fidelity_parity.png`: Parity hexbin density plots for Height ($R^2=0.9982$) and AGB ($R^2=0.9991$).

### 2. Presentation Decks
* **`presentation.pptx`**: 12-slide modern 16:9 widescreen presentation for Microsoft PowerPoint, Google Slides, or Keynote.
* **`presentation.tex`**: 12-slide LaTeX Beamer presentation for Overleaf (`aspectratio=169`).

### 3. Generation & Reproduction Scripts
* **`create_presentation.py`**: Python script generating `presentation.pptx` using `python-pptx`.
* **`generate_paper_figures.py`**: Python script generating the core architectural, trajectory, parity, and progression figures.
* **`generate_correlation_figure.py`**: Python script computing and rendering the lower-triangular biophysical correlation heatmap.

---

### Authors & Affiliation
* **Authors**: Aswitha K, Badhri Narayanan M, Bavin Aadithiya S, Bose M
* **Institution**: Department of Computer Science and Engineering, Sri Sivasubramaniya Nadar College of Engineering, Chennai, India
