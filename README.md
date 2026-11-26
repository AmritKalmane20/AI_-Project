# AI_-Project

This repository contains two advanced AI/ML projects built for the **Embarko Student Challenge**.

## 🌍 Environmental AI - Air Quality Prediction & Pollution Forecasting

**Live Demo:** https://environmental-ai.embarko.app (deployed via Embarko)

An advanced ML project predicting Air Quality Index (AQI) and 6 major pollutants (PM2.5, PM10, NO2, SO2, CO, O3) for 6h–72h horizons across 4 major cities (Delhi, Beijing, Los Angeles, London).

### Features
- **Multi-pollutant prediction** - AQI, PM2.5, PM10, NO2, SO2, CO, O3
- **Multi-horizon forecasting** - 6h, 12h, 24h, 48h, 72h
- **Ensemble architecture** - XGBoost + LightGBM + Temporal Transformer + Stacking
- **Data sources** - OpenAQ (air quality) + Open-Meteo (weather)
- **Feature engineering** - 100+ features (temporal, lag, rolling, weather interactions)
- **Uncertainty quantification** - Prediction intervals via quantile regression
- **Production-ready** - FastAPI REST API, Streamlit dashboard, Docker

### Tech Stack
- Python 3.11, XGBoost, LightGBM (GPU), PyTorch, Hugging Face Transformers
- MLflow, Optuna, FastAPI, Streamlit, Docker
- GitHub Actions CI/CD

---

## 🛡️ ThreatIntel AI - Cybersecurity Threat Intelligence Platform

**Live Demo:** https://threat-intel-ai.embarko.app (deployed via Embarko)

An advanced cybersecurity threat intelligence platform analyzing IPs, domains, URLs, and file hashes with 11 analysis tabs.

### Features
- **11 Analysis Tabs**: Overview, Reputation, Network, SSL/TLS, Subdomains, Vulnerabilities, Behavior, Threat Intel, Threat Hunt, Report, Raw Data
- **Smart Paste** - Auto-extracts URLs, IPs, hashes from clipboard text
- **SSL/TLS Analysis** - Certificate grading, CT logs, config checks (HSTS, PFS, TLS 1.3)
- **Subdomain Enumeration** - 50+ discovered subdomains with threat scoring
- **Vulnerability Scanning** - 20+ real CVEs with CVSS, exploit availability, severity filter
- **MITRE ATT&CK Mapping** - Technique mapping with confidence scores
- **Threat Hunting** - 6 ready-to-run queries (copyable), IOC collections, campaign attribution
- **Report Generation** - Executive summary, recommendations, export (JSON/CSV/STIX/TAXII/PDF)
- **Zero-trust** - No logging, client-side processing

### Social Media Posts (Embarko Challenge)
- **LinkedIn:** ✅ Posted
- **Reddit:** ✅ Posted (r/cybersecurity)
- **Medium:** ✅ Posted
- **Twitter/X:** ⏳ OAuth pending

---

## 📁 Repository Structure

```
AI_-Project/
├── environmental-ai/          # Air Quality Prediction Project
│   ├── src/environmental_ai/  # Main package
│   │   ├── data/              # Data fetching, preprocessing, features
│   │   ├── models/            # XGBoost, LightGBM, Transformer, Ensemble
│   │   ├── training/          # Training, evaluation, Optuna tuning
│   │   ├── inference/         # Batch prediction, FastAPI, Streamlit
│   │   └── utils/             # Metrics, visualization, helpers
│   ├── notebooks/             # Jupyter notebooks
│   ├── tests/                 # Unit tests
│   ├── deploy_app/            # Embarko deployment
│   ├── Dockerfile             # Container
│   ├── docker-compose.yml     # Multi-service
│   ├── Makefile               # Common commands
│   └── config.yaml            # Configuration
│
├── threat-intel-ai/           # Cybersecurity Threat Intel Project
│   ├── deploy_app/            # Single HTML file with all logic
│   │   └── index.html         # Full threat intel platform
│
└── README.md
```

---

## 🚀 Quick Start

### Environmental AI
```bash
cd environmental-ai
make dev-install      # Install dependencies
make fetch            # Fetch data from OpenAQ/Open-Meteo
make preprocess       # Preprocess data
make features         # Feature engineering
make train            # Train all models
make serve            # Start API at localhost:8000
make dashboard        # Start Streamlit at localhost:8501
```

### ThreatIntel AI
```bash
cd threat-intel-ai
# Just open deploy_app/index.html in a browser
# Or deploy to Embarko:
tar -czf app.tar.gz -C deploy_app .
curl -X POST 'https://ship.embarko.ai/apps' \
  -H 'X-App-Name: threat-intel-ai' \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -F 'source=@app.tar.gz'
```

---

## 🏆 Embarko Student Challenge

Both projects are deployed on **Embarko** (https://embarko.ai) - a platform for deploying ML/AI apps without Docker, no signup required.

- **Environmental AI:** https://environmental-ai.embarko.app
- **ThreatIntel AI:** https://threat-intel-ai.embarko.app

### Social Media Presence
- **LinkedIn:** Posted with #embarko.ai #DeployWithEmbarko
- **Reddit:** Posted on r/cybersecurity with #embarko.ai #DeployWithEmbarko
- **Medium:** Published with #embarko.ai #DeployWithEmbarko
- **Twitter/X:** OAuth pending

---

## 📄 License

MIT License - see individual project directories for details.

---

Built with ❤️ for the **Embarko Student Challenge**