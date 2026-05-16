"""
Extreme Tech store scraper
Fetches components from extremetechcr.com
"""

import requests
from bs4 import BeautifulSoup
from base_scraper import BaseScraper


class ExtremetechScraper(BaseScraper):
    """Scraper for Extreme Tech store"""

    def __init__(self):
        super().__init__("Extreme Tech", "extremetech")

    def scrape(self):
        """Scrape components from Extreme Tech website"""
        base_url = "https://extremetechcr.com"
        url = f"{base_url}/tienda/12-componentes"
        productos = []
        page = 1

        try:
            while True:
                page_url = url + (f"?page={page}" if page > 1 else "")
                r = requests.get(page_url, timeout=10)
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

                    categoria = self.categorizar(nombre)
                    productos.append({
                        "nombre": nombre,
                        "precio": precio,
                        "stock": stock,
                        "url": url_prod,
                        "categoria": categoria,
                        "tienda": "Extreme Tech",
                        "imagen": img_url
                    })

                # Check for next page
                next_btn = soup.select_one("li.page-item.active + li.page-item a")
                if not next_btn:
                    break
                page += 1

        except Exception as e:
            print(f"[ERROR] Scraping Extreme Tech failed: {e}")

        return productos


def obtener_componentes(categoria=None):
    """Get components from Extreme Tech store"""
    scraper = ExtremetechScraper()
    scraper.actualizar_db()
    return scraper.obtener_componentes(categoria)


def actualizar_db():
    """Update Extreme Tech database"""
    scraper = ExtremetechScraper()
    scraper.actualizar_db()


if __name__ == "__main__":
    actualizar_db()
    print("Extreme Tech database updated")
