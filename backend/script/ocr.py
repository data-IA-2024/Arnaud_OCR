import pytesseract
import os
from dotenv import load_dotenv
from backend.script.utils import load_image
import re
from glob import glob

load_dotenv(dotenv_path="../../.env")
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(image):
    return re.split (r"\n+",pytesseract.image_to_string(image, lang="eng", config="--psm 6 --oem 1"))[:-1]

if __name__ == "__main__":
    file = sorted(glob('../../data/2018/*.png'))[0]
    print(file)
    print(pytesseract.pytesseract.tesseract_cmd)
    image = load_image(file)
    print(extract_text(image))