import os
import cv2
import pytesseract
import glob
from PIL import Image, ImageEnhance
from utils import open_image
from segmentation import rgb_to_gray, extract_blocks
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))

def fix_email_format(email):
    """Corrige les erreurs courantes dans les adresses e-mail."""
    email = email.replace(" ", "").strip()
    if "@" not in email:
        email = email.replace("xample.org", "@example.org")
    return email

def clean_text(text):
    """Supprime les mots indésirables, corrige les caractères spéciaux et ajuste les adresses email."""
    words_to_remove = ["Issue date", "Email", "Adress", "Bill to"]
    lines = text.split("\n")
    
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        for word in words_to_remove:
            if line.startswith(word):
                line = line.replace(word, "").strip()
        
        line = re.sub(r'^[^\w]+|[^\w]+$', '', line)
        line = re.sub(r'([0-9]+)[^0-9x]+x', r'\1 x', line)
        line = re.sub(r'\W$', '', line)
        
        if "example.org" in line or "xample.org" in line:
            line = fix_email_format(line)
        
        # Ajout d'une couleur blanche entre chaque espace
        line = re.sub(r' {2,}', lambda m: m.group(0).replace(" ", "\u2003"), line)
        
        cleaned_lines.append(line)
    
    return "\n".join(cleaned_lines).strip()

def remove_special_chars(text):
    """Supprime les points situés entre une lettre et un chiffre ou un chiffre et une lettre, après chaque mot sauf les symboles seuls comme 'x', et ne touche pas les nombres."""
    text = re.sub(r'(?<=[a-zA-Z])\.(?=\d)|(?<=\d)\.(?=[a-zA-Z])', '', text)  # Supprime les points entre lettres et chiffres
    text = re.sub(r'\b([a-zA-Z]{2,})\.', r'\1', text)  # Supprime les points après chaque mot de 2 lettres ou plus
    return text

def process_invoice(image_path):
    """Applique l'OCR sur une facture et corrige les adresses email mal reconnues."""
    print(f"📄 Traitement du fichier : {image_path}")

    image = open_image(image_path)
    if image is None:
        print(f"❌ Impossible de charger {image_path}")
        return
    
    gray = rgb_to_gray(image)
    blocks = extract_blocks(gray)
    extracted_texts = {}
    custom_config = "--oem 3 --psm 6"
    
    for block_name in ["bloc_facturation", "bloc_table"]:
        if block_name in blocks:
            block = blocks[block_name]
            pil_image = Image.fromarray(block).convert("L")
            enhancer = ImageEnhance.Contrast(pil_image)
            pil_image = enhancer.enhance(2.0)
            
            text = pytesseract.image_to_string(pil_image, lang="eng", config=custom_config).strip()
            text = clean_text(text)
            
            if block_name == "bloc_table":
                text = remove_special_chars(text)
            
            extracted_texts[block_name] = text
            
            text_output_path = image_path.replace(".png", f"_{block_name}.txt")
            with open(text_output_path, "w", encoding="utf-8") as f:
                f.write(text)
            
            print(f"✅ Texte extrait pour {block_name} -> {text_output_path}")

def process_all_invoices():
    """Boucle sur toutes les factures de 2018 à 2024 et applique l'OCR."""
    for year in range(2018, 2025):
        year_dir = os.path.join(data_dir, str(year))
        if os.path.exists(year_dir):
            image_paths = glob.glob(os.path.join(year_dir, "*.png"))
            for image_path in image_paths:
                process_invoice(image_path)
        else:
            print(f"⚠️ Dossier {year_dir} non trouvé.")

if __name__ == "__main__":
    process_all_invoices()
