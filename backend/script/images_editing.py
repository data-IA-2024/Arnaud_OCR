import os
import pytesseract
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

# 🔹 Charger l'image avec OpenCV (Gestion des erreurs)
image_cv = cv2.imread(image_path)
if image_cv is None:
    raise FileNotFoundError(f"L'image '{image_path}' n'a pas pu être chargée.")

# 🔹 Convertir en niveaux de gris
gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)

# 🔹 Dimensions de l'image
height, width = gray.shape
stroke_width=3
x1= y1= stroke_width
w1=0.4*width-stroke_width
h1=0.14*height-2*stroke_width

x2= w1 *(1+0.6)
y2= stroke_width
w2=0.17*width
h2=h1

x3=stroke_width
y3= h1+stroke_width
w3=width-2*stroke_width
h3=0.86*height-stroke_width
# 🔹 Définition des blocs bien délimités
blocks = {
    "bloc_1": (x1,y1,w1,h1),  # Bloc de "Invoice" au dernier chiffre à 5 chiffres
    "bloc_2": (x2,y2,w2,h2),  # Bloc des 2 encadrés en haut à droite
    "bloc_3": (x3,y3,w3,h3)  # Bloc de tout le reste
}

# 🔹 Dessiner les blocs sur l'image
image_contours = image_cv.copy()
for block_name, coord in blocks.items():
    print(coord)
    x, y, w, h = coord
    cv2.rectangle(gray, (int(x), int(y)), (int(x+w), int(y+h)), (0, 255, 0), stroke_width)
    img=gray[int(y):int(y+h), int(x):int(x+w)]
    cv2.imwrite(block_name+".png",img)
# 🔹 Sauvegarder l'image annotée avec blocs
output_path = os.path.join(base_dir, "data", "2018", "FAC_2018_0001-654_blocks.png")
cv2.imwrite(output_path, gray)
print(f"✅ Image segmentée sauvegardée sous : {output_path}")

# 🔹 OCR par bloc
custom_config = "--oem 3 --psm 6"
extracted_texts = {}

"""
for block_name, (x1, y1, x2, y2) in blocks.items():
    block_image = gray[int(y1):int(y2), int(x1):int(x2)]
    pil_image = Image.fromarray(block_image).convert("L")
    pil_image = pil_image.filter(ImageFilter.SHARPEN)
    enhancer = ImageEnhance.Contrast(pil_image)
    pil_image = enhancer.enhance(2.0)
    text = pytesseract.image_to_string(pil_image, lang="eng", config=custom_config).strip()
    extracted_texts[block_name] = text
    print(f"✅ Texte extrait pour {block_name} :\n{text}\n")

# 🔹 Sauvegarde des textes
text_output_path = os.path.join(base_dir, "data", "2018", "FAC_2018_0001-654_extracted_blocs.txt")
with open(text_output_path, "w", encoding="utf-8") as f:
    for block_name, text in extracted_texts.items():
        f.write(f"[{block_name}]\n{text}\n\n")
print(f"✅ Texte OCR par blocs sauvegardé sous : {text_output_path}")"
"""