WORD_TARGET_NOTE: approx 1550 words

# 1 Introduction

## 1.1 Background and context

Data centres are critical infrastructure for contemporary economies, supporting cloud computing, artificial intelligence, public services and everyday digital communication. Their social and economic importance is accompanied by substantial electricity demand and by operational dependencies on cooling systems, water and electricity-grid carbon intensity. International energy assessments consequently identify data centres as a material and rapidly evolving component of electricity demand (International Energy Agency, 2024). The operational problem is not limited to reducing consumption. Facilities must maintain availability while interpreting interacting measurements whose meaning varies with workload, weather, plant condition and site design.

Sustainability monitoring therefore requires more than a static energy total. Power Usage Effectiveness (PUE) relates total facility energy to information-technology energy and is widely used to indicate infrastructure overhead (ISO, 2016; The Green Grid, 2007). Water Usage Effectiveness (WUE) and Carbon Usage Effectiveness (CUE) extend observation to water and carbon impacts (The Green Grid, 2010a; 2010b). These ratios are useful only when boundaries, units and denominators are explicit. They also describe past or present performance rather than anticipated demand. Forecasting and anomaly detection can supplement KPI reporting by identifying likely future loads and unusual multivariate conditions, although neither technique directly establishes causes or guarantees effective intervention.

This dissertation addresses that integration problem through an AI-Based Sustainability Monitoring System. The artefact consists of a Python machine-learning pipeline and multi-page Streamlit dashboard for an academic demonstration of UK data-centre operations decision support. It combines verified KPI calculations, forecasting of total energy, cooling demand and water consumption, Isolation Forest anomaly detection, configurable alerts and deterministic recommendations. The interface may display the internal product label “EcoNexus AI”; throughout this dissertation the artefact is referred to by its research name.

## 1.2 Problem statement

Operational sustainability evidence is commonly dispersed across domain-specific views. Energy, cooling, water and carbon measurements can be reported separately even though they are physically and temporally related. A high cooling load, for example, may be expected during hot weather and high IT utilisation, while the same value under mild conditions may warrant attention. A monitoring design that treats measurements independently can therefore create either missed signals or excessive alerts.

Three related gaps motivate this project. First, KPI correctness requires stable formulae, valid units and defensive handling of invalid denominators. Attractive dashboards do not compensate for incorrect calculations. Secondly, descriptive views alone provide limited preparation for near-term demand. Forecasting should be compared with a credible simple baseline under a chronological evaluation rather than judged from visual fit or random train/test partitions. Thirdly, unsupervised anomaly scores are not equivalent to verified incidents. Their operational value depends on explicit thresholds and evaluation against labels, while labels themselves may be incomplete or artificial (Chandola, Banerjee and Kumar, 2009).

The project consequently treats “AI” as a bounded analytical capability, not as autonomous intelligence. Forecasts estimate associations in the generated telemetry; anomaly detection ranks unusual combinations; and recommendations translate measured conditions into reviewable rules. The system supports human interpretation but does not control cooling equipment, migrate workloads or claim causal environmental savings.

## 1.3 Research aim, question and objectives

The research aim is to design, implement and evaluate an integrated AI-based sustainability monitoring decision-support artefact for UK data-centre operations.

The main research question is:

> To what extent can an integrated forecasting, anomaly-detection and KPI dashboard improve decision-support readiness for data-centre sustainability monitoring under reproducible evaluation on synthetic multi-site telemetry?

Four sub-questions structure the evaluation:

1. Are PUE, WUE, CUE and the project-specific sustainability score calculated consistently and presented with appropriate boundaries?
2. How accurately do Linear Regression, Random Forest and HistGradientBoosting forecast energy, cooling and water demand relative to a previous-day baseline?
3. How effectively does Isolation Forest recover reproducibly injected anomalies, measured using precision, recall and F1?
4. To what extent does the implemented artefact satisfy its functional requirements and support reproducible verification?

The corresponding objectives are to reconstruct and trace the system requirements; design an integrated architecture; implement the data pipeline, analytical models and dashboard; evaluate forecasts, anomalies, KPIs and functional behaviour; and critically discuss validity, limitations and future development.

## 1.4 Scope and boundaries

The evaluated dataset contains 17,568 hourly rows for London-DC1 and Manchester-DC2, covering 1 January to 31 December 2024. Each site contributes 8,784 leap-year observations. Thirty-seven columns represent operational, environmental and derived variables, including 288 injected anomaly labels. The telemetry is synthetic and deterministic. It was chosen to provide a reproducible, complete test bed where relationships and ground truth could be evaluated without access to commercially sensitive facility data.

The analytical scope includes three supervised forecasting targets: `total_energy_kwh`, `cooling_demand_kw` and `water_consumption_l`. Candidate models comprise a previous-day baseline, Linear Regression, Random Forest and HistGradientBoosting. A chronological 80/20 split preserves temporal ordering, and lagged and rolling features are shifted to prevent future target information entering predictors. Isolation Forest supplies unsupervised multivariate anomaly scores. YAML files externalise thresholds used by alerts and recommendations.

The dashboard comprises Command Center, Energy Intelligence, Water Intelligence, Cooling Intelligence, Carbon Intelligence, Forecast Center, Anomaly Intelligence, AI Advisor, Scenario Lab, Model Intelligence, Data Explorer and System Health views. These pages provide an integrated route from overview to evidence and technical status. The Scenario Lab is exploratory; it does not represent a validated physical simulator. Similarly, recommendations are rule-based prompts for investigation rather than instructions proven safe on live infrastructure.

The work excludes deployment to a public URL, connections to building-management systems, autonomous plant control and empirical claims about savings. No participant usability study was administered. An available questionnaire is a future evaluation instrument and supplies no findings. The evaluation is instead limited to quantitative model comparison, KPI outputs, generated figures, automated tests and an executable project validator.

## 1.5 Research approach

Design Science Research (DSR) provides the overarching methodology because the principal contribution is an evaluated software artefact intended to address a practical information problem. Hevner et al. (2004) describe design science as the construction and evaluation of purposeful artefacts, while Peffers et al. (2007) organise work into problem identification, objectives, design and development, demonstration, evaluation and communication. This structure fits the project more closely than a purely observational study.

Evaluation combines three forms of evidence. Comparative machine-learning evaluation measures held-out MAE, RMSE and coefficient of determination (R²), with the previous-day predictor establishing whether model complexity adds value. Anomaly performance is assessed by confusion-matrix counts and derived classification metrics. Functional verification uses 12 pytest tests and 19 checks in `validate_project.py`, supplemented by 21 research figures and machine-readable evaluation outputs. This triangulation establishes computational behaviour and reproducibility; it does not establish organisational adoption or real-world environmental impact.

## 1.6 Contributions

The first contribution is an integrated architecture that turns consistent synthetic telemetry into sustainability indicators, forecasts, anomaly evidence and recommendations within one navigable interface. The value lies in connected evidence: an operator can move from a KPI trend to model performance, anomalous periods and a rule-triggered response without assuming that each output has the same epistemic status.

The second contribution is a reproducible evaluation design. Dataset generation, feature engineering, chronological splitting, persisted models, reports and validation checks are implemented in code. The evaluated revision is commit `756cc2493cdae4085620b385e7be4f3ce9cfc6af` in the public project repository (Gowda, 2026). This identifies the exact artefact under discussion without relying on undocumented manual steps.

The third contribution is critical evidence about unequal analytical maturity. HistGradientBoosting substantially outperforms the previous-day baseline for all targets, whereas Isolation Forest performance is weak: 0.191 precision, 0.292 recall and 0.231 F1. Reporting both outcomes prevents a uniformly positive interpretation of the system and demonstrates why decision-support readiness must be assessed component by component.

## 1.7 Significance of the study

The study is significant in two respects. Practically, it demonstrates how measurements that are often considered separately can be organised around an operational question rather than a technology. Energy, water, cooling and carbon views provide the descriptive foundation; forecasting adds anticipation; anomaly detection supports investigation; and recommendations connect evidence to a reviewable next step. Bringing these capabilities into one artefact does not remove the need for specialist judgement, but it can reduce the effort required to move between disconnected analytical outputs.

Academically, the project provides a bounded test of what “AI-based” sustainability monitoring can credibly mean. The term can encourage attention to model novelty while obscuring measurement validity, baseline performance and software verification. This dissertation instead evaluates each analytical component according to its own evidence. Forecasts are assessed through chronological hold-out errors, anomalies through precision and recall, KPIs through formula and boundary checks, and the complete artefact through traceable functional tests. The resulting account includes negative evidence where the anomaly detector performs poorly.

The work also demonstrates the value of reproducibility for an MSc computing artefact. Source code, deterministic telemetry, persisted models, configuration, tabular results and figures form an inspectable chain from implementation to claim. Another investigator can challenge assumptions or substitute real data without relying solely on screenshots. Reproducibility does not solve the problem of synthetic validity, but it makes that limitation explicit and creates a practical basis for subsequent evaluation.

## 1.8 Dissertation structure

Chapter 2 critically reviews data-centre sustainability metrics, forecasting, anomaly detection, decision-support visualisation and artefact-evaluation literature. Chapter 3 explains the DSR methodology, requirements, dataset, modelling procedures and verification strategy. Chapter 4 reports KPI, forecasting, anomaly and functional results and answers each research question. Chapter 5 synthesises the contributions, limitations and practical implications and proposes evidence-led future work. References follow Harvard Cite Them Right conventions.
