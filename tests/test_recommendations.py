from src.recommendations import generate_recommendations

THRESHOLDS = {
    "pue_warning": 1.1,
    "wue_warning_l_per_kwh": 0.1,
    "cooling_efficiency_low": 10,
    "server_utilisation_low_pct": 99,
    "carbon_intensity_high_g_per_kwh": 1,
    "energy_peak_percentile": 0.95,
}


def test_rules_are_structured_and_data_backed(sample_data):
    rec = generate_recommendations(sample_data, THRESHOLDS, predicted_peak=9999)
    assert len(rec) >= 5
    assert {
        "triggered_by",
        "current_value",
        "reference_value",
        "priority",
        "confidence",
    } <= set(rec)


def test_empty_input(sample_data):
    assert generate_recommendations(sample_data.iloc[0:0], THRESHOLDS).empty
