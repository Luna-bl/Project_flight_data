#Tu donnes en entrée un fichier CSV avec des données brutes.
#Il « nettoie » et prépare ces données (calcul de vitesse verticale, segmentation).
#Il produit un fichier .parquet prêt à l’usage dans d’autres scripts.
#Il génère des graphiques pour visualiser ces données dans un dossier spécifique.
 
#Ce script correspond à une étape de pré-traitement des données.
#Les fichiers .parquet générés sont utilisés dans les étapes suivantes, 
#par exemple pour calculer des métriques ou générer des rapports.


from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
from rich.console import Console
from src.io import load_csv, save_parquet
from src.derive import compute_vertical_speed, segment_phases
from src.plotting import plot_altitude, plot_vs, plot_planview, plot_speed_phase_timeline
console = Console()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--in', dest='inp', required=True)
    ap.add_argument('--out', dest='outp', required=True)
    args = ap.parse_args()

    console.log(f'Reading {args.inp}')
    df = load_csv(args.inp)

    # Basic sanity: sampling interval estimate
    dt = df['timestamp'].diff().dt.total_seconds().dropna()
    rate_hz = 1.0 / dt.median() if not dt.empty else float('nan')
    console.log(f'Approx sampling rate: {rate_hz:.2f} Hz')

    # Derive vertical speed if missing; smooth a bit
    if 'vs_mps' not in df.columns:
        console.log('Computing vertical speed from altitude...')
        df['vs_mps'] = compute_vertical_speed(df)
    else:
        df['vs_mps'] = df['vs_mps'].fillna(0.0)

    # Phase segmentation
    console.log('Segmenting phases...')
    df['phase'] = segment_phases(df)

    # Output dirs
    outp = Path(args.outp)
    outp.parent.mkdir(parents=True, exist_ok=True)

    # Save cleaned parquet
    console.log(f'Writing cleaned parquet → {outp}')
    save_parquet(df, str(outp))

    # Plots
    figs_dir = Path('docs') / 'figures'
    figs_dir.mkdir(parents=True, exist_ok=True)
    plot_altitude(df, str(figs_dir))
    plot_vs(df, str(figs_dir))
    plot_planview(df, str(figs_dir))
    plot_speed_phase_timeline(df, str(figs_dir))  # 


    console.log('Done. Figures in docs/figures')

if __name__ == '__main__':
    main()
