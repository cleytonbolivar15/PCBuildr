"""
Recommendation engine for PC components based on use case and budget.
"""

from typing import Dict, List, Optional


class RecommendationEngine:
    """Generates PC build recommendations"""

    def __init__(self, language: str = "es"):
        self.language = language

    def recommend_build(self, budget: int, use_case: str) -> Dict:
        """
        Recommend a complete PC build based on budget and use case.

        Args:
            budget: Total budget in dollars
            use_case: "gaming", "workstation", "office", "streaming", etc.

        Returns:
            Recommended build configuration
        """
        if use_case == "gaming":
            return self._recommend_gaming(budget)
        elif use_case == "workstation":
            return self._recommend_workstation(budget)
        elif use_case == "streaming":
            return self._recommend_streaming(budget)
        else:
            return self._recommend_office(budget)

    def _recommend_gaming(self, budget: int) -> Dict:
        """Recommend gaming PC"""
        if budget < 600:
            tier = "entry"
            cpu = {"nombre": "Intel Core i3-12100", "socket": "Socket 1700"}
            gpu = {"nombre": "GTX 1650", "largo_mm": 200}
            ram = {"tipo": "DDR4", "capacidad": 16, "sticks": 2}
        elif budget < 1200:
            tier = "mid"
            cpu = {"nombre": "Intel Core i5-12400", "socket": "Socket 1700"}
            gpu = {"nombre": "RTX 3060 Ti", "largo_mm": 290}
            ram = {"tipo": "DDR4", "capacidad": 16, "sticks": 2}
        else:
            tier = "high"
            cpu = {"nombre": "Intel Core i7-13700K", "socket": "Socket 1700"}
            gpu = {"nombre": "RTX 4080", "largo_mm": 320}
            ram = {"tipo": "DDR5", "capacidad": 32, "sticks": 2}

        return {
            "tier": tier,
            "use_case": "gaming",
            "cpu": cpu,
            "gpu": gpu,
            "ram": ram,
            "psu": {"potencia": self._estimate_psu(cpu, gpu)},
        }

    def _recommend_workstation(self, budget: int) -> Dict:
        """Recommend workstation PC"""
        if budget < 2000:
            cpu = {"nombre": "AMD Ryzen 7 5700X", "socket": "Socket AM4"}
            gpu = {"nombre": "RTX 3090", "largo_mm": 300}
            ram = {"tipo": "DDR4", "capacidad": 32, "sticks": 2}
        else:
            cpu = {"nombre": "AMD Ryzen 9 7950X", "socket": "Socket AM5"}
            gpu = {"nombre": "RTX 4090", "largo_mm": 320}
            ram = {"tipo": "DDR5", "capacidad": 64, "sticks": 2}

        return {
            "tier": "professional",
            "use_case": "workstation",
            "cpu": cpu,
            "gpu": gpu,
            "ram": ram,
            "psu": {"potencia": self._estimate_psu(cpu, gpu)},
        }

    def _recommend_streaming(self, budget: int) -> Dict:
        """Recommend streaming PC"""
        cpu = {"nombre": "AMD Ryzen 7 5800X3D", "socket": "Socket AM4"}
        gpu = {"nombre": "RTX 3070", "largo_mm": 280}
        ram = {"tipo": "DDR4", "capacidad": 32, "sticks": 2}

        return {
            "tier": "streaming",
            "use_case": "streaming",
            "cpu": cpu,
            "gpu": gpu,
            "ram": ram,
            "psu": {"potencia": self._estimate_psu(cpu, gpu)},
        }

    def _recommend_office(self, budget: int) -> Dict:
        """Recommend office PC"""
        cpu = {"nombre": "Intel Core i3-12100", "socket": "Socket 1700"}
        gpu = {"nombre": "Integrated", "largo_mm": 0}
        ram = {"tipo": "DDR4", "capacidad": 16, "sticks": 1}

        return {
            "tier": "office",
            "use_case": "office",
            "cpu": cpu,
            "gpu": gpu,
            "ram": ram,
            "psu": {"potencia": 450},
        }

    def suggest_alternative(self, component: Dict, reason: str) -> Optional[Dict]:
        """Suggest alternative component"""
        component_type = component.get("type", "")

        alternatives = {
            "GPU": [
                {"nombre": "RTX 4090", "precio": 1599},
                {"nombre": "RTX 4080", "precio": 1199},
                {"nombre": "RTX 4070", "precio": 799},
                {"nombre": "AMD RX 7900 XTX", "precio": 1399},
            ],
            "CPU": [
                {"nombre": "Intel Core i9-13900K", "precio": 689},
                {"nombre": "AMD Ryzen 9 7950X", "precio": 699},
                {"nombre": "Intel Core i7-13700K", "precio": 419},
            ],
        }

        options = alternatives.get(component_type, [])
        if options:
            return options[0]

        return None

    def rank_components(self, category: str, filters: Optional[Dict] = None) -> List[Dict]:
        """Rank components by value and performance"""
        components = {
            "CPU": [
                {"nombre": "Intel Core i7-13700K", "rendimiento": 9, "precio": 419},
                {"nombre": "Intel Core i5-13600K", "rendimiento": 8, "precio": 319},
                {"nombre": "AMD Ryzen 7 5700X", "rendimiento": 8, "precio": 299},
            ],
            "GPU": [
                {"nombre": "RTX 4080", "rendimiento": 9, "precio": 1199},
                {"nombre": "RTX 4070", "rendimiento": 8, "precio": 799},
                {"nombre": "RTX 3080", "rendimiento": 7, "precio": 699},
            ],
        }

        ranked = components.get(category, [])
        # Sort by value (performance/price)
        ranked.sort(key=lambda x: x.get("rendimiento", 0) / max(x.get("precio", 1), 1), reverse=True)

        return ranked

    def _estimate_psu(self, cpu: Dict, gpu: Dict) -> int:
        """Estimate PSU wattage needed"""
        cpu_name = cpu.get("nombre", "").lower()
        gpu_name = gpu.get("nombre", "").lower()

        cpu_tdp = 95 if "i7" in cpu_name else 65 if "i5" in cpu_name else 45
        gpu_tdp = 320 if "4090" in gpu_name else 300 if "4080" in gpu_name else 250

        total = cpu_tdp + gpu_tdp + 150  # Add overhead
        psu = int((total * 1.3) / 50) * 50  # Round up to nearest 50W

        return max(psu, 450)
