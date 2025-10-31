# 📦 Guía de Instalación - Portfolio Tracker (Windows)

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

### 1. Python 3.11 o superior

```powershell
# Verificar instalación
python --version

# Debería mostrar: Python 3.11.x o superior
```

**Si no está instalado:**
1. Descargar de https://www.python.org/downloads/
2. Durante la instalación, marcar "Add Python to PATH"
3. Verificar con: `python --version`

### 2. Node.js 18 o superior

```powershell
# Verificar instalación
node --version
npm --version
```

**Si no está instalado:**
1. Descargar de https://nodejs.org/
2. Instalar la versión LTS
3. Verificar con: `node --version`

### 3. Git (Opcional, recomendado)

```powershell
# Verificar instalación
git --version
```

**Si no está instalado:**
- Descargar de https://git-scm.com/download/win

---

## 🚀 Instalación Rápida (Método Recomendado)

### Opción A: Con Script Automático

1. **Abrir PowerShell como Administrador**
   - Presiona `Win + X`
   - Selecciona "Windows PowerShell (Admin)"

2. **Navegar al directorio del proyecto**
   ```powershell
   cd C:\Users\TuUsuario\Documents\portfolio-tracker
   ```

3. **Ejecutar el script de setup**
   ```powershell
   .\scripts\setup_windows.ps1
   ```

   **Nota:** Si obtienes un error de "execution policy", ejecuta:
   ```powershell
   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
   ```

4. **¡Listo!** El script instalará todo automáticamente

---

## 🔧 Instalación Manual (Paso a Paso)

Si prefieres instalar manualmente o el script automático falla:

### Paso 1: Configurar Backend

```powershell
# Navegar a la carpeta del backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo .env
copy ..\.env.example .env

# Inicializar base de datos
python -c "import asyncio; from app.core.database import init_db; asyncio.run(init_db())"
```

### Paso 2: Configurar Frontend

```powershell
# Navegar a la carpeta del frontend
cd ../frontend

# Instalar dependencias
npm install

# Verificar instalación
npm run dev -- --version
```

### Paso 3: Verificar Instalación

```powershell
# Backend
cd ../backend
.\venv\Scripts\Activate.ps1
python -c "from app.core.config import settings; print(f'Backend OK - {settings.APP_NAME}')"

# Frontend
cd ../frontend
npm list react
```

Si todos los comandos funcionan sin errores, ¡instalación exitosa!

---

## ▶️ Iniciar la Aplicación

### Método 1: Inicio Automático (Recomendado)

```powershell
# Desde la raíz del proyecto
.\scripts\start_dev.ps1
```

Esto abrirá dos ventanas de PowerShell:
- Una para el backend (API)
- Una para el frontend (UI)

### Método 2: Inicio Manual

**Terminal 1 - Backend:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```powershell
cd frontend
npm run dev
```

---

## 🌐 Acceder a la Aplicación

Una vez iniciado:

- **Dashboard (UI):** http://localhost:5173
- **API Backend:** http://localhost:8000
- **API Docs (Swagger):** http://localhost:8000/docs
- **API Docs (ReDoc):** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

---

## 🧪 Verificar que Todo Funciona

### 1. Verificar Backend

```powershell
# En PowerShell
curl http://localhost:8000/health

# Debería retornar:
# {"status":"healthy","app":"Portfolio Tracker API","version":"1.0.0"}
```

### 2. Verificar Frontend

- Abrir navegador en http://localhost:5173
- Deberías ver la interfaz del Portfolio Tracker

### 3. Verificar API Docs

- Abrir http://localhost:8000/docs
- Deberías ver la documentación interactiva de Swagger

---

## ❌ Solución de Problemas Comunes

### Problema: "python no se reconoce como comando"

**Solución:**
1. Verifica que Python esté instalado
2. Agrega Python al PATH:
   - Busca "Variables de entorno" en Windows
   - Edita "Path" en variables del sistema
   - Agrega: `C:\Users\TuUsuario\AppData\Local\Programs\Python\Python311`

### Problema: "pip no se reconoce como comando"

**Solución:**
```powershell
python -m pip --version
# Usa "python -m pip" en lugar de solo "pip"
```

### Problema: Error al activar entorno virtual

**Solución:**
```powershell
# Permitir scripts
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

# Activar de nuevo
.\venv\Scripts\Activate.ps1
```

### Problema: "node no se reconoce como comando"

**Solución:**
1. Reinicia PowerShell después de instalar Node.js
2. Verifica instalación: `node --version`
3. Si persiste, reinstala Node.js marcando "Add to PATH"

### Problema: Puerto 8000 o 5173 en uso

**Solución:**
```powershell
# Ver qué proceso usa el puerto
netstat -ano | findstr :8000

# Matar el proceso (reemplaza PID con el número mostrado)
taskkill /PID [PID] /F

# O cambiar puerto en .env:
# PORT=8001
```

### Problema: Error de CORS en frontend

**Solución:**
1. Verificar que backend esté corriendo en puerto 8000
2. Verificar `CORS_ORIGINS` en `.env` incluya `http://localhost:5173`
3. Reiniciar backend después de cambiar `.env`

### Problema: Base de datos no se crea

**Solución:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python

# En Python:
>>> import asyncio
>>> from app.core.database import init_db
>>> asyncio.run(init_db())
>>> exit()
```

---

## 🔄 Actualizar el Sistema

```powershell
# Actualizar dependencias de Python
cd backend
.\venv\Scripts\Activate.ps1
pip install --upgrade -r requirements.txt

# Actualizar dependencias de Node.js
cd ../frontend
npm update

# Si hay cambios en la DB
cd ../backend
alembic upgrade head
```

---

## 🛑 Detener la Aplicación

- Presiona `Ctrl + C` en cada terminal
- O cierra las ventanas de PowerShell

---

## 📁 Estructura de Archivos Importante

```
portfolio-tracker/
├── backend/
│   ├── app/                    # Código de la aplicación
│   ├── venv/                   # Entorno virtual (creado al instalar)
│   ├── requirements.txt        # Dependencias Python
│   ├── .env                    # Configuración (crear desde .env.example)
│   └── portfolio_tracker.db   # Base de datos SQLite (creado automáticamente)
├── frontend/
│   ├── src/                    # Código React
│   ├── node_modules/           # Dependencias Node (creado al instalar)
│   └── package.json            # Configuración frontend
├── scripts/
│   ├── setup_windows.ps1       # Script de instalación
│   └── start_dev.ps1           # Script de inicio
└── .env.example                # Template de configuración
```

---

## 🎯 Próximos Pasos

Después de la instalación exitosa:

1. **Crear tu primer portfolio**
   - Abre http://localhost:5173
   - Click en "Nuevo Portfolio"
   - Nombra tu portfolio (ej: "Mi Cubeta 1")

2. **Agregar tus holdings**
   - Click en "Agregar Holding"
   - Ingresa: ticker (VOO), cantidad (0.85), precio promedio (490)
   - Repetir para cada activo

3. **Ver el dashboard**
   - Los precios se actualizarán automáticamente
   - Verás gráficas y métricas en tiempo real

---

## 📚 Recursos Adicionales

- **Documentación de API:** http://localhost:8000/docs
- **Código fuente:** `./backend/app/` y `./frontend/src/`
- **Logs:** `./logs/`
- **Base de datos:** `./backend/portfolio_tracker.db`

---

## 💡 Tips para Desarrollo

```powershell
# Ver logs del backend en tiempo real
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --log-level debug

# Limpiar cache del frontend
cd frontend
npm run build
```

---

¿Necesitas ayuda? Revisa la documentación completa en `./docs/`
