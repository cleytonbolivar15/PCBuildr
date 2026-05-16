"""
Intelec store scraper
Fetches components from intelec.co.cr
"""

import requests
from bs4 import BeautifulSoup
from base_scraper import BaseScraper


class IntelecScraper(BaseScraper):
    """Scraper for Intelec store"""

    def __init__(self):
        super().__init__("Intelec", "intelec")

    def scrape(self):
        """Scrape components from Intelec website"""
        url = "https://www.intelec.co.cr/componentes/"
        productos = []

        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            items = soup.find_all("div", class_="product")

            for item in items:
                nombre_tag = item.find("a", class_="product-name")
                precio_tag = item.find("span", class_="price")

                if not nombre_tag:
                    continue

                nombre = nombre_tag.get_text(strip=True)
                precio = 0
                if precio_tag:
                    precio_txt = "".join(filter(str.isdigit, precio_tag.get_text(strip=True)))
                    precio = int(precio_txt) if precio_txt else 0

                url_prod = nombre_tag.get("href", "")
                categoria = self.categorizar(nombre)

                productos.append({
                    "nombre": nombre,
                    "precio": precio,
                    "stock": 1,
                    "url": url_prod,
                    "categoria": categoria,
                    "tienda": "Intelec",
                })

        except Exception as e:
            print(f"[ERROR] Scraping Intelec failed: {e}")

        return productos


def obtener_componentes(categoria=None):
    """Get components from Intelec store"""
    scraper = IntelecScraper()
    scraper.actualizar_db()
    return scraper.obtener_componentes(categoria)


def actualizar_db():
    """Update Intelec database"""
    scraper = IntelecScraper()
    scraper.actualizar_db()


if __name__ == "__main__":
    actualizar_db()
    print("Intelec database updated")
