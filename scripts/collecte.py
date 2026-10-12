import pandas as pd
import requests

from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
FILE_PATH = DATA_DIR / "eco-counter-data.csv"

# -------------------------
# 1. Charger anciennes données
# -------------------------
try:
    df_old = pd.read_csv(FILE_PATH)

    
    df_old["Date_Heure"] = pd.to_datetime(df_old["Date_Heure"], format="mixed", errors="coerce")
    df_old = df_old.dropna(subset=["Date_Heure"])

    last_date = df_old["Date_Heure"].max().isoformat()

except Exception as e:
    print("ERREUR :", e)
    df_old = pd.DataFrame()
    last_date = "2026-03-11T00:00:00"

print("Dernière date :", last_date)

# -------------------------
# 2. Récupération API 
# -------------------------
url = "https://data.metropole-rouen-normandie.fr/api/explore/v2.1/catalog/datasets/eco-counter-data/records"

all_new_data = []
offset = 0

while True:
    params = {
        "limit": 100,
        "offset": offset,
        "order_by": "date ASC, id ASC",
        "where": f"date >= '{last_date}'"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
    except requests.exceptions.RequestException:
        print("Erreur réseau")
        break

    if response.status_code != 200:
        print("Erreur API :", response.status_code)
        break

    data = response.json()
    records = data.get("results", [])

    if not records:
        break

    all_new_data.extend(records)

    offset += 100

    print(f"{len(all_new_data)} lignes récupérées...")

    if len(records) < 100:
        break

# -------------------------
# 3. Création DataFrame
# -------------------------
df_new = pd.DataFrame(all_new_data)

# transformer location
if "location" in df_new.columns:
    df_new["lat"] = df_new["location"].apply(lambda x: x.get("lat") if isinstance(x, dict) else None)
    df_new["lon"] = df_new["location"].apply(lambda x: x.get("lon") if isinstance(x, dict) else None)
    df_new = df_new.drop(columns=["location"])

df_new.drop_duplicates(inplace=True)

print("\nNouvelles lignes :", len(df_new))

# -------------------------
# 3bis. Stats par jour
# -------------------------
if not df_new.empty:
    df_new["date"] = pd.to_datetime(df_new["date"], format="mixed", errors="coerce")
    df_new = df_new.dropna(subset=["date"])

    counts = df_new["date"].dt.date.value_counts().sort_index()

    print("\n=== Lignes récupérées par jour ===")
    for day, count in counts.items():
        print(f"{day} : {count} lignes")

# -------------------------
# 4. Fusion
# -------------------------
if df_old.empty:
    df = df_new.copy()
elif df_new.empty:
    df = df_old.copy()
else:
    df = pd.concat([df_old, df_new], ignore_index=True)


# -------------------------
# 5. Sauvegarde
# -------------------------
df.to_csv(FILE_PATH, index=False)

print(f"\n[OK] Mise à jour terminée : {len(df)} lignes")