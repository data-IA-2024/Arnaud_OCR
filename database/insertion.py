import json
from glob import glob
import os.path
from db_connector import SQLClient
from crud import add_customer, add_invoice
import logging


def edit_filename(filename,prefix):
    return filename.replace(".png",f"{prefix}.json")


def read_json(file):
    with open(file,"r") as f:
        return json.load(f)

def insert_db(client, file):
    fact_json=edit_filename(file,"_fact")
    table_json=edit_filename(file,"_table")
    qr_json=edit_filename(file,"_qr")

    
    if not os.path.isfile(fact_json) or not os.path.isfile(table_json) or not os.path.isfile(qr_json):
        return 
    text_fact=read_json(fact_json)
    text_table=read_json(table_json)
    text_qr=read_json(qr_json)
    

    add_customer(client, email=text_fact["email"], name=text_fact["name"], gender=text_qr["customer_sex"], adress=text_fact["adress"], birth=text_qr["customer_birthdate"])
    add_invoice(client, invoice_number=text_qr["invoice_number"], total=text_table["total"], customer_email=text_fact["email"], creation_date=text_fact["date"])


def main():
    files = sorted(glob("../data/**/*.png"))
    client = SQLClient()
    nb_files = len(files)
    for i, file in enumerate(files):
        print(f"\r{(i+1)*100/nb_files:06.2f}% {file}\033[0K", end="", flush=True)
        try:
            insert_db(client,file)
        except Exception as e:
            print(e)
    
def drop_all():
     client = SQLClient()
     client.drop_all()




if __name__ == "__main__":
    logging.getLogger('sqlalchemy.engine.Engine').disabled = True
    main()
    #drop_all()