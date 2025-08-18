.PHONY: setup install test clean inspect metrics report fmt

setup:
	python -m venv .venv

install:
	. .venv/bin/activate && pip install -r requirements.txt

test:
	. .venv/bin/activate && pytest -q

clean:
	rm -rf data/clean docs/figures docs/report.*

inspect:
	. .venv/bin/activate && python -m src.scripts.inspect_clean --in data/raw/flight_sample.csv --out data/clean/cleaned.parquet

metrics:
	. .venv/bin/activate && python -m src.scripts.compute_metrics --in data/clean/cleaned.parquet --out docs/metrics.json

report:
	. .venv/bin/activate && python -m src.scripts.generate_report --clean data/clean/cleaned.parquet --metrics docs/metrics.json --out docs/report.md

fmt:
	python - <<'PY'
from pathlib import Path
import subprocess
files=[str(p) for p in Path('src').rglob('*.py')]+[str(p) for p in Path('tests').rglob('*.py')]
if files:
    subprocess.run(['python','-m','black','--quiet',*files])
else:
    print('No Python files found')
PY
