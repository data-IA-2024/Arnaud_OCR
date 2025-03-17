from sqlalchemy import MetaData, Column, Integer, String, DateTime, Date, ForeignKey, Numeric  
# 📌 `MetaData` : Stocke la structure de la base (tables, colonnes…)
# 📌 `ForeignKey` : Définit une relation entre deux tables (clé étrangère)  
# 📌 `Numeric` : Type pour stocker des nombres avec des décimales (ex: prix)  

from sqlalchemy.orm import declarative_base, relationship  
# 📌 `declarative_base` : Classe Python qui sera transformée en SQL
# 📌 `relationship` : Permet de créer des relations entre les tables dans SQLAlchemy ORM  

from sqlalchemy import create_engine
import os 
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base(metadata=MetaData(schema="arnaud"))

class Customer(Base):
    __tablename__ = 'customers'
    name = Column(String, nullable=False) 
    email = Column(String, primary_key=True, nullable=False)
    adress = Column(String, nullable=True)
    birth = Column(Date, nullable=True)

    invoices = relationship("Invoice", back_populates="customer")

    def __repr__(self):
        return f"CUST {self.email}"

class Invoice(Base):
    __tablename__ = 'invoices'
    invoice_number = Column(String, primary_key=True, nullable=False)  # Ajout de nullable=False
    total = Column(Numeric(8,2))
    customer_email = Column(String, ForeignKey('customers.email'), nullable=True)
    
    customer = relationship("Customer", back_populates="invoices")

    def __repr__(self):
        return f"INVOICE n°{self.no} (client: {self.cust_email})"

    
if __name__ == "__main__":
    #test_connection()
    engine = create_engine(os.getenv('POSTGRES_URI'))
    
    Base.metadata.create_all(bind=engine, checkfirst=True)  # Crée les tables si elles n'existent pas déjà
