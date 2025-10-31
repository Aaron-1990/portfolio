"""
Base Repository

Implementa el patrón Repository con operaciones CRUD genéricas.

Principios aplicados:
- DRY: Código CRUD reutilizable
- Generic: Funciona con cualquier modelo
- Type-safe: Con TypeVar para type hints correctos
- Async: Todas las operaciones son asíncronas
"""

from typing import Generic, TypeVar, Type, Optional, List, Any
from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Repository base con operaciones CRUD genéricas.
    
    Uso:
        class PortfolioRepository(BaseRepository[Portfolio]):
            pass
    """
    
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        """
        Args:
            model: El modelo SQLAlchemy (ej: Portfolio)
            db: Sesión de base de datos
        """
        self.model = model
        self.db = db
    
    async def get_by_id(self, id: int) -> Optional[ModelType]:
        """Obtiene un registro por ID"""
        stmt = select(self.model).where(self.model.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[dict] = None
    ) -> List[ModelType]:
        """
        Obtiene múltiples registros con paginación.
        
        Args:
            skip: Cantidad de registros a saltar
            limit: Máximo de registros a retornar
            filters: Dict con filtros {campo: valor}
        """
        stmt = select(self.model)
        
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field):
                    stmt = stmt.where(getattr(self.model, field) == value)
        
        stmt = stmt.offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
    
    async def create(self, obj_in: dict) -> ModelType:
        """Crea un nuevo registro"""
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        await self.db.flush()
        await self.db.refresh(db_obj)
        return db_obj
    
    async def update(self, id: int, obj_in: dict) -> Optional[ModelType]:
        """Actualiza un registro existente"""
        # Filtrar None values
        update_data = {k: v for k, v in obj_in.items() if v is not None}
        
        if not update_data:
            return await self.get_by_id(id)
        
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**update_data)
            .execution_options(synchronize_session="fetch")
        )
        
        await self.db.execute(stmt)
        await self.db.flush()
        return await self.get_by_id(id)
    
    async def delete(self, id: int) -> bool:
        """Elimina un registro"""
        stmt = delete(self.model).where(self.model.id == id)
        result = await self.db.execute(stmt)
        await self.db.flush()
        return result.rowcount > 0
    
    async def count(self, filters: Optional[dict] = None) -> int:
        """Cuenta registros con filtros opcionales"""
        stmt = select(func.count()).select_from(self.model)
        
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field):
                    stmt = stmt.where(getattr(self.model, field) == value)
        
        result = await self.db.execute(stmt)
        return result.scalar_one()
    
    async def exists(self, id: int) -> bool:
        """Verifica si existe un registro"""
        stmt = select(func.count()).select_from(self.model).where(self.model.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one() > 0
