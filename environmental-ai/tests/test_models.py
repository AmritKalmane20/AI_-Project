"""
Tests for models module.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path

from environmental_ai.models.xgboost_model import XGBoostModel
from environmental_ai.models.lightgbm_model import LightGBMModel
from environmental_ai.models.baseline import PersistenceModel, SeasonalNaiveModel, LinearTrendModel
from environmental_ai.config import Config


class TestXGBoostModel:
    """Tests for XGBoostModel."""

    @pytest.fixture
    def config(self):
        # Use smaller params for faster testing
        config = Config.from_yaml("config.yaml")
        config._raw["models"]["xgboost"]["params"]["n_estimators"] = 10
        config._raw["models"]["xgboost"]["params"]["early_stopping_rounds"] = 5
        return config

    @pytest.fixture
    def model(self, config):
        return XGBoostModel(config)

    @pytest.fixture
    def sample_data(self):
        """Create sample training data."""
        np.random.seed(42)
        n = 200
        X = pd.DataFrame({
            f"feature_{i}": np.random.randn(n) for i in range(10)
        })
        y = pd.DataFrame({
            "pm25": np.random.uniform(10, 100, n),
            "pm10": np.random.uniform(20, 150, n),
            "no2": np.random.uniform(5, 80, n),
        })
        return X, y

    def test_fit_predict(self, model, sample_data):
        """Test basic fit and predict."""
        X, y = sample_data

        # Split
        X_train, X_val = X.iloc[:150], X.iloc[150:]
        y_train, y_val = y.iloc[:150], y.iloc[150:]

        model.fit(X_train, y_train, X_val, y_val, verbose=False)

        preds = model.predict(X_val)

        assert "pm25" in preds.columns
        assert "pm10" in preds.columns
        assert len(preds) == len(X_val)

    def test_feature_importance(self, model, sample_data):
        """Test feature importance extraction."""
        X, y = sample_data

        model.fit(X, y, verbose=False)

        fi = model.get_feature_importance("pm25")

        assert "feature" in fi.columns
        assert "importance" in fi.columns
        assert len(fi) == len(X.columns)


class TestLightGBMModel:
    """Tests for LightGBMModel."""

    @pytest.fixture
    def config(self):
        config = Config.from_yaml("config.yaml")
        config._raw["models"]["lightgbm"]["params"]["n_estimators"] = 10
        config._raw["models"]["lightgbm"]["params"]["early_stopping_rounds"] = 5
        config._raw["training"]["hardware"]["use_gpu"] = False  # Disable GPU for tests
        return config

    @pytest.fixture
    def model(self, config):
        return LightGBMModel(config)

    @pytest.fixture
    def sample_data(self):
        """Create sample training data."""
        np.random.seed(42)
        n = 200
        X = pd.DataFrame({
            f"feature_{i}": np.random.randn(n) for i in range(10)
        })
        y = pd.DataFrame({
            "pm25": np.random.uniform(10, 100, n),
            "pm10": np.random.uniform(20, 150, n),
        })
        return X, y

    def test_fit_predict(self, model, sample_data):
        """Test basic fit and predict."""
        X, y = sample_data

        X_train, X_val = X.iloc[:150], X.iloc[150:]
        y_train, y_val = y.iloc[:150], y.iloc[150:]

        model.fit(X_train, y_train, X_val, y_val, verbose=False)

        preds = model.predict(X_val)

        assert "pm25" in preds.columns
        assert len(preds) == len(X_val)


class TestBaselineModels:
    """Tests for baseline models."""

    @pytest.fixture
    def sample_data(self):
        """Create sample data with datetime index."""
        dates = pd.date_range("2023-01-01", periods=200, freq="1H")
        X = pd.DataFrame(index=dates)
        y = pd.DataFrame({
            "pm25": np.random.uniform(10, 100, 200),
            "pm10": np.random.uniform(20, 150, 200),
        }, index=dates)
        return X, y

    def test_persistence_model(self, sample_data):
        """Test PersistenceModel."""
        X, y = sample_data

        X_train, X_test = X.iloc[:150], X.iloc[150:]
        y_train, y_test = y.iloc[:150], y.iloc[150:]

        model = PersistenceModel()
        model.fit(X_train, y_train)

        preds = model.predict(X_test)

        # Should predict last training value
        assert preds["pm25"].iloc[0] == y_train["pm25"].iloc[-1]
        assert len(preds) == len(X_test)

    def test_seasonal_naive_model(self, sample_data):
        """Test SeasonalNaiveModel."""
        X, y = sample_data

        X_train, X_test = X.iloc[:150], X.iloc[150:]
        y_train, y_test = y.iloc[:150], y.iloc[150:]

        model = SeasonalNaiveModel(seasonality=24)
        model.fit(X_train, y_train)

        preds = model.predict(X_test)

        assert len(preds) == len(X_test)

    def test_linear_trend_model(self, sample_data):
        """Test LinearTrendModel."""
        X, y = sample_data

        X_train, X_test = X.iloc[:150], X.iloc[150:]
        y_train, y_test = y.iloc[:150], y.iloc[150:]

        model = LinearTrendModel()
        model.fit(X_train, y_train)

        preds = model.predict(X_test)

        assert len(preds) == len(X_test)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])