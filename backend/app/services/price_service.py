"""
Price Service

Orquesta la obtención y almacenamiento de precios.

Principios aplicados:
- Strategy Pattern: Múltiples providers intercambiables
- Dependency Injection: Providers como dependencias
- Fault Tolerance: Fallback entre providers
"""

from decimal import Decimal
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict

from app.models.price import Price
from app.providers.yahoo_finance import YahooFinanceProvider
from app.providers.coingecko import CoinGeckoProvider
from app.providers.exchange_rate import ExchangeRateProvider
from app.core.logging import get_logger

logger = get_logger(__name__)


class PriceService:
    """
    Servicio para gestión de precios.
    
    Coordina múltiples providers y almacena histórico.
    """
    
    # Mapeo de tickers a providers
    STOCK_TICKERS = ["VOO", "VGT"]
    CRYPTO_TICKERS = ["BTC", "ETH"]
    
    def __init__(self, db: AsyncSession):
        """
        Inicializa el servicio con providers.
        
        Args:
            db: Sesión async de SQLAlchemy
        """
        self.db = db
        self.yahoo_provider = YahooFinanceProvider()
        self.coingecko_provider = CoinGeckoProvider()
        self.exchange_rate_provider = ExchangeRateProvider()
    
    async def get_latest_prices(
        self,
        tickers: list[str] | None = None
    ) -> Dict[str, Decimal]:
        """
        Obtiene precios actuales de todos los activos.
        
        Args:
            tickers: Lista de tickers (opcional, default: todos)
        
        Returns:
            Dict con ticker: precio en USD
        """
        if tickers is None:
            tickers = self.STOCK_TICKERS + self.CRYPTO_TICKERS
        
        prices = {}
        
        # Obtener precios de stocks
        for ticker in tickers:
            if ticker in self.STOCK_TICKERS:
                try:
                    price = await self.yahoo_provider.get_price(ticker)
                    prices[ticker] = price
                    logger.debug(f"Precio obtenido para {ticker}: ${price}")
                except Exception as e:
                    logger.error(f"Error obteniendo precio de {ticker}: {e}")
        
        # Obtener precios de crypto
        crypto_tickers_to_fetch = [
            t for t in tickers if t in self.CRYPTO_TICKERS
        ]
        if crypto_tickers_to_fetch:
            try:
                crypto_prices = await self.coingecko_provider.get_prices(
                    crypto_tickers_to_fetch
                )
                prices.update(crypto_prices)
                logger.debug(f"Precios crypto obtenidos: {crypto_prices}")
            except Exception as e:
                logger.error(f"Error obteniendo precios crypto: {e}")
        
        return prices
    
    async def fetch_and_store_prices(
        self,
        tickers: list[str] | None = None
    ) -> int:
        """
        Obtiene precios actuales y los almacena en DB.
        
        Args:
            tickers: Lista de tickers (opcional)
        
        Returns:
            Número de precios almacenados
        """
        # Obtener tipo de cambio
        try:
            exchange_rate = await self.exchange_rate_provider.get_rate("USD", "MXN")
        except Exception as e:
            logger.warning(f"Error obteniendo tipo de cambio: {e}")
            exchange_rate = Decimal("20.0")  # Fallback
        
        # Obtener precios
        prices = await self.get_latest_prices(tickers)
        
        # Almacenar en DB
        stored_count = 0
        for ticker, price_usd in prices.items():
            try:
                # Determinar source
                source = (
                    "yahoo" if ticker in self.STOCK_TICKERS
                    else "coingecko"
                )
                
                # Crear registro de precio
                price = Price.create_from_api(
                    ticker=ticker,
                    price_usd=price_usd,
                    source=source,
                    exchange_rate=exchange_rate
                )
                
                self.db.add(price)
                stored_count += 1
                
            except Exception as e:
                logger.error(f"Error almacenando precio de {ticker}: {e}")
        
        # Commit
        try:
            await self.db.commit()
            logger.info(f"Almacenados {stored_count} precios")
        except Exception as e:
            logger.error(f"Error en commit de precios: {e}")
            await self.db.rollback()
            stored_count = 0
        
        return stored_count
    
    async def get_price_history(
        self,
        ticker: str,
        start_date: datetime,
        end_date: datetime
    ) -> list[Price]:
        """
        Obtiene histórico de precios para un ticker.
        
        Args:
            ticker: Symbol del activo
            start_date: Fecha inicial
            end_date: Fecha final
        
        Returns:
            Lista de precios ordenados por timestamp
        
        TODO: Implementar query a la base de datos
        """
        return []
    
    async def get_current_price(self, ticker: str) -> Decimal | None:
        """
        Obtiene el precio más reciente de un ticker.
        
        Primero busca en cache/DB, si no hay, fetch de API.
        
        Args:
            ticker: Symbol del activo
        
        Returns:
            Precio en USD o None si no disponible
        """
        try:
            prices = await self.get_latest_prices([ticker])
            return prices.get(ticker)
        except Exception as e:
            logger.error(f"Error obteniendo precio actual de {ticker}: {e}")
            return None
