"""
Modelo de datos y validaciones de compatibilidad para PCBuildr
"""

from dataclasses import dataclass
from typing import List, Optional

@dataclass
class CPU:
    nombre: str
    socket: str
    tdp: int
    generacion: str

@dataclass
class Motherboard:
    nombre: str
    socket: str
    chipset: str
    formato: str
    ram_tipo: str
    ram_slots: int
    max_ram: int

@dataclass
class RAM:
    nombre: str
    tipo: str
    capacidad: int
    velocidad: int
    sticks: int

@dataclass
class GPU:
    nombre: str
    largo_mm: int
    tdp: int
    pines: List[str]

@dataclass
class Fuente:
    nombre: str
    potencia: int
    pines_gpu: List[str]
    certificacion: str

@dataclass
class Gabinete:
    nombre: str
    formato: List[str]
    max_gpu_mm: int
    max_cooler_mm: int

@dataclass
class Cooler:
    nombre: str
    altura_mm: int

def validar_compatibilidad(cpu: CPU, mb: Motherboard, ram: RAM, gpu: GPU, fuente: Fuente, gabinete: Gabinete, cooler: Optional[Cooler]=None) -> List[str]:
    """Validate PC component compatibility"""
    errores = []
    if cpu.socket != mb.socket:
        errores.append(f"El socket de la CPU ({cpu.socket}) no es compatible con la motherboard ({mb.socket})")
    if ram.tipo != mb.ram_tipo:
        errores.append(f"La RAM ({ram.tipo}) no es compatible con la motherboard ({mb.ram_tipo})")
    if ram.sticks > mb.ram_slots:
        errores.append(f"La motherboard solo tiene {mb.ram_slots} slots de RAM, pero seleccionaste {ram.sticks}")
    if gpu.largo_mm > gabinete.max_gpu_mm:
        errores.append(f"La GPU es demasiado larga para el gabinete (máx {gabinete.max_gpu_mm}mm)")
    for pin in gpu.pines:
        if pin not in fuente.pines_gpu:
            errores.append(f"La fuente no tiene el conector {pin} necesario para la GPU")
    if cooler and cooler.altura_mm > gabinete.max_cooler_mm:
        errores.append(f"El cooler es demasiado alto para el gabinete (máx {gabinete.max_cooler_mm}mm)")
    return errores
