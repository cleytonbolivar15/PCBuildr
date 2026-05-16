import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from componentes import CPU, Motherboard, RAM, GPU, Fuente, Gabinete, Cooler, validar_compatibilidad
from scrapers.extremetech import obtener_componentes as obtener_extremetech
from scrapers.intelec import obtener_componentes as obtener_intelec
from scrapers.facebook import obtener_componentes as obtener_facebook
from pydantic import BaseModel
from typing import List, Optional
import json
from fastapi import HTTPException

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos para recibir builds desde el frontend
class BuildRequest(BaseModel):
    cpu: dict
    mb: dict
    ram: dict
    gpu: dict
    fuente: dict
    gabinete: dict
    cooler: Optional[dict] = None

USERS_FILE = os.path.join(os.path.dirname(__file__), "..", "usuarios.json")

DEFAULT_USERS = {"DemoUsr": "2025"}

def load_users():
    # Carga usuarios desde el archivo, siempre incluye el usuario demo
    users = {}
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                users = json.load(f)
        except Exception:
            users = {}
    users.update(DEFAULT_USERS)
    return users

def save_users(users):
    # Nunca borra el usuario demo
    users = {k: v for k, v in users.items() if k != ""}  # limpia claves vacías
    users.update(DEFAULT_USERS)
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

@app.get("/")
def read_root():
    return {"msg": "PCBuildr backend running"}

@app.post("/validar_build")
def validar_build(build: BuildRequest):
    cpu = CPU(**build.cpu)
    mb = Motherboard(**build.mb)
    ram = RAM(**build.ram)
    gpu = GPU(**build.gpu)
    fuente = Fuente(**build.fuente)
    gabinete = Gabinete(**build.gabinete)
    cooler = Cooler(**build.cooler) if build.cooler else None
    # Permite builds grandes, aumenta el límite de tamaño de respuesta
    errores = validar_compatibilidad(cpu, mb, ram, gpu, fuente, gabinete, cooler)
    return {"errores": errores}

@app.get("/precios")
def precios():
    """Get prices for all components from all stores"""
    try:
        # Combine prices from all stores
        comps = []
        comps.extend(obtener_extremetech())
        comps.extend(obtener_intelec())
        comps.extend(obtener_facebook())
        return comps
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener precios: {e}")

@app.get("/componentes")
def get_componentes(categoria: str = None, tienda: str = None):
    try:
        comps = []
        if not tienda or tienda.lower() == "extremetech":
            comps += obtener_extremetech(categoria)
        if not tienda or tienda.lower() == "intelec":
            comps += obtener_intelec(categoria)
        if not tienda or tienda.lower() in ["facebook", "facebook marketplace", "marketplace"]:
            comps += obtener_facebook(categoria)
        return comps
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener componentes: {e}")

@app.post("/register")
def register(data: dict):
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    if not username or not password:
        raise HTTPException(status_code=400, detail="Usuario y contraseña requeridos")
    if username == "DemoUsr":
        raise HTTPException(status_code=409, detail="El usuario demo ya existe")
    users = load_users()
    if username in users:
        raise HTTPException(status_code=409, detail="El usuario ya existe")
    users[username] = password
    save_users(users)
    return {"msg": "Usuario registrado correctamente"}

@app.post("/login")
def login(data: dict):
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    users = load_users()
    if username in users and users[username] == password:
        return {"msg": "Login exitoso"}
    raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

@app.post("/delete_user")
def delete_user(data: dict):
    username = data.get("username", "").strip()
    if username == "DemoUsr":
        raise HTTPException(status_code=403, detail="No puedes borrar el usuario demo")
    users = load_users()
    if username in users:
        del users[username]
        save_users(users)
        return {"msg": f"Usuario {username} eliminado"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
