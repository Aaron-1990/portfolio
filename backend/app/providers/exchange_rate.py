"""
Exchange Rate Provider

Obtiene tasas de cambio USD/MXN.
"""

from typing import Optional
from datetime import datetime
from app.providers.base import BaseProvider, ExchangeRateData


class ExchangeRateProvider(BaseProvider):
    """
    Provider para exchange rates.
    
    Usa exchangerate-api.com (gratis, 1500 requests/mes)
    """
    
    BASE_URL = "https://api.exchangerate-api.com/v4/latest"
    
    @property
    def name(self) -> str:
        return "exchangerate-api"
    
    async def get_rate(
        self,
        from_currency: str = "USD",
        to_currency: str = "MXN"
    ) -> Optional[ExchangeRateData]:
        """Obtiene exchange rate USD/MXN"""
        url = f"{self.BASE_URL}/{from_currency}"
        
        data = await self._make_request(url)
        
        if not data or "rates" not in data:
            return None
        
        rates = data["rates"]
        if to_currency not in rates:
            return None
        
        return ExchangeRateData(
            from_currency=from_currency,
            to_currency=to_currency,
            rate=float(rates[to_currency]),
            source=self.name,
            timestamp=datetime.utcnow()
        )
    
    async def get_price(self, ticker: str, asset_type: str):
        """No implementado - este provider solo hace exchange rates"""
        return None
    
    async def get_multiple_prices(self, tickers):
        """No implementado - este provider solo hace exchange rates"""
        return []
    
    async def is_available(self) -> bool:
        """Verifica disponibilidad"""
        try:
            result = await self.get_rate()
            return result is not None
        except:
            return False
