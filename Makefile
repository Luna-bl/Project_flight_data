.PHONY: setup install test clean inspect metrics report fmt

setup:
	python -m venv .venv

install:
	.venv\Scripts\python -m pip install -r requirements.txt

test:
	.venv\Scripts\python -m pytest -q

clean:
	-rmdir /S /Q data\clean 2>nul || cmd /c "exit 0"
	-del /Q docs\figures\* 2>nul || cmd /c "exit 0"
	-del /Q docs\report.* 2>nul || cmd /c "exit 0"

inspect:
	.venv\Scripts\python -m src.scripts.inspect_clean --in data/raw/flight_sample.csv --out data/clean/cleaned.parquet

metrics:
	.venv\Scripts\python -m src.scripts.compute_metrics --in data/clean/cleaned.parquet --out docs/metrics.json

report:
	.venv\Scripts\python -m src.scripts.generate_report --clean data/clean/cleaned.parquet --metrics docs/metrics.json --out docs/report.md

fmt:
	.venv\Scripts\python - <<'PY'
		from pathlib import Path
		import subprocess
		files=[str(p) for p in Path('src').rglob('*.py')]+[str(p) for p in Path('tests').rglob('*.py')]
		if files:
			subprocess.run(['.venv\\Scripts\\python','-m','black','--quiet',*files])
		else:
			print('No Python files found')
	PY
