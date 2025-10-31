"""
Price Model

Almacena historial de precios de todos los activos.

Principios aplicados:
- Single Responsibility: Solo estructura de precios históricos
- Time Series Optimization: Índices optimizados para queries temporales
"""

from decimal import Decimal
from datetime import datetime
from sqlalchemy import Column, String, Numeric, DateTime, Index, UniqueConstraint
from sqlalchemy.sql import func

from app.db.base import Base, PKMixin


class Price(Base, PKMixin):
    """
    Modelo de Precio Histórico.
    
    Almacena snapshots de precios para análisis temporal.
    Optimizado para time-series queries.
    
    Attributes:
        id: Identificador único
        ticker: Symbol del activo
        price_usd: Precio en USD
        price_mxn: Precio en MXN
        exchange_rate: Tipo de cambio USD/MXN usado
        volume_24h: Volumen de trading 24h
        market_cap: Market cap (solo crypto)
        source: Fuente del precio (yahoo, coingecko)
        timestamp: Momento del precio
    """
    
    __tablename__ = "prices"
    
    # Información del activo
    ticker = Column(
        String(20),
        nullable=False,
        index=True,
        doc="Symbol del activo"
    )
    
    # Precios
    price_usd = Column(
        Numeric(precision=20, scale=2),
        nullable=False,
        doc="Precio en USD"
    )
    
    price_mxn = Column(
        Numeric(precision=20, scale=2),
        nullable=True,
        doc="Precio en MXN"
    )
    
    exchange_rate = Column(
        Numeric(precision=10, scale=4),
        nullable=True,
        doc="Tipo de cambio USD/MXN"
    )
    
    # Metadata adicional
    volume_24h = Column(
        Numeric(precision=30, scale=2),
        nullable=True,
        doc="Volumen de trading 24h"
    )
    
    market_cap = Column(
        Numeric(precision=30, scale=2),
        nullable=True,
        doc="Market capitalization (crypto)"
    )
    
    source = Column(
        String(50),
        nullable=False,
        doc="Fuente del precio (yahoo, coingecko)"
    )
    
    # Timestamp
    timestamp = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True,
        server_default=func.now(),
        doc="Momento del precio"
    )
    
    # Índices compuestos para queries eficientes
    __table_args__ = (
        # Índice para búsquedas por ticker y fecha
        Index('ix_ticker_timestamp', 'ticker', 'timestamp'),
        # Constraint para evitar duplicados
        UniqueConstraint(
            'ticker',
            'timestamp',
            name='uq_ticker_timestamp'
        ),
    )
    
    def __repr__(self) -> str:
        return (
            f"<Price(ticker='{self.ticker}', "
            f"price=${self.price_usd}, "
            f"timestamp={self.timestamp})>"
        )
    
    @classmethod
    def create_from_api(
        cls,
        ticker: str,
        price_usd: Decimal,
        source: str,
        exchange_rate: Decimal | None = None,
        **kwargs
    ) -> "Price":
        """
        Factory method para crear Price desde respuesta de API.
        
        Args:
            ticker: Symbol del activo
            price_usd: Precio en USD
            source: Fuente del precio
            exchange_rate: Tipo de cambio (opcional)
            **kwargs: Campos adicionales (volume, market_cap, etc)
        
        Returns:
            Instancia de Price
        """
        price_mxn = None
        if exchange_rate:
            price_mxn = price_usd * exchange_rate
        
        return cls(
            ticker=ticker,
            price_usd=price_usd,
            price_mxn=price_mxn,
            exchange_rate=exchange_rate,
            source=source,
            **kwargs
        )
