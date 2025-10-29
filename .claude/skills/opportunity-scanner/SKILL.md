---
name: opportunity-scanner
description: Automatically scan multiple currency pairs, indices, and commodities to identify best trading opportunities with ranked probability scores. Use when user asks "what should I trade today", "scan the market", requests market watchlist, or wants to compare opportunities across symbols like EURUSD, GBPUSD, XAUUSD, etc.
---

# Trading Opportunity Scanner Skill

## Purpose
Automatically scan multiple currency pairs and symbols to identify the best trading opportunities based on technical analysis, with ranked probability scores.

## When to Use This Skill
- User wants to find trading opportunities across multiple symbols
- User asks "what should I trade today?"
- User requests a market scan or watchlist
- User wants to compare opportunities across different pairs

## Scanner Workflow

### 1. Symbol Selection

#### Major Forex Pairs (High Liquidity)
```
- EURUSD (Euro/US Dollar)
- GBPUSD (British Pound/US Dollar)
- USDJPY (US Dollar/Japanese Yen)
- USDCHF (US Dollar/Swiss Franc)
- AUDUSD (Australian Dollar/US Dollar)
- USDCAD (US Dollar/Canadian Dollar)
- NZDUSD (New Zealand Dollar/US Dollar)
```

#### Minor & Exotic Pairs (Medium to Lower Liquidity)
```
- EURJPY, EURGBP, EURCHF
- GBPJPY, GBPCHF, GBPAUD
- AUDJPY, AUDCAD, AUDNZD
- CADJPY, CHFJPY
```

#### Indices (if available in broker)
```
- US30 (Dow Jones)
- US500 (S&P 500)
- NAS100 (Nasdaq)
- GER40 (DAX)
- UK100 (FTSE)
```

#### Commodities (if available)
```
- XAUUSD (Gold)
- XAGUSD (Silver)
- USOIL (Crude Oil)
```

### 2. Scanning Process

```
FOR EACH symbol IN symbol_list:

    STEP 1: Get Current Market Data
    → metatrader:get_symbol_price(symbol_name)
    → Check if market is open and tradeable

    STEP 2: Get Multi-Timeframe Candles
    → H4 candles (200 count) - Trend context
    → H1 candles (200 count) - Trading timeframe
    → M15 candles (100 count) - Entry precision

    STEP 3: Quick Technical Analysis
    → Calculate key indicators (MA, RSI, MACD)
    → Identify trend direction
    → Detect signals and patterns

    STEP 4: Score the Opportunity
    → Apply scoring matrix (see below)
    → Calculate success probability
    → Determine trade direction (BUY/SELL)

    STEP 5: Risk/Reward Assessment
    → Identify stop loss level
    → Identify take profit targets
    → Calculate R:R ratio

    STEP 6: Add to Results
    → Store if probability > 60%
    → Include all relevant details

STEP 7: Rank Opportunities
→ Sort by probability score (highest first)
→ Present top 5-10 opportunities

STEP 8: Generate Report
→ Summary of best opportunities
→ Quick trade setup for each
→ Market overview and conditions
```

### 3. Opportunity Scoring Matrix

```python
def score_opportunity(symbol_data):
    score = 0
    factors = []

    # TREND ALIGNMENT (Max 25 points)
    if all_timeframes_aligned():
        score += 25
        factors.append("Multi-timeframe trend alignment")
    elif two_timeframes_aligned():
        score += 15
        factors.append("Partial trend alignment")

    # MOMENTUM (Max 20 points)
    if rsi_in_favorable_zone() and macd_aligned():
        score += 20
        factors.append("Strong momentum")
    elif rsi_in_favorable_zone() or macd_aligned():
        score += 10
        factors.append("Moderate momentum")

    # SUPPORT/RESISTANCE (Max 15 points)
    if at_key_support_resistance():
        score += 15
        factors.append("At key S/R level")
    elif near_support_resistance():
        score += 8
        factors.append("Near S/R level")

    # PATTERN (Max 15 points)
    if high_probability_pattern_detected():
        score += 15
        factors.append("High-probability pattern")

    # VOLATILITY (Max 10 points)
    if normal_volatility():
        score += 10
        factors.append("Normal volatility")
    elif low_volatility():
        score += 5
        factors.append("Low volatility (breakout potential)")

    # RISK/REWARD (Max 15 points)
    rr_ratio = calculate_risk_reward()
    if rr_ratio >= 2.5:
        score += 15
        factors.append(f"Excellent R:R ({rr_ratio}:1)")
    elif rr_ratio >= 1.5:
        score += 10
        factors.append(f"Good R:R ({rr_ratio}:1)")
    elif rr_ratio >= 1.0:
        score += 5
        factors.append(f"Acceptable R:R ({rr_ratio}:1)")

    # Total Score: 0-100
    # Convert to probability: 50% + (score/2)
    # This gives range of 50-100% probability

    probability = 50 + (score / 2)

    return {
        'score': score,
        'probability': min(probability, 85),  # Cap at 85%
        'factors': factors
    }
```

### 4. Quick Analysis Per Symbol

For each symbol, perform this streamlined analysis:

#### A. Trend Detection (Fast)
```python
# Get last 50 candles of H1
candles = get_candles(symbol, "H1", 50)

# Quick MA calculation
sma_20 = average(close_prices[-20:])
sma_50 = average(close_prices[-50:])
current_price = close_prices[-1]

# Determine trend
if current_price > sma_20 > sma_50:
    trend = "BULLISH"
elif current_price < sma_20 < sma_50:
    trend = "BEARISH"
else:
    trend = "NEUTRAL"
```

#### B. Momentum Check (Fast)
```python
# Calculate 14-period RSI
rsi = calculate_rsi(close_prices, period=14)

# Quick MACD
ema_12 = ema(close_prices, 12)
ema_26 = ema(close_prices, 26)
macd = ema_12 - ema_26
signal = ema(macd, 9)

momentum = {
    'rsi': rsi,
    'rsi_zone': 'overbought' if rsi > 70 else 'oversold' if rsi < 30 else 'neutral',
    'macd_signal': 'bullish' if macd > signal else 'bearish'
}
```

#### C. Signal Detection
```python
# Look for actionable signals
signals = []

# Trend + Momentum alignment
if trend == "BULLISH" and macd > signal and 30 < rsi < 70:
    signals.append(("BUY", "Trend + Momentum alignment"))

if trend == "BEARISH" and macd < signal and 30 < rsi < 70:
    signals.append(("SELL", "Trend + Momentum alignment"))

# Oversold bounce in uptrend
if trend == "BULLISH" and rsi < 35:
    signals.append(("BUY", "Oversold bounce in uptrend"))

# Overbought rejection in downtrend
if trend == "BEARISH" and rsi > 65:
    signals.append(("SELL", "Overbought rejection in downtrend"))
```

### 5. Output Format

```
╔════════════════════════════════════════════════════════════╗
║           MARKET SCANNER - TRADING OPPORTUNITIES           ║
║                    [Date & Time]                           ║
╚════════════════════════════════════════════════════════════╝

📊 SCAN SUMMARY
Symbols Scanned: 15
Opportunities Found: 7
High Probability (>70%): 3
Medium Probability (60-70%): 4

═══════════════════════════════════════════════════════════════

🥇 TOP OPPORTUNITY #1

Symbol: EURUSD
Current Price: 1.0850
Direction: BUY 📈
Probability: 78%

Setup:
  Entry: 1.0845 - 1.0855
  Stop Loss: 1.0815 (30 pips)
  Take Profit: 1.0920 (70 pips)
  Risk/Reward: 1:2.3

Confluence Factors:
  ✓ Bullish trend on all timeframes
  ✓ MACD bullish crossover
  ✓ RSI at 52 (room to rise)
  ✓ At key support level (SMA 50)
  ✓ Excellent R:R ratio

Key Levels:
  Support: 1.0820, 1.0780
  Resistance: 1.0890, 1.0920

Note: Strong momentum, consider scaling in

───────────────────────────────────────────────────────────────

🥈 TOP OPPORTUNITY #2

Symbol: GBPJPY
Current Price: 195.45
Direction: SELL 📉
Probability: 72%

Setup:
  Entry: 195.40 - 195.50
  Stop Loss: 196.00 (50 pips)
  Take Profit: 194.00 (140 pips)
  Risk/Reward: 1:2.8

Confluence Factors:
  ✓ Bearish trend H4 and Daily
  ✓ Overbought on RSI (73)
  ✓ At resistance level
  ✓ Bearish divergence detected
  ✓ High volatility pair (good for swing)

Key Levels:
  Resistance: 195.80, 196.20
  Support: 194.50, 193.80

Note: Wait for rejection confirmation

───────────────────────────────────────────────────────────────

🥉 TOP OPPORTUNITY #3

Symbol: XAUUSD (Gold)
Current Price: 2015.50
Direction: BUY 📈
Probability: 70%

Setup:
  Entry: 2012.00 - 2016.00
  Stop Loss: 2005.00 ($ 7-11)
  Take Profit: 2035.00 ($ 19-23)
  Risk/Reward: 1:2.1

Confluence Factors:
  ✓ Uptrend on Daily
  ✓ Bounce from support zone
  ✓ RSI showing bullish divergence
  ✓ Safe-haven demand increasing
  ✓ Technical and fundamental alignment

Key Levels:
  Support: 2010, 2000 (psychological)
  Resistance: 2025, 2035

Note: Check USD news events

═══════════════════════════════════════════════════════════════

📋 OTHER OPPORTUNITIES (60-69% Probability)

4. AUDUSD - SELL at 0.6520 (65%)
   R:R 1:1.8, Bearish reversal pattern

5. USDCAD - BUY at 1.3750 (63%)
   R:R 1:1.5, Trend continuation

6. USDJPY - BUY at 149.80 (62%)
   R:R 1:1.6, Support bounce

7. EURJPY - SELL at 162.30 (60%)
   R:R 1:1.4, Resistance rejection

═══════════════════════════════════════════════════════════════

⚠️ MARKET CONDITIONS

Overall Sentiment: RISK-ON
Volatility: MODERATE
USD Strength: NEUTRAL
Key Events Today:
  - 14:30 UTC: US GDP Data
  - 18:00 UTC: Fed Speaker

📌 TRADING NOTES

✓ Best setups: EURUSD, GBPJPY, XAUUSD
✓ Market favoring trend continuation
⚠ Watch for USD volatility around news
⚠ Adjust position sizes for high-volatility pairs

═══════════════════════════════════════════════════════════════
Last Updated: [Timestamp]
Next Scan Recommended: In 4 hours
```

### 6. Advanced Filtering Options

Allow users to customize scans:

```python
def scan_markets(filters=None):
    """
    filters = {
        'min_probability': 65,  # Only show 65%+ opportunities
        'direction': 'BUY',  # Only longs, or 'SELL', or 'BOTH'
        'risk_reward_min': 2.0,  # Minimum R:R ratio
        'symbols': ['EURUSD', 'GBPUSD'],  # Specific symbols
        'timeframe': 'H1',  # Primary analysis timeframe
        'max_results': 5,  # Top N opportunities
        'include_ranging': False  # Exclude ranging markets
    }
    """
```

### Scripts Disponibles

El archivo `scripts/market_scanner.py` encapsula toda la lógica anterior:

**Qué incluye:**
- Carga automática del `indicator_suite` del skill de análisis técnico.
- Función `scan_markets()` para obtener oportunidades rankeadas con filtros.
- Clase `ScannerFilters` para ajustar probabilidad mínima, dirección y número máximo de resultados.
- Objeto `Opportunity` con detalle por timeframe y notas de confluencia.

**Ejemplo de uso combinado con MetaTrader MCP:**
```python
import sys
from pathlib import Path

base = Path(r"C:/Users/luces/Downloads/trading-skills/.claude/skills")
sys.path.append(str(base / "opportunity-scanner" / "scripts"))

from market_scanner import scan_markets, ScannerFilters

class MCPProvider:
    def get_candles(self, symbol, timeframe, count):
        return metatrader.get_candles_latest(symbol, timeframe, count)

    def get_price(self, symbol):
        return metatrader.get_symbol_price(symbol)["ask"]

provider = MCPProvider()
symbols = ["EURUSD", "GBPUSD", "XAUUSD", "US500"]
filters = ScannerFilters(min_probability=65, direction="BOTH", max_results=5)

opps = scan_markets(provider=provider, symbols=symbols, filters=filters)
for opp in opps:
    print(opp.symbol, opp.direction, opp.probability, opp.risk_reward)
```

**Ventajas:**
- Reutiliza el scoring del skill técnico sin copiar código.
- Añade notas por timeframe (bias, volatilidad, probabilidad).
- Facilita enviar respuestas con ranking, R:R estimado y comentarios listos para presentar.

### 7. Real-Time Monitoring

For active monitoring mode:

```
CONTINUOUS SCAN MODE:
1. Scan every 15-30 minutes
2. Alert on new high-probability setups
3. Update existing opportunity status
4. Notify when signals invalidate
5. Track which opportunities triggered
```

### 8. Integration with MetaTrader Tools

```python
# Get available symbols from broker
symbols = metatrader:get_all_symbols()

# For each major pair
for symbol in priority_list:
    # Check if symbol exists in broker
    if symbol in symbols:
        # Get price data
        price = metatrader:get_symbol_price(symbol)

        # Get candles for analysis
        h4_candles = metatrader:get_candles_latest(symbol, "H4", 200)
        h1_candles = metatrader:get_candles_latest(symbol, "H1", 200)

        # Analyze and score
        opportunity = analyze_symbol(symbol, price, h4_candles, h1_candles)

        # Add to results if meets threshold
        if opportunity['probability'] >= threshold:
            opportunities.append(opportunity)

# Sort and present
opportunities.sort(key=lambda x: x['probability'], reverse=True)
```

## Best Practices

1. **Scan during active market hours**: Avoid low-liquidity periods
2. **Prioritize high-probability setups**: Focus on 70%+ opportunities
3. **Consider correlation**: Don't take multiple correlated trades
4. **Update regularly**: Markets change, rescan every 4-6 hours
5. **Validate manually**: Always check top opportunities yourself
6. **Track performance**: Record which scanner signals you trade

## Performance Tracking

Keep a log of scanner results:
```
Date | Symbol | Probability | Direction | Result | Actual %
-----|--------|-------------|-----------|--------|----------
10/27| EURUSD | 78%         | BUY       | WIN    | +2.3%
10/27| GBPJPY | 72%         | SELL      | WIN    | +2.8%
10/27| AUDUSD | 65%         | SELL      | LOSS   | -1.5%
```

This helps calibrate the probability model over time.

---

**Note**: This scanner provides technical analysis only. Always consider fundamental factors, news events, and overall market conditions before trading.
