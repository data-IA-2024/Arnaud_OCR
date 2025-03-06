import os
import requests
from dotenv import load_dotenv
import urllib.parse

# Charger les variables d'environnement
load_dotenv()


# 📂 Dossier où enregistrer les images PNG
OUTPUT_DIR = "data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Récupérer les valeurs depuis le .env
CONTAINER_URL = os.getenv("CONTAINER_URL")
CONTAINER_SAS = os.getenv("CONTAINER_SAS")

def clean_sas_token(sas_token):
    """Nettoie le SAS Token en supprimant les paramètres `restype=container&comp=list`."""
    if not sas_token.startswith("?"):
        sas_token = f"?{sas_token}"
    
    parsed_sas = urllib.parse.urlparse(sas_token)
    cleaned_query = "&".join([
        param for param in urllib.parse.parse_qs(parsed_sas.query, keep_blank_values=True)
        if not param.startswith("restype") and not param.startswith("comp")
    ])
    
    return f"?{cleaned_query}" if cleaned_query else ""

def download_png_files(png_files):
    """Télécharge les fichiers PNG et les enregistre dans le dossier data/."""

    print(f"📂 Fichiers reçus pour téléchargement : {png_files}")  # Debug

    # 🔍 Vérification si des fichiers sont trouvés
    if not png_files:
        print("⚠️ Aucun fichier trouvé à télécharger. Vérifie `getlist.py` et `main.py`.")
        return

    # 🔹 Nettoyage du SAS Token
    sas_clean = clean_sas_token(CONTAINER_SAS)

    for file_name in png_files:
        # ✅ Construction correcte de l'URL
        file_url = f"{CONTAINER_URL}/{file_name}{CONTAINER_SAS}"
        # 🔍 DEBUG : Vérifier l'URL générée
        print(f"🔗 Vérifie cette URL dans ton navigateur : {file_url}")

        try:
            response = requests.get(file_url, stream=True)

            if response.status_code == 200:
                # 📥 Enregistrer l'image dans le dossier 'data'
                file_path = os.path.join(OUTPUT_DIR, file_name)
                with open(file_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        file.write(chunk)

                print(f"✅ Image téléchargée : {file_path}")
            else:
                print(f"❌ Erreur {response.status_code} pour {file_url}")

        except Exception as e:
            print(f"❌ Échec du téléchargement {file_name}: {e}")

# 🔹 TESTER SEULEMENT `extract_png.py` (hors `main.py`)
if __name__ == "__main__":
    test_files = ["FAC_2018_0001-654.png", "FAC_2018_0002-114.png"]  # Test avec des noms d'images
    download_png_files(test_files)
