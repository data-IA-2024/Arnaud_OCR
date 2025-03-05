import os
import requests
from dotenv import load_dotenv
import xml.etree.ElementTree as ET

# Charger les variables d'environnement
load_dotenv()

# Récupérer les valeurs depuis le .env
CONTAINER_URL = os.getenv("CONTAINER_URL")
CONTAINER_SAS = os.getenv("CONTAINER_SAS")

# Construire l'URL complète
url = f"{CONTAINER_URL}{CONTAINER_SAS}"

# Faire la requête GET
response = requests.get(url)

 # Utiliser le XML retourné, pas l'URL !
xml_data = response.text
root = ET.fromstring(xml_data)

# Trouver tous les fichiers .png
png_files = [blob.find("Name").text for blob in root.findall(".//Blob") if ".png" in blob.find("Name").text]
print(png_files)