import pytest
from src.anomaly_detection import detect_anomalies


def test_anomaly_output_and_metrics(sample_data):
    enriched, events, model, metrics = detect_anomalies(sample_data, 0.05)
    assert {"detected_anomaly", "anomaly_score"} <= set(enriched)
    assert {"severity", "affected_metric", "suggested_action"} <= set(events)
    assert 0 <= metrics["f1"] <= 1


def test_empty_anomalies_rejected(sample_data):
    with pytest.raises(ValueError):
        detect_anomalies(sample_data.iloc[0:0])
