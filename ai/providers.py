"""
AI Provider abstraction layer.
Allows switching between offline mode, OpenAI, OpenRouter, and Groq.
Default: Offline (no API key needed).
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict
import os


class AIProvider(ABC):
    """Abstract base class for AI providers"""

    def __init__(self, language: str = "es"):
        self.language = language

    @abstractmethod
    def query(self, messages: List[Dict[str, str]]) -> str:
        """Query the AI provider with a list of messages"""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is available/configured"""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Get provider name"""
        pass


class OfflineProvider(AIProvider):
    """Offline provider using ResponseGenerator - DEFAULT"""

    def __init__(self, language: str = "es"):
        super().__init__(language)
        from core.responses import ResponseGenerator
        self.generator = ResponseGenerator(language)
        self.name = "offline"

    def query(self, messages: List[Dict[str, str]]) -> str:
        """Get response using offline logic"""
        # Extract last user message
        user_message = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                user_message = msg.get("content", "")
                break

        return self.generator.answer_question(user_message)

    def is_available(self) -> bool:
        """Always available"""
        return True

    def get_name(self) -> str:
        return "offline"


class OpenAIProvider(AIProvider):
    """OpenAI provider - requires OPENAI_API_KEY"""

    def __init__(self, language: str = "es"):
        super().__init__(language)
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        self.name = "openai"
        self.client = None

        if self.api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
            except ImportError:
                pass

    def query(self, messages: List[Dict[str, str]]) -> str:
        """Query OpenAI API"""
        if not self.is_available():
            return "OpenAI provider not available"

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=256,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error querying OpenAI: {str(e)}"

    def is_available(self) -> bool:
        """Check if OpenAI is properly configured"""
        return bool(self.api_key and self.client is not None)

    def get_name(self) -> str:
        return "openai"


class OpenRouterProvider(AIProvider):
    """OpenRouter provider - requires OPENROUTER_API_KEY"""

    def __init__(self, language: str = "es"):
        super().__init__(language)
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-2-7b-chat")
        self.name = "openrouter"

    def query(self, messages: List[Dict[str, str]]) -> str:
        """Query OpenRouter API"""
        if not self.is_available():
            return "OpenRouter provider not available"

        try:
            import requests

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "HTTP-Referer": "https://github.com/pcbuildr/pcbuildr",
            }

            payload = {
                "model": self.model,
                "messages": messages,
            }

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                return data.get("choices", [{}])[0].get("message", {}).get("content", "")
            else:
                return f"OpenRouter error: {response.status_code}"

        except Exception as e:
            return f"Error querying OpenRouter: {str(e)}"

    def is_available(self) -> bool:
        """Check if OpenRouter is properly configured"""
        return bool(self.api_key)

    def get_name(self) -> str:
        return "openrouter"


class GroqProvider(AIProvider):
    """Groq provider - requires GROQ_API_KEY"""

    def __init__(self, language: str = "es"):
        super().__init__(language)
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")
        self.name = "groq"
        self.client = None

        if self.api_key:
            try:
                from groq import Groq
                self.client = Groq(api_key=self.api_key)
            except ImportError:
                pass

    def query(self, messages: List[Dict[str, str]]) -> str:
        """Query Groq API"""
        if not self.is_available():
            return "Groq provider not available"

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=256,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error querying Groq: {str(e)}"

    def is_available(self) -> bool:
        """Check if Groq is properly configured"""
        return bool(self.api_key and self.client is not None)

    def get_name(self) -> str:
        return "groq"


class AIProviderFactory:
    """Factory for creating AI providers with automatic fallback"""

    def __init__(self, language: str = "es"):
        self.language = language

    def get_provider(self) -> AIProvider:
        """
        Get the appropriate AI provider.
        Falls back to offline if configured provider is unavailable.
        """
        from config import Config

        requested_provider = Config.get_effective_ai_provider().lower()

        providers = {
            "openai": OpenAIProvider(self.language),
            "openrouter": OpenRouterProvider(self.language),
            "groq": GroqProvider(self.language),
            "offline": OfflineProvider(self.language),
        }

        # Try requested provider first
        if requested_provider in providers:
            provider = providers[requested_provider]
            if provider.is_available():
                print(f"[INFO] Using {provider.get_name()} AI provider")
                return provider

        # Fallback to offline
        print("[INFO] No configured AI provider available, using offline mode")
        return providers["offline"]

    def get_all_providers(self) -> Dict[str, AIProvider]:
        """Get all available providers"""
        return {
            "openai": OpenAIProvider(self.language),
            "openrouter": OpenRouterProvider(self.language),
            "groq": GroqProvider(self.language),
            "offline": OfflineProvider(self.language),
        }


class AIProviderManager:
    """Manages AI provider with transparent fallback"""

    def __init__(self, language: str = "es"):
        self.language = language
        self.factory = AIProviderFactory(language)
        self.primary_provider = self.factory.get_provider()
        self.offline_provider = OfflineProvider(language)

    def query(self, messages: List[Dict[str, str]], fallback_to_offline: bool = True) -> str:
        """
        Query AI with automatic fallback.

        If primary provider fails and fallback_to_offline is True,
        silently switches to offline mode.
        """
        try:
            result = self.primary_provider.query(messages)

            # Check if result looks like an error
            if not result or "error" in result.lower():
                if fallback_to_offline:
                    return self.offline_provider.query(messages)
                return result

            return result

        except Exception as e:
            if fallback_to_offline:
                # Silently fallback
                return self.offline_provider.query(messages)
            raise

    def switch_provider(self, provider_name: str) -> bool:
        """Switch to a different provider"""
        providers = self.factory.get_all_providers()
        if provider_name in providers:
            self.primary_provider = providers[provider_name]
            return self.primary_provider.is_available()
        return False

    def get_current_provider(self) -> str:
        """Get name of current provider"""
        return self.primary_provider.get_name()

    def list_available_providers(self) -> List[str]:
        """List all available (configured) providers"""
        available = []
        providers = self.factory.get_all_providers()
        for name, provider in providers.items():
            if provider.is_available():
                available.append(name)
        return available
