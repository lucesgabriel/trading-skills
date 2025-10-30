# Phase 2 Instructions - Anthropic Best Practices (Continuación)

## 📋 Estado Actual del Proyecto

### ✅ Completado - Fase 1 (Mejoras Críticas)

**Commits subidos a GitHub:**
- `e1f616f` - Phase 1: Implement Anthropic best practices for Claude Code skills
- `312374f` - Fix: Correct pattern-scanner execution documentation
- `b135e50` - Fix: Use temp file method as primary execution approach
- `c15dfec` - Fix: Add explicit code template for pattern-scanner execution

**Mejoras implementadas:**
1. ✅ Refactorización YAML descriptions (6 skills) - 150-300 chars → 100-150 chars
2. ✅ Creación de 5 slash commands (/scan, /analyze, /risk, /opportunities, /backtest)
3. ✅ Optimización de tokens pattern-scanner (36% reducción)
4. ✅ Estandarización secciones "When to Use" (6 skills)
5. ✅ Documentación corregida con templates explícitos

**Nivel de cumplimiento:** 70% → 85% best practices de Anthropic

---

## 🎯 Fase 2 - Mejoras Avanzadas (Media Prioridad)

**Objetivo:** Mejorar la experiencia de usuario y mantenibilidad del proyecto.

**Tiempo estimado:** 6-8 horas

**Beneficios:**
- Workflows más claros para usuarios
- Mensajes de error más profesionales
- Mejor documentación para contribuidores
- Metadata estructurada para futuras mejoras

---

## 📝 Tareas de la Fase 2

### 1. Skill Composition Workflows (3 horas)

**Objetivo:** Documentar cómo los skills trabajan juntos en workflows completos de trading.

#### Archivo a crear: `.claude/skills/WORKFLOWS.md`

```markdown
# Skill Composition Workflows

Workflows completos que combinan múltiples skills para análisis profesional.

## 🎯 Workflow Completo de Trading

### 1. Descubrimiento (opportunity-scanner)
**Comando:** `/opportunities`
**Propósito:** Encontrar los mejores setups del día
**Output:** Lista rankeada de símbolos con probabilidades

### 2. Análisis Profundo (technical-analysis + pattern-scanner)
**Comandos:**
```
/analyze EURUSD
/scan EURUSD
```
**Propósito:** Validar señal con indicadores y patrones
**Output:** Confluencia de señales técnicas

### 3. Gestión de Riesgo (risk-management)
**Comando:** `/risk EURUSD entry:1.0850 stop:1.0820`
**Propósito:** Calcular tamaño de posición óptimo
**Output:** Lot size, riesgo en $, R:R ratio

### 4. Validación Histórica (backtesting)
**Comando:** `/backtest "Bullish Engulfing + RSI < 30"`
**Propósito:** Verificar que la estrategia funciona
**Output:** Win rate, profit factor, drawdown

### 5. Métricas Avanzadas (advanced-analytics)
**Comando:** "calculate Sharpe ratio for last month"
**Propósito:** Evaluar desempeño ajustado por riesgo
**Output:** Sharpe, Sortino, Calmar ratios

## 📊 Workflows por Caso de Uso

### Swing Trading Setup
1. `/opportunities` - Buscar swing setups
2. `/analyze [SYMBOL]` - Confirmar tendencia D1/W1
3. `/risk [SYMBOL]` - Calcular posición con stop amplio
4. Ejecutar trade manualmente

### Day Trading Setup
1. `/scan [SYMBOL]` - Patrones en M15/H1
2. `/analyze [SYMBOL]` - Validar con RSI/MACD
3. `/risk [SYMBOL]` - Stop tight, posición más grande
4. Ejecutar con límites de tiempo

### Strategy Development
1. Idea → Definir reglas claras
2. `/backtest "strategy"` - Probar en histórico
3. Optimizar parámetros si win rate < 50%
4. `/backtest` nuevamente en otro símbolo
5. Paper trading 1 mes antes de real

## 🔄 Skill Dependencies

```
opportunity-scanner
    ↓
technical-analysis ← pattern-scanner
    ↓
risk-management
    ↓
[TRADE EXECUTION]
    ↓
advanced-analytics (post-trade review)
```

## 💡 Tips de Workflow

- **No saltarse risk-management** - Siempre calcular posición antes de operar
- **Usar confluencia** - Combinar technical-analysis + pattern-scanner
- **Backtest primero** - Nunca operar estrategia sin validar
- **Review regular** - Usar advanced-analytics cada semana
```

**Pasos para implementar:**
1. Crear archivo `.claude/skills/WORKFLOWS.md`
2. Copiar contenido anterior y expandir con más ejemplos
3. Agregar diagramas de flujo si es posible (usando ASCII art o Mermaid)
4. Documentar errores comunes en workflows

---

### 2. Enhanced Error Handling (2 horas)

**Objetivo:** Códigos de error estructurados para diagnóstico más rápido.

#### Archivo a crear: `.claude/skills/ERROR_CODES.md`

```markdown
# Error Codes Reference

Sistema de códigos de error para todos los skills del proyecto trading-skills.

## Format
`ERR_[SKILL]_[NUMBER]: [Description]`

## Pattern Scanner (ERR_PS_xxx)

### ERR_PS_001: Insufficient Candle Data
**Causa:** MCP retornó menos de 50 velas para un timeframe
**Solución:**
- Verificar que MetaTrader esté conectado
- Solicitar más historia en MetaTrader (Tools → History Center)
- Reducir `minCandles` en la configuración
**Mensaje al usuario:**
```
❌ ERR_PS_001: Datos insuficientes para M15 (solo 30 velas, se requieren 50+)
💡 Solución: Descarga más historia en MetaTrader (Tools → History Center)
```

### ERR_PS_002: Invalid Symbol
**Causa:** Símbolo no disponible en el broker
**Solución:**
- Verificar spelling (EURUSD no EUR/USD)
- Confirmar que broker soporta el símbolo
- Ver símbolos disponibles con `mcp__metatrader__get_all_symbols`
**Mensaje al usuario:**
```
❌ ERR_PS_002: Símbolo 'EURUSDD' no encontrado
💡 ¿Quisiste decir 'EURUSD'? Símbolos disponibles: ...
```

### ERR_PS_003: MCP Connection Failed
**Causa:** MetaTrader no está ejecutándose o MCP server no responde
**Solución:**
- Verificar que MetaTrader 5 esté abierto
- Reiniciar MCP server
- Verificar configuración en `.claude/settings.local.json`
**Mensaje al usuario:**
```
❌ ERR_PS_003: No se puede conectar a MetaTrader
💡 Pasos:
   1. Abre MetaTrader 5
   2. Reinicia Claude Code
   3. Verifica configuración MCP en settings
```

## Technical Analysis (ERR_TA_xxx)

### ERR_TA_001: Indicator Calculation Failed
**Causa:** Datos insuficientes para calcular indicador
**Solución:**
- MACD requiere mínimo 34 velas
- RSI requiere mínimo 14 velas
- MA 200 requiere mínimo 200 velas
**Mensaje al usuario:**
```
❌ ERR_TA_001: No se puede calcular MA200 (solo 100 velas disponibles)
💡 Usa timeframe mayor (H4/D1) o reduce periodo del indicador
```

## Risk Management (ERR_RM_xxx)

### ERR_RM_001: Insufficient Account Balance
**Causa:** Balance muy bajo para el riesgo solicitado
**Solución:**
- Reducir lot size
- Aumentar stop loss (menor riesgo por pip)
- Depositar más fondos
**Mensaje al usuario:**
```
❌ ERR_RM_001: Riesgo de $500 excede balance de $1000
💡 Máximo recomendado: $20 (2% de $1000)
   Considera reducir posición a 0.1 lots
```

### ERR_RM_002: Risk:Reward Too Low
**Causa:** R:R ratio menor a 1:1.5
**Solución:**
- Ampliar take profit
- Reducir stop loss (si es técnicamente válido)
- Buscar otro setup
**Mensaje al usuario:**
```
⚠️ ERR_RM_002: R:R de 1:0.8 es muy bajo (mínimo 1:1.5)
💡 Ajustar: TP de 30 pips → 45+ pips para R:R aceptable
```

## Backtesting (ERR_BT_xxx)

### ERR_BT_001: Insufficient Historical Data
**Causa:** No hay suficientes velas para backtest significativo
**Solución:**
- Descargar más historia
- Usar timeframe mayor
- Reducir periodo de prueba
**Mensaje al usuario:**
```
❌ ERR_BT_001: Solo 50 trades encontrados (mínimo: 100)
💡 Opciones:
   - Extender periodo: 3 meses → 6 meses
   - Usar timeframe menor: D1 → H4
```

### ERR_BT_002: Strategy Undefined
**Causa:** Reglas de estrategia no están claras
**Solución:**
- Definir condiciones de entrada exactas
- Especificar reglas de salida
- Incluir filtros si aplican
**Mensaje al usuario:**
```
❌ ERR_BT_002: Estrategia "comprar cuando sube" es muy vaga
💡 Ejemplo claro: "Comprar cuando RSI < 30 Y precio toca MA50"
```

## Advanced Analytics (ERR_AA_xxx)

### ERR_AA_001: No Trade History
**Causa:** No hay trades para analizar
**Solución:**
- Ejecutar algunos trades primero
- Importar historial de MetaTrader
**Mensaje al usuario:**
```
❌ ERR_AA_001: No hay trades para calcular Sharpe ratio
💡 Ejecuta al menos 10 trades o importa historial
```

## General Errors (ERR_GEN_xxx)

### ERR_GEN_001: Timeout
**Causa:** Operación tardó más de 2 minutos
**Solución:**
- Reducir cantidad de datos
- Verificar conexión a internet
**Mensaje al usuario:**
```
❌ ERR_GEN_001: Operación cancelada por timeout (> 2min)
💡 Intenta con menos símbolos o periodo más corto
```

## 📝 Implementación en Skills

Actualizar cada skill para usar estos códigos:

```python
# En scripts/run_scan.py
def validate_data(candles):
    if len(candles) < 50:
        raise InsufficientDataError(
            "ERR_PS_001",
            f"Solo {len(candles)} velas disponibles (se requieren 50+)"
        )
```

## 🎨 Formato de Mensajes de Error

**Template estándar:**
```
❌ [ERROR_CODE]: [Descripción breve]
📊 Detalles: [Info específica del error]
💡 Solución: [Pasos concretos para resolver]
🔗 Más info: [Link a documentación si aplica]
```
```

**Pasos para implementar:**
1. Crear `.claude/skills/ERROR_CODES.md`
2. Agregar códigos de error para cada skill
3. (Opcional) Actualizar scripts Python para usar códigos
4. Referenciar desde troubleshooting.md de cada skill

---

### 3. Add YAML Metadata (1 hora)

**Objetivo:** Metadata estructurada para futuras funcionalidades.

#### Actualizar 6 SKILL.md files

**Antes:**
```yaml
---
name: pattern-scanner
description: Use when detecting candlestick patterns...
---
```

**Después:**
```yaml
---
name: pattern-scanner
description: Use when detecting candlestick patterns, scanning forex symbols for trading signals, or analyzing chart formations across multiple timeframes.
version: 2.2.1
tags: [trading, patterns, candlestick, forex, technical-analysis, reversal]
category: market-analysis
requires:
  mcp:
    - mcp__metatrader__get_symbol_price
    - mcp__metatrader__get_candles_latest
  skills:
    - technical-analysis
difficulty: intermediate
estimated_time: 30-60s
output_format: [console, html]
author: Gabriel Luces
repository: https://github.com/lucesgabriel/trading-skills
---
```

**Campos recomendados:**
- `version`: Versión del skill (seguir semantic versioning)
- `tags`: Para búsqueda y categorización
- `category`: market-analysis | risk-management | strategy-validation | analytics
- `requires`: Dependencias (MCP servers, otros skills)
- `difficulty`: beginner | intermediate | advanced
- `estimated_time`: Tiempo promedio de ejecución
- `output_format`: Tipo de output generado
- `author`: Creador del skill
- `repository`: Link al repo

**Pasos para implementar:**
1. Actualizar pattern-scanner/SKILL.md primero
2. Aplicar mismo formato a los otros 5 skills
3. Verificar que YAML sea válido (usar parser online)

---

### 4. Create Discovery Guide (2 horas)

**Objetivo:** Ayudar a nuevos usuarios a entender cómo Claude selecciona skills.

#### Archivo a crear: `.claude/skills/DISCOVERY.md`

```markdown
# Skill Discovery Guide

Cómo Claude Code descubre y selecciona el skill correcto para tu solicitud.

## 🔍 Proceso de Selección de Skills

### 1. Análisis de Intent (Usuario → Claude)

Cuando escribes:
```
"scan EURUSD for patterns"
```

Claude analiza:
- **Keywords:** "scan", "patterns"
- **Symbol:** "EURUSD"
- **Context:** Trading, technical analysis

### 2. Matching de Skills (Claude → SKILL.md)

Claude lee los YAML frontmatter de todos los skills:

```yaml
# pattern-scanner
description: Use when detecting candlestick patterns...

# technical-analysis
description: Use when analyzing market trends...

# opportunity-scanner
description: Use when finding the best trading opportunities...
```

Match encontrado: **pattern-scanner** (keyword: "scan", "patterns")

### 3. Loading del Skill (SKILL.md → Memoria)

Claude carga en memoria:
- SKILL.md completo (~2,700 tokens)
- "When to Use This Skill" section
- Execution Instructions

### 4. Ejecución del Workflow

Claude sigue las instrucciones del SKILL.md:
1. Fetch market data (MCP calls)
2. Create temp script
3. Execute scanner
4. Report results

## 📊 Cómo Mejorar el Matching

### ✅ Usar Palabras Clave Claras

**Bien:**
- "scan EURUSD for patterns" → pattern-scanner ✓
- "analyze GBPUSD trend" → technical-analysis ✓
- "calculate position size" → risk-management ✓

**Mal (ambiguo):**
- "check EURUSD" → ¿pattern-scanner? ¿technical-analysis?
- "look at market" → ¿opportunity-scanner? ¿technical-analysis?

### ✅ Usar Slash Commands

Eliminan ambigüedad completamente:
- `/scan EURUSD` → pattern-scanner (garantizado)
- `/analyze EURUSD` → technical-analysis (garantizado)
- `/opportunities` → opportunity-scanner (garantizado)

### ✅ Ser Específico con Requirements

"I want to trade EURUSD" → Muy vago

Mejor:
"Scan EURUSD for reversal patterns, then calculate position size with 1% risk"

Claude ejecutará:
1. pattern-scanner
2. risk-management

## 🎯 Skill Selection Decision Tree

```
User Input
    │
    ├─ Contains "scan" / "pattern"?
    │   YES → pattern-scanner
    │   NO → Continue
    │
    ├─ Contains "analyze" / "trend" / "indicator"?
    │   YES → technical-analysis
    │   NO → Continue
    │
    ├─ Contains "best" / "opportunities" / "what to trade"?
    │   YES → opportunity-scanner
    │   NO → Continue
    │
    ├─ Contains "risk" / "position size" / "lot size"?
    │   YES → risk-management
    │   NO → Continue
    │
    ├─ Contains "backtest" / "test strategy" / "historical"?
    │   YES → backtesting
    │   NO → Continue
    │
    └─ Contains "Sharpe" / "correlation" / "Monte Carlo"?
        YES → advanced-analytics
        NO → Ask user for clarification
```

## 🔧 Debugging Skill Selection

Si Claude selecciona el skill incorrecto:

### Opción 1: Reformular Request
❌ "check EURUSD"
✅ "scan EURUSD for candlestick patterns"

### Opción 2: Usar Slash Command
✅ `/scan EURUSD`

### Opción 3: Ser Explícito
✅ "Use the pattern-scanner skill to analyze EURUSD"

## 📚 Skill Descriptions Cheat Sheet

**pattern-scanner:**
"Use when detecting candlestick patterns..."
Keywords: scan, pattern, candlestick, reversal, formation

**technical-analysis:**
"Use when analyzing market trends..."
Keywords: analyze, trend, indicator, RSI, MACD, signal

**opportunity-scanner:**
"Use when finding the best trading opportunities..."
Keywords: opportunities, best, what to trade, market scan

**risk-management:**
"Use when calculating position sizes..."
Keywords: risk, position size, lot size, stop loss

**backtesting:**
"Use when validating trading strategies..."
Keywords: backtest, test strategy, historical, win rate

**advanced-analytics:**
"Use when analyzing performance metrics..."
Keywords: Sharpe, correlation, Sortino, Monte Carlo

## 💡 Pro Tips

1. **Slash commands son más rápidos** - Use `/scan` en vez de escribir full sentence
2. **Encadena skills explícitamente** - "First scan EURUSD, then calculate risk"
3. **Un skill a la vez** - Claude ejecuta mejor con instrucciones claras
4. **Revisa output de cada skill** - Antes de pasar al siguiente
```

**Pasos para implementar:**
1. Crear `.claude/skills/DISCOVERY.md`
2. Agregar ejemplos reales de tus sesiones
3. Incluir capturas de pantalla si es posible
4. Referenciar desde README principal

---

## 📦 Checklist de Implementación Fase 2

```
[ ] 1. Skill Composition Workflows
    [ ] Crear .claude/skills/WORKFLOWS.md
    [ ] Documentar 5+ workflows completos
    [ ] Añadir diagramas de flujo
    [ ] Ejemplos de cada caso de uso

[ ] 2. Enhanced Error Handling
    [ ] Crear .claude/skills/ERROR_CODES.md
    [ ] Definir códigos para pattern-scanner (5+)
    [ ] Definir códigos para technical-analysis (3+)
    [ ] Definir códigos para risk-management (3+)
    [ ] Definir códigos para backtesting (2+)
    [ ] Definir códigos para advanced-analytics (2+)
    [ ] Template de mensajes de error
    [ ] (Opcional) Implementar en scripts Python

[ ] 3. Add YAML Metadata
    [ ] Actualizar pattern-scanner/SKILL.md
    [ ] Actualizar technical-analysis/SKILL.md
    [ ] Actualizar opportunity-scanner/SKILL.md
    [ ] Actualizar risk-management/SKILL.md
    [ ] Actualizar backtesting/SKILL.md
    [ ] Actualizar advanced-analytics/SKILL.md
    [ ] Validar YAML en todos los archivos

[ ] 4. Create Discovery Guide
    [ ] Crear .claude/skills/DISCOVERY.md
    [ ] Documentar proceso de selección
    [ ] Decision tree
    [ ] Tips de debugging
    [ ] Cheat sheet de keywords

[ ] 5. Testing & Validation
    [ ] Probar cada workflow documentado
    [ ] Verificar que códigos de error sean claros
    [ ] Validar YAML metadata
    [ ] Revisar discovery guide con ejemplos reales

[ ] 6. Documentation Updates
    [ ] Actualizar README principal
    [ ] Actualizar IMPROVEMENTS_PHASE1.md → IMPROVEMENTS.md
    [ ] Crear IMPROVEMENTS_PHASE2.md
    [ ] Commit y push cambios
```

---

## 🚀 Cómo Comenzar la Fase 2 en Nueva Sesión

### Paso 1: Verificar Estado Actual

```bash
cd "D:\Programing Language html css js php DB\28102025"
git status
git log --oneline -5
```

Deberías ver:
```
c15dfec Fix: Add explicit code template for pattern-scanner execution
b135e50 Fix: Use temp file method as primary execution approach
312374f Fix: Correct pattern-scanner execution documentation
e1f616f Phase 1: Implement Anthropic best practices for Claude Code skills
```

### Paso 2: Crear Rama para Fase 2 (Opcional pero Recomendado)

```bash
git checkout -b phase2-enhancements
```

### Paso 3: Comenzar con Workflows

```bash
# Crear archivo
code .claude/skills/WORKFLOWS.md

# O pedirle a Claude Code:
"Create .claude/skills/WORKFLOWS.md with skill composition workflows based on PHASE2_INSTRUCTIONS.md"
```

### Paso 4: Trabajar Tarea por Tarea

1. Completar WORKFLOWS.md (3 horas)
2. Commit: `git commit -m "Add skill composition workflows documentation"`
3. Completar ERROR_CODES.md (2 horas)
4. Commit: `git commit -m "Add structured error code system"`
5. Actualizar YAML metadata (1 hora)
6. Commit: `git commit -m "Add metadata to all SKILL.md frontmatter"`
7. Completar DISCOVERY.md (2 horas)
8. Commit: `git commit -m "Add skill discovery guide"`

### Paso 5: Finalizar Fase 2

```bash
# Merge a main
git checkout main
git merge phase2-enhancements

# Push
git push origin main
```

---

## 💡 Tips para la Fase 2

1. **No es urgente** - Fase 1 ya tiene el 85% de best practices
2. **Prioriza calidad** - Mejor documentación clara que rápida
3. **Usa ejemplos reales** - De tus propias sesiones de trading
4. **Prueba workflows** - Antes de documentarlos
5. **Pide feedback** - A otros usuarios si es posible

---

## 📊 Resultado Esperado Fase 2

**Antes Fase 2:** 85% compliance
**Después Fase 2:** 90-95% compliance

**Mejoras adicionales:**
- ✅ Workflows documentados para nuevos usuarios
- ✅ Errores más claros y accionables
- ✅ Metadata para futuras features
- ✅ Guía de discovery para troubleshooting

**Tiempo total invertido:**
- Fase 1: ~8 horas
- Fase 2: ~8 horas
- **Total: ~16 horas para proyecto best-in-class**

---

## 🎯 Fase 3 (Opcional - Baja Prioridad)

Si después de Fase 2 quieres llegar al 95%+:

1. **Tests de integración** - Validar que workflows funcionen
2. **Skill packaging** - Sistema de distribución
3. **Performance metrics** - Tracking de uso y tiempos
4. **Multi-idioma** - Soporte para ES/EN
5. **Video tutorials** - Demos de workflows

**Tiempo estimado Fase 3:** 8-10 horas

---

## 📞 Soporte

Si tienes dudas durante Fase 2:
- GitHub Issues: https://github.com/lucesgabriel/trading-skills/issues
- Anthropic Docs: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview
- Este documento: `PHASE2_INSTRUCTIONS.md`

---

**Última actualización:** 2025-10-30
**Versión:** 1.0
**Autor:** Claude Code Assistant
