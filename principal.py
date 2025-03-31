import sys
import os
import database.crud
from database.db_connector import engine, Base, SessionLocal
import database.model_table
from backend.script import utils
from backend.script.utils import extract_invoice_details

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))


if __name__ == "__main__":
    print("Création des tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables créées avec succès !")

    session = SessionLocal()

    # Ajout d'un client (à activer si besoin)
    # crud.add_customer(session, 'test@example.com', 'Client Test')

    customers = database.crud.get_customers(session)
    print(f"📌 Clients en base : {customers}")

    session.close()  # 🔥 Remplace commit() par close()
    facturation_text = """INVOICE FAC/2018/0001
2018-10-13
Carol Potter
ashley38@example.org
Address 405 Adrian Crest Suite 095
Jamesstad, MN 36094"""

    table_text = """Edge so crime share 4x 12.18 Euro
Thank do article especially 1 x 67.86 Euro
Include dinner main friend 3 x 287.99 Euro
Capital hear moming people 3 x 55.43 Euro
TOTAL 1146.84 Euro"""

    invoice_data = extract_invoice_details(facturation_text, table_text)
    print(invoice_data)
    database.crud.add_customer(session, invoice_data["email"], invoice_data["name"],"",None)
    database.crud.add_invoice(session, invoice_data["no"], invoice_data["total"], invoice_data["email"])

