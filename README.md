# AI-Based Sustainability Monitoring System for Data Centres

A reproducible MSc dissertation prototype that turns hourly data-centre telemetry into sustainability KPIs, forecasts, Isolation Forest anomaly evidence, alerts, and actionable decision support. It is a **decision-support prototype**, not autonomous plant control.

## Research problem and objectives

Data centres must balance digital demand with energy, water, cooling and carbon impacts. Operational signals interact, peaks arrive before teams can respond, and inefficient behaviour may be difficult to recognise. This project monitors those signals, calculates documented KPIs, predicts facility energy/cooling/water demand, detects abnormal multivariate behaviour, explains model associations, and connects measured conditions to qualified recommendations.

## Completed features (all runtime-verified)

- Deterministic 12-month, hourly, two-site synthetic telemetry (17,568 rows, 37 columns) with daily/weekly/seasonal patterns and 288 injected workload, cooling, water and sensor faults.
- Schema and data-quality validation (all checks pass), cleaning, chronological splitting, cyclic features, 1/24/48/168-hour lags, and shifted rolling statistics with no data leakage.
- PUE (mean 1.23), WUE (mean 0.33 L/kWh), CUE (mean 0.31 kg/kWh), energy/workload and a configurable 0–100 project sustainability score (86/100 Excellent).
- Previous-day baseline, Linear Regression, Random Forest and HistGradientBoosting comparison for energy (R²=0.969), cooling (R²=0.945) and water (R²=0.756). Test periods are chronological; models and JSON metadata are persisted with Joblib.
- Isolation Forest anomaly detection: 440 detections, precision=0.191, recall=0.292, F1=0.231 against synthetic ground truth.
- Configuration-driven alerts and structured, prioritised, data-linked recommendations.
- Premium multi-page Streamlit interface: Overview, Energy, Water, Cooling, Carbon, AI Forecasting, Anomalies, Recommendations, Model Performance, Data Explorer and an advanced What-if simulator. All 11 pages runtime-verified.
- 21 research figures, evaluation CSVs, usability questionnaire framework, 12 automated tests (all passing), traceability matrix and executable validation audit (19/19 passed).

## Architecture

```text
app.py                       executive dashboard entry point
components/                  shared Streamlit controls and styling
pages/                       domain, AI, evaluation, and explorer pages
config/                      thresholds, weights, seeds, targets
src/                         generation, validation, KPIs, ML and decisions
data/generated/              reproducible CSV telemetry
models/{forecasting,...}/    persisted Joblib artifacts and JSON metadata
reports/{evaluation,figures}/ research-ready calculated outputs
tests/                       unit and integration tests
validate_project.py          mandatory artefact/behaviour audit
```

## Dataset and units

`python -m src.data_generation` creates 8,784 hourly observations per site (17,568 rows). Workload drives IT kW/kWh; IT load and outdoor temperature drive cooling; cooling drives electricity and water; facility energy and grid intensity drive location-based carbon. Noise, maintenance and reproducibly injected anomalies add variance. Core units are kW demand, kWh hourly energy, litres, °C, %, gCO2e/kWh and kgCO2e. The hidden `anomaly_ground_truth` supports evaluation only.

## Sustainability metrics

| KPI | Formula | Unit / assumption |
|---|---|---|
| PUE | total facility energy / IT energy | Dimensionless, hourly energy boundary |
| WUE | site water / IT energy | L/kWh IT; synthetic site water boundary |
| CUE | location-based carbon / IT energy | kgCO2e/kWh IT |
| Score | configurable weighted normalised PUE, WUE, carbon, cooling, utilisation, anomalies | 0–100 **project-specific indicator, not an industry standard** |

Zero, missing, or negative denominators yield `NaN`, rather than misleading infinite values.

## AI methodology

Feature creation shifts all target rolling windows by one hour and keeps the last 20% as test data. A previous-day baseline is compared with three fitted regressors using MAE, RMSE and R². Selection uses held-out RMSE, while persistence prevents dashboard retraining. Feature importance/coefficient magnitude indicates **model association**, never causality. Isolation Forest identifies multivariate deviations across energy, cooling, water, PUE, utilisation and carbon. Recommendations are deterministic rules triggered by selected-period evidence and external YAML thresholds.

## Install and reproduce

```bash
git clone <repository-url>
cd Sustainability_Monitoring_System_1
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m src.data_generation
python -m src.forecasting
python -m src.audit_pipeline
pytest
python validate_project.py
streamlit run app.py
```

`src.audit_pipeline` executes anomaly evaluation, model reload-based figures, data-quality and realism reports, recommendation evidence, and writes `reports/FINAL_RESULTS.md` from calculated values. The validator intentionally fails if those runtime artifacts are absent.

Use the sidebar date/site/aggregation controls. A refresh button invalidates the data cache. Missing data/models produce actionable dashboard messages rather than retraining or silently substituting values.

## Evaluation and dissertation use

Calculated model comparison and prediction records are in `reports/evaluation/`; 200-DPI figures are in `reports/figures/`. `reports/usability_questionnaire.md` provides an uncompleted evaluation framework—no participants or findings are fabricated. Decision-support value can be assessed through successful identification of inefficiency, demand, anomalies, and intervention opportunities.

## Security and ethics

Only schema-checked CSV input is supported; arbitrary code or unsafe object upload is not accepted. Secrets belong in `.env`, which is ignored. Synthetic telemetry contains no personal data. Operational actions must be reviewed by qualified facilities and safety personnel.

## Limitations

- Synthetic data and simplified physical relationships cannot fully represent a real facility.
- Recommendations and estimated what-if impacts have not been validated on physical infrastructure.
- Forecast accuracy depends on simulation realism and known contemporaneous predictors.
- Injected anomaly labels simplify ambiguous real faults; precision/recall may not transfer.
- Location-based carbon, water boundaries, and KPI conclusions depend on stated unit assumptions.
- This prototype provides decision support, not autonomous control or guaranteed savings.

## Future work (not claimed complete)

Validate against metered multi-facility data; perform approved participant usability testing; add robust probabilistic intervals, drift monitoring, authenticated persistence and audited workload orchestration integrations.
