from __future__ import annotations
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib.patches import Patch


def set_style():
    plt.rcParams['figure.figsize'] = (10, 4)
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.alpha'] = 0.3

def plot_altitude(df: pd.DataFrame, outdir: str) -> str:
    set_style()
    fig = plt.figure()
    ax = plt.gca()
    ax.plot(df['timestamp'], df['alt_m'])
    ax.set_title('Altitude Profile')
    ax.set_xlabel('Time')
    ax.set_ylabel('Altitude [m]')
    out = Path(outdir) / 'altitude_profile.png'
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)
    return str(out)

def plot_vs(df: pd.DataFrame, outdir: str) -> str:
    set_style()
    fig = plt.figure()
    ax = plt.gca()
    ax.plot(df['timestamp'], df['vs_mps'])
    ax.set_title('Vertical Speed')
    ax.set_xlabel('Time')
    ax.set_ylabel('VS [m/s]')
    out = Path(outdir) / 'vertical_speed.png'
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)
    return str(out)

def plot_planview(df: pd.DataFrame, outdir: str) -> str:
    set_style()
    fig = plt.figure()
    ax = plt.gca()
    ax.plot(df['lon'], df['lat'])
    ax.set_title('Plan-View Path')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    out = Path(outdir) / 'plan_view.png'
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)
    return str(out)


def plot_speed_phase_timeline(df: pd.DataFrame, outdir: str) -> str:
    fig, ax = plt.subplots(figsize=(10, 3))
    # On parcourt les phases consécutives pour tracer des barres horizontales
    start_time = df['timestamp'].iloc[0]
    prev_phase = df['phase'].iloc[0]
    phase_start = start_time

    for i, (ts, phase) in enumerate(zip(df['timestamp'], df['phase'])):
        if phase != prev_phase or i == len(df) - 1:
            ax.barh(0, (ts - phase_start).total_seconds(), left=(phase_start - start_time).total_seconds(),
                    height=0.5, label=prev_phase, alpha=0.6)
            phase_start = ts
            prev_phase = phase

    ax.set_yticks([])
    ax.set_xlabel('Time (seconds)')
    ax.set_title('Speed Phase Timeline (Gantt)')
    ax.legend(loc='upper right') 

    out = Path(outdir) / 'speed_phase_timeline.png'
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)
    return str(out)
