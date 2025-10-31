# 🏗️ Arquitectura del Sistema - Portfolio Tracker

## 📐 Principios Arquitectónicos

Este sistema fue diseñado siguiendo principios de arquitectura profesional:

### Principios SOLID

1. **Single Responsibility Principle (SRP)**
   - Cada clase/módulo tiene UNA responsabilidad
   - Ejemplo: `PriceFetcher` solo obtiene precios, `Calculator` solo calcula valores

2. **Open/Closed Principle (OCP)**
   - Abierto a extensión, cerrado a modificación
   - Nuevos price providers se agregan sin cambiar código existente

3. **Liskov Substitution Principle (LSP)**
   - Interfaces bien definidas (IPriceProvider)
   - Cualquier implementación es intercambiable

4. **Interface Segregation Principle (ISP)**
   - Interfaces específicas, no genéricas
   - Clientes no dependen de métodos que no usan

5. **Dependency Inversion Principle (DIP)**
   - Dependencias en abstracciones, no concreciones
   - Services dependen de IRepository, no de implementación específica

### Otros Principios

- **DRY (Don't Repeat Yourself)**: BaseRepository elimina código duplicado
- **KISS (Keep It Simple, Stupid)**: Soluciones simples sobre complejas
- **YAGNI (You Aren't Gonna Need It)**: No construimos lo que no necesitamos

---

## 🏛️ Arquitectura de Capas

```
┌─────────────────────────────────────────────────────────┐
│                 PRESENTATION LAYER                       │
│              (React + TypeScript)                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │Dashboard │  │Portfolio │  │Settings  │              │
│  │Component │  │Component │  │Component │              │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘              │
└───────┼─────────────┼─────────────┼─────────────────────┘
        │             │             │ HTTP/REST
┌───────┼─────────────┼─────────────┼─────────────────────┐
│       ▼             ▼             ▼  API LAYER           │
│              (FastAPI + Pydantic)                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │Portfolio │  │Price     │  │Analytics │              │
│  │Router    │  │Router    │  │Router    │              │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘              │
└───────┼─────────────┼─────────────┼─────────────────────┘
        │             │             │
┌───────┼─────────────┼─────────────┼─────────────────────┐
│       ▼             ▼             ▼  SERVICE LAYER       │
│              (Business Logic)                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │Portfolio │  │Price     │  │Calculator│              │
│  │Service   │  │Service   │  │Service   │              │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘              │
└───────┼─────────────┼─────────────┼─────────────────────┘
        │             │             │
┌───────┼─────────────┼─────────────┼─────────────────────┐
│       ▼             ▼             ▼  REPOSITORY LAYER    │
│              (Data Access)                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │Portfolio │  │Price     │  │Transaction               │
│  │Repo      │  │Repo      │  │Repo       │              │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘              │
└───────┼─────────────┼─────────────┼─────────────────────┘
        │             │             │
┌───────┼─────────────┼─────────────┼─────────────────────┐
│       ▼             ▼             ▼  DATA LAYER          │
│                (SQLite/PostgreSQL)                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │portfolios│  │prices    │  │transactions              │
│  │holdings  │  │exchange  │  │           │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└─────────────────────────────────────────────────────────┘

EXTERNAL SERVICES (APIs)
┌─────────────────────────────────────────────────────────┐
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │Yahoo     │  │CoinGecko │  │Exchange  │              │
│  │Finance   │  │API       │  │Rate API  │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 Modelo de Datos

### Diagrama ER

```
┌─────────────┐
│ Portfolio   │
├─────────────┤
│ id (PK)     │
│ name        │
│ description │
│ is_active   │
│ target_allocation  │
│ created_at  │
│ updated_at  │
└──────┬──────┘
       │ 1
       │
       │ N
┌──────▼──────┐          ┌─────────────┐
│  Holding    │          │ Transaction │
├─────────────┤          ├─────────────┤
│ id (PK)     │          │ id (PK)     │
│ portfolio_id│◄─────────┤ portfolio_id│
│ ticker      │          │ type        │
│ asset_type  │          │ ticker      │
│ quantity    │          │ quantity    │
│ average_cost│          │ price       │
│ platform    │          │ date        │
│ created_at  │          │ created_at  │
└─────────────┘          └─────────────┘

┌─────────────┐          ┌───────────────┐
│   Price     │          │ ExchangeRate  │
├─────────────┤          ├───────────────┤
│ id (PK)     │          │ id (PK)       │
│ ticker      │          │ from_currency │
│ price_usd   │          │ to_currency   │
│ source      │          │ rate          │
│ timestamp   │          │ timestamp     │
│ volume      │          │ source        │
│ market_cap  │          └───────────────┘
└─────────────┘
```

### Relaciones

- **Portfolio 1:N Holding**: Un portfolio tiene múltiples holdings
- **Portfolio 1:N Transaction**: Un portfolio tiene múltiples transacciones
- **Price**: Tabla independiente con histórico de precios
- **ExchangeRate**: Tabla independiente con histórico de tipos de cambio

---

## 🔄 Flujo de Datos

### 1. Actualización de Precios (Automático)

```
┌──────────────────────────────────────────────────────────┐
│                  PRICE FETCHER WORKER                     │
│                  (Corre cada hora)                        │
└────────────────────┬─────────────────────────────────────┘
                     │
         ┌───────────▼───────────┐
         │ Get unique tickers    │
         │ from all holdings     │
         └───────────┬───────────┘
                     │
         ┌───────────▼───────────┐
         │ Classify by type      │
         │ ETF: VOO, VGT         │
         │ Crypto: BTC, ETH      │
         └───────────┬───────────┘
                     │
         ┌───────────▼───────────┬───────────┐
         │                       │           │
    ┌────▼─────┐         ┌──────▼──────┐   ┌▼───────────┐
    │  Yahoo   │         │  CoinGecko  │   │  Exchange  │
    │ Finance  │         │     API     │   │  Rate API  │
    └────┬─────┘         └──────┬──────┘   └┬───────────┘
         │                      │             │
         └──────────┬───────────┴─────────────┘
                    │
         ┌──────────▼─────────────┐
         │  Save to DB:           │
         │  - prices table        │
         │  - exchange_rates      │
         └────────────────────────┘
```

### 2. Cálculo de Valor del Portfolio

```
USER REQUEST: Get portfolio value
         │
         ▼
┌────────────────────┐
│ API Endpoint       │
│ GET /portfolios/1  │
└─────────┬──────────┘
          │
          ▼
┌─────────────────────────┐
│ PortfolioService        │
│ - Get portfolio by ID   │
│ - Get all holdings      │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────────────┐
│ For each holding:               │
│ 1. Get latest price from DB     │
│ 2. Get latest exchange rate     │
│ 3. Calculate value:             │
│    value_mxn = quantity ×       │
│                price_usd ×      │
│                exchange_rate    │
│ 4. Calculate gain/loss          │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────┐
│ Aggregate:              │
│ - Total value           │
│ - Total invested        │
│ - Total gain/loss       │
│ - Percentage gain       │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ Return JSON response    │
└─────────────────────────┘
```

---

## 🛠️ Patrones de Diseño Utilizados

### 1. Repository Pattern

**Propósito**: Separar lógica de negocio del acceso a datos

**Implementación**:
```python
class IRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: int): ...
    
class PortfolioRepository(IRepository):
    async def get_by_id(self, id: int) -> Portfolio:
        # Implementación específica
```

**Beneficios**:
- Cambiar DB (SQLite → PostgreSQL) sin cambiar lógica
- Facilita testing (mock repositories)
- Código más limpio y organizado

### 2. Factory Pattern

**Propósito**: Crear instancias de price providers dinámicamente

**Implementación**:
```python
class PriceProviderFactory:
    @staticmethod
    def get_provider(asset_type: str) -> IPriceProvider:
        if asset_type in ["stock", "etf"]:
            return YahooFinanceProvider()
        elif asset_type == "crypto":
            return CoinGeckoProvider()
```

**Beneficios**:
- Fácil agregar nuevos providers
- Lógica de selección centralizada

### 3. Strategy Pattern

**Propósito**: Diferentes estrategias para obtener precios

**Implementación**:
```python
class IPriceProvider(ABC):
    @abstractmethod
    async def get_price(self, ticker: str): ...

class YahooFinanceProvider(IPriceProvider): ...
class CoinGeckoProvider(IPriceProvider): ...
```

**Beneficios**:
- Intercambiable en runtime
- Fácil agregar nuevas estrategias

### 4. Dependency Injection

**Propósito**: Inversión de dependencias

**Implementación**:
```python
@router.get("/portfolios/{id}")
async def get_portfolio(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    service = PortfolioService(db)
    return await service.get_by_id(id)
```

**Beneficios**:
- Desacoplamiento
- Testeable
- Flexible

---

## 🚀 Decisiones de Arquitectura y Trade-offs

### SQLite vs PostgreSQL

**Decisión**: SQLite inicialmente, con path a PostgreSQL

**Razones**:
- ✅ Zero configuración en Windows
- ✅ Portátil (un archivo)
- ✅ Suficiente para 100,000+ registros
- ✅ Migrations con Alembic permiten migrar después

**Trade-offs**:
- ⚠️ No ideal para >50 usuarios concurrentes
- ⚠️ Sin replicación nativa
- ✅ Pero para uso personal es perfecto

**Escalabilidad**:
- 1-10 usuarios: SQLite ✅
- 50+ usuarios: Migrar a PostgreSQL (cambio de 1 línea en .env)

### Monolito vs Microservicios

**Decisión**: Monolito modular

**Razones**:
- ✅ Simple deployment
- ✅ Desarrollo más rápido
- ✅ Debugging más fácil
- ✅ Suficiente para 1-100 usuarios

**Trade-offs**:
- ⚠️ Escala vertical, no horizontal
- ⚠️ Un punto de falla
- ✅ Pero código modular permite migrar a microservicios después

### REST vs GraphQL

**Decisión**: REST API

**Razones**:
- ✅ Simple, estándar
- ✅ Cacheable con HTTP
- ✅ Tooling maduro

**Trade-offs**:
- ⚠️ Puede requerir múltiples requests
- ⚠️ Over/under fetching
- ✅ Pero para este caso REST es suficiente

---

## 📈 Escalabilidad

### Escenario 1: 1 Usuario (Actual)

```
SQLite Local
├─ 0 configuración
├─ Backup con simple copy
└─ Performance excelente
```

### Escenario 2: 5-10 Usuarios (Familia)

```
SQLite en NAS/Shared Drive
├─ Múltiples usuarios leen
├─ Sincronización automática
└─ Sin cambios de código
```

### Escenario 3: 50-100 Usuarios

```
Migración a PostgreSQL
├─ Cambiar DATABASE_URL en .env
├─ Run migrations: alembic upgrade head
├─ Deploy en VPS (DigitalOcean, Railway)
└─ Sin cambios de código
```

### Escenario 4: 1000+ Usuarios

```
Arquitectura Cloud (Nivel 3)
├─ Backend: Railway/Vercel
├─ DB: Supabase/PostgreSQL
├─ Cache: Redis/Upstash
├─ CDN: Cloudflare
└─ Requiere refactor mínimo
```

---

## 🔐 Seguridad

### Arquitectura Zero-Trust con Exchanges

```
❌ NO nos conectamos a:
   ├─ GBM
   ├─ Bitso
   └─ Ningún exchange

✅ Solo usamos:
   ├─ Yahoo Finance (precios públicos)
   ├─ CoinGecko (precios públicos)
   └─ ExchangeRate API (público)

🔒 Beneficios:
   ├─ Zero riesgo de seguridad
   ├─ No se requieren credenciales
   └─ 100% compliance
```

### Input Validation

- Pydantic valida todos los inputs
- SQL injection prevention (SQLAlchemy ORM)
- CORS configurado restrictivamente
- Rate limiting en providers

---

## 🧪 Testing Strategy

```
Unit Tests (pytest)
├─ Repositories
├─ Services
├─ Providers
└─ Utils

Integration Tests
├─ API endpoints
├─ Database operations
└─ External API calls

End-to-End Tests (Vitest)
├─ User flows
├─ Dashboard interactions
└─ CRUD operations
```

---

## 📝 Logging y Monitoring

### Structured Logging

```python
logger.info(
    "portfolio_created",
    portfolio_id=portfolio.id,
    user_id=user.id,
    holdings_count=len(holdings)
)
```

### Health Checks

- `/health`: Application health
- Database connectivity
- External API availability

---

## 🔄 CI/CD Pipeline (Futuro)

```
GitHub Actions
├─ On Push to main:
│  ├─ Run tests
│  ├─ Build Docker images
│  ├─ Deploy to staging
│  └─ Run E2E tests
└─ On Tag:
   ├─ Deploy to production
   └─ Create release notes
```

---

## 📚 Recursos Adicionales

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org/
- **React Docs**: https://react.dev/
- **Clean Architecture**: Robert C. Martin

---

Esta arquitectura está diseñada para:
- ✅ Fácil mantenimiento
- ✅ Escalabilidad incremental
- ✅ Testing completo
- ✅ Deploy simple
- ✅ Evolución sin rewrites completos
