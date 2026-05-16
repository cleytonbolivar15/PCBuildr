"""
Offline response generation for Bytecoon assistant.
Provides intelligent-sounding responses using predefined templates, context matching,
and heuristic logic instead of requiring a local LLM.
"""

import re
from typing import Dict, List, Optional, Tuple


class ResponseGenerator:
    """Generates intelligent responses without requiring an AI model"""

    def __init__(self, language: str = "es"):
        self.language = language
        self.known_hardware = {}
        self._load_hardware_knowledge()

    def _load_hardware_knowledge(self):
        """Load basic hardware knowledge"""
        self.known_hardware = {
            "cpu": ["Intel Core i3", "Intel Core i5", "Intel Core i7", "Intel Core i9",
                    "AMD Ryzen 3", "AMD Ryzen 5", "AMD Ryzen 7", "AMD Ryzen 9"],
            "gpu": ["NVIDIA RTX 4090", "NVIDIA RTX 4080", "NVIDIA RTX 4070", "NVIDIA RTX 4060",
                    "AMD RX 7900 XTX", "AMD RX 7900 XT", "AMD RX 6700 XT"],
            "ram": ["DDR4", "DDR5", "16GB", "32GB", "64GB"],
            "psu": ["650W", "750W", "850W", "1000W"],
            "case": ["ATX", "Micro-ATX", "Mini-ITX", "E-ATX"],
            "motherboard": ["Socket 1700", "Socket AM5", "Socket AM4", "LGA1151"]
        }

    def answer_question(self, question: str, context: Optional[Dict] = None) -> str:
        """
        Answer a hardware question using intelligent heuristics.

        Args:
            question: User's question
            context: Optional context about current build

        Returns:
            Intelligent response
        """
        question_lower = question.lower()

        # Detect question type
        if self._is_recommendation_question(question_lower):
            return self._get_recommendation_response(question, context)
        elif self._is_compatibility_question(question_lower):
            return self._get_compatibility_response(question, context)
        elif self._is_performance_question(question_lower):
            return self._get_performance_response(question, context)
        elif self._is_specification_question(question_lower):
            return self._get_specification_response(question, context)
        else:
            return self._get_general_response(question)

    def _is_recommendation_question(self, question: str) -> bool:
        """Detect if question is asking for recommendations"""
        keywords = ["recomienda", "recommend", "cuál", "which", "mejor", "best",
                    "bueno", "good", "comprar", "buy", "elegir", "choose"]
        return any(kw in question for kw in keywords)

    def _is_compatibility_question(self, question: str) -> bool:
        """Detect if question is about compatibility"""
        keywords = ["compatible", "compatibil", "funciona", "work", "encaja", "fit",
                    "socket", "voltaje", "voltage", "conector", "connector"]
        return any(kw in question for kw in keywords)

    def _is_performance_question(self, question: str) -> bool:
        """Detect if question is about performance"""
        keywords = ["rendimiento", "performance", "fps", "velocidad", "speed",
                    "rápido", "fast", "lento", "slow", "potencia", "power",
                    "bottleneck", "cuello"]
        return any(kw in question for kw in keywords)

    def _is_specification_question(self, question: str) -> bool:
        """Detect if question is asking for specs"""
        keywords = ["especificaciones", "specifications", "specs", "especificacion",
                    "tdp", "socket", "cores", "velocidad", "memory", "memoria"]
        return any(kw in question for kw in keywords)

    def _get_recommendation_response(self, question: str, context: Optional[Dict] = None) -> str:
        """Generate recommendation response"""
        budget = self._extract_budget(question)
        use_case = self._extract_use_case(question)

        if self.language == "es":
            intro = "✨ Basándome en tus criterios, te recomiendo:\n\n"
            outro = "\n\n💡 Pro tip: Estos componentes tienen excelente relación precio-rendimiento."
        else:
            intro = "✨ Based on your criteria, I recommend:\n\n"
            outro = "\n\n💡 Pro tip: These components offer excellent value for money."

        if use_case == "gaming":
            if self.language == "es":
                components = "• CPU: Intel Core i5-13600K o AMD Ryzen 7 5700X\n"
                components += "• GPU: NVIDIA RTX 4070 o mejor\n"
                components += "• Memoria: 32GB DDR4/DDR5\n"
                components += "• Tipo: PC Gaming de Alta Gama"
            else:
                components = "• CPU: Intel Core i5-13600K or AMD Ryzen 7 5700X\n"
                components += "• GPU: NVIDIA RTX 4070 or better\n"
                components += "• Memory: 32GB DDR4/DDR5\n"
                components += "• Type: High-End Gaming PC"
        elif use_case == "workstation":
            if self.language == "es":
                components = "• CPU: AMD Ryzen 9 5950X o Intel Core i9-13900K\n"
                components += "• GPU: NVIDIA RTX 4090 o RTX 6000\n"
                components += "• Memoria: 64GB DDR5\n"
                components += "• Tipo: Estación de Trabajo Profesional"
            else:
                components = "• CPU: AMD Ryzen 9 5950X or Intel Core i9-13900K\n"
                components += "• GPU: NVIDIA RTX 4090 or RTX 6000\n"
                components += "• Memory: 64GB DDR5\n"
                components += "• Type: Professional Workstation"
        else:
            if self.language == "es":
                components = "• CPU: Intel Core i3 o AMD Ryzen 5\n"
                components += "• GPU: Integrada o GTX 1650\n"
                components += "• Memoria: 16GB DDR4\n"
                components += "• Tipo: PC Oficina/Estudio"
            else:
                components = "• CPU: Intel Core i3 or AMD Ryzen 5\n"
                components += "• GPU: Integrated or GTX 1650\n"
                components += "• Memory: 16GB DDR4\n"
                components += "• Type: Office/Study PC"

        return intro + components + outro

    def _get_compatibility_response(self, question: str, context: Optional[Dict] = None) -> str:
        """Generate compatibility response"""
        if self.language == "es":
            return ("✅ Para verificar compatibilidad:\n\n"
                    "1. Verifica que CPU y Motherboard comparten el mismo socket\n"
                    "2. La RAM debe ser del tipo DDR4 o DDR5 según la placa\n"
                    "3. La GPU debe caber físicamente en el gabinete\n"
                    "4. La fuente debe tener al menos 20% más de potencia que el consumo total\n\n"
                    "📊 PCBuildr verifica automáticamente esto en tu build.")
        else:
            return ("✅ To verify compatibility:\n\n"
                    "1. Ensure CPU and Motherboard share the same socket\n"
                    "2. RAM must be DDR4 or DDR5 according to the motherboard\n"
                    "3. GPU must physically fit in the case\n"
                    "4. PSU must be at least 20% above total power consumption\n\n"
                    "📊 PCBuildr automatically checks this in your build.")

    def _get_performance_response(self, question: str, context: Optional[Dict] = None) -> str:
        """Generate performance response"""
        if self.language == "es":
            return ("⚡ Rendimiento de tu PC:\n\n"
                    "El rendimiento depende de:\n"
                    "• Procesador (CPU): Velocidad en juegos\n"
                    "• Tarjeta gráfica (GPU): FPS en videojuegos, rendering\n"
                    "• Memoria (RAM): Multitarea, carga de programas\n"
                    "• Almacenamiento: Velocidad de carga (SSD vs HDD)\n\n"
                    "💪 Cuello de botella (Bottleneck): Si una componente es mucho más lenta que otras, limita el rendimiento general.")
        else:
            return ("⚡ Your PC's performance depends on:\n\n"
                    "• Processor (CPU): Gaming speed\n"
                    "• Graphics card (GPU): FPS in games, rendering\n"
                    "• Memory (RAM): Multitasking, app loading\n"
                    "• Storage: Load times (SSD vs HDD)\n\n"
                    "💪 Bottleneck: If one component is much slower than others, it limits overall performance.")

    def _get_specification_response(self, question: str, context: Optional[Dict] = None) -> str:
        """Generate specification response"""
        hardware_type = self._detect_hardware_type(question)

        if hardware_type == "cpu":
            if self.language == "es":
                return ("📋 Especificaciones importantes de CPU:\n\n"
                        "• Cores (Núcleos): Más cores = mejor multitarea\n"
                        "• Threads: Más threads = mejor rendimiento paralelo\n"
                        "• Socket: Determina compatibilidad con placa madre\n"
                        "• TDP: Potencia térmica disipada (watts)\n"
                        "• Frecuencia (GHz): Más GHz = más velocidad pura")
            else:
                return ("📋 Important CPU specifications:\n\n"
                        "• Cores: More cores = better multitasking\n"
                        "• Threads: More threads = better parallel performance\n"
                        "• Socket: Determines motherboard compatibility\n"
                        "• TDP: Thermal Design Power (watts)\n"
                        "• Frequency (GHz): More GHz = faster speed")
        elif hardware_type == "gpu":
            if self.language == "es":
                return ("📋 Especificaciones importantes de GPU:\n\n"
                        "• VRAM: Más memoria = mejores gráficos/resoluciones\n"
                        "• CORTEX/CUDA/Streaming Cores: Potencia de cálculo\n"
                        "• Bus de memoria: Ancho influye en velocidad\n"
                        "• TDP: Potencia requerida\n"
                        "• Ray Tracing: Iluminación realista")
            else:
                return ("📋 Important GPU specifications:\n\n"
                        "• VRAM: More memory = better graphics/resolutions\n"
                        "• Cores: Computing power\n"
                        "• Memory Bus: Width affects speed\n"
                        "• TDP: Required power\n"
                        "• Ray Tracing: Realistic lighting")
        else:
            if self.language == "es":
                return "📋 ¿De qué componente quieres conocer especificaciones? CPU, GPU, RAM, Fuente, Placa madre, Almacenamiento..."
            else:
                return "📋 Which component would you like to know specs for? CPU, GPU, RAM, PSU, Motherboard, Storage..."

    def _get_general_response(self, question: str) -> str:
        """Generate general response"""
        if self.language == "es":
            responses = [
                "🦝 Soy Bytecoon, tu asistente en PCBuildr. ¿Tienes preguntas sobre armar tu PC?",
                "💡 Te puedo ayudar con recomendaciones de componentes, verificar compatibilidad, o explicar especificaciones.",
                "🎮 ¿Quieres armar un PC para gaming? ¿Trabajo profesional? ¿Oficina? Dime tu presupuesto y uso.",
                "🔧 Puedo verificar si tus componentes seleccionados son compatibles entre sí.",
            ]
        else:
            responses = [
                "🦝 I'm Bytecoon, your PCBuildr assistant. Got questions about building your PC?",
                "💡 I can help with component recommendations, verify compatibility, or explain specs.",
                "🎮 Want to build a gaming PC? Professional workstation? Office machine? Tell me your budget and use case.",
                "🔧 I can verify if your selected components are compatible with each other.",
            ]

        import random
        return random.choice(responses)

    def _extract_budget(self, question: str) -> int:
        """Extract budget from question"""
        # Look for budget patterns like "1000", "$1000", "1000 dólares", etc.
        numbers = re.findall(r'\d+', question)
        if numbers:
            return int(numbers[-1])
        return 1000

    def _extract_use_case(self, question: str) -> str:
        """Extract use case from question"""
        question_lower = question.lower()
        if any(w in question_lower for w in ["juego", "gaming", "game", "gamer"]):
            return "gaming"
        elif any(w in question_lower for w in ["trabajo", "trabajo", "profesional", "render", "video"]):
            return "workstation"
        elif any(w in question_lower for w in ["oficina", "office", "mail", "web", "browsing"]):
            return "office"
        return "general"

    def _detect_hardware_type(self, question: str) -> str:
        """Detect what hardware type is being asked about"""
        question_lower = question.lower()
        if any(w in question_lower for w in ["procesador", "cpu", "intel", "ryzen", "core i"]):
            return "cpu"
        elif any(w in question_lower for w in ["gpu", "gráfica", "nvidia", "rtx", "radeon"]):
            return "gpu"
        elif any(w in question_lower for w in ["ram", "memoria", "ddr4", "ddr5"]):
            return "ram"
        elif any(w in question_lower for w in ["fuente", "psu", "watt", "watts"]):
            return "psu"
        elif any(w in question_lower for w in ["placa", "motherboard", "socket"]):
            return "motherboard"
        return "unknown"

    def format_component_info(self, component: Dict) -> str:
        """Format component information in natural language"""
        name = component.get("nombre", "Unknown")
        price = component.get("precio", 0)
        store = component.get("tienda", "Unknown")

        if self.language == "es":
            return f"💼 {name}\n→ Precio: ${price} en {store}"
        else:
            return f"💼 {name}\n→ Price: ${price} at {store}"

    def get_conversational_response(self, user_message: str = "") -> str:
        """Get a casual conversational response from Bytecoon"""
        if self.language == "es":
            responses = {
                "hola": "¡Hola! 🦝 Soy Bytecoon. ¿En qué puedo ayudarte con tu PC?",
                "gracias": "¡De nada! Estoy aquí para ayudarte. ¿Algo más? 😊",
                "adiós": "¡Hasta luego! Que disfrutes construyendo tu PC. 🚀",
                "chao": "¡Nos vemos! 🦝",
            }
        else:
            responses = {
                "hello": "Hi! 🦝 I'm Bytecoon. How can I help you build your PC?",
                "hi": "Hi! 🦝 I'm Bytecoon. How can I help you build your PC?",
                "thanks": "You're welcome! I'm here to help. Anything else? 😊",
                "goodbye": "Goodbye! Enjoy building your PC. 🚀",
                "bye": "See you! 🦝",
            }

        user_lower = user_message.lower().strip()

        for greeting, response in responses.items():
            if greeting in user_lower:
                return response

        return self.answer_question(user_message)
