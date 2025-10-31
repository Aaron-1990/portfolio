"""
Portfolio Service

Implementa lógica de negocio para portafolios.

Principios aplicados:
- Single Responsibility: Solo lógica de portafolios
- Dependency Injection: Repository como dependencia
- Business Logic Layer: Separado de controllers y data access
"""

from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.models.portfolio import Portfolio
from app.models.holding import Holding
from app.core.logging import get_logger
from app.schemas.portfolio import PortfolioCreate, PortfolioUpdate

logger = get_logger(__name__)


class PortfolioService:
    """
    Servicio para gestión de portafolios.
    
    Encapsula lógica de negocio y orquesta operaciones complejas.
    """
    
    def __init__(self, db: AsyncSession):
        """
        Inicializa el servicio con una sesión de base de datos.
        
        Args:
            db: Sesión async de SQLAlchemy
        """
        self.db = db
    
    async def create_portfolio(
        self,
        portfolio_data: PortfolioCreate
    ) -> Portfolio:
        """
        Crea un nuevo portafolio.
        
        Args:
            portfolio_data: Datos del portafolio
        
        Returns:
            Portafolio creado
        
        Raises:
            ValueError: Si la suma de porcentajes no es 100%
        """
        # Validar que la suma de porcentajes sea 100%
        total_percent = (
            portfolio_data.target_voo_percent +
            portfolio_data.target_vgt_percent +
            portfolio_data.target_btc_percent +
            portfolio_data.target_eth_percent
        )
        
        if abs(total_percent - Decimal("100.0")) > Decimal("0.01"):
            raise ValueError(
                f"La suma de porcentajes debe ser 100%. Suma actual: {total_percent}%"
            )
        
        # Crear portafolio
        portfolio = Portfolio(
            **portfolio_data.model_dump()
        )
        
        self.db.add(portfolio)
        await self.db.commit()
        await self.db.refresh(portfolio)
        
        logger.info(
            "Portfolio created",
            extra={"portfolio_id": portfolio.id, "name": portfolio.name}
        )
        
        return portfolio
    
    async def get_portfolio(self, portfolio_id: int) -> Portfolio | None:
        """
        Obtiene un portafolio por ID.
        
        Args:
            portfolio_id: ID del portafolio
        
        Returns:
            Portafolio o None si no existe
        """
        result = await self.db.execute(
            select(Portfolio)
            .where(Portfolio.id == portfolio_id)
        )
        return result.scalar_one_or_none()
    
    async def get_all_portfolios(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[Portfolio]:
        """
        Obtiene lista de portafolios con paginación.
        
        Args:
            skip: Número de registros a saltar
            limit: Máximo número de registros
        
        Returns:
            Lista de portafolios
        """
        result = await self.db.execute(
            select(Portfolio)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def update_portfolio(
        self,
        portfolio_id: int,
        portfolio_data: PortfolioUpdate
    ) -> Portfolio | None:
        """
        Actualiza un portafolio existente.
        
        Args:
            portfolio_id: ID del portafolio
            portfolio_data: Datos a actualizar
        
        Returns:
            Portafolio actualizado o None si no existe
        """
        portfolio = await self.get_portfolio(portfolio_id)
        
        if not portfolio:
            return None
        
        # Actualizar solo campos proporcionados
        update_data = portfolio_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(portfolio, field, value)
        
        await self.db.commit()
        await self.db.refresh(portfolio)
        
        logger.info(
            "Portfolio updated",
            extra={"portfolio_id": portfolio.id}
        )
        
        return portfolio
    
    async def delete_portfolio(self, portfolio_id: int) -> bool:
        """
        Elimina un portafolio.
        
        Cascade delete eliminará holdings y transactions asociadas.
        
        Args:
            portfolio_id: ID del portafolio
        
        Returns:
            True si se eliminó, False si no existía
        """
        portfolio = await self.get_portfolio(portfolio_id)
        
        if not portfolio:
            return False
        
        await self.db.delete(portfolio)
        await self.db.commit()
        
        logger.info(
            "Portfolio deleted",
            extra={"portfolio_id": portfolio_id}
        )
        
        return True
    
    async def get_portfolio_value(self, portfolio_id: int) -> Decimal:
        """
        Calcula el valor total actual del portafolio.
        
        Args:
            portfolio_id: ID del portafolio
        
        Returns:
            Valor total en USD
        
        TODO: Implementar cálculo con precios actuales
        """
        # Por ahora retorna 0, implementar con PriceService
        return Decimal("0")
    
    async def get_portfolio_distribution(
        self,
        portfolio_id: int
    ) -> dict[str, Decimal]:
        """
        Calcula la distribución actual de activos.
        
        Args:
            portfolio_id: ID del portafolio
        
        Returns:
            Dict con ticker: percentage
        
        TODO: Implementar con holdings actuales
        """
        return {}
