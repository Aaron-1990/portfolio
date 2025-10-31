"""
Portfolio Repository

Maneja acceso a datos de portfolios y holdings.
"""

from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models import Portfolio, Holding
from app.repositories.base import BaseRepository


class PortfolioRepository(BaseRepository[Portfolio]):
    """Repository para Portfolio con métodos específicos"""
    
    def __init__(self, db: AsyncSession):
        super().__init__(Portfolio, db)
    
    async def get_with_holdings(self, portfolio_id: int) -> Optional[Portfolio]:
        """Obtiene portfolio con todos sus holdings"""
        stmt = (
            select(Portfolio)
            .where(Portfolio.id == portfolio_id)
            .options(selectinload(Portfolio.holdings))
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_active_portfolios(self) -> List[Portfolio]:
        """Obtiene solo portfolios activos"""
        stmt = (
            select(Portfolio)
            .where(Portfolio.is_active == True)
            .options(selectinload(Portfolio.holdings))
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
    
    async def get_by_name(self, name: str) -> Optional[Portfolio]:
        """Busca portfolio por nombre"""
        stmt = select(Portfolio).where(Portfolio.name == name)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()


class HoldingRepository(BaseRepository[Holding]):
    """Repository para Holding con métodos específicos"""
    
    def __init__(self, db: AsyncSession):
        super().__init__(Holding, db)
    
    async def get_by_portfolio(self, portfolio_id: int) -> List[Holding]:
        """Obtiene todos los holdings de un portfolio"""
        stmt = select(Holding).where(Holding.portfolio_id == portfolio_id)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
    
    async def get_by_ticker(self, portfolio_id: int, ticker: str) -> Optional[Holding]:
        """Busca holding por ticker en un portfolio específico"""
        stmt = select(Holding).where(
            Holding.portfolio_id == portfolio_id,
            Holding.ticker == ticker.upper()
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def update_quantity(
        self,
        holding_id: int,
        new_quantity: float,
        new_avg_cost: float
    ) -> Optional[Holding]:
        """Actualiza cantidad y precio promedio de un holding"""
        return await self.update(
            holding_id,
            {"quantity": new_quantity, "average_cost": new_avg_cost}
        )
