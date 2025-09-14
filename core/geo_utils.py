import math
from typing import Tuple

def haversine(lon1, lat1, lon2, lat2) -> float:
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R*c

def trip_length_meters(track_df):
    total = 0.0
    prev = None
    for _, row in track_df.iterrows():
        if prev is not None:
            total += haversine(prev['lng'], prev['lat'], row['lng'], row['lat'])
        prev = row
    return total
