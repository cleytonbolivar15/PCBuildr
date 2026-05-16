import requests
import sqlite3
import time
from bs4 import BeautifulSoup
import os
import re

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "facebook.sqlite")

SEARCH_URLS = [
    "https://www.facebook.com/marketplace/113489138666560/search?query=Componentes",
    "https://www.facebook.com/marketplace/113489138666560/search?query=Grafica",
    "https://www.facebook.com/marketplace/113489138666560/search?query=Cpu",
    "https://www.facebook.com/marketplace/113489138666560/search?query=Ryzen",
    "https://www.facebook.com/marketplace/113489138666560/search?query=Intel%20core%205",
    "https://www.facebook.com/marketplace/113489138666560/search?query=Tarjeta%20madre",
    "https://www.facebook.com/marketplace/113489138666560/search?query=fuente%20de%20poder",
    "https://www.facebook.com/marketplace/113489138666560/search?query=Case%20pc",
    "https://www.facebook.com/marketplace/113489138666560/search?query=Ventilador%20pc",
    "https://www.facebook.com/marketplace/113489138666560/search?query=Cooler%20pc",
    "https://www.facebook.com/marketplace/113489138666560/search?query=Ram",
    "https://www.facebook.com/marketplace/113489138666560/search?query=SSD",
]

def crear_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS componentes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        precio INTEGER,
        stock INTEGER,
        url TEXT,
        categoria TEXT,
        tienda TEXT,
        timestamp INTEGER
    )
    """)
    conn.commit()
    conn.close()

def categorizar(nombre):
    n = nombre.lower()
    if "procesador" in n or "cpu" in n or "ryzen" in n or "intel" in n:
        return "CPU"
    if "tarjeta madre" in n or "motherboard" in n or "mainboard" in n:
        return "Motherboard"
    if "ram" in n or "memoria" in n:
        return "RAM"
    if "ssd" in n or "hdd" in n or "m.2" in n or "almacenamiento" in n:
        return "Almacenamiento"
    if "fuente" in n or "psu" in n or "power supply" in n:
        return "Fuente"
    if "gabinete" in n or "case" in n:
        return "Gabinete"
    if "ventilador" in n or "fan" in n or "cooler" in n:
        return "Ventilador"
    if "tarjeta gráfica" in n or "gpu" in n or "rtx" in n or "gtx" in n or "radeon" in n:
        return "GPU"
    return "Otro"

def scrape_facebook():
    productos = []
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    for url in SEARCH_URLS:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        for item in soup.find_all("div"):
            title = item.get_text(strip=True)
            if not title or "gratis" in title.lower():
                continue
            price_match = re.search(r"₡\s?([\d,\.]+)", title)
            if not price_match:
                continue
            precio = int(price_match.group(1).replace(",", "").replace(".", ""))
            categoria = categorizar(title)
            productos.append({
                "nombre": title[:60],
                "precio": precio,
                "stock": 1,
                "url": url,
                "categoria": categoria,
                "tienda": "Facebook Marketplace",
                "imagen": ""
            })
    return productos

def actualizar_db():
    crear_db()
    productos = scrape_facebook()
    ts = int(time.time())
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for prod in productos:
        c.execute("""
        INSERT INTO componentes (nombre, precio, stock, url, categoria, tienda, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (prod["nombre"], prod["precio"], prod["stock"], prod["url"], prod["categoria"], prod["tienda"], ts))
    conn.commit()
    conn.close()

def obtener_componentes(categoria=None):
    crear_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    ts_limite = int(time.time()) - 12*3600
    if categoria:
        c.execute("""
        SELECT nombre, precio, stock, url, categoria, tienda FROM componentes
        WHERE categoria=? AND timestamp>? ORDER BY precio ASC
        """, (categoria, ts_limite))
    else:
        c.execute("""
        SELECT nombre, precio, stock, url, categoria, tienda FROM componentes
        WHERE timestamp>? ORDER BY categoria, precio ASC
        """, (ts_limite,))
    res = [
        {"nombre": n, "precio": p, "stock": s, "url": u, "categoria": cat, "tienda": t}
        for n, p, s, u, cat, t in c.fetchall()
    ]
    conn.close()
    return res

if __name__ == "__main__":
    print("Creando base de datos y scrapeando Facebook Marketplace...")
    actualizar_db()
    print("Componentes guardados en facebook.sqlite")
