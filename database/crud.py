from model_table import Invoice, Customer
from db_connector import SQLClient
import os

def add_customer(db,email, name, adress, birth):
    # Ajoute un Customer
    cust = Customer(name=name, email=email, adress=adress, birth=birth)
    db.add(cust)
    db.commit()  

def add_invoice(db,invoice_number, total, customer_email):
    # Ajoute un Invoice
    invoice = Invoice(invoice_number=invoice_number, total=total, customer_email=customer_email)
    db.add(invoice)
    db.commit() 

def get_customers(db):
    # Récupère tous les clients
    return db.query(Customer).all()

if __name__ == "__main__":
    #test_connection()
    client = SQLClient()
    db = next(client.get_session())
    
    add_customer(db, 'a7a@oo.fr', 'Client Test', 'Paris', '1990-01-01')
