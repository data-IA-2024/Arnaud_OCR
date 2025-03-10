from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from database.db_connector import engine

# Définition de la base ORM
Base = declarative_base()

# Définition du modèle User
class User(Base):
    __tablename__ = "customers"  # Nom de la table

    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

# Création des tables en base
Base.metadata.create_all(bind=engine)
