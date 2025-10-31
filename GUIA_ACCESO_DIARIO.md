# 🖥️ GUÍA DE ACCESO DIARIO - Portfolio Tracker

## 📋 RESUMEN EJECUTIVO

**¿Cómo funciona el acceso?**

```
Portfolio Tracker NO es un archivo HTML estático ❌
Portfolio Tracker ES una aplicación web que necesita "servidores" corriendo ✅

Similar a:
  ✅ Usar Excel (doble-click para abrir)
  ✅ Usar Spotify Desktop (se inicia y se minimiza)
  ✅ Usar una base de datos local
  
NO similar a:
  ❌ Abrir un HTML guardado
  ❌ Abrir un PDF
  ❌ Ver una imagen
```

---

## 🎯 OPCIÓN 1: SCRIPT DE UN CLICK (⭐ RECOMENDADA)

### **Flujo de Uso Diario**

```
┌──────────────────────────────────────────────────┐
│  LUNES 8:00 AM - Quieres revisar tu portfolio   │
└──────────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────────┐
│  1. Ir a la carpeta del proyecto                 │
│     C:\Users\TuUsuario\portfolio-tracker\        │
└──────────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────────┐
│  2. DOBLE-CLICK en:                              │
│     START_PORTFOLIO_TRACKER.ps1                  │
└──────────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────────┐
│  3. Esperar 10 segundos                          │
│     - Se abren 2 ventanas de PowerShell         │
│     - Se abre automáticamente tu navegador      │
└──────────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────────┐
│  4. ¡LISTO! Usar el Dashboard                    │
│     Ya puedes ver tu portfolio                   │
└──────────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────────┐
│  5. Cuando termines:                             │
│     - Cerrar navegador                           │
│     - DOBLE-CLICK: STOP_PORTFOLIO_TRACKER.ps1    │
│     O simplemente cerrar las 2 ventanas PS       │
└──────────────────────────────────────────────────┘
```

### **Qué Verás:**

#### **Paso 1: Doble-click en START_PORTFOLIO_TRACKER.ps1**

```
Tu Explorador de Archivos:

📁 portfolio-tracker/
  ├─ 📄 START_PORTFOLIO_TRACKER.ps1  ← DOBLE-CLICK AQUÍ ⭐
  ├─ 📄 STOP_PORTFOLIO_TRACKER.ps1
  ├─ 📄 setup.ps1
  ├─ 📄 README.md
  ├─ 📁 backend/
  └─ 📁 frontend/
```

#### **Paso 2: Se abren 3 ventanas**

```
Ventana 1: PowerShell (NEGRA) - Control
┌─────────────────────────────────────────┐
│ 📊 PORTFOLIO TRACKER - INICIANDO...     │
│                                         │
│ [1/4] Verificando instalación... ✓     │
│ [2/4] Iniciando Backend...       ✓     │
│ [3/4] Iniciando Frontend...      ✓     │
│ [4/4] Abriendo navegador...      ✓     │
│                                         │
│ ✅ SISTEMA INICIADO EXITOSAMENTE       │
│                                         │
│ 📊 Dashboard:     localhost:5173        │
│ 📖 API Docs:      localhost:8000/docs   │
│                                         │
│ Presiona cualquier tecla para           │
│ minimizar esta ventana...               │
└─────────────────────────────────────────┘

Ventana 2: PowerShell (AZUL) - Backend
┌─────────────────────────────────────────┐
│ 🐍 BACKEND API - Puerto 8000            │
│                                         │
│ INFO: Uvicorn running on 0.0.0.0:8000  │
│ INFO: Application startup complete      │
│ INFO: Waiting for requests...           │
│                                         │
│ ⚠️  NO CERRAR ESTA VENTANA             │
└─────────────────────────────────────────┘

Ventana 3: PowerShell (VERDE) - Frontend
┌─────────────────────────────────────────┐
│ ⚛️  FRONTEND REACT - Puerto 5173        │
│                                         │
│ VITE v5.0.2  ready in 500 ms            │
│                                         │
│ ➜  Local:   http://localhost:5173/     │
│ ➜  Network: http://192.168.1.x:5173/   │
│                                         │
│ ⚠️  NO CERRAR ESTA VENTANA             │
└─────────────────────────────────────────┘

Ventana 4: Navegador (Chrome/Edge)
┌─────────────────────────────────────────┐
│ http://localhost:5173                   │
├─────────────────────────────────────────┤
│                                         │
│  📊 Portfolio Tracker                   │
│  ────────────────────────────────       │
│                                         │
│  Portafolio: [Carlos - Cubeta 1 ▼]     │
│                                         │
│  💰 Valor Total: $127,450 USD           │
│  📈 Ganancia: +$12,450 (+10.85%)        │
│                                         │
│  [Gráfica de distribución]              │
│  [Tabla de activos]                     │
│                                         │
└─────────────────────────────────────────┘
```

#### **Paso 3: Uso Normal**

```
✅ Puedes:
  • Navegar en el dashboard
  • Cambiar de portafolio
  • Actualizar precios
  • Ver gráficas
  • Minimizar el navegador
  • Hacer otras cosas en tu PC

⚠️  NO Cerres:
  • Ventana AZUL (Backend)
  • Ventana VERDE (Frontend)
  
✅ Sí puedes minimizarlas
```

#### **Paso 4: Detener el Sistema**

**Opción A: Script automático**
```
Doble-click en: STOP_PORTFOLIO_TRACKER.ps1

Resultado:
┌─────────────────────────────────────────┐
│ 🛑 PORTFOLIO TRACKER - DETENIENDO...    │
│                                         │
│ Buscando procesos activos...           │
│                                         │
│ 📍 Encontrados 2 procesos de Backend    │
│   ✓ Proceso Backend detenido           │
│                                         │
│ 📍 Encontrados 1 proceso de Frontend    │
│   ✓ Proceso Frontend detenido          │
│                                         │
│ ✅ Sistema detenido exitosamente        │
└─────────────────────────────────────────┘
```

**Opción B: Manual**
```
1. Cerrar ventana AZUL (Backend)
2. Cerrar ventana VERDE (Frontend)
3. Cerrar ventana NEGRA (Control) - opcional
```

---

## 🖱️ CREAR ACCESO DIRECTO EN ESCRITORIO

### **Para acceso más rápido:**

**Paso 1: Crear acceso directo**
```
1. Click derecho en START_PORTFOLIO_TRACKER.ps1
2. Seleccionar "Crear acceso directo"
3. Arrastrar el acceso directo al Escritorio
4. (Opcional) Renombrar a "Portfolio Tracker"
```

**Paso 2: Cambiar ícono (Opcional)**
```
1. Click derecho en acceso directo → Propiedades
2. Pestaña "Acceso directo" → Botón "Cambiar icono"
3. Seleccionar un ícono de gráfica/finanzas
4. Aplicar → OK
```

**Resultado:**
```
Tu Escritorio:

┌─────────────┐
│   📊 💰     │
│             │
│  Portfolio  │
│   Tracker   │
└─────────────┘
      ↑
  DOBLE-CLICK
  para iniciar
```

---

## 🎯 OPCIÓN 2: DESDE VS CODE

### **Para Desarrollo / Debugging**

**Cuándo usar:**
- Estás modificando el código
- Quieres ver logs detallados
- Debugging de errores

**Cómo usar:**

```
1. Abrir VS Code
2. File → Open Folder → portfolio-tracker
3. Abrir 2 terminales integradas:

Terminal 1 (Backend):
  cd backend
  .\venv\Scripts\Activate.ps1
  uvicorn app.main:app --reload

Terminal 2 (Frontend):
  cd frontend
  npm run dev

4. Abrir http://localhost:5173 en navegador
```

**Ventaja:**
- ✅ Ver código mientras usas el sistema
- ✅ Logs más detallados
- ✅ Auto-reload cuando cambias código

**Desventaja:**
- ⚠️  Requiere VS Code abierto
- ⚠️  Más pasos que el script

---

## 🐳 OPCIÓN 3: DOCKER DESKTOP (UN CLICK)

### **Setup Inicial (Una sola vez)**

```powershell
# 1. Instalar Docker Desktop
# Descargar desde: https://www.docker.com/products/docker-desktop/

# 2. Abrir PowerShell en la carpeta del proyecto
cd C:\...\portfolio-tracker

# 3. Construir contenedores (primera vez - tarda 5-10 min)
docker-compose build
```

### **Uso Diario:**

**Iniciar:**
```powershell
docker-compose up -d
```

**Ver en navegador:**
```
http://localhost:5173
```

**Detener:**
```powershell
docker-compose down
```

**Ventajas:**
- ✅ Un solo comando
- ✅ Aislamiento completo
- ✅ Fácil hacer backup
- ✅ Portable a otros PCs

**Desventajas:**
- ⚠️  Requiere Docker Desktop corriendo
- ⚠️  Usa más recursos (RAM)
- ⚠️  Setup inicial más complejo

---

## ⚙️ OPCIÓN 4: SERVICIO DE WINDOWS (AVANZADO)

### **Sistema se inicia automáticamente con Windows**

**Setup (Una sola vez):**

```powershell
# Crear tarea programada
schtasks /create /tn "Portfolio Tracker" /tr "C:\...\START_PORTFOLIO_TRACKER.ps1" /sc onlogon /ru SYSTEM
```

**Resultado:**
```
✅ Sistema inicia automáticamente al encender PC
✅ Siempre disponible en http://localhost:5173
✅ No necesitas hacer nada

⚠️  Usa recursos constantemente
⚠️  Solo recomendado si lo usas TODOS los días
```

---

## ☁️ OPCIÓN 5: SERVIDOR EN LA NUBE (PROFESIONAL)

### **Acceso desde cualquier lugar**

**Deployment en Railway/Vercel:**

```bash
# Una sola vez
railway login
railway up

# Resultado:
# URL: https://portfolio-tracker-tuusuario.railway.app
```

**Ventajas:**
- ✅ Acceso desde cualquier dispositivo
- ✅ Celular, tablet, otro PC
- ✅ Siempre disponible 24/7
- ✅ No usa recursos de tu PC

**Desventajas:**
- ⚠️  Costo mensual ($5-20 USD)
- ⚠️  Requiere internet
- ⚠️  Setup más complejo

---

## 🔄 COMPARACIÓN DE OPCIONES

| Opción | Facilidad | Costo | Acceso | Recursos |
|--------|-----------|-------|--------|----------|
| **1. Script Doble-Click** | ⭐⭐⭐⭐⭐ | Gratis | Local | Bajo |
| **2. VS Code** | ⭐⭐⭐⭐ | Gratis | Local | Bajo |
| **3. Docker** | ⭐⭐⭐ | Gratis | Local | Medio |
| **4. Servicio Windows** | ⭐⭐ | Gratis | Local | Medio |
| **5. Cloud** | ⭐⭐ | $5-20/mes | Global | Ninguno |

---

## 💡 RECOMENDACIÓN POR USO

### **Para ti y tu esposa (Uso personal):**

```
✅ MEJOR OPCIÓN: Script Doble-Click

Por qué:
  • Más fácil para usuarios no técnicos
  • Tu esposa puede iniciarlo sin problemas
  • Cero costo
  • Datos privados en tu PC
  • Funciona sin internet

Crear acceso directo en el escritorio de ambos usuarios
```

### **Si lo usas diariamente TODO el día:**

```
✅ MEJOR OPCIÓN: Servicio de Windows

Por qué:
  • Se inicia automáticamente
  • Siempre disponible
  • Un bookmark en el navegador
  • Como usar Gmail (siempre está ahí)
```

### **Si quieres acceso desde trabajo/celular:**

```
✅ MEJOR OPCIÓN: Cloud Deployment

Por qué:
  • Acceso desde cualquier lugar
  • Sincronización automática
  • No depende de tu PC
```

---

## 📱 FLUJO TÍPICO DE USO

### **Escenario 1: Revisión Matutina (5 minutos)**

```
8:00 AM - Desayunando
  ↓
1. Doble-click: START_PORTFOLIO_TRACKER.ps1
   (10 segundos para iniciar)
  ↓
2. Navegar a http://localhost:5173
   (ya abre automáticamente)
  ↓
3. Revisar portfolio
   - Ver ganancias del día
   - Comparar con esposa
   - Actualizar precios
  ↓
4. Cerrar navegador
   (dejar sistema corriendo)
  ↓
8:05 AM - Seguir con tu día
```

### **Escenario 2: Día de Inversión (30 minutos)**

```
Día 5 del mes - Día de inversión
  ↓
1. Sistema ya corriendo desde la mañana
   O iniciar con doble-click
  ↓
2. Comprar en GBM/Bitso
  ↓
3. Abrir Portfolio Tracker
  ↓
4. Registrar transacciones:
   POST /api/v1/transactions
   {
     "ticker": "VOO",
     "quantity": 0.08,
     "price": 520.00,
     ...
   }
  ↓
5. Ver portfolio actualizado
  ↓
6. Dejar corriendo hasta la noche
```

### **Escenario 3: Fin del Día**

```
10:00 PM - Antes de dormir
  ↓
1. Última revisión en navegador
  ↓
2. Cerrar navegador
  ↓
3. Doble-click: STOP_PORTFOLIO_TRACKER.ps1
   O simplemente apagar PC (se cierra solo)
```

---

## ⚠️ PREGUNTAS FRECUENTES

### **P: ¿Por qué no es como un HTML simple?**

```
R: Porque el sistema tiene 3 partes:

1. BACKEND (Python/FastAPI)
   - Conecta con APIs externas
   - Calcula ganancias/pérdidas
   - Maneja base de datos
   
2. FRONTEND (React)
   - Interface visual
   - Gráficas interactivas
   - Componentes dinámicos
   
3. BASE DE DATOS (SQLite)
   - Almacena tus datos
   - Histórico de precios
   - Transacciones

Un HTML estático no puede hacer APIs calls ni
conectarse a base de datos.
```

### **P: ¿Puedo dejar el sistema corriendo todo el día?**

```
R: SÍ, totalmente seguro.

✅ Consume muy pocos recursos:
   • Backend: ~100MB RAM
   • Frontend: ~50MB RAM
   • Total: menos que Chrome con 3 tabs

✅ No hace nada cuando no lo usas
   (solo actualiza precios cada hora)

✅ Puedes minimizar las ventanas
```

### **P: ¿Qué pasa si cierro el navegador?**

```
R: El sistema sigue corriendo en background.

Solo cierra la interface visual.
Backend y Frontend siguen activos.

Para volver a verlo:
  Abrir http://localhost:5173 en navegador
```

### **P: ¿Necesito internet?**

```
R: Depende de qué quieras hacer:

SIN INTERNET:
  ✅ Ver portfolio con últimos precios
  ✅ Navegar en el dashboard
  ✅ Ver gráficas históricas

CON INTERNET:
  ✅ Actualizar precios en vivo
  ✅ Obtener datos de Yahoo Finance
  ✅ Obtener datos de CoinGecko
```

### **P: ¿Mi esposa puede usarlo al mismo tiempo?**

```
R: Depende del setup:

OPCIÓN 1 (Script local):
  ⚠️  Solo uno a la vez
  Si ella inicia en su usuario de Windows,
  creará otra instancia (puerto diferente)
  
  Mejor: Compartir misma sesión de Windows
  O usar perfil de usuario diferente

OPCIÓN 5 (Cloud):
  ✅ Ambos simultáneamente
  Cada uno desde su dispositivo
```

---

## ✅ CHECKLIST DE PRIMERA VEZ

```
Primera vez usando el sistema:

□ 1. Ejecutaste setup.ps1 (instalación)
□ 2. Verificaste que backend/venv existe
□ 3. Verificaste que frontend/node_modules existe
□ 4. Creaste acceso directo en escritorio
□ 5. Probaste START_PORTFOLIO_TRACKER.ps1
□ 6. Viste las 3 ventanas abrir
□ 7. Navegador abrió automáticamente
□ 8. Dashboard cargó correctamente
□ 9. Probaste STOP_PORTFOLIO_TRACKER.ps1
□ 10. Todo se cerró correctamente

¡Listo para uso diario! 🚀
```

---

## 🎯 RESUMEN: TU SETUP RECOMENDADO

```
┌────────────────────────────────────────────┐
│  SETUP RECOMENDADO PARA TI Y TU ESPOSA    │
└────────────────────────────────────────────┘

📍 Ubicación:
   C:\Users\Compartido\portfolio-tracker\

📍 Escritorio:
   Acceso directo → START_PORTFOLIO_TRACKER.ps1
   Ícono: 📊💰

📍 Uso diario:
   1. Doble-click ícono en escritorio
   2. Esperar 10 segundos
   3. Usar dashboard
   4. Al terminar: Doble-click STOP o cerrar ventanas

📍 Frecuencia:
   • Revisión matutina: 5 min
   • Día de inversión: 30 min
   • Revisión semanal: 15 min

📍 Responsables:
   • Ambos pueden iniciar/detener
   • Datos compartidos
   • Portafolios separados pero visibles
```

---

**¿Todo claro? ¡Es más fácil de lo que parece!** 🎉

En resumen: **Doble-click → Esperar 10 seg → Usar dashboard** ✅
