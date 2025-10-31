# 🚀 Guía de Instalación y Uso - Windows

## 📋 Tabla de Contenidos
1. [Prerrequisitos](#prerrequisitos)
2. [Instalación](#instalación)
3. [Configuración](#configuración)
4. [Ejecución](#ejecución)
5. [Uso Básico](#uso-básico)
6. [Arquitectura del Sistema](#arquitectura)
7. [Troubleshooting](#troubleshooting)

---

## 📦 Prerrequisitos

### Software Requerido

1. **Python 3.11+**
   - Descargar desde: https://www.python.org/downloads/
   - Durante instalación: ✅ Marcar "Add Python to PATH"

2. **Node.js 18+**
   - Descargar desde: https://nodejs.org/
   - Incluye npm automáticamente

3. **VS Code** (Recomendado)
   - Descargar desde: https://code.visualstudio.com/
   - Extensiones recomendadas:
     - Python
     - Pylance
     - ESLint
     - Prettier

4. **Git** (Opcional)
   - Descargar desde: https://git-scm.com/download/win

5. **Docker Desktop** (Opcional - para deployment con contenedores)
   - Descargar desde: https://www.docker.com/products/docker-desktop/

### Verificar Instalación

Abrir PowerShell y ejecutar:

```powershell
# Verificar Python
python --version
# Debe mostrar: Python 3.11.x o superior

# Verificar Node.js
node --version
# Debe mostrar: v18.x.x o superior

# Verificar npm
npm --version
# Debe mostrar: 9.x.x o superior
```

---

## 🔧 Instalación

### Opción 1: Instalación Automatizada (Recomendada)

1. **Abrir PowerShell**
   - Presionar `Win + X`
   - Seleccionar "Windows PowerShell"

2. **Navegar al directorio del proyecto**
   ```powershell
   cd C:\Ruta\A\portfolio-tracker
   ```

3. **Ejecutar script de instalación**
   ```powershell
   .\setup.ps1
   ```

   Si aparece error de política de ejecución:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   .\setup.ps1
   ```

4. **Esperar a que termine** (~5-10 minutos)

### Opción 2: Instalación Manual

#### A. Backend

```powershell
# 1. Navegar a backend
cd backend

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
.\venv\Scripts\Activate.ps1

# 4. Actualizar pip
python -m pip install --upgrade pip

# 5. Instalar dependencias
pip install -r requirements.txt

# 6. Copiar configuración
copy .env.example .env

# 7. Crear directorio de logs
mkdir logs

# 8. Volver al directorio raíz
cd ..
```

#### B. Frontend

```powershell
# 1. Navegar a frontend
cd frontend

# 2. Instalar dependencias
npm install

# 3. Volver al directorio raíz
cd ..
```

---

## ⚙️ Configuración

### 1. Configurar Backend (.env)

Editar archivo `backend/.env`:

```env
# Aplicación
APP_NAME="Portfolio Tracker"
DEBUG=True
ENVIRONMENT=development

# Base de datos
DATABASE_URL=sqlite+aiosqlite:///./portfolio_tracker.db

# Actualización de precios
PRICE_UPDATE_INTERVAL_MINUTES=60
ENABLE_AUTO_PRICE_UPDATES=True

# Logging
LOG_LEVEL=INFO
```

### 2. Configurar Frontend

Crear archivo `frontend/.env.local`:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

---

## ▶️ Ejecución

### Opción 1: Manual (Dos Terminales)

#### Terminal 1 - Backend

```powershell
# Navegar a backend
cd backend

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Iniciar servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Verás:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

#### Terminal 2 - Frontend

```powershell
# Navegar a frontend
cd frontend

# Iniciar desarrollo
npm run dev
```

Verás:
```
VITE v5.0.2  ready in 500 ms

➜  Local:   http://localhost:5173/
➜  Network: http://192.168.1.x:5173/
```

### Opción 2: Docker Compose (Una Terminal)

```powershell
# Desde directorio raíz
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

---

## 🎯 Uso Básico

### 1. Primera Ejecución

1. **Abrir navegador en**: http://localhost:5173

2. **Crear primer portafolio**
   - Click en "Crear Primer Portafolio"
   - Nombre: "Mi Portafolio Cubeta 1"
   - Distribución:
     - VOO: 35%
     - VGT: 35%
     - BTC: 15%
     - ETH: 15%
   - Click "Crear"

### 2. Agregar Holdings (Posiciones)

Actualmente los holdings están hardcodeados para demo. En producción:

```python
# Ejemplo de API call (desde consola del navegador)
fetch('http://localhost:8000/api/v1/holdings', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    portfolio_id: 1,
    ticker: 'VOO',
    quantity: 0.85,
    average_buy_price: 490.00,
    asset_type: 'stock',
    platform: 'GBM'
  })
})
```

### 3. Actualizar Precios

- Click en botón "🔄 Actualizar" en el header
- O llamar directamente al API:
  ```bash
  curl -X POST http://localhost:8000/api/v1/prices/refresh
  ```

### 4. Ver Documentación de API

Abrir en navegador:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🏗️ Arquitectura del Sistema

### Flujo de Datos

```
Frontend (React)
    ↓ HTTP Request
API Gateway (FastAPI)
    ↓ Service Layer
Business Logic (Services)
    ↓ Repository Pattern
Database (SQLite)

Paralelo:
Price Fetcher (Background)
    ↓ APIs Externas
Yahoo Finance / CoinGecko
    ↓ Store
Database (Prices Table)
```

### Estructura de Directorios

```
portfolio-tracker/
├── backend/
│   ├── app/
│   │   ├── api/              # Endpoints REST
│   │   ├── core/             # Configuración
│   │   ├── db/               # Database setup
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   ├── providers/        # External APIs
│   │   └── main.py           # Entry point
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/              # API client
│   │   ├── components/       # React components
│   │   ├── pages/            # Pages
│   │   └── main.tsx          # Entry point
│   └── package.json
└── docker-compose.yml
```

### Patrones de Diseño Aplicados

- **Repository Pattern**: Abstracción de acceso a datos
- **Service Layer**: Lógica de negocio separada
- **Dependency Injection**: FastAPI Depends()
- **Factory Pattern**: Creación de price providers
- **Strategy Pattern**: Múltiples price sources

---

## 🐛 Troubleshooting

### Problema: "python no reconocido"

**Solución**:
1. Reinstalar Python marcando "Add to PATH"
2. O agregar manualmente a PATH:
   - Buscar "Variables de entorno"
   - Editar PATH
   - Agregar: `C:\Users\TuUsuario\AppData\Local\Programs\Python\Python311`

### Problema: "pip install falla"

**Solución**:
```powershell
# Actualizar pip
python -m pip install --upgrade pip

# Si falla con SSL
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

### Problema: "Cannot find module 'vite'"

**Solución**:
```powershell
cd frontend
rm -r node_modules
rm package-lock.json
npm install
```

### Problema: "Puerto 8000 ya en uso"

**Solución**:
```powershell
# Ver qué usa el puerto
netstat -ano | findstr :8000

# Matar proceso (reemplazar PID)
taskkill /PID 12345 /F

# O usar otro puerto
uvicorn app.main:app --port 8001
```

### Problema: "CORS error en navegador"

**Solución**:
1. Verificar que backend está corriendo
2. Verificar `BACKEND_CORS_ORIGINS` en `.env`
3. Debe incluir: `http://localhost:5173`

### Problema: "SQLite locked database"

**Solución**:
```powershell
# Cerrar todas las conexiones
cd backend
rm portfolio_tracker.db
python -c "from app.db.session import init_db; import asyncio; asyncio.run(init_db())"
```

---

## 📚 Recursos Adicionales

- **Documentación FastAPI**: https://fastapi.tiangolo.com/
- **Documentación React**: https://react.dev/
- **Documentación SQLAlchemy**: https://docs.sqlalchemy.org/
- **Yahoo Finance API**: https://pypi.org/project/yfinance/
- **CoinGecko API**: https://www.coingecko.com/en/api

---

## 🤝 Soporte

Si encuentras problemas:

1. Revisar logs:
   - Backend: `backend/logs/app.log`
   - Frontend: Consola del navegador (F12)

2. Verificar que todas las dependencias estén instaladas

3. Reiniciar ambos servicios

4. Si persiste, crear issue con:
   - Sistema operativo y versión
   - Python version
   - Node version
   - Logs completos del error
