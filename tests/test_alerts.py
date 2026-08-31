from src.alerts import active_alerts

THRESHOLDS = {
    "pue_warning": 1.6,
    "wue_warning_l_per_kwh": 1.8,
    "carbon_intensity_high_g_per_kwh": 350,
    "energy_peak_percentile": 0.95,
}


def test_empty_data_alert(sample_data):
    assert active_alerts(sample_data.iloc[0:0], THRESHOLDS) == [
        "No data in selected range"
    ]


def test_configured_resource_alerts(sample_data):
    data = sample_data.copy()
    last = data.sort_values("timestamp").index[-1]
    data.loc[last, ["pue", "wue_l_per_kwh", "grid_carbon_intensity_g_per_kwh"]] = [
        2.0,
        3.0,
        500,
    ]
    data.loc[last, ["total_energy_kwh", "water_consumption_l", "cooling_demand_kw"]] = (
        10_000
    )
    alerts = active_alerts(data, THRESHOLDS)
    assert any("PUE" in alert for alert in alerts)
    assert any("Water consumption" in alert for alert in alerts)
    assert any("Cooling demand" in alert for alert in alerts)
