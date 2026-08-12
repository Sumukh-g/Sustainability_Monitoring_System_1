"""Executable, evidence-based mandatory artefact and behaviour audit."""

from pathlib import Path
import sys
from src.data_loader import load_data, REQUIRED_COLUMNS, validate_data
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
    checks["Forecast model"] = Path(
        "models/forecasting/total_energy_kwh.joblib"
    ).exists()
    checks["Model evaluation"] = Path(
        "reports/evaluation/model_comparison.csv"
    ).exists()
    checks["Anomaly model"] = Path(
        "models/anomaly_detection/isolation_forest.joblib"
    ).exists()
    checks["Recommendation module"] = Path("src/recommendations.py").exists()
    checks["Streamlit application"] = Path("app.py").exists()
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
    for name, passed in checks.items():
        print(f"[{'PASS' if passed else 'FAIL'}] {name}")
    passed = sum(checks.values())
    print(f"\nMANDATORY REQUIREMENTS:\n{passed}/{len(checks)} PASSED")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
