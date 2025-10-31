"""
Holdings Endpoints

Implementa API REST para gestión de holdings (posiciones).

TODO: Implementar completamente
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_holdings():
    """Lista holdings de un portafolio."""
    return []


@router.post("/")
async def create_holding():
    """Crea un nuevo holding."""
    return {"status": "not_implemented"}
