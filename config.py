"""
PCBuildr Configuration Management
Centralizes all configuration from environment variables with sensible defaults.
"""

import os
from pathlib import Path
from typing import Optional

class Config:
    """Configuration management for PCBuildr"""

    # Backend settings
    BACKEND_HOST: str = os.getenv("BACKEND_HOST", "127.0.0.1")
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", "8000"))
    BACKEND_URL: str = os.getenv(
        "BACKEND_URL",
        f"http://{BACKEND_HOST}:{BACKEND_PORT}"
    )

    # AI Provider settings
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "offline")  # offline, openai, openrouter, groq
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    OPENROUTER_API_KEY: Optional[str] = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-2-7b-chat")
    GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")

    # Database settings
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "./pcbuildr.db")
    USER_DATA_DIR: str = os.getenv("USER_DATA_DIR", "./userdata")

    # UI settings
    DEFAULT_LANGUAGE: str = os.getenv("DEFAULT_LANGUAGE", "es")
    DEFAULT_THEME: str = os.getenv("DEFAULT_THEME", "dark")  # dark, light

    # Debug/Development
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # Data paths (relative to project root)
    @classmethod
    def get_data_dir(cls) -> Path:
        """Get the data directory path for seed/reference data"""
        return Path(__file__).parent / "data"

    @classmethod
    def get_core_dir(cls) -> Path:
        """Get the core (AI) modules directory"""
        return Path(__file__).parent / "core"

    @classmethod
    def get_ai_dir(cls) -> Path:
        """Get the AI provider directory"""
        return Path(__file__).parent / "ai"

    @classmethod
    def get_frontend_dir(cls) -> Path:
        """Get the frontend directory"""
        return Path(__file__).parent / "Frontend"

    @classmethod
    def get_backend_dir(cls) -> Path:
        """Get the backend directory"""
        return Path(__file__).parent / "Backend"

    @classmethod
    def get_user_data_dir(cls) -> Path:
        """Get the user data directory, creating it if needed"""
        user_dir = Path(cls.USER_DATA_DIR)
        user_dir.mkdir(parents=True, exist_ok=True)
        return user_dir

    @classmethod
    def get_database_path(cls) -> Path:
        """Get the database path"""
        db_path = Path(cls.DATABASE_PATH)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        return db_path

    @classmethod
    def validate_ai_provider(cls) -> bool:
        """Validate that selected AI provider has necessary configuration"""
        provider = cls.AI_PROVIDER.lower()

        if provider == "offline":
            return True
        elif provider == "openai":
            return bool(cls.OPENAI_API_KEY)
        elif provider == "openrouter":
            return bool(cls.OPENROUTER_API_KEY)
        elif provider == "groq":
            return bool(cls.GROQ_API_KEY)

        return False

    @classmethod
    def get_effective_ai_provider(cls) -> str:
        """Get effective AI provider, falling back to offline if validation fails"""
        if cls.validate_ai_provider():
            return cls.AI_PROVIDER.lower()
        return "offline"
