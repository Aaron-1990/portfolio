"""
Transaction Schemas
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator, ConfigDict
from app.models.transaction import TransactionType


class TransactionBase(BaseModel):
    """Base schema para Transaction"""
    ticker: str = Field(..., max_length=20)
    asset_type: str = Field(..., pattern="^(stock|etf|crypto|other)$")
    transaction_type: TransactionType
    quantity: float = Field(..., description="Positivo para compra, negativo para venta")
    price_per_unit: float = Field(..., gt=0)
    fee: float = Field(default=0.0, ge=0)
    platform: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = Field(None, max_length=500)
    transaction_date: datetime
    exchange_rate: Optional[float] = Field(None, gt=0)
    
    @validator("ticker")
    def ticker_uppercase(cls, v):
        return v.upper().strip()


class TransactionCreate(TransactionBase):
    """Schema para crear transacción"""
    pass


class TransactionResponse(TransactionBase):
    """Schema para respuesta"""
    id: int
    portfolio_id: int
    total_value: float
    total_value_mxn: Optional[float]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class TransactionSummary(BaseModel):
    """Resumen de transacciones por activo"""
    ticker: str
    total_quantity: float
    total_invested_usd: float
    total_invested_mxn: float
    average_cost: float
    transaction_count: int
    first_purchase_date: Optional[datetime]
    last_purchase_date: Optional[datetime]
