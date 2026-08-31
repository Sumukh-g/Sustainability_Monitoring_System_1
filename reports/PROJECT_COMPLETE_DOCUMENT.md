# AI-Based Sustainability Monitoring System
## Complete Project Document (Code, Methodology, Tech Stack, Testing & Results)

**Document date:** 31 August 2026  
**Application URL (local):** http://localhost:8501  
**Repository:** https://github.com/Sumukh-g/Sustainability_Monitoring_System_1  
**Status:** Runtime verified after UI fixes and full scenario testing  

---

## 1. Executive summary

This project is a reproducible **decision-support prototype** for UK data-centre sustainability operations. It combines:

- synthetic but physically motivated hourly telemetry for **London-DC1** and **Manchester-DC2**;
- sustainability KPIs (**PUE**, **WUE**, **CUE** and a project-specific score);
- multi-model demand forecasting;
- Isolation Forest anomaly detection;
- threshold alerts and rule-based recommendations;
- a multi-page Streamlit dashboard.

It is **not** autonomous plant control and does **not** claim real facility savings.

On the latest full run:

| Gate | Result |
|------|--------|
| Automated unit/integration tests (`pytest`) | **12/12 passed** |
| Project validator (`validate_project.py`) | **19/19 passed** |
| Scenario tests (`tests/run_scenario_tests.py`) | **13/13 passed** |
| UI sidebar + navigation (`tests/run_ui_sidebar_test.py`) | **PASS** (collapse, reopen, 6 key pages) |
| Streamlit application | **Running** on port 8501 |

---

## 2. Problem and purpose

Data-centre operators need a single place to inspect energy, water, cooling and carbon behaviour, anticipate demand, spot abnormal multivariate patterns, and link observations to candidate actions. In practice those capabilities are often split across monitoring tools, spreadsheets and ad-hoc models.

This artefact addresses that integration gap for an **academic UK operations demo**: two stylised sites, one year of hourly data, transparent metrics, persisted models, and an inspectable dashboard.

---

## 3. Tech stack

| Layer | Technology | Role in this project |
|-------|------------|----------------------|
| Language | Python 3.11 | Core implementation language |
| UI | Streamlit | Multi-page interactive dashboard |
| Data | pandas, NumPy | Telemetry tables, transforms, metrics |
| ML | scikit-learn | Forecasting & Isolation Forest |
| Persistence | Joblib + JSON | Model binaries and metadata |
| Charts | Plotly, Matplotlib | Interactive UI charts and research figures |
| Config | PyYAML | Seeds, targets, thresholds, score weights |
| Testing | pytest, Playwright | Automated logic tests and UI scenarios |
| Storage | CSV files | Generated dataset and evaluation exports |

**Dependencies** are pinned by range in `requirements.txt` (`pandas`, `numpy`, `scikit-learn`, `streamlit`, `plotly`, `PyYAML`, `joblib`, `matplotlib`, `pytest`).

There is **no** cloud deployment URL, database server, or external live BMS integration in the current prototype.

---

## 4. Code architecture

### 4.1 Layout

```text
app.py                 Command Centre (landing page)
pages/                 Domain + AI + explorer pages (11 pages)
ui/                    Theme, CSS, cards, charts, layout helpers
components/            Shared Streamlit helpers
src/                   Data, KPIs, ML, alerts, recommendations, audit
config/                settings.yaml, thresholds.yaml
data/generated/        data_centre_hourly.csv
models/                forecasting/*.joblib, anomaly_detection/*.joblib, metadata/*.json
reports/               evaluation CSVs, figures, FINAL_RESULTS.md, test reports
tests/                 pytest suite + scenario/UI runners
validate_project.py    Mandatory end-to-end artefact audit
```

### 4.2 Core modules (what the code does)

| Module | Responsibility |
|--------|----------------|
| `src/data_generation.py` | Deterministic synthetic hourly generator (seed=42), two UK sites, injected faults |
| `src/data_loader.py` | CSV-only load, schema check, quality validation table |
| `src/preprocessing.py` | Cleaning and time-aware preparation |
| `src/feature_engineering.py` | Cyclic time features, lags, shifted rolling stats (leakage-safe) |
| `src/sustainability_metrics.py` | PUE / WUE / CUE and weighted project score |
| `src/forecasting.py` | Baseline + LR / RF / HistGradientBoosting training, selection, persistence |
| `src/anomaly_detection.py` | Isolation Forest, event enrichment, precision/recall/F1 vs ground truth |
| `src/alerts.py` | Latest-observation threshold alerts |
| `src/recommendations.py` | Deterministic, evidence-linked recommendation table |
| `src/explainability.py` | Feature importance / coefficient magnitude (association, not causation) |
| `src/evaluation.py` / `src/audit_pipeline.py` | Figures, evaluation CSVs, `FINAL_RESULTS.md` |
| `ui/styles.py` | Global CSS (sidebar visibility, overflow/wrapping fixes) |
| `ui/layout.py` | Filters, branding, cached data/config access |

### 4.3 Dashboard pages

1. Command Centre (`app.py`)
2. Energy Intelligence
3. Water Intelligence
4. Cooling Intelligence
5. Carbon Intelligence
6. Forecast Center
7. Anomaly Intelligence
8. AI Advisor
9. Scenario Lab
10. Model Intelligence
11. Data Explorer
12. System Health

Global sidebar filters support site selection and period presets (`24H` / `7D` / `30D` / `90D` / `1Y` / Custom).

---

## 5. Methodology

### 5.1 Research / engineering approach

The system was built as an **artefact-centred** prototype:

1. Define decision-support requirements (monitor → measure → forecast → detect → recommend).
2. Generate reproducible synthetic telemetry with causal-style relationships (workload → IT energy → cooling → water/carbon).
3. Implement transparent KPI formulae with safe division.
4. Engineer leakage-safe features and a **chronological 80/20** hold-out (no shuffle).
5. Compare a previous-day baseline with three regressors; persist the best by RMSE.
6. Fit Isolation Forest and evaluate against injected labels.
7. Surface everything in Streamlit with configuration-driven thresholds.
8. Verify with automated tests, validator checks, scenario scripts and UI automation.

### 5.2 Dataset methodology

- **Seed:** 42  
- **Frequency:** hourly  
- **Period:** 2024-01-01 to 2024-12-31  
- **Sites:** London-DC1, Manchester-DC2  
- **Rows:** 17,568 (8,784 per site)  
- **Columns:** 37  
- **Injected labelled anomalies:** 288  

Synthetic data is labelled as synthetic. It supports reproducible evaluation; it is not metered plant data.

### 5.3 KPI methodology

| KPI | Formula used in code | Notes |
|-----|----------------------|-------|
| PUE | facility energy / IT energy | Dimensionless hourly energy boundary |
| WUE | site water / IT energy | L/kWh IT |
| CUE | location-based carbon / IT energy | kgCO2e/kWh IT |
| Score | Weighted normalised components | **Project-specific**, not an industry standard |

Invalid denominators yield `NaN` rather than infinite values.

### 5.4 Forecasting methodology

**Targets:** `total_energy_kwh`, `cooling_demand_kw`, `water_consumption_l`

**Candidates:**

- Previous-day baseline (`lag_24`)
- Linear Regression
- Random Forest
- HistGradientBoosting

**Features:** weather/IT/utilisation/cooling efficiency + hour/month cyclic encodings + weekday/weekend + target lags (1/24/48/168) + shifted rolling means.

**Selection:** lowest chronological test RMSE; selected model + metadata persisted for dashboard inference (no silent retrain in UI).

### 5.5 Anomaly methodology

Isolation Forest on multivariate features (energy, cooling, water, PUE, utilisation, carbon). Contamination comes from config (`0.025`). Evaluation uses synthetic ground-truth labels to compute precision, recall, F1 and a confusion matrix.

### 5.6 Recommendation methodology

Deterministic rules fire only when selected-period evidence exceeds YAML thresholds (for example elevated mean PUE/WUE or low cooling efficiency). Outputs are structured action records with severity, priority and explanation. They require human engineering review.

---

## 6. UI issues found and fixed

### 6.1 Sidebar could not be reopened

**Root cause:** `ui/styles.py` set `.stApp > header { display: none !important; }`.  
Streamlit’s **expand-sidebar control lives in the header**, so hiding the header removed the only reliable way to reopen a collapsed sidebar.

**Fix:**

- Keep the header visible (transparent styling).
- Force visibility/clickability of collapse/expand controls (`stExpandSidebarButton`, `collapsedControl`, related header buttons).
- Raise z-index so controls are not covered.

**Verified:** Playwright test collapsed sidebar (`aria-expanded=false`) then reopened via `[data-testid="stExpandSidebarButton"]` (`aria-expanded=true`).

### 6.2 Text covered / overlapping

**Contributing causes:**

- Aggressive hidden header reducing top padding.
- Horizontal period radio chips crowding the narrow sidebar.
- Cards/values without wrapping on constrained widths.
- Column/chart overflow.

**Fix:**

- Extra top padding on main content.
- Period radios set to **vertical** layout.
- `overflow-wrap: anywhere` / responsive `clamp()` font sizes on cards and heroes.
- Horizontal blocks wrap; columns use `min-width: 0`; charts capped to container width.

Files changed: `ui/styles.py`, `ui/layout.py`, `ui/cards.py`.

---

## 7. How the system was tested (actual testing)

### 7.1 Tools used

| Tool | Purpose |
|------|---------|
| `pytest` | Unit/integration tests for metrics, preprocessing, forecasting, anomalies, alerts, recommendations |
| `validate_project.py` | Mandatory artefact/behaviour audit (folders, schema, KPIs, models, pages, docs, figures) |
| `python -m src.data_generation` | Fresh dataset regeneration |
| `python -m src.forecasting` | Model training + persistence |
| `python -m src.audit_pipeline` | Anomaly metrics, figures, FINAL_RESULTS |
| `tests/run_scenario_tests.py` | End-to-end operational scenarios against live modules/artefacts |
| Playwright (`tests/run_ui_sidebar_test.py`) | Real browser UI tests against http://localhost:8501 |
| Manual/browser inspection | Confirm Streamlit pages load after restart |

### 7.2 Automated pytest suite (12 tests)

Executed command: `python -m pytest -q`

**Result:** **12 passed** (2 pandas datetime parsing warnings only).

Coverage areas include preprocessing edge cases, KPI maths, forecasting behaviour, anomaly detection, alerts and recommendations.

### 7.3 Project validator (19 checks)

Executed command: `python validate_project.py`

**Result:** **19/19 PASSED**, including dataset, schema, quality, PUE/WUE/CUE, forecast reload, anomaly outputs, recommendations, Streamlit app presence, tests, figures and final research results.

### 7.4 Scenario tests (13 scenarios) — actual operational cases

Executed command: `PYTHONPATH=. python tests/run_scenario_tests.py`  
Evidence file: `reports/SCENARIO_TEST_REPORT.md`

| ID | Scenario | Outcome |
|----|----------|---------|
| S1 | Load dataset; confirm UK sites and 17,568 rows | PASS |
| S2 | Run 9 data-quality checks | PASS (0 failed) |
| S3 | Filter London-DC1 only | PASS (8,784 rows) |
| S4 | Filter last 30 days | PASS (1,442 rows) |
| S5 | Compute sustainability score on filtered window | PASS (≈86.3 Excellent) |
| S6 | Force elevated PUE and confirm alert fires | PASS (1 alert) |
| S7 | Generate recommendations for stressed period | PASS (1 recommendation) |
| S8 | Run Isolation Forest on full dataset | PASS (440 detections, F1≈0.231) |
| S9 | Confirm persisted forecast models + prediction CSVs | PASS |
| S10 | Empty selection → zero recommendations | PASS |
| S11 | Scenario Lab style −10% energy estimate | PASS |
| S12 | Compile all 11 Streamlit page modules | PASS |
| S13 | Confirm sidebar/overflow CSS fixes present | PASS |

### 7.5 UI browser scenarios (Playwright)

Evidence file: `reports/UI_SIDEBAR_TEST.md`

| Scenario | Result |
|----------|--------|
| Command Centre loads with Filters | PASS |
| Collapse sidebar | PASS (`aria-expanded=false`) |
| Reopen sidebar via expand control | PASS (`aria-expanded=true`) |
| Navigate Energy / Forecast / Anomaly / AI Advisor / Scenario Lab / System Health | PASS (no uncaught page exceptions in body text) |

### 7.6 Reproduction commands used

```bash
python -m src.data_generation
python -m src.forecasting
python -m src.audit_pipeline
python -m pytest -q
python validate_project.py
streamlit run app.py
PYTHONPATH=. python tests/run_scenario_tests.py
PYTHONPATH=. python tests/run_ui_sidebar_test.py
```

---

## 8. Results achieved

### 8.1 Forecasting (chronological test set)

Source: `reports/FINAL_RESULTS.md` / `reports/evaluation/model_comparison.csv`

| Target | Best model | MAE | RMSE | R² | RMSE improvement vs baseline |
|--------|------------|-----|------|----|------------------------------|
| total_energy_kwh | HistGradientBoosting | 8.22 | 17.41 | 0.969 | 71.89% |
| cooling_demand_kw | HistGradientBoosting | 8.24 | 10.44 | 0.945 | 62.44% |
| water_consumption_l | HistGradientBoosting | 11.24 | 21.37 | 0.756 | 39.82% |

### 8.2 Anomaly detection

| Metric | Value |
|--------|-------|
| Detections | 440 |
| Precision | 0.191 |
| Recall | 0.292 |
| F1 | 0.231 |
| Confusion | TP 84 / FP 356 / FN 204 / TN 16,924 |

Interpretation: forecasting quality is strong on this synthetic series; anomaly detection is weaker and must be treated cautiously (high false positives relative to injected labels).

### 8.3 Sustainability KPIs (full dataset aggregates)

| KPI | Mean | Median |
|-----|------|--------|
| PUE | 1.2301 | 1.2310 |
| WUE (L/kWh IT) | 0.3306 | 0.3158 |
| CUE (kgCO2e/kWh IT) | 0.3141 | 0.3137 |
| Project score | ~86.2 / 100 (Excellent) | — |

Totals (synthetic year): facility energy ≈ 9.61e6 kWh; water ≈ 2.60e6 L; carbon ≈ 2.41e6 kgCO2e.

### 8.4 Functional readiness

- Dataset, models, metadata, evaluation figures and dashboard pages are present and reloadable.
- Alerts and recommendations trigger on evidence-backed threshold breaches.
- UI sidebar reopen issue is fixed and regression-tested.

---

## 9. Limitations (explicit)

1. Telemetry is **synthetic**, not from a live UK facility meter stream.
2. Anomaly labels are **injected**; real faults are noisier and incomplete.
3. Recommendations are **not physically validated**.
4. No public deployment URL; local Streamlit only.
5. No participant usability study administered.
6. Project sustainability score is **not** an industry standard KPI.

---

## 10. How to run the completed application

```bash
cd Sustainability_Monitoring_System_1
.\.venv\Scripts\activate
pip install -r requirements.txt
python -m src.data_generation
python -m src.forecasting
python -m src.audit_pipeline
pytest
python validate_project.py
streamlit run app.py
```

Then open **http://localhost:8501**.

If the sidebar is closed, use the **expand control** at the top-left of the page (Streamlit chevron / double-arrow). It remains available after the CSS fix.

---

## 11. Evidence index

| Evidence | Path |
|----------|------|
| Final calculated results | `reports/FINAL_RESULTS.md` |
| Scenario test report | `reports/SCENARIO_TEST_REPORT.md` |
| UI sidebar test report | `reports/UI_SIDEBAR_TEST.md` |
| Model comparison | `reports/evaluation/model_comparison.csv` |
| Anomaly metrics | `reports/evaluation/anomaly_metrics.json` |
| Research figures | `reports/figures/` |
| Scenario runner | `tests/run_scenario_tests.py` |
| UI runner | `tests/run_ui_sidebar_test.py` |
| Validator | `validate_project.py` |

---

## 12. Conclusion

The AI-Based Sustainability Monitoring System is a complete, locally runnable decision-support prototype with verified data, models, KPIs, tests and dashboard pages. The critical UI defects (sidebar reopen blocked by hidden header; overlapping/clipped text) were identified, fixed in CSS/layout, and confirmed with Playwright. Quantitative results show strong forecasting on synthetic hold-out data, usable KPI monitoring, and weaker anomaly-detection F1 that is reported transparently rather than overstated.
