"""Research-ready figures generated from executed pipeline outputs."""

from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd

from src.explainability import feature_importance


def create_forecast_figures(target: str, output="reports/figures") -> list[Path]:
    """Create prediction, residual and non-causal importance figures for a target."""
    data = pd.read_csv(f"reports/evaluation/test_predictions_{target}.csv")
    out = Path(output)
    out.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    plots = [
        (
            "actual_vs_predicted",
            lambda ax: ax.scatter(data.actual, data.predicted, s=4, alpha=0.35),
            "Actual",
            "Predicted",
        ),
        (
            "residual_distribution",
            lambda ax: ax.hist(data.residual, bins=50),
            "Residual",
            "Frequency",
        ),
        (
            "residual_vs_predicted",
            lambda ax: ax.scatter(data.predicted, data.residual, s=4, alpha=0.35),
            "Predicted",
            "Residual",
        ),
    ]
    for name, plotter, xlabel, ylabel in plots:
        fig, ax = plt.subplots(figsize=(8, 5))
        plotter(ax)
        ax.set(
            title=f"{target}: {name.replace('_', ' ').title()}",
            xlabel=xlabel,
            ylabel=ylabel,
        )
        fig.tight_layout()
        path = out / f"{target}_{name}.png"
        fig.savefig(path, dpi=200)
        plt.close(fig)
        paths.append(path)
    timeline = data.tail(336)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(pd.to_datetime(timeline.timestamp), timeline.actual, label="Actual")
    ax.plot(pd.to_datetime(timeline.timestamp), timeline.predicted, label="Predicted")
    ax.legend()
    ax.set(
        title=f"{target}: Held-out prediction timeline",
        xlabel="Timestamp",
        ylabel=target,
    )
    fig.tight_layout()
    path = out / f"{target}_prediction_timeline.png"
    fig.savefig(path, dpi=200)
    plt.close(fig)
    paths.append(path)
    artifact = joblib.load(f"models/forecasting/{target}.joblib")
    importance = feature_importance(artifact).head(15).sort_values("importance")
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.barh(importance.feature, importance.importance)
    ax.set(
        title=f"{target}: Predictive feature importance",
        xlabel="Model importance (association, not causation)",
    )
    fig.tight_layout()
    path = out / f"{target}_feature_importance.png"
    fig.savefig(path, dpi=200)
    plt.close(fig)
    paths.append(path)
    return paths


def create_monitoring_figures(
    data: pd.DataFrame, events: pd.DataFrame, output="reports/figures"
) -> list[Path]:
    """Create anomaly, KPI trend, and correlation figures from telemetry."""
    out = Path(output)
    out.mkdir(parents=True, exist_ok=True)
    paths = []
    daily = data.set_index("timestamp").resample("D").mean(numeric_only=True)
    for metric, unit in [
        ("pue", "ratio"),
        ("wue_l_per_kwh", "L/kWh IT"),
        ("carbon_emissions_kg", "kg CO2e/hour"),
    ]:
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(daily.index, daily[metric])
        ax.set(title=f"Daily {metric} trend", xlabel="Date", ylabel=unit)
        fig.tight_layout()
        path = out / f"{metric}_trend.png"
        fig.savefig(path, dpi=200)
        plt.close(fig)
        paths.append(path)
    fig, ax = plt.subplots(figsize=(10, 4))
    sample = data.iloc[::24]
    ax.plot(sample.timestamp, sample.total_energy_kwh, label="Energy")
    ax.scatter(
        events.timestamp,
        events.total_energy_kwh,
        color="red",
        s=12,
        label="Detected anomaly",
    )
    ax.legend()
    ax.set(
        title="Detected anomaly timeline",
        xlabel="Timestamp",
        ylabel="Facility energy (kWh)",
    )
    fig.tight_layout()
    path = out / "anomaly_timeline.png"
    fig.savefig(path, dpi=200)
    plt.close(fig)
    paths.append(path)
    columns = [
        "it_load_kw",
        "it_energy_kwh",
        "total_energy_kwh",
        "external_temperature_c",
        "cooling_demand_kw",
        "cooling_energy_kwh",
        "water_consumption_l",
        "carbon_emissions_kg",
    ]
    corr = data[columns].corr()
    fig, ax = plt.subplots(figsize=(9, 7))
    image = ax.imshow(corr, vmin=-1, vmax=1, cmap="RdBu_r")
    ax.set_xticks(range(len(columns)), columns, rotation=60, ha="right")
    ax.set_yticks(range(len(columns)), columns)
    fig.colorbar(image, ax=ax, label="Pearson correlation")
    ax.set_title("Synthetic telemetry correlations (not causal effects)")
    fig.tight_layout()
    path = out / "correlation_heatmap.png"
    fig.savefig(path, dpi=200)
    plt.close(fig)
    paths.append(path)
    return paths


def create_research_figures(output="reports/figures") -> list[Path]:
    """Create figures for every target with an executed prediction output."""
    paths: list[Path] = []
    for prediction in Path("reports/evaluation").glob("test_predictions_*.csv"):
        paths.extend(
            create_forecast_figures(
                prediction.stem.removeprefix("test_predictions_"), output
            )
        )
    return paths
