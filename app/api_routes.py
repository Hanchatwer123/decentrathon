from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
import io
import pandas as pd
from core.data_loader import load_geotracks_from_csv
from core.heatmap import generate_heatmap_html
from ml.predict import predict_trip_score
from utils.io_helpers import load_model
from core.features import extract_trip_features

router = APIRouter()

@router.post("/upload-tracks")
async def upload_tracks(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files allowed")
    contents = await file.read()
    buffer = io.BytesIO(contents)
    try:
        df = load_geotracks_from_csv(buffer)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    df.to_csv("data/latest_upload.csv", index=False)
    try:
        scores = predict_trip_score(df)
        top_scores = scores.head(10).to_dict(orient='records')
    except Exception:
        top_scores = []
    return JSONResponse({"n_points": len(df), "n_trips": df['randomized_id'].nunique(), "top_trip_scores": top_scores})

@router.get("/heatmap", response_class=HTMLResponse)
def heatmap_view():
    try:
        df = pd.read_csv("data/latest_upload.csv")
    except Exception:
        df = pd.DataFrame(columns=['lat','lng'])
    html = generate_heatmap_html(df)
    return HTMLResponse(content=html)

@router.get("/stats")
def stats_view():
    try:
        df = pd.read_csv("data/latest_upload.csv")
    except Exception:
        raise HTTPException(status_code=404, detail="No uploaded tracks yet")
    feats = extract_trip_features(df)
    summary = {
        "total_trips": int(feats.shape[0]),
        "avg_trip_len_m": float(feats['trip_len_m'].mean() if not feats.empty else 0),
        "avg_speed": float(feats['avg_speed'].mean() if not feats.empty else 0)
    }
    return JSONResponse(summary)
