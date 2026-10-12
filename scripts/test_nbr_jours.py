import pandas as pd

from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
FILE_PATH = DATA_DIR / "eco-counter-data.csv"

# Charger avec bon séparateur
df = pd.read_csv(FILE_PATH, sep = ',')

# nettoyer noms colonnes
df.columns = df.columns.str.strip()

print("Colonnes :", df.columns)

# vérifier
if "Date" not in df.columns:
    print("[ERREUR] colonne 'Date' introuvable")
    exit()

# convertir date
df["Date"] = pd.to_datetime(df["Date"], format="mixed", errors="coerce")

df = df.dropna(subset=["Date"])

# filtrer
df_filtered = df[
    (df["Date"].dt.year == 2022) &
    (df["Date"].dt.month == 1) &
    (df["Date"].dt.day.isin([1]))&
    (df["Id"] == 100005524)
]

print("Total lignes :", len(df_filtered))
print(df_filtered["Date"].dt.date.value_counts().sort_index())

print(len(df_filtered["Date_Heure"].unique()))