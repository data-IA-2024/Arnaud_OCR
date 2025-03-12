import os
import cv2

def open_image(image_path):
    # Charger l'image correctement
    if os.path.isfile(image_path):
        return cv2.imread(image_path)
    raise FileNotFoundError(f"❌ L'image {image_path} n'existe pas.")
    