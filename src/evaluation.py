"""Research-ready evaluation figure generation."""

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def create_research_figures(
    prediction_path="reports/evaluation/test_predictions.csv", output="reports/figures"
) -> list[Path]:
    data = pd.read_csv(prediction_path)
    out = Path(output)
    out.mkdir(parents=True, exist_ok=True)
    paths = []
    for name, plotter in [
        (
            "actual_vs_predicted",
            lambda ax: ax.scatter(data.actual, data.predicted, s=4, alpha=0.35),
        ),
        ("residual_distribution", lambda ax: ax.hist(data.residual, bins=50)),
    ]:
        fig, ax = plt.subplots(figsize=(8, 5))
        plotter(ax)
        ax.set_title(name.replace("_", " ").title())
        fig.tight_layout()
        path = out / f"{name}.png"
        fig.savefig(path, dpi=200)
        plt.close(fig)
        paths.append(path)
    return paths
