"""
Database Base Models

Define clase base y mixins comunes para todos los modelos.

Principios aplicados:
- DRY: Funcionalidad común en base class
- Single Responsibility: Cada mixin una responsabilidad
"""

from datetime import datetime
from typing import Any
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    """
    Clase base para todos los modelos SQLAlchemy.
    
    Proporciona funcionalidad común y convenciones.
    """
    
    # Generación automática de nombres de tabla
    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        Genera nombre de tabla automáticamente desde nombre de clase.
        
        Ejemplo:
            PortfolioModel -> portfolio_model
        """
        return cls.__name__.lower()
    
    def to_dict(self) -> dict[str, Any]:
        """
        Convierte modelo a diccionario.
        
        Útil para serialización y debugging.
        """
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }


class TimestampMixin:
    """
    Mixin para timestamps automáticos.
    
    Agrega created_at y updated_at a cualquier modelo.
    """
    
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        doc="Timestamp de creación del registro"
    )
    
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        doc="Timestamp de última actualización"
    )


class PKMixin:
    """
    Mixin para primary key auto-incremental.
    
    Convención estándar: id como PK.
    """
    
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
        doc="Primary key único del registro"
    )
