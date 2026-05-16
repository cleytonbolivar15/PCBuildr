"""
Base scraper class - common functionality for all store scrapers.
Applies DRY principle to avoid duplication across scrapers.
"""

import sqlite3
import os
import time
from abc import ABC, abstractmethod
from typing import List, Dict


class BaseScraper(ABC):
    """Abstract base class for component scrapers"""

    def __init__(self, store_name: str, db_name: str):
        self.store_name = store_name
        self.db_name = db_name
        self.db_path = os.path.join(os.path.dirname(__file__), "..", f"{db_name}.sqlite")

    def crear_db(self):
        """Create database table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
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

    def categorizar(self, nombre: str) -> str:
        """Categorize component by name (shared logic across all scrapers)"""
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

    @abstractmethod
    def scrape(self) -> List[Dict]:
        """Scrape components from store (implements per-store logic)"""
        pass

    def actualizar_db(self):
        """Update database with scraped components"""
        self.crear_db()
        productos = self.scrape()
        ts = int(time.time())

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # Clear old data (keep only last 24 hours)
        c.execute("DELETE FROM componentes WHERE timestamp < ?", (ts - 86400,))

        # Insert new data
        for prod in productos:
            c.execute("""
            INSERT INTO componentes (nombre, precio, stock, url, categoria, tienda, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                prod.get("nombre", ""),
                prod.get("precio", 0),
                prod.get("stock", 1),
                prod.get("url", ""),
                prod.get("categoria", ""),
                self.store_name,
                ts
            ))

        conn.commit()
        conn.close()

    def obtener_componentes(self, categoria: str = None) -> List[Dict]:
        """Get components from database, optionally filtered by category"""
        self.crear_db()
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        if categoria:
            c.execute("SELECT * FROM componentes WHERE categoria = ?", (categoria,))
        else:
            c.execute("SELECT * FROM componentes")

        rows = c.fetchall()
        conn.close()

        # Convert to dictionaries
        componentes = []
        for row in rows:
            componentes.append({
                "id": row[0],
                "nombre": row[1],
                "precio": row[2],
                "stock": row[3],
                "url": row[4],
                "categoria": row[5],
                "tienda": row[6],
                "timestamp": row[7]
            })

        return componentes
