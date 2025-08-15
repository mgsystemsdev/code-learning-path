import os
from pathlib import Path
from typing import Optional


class Config:
    """Centralized configuration management."""
    
    # Application paths
    ROOT_DIR = Path(__file__).parent
    DATA_DIR = ROOT_DIR / "data"
    HISTORY_DIR = DATA_DIR / "history"
    AGENTS_DIR = DATA_DIR / "agents"
    
    # Ollama configuration
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen2.5:7b-instruct")
    OLLAMA_TIMEOUT: int = int(os.getenv("OLLAMA_TIMEOUT", "120"))
    
    # UI configuration
    WINDOW_WIDTH: int = int(os.getenv("WINDOW_WIDTH", "1280"))
    WINDOW_HEIGHT: int = int(os.getenv("WINDOW_HEIGHT", "760"))
    
    # Logging configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: Optional[str] = os.getenv("LOG_FILE")
    
    # Chat configuration
    MAX_HISTORY_LENGTH: int = int(os.getenv("MAX_HISTORY_LENGTH", "200"))
    DEFAULT_ROLE: str = os.getenv("DEFAULT_ROLE", "Engineer")
    
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist."""
        cls.HISTORY_DIR.mkdir(parents=True, exist_ok=True)
        cls.AGENTS_DIR.mkdir(parents=True, exist_ok=True)


# Global config instance
config = Config()
