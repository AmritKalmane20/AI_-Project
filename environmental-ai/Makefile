# Environmental AI - Makefile
# Common commands for development, training, and deployment

.PHONY: help install dev-install test lint format typecheck clean \
        fetch preprocess features train tune predict serve dashboard \
        docker-build docker-up docker-down docker-logs

# Default target
help:
	@echo "Environmental AI - Air Quality Prediction"
	@echo ""
	@echo "Available commands:"
	@echo "  make install        - Install production dependencies"
	@echo "  make dev-install    - Install development dependencies"
	@echo "  make test           - Run tests"
	@echo "  make lint           - Run linters (flake8)"
	@echo "  make format         - Format code (black + isort)"
	@echo "  make typecheck      - Type check (mypy)"
	@echo "  make clean          - Clean build artifacts"
	@echo ""
	@echo "Data pipeline:"
	@echo "  make fetch          - Fetch data from APIs"
	@echo "  make preprocess     - Preprocess raw data"
	@echo "  make features       - Run feature engineering"
	@echo ""
	@echo "Model training:"
	@echo "  make train          - Train all models"
	@echo "  make train-xgb      - Train XGBoost only"
	@echo "  make train-lgb      - Train LightGBM only"
	@echo "  make train-ensemble - Train ensemble"
	@echo "  make tune           - Hyperparameter tuning"
	@echo ""
	@echo "Inference:"
	@echo "  make predict        - Batch prediction"
	@echo "  make predict-city   - Predict for a city"
	@echo "  make serve          - Start API server"
	@echo "  make dashboard      - Start Streamlit dashboard"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build   - Build Docker image"
	@echo "  make docker-up      - Start all services"
	@echo "  make docker-down    - Stop all services"
	@echo "  make docker-logs    - View logs"

# Installation
install:
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -e .

dev-install:
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -e ".[dev]"
	pre-commit install

# Code quality
test:
	pytest tests/ -v --tb=short --cov=src/environmental_ai --cov-report=term-missing

lint:
	flake8 src/
	mypy src/

format:
	black src/
	isort src/

typecheck:
	mypy src/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov dist build *.egg-info
	rm -rf logs/*.log outputs/*.png outputs/*.json outputs/*.csv

# Data pipeline
fetch:
	python -m environmental_ai.cli fetch

fetch-city:
	python -m environmental_ai.cli fetch --city $(CITY)

preprocess:
	python -m environmental_ai.cli preprocess

features:
	python -m environmental_ai.cli features

# Model training
train:
	python -m environmental_ai.cli train --model all

train-xgb:
	python -m environmental_ai.cli train --model xgboost

train-lgb:
	python -m environmental_ai.cli train --model lightgbm

train-baselines:
	python -m environmental_ai.cli train --model baselines

train-ensemble:
	python -m environmental_ai.cli train --model ensemble

# Hyperparameter tuning
tune:
	python -m environmental_ai.cli tune --model all --trials 100

tune-xgb:
	python -m environmental_ai.cli tune --model xgboost --trials 50

tune-lgb:
	python -m environmental_ai.cli tune --model lightgbm --trials 50

# Inference
predict:
	python -m environmental_ai.cli predict

predict-city:
	python -m environmental_ai.cli predict-city --city $(CITY)

serve:
	python -m environmental_ai.cli serve --host 0.0.0.0 --port 8000

dashboard:
	streamlit run notebooks/05_inference_demo.py --server.port 8501 --server.address 0.0.0.0

# Evaluation
evaluate:
	python -m environmental_ai.cli evaluate

# Docker
docker-build:
	docker build -t environmental-ai:latest .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-train:
	docker-compose --profile training up train

docker-tune:
	docker-compose --profile tuning up tune

docker-fetch:
	docker-compose --profile data up fetch

# Full pipeline
pipeline: fetch preprocess features train
	@echo "Full pipeline completed!"

# Quick development cycle
dev-cycle: format test
	@echo "Development cycle complete!"