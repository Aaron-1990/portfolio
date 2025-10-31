"""
Portfolio Schemas

Define los schemas Pydantic para validación y serialización de portfolios y holdings.

Principios aplicados:
- Type Safety: Validación automática de tipos
- Data Validation: Reglas de negocio en schemas
- API Documentation: Schemas auto-documentan la API
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator, ConfigDict


# ============================================================================
# HOLDING SCHEMAS
# ============================================================================

class HoldingBase(BaseModel):
    """Base schema para Holding con campos comunes"""
    
    ticker: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Ticker del activo (VOO, VGT, BTC, ETH)",
        examples=["VOO", "BTC"]
    )
    
    asset_type: str = Field(
        ...,
        description="Tipo de activo",
        pattern="^(stock|etf|crypto|other)$",
        examples=["etf", "crypto"]
    )
    
    quantity: float = Field(
        ...,
        gt=0,
        description="Cantidad del activo (debe ser positivo)",
        examples=[0.85, 0.015]
    )
    
    average_cost: float = Field(
        ...,
        gt=0,
        description="Precio promedio de compra en USD",
        examples=[490.00, 45000.00]
    )
    
    platform: Optional[str] = Field(
        None,
        max_length=50,
        description="Plataforma donde se compró (GBM, Bitso, etc)",
        examples=["GBM", "Bitso"]
    )
    
    notes: Optional[str] = Field(
        None,
        max_length=500,
        description="Notas adicionales"
    )
    
    @validator("ticker")
    def ticker_uppercase(cls, v):
        """Convierte ticker a mayúsculas"""
        return v.upper().strip()
    
    @validator("asset_type")
    def asset_type_lowercase(cls, v):
        """Convierte asset_type a minúsculas"""
        return v.lower().strip()


class HoldingCreate(HoldingBase):
    """Schema para crear un nuevo holding"""
    pass


class HoldingUpdate(BaseModel):
    """Schema para actualizar un holding existente"""
    
    quantity: Optional[float] = Field(None, gt=0)
    average_cost: Optional[float] = Field(None, gt=0)
    platform: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = Field(None, max_length=500)
    
    model_config = ConfigDict(extra="forbid")  # No permitir campos extra


class HoldingResponse(HoldingBase):
    """Schema para respuesta de API con datos de holding"""
    
    id: int
    portfolio_id: int
    created_at: datetime
    updated_at: datetime
    
    # Campos calculados (agregados por el servicio)
    current_price: Optional[float] = Field(
        None,
        description="Precio actual en USD"
    )
    current_value_usd: Optional[float] = Field(
        None,
        description="Valor actual en USD"
    )
    current_value_mxn: Optional[float] = Field(
        None,
        description="Valor actual en MXN"
    )
    total_cost_usd: Optional[float] = Field(
        None,
        description="Costo total invertido en USD"
    )
    gain_loss_usd: Optional[float] = Field(
        None,
        description="Ganancia/pérdida en USD"
    )
    gain_loss_percent: Optional[float] = Field(
        None,
        description="Ganancia/pérdida en porcentaje"
    )
    
    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# PORTFOLIO SCHEMAS
# ============================================================================

class PortfolioBase(BaseModel):
    """Base schema para Portfolio"""
    
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Nombre del portfolio",
        examples=["Mi Portfolio Cubeta 1"]
    )
    
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Descripción del portfolio"
    )
    
    target_allocation: Optional[str] = Field(
        None,
        description="Target allocation en formato JSON string",
        examples=['{"VOO": 35, "VGT": 35, "BTC": 15, "ETH": 15}']
    )


class PortfolioCreate(PortfolioBase):
    """Schema para crear un nuevo portfolio"""
    
    is_active: bool = Field(
        default=True,
        description="Si el portfolio está activo"
    )


class PortfolioUpdate(BaseModel):
    """Schema para actualizar un portfolio existente"""
    
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    target_allocation: Optional[str] = None
    is_active: Optional[bool] = None
    
    model_config = ConfigDict(extra="forbid")


class PortfolioResponse(PortfolioBase):
    """Schema para respuesta de API con datos de portfolio"""
    
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    # Holdings relacionados
    holdings: List[HoldingResponse] = Field(
        default_factory=list,
        description="Lista de holdings en este portfolio"
    )
    
    # Métricas calculadas (agregadas por el servicio)
    total_value_usd: Optional[float] = Field(
        None,
        description="Valor total del portfolio en USD"
    )
    total_value_mxn: Optional[float] = Field(
        None,
        description="Valor total del portfolio en MXN"
    )
    total_invested_usd: Optional[float] = Field(
        None,
        description="Total invertido en USD"
    )
    total_gain_loss_usd: Optional[float] = Field(
        None,
        description="Ganancia/pérdida total en USD"
    )
    total_gain_loss_percent: Optional[float] = Field(
        None,
        description="Ganancia/pérdida total en porcentaje"
    )
    
    model_config = ConfigDict(from_attributes=True)


class PortfolioSummary(BaseModel):
    """Schema para resumen rápido de portfolio (sin holdings completos)"""
    
    id: int
    name: str
    description: Optional[str]
    is_active: bool
    holdings_count: int = Field(description="Número de holdings")
    total_value_usd: Optional[float]
    total_value_mxn: Optional[float]
    total_gain_loss_percent: Optional[float]
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# BULK OPERATIONS
# ============================================================================

class BulkHoldingCreate(BaseModel):
    """Schema para crear múltiples holdings a la vez"""
    
    portfolio_id: int = Field(..., description="ID del portfolio")
    holdings: List[HoldingCreate] = Field(
        ...,
        min_length=1,
        description="Lista de holdings a crear"
    )


class BulkHoldingResponse(BaseModel):
    """Respuesta de operación bulk"""
    
    success: bool
    created_count: int
    failed_count: int
    holdings: List[HoldingResponse]
    errors: Optional[List[str]] = None
