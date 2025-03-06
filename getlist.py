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

    # 🔍 Assurer que le SAS Token commence bien par `?`
    sas = CONTAINER_SAS if CONTAINER_SAS.startswith("?") else f"?{CONTAINER_SAS}"
    url = f"{CONTAINER_URL}{sas}"
    

    print(f"🔗 URL requête Azure : {url}")  # Debug: Vérifie si l'URL est correcte
    response = requests.get(url)

    if response.status_code != 200:
        print(f"❌ Erreur {response.status_code} lors de la récupération du XML")
        print(f"📜 Contenu réponse : {response.text[:500]}")  # Voir ce qu'Azure retourne
        return []

    # 🔍 Analyser le XML retourné
    xml_data = response.text
    root = ET.fromstring(xml_data)

    # 🛠 Debug: Afficher tout le XML
    print(f"📜 XML reçu : {xml_data[:500]}...")  # Voir si les fichiers sont bien listés

    # 📂 Trouver tous les fichiers .png et récupérer uniquement les noms des fichiers
    png_files = [blob.find("Name").text for blob in root.findall(".//Blob") if ".png" in blob.find("Name").text]

    print(f"📸 Fichiers PNG trouvés : {png_files}")  # Vérifier la liste trouvée
    return png_files

if __name__ == "__main__":
    files = get_png_files()
