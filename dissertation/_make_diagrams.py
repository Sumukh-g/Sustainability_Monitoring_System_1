"""Generate architecture diagrams for the dissertation."""
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

out = Path("dissertation/assets/diagrams")
out.mkdir(parents=True, exist_ok=True)


def box(ax, x, y, w, h, text, fc="#E8F5F1", ec="#0F766E"):
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.02",
        linewidth=1.2,
        facecolor=fc,
        edgecolor=ec,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=8)


fig, ax = plt.subplots(figsize=(10, 6), dpi=200)
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis("off")
ax.set_title(
    "System context: AI-Based Sustainability Monitoring System", fontsize=11, pad=12
)
box(
    ax,
    0.3,
    2.2,
    2.0,
    1.6,
    "UK data-centre\noperations user\n(facility / energy\nengineer)",
)
box(
    ax,
    3.5,
    2.0,
    3.0,
    2.0,
    "AI-Based Sustainability\nMonitoring System\n(Streamlit decision-support\nartefact)",
)
box(ax, 7.5, 3.2, 2.2, 1.4, "Synthetic / CSV\ntelemetry store")
box(ax, 7.5, 1.2, 2.2, 1.4, "Persisted ML\nartefacts\n(Joblib + metadata)")
for a, b in [
    ((2.3, 3.0), (3.5, 3.0)),
    ((6.5, 3.4), (7.5, 3.8)),
    ((6.5, 2.6), (7.5, 1.9)),
]:
    ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="->", color="#334155", lw=1.2))
ax.text(
    5,
    0.4,
    "Source: Author's analysis of the implemented prototype",
    fontsize=7,
    ha="center",
    color="#64748B",
)
fig.tight_layout()
fig.savefig(out / "figure_3_1_system_context.png", bbox_inches="tight")
plt.close()

fig, ax = plt.subplots(figsize=(11, 6.5), dpi=200)
ax.set_xlim(0, 11)
ax.set_ylim(0, 7)
ax.axis("off")
ax.set_title("Component architecture of the monitoring artefact", fontsize=11, pad=12)
comps = [
    (0.3, 5.2, 2.4, 1.2, "Streamlit UI\napp.py + pages/ + ui/", "#DBEAFE", "#1D4ED8"),
    (3.2, 5.2, 2.4, 1.2, "Shared controls\ncomponents/", "#DBEAFE", "#1D4ED8"),
    (6.2, 5.2, 2.2, 1.2, "YAML config\nsettings + thresholds", "#FEF3C7", "#B45309"),
    (0.3, 3.2, 2.0, 1.3, "Data gen &\nvalidation", "#DCFCE7", "#15803D"),
    (2.6, 3.2, 2.0, 1.3, "Features &\npreprocessing", "#DCFCE7", "#15803D"),
    (4.9, 3.2, 2.0, 1.3, "Forecasting &\nexplainability", "#DCFCE7", "#15803D"),
    (7.2, 3.2, 2.0, 1.3, "Anomaly &\nrecommendations", "#DCFCE7", "#15803D"),
    (9.4, 3.2, 1.4, 1.3, "KPIs &\nalerts", "#DCFCE7", "#15803D"),
    (1.5, 1.1, 2.5, 1.2, "data/generated CSV", "#F1F5F9", "#475569"),
    (4.5, 1.1, 2.5, 1.2, "models/ Joblib+JSON", "#F1F5F9", "#475569"),
    (7.5, 1.1, 2.5, 1.2, "reports/ eval+figures", "#F1F5F9", "#475569"),
]
for x, y, w, h, t, fc, ec in comps:
    box(ax, x, y, w, h, t, fc, ec)
ax.text(
    5.5,
    0.35,
    "Source: Author's analysis of repository modules",
    fontsize=7,
    ha="center",
    color="#64748B",
)
fig.tight_layout()
fig.savefig(out / "figure_3_2_component_architecture.png", bbox_inches="tight")
plt.close()

fig, ax = plt.subplots(figsize=(11, 5.5), dpi=200)
ax.set_xlim(0, 11)
ax.set_ylim(0, 5)
ax.axis("off")
ax.set_title("ML training and inference data flow", fontsize=11, pad=12)
steps = [
    (0.2, 2.0, 1.6, 1.4, "Generate /\nload CSV"),
    (2.1, 2.0, 1.6, 1.4, "Validate &\nclean"),
    (4.0, 2.0, 1.6, 1.4, "Leakage-safe\nfeatures"),
    (5.9, 2.0, 1.6, 1.4, "Chronological\n80/20 split"),
    (7.8, 2.0, 1.5, 1.4, "Train &\nselect model"),
    (9.5, 2.0, 1.4, 1.4, "Persist &\ndashboard\ninference"),
]
for i, (x, y, w, h, t) in enumerate(steps):
    box(ax, x, y, w, h, t, "#ECFDF5", "#047857")
    if i < len(steps) - 1:
        ax.annotate(
            "",
            xy=(steps[i + 1][0], 2.7),
            xytext=(x + w, 2.7),
            arrowprops=dict(arrowstyle="->", color="#334155"),
        )
ax.text(
    5.5,
    0.5,
    "Source: Author's analysis of forecasting and anomaly pipelines",
    fontsize=7,
    ha="center",
    color="#64748B",
)
fig.tight_layout()
fig.savefig(out / "figure_3_3_ml_pipeline.png", bbox_inches="tight")
plt.close()
print("diagrams ok")
