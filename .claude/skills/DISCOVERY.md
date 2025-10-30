# Skill Discovery Guide

Cómo Claude Code descubre y selecciona el skill correcto para tu solicitud de trading.

## 🔍 Proceso de Selección de Skills

### 1. Análisis de Intent (Usuario → Claude)

Cuando escribes en Claude Code:
```
"scan EURUSD for patterns"
```

Claude analiza automáticamente:
- **Keywords principales:** "scan", "patterns"
- **Símbolo objetivo:** "EURUSD"
- **Contexto implícito:** Trading, análisis técnico, forex
- **Intent del usuario:** Detectar patrones de velas

### 2. Matching de Skills (Claude → SKILL.md)

Claude lee los YAML frontmatter de todos los skills disponibles en `.claude/skills/`:

```yaml
# pattern-scanner/SKILL.md
name: pattern-scanner
description: Use when detecting candlestick patterns, scanning forex symbols...
tags: [trading, patterns, candlestick, forex, ...]

# technical-analysis/SKILL.md
name: technical-analysis
description: Use when analyzing market trends, evaluating technical indicators...
tags: [trading, indicators, technical-analysis, RSI, MACD, ...]

# opportunity-scanner/SKILL.md
name: opportunity-scanner
description: Use when finding the best trading opportunities, scanning multiple symbols...
tags: [trading, scanner, opportunities, multi-symbol, ...]
```

**Match encontrado:** `pattern-scanner`
- Keyword principal: "scan" ✓
- Keyword secundario: "patterns" ✓
- Context: forex trading ✓
- Confidence: Alta

### 3. Loading del Skill (SKILL.md → Memoria)

Claude carga en memoria activa:
- SKILL.md completo (~2,000-3,000 tokens)
- Sección "When to Use This Skill"
- Execution Instructions
- Required MCP tools
- Dependencies

### 4. Ejecución del Workflow

Claude sigue las instrucciones específicas del SKILL.md:
1. Fetch market data usando MCP calls
2. Create temporary script si es necesario
3. Execute scanner/analysis
4. Parse results
5. Format output for user
6. Generate HTML report si aplica

---

## 📊 Cómo Mejorar el Matching

### ✅ Usar Palabras Clave Claras

**Requests efectivos:**
```
✓ "scan EURUSD for patterns" → pattern-scanner
✓ "analyze GBPUSD trend" → technical-analysis
✓ "calculate position size for USDJPY" → risk-management
✓ "what should I trade today?" → opportunity-scanner
✓ "backtest Bullish Engulfing strategy" → backtesting
✓ "calculate my Sharpe ratio" → advanced-analytics
```

**Requests ambiguos (evitar):**
```
✗ "check EURUSD" → ¿pattern-scanner? ¿technical-analysis?
✗ "look at market" → ¿opportunity-scanner? ¿technical-analysis?
✗ "help me trade" → ¿Qué tipo de ayuda exactamente?
✗ "analyze" → ¿Qué quieres analizar? ¿Patrones, indicadores, riesgo?
```

**Solución para requests ambiguos:**
Ser más específico:
```
✓ "check EURUSD for reversal patterns" → pattern-scanner
✓ "look at market for best opportunities" → opportunity-scanner
✓ "help me trade by analyzing EURUSD indicators" → technical-analysis
✓ "analyze EURUSD candlestick patterns" → pattern-scanner
```

---

### ✅ Usar Slash Commands (Recomendado)

Los slash commands eliminan toda ambigüedad:

```
/scan EURUSD          → pattern-scanner (100% guaranteed)
/analyze EURUSD       → technical-analysis (100% guaranteed)
/opportunities        → opportunity-scanner (100% guaranteed)
/risk EURUSD          → risk-management (100% guaranteed)
/backtest "strategy"  → backtesting (100% guaranteed)
```

**Ventajas de slash commands:**
- Selección instantánea y precisa
- No hay interpretación ambigua
- Más rápido que escribir frases completas
- Documentación clara en `.claude/commands/`

**Cómo usar:**
1. Escribe `/` en Claude Code
2. Ve la lista de comandos disponibles
3. Selecciona el comando deseado
4. Agrega parámetros si es necesario

---

### ✅ Ser Específico con Requirements

**Request vago:**
```
❌ "I want to trade EURUSD"
```
Claude no sabe qué hacer: ¿Escanear patrones? ¿Analizar indicadores? ¿Calcular riesgo?

**Request específico:**
```
✅ "Scan EURUSD for reversal patterns, then calculate position size with 1% risk"
```

Claude ejecutará automáticamente:
1. `pattern-scanner` → Detectar patrones
2. `risk-management` → Calcular posición

**Request encadenado:**
```
✅ "First scan the market for opportunities, then analyze the top 3 symbols"
```

Claude ejecutará:
1. `opportunity-scanner` → Identificar mejores símbolos
2. `technical-analysis` → Analizar cada símbolo identificado

---

## 🎯 Skill Selection Decision Tree

Proceso de decisión de Claude:

```
User Input
    │
    ├─ Contains "scan" OR "pattern" OR "candlestick"?
    │   YES → pattern-scanner
    │   Example: "scan EURUSD", "detect patterns on GBPUSD"
    │   NO → Continue
    │
    ├─ Contains "analyze" OR "trend" OR "indicator" OR "RSI" OR "MACD"?
    │   YES → technical-analysis
    │   Example: "analyze EURUSD", "check RSI on GBPUSD"
    │   NO → Continue
    │
    ├─ Contains "best" OR "opportunities" OR "what to trade" OR "scan market"?
    │   YES → opportunity-scanner
    │   Example: "what should I trade?", "find best setups"
    │   NO → Continue
    │
    ├─ Contains "risk" OR "position size" OR "lot size" OR "how much"?
    │   YES → risk-management
    │   Example: "calculate position size", "how much should I risk?"
    │   NO → Continue
    │
    ├─ Contains "backtest" OR "test strategy" OR "historical" OR "win rate"?
    │   YES → backtesting
    │   Example: "backtest RSI strategy", "does this work?"
    │   NO → Continue
    │
    └─ Contains "Sharpe" OR "correlation" OR "Monte Carlo" OR "performance"?
        YES → advanced-analytics
        Example: "calculate Sharpe ratio", "correlation between pairs"
        NO → Ask user for clarification
```

---

## 🔧 Debugging Skill Selection

Si Claude selecciona el skill incorrecto o no entiende tu request:

### Opción 1: Reformular Request

**Antes:**
```
❌ "check EURUSD"
```
Demasiado vago, Claude podría confundirse.

**Después:**
```
✅ "scan EURUSD for candlestick patterns"
```
Keyword "scan" + "patterns" → pattern-scanner garantizado

---

### Opción 2: Usar Slash Command

La forma más confiable:
```
✅ /scan EURUSD
```
Selección directa, sin ambigüedad.

---

### Opción 3: Ser Explícito

Decirle a Claude exactamente qué skill usar:
```
✅ "Use the pattern-scanner skill to analyze EURUSD"
✅ "I want to use technical-analysis skill for GBPUSD"
```

---

### Opción 4: Encadenar Skills Explícitamente

```
✅ "First use opportunity-scanner to find best symbols, then use pattern-scanner on the top result"
```

Claude ejecutará:
1. opportunity-scanner
2. pattern-scanner (con símbolo identificado en paso 1)

---

## 📚 Skill Descriptions Cheat Sheet

Guía rápida de keywords por skill:

### pattern-scanner
**Description:** "Use when detecting candlestick patterns..."

**Keywords primarios:** scan, pattern, candlestick, reversal, formation

**Keywords secundarios:** hammer, engulfing, doji, morning star, evening star

**Ejemplos de uso:**
- "scan EURUSD for patterns"
- "detect reversal patterns on GBPUSD"
- "find candlestick setups for XAUUSD"

**Avoid using for:**
- Análisis de indicadores (use technical-analysis)
- Cálculo de riesgo (use risk-management)

---

### technical-analysis
**Description:** "Use when analyzing market trends, evaluating technical indicators..."

**Keywords primarios:** analyze, trend, indicator, RSI, MACD, signal

**Keywords secundarios:** moving average, bollinger bands, stochastic, momentum, overbought, oversold

**Ejemplos de uso:**
- "analyze EURUSD trend"
- "check RSI on GBPUSD"
- "what are MACD indicators showing?"

**Avoid using for:**
- Solo patrones de velas (use pattern-scanner)
- Escaneo multi-símbolo (use opportunity-scanner)

---

### opportunity-scanner
**Description:** "Use when finding the best trading opportunities..."

**Keywords primarios:** opportunities, best, what to trade, market scan, compare symbols

**Keywords secundarios:** top setups, which pairs, find trades, scan market

**Ejemplos de uso:**
- "what should I trade today?"
- "scan the market for opportunities"
- "find the best forex pairs"

**Avoid using for:**
- Análisis de un solo símbolo (use pattern-scanner o technical-analysis)
- Validación de estrategia (use backtesting)

---

### risk-management
**Description:** "Use when calculating position sizes, determining stop loss..."

**Keywords primarios:** risk, position size, lot size, stop loss, how much

**Keywords secundarios:** take profit, money management, capital preservation, R:R ratio

**Ejemplos de uso:**
- "calculate position size for EURUSD"
- "how much should I risk on this trade?"
- "what lot size should I use?"

**Avoid using for:**
- Análisis de patrones (use pattern-scanner)
- Análisis de indicadores (use technical-analysis)

---

### backtesting
**Description:** "Use when validating trading strategies with historical data..."

**Keywords primarios:** backtest, test strategy, historical, win rate, does it work

**Keywords secundarios:** validate, profit factor, optimization, performance history

**Ejemplos de uso:**
- "backtest Bullish Engulfing strategy"
- "does this RSI strategy work?"
- "test my trading system on historical data"

**Avoid using for:**
- Análisis en tiempo real (use technical-analysis)
- Métricas de trading activo (use advanced-analytics)

---

### advanced-analytics
**Description:** "Use when analyzing performance metrics, detecting price patterns..."

**Keywords primarios:** Sharpe, correlation, Sortino, Monte Carlo, performance metrics

**Keywords secundarios:** risk-adjusted returns, portfolio analysis, statistical analysis

**Ejemplos de uso:**
- "calculate my Sharpe ratio"
- "correlation between EURUSD and GBPUSD"
- "run Monte Carlo simulation"

**Avoid using for:**
- Backtesting (use backtesting skill)
- Análisis básico de indicadores (use technical-analysis)

---

## 💡 Pro Tips

### 1. Slash Commands Son Más Rápidos

**En vez de:**
```
"I want to scan EURUSD for candlestick patterns"
```

**Usa:**
```
/scan EURUSD
```

Ahorro: ~40 caracteres, selección instantánea

---

### 2. Encadena Skills Explícitamente

**Request claro:**
```
"First scan EURUSD for patterns, then if you find a bullish pattern, calculate my position size with 2% risk"
```

Claude ejecutará:
1. pattern-scanner → Detectar patrones
2. risk-management → Calcular posición (solo si hay patrón alcista)

---

### 3. Un Skill a la Vez

**Mejor performance:**
```
User: /scan EURUSD
[Wait for results]
User: Now /analyze EURUSD
[Wait for results]
User: /risk EURUSD entry:1.0850 stop:1.0820
```

**Evitar (puede ser confuso):**
```
❌ "scan and analyze and calculate risk for EURUSD"
```

Claude podría no ejecutar todos en orden correcto.

---

### 4. Revisa Output de Cada Skill

Antes de pasar al siguiente skill, lee los resultados:

```
User: /scan EURUSD
Claude: [Shows patterns: Bullish Engulfing on H4]

User: Good, now /analyze EURUSD
Claude: [Shows RSI oversold, MACD bullish]

User: Perfect, /risk EURUSD entry:1.0850 stop:1.0820 risk:2%
Claude: [Calculates position size: 0.5 lots]
```

Cada paso valida el anterior antes de continuar.

---

### 5. Usa Context de Sesión

Claude recuerda el contexto de la conversación:

```
User: /scan EURUSD
Claude: [Muestra Bullish Engulfing en 1.0850]

User: Calculate position size for this setup with 2% risk, stop at 1.0820
Claude: [Automáticamente infiere entry:1.0850 del scan anterior]
```

No necesitas repetir toda la información.

---

## 🎓 Ejemplos de Workflows Completos

### Workflow 1: Day Trading Setup

```
User: What's the best forex pair to trade right now?
→ opportunity-scanner activado

Claude: [Scans market, identifies EURUSD with 72% probability]

User: Good, scan EURUSD for patterns
→ pattern-scanner activado

Claude: [Detects Bullish Engulfing on H1 at 1.0850]

User: Analyze EURUSD to confirm
→ technical-analysis activado

Claude: [RSI 28 (oversold), MACD bullish crossover]

User: Calculate position size, entry 1.0850, stop 1.0820, risk 2%
→ risk-management activado

Claude: [Position size: 0.67 lots, TP: 1.0910 (R:R 1:2)]

User: Perfect, I'll execute this trade manually
```

---

### Workflow 2: Strategy Development

```
User: I have a strategy idea: Buy when RSI < 30 and Bullish Engulfing appears. Does it work?
→ backtesting activado

Claude: [Backtests strategy, shows 58% win rate, profit factor 1.8]

User: Good, let me find a live setup to try it. Scan EURUSD
→ pattern-scanner activado

Claude: [Bullish Engulfing detected on H4]

User: Check if RSI is below 30
→ technical-analysis activado

Claude: [RSI: 28, condition met!]

User: Calculate risk for this trade
→ risk-management activado

Claude: [Position size calculated]

User: Execute trade
```

---

### Workflow 3: Weekly Review

```
User: Analyze my trading performance this week
→ advanced-analytics activado

Claude: [Shows win rate 55%, Sharpe 1.4, correlation analysis]

User: Which symbol performed best?
→ advanced-analytics activado

Claude: [EURUSD: 75% win rate, GBPUSD: 40% win rate]

User: Find opportunities for next week focusing on EURUSD
→ opportunity-scanner activado (filtered for EURUSD-like pairs)

Claude: [EURUSD, EURJPY, EURGBP show strong setups]

User: Scan EURUSD for patterns
→ pattern-scanner activado

Claude: [Morning Star forming on D1]
```

---

## 🐛 Troubleshooting

### Problema: Claude selecciona skill incorrecto

**Síntoma:**
```
User: "scan EURUSD"
Claude: [Activa technical-analysis en vez de pattern-scanner]
```

**Soluciones:**
1. Usar slash command: `/scan EURUSD`
2. Ser más específico: "scan EURUSD for candlestick patterns"
3. Ser explícito: "Use pattern-scanner skill for EURUSD"

---

### Problema: Claude no ejecuta ningún skill

**Síntoma:**
```
User: "EURUSD"
Claude: "What would you like me to do with EURUSD?"
```

**Solución:**
Request demasiado vago, agregar acción:
- "scan EURUSD for patterns"
- "analyze EURUSD"
- "calculate position size for EURUSD"

---

### Problema: Claude ejecuta múltiples skills cuando solo quiero uno

**Síntoma:**
```
User: "analyze EURUSD patterns"
Claude: [Ejecuta technical-analysis Y pattern-scanner]
```

**Solución:**
Si solo quieres uno:
- Para patterns: "scan EURUSD" o `/scan EURUSD`
- Para indicators: "analyze EURUSD indicators"

Si quieres ambos, está correcto.

---

### Problema: No sé qué skill usar

**Solución:**
Pregunta directamente:
```
User: "What skill should I use to find trading opportunities across multiple pairs?"
Claude: "Use opportunity-scanner skill with /opportunities command"
```

O consulta este documento (DISCOVERY.md) o WORKFLOWS.md

---

## 📖 Referencias

### Documentación de Skills
- **Pattern Scanner:** `.claude/skills/pattern-scanner/SKILL.md`
- **Technical Analysis:** `.claude/skills/technical-analysis/SKILL.md`
- **Opportunity Scanner:** `.claude/skills/opportunity-scanner/SKILL.md`
- **Risk Management:** `.claude/skills/risk-management/SKILL.md`
- **Backtesting:** `.claude/skills/backtesting/SKILL.md`
- **Advanced Analytics:** `.claude/skills/advanced-analytics/SKILL.md`

### Otras Guías
- **Workflows:** `.claude/skills/WORKFLOWS.md` - Workflows completos paso a paso
- **Error Codes:** `.claude/skills/ERROR_CODES.md` - Códigos de error y soluciones
- **Slash Commands:** `.claude/commands/` - Lista de comandos disponibles

### Links Externos
- **Anthropic Docs:** https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview
- **GitHub Repo:** https://github.com/lucesgabriel/trading-skills
- **GitHub Issues:** https://github.com/lucesgabriel/trading-skills/issues

---

## 🎯 Quick Reference Card

| Want to... | Keyword | Slash Command | Skill |
|-----------|---------|---------------|-------|
| Detect patterns | "scan", "pattern" | `/scan SYMBOL` | pattern-scanner |
| Analyze indicators | "analyze", "RSI", "MACD" | `/analyze SYMBOL` | technical-analysis |
| Find best setups | "opportunities", "best" | `/opportunities` | opportunity-scanner |
| Calculate position | "risk", "position size" | `/risk SYMBOL` | risk-management |
| Test strategy | "backtest", "win rate" | `/backtest` | backtesting |
| Performance metrics | "Sharpe", "correlation" | N/A | advanced-analytics |

---

**Última actualización:** 2025-10-30
**Versión:** 1.0
**Autor:** Trading Skills Project - Phase 2
