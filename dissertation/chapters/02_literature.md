WORD_TARGET_NOTE: approx 4300 words

# 2 Literature Review

## 2.1 Introduction

This chapter locates the AI-Based Sustainability Monitoring System within five connected bodies of knowledge: the environmental significance of data centres; sustainability KPIs; forecasting; anomaly detection; and the design and evaluation of operational decision-support software. The review is deliberately critical. It distinguishes standardised measures from project-specific indicators, prediction from causation, and technically correct software from an artefact proven effective in organisational use.

## 2.2 Data-centre sustainability as a systems problem

Data centres convert electrical power into computation while requiring supporting power distribution, cooling, lighting and control systems. Their environmental burden cannot be inferred from IT demand alone because infrastructure overhead, climate, electricity generation and water use vary by site and time. Dayarathna, Wen and Fan (2016) describe data-centre energy consumption through interacting server, network, cooling and power components, showing that optimisation in one subsystem can shift demand elsewhere. Masanet et al. (2020) likewise demonstrate that rapid growth in computing services does not translate mechanically into proportional global electricity growth because hardware, utilisation and infrastructure efficiency change concurrently. The implication for monitoring is that aggregate narratives are insufficient for operational diagnosis.

Recent International Energy Agency analysis identifies data centres as an increasingly important electricity consumer, particularly under growth in accelerated computing and AI (International Energy Agency, 2024). However, global estimates do not answer site-level questions: whether cooling overhead is abnormal, whether a demand peak is predictable, or whether carbon rises because of workload, facility inefficiency or grid intensity. Operational decision support therefore needs granular, temporally aligned evidence.

Electricity is not the sole concern. Cooling technologies may exchange lower electricity demand for higher direct water consumption, while electricity production can embody additional off-site water use (Mytton, 2021). Location-based carbon emissions also vary with grid generation. A facility can improve PUE while its absolute energy or carbon footprint rises through workload growth. Shehabi et al. (2016) emphasise the importance of workload and infrastructure efficiency when assessing sector electricity demand. These interactions justify a multi-domain dashboard but also caution against collapsing diverse impacts into one apparently objective score.

UK operations add a specific carbon context. Government conversion factors provide a recognised basis for greenhouse-gas reporting, although annual factors simplify intra-day variation (Department for Energy Security and Net Zero, 2024). An hourly monitoring artefact can represent changing grid intensity, but its conclusions remain dependent on the factor source and emissions boundary. Consequently, carbon values should be presented as location-based estimates rather than measurements of causal emissions avoided.

## 2.3 Sustainability indicators and measurement boundaries

### 2.3.1 Power Usage Effectiveness

PUE is defined as total data-centre energy divided by IT-equipment energy. It was introduced by The Green Grid (2007) and subsequently standardised in ISO/IEC 30134-2 (ISO, 2016). A value of 1 would imply no supporting overhead; practical values are higher. PUE’s attraction is its simplicity and its ability to reveal the proportion of facility energy not delivered to IT equipment.

That simplicity creates limitations. PUE is a ratio rather than a measure of useful computational output, and it can improve when IT load increases even if total consumption also increases. Boundary choices and temporal aggregation affect comparability. Patterson (2008) argues that PUE must be interpreted with workload and measurement context, while Uptime Institute (2023) reports that industry efficiency gains have slowed. Therefore, a dashboard should show trends and component demand alongside PUE, not rank facilities from the ratio alone.

The project calculates hourly PUE using total facility energy and IT energy within the same period. This is dimensionally coherent because hourly kWh values share a boundary. Invalid, zero or negative IT denominators produce missing values instead of infinities. This defensive behaviour matters: silent division by zero could create extreme points that are then misclassified as operational anomalies.

### 2.3.2 Water Usage Effectiveness

The Green Grid (2010a) defines WUE as annual site water usage divided by IT-equipment energy, conventionally expressed in litres per kWh. WUE makes direct water consumption visible, but comparison requires clarity about water boundaries, climate and cooling technology. Mytton (2021) finds that data-centre water reporting remains inconsistent and argues for attention to both direct and indirect water impacts.

The system uses a synthetic site-water boundary and reports L/kWh IT. It does not claim full lifecycle water accounting. Hourly WUE is valuable for identifying temporal co-movement, but it should not be treated as directly interchangeable with annual public disclosures. Weather and maintenance may create legitimate short-period volatility. Water monitoring is thus strongest when the ratio is accompanied by absolute consumption and cooling context.

### 2.3.3 Carbon Usage Effectiveness

CUE was proposed to relate carbon emissions attributable to data-centre energy to IT-equipment energy (The Green Grid, 2010b). In this project it is expressed as kg CO2e per kWh IT. CUE combines facility efficiency and electricity carbon intensity: two sites with similar PUE can have different CUE values because of their electricity mix. Conversely, a lower-carbon period can improve CUE without a change in physical efficiency.

Carbon accounting requires care about location- versus market-based reporting and temporal resolution. The Greenhouse Gas Protocol Scope 2 Guidance distinguishes contractual instruments from grid-average factors (World Resources Institute and World Business Council for Sustainable Development, 2015). The artefact uses location-based carbon relationships in synthetic data, so it does not represent supplier-specific procurement or embodied equipment emissions. That limitation is a necessary interpretive label, not merely a modelling detail.

### 2.3.4 Composite scores

Composite indicators can reduce cognitive load by summarising multiple dimensions, but weighting and normalisation embed value judgements. The OECD and Joint Research Centre (2008) warn that poor construction can produce misleading policy conclusions. The system’s 0–100 sustainability score combines configurable normalised contributions for PUE, WUE, carbon, cooling, utilisation and anomalies. Its result of approximately 86/100, labelled “Excellent”, is explicitly project-specific. It is not an ISO measure, an industry benchmark or independent certification.

The score is therefore best used as a navigational signal. Operators should be able to inspect contributing measures and YAML-configured thresholds rather than accept a single number. This supports transparency and allows local priorities to be changed without modifying analytical code. It also limits overclaiming: the score describes performance under the artefact’s chosen rules.

## 2.4 Forecasting operational demand

### 2.4.1 Role and evaluation

Forecasting can move monitoring from retrospective description towards preparation. Estimates of future facility energy, cooling demand and water consumption may support staffing, investigation and capacity planning. Yet forecast usefulness depends on horizon, available predictors, temporal validation and comparison with a simple alternative. Hyndman and Athanasopoulos (2021) stress that time-series evaluation should preserve temporal ordering and use benchmark methods because complex models can otherwise appear impressive without adding practical skill.

Mean absolute error (MAE) reports average absolute deviation in the target unit and is comparatively interpretable. Root mean squared error (RMSE) penalises large errors more strongly, which is relevant where missed peaks matter but also makes results sensitive to outliers. R² reports variance explained relative to a mean-based reference, but a high R² does not establish small operational errors or causality. Willmott and Matsuura (2005) argue that MAE and RMSE convey different properties and should not be conflated. The project consequently reports all three metrics and selects models by held-out RMSE.

A previous-day baseline predicts from the same hour 24 hours earlier. Data-centre loads often have strong diurnal regularity, making this more demanding than a global mean. Improvement over this baseline indicates that multivariate and longer-memory features contribute information. It does not show superiority over every statistical or deep-learning method.

### 2.4.2 Linear Regression

Linear Regression offers an interpretable benchmark. It estimates an additive relationship between predictors and target and can perform well where engineered lag variables capture the dominant structure. Its coefficients can indicate model association, although collinearity among lags and rolling summaries weakens direct interpretation. Linear models also struggle with threshold effects and nonlinear interactions between workload and outdoor temperature.

Retaining Linear Regression is methodologically useful even if it is not selected. If an ensemble offers negligible improvement, the simpler model may be preferable because it is faster and easier to inspect. The literature on interpretable modelling cautions against equating a complex model with better explanation (Rudin, 2019).

### 2.4.3 Random Forest

Random Forest builds an ensemble of decorrelated decision trees from bootstrapped data and random feature subsets (Breiman, 2001). It captures nonlinear relationships and interactions without requiring a predefined functional form. Averaging reduces variance compared with an individual tree, making the method a robust tabular-data benchmark.

Its disadvantages include model size, training cost and weak extrapolation beyond observed target regions. Conventional impurity-based feature importance can also favour certain predictor types and should not be interpreted causally. In a monitoring system, these trade-offs support reporting held-out performance and prediction time rather than presenting the algorithm as intrinsically intelligent.

### 2.4.4 Gradient boosting and HistGradientBoosting

Gradient boosting constructs an additive predictor by sequentially correcting residual errors (Friedman, 2001). Histogram-based implementations bin continuous features, reducing computational cost on larger tabular datasets. Scikit-learn’s HistGradientBoostingRegressor supports nonlinear interactions and missing values within a maintained machine-learning library (Pedregosa et al., 2011; scikit-learn developers, 2025).

Boosting can fit complex patterns effectively but requires control of learning rate, tree complexity and iteration count. Held-out chronological testing is therefore essential. The project’s model comparison evaluates fitted candidates on the same final 20 per cent of observations. Selection by test RMSE is suitable for a bounded academic comparison, although repeated use of the same test period for model choice and final reporting risks optimistic selection. A stronger future design would introduce a training/validation/test split or rolling-origin evaluation.

### 2.4.5 Leakage and temporal dependence

Randomly splitting rows from time-dependent data allows nearby or future conditions to influence training and can overstate generalisation. Bergmeir, Hyndman and Koo (2018) discuss cross-validation for autoregressive models, while Cerqueira, Torgo and Mozetič (2020) show that evaluation strategy should reflect non-stationarity. The system uses a chronological 80/20 split and creates 1-, 24-, 48- and 168-hour lags. Rolling statistics are shifted by one hour, so the current target is not included in its own predictor.

Leakage safety is necessary but not sufficient. Some contemporaneous synthetic variables may be known only after the forecast time in a real facility. The experiment demonstrates reproducible predictive modelling under its feature-availability assumptions; deployment would require a formal forecast horizon and source-by-source availability audit.

## 2.5 Anomaly detection

### 2.5.1 Operational meaning

An anomaly is an observation that differs sufficiently from expected behaviour under a defined context. Chandola, Banerjee and Kumar (2009) distinguish point, contextual and collective anomalies. Data-centre faults are often contextual: high cooling demand may be appropriate in hot weather but unusual under low workload and cool conditions. Rule thresholds alone can miss such combinations, whereas multivariate models can identify unusual joint states.

Operational labels are difficult. Fault logs may be incomplete, delayed or aligned to incidents rather than individual sensor intervals. Synthetic injection provides exact labels but simplifies reality because the generating mechanism is known and the event types are bounded. Performance against injected ground truth therefore evaluates algorithm–generator alignment, not production incident detection.

### 2.5.2 Isolation Forest

Isolation Forest isolates observations by recursively choosing random features and split values. Anomalies tend to require shorter path lengths because they occupy sparse regions (Liu, Ting and Zhou, 2008). The method is computationally efficient and does not require labelled training data, making it appropriate when known incidents are scarce.

Several limitations follow. The contamination setting effectively influences the number of flagged observations, and an anomaly score does not identify a root cause. Correlated seasonal behaviour and heterogeneous site distributions can create false positives. Isolation Forest also treats rows as feature vectors unless temporal context is engineered explicitly. For decision support, the detector should therefore expose affected time, site and contributing telemetry and avoid calling every flag a confirmed fault.

### 2.5.3 Evaluation metrics

With rare anomalies, accuracy is misleading because a model predicting every row as normal can appear highly accurate. Precision measures the proportion of detections that match labels; recall measures the proportion of labelled anomalies recovered; and F1 is their harmonic mean. Saito and Rehmsmeier (2015) show why precision–recall analysis is especially informative under class imbalance.

The relative cost of false positives and false negatives depends on operational context. Low precision can cause alert fatigue, while low recall misses incidents. A balanced F1 score is a convenient summary but does not encode these costs. Confusion-matrix counts are consequently needed alongside rates. Threshold calibration should be informed by operator capacity and event severity rather than selected solely for numerical F1.

## 2.6 Recommendations and decision support

Rule-based recommendations connect analytics to action while retaining traceability. A condition such as elevated PUE can trigger a prompt to inspect cooling and power overhead, with priority derived from configured thresholds. External YAML configuration separates operational policy from application logic and supports audit.

This approach is intentionally modest. Rules can be inspected and reproduced, unlike unconstrained generated advice, but they are only as valid as their thresholds and assumptions. Endsley (1995) describes situation awareness as perception, comprehension and projection; the dashboard maps approximately onto these stages through current KPIs, contextual trends and forecasts. It does not complete the decision cycle because a qualified operator must assess constraints and consequences.

Decision-support systems should preserve human authority where actions affect critical infrastructure. Parasuraman, Sheridan and Wickens (2000) show that automation exists at levels from information acquisition to action implementation. The present artefact remains at information analysis and suggested response. It neither actuates equipment nor guarantees savings. Recommendation effectiveness would require intervention studies or validated simulation, neither of which was conducted.

## 2.7 Dashboard and software-quality design

Streamlit supports rapid construction of data applications in Python and integrates with pandas and Plotly (Streamlit, 2025). Plotly provides interactive charts that can expose time-series detail, while pandas supplies tabular transformations (McKinney, 2010; Plotly Technologies, 2025). Joblib persists fitted scikit-learn models so the dashboard need not retrain at each interaction (Joblib developers, 2025). This stack is suitable for a demonstrator, though production use would require authentication, concurrent-load testing, controlled model governance and more durable data services.

The page structure addresses progressive disclosure. Command Center summarises status; domain pages separate energy, water, cooling and carbon; analytical pages expose forecasts and anomalies; Model Intelligence reports evidence; Data Explorer supports inspection; and System Health reports artefact readiness. Consistent filters are important because charts based on different sites or periods can otherwise invite invalid comparison.

Nielsen’s usability heuristics emphasise system-status visibility, consistency, user control and error prevention (Nielsen, 1994). These principles support clear labels, visible data scope and actionable missing-file messages. However, heuristic alignment is not evidence of actual usability. ISO 9241-11 defines usability in relation to specified users, goals and context (ISO, 2018). Because no participant study was administered, the dissertation can report implemented usability provisions but not measured effectiveness, efficiency or satisfaction.

ISO/IEC 25010 frames software quality through characteristics including functional suitability, performance efficiency, compatibility, usability, reliability, security, maintainability and portability (ISO/IEC, 2011). The project’s tests and validator provide evidence mainly for functional suitability and reproducibility. They do not constitute full certification or comprehensive security and performance evaluation.

### 2.7.1 Visual encoding and analytical interpretation

Time-series visualisation is central to operational monitoring because averages can hide short-lived peaks, seasonal changes and site-specific behaviour. A line chart preserves temporal order and can place actual and predicted values on a common axis, while an actual-versus-predicted scatter plot emphasises calibration across the observed range. Residual distributions expose asymmetry and extreme errors that a headline R² may conceal. Each representation answers a different question; duplicating the same metric across decorative charts would add interface complexity without adding evidence.

Visual comparison also introduces risks. Dual axes can imply relationships between quantities with incompatible scales, truncated axes can exaggerate change, and aggregation can suppress anomalies. Filters should therefore display their active site, period and temporal granularity. Units need to remain visible at the point of interpretation rather than only in documentation. These provisions accord with Nielsen’s (1994) principles of visibility and consistency, but they require empirical user evaluation before their practical effectiveness can be claimed.

Dashboard hierarchy affects how uncertainty is perceived. A large composite score may dominate smaller contextual warnings even though the score depends on configurable weights. Similarly, an anomaly badge may be read as a confirmed fault unless the interface distinguishes an unsupervised detection from a labelled incident. Model metrics belong near predictions because confidence should derive from held-out evidence, not merely from a visually smooth forecast line. System Health contributes a separate form of status visibility by indicating whether data and model artefacts are available.

Interactive filtering can improve exploration but also permit accidental comparison of non-equivalent periods. A user may inspect an annual KPI beside a forecast generated for a shorter horizon or compare a site-specific trend with a combined score. Shared state and clear captions reduce this risk. The Data Explorer offers a route from aggregation to individual records, supporting audit where a plotted point appears questionable.

### 2.7.2 Decision-support quality beyond prediction

Prediction accuracy is only one condition of decision-support quality. Outputs must be timely, comprehensible and linked to a feasible decision. Endsley’s (1995) situation-awareness framework indicates that perception without comprehension and projection is incomplete. Conversely, a technically accurate prediction may be operationally irrelevant if it arrives after decisions must be made or omits the constraints needed to act.

The distinction between information and action is especially important in data centres because availability requirements can conflict with sustainability objectives. A recommendation to alter cooling or shift workload may affect resilience, latency or service obligations. Transparent rules can state why an action is suggested, but they cannot encode every local dependency. The appropriate automation level is therefore advisory, consistent with Parasuraman, Sheridan and Wickens (2000): the system acquires and analyses information while a responsible human retains action selection and implementation.

Decision-support evaluation should ultimately examine whether representative users identify conditions correctly, understand uncertainty and choose appropriate responses. ISO 9241-11 defines usability relative to users, goals and context (ISO, 2018), making a generic questionnaire alone insufficient. Task-based observation would be needed to establish effectiveness and efficiency. Since the present project administered no participant study, only design provisions and technical readiness can be reported.

## 2.8 Design Science Research and artefact evaluation

Hevner et al. (2004) position design science at the intersection of relevance, rigour and design cycles. An artefact should address an important problem, draw on a knowledge base and be evaluated. Peffers et al. (2007) operationalise this orientation through the Design Science Research Methodology (DSRM): identify the problem, define solution objectives, design and develop, demonstrate, evaluate and communicate.

The framework is appropriate because this research asks what an integrated monitoring artefact can achieve, not only whether one algorithm is statistically superior. Requirements, interface architecture, data contracts, model persistence and reproducibility are part of the research object. March and Smith (1995) classify design-science outputs as constructs, models, methods and instantiations; this project primarily contributes an instantiation supported by calculation and evaluation methods.

Artefact evaluation must fit the claims made. Venable, Pries-Heje and Baskerville (2016) distinguish artificial and naturalistic evaluation. The present work is predominantly artificial: synthetic telemetry, controlled test splits and executable validation. This supports repeatability and fault isolation but weakens ecological validity. Demonstrating that pages load and models outperform a baseline is not the same as demonstrating improved decisions in a live operations team.

Reproducibility improves transparency. Versioned source, deterministic generation, persisted model metadata, evaluation CSVs and tests enable another researcher to inspect how reported numbers were produced. Peng (2011) argues that reproducible computational research requires a spectrum of accessible code and data. The analysed commit anchors this study to one version. Nonetheless, exact numerical reproduction can still depend on Python and library versions, platform and random-number implementation, so environment documentation remains part of the evidence.

## 2.9 Data integration, governance and operational trust

An integrated dashboard depends on a shared data model. Timestamp, site identity, units and aggregation rules must remain consistent as records pass from ingestion to KPI and model outputs. Without such contracts, apparent agreement between charts can conceal incompatible boundaries. Data Explorer and machine-readable evaluation files provide complementary forms of transparency: the former supports local inspection, while the latter enables independent recalculation.

Model persistence introduces a further governance requirement. A saved estimator is meaningful only when linked to its training features, target, test metrics and software environment. Joblib offers efficient persistence but is not a provenance system and should load only trusted artefacts. JSON metadata partly closes this gap by recording model context. A production design would additionally require an immutable model registry, approval status, checksums, rollback and monitoring of the data distribution.

Trust in analytical decision support should be calibrated rather than maximised indiscriminately. Parasuraman, Sheridan and Wickens (2000) note that inappropriate automation can produce misuse and disuse. A model presented without performance evidence may receive excessive trust; a noisy detector may be ignored after repeated false alerts. Model Intelligence and System Health can support calibration by showing held-out metrics and artefact availability, but effective calibration ultimately requires observation of user behaviour.

Error handling also affects trust. A missing model should not trigger retraining on an unknown slice of data, because the newly produced output would no longer correspond to reported evaluation. Similarly, a missing CSV should not be replaced silently with sample values. Explicit failure messages preserve the distinction between unavailable and unfavourable evidence. This principle supports reproducibility as well as interface integrity.

## 2.10 Alternative analytical approaches

The chosen model set is deliberately bounded. Statistical methods such as exponential smoothing and autoregressive integrated moving-average models offer interpretable temporal benchmarks (Hyndman and Athanasopoulos, 2021). Their explicit treatment of trend and seasonality may be advantageous for stable aggregate demand. More complex recurrent or transformer architectures can learn temporal representations, but they require more data, tuning and governance and are not automatically superior on medium-sized tabular telemetry.

Probabilistic forecasting would add information absent from point estimates. A prediction interval communicates that uncertainty generally widens in volatile periods and permits alerts to consider whether an observation lies outside an expected range. Point RMSE alone cannot distinguish well-calibrated uncertainty from overconfident predictions. For operational planning, quantile loss and interval coverage could therefore complement MAE and RMSE.

Anomaly alternatives include robust statistical limits, one-class support-vector machines, local density methods, autoencoders and supervised classifiers where incident labels are sufficient (Chandola, Banerjee and Kumar, 2009). Rules remain valuable for known engineering limits, while data-driven methods can search for unanticipated combinations. A hybrid architecture could require agreement between contextual residuals and operational rules or use forecast residuals as anomaly features. Such a design may reduce false positives, but its additional complexity would need to be justified through event-level evaluation.

The literature does not identify one universally best method because anomaly meaning depends on context and cost. In a critical facility, a missed high-severity cooling incident may matter more than many low-priority false flags. Binary F1 weights all labelled rows equally. Future evaluation should therefore stratify event type and severity and measure review workload.

## 2.11 Sustainability decisions and rebound effects

Efficiency measures can have indirect consequences. A lower PUE does not necessarily reduce absolute electricity if IT demand grows, and shifting workloads to lower-carbon periods may affect service latency or capacity. Water and energy can also trade off through cooling technology. A decision-support system should make such tensions visible rather than optimise one measure without constraints.

Absolute totals and intensity ratios answer different questions. Totals describe environmental scale; PUE, WUE and CUE describe resource use relative to IT energy. Workload-normalised indicators can help distinguish demand growth from facility overhead, but computational output is not homogeneous: one kWh of IT energy can deliver different useful work depending on hardware and workload. No single denominator captures service value completely.

The project’s composite score is consequently subordinate to its component evidence. A score can direct attention, but a recommendation should identify which measure triggered it and what trade-off an action might introduce. This is particularly important where carbon intensity, water stress and operational resilience have different local priorities. Configurable YAML rules support local adaptation, although configuration itself requires governance and review.

## 2.12 Synthesis and conceptual framework

The literature indicates that decision-support readiness has four necessary dimensions. Measurement validity concerns formulae, units, boundaries and missing-value behaviour. Predictive validity concerns temporal evaluation, benchmark comparison and error interpretation. Diagnostic validity concerns class imbalance, false-alert cost and the gap between unusualness and fault. Artefact validity concerns requirements coverage, navigability, reproducibility and reliable failure handling.

No single KPI or model resolves all four. PUE, WUE and CUE are interpretable but retrospective and boundary-dependent. Forecasting can anticipate demand but depends on stable relationships and available features. Isolation Forest can rank unusual combinations without labels but may generate substantial false alarms. Rule-based advice is transparent but needs physical validation. An integrated system is valuable when it displays these outputs with their limitations, not when it merges them into an unqualified “AI” claim.

This synthesis guides the methodology. KPI outputs are checked against explicit formulae; forecasts are compared on a chronological hold-out against a previous-day baseline; anomaly flags are evaluated against injected labels using a full confusion matrix; and the dashboard is verified through tests and traceability. The main research question is therefore answered in terms of readiness under reproducible synthetic evaluation, not deployment effectiveness.

## 2.13 Chapter summary

Data-centre sustainability is a multi-variable operational problem involving energy, cooling, water and carbon. Standard KPIs provide a foundation but require explicit boundaries and contextual interpretation. Ensemble regressors offer suitable nonlinear forecasting candidates when evaluated chronologically and against baselines. Isolation Forest supports unsupervised detection but its outputs require calibrated thresholds and cautious language. DSR provides a coherent approach for building and evaluating the integrated artefact, while software-quality and usability literature prevents functional verification from being mistaken for user validation. Chapter 3 translates these principles into the project methodology.
