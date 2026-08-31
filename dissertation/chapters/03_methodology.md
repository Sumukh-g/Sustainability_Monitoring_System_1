WORD_TARGET_NOTE: approx 2300 words

# 3 Methodology

## 3.1 Introduction

This chapter explains how the AI-Based Sustainability Monitoring System was designed and evaluated. It defines the Design Science Research strategy, converts the research questions into requirements, documents the synthetic dataset and analytical procedures, and specifies the verification evidence used to assess the artefact. The methodology prioritises reproducibility and guards against temporal leakage. Its claims remain bounded by an artificial evaluation environment.

## 3.2 Research design

The study follows Design Science Research (DSR), in which knowledge is generated through constructing and evaluating a purposeful artefact (Hevner et al., 2004). The Design Science Research Methodology of Peffers et al. (2007) provides the process model. Problem identification concerned fragmented sustainability evidence and the limited anticipatory value of retrospective dashboards. Objectives were defined as integrated, reproducible and critically evaluated decision support. Design and development produced the data pipeline, models, rules and Streamlit interface. Demonstration used one year of synthetic two-site telemetry. Evaluation combined model comparison, anomaly classification metrics, KPI inspection and functional verification. This dissertation communicates both successful and weak results.

The approach iterated between design, evidence and refinement rather than following a strictly linear lifecycle. For example, requirements for persisted model metadata and missing-artifact messages arose from the need to make evaluation reproducible at dashboard runtime. This reflects Hevner et al.’s (2004) design cycle between building and evaluation.

The unit of analysis is the software artefact at commit `756cc2493cdae4085620b385e7be4f3ce9cfc6af`. The evaluation does not study people or organisations. No interviews, participant observations or administered usability questionnaire form part of the evidence. Consequently, the research evaluates computational and functional readiness, not adoption or observed improvement in human decisions.

## 3.3 Requirements and traceability

Requirements were reconstructed from the research aim and operational workflow. They were grouped into data, KPI, forecasting, anomaly, decision-support, interface and verification concerns (Table 3.1). Each requirement was associated with an implementation component and at least one evidence source, reducing the risk that visible interface breadth would substitute for tested behaviour.

**Table 3.1: Principal artefact requirements**

| ID | Requirement | Primary verification |
|---|---|---|
| R1 | Generate/load hourly multi-site telemetry with a stable schema | Dataset summary and schema tests |
| R2 | Calculate PUE, WUE and CUE defensively | KPI tests and summary output |
| R3 | Compare three regressors with a previous-day baseline | Model comparison CSVs |
| R4 | Preserve temporal order and prevent target leakage | Feature-code inspection and metadata |
| R5 | Detect multivariate anomalies and report labelled performance | Confusion matrix and anomaly metrics |
| R6 | Produce transparent threshold-based alerts and recommendations | YAML configuration and recommendation output |
| R7 | Present domain and analytical evidence through coherent pages | Runtime page validation |
| R8 | Persist models and evaluation artefacts | Joblib, JSON, CSV and figures |
| R9 | Fail informatively when required artefacts are unavailable | Tests and validator |
| R10 | Reproduce the project through documented commands | pytest and executable validation |

The requirements operationalise the research sub-questions. R2 addresses KPI correctness; R3 and R4 address forecasting; R5 addresses anomaly detection; and R1 and R6–R10 address coverage and reproducibility. Traceability does not prove that each design choice is optimal, but it makes omissions and claims inspectable.

## 3.4 Artefact architecture

The architecture separates data, analytics, decision logic, persistence and presentation (Figure 3.1). Python modules generate and validate data, compute KPIs, engineer features, train models and create audit outputs. Configuration files contain seeds, target lists, score weights and operational thresholds. Trained forecasters and the anomaly detector are persisted using Joblib, with JSON metadata for forecasting models. Evaluation data and figures are written separately from runtime interface code.

**Figure 3.1:** Logical architecture from synthetic telemetry through validation, KPI and machine-learning services to persisted evidence and Streamlit pages.

Streamlit provides the multi-page presentation layer, pandas supports transformations, scikit-learn supplies estimators and metrics, Plotly supplies interactive charts, PyYAML reads configuration and pytest automates functional checks (McKinney, 2010; Pedregosa et al., 2011). Separation reduces dashboard latency because models are trained in the pipeline rather than silently retrained during page rendering. It also ensures that Model Intelligence reports the persisted evaluated artefacts.

The interface includes Command Center; Energy, Water, Cooling and Carbon Intelligence; Forecast Center; Anomaly Intelligence; AI Advisor; Scenario Lab; Model Intelligence; Data Explorer; and System Health. Shared filters support site, period and aggregation choices. These views are an implementation of progressive disclosure: summary first, then domain detail, analytical evidence and system status.

## 3.5 Synthetic data

The dataset contains 17,568 rows and 37 columns. It represents hourly records for London-DC1 and Manchester-DC2 from 00:00 on 1 January to 23:00 on 31 December 2024. Because 2024 is a leap year, each site contributes 8,784 hours. A deterministic generator creates daily, weekly and seasonal patterns. Workload influences IT power; IT load and outdoor temperature influence cooling; cooling contributes to facility electricity and water use; and facility energy and grid intensity influence location-based carbon.

Noise, maintenance effects and anomalies introduce variation. In total, 288 labels represent injected workload, cooling, water and sensor events. The hidden `anomaly_ground_truth` field is used for evaluation, not as an input to unsupervised fitting. Synthetic generation provides complete, shareable data and exact labels, avoiding confidentiality restrictions. However, the equations inevitably reflect developer assumptions and can favour models that recover those relationships. Exact injected labels are also cleaner than real maintenance records. Synthetic performance is therefore internal evidence, not an estimate of deployment performance.

Data validation checks the expected schema, timestamp parsing, site coverage, row count, units and quality conditions before modelling. The reported data-quality audit passed. Invalid KPI denominators produce missing values rather than infinite values. This prevents data errors being disguised as genuine extremes.

## 3.6 KPI calculation

Three established ratios were implemented:

\[
PUE = \frac{\text{total facility energy}}{\text{IT energy}}
\]

\[
WUE = \frac{\text{site water consumption (L)}}{\text{IT energy (kWh)}}
\]

\[
CUE = \frac{\text{location-based carbon emissions (kg CO2e)}}{\text{IT energy (kWh)}}
\]

These follow the concepts defined by ISO/IEC 30134-2 and The Green Grid (ISO, 2016; The Green Grid, 2010a; 2010b). All numerator and denominator values refer to an aligned hourly boundary. Aggregated results are calculated from the validated dataset and reported with absolute energy, water and carbon totals.

The 0–100 sustainability score is a configurable project indicator combining normalised PUE, WUE, carbon, cooling, utilisation and anomaly terms. YAML weights and thresholds make its assumptions visible. The qualitative category “Excellent” applies only within this project. No external benchmark or certification is implied.

## 3.7 Forecasting procedure

### 3.7.1 Targets and features

Separate regressors were trained for `total_energy_kwh`, `cooling_demand_kw` and `water_consumption_l`. Calendar variables and cyclic encodings represent hour and seasonal structure. Lagged values at 1, 24, 48 and 168 hours represent immediate, daily, two-day and weekly memory. Rolling summaries are shifted by one hour before calculation. Thus, a feature at time \(t\) can depend on observations no later than \(t-1\), preventing the current target from entering its predictors.

Rows lacking the history required by lag construction are excluded from model fitting. The remaining observations are sorted chronologically, and the first 80 per cent forms training data while the final 20 per cent forms the test set. The split simulates training on earlier observations and predicting a later period. It is more credible than random row allocation for time-dependent telemetry, although a single split does not estimate performance variation across seasons.

### 3.7.2 Models

The previous-day baseline assigns the value from 24 hours earlier. Three supervised candidates are fitted: Linear Regression, Random Forest and HistGradientBoosting. Linear Regression provides an additive benchmark; Random Forest models nonlinear interactions through averaged trees (Breiman, 2001); and HistGradientBoosting sequentially improves shallow learners using histogram-binned predictors (Friedman, 2001).

For each target, candidate predictions are evaluated on the same chronological test rows. The fitted model with the lowest held-out RMSE is selected and persisted. Although operationally convenient, selection and final reporting on one hold-out may bias the reported winning performance slightly. Future work should reserve a final untouched test period after model tuning.

### 3.7.3 Metrics

MAE, RMSE and R² are calculated:

\[
MAE = \frac{1}{n}\sum_{i=1}^{n}|y_i-\hat{y}_i|
\]

\[
RMSE = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(y_i-\hat{y}_i)^2}
\]

\[
R^2 = 1-\frac{\sum(y_i-\hat{y}_i)^2}{\sum(y_i-\bar{y})^2}
\]

MAE and RMSE retain target units, while R² describes explained variation. Percentage RMSE improvement over baseline is \((RMSE_b-RMSE_m)/RMSE_b \times 100\). Prediction timelines, actual-versus-predicted plots, residual distributions, residual-versus-predicted plots and feature-importance views support diagnosis. Importance is interpreted as model association, not causality.

## 3.8 Anomaly-detection procedure

Isolation Forest was fitted to a multivariate feature set covering energy, cooling, water, PUE, utilisation and carbon. The algorithm isolates sparse observations through random recursive partitions (Liu, Ting and Zhou, 2008). Its output is converted to a binary detection flag according to the configured setup. Ground-truth labels are withheld from fitting and then joined for evaluation.

True positives (TP) are detected injected anomalies; false positives (FP) are detections without injected labels; false negatives (FN) are injected anomalies not detected; and true negatives (TN) are correctly unflagged normal rows. Precision, recall and F1 are:

\[
Precision = \frac{TP}{TP+FP},\quad Recall = \frac{TP}{TP+FN}
\]

\[
F1 = 2\frac{Precision \times Recall}{Precision+Recall}
\]

The full counts are retained because a single score hides alert burden. No accuracy claim is emphasised due to severe class imbalance. The timeline and confusion-matrix figures permit inspection of when detections and labelled events occur.

## 3.9 Recommendation and scenario methods

Recommendations are generated by deterministic rules applied to selected-period evidence. YAML thresholds determine when a KPI or operational measure warrants attention. Outputs identify the relevant evidence and priority. This design supports traceability: the same input and configuration produce the same recommendation.

The Scenario Lab varies selected inputs to illustrate conditional effects. It is a what-if decision aid, not a calibrated digital twin. Neither recommendations nor scenarios were tested on physical infrastructure, and no savings are claimed. Any operational response would require engineering review, safety procedures and site-specific constraints.

## 3.10 Verification and analysis

Evaluation outputs comprise model-comparison and prediction CSVs, KPI summaries, anomaly metrics and events, data-quality and realism reports, recommendations and 21 research figures. Twelve pytest tests cover calculation and integration behaviour. An independent project-validation script performs 19 required checks across artefacts and runtime conditions. Passing both establishes that expected components exist and behave as encoded.

Functional verification is mapped to requirements (Table 3.2). Quantitative results are reported to appropriate precision and checked against machine-readable files. Runtime model loading verifies that dashboards use persisted artefacts. Missing-data and missing-model paths present actionable messages rather than substituting invented output.

**Table 3.2: Evaluation evidence**

| Dimension | Evidence | Interpretive boundary |
|---|---|---|
| KPI validity | Formula tests and aggregate summary | Synthetic boundaries only |
| Forecast skill | Chronological test metrics and baseline | One synthetic year |
| Anomaly detection | Confusion matrix and PR metrics | Injected labels |
| Functional coverage | 12 tests and 19 validator checks | Encoded requirements |
| Presentation | Eleven analytical/domain page groups and figures | No participant usability result |
| Reproducibility | Source commit, configuration and generated outputs | Environment dependence remains |

## 3.11 Reproducibility protocol

Reproduction begins from the identified repository revision and a Python 3.11 environment populated from the declared dependencies. The data-generation module creates the complete hourly CSV from configured random seeds. The forecasting module engineers features, applies the chronological split, compares candidate estimators and writes selected Joblib models and JSON metadata. The audit pipeline then reloads persisted artefacts to produce evaluation tables and figures. Finally, `pytest` and `validate_project.py` provide independent executable checks of expected behaviour and required outputs.

This order is important. Generating figures directly from in-memory training objects could produce results that differ from the models used by the dashboard. Reloading the persisted artefacts confirms that serialisation succeeded and that the reported predictions correspond to deployable files. Machine-readable CSV outputs also permit metric recalculation without extracting values from plotted images.

Reproducibility was assessed as an artefact property rather than by claiming byte-identical execution across every platform. Random seeds constrain stochastic generation and model behaviour, but differences in library versions, parallel execution and numerical implementations can still affect fitted models or timings. The analysed commit, dependency specification, configuration and saved metadata therefore form the minimum reproduction context.

No manual correction of reported metrics was permitted. The final-results summary derives from calculated files, and required runtime artefacts are checked explicitly. If a model or dataset is absent, the interface presents an actionable error instead of training silently or substituting demonstration values. This makes absence observable and protects the link between the evaluated pipeline and displayed evidence.

## 3.12 Methodological validity

Internal validity is strengthened by deterministic generation, leakage-safe features, common test rows and executable metrics. Construct validity is supported by documented KPI formulae and standard regression and classification measures. Reliability is strengthened by versioned code and repeated checks.

External validity is limited because the telemetry is synthetic, covers only two stylised UK sites and contains injected anomaly types. The chosen relationships may be smoother than real plant behaviour. Ecological validity is further limited by the absence of a live operations deployment or participant evaluation. Conclusion validity is constrained by one chronological hold-out and no uncertainty intervals or repeated seeds for every model.

These limitations are addressed by narrowing claims. The study asks about decision-support readiness under reproducible synthetic evaluation. It does not infer real-facility savings, causal interventions, detector reliability in production or improved operator performance.

## 3.13 Chapter summary

The methodology combines DSR artefact construction with comparative machine learning and functional verification. It uses explicit requirements, deterministic multi-site data, defensible KPI calculations, chronological forecasting evaluation, labelled anomaly assessment and executable validation. The design produces inspectable evidence while preserving clear boundaries around synthetic data, rules and user evaluation. Chapter 4 presents the resulting findings.
