from sqlalchemy import create_engine, MetaData, text  
# 🔹 `create_engine` : Permet de se connecter à une base de données 
# 🔹 `MetaData` : Stocke la structure de la base (tables, colonnes…)
# 🔹 `text` : Permet d'exécuter des requêtes SQL brutes sous forme de texte

from sqlalchemy.orm import sessionmaker  
# 🔹 `sessionmaker` : Crée une session pour interagir avec la base de données (ajout, requêtes, modifications…)

import dotenv
import os
from model_table import Base


# Charger les variables d'environnement
dotenv.load_dotenv()
class SQLClient:
    def __init__(self, uri=os.getenv('POSTGRES_URI')):
        self.engine = create_engine(uri, echo=True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = Base
        self.Base.metadata.create_all(bind=self.engine, checkfirst=True)

    def get_session(self):
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()

    def test_connection(self):
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT version();"))
                print("✅ Connexion réussie à PostgreSQL !")
                for row in result:
                    print(f"Version PostgreSQL : {row[0]}")
        except Exception as e:
            print(f"❌ Erreur de connexion : {e}")


# Exécuter le test seulement si ce fichier est lancé directement"""
if __name__ == "__main__":
    #test_connection()
    client = SQLClient()
