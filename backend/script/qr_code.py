import cv2
from pyzbar.pyzbar import decode
import os.path
from PIL import Image
import glob


def read_qrcode(image):

    # Décoder le QR code
    qr_codes = decode(image)

    text=qr_codes[0].data.decode("utf-8")
    lines=text.split("\n")

    invoice_number=lines[0][8:]

    date=lines[1][5:]
    
    customer_sex,birthdate=lines[2].split(", ")
   
    customer_sex=customer_sex[5:]
   
    birthdate=birthdate[6:]

    return {
        "invoice_number": invoice_number,
        "date": date,
        "customer_sex": customer_sex,
        "customer_birthdate": birthdate
    }

def open_image(image_path):
    # Charger l'image correctement
    if os.path.isfile(image_path):
        return cv2.imread(image_path)
    raise FileNotFoundError(f"❌ L'image {image_path} n'existe pas.")
    
if __name__ == "__main__":
    data_content = glob.glob("./../../data/*")
    for year in data_content:
        image_paths = glob.glob(year + "/*.png")
        for image_path in image_paths:
            print(f"\r{image_path}\033[0K", end="")
            image = open_image(image_path)
            try:
                text = read_qrcode(image)
            except IndexError:
                pass
    
