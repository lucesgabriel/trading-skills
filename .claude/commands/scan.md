---
description: Quick pattern scan for forex symbols across multiple timeframes
---

# Quick Pattern Scanner

Scan forex symbols for candlestick patterns and trading signals.

## Usage

Single symbol:
```
/scan EURUSD
```

Multiple symbols:
```
/scan EURUSD GBPUSD XAUUSD
```

## What It Does

Use the pattern-scanner skill to:

1. **Fetch Live Market Data** - Get current price and candles for M15, H1, H4, and D1 timeframes from MetaTrader
2. **Detect Patterns** - Identify 12+ candlestick patterns (Engulfing, Morning Star, Hammer, Doji, etc.)
3. **Calculate Probability** - Weighted confluence scoring across timeframes (D1: 40%, H4: 30%, H1: 20%, M15: 10%)
4. **Generate Report** - Create comprehensive HTML report with:
   - Visual pattern cards with explanations
   - Interactive candlestick charts
   - Technical indicator analysis (RSI, MACD, trend)
   - Complete trading setup (Entry/SL/TP)
   - Risk management recommendations
   - Professional vibrant design
5. **Display Results** - Show summary in console and auto-open HTML report

## Output Format

Console summary includes:
- Detected patterns with emojis
- Overall signal (LONG/SHORT/NEUTRAL)
- Probability score (25-90%)
- Entry price and stop loss
- Take profit levels (TP1, TP2, TP3)

HTML report location: `reports/[SYMBOL]_pattern_scan_[TIMESTAMP].html`

## Example

```
/scan EURUSD
```

Results in:
```
🔍 EURUSD Pattern Scan Complete

📊 Patterns Detected:
  🟢 Bullish Engulfing (H4) - 75% confidence
  🟢 Morning Star (D1) - 68% confidence

📈 Signal: LONG
🎯 Probability: 72%
💰 Entry: 1.0850
🛡️ Stop Loss: 1.0820 (30 pips)
🎯 TP1: 1.0880 | TP2: 1.0910 | TP3: 1.0940

📄 Full report: reports/EURUSD_pattern_scan_20251029_143022.html
```

## See Also

- `/analyze` - Full technical analysis with multiple indicators
- `/risk` - Position sizing and risk calculation
- `/opportunities` - Scan multiple symbols for best setups
