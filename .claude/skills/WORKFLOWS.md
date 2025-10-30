# Skill Composition Workflows

Workflows completos que combinan múltiples skills para análisis profesional de trading.

## 🎯 Workflow Completo de Trading

### 1. Descubrimiento (opportunity-scanner)
**Comando:** `/opportunities` o "scan the market for best trading opportunities"

**Propósito:** Encontrar los mejores setups del día en múltiples símbolos

**Output:** Lista rankeada de símbolos con probabilidades calculadas

**Ejemplo de uso:**
```
/opportunities
```

**Resultado esperado:**
- EURUSD: 72% probabilidad (3 señales confluentes)
- GBPUSD: 68% probabilidad (2 señales confluentes)
- XAUUSD: 55% probabilidad (1 señal)

---

### 2. Análisis Profundo (technical-analysis + pattern-scanner)
**Comandos:**
```
/analyze EURUSD
/scan EURUSD
```

**Propósito:** Validar la señal identificada con confluencia de indicadores técnicos y patrones de velas

**Output:**
- Indicadores: RSI, MACD, MA, Bollinger Bands, Stochastic, ATR
- Patrones: Morning Star, Engulfing, Hammer, Doji, etc.
- Probabilidad de éxito calculada

**Ejemplo de uso:**
```
First run /analyze EURUSD to check indicators
Then run /scan EURUSD to detect patterns
```

**Confluencia ideal:**
- RSI oversold (<30) + Bullish Engulfing = Alta probabilidad de reversión alcista
- MACD bullish crossover + Hammer = Confirmación de momentum
- Precio en soporte MA200 + Morning Star = Setup de alta confianza

---

### 3. Gestión de Riesgo (risk-management)
**Comando:** `/risk EURUSD entry:1.0850 stop:1.0820`

**Propósito:** Calcular el tamaño de posición óptimo basado en tu capital y tolerancia al riesgo

**Output:**
- Lot size recomendado
- Riesgo en dólares
- Risk:Reward ratio
- Take profit sugerido

**Ejemplo de uso:**
```
/risk EURUSD entry:1.0850 stop:1.0820 risk:2%
```

**Resultado esperado:**
```
Account Balance: $10,000
Risk per trade: $200 (2%)
Stop loss: 30 pips
Position size: 0.67 lots
Minimum R:R: 1:2 (TP at 1.0910 = 60 pips)
```

**Reglas importantes:**
- Nunca arriesgar más del 2% del capital por trade
- R:R mínimo de 1:1.5 (preferible 1:2 o mayor)
- Ajustar lot size si el stop loss es muy amplio

---

### 4. Validación Histórica (backtesting)
**Comando:** `/backtest "Bullish Engulfing + RSI < 30"`

**Propósito:** Verificar que la estrategia funciona con datos históricos antes de arriesgar capital

**Output:**
- Win rate (%)
- Profit factor
- Maximum drawdown
- Número de trades
- Expectativa matemática

**Ejemplo de uso:**
```
/backtest "Buy when RSI < 30 AND Bullish Engulfing appears on H4"
```

**Resultado esperado:**
```
Backtesting Results (6 months, H4):
- Total trades: 127
- Win rate: 58%
- Profit factor: 1.8
- Max drawdown: 12%
- Average R:R: 1:2.3
- Expectativa: +$45 per trade

Verdict: Strategy is viable ✓
```

**Criterios de aceptación:**
- Win rate > 50%
- Profit factor > 1.5
- Max drawdown < 20%
- Mínimo 100 trades para ser estadísticamente significativo

---

### 5. Métricas Avanzadas (advanced-analytics)
**Comando:** "calculate Sharpe ratio for last month"

**Propósito:** Evaluar desempeño ajustado por riesgo de tu portfolio

**Output:**
- Sharpe ratio
- Sortino ratio
- Calmar ratio
- Correlación entre símbolos
- Monte Carlo simulation

**Ejemplo de uso:**
```
Analyze my trading performance for the last month
Calculate Sharpe and Sortino ratios
Run Monte Carlo simulation with 1000 iterations
```

**Resultado esperado:**
```
Portfolio Analytics (Last 30 days):
- Sharpe Ratio: 1.85 (Bueno)
- Sortino Ratio: 2.34 (Excelente)
- Calmar Ratio: 1.12 (Aceptable)
- Correlation EURUSD-GBPUSD: 0.78 (Alta)
- Monte Carlo 95% confidence: +$2,300 to +$8,900

Recommendation: Reduce correlation, diversify with XAUUSD
```

---

## 📊 Workflows por Caso de Uso

### Swing Trading Setup (Posiciones de varios días)

**Objetivo:** Capturar movimientos de tendencia en timeframes mayores

**Workflow:**
1. **Escanear mercado** → `/opportunities`
   - Buscar setups en D1/W1
   - Filtrar por tendencia clara

2. **Confirmar tendencia** → `/analyze [SYMBOL]`
   - Verificar MA50/MA200 alineadas
   - RSI entre 40-60 (tendencia saludable)
   - MACD consistente con tendencia

3. **Calcular posición** → `/risk [SYMBOL]`
   - Stop loss amplio (100-150 pips)
   - Position size ajustado al stop
   - R:R mínimo 1:3

4. **Ejecutar trade** → Manualmente en MetaTrader
   - Colocar orden con SL/TP
   - Trailing stop después de 1:1

**Ejemplo completo:**
```
User: "I want to find a swing trade for this week"

Step 1: /opportunities
Result: GBPUSD shows strong uptrend on D1

Step 2: /analyze GBPUSD
Result: MA50 > MA200, RSI 58, MACD bullish

Step 3: /scan GBPUSD
Result: Bullish flag pattern detected on D1

Step 4: /risk GBPUSD entry:1.2650 stop:1.2500
Result: 0.13 lots, risk $200, TP:1.3100 (R:R 1:3)

Step 5: Execute trade manually
```

---

### Day Trading Setup (Posiciones intraday)

**Objetivo:** Capturar movimientos rápidos en timeframes menores

**Workflow:**
1. **Identificar patrones** → `/scan [SYMBOL]`
   - Timeframes: M15/H1
   - Buscar reversiones en soportes/resistencias

2. **Validar con indicadores** → `/analyze [SYMBOL]`
   - RSI extremo (<30 o >70)
   - MACD divergencia
   - Bollinger Bands squeeze

3. **Calcular riesgo** → `/risk [SYMBOL]`
   - Stop loss tight (15-30 pips)
   - Position size mayor (por menor riesgo/pip)
   - R:R mínimo 1:2

4. **Ejecutar con límites de tiempo**
   - Cierre forzado al final del día
   - No hold overnight
   - Maximum 3 trades/día

**Ejemplo completo:**
```
User: "Find me a day trade on EURUSD"

Step 1: /scan EURUSD
Result: Hammer at support 1.0830 on H1

Step 2: /analyze EURUSD
Result: RSI 28 (oversold), MACD starting to turn

Step 3: /risk EURUSD entry:1.0835 stop:1.0815
Result: 1.0 lots, risk $200, TP:1.0875 (R:R 1:2)

Step 4: Execute immediately, monitor closely
```

---

### Strategy Development (Crear nueva estrategia)

**Objetivo:** Desarrollar y validar una nueva estrategia de trading

**Workflow:**
1. **Definir reglas claras**
   - Condiciones de entrada específicas
   - Condiciones de salida (SL/TP)
   - Filtros de mercado

2. **Backtest inicial** → `/backtest "strategy"`
   - Probar en 6-12 meses de datos
   - Verificar win rate > 50%
   - Profit factor > 1.5

3. **Optimizar parámetros**
   - Si win rate < 50%: Ajustar condiciones
   - Si max DD > 20%: Reducir riesgo
   - Si pocos trades: Relajar filtros

4. **Validación cruzada** → Backtest en otro símbolo
   - Probar en instrumento diferente
   - Verificar que funcione en múltiples mercados

5. **Paper trading** → 1 mes sin dinero real
   - Ejecutar en demo account
   - Documentar cada trade
   - Revisar con advanced-analytics

6. **Trading real** → Comenzar con 0.01 lots
   - Primeras 20 trades con posición mínima
   - Incrementar gradualmente

**Ejemplo completo:**
```
User: "I want to create a strategy based on RSI divergence"

Step 1: Define rules
- Entry: RSI makes higher low, price makes lower low
- Stop: Below recent swing low
- TP: 1:2 risk-reward
- Filter: Only in trending markets (MA50 > MA200)

Step 2: /backtest "Buy on bullish RSI divergence with MA50>MA200"
Result: Win rate 62%, profit factor 1.9, looks good!

Step 3: Validate on GBPUSD
/backtest "same strategy on GBPUSD"
Result: Win rate 58%, still profitable ✓

Step 4: Paper trade for 1 month
Execute strategy in demo, document results

Step 5: If successful → Start real trading with micro lots
```

---

### Portfolio Review (Análisis semanal)

**Objetivo:** Revisar desempeño y mejorar estrategia

**Workflow:**
1. **Calcular métricas** → advanced-analytics
   - Sharpe ratio
   - Win rate por símbolo
   - Average R:R achieved

2. **Identificar patrones** → advanced-analytics
   - ¿Qué tipo de trades ganan más?
   - ¿Qué símbolos son más rentables?
   - ¿Hay correlación entre trades perdedores?

3. **Ajustar estrategia**
   - Reducir exposición a símbolos no rentables
   - Aumentar posición en setups ganadores
   - Modificar parámetros si es necesario

4. **Plan para próxima semana**
   - Definir objetivos (número de trades, R:R target)
   - Identificar setups a monitorear
   - Preparar watchlist

**Ejemplo completo:**
```
User: "Review my trading performance this week"

Step 1: "Analyze my trading history for the last 7 days"
Result:
- Total trades: 12
- Win rate: 58%
- Avg R:R: 1:1.8
- Best symbol: EURUSD (75% win rate)
- Worst symbol: XAUUSD (25% win rate)

Step 2: "Calculate Sharpe ratio"
Result: Sharpe 1.6 (good), but high correlation EURUSD-GBPUSD

Step 3: Decisions
- Focus on EURUSD (proven winner)
- Reduce XAUUSD exposure (not working)
- Diversify with USDJPY to reduce correlation

Step 4: Next week plan
- Target: 10 trades, 60% win rate
- Watch: EURUSD breakouts, USDJPY reversals
- Avoid: XAUUSD until strategy improves
```

---

## 🔄 Skill Dependencies

```
           opportunity-scanner
                    ↓
    ┌───────────────┴───────────────┐
    ↓                               ↓
technical-analysis          pattern-scanner
    └───────────────┬───────────────┘
                    ↓
            risk-management
                    ↓
          [TRADE EXECUTION]
                    ↓
          advanced-analytics
         (post-trade review)
```

**Flujo recomendado:**
1. Opportunity scanner identifica mejores setups
2. Technical analysis + Pattern scanner validan señal
3. Risk management calcula posición
4. Ejecutar trade manualmente
5. Advanced analytics revisa desempeño

**Relaciones entre skills:**
- **opportunity-scanner** → Encuentra qué analizar
- **technical-analysis** ↔ **pattern-scanner** → Confluencia de señales
- **risk-management** → Depende de entry/stop de los anteriores
- **backtesting** → Valida estrategias antes de operar
- **advanced-analytics** → Mejora continua basada en resultados

---

## 💡 Tips de Workflow

### ✅ Mejores Prácticas

1. **No saltarse risk-management**
   - Siempre calcular posición antes de operar
   - Nunca "adivinar" el lot size
   - Respetar el 2% máximo de riesgo

2. **Usar confluencia**
   - Combinar technical-analysis + pattern-scanner
   - Mínimo 2 señales concordantes
   - Ejemplo: RSI oversold + Bullish Engulfing + Soporte MA200

3. **Backtest primero**
   - Nunca operar estrategia sin validar
   - Mínimo 100 trades para significancia estadística
   - Validar en múltiples símbolos

4. **Review regular**
   - Usar advanced-analytics cada semana
   - Documentar lecciones aprendidas
   - Ajustar estrategia basado en datos

5. **Un skill a la vez**
   - No intentar hacer todo simultáneamente
   - Revisar output de cada skill antes de continuar
   - Usar slash commands para claridad

### ⚠️ Errores Comunes

1. **No calcular riesgo**
   ```
   ❌ "I'll just use 1 lot, should be fine"
   ✅ /risk EURUSD entry:1.0850 stop:1.0820 risk:2%
   ```

2. **Ignorar backtesting**
   ```
   ❌ "This pattern looks good, let's trade it"
   ✅ /backtest "Bullish Engulfing" first, then decide
   ```

3. **No usar confluencia**
   ```
   ❌ Only checking /scan EURUSD
   ✅ Run both /scan EURUSD and /analyze EURUSD
   ```

4. **Operar sin plan**
   ```
   ❌ "Let me check what looks good today"
   ✅ /opportunities → pick best setup → analyze → risk → execute
   ```

5. **No revisar desempeño**
   ```
   ❌ Trading without tracking results
   ✅ Weekly review with advanced-analytics
   ```

---

## 🎓 Learning Path

### Principiante (Semana 1-2)

**Objetivo:** Familiarizarse con los skills básicos

1. Aprender `/scan` en un símbolo
2. Aprender `/analyze` en el mismo símbolo
3. Practicar `/risk` con diferentes scenarios
4. Demo account: 10 trades siguiendo workflow básico

**Workflow básico principiante:**
```
/scan EURUSD → /analyze EURUSD → /risk EURUSD → Execute on demo
```

### Intermedio (Semana 3-4)

**Objetivo:** Desarrollar estrategia propia

1. Usar `/opportunities` para encontrar mejores setups
2. Combinar technical-analysis + pattern-scanner
3. Ejecutar `/backtest` de estrategia preferida
4. Demo account: 20 trades con 55%+ win rate

**Workflow intermedio:**
```
/opportunities → /scan + /analyze top picks → /backtest strategy → Execute
```

### Avanzado (Mes 2+)

**Objetivo:** Optimización y scaling

1. Usar advanced-analytics para métricas avanzadas
2. Optimizar estrategia basado en Sharpe/Sortino
3. Diversificar portfolio con correlación baja
4. Real account: Comenzar con micro lots

**Workflow avanzado:**
```
Weekly review (analytics) → Optimize strategy → /opportunities →
Full analysis → Risk management → Execute → Track & improve
```

---

## 📈 Success Metrics

### Short-term (1 mes)
- [ ] Win rate > 50%
- [ ] Average R:R > 1:1.5
- [ ] Máximo 2% riesgo por trade
- [ ] Documentar todos los trades

### Medium-term (3 meses)
- [ ] Win rate > 55%
- [ ] Profit factor > 1.5
- [ ] Sharpe ratio > 1.0
- [ ] Max drawdown < 15%

### Long-term (6 meses)
- [ ] Win rate > 58%
- [ ] Profit factor > 1.8
- [ ] Sharpe ratio > 1.5
- [ ] Consistent monthly profits

---

## 🔗 Enlaces Relacionados

- **Slash Commands:** `.claude/commands/` (para workflows rápidos)
- **Error Codes:** `.claude/skills/ERROR_CODES.md` (troubleshooting)
- **Discovery Guide:** `.claude/skills/DISCOVERY.md` (cómo Claude selecciona skills)
- **Individual Skills:** `.claude/skills/[skill-name]/SKILL.md`

---

**Última actualización:** 2025-10-30
**Versión:** 1.0
**Autor:** Trading Skills Project - Phase 2
