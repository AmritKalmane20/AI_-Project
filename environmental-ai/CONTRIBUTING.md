# Contributing to Environmental AI

Thank you for your interest in contributing! This project is for the Embarko Student Challenge and welcomes contributions.

## Getting Started

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/yourusername/environmental-ai.git
   cd environmental-ai
   ```
3. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
4. **Install development dependencies**
   ```bash
   make dev-install
   ```
5. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### Code Style
- **Formatting**: Black (line length 100)
- **Imports**: isort (Black profile)
- **Linting**: flake8 + mypy
- **Pre-commit**: Runs automatically on commit

```bash
# Format code
make format

# Run linters
make lint

# Run type checking
make typecheck
```

### Running Tests
```bash
# Run all tests
make test

# Run with coverage
pytest tests/ --cov=src/environmental_ai --cov-report=html
```

### Data Pipeline
```bash
# Fetch data from APIs
make fetch

# Preprocess raw data
make preprocess

# Run feature engineering
make features
```

### Model Training
```bash
# Train all models
make train

# Train specific model
make train-xgb
make train-lgb

# Hyperparameter tuning
make tune
```

### Inference & Serving
```bash
# Batch prediction
make predict

# Predict for specific city
make predict-city CITY=Delhi

# Start API server
make serve

# Start Streamlit dashboard
make dashboard
```

## Project Structure

```
environmental-ai/
├── src/environmental_ai/       # Main package
│   ├── data/                   # Data fetching, preprocessing, features
│   ├── models/                 # Model implementations
│   ├── training/               # Training, evaluation, tuning
│   ├── inference/              # Prediction, API serving
│   └── utils/                  # Metrics, visualization, helpers
├── notebooks/                  # Jupyter notebooks
├── tests/                      # Unit tests
├── data/                       # Data directories (gitignored)
├── models/                     # Saved models (gitignored)
├── logs/                       # Training logs (gitignored)
├── outputs/                    # Predictions, visualizations (gitignored)
├── config.yaml                 # Configuration
├── requirements.txt            # Dependencies
├── pyproject.toml             # Package metadata
├── Dockerfile                 # Docker image
├── docker-compose.yml         # Multi-container setup
└── Makefile                   # Common commands
```

## Adding New Models

1. Create model class in `src/environmental_ai/models/`
2. Implement `fit()`, `predict()`, `save()`, `load()` methods
3. Add to `src/environmental_ai/models/__init__.py`
4. Update ensemble to include new model
5. Add tests in `tests/test_models.py`

## Adding New Features

1. Add feature engineering method in `FeatureEngineer` class
2. Update config.yaml with feature parameters
3. Add tests in `tests/test_data.py`

## Configuration

All hyperparameters and settings are in `config.yaml`. Modify this file instead of hardcoding values.

## Pull Request Process

1. **Update documentation** for any new features
2. **Add tests** for new functionality
3. **Ensure all checks pass**: `make format && make lint && make test`
4. **Write clear commit messages** following conventional commits
5. **Open a PR** with description of changes

### Commit Message Format
```
type(scope): description

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Example:
```
feat(models): add CatBoost model to ensemble

- Implement CatBoostModel class with GPU support
- Add to stacking ensemble meta-learner
- Update config with CatBoost parameters

Closes #123
```

## Reporting Issues

Use GitHub Issues for:
- Bug reports
- Feature requests
- Documentation improvements
- Performance issues

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Happy coding!** 🌍