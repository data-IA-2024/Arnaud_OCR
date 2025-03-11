import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

# Charger les variables d’environnement
load_dotenv()

# Vérifier que les variables d'environnement sont bien définies
try:
    endpoint = os.environ["VISION_ENDPOINT"]
    key = os.environ["VISION_KEY"]
except KeyError:
    print("❌ Missing environment variable 'VISION_ENDPOINT' or 'VISION_KEY'")
    exit()

# Créer un client Azure Computer Vision
client = ImageAnalysisClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Construire le bon chemin du fichier
file_path = os.path.join(base_dir, "data", "2018", "FAC_2018_0001-654.png")

# Vérifier si le fichier existe
if not os.path.exists(file_path):
    print(f"❌ Fichier introuvable : {file_path}")
    exit()

# Lire l’image en mode binaire
with open(file_path, "rb") as f:
    image_data = f.read()

print("✅ Fichier trouvé et chargé avec succès !")
print(type(image_data))
print(len(image_data))  # Nombre d'octets dans l'image
