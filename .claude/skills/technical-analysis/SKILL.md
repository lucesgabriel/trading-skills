---
name: technical-analysis
description: Use when analyzing market trends, evaluating technical indicators, or calculating success probabilities for forex trading signals.
---

# Technical Analysis Skill

## Purpose
Comprehensive technical analysis for forex and financial markets using MetaTrader data and multiple indicators to identify trading opportunities with calculated success probabilities.

## When to Use This Skill

**Primary Triggers:**
- "analyze [SYMBOL]" or "technical analysis for [SYMBOL]"
- "what are the indicators showing for [SYMBOL]?"
- "is [SYMBOL] bullish or bearish?"
- "give me a trading signal for [SYMBOL]"

**Use Cases:**
- User wants comprehensive multi-indicator analysis
- User needs trend direction and market conditions
- User asks for success probability calculations
- User wants trading signals with entry/stop/target levels

**Example Inputs:**
```
✓ "analyze EURUSD"
✓ "what's the trend on GBPUSD?"
✓ "give me indicators for XAUUSD"
✓ "is USDJPY showing a buy signal?"
✗ "scan for patterns" → Use pattern-scanner skill instead
```

## Core Analysis Methodology

### 1. Multi-Timeframe Analysis
Always analyze at least 3 timeframes for context:
- **Higher Timeframe (H4/Daily)**: Overall trend direction
- **Trading Timeframe (H1)**: Entry signals and patterns
- **Lower Timeframe (M15)**: Precise entry timing

### 2. Essential Indicators to Calculate

#### Trend Indicators
- **Moving Averages**:
  - Calculate SMA(20), SMA(50), SMA(200) from candle data
  - EMA(12), EMA(26) for MACD
  - Price position relative to MAs indicates trend strength

- **MACD (Moving Average Convergence Divergence)**:
  - MACD Line = EMA(12) - EMA(26)
  - Signal Line = EMA(9) of MACD Line
  - Histogram = MACD Line - Signal Line
  - Crossovers indicate momentum shifts

#### Momentum Indicators
- **RSI (Relative Strength Index)**:
  - Calculate 14-period RSI from price data
  - RSI > 70: Overbought (potential reversal down)
  - RSI < 30: Oversold (potential reversal up)
  - RSI 40-60: Neutral zone
  - Divergences are powerful signals

- **Stochastic Oscillator**:
  - %K = (Close - Lowest Low) / (Highest High - Lowest Low) × 100
  - %D = SMA(3) of %K
  - Values > 80: Overbought
  - Values < 20: Oversold

#### Volatility Indicators
- **Bollinger Bands**:
  - Middle Band = SMA(20)
  - Upper Band = SMA(20) + (2 × Standard Deviation)
  - Lower Band = SMA(20) - (2 × Standard Deviation)
  - Price touching bands indicates potential reversals
  - Band squeeze indicates volatility expansion coming

- **ATR (Average True Range)**:
  - Measures market volatility
  - Use for stop-loss calculation
  - Higher ATR = wider stops needed

### 3. Analysis Workflow

```
STEP 1: GET MARKET DATA
→ Use metatrader:get_symbol_price for current price
→ Use metatrader:get_candles_latest for historical data (at least 200 candles)
→ Analyze multiple timeframes (M15, H1, H4, Daily)

STEP 2: CALCULATE INDICATORS
→ Process candle data to calculate all indicators
→ Use pandas/numpy for calculations if needed
→ Store indicator values for comparison

STEP 3: IDENTIFY TREND
→ Check MA alignment and slope
→ Verify with MACD direction
→ Confirm with price action (higher highs/lows)

STEP 4: DETECT SIGNALS
→ Look for indicator confluences
→ Identify support/resistance levels
→ Check for divergences (RSI/MACD vs Price)
→ Spot chart patterns

STEP 5: CALCULATE SUCCESS PROBABILITY
→ Count confluence factors (more = higher probability)
→ Check historical patterns
→ Assess risk/reward ratio
→ Consider market conditions (trending vs ranging)

STEP 6: PRESENT FINDINGS
→ Clear trend direction
→ Key support/resistance levels
→ Entry/exit suggestions
→ Stop loss recommendations based on ATR
→ Probability assessment (percentage)
```

### 4. Success Probability Calculation

Use this weighted scoring system:

```python
# Confluence Factors (each adds 10-15%)
- Trend alignment across timeframes: +15%
- Multiple indicator confirmation: +15%
- Support/resistance at entry: +10%
- RSI in favorable zone: +10%
- MACD alignment: +10%
- Bollinger band position: +10%
- Volume confirmation: +10%
- Chart pattern present: +15%

# Deduction Factors
- Counter-trend trade: -20%
- High volatility period: -10%
- News event nearby: -15%
- Divergence against position: -15%

# Base probability: 50%
# Final probability = Base + Sum(Positive Factors) - Sum(Negative Factors)
# Cap between 30% and 85% (no trade is guaranteed)
```

### Scripts de Apoyo

Se incluye el script `scripts/indicator_suite.py` para automatizar cálculos y scoring consistentes.

**Funciones clave:**
- `candles_to_dataframe()` transforma velas de MetaTrader en DataFrame ordenado.
- `build_indicator_snapshot()` calcula SMA, EMA, MACD, RSI, Stochastic, Bollinger Bands y ATR en un paso.
- `score_direction()` genera probabilidades LONG/SHORT en el rango 30%-85% según confluencias.
- `generate_snapshot_from_candles()` produce un resumen listo para redactar en la respuesta.

**Ejemplo de uso:**
```python
import sys
from pathlib import Path
base = Path(r"C:/Users/luces/Downloads/trading-skills/.claude/skills/technical-analysis/scripts")
sys.path.append(str(base))

from indicator_suite import generate_snapshot_from_candles

candles = metatrader.get_candles_latest("EURUSD", "H1", 250)
snapshot = generate_snapshot_from_candles(candles, timeframe="H1")

print(snapshot["trend_bias"], snapshot["long_probability"])
```

**Ventajas:**
- Evita reescribir lógica de indicadores en cada análisis.
- Mantiene alineado el cálculo de probabilidades con la tabla de confluencias.
- El snapshot devuelto puede compartirse con otros skills como `opportunity-scanner` o `risk-management`.

### 5. Trading Opportunity Types

#### High Probability Setups (70%+ success rate)
- Trend continuation with multiple confirmations
- Support/resistance bounces with divergence
- Breakouts with volume confirmation
- Three timeframe alignment

#### Medium Probability Setups (55-70%)
- Single indicator signals
- Counter-trend reversals with confirmation
- Range trading in clear boundaries

#### Low Probability Setups (<55%)
- Counter-trend without strong reversal signals
- Conflicting indicators
- Low volume breakouts

## Implementation with MetaTrader Tools

### Getting Data
```python
# Get current price
metatrader:get_symbol_price(symbol_name="EURUSD")

# Get candle data for analysis
metatrader:get_candles_latest(
    symbol_name="EURUSD",
    timeframe="H1",  # or "M15", "H4", "D1"
    count=200  # enough for 200-period MA
)
```

### Example Analysis Output Format

```
=== TECHNICAL ANALYSIS: EURUSD ===

📊 MARKET OVERVIEW
Current Price: 1.0850
Spread: 1.2 pips
Market Status: High volatility

🎯 TREND ANALYSIS
Daily Trend: BULLISH ↑ (above SMA 50, 200)
H4 Trend: BULLISH ↑ (MA alignment positive)
H1 Trend: CONSOLIDATING (sideways)

📈 INDICATORS (H1 Timeframe)
Moving Averages:
  - Price above SMA(20): BULLISH
  - SMA(20) above SMA(50): BULLISH
  - SMA(50) above SMA(200): BULLISH

MACD:
  - MACD Line: 0.0023 (above signal)
  - Histogram: Increasing
  - Status: BULLISH momentum

RSI (14):
  - Value: 58 (neutral zone)
  - No divergence detected
  - Status: Room to rise

Bollinger Bands:
  - Position: Middle band
  - Width: Normal
  - Status: Neutral

Stochastic:
  - %K: 62, %D: 58
  - Status: Rising in neutral zone

🎯 KEY LEVELS
Resistance: 1.0890 (previous high)
Support: 1.0820 (SMA 50)
Major Support: 1.0780 (SMA 200)

💡 TRADING OPPORTUNITY
Type: LONG (Buy)
Entry: 1.0850 - 1.0855
Stop Loss: 1.0820 (30 pips, based on ATR)
Take Profit 1: 1.0890 (40 pips)
Take Profit 2: 1.0920 (70 pips)
Risk/Reward: 1:2.3

✅ CONFLUENCE FACTORS
+ Uptrend across all timeframes (+15%)
+ MACD bullish (+10%)
+ Price above key MAs (+10%)
+ Support at SMA 50 (+10%)
+ RSI in buy zone (+10%)
+ Bullish momentum (+10%)

📊 SUCCESS PROBABILITY: 75%

Reasoning: Multiple timeframe alignment, strong MA support,
bullish momentum across indicators. Entry at key support level
with favorable risk/reward ratio.

⚠️ RISK FACTORS
- Watch for news events (ECB announcements)
- Monitor for RSI divergence at highs
- Respect stop loss (volatility possible)
```

## Advanced Techniques

### Pattern Recognition
Look for these high-probability patterns:
- **Head and Shoulders**: Reversal pattern
- **Double Top/Bottom**: Reversal signals
- **Triangles**: Continuation/breakout setups
- **Flags and Pennants**: Continuation patterns
- **Cup and Handle**: Bullish continuation

### Divergence Detection
- **Bullish Divergence**: Price makes lower low, RSI makes higher low
- **Bearish Divergence**: Price makes higher high, RSI makes lower high
- These are powerful reversal signals

### Volume Analysis
- Breakouts need volume confirmation
- Low volume rallies often fail
- Volume spikes indicate strong moves

## Risk Management Integration

### Position Sizing
```
Risk Per Trade = Account Balance × Risk % (usually 1-2%)
Position Size = Risk Per Trade / (Entry Price - Stop Loss Price)
```

### Stop Loss Calculation
```
ATR-based Stop: Entry ± (2 × ATR)
Support/Resistance Stop: Just beyond key level
Percentage Stop: 1-3% from entry
```

## Best Practices

1. **Never trade on single indicator**: Always look for confluence
2. **Respect the trend**: Trend trades have higher success rates
3. **Use multiple timeframes**: Avoid trading against higher TF trend
4. **Wait for confirmation**: Don't jump into trades early
5. **Manage risk**: Never risk more than 2% per trade
6. **Document everything**: Track your analysis accuracy
7. **Adapt to conditions**: Trending vs ranging markets need different approaches

## Common Mistakes to Avoid

❌ Over-relying on one indicator
❌ Ignoring higher timeframe context
❌ Trading during major news without protection
❌ Moving stops to avoid losses
❌ Averaging down on losing positions
❌ Revenge trading after losses
❌ Ignoring risk management rules

## Integration with Other Skills

- **Opportunity Scanner**: Use this analysis to screen multiple symbols
- **Trade Management**: Apply this analysis to open positions
- **Backtest Results**: Validate strategies with historical data
- **Risk Calculator**: Size positions based on this analysis

---

Remember: No analysis guarantees success. Always use proper risk management and never risk more than you can afford to lose.
