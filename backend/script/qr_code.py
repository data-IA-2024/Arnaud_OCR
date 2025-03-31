import cv2
from pyzbar.pyzbar import decode
import os
import glob
import json

def read_qrcode(image):
    """Décode le QR code d'une image et extrait les informations."""
    
    # Détecter les QR codes dans l'image
    qr_codes = decode(image)

    if not qr_codes:
        raise ValueError("❌ Aucun QR code détecté.")

    try:
        text = qr_codes[0].data.decode("utf-8")
        lines = text.split("\n")

        return lines
    
    except (IndexError, ValueError) as e:
        raise ValueError(f"❌ Erreur lors de l'extraction des données du QR code : {e}")


    
