"""
Portfolio Model

Representa un portafolio de inversión del usuario.

Principios aplicados:
- Single Responsibility: Solo estructura de datos del portafolio
- Rich Domain Model: Lógica de negocio en el modelo
"""

from sqlalchemy import Column, String, Text, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base, PKMixin, TimestampMixin


class Portfolio(Base, PKMixin, TimestampMixin):
    """
    Modelo de Portafolio de Inversión.
    
    Attributes:
        id: Identificador único
        name: Nombre del portafolio (ej: "Cubeta 1 - Largo Plazo")
        description: Descripción opcional
        is_active: Si el portafolio está activo
        target_voo_percent: Porcentaje objetivo para VOO
        target_vgt_percent: Porcentaje objetivo para VGT
        target_btc_percent: Porcentaje objetivo para BTC
        target_eth_percent: Porcentaje objetivo para ETH
        holdings: Relación con holdings
        transactions: Relación con transacciones
    """
    
    __tablename__ = "portfolios"
    
    # Información básica
    name = Column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
        doc="Nombre único del portafolio"
    )
    
    description = Column(
        Text,
        nullable=True,
        doc="Descripción opcional del portafolio"
    )
    
    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
        doc="Indica si el portafolio está activo"
    )
    
    # Distribución objetivo (%)
    target_voo_percent = Column(
        String(10),
        default="35.0",
        nullable=False,
        doc="Porcentaje objetivo para VOO"
    )
    
    target_vgt_percent = Column(
        String(10),
        default="35.0",
        nullable=False,
        doc="Porcentaje objetivo para VGT"
    )
    
    target_btc_percent = Column(
        String(10),
        default="15.0",
        nullable=False,
        doc="Porcentaje objetivo para BTC"
    )
    
    target_eth_percent = Column(
        String(10),
        default="15.0",
        nullable=False,
        doc="Porcentaje objetivo para ETH"
    )
    
    # Relaciones
    holdings = relationship(
        "Holding",
        back_populates="portfolio",
        cascade="all, delete-orphan",
        doc="Holdings (posiciones) en este portafolio"
    )
    
    transactions = relationship(
        "Transaction",
        back_populates="portfolio",
        cascade="all, delete-orphan",
        order_by="Transaction.transaction_date.desc()",
        doc="Transacciones de este portafolio"
    )
    
    def __repr__(self) -> str:
        return f"<Portfolio(id={self.id}, name='{self.name}', active={self.is_active})>"
    
    @property
    def target_distribution(self) -> dict[str, float]:
        """
        Retorna la distribución objetivo como diccionario.
        
        Returns:
            Dict con tickers y sus porcentajes objetivo
        """
        return {
            "VOO": float(self.target_voo_percent),
            "VGT": float(self.target_vgt_percent),
            "BTC": float(self.target_btc_percent),
            "ETH": float(self.target_eth_percent),
        }
