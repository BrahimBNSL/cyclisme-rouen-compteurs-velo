import pandas as pd

from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
FILE_PATH = DATA_DIR / "eco-counter-data.csv"

df = pd.read_csv(FILE_PATH, sep = ';')

print(df.isna().sum())

# -------------------------
# Nettoyage colonnes inutiles
# -------------------------
#df = df.drop(columns=["Photo", "Date"], errors="ignore")

# -------------------------
# conversion date
# -------------------------
df["Date_Heure"] = pd.to_datetime(df["Date_Heure"], errors="coerce", utc=True).dt.tz_convert(None)
# -------------------------
# nettoyage types
# -------------------------
df["Counts"] = pd.to_numeric(df["Counts"], errors="coerce")

# -------------------------
# suppression valeurs aberrantes
# -------------------------
df = df[df["Counts"] >= 0]
df["Counts"] = df.groupby("Id")["Counts"].transform(
    lambda x: x.clip(upper=x.quantile(0.99))
)

# -------------------------
# tri
# -------------------------
df = df.sort_values(["Id", "Date_Heure"])

# -------------------------
# interpolation 
# -------------------------
df["Counts"] = df.groupby("Id")["Counts"].transform(
    lambda x: x.interpolate(method="linear")
)

# -------------------------
# fallback si trous persistants
# -------------------------
df["Counts"] = df["Counts"].bfill().ffill()

# -------------------------
# feature engineering (IMPORTANT)
# -------------------------
df["heure"] = df["Date_Heure"].dt.hour
df["jour"] = df["Date_Heure"].dt.date
df["jour_semaine"] = df["Date_Heure"].dt.day_name()
df["mois"] = df["Date_Heure"].dt.month
df["annee"] = df["Date_Heure"].dt.year

# -------------------------
# nettoyage texte
# -------------------------
df["Nom"] = df["Nom"].str.strip()

# -------------------------
# optimisation mémoire
# -------------------------
df["Nom"] = df["Nom"].astype("category")
df["Commune"] = df["Commune"].astype("category")

# -------------------------
# gestion location
# -------------------------
if "location" in df.columns:
    df["lat"] = df["location"].apply(lambda x: x.get("lat") if isinstance(x, dict) else None)
    df["lon"] = df["location"].apply(lambda x: x.get("lon") if isinstance(x, dict) else None)
    df = df.drop(columns=["location"])

# -------------------------
# suppression doublons
# -------------------------
df.drop_duplicates(inplace=True)

# -------------------------
# résultats
# -------------------------
print("\nAprès nettoyage :")
print(df.isna().sum())

print(df["Counts"].describe())
print(len(df[df["Counts"] > 100]))

# -------------------------
# 5. Sauvegarde
# -------------------------
print(df.columns)
df.to_csv(DATA_DIR / "data-set-clean.csv", index=False)
print(df.head(10))

print(f"\n[OK] Néttoyage terminée ")
