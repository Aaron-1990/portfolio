"""
Portfolio Endpoints

Implementa API REST para gestión de portafolios.

Principios aplicados:
- RESTful Design: Verbos HTTP semánticos
- Dependency Injection: Services como dependencias
- Error Handling: Respuestas HTTP apropiadas
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api.deps import get_db
from app.services.portfolio_service import PortfolioService
from app.schemas.portfolio import (
    Portfolio,
    PortfolioCreate,
    PortfolioUpdate,
    PortfolioWithHoldings
)

router = APIRouter()


@router.post(
    "/",
    response_model=Portfolio,
    status_code=status.HTTP_201_CREATED,
    summary="Crear portafolio",
    description="Crea un nuevo portafolio de inversión"
)
async def create_portfolio(
    portfolio_data: PortfolioCreate,
    db: AsyncSession = Depends(get_db)
) -> Portfolio:
    """
    Crea un nuevo portafolio.
    
    - **name**: Nombre único del portafolio
    - **description**: Descripción opcional
    - **target_*_percent**: Distribución objetivo (debe sumar 100%)
    """
    service = PortfolioService(db)
    
    try:
        portfolio = await service.create_portfolio(portfolio_data)
        return portfolio
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/",
    response_model=List[Portfolio],
    summary="Listar portafolios",
    description="Obtiene lista de todos los portafolios"
)
async def list_portfolios(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
) -> List[Portfolio]:
    """
    Obtiene lista de portafolios con paginación.
    
    - **skip**: Número de registros a saltar (default: 0)
    - **limit**: Máximo número de registros (default: 100)
    """
    service = PortfolioService(db)
    portfolios = await service.get_all_portfolios(skip, limit)
    return portfolios


@router.get(
    "/{portfolio_id}",
    response_model=Portfolio,
    summary="Obtener portafolio",
    description="Obtiene un portafolio específico por ID"
)
async def get_portfolio(
    portfolio_id: int,
    db: AsyncSession = Depends(get_db)
) -> Portfolio:
    """
    Obtiene detalles de un portafolio específico.
    
    - **portfolio_id**: ID del portafolio
    """
    service = PortfolioService(db)
    portfolio = await service.get_portfolio(portfolio_id)
    
    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Portafolio con ID {portfolio_id} no encontrado"
        )
    
    return portfolio


@router.patch(
    "/{portfolio_id}",
    response_model=Portfolio,
    summary="Actualizar portafolio",
    description="Actualiza un portafolio existente"
)
async def update_portfolio(
    portfolio_id: int,
    portfolio_data: PortfolioUpdate,
    db: AsyncSession = Depends(get_db)
) -> Portfolio:
    """
    Actualiza campos de un portafolio.
    
    Solo los campos proporcionados serán actualizados.
    
    - **portfolio_id**: ID del portafolio
    """
    service = PortfolioService(db)
    portfolio = await service.update_portfolio(portfolio_id, portfolio_data)
    
    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Portafolio con ID {portfolio_id} no encontrado"
        )
    
    return portfolio


@router.delete(
    "/{portfolio_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar portafolio",
    description="Elimina un portafolio y sus holdings/transactions"
)
async def delete_portfolio(
    portfolio_id: int,
    db: AsyncSession = Depends(get_db)
) -> None:
    """
    Elimina un portafolio.
    
    ADVERTENCIA: También eliminará todos los holdings y transactions asociados.
    
    - **portfolio_id**: ID del portafolio
    """
    service = PortfolioService(db)
    deleted = await service.delete_portfolio(portfolio_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Portafolio con ID {portfolio_id} no encontrado"
        )


@router.get(
    "/{portfolio_id}/summary",
    response_model=dict,
    summary="Obtener resumen",
    description="Obtiene resumen completo con valor y distribución"
)
async def get_portfolio_summary(
    portfolio_id: int,
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Obtiene resumen completo del portafolio.
    
    Incluye:
    - Valor total actual
    - Distribución de activos
    - Comparación con targets
    - Ganancias/pérdidas
    
    - **portfolio_id**: ID del portafolio
    """
    service = PortfolioService(db)
    portfolio = await service.get_portfolio(portfolio_id)
    
    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Portafolio con ID {portfolio_id} no encontrado"
        )
    
    # TODO: Implementar cálculos completos
    return {
        "portfolio_id": portfolio.id,
        "name": portfolio.name,
        "total_value_usd": 0,
        "total_value_mxn": 0,
        "total_gain_loss": 0,
        "distribution": {},
        "target_distribution": portfolio.target_distribution
    }
