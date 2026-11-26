# Environmental AI: Air Quality Prediction & Pollution Forecasting

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Embarko Challenge](https://img.shields.io/badge/Embarko-Student%20Challenge-orange.svg)](https://embarko.com)

> **Advanced ML project for the Embarko Student Challenge** — Predicting Air Quality Index (AQI) and major pollutant concentrations using ensemble methods combining Gradient Boosting (XGBoost/LightGBM) with Temporal Transformers.

## 🎯 Problem Statement

Air pollution causes **7 million premature deaths annually** (WHO). Accurate forecasting of Air Quality Index (AQI) and pollutant levels (PM2.5, PM10, NO2, SO2, CO, O3) enables:
- Public health warnings and advisories
- Traffic management and emission control policies
- Industrial activity planning
- Personal exposure reduction strategies

This project builds a **production-ready multi-horizon forecasting system** (6h–72h ahead) using state-of-the-art ensemble methods.

## 🏗️ Architecture Overview

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  XGBoost        │     │  LightGBM       │     │  Temporal       │
│  (Tabular)      │     │  (Tabular)      │     │  Transformer    │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 ▼
                    ┌────────────────────────┐
                    │   Stacking Ensemble    │
                    │   (Ridge Meta-learner) │
                    └────────────┬───────────┘
                                 ▼
                    ┌────────────────────────┐
                    │   Multi-output         │
                    │   Predictions          │
                    │   AQI + 6 Pollutants   │
                    └────────────────────────┘
```

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| **Multi-Horizon Forecasting** | 6h, 12h, 24h, 48h, 72h ahead predictions |
| **Multi-Pollutant** | Simultaneous prediction of AQI, PM2.5, PM10, NO2, SO2, CO, O3 |
| **Ensemble Learning** | Stacking XGBoost + LightGBM + Transformer |
| **Uncertainty Quantification** | Prediction intervals via quantile regression |
| **Interpretability** | SHAP values for regulatory compliance |
| **Temporal CV** | Proper time-series splits with purge/embargo |
| **Production API** | FastAPI service with batch/online inference |
| **Interactive Demo** | Streamlit dashboard for real-time visualization |

## 📊 Results (Preliminary)

| Pollutant | 24h MAE | 24h RMSE | 24h R² | 72h MAE |
|-----------|---------|----------|--------|---------|
| AQI       | 8.2     | 12.1     | 0.81   | 11.5    |
| PM2.5     | 6.4     | 9.8      | 0.78   | 9.1     |
| PM10      | 12.3    | 18.7     | 0.72   | 16.8    |
| NO2       | 4.1     | 6.2      | 0.85   | 5.8     |
| SO2       | 2.8     | 4.1      | 0.79   | 3.9     |
| CO        | 0.15    | 0.22     | 0.83   | 0.20    |
| O3        | 5.6     | 8.3      | 0.76   | 7.9     |

*Results on held-out test set across 4 major cities (Delhi, Beijing, Los Angeles, London)*

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/amritkalmane/environmental-ai.git
cd environmental-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

### Configuration

```bash
# Copy and edit config
cp config.yaml config.local.yaml
# Edit config.local.yaml with your API keys and preferences
```

### Data Download

```bash
# Download training data from OpenAQ + weather APIs
python -m environmental_ai.data.fetch --config config.local.yaml
```

### Training

```bash
# Train all models with hyperparameter tuning
python -m environmental_ai.training.train --config config.local.yaml --tune

# Train specific model
python -m environmental_ai.training.train --model xgboost --config config.local.yaml
```

### Inference

```bash
# Batch prediction
python -m environmental_ai.inference.predict --input data/processed/test.csv --output outputs/predictions.csv

# Start API server
python -m environmental_ai.inference.serve --config config.local.yaml
```

### Demo Dashboard

```bash
# Launch Streamlit dashboard
streamlit run notebooks/05_inference_demo.py
```

## 📁 Project Structure

```
environmental-ai/
├── config.yaml              # Main configuration
├── requirements.txt         # Python dependencies
├── pyproject.toml          # Package metadata
├── src/
│   └── environmental_ai/
│       ├── data/           # Data fetching, preprocessing, features
│       ├── models/         # Model implementations
│       ├── training/       # Training loops, evaluation, tuning
│       ├── inference/      # Prediction, API serving
│       └── utils/          # Metrics, visualization, helpers
├── notebooks/              # Jupyter notebooks for exploration
├── tests/                  # Unit and integration tests
├── data/                   # Data directories (gitignored)
├── models/                 # Saved models (gitignored)
├── logs/                   # Training logs
└── outputs/                # Predictions, visualizations
```

## 🔬 Technical Details

### Feature Engineering
- **Temporal**: Cyclical encoding (hour, day, month), holidays, seasons
- **Lag Features**: 1h–72h lags for all pollutants + weather
- **Rolling Statistics**: 3h–72h windows (mean, std, min, max, median)
- **Weather Interactions**: Temp×Humidity, Wind×Pollutants
- **AQI Calculation**: EPA standard breakpoints

### Models
1. **XGBoost**: 2000 trees, depth 8, early stopping, per-target models
2. **LightGBM**: 2000 trees, 127 leaves, GPU-accelerated
3. **Temporal Transformer**: 4 layers, 8 heads, 256 dim, 168h context
4. **Baselines**: Persistence, Seasonal Naive, ARIMA, Prophet
5. **Stacking Ensemble**: Ridge meta-learner on out-of-fold predictions

### Evaluation
- **Metrics**: MAE, RMSE, R², MAPE, SMAPE, Quantile Loss
- **Cross-Validation**: Purged TimeSeriesSplit (5 folds, 24h gap)
- **Uncertainty**: Quantile regression (5%, 10%, 25%, 50%, 75%, 90%, 95%)

## 📈 Notebooks

| Notebook | Description |
|----------|-------------|
| `01_data_exploration.ipynb` | EDA of air quality & weather data |
| `02_feature_engineering.ipynb` | Feature creation & validation |
| `03_model_training.ipynb` | Individual model training & tuning |
| `04_ensemble_evaluation.ipynb` | Ensemble construction & comparison |
| `05_inference_demo.ipynb` | Interactive prediction dashboard |

## 🐳 Docker Deployment

```bash
# Build image
docker build -t environmental-ai .

# Run API server
docker run -p 8000:8000 environmental-ai serve

# Run Streamlit dashboard
docker run -p 8501:8501 environmental-ai streamlit
```

## 📝 Challenge Submission

This project was built for the **Embarko Student Challenge** demonstrating:

- ✅ **Technical Depth**: Advanced ensemble methods, transformers, proper ML practices
- ✅ **Real-World Impact**: Addresses global health crisis (air pollution)
- ✅ **Production Readiness**: API, monitoring, Docker, comprehensive tests
- ✅ **Innovation**: Novel combination of GBTs + Transformers for environmental time series
- ✅ **Reproducibility**: Config-driven, versioned, documented

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- **OpenAQ** for open air quality data
- **Open-Meteo** for free weather API
- **Embarko** for the challenge opportunity
- **Hugging Face** for transformer ecosystem

---

**Built with ❤️ for the Embarko Student Challenge** | [Report](docs/report.pdf) | [Presentation](docs/presentation.pdf) | [Video Demo](https://youtube.com/...)