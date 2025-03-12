import cv2
from pyzbar.pyzbar import decode
import os
import glob
import json

def read_qrcode(image):
    """Décode le QR code d'une image et extrait les informations."""
    
    # Détecter les QR codes dans l'image
    qr_codes = decode(image)

    if not qr_codes:
        raise ValueError("❌ Aucun QR code détecté.")

    try:
        text = qr_codes[0].data.decode("utf-8")
        lines = text.split("\n")

        invoice_number = lines[0][8:]
        
        # Extraire uniquement la date sans l'heure
        full_date = lines[1][5:]
        date_only = full_date.split(" ")[0]  # Récupère uniquement la partie YYYY-MM-DD

        customer_sex, birthdate = lines[2].split(", ")
        customer_sex = customer_sex[5:]
        birthdate = birthdate[6:]

        return {
            "invoice_number": invoice_number,
            "date": date_only,  # Stocke seulement YYYY-MM-DD
            "customer_sex": customer_sex,
            "customer_birthdate": birthdate
        }

    except (IndexError, ValueError) as e:
        raise ValueError(f"❌ Erreur lors de l'extraction des données du QR code : {e}")


def open_image(image_path):
    """Charge une image en vérifiant qu'elle existe."""
    if os.path.isfile(image_path):
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"L'image {image_path} ne peut pas être chargée.")
        return image
    raise FileNotFoundError(f"L'image {image_path} n'existe pas.")

if __name__ == "__main__":
    data_content = glob.glob("./../../data/*")  # Liste des dossiers par année
    extracted_data = []  # Stocke toutes les données extraites

    for year in data_content:
        image_paths = glob.glob(year + "/*.png")  # Liste des images
        for image_path in image_paths:
            print(f"📂 Traitement de {image_path}...", end=" ")

            try:
                image = open_image(image_path)  # Ouvre l'image
                data = read_qrcode(image)  # Extrait les infos
                extracted_data.append(data)  # Ajoute à la liste des résultats
                print("✅ Succès :", data)

            except Exception as e:
                print(f"❌ Erreur : {e}")

    # Sauvegarde les résultats dans un fichier JSON
    output_file = "extracted_qr_codes.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(extracted_data, f, indent=4, ensure_ascii=False)

    print(f"\n🔍 Extraction terminée. {len(extracted_data)} QR codes traités et enregistrés dans '{output_file}'.")
