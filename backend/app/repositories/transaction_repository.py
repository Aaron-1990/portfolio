"""
Transaction Repository
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import select, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Transaction, TransactionType
from app.repositories.base import BaseRepository


class TransactionRepository(BaseRepository[Transaction]):
    """Repository para Transaction"""
    
    def __init__(self, db: AsyncSession):
        super().__init__(Transaction, db)
    
    async def get_by_portfolio(
        self,
        portfolio_id: int,
        transaction_type: Optional[TransactionType] = None
    ) -> List[Transaction]:
        """Obtiene transacciones de un portfolio"""
        stmt = select(Transaction).where(Transaction.portfolio_id == portfolio_id)
        
        if transaction_type:
            stmt = stmt.where(Transaction.transaction_type == transaction_type)
        
        stmt = stmt.order_by(desc(Transaction.transaction_date))
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
    
    async def get_by_ticker(
        self,
        portfolio_id: int,
        ticker: str
    ) -> List[Transaction]:
        """Obtiene transacciones de un ticker específico"""
        stmt = (
            select(Transaction)
            .where(
                and_(
                    Transaction.portfolio_id == portfolio_id,
                    Transaction.ticker == ticker.upper()
                )
            )
            .order_by(Transaction.transaction_date)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
