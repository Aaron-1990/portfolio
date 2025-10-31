# Portfolio Tracker - Backend API
# Version minima funcional con endpoints mock

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Crear aplicacion FastAPI
app = FastAPI(
    title="Portfolio Tracker API",
    description="Sistema profesional de tracking de inversiones",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# ENDPOINTS
# ============================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": "Portfolio Tracker",
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    """Root endpoint con info de la API"""
    return {
        "app": "Portfolio Tracker API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

# ============================================
# PORTFOLIOS ENDPOINTS
# ============================================

@app.get("/api/v1/portfolios")
async def list_portfolios():
    """Lista todos los portfolios (mock data)"""
    return [
        {
            "id": 1,
            "name": "Portfolio Principal",
            "description": "Mi portafolio de inversiones",
            "target_voo_percent": 40.0,
            "target_vgt_percent": 30.0,
            "target_btc_percent": 20.0,
            "target_eth_percent": 10.0,
            "created_at": "2025-01-01T00:00:00",
            "updated_at": "2025-01-01T00:00:00"
        },
        {
            "id": 2,
            "name": "Portfolio Agresivo",
            "description": "Portfolio con mayor riesgo",
            "target_voo_percent": 20.0,
            "target_vgt_percent": 30.0,
            "target_btc_percent": 30.0,
            "target_eth_percent": 20.0,
            "created_at": "2025-01-01T00:00:00",
            "updated_at": "2025-01-01T00:00:00"
        }
    ]

@app.get("/api/v1/portfolios/{portfolio_id}")
async def get_portfolio(portfolio_id: int):
    """Obtiene un portfolio especifico por ID"""
    return {
        "id": portfolio_id,
        "name": "Portfolio Principal",
        "description": "Mi portafolio de inversiones",
        "target_voo_percent": 40.0,
        "target_vgt_percent": 30.0,
        "target_btc_percent": 20.0,
        "target_eth_percent": 10.0,
        "created_at": "2025-01-01T00:00:00",
        "updated_at": "2025-01-01T00:00:00"
    }

# ============================================
# HOLDINGS ENDPOINTS
# ============================================

@app.get("/api/v1/holdings")
async def list_holdings(portfolio_id: int = None):
    """Lista holdings de un portfolio (mock data)"""
    holdings = [
        {
            "id": 1,
            "portfolio_id": 1,
            "ticker": "VOO",
            "quantity": 10.0,
            "average_buy_price": 450.0,
            "asset_type": "stock",
            "platform": "Interactive Brokers",
            "created_at": "2025-01-01T00:00:00"
        },
        {
            "id": 2,
            "portfolio_id": 1,
            "ticker": "VGT",
            "quantity": 5.0,
            "average_buy_price": 480.0,
            "asset_type": "stock",
            "platform": "Interactive Brokers",
            "created_at": "2025-01-01T00:00:00"
        },
        {
            "id": 3,
            "portfolio_id": 1,
            "ticker": "BTC",
            "quantity": 0.5,
            "average_buy_price": 42000.0,
            "asset_type": "crypto",
            "platform": "Coinbase",
            "created_at": "2025-01-01T00:00:00"
        },
        {
            "id": 4,
            "portfolio_id": 1,
            "ticker": "ETH",
            "quantity": 2.0,
            "average_buy_price": 2400.0,
            "asset_type": "crypto",
            "platform": "Coinbase",
            "created_at": "2025-01-01T00:00:00"
        }
    ]
    
    if portfolio_id:
        holdings = [h for h in holdings if h["portfolio_id"] == portfolio_id]
    
    return holdings

# ============================================
# PRICES ENDPOINTS
# ============================================

@app.get("/api/v1/prices/latest")
async def get_latest_prices():
    """Obtiene precios actuales de todos los activos (mock data)"""
    return {
        "VOO": 470.50,
        "VGT": 510.25,
        "BTC": 45000.00,
        "ETH": 2500.00,
        "timestamp": "2025-10-31T14:00:00"
    }

@app.get("/api/v1/prices/{ticker}")
async def get_price(ticker: str):
    """Obtiene precio actual de un ticker especifico"""
    prices = {
        "VOO": 470.50,
        "VGT": 510.25,
        "BTC": 45000.00,
        "ETH": 2500.00
    }
    
    price = prices.get(ticker.upper())
    if not price:
        return {"error": f"Ticker {ticker} no encontrado"}
    
    return {
        "ticker": ticker.upper(),
        "price": price,
        "timestamp": "2025-10-31T14:00:00"
    }

# ============================================
# ANALYTICS ENDPOINTS
# ============================================

@app.get("/api/v1/analytics/summary")
async def get_analytics_summary(portfolio_id: int = 1):
    """Resumen analitico del portfolio (mock data)"""
    return {
        "portfolio_id": portfolio_id,
        "total_value": 27500.00,
        "total_cost": 25000.00,
        "total_gain": 2500.00,
        "total_gain_percent": 10.0,
        "distribution": {
            "VOO": {"value": 4705.00, "percent": 17.1, "target": 40.0},
            "VGT": {"value": 2551.25, "percent": 9.3, "target": 30.0},
            "BTC": {"value": 22500.00, "percent": 81.8, "target": 20.0},
            "ETH": {"value": 5000.00, "percent": 18.2, "target": 10.0}
        },
        "by_asset_type": {
            "stock": 26.4,
            "crypto": 73.6
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
