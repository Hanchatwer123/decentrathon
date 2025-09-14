import pandas as pd
import numpy as np
import joblib
import hdbscan
import numpy as np

def train_hotspots(df, min_samples=10, xi=0.05, min_cluster_size=50):
    coords = df[['lat', 'lng']].to_numpy()
    coords_rad = np.radians(coords)
    clusterer = hdbscan.HDBSCAN(
        min_samples=min_samples,
        min_cluster_size=min_cluster_size,
        metric='haversine',             
        cluster_selection_epsilon=xi    
    )
    labels = clusterer.fit_predict(coords_rad)
    df['cluster'] = labels

    return df, clusterer

def save_model(model, path="models/optics_model.pkl"):
    joblib.dump(model, path)
    print(f"Модель сохранена в {path}")

def run_training_pipeline(csv_path):
    df = pd.read_csv(csv_path)
    print(f"Загружено {len(df)} точек")
    df, model = train_hotspots(df)
    save_model(model)
    df.to_csv("data/clustered_astana.csv", index=False)
    print("Результаты сохранены в data/clustered_astana.csv")

if __name__ == "__main__":
    run_training_pipeline("data/geo_locations_astana_hackathon.csv")
