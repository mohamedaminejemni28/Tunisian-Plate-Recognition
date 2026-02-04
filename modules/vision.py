import os
import cv2
import numpy as np
import easyocr
import re
from ultralytics import YOLO
import matplotlib.pyplot as plt





# --- CONFIGURATION DES CHEMINS ---
# On récupère le chemin absolu du dossier où se trouve ce script (modules)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# On remonte d'un cran pour atteindre 'models'
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "best1.pt")






# Vérification de sécurité
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f" Le modèle est introuvable ici : {MODEL_PATH}")





# --- INITIALISATION GLOBALE (Une seule fois) ---
print(" Chargement des modèles...")
model = YOLO(MODEL_PATH)
reader = easyocr.Reader(['ar', 'en'], gpu=False) # gpu=True si tu as CUDA configuré


def analyze_image(image_path):
    """
    Analyse une image via son chemin, détecte la plaque et extrait le texte.
    """
    img = cv2.imread(image_path)
    if img is None:
        print(f" Impossible de charger l'image : {image_path}")
        return None

    # Optionnel : Affichage (Attention, plt.show() bloque l'exécution jusqu'à fermeture)
    # img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # plt.imshow(img_rgb); plt.axis("off"); plt.show()

    # 2. Détection avec YOLO
    # Correction : on utilise l'argument 'image_path' passé à la fonction
    results = model.predict(source=img, imgsz=640, conf=0.25, verbose=False)
    
    if len(results[0].boxes) == 0:
        print(" Aucune plaque détectée")
        return None

    print(f" {len(results[0].boxes)} plaque(s) détectée(s)")

    # 3. Extraction et recadrage
    box = results[0].boxes.xyxy[0].cpu().numpy()
    x1, y1, x2, y2 = map(int, box)
    
    h, w = img.shape[:2]
    crop = img[max(0, y1):min(h, y2), max(0, x1):min(w, x2)]

    # 4. Prétraitement OCR
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # 5. Lecture OCR
    ocr_results = reader.readtext(gray, detail=0)
    
    # 6. Post-traitement (Nettoyage)
    corrected_result = [
        " ".join(['تونس' if 'ت' in word or 'TU' in word.upper() else word for word in text.split()])
        for text in ocr_results
    ]

    final_text = " ".join(corrected_result)
    print(f" Texte final  ---> : {final_text}")
    
    return {
        "text": final_text,
        "box": [x1, y1, x2, y2]
    }

# --- TEST ---
if __name__ == "__main__":
    test_path = r"D:\Downloads\SmartALPR_Project\merged_dataset\test\images\4.jpg"
    if os.path.exists(test_path):
        analyze_image(test_path)
    else:
        print(f"  Image de test introuvable : {test_path}")