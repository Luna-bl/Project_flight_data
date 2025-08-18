from __future__ import annotations
import numpy as np
import pandas as pd
from math import atan2, degrees

def compute_vertical_speed(df: pd.DataFrame, dt_seconds: float = 1.0, window: int = 5) -> pd.Series:
    alt = df['alt_m'].to_numpy()
    vs = np.insert(np.diff(alt), 0, 0.0) / dt_seconds
    if window and window > 1:
        vs = pd.Series(vs).rolling(window, min_periods=1, center=True).mean().to_numpy()
    return pd.Series(vs, index=df.index, name='vs_mps')

def compute_ground_track(lat: pd.Series, lon: pd.Series) -> pd.Series:
    lat_rad = np.radians(lat.to_numpy())
    lon_rad = np.radians(lon.to_numpy())
    dlon = np.diff(lon_rad, prepend=lon_rad[0])
    dlat = np.diff(lat_rad, prepend=lat_rad[0])
    y = np.sin(dlon) * np.cos(lat_rad)
    x = np.cos(lat_rad[:-1]) * np.sin(lat_rad[1:]) - np.sin(lat_rad[:-1]) * np.cos(lat_rad[1:]) * np.cos(dlon[1:])
    x = np.insert(x, 0, 0.0)
    hdg = (np.degrees(np.arctan2(y, x)) + 360) % 360
    return pd.Series(hdg, index=lat.index, name='trk_deg')

def segment_phases(df: pd.DataFrame) -> pd.Series:
    # Simple rule-based segmentation by speed and vertical speed thresholds
    gs = df['gs_mps'].fillna(0.0).to_numpy()
    vs = df['vs_mps'].fillna(0.0).to_numpy()
    phase = np.full(len(df), 'unknown', dtype=object)
    for i in range(len(df)):
        if gs[i] < 5 and abs(vs[i]) < 0.5:
            phase[i] = 'taxi'
        elif vs[i] > 1.0:
            phase[i] = 'climb'
        elif vs[i] < -1.0:
            phase[i] = 'descent'
        elif gs[i] >= 20 and abs(vs[i]) <= 0.5:
            phase[i] = 'cruise'
        else:
            phase[i] = 'transition'
    return pd.Series(phase, index=df.index, name='phase')
