"""
Price Schemas

Schemas Pydantic para prices y exchange rates.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class PriceBase(BaseModel):
    """Base schema para Price"""
    ticker: str = Field(..., max_length=20)
    asset_type: str = Field(..., pattern="^(stock|etf|crypto|other)$")
    price_usd: float = Field(..., gt=0)
    source: str = Field(..., max_length=50)
    volume: Optional[float] = Field(None, ge=0)
    market_cap: Optional[float] = Field(None, ge=0)


class PriceCreate(PriceBase):
    """Schema para crear price"""
    timestamp: Optional[datetime] = None


class PriceResponse(PriceBase):
    """Schema para respuesta de API"""
    id: int
    timestamp: datetime
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class LatestPriceResponse(BaseModel):
    """Último precio de un activo con metadata"""
    ticker: str
    price_usd: float
    price_mxn: Optional[float] = None
    exchange_rate: Optional[float] = None
    timestamp: datetime
    source: str
    change_24h_percent: Optional[float] = None


class ExchangeRateBase(BaseModel):
    """Base schema para ExchangeRate"""
    from_currency: str = Field(default="USD", max_length=3)
    to_currency: str = Field(default="MXN", max_length=3)
    rate: float = Field(..., gt=0)
    source: str = Field(..., max_length=50)


class ExchangeRateCreate(ExchangeRateBase):
    """Schema para crear exchange rate"""
    timestamp: Optional[datetime] = None


class ExchangeRateResponse(ExchangeRateBase):
    """Schema para respuesta"""
    id: int
    timestamp: datetime
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class PriceHistoryRequest(BaseModel):
    """Request para obtener historial de precios"""
    ticker: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    interval: str = Field(default="1h", pattern="^(1h|1d|1w|1m)$")


class PriceHistoryResponse(BaseModel):
    """Respuesta con historial de precios"""
    ticker: str
    prices: List[PriceResponse]
    start_date: datetime
    end_date: datetime
    count: int
