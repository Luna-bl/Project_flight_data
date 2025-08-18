import sys
import os

# Ajouter le dossier 'src' au chemin de recherche des modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))


import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone
#from src.derive import compute_vertical_speed, segment_phases
#from src.metrics import climb_gradient, tas_stability, descent_energy_rate
from derive import compute_vertical_speed, segment_phases
from metrics import climb_gradient, tas_stability, descent_energy_rate

def make_df(n=10, dt=1.0):
    t0 = datetime(2024,1,1,tzinfo=timezone.utc)
    ts = [t0 + timedelta(seconds=i*dt) for i in range(n)]
    alt = np.linspace(0, 9, n)  # 1 m/s climb
    gs = np.ones(n) * 50.0
    tas = gs.copy()
    df = pd.DataFrame({'timestamp': ts, 'alt_m': alt, 'gs_mps': gs, 'tas_mps': tas})
    return df

def test_vertical_speed_basic():
    df = make_df()
    vs = compute_vertical_speed(df)
    assert abs(vs.iloc[-1] - 1.0) < 0.2

def test_segment_phases_has_labels():
    df = make_df()
    df['vs_mps'] = compute_vertical_speed(df)
    phase = segment_phases(df)
    assert set(phase.unique()) - {'climb', 'cruise', 'descent', 'taxi', 'transition'} == set()

def test_metrics_do_not_crash():
    df = make_df(120)
    df['vs_mps'] = compute_vertical_speed(df)
    df['phase'] = segment_phases(df)
    _ = climb_gradient(df)
    _ = tas_stability(df, window_s=30)
    _ = descent_energy_rate(df)
