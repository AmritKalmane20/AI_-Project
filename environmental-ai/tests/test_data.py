"""
Tests for data module.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path

from environmental_ai.data.preprocess import DataPreprocessor
from environmental_ai.data.features import FeatureEngineer
from environmental_ai.config import Config


class TestDataPreprocessor:
    """Tests for DataPreprocessor."""

    @pytest.fixture
    def config(self):
        return Config.from_yaml("config.yaml")

    @pytest.fixture
    def preprocessor(self, config):
        return DataPreprocessor(config)

    @pytest.fixture
    def sample_aq_data(self):
        """Create sample air quality data."""
        dates = pd.date_range("2023-01-01", periods=100, freq="1H")
        return pd.DataFrame({
            "datetime": dates,
            "pm25": np.random.uniform(10, 100, 100),
            "pm10": np.random.uniform(20, 150, 100),
            "no2": np.random.uniform(5, 80, 100),
            "location_id": "test_station",
            "city": "Test City",
            "country": "TC",
        }).set_index("datetime")

    @pytest.fixture
    def sample_weather_data(self):
        """Create sample weather data."""
        dates = pd.date_range("2023-01-01", periods=100, freq="1H")
        return pd.DataFrame({
            "datetime": dates,
            "temperature_2m": np.random.uniform(-10, 35, 100),
            "relative_humidity_2m": np.random.uniform(20, 90, 100),
            "wind_speed_10m": np.random.uniform(0, 15, 100),
            "wind_direction_10m": np.random.uniform(0, 360, 100),
            "surface_pressure": np.random.uniform(990, 1030, 100),
            "precipitation": np.random.uniform(0, 10, 100),
        }).set_index("datetime")

    def test_clean_aq_data(self, preprocessor, sample_aq_data):
        """Test AQ data cleaning."""
        # Add some negative values
        sample_aq_data.loc[sample_aq_data.index[0], "pm25"] = -5

        cleaned = preprocessor.clean_aq_data(sample_aq_data)

        # Negative values should be NaN
        assert pd.isna(cleaned.loc[cleaned.index[0], "pm25"])

    def test_clean_weather_data(self, preprocessor, sample_weather_data):
        """Test weather data cleaning."""
        # Add out of bounds values
        sample_weather_data.loc[sample_weather_data.index[0], "temperature_2m"] = 100

        cleaned = preprocessor.clean_weather_data(sample_weather_data)

        # Out of bounds should be NaN
        assert pd.isna(cleaned.loc[cleaned.index[0], "temperature_2m"])

    def test_resample_data(self, preprocessor, sample_aq_data):
        """Test resampling."""
        resampled = preprocessor.resample_data(sample_aq_data, "30min")
        assert len(resampled) > len(sample_aq_data)

    def test_align_data(self, preprocessor, sample_aq_data, sample_weather_data):
        """Test data alignment."""
        aligned = preprocessor.align_data(sample_aq_data, sample_weather_data)
        assert len(aligned) > 0
        assert "pm25" in aligned.columns
        assert "temperature_2m" in aligned.columns

    def test_handle_missing_data(self, preprocessor, sample_aq_data):
        """Test missing data handling."""
        # Add NaN values
        sample_aq_data.loc[sample_aq_data.index[10:15], "pm25"] = np.nan

        handled = preprocessor.handle_missing_data(sample_aq_data)

        # Should have fewer NaN values
        assert handled["pm25"].isna().sum() < sample_aq_data["pm25"].isna().sum()

    def test_calculate_aqi(self, preprocessor, sample_aq_data):
        """Test AQI calculation."""
        with_aqi = preprocessor.calculate_aqi(sample_aq_data)

        assert "aqi" in with_aqi.columns
        assert "pm25_aqi" in with_aqi.columns
        assert with_aqi["aqi"].notna().any()


class TestFeatureEngineer:
    """Tests for FeatureEngineer."""

    @pytest.fixture
    def config(self):
        return Config.from_yaml("config.yaml")

    @pytest.fixture
    def engineer(self, config):
        return FeatureEngineer(config)

    @pytest.fixture
    def sample_data(self):
        """Create sample data with datetime index."""
        dates = pd.date_range("2023-01-01", periods=500, freq="1H")
        return pd.DataFrame({
            "pm25": np.random.uniform(10, 100, 500),
            "pm10": np.random.uniform(20, 150, 500),
            "no2": np.random.uniform(5, 80, 500),
            "so2": np.random.uniform(2, 50, 500),
            "co": np.random.uniform(0.1, 5, 500),
            "o3": np.random.uniform(10, 120, 500),
            "aqi": np.random.uniform(20, 200, 500),
            "temperature_2m": np.random.uniform(-10, 35, 500),
            "relative_humidity_2m": np.random.uniform(20, 90, 500),
            "wind_speed_10m": np.random.uniform(0, 15, 500),
            "wind_direction_10m": np.random.uniform(0, 360, 500),
            "surface_pressure": np.random.uniform(990, 1030, 500),
            "precipitation": np.random.uniform(0, 10, 500),
        }, index=dates)

    def test_create_temporal_features(self, engineer, sample_data):
        """Test temporal feature creation."""
        result = engineer.create_temporal_features(sample_data)

        assert "hour" in result.columns
        assert "dayofweek" in result.columns
        assert "month" in result.columns
        assert "hour_sin" in result.columns
        assert "hour_cos" in result.columns
        assert "is_weekend" in result.columns

    def test_create_lag_features(self, engineer, sample_data):
        """Test lag feature creation."""
        result = engineer.create_lag_features(sample_data, target_cols=["pm25"])

        assert "pm25_lag_1" in result.columns
        assert "pm25_lag_24" in result.columns

    def test_create_rolling_features(self, engineer, sample_data):
        """Test rolling feature creation."""
        result = engineer.create_rolling_features(sample_data, target_cols=["pm25"])

        assert "pm25_roll_24_mean" in result.columns
        assert "pm25_roll_24_std" in result.columns

    def test_create_weather_interactions(self, engineer, sample_data):
        """Test weather interaction features."""
        result = engineer.create_weather_interactions(sample_data)

        assert "temp_humidity" in result.columns
        assert "wind_pm25" in result.columns
        assert "wind_u" in result.columns
        assert "wind_v" in result.columns

    def test_create_all_features(self, engineer, sample_data):
        """Test full feature engineering pipeline."""
        result = engineer.create_all_features(sample_data, country="US")

        # Should have many more features
        assert len(result.columns) > len(sample_data.columns) * 5
        assert len(engineer.created_features) > 100

    def test_get_feature_columns(self, engineer, sample_data):
        """Test feature column extraction."""
        result = engineer.create_all_features(sample_data)
        feature_cols = engineer.get_feature_columns(result, exclude_targets=True)

        # Should not include targets
        targets = ["pm25", "pm10", "no2", "so2", "co", "o3", "aqi"]
        for target in targets:
            assert target not in feature_cols


class TestConfig:
    """Tests for configuration."""

    def test_load_config(self):
        """Test loading config from YAML."""
        config = Config.from_yaml("config.yaml")

        assert config.project_name == "environmental-ai-aq-prediction"
        assert config.version == "1.0.0"
        assert len(config.targets) > 0

    def test_config_values(self):
        """Test config value access."""
        config = Config.from_yaml("config.yaml")

        # Check nested access
        assert config.get("models.xgboost.params.n_estimators") == 2000
        assert config.get("models.lightgbm.params.max_depth") == 8
        assert config.get("training.cv.n_splits") == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])