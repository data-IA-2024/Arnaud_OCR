from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from datetime import datetime

app = FastAPI()

# Montage du dossier static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Définition du dossier des templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/navbar", response_class=HTMLResponse)
async def navbar_page(request: Request):
    return templates.TemplateResponse("navbar.html", {"request": request})
@app.post("/upload")
async def upload_file(file: UploadFile):
    try:
        # Définir un chemin pour enregistrer les fichiers
        upload_folder = "./uploads"
        os.makedirs(upload_folder, exist_ok=True)
        
        # Enregistrer le fichier sur le serveur
        file_path = os.path.join(upload_folder, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        return {"message": f"Fichier {file.filename} uploadé avec succès."}
    except Exception as e:
        return {"error": str(e)}

@app.get("/logout", response_class=HTMLResponse)
async def logout_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
