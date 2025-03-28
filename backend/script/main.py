from glob import glob
from backend.script.utils import load_image
from backend.script.segmentation import rgb_to_gray, extract_blocks
from pprint import pprint
from backend.script.qr_code import read_qrcode
from backend.script.ocr import extract_text
from backend.script.parser import extract_invoice_details, extract_table_details,extract_qrcode
import json
import logging


def edit_filename(filename,prefix):
    return filename.replace(".png",f"{prefix}.json")

def save_fact(file,text_fact):
    with open(edit_filename(file,"_fact"),"w")as f:
        json.dump(text_fact,f)

def save_table(file,text_table):
    with open(edit_filename(file,"_table"),"w")as f:
        json.dump(text_table,f)

def save_qr(file,text_qr):
    with open(edit_filename(file,"_qr"),"w")as f:
        json.dump(text_qr,f)

def process_image(file:str):
    logging.info("debut_process_image")
    image = load_image(file)
    #gray = rgb_to_gray(image)
    blocks = extract_blocks(image)
    info_qr = read_qrcode(blocks['bloc_qr_code'])
    info_fact = extract_text(blocks["bloc_facturation"])
    info_table = extract_text(blocks["bloc_table"])
    text_fact = extract_invoice_details(info_fact)
    text_table = extract_table_details(info_table)
    text_qrcode = extract_qrcode(info_qr)

    save_fact(file, text_fact)
    save_table(file,text_table)
    save_qr(file,text_qrcode)
    logging.info("fin_process_image")

    return {
        "fact": text_fact,
        "table": text_table,
        "qr_code": text_qrcode
    }

    #pprint(text_qrcode)
    #pprint(text_fact)
    #pprint(text_table)
    #(blocks)

def main():
    files = sorted(glob("../../data/**/*.png"))
    
    nb_files = len(files)
    for i, file in enumerate(files):
        print(f"\r{(i+1)*100/nb_files:06.2f}% {file}\033[0K", end="", flush=True)
        try:
            process_image(file)
        except Exception as e:
            print(e)
    
    print()
if __name__ == "__main__":
    main()

    