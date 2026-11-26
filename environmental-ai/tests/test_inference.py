"""
Tests for inference module.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from environmental_ai.inference.predict import Predictor, predict_batch
from environmental_ai.config import Config


class TestPredictor:
    """Tests for Predictor class."""

    @pytest.fixture
    def config(self):
        return Config.from_yaml("config.yaml")

    @pytest.fixture
    def predictor(self, config):
        """Create predictor with mocked models."""
        predictor = Predictor(config)

        # Mock models
        predictor.xgboost_model = Mock()
        predictor.xgboost_model.feature_cols = ["feature_1", "feature_2"]
        predictor.xgboost_model.predict.return_value = pd.DataFrame({
            "pm25": [10.0, 11.0],
            "pm10": [20.0, 21.0],
        })

        predictor.lightgbm_model = Mock()
        predictor.lightgbm_model.feature_cols = ["feature_1", "feature_2"]
        predictor.lightgbm_model.predict.return_value = pd.DataFrame({
            "pm25": [10.5, 11.5],
            "pm10": [20.5, 21.5],
        })

        predictor.ensemble = Mock()
        predictor.ensemble.feature_cols = ["feature_1", "feature_2"]
        predictor.ensemble.predict.return_value = pd.DataFrame({
            "pm25": [10.2, 11.2],
            "pm10": [20.2, 21.2],
        })
        predictor.ensemble.predict_with_uncertainty.return_value = {
            "pm25": pd.DataFrame({
                "q5": [9.0, 10.0],
                "q50": [10.2, 11.2],
                "q95": [11.5, 12.5],
            })
        }

        predictor.feature_cols = ["feature_1", "feature_2"]
        predictor.is_loaded = True

        return predictor

    @pytest.fixture
    def sample_features(self):
        """Create sample feature DataFrame."""
        return pd.DataFrame({
            "feature_1": [1.0, 2.0],
            "feature_2": [3.0, 4.0],
            "pm25": [10.0, 11.0],  # target column (should be excluded)
        })

    def test_prepare_features(self, predictor, sample_features):
        """Test feature preparation."""
        X = predictor.prepare_features(sample_features)

        assert "feature_1" in X.columns
        assert "feature_2" in X.columns
        assert "pm25" not in X.columns  # Target should be excluded
        assert len(X) == 2

    def test_predict_ensemble(self, predictor, sample_features):
        """Test ensemble prediction."""
        preds = predictor.predict(sample_features, model_name="ensemble")

        assert "pm25" in preds.columns
        assert "pm10" in preds.columns
        assert len(preds) == 2

    def test_predict_xgboost(self, predictor, sample_features):
        """Test XGBoost prediction."""
        preds = predictor.predict(sample_features, model_name="xgboost")

        assert "pm25" in preds.columns
        predictor.xgboost_model.predict.assert_called_once()

    def test_predict_lightgbm(self, predictor, sample_features):
        """Test LightGBM prediction."""
        preds = predictor.predict(sample_features, model_name="lightgbm")

        assert "pm25" in preds.columns
        predictor.lightgbm_model.predict.assert_called_once()

    def test_predict_with_uncertainty(self, predictor, sample_features):
        """Test prediction with uncertainty."""
        preds, uncertainty = predictor.predict(sample_features, model_name="ensemble", return_uncertainty=True)

        assert "pm25" in preds.columns
        assert "pm25" in uncertainty
        assert "q5" in uncertainty["pm25"].columns
        assert "q50" in uncertainty["pm25"].columns
        assert "q95" in uncertainty["pm25"].columns


class TestPredictBatch:
    """Tests for batch prediction function."""

    @pytest.fixture
    def config(self):
        return Config.from_yaml("config.yaml")

    def test_predict_batch_creates_output(self, config, tmp_path):
        """Test that predict_batch creates output file."""
        # Create mock input data
        input_df = pd.DataFrame({
            "feature_1": np.random.randn(10),
            "feature_2": np.random.randn(10),
        })

        input_path = tmp_path / "input.parquet"
        output_path = tmp_path / "output.parquet"
        input_df.to_parquet(input_path)

        # Mock Predictor
        with patch("environmental_ai.inference.predict.Predictor") as MockPredictor:
            mock_predictor = MockPredictor.return_value
            mock_predictor.load_models.return_value = mock_predictor
            mock_predictor.prepare_features.return_value = input_df
            mock_predictor.predict.return_value = pd.DataFrame({
                "pm25": np.random.uniform(10, 50, 10),
                "pm10": np.random.uniform(20, 100, 10),
            })

            result = predict_batch(config, input_path, output_path)

            assert output_path.exists()
            assert len(result) == 10
            assert "pm25" in result.columns


class TestConfigIntegration:
    """Tests for config integration."""

    def test_config_has_required_keys(self):
        """Test that config has all required keys."""
        config = Config.from_yaml("config.yaml")

        # Check main sections
        assert hasattr(config, "project_name")
        assert hasattr(config, "version")
        assert hasattr(config, "targets")
        assert hasattr(config, "feature_cols")

        # Check model configs
        assert config.get("models.xgboost.enabled") is True
        assert config.get("models.lightgbm.enabled") is True
        assert config.get("models.transformer.enabled") is True
        assert config.get("models.ensemble.enabled") is True

    def test_target_cities(self):
        """Test that target cities are configured."""
        config = Config.from_yaml("config.yaml")

        cities = [t["city"] for t in config.targets]
        assert "Delhi" in cities
        assert "Beijing" in cities
        assert "Los Angeles" in cities
        assert "London" in cities


if __name__ == "__main__":
    pytest.main([__file__, "-v"])