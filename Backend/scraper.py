"""
Scraper de ejemplo para obtener precios y stock de componentes de una tienda ficticia.
Puedes adaptarlo para tiendas reales agregando requests y parsing de HTML/JSON.
"""

def obtener_precios_tienda():
    # Simulación de respuesta de una API/HTML de tienda
    return [
        {"nombre": "Ryzen 5 5600X", "precio": 95000, "stock": 5, "tienda": "TiendaX"},
        {"nombre": "B550M DS3H", "precio": 65000, "stock": 2, "tienda": "TiendaX"},
        {"nombre": "Corsair Vengeance 16GB", "precio": 32000, "stock": 10, "tienda": "TiendaX"},
        {"nombre": "RTX 4060", "precio": 210000, "stock": 1, "tienda": "TiendaX"},
        {"nombre": "EVGA 600W", "precio": 28000, "stock": 7, "tienda": "TiendaX"},
        {"nombre": "NZXT H510", "precio": 45000, "stock": 3, "tienda": "TiendaX"},
        {"nombre": "Cooler Master Hyper 212", "precio": 18000, "stock": 4, "tienda": "TiendaX"},
    ]

def buscar_componente(nombre: str, inventario) -> dict:
    for comp in inventario:
        if comp["nombre"].lower() == nombre.lower():
            return comp
    return {"nombre": nombre, "precio": None, "stock": 0, "tienda": "No encontrado"}
