# Usage du vélo à Rouen : tableau de bord Dash

Application web interactive qui visualise l'usage du vélo dans la métropole de Rouen à partir des données de compteurs Eco-Counter (2022 à 2026). Elle combine une carte des compteurs et des graphiques de fréquentation, avec des scripts de collecte et de nettoyage des données.

## Aperçu

- **Carte** des compteurs (dash-leaflet), avec les communes concernées.
- **Visualisations** de fréquentation (plotly) : évolution, répartition par heure, jour de la semaine et mois.
- **Barre latérale** repliable pour les filtres.

## Structure

```
.
├── app/
│   ├── app.py              Application complète (carte + visualisations)
│   ├── app_petit.py        Version allégée (carte seule)
│   ├── carte.py            Carte des compteurs et callbacks associés
│   ├── layout.py           Mise en page et gabarit HTML
│   └── visualisation.py    Graphiques et callbacks
├── data/
│   ├── eco-counter-data.csv   Données brutes collectées
│   └── data-set-clean.csv     Données nettoyées, utilisées par l'application
└── scripts/
    ├── collecte.py         Interroge l'API open data et met à jour le CSV brut
    ├── nettoyage.py        Contrôle des valeurs manquantes et nettoyage
    ├── recup_capteur.py    Extraction des 29 compteurs retenus
    └── test_nbr_jours.py   Vérification du nombre de jours par compteur
```

## Données

Source : portail open data de la Métropole Rouen Normandie, jeu `eco-counter-data`.
<https://data.metropole-rouen-normandie.fr/explore/dataset/eco-counter-data/>

Le fichier nettoyé contient environ 878 000 lignes et les colonnes suivantes :

| Colonne | Description |
|---|---|
| `Id`, `Nom` | Identifiant et nom du compteur |
| `Année`, `Date`, `Date_Heure` | Date et heure de la mesure |
| `Commune` | Commune du compteur |
| `Counts` | Nombre de passages mesurés |
| `Mode` | Mode de déplacement (ici : vélo) |
| `Coordonnées` | Latitude, longitude |
| `heure`, `jour`, `jour_semaine`, `mois`, `annee` | Variables dérivées pour l'analyse |

Les données couvrent 2022 à 2026, et les compteurs sont majoritairement situés à Rouen, Mont-Saint-Aignan, Bois-Guillaume et Bihorel.

## Installation

Python 3.10 ou plus récent est recommandé.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install dash plotly dash-leaflet pandas requests
```

Il n'y a pas de fichier `requirements.txt` pour l'instant : les dépendances ci-dessus sont celles importées par le code.

## Lancement

```bash
cd app
python app.py
```

L'application est ensuite disponible sur <http://127.0.0.1:5003>.

Pour la version allégée, lancez `python app_petit.py` à la place.

## Mise à jour des données

```bash
cd scripts
python collecte.py      # ajoute les nouvelles mesures au fichier brut
python nettoyage.py     # produit le fichier nettoyé
```

`collecte.py` interroge l'API open data, fusionne les nouvelles mesures avec l'existant, puis réécrit `eco-counter-data.csv`. Une sauvegarde préalable est conseillée.


## Auteurs

Projet annuel réalisé en binôme :

- **Brahim Bensalah** : Master 2 Intelligence Artificielle, Université Abderrahmane Mira de Béjaïa
- **Mohend Laid Ainas** : Master 1, Université de Rouen
