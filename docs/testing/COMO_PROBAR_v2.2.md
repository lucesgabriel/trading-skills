# 🧪 Cómo Probar Pattern Scanner v2.2

## 🚀 Test Rápido (Recomendado)

### En Nueva Sesión de Claude Code

```bash
# Abrir nueva sesión de Claude Code
# Ejecutar:
> scan EURUSD
```

**Resultado Esperado**:
```
✅ Fetch MCP data
✅ Create temp_scan.py
✅ Execute scanner
✅ Pattern detection (ej: 16 patterns)
✅ HTML report generated
✅ Cleanup temp_scan.py
✅ Results displayed
```

---

## 🔍 Verificar el Flujo Paso a Paso

### 1. Verificar que temp_scan.py se crea

Después de ejecutar `scan EURUSD`, verifica:

```bash
# Durante ejecución (antes de cleanup)
ls .claude/skills/pattern-scanner/scripts/temp_scan.py

# Debería existir temporalmente
```

### 2. Verificar el contenido (opcional)

Si quieres ver cómo se ve el script:

```bash
# Mantener temp_scan.py (comentar cleanup en SKILL.md temporalmente)
cat .claude/skills/pattern-scanner/scripts/temp_scan.py
```

Deberías ver:
```python
#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from run_scan import run_pattern_scan

mcp_data = {
    "price": {"bid": 1.16381, ...},
    "candles_m15": """time,open,high,low,close,...
    99,2025-10-29 21:30:00+00:00,1.16392,1.16426,1.16375,1.1638,606,0,0
    ...""",
    ...
}

report_path = run_pattern_scan("EURUSD", mcp_data)
```

### 3. Verificar el reporte HTML

```bash
# Listar reportes generados
ls -lh reports/EURUSD*.html | head -3

# Abrir el más reciente
# Debería tener diseño vibrante (purple/violet)
```

---

## 🎨 Verificar Diseño Vibrante

Al abrir el HTML report, verifica:

- ✅ Gradiente de fondo purple/violet
- ✅ Pattern cards con emojis (🔥 🔨 🌅)
- ✅ Chart.js interactive
- ✅ 3 secciones nuevas:
  - ⚠️ Risk Management
  - 🚨 Warnings
  - 📝 Executive Summary

---

## 🐛 Si Hay Problemas

### Problema: temp_scan.py no se crea

**Causa**: Write tool failing
**Solución**: Verificar permisos de escritura en `.claude/skills/pattern-scanner/scripts/`

### Problema: SyntaxError en temp_scan.py

**Causa**: CSV strings mal escapados
**Solución**: Verificar que se usen triple quotes `"""..."""`

### Problema: Module not found

**Causa**: sys.path.insert incorrecto
**Solución**: Verificar que temp_scan.py esté en el directorio correcto

### Problema: Cleanup falla

**Causa**: Comando del/rm según plataforma
**Solución**: Verificar OS y usar comando apropiado

---

## 📊 Test con Otros Símbolos

Una vez que funciona con EURUSD, probar:

```bash
> scan GBPUSD
> scan XAUUSD
> scan USDJPY
```

Todos deberían funcionar con el mismo flujo.

---

## 🔬 Test Avanzado (Opcional)

### Ejecutar example_temp_scan.py

```bash
# Test del flujo con datos de ejemplo
python example_temp_scan.py
```

**Output esperado**:
```
============================================================
EJEMPLO: Ejecutando pattern scanner con datos embebidos
============================================================

📊 Escaneando EURUSD para patrones de velas...
💰 Precio actual: 1.16381
✓ M15: 100 velas cargadas
...
✅ Scan complete! Report: reports/EURUSD_pattern_scan_XXXXXX.html
```

---

## ✅ Checklist de Validación

- [ ] Ejecutar `scan EURUSD` en nueva sesión
- [ ] Verificar que no hay errores de Write tool
- [ ] Verificar que no hay errores de heredoc
- [ ] Verificar que temp_scan.py se crea temporalmente
- [ ] Verificar que el scanner ejecuta correctamente
- [ ] Verificar que se genera reporte HTML
- [ ] Verificar que temp_scan.py se elimina (cleanup)
- [ ] Verificar diseño vibrante en HTML
- [ ] Probar con otros símbolos (GBPUSD, XAUUSD)

Si todos los items pasan: **✅ v2.2 VALIDADO!**

---

## 🎉 Resultado Esperado Final

```
> scan EURUSD

● I'll scan EURUSD for candlestick patterns...
● Fetched MCP data ✅
● Created temp_scan.py ✅
● Pattern detection complete ✅
● HTML report generated ✅

📊 Results:
- Patterns detected: 16
- Signal: SHORT (SELL) - BEARISH
- Probability: 62.1%
- Report: reports/EURUSD_pattern_scan_20251029_213045.html

✅ Success!
```

---

**🎨 Happy Testing!** 📊

*Pattern Scanner v2.2 - Testing Guide*
