from backend.script.access_to_xml import list_png_files
from backend.script.extract_png import download_png
import os

def main():
    print("🔍 Récupération de la liste des fichiers PNG de 2018 à 2024...")
    png_files = list_png_files()
    
    # Définir les années à télécharger
    YEARS = [str(year) for year in range(2018, 2025)]
    
    # Filtrer les fichiers par année
    png_by_year = {year: [] for year in YEARS}

    for file in png_files:
        for year in YEARS:
            if year in file:
                png_by_year[year].append(file)
                break

    # Afficher les fichiers trouvés
    total_files = sum(len(files) for files in png_by_year.values())
    
    if total_files == 0:
        print("❌ Aucun fichier PNG trouvé.")
        return

    for year, files in png_by_year.items():
        if files:
            print(f"\n📂 {len(files)} fichiers trouvés pour {year} :")
            for file in files[:5]:  # Afficher un aperçu des 5 premiers fichiers
                print(f" - {file}")
            if len(files) > 5:
                print(f"   ... et {len(files) - 5} autres fichiers.")

    choix = input("\n➡️ Voulez-vous télécharger tous ces fichiers ? (o/n) : ").strip().lower()

    if choix == "o":
        for year, files in png_by_year.items():
            if files:
                os.makedirs(f"./data/{year}", exist_ok=True)
                for file_name in files:
                    download_png(file_name, year)

        print(f"✅ {total_files} fichiers téléchargés avec succès !")
    else:
        print("❌ Téléchargement annulé.")

if __name__ == "__main__":
    main()