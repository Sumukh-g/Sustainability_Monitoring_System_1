# Requirements Traceability Matrix

Evidence is produced from executable code and generated artifacts; advanced work is explicitly separated.

| ID | Requirement | Mandatory/Advanced | Implemented | File/Module | Dashboard Page | Test | Evidence | Notes |
|---|---|---|---|---|---|---|---|---|
| T1-01 | Realistic hourly energy/water/cooling/carbon/IT/environment data and labelled faults | Mandatory | Yes | `src/data_generation.py` | Data Explorer | generation fixtures | generated CSV/schema | Two sites, 12 months |
| T1-02 | Missing, duplicate, negative, range, continuity, outlier/ratio validation | Mandatory | Yes | `src/data_loader.py` | Data Explorer | preprocessing tests | quality table | Sensor bounds surface injected sensor events |
| T1-03 | Cleaning and time-aware split | Mandatory | Yes | `src/preprocessing.py` | Model Performance | `test_preprocessing.py` | chronological tests | No shuffle |
| T1-04 | Time, cyclic, 1/24/48/168 lag and 3/6/24/168 rolling features | Mandatory | Yes | `src/feature_engineering.py` | Model Performance | `test_preprocessing.py` | feature columns | Rolling target shifted first |
| T1-05 | PUE/WUE/CUE and operational KPIs | Mandatory | Yes | `src/sustainability_metrics.py` | Overview/domain pages | `test_metrics.py` | cards/trends | Units documented |
| T1-06 | Energy analytics | Mandatory | Yes | `pages/1_Energy.py` | Energy | dashboard smoke/import | interactive charts | Workload and PUE |
| T1-07 | Water analytics | Mandatory | Yes | `pages/2_Water.py` | Water | dashboard smoke/import | interactive charts | WUE/relationships |
| T1-08 | Cooling analytics | Mandatory | Yes | `pages/3_Cooling.py` | Cooling | dashboard smoke/import | interactive charts | Load/temperature |
| T1-09 | Carbon analytics | Mandatory | Yes | `pages/4_Carbon.py` | Carbon | dashboard smoke/import | interactive charts | CUE/grid intensity |
| T1-10 | Configurable score and alerts | Mandatory | Yes | `sustainability_metrics.py`, `alerts.py`, YAML | Overview | metric tests | score/alerts | Score is not standard |
| T1-11 | Baseline and multiple forecast models | Mandatory | Yes | `src/forecasting.py` | AI Forecasting | `test_forecasting.py` | Joblib/table | Three targets trained |
| T1-12 | MAE/RMSE/R², timings, metadata and selected model | Mandatory | Yes | `src/forecasting.py` | Model Performance | forecast tests | CSV/JSON | Held-out selection |
| T1-13 | Actual/predicted/residual visualisation | Mandatory | Yes | `pages/5_AI_Forecasting.py` | AI Forecasting | forecast tests | persisted prediction | Backtest clearly labelled |
| T1-14 | Proper anomaly detection and severity/event structure | Mandatory | Yes | `src/anomaly_detection.py` | Anomalies | `test_anomalies.py` | Joblib/events/metrics | Isolation Forest |
| T1-15 | Data-linked prioritised recommendations | Mandatory | Yes | `src/recommendations.py` | Recommendations | `test_recommendations.py` | structured outputs | Engineering review required |
| T1-16 | Explainability | Mandatory | Yes | `src/explainability.py` | Model Performance | forecast integration | importance chart | Association, not causation |
| T1-17 | Multi-page usable dashboard and global controls | Mandatory | Yes | `app.py`, `components/`, `pages/` | All | launch check | live app | Cached data, graceful errors |
| T1-18 | Data explorer/export/correlations | Mandatory | Yes | `pages/9_Data_Explorer.py` | Data Explorer | validator | CSV download | Correlation disclaimer |
| T1-19 | Research and anomaly evaluation | Mandatory | Yes | `evaluation.py`, performance page | Model Performance | pipeline tests | CSV/PNG/F1 | Synthetic-label limitation |
| T1-20 | Usability and decision-value evaluation framework | Mandatory | Yes | `reports/usability_questionnaire.md` | README | document audit | questionnaire | No fabricated responses |
| T1-21 | Reproducibility/docs/error handling/tests | Mandatory | Yes | README, requirements, validator | All | pytest/validator | clean commands | Environment external |
| T2-01 | What-if sustainability simulator | Advanced | Yes | `pages/10_What_If.py` | What-if | manual UI | live estimates | Explicitly modelled estimates |
| T2-02 | Renewable-energy context | Advanced | Yes | generator, carbon page | Carbon | data schema | renewable percentage | Simulated |

