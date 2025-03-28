# Ce fichier permet d'ajouter et récupérer des données clients et factures en base.

from model_table import Invoice, Customer
from db_connector import SQLClient
import os
import glob
import json
import logging
import csv
import re
from datetime import datetime
from mock import mock

# ==========================
# 🔹 CONSTANTES
# ==========================
DATA_PATH = r"C:\Users\mpadmin\Documents\projet-OCR\data"
JSON_PATH = r"C:\Users\mpadmin\Documents\projet-OCR\backend\script\extracted_qr_codes.json"

# ==========================
# 🔹 FONCTIONS D'INSERTION
# ==========================

def commit(client):
    """Commit les transactions en base"""
    with client.get_session() as session:
        session.commit()

def add_customer(client, email, name, gender, adress, birth):
    """Ajoute un Customer à la base de données"""

    #print(f"📝 Préparation de l'insertion en base : {email} | Birth: {birth} | Gender: {gender}")


    new_customer = Customer(name=name, email=email, gender=gender, adress=adress, birth=birth)
    #print(f"🔄 Commit en cours pour {email}...") 
    client.insert(new_customer)

    #print(f"✅ Insertion réussie pour {email}")

    return email


def add_invoice(client, invoice_number, total, customer_email, creation_date):
    """Ajoute une facture (Invoice) dans la base de données"""
    invoice = Invoice(invoice_number=invoice_number, total=total, customer_email=customer_email, creation_date=creation_date)
    client.insert(invoice)
    return invoice

# ==========================
# 🔹 CHARGEMENT DES INFORMATIONS CLIENTS (DATE DE NAISSANCE & SEXE)
# ==========================

def load_customer_info():
    """Charge la date de naissance et le sexe des clients depuis extracted_qr_codes.json."""
    customer_info = {}
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            json_data = json.load(f)

        print("\n📂 Chargement des clients depuis extracted_qr_codes.json...")

        for entry in json_data:
            invoice_number = entry.get("invoice_number")
            birth_date = entry.get("customer_birthdate")
            gender = entry.get("customer_sex")

            # Vérifier que l'email est bien extrait de la facture
            customer_email = None
            for fact_file in glob.glob(os.path.join(DATA_PATH, "**", "*_bloc_facturation.txt"), recursive=True):
                with open(fact_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    if invoice_number in lines[0]:  # Vérifie si la facture correspond
                        customer_email = lines[3].strip()  # Extrait l'email
                        break

            if customer_email:
                birth = None
                if birth_date:
                    try:
                        birth = datetime.strptime(birth_date, "%Y-%m-%d").date()
                    except ValueError:
                        print(f"⚠️ Erreur format date pour {invoice_number}: {birth_date}")

                print(f"✅ Client trouvé : {customer_email} (facture {invoice_number}) | Birth : {birth} | Gender : {gender}")
                customer_info[customer_email] = {"birth": birth, "gender": gender}  # 🔄 Stocker avec `customer_email`

    except Exception as e:
        print(f"❌ Erreur lors du chargement du JSON: {e}")

    return customer_info


# ==========================
# 🔹 TRAITEMENT DES FICHIERS FACTURATION & TABLE
# ==========================

def get_all_invoice_files():
    """Recherche tous les fichiers *_bloc_facturation.txt et *_bloc_table.txt dans les sous-dossiers."""
    facturation_files = sorted(glob.glob(os.path.join(DATA_PATH, "**", "*_bloc_facturation.txt"), recursive=True))
    table_files       = sorted(glob.glob(os.path.join(DATA_PATH, "**", "*_bloc_table.txt"), recursive=True))

    # For security reasons
    #assert len(facturation_files) == len(table_files)

    # Not Useful !!!!

    # print("\n📂 Factures détectées :")
    #for file in facturation_files:
    #    print(f"📄 {file}")

    return facturation_files, table_files

def read_facturation(file):
    """Lit un fichier _bloc_facturation.txt et extrait les informations du client et de la facture."""
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    invoice_number = lines[0].strip().split(' ')[-1]  
    customer_name = lines[2].strip()
    customer_email = lines[3].strip()
    customer_adress = " ".join([line.strip() for line in lines[4:]])

    return {
        "invoice_number": invoice_number,
        "customer_name": customer_name,
        "customer_email": customer_email,
        "customer_adress": customer_adress
    }

def read_table(file):
    """Lit un fichier _bloc_table.txt pour récupérer le total de la facture."""
    total = None
    try:
        with open(file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            match = re.search(r"\bTOTAL\b[:\s]*([\d,.]+)", line, flags=re.IGNORECASE)
            if match:
                total_str = match.group(1).replace(",", ".")
                # Why is this needed ???. In principle, it is not needed
                total_str = re.sub(r"[^\d.]", "", total_str)
                try:
                    total = float(total_str)
                    break
                except ValueError:
                    continue

        if total is None:
            print(f"\n⚠️ Total non trouvé dans {file}")

    except Exception as e:
        print(f"\n❌ Erreur lors de la lecture du fichier {file}: {e}")

    return total

# ==========================
# 🔹 INSERTION DES DONNÉES DANS LA BASE
# ==========================

def insert_facturation(client, customer_info, facturation):
    table = facturation.replace("_bloc_facturation.txt", "_bloc_table.txt")
    if not os.path.isfile(table) :
        print(f"Le fichier {table} n'existe pas.")
        return
    
    fact_data = read_facturation(facturation)
    invoice_number = fact_data["invoice_number"]
    total = read_table(table)

    if total is None :
        print(f"Aucun total trouvé dans le fichier {table}.")
        return 

    creation_date = datetime.now().date()

    info = customer_info.get(fact_data["customer_email"], {})  # ✅ Correction : récupérer via l'email

    add_customer(
        client, 
        email=fact_data["customer_email"], 
        name=fact_data["customer_name"], 
        gender=info.get("gender"),
        adress=fact_data["customer_adress"], 
        birth=info.get("birth")
    )

    add_invoice(
        client,
        invoice_number=invoice_number,
        total=total,
        customer_email=fact_data["customer_email"],
        creation_date=creation_date
    )

def insert_facturation_all():
    """Insère les clients et les factures en base de données à partir des fichiers texte."""
    client = SQLClient()

    #customer_info = load_customer_info()
    facturation_files, table_files = get_all_invoice_files()

    num_files = len(facturation_files)

    print("\n🔍 Vérification des fichiers disponibles...")

    # Should not be necessary waste of time
    #
    #for file in facturation_files:
    #    table_file = file.replace("_bloc_facturation.txt", "_bloc_table.txt")
    #    if table_file in table_files:
    #        print(f"✅ Trouvé : {table_file}")
    #    else:
    #        print(f"❌ Manquant : {table_file}")

    for j, fact_file in enumerate(facturation_files):
        print(f"\r{(j+1)*100/num_files:.2f} % | {fact_file}\033[0K", end='', flush=True)
        #insert_facturation(client, customer_info, fact_file)
        
    print("\n✅ Insertion terminée !")

# ==========================
# 🔹 EXECUTION DU SCRIPT
# ==========================



####################################################################################
###                             Rules to follows                                 ###
####################################################################################

# 1. read_facturation/read_table OCR text
# 2. extract_data 
# 3. insert data into table

if __name__ == "__main__":
    # Disable sqlalchemy logger
    logging.getLogger('sqlalchemy.engine.Engine').disabled = True

    #client = SQLClient()

    print("\n📥 Importation des clients et factures...")
    insert_facturation_all()

    print("\n📜 Affichage des données :")
    #for customer in get_customers(client):
        #print(customer)

    #for invoice in get_invoices(client):
        #print(invoice)
