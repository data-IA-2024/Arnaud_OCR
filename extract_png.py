import os
import requests
from dotenv import load_dotenv  # Import pour charger les variables d'environnement

# Charger les variables d'environnement
load_dotenv()

# 📂 Dossier où enregistrer les images PNG
OUTPUT_DIR = "data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Récupérer les valeurs depuis le .env
CONTAINER_URL = os.getenv("CONTAINER_URL")  # Charger la variable CONTAINER_URL depuis .env
CONTAINER_SAS = os.getenv("CONTAINER_SAS")  # Charger la variable CONTAINER_SAS depuis .env

def download_png_files(png_files):
    """Télécharge les fichiers PNG et les enregistre dans le dossier data/."""
    if not png_files:
        print("❌ Aucune image PNG trouvée.")
        return

    for idx, file_name in enumerate(png_files):
        # Créer l'URL complète avec le nom du fichier PNG
        file_url = f"{CONTAINER_URL}/{file_name}"

        try:
            response = requests.get(file_url)
            if response.status_code == 200:
                # Enregistrer l'image dans le dossier 'data'
                file_path = os.path.join(OUTPUT_DIR, file_name)
                with open(file_path, "wb") as file:
                    file.write(response.content)
                
                print(f"✅ Image téléchargée : {file_path}")
            else:
                print(f"❌ Erreur ({response.status_code}) pour {file_url}")

        except Exception as e:
            print(f"❌ Échec du téléchargement {file_name}: {e}")

if __name__ == "__main__":
    png_files = ['FAC_2018_0001-654.png', 'FAC_2018_0002-114.png']  # Pour tester, tu peux appeler la fonction avec les noms de fichiers
    download_png_files(png_files)
