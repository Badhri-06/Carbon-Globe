# CarbonGlobe Dataset
Our dataset, CarbonGlobe, is accepted to NeurIPS 2025 Dataset and Benchmark track.

## Overview
The CarbonGlobe dataset is designed for forest carbon dynamics monitoring and forecasting. It includes various ecological and environmental variables collected over a 40-year temporal range and a global spatial scale. This ML-ready dataset integrates over 100 variables from heterogeneous sources.

## Data Structure
Main Directory
data_global/: Contains input features and output data for different forest ages.
	glob_X_fea.npy: Input features.
	glob_Y001.npy to glob_Y500.npy: Output data at different forest ages.
data_stats/: Contains statistical information.
	data_stats.npz: Mean and standard deviation information.
	age_triplet.npz: Age triplet data.
	mask2d.npy: Mask data converting 1d raw data to 2d at global scale.
insitu_data/: Contains in-situ observations from the ABoVE GPP dataset
	lat....csv: contains the GPP observations in this location.
	lat_lon_age_weights.csv: weighted sum all ages from 1 to 500 to recover the obs.
train.csv: Indices for training samples.
val.csv: Indices for validation samples.
test.csv: Indices for test samples.
readme.txt: This file.

## Code Repository
The code used for developing the dataset is available on GitHub: https://github.com/zhwang0/carbon-globe

## Keywords
carbon-dynamics
forest-ecosystem
climate-modeling
environmental-science
time-series-forecasting
ecological-data
machine-learning


