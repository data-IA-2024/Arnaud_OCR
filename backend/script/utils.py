import os
import cv2
import re

def open_image(image_path):
    # Charger l'image correctement
    if os.path.isfile(image_path):
        return cv2.imread(image_path)
    raise FileNotFoundError(f"❌ L'image {image_path} n'existe pas.")
    

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
        if "@" in line:  # La ligne contenant l'email
            email_line_index = lines.index(line)
            invoice_data["email"] = line.strip()

            # Supposons que le nom est juste au-dessus de l'email
            if email_line_index > 0:
                invoice_data["name"] = lines[email_line_index - 1].strip()
            break

    # Extraction du total de la facture
    match = re.search(r'TOTAL\s+([\d,]+\.\d{2})', table_text)
    if match:
        invoice_data["total"] = match.group(1).replace(",", "")  # Remplace les virgules par des points si besoin

    return invoice_data
