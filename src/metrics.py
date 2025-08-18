#Ce fichier metrics.py contient les fonctions qui calculent des métriques physiques 
#à partir des données de vol nettoyées (altitude, vitesse, phases de vol, etc.).
#Il est utilisé dans l’étape où tu exécutes

from __future__ import annotations
import numpy as np
import pandas as pd

def climb_gradient(df: pd.DataFrame) -> float:
    # gradient = delta_alt / horizontal_distance. Approx via ground speed * time during climb.
    dt = df['timestamp'].diff().dt.total_seconds().fillna(0.0).to_numpy()
    climb_mask = (df['phase'] == 'climb').to_numpy()
    alt = df['alt_m'].to_numpy()
    gs = df['gs_mps'].to_numpy()
    delta_alt = (alt[climb_mask][-1] - alt[climb_mask][0]) if climb_mask.any() else 0.0
    horiz_dist = (gs[climb_mask] * dt[climb_mask]).sum() if climb_mask.any() else 0.0
    if horiz_dist <= 1e-6:
        return float('nan')
    return delta_alt / horiz_dist  # unitless (m/m)

def tas_stability(df: pd.DataFrame, window_s: int = 60) -> float:
    # Std of TAS over cruise segments aggregated by window; return mean windowed std.
    if 'tas_mps' not in df.columns:
        return float('nan')
    cruise = df[df['phase'] == 'cruise']
    if cruise.empty:
        return float('nan')
    cruise = cruise.set_index('timestamp').sort_index()
    roll = cruise['tas_mps'].rolling(f'{window_s}s').std().dropna()
    return float(roll.mean()) if not roll.empty else float('nan')

def descent_energy_rate(df: pd.DataFrame) -> float:
    # Approx potential energy change rate during descent: dE/dt = m*g*vs (m cancels if relative)
    g = 9.80665
    desc = df[df['phase'] == 'descent']
    if desc.empty:
        return float('nan')
    vs = desc['vs_mps'].to_numpy()
    return float(np.mean(g * vs))  # J/(s*kg) = m^2/s^3
