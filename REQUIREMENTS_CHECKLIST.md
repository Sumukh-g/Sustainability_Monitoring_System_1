# Requirements Traceability Matrix

Evidence is produced from executable code and generated artifacts; advanced work is explicitly separated.

| ID | Requirement | Mandatory/Advanced | Runtime status | File/Module | Dashboard Page | Test | Evidence | Notes |
|---|---|---|---|---|---|---|---|---|
| T1-01 | Realistic hourly energy/water/cooling/carbon/IT/environment data and labelled faults | Mandatory | PASS | `src/data_generation.py` | Data Explorer | generation fixtures | `data/generated/data_centre_hourly.csv` (17,568 rows) | Two sites, 12 months |
| T1-02 | Missing, duplicate, negative, range, continuity, outlier/ratio validation | Mandatory | PASS | `src/data_loader.py` | Data Explorer | preprocessing tests | `reports/evaluation/data_quality_report.csv` | All checks pass |
| T1-03 | Cleaning and time-aware split | Mandatory | PASS | `src/preprocessing.py` | Model Performance | `test_preprocessing.py` | chronological tests | No shuffle |
| T1-04 | Time, cyclic, lag and rolling features | Mandatory | PASS | `src/feature_engineering.py` | Model Performance | `test_preprocessing.py` | feature columns | Rolling target shifted first; no leakage |
| T1-05 | PUE/WUE/CUE and operational KPIs | Mandatory | PASS | `src/sustainability_metrics.py` | Overview/domain pages | `test_metrics.py` | cards/trends | Units verified mathematically |
| T1-06 | Energy analytics | Mandatory | PASS | `pages/1_Energy.py` | Energy | runtime verified | interactive charts | Workload and PUE |
| T1-07 | Water analytics | Mandatory | PASS | `pages/2_Water.py` | Water | runtime verified | interactive charts | WUE/relationships |
| T1-08 | Cooling analytics | Mandatory | PASS | `pages/3_Cooling.py` | Cooling | runtime verified | interactive charts | Load/temperature |
| T1-09 | Carbon analytics | Mandatory | PASS | `pages/4_Carbon.py` | Carbon | runtime verified | interactive charts | CUE/grid intensity |
| T1-10 | Configurable score and alerts | Mandatory | PASS | `sustainability_metrics.py`, `alerts.py`, YAML | Overview | metric tests | score=86/100, alerts | Score is project-specific |
| T1-11 | Baseline and multiple forecast models | Mandatory | PASS | `src/forecasting.py` | AI Forecasting | `test_forecasting.py` | Joblib/table | 3 targets x 4 models = 12 combinations |
| T1-12 | MAE/RMSE/R², timings, metadata and selected model | Mandatory | PASS | `src/forecasting.py` | Model Performance | forecast tests | CSV/JSON | HistGradientBoosting selected for all targets |
| T1-13 | Actual/predicted/residual visualisation | Mandatory | PASS | `pages/5_AI_Forecasting.py` | AI Forecasting | forecast tests | persisted prediction | Backtest clearly labelled |
| T1-14 | Proper anomaly detection and severity/event structure | Mandatory | PASS | `src/anomaly_detection.py` | Anomalies | `test_anomalies.py` | Joblib/events/metrics | Isolation Forest, F1=0.231 |
| T1-15 | Data-linked prioritised recommendations | Mandatory | PASS | `src/recommendations.py` | Recommendations | `test_recommendations.py` | structured outputs | Triggers verified |
| T1-16 | Explainability | Mandatory | PASS | `src/explainability.py` | Model Performance | forecast integration | importance charts | Association, not causation |
| T1-17 | Multi-page usable dashboard and global controls | Mandatory | PASS | `app.py`, `components/`, `pages/` | All 11 pages | launch check | live app | Site/date/aggregation filters |
| T1-18 | Data explorer/export/correlations | Mandatory | PASS | `pages/9_Data_Explorer.py` | Data Explorer | validator | CSV download | Correlation disclaimer |
| T1-19 | Research and anomaly evaluation | Mandatory | PASS | `evaluation.py`, performance page | Model Performance | pipeline tests | 21 PNG/CSV/F1 | Synthetic-label limitation |
| T1-20 | Usability and decision-value evaluation framework | Mandatory | PASS | `reports/usability_questionnaire.md` | README | document audit | questionnaire | No fabricated responses |
| T1-21 | Reproducibility/docs/error handling/tests | Mandatory | PASS | README, requirements, validator | All | pytest: 12/12 passed | clean commands | 19/19 validator checks |
| T2-01 | What-if sustainability simulator | Advanced | PASS | `pages/10_What_If.py` | What-if | runtime verified | live estimates | Modelled estimates |
| T2-02 | Renewable-energy context | Advanced | PASS | generator, carbon page | Carbon | data schema | renewable percentage | Simulated |


## Runtime evidence status

On 2026-08-12 a clean virtual environment (Python 3.11.5) was created and every documented runtime entry point was executed successfully. All 19/19 validator checks pass. All 12/12 pytest tests pass. All dashboard pages render correctly. All research artifacts are generated. See `FINAL_AUDIT.md` for detailed status per requirement.
