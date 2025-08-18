from __future__ import annotations
import argparse, json
from pathlib import Path
import pandas as pd

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--clean', required=True)
    ap.add_argument('--metrics', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()

    df = pd.read_parquet(args.clean)
    metrics = json.load(open(args.metrics))

    figures = ['altitude_profile.png', 'vertical_speed.png', 'plan_view.png']
    figures_paths = [str(Path('docs/figures')/f) for f in figures]

    md = []
    md.append('# Flight Data Explorer — Report\n')
    md.append('## Dataset\n')
    md.append(f'- Samples: {len(df)}\n')
    dt = df['timestamp'].diff().dt.total_seconds().dropna()
    sr = 1.0/dt.median() if not dt.empty else float('nan')
    md.append(f'- Approx sampling rate: {sr:.2f} Hz\n')
    md.append('## Metrics\n')
    for k, v in metrics.items():
        md.append(f'- **{k}**: {v}\n')
    md.append('## Figures\n')
    for p in figures_paths:
        md.append(f'![{Path(p).name}]({p})\n')
    md_text = "\n".join(md)

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(md_text, encoding='utf-8')
    print(f'Report written → {args.out}')

if __name__ == '__main__':
    main()
