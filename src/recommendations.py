"""Data-linked deterministic recommendation decision support."""

import pandas as pd


def generate_recommendations(
    data: pd.DataFrame, thresholds: dict, predicted_peak: float | None = None
) -> pd.DataFrame:
    """Generate structured actions only for conditions evidenced in selected data."""
    columns = [
        "title",
        "triggered_by",
        "metric",
        "current_value",
        "reference_value",
        "severity",
        "priority",
        "recommended_action",
        "expected_benefit",
        "confidence",
        "explanation",
    ]
    if data.empty:
        return pd.DataFrame(columns=columns)
    current = data.mean(numeric_only=True)
    rec = []

    def add(
        title,
        trigger,
        metric,
        value,
        reference,
        severity,
        priority,
        action,
        benefit,
        confidence,
        explanation,
    ):
        rec.append(
            dict(
                zip(
                    columns,
                    [
                        title,
                        trigger,
                        metric,
                        round(float(value), 3),
                        reference,
                        severity,
                        priority,
                        action,
                        benefit,
                        confidence,
                        explanation,
                    ],
                )
            )
        )

    if current.pue > thresholds["pue_warning"]:
        add(
            "Reduce facility overhead",
            "Mean PUE above threshold",
            "PUE",
            current.pue,
            thresholds["pue_warning"],
            "High",
            "High Priority",
            "Inspect cooling set points, airflow containment, and non-IT loads.",
            "Lower non-IT energy if the diagnosed issue is remediated.",
            0.90,
            "The selected period's measured PUE exceeds the configured reference.",
        )
    if current.wue_l_per_kwh > thresholds["wue_warning_l_per_kwh"]:
        add(
            "Investigate water intensity",
            "Mean WUE above threshold",
            "WUE (L/kWh)",
            current.wue_l_per_kwh,
            thresholds["wue_warning_l_per_kwh"],
            "High",
            "High Priority",
            "Inspect cooling tower cycles and water circuit for leakage.",
            "Potential water avoidance; magnitude requires engineering validation.",
            0.88,
            "Measured water per IT kWh is above the configured reference.",
        )
    if current.cooling_efficiency < thresholds["cooling_efficiency_low"]:
        add(
            "Restore cooling efficiency",
            "Low mean cooling COP",
            "Cooling efficiency",
            current.cooling_efficiency,
            thresholds["cooling_efficiency_low"],
            "High",
            "Immediate",
            "Review plant, filters, airflow and temperature set points.",
            "Potential cooling-energy reduction after confirmed repair.",
            0.85,
            "Cooling efficiency is below its configured reference.",
        )
    if current.server_utilisation_pct < thresholds["server_utilisation_low_pct"]:
        add(
            "Consolidate workloads",
            "Low mean utilisation",
            "Server utilisation (%)",
            current.server_utilisation_pct,
            thresholds["server_utilisation_low_pct"],
            "Medium",
            "Medium Priority",
            "Consolidate suitable workloads and idle unnecessary servers after resilience review.",
            "Reduced idle IT energy.",
            0.82,
            "Active capacity appears under-utilised in the selected period.",
        )
    if (
        current.grid_carbon_intensity_g_per_kwh
        > thresholds["carbon_intensity_high_g_per_kwh"]
    ):
        add(
            "Use lower-carbon windows",
            "High grid carbon intensity",
            "Grid intensity (g/kWh)",
            current.grid_carbon_intensity_g_per_kwh,
            thresholds["carbon_intensity_high_g_per_kwh"],
            "Medium",
            "Medium Priority",
            "Shift flexible compute to forecast lower-carbon windows where constraints allow.",
            "Lower location-based emissions for flexible work.",
            0.80,
            "Observed mean grid intensity is above the configured threshold.",
        )
    if predicted_peak is not None and predicted_peak > data.total_energy_kwh.quantile(
        thresholds["energy_peak_percentile"]
    ):
        add(
            "Prepare for forecast energy peak",
            "Forecast exceeds historical percentile",
            "Energy (kWh)",
            predicted_peak,
            data.total_energy_kwh.quantile(thresholds["energy_peak_percentile"]),
            "High",
            "High Priority",
            "Pre-plan cooling and defer non-critical workloads if operationally safe.",
            "Peak-demand avoidance where scheduling is feasible.",
            0.75,
            "Modelled demand exceeds the selected period's peak reference.",
        )
    return pd.DataFrame(rec, columns=columns)
