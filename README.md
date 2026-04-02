# Mitigation Surgeon

A Flask app that performs a "surgical" stress test of Hazard Mitigation Plan files (`.pdf`, `.docx`, `.txt`).

## Features

- Upload and parse plan documents
- Run diagnostics for:
  - historical failure replay
  - BRIC/funding criteria coverage
  - equity and language readiness
  - climate-forward planning signals
- Generate quick policy patch recommendations
- Produce a downloadable PDF report

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:5000`.
