# Error Codes Reference

Sistema de códigos de error estructurados para todos los skills del proyecto trading-skills.

## 📋 Formato de Código

```
ERR_[SKILL]_[NUMBER]: [Description]
```

**Convención:**
- **ERR_PS_xxx** - Pattern Scanner
- **ERR_TA_xxx** - Technical Analysis
- **ERR_OS_xxx** - Opportunity Scanner
- **ERR_RM_xxx** - Risk Management
- **ERR_BT_xxx** - Backtesting
- **ERR_AA_xxx** - Advanced Analytics
- **ERR_GEN_xxx** - General Errors

---

## 🔍 Pattern Scanner (ERR_PS_xxx)

### ERR_PS_001: Insufficient Candle Data
**Causa:** MCP retornó menos de 50 velas para un timeframe

**Razones comunes:**
- MetaTrader no tiene suficiente historia descargada
- Broker limita datos históricos
- Símbolo recién añadido al servidor

**Solución:**
1. Verificar que MetaTrader 5 esté conectado
2. Ir a Tools → History Center en MetaTrader
3. Seleccionar símbolo y descargar más historia
4. Reiniciar el scan después de descargar

**Mensaje al usuario:**
```
❌ ERR_PS_001: Datos insuficientes para M15 (solo 30 velas, se requieren 50+)
📊 Detalles: Pattern scanner necesita mínimo 50 velas para análisis confiable
💡 Solución:
   1. Abre MetaTrader 5
   2. Tools → History Center
   3. Selecciona EURUSD → M15
   4. Click "Download" para obtener más historia
   5. Reintenta el scan
🔗 Más info: .claude/skills/pattern-scanner/troubleshooting.md
```

---

### ERR_PS_002: Invalid Symbol
**Causa:** Símbolo no disponible en el broker

**Razones comunes:**
- Typo en el nombre del símbolo (EURUSDD en vez de EURUSD)
- Broker no soporta ese símbolo
- Símbolo escrito con formato incorrecto (EUR/USD vs EURUSD)

**Solución:**
1. Verificar spelling del símbolo
2. Confirmar que broker soporta el símbolo
3. Ver símbolos disponibles con `mcp__metatrader__get_all_symbols`
4. Usar formato correcto según broker

**Mensaje al usuario:**
```
❌ ERR_PS_002: Símbolo 'EURUSDD' no encontrado en broker
📊 Detalles: El símbolo solicitado no existe en tu servidor MetaTrader
💡 Solución:
   ¿Quisiste decir 'EURUSD'?

   Símbolos disponibles que coinciden:
   - EURUSD
   - EURUSD.raw
   - EURUSD_i

   Para ver todos: Usa "get all available symbols"
🔗 Más info: .claude/skills/pattern-scanner/troubleshooting.md
```

---

### ERR_PS_003: MCP Connection Failed
**Causa:** MetaTrader no está ejecutándose o MCP server no responde

**Razones comunes:**
- MetaTrader 5 cerrado
- MCP server no iniciado
- Configuración incorrecta en `.claude/settings.local.json`
- Firewall bloqueando conexión

**Solución:**
1. Verificar que MetaTrader 5 esté abierto
2. Verificar que MCP server esté corriendo
3. Reiniciar Claude Code
4. Verificar configuración MCP en settings

**Mensaje al usuario:**
```
❌ ERR_PS_003: No se puede conectar a MetaTrader via MCP
📊 Detalles: El servidor MCP de MetaTrader no responde
💡 Solución:
   1. Verifica que MetaTrader 5 esté abierto
   2. Reinicia Claude Code (cierra y abre de nuevo)
   3. Verifica configuración en .claude/settings.local.json:
      - Debe tener "metatrader" en mcpServers
      - Command debe apuntar a Python correcto
   4. Si persiste: Revisa logs en MetaTrader (Tools → Options → Expert Advisors)
🔗 Más info: .claude/skills/pattern-scanner/troubleshooting.md
```

---

### ERR_PS_004: No Patterns Detected
**Causa:** No se detectaron patrones de velas en los timeframes analizados

**Razones comunes:**
- Mercado en consolidación (sin patrones claros)
- Timeframes seleccionados no muestran formaciones
- Parámetros de detección demasiado estrictos

**Solución:**
1. Probar con diferentes timeframes
2. Esperar a que se forme un patrón
3. Analizar otros símbolos

**Mensaje al usuario:**
```
⚠️ ERR_PS_004: No se detectaron patrones en EURUSD
📊 Detalles: Ningún patrón de velas encontrado en M15, H1, H4, D1
💡 Solución:
   Esto es normal cuando el mercado está en consolidación.

   Opciones:
   1. Espera y reintenta en 1-2 horas
   2. Analiza otro símbolo: /scan GBPUSD
   3. Usa /analyze EURUSD para ver indicadores técnicos
🔗 Más info: Esto no es un error, solo ausencia de señales
```

---

### ERR_PS_005: Pattern Detection Failed
**Causa:** Error durante el proceso de detección de patrones

**Razones comunes:**
- Datos corruptos en velas
- Error en script de Python
- Parámetros inválidos

**Solución:**
1. Reintentar el scan
2. Verificar logs de Python
3. Reportar bug si persiste

**Mensaje al usuario:**
```
❌ ERR_PS_005: Error inesperado al detectar patrones
📊 Detalles: El algoritmo de detección encontró un problema
💡 Solución:
   1. Reintenta el comando: /scan EURUSD
   2. Si persiste, intenta con otro símbolo
   3. Reporta el error con detalles:
      - Símbolo afectado
      - Mensaje de error completo
🔗 Más info: GitHub Issues: https://github.com/lucesgabriel/trading-skills/issues
```

---

## 📊 Technical Analysis (ERR_TA_xxx)

### ERR_TA_001: Indicator Calculation Failed
**Causa:** Datos insuficientes para calcular indicador

**Razones comunes:**
- MACD requiere mínimo 34 velas (26 + 12 - 1)
- RSI requiere mínimo 14 velas
- MA 200 requiere mínimo 200 velas
- Timeframe muy bajo con poca historia

**Solución:**
1. Usar timeframe mayor (H4/D1 en vez de M15)
2. Reducir periodo del indicador
3. Descargar más historia

**Mensaje al usuario:**
```
❌ ERR_TA_001: No se puede calcular MA200 (solo 100 velas disponibles)
📊 Detalles: Moving Average de 200 periodos requiere mínimo 200 velas
💡 Solución:
   Opciones:
   1. Usa timeframe mayor: /analyze EURUSD (en H4 o D1)
   2. Reduce periodo: Usa MA50 o MA100 en vez de MA200
   3. Descarga más historia en MetaTrader

   Indicadores disponibles con 100 velas:
   ✅ MA50
   ✅ RSI (14)
   ✅ MACD (12,26,9)
   ❌ MA200
🔗 Más info: .claude/skills/technical-analysis/troubleshooting.md
```

---

### ERR_TA_002: Invalid Timeframe
**Causa:** Timeframe solicitado no es válido

**Razones comunes:**
- Formato incorrecto (M1 vs 1M)
- Timeframe no soportado por broker

**Solución:**
1. Usar timeframes válidos: M1, M5, M15, M30, H1, H4, D1, W1, MN1
2. Verificar formato correcto

**Mensaje al usuario:**
```
❌ ERR_TA_002: Timeframe '5M' no es válido
📊 Detalles: Formato de timeframe incorrecto
💡 Solución:
   Usa el formato correcto:
   ✅ M5  (5 minutos)
   ✅ M15 (15 minutos)
   ✅ H1  (1 hora)
   ✅ H4  (4 horas)
   ✅ D1  (diario)

   ❌ 5M, 15m, 1h (formatos incorrectos)
🔗 Más info: .claude/skills/technical-analysis/troubleshooting.md
```

---

### ERR_TA_003: Conflicting Signals
**Causa:** Indicadores muestran señales contradictorias

**Razones comunes:**
- Mercado en consolidación
- Reversión de tendencia en progreso
- Divergencias normales entre indicadores

**Solución:**
1. Esperar confirmación
2. Analizar timeframe mayor
3. Buscar confluencia con patterns

**Mensaje al usuario:**
```
⚠️ ERR_TA_003: Señales contradictorias detectadas en EURUSD
📊 Detalles:
   - RSI: Oversold (28) → Señal de compra
   - MACD: Bearish crossover → Señal de venta
   - MA: Precio bajo MA200 → Tendencia bajista

💡 Interpretación:
   Esto indica indecisión del mercado o posible reversión.

   Recomendación:
   1. NO operar hasta tener confirmación
   2. Espera a que MACD confirme reversión
   3. Usa /scan EURUSD para buscar patrones de reversión
   4. Analiza timeframe mayor: /analyze EURUSD (en D1)
🔗 Más info: No es un error, es información importante
```

---

## 🎯 Opportunity Scanner (ERR_OS_xxx)

### ERR_OS_001: No Symbols Available
**Causa:** No hay símbolos disponibles para escanear

**Razones comunes:**
- MetaTrader desconectado
- Filtro de símbolos demasiado restrictivo

**Solución:**
1. Verificar conexión a MetaTrader
2. Ajustar filtros de búsqueda

**Mensaje al usuario:**
```
❌ ERR_OS_001: No se encontraron símbolos para escanear
📊 Detalles: La lista de símbolos está vacía
💡 Solución:
   1. Verifica que MetaTrader esté conectado
   2. Si usaste filtros, prueba sin filtrar:
      /opportunities (sin filtros)
   3. Verifica símbolos disponibles: "get all available symbols"
🔗 Más info: .claude/skills/opportunity-scanner/troubleshooting.md
```

---

### ERR_OS_002: Scan Timeout
**Causa:** El escaneo tardó más de lo esperado

**Razones comunes:**
- Demasiados símbolos para analizar
- Servidor lento
- Conexión inestable

**Solución:**
1. Reducir número de símbolos
2. Escanear por categorías (solo forex mayor, solo metales, etc.)
3. Verificar conexión a internet

**Mensaje al usuario:**
```
❌ ERR_OS_002: Escaneo cancelado por timeout (> 2 minutos)
📊 Detalles: El escaneo de 50 símbolos tardó demasiado
💡 Solución:
   Reduce el alcance del escaneo:

   En vez de: /opportunities (todos los símbolos)
   Usa: /opportunities forex (solo pares forex)
   O: /opportunities majors (solo pares principales)

   Símbolos principales:
   - EURUSD, GBPUSD, USDJPY, USDCHF
   - AUDUSD, NZDUSD, USDCAD
   - XAUUSD (oro)
🔗 Más info: .claude/skills/opportunity-scanner/troubleshooting.md
```

---

### ERR_OS_003: No Opportunities Found
**Causa:** No se encontraron oportunidades de trading con alta probabilidad

**Razones comunes:**
- Mercado en consolidación general
- Criterios de selección muy estrictos
- Momento del día (poco movimiento)

**Solución:**
1. Normal cuando mercado está tranquilo
2. Esperar a sesiones más activas
3. Reducir threshold de probabilidad

**Mensaje al usuario:**
```
⚠️ ERR_OS_003: No se encontraron oportunidades de alta probabilidad
📊 Detalles: Ningún símbolo cumple criterios (probabilidad > 65%)
💡 Interpretación:
   Esto es normal cuando el mercado está en consolidación.

   Opciones:
   1. Espera a sesiones más activas:
      - London open: 8:00 GMT
      - NY open: 13:00 GMT
      - London/NY overlap: 13:00-17:00 GMT

   2. Revisa símbolos manualmente:
      /analyze EURUSD
      /scan GBPUSD

   3. Reduce threshold: "find opportunities with 50%+ probability"
🔗 Más info: No es un error, es información del mercado
```

---

## 💰 Risk Management (ERR_RM_xxx)

### ERR_RM_001: Insufficient Account Balance
**Causa:** Balance muy bajo para el riesgo solicitado

**Razones comunes:**
- Intentar arriesgar más del 2% recomendado
- Lot size demasiado grande para la cuenta
- Stop loss muy amplio para el capital disponible

**Solución:**
1. Reducir lot size
2. Aumentar stop loss (menor riesgo por pip)
3. Reducir porcentaje de riesgo
4. Depositar más fondos

**Mensaje al usuario:**
```
❌ ERR_RM_001: Riesgo de $500 excede límite recomendado
📊 Detalles:
   - Balance: $1,000
   - Riesgo solicitado: $500 (50%)
   - Máximo recomendado: $20 (2%)

💡 Solución:
   Nunca arriesgues más del 2% por trade.

   Para este trade:
   - Entry: 1.0850
   - Stop: 1.0820 (30 pips)
   - Balance: $1,000

   Cálculo correcto:
   - Riesgo máximo: $20 (2% de $1,000)
   - Position size: 0.067 lots
   - Riesgo por pip: $0.67

   Comando correcto:
   /risk EURUSD entry:1.0850 stop:1.0820 risk:2%
🔗 Más info: .claude/skills/risk-management/SKILL.md
```

---

### ERR_RM_002: Risk:Reward Too Low
**Causa:** R:R ratio menor al mínimo recomendado (1:1.5)

**Razones comunes:**
- Take profit muy cercano
- Stop loss muy amplio
- Setup no favorable

**Solución:**
1. Ampliar take profit
2. Reducir stop loss (si es técnicamente válido)
3. Buscar otro setup mejor

**Mensaje al usuario:**
```
⚠️ ERR_RM_002: Risk:Reward de 1:0.8 es muy bajo
📊 Detalles:
   - Entry: 1.0850
   - Stop loss: 1.0820 (30 pips de riesgo)
   - Take profit: 1.0874 (24 pips de ganancia)
   - R:R actual: 1:0.8
   - R:R mínimo: 1:1.5

💡 Solución:
   Ajustar take profit para mejor R:R:

   Opciones:
   1. TP conservador 1:1.5 → 1.0895 (45 pips)
   2. TP ideal 1:2 → 1.0910 (60 pips)
   3. TP agresivo 1:3 → 1.0940 (90 pips)

   Recomendación:
   Usa mínimo 1:2 para compensar trades perdedores.
   Con 50% win rate y R:R 1:2, eres rentable.
🔗 Más info: .claude/skills/risk-management/SKILL.md
```

---

### ERR_RM_003: Invalid Stop Loss
**Causa:** Stop loss no es válido

**Razones comunes:**
- Stop loss demasiado cercano (< 10 pips)
- Stop loss en dirección incorrecta (buy con SL arriba del entry)
- Stop loss = entry price

**Solución:**
1. Colocar stop loss en nivel técnico válido
2. Mínimo 10-15 pips de distancia
3. Verificar dirección del trade

**Mensaje al usuario:**
```
❌ ERR_RM_003: Stop loss inválido
📊 Detalles:
   - Entry: 1.0850
   - Stop loss: 1.0849 (solo 1 pip)
   - Tipo de trade: BUY

💡 Problema:
   Stop loss de 1 pip es demasiado cercano.
   Será activado por ruido normal del mercado.

   Solución:
   Coloca stop loss en nivel técnico:
   - Debajo de soporte reciente
   - Debajo de swing low
   - Mínimo 15-20 pips de distancia

   Ejemplo:
   Si último swing low es 1.0820:
   /risk EURUSD entry:1.0850 stop:1.0815
🔗 Más info: .claude/skills/risk-management/SKILL.md
```

---

## 📈 Backtesting (ERR_BT_xxx)

### ERR_BT_001: Insufficient Historical Data
**Causa:** No hay suficientes velas para backtest significativo

**Razones comunes:**
- Periodo de prueba muy corto
- Estrategia genera pocos trades
- Timeframe muy alto (W1, MN1)

**Solución:**
1. Descargar más historia
2. Usar timeframe menor
3. Extender periodo de prueba

**Mensaje al usuario:**
```
❌ ERR_BT_001: Solo 50 trades encontrados (mínimo: 100 para significancia estadística)
📊 Detalles:
   - Periodo: 3 meses
   - Timeframe: D1
   - Trades: 50
   - Mínimo recomendado: 100

💡 Solución:
   Opciones para obtener más trades:

   1. Extender periodo:
      3 meses → 6-12 meses

   2. Usar timeframe menor:
      D1 → H4 (más señales)

   3. Relajar filtros de estrategia:
      Si es muy restrictiva, menos trades

   Ejemplo:
   /backtest "Bullish Engulfing + RSI < 30" period:12months timeframe:H4
🔗 Más info: .claude/skills/backtesting/troubleshooting.md
```

---

### ERR_BT_002: Strategy Undefined
**Causa:** Reglas de estrategia no están claras

**Razones comunes:**
- Descripción muy vaga
- Faltan condiciones de entrada/salida
- Reglas ambiguas

**Solución:**
1. Definir condiciones de entrada específicas
2. Especificar reglas de salida claras
3. Incluir filtros si aplican

**Mensaje al usuario:**
```
❌ ERR_BT_002: Estrategia "comprar cuando sube" es muy vaga
📊 Detalles: La descripción no tiene reglas específicas para backtesting
💡 Solución:
   Define una estrategia clara con:

   1. Condición de entrada exacta
   2. Stop loss
   3. Take profit
   4. Filtros opcionales

   Ejemplos MALOS (muy vagos):
   ❌ "comprar cuando sube"
   ❌ "usar RSI para operar"
   ❌ "trade breakouts"

   Ejemplos BUENOS (específicos):
   ✅ "Buy when RSI < 30 AND Bullish Engulfing appears on H4"
   ✅ "Sell when MACD bearish crossover AND price > MA200"
   ✅ "Buy when price breaks above resistance with volume increase"

   Template recomendado:
   "BUY/SELL when [indicator condition] AND [pattern] on [timeframe]"
🔗 Más info: .claude/skills/backtesting/SKILL.md
```

---

### ERR_BT_003: Strategy Performance Poor
**Causa:** La estrategia testeada tiene mal desempeño

**Razones comunes:**
- Win rate < 40%
- Profit factor < 1.0 (perdedor neto)
- Max drawdown > 30%

**Solución:**
1. NO operar esta estrategia
2. Optimizar parámetros
3. Buscar otra estrategia

**Mensaje al usuario:**
```
⚠️ ERR_BT_003: Estrategia muestra desempeño pobre
📊 Resultados del backtest:
   - Win rate: 38% (bajo, mínimo 50%)
   - Profit factor: 0.85 (perdedor neto, mínimo 1.5)
   - Max drawdown: 35% (muy alto, máximo 20%)
   - Trades: 150

💡 Interpretación:
   ❌ NO operes esta estrategia con dinero real

   Esta estrategia pierde dinero en promedio.

   Opciones:
   1. Optimiza parámetros:
      - Ajusta niveles de RSI
      - Cambia timeframe
      - Añade filtros de tendencia

   2. Prueba estrategia diferente:
      /backtest "Buy when price bounces off MA200 with RSI < 35"

   3. Analiza por qué falla:
      - ¿Muchos falsos breakouts?
      - ¿Stop loss muy cercano?
      - ¿Take profit muy lejano?
🔗 Más info: .claude/skills/backtesting/SKILL.md
```

---

## 📉 Advanced Analytics (ERR_AA_xxx)

### ERR_AA_001: No Trade History
**Causa:** No hay trades para analizar

**Razones comunes:**
- Cuenta nueva sin historial
- Periodo de análisis sin trades
- Filtros muy restrictivos

**Solución:**
1. Ejecutar algunos trades primero
2. Importar historial de MetaTrader
3. Ajustar periodo de análisis

**Mensaje al usuario:**
```
❌ ERR_AA_001: No hay trades para calcular Sharpe ratio
📊 Detalles: El historial de trading está vacío
💡 Solución:
   Para calcular métricas necesitas historial de trades.

   Opciones:
   1. Si eres nuevo:
      - Ejecuta al menos 10-20 trades en demo
      - Documenta resultados
      - Luego usa analytics para revisar desempeño

   2. Si tienes historial en MetaTrader:
      - Importa deals: "get deals from last 3 months"
      - Luego: "calculate Sharpe ratio from imported data"

   3. Si no tienes trades aún:
      - Comienza con backtesting: /backtest
      - Luego opera en demo
      - Finalmente usa analytics
🔗 Más info: .claude/skills/advanced-analytics/SKILL.md
```

---

### ERR_AA_002: Insufficient Sample Size
**Causa:** Muy pocos trades para análisis estadístico significativo

**Razones comunes:**
- Menos de 20 trades
- Periodo muy corto
- Estrategia genera pocas señales

**Solución:**
1. Esperar más trades
2. Extender periodo de análisis
3. Usar con precaución

**Mensaje al usuario:**
```
⚠️ ERR_AA_002: Solo 8 trades (mínimo 20 para significancia estadística)
📊 Detalles:
   - Trades analizados: 8
   - Mínimo recomendado: 20
   - Ideal: 50+

💡 Interpretación:
   Puedo calcular las métricas, pero no son muy confiables.

   Con 8 trades:
   ✅ Puedo calcular: Win rate básico, avg R:R
   ⚠️ Poco confiable: Sharpe ratio, Sortino, estadísticas avanzadas
   ❌ No recomendado: Tomar decisiones importantes basado en esto

   Recomendación:
   1. Opera al menos 20 trades más
   2. Luego repite el análisis
   3. Decisiones importantes requieren 50+ trades
🔗 Más info: .claude/skills/advanced-analytics/SKILL.md
```

---

### ERR_AA_003: Data Quality Issues
**Causa:** Problemas con calidad de datos

**Razones comunes:**
- Trades con datos incompletos
- Precios de entrada/salida faltantes
- Trades duplicados

**Solución:**
1. Limpiar datos
2. Revisar importación
3. Excluir trades problemáticos

**Mensaje al usuario:**
```
⚠️ ERR_AA_003: Problemas de calidad detectados en datos
📊 Detalles:
   - Trades con SL/TP faltante: 5
   - Trades con profit = 0: 2
   - Posibles duplicados: 1

💡 Solución:
   Voy a proceder excluyendo trades problemáticos.

   Trades válidos para análisis: 43 de 50
   Trades excluidos: 7

   Si necesitas incluir todos:
   1. Revisa historial en MetaTrader
   2. Completa datos faltantes manualmente
   3. Reimporta datos limpios
🔗 Más info: .claude/skills/advanced-analytics/troubleshooting.md
```

---

## 🔧 General Errors (ERR_GEN_xxx)

### ERR_GEN_001: Timeout
**Causa:** Operación tardó más de 2 minutos

**Razones comunes:**
- Demasiados datos para procesar
- Servidor lento
- Conexión inestable

**Solución:**
1. Reducir cantidad de datos
2. Verificar conexión a internet
3. Dividir operación en partes más pequeñas

**Mensaje al usuario:**
```
❌ ERR_GEN_001: Operación cancelada por timeout (> 2 minutos)
📊 Detalles: El comando tardó demasiado en completarse
💡 Solución:
   Reduce el alcance de la operación:

   Si estabas:
   - Escaneando 50 símbolos → Reduce a 10-15
   - Backtesting 2 años → Reduce a 6 meses
   - Analizando múltiples timeframes → Analiza uno a la vez

   Ejemplo:
   En vez de: /opportunities (todos)
   Usa: /opportunities majors (solo pares principales)
🔗 Más info: contacta support si persiste
```

---

### ERR_GEN_002: MCP Server Error
**Causa:** Error general del servidor MCP

**Razones comunes:**
- MCP server crasheó
- MetaTrader perdió conexión
- Error en configuración

**Solución:**
1. Reiniciar MetaTrader
2. Reiniciar Claude Code
3. Verificar configuración MCP

**Mensaje al usuario:**
```
❌ ERR_GEN_002: Error del servidor MCP
📊 Detalles: El servidor MCP encontró un problema inesperado
💡 Solución:
   1. Reinicia MetaTrader 5 completamente
   2. Reinicia Claude Code
   3. Reintenta el comando

   Si el error persiste:
   - Verifica logs en MetaTrader (Tools → Options → Experts)
   - Revisa configuración en .claude/settings.local.json
   - Reporta el error con mensaje completo
🔗 Más info: .claude/skills/troubleshooting.md
```

---

### ERR_GEN_003: Invalid Parameter
**Causa:** Parámetro proporcionado no es válido

**Razones comunes:**
- Formato incorrecto
- Valor fuera de rango
- Tipo de dato incorrecto

**Solución:**
1. Verificar formato del parámetro
2. Ver ejemplos en documentación
3. Usar valores válidos

**Mensaje al usuario:**
```
❌ ERR_GEN_003: Parámetro 'risk:5%' tiene formato inválido
📊 Detalles: El valor debe ser un número sin el símbolo %
💡 Solución:
   Formato correcto:

   ❌ risk:5%
   ✅ risk:5

   ❌ entry:1.0850.00
   ✅ entry:1.0850

   ❌ stop:1.0820pips
   ✅ stop:1.0820

   Ejemplo completo:
   /risk EURUSD entry:1.0850 stop:1.0820 risk:2
🔗 Más info: Ver documentación del comando específico
```

---

## 🎨 Template de Mensajes de Error

Formato estándar para todos los errores:

```
❌ [ERROR_CODE]: [Descripción breve del error]
📊 Detalles: [Información específica del contexto]
💡 Solución: [Pasos concretos y accionables]
🔗 Más info: [Link a documentación relevante]
```

**Ejemplo de implementación en código:**

```python
class TradingError(Exception):
    def __init__(self, code, description, details, solution, docs_link):
        self.code = code
        self.description = description
        self.details = details
        self.solution = solution
        self.docs_link = docs_link

    def format_message(self):
        return f"""
❌ {self.code}: {self.description}
📊 Detalles: {self.details}
💡 Solución: {self.solution}
🔗 Más info: {self.docs_link}
"""

# Uso
raise TradingError(
    code="ERR_PS_001",
    description="Datos insuficientes para M15",
    details=f"Solo {len(candles)} velas disponibles (se requieren 50+)",
    solution="Descarga más historia en MetaTrader (Tools → History Center)",
    docs_link=".claude/skills/pattern-scanner/troubleshooting.md"
)
```

---

## 📝 Implementación en Skills

### Ejemplo: pattern-scanner

```python
# En scripts/run_scan.py

def validate_candle_data(symbol, timeframe, candles):
    """Validate that we have enough candles for pattern detection"""

    MIN_CANDLES = 50

    if len(candles) < MIN_CANDLES:
        raise InsufficientDataError(
            code="ERR_PS_001",
            description=f"Datos insuficientes para {timeframe}",
            details=f"Solo {len(candles)} velas disponibles (se requieren {MIN_CANDLES}+)",
            solution=f"""
1. Abre MetaTrader 5
2. Tools → History Center
3. Selecciona {symbol} → {timeframe}
4. Click "Download" para obtener más historia
5. Reintenta el scan
            """,
            docs_link=".claude/skills/pattern-scanner/troubleshooting.md"
        )

    return True

def validate_symbol(symbol, available_symbols):
    """Validate that symbol exists in broker"""

    if symbol not in available_symbols:
        # Find similar symbols
        similar = [s for s in available_symbols if symbol[:3] in s]

        suggestion = f"\n¿Quisiste decir '{similar[0]}'?" if similar else ""
        symbol_list = "\n".join(similar[:5]) if similar else "Use 'get all symbols'"

        raise InvalidSymbolError(
            code="ERR_PS_002",
            description=f"Símbolo '{symbol}' no encontrado",
            details=f"El símbolo solicitado no existe en tu broker{suggestion}",
            solution=f"""
Símbolos disponibles que coinciden:
{symbol_list}

Para ver todos: "get all available symbols"
            """,
            docs_link=".claude/skills/pattern-scanner/troubleshooting.md"
        )
```

### Ejemplo: risk-management

```python
# En risk calculation script

def validate_risk_parameters(balance, risk_pct, entry, stop):
    """Validate risk management parameters"""

    MAX_RISK_PCT = 2.0
    MIN_STOP_DISTANCE_PIPS = 10

    # Check risk percentage
    if risk_pct > MAX_RISK_PCT:
        risk_amount = balance * (risk_pct / 100)
        max_amount = balance * (MAX_RISK_PCT / 100)

        raise ExcessiveRiskError(
            code="ERR_RM_001",
            description=f"Riesgo de ${risk_amount:.2f} excede límite",
            details=f"""
Balance: ${balance:,.2f}
Riesgo solicitado: ${risk_amount:.2f} ({risk_pct}%)
Máximo recomendado: ${max_amount:.2f} ({MAX_RISK_PCT}%)
            """,
            solution=f"""
Nunca arriesgues más del {MAX_RISK_PCT}% por trade.

Comando correcto:
/risk SYMBOL entry:{entry} stop:{stop} risk:{MAX_RISK_PCT}
            """,
            docs_link=".claude/skills/risk-management/SKILL.md"
        )

    # Check stop loss distance
    stop_distance_pips = abs(entry - stop) * 10000
    if stop_distance_pips < MIN_STOP_DISTANCE_PIPS:
        raise InvalidStopLossError(
            code="ERR_RM_003",
            description="Stop loss demasiado cercano",
            details=f"""
Entry: {entry}
Stop loss: {stop} (solo {stop_distance_pips:.0f} pips)
Mínimo: {MIN_STOP_DISTANCE_PIPS} pips
            """,
            solution=f"""
Coloca stop loss en nivel técnico:
- Debajo de soporte reciente
- Debajo de swing low
- Mínimo {MIN_STOP_DISTANCE_PIPS} pips de distancia
            """,
            docs_link=".claude/skills/risk-management/SKILL.md"
        )
```

---

## 🔍 Debugging y Troubleshooting

### Cómo Usar los Códigos de Error

1. **Usuario ve error** → Identifica el código (ERR_XX_YYY)
2. **Busca en este documento** → Lee descripción y causa
3. **Sigue solución propuesta** → Pasos concretos para resolver
4. **Si persiste** → Consulta docs_link para más detalles

### Reportar Errores

Si un error persiste después de seguir las soluciones:

1. Anota el código de error completo
2. Copia el mensaje de error
3. Documenta pasos para reproducir
4. Reporta en GitHub Issues con template:

```markdown
## Error Report

**Error Code:** ERR_PS_001

**Descripción:**
[Copia el mensaje de error completo]

**Pasos para reproducir:**
1. /scan EURUSD
2. [describe qué hiciste]

**Configuración:**
- OS: Windows 11
- Claude Code version: 1.x
- MetaTrader 5 build: XXXX
- Broker: [nombre]

**Logs:**
[Pega logs relevantes si están disponibles]
```

---

## 📚 Referencias

- **Pattern Scanner:** `.claude/skills/pattern-scanner/troubleshooting.md`
- **Technical Analysis:** `.claude/skills/technical-analysis/troubleshooting.md`
- **Risk Management:** `.claude/skills/risk-management/SKILL.md`
- **Backtesting:** `.claude/skills/backtesting/troubleshooting.md`
- **Advanced Analytics:** `.claude/skills/advanced-analytics/SKILL.md`
- **MCP Configuration:** `.claude/settings.local.json`

---

**Última actualización:** 2025-10-30
**Versión:** 1.0
**Autor:** Trading Skills Project - Phase 2
