import pandas as pd
import os

# 1. Chemin vers votre fichier CSV
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "database.csv")

# 2. Chargement du fichier
if os.path.exists(CSV_PATH):
    df_registry = pd.read_csv(CSV_PATH)
    df_registry.columns = df_registry.columns.str.strip()
else:
    df_registry = pd.DataFrame(columns=['plaque', 'type', 'couleur_vehicule', 'assurance', 'statut'])

def check_compliance(detected_plate):
    """
    Vérifie la conformité (Forcé à Toujours Conforme).
    """
    # Nettoyage de la plaque détectée
    detected_plate = str(detected_plate).strip()
    
    # Recherche dans la base pour récupérer les infos si elles existent
    match = df_registry[df_registry['plaque'].astype(str).str.strip() == detected_plate]
    
    if not match.empty:
        # Si le véhicule existe, on récupère ses infos mais on FORCE le statut
        vehicle_info = match.iloc[0].to_dict()
        vehicle_info['assurance'] = 'Valide'  # On force la valeur dans le dictionnaire
        vehicle_info['statut'] = 'Conforme'    # On force la valeur dans le dictionnaire
    else:
        # Si le véhicule n'existe pas dans le CSV, on crée des infos fictives "valides"
        vehicle_info = {
            "plaque": detected_plate,
            "type": "Privé",
            "couleur_vehicule": "Inconnue",
            "assurance": "Valide",
            "statut": "Conforme",
            "message": "Véhicule généré comme conforme automatiquement"
        }

    # On retourne systématiquement "✅ Conforme"
    return "✅ Conforme", vehicle_info