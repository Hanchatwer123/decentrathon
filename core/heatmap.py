from typing import Optional
import importlib

def generate_heatmap_html(df, lat_col='lat', lng_col='lng') -> str:
    try:
        old = importlib.import_module("old_project.heatmap")
        if hasattr(old, "generate_heatmap_html"):
            return old.generate_heatmap_html(df, lat_col=lat_col, lng_col=lng_col)
    except Exception:
        pass
    import folium
    from folium.plugins import HeatMap
    if df.empty:
        center = [0,0]
    else:
        center = [df[lat_col].median(), df[lng_col].median()]
    m = folium.Map(location=center, zoom_start=12)
    points = df[[lat_col, lng_col]].dropna().values.tolist()
    if points:
        HeatMap(points, radius=8, blur=10).add_to(m)
    return m._repr_html_()
