import os
import cv2
import pytesseract
import glob
from PIL import Image, ImageEnhance
import re

# 🔹 Définir le chemin exact du dossier DATA/2024
DATA_DIR = r"C:\Users\mpadmin\Documents\projet-OCR\data\2024"

def extract_invoice_details(facturation_text, table_text):
    """ Extrait les informations essentielles d'une facture OCR """
    invoice_data = {
        "no": None,
        "date": None,
        "name": None,
        "email": None,
        "total": None
    }
    match = re.search(r'INVOICE (\S+)', facturation_text)
    if match:
        invoice_data["no"] = match.group(1)
    match = re.search(r'\d{4}-\d{2}-\d{2}', facturation_text)
    if match:
        invoice_data["date"] = match.group()
    lines = facturation_text.split("\n")
    for line in lines:
        if "@" in line:
            email_line_index = lines.index(line)
            invoice_data["email"] = line.strip()
            if email_line_index > 0:
                invoice_data["name"] = lines[email_line_index - 1].strip()
            break
    match = re.search(r'TOTAL\s+([\d,]+\.\d{2})', table_text)
    if match:
        invoice_data["total"] = match.group(1).replace(",", "")
    return invoice_data

def process_text_files():
    """Applique l'extraction sur les fichiers bloc_facturation.txt et bloc_table.txt et modifie directement les fichiers."""
    
    print(f"🔍 Vérification du dossier : {DATA_DIR}")

    # Vérifier si le dossier existe
    if not os.path.exists(DATA_DIR):
        print(f"⚠️ ERREUR : Le dossier {DATA_DIR} n'existe pas !")
        return

    text_files = glob.glob(os.path.join(DATA_DIR, "*_bloc_facturation.txt"))

    if not text_files:
        print("⚠️ Aucun fichier _bloc_facturation.txt trouvé. Arrêt du script.")
        return

    print(f"📂 {len(text_files)} fichiers trouvés. Traitement en cours...")

    for facturation_file in text_files:
        print(f"\n📄 Traitement du fichier : {facturation_file}")

        table_file = facturation_file.replace("_bloc_facturation.txt", "_bloc_table.txt")
        
        if not os.path.exists(table_file):
            print(f"⚠️ Fichier manquant : {table_file}, la facture sera traitée sans total.")
            table_text = ""
        else:
            with open(table_file, "r", encoding="utf-8") as f:
                table_text = f.read()

        with open(facturation_file, "r", encoding="utf-8") as f:
            facturation_text = f.read()

        print(f"🔍 Extraction des détails pour {facturation_file}...")

        invoice_details = extract_invoice_details(facturation_text, table_text)

        if not any(invoice_details.values()):
            print(f"⚠️ Aucune information extraite pour {facturation_file}. Vérifiez le contenu OCR.")
            continue

        print("✅ Détails extraits :", invoice_details)

        # 🔹 Modifier directement les fichiers existants avec les informations extraites
        with open(facturation_file, "a", encoding="utf-8") as f:
            f.write("\n---\n")
            for key, value in invoice_details.items():
                f.write(f"{key}: {value}\n")

        print(f"✅ Détails ajoutés dans {facturation_file}")

# 🔹 Exécution du script
if __name__ == "__main__":
    process_text_files()