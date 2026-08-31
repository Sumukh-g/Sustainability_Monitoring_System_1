WORD_TARGET_NOTE: approx 1550 words

# 5 Conclusion

## 5.1 Introduction

This dissertation investigated the design and reproducible evaluation of an integrated sustainability monitoring artefact for UK data-centre operations. The research responded to a practical gap between retrospective KPI reporting and the broader evidence needed for operational preparation: forecasts, unusual-condition detection, traceable recommendations and confidence that the underlying software behaves as claimed. The result is the AI-Based Sustainability Monitoring System, a Python machine-learning pipeline and multi-page Streamlit dashboard evaluated on deterministic multi-site synthetic telemetry.

## 5.2 Achievement of the aim and objectives

The research aim was to design, implement and evaluate an integrated AI-based sustainability monitoring decision-support artefact. This aim was achieved within the defined academic scope. Requirements were reconstructed and traced to implementation and evidence. A layered architecture separated generation, validation, KPI logic, machine learning, decision rules, persistence and presentation. The completed interface provided Command Center, four domain intelligence views, Forecast Center, Anomaly Intelligence, AI Advisor, Scenario Lab, Model Intelligence, Data Explorer and System Health.

The implementation objective was met through a reproducible pipeline using Python 3.11, pandas, scikit-learn, Plotly, Streamlit, Joblib, PyYAML and pytest. The pipeline generated 17,568 hourly rows for London-DC1 and Manchester-DC2, calculated KPIs, engineered leakage-safe features, compared forecasting models, fitted Isolation Forest, persisted models and produced audit outputs. Twenty-one research figures and machine-readable reports link interface claims to calculated evidence.

The evaluation objective was met through a chronological 80/20 split, a previous-day baseline, three fitted regressors, held-out regression metrics, an anomaly confusion matrix and functional verification. All 12 pytest tests and all 19 executable project checks passed. This evidence establishes functional and computational readiness under the project conditions.

The final objective—critical discussion—was essential because individual components achieved very different results. Forecasting was strong, whereas anomaly detection was weak. Synthetic data enabled exact reproduction but restricted ecological validity. Recommendations were transparent but not physically validated. These boundaries prevent successful implementation from being misrepresented as proven operational impact.

## 5.3 Answers to the research questions

The KPI sub-question concerned calculation correctness and presentation. The system produced mean PUE of 1.23, WUE of 0.33 L/kWh and CUE of 0.31 kg CO2e/kWh, with aligned units and defensive denominator behaviour. The project score was 86/100 and labelled “Excellent”, but was explicitly identified as a configurable project-specific indicator rather than an industry standard. KPI readiness was therefore demonstrated internally, while comparisons with real facilities would require harmonised boundaries.

The forecasting sub-question concerned accuracy relative to a baseline. HistGradientBoosting achieved the lowest RMSE for all targets. Energy forecasting produced MAE 8.22 kWh, RMSE 17.41 kWh and R² 0.969, improving RMSE by 71.89% over the previous-day baseline. Cooling achieved MAE 8.24 kW, RMSE 10.44 kW and R² 0.945, a 62.44% improvement. Water achieved MAE 11.24 L, RMSE 21.37 L and R² 0.756, a smaller but material 39.82% improvement. Forecasting therefore provides the strongest evidence that the artefact adds anticipatory capability beyond descriptive monitoring.

The anomaly sub-question produced a less favourable answer. Isolation Forest issued 440 detections, of which 84 were true positives and 356 false positives; it missed 204 of the 288 injected anomalies. Precision was 0.191, recall 0.292 and F1 0.231. The detector can identify unusual observations for exploratory review, but it is unsuitable as a high-confidence operational alarm. This finding also demonstrates the importance of publishing false-positive and false-negative evidence rather than presenting an anomaly count as success.

The requirements and reproducibility sub-question was answered positively at prototype level. Page coverage, persisted artefacts, explicit configuration, generated evidence, passing tests and the executable validator provide a traceable route from requirements to results. The exact evaluated source revision further supports inspection. Nevertheless, the absence of deployed infrastructure, security evaluation and participant testing means that reproducibility should not be conflated with production quality.

The main research question asked to what extent the integrated dashboard can improve decision-support readiness under reproducible synthetic evaluation. It can improve readiness to a meaningful but bounded extent. The artefact makes sustainability status inspectable, provides forecasts that substantially outperform a daily baseline, reveals model quality and limitations, and connects threshold conditions to deterministic recommendations. Its integrated design reduces fragmentation between domains and between prediction and evaluation.

The evidence does not support claims that the system improves actual operator decisions, produces environmental savings or controls facilities safely. “Readiness” is therefore the correct level of conclusion: the project establishes a credible platform and evaluation pattern for further operational study.

## 5.4 Contributions

The principal practical contribution is a unified academic demonstrator for energy, water, cooling and carbon intelligence. Instead of treating AI as a single opaque output, the artefact distinguishes established ratios, supervised forecasts, unsupervised anomaly scores, deterministic recommendations and project-specific scoring. This separation helps users assign appropriate confidence to each type of evidence.

The methodological contribution is a reproducible evaluation that combines DSR, comparative machine learning and functional verification. A simple baseline prevents ensemble performance from being judged in isolation. Chronological splitting and shifted rolling features reduce temporal leakage. Confusion-matrix counts expose the operational burden hidden by aggregate anomaly claims. Tests and persisted outputs connect analytical results to software behaviour.

The critical contribution is evidence that integration does not make all components equally mature. High forecast R² values coexist with low anomaly F1. The finding argues against broad declarations that an “AI dashboard” is accurate. Evaluation must remain task-specific, and interface language should communicate uncertainty and limitations.

Taken together, these contributions show that artefact value resides as much in the quality and traceability of evidence as in model sophistication. The project makes favourable and unfavourable findings visible within the same system. This enables subsequent work to preserve the validated KPI and forecasting foundation while replacing or recalibrating weaker analytical components, rather than treating the dashboard as one indivisible model.

## 5.5 Limitations

Synthetic telemetry is the dominant limitation. The generator provides complete records, known relationships and exact anomaly labels, whereas real facilities contain sensor drift, maintenance changes, missing intervals, evolving workload and undocumented interventions. Models may have learned structures that are easier and more stable than operational data.

Only two stylised UK sites and one year were represented. A single chronological hold-out cannot demonstrate robustness across years or facilities. Model selection and reporting used the same held-out period, and no confidence intervals or rolling-origin results were produced. Forecast feature availability also requires re-examination for a concrete prediction horizon in production.

Isolation Forest was evaluated against injected row labels. Real incidents may span periods and possess uncertain onset and resolution. The detector’s weak precision and recall could create both alert fatigue and missed faults. Its output should remain advisory until calibrated against operationally reviewed events.

Recommendations and Scenario Lab outputs were not tested on physical plant. They do not account comprehensively for resilience, service-level constraints, equipment warranties or site safety procedures. No energy, water, carbon or financial savings can be attributed to the artefact.

Finally, no participant usability study was administered. The existence of a questionnaire does not constitute user evidence. Dashboard consistency, page coverage and error messages can be verified functionally, but effectiveness, efficiency, trust and comprehension remain unknown.

## 5.6 Future work

The first priority is evaluation with metered multi-facility data under an appropriate data-sharing and governance arrangement. A staged shadow deployment could ingest read-only telemetry, compare KPI calculations with existing operational reports and record forecast errors without influencing control. Site engineers should review measurement boundaries and event labels.

Forecast evaluation should adopt rolling-origin validation, an untouched final test period and uncertainty intervals. Explicit forecast horizons and feature-availability contracts would prevent contemporaneous information from being used when unavailable in practice. Drift monitoring should test whether relationships change after maintenance, workload migration or seasonal transitions.

Anomaly research should move from one global Isolation Forest towards site- and regime-aware models, temporal windows and event-level evaluation. Thresholds should reflect the relative cost of false alarms and missed incidents. A labelled review workflow could support semi-supervised models and document why observations are operationally important.

Recommendation rules should be reviewed by qualified facilities personnel and evaluated first in a validated simulator or controlled shadow process. Any later automation should preserve human approval, safety interlocks and complete audit trails. The system should continue to be treated as decision support rather than direct control.

A formally approved participant study should evaluate representative tasks, not general impressions alone. Measures could include task completion, error rate, time, perceived usability and interpretation of KPI and anomaly uncertainty. The unused questionnaire can inform this design but should be revised for the target roles and context.

Production-oriented engineering would require authenticated access, role-based permissions, secure and observable ingestion, database-backed persistence, deployment monitoring, accessibility testing and controlled model/version governance. These steps are substantial and should not be implied by the successful local demonstrator.

## 5.7 Final conclusion

The AI-Based Sustainability Monitoring System demonstrates that sustainability KPIs, forecasting, anomaly evidence and rule-based advice can be integrated into a coherent and reproducibly evaluated decision-support artefact. Its strongest result is forecasting: HistGradientBoosting substantially outperformed a previous-day baseline across energy, cooling and water. Its weakest result is anomaly detection, where low precision and recall preclude confident alarm use.

The system therefore makes a credible MSc contribution as an evaluated design and implementation, not as proof of deployed environmental benefit. By preserving that distinction, the dissertation offers both a functioning artefact and a transparent account of what evidence is still required before such a system could support real UK data-centre operations.
