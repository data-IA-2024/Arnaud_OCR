import re

def remove_space(text):
    return text.replace(" ", "")

def extract_invoice_number(line):
    m = re.search(r'\w+\s+(\S+)', line)
    if m:
        return m.group(1)
    return None

def extract_invoice_date(line):
    m = re.search(r'(\d{4}-\d{2}-\d{2})', line)
    if m:
        return m.group(1)
    return None

def extract_invoice_name(line):
    m = re.search(r'\w+\s+\w+\s+(.+)$', line)
    if m:
        return m.group(1)
    return None

def extract_invoice_email(line):
    m = re.search(r'\w+\s+(.+)$', line)
    if m:
        return remove_space(m.group(1))
    return None

def extract_invoice_adress(lines):
    m = re.search(r'\w+\s+(.+)$', lines[0])
    line1 = ""
    if m:
        line1 =  m.group(1)
    return ', '.join([line1, lines[1]])

def extract_invoice_details(text):
    """ Extrait les informations essentielles d'une facture OCR """
    return {
        "no": extract_invoice_number(text[0]),
        "date": extract_invoice_date(text[1]),
        "name": extract_invoice_name(text[2]),
        "email": extract_invoice_email(text[3]),
        "adress": extract_invoice_adress(text[4:]),
    }

def extract_product_info(line):
    m = re.search(r"([\w\s]+)[,.][^\d]*(\d+)[^\d]*([\d,.]+)",line)
    if m:
        p_name=m.group(1).strip()
        p_quant=int(m.group(2))
        p_price=float(m.group(3).replace(",","."))
        return p_name, p_quant,p_price

def extract_table_total(line):
    m = re.search(r'\w+\s+([\d,.]+)\s+\w+$', line)
    if m:
        return float (remove_space(m.group(1).replace("," ,".")))

    
def extract_table_details(lines):
    table ={
        "item":{
            "product_name":[],
            "quantity":[],
            "price":[]
        }
    }
    for line in lines[:-1]:
        p_name,p_quant,p_price=extract_product_info(line)
        table["item"]["product_name"].append(p_name)
        table["item"]["quantity"].append(p_quant)
        table["item"]["price"].append(p_price)
    
    table["total"]=extract_table_total(lines[-1])
    return table
    
def extract_qrcode(lines):
    invoice_number = lines[0][8:]
    
    # Extraire uniquement la date sans l'heure
    full_date = lines[1][5:]
    date_only = full_date.split(" ")[0]  # Récupère uniquement la partie YYYY-MM-DD

    customer_sex, birthdate = lines[2].split(", ")
    customer_sex = customer_sex[5:]
    birthdate = birthdate[6:]

    return {
        "invoice_number": invoice_number,
        "date": date_only,  # Stocke seulement YYYY-MM-DD
        "customer_sex": customer_sex,
        "customer_birthdate": birthdate
    }
