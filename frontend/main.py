from fastapi import FastAPI, Request, File, UploadFile, Depends, HTTPException, status, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime, timedelta
import os
from PIL import Image
import io
from fastapi.responses import RedirectResponse
from backend.script.main import process_image
from psswd import verify_credentials
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
    "username": "arnaud",
    "password": "1234",  # À ne PAS faire en production
    "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # Hachage de '1234'
}
print('crypt...')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
print('crypt Done')
# Configuration des templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
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
async def home(request: Request, user:str = Depends(get_current_user)):
    print(user, 14)
    if isinstance (user, str):
        return templates.TemplateResponse("index.html", {"request": request})
    return RedirectResponse(url="/signin")

@app.get("/signin", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if username != HARDCODED_USER["username"] or not pwd_context.verify(password, HARDCODED_USER["hashed_password"]):
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

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie("access_token")
    return response

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

@app.post("/OCR")
async def OCR_page(file: UploadFile = File(...), user: str = 'arno'):#Depends(get_current_user)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    image.save("temp/temp.png")
    return {'filename': file.filename, 'result': process_image('temp/temp.png')}