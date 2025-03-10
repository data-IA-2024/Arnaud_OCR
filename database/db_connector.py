import requests, json, os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Charger les variables d'environnement du fichier .env
load_dotenv()

POSTGRES_URI = os.getenv("POSTGRES_URI")

engine = create_engine(POSTGRES_URI)
conn = engine.connect()

def add_invoice(obj):
    conn.execute(text(f"""
INSERT INTO goudot.invoices ("no","CreationTime","ContentLength","ContentMD5") 
VALUES (:no,:CreationTime,:ContentLength,:ContentMD5)
ON CONFLICT DO NOTHING;
"""), obj)
    conn.commit()