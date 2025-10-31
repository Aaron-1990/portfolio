"""
Database Session Management

Implementa async session management con context managers.

Principios aplicados:
- Dependency Inversion: Session como dependencia inyectable
- Single Responsibility: Solo gestión de sesiones
- Resource Management: Context managers para cleanup automático
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


# Configuración del engine
# Para SQLite usamos StaticPool para evitar threading issues
# En producción con PostgreSQL, usar QueuePool
engine_kwargs = {}
if settings.DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}
    engine_kwargs["poolclass"] = StaticPool

# Crear engine async
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Log SQL queries en desarrollo
    future=True,
    **engine_kwargs
)

# Session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Importante para evitar lazy loading issues
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency provider para FastAPI.
    
    Uso en endpoints:
        @app.get("/portfolios")
        async def get_portfolios(db: AsyncSession = Depends(get_db)):
            # usar db aquí
    
    Características:
    - Context manager automático
    - Rollback en caso de error
    - Cleanup garantizado
    
    Yields:
        AsyncSession lista para usar
    """
    async with AsyncSessionLocal() as session:
        try:
            logger.debug("Database session created")
            yield session
            await session.commit()
            logger.debug("Database session committed")
        except Exception as e:
            logger.error(f"Database session error: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()
            logger.debug("Database session closed")


async def init_db() -> None:
    """
    Inicializa la base de datos.
    
    Crea todas las tablas definidas en los modelos.
    Solo usar en desarrollo - en producción usar Alembic migrations.
    """
    from app.db.base import Base
    # Importar todos los modelos para que SQLAlchemy los registre
    from app.models import portfolio, holding, transaction, price  # noqa
    
    async with engine.begin() as conn:
        logger.info("Creating database tables...")
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")


async def close_db() -> None:
    """
    Cierra todas las conexiones de la base de datos.
    
    Llamar durante shutdown de la aplicación.
    """
    logger.info("Closing database connections...")
    await engine.dispose()
    logger.info("Database connections closed")
