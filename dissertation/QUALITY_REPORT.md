# Final quality report

## Deliverables

| Artefact | Path |
|---|---|
| DOCX | `dissertation/AI_Based_Sustainability_Monitoring_System_Dissertation.docx` |
| PDF | `dissertation/AI_Based_Sustainability_Monitoring_System_Dissertation.pdf` |
| Supporting package | `dissertation/` |

## Word counts (chapters 1–5 body, excluding references/appendices)

| Chapter | Words |
|---|---:|
| 1 Introduction | 1,555 |
| 2 Literature | 4,276 |
| 3 Methodology | 2,276 |
| 4 Results | 5,273 |
| 5 Conclusion | 1,548 |
| **Total** | **14,928** |

Within 15,000 ±10% (13,500–16,500). Abstract ≈259 words (separate). References excluded.

## Sources

- Harvard author–date
- ~47 reference-list entries in `chapters/references.md`
- Peer-reviewed and standards sources used for methodology, KPIs, ML and evaluation framing

## Repository evidence

- Analysed commit: `756cc2493cdae4085620b385e7be4f3ce9cfc6af`
- Remote: `https://github.com/Sumukh-g/Sustainability_Monitoring_System_1.git`
- Tests re-run this session: **12/12 passed**
- Validator re-run this session: **19/19 passed**
- PDF pages: **75**

## Evaluation methods used

- Design Science Research framing
- Comparative forecasting (baseline, LR, RF, HistGradientBoosting)
- Isolation Forest metrics against synthetic labels
- KPI verification from generated artefacts
- Functional/runtime verification and screenshots
- No participant usability study (correctly not claimed)

## Principal verified results

- Energy HGB: RMSE 17.41, R² 0.969
- Cooling HGB: RMSE 10.44, R² 0.945
- Water HGB: RMSE 21.37, R² 0.756
- Anomaly F1 0.231 (precision 0.191, recall 0.292)
- Mean PUE 1.23; WUE 0.33 L/kWh; CUE 0.31 kg/kWh; project score ~86/100

## Known limitations (also stated in dissertation)

- Synthetic telemetry; not a real metered facility
- Injected anomaly labels simplify real faults
- Recommendations not physically validated
- Local prototype only (no deployed URL)
- No administered usability study
- UI may show internal brand label; dissertation name is AI-Based Sustainability Monitoring System

## Formatting checks

- US Letter; 1.25" L/R; 1" T/B
- Times New Roman body; 1.5 line spacing
- Chapter starts on new pages
- DOCX→PDF conversion succeeded via docx2pdf
- TOC field requires Update Field in Word before final print/PDF if university requires auto TOC page sync

## Remaining placeholders for you to complete

- `[STUDENT NAME]`, `[STUDENT ID]`, `[UNIVERSITY]`, `[SCHOOL OR DEPARTMENT]`
- `[DEGREE TITLE]`, `[SUPERVISOR NAME]`, `[ACADEMIC YEAR]`, `[SUBMISSION DATE]`
- Declaration signature/date; Acknowledgements text

## Sections to personalise

- Acknowledgements
- Any university-required AI-use declaration (not invented here)
- Title-page degree/university block
- Optional alignment to an official Word template if your school mandates one

## Academic integrity note

Evidence, metrics, screenshots and citations are drawn from the project and verifiable sources. Do not present this as participant research. Follow your university AI-assistance disclosure rules before submission.
