"""Chronological baseline/candidate training, persistence, evaluation, and forecasts."""

from __future__ import annotations
import json
import time
from datetime import datetime, timezone
from pathlib import Path
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from src.data_loader import load_data
from src.feature_engineering import create_features

BASE_FEATURES = [
    "external_temperature_c",
    "humidity_pct",
    "it_load_kw",
    "server_utilisation_pct",
    "cooling_efficiency",
    "hour_sin",
    "hour_cos",
    "month_sin",
    "month_cos",
    "weekday",
    "weekend",
]


def metric_row(
    name: str, target: str, actual, predicted, training_time=0.0, prediction_time=0.0
) -> dict:
    return {
        "Model": name,
        "Target": target,
        "MAE": float(mean_absolute_error(actual, predicted)),
        "RMSE": float(mean_squared_error(actual, predicted) ** 0.5),
        "R2": float(r2_score(actual, predicted)),
        "Training Time": training_time,
        "Prediction Time": prediction_time,
    }


def train_models(
    data: pd.DataFrame,
    target: str = "total_energy_kwh",
    output_dir: str | Path = "models",
) -> tuple[pd.DataFrame, dict]:
    """Compare previous-day baseline and three regressors on the final chronological 20%."""
    featured = create_features(data, target)
    lag_features = [f"{target}_lag_{x}" for x in (1, 24, 48, 168)] + [
        f"{target}_roll_mean_{x}" for x in (3, 6, 24, 168)
    ]
    features = BASE_FEATURES + lag_features
    split = int(len(featured) * 0.8)
    train, test = featured.iloc[:split], featured.iloc[split:]
    X_train, y_train = train[features], train[target]
    X_test, y_test = test[features], test[target]
    predictions = {"Previous day baseline": X_test[f"{target}_lag_24"].to_numpy()}
    results = [
        metric_row(
            "Previous day baseline",
            target,
            y_test,
            predictions["Previous day baseline"],
        )
    ]
    candidates = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(
            n_estimators=80,
            max_depth=14,
            min_samples_leaf=2,
            n_jobs=-1,
            random_state=42,
        ),
        "HistGradientBoosting": HistGradientBoostingRegressor(
            max_iter=140, l2_regularization=0.1, random_state=42
        ),
    }
    fitted = {}
    for name, model in candidates.items():
        start = time.perf_counter()
        model.fit(X_train, y_train)
        fit_time = time.perf_counter() - start
        start = time.perf_counter()
        pred = model.predict(X_test)
        pred_time = time.perf_counter() - start
        predictions[name] = pred
        results.append(metric_row(name, target, y_test, pred, fit_time, pred_time))
        fitted[name] = model
    table = pd.DataFrame(results).sort_values("RMSE").reset_index(drop=True)
    selected = table.iloc[0]["Model"]
    if selected == "Previous day baseline":
        selected = table[table["Model"] != selected].iloc[0]["Model"]
    out = Path(output_dir)
    (out / "forecasting").mkdir(parents=True, exist_ok=True)
    (out / "metadata").mkdir(parents=True, exist_ok=True)
    Path("reports/evaluation").mkdir(parents=True, exist_ok=True)
    artifact = {"model": fitted[selected], "features": features, "target": target}
    joblib.dump(artifact, out / "forecasting" / f"{target}.joblib")
    selected_row = table[table.Model == selected].iloc[0]
    metadata = {
        "model_name": selected,
        "target": target,
        "features": features,
        "training_start": str(train.timestamp.min()),
        "training_end": str(train.timestamp.max()),
        "test_start": str(test.timestamp.min()),
        "test_end": str(test.timestamp.max()),
        "mae": float(selected_row.MAE),
        "rmse": float(selected_row.RMSE),
        "r2": float(selected_row.R2),
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "version": "1.0",
        "training_samples": len(train),
        "test_samples": len(test),
    }
    (out / "metadata" / f"{target}.json").write_text(json.dumps(metadata, indent=2))
    table.to_csv(
        Path("reports/evaluation") / f"model_comparison_{target}.csv", index=False
    )
    pd.DataFrame(
        {
            "timestamp": test.timestamp,
            "actual": y_test,
            "predicted": predictions[selected],
            "residual": y_test - predictions[selected],
        }
    ).to_csv(Path("reports/evaluation") / f"test_predictions_{target}.csv", index=False)
    return table, metadata


def predict_test(
    data: pd.DataFrame, target="total_energy_kwh", model_dir="models"
) -> pd.DataFrame:
    """Recreate features and return held-out predictions from a persisted artifact."""
    path = Path(model_dir) / "forecasting" / f"{target}.joblib"
    if not path.exists():
        raise FileNotFoundError("Forecast model missing. Run python -m src.forecasting")
    artifact = joblib.load(path)
    featured = create_features(data, target)
    test = featured.iloc[int(len(featured) * 0.8) :].copy()
    test["predicted"] = artifact["model"].predict(test[artifact["features"]])
    test["residual"] = test[target] - test["predicted"]
    return test


def main() -> None:
    data = load_data()
    comparisons = []
    for target in ("total_energy_kwh", "cooling_demand_kw", "water_consumption_l"):
        table, meta = train_models(data, target)
        table["Selected"] = table["Model"].eq(meta["model_name"])
        comparisons.append(table)
        print(
            f"{target}: {meta['model_name']} RMSE={meta['rmse']:.3f} R2={meta['r2']:.3f}"
        )
    pd.concat(comparisons, ignore_index=True).to_csv(
        "reports/evaluation/model_comparison.csv", index=False
    )


if __name__ == "__main__":
    main()
