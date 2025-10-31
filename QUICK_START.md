# 🚀 INICIO RÁPIDO - Portfolio Tracker

## ⚡ 3 PASOS SIMPLES

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  PASO 1: INSTALAR (Primera vez - 15 minutos)               │
│                                                             │
│  📁 Abrir PowerShell en esta carpeta                        │
│  ⌨️  Escribir: .\setup.ps1                                  │
│  ⏳ Esperar a que termine                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  PASO 2: INICIAR (Uso diario - 10 segundos)                │
│                                                             │
│  🖱️  Doble-click en:                                        │
│      START_PORTFOLIO_TRACKER.ps1                            │
│                                                             │
│  ⏳ Esperar 10 segundos                                     │
│  🌐 Se abre el navegador automáticamente                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  PASO 3: USAR                                               │
│                                                             │
│  ✅ Ver tu dashboard                                        │
│  ✅ Revisar ganancias/pérdidas                              │
│  ✅ Actualizar precios                                      │
│  ✅ Cambiar entre portafolios                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  PARA DETENER:                                              │
│                                                             │
│  🖱️  Doble-click en:                                        │
│      STOP_PORTFOLIO_TRACKER.ps1                             │
│                                                             │
│  O simplemente cierra las ventanas de PowerShell           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 ARCHIVOS IMPORTANTES

```
portfolio-tracker/
│
├─ 🟢 START_PORTFOLIO_TRACKER.ps1  ← INICIAR SISTEMA
├─ 🔴 STOP_PORTFOLIO_TRACKER.ps1   ← DETENER SISTEMA
├─ ⚙️  setup.ps1                    ← Instalación (solo 1ra vez)
│
├─ 📖 GUIA_ACCESO_DIARIO.md        ← Guía completa de uso
├─ 📖 INSTALLATION_GUIDE.md        ← Guía de instalación
├─ 📖 ARCHITECTURE.md              ← Documentación técnica
│
├─ 📁 backend/                     ← Código del servidor
└─ 📁 frontend/                    ← Código de la interface
```

---

## 🎯 LO QUE VERÁS

### Cuando ejecutes START_PORTFOLIO_TRACKER.ps1:

```
Se abren 3 ventanas:

┌─────────────────────┐
│ Ventana 1: CONTROL  │  ← Puedes minimizar
│ (Negra)             │
└─────────────────────┘

┌─────────────────────┐
│ Ventana 2: BACKEND  │  ← NO cerrar
│ (Azul)              │
└─────────────────────┘

┌─────────────────────┐
│ Ventana 3: FRONTEND │  ← NO cerrar
│ (Verde)             │
└─────────────────────┘

┌─────────────────────┐
│ Navegador           │  ← AQUÍ USAS EL SISTEMA
│ localhost:5173      │
└─────────────────────┘
```

---

## ❓ PREGUNTAS RÁPIDAS

**¿Es como abrir un HTML?**
❌ No, necesitas "iniciar el servidor" primero (doble-click en START)

**¿Necesito VS Code abierto?**
❌ No, el script lo hace todo automáticamente

**¿Necesito internet?**
⚠️  Solo para actualizar precios. Ver portfolio funciona sin internet.

**¿Mi esposa puede usarlo?**
✅ Sí, solo necesita hacer doble-click en START

**¿Puedo dejarlo corriendo todo el día?**
✅ Sí, consume muy pocos recursos

**¿Qué hago si algo sale mal?**
📖 Leer: GUIA_ACCESO_DIARIO.md (sección Troubleshooting)

---

## 🆘 AYUDA RÁPIDA

**Error: "No se puede ejecutar script"**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Error: "Puerto 8000 en uso"**
```powershell
# Ejecutar STOP primero
.\STOP_PORTFOLIO_TRACKER.ps1
# Luego START de nuevo
.\START_PORTFOLIO_TRACKER.ps1
```

**No abre el navegador automáticamente**
```
Abrir manualmente: http://localhost:5173
```

---

## 💡 TIPS

✅ Crea un acceso directo en tu escritorio a START_PORTFOLIO_TRACKER.ps1
✅ Puedes minimizar las ventanas azul/verde (pero NO cerrarlas)
✅ Bookmark http://localhost:5173 en tu navegador
✅ El sistema guarda todo automáticamente

---

## 📞 MÁS INFORMACIÓN

- **Uso diario**: Ver `GUIA_ACCESO_DIARIO.md`
- **Instalación completa**: Ver `INSTALLATION_GUIDE.md`
- **Arquitectura**: Ver `ARCHITECTURE.md`
- **API Docs**: http://localhost:8000/docs (cuando esté corriendo)

---

## ✅ CHECKLIST

Primera vez:
- [ ] Ejecuté setup.ps1
- [ ] Probé START_PORTFOLIO_TRACKER.ps1
- [ ] Vi el dashboard en el navegador
- [ ] Probé STOP_PORTFOLIO_TRACKER.ps1

Listo para usar diariamente:
- [ ] Creé acceso directo en escritorio
- [ ] Guardé bookmark del dashboard
- [ ] Leí la guía de acceso diario

---

**¡Eso es todo! Es más simple de lo que parece.** 🎉

**Resumen:** Doble-click → Esperar → Usar → Cerrar ✅
