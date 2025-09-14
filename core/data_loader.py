import pandas as pd
from typing import Tuple

EXPECTED_COLS = ["randomized_id","lat","lng","alt","spd","azm"]

def load_geotracks_from_csv(path_or_buffer) -> pd.DataFrame:
    df = pd.read_csv(path_or_buffer)
    df.columns = [c.strip() for c in df.columns]
    missing = [c for c in EXPECTED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    df = df[EXPECTED_COLS].copy()
    df[['lat','lng','alt','spd','azm']] = df[['lat','lng','alt','spd','azm']].astype(float)
    df['idx'] = df.groupby('randomized_id').cumcount()
    return df
