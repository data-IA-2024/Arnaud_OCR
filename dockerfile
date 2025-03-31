# Étape 1 : Utiliser une image Python officielle
FROM python:3.12-slim

# Étape 2 : Définir variables d'environnement en fonction du projet, laisser leur valeur VIDE
ENV DATABASE_URL=
ENV OCR_API=
ENV VISION_KEY=
ENV VISION_ENDPOINT=
ENV JWT_SECRET_KEY=
ENV JWT_ALGORITHM=

# Étape 3 : Installer Tesseract OCR et ses dépendances système
RUN apt-get update && apt-get install -y tesseract-ocr imagemagick zbar-tools && apt-get clean && rm -rf /var/lib/apt/lists/*

# Étape 4 : Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Étape 5 : Copier les fichiers nécessaires dans le répertoire de travail /app du conteneur
COPY . .

# Étape 6 : Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Étape 7 : Exposer le port utilisé par FastAPI
EXPOSE 8000

# Étape 8 : Commande pour exécuter l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]