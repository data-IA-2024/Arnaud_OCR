from fastapi import FastAPI, Request, File, UploadFile, Depends, HTTPException, status, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from pydantic import BaseModel
from datetime import datetime, timedelta
import os
from PIL import Image
import io
from fastapi.responses import RedirectResponse
from backend.script.main import process_image
from psswd import verify_credentials
from sqlalchemy.orm import Session
from database.db_connector import get_db
from database.model_table import Customer
from typing import Optional
import logging
import json
import traceback

TEMP_DIR = './temp/'

nbre_factures_OK = 0

#from psswd import verify_password
app = FastAPI()

# Configuration CORS corrigée
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],  # Port corrigé (8000 au lieu de 800)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration JWT
SECRET_KEY = "votre_clé_secrète_très_longue_et_aléatoire"  # À changer en production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Authentification en dur
HARDCODED_USER = {
    "username": "a@gmail.com",
    "password": "1234",  # À ne PAS faire en production
    "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # Hachage de '1234'
}
print('crypt...')
print('crypt Done')
# Configuration des templates
app.mount("/static", StaticFiles(directory="static"), name="static")

# Définition du chemin absolu vers le dossier templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates_path = os.path.join(BASE_DIR, "templates")

print(f"Templates path: {templates_path}")
print(f"Base.html exists: {os.path.exists(os.path.join(templates_path, 'base.html'))}")

if not os.path.exists(templates_path):
    os.makedirs(templates_path)
    print(f"Created templates directory at {templates_path}")

templates = Jinja2Templates(directory=templates_path)

print('jinja Done')
# Récupération du token depuis les cookies
async def get_current_user(request: Request):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentification requise",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = request.cookies.get("access_token")
    if not token or not token.startswith("Bearer "):
        return None
        #raise credentials_exception

    try:
        token = token.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username != HARDCODED_USER["username"]:
            #raise credentials_exception
            return None
        return username
    except JWTError:
        #raise credentials_exception
        return None

# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    #print(user, 14)
    #if isinstance (user, str):
    return templates.TemplateResponse("index.html", {"request": request})
    #return RedirectResponse(url="/signin")

@app.get("/signin", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if not verify_credentials(username, password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects"
        )

    access_token = jwt.encode(
        {"sub": username, "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="Lax"
    )
    return response

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@app.get("/billing", response_class=HTMLResponse)
async def billing_data(request: Request, user: str = Depends(get_current_user)):
    try:
        # Vérification du token
        if not user:
            return RedirectResponse(url="/monitoring")
        
        # Vérification du template
        if not hasattr(templates, "get_template"):
            raise Exception("Templates not properly configured")
            
        # Test du rendu template minimal
        try:
            return templates.TemplateResponse(
                "billing.html",
                {
                    "request": request,
                    "billing_data": [],
                    "user": user
                }
            )
        except Exception as template_error:
            print(f"Template error: {str(template_error)}")
            return JSONResponse(
                status_code=500,
                content={"error": f"Template error: {str(template_error)}"}
            )
            
    except Exception as e:
        print(f"Error in billing route: {str(e)}")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "trace": traceback.format_exc()}
        )

@app.get("/monitoring", response_class=HTMLResponse)
async def monitoring_data(request: Request):
    #if isinstance(user, str):
    return templates.TemplateResponse("monitoring.html", {"request": request, "log_1":nbre_factures_OK//2, "date_today":datetime.now().strftime('%d-%m-%Y')})
#    return RedirectResponse(url="/signin")


@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/signin")
    response.delete_cookie("access_token")
    return response

@app.get("/customers", response_class=HTMLResponse)
async def customers_page(request: Request, user: str = Depends(get_current_user)):
    if isinstance(user, str):
        return templates.TemplateResponse("customers.html", {"request": request})
    return RedirectResponse(url="/signin")

@app.get("/api/customers")
async def get_customers(name: str = None, email: str = None, db: Session = Depends(get_db)):
    query = db.query(Customer)
    if name:
        query = query.filter(Customer.name.ilike(f"%{name}%"))
    if email:
        query = query.filter(Customer.email.ilike(f"%{email}%"))
    customers = query.all()
    return [
        {
            "email": customer.email,
            "name": customer.name,
            "gender": customer.gender,
            "adress": customer.adress,
            "birth": customer.birth.isoformat() if customer.birth else None
        }
        for customer in customers
    ]


# Routes protégées
@app.post("/upload")
async def upload_file(file: UploadFile, user: str = Depends(get_current_user)):
    try:
        upload_folder = "./uploads"
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        return {"message": f"Fichier {file.filename} uploadé avec succès."}
    except Exception as e:
        return {"error": str(e)}
    
    # Configuration du logging
logging.basicConfig(
    filename='ocr_monitoring.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@app.post("/OCR")
async def OCR_page(file: UploadFile = File(...)):
    
    temp_file = TEMP_DIR + '/invoice-temp.png'
    try:
        if not file.content_type.startswith("image/"):
            logging.error(f"Type de fichier invalide: {file.content_type}")
            raise HTTPException(400, "Seules les images sont acceptées")

        logging.info(f"Traitement de l'image: {file.filename}")
        
        with open(temp_file, 'wb') as f:
            f.write(await file.read())
       
        start_time = datetime.now()
        result = process_image(temp_file)
        #processing_time = (datetime.now() - start_time).total_seconds()
        
       
    #    # Log du résultat
    #     log_entry = {
    #         "timestamp": datetime.now().isoformat(),
    #         "filename": file.filename,
    #         "processing_time": processing_time,
    #         "success": True,
    #         "data": {
    #             "numero_facture": result["fact"]["no"],
    #             "date": result["qr_code"]["date"],
    #             "email": result["fact"]["email"],
    #             "montant": result["table"]["total"]
    #         }
    #     }

        global nbre_factures_OK
        nbre_factures_OK =  nbre_factures_OK + 1
        
        return {
            "numero_facture": result["fact"]["no"],
            "date": result["qr_code"]["date"],
            "nom": result["fact"]["name"],
            "email": result["fact"]["email"],
            "adresse": result["fact"]["adress"],
            "montant": f"{result['table']['total']}€"
        }

    except Exception as e:
        logging.error(f"Erreur de traitement: {str(e)}")
        raise HTTPException(500, detail=f"Erreur de traitement : {str(e)}")
    