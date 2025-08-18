from __future__ import annotations
from typing import Optional
import pandas as pd

#But : Charger un fichier CSV contenant des données de vol.
def load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    if 'timestamp' not in df.columns:
        raise ValueError('CSV must have a timestamp column')
    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
    df = df.sort_values('timestamp').reset_index(drop=True)
    return df

#But : Enregistrer un DataFrame dans un fichier au format parquet (format compressé et efficace).
def save_parquet(df: pd.DataFrame, path: str) -> None:
    df.to_parquet(path, index=False)
