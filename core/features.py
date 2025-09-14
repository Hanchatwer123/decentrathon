import pandas as pd
import numpy as np
from core.geo_utils import trip_length_meters

def extract_trip_features(df: pd.DataFrame) -> pd.DataFrame:
    groups = []
    for tid, g in df.groupby('randomized_id'):
        g = g.sort_values('idx')
        trip_len = trip_length_meters(g)
        avg_speed = g['spd'].mean()
        max_speed = g['spd'].max()
        std_speed = g['spd'].std(ddof=0) if len(g)>1 else 0.0
        elevation_gain = (g['alt'].diff().clip(lower=0).sum())
        num_points = len(g)
        groups.append({
            "randomized_id": tid,
            "trip_len_m": trip_len,
            "avg_speed": float(avg_speed),
            "max_speed": float(max_speed),
            "std_speed": float(np.nan_to_num(std_speed)),
            "elevation_gain": float(elevation_gain),
            "num_points": num_points
        })
    return pd.DataFrame(groups)
