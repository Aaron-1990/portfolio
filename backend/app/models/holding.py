"""
Holding Model

Representa una posición (tenencia) de un activo en un portafolio.

Principios aplicados:
- Single Responsibility: Solo estructura de datos de tenencias
- Data Integrity: Foreign keys y constraints
"""

from decimal import Decimal
from sqlalchemy import Column, String, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base import Base, PKMixin, TimestampMixin


class Holding(Base, PKMixin, TimestampMixin):
    """
    Modelo de Tenencia (Holding) de Activo.
    
    Representa cuánto de cada activo posee el usuario en un portafolio.
    
    Attributes:
        id: Identificador único
        portfolio_id: ID del portafolio al que pertenece
        ticker: Symbol del activo (VOO, VGT, BTC, ETH)
        asset_type: Tipo de activo (stock, crypto)
        quantity: Cantidad poseída
        average_buy_price: Precio promedio de compra
        platform: Plataforma donde se compró (GBM, Bitso, etc)
        portfolio: Relación con Portfolio
    """
    
    __tablename__ = "holdings"
    
    # Foreign Keys
    portfolio_id = Column(
        ForeignKey("portfolios.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="ID del portafolio al que pertenece"
    )
    
    # Información del activo
    ticker = Column(
        String(20),
        nullable=False,
        index=True,
        doc="Symbol del activo (ej: VOO, BTC)"
    )
    
    asset_type = Column(
        String(20),
        nullable=False,
        doc="Tipo de activo: stock o crypto"
    )
    
    # Cantidades
    quantity = Column(
        Numeric(precision=20, scale=8),
        nullable=False,
        default=Decimal("0"),
        doc="Cantidad poseída del activo"
    )
    
    average_buy_price = Column(
        Numeric(precision=20, scale=2),
        nullable=False,
        default=Decimal("0"),
        doc="Precio promedio de compra en USD"
    )
    
    # Metadata
    platform = Column(
        String(50),
        nullable=True,
        doc="Plataforma donde se compró (GBM, Bitso, etc)"
    )
    
    # Relaciones
    portfolio = relationship(
        "Portfolio",
        back_populates="holdings"
    )
    
    # Constraints
    __table_args__ = (
        UniqueConstraint(
            'portfolio_id',
            'ticker',
            name='uq_portfolio_ticker'
        ),
    )
    
    def __repr__(self) -> str:
        return (
            f"<Holding(id={self.id}, ticker='{self.ticker}', "
            f"quantity={self.quantity}, avg_price={self.average_buy_price})>"
        )
    
    @property
    def total_invested(self) -> Decimal:
        """
        Calcula el monto total invertido.
        
        Returns:
            Cantidad × Precio Promedio
        """
        return Decimal(str(self.quantity)) * Decimal(str(self.average_buy_price))
    
    def update_average_price(
        self,
        new_quantity: Decimal,
        new_price: Decimal
    ) -> None:
        """
        Actualiza el precio promedio después de una compra.
        
        Formula: 
            new_avg = (current_value + new_purchase) / total_quantity
        
        Args:
            new_quantity: Cantidad comprada
            new_price: Precio de la nueva compra
        """
        current_value = self.total_invested
        new_purchase = new_quantity * new_price
        total_quantity = self.quantity + new_quantity
        
        if total_quantity > 0:
            self.average_buy_price = (
                current_value + new_purchase
            ) / total_quantity
        
        self.quantity = total_quantity
