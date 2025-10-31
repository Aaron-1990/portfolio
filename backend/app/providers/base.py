"""
Base Price Provider

Define la interface común para todos los price providers.

Principios aplicados:
- Open/Closed: Fácil agregar nuevos providers sin modificar código existente
- Dependency Inversion: Servicios dependen de IPriceProvider, no implementaciones concretas
- Strategy Pattern: Diferentes estrategias para obtener precios
"""

from abc import ABC, abstractmethod
from typing import Optional, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class PriceData:
    """Data class para datos de precio"""
    ticker: str
    price_usd: float
    source: str
    timestamp: datetime
    volume: Optional[float] = None
    market_cap: Optional[float] = None
    change_24h_percent: Optional[float] = None


@dataclass
class ExchangeRateData:
    """Data class para exchange rate"""
    from_currency: str
    to_currency: str
    rate: float
    source: str
    timestamp: datetime


class IPriceProvider(ABC):
    """
    Interface para price providers.
    
    Cualquier nuevo provider debe implementar estos métodos.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Nombre del provider"""
        pass
    
    @abstractmethod
    async def get_price(self, ticker: str, asset_type: str) -> Optional[PriceData]:
        """
        Obtiene el precio actual de un activo.
        
        Args:
            ticker: Symbol del activo (VOO, BTC, etc)
            asset_type: Tipo del activo (stock, etf, crypto)
        
        Returns:
            PriceData o None si falla
        """
        pass
    
    @abstractmethod
    async def get_multiple_prices(
        self,
        tickers: List[tuple[str, str]]
    ) -> List[PriceData]:
        """
        Obtiene precios de múltiples activos.
        
        Args:
            tickers: Lista de (ticker, asset_type)
        
        Returns:
            Lista de PriceData
        """
        pass
    
    @abstractmethod
    async def is_available(self) -> bool:
        """
        Verifica si el provider está disponible.
        
        Returns:
            True si está disponible, False si está down
        """
        pass


class BaseProvider(IPriceProvider):
    """
    Implementación base con utilidades comunes.
    """
    
    def __init__(self, timeout: int = 10, max_retries: int = 3):
        self.timeout = timeout
        self.max_retries = max_retries
        self._session = None
    
    async def _make_request(
        self,
        url: str,
        params: Optional[dict] = None,
        headers: Optional[dict] = None
    ) -> Optional[dict]:
        """
        Hace una request HTTP con retry logic.
        
        Returns:
            JSON response o None si falla
        """
        import aiohttp
        import asyncio
        
        for attempt in range(self.max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        url,
                        params=params,
                        headers=headers,
                        timeout=aiohttp.ClientTimeout(total=self.timeout)
                    ) as response:
                        if response.status == 200:
                            return await response.json()
                        elif response.status == 429:  # Rate limit
                            wait_time = 2 ** attempt  # Exponential backoff
                            await asyncio.sleep(wait_time)
                        else:
                            return None
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                if attempt == self.max_retries - 1:
                    print(f"Error in {self.name}: {str(e)}")
                    return None
                await asyncio.sleep(1)
        
        return None
    
    def _normalize_ticker(self, ticker: str, asset_type: str) -> str:
        """
        Normaliza ticker según el formato que requiere cada API.
        Override en subclases si necesario.
        """
        return ticker.upper().strip()
