"""
CoinGecko Provider

Obtiene precios de criptomonedas desde CoinGecko API.
"""

from typing import Optional, List
from datetime import datetime
from app.providers.base import BaseProvider, PriceData


class CoinGeckoProvider(BaseProvider):
    """
    Provider para CoinGecko API.
    
    Soporta:
    - Bitcoin, Ethereum, y +13,000 cryptos
    
    Rate Limits: 50 requests/min (free tier)
    """
    
    BASE_URL = "https://api.coingecko.com/api/v3"
    
    # Mapeo de tickers a IDs de CoinGecko
    TICKER_TO_ID = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "USDT": "tether",
        "BNB": "binancecoin",
        "SOL": "solana",
        "ADA": "cardano",
        "XRP": "ripple",
        "DOT": "polkadot",
        "DOGE": "dogecoin",
        "AVAX": "avalanche-2",
    }
    
    @property
    def name(self) -> str:
        return "coingecko"
    
    def _get_coin_id(self, ticker: str) -> str:
        """Convierte ticker a CoinGecko ID"""
        ticker_upper = ticker.upper()
        return self.TICKER_TO_ID.get(ticker_upper, ticker.lower())
    
    async def get_price(self, ticker: str, asset_type: str) -> Optional[PriceData]:
        """Obtiene precio de CoinGecko"""
        coin_id = self._get_coin_id(ticker)
        
        url = f"{self.BASE_URL}/simple/price"
        params = {
            "ids": coin_id,
            "vs_currencies": "usd",
            "include_market_cap": "true",
            "include_24hr_vol": "true",
            "include_24hr_change": "true"
        }
        
        data = await self._make_request(url, params=params)
        
        if not data or coin_id not in data:
            return None
        
        coin_data = data[coin_id]
        
        return PriceData(
            ticker=ticker.upper(),
            price_usd=float(coin_data.get("usd", 0)),
            source=self.name,
            timestamp=datetime.utcnow(),
            volume=float(coin_data.get("usd_24h_vol", 0)),
            market_cap=float(coin_data.get("usd_market_cap", 0)),
            change_24h_percent=float(coin_data.get("usd_24h_change", 0))
        )
    
    async def get_multiple_prices(
        self,
        tickers: List[tuple[str, str]]
    ) -> List[PriceData]:
        """Obtiene múltiples precios en una sola request"""
        # Extraer solo tickers de crypto
        crypto_tickers = [t for t, at in tickers if at == "crypto"]
        
        if not crypto_tickers:
            return []
        
        # Convertir a IDs
        coin_ids = [self._get_coin_id(t) for t in crypto_tickers]
        
        url = f"{self.BASE_URL}/simple/price"
        params = {
            "ids": ",".join(coin_ids),
            "vs_currencies": "usd",
            "include_market_cap": "true",
            "include_24hr_vol": "true",
            "include_24hr_change": "true"
        }
        
        data = await self._make_request(url, params=params)
        
        if not data:
            return []
        
        results = []
        for ticker in crypto_tickers:
            coin_id = self._get_coin_id(ticker)
            if coin_id in data:
                coin_data = data[coin_id]
                results.append(PriceData(
                    ticker=ticker.upper(),
                    price_usd=float(coin_data.get("usd", 0)),
                    source=self.name,
                    timestamp=datetime.utcnow(),
                    volume=float(coin_data.get("usd_24h_vol", 0)),
                    market_cap=float(coin_data.get("usd_market_cap", 0)),
                    change_24h_percent=float(coin_data.get("usd_24h_change", 0))
                ))
        
        return results
    
    async def is_available(self) -> bool:
        """Verifica si CoinGecko está disponible"""
        try:
            url = f"{self.BASE_URL}/ping"
            data = await self._make_request(url)
            return data is not None and "gecko_says" in data
        except:
            return False
