import requests
import sqlite3
import time
from bs4 import BeautifulSoup
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "extremetech.sqlite")

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

def scrape_extremetech():
    # Scraping de la sección de componentes de Extreme Tech
    base_url = "https://extremetechcr.com"
    url = f"{base_url}/tienda/12-componentes"
    productos = []
    page = 1
    while True:
        page_url = url + (f"?page={page}" if page > 1 else "")
        r = requests.get(page_url)
        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.select("div.product-miniature")
        if not items:
            break
        for item in items:
            nombre_tag = item.select_one(".product-title")
            precio_tag = item.select_one(".price")
            url_tag = item.select_one("a.product-thumbnail")
            img_tag = item.select_one("img")
            stock_tag = item.select_one(".availability span")
            nombre = nombre_tag.get_text(strip=True) if nombre_tag else "Sin nombre"
            precio = 0
            if precio_tag:
                precio_txt = precio_tag.get_text(strip=True).replace("₡", "").replace(",", "").replace(".", "")
                precio = int("".join(filter(str.isdigit, precio_txt))) if precio_txt else 0
            url_prod = base_url + url_tag["href"] if url_tag and url_tag.has_attr("href") else ""
            img_url = img_tag["src"] if img_tag and img_tag.has_attr("src") else ""
            stock = 1
            if stock_tag:
                stock_txt = stock_tag.get_text(strip=True).lower()
                if "agotado" in stock_txt or "no disponible" in stock_txt:
                    stock = 0
            categoria = categorizar(nombre)
            productos.append({
                "nombre": nombre,
                "precio": precio,
                "stock": stock,
                "url": url_prod,
                "categoria": categoria,
                "tienda": "Extreme Tech",
                "imagen": img_url
            })
        # Verifica si hay siguiente página
        next_btn = soup.select_one("li.page-item.active + li.page-item a")
        if not next_btn:
            break
        page += 1
    return productos

def actualizar_db():
    crear_db()
    productos = scrape_extremetech()
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
    # Permite crear la base de datos y poblarla manualmente
    print("Creando base de datos y scrapeando Extreme Tech...")
    actualizar_db()
    print("Componentes guardados en extremetech.sqlite")
