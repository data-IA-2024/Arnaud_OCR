import os
from azure.storage.blob import BlobClient
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Définir l'URL du conteneur
BASE_URL = "https://projetocrstorageacc.blob.core.windows.net/"
SAS_TOKEN = "?" + os.getenv("CONTAINER_SAS")

def download_png(file_name, year):
    """Télécharge un fichier PNG et l'enregistre dans le dossier correspondant à l'année."""
    
    # Construire l'URL complète du blob
    blob_url = f"{BASE_URL}invoices-{year}/{file_name}{SAS_TOKEN}"
    
    # Définir le dossier où enregistrer le fichier
    save_dir = f"data/{year}/"
    os.makedirs(save_dir, exist_ok=True)  # Crée le dossier s'il n'existe pas

    save_path = os.path.join(save_dir, file_name)
    
    try:
        # Créer un client Blob
        blob_client = BlobClient.from_blob_url(blob_url)
        
        # Télécharger le fichier
        with open(save_path, "wb") as file:
            file.write(blob_client.download_blob().readall())
        
        print(f"✅ {file_name} téléchargé dans {save_path}")
    except Exception as e:
        print(f"❌ Erreur lors du téléchargement de {file_name} : {e}")

if __name__ == "__main__":
    # Exemple de test avec un fichier
    file_name = "FAC_2019_0001-123.png"  # Exemple, remplace par un vrai fichier de getlist.py
    download_png(file_name, "2019")
