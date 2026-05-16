import requests
import sqlite3
import time
from bs4 import BeautifulSoup
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "intelec.sqlite")

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

def scrape_intelec():
    base_url = "https://www.intelec.co.cr"
    url = f"{base_url}/componentes/"
    productos = []
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    for item in soup.select(".product"):
        nombre_tag = item.select_one(".woocommerce-loop-product__title")
        precio_tag = item.select_one(".price")
        url_tag = item.select_one("a.woocommerce-LoopProduct-link")
        img_tag = item.select_one("img")
        nombre = nombre_tag.get_text(strip=True) if nombre_tag else "Sin nombre"
        precio = 0
        if precio_tag:
            precio_txt = precio_tag.get_text(strip=True).replace("₡", "").replace(",", "").replace(".", "")
            precio = int("".join(filter(str.isdigit, precio_txt))) if precio_txt else 0
        url_prod = url_tag["href"] if url_tag and url_tag.has_attr("href") else ""
        img_url = img_tag["src"] if img_tag and img_tag.has_attr("src") else ""
        stock = 1  # Intelec no muestra stock en listado, asume 1
        categoria = categorizar(nombre)
        productos.append({
            "nombre": nombre,
            "precio": precio,
            "stock": stock,
            "url": url_prod,
            "categoria": categoria,
            "tienda": "Intelec",
            "imagen": img_url
        })
    return productos

def actualizar_db():
    crear_db()
    productos = scrape_intelec()
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
    print("Creando base de datos y scrapeando Intelec...")
    actualizar_db()
    print("Componentes guardados en intelec.sqlite")
