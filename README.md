# Project 1 — Flight Data Explorer

Quickstart:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Inspect & clean
python -m src.scripts.inspect_clean --in data/raw/flight_sample.csv --out data/clean/cleaned.parquet

# Compute metrics & plots
python -m src.scripts.compute_metrics --in data/clean/cleaned.parquet --out docs/metrics.json

# Generate a mini report (markdown + images)
python -m src.scripts.generate_report --clean data/clean/cleaned.parquet --metrics docs/metrics.json --out docs/report.md
```

See `docs/README.md` for the analysis brief.
