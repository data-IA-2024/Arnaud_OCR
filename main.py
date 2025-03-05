from getlist import get_png_files
from extract_png import download_png_files

if __name__ == "__main__":
    # 1️⃣ Récupérer la liste des fichiers PNG depuis le XML
    png_urls = get_png_files()

    # 2️⃣ Télécharger les fichiers PNG
    download_png_files(png_urls)
