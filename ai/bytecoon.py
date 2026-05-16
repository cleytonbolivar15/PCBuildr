"""
Bytecoon - The PCBuildr AI Assistant
Intelligent assistant for PC building using composable AI modules.
"""

from typing import List, Dict, Optional
from ai.providers import AIProviderManager
from core.responses import ResponseGenerator
from core.compatibility import CompatibilityChecker
from core.recommender import RecommendationEngine
from core.explainer import HardwareExplainer
from core.scoring import BuildScorer


class Bytecoon:
    """
    PCBuildr's intelligent assistant.
    Combines multiple AI modules for comprehensive PC building support.
    """

    def __init__(self, language: str = "es"):
        self.language = language
        self.name = "Bytecoon 🦝"
        self.version = "0.1.0-beta"

        # Initialize modules
        self.ai_manager = AIProviderManager(language)
        self.response_gen = ResponseGenerator(language)
        self.compatibility = CompatibilityChecker(language)
        self.recommender = RecommendationEngine(language)
        self.explainer = HardwareExplainer(language)
        self.scorer = BuildScorer(language)

        # Conversation history
        self.history: List[Dict[str, str]] = []
        self._add_system_message()

    def _add_system_message(self):
        """Add system context"""
        if self.language == "es":
            system_prompt = (
                "Eres Bytecoon, un asistente experto en montaje de computadoras. "
                "Tu rol es ayudar a los usuarios a:\n"
                "- Seleccionar componentes de hardware\n"
                "- Verificar compatibilidad\n"
                "- Entender especificaciones técnicas\n"
                "- Obtener recomendaciones según presupuesto y uso\n"
                "Sé amable, conciso y siempre brinda soluciones prácticas. "
                "Eres el mapache tecnológico que entiende de PCs. 🦝"
            )
        else:
            system_prompt = (
                "You are Bytecoon, an expert PC building assistant. "
                "Your role is to help users:\n"
                "- Select hardware components\n"
                "- Verify compatibility\n"
                "- Understand technical specifications\n"
                "- Get recommendations based on budget and use case\n"
                "Be friendly, concise, and always provide practical solutions. "
                "You're the tech-savvy raccoon who knows PC building. 🦝"
            )

        self.history.append({"role": "system", "content": system_prompt})

    def ask(self, question: str) -> str:
        """
        Ask Bytecoon a question.

        Args:
            question: User's question

        Returns:
            Intelligent response
        """
        # Add user message to history
        self.history.append({"role": "user", "content": question})

        # Get response from AI
        response = self.ai_manager.query(self.history)

        # Add assistant response to history
        self.history.append({"role": "assistant", "content": response})

        return response

    def get_recommendation(self, budget: int, use_case: str) -> Dict:
        """Get a PC build recommendation"""
        return self.recommender.recommend_build(budget, use_case)

    def check_compatibility(self, build: Dict) -> List[Dict]:
        """Check build compatibility"""
        return self.compatibility.check_build(build)

    def score_build(self, build: Dict) -> Dict:
        """Score a build"""
        return self.scorer.score_build(build)

    def explain_component(self, component_name: str, component_type: str) -> str:
        """Explain a component"""
        return self.explainer.explain_component(component_name, component_type)

    def suggest_alternative(self, component: Dict) -> Optional[Dict]:
        """Suggest alternative component"""
        return self.recommender.suggest_alternative(component, "user request")

    def get_action_suggestion(self, build: Dict) -> str:
        """Get proactive suggestion based on current build"""
        issues = self.check_compatibility(build)

        if issues:
            if self.language == "es":
                return f"⚠️ Detecté {len(issues)} problemas en tu build. Haz clic para ver detalles."
            else:
                return f"⚠️ I detected {len(issues)} issues in your build. Click to see details."

        score = self.score_build(build)
        rating = score.get("rating", "")

        if self.language == "es":
            return f"✨ Tu build actual se ve bien: {rating}"
        else:
            return f"✨ Your current build looks good: {rating}"

    def clear_history(self):
        """Clear conversation history (but keep system prompt)"""
        system_msg = self.history[0] if self.history else None
        self.history = []
        if system_msg:
            self.history.append(system_msg)

    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        return self.history[1:]  # Exclude system message

    def get_personality(self) -> str:
        """Get Bytecoon's personality description"""
        if self.language == "es":
            return (
                f"🦝 **{self.name}** v{self.version}\n\n"
                "Soy tu asistente inteligente para armar computadoras de escritorio.\n\n"
                "Puedo ayudarte con:\n"
                "✅ Recomendaciones de componentes\n"
                "✅ Verificación de compatibilidad\n"
                "✅ Explicaciones técnicas\n"
                "✅ Comparación de hardware\n"
                "✅ Detección de cuellos de botella\n\n"
                "Cuéntame tu presupuesto y para qué usarás tu PC, ¡y te ayudaré a crear la máquina perfecta!"
            )
        else:
            return (
                f"🦝 **{self.name}** v{self.version}\n\n"
                "I'm your intelligent PC building assistant.\n\n"
                "I can help you with:\n"
                "✅ Component recommendations\n"
                "✅ Compatibility verification\n"
                "✅ Technical explanations\n"
                "✅ Hardware comparisons\n"
                "✅ Bottleneck detection\n\n"
                "Tell me your budget and use case, and I'll help you build the perfect machine!"
            )

    def switch_language(self, language: str):
        """Switch assistant language"""
        if language in ["es", "en"]:
            self.language = language
            # Reinitialize modules with new language
            self.response_gen = ResponseGenerator(language)
            self.compatibility = CompatibilityChecker(language)
            self.recommender = RecommendationEngine(language)
            self.explainer = HardwareExplainer(language)
            self.scorer = BuildScorer(language)
            self.ai_manager = AIProviderManager(language)
            self.clear_history()
            self._add_system_message()

    def get_info(self) -> str:
        """Get Bytecoon info"""
        provider = self.ai_manager.get_current_provider()
        available = self.ai_manager.list_available_providers()

        if self.language == "es":
            return (
                f"Información de Bytecoon:\n"
                f"Versión: {self.version}\n"
                f"Proveedor actual: {provider}\n"
                f"Proveedores disponibles: {', '.join(available)}\n"
                f"Idioma: {'Español' if self.language == 'es' else 'English'}"
            )
        else:
            return (
                f"Bytecoon Information:\n"
                f"Version: {self.version}\n"
                f"Current Provider: {provider}\n"
                f"Available Providers: {', '.join(available)}\n"
                f"Language: {'Spanish' if self.language == 'es' else 'English'}"
            )
