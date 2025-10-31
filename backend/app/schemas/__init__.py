"""
Schemas Package

Expone todos los schemas Pydantic.
"""

from app.schemas.portfolio import (
    HoldingBase, HoldingCreate, HoldingUpdate, HoldingResponse,
    PortfolioBase, PortfolioCreate, PortfolioUpdate, PortfolioResponse,
    PortfolioSummary, BulkHoldingCreate, BulkHoldingResponse
)
from app.schemas.price import (
    PriceBase, PriceCreate, PriceResponse, LatestPriceResponse,
    ExchangeRateBase, ExchangeRateCreate, ExchangeRateResponse,
    PriceHistoryRequest, PriceHistoryResponse
)
from app.schemas.transaction import (
    TransactionBase, TransactionCreate, TransactionResponse, TransactionSummary
)

__all__ = [
    # Portfolio & Holdings
    "HoldingBase", "HoldingCreate", "HoldingUpdate", "HoldingResponse",
    "PortfolioBase", "PortfolioCreate", "PortfolioUpdate", "PortfolioResponse",
    "PortfolioSummary", "BulkHoldingCreate", "BulkHoldingResponse",
    # Prices
    "PriceBase", "PriceCreate", "PriceResponse", "LatestPriceResponse",
    "ExchangeRateBase", "ExchangeRateCreate", "ExchangeRateResponse",
    "PriceHistoryRequest", "PriceHistoryResponse",
    # Transactions
    "TransactionBase", "TransactionCreate", "TransactionResponse", "TransactionSummary",
]
