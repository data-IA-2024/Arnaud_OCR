import os
import requests
from dotenv import load_dotenv
import xml.etree.ElementTree as ET

# Charger les variables d'environnement
load_dotenv()

# Récupérer les valeurs depuis le .env
CONTAINER_URL = os.getenv("CONTAINER_URL")
CONTAINER_SAS = os.getenv("CONTAINER_SAS")

def get_png_files():
    """ Récupère la liste des fichiers PNG depuis le XML du serveur """
    url = f"{CONTAINER_URL}{CONTAINER_SAS}"
    response = requests.get(url)

    if response.status_code != 200:
        print("❌ Erreur lors de la récupération du XML")
        return []

    # Analyser le XML retourné
    xml_data = response.text
    root = ET.fromstring(xml_data)

    # Trouver tous les fichiers .png et récupérer uniquement les noms des fichiers
    png_files = [blob.find("Name").text for blob in root.findall(".//Blob") if ".png" in blob.find("Name").text]
    
    return png_files

if __name__ == "__main__":
    files = get_png_files()
    print(files)  # Vérifier la liste des fichiers PNG (uniquement les noms)
