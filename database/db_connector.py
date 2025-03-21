#Ce fichier gère la connexion à une base de données PostgreSQL en utilisant SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from model_table import Base
from sqlalchemy import URL
from contextlib import contextmanager
import sqlalchemy

load_dotenv()

def build_url():
    return URL.create(
        drivername = "postgresql",
        username   = os.environ.get('DB_USER'),
        password   = os.environ.get('DB_PASS'),
        host       = os.environ.get('DB_HOST'),
        port       = os.environ.get('DB_PORT'),
        database   = os.environ.get('DB_NAME') 
    )

def build_engine(echo=False):
    return create_engine(
        url = build_url(),
        echo=echo
    )

# Charger les variables d'environnement

class SQLClient:
    def __init__(self):
        self.engine = build_engine(echo=True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine, checkfirst=True)

    @contextmanager
    def get_session(self):
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()
    
    def drop_all(self):
        """ Supprime toute les tables """
        Base.metadata.drop_all(bind=self.engine)
    
    def insert(self, row):
        with self.get_session() as session:
            try :
                session.merge(row)
                session.commit()
            except sqlalchemy.exc.IntegrityError as e : 
                print(f"❌ {row} already exists.")

    def test_connection(self):
        try:
            with self.get_session() as session:
                result = session.execute(text("SELECT version();"))
                print("✅ Connexion réussie à PostgreSQL !")
                for row in result:
                    print(f"Version PostgreSQL : {row[0]}")
        except Exception as e:
            print(f"❌ Erreur de connexion : {e}")


# Exécuter le test seulement si ce fichier est lancé directement
if __name__ == "__main__":
    client = SQLClient()
    client.test_connection()