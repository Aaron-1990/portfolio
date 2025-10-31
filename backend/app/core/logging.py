"""
Logging Configuration Module

Implementa logging estructurado con JSON para producción.
Facilita debugging y monitoreo en entornos profesionales.

Principios aplicados:
- Single Responsibility: Solo configuración de logging
- Open/Closed: Extensible con nuevos handlers
"""

import logging
import sys
from pathlib import Path
from pythonjsonlogger import jsonlogger

from app.core.config import settings


def setup_logging() -> logging.Logger:
    """
    Configura logging estructurado para la aplicación.
    
    Características:
    - JSON format para producción (fácil parsing)
    - Console output para desarrollo
    - File rotation automático
    - Context propagation
    
    Returns:
        Logger configurado y listo para usar
    """
    
    # Crear directorio de logs si no existe
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configurar logger raíz
    logger = logging.getLogger("portfolio_tracker")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Limpiar handlers existentes
    logger.handlers.clear()
    
    # Handler para consola (desarrollo)
    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
    
    # Handler para archivo (producción - JSON format)
    file_handler = logging.FileHandler(settings.LOG_FILE)
    json_formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(json_formatter)
    file_handler.setLevel(logging.INFO)
    
    # Agregar handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    # Prevenir propagación duplicada
    logger.propagate = False
    
    # Log inicial
    logger.info(
        "Logging initialized",
        extra={
            "environment": settings.ENVIRONMENT,
            "log_level": settings.LOG_LEVEL,
            "debug": settings.DEBUG
        }
    )
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Obtiene logger específico para módulo.
    
    Args:
        name: Nombre del módulo (usualmente __name__)
    
    Returns:
        Logger configurado para el módulo
    
    Ejemplo:
        logger = get_logger(__name__)
        logger.info("Processing portfolio", extra={"portfolio_id": 123})
    """
    return logging.getLogger(f"portfolio_tracker.{name}")


# Logger principal de la aplicación
logger = setup_logging()
