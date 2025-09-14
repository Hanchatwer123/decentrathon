import joblib
from pathlib import Path

def save_model(obj, path: str):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(obj, path)

def load_model(path: str):
    return joblib.load(path)
