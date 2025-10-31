"""
Transaction Models

Define la tabla de transacciones (compras/ventas).

Principios aplicados:
- Auditability: Registro completo de todas las operaciones
- Immutability: Transacciones no se modifican, solo se agregan
- Data Integrity: Validaciones robustas
"""

from datetime import datetime
from enum import Enum
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    CheckConstraint,
    Index,
    Enum as SQLEnum,
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class TransactionType(str, Enum):
    """Tipos de transacciones"""
    BUY = "buy"
    SELL = "sell"
    DIVIDEND = "dividend"  # Para tracking de dividendos futuro
    FEE = "fee"  # Para tracking de comisiones


class Transaction(Base):
    """
    Transaction Model - Registro inmutable de todas las operaciones.
    
    Cada compra/venta se registra aquí para:
    - Auditabilidad completa
    - Cálculo de precio promedio
    - Reportes de impuestos
    - Análisis histórico
    
    Relaciones:
    - Una transacción pertenece a un portfolio (many-to-one)
    """
    
    __tablename__ = "transactions"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign Key
    portfolio_id = Column(
        Integer,
        ForeignKey("portfolios.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="ID del portfolio"
    )
    
    # Transaction Type
    transaction_type = Column(
        SQLEnum(TransactionType),
        nullable=False,
        index=True,
        comment="Tipo: buy, sell, dividend, fee"
    )
    
    # Asset Information
    ticker = Column(
        String(20),
        nullable=False,
        index=True,
        comment="Ticker del activo"
    )
    
    asset_type = Column(
        String(20),
        nullable=False,
        comment="Tipo: 'stock', 'etf', 'crypto'"
    )
    
    # Transaction Details
    quantity = Column(
        Float,
        nullable=False,
        comment="Cantidad comprada/vendida (positivo para compra, negativo para venta)"
    )
    
    price_per_unit = Column(
        Float,
        nullable=False,
        comment="Precio por unidad en USD al momento de la transacción"
    )
    
    total_value = Column(
        Float,
        nullable=False,
        comment="Valor total = quantity × price_per_unit"
    )
    
    # Fees & Exchange Rate
    fee = Column(
        Float,
        default=0.0,
        nullable=False,
        comment="Comisión pagada en USD"
    )
    
    exchange_rate = Column(
        Float,
        nullable=True,
        comment="Tasa USD/MXN al momento de la transacción (para reportes)"
    )
    
    total_value_mxn = Column(
        Float,
        nullable=True,
        comment="Valor total en MXN (calculado con exchange_rate)"
    )
    
    # Platform & Notes
    platform = Column(
        String(50),
        nullable=True,
        comment="Plataforma donde se ejecutó (GBM, Bitso, etc)"
    )
    
    notes = Column(
        String(500),
        nullable=True,
        comment="Notas adicionales sobre esta transacción"
    )
    
    # Timestamps
    transaction_date = Column(
        DateTime,
        nullable=False,
        index=True,
        comment="Fecha/hora real de la transacción"
    )
    
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment="Cuándo se registró en el sistema"
    )
    
    # Relationships
    portfolio = relationship("Portfolio", back_populates="transactions")
    
    # Constraints
    __table_args__ = (
        # Precio debe ser positivo
        CheckConstraint("price_per_unit > 0", name="check_price_per_unit_positive"),
        
        # Fee no puede ser negativo
        CheckConstraint("fee >= 0", name="check_fee_non_negative"),
        
        # Exchange rate debe ser positivo si está presente
        CheckConstraint(
            "exchange_rate IS NULL OR exchange_rate > 0",
            name="check_exchange_rate_positive"
        ),
        
        # Índices para queries comunes
        Index("idx_portfolio_date", "portfolio_id", "transaction_date"),
        Index("idx_ticker_date", "ticker", "transaction_date"),
        Index("idx_transaction_type", "transaction_type"),
    )
    
    def __repr__(self) -> str:
        return (
            f"<Transaction(type={self.transaction_type}, ticker='{self.ticker}', "
            f"quantity={self.quantity}, price=${self.price_per_unit})>"
        )
    
    @property
    def total_cost_with_fee(self) -> float:
        """Costo total incluyendo comisión"""
        return abs(self.total_value) + self.fee
    
    def to_dict(self) -> dict:
        """Convierte a dict para JSON serialization"""
        return {
            "id": self.id,
            "portfolio_id": self.portfolio_id,
            "transaction_type": self.transaction_type.value,
            "ticker": self.ticker,
            "asset_type": self.asset_type,
            "quantity": self.quantity,
            "price_per_unit": self.price_per_unit,
            "total_value": self.total_value,
            "fee": self.fee,
            "exchange_rate": self.exchange_rate,
            "total_value_mxn": self.total_value_mxn,
            "platform": self.platform,
            "notes": self.notes,
            "transaction_date": self.transaction_date.isoformat() if self.transaction_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class TransactionHelper:
    """
    Helper class para operaciones comunes con transacciones.
    
    No es un modelo de DB, pero provee utilidades relacionadas.
    """
    
    @staticmethod
    def calculate_average_cost(transactions: list[Transaction]) -> float:
        """
        Calcula el precio promedio ponderado de compra.
        
        Formula: Sum(quantity × price) / Sum(quantity)
        
        Args:
            transactions: Lista de transacciones de compra del mismo ticker
        
        Returns:
            Precio promedio ponderado
        """
        if not transactions:
            return 0.0
        
        total_quantity = 0.0
        total_cost = 0.0
        
        for txn in transactions:
            if txn.transaction_type == TransactionType.BUY:
                total_quantity += txn.quantity
                total_cost += txn.quantity * txn.price_per_unit
        
        if total_quantity == 0:
            return 0.0
        
        return total_cost / total_quantity
    
    @staticmethod
    def calculate_total_invested(transactions: list[Transaction]) -> dict:
        """
        Calcula el total invertido (compras - ventas).
        
        Returns:
            Dict con total_invested_usd y total_invested_mxn
        """
        total_usd = 0.0
        total_mxn = 0.0
        
        for txn in transactions:
            if txn.transaction_type == TransactionType.BUY:
                total_usd += txn.total_value + txn.fee
                if txn.total_value_mxn:
                    total_mxn += txn.total_value_mxn
            elif txn.transaction_type == TransactionType.SELL:
                total_usd -= txn.total_value - txn.fee
                if txn.total_value_mxn:
                    total_mxn -= txn.total_value_mxn
        
        return {
            "total_invested_usd": round(total_usd, 2),
            "total_invested_mxn": round(total_mxn, 2),
        }
