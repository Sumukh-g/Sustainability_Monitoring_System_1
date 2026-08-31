"""Execute evaluation, persist evidence, and write the final results summary."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import yaml

from src.anomaly_detection import detect_anomalies
from src.data_loader import load_data, validate_data
from src.evaluation import create_monitoring_figures, create_research_figures
from src.recommendations import generate_recommendations
from src.sustainability_metrics import sustainability_score


def execute_audit() -> dict:
    """Run post-training research evaluation and persist every calculated result."""
    evaluation = Path("reports/evaluation")
    evaluation.mkdir(parents=True, exist_ok=True)
    data = load_data()
    quality = validate_data(data)
    quality.to_csv(evaluation / "data_quality_report.csv", index=False)
    _, events, _, anomaly = detect_anomalies(
        data, model_path="models/anomaly_detection/isolation_forest.joblib"
    )
    events.to_csv(evaluation / "anomaly_events.csv", index=False)
    (evaluation / "anomaly_metrics.json").write_text(json.dumps(anomaly, indent=2))
    pd.DataFrame(
        [{k: v for k, v in anomaly.items() if k != "confusion_matrix"}]
    ).to_csv(evaluation / "anomaly_metrics.csv", index=False)
    matrix = anomaly["confusion_matrix"]
    fig, ax = plt.subplots(figsize=(5, 4))
    image = ax.imshow(matrix, cmap="Blues")
    for row in range(2):
        for column in range(2):
            ax.text(column, row, matrix[row][column], ha="center", va="center")
    ax.set(
        xticks=[0, 1],
        yticks=[0, 1],
        xticklabels=["Normal", "Anomaly"],
        yticklabels=["Normal", "Anomaly"],
        xlabel="Predicted",
        ylabel="Synthetic ground truth",
        title="Isolation Forest confusion matrix",
    )
    fig.colorbar(image, ax=ax)
    fig.tight_layout()
    fig.savefig("reports/figures/anomaly_confusion_matrix.png", dpi=200)
    plt.close(fig)
    correlations = {
        "it_load_vs_it_energy": data.it_load_kw.corr(data.it_energy_kwh),
        "it_load_vs_facility_energy": data.it_load_kw.corr(data.total_energy_kwh),
        "temperature_vs_cooling_demand": data.external_temperature_c.corr(
            data.cooling_demand_kw
        ),
        "cooling_demand_vs_cooling_energy": data.cooling_demand_kw.corr(
            data.cooling_energy_kwh
        ),
        "cooling_demand_vs_water": data.cooling_demand_kw.corr(
            data.water_consumption_l
        ),
        "facility_energy_vs_carbon": data.total_energy_kwh.corr(
            data.carbon_emissions_kg
        ),
        "carbon_intensity_vs_carbon": data.grid_carbon_intensity_g_per_kwh.corr(
            data.carbon_emissions_kg
        ),
        "utilisation_vs_workload": data.server_utilisation_pct.corr(
            data.compute_workload_units
        ),
    }
    pd.DataFrame([correlations]).T.rename(columns={0: "pearson_correlation"}).to_csv(
        evaluation / "data_realism_correlations.csv"
    )
    data.groupby("site").agg(
        rows=("timestamp", "size"),
        start=("timestamp", "min"),
        end=("timestamp", "max"),
        labelled_anomalies=("anomaly_ground_truth", "sum"),
    ).to_csv(evaluation / "dataset_summary.csv")
    kpis = pd.DataFrame(
        [
            {
                "total_energy_kwh_sum": data.total_energy_kwh.sum(),
                "total_energy_kwh_mean": data.total_energy_kwh.mean(),
                "water_consumption_l_sum": data.water_consumption_l.sum(),
                "water_consumption_l_mean": data.water_consumption_l.mean(),
                "carbon_emissions_kg_sum": data.carbon_emissions_kg.sum(),
                "carbon_emissions_kg_mean": data.carbon_emissions_kg.mean(),
                "pue_mean": data.pue.mean(),
                "pue_median": data.pue.median(),
                "wue_mean": data.wue_l_per_kwh.mean(),
                "wue_median": data.wue_l_per_kwh.median(),
                "cue_mean": data.cue_kg_per_kwh.mean(),
                "cue_median": data.cue_kg_per_kwh.median(),
            }
        ]
    )
    kpis.to_csv(evaluation / "sustainability_kpi_summary.csv", index=False)
    _, thresholds = yaml.safe_load(
        Path("config/settings.yaml").read_text()
    ), yaml.safe_load(Path("config/thresholds.yaml").read_text())
    recommendations = generate_recommendations(data, thresholds)
    recommendations.to_csv(evaluation / "recommendations.csv", index=False)
    create_research_figures()
    create_monitoring_figures(data, events)
    comparison = pd.read_csv(evaluation / "model_comparison.csv")
    score, label = sustainability_score(data)
    sections = []
    for target, group in comparison.groupby("Target"):
        baseline = group[group.Model == "Previous day baseline"].iloc[0]
        selected = group[group.Selected.astype(str).str.lower() == "true"].iloc[0]
        sections.append(
            f"### {target}\n- Baseline RMSE: {baseline.RMSE:.4f}\n- Best persisted ML model: {selected.Model}\n- MAE: {selected.MAE:.4f}\n- RMSE: {selected.RMSE:.4f}\n- R²: {selected.R2:.4f}\n- RMSE improvement over baseline: {(baseline.RMSE-selected.RMSE)/baseline.RMSE*100:.2f}%"
        )
    text = f"""# Final Executed Results

## Dataset
- Sites: {data.site.nunique()}
- Rows: {len(data):,}
- Time period: {data.timestamp.min()} to {data.timestamp.max()}
- Interval: hourly
- Labelled anomalies: {int(data.anomaly_ground_truth.sum())}

## Forecasting
{chr(10).join(sections)}

## Anomaly Detection
- Detected anomalies: {anomaly['detected']}
- Precision: {anomaly['precision']:.4f}
- Recall: {anomaly['recall']:.4f}
- F1: {anomaly['f1']:.4f}
- TP / FP / FN / TN: {anomaly['true_positive']} / {anomaly['false_positive']} / {anomaly['false_negative']} / {anomaly['true_negative']}

Synthetic labels are explicit and therefore make evaluation easier than ambiguous, incomplete real-world fault records.

## Sustainability
- Mean / median PUE: {data.pue.mean():.4f} / {data.pue.median():.4f}
- Mean / median WUE: {data.wue_l_per_kwh.mean():.4f} / {data.wue_l_per_kwh.median():.4f} L/kWh IT
- Mean / median CUE: {data.cue_kg_per_kwh.mean():.4f} / {data.cue_kg_per_kwh.median():.4f} kg CO2e/kWh IT
- Total facility energy: {data.total_energy_kwh.sum():,.2f} kWh
- Total water: {data.water_consumption_l.sum():,.2f} L
- Total carbon: {data.carbon_emissions_kg.sum():,.2f} kg CO2e
- Project-specific sustainability score: {score:.2f}/100 ({label})

## Limitations
Results use synthetic relationships and injected labels; they do not demonstrate real-facility savings, causal effects, or autonomous-control safety. Recommendation effectiveness requires qualified operational validation.
"""
    Path("reports/FINAL_RESULTS.md").write_text(text)
    return {
        "rows": len(data),
        "quality_passed": bool(quality.passed.all()),
        "anomaly": anomaly,
        "recommendations": len(recommendations),
    }


if __name__ == "__main__":
    print(json.dumps(execute_audit(), indent=2))
