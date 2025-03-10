import os
import pytesseract
import matplotlib.pyplot as plt
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw

# 🔹 Définir le chemin vers Tesseract (Windows uniquement)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 🔹 Récupérer le chemin du dossier contenant le script
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.abspath(os.path.join(script_dir, "..", ".."))

# 🔹 Construire le chemin de l'image originale
image_path = os.path.join(base_dir, "data", "2018", "FAC_2018_0001-654.png")

# 🔹 Vérifier si l'image existe
if not os.path.exists(image_path):
    print(f"❌ Erreur : Le fichier {image_path} n'existe pas.")
    exit()
else:
    print(f"✅ Fichier trouvé : {image_path}")
    image_original = Image.open(image_path)  # Charger l'image originale pour affichage final


# 🔹 Charger l'image avec OpenCV
image_cv = cv2.imread(image_path)

# 🔹 Convertir en niveaux de gris
gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)

# 🔹 Détecter les QR Codes et les masquer
qr_detector = cv2.QRCodeDetector()
retval, points = qr_detector.detect(gray)

if retval:
    points = points.astype(int)
    x_min, y_min = np.min(points[:, :, 0]), np.min(points[:, :, 1])
    x_max, y_max = np.max(points[:, :, 0]), np.max(points[:, :, 1])
    cv2.rectangle(image_cv, (x_min, y_min), (x_max, y_max), (255, 255, 255), thickness=-1)
    print("✅ QR Code détecté et masqué.")

    # 🔹 Détection des contours pour supprimer le cadre près du QR Code
edges = cv2.Canny(gray, 50, 150)  # Détection des bords
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Définir des marges pour élargir la suppression
padding_right = 30  # Ajuste si nécessaire pour supprimer plus à droite
padding_top = 30  # Ajuste si nécessaire pour monter plus haut

for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)

    # Filtrer les rectangles assez grands (cadres) et proches du QR Code
    if w > 50 and h > 50:  
        x_max = min(image_cv.shape[1], x + w + padding_right)  # Élargir la suppression à droite
        y_min = max(0, y - padding_top)  # Monter légèrement pour supprimer plus haut

        # Remplir en blanc la zone élargie
        cv2.rectangle(image_cv, (x, y_min), (x_max, y + h), (255, 255, 255), thickness=-1)
        print(f"✅ Cadre élargi et supprimé : x={x}, y={y_min}, largeur={x_max - x}, hauteur={h}")


# 🔹 Convertir l'image OpenCV en format PIL
image_processed = Image.fromarray(cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB))

# 🔹 Appliquer un traitement avec PIL (niveaux de gris + contraste + agrandissement)
image_processed = image_processed.convert("L")
image_processed = image_processed.filter(ImageFilter.SHARPEN)
enhancer = ImageEnhance.Contrast(image_processed)
image_processed = enhancer.enhance(2.0)
image_processed = image_processed.resize((image_processed.width * 2, image_processed.height * 2), Image.LANCZOS)

# 🔹 Sauvegarder l'image prétraitée
preprocessed_path = os.path.join(base_dir, "data", "2018", "FAC_2018_0001-654_preprocessed.png")
image_processed.save(preprocessed_path)
print(f"✅ Image prétraitée sauvegardée sous : {preprocessed_path}")

# 🔹 Lire le fichier prétraité avec Tesseract
custom_config = "--oem 3 --psm 3"
ocr_text = pytesseract.image_to_string(image_processed, lang="eng", config=custom_config)

# 🔹 Vérifier si du texte est détecté
if not ocr_text.strip():
    print("❌ Aucun texte détecté par Tesseract.")
    exit()

# 🔹 Sauvegarder le texte extrait
text_output_path = os.path.join(base_dir, "data", "2018", "FAC_2018_0001-654_extracted.txt")
with open(text_output_path, "w", encoding="utf-8") as f:
    f.write("📄 Texte extrait par Tesseract OCR :\n\n")
    f.write(ocr_text)
print(f"✅ Texte OCR sauvegardé dans : {text_output_path}")

# 🔹 Dessiner les boîtes de texte détectées sur l'image
image_annotated = image_processed.convert("RGB")
draw = ImageDraw.Draw(image_annotated)

detection_data = pytesseract.image_to_data(image_processed, lang="eng", config=custom_config, output_type=pytesseract.Output.DICT)

# 🔹 Dessiner les boîtes des mots détectés
for i in range(len(detection_data["text"])):
    word = detection_data["text"][i].strip()
    if word:
        x_min = detection_data["left"][i]
        y_min = detection_data["top"][i]
        width = detection_data["width"][i]
        height = detection_data["height"][i]
        x_max, y_max = x_min + width, y_min + height
        y_min, y_max = image_processed.height - y_min, image_processed.height - y_max
        y_min, y_max = min(y_min, y_max), max(y_min, y_max)
        draw.rectangle([(x_min, y_min), (x_max, y_max)], outline="red", width=2)

# 🔹 Sauvegarder l’image annotée
annotated_path = os.path.join(base_dir, "data", "2018", "FAC_2018_0001-654_annotated.png")
image_annotated.save(annotated_path)
print(f"✅ Image annotée sauvegardée sous : {annotated_path}")

# 🔹 Afficher les images côte à côte
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
axes[0].imshow(image_original)
axes[0].set_title("📂 Image Originale")
axes[0].axis("off")
axes[1].imshow(image_processed, cmap="gray")
axes[1].set_title("🎨 Image Traité avec PIL")
axes[1].axis("off")
axes[2].imshow(image_annotated)
axes[2].set_title("🔍 Image Annotée (Tesseract OCR)")
axes[2].axis("off")
plt.show(block=False)
