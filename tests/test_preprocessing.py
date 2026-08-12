import pandas as pd
import pytest
from src.preprocessing import clean_data, chronological_split
from src.feature_engineering import create_features


def test_cleaning_deduplicates_and_clips(sample_data):
    dirty = pd.concat([sample_data, sample_data.iloc[[0]]])
    dirty.loc[1, "water_consumption_l"] = -1
    result = clean_data(dirty)
    assert not result.duplicated(["site", "timestamp"]).any()
    assert result.water_consumption_l.min() >= 0


def test_time_split_and_past_only_features(sample_data):
    train, val, test = chronological_split(sample_data)
    assert train.timestamp.max() <= val.timestamp.min() <= test.timestamp.min()
    featured = create_features(sample_data)
    assert {
        "total_energy_kwh_lag_168",
        "total_energy_kwh_roll_mean_24",
        "hour_sin",
    } <= set(featured)


def test_invalid_target_and_dates(sample_data):
    with pytest.raises(ValueError):
        create_features(sample_data, "missing")
    dirty = sample_data.copy()
    dirty.loc[0, "timestamp"] = "invalid"
    assert len(clean_data(dirty)) == len(dirty) - 1
