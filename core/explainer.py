"""
Hardware explainer - provides technical information about components.
"""

from typing import Dict, Optional


class HardwareExplainer:
    """Explains PC hardware in user-friendly language"""

    def __init__(self, language: str = "es"):
        self.language = language

    def explain_component(self, component_name: str, component_type: str) -> str:
        """Explain what a component does and why it matters"""
        exp_lower = component_name.lower()
        type_lower = component_type.lower()

        if "cpu" in type_lower or "procesador" in type_lower:
            return self._explain_cpu(exp_lower)
        elif "gpu" in type_lower or "tarjeta" in type_lower or "gráfica" in type_lower:
            return self._explain_gpu(exp_lower)
        elif "ram" in type_lower or "memoria" in type_lower:
            return self._explain_ram(exp_lower)
        elif "psu" in type_lower or "fuente" in type_lower:
            return self._explain_psu()
        elif "case" in type_lower or "gabinete" in type_lower:
            return self._explain_case()
        elif "cooler" in type_lower:
            return self._explain_cooler()
        elif "motherboard" in type_lower or "placa" in type_lower:
            return self._explain_motherboard()
        else:
            return self._get_generic_explanation()

    def _explain_cpu(self, name: str) -> str:
        """Explain CPU"""
        if self.language == "es":
            return ("⚙️ **Procesador (CPU)**\n\n"
                    "Cerebro de tu PC. A mayor velocidad (GHz) y más cores, mejor.\n"
                    "• Cores: Tareas simultáneas\n"
                    "• Threads: Instrucciones paralelas\n"
                    "• Socket: Determina compatibilidad\n"
                    "• TDP: Calor generado (importante para cooler)\n\n"
                    "Marcas: Intel Core i3/i5/i7/i9 | AMD Ryzen")
        else:
            return ("⚙️ **Processor (CPU)**\n\n"
                    "Your PC's brain. Higher speed (GHz) and more cores = better.\n"
                    "• Cores: Simultaneous tasks\n"
                    "• Threads: Parallel instructions\n"
                    "• Socket: Determines compatibility\n"
                    "• TDP: Heat generated (important for cooler)\n\n"
                    "Brands: Intel Core i3/i5/i7/i9 | AMD Ryzen")

    def _explain_gpu(self, name: str) -> str:
        """Explain GPU"""
        if self.language == "es":
            return ("🎮 **Tarjeta Gráfica (GPU)**\n\n"
                    "Especialista en gráficos y juegos. Crítica para gaming.\n"
                    "• VRAM: Más = mejor para alta resolución/texturas\n"
                    "• Cores: Potencia de cálculo\n"
                    "• Ray Tracing: Iluminación realista\n"
                    "• TDP: Consumo de energía\n\n"
                    "Marcas: NVIDIA RTX | AMD RX")
        else:
            return ("🎮 **Graphics Card (GPU)**\n\n"
                    "Graphics specialist, essential for gaming.\n"
                    "• VRAM: More = better for high resolution/textures\n"
                    "• Cores: Computing power\n"
                    "• Ray Tracing: Realistic lighting\n"
                    "• TDP: Power consumption\n\n"
                    "Brands: NVIDIA RTX | AMD RX")

    def _explain_ram(self, name: str) -> str:
        """Explain RAM"""
        if self.language == "es":
            return ("🧠 **Memoria RAM**\n\n"
                    "Almacenamiento temporal rápido. Más RAM = mejor multitarea.\n"
                    "• 8GB: Básico, navegación\n"
                    "• 16GB: Estándar gaming, trabajo\n"
                    "• 32GB+: Multitarea pesada, streaming, rendering\n"
                    "• DDR4 vs DDR5: DDR5 es más rápida (más cara)\n"
                    "• Velocidad (MHz): Más rápido = mejor rendimiento")
        else:
            return ("🧠 **RAM Memory**\n\n"
                    "Fast temporary storage. More RAM = better multitasking.\n"
                    "• 8GB: Basic, browsing\n"
                    "• 16GB: Standard gaming, work\n"
                    "• 32GB+: Heavy multitasking, streaming, rendering\n"
                    "• DDR4 vs DDR5: DDR5 is faster (more expensive)\n"
                    "• Speed (MHz): Faster = better performance")

    def _explain_psu(self) -> str:
        """Explain PSU"""
        if self.language == "es":
            return ("⚡ **Fuente de Poder (PSU)**\n\n"
                    "Suministra energía a todos los componentes.\n"
                    "• Wattage: Debe ser 20-30% mayor al uso total\n"
                    "• 80+ Certifications: Gold/Platinum = más eficiente\n"
                    "• Modular: Cables desconectables = mejor airflow\n"
                    "• Evita fuentes chinas baratas = riesgo de daño\n\n"
                    "Regla: Si tu PC consume 400W, usa PSU 500-550W mínimo")
        else:
            return ("⚡ **Power Supply Unit (PSU)**\n\n"
                    "Supplies power to all components.\n"
                    "• Wattage: Should be 20-30% above total usage\n"
                    "• 80+ Certifications: Gold/Platinum = more efficient\n"
                    "• Modular: Removable cables = better airflow\n"
                    "• Avoid cheap no-name PSUs = risk of damage\n\n"
                    "Rule: If your PC uses 400W, get 500-550W PSU minimum")

    def _explain_case(self) -> str:
        """Explain case"""
        if self.language == "es":
            return ("🏠 **Gabinete (Case)**\n\n"
                    "Aloja todos los componentes.\n"
                    "• ATX: Grande, muchos compartimentos\n"
                    "• Micro-ATX: Más pequeño\n"
                    "• Mini-ITX: Muy compacto\n"
                    "• Airflow: Importante para cooling\n"
                    "• Verificar compatibilidad: Largo GPU, altura cooler\n\n"
                    "Buenas marcas: NZXT, Corsair, Lian Li")
        else:
            return ("🏠 **Case (Chassis)**\n\n"
                    "Holds all components.\n"
                    "• ATX: Large, many compartments\n"
                    "• Micro-ATX: Smaller\n"
                    "• Mini-ITX: Very compact\n"
                    "• Airflow: Important for cooling\n"
                    "• Check compatibility: GPU length, cooler height\n\n"
                    "Good brands: NZXT, Corsair, Lian Li")

    def _explain_cooler(self) -> str:
        """Explain cooler"""
        if self.language == "es":
            return ("❄️ **Cooler (Enfriador)**\n\n"
                    "Mantiene CPU fría para evitar throttling.\n"
                    "• Air Cooler: Económico, funciona bien\n"
                    "• Liquid Cooler: Mejor performance, más caro\n"
                    "• TDP: Debe ser >= TDP del CPU\n"
                    "• Altura: Verificar que cabe en gabinete")
        else:
            return ("❄️ **CPU Cooler**\n\n"
                    "Keeps CPU cool to prevent throttling.\n"
                    "• Air Cooler: Economical, works well\n"
                    "• Liquid Cooler: Better performance, expensive\n"
                    "• TDP: Should be >= CPU TDP\n"
                    "• Height: Check it fits in case")

    def _explain_motherboard(self) -> str:
        """Explain motherboard"""
        if self.language == "es":
            return ("🔌 **Placa Madre (Motherboard)**\n\n"
                    "Conecta todos los componentes.\n"
                    "• Socket: CPU debe coincidir\n"
                    "• Chipset: Define soporte de características\n"
                    "• RAM Slots: Dónde va la memoria\n"
                    "• Forma: ATX, Micro-ATX, Mini-ITX")
        else:
            return ("🔌 **Motherboard**\n\n"
                    "Connects all components.\n"
                    "• Socket: CPU must match\n"
                    "• Chipset: Defines feature support\n"
                    "• RAM Slots: Where memory goes\n"
                    "• Form Factor: ATX, Micro-ATX, Mini-ITX")

    def _get_generic_explanation(self) -> str:
        """Generic explanation"""
        if self.language == "es":
            return "📖 Componente importante de tu PC. Consulta su manual para más detalles."
        else:
            return "📖 Important PC component. Check its manual for more details."

    def compare_cpus(self, cpu1_name: str, cpu2_name: str) -> str:
        """Compare two CPUs"""
        if self.language == "es":
            return f"📊 Comparación: {cpu1_name} vs {cpu2_name}\n\nAmbas son opciones sólidas. La diferencia es marginal en aplicaciones reales."
        else:
            return f"📊 Comparison: {cpu1_name} vs {cpu2_name}\n\nBoth are solid options. Difference is marginal in real applications."

    def compare_gpus(self, gpu1_name: str, gpu2_name: str) -> str:
        """Compare two GPUs"""
        if self.language == "es":
            return f"📊 Comparación: {gpu1_name} vs {gpu2_name}\n\nPara gaming, elige la que ofrezca mejor FPS en los juegos que juegas."
        else:
            return f"📊 Comparison: {gpu1_name} vs {gpu2_name}\n\nFor gaming, choose the one that offers better FPS in your games."

    def explain_compatibility_issue(self, issue: Dict) -> str:
        """Explain a compatibility issue in detail"""
        title = issue.get("title", "")
        description = issue.get("description", "")
        fix = issue.get("fix", "")

        return f"⚠️ **{title}**\n\n{description}\n\n✅ **Solución**: {fix}"
