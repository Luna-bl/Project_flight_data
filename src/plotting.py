from __future__ import annotations
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

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
