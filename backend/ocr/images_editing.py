import os
import easyocr
import matplotlib.pyplot as plt
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw

# Récupérer le chemin du dossier contenant le script
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.abspath(os.path.join(script_dir, "..", ".."))

# Construire le chemin de l'image originale
image_path = os.path.join(base_dir, "data", "2018", "FAC_2018_0001-654.png")

# Vérifier si l'image existe
if not os.path.exists(image_path):
    print(f"❌ Erreur : Le fichier {image_path} n'existe pas.")
    exit()
else:
    print(f"✅ Fichier trouvé : {image_path}")

# Charger l'image originale
image_original = Image.open(image_path)

# Appliquer un traitement avec PIL (niveaux de gris + contraste)
image_processed = image_original.convert("L")  # Conversion en niveaux de gris
image_processed = image_processed.filter(ImageFilter.SHARPEN)  # Amélioration de la netteté
enhancer = ImageEnhance.Contrast(image_processed)
image_processed = enhancer.enhance(2.0)  # Augmentation du contraste x2

# Sauvegarder l'image prétraitée
preprocessed_path = os.path.join(base_dir, "data", "2018", "FAC_2018_0001-654_preprocessed.png")
image_processed.save(preprocessed_path)
print(f"✅ Image prétraitée sauvegardée sous : {preprocessed_path}")

# Initialiser EasyOCR
reader = easyocr.Reader(['fr'])

# Lire le fichier prétraité avec EasyOCR
results = reader.readtext(preprocessed_path, detail=1)

# Vérifier si EasyOCR a trouvé du texte
print("\n📝 Résultat brut de EasyOCR :", results)
if not results:
    print("❌ Aucun texte détecté par EasyOCR.")
    exit()

# Calculer la moyenne de l'indice de performance (confiance)
total_confidence = sum(confidence for (_, _, confidence) in results)
average_confidence = total_confidence / len(results) if results else 0

# Définir le chemin du fichier texte pour sauvegarder le texte extrait
text_output_path = os.path.join(base_dir, "data", "2018", "FAC_2018_0001-654_extracted.txt")

# Ouvrir le fichier en mode écriture et sauvegarder le texte extrait
with open(text_output_path, "w", encoding="utf-8") as f:
    f.write("📄 Texte extrait par OCR :\n\n")
    
    # Boucle qui ajoute chaque texte extrait dans le fichier
    for (bbox, text, confidence) in results:
        f.write(f"📝 Texte détecté : '{text}'\n")
        f.write(f"🔹 Confiance : {confidence:.2f}\n")

    # Ajouter la moyenne globale de l'indice de performance
    f.write(f"\n📊 Moyenne globale de confiance OCR : {average_confidence:.2f}\n")

print(f"\n✅ Texte OCR sauvegardé dans : {text_output_path}")
print(f"📊 Moyenne globale de confiance OCR : {average_confidence:.2f}")

# Dessiner les boîtes sur l'image pour visualisation
image_annotated = image_processed.convert("RGB")  
draw = ImageDraw.Draw(image_annotated)

# Convertir bbox pour PIL et dessiner les rectangles
for (bbox, text, confidence) in results:
    x_min = min(point[0] for point in bbox)
    y_min = min(point[1] for point in bbox)
    x_max = max(point[0] for point in bbox)
    y_max = max(point[1] for point in bbox)

    draw.rectangle([(x_min, y_min), (x_max, y_max)], outline="red", width=2)

# Sauvegarder l’image annotée
annotated_path = os.path.join(base_dir, "data", "2018", "FAC_2018_0001-654_annotated.png")
image_annotated.save(annotated_path)
print(f"\n✅ Image annotée sauvegardée sous : {annotated_path}")

# Afficher les images côte à côte
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

axes[0].imshow(image_original)
axes[0].set_title("📂 Image Originale", fontsize=14)
axes[0].axis("off")

axes[1].imshow(image_processed, cmap="gray")  
axes[1].set_title("🎨 Image Traité avec PIL", fontsize=14)
axes[1].axis("off")

axes[2].imshow(image_annotated)  
axes[2].set_title("🔍 Image Annotée (OCR)", fontsize=14)
axes[2].axis("off")

plt.show(block=False)
