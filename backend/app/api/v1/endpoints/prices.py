"""
Price Endpoints

Implementa API REST para consulta y actualización de precios.

Principios aplicados:
- RESTful Design: Recursos y acciones claras
- Idempotency: POST /refresh es idempotente
- Caching: Respuestas cacheables
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict
from decimal import Decimal

from app.api.deps import get_db
from app.services.price_service import PriceService

router = APIRouter()


@router.get(
    "/latest",
    response_model=Dict[str, Decimal],
    summary="Obtener precios actuales",
    description="Obtiene los precios más recientes de todos los activos"
)
async def get_latest_prices(
    tickers: str | None = None,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Decimal]:
    """
    Obtiene precios actuales de los activos.
    
    - **tickers**: Lista de tickers separados por coma (opcional)
      Ejemplo: VOO,VGT,BTC,ETH
      Si no se proporciona, retorna todos los activos soportados.
    
    Returns:
        Dict con ticker: precio en USD
    
    Ejemplo de respuesta:
    ```json
    {
        "VOO": 523.18,
        "VGT": 592.45,
        "BTC": 67234.00,
        "ETH": 2580.00
    }
    ```
    """
    service = PriceService(db)
    
    # Parsear tickers si se proporcionan
    ticker_list = None
    if tickers:
        ticker_list = [t.strip().upper() for t in tickers.split(",")]
    
    try:
        prices = await service.get_latest_prices(ticker_list)
        return prices
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo precios: {str(e)}"
        )


@router.post(
    "/refresh",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Actualizar precios",
    description="Forzar actualización de precios desde APIs externas"
)
async def refresh_prices(
    tickers: str | None = None,
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Actualiza precios obteniendo datos frescos de las APIs.
    
    Este endpoint:
    1. Obtiene precios actuales de Yahoo Finance y CoinGecko
    2. Almacena los precios en la base de datos
    3. Retorna número de precios actualizados
    
    - **tickers**: Lista de tickers separados por coma (opcional)
    
    Returns:
        Dict con información de la actualización
    
    Ejemplo de respuesta:
    ```json
    {
        "status": "success",
        "prices_updated": 4,
        "timestamp": "2025-10-28T14:30:00"
    }
    ```
    """
    service = PriceService(db)
    
    # Parsear tickers si se proporcionan
    ticker_list = None
    if tickers:
        ticker_list = [t.strip().upper() for t in tickers.split(",")]
    
    try:
        from datetime import datetime
        
        count = await service.fetch_and_store_prices(ticker_list)
        
        return {
            "status": "success",
            "prices_updated": count,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error actualizando precios: {str(e)}"
        )


@router.get(
    "/{ticker}",
    response_model=dict,
    summary="Obtener precio de ticker",
    description="Obtiene el precio actual de un ticker específico"
)
async def get_ticker_price(
    ticker: str,
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Obtiene precio actual de un ticker específico.
    
    - **ticker**: Symbol del activo (VOO, VGT, BTC, ETH)
    
    Returns:
        Dict con información del precio
    
    Ejemplo de respuesta:
    ```json
    {
        "ticker": "VOO",
        "price_usd": 523.18,
        "source": "yahoo",
        "timestamp": "2025-10-28T14:30:00"
    }
    ```
    """
    service = PriceService(db)
    ticker = ticker.upper()
    
    try:
        price = await service.get_current_price(ticker)
        
        if price is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Precio no disponible para {ticker}"
            )
        
        from datetime import datetime
        
        return {
            "ticker": ticker,
            "price_usd": float(price),
            "source": "yahoo" if ticker in ["VOO", "VGT"] else "coingecko",
            "timestamp": datetime.utcnow().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo precio: {str(e)}"
        )


@router.get(
    "/history/{ticker}",
    response_model=list,
    summary="Obtener histórico de precios",
    description="Obtiene histórico de precios para un ticker"
)
async def get_price_history(
    ticker: str,
    days: int = 30,
    db: AsyncSession = Depends(get_db)
) -> list:
    """
    Obtiene histórico de precios.
    
    - **ticker**: Symbol del activo
    - **days**: Número de días de histórico (default: 30)
    
    TODO: Implementar query a base de datos
    """
    return []
