"""
Transactions Endpoints

Implementa API REST para gestión de transacciones.

TODO: Implementar completamente
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_transactions():
    """Lista transacciones de un portafolio."""
    return []


@router.post("/")
async def create_transaction():
    """Registra una nueva transacción."""
    return {"status": "not_implemented"}
