WORD_TARGET_NOTE: approx 5200 words

# 4 Results and Discussion

## 4.1 Introduction

This chapter reports and critically interprets the evaluation of the AI-Based Sustainability Monitoring System. It first establishes dataset and KPI outputs, then compares forecasting models, assesses Isolation Forest anomaly detection, examines the integrated dashboard and verifies functional coverage. Results are related directly to the research questions. Numerical values derive from the persisted evaluation artefacts for the analysed commit rather than visual estimation from charts.

## 4.2 Dataset and data-quality results

The generated dataset contained the expected 17,568 rows and 37 columns. London-DC1 and Manchester-DC2 each contributed 8,784 consecutive hourly records, covering the complete 2024 leap year. The period extended from 1 January 2024 00:00 to 31 December 2024 23:00. The row count therefore reconciled exactly with \(2 \times 366 \times 24\), supporting temporal completeness at the designed frequency.

The generator produced workload, IT demand, cooling, facility energy, water, carbon and contextual variables with daily, weekly and seasonal behaviour. A correlation heatmap provides a high-level check that expected synthetic relationships are present (Figure 4.1). Correlation is not physical validation: it confirms that generated variables vary together as designed but does not show that magnitudes reproduce a real UK facility.

There were 288 labelled anomalies, representing approximately 1.64% of all observations. Their rarity creates a realistic evaluation problem in one respect—normal observations dominate—but their exact injection makes ground truth less ambiguous than real incident records. Data-quality checks passed and no schema failure prevented downstream analysis. This supports repeatability of the pipeline but should not be interpreted as evidence about noisy production sensors, delayed records or changing tag names.

**Table 4.1: Dataset summary**

| Property | Result |
|---|---:|
| Sites | 2 |
| Site identifiers | London-DC1; Manchester-DC2 |
| Period | 1 January–31 December 2024 |
| Frequency | Hourly |
| Rows | 17,568 |
| Columns | 37 |
| Labelled anomalies | 288 |

## 4.3 Sustainability KPI results

Across both sites and the full period, total facility electricity was 9,610,651.29 kWh, total site water was 2,596,958.05 litres and location-based carbon emissions were 2,406,388.82 kg CO2e. These are aggregate synthetic quantities rather than measured resource use. Their principal purpose is to provide internally consistent operational telemetry against which KPI logic and visualisation can be evaluated.

Mean PUE was 1.2301 and median PUE was 1.2310. The proximity of mean and median indicates that, at aggregate level, extreme periods did not materially displace the central value. The PUE trend view (Figure 4.2) is more informative than the single annual statistic because it reveals variation associated with workload, cooling demand and anomalies. The value should not be used to claim industry leadership. The project’s facility boundary is synthetic, and cross-facility comparisons require equivalent measurement boundaries and aggregation (ISO, 2016).

Mean WUE was 0.3306 L/kWh IT and median WUE was 0.3158 L/kWh IT. The larger difference between mean and median than for PUE is consistent with a right-skewed water-demand distribution or high-consumption periods. The WUE trend (Figure 4.3) allows such periods to be located. However, this WUE represents direct synthetic site water and does not include electricity-supply water, construction or equipment lifecycle water. It is therefore a bounded operational indicator.

Mean CUE was 0.3141 kg CO2e/kWh IT and median CUE was 0.3137 kg CO2e/kWh IT. Carbon trends (Figure 4.4) combine changing energy consumption and grid-intensity assumptions. This separation matters: a period of lower CUE need not imply improved cooling or electrical efficiency if the grid factor has fallen.

The composite score was 86.17/100, rounded in the interface to 86/100 and categorised as “Excellent”. This category is valid only under the project’s configured normalisation, weights and thresholds. It is not a standard data-centre rating. The dashboard appropriately offers component KPIs so the score is not the sole basis for interpretation.

**Table 4.2: Sustainability results**

| Measure | Mean/total | Median where applicable |
|---|---:|---:|
| Total facility energy | 9,610,651.29 kWh | — |
| Water consumption | 2,596,958.05 L | — |
| Carbon emissions | 2,406,388.82 kg CO2e | — |
| PUE | 1.2301 | 1.2310 |
| WUE | 0.3306 L/kWh IT | 0.3158 |
| CUE | 0.3141 kg CO2e/kWh IT | 0.3137 |
| Project score | 86.17/100 (“Excellent”) | — |

These results answer the first sub-question at the implementation level. PUE, WUE and CUE were generated from aligned quantities, aggregated successfully and presented with explicit units. Defensive denominator handling was verified by tests. Correct implementation does not validate the synthetic input boundary, but it establishes that the dashboard reports internally coherent measures.

## 4.4 Forecasting results

### 4.4.1 Overall comparison

HistGradientBoosting achieved the lowest test RMSE for all three targets and was therefore persisted as the selected model in each case. The result is consistent with the nonlinear relationships in the synthetic generator: histogram gradient boosting can represent interactions among workload, time, weather and lagged demand that are difficult for an additive linear model. Random Forest was competitive but never best. All fitted models outperformed the previous-day baseline.

**Table 4.3: Chronological test-set forecasting results**

| Target | Model | MAE | RMSE | R² | Selected |
|---|---|---:|---:|---:|:---:|
| Total energy (kWh) | HistGradientBoosting | 8.22 | 17.41 | 0.969 | Yes |
|  | Linear Regression | 8.81 | 17.51 | 0.969 | No |
|  | Random Forest | 8.54 | 17.78 | 0.968 | No |
|  | Previous-day baseline | 42.56 | 61.96 | 0.608 | No |
| Cooling demand (kW) | HistGradientBoosting | 8.24 | 10.44 | 0.945 | Yes |
|  | Random Forest | 8.33 | 10.58 | 0.943 | No |
|  | Linear Regression | 11.24 | 14.32 | 0.896 | No |
|  | Previous-day baseline | 21.15 | 27.78 | 0.608 | No |
| Water consumption (L) | HistGradientBoosting | 11.24 | 21.37 | 0.756 | Yes |
|  | Random Forest | 11.25 | 21.44 | 0.755 | No |
|  | Linear Regression | 13.34 | 23.27 | 0.711 | No |
|  | Previous-day baseline | 21.87 | 35.51 | 0.327 | No |

The ranking is credible only for the defined data and split. HistGradientBoosting’s margin over alternatives was small among fitted models, especially for total energy and water. It would be inaccurate to imply that it was overwhelmingly superior to every candidate. Its main advantage was over the previous-day baseline. A future repeated or rolling evaluation might find that model rankings vary over time.

### 4.4.2 Total-energy forecasting

For `total_energy_kwh`, HistGradientBoosting achieved MAE 8.2163 kWh, RMSE 17.4145 kWh and R² 0.9691. Relative to the baseline RMSE of 61.9581 kWh, this is a 71.89% improvement. The model explained approximately 96.9% of held-out variance under the R² definition.

The actual-versus-predicted plot shows observations concentrated near the ideal diagonal (Figure 4.5), while the prediction timeline shows close tracking across most of the test interval (Figure 4.6). Residual plots (Figures 4.7 and 4.8) are necessary because a strong R² can conceal peak errors. RMSE was more than twice MAE, indicating that a smaller number of large deviations materially increased squared error. Such periods may align with injected anomalies or rapid changes not fully captured by lagged features.

Linear Regression produced RMSE 17.5102, only 0.0957 kWh worse than HistGradientBoosting, and R² 0.9687. Random Forest produced RMSE 17.7759. Thus, engineered temporal features captured much of the predictable structure even for a simple additive model. If interpretability and computational simplicity were weighted more heavily than the smallest RMSE, Linear Regression would be a defensible candidate. The chosen rule nevertheless selected HistGradientBoosting consistently by the predefined metric.

The result supports decision-support readiness for identifying expected facility-energy trajectories. It does not show that predicted energy would cause an operator to save energy, nor does it define uncertainty around each prediction. Operational use would benefit from prediction intervals and alert thresholds linked to forecast uncertainty.

### 4.4.3 Cooling-demand forecasting

HistGradientBoosting achieved cooling MAE 8.2391 kW, RMSE 10.4354 kW and R² 0.9447. The 62.44% RMSE improvement over the previous-day baseline (27.7837 kW) demonstrates substantial additional skill. Random Forest was close, at RMSE 10.5831 and R² 0.9431. Linear Regression was materially weaker, at RMSE 14.3212 and R² 0.8958.

This pattern is consistent with nonlinear cooling behaviour. Cooling demand may respond differently to outdoor temperature under different IT loads, and threshold-like plant relationships are not naturally additive. The ensemble methods can represent these interactions. However, because the relationships are generated, this interpretation confirms recovery of simulated structure rather than discovery of real plant thermodynamics.

The actual-versus-predicted chart and timeline (Figures 4.9 and 4.10) show the level of agreement, while residual distribution and residual-versus-predicted charts (Figures 4.11 and 4.12) reveal whether errors change with demand. A model suitable for ordinary periods may still underpredict extreme cooling peaks. As cooling availability affects operational resilience, large errors warrant separate analysis rather than reliance on average metrics.

The cooling result has practical decision-support relevance: the forecast can draw attention to forthcoming demand and allow inspection of temperature, workload and recent cooling history. It should not actuate cooling set points. A physical facility would require equipment constraints, redundancy state and weather forecasts that are outside this model.

### 4.4.4 Water-consumption forecasting

Water was the most difficult target. HistGradientBoosting achieved MAE 11.2389 L, RMSE 21.3708 L and R² 0.7562. This was a 39.82% improvement over baseline RMSE 35.5097 L, but noticeably weaker than energy and cooling performance. Random Forest was almost identical, with RMSE 21.4419 and R² 0.7546. Linear Regression achieved RMSE 23.2652 and R² 0.7111.

The result suggests that the available features explain less of held-out water variability. Water may include intermittent maintenance, cooling-mode transitions and injected events that are less temporally regular than energy. The discrepancy between MAE and RMSE is again notable: RMSE is nearly twice MAE, indicating sizeable errors in a minority of periods. Figures 4.13–4.16 show actual-versus-predicted values, timeline, residual distribution and residual relationship.

Water forecasting still adds value relative to the baseline, but its limitations should affect presentation. A common “high accuracy” label across targets would obscure the lower R² and smaller improvement. The dashboard’s Model Intelligence page enables target-level results, supporting calibrated trust. Future work could model zero-inflated or regime-dependent water behaviour and include cooling-mode state where available.

### 4.4.5 Feature importance and interpretation

Feature-importance figures for the three selected models (Figures 4.17–4.19) identify predictors used most strongly by each fitted estimator. Lagged target values and variables representing workload, time, temperature or related resource demand are expected to be influential given the data-generation logic. These charts assist model diagnosis and can reveal accidental reliance on inappropriate features.

Importance does not establish causal effect. Correlated predictors can substitute for one another, and impurity- or permutation-based measures answer model-specific questions. An operational claim such as “reducing feature X will reduce energy by Y” cannot be derived from these plots. The Scenario Lab is correspondingly framed as exploratory rather than causal optimisation.

### 4.4.6 Training and prediction cost

On the recorded execution, HistGradientBoosting training took approximately 5.45 seconds for energy, 1.12 seconds for cooling and 1.00 second for water. Prediction took about 0.04 seconds for each target. Random Forest training was approximately 7.35–7.73 seconds, while Linear Regression trained in 0.02–0.05 seconds. Hardware and background workload were not controlled, so these timings should not be generalised as benchmarks.

For the prototype, all candidates were fast enough for offline training, and persisted models made page-time retraining unnecessary. The performance result therefore dominated model selection. At production scale, memory, retraining frequency, concurrent inference and monitoring cost would require separate evaluation.

## 4.5 Anomaly-detection results

### 4.5.1 Confusion matrix

Isolation Forest flagged 440 observations. Against the 288 injected labels, the confusion matrix contained 84 true positives, 356 false positives, 204 false negatives and 16,924 true negatives (Table 4.4; Figure 4.20). The counts reconcile to 17,568 observations.

**Table 4.4: Isolation Forest confusion matrix**

|  | Labelled anomaly | Labelled normal |
|---|---:|---:|
| Detected anomaly | TP = 84 | FP = 356 |
| Detected normal | FN = 204 | TN = 16,924 |

Precision was 0.1909, meaning that only about 19% of flags coincided with an injected label. Recall was 0.2917, meaning that about 29% of injected anomalies were recovered. F1 was 0.2308. These values are weak and materially qualify the artefact’s anomaly capability.

Although the detector correctly classified a large majority of all rows as normal, accuracy would be uninformative because normal data dominates. The 356 false positives create over four false alerts for every true positive. If each flag required manual review, this burden could produce alert fatigue. Simultaneously, the 204 false negatives show that most injected anomalies were missed. The detector is therefore suitable as an exploratory unusualness signal, not a dependable incident alarm.

### 4.5.2 Interpretation

Several factors may explain the result. Isolation Forest optimises isolation in feature space, not agreement with the generator’s event labels. Some injected events may be modest after contextual variables are considered, while naturally extreme but unlabelled synthetic observations may be isolated. A single global contamination or score threshold may not suit both sites, seasons and anomaly types. Temporal events extending over several hours may also be better evaluated at event level rather than row level.

The anomaly timeline (Figure 4.21) shows detections and injected labels through time. Clusters permit inspection of whether the algorithm detects portions of an event even when individual hours are missed. Such visual evidence can guide threshold calibration, but manual inspection must not replace predeclared quantitative metrics.

The result illustrates a broader methodological point. Unsupervised algorithms are often selected because labels are unavailable, yet evaluating them requires an operational definition of valuable anomalies. Synthetic labels resolve this for the experiment but encode only injected mechanisms. Improving numerical agreement could overfit the detector to those mechanisms without improving real fault discovery.

### 4.5.3 Decision-support implications

Anomaly Intelligence should expose the score, timestamp, site and accompanying signals, allowing a user to triage rather than accept a binary verdict. Rule-based prioritisation can combine anomaly evidence with threshold breaches, but this does not convert flags into confirmed diagnoses. Language such as “unusual observation” is more accurate than “fault detected”.

The anomaly result answers the third sub-question negatively in performance terms. Isolation Forest did identify some injected events, but precision, recall and F1 were insufficient for high-confidence operational alerting. The honest inclusion of this weak result improves the credibility of the overall evaluation and indicates a precise future-development priority.

## 4.6 Recommendation results

The AI Advisor generated deterministic recommendations from selected-period metrics and YAML thresholds. Each recommendation could be traced to a condition rather than being produced by an opaque generative model. The architecture therefore supports repeatability and policy adjustment without editing core application code.

Recommendations connect domain evidence: elevated PUE can prompt inspection of cooling overhead; water conditions can prompt leak or cooling-mode review; and carbon conditions can prompt examination of timing and grid intensity. Their usefulness lies in structuring attention. They do not prove that the suggested action is technically appropriate for a particular site.

No recommendation was physically implemented or validated. There are therefore no defensible savings, payback or safety results. Any numerical what-if outputs in Scenario Lab represent conditional calculations under project assumptions, not guaranteed outcomes. This distinction is central for critical-infrastructure decision support.

## 4.7 Dashboard and integration results

The implemented interface covers the full intended workflow. Command Center summarises current sustainability status and provides navigation. Energy, Water, Cooling and Carbon Intelligence provide domain trends. Forecast Center presents future-oriented outputs; Anomaly Intelligence presents unusual periods and evaluation evidence; AI Advisor presents rules; Scenario Lab supports assumption exploration; Model Intelligence displays comparative performance; Data Explorer supports record-level inspection; and System Health exposes pipeline and artefact status.

This integration contributes more than a collection of charts. Shared site and time controls allow evidence to be scoped consistently. Persisted models separate expensive training from presentation. Evaluation artefacts make reported model quality visible alongside predictions. Actionable missing-artifact messages avoid silent fallback values, reducing the risk that a polished page conceals absent evidence.

The interface nevertheless has unmeasured qualities. Page existence and runtime checks do not establish that operators can complete tasks efficiently, understand metric boundaries or avoid misinterpreting anomaly flags. Nielsen’s heuristics informed visibility and consistency, but no participant usability study was administered (Nielsen, 1994). The questionnaire in the repository remains unused and provides no quantitative or qualitative findings.

There is no deployed URL. The artefact is a local academic demonstrator intended to show an integrated decision-support pattern for UK data-centre operations. Production readiness would require authentication, access control, secure data ingestion, monitoring, concurrency testing, model governance and integration with operational systems.

## 4.8 Functional verification and reproducibility

All 12 pytest tests passed. All 19 checks in `validate_project.py` also passed. The validator confirms required artefacts and behaviour across data, models, reports and pages rather than merely importing one module. Twenty-one research figures were generated, together with model comparisons, held-out predictions, anomaly metrics, data-quality outputs, KPI summaries and recommendation evidence.

**Table 4.5: Verification summary**

| Verification source | Passed | Total | Result |
|---|---:|---:|---|
| pytest | 12 | 12 | Pass |
| `validate_project.py` | 19 | 19 | Pass |
| Research figures generated | 21 | 21 expected | Complete |

These results support the fourth sub-question: the implemented requirements are covered by executable and persisted evidence. Reproduction is assisted by Python 3.11, explicit dependencies, deterministic generation commands and a source revision. Joblib persistence and JSON metadata link runtime forecasts to evaluated models.

Passing tests does not prove absence of defects. The suite checks selected requirements, not every browser interaction, numerical edge case, security property or deployment environment. Furthermore, generated binary models can be sensitive to library versions. The evidence establishes a repeatable academic artefact rather than production assurance under ISO/IEC 25010.

## 4.9 Research-question synthesis

### 4.9.1 KPI correctness

The first sub-question asked whether KPIs were calculated consistently and presented with appropriate boundaries. The implementation produced coherent aggregate PUE, WUE and CUE values, tests passed, units were explicit and invalid denominators were handled defensively. The project score was labelled as project-specific. KPI readiness is therefore strong within the synthetic boundary, while external comparability remains limited.

### 4.9.2 Forecast accuracy against baseline

The second sub-question asked whether fitted models improve on a previous-day baseline. HistGradientBoosting reduced RMSE by 71.89% for energy, 62.44% for cooling and 39.82% for water. All three fitted model families beat the baseline, and selected-model R² ranged from 0.756 to 0.969. Forecasting provides the strongest quantitative support for anticipatory decision support, especially for energy and cooling. Water performance is useful but less convincing.

### 4.9.3 Anomaly performance

The third sub-question asked how effectively Isolation Forest recovered injected anomalies. With F1 0.231, the answer is: only weakly. False positives and false negatives are both operationally material. The component adds exploratory evidence but is not ready to function as a trusted alarm without calibration, richer temporal features or supervised/semi-supervised alternatives.

### 4.9.4 Requirements coverage and reproducibility

The fourth sub-question asked about requirements and reproducibility. The eleven functional areas, pipeline outputs, 12 tests, 19 validation checks and 21 figures demonstrate broad implementation coverage. Configuration, persisted models and machine-readable reports support inspection. The lack of deployment and participant evaluation restricts the conclusion to technical artefact readiness.

### 4.9.5 Main research question

The main question asks to what extent the integrated artefact can improve decision-support readiness under reproducible evaluation. The results support a qualified positive conclusion. Integration improves readiness by placing validated KPI calculations, substantially baseline-beating forecasts, anomaly evidence, threshold rules and system status within a coherent interface. Reproducibility is strong for an MSc prototype.

However, improvement is uneven. KPI and forecast components are technically convincing in the generated environment; anomaly detection is weak; recommendations remain unvalidated; and no evidence shows changed operator decisions or real resource savings. The system should therefore be described as a credible decision-support demonstrator with a strong forecasting core, not a deployment-ready optimisation platform.

## 4.10 Cross-component discussion

### 4.10.1 From monitoring to readiness

The artefact’s central claim concerns readiness rather than optimisation. Readiness requires that an operator can perceive current conditions, understand their context and inspect plausible future demand. The Command Center and domain pages support perception; KPI decomposition, anomaly context and Data Explorer support comprehension; and the Forecast Center supports projection. AI Advisor then provides a reviewable transition from evidence to a possible response.

This sequence is more defensible than presenting recommendations without provenance. A forecast can be checked against its held-out error, and a recommendation can be checked against its triggering threshold. Nevertheless, the sequence remains informational. It does not show that a user noticed the correct signal, selected an appropriate response or improved an outcome. Those later stages need task-based and operational evaluation.

The system’s technical results suggest that forecasting should receive greater interface prominence than anomaly detection. The selected forecasters beat a credible baseline by 40–72%, while the detector’s precision and recall remained below 0.30. Presenting both with identical confidence styling would be inconsistent with the evidence. A mature interface should distinguish “forecast”, “unusual observation” and “confirmed incident”, and show uncertainty or evaluation status adjacent to each.

### 4.10.2 Relationship between KPI and forecast evidence

KPIs and forecasts answer complementary questions. PUE, WUE and CUE describe resource relationships already observed; target models estimate near-term numerical demand under learned relationships. A low current PUE does not imply low future facility electricity, and a high predicted cooling load may be normal under forecast conditions. Integration permits these distinctions to be inspected in one context.

The total-energy and cooling results are mutually coherent because cooling forms part of facility demand in the synthetic system. Their high R² values should not be treated as independent confirmations of realism: both may reflect the same generator structure. Water’s lower performance is informative because it reveals a target with less regular or less completely modelled variance. This heterogeneity is preferable to an evaluation that reports only the strongest target.

Prediction error can itself become monitoring evidence. Large residuals identify periods where observed demand differs from the model’s conditional expectation. A future hybrid detector could combine residual magnitude, operational thresholds and multivariate unusualness. The present study does not evaluate that architecture, but the residual figures provide a basis for it.

### 4.10.3 Configuration and reproducibility

External YAML thresholds make decision logic visible and editable. This supports reproducibility only when configuration versions accompany outputs. Two executions with identical data and model files but different score weights or recommendation thresholds can produce different decisions. The source commit anchors default configuration, but production governance would need to record active configuration with every alert and report.

Persisted model metadata addresses a similar concern. The dashboard can load the exact model associated with reported metrics rather than training opportunistically from whichever data happen to be present. This design reduces inconsistency between Model Intelligence and live predictions. It does not eliminate model risk: an artefact may load successfully while its input distribution has shifted.

The 12 tests and 19 validation checks create an executable definition of minimum completeness. This is stronger than a manual checklist because failures are repeatable and visible. However, tests can only enforce encoded expectations. If an incorrect scientific assumption is consistently represented in code and tests, all checks may pass. Independent formula review and real-data validation remain necessary.

### 4.10.4 Operational interpretation of false alerts

The anomaly confusion matrix can be translated into review burden. Of 440 detections, 356 were false positives relative to injected labels. For every 100 alerts, only about 19 would match labelled anomalies under these conditions. Even if some “false” detections represent plausible but uninjected unusual states, the evaluation offers no evidence that they are useful. They must therefore remain false positives for reported metrics.

Likewise, the 204 false negatives are not made less important by the large true-negative count. The detector recovered only 84 labelled rows. Depending on event duration, some incidents might receive partial warning, but row-level results do not establish adequate event coverage. A future evaluation should report both event-level detection and time-to-detection while retaining row-level metrics for comparability.

Threshold changes would trade precision against recall. Raising sensitivity might recover more anomalies while increasing already substantial false alerts; lowering sensitivity might improve review burden while missing more incidents. There is no universally correct operating point. Selection should reflect severity and human review capacity and should be validated on data separate from threshold tuning.

### 4.10.5 Comparison with literature

The forecasting findings are consistent with the advantages of tree ensembles on nonlinear tabular data described by Breiman (2001) and Friedman (2001). They also reinforce Hyndman and Athanasopoulos’s (2021) argument for baseline comparison: without the previous-day results, high R² values would lack a practical reference. The small margin between HistGradientBoosting and Linear Regression for energy also supports caution against assuming that complexity is necessary.

The anomaly findings align with Chandola, Banerjee and Kumar’s (2009) warning that contextual definition is fundamental. Isolation Forest efficiently identifies sparse combinations, as proposed by Liu, Ting and Zhou (2008), but sparse does not mean operationally faulty. The result is not a contradiction of the algorithm; it shows a mismatch between its unsupervised objective and injected labels under the selected features and threshold.

The score findings illustrate OECD and Joint Research Centre (2008) concerns about composite indicators. A concise headline is useful, but the “Excellent” category depends on project choices. By retaining PUE, WUE, CUE and absolute totals, the artefact allows the composite to be challenged rather than accepted as an independent fact.

### 4.10.6 Magnitude and practical meaning of forecast errors

The regression metrics retain the unit of each target, but direct comparison across targets remains inappropriate because energy, cooling and water have different scales and operational consequences. An MAE of 8.22 kWh does not imply the same quality as an MAE of 8.24 kW merely because the numbers are similar. R² provides a scale-independent description of explained variance, yet it also depends on test-set variability. The combination of unit errors, R², baseline improvement and residual plots therefore provides a more complete judgement than any single value.

For energy, the very large improvement over the previous-day baseline is more operationally meaningful than the small difference among fitted models. HistGradientBoosting’s RMSE was only 0.10 kWh below Linear Regression and 0.36 kWh below Random Forest after rounding to two decimals. This indicates that feature engineering and the availability of related telemetry contributed much of the gain. The selection rule was followed consistently, but the evidence would not justify dismissing the simpler linear estimator for a deployment that prioritised transparency or easier maintenance.

Cooling differs because Linear Regression’s RMSE was 14.32 kW compared with 10.44 kW for HistGradientBoosting. The larger gap supports the value of nonlinear modelling for this target. Random Forest remained close at 10.58 kW, so the finding supports tree ensembles generally more strongly than one uniquely superior algorithm. A repeated temporal evaluation would be required to determine whether the 0.15 kW difference between the ensembles is stable.

Water produced the lowest R² and smallest baseline improvement. Its HistGradientBoosting and Random Forest results were nearly indistinguishable, differing by approximately 0.07 L in RMSE. The weaker result is not a failure to beat the baseline, but it indicates less dependable point estimates and a greater need to expose error. A dashboard that displayed only the selected model name would conceal this variation in target difficulty.

RMSE exceeding MAE for every target shows that larger errors contribute disproportionately. This is expected mathematically, but the size of the gaps directs attention to peak periods. Operational evaluation should examine whether those periods coincide with high demand or injected events, because underprediction during critical peaks can matter more than similar absolute error during ordinary operation. The current evidence supports this diagnostic question but does not provide a cost-weighted loss function.

### 4.10.7 Evidence hierarchy and claim calibration

The results support different strengths of claim. Directly calculated facts include dataset dimensions, aggregate KPIs, held-out errors and confusion-matrix counts. Functional facts include passing tests, validation checks and generated artefacts. Interpretations—such as the likely role of nonlinear cooling relationships—are plausible explanations grounded in model behaviour and synthetic design, but are not independently measured causal findings.

Claims about decisions and impacts occupy a weaker level. The integrated interface is capable of presenting evidence relevant to a decision, but no participant completed an operational task and no recommendation was implemented. It is therefore valid to state that the artefact supports a decision workflow by design; it is not valid to state that it improved decision quality. Similarly, total synthetic energy and carbon values exercise the monitoring calculations but are not environmental impacts attributable to a real facility.

This hierarchy explains why the main answer is qualified. Reproducible technical readiness is demonstrated through direct evidence. Potential operational usefulness follows from the integration and forecast skill, while realised usefulness remains untested. Maintaining this distinction prevents the strongest result—forecast accuracy—from being used to imply success for the anomaly detector, recommendation rules or complete socio-technical system.

### 4.10.8 Implications for dashboard presentation

The evaluation suggests concrete presentation priorities. Forecast views should identify target, units, test-period metrics and baseline alongside plotted predictions. Water forecasts warrant stronger uncertainty cues than energy forecasts because their held-out fit is weaker. Anomaly views should state that flags are unsupervised and show the low precision and recall where appropriate; a prominent count without this context could imply 440 confirmed incidents.

KPI pages should display absolute totals with intensity ratios. This prevents a favourable PUE from obscuring high total demand and allows users to distinguish facility overhead from environmental scale. The project score should retain its “project-specific” label and make component values accessible. Recommendation cards should show the triggering condition and avoid imperative wording, reflecting their unvalidated advisory status.

System Health and Model Intelligence are consequently part of result communication rather than merely administrative pages. They expose whether required artefacts are present and whether predictions have supporting evaluation. This design cannot guarantee correct interpretation, but it provides the information needed for calibrated use and creates testable hypotheses for a future participant study.

## 4.11 Threats to validity

The principal threat is synthetic-data bias. The same project defines the relationships, anomaly injections and models, so high predictive performance may reflect recoverable generator structure. Two stylised sites cannot represent differences in plant topology, sensor calibration, workload mix or operational practice across UK data centres.

The one-year chronological split provides a meaningful future hold-out but only one seasonal sequence. Model selection and final reporting use the same test portion, introducing selection optimism among the three fitted candidates. No confidence intervals, rolling-origin evaluation or multi-seed sensitivity analysis are reported.

Injected anomaly labels improve metric calculation but simplify incident truth. The row-level confusion matrix may penalise partial event detection and does not weight severity. Conversely, tuning specifically to injections might yield optimistic event recognition without production value.

The score’s weights and “Excellent” label are normative project choices. The system makes them configurable and explicitly non-standard, but a prominent score can still create anchoring. A future interface should show sensitivity to weight changes and the component contribution beside every score.

Functional tests and validation are strong evidence of encoded behaviour, but there was no independent penetration test, load test, accessibility audit or participant usability study. These omissions prevent claims of production quality or demonstrated human effectiveness.

## 4.12 Chapter summary

The artefact produced internally consistent KPI results, strong forecasting performance and complete functional verification. HistGradientBoosting was selected for all targets and substantially improved on the previous-day baseline. In contrast, Isolation Forest achieved low precision, recall and F1, requiring cautious use. The integrated dashboard successfully assembles evidence and recommendations, but synthetic data and absent physical and participant validation restrict the contribution to reproducible decision-support readiness. Chapter 5 concludes the dissertation and defines priorities for real-world validation.
