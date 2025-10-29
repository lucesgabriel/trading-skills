# Trading Skills para Claude Code + MetaTrader MCP

Sistema profesional de skills para análisis técnico, escaneo de oportunidades, gestión de riesgo, backtesting y análisis avanzado, integrado con MetaTrader.

## 📦 Skills Disponibles

### 1. **technical-analysis**
Análisis técnico completo con múltiples indicadores y timeframes.

**Capacidades:**
- Multi-timeframe analysis (M15, H1, H4, Daily)
- Indicadores: MA, MACD, RSI, Stochastic, Bollinger Bands, ATR
- Cálculo de probabilidad de éxito (30-85%)
- Niveles de soporte/resistencia
- Sugerencias de entrada/salida con R:R

**Uso:**
```
"Analiza EURUSD técnicamente"
"¿Cuál es la tendencia de GBPJPY?"
"Dame un análisis completo de XAUUSD"
```

**Scripts Python incluidos:**
- `.claude/skills/technical-analysis/scripts/indicator_suite.py`: Calcula indicadores y genera snapshots con probabilidades LONG/SHORT reutilizables.

### 2. **opportunity-scanner**
Escanea múltiples símbolos para encontrar las mejores oportunidades.

**Capacidades:**
- Escaneo de 15+ símbolos automáticamente
- Ranking por probabilidad de éxito
- Identificación de setups de alta probabilidad (>70%)
- Filtros personalizables

**Uso:**
```
"Escanea el mercado y muéstrame las mejores oportunidades"
"¿Qué debería tradear hoy?"
"Busca oportunidades de compra con probabilidad >70%"
```

**Scripts Python incluidos:**
- `.claude/skills/opportunity-scanner/scripts/market_scanner.py`: Escaneo multi-timeframe reutilizando el snapshot del indicador suite y ranking de oportunidades.

### 3. **risk-management**
Gestión profesional de riesgo y sizing de posiciones.

**Capacidades:**
- Cálculo automático de tamaño de posición
- Stop loss óptimo (ATR, técnico, porcentaje)
- Take profit múltiple (R:R, scaling out, trailing)
- Evaluación de exposición de portfolio

**Uso:**
```
"¿Cuántos lotes debo comprar en EURUSD con stop en 1.0820?"
"Calcula mi riesgo total de portfolio"
"¿Cuál es el stop loss óptimo para esta operación?"
```

**Scripts Python incluidos:**
- `.claude/skills/risk-management/scripts/position_sizing.py`: Calcula tamano de posicion, dimensiona con ATR y agrega riesgo de cartera.

### 4. **backtesting**
Validación de estrategias con datos históricos.

**Capacidades:**
- Backtesting completo con datos históricos
- Métricas: Win Rate, Profit Factor, Expectancy, Drawdown
- Optimización de parámetros
- Walk-forward analysis

**Uso:**
```
"Testea mi estrategia de MA crossover en EURUSD"
"¿Cuál es el win rate histórico de este setup?"
"Valida esta estrategia con datos de los últimos 2 años"
```

**Scripts Python incluidos:**
- `.claude/skills/backtesting/scripts/backtest_engine.py`: Ejecucion vectorizada de backtests con metricas clave y lista de trades.

### 5. **advanced-analytics** ⭐
Análisis sofisticado más allá de indicadores básicos.

**Capacidades:**
- Estadísticas avanzadas: Sharpe, Sortino, Calmar ratios
- Detección de patrones de velas (13+ patrones)
- Análisis de correlaciones de portfolio
- Simulaciones Monte Carlo
- Risk of Ruin

**Uso:**
```
"Calcula mi Sharpe ratio del último mes"
"Detecta patrones de velas en EURUSD"
"¿Están correlacionados EURUSD y GBPUSD?"
"Simula 1000 escenarios de mi estrategia"
```

**Scripts Python incluidos:**
- `.claude/skills/advanced-analytics/scripts/advanced_statistics.py`: 15+ metricas de rendimiento
- `.claude/skills/advanced-analytics/scripts/pattern_recognition.py`: 13 patrones de velas
- `.claude/skills/advanced-analytics/scripts/correlation_analysis.py`: Matrices de correlacion
- `.claude/skills/advanced-analytics/scripts/volatility_analysis.py`: 5+ metodos de analisis

## 🚀 Inicio Rápido

### Workflow Completo de Trading

1. **Escaneo Matutino**
   ```
   "Escanea el mercado y muéstrame las mejores oportunidades"
   ```

2. **Análisis Detallado**
   ```
   "Analiza EURUSD en detalle con probabilidad de éxito"
   ```

3. **Cálculo de Riesgo**
   ```
   "Calcula el tamaño de posición para EURUSD, entry 1.0850, stop 1.0820"
   ```

4. **Validación**
   ```
   "¿Ha funcionado este setup históricamente en EURUSD?"
   ```

## 📊 Estructura de Archivos

```
.claude/skills/
  technical-analysis/
    SKILL.md
    scripts/
      indicator_suite.py
  opportunity-scanner/
    SKILL.md
    scripts/
      market_scanner.py
  risk-management/
    SKILL.md
    scripts/
      position_sizing.py
  backtesting/
    SKILL.md
    scripts/
      backtest_engine.py
  advanced-analytics/
    SKILL.md
    scripts/
      advanced_statistics.py
      pattern_recognition.py
      correlation_analysis.py
      volatility_analysis.py
  README.md (este archivo)
```

## ⚡ Comandos Útiles

### Análisis Rápido
```
"Análisis técnico de EURUSD"
"Estado de mis posiciones"
"Riesgo actual del portfolio"
```

### Análisis Profundo
```
"Análisis completo de GBPJPY con patrones de velas y correlaciones"
"Performance del último mes con métricas avanzadas"
```

### Escaneo y Validación
```
"Escanea pares con EUR y dame el mejor setup"
"Testea estrategia de RSI en XAUUSD últimos 12 meses"
```

## 🎯 Mejores Prácticas

1. **Siempre usa confluencias**: No operes con un solo indicador
2. **Respeta el riesgo**: Nunca más del 1-2% por operación
3. **Valida con backtesting**: Prueba estrategias antes de operar
4. **Monitorea correlaciones**: Evita riesgo concentrado
5. **Usa trailing stops**: Protege ganancias
6. **Mantén registros**: Aprende de cada operación

## 🔧 Configuración MetaTrader MCP

Ver archivo `.mcp.json` en la raíz del proyecto para configuración del servidor MetaTrader.

## 📝 Notas Importantes

⚠️ **Trading tiene riesgo**
- Ningún skill garantiza ganancias
- Siempre usa stop loss
- No arriesgues más de lo que puedes perder
- Practica en demo antes de real

✅ **Para mejores resultados**
- Combina múltiples skills
- Sigue un plan sistemático
- Mantén disciplina emocional
- Aprende continuamente del mercado

## 📄 Documentación de Referencia

Para ejemplos de código Python y casos de uso avanzados, consulta:
- `trading-skills/PYTHON-EXAMPLES-UPDATED.md` - Ejemplos de código
- Documentación oficial de Claude Code Skills

---

**Versión**: 2.0
**Última actualización**: Octubre 2025
**Compatibilidad**: Claude Code CLI + MetaTrader 5 MCP
