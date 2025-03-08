import os
import re
from azure.storage.blob import ContainerClient
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Liste des dossiers à scanner (manuellement)
YEARS = [str(year) for year in range(2018, 2025)]
BASE_URL = "https://projetocrstorageacc.blob.core.windows.net/"
SAS_TOKEN = "?" + os.getenv("CONTAINER_SAS")

def list_png_files():
    png_files = []

    for year in YEARS:
        folder_url = f"{BASE_URL}invoices-{year}{SAS_TOKEN}"
        try:
            container_client = ContainerClient.from_container_url(folder_url)
            for blob in container_client.list_blobs():
                if blob.name.endswith('.png'):
                    png_files.append(blob.name)
        except Exception as e:
            print(f"⚠️ Impossible de lire {folder_url}: {e}")

    return png_files

if __name__ == "__main__":
    png_files = list_png_files()
    print("📂 Fichiers PNG trouvés :", png_files)
