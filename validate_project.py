"""Executable, evidence-based mandatory artefact and behaviour audit."""

from pathlib import Path
import sys
import json
import joblib
import yaml
import pandas as pd
from src.anomaly_detection import detect_anomalies
from src.data_loader import load_data, REQUIRED_COLUMNS, validate_data
from src.recommendations import generate_recommendations
from src.sustainability_metrics import calculate_pue, calculate_wue, calculate_cue


def main() -> int:
    checks = {}
    required = [
        "src",
        "components",
        "pages",
        "tests",
        "config",
        "data/generated",
        "models/forecasting",
        "reports/evaluation",
    ]
    checks["Required folders"] = all(Path(p).is_dir() for p in required)
    try:
        data = load_data()
        checks["Dataset available"] = not data.empty
        checks["Required data schema"] = REQUIRED_COLUMNS <= set(data)
        checks["Data quality"] = validate_data(data).passed.all()
    except Exception:
        data = None
        checks.update(
            {
                "Dataset available": False,
                "Required data schema": False,
                "Data quality": False,
            }
        )
    checks["PUE implemented"] = (
        float(
            calculate_pue(
                __import__("pandas").Series([15]), __import__("pandas").Series([10])
            ).iloc[0]
        )
        == 1.5
    )
    checks["WUE implemented"] = (
        float(
            calculate_wue(
                __import__("pandas").Series([20]), __import__("pandas").Series([10])
            ).iloc[0]
        )
        == 2
    )
    checks["CUE implemented"] = (
        float(
            calculate_cue(
                __import__("pandas").Series([3]), __import__("pandas").Series([10])
            ).iloc[0]
        )
        == 0.3
    )
    targets = ["total_energy_kwh", "cooling_demand_kw", "water_consumption_l"]
    model_paths = [
        Path("models/forecasting") / f"{target}.joblib" for target in targets
    ]
    metadata_paths = [Path("models/metadata") / f"{target}.json" for target in targets]
    checks["Forecast models"] = all(path.exists() for path in model_paths)
    checks["Forecast models reload"] = (
        all(
            joblib.load(path).get("target") == target
            for path, target in zip(model_paths, targets)
        )
        if checks["Forecast models"]
        else False
    )
    checks["Model metadata"] = all(
        path.exists() and json.loads(path.read_text()).get("target") == target
        for path, target in zip(metadata_paths, targets)
    )
    checks["Model evaluation"] = Path(
        "reports/evaluation/model_comparison.csv"
    ).exists()
    checks["Anomaly model"] = Path(
        "models/anomaly_detection/isolation_forest.joblib"
    ).exists()
    if data is not None:
        _, events, _, metrics = detect_anomalies(data.head(min(2000, len(data))))
        checks["Anomaly runtime output"] = (
            bool(metrics)
            and not events.empty
            and {
                "severity",
                "affected_metric",
                "suggested_action",
            }
            <= set(events)
        )
        thresholds = yaml.safe_load(Path("config/thresholds.yaml").read_text())
        checks["Recommendation runtime"] = isinstance(
            generate_recommendations(data, thresholds), pd.DataFrame
        )
    else:
        checks["Anomaly runtime output"] = False
        checks["Recommendation runtime"] = False
    dashboard_files = [Path("app.py"), *Path("pages").glob("*.py")]
    checks["Streamlit application"] = len(dashboard_files) >= 11 and all(
        path.read_text().strip() for path in dashboard_files
    )
    checks["Documentation"] = all(
        Path(p).exists()
        for p in [
            "README.md",
            "REQUIREMENTS_CHECKLIST.md",
            "PROJECT_STATUS.md",
            "requirements.txt",
        ]
    )
    checks["Tests"] = len(list(Path("tests").glob("test_*.py"))) >= 5
    checks["Final research results"] = Path("reports/FINAL_RESULTS.md").exists()
    checks["Research figures"] = len(list(Path("reports/figures").glob("*.png"))) >= 14
    for name, passed in checks.items():
        print(f"[{'PASS' if passed else 'FAIL'}] {name}")
    passed = sum(checks.values())
    print(f"\nMANDATORY REQUIREMENTS:\n{passed}/{len(checks)} PASSED")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
