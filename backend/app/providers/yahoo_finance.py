"""
Yahoo Finance Provider

Obtiene precios de stocks y ETFs desde Yahoo Finance API.
"""

from typing import Optional, List
from datetime import datetime
import yfinance as yf
from app.providers.base import BaseProvider, PriceData


class YahooFinanceProvider(BaseProvider):
    """
    Provider para Yahoo Finance.
    
    Soporta:
    - Stocks (AAPL, MSFT, etc)
    - ETFs (VOO, VGT, etc)
    
    Rate Limits: ~2000 requests/hora
    """
    
    @property
    def name(self) -> str:
        return "yahoo_finance"
    
    async def get_price(self, ticker: str, asset_type: str) -> Optional[PriceData]:
        """Obtiene precio de Yahoo Finance"""
        try:
            # yfinance es síncrono, pero es rápido
            stock = yf.Ticker(ticker)
            info = stock.info
            
            if not info or 'regularMarketPrice' not in info:
                # Fallback: usar history
                hist = stock.history(period="1d")
                if hist.empty:
                    return None
                
                price = float(hist['Close'].iloc[-1])
                volume = float(hist['Volume'].iloc[-1]) if 'Volume' in hist else None
            else:
                price = float(info.get('regularMarketPrice', 0))
                volume = float(info.get('volume', 0)) if 'volume' in info else None
            
            if price <= 0:
                return None
            
            return PriceData(
                ticker=ticker.upper(),
                price_usd=price,
                source=self.name,
                timestamp=datetime.utcnow(),
                volume=volume,
                market_cap=None,
                change_24h_percent=None
            )
        
        except Exception as e:
            print(f"Error fetching {ticker} from Yahoo Finance: {str(e)}")
            return None
    
    async def get_multiple_prices(
        self,
        tickers: List[tuple[str, str]]
    ) -> List[PriceData]:
        """Obtiene múltiples precios en paralelo"""
        import asyncio
        
        tasks = [
            self.get_price(ticker, asset_type)
            for ticker, asset_type in tickers
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return [
            result for result in results
            if isinstance(result, PriceData) and result is not None
        ]
    
    async def is_available(self) -> bool:
        """Verifica si Yahoo Finance está disponible"""
        try:
            # Test con un ticker conocido
            result = await self.get_price("VOO", "etf")
            return result is not None
        except:
            return False
