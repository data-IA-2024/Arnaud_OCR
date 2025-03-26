import os
import glob
import re
import cv2

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
    # Extraction du numéro de facture
    match = re.search(r'INVOICE (\S+)', facturation_text)
    if match:
        invoice_data["no"] = match.group(1)
    # Extraction de la date (format YYYY-MM-DD)
    match = re.search(r'\d{4}-\d{2}-\d{2}', facturation_text)
    if match:
        invoice_data["date"] = match.group()
    # Extraction du nom du client
    lines = facturation_text.split("\n")
    for line in lines:
        if "@" in line:
            email_line_index = lines.index(line)
            invoice_data["email"] = line.strip()
            if email_line_index > 0:
                invoice_data["name"] = lines[email_line_index - 1].strip()
            break
    # Extraction du total de la facture
    match = re.search(r'TOTAL\s+([\d,]+\.\d{2})', table_text)
    if match:
        invoice_data["total"] = match.group(1).replace(",", "")
    return invoice_data

def process_extracted_texts():
    """Applique le traitement aux fichiers texte extraits de l'OCR."""
    if not os.path.exists(DATA_DIR):
        print(f"⚠️ Dossier {DATA_DIR} non trouvé.")
        return

    facturation_files = glob.glob(os.path.join(DATA_DIR, "*_bloc_facturation.txt"))

    if not facturation_files:
        print(f"⚠️ Aucune extraction de bloc facturation trouvée dans {DATA_DIR}.")
        return

    for facturation_file in facturation_files:
        table_file = facturation_file.replace("_bloc_facturation.txt", "_bloc_table.txt")

        if not os.path.exists(table_file):
            print(f"⚠️ Fichier manquant : {table_file}, la facture sera traitée sans total.")
            table_text = ""
        else:
            with open(table_file, "r", encoding="utf-8") as f:
                table_text = f.read()

        with open(facturation_file, "r", encoding="utf-8") as f:
            facturation_text = f.read()

        invoice_details = extract_invoice_details(facturation_text, table_text)

        # 🔹 Enregistrement des détails extraits
        details_output_path = facturation_file.replace("_bloc_facturation.txt", "_details.txt")
        with open(details_output_path, "w", encoding="utf-8") as f:
            for key, value in invoice_details.items():
                f.write(f"{key}: {value}\n")

        print(f"✅ Détails extraits -> {details_output_path}")

def load_image(image_path):
    return cv2.imread(image_path)

# 🔹 Exécution du script pour traiter les fichiers `.txt`
if __name__ == "__main__":
    process_extracted_texts()