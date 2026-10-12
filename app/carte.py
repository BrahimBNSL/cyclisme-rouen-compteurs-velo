# app/carte.py
import os
import pandas as pd
import requests
from dash import html, dcc, Input, Output
import dash_leaflet as dl
import dash

# ── Chemin dynamique vers le CSV ───────────────────────────
BASE_DIR = os.path.dirname(__file__)  # dossier app/
CSV_PATH = os.path.join(BASE_DIR, "..", "data", "data-set-clean.csv")

print("Chemin utilisé :", os.path.abspath(CSV_PATH))
print("Fichier existe :", os.path.exists(CSV_PATH))

df = pd.read_csv(CSV_PATH) if os.path.exists(CSV_PATH) else pd.DataFrame()

# ── Pistes cyclables ───────────────────────────────────────
def get_pistes_cyclables():
    query = """
    [out:json][timeout:25];
    area["name"="Rouen"]["admin_level"="8"]->.searchArea;
    (
      way["highway"="cycleway"](area.searchArea);
      way["bicycle"="designated"](area.searchArea);
      way["cycleway"="track"](area.searchArea);
      way["cycleway"="lane"](area.searchArea);
    );
    out geom;
    """
    try:
        response = requests.post(
            "https://overpass-api.de/api/interpreter",
            data=query,
            timeout=30
        )
        data = response.json()
        features = []
        for element in data.get("elements", []):
            if "geometry" in element:
                coords = [[pt["lon"], pt["lat"]] for pt in element["geometry"]]
                features.append({
                    "type": "Feature",
                    "geometry": {"type": "LineString", "coordinates": coords},
                    "properties": {}
                })
        return {"type": "FeatureCollection", "features": features}
    except Exception as e:
        print("Erreur Overpass:", e)
        return {"type": "FeatureCollection", "features": []}

pistes_cyclables = get_pistes_cyclables()

# ── Données capteurs ───────────────────────────────────────
liste = [
    100005524, 100005525, 100005527, 100007115, 100007116, 100007117,
    100018089, 100018293, 100018294, 100019265, 100033300, 100033301,
    100033302, 100037866, 100048215, 100056983, 100057696, 100057697,
    300023463, 300027449, 300028856, 300033014, 300035379, 300035391,
    300035455, 300037150, 300040062, 300047382, 300047398
]

if not df.empty:
    liste_cordon = df[df["Id"].isin(liste)][["Id", "Nom", "Coordonnées", "Photo"]].drop_duplicates(subset="Id")
else:
    liste_cordon = pd.DataFrame(columns=["Id", "Nom", "Coordonnées", "Photo"])

points = []
for _, row in liste_cordon.iterrows():
    try:
        lat, lon = row["Coordonnées"].split(",")
        lat, lon = float(lat.strip()), float(lon.strip())
        points.append({
            "nom": row["Nom"],
            "lat": lat,
            "lon": lon,
            "photo": str(row["Photo"]) if pd.notna(row["Photo"]) else "",
        })
    except Exception as e:
        print("Erreur coordonnées:", row["Coordonnées"], e)

options = [{"label": p["nom"], "value": i} for i, p in enumerate(points)]

markers = [
    dl.Marker(position=[p["lat"], p["lon"]], children=dl.Tooltip(p["nom"]))
    for p in points
]

# ── Styles ───────────────────────────────────────────────
img_visible = {"width": "100%", "display": "block", "borderRadius": "10px", "objectFit": "cover"}
img_hidden  = {"display": "none"}
ph_visible  = {"display": "flex", "alignItems": "center", "justifyContent": "center",
               "height": "120px", "color": "#a78bfa", "fontSize": "13px"}
ph_hidden   = {"display": "none"}

# ── Layout ──────────────────────────────────────────────
def carte_layout():
    return html.Div([
        # Card sélecteur
        html.Div([
            html.Div([html.Span("Capteur", className="card-title")], className="card-header"),
            html.Div([
                dcc.Dropdown(id="select-capteur", options=options, placeholder="Rechercher un capteur..."),
                html.Button("← Vue globale", id="btn-reset", n_clicks=0, className="btn-reset", style={"display": "none"}),
            ], className="card-body"),
        ], className="card"),

        # Card carte
        html.Div([
            html.Div([html.Span("Carte", className="card-title")], className="card-header"),
            html.Div([
                dl.Map(
                    id="map",
                    center=[49.4431, 1.0993],
                    zoom=12,
                    children=[
                        dl.TileLayer(url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"),
                        dl.GeoJSON(data=pistes_cyclables, style={"color": "#16a34a", "weight": 3, "opacity": 0.8}),
                        dl.LayerGroup(children=markers),
                    ],
                    style={"width": "100%", "height": "360px"}
                )
            ], className="mini-map-wrapper"),
        ], className="card"),

        # Card photo
        html.Div(
            id="panel-photo",
            children=[
                html.Div([html.Span("Photo", className="card-title")], className="card-header"),
                html.Div([
                    html.Div(id="photo-titre", className="photo-nom"),
                    html.Img(id="photo-img", src="", style=img_hidden),
                    html.Div("Aucune photo disponible", id="photo-placeholder", style=ph_hidden),
                ], className="card-body"),
            ],
            className="card",
            style={"display": "none"}
        ),
    ], className="sidebar-inner")

# ── Callbacks ───────────────────────────────────────────
def register_carte_callbacks(app):
    @app.callback(
        Output("map", "center"),
        Output("map", "zoom"),
        Output("photo-titre", "children"),
        Output("photo-img", "src"),
        Output("photo-img", "style"),
        Output("photo-placeholder", "style"),
        Output("panel-photo", "style"),
        Output("btn-reset", "style"),
        Input("select-capteur", "value"),
        Input("btn-reset", "n_clicks"),
        prevent_initial_call=True
    )
    def update(index, n_clicks):
        ctx = dash.callback_context
        triggered = ctx.triggered[0]["prop_id"]

        btn_style = {
            "display": "block", "width": "100%", "marginTop": "10px", "padding": "9px",
            "background": "#f8f9fc", "border": "1px solid #e8eaf0", "borderRadius": "10px",
            "color": "#8892a4", "fontSize": "12px", "fontFamily": "Outfit, sans-serif",
            "cursor": "pointer"
        }
        card_visible = {
            "display": "block", "background": "#fff", "borderRadius": "14px",
            "border": "1px solid #e8eaf0", "boxShadow": "0 2px 8px rgba(0,0,0,0.04)",
            "overflow": "visible"
        }

        if "btn-reset" in triggered:
            return (
                [49.4431, 1.0993], 12,
                "", "", img_hidden, ph_hidden,
                {"display": "none"}, {"display": "none"}
            )

        if index is not None and 0 <= index < len(points):
            p = points[int(index)]
            photo = p["photo"]
            center, zoom = [p["lat"], p["lon"]], 17

            if photo and photo != "nan":
                return (center, zoom, p["nom"], photo, img_visible, ph_hidden, card_visible, btn_style)
            else:
                return (center, zoom, p["nom"], "", img_hidden, ph_visible, card_visible, btn_style)

        return dash.no_update