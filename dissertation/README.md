# Dissertation supporting package

This folder contains the dissertation deliverables for the **AI-Based Sustainability Monitoring System**.

## Outputs

- `AI_Based_Sustainability_Monitoring_System_Dissertation.docx`
- `AI_Based_Sustainability_Monitoring_System_Dissertation.pdf` (if Word/docx2pdf conversion succeeded)
- `chapters/` — source Markdown used to build the document
- `assets/figures/` — evaluation charts copied from `reports/figures`
- `assets/screenshots/` — Streamlit UI captures
- `assets/diagrams/` — architecture diagrams
- `source_register/` — citation register
- `appendices/` — matrices and checklists
- `QUALITY_REPORT.md` — final verification notes

## Word-count rule applied

Main text target: 15,000 words ±10% (13,500–16,500). References and appendices excluded. Abstract counted separately from chapter totals unless university rules state otherwise.

## Rebuild

```bash
python dissertation/_make_diagrams.py
python dissertation/build_dissertation.py
```

Analysed repository commit: `756cc2493cdae4085620b385e7be4f3ce9cfc6af`
