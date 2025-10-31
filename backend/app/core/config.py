"""
Core Configuration Module

Implementa el patrón Singleton para configuración centralizada.
Usa Pydantic Settings para validación de tipos y variables de entorno.

Principios aplicados:
- Single Responsibility: Solo manejo de configuración
- Dependency Inversion: Configuración como abstracción
"""

from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    """
    Configuración global de la aplicación.
    
    Valida y carga variables de entorno con type safety.
    """
    
    # Application
    APP_NAME: str = "Portfolio Tracker"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./portfolio_tracker.db"
    
    # Price Updates
    PRICE_UPDATE_INTERVAL_MINUTES: int = 60
    ENABLE_AUTO_PRICE_UPDATES: bool = True
    
    # External APIs
    COINGECKO_API_URL: str = "https://api.coingecko.com/api/v3"
    COINGECKO_API_KEY: str | None = None
    EXCHANGE_RATE_API_URL: str = "https://api.exchangerate-api.com/v4/latest"
    EXCHANGE_RATE_API_KEY: str | None = None
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
        """
        Valida y normaliza CORS origins.
        Permite string JSON o lista Python.
        """
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        raise ValueError(v)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Singleton instance
settings = Settings()


def get_settings() -> Settings:
    """
    Dependency injection helper.
    
    Permite mockear configuración en tests.
    """
    return settings
