#Ce script "compute_metrics" sert à prendre un dataset nettoyé de vols, 
#calculer des indicateurs importants (comme le gradient de montée, 
#la stabilité de la vitesse, etc.), 
#puis sauvegarder ces indicateurs dans un fichier JSON, 
#tout en affichant ces résultats dans la console.


from __future__ import annotations
import argparse, json
import pandas as pd
from pathlib import Path
from rich.console import Console
from src.io import load_csv
from src.metrics import climb_gradient, tas_stability, descent_energy_rate

console = Console()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--in', dest='inp', required=True)
    ap.add_argument('--out', dest='outp', required=True)
    args = ap.parse_args()
    console.log(f'Reading cleaned dataset {args.inp}')
    df = pd.read_parquet(args.inp)

    metrics = {
        'climb_gradient_m_per_m': climb_gradient(df),
        'tas_stability_std_mps_over_60s': tas_stability(df, window_s=60),
        'descent_energy_rate_m2_per_s3': descent_energy_rate(df),
    }

    Path(args.outp).parent.mkdir(parents=True, exist_ok=True)
    with open(args.outp, 'w') as f:
        json.dump(metrics, f, indent=2)
    console.log(f'Wrote metrics → {args.outp}')
    for k,v in metrics.items():
        console.log(f'{k}: {v:.4f}' if isinstance(v, (int,float)) else f'{k}: {v}')

if __name__ == '__main__':
    main()
