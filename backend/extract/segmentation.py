import cv2

def rgb_to_gray(image):# 🔹 Convertir en niveaux de gris
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def extract_blocks(gray):
    height, width = gray.shape
    stroke_width=3
    x1= y1= stroke_width
    w1=0.4*width-stroke_width
    h1=0.14*height-2*stroke_width

    x2= w1 *(1+0.6)
    y2= stroke_width
    w2=0.17*width
    h2=h1

    x3=stroke_width
    y3= h1+stroke_width
    w3=width-2*stroke_width
    h3=0.86*height-stroke_width
    # 🔹 Définition des blocs bien délimités
    rects = {
        "bloc_facturation": (x1,y1,w1,h1),  # Bloc de "Invoice" au dernier chiffre à 5 chiffres
        "bloc_qr_code": (x2,y2,w2,h2),  # Bloc des 2 encadrés en haut à droite
        "bloc_table": (x3,y3,w3,h3)  # Bloc de tout le reste
    }
    blocks = {}
    # 🔹 Dessiner les blocs sur l'image
    
    for block_name, coord in rects.items():
        
        x, y, w, h = coord
        cv2.rectangle(gray, (int(x), int(y)), (int(x+w), int(y+h)), (0, 255, 0), stroke_width)
        blocks[block_name]=gray[int(y):int(y+h), int(x):int(x+w)]
    return blocks  
