"""
Price Repository

Maneja acceso a datos de precios y exchange rates con optimizaciones para time-series.
"""

from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy import select, desc, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Price, ExchangeRate
from app.repositories.base import BaseRepository


class PriceRepository(BaseRepository[Price]):
    """Repository para Price con queries time-series"""
    
    def __init__(self, db: AsyncSession):
        super().__init__(Price, db)
    
    async def get_latest_price(self, ticker: str) -> Optional[Price]:
        """Obtiene el precio más reciente de un ticker"""
        stmt = (
            select(Price)
            .where(Price.ticker == ticker.upper())
            .order_by(desc(Price.timestamp))
            .limit(1)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_latest_prices(self, tickers: List[str]) -> List[Price]:
        """Obtiene precios más recientes de múltiples tickers"""
        # Subquery para obtener timestamp más reciente por ticker
        latest_timestamps = (
            select(
                Price.ticker,
                func.max(Price.timestamp).label('max_timestamp')
            )
            .where(Price.ticker.in_([t.upper() for t in tickers]))
            .group_by(Price.ticker)
            .subquery()
        )
        
        # Join para obtener precios con timestamp más reciente
        stmt = (
            select(Price)
            .join(
                latest_timestamps,
                and_(
                    Price.ticker == latest_timestamps.c.ticker,
                    Price.timestamp == latest_timestamps.c.max_timestamp
                )
            )
        )
        
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
    
    async def get_price_history(
        self,
        ticker: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 1000
    ) -> List[Price]:
        """Obtiene historial de precios con filtros de fecha"""
        stmt = select(Price).where(Price.ticker == ticker.upper())
        
        if start_date:
            stmt = stmt.where(Price.timestamp >= start_date)
        if end_date:
            stmt = stmt.where(Price.timestamp <= end_date)
        
        stmt = stmt.order_by(Price.timestamp).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
    
    async def delete_old_prices(self, days: int = 365) -> int:
        """Elimina precios más antiguos que X días"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        stmt = delete(Price).where(Price.timestamp < cutoff_date)
        result = await self.db.execute(stmt)
        await self.db.flush()
        return result.rowcount


class ExchangeRateRepository(BaseRepository[ExchangeRate]):
    """Repository para ExchangeRate"""
    
    def __init__(self, db: AsyncSession):
        super().__init__(ExchangeRate, db)
    
    async def get_latest_rate(
        self,
        from_currency: str = "USD",
        to_currency: str = "MXN"
    ) -> Optional[ExchangeRate]:
        """Obtiene el exchange rate más reciente"""
        stmt = (
            select(ExchangeRate)
            .where(
                ExchangeRate.from_currency == from_currency,
                ExchangeRate.to_currency == to_currency
            )
            .order_by(desc(ExchangeRate.timestamp))
            .limit(1)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()


from sqlalchemy import delete, func
