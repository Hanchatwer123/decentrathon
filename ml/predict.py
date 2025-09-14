import pandas as pd
from utils.io_helpers import load_model
from core.features import extract_trip_features

def predict_trip_score(tracks_df):
    feats = extract_trip_features(tracks_df)
    model = load_model("ml/models/route_rf.joblib")
    X = feats[["trip_len_m","avg_speed","max_speed","std_speed","elevation_gain"]].fillna(0)
    preds = model.predict(X)
    feats['score'] = preds
    return feats.sort_values('score', ascending=False)
