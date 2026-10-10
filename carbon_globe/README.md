---
pretty_name: CarbonGlobe
language:
- en
license: cc-by-4.0
task_categories:
- time-series-forecasting
- tabular-regression
tags:
- carbon-cycle
- forest-ecosystems
- ecosystem-modeling
- earth-system-science
- remote-sensing
- deep-learning
- time-series
- forecasting
- ecological-forecasting
- process-based-modeling
- ecosystem-demography-model
- ed-v3
- benchmark
- neurips-2025
size_categories:
- 10K<n<100K
---

# CarbonGlobe: A Global-Scale, Multi-Decade Dataset and Benchmark for Carbon Forecasting in Forest Ecosystems

**CarbonGlobe** is a global-scale, multi-decade, machine-learning-ready dataset and benchmark for forecasting carbon dynamics in forest ecosystems. The dataset provides harmonized environmental drivers and carbon-related ecosystem outputs simulated by the **Ecosystem Demography model version 3 (ED v3)**, enabling the development, evaluation, and comparison of deep learning models for global forest carbon forecasting.

CarbonGlobe was accepted to the **NeurIPS 2025 Datasets & Benchmarks Track**. 

**Project page**: https://github.com/zhwang0/carbon-globe

## Dataset Description

Forest ecosystems play a central role in the global carbon cycle, but forecasting their long-term dynamics remains challenging because process-based ecosystem models are computationally expensive and difficult to scale across large spatial domains and many scenarios.

CarbonGlobe addresses this challenge by providing a reproducible benchmark for learning from process-based ecosystem simulations. It bridges **Earth system science** and **machine learning** by transforming global ED v3 simulations and associated environmental drivers into a standardized dataset for carbon forecasting.

The dataset is designed to support the development of machine learning emulators and forecasting models that can predict multivariate ecosystem trajectories under diverse environmental, regional, and ecological conditions.

## Dataset Summary

CarbonGlobe includes:

- **Global 0.5° spatial coverage**, with approximately 70,000 grid cells
- **Multi-decade temporal coverage**, spanning more than 40 years from 1980 to 2020
- **Monthly time-series data** for long-term ecosystem forecasting
- **100+ environmental input variables** from meteorological, atmospheric, soil, and vegetation-related sources
- **ED v3-simulated ecosystem output variables**, including carbon stocks, vegetation structure, and ecosystem fluxes
- **ML-ready samples** for training and evaluating time-series forecasting models
- **Scenario-based evaluation protocols** for assessing model robustness under environmental, forest-age, and regional domain shifts

## Supported Tasks

CarbonGlobe supports the following machine learning tasks:

- Multivariate time-series forecasting
- Forest carbon forecasting
- Ecosystem model emulation
- Long-horizon sequence prediction
- Spatiotemporal environmental modeling
- Domain generalization across environmental conditions, regions, and forest conditions
- Benchmarking deep learning models for Earth system applications

## Dataset Structure

Each sample contains environmental input drivers, ED-simulated target variables, temporal information, and geographic/ecological metadata.

Input variables include environmental drivers such as:

```text
Meteorological variables, atmospheric CO2, soil properties, vegetation-related variables, and other environmental covariates.
```

Target variables include ED v3-simulated ecosystem states and fluxes, such as:

```text
Vegetation height, soil carbon (SC), above-ground biomass (AGB), leaf area index (LAI), gross primary productivity (GPP), net primary productivity (NPP), heterotrophic respiration (RH).
```


## Data Sources

CarbonGlobe is constructed from harmonized environmental input variables and outputs simulated by the **Ecosystem Demography model version 3 (ED v3)**.

The dataset is intended to provide a standardized machine learning benchmark for carbon forecasting in forest ecosystems. It enables users to train data-driven forecasting models using the same input-output structure as process-based ecosystem simulations, while supporting controlled evaluation across ecological and geographic domains.

## Dataset Splits

CarbonGlobe supports multiple evaluation settings for both standard forecasting and domain generalization.

Recommended split types include:

- **Random split**: standard train/validation/test evaluation across global samples
- **Regional split**: evaluation across geographic regions
- **Environmental-condition split**: evaluation across diverse environmental conditions
- **Forest-age or ecosystem-condition split**: evaluation across different ecosystem development stages
- **Temporal forecasting split**: training on historical sequences and evaluating long-horizon future prediction

Please refer to the accompanying benchmark code for the exact split definitions and evaluation protocol.

## Metadata

Each sample may include metadata such as:

- Geographic coordinates
- Grid identifier
- Diverse environmental condition
- Dominant forest type
- Monthly time index
- Train/validation/test split indicator

These metadata enable controlled evaluation of model generalization across environmental domains, including:

- Tropical to temperate transfer
- Humid to arid condition transfer
- Cross-region forecasting
- Cross-forest-type forecasting
- Generalization across forest structural or developmental conditions

## Benchmark Models

CarbonGlobe includes benchmark results from representative forecasting models across multiple modeling paradigms.

Evaluated models include:

- **LSTM**
- **LSTNet**
- **DeepED**, a physics-guided deep learning emulator for ecosystem dynamics
- **Transformer**
- **Informer**
- **Crossformer**
- **TimeXer**
- **DLinear**

These models are evaluated for multivariate ecosystem trajectory prediction under both standard and domain-shift settings.

## Evaluation

CarbonGlobe is designed for multivariate, long-horizon ecosystem forecasting. Recommended evaluation metrics include:

- Root mean squared error (RMSE)
- Mean absolute error (MAE)
- Delta error
- Cumulative error

In addition to pointwise prediction accuracy, users are encouraged to report trajectory-level metrics that evaluate whether models preserve long-term ecosystem dynamics, temporal changes, and accumulated carbon-cycle behavior.

## Intended Uses

CarbonGlobe is intended for research and benchmarking in:

- Forest carbon forecasting
- Ecosystem model emulation
- Environmental impact assessment
- Long-term ecological forecasting
- Earth system machine learning
- Development and evaluation of deep learning models for environmental time series
- Benchmarking generalization under environmental, regional, and ecological domain shifts
- Scalable approximation of process-based ecosystem model outputs

## Ethical and Environmental Considerations

CarbonGlobe does not contain personal or sensitive human information. The dataset is based on environmental drivers and process-based ecosystem model simulations.

Potential positive impacts include improved accessibility of global carbon forecasting benchmarks, reduced computational barriers for ecosystem model emulation, and stronger collaboration between machine learning and Earth system science communities.

Potential risks include over-interpreting model predictions as direct real-world forecasts, using outputs without accounting for uncertainty, or applying benchmark-trained models to policy-sensitive decisions without additional validation.

## How to Use

Example loading workflow:

```python
from datasets import load_dataset

dataset = load_dataset("zhwang1/CarbonGlobe")
print(dataset)
print(dataset["train"][0])
```

The GitHub repository is available here: https://github.com/zhwang0/carbon-globe.

## Citation

If you use **CarbonGlobe** in your research, please cite:

```bibtex
@inproceedings{wang2025carbonglobe,
  title     = {CarbonGlobe: A Global-Scale, Multi-Decade Dataset and Benchmark for Carbon Forecasting in Forest Ecosystems},
  author    = {Wang, Zhihao and Ma, Lei and Hurtt, George and Jia, Xiaowei and Li, Yanhua and Li, Ruohan and Li, Zhili and Xu, Shuo and Xie, Yiqun},
  booktitle = {Proceedings of the 39th Conference on Neural Information Processing Systems (NeurIPS 2025), Datasets and Benchmarks Track},
  year      = {2025}
}
```

## Dataset Contact

For questions, issues, or collaboration inquiries, please open an issue in the associated GitHub repository or contact the dataset authors.

## Acknowledgements

CarbonGlobe was developed to support reproducible machine learning research for forest carbon forecasting and ecosystem model emulation. We thank the collaborators, data providers, and research communities that supported dataset development, simulation, benchmarking, and validation.