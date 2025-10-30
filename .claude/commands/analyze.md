---
description: Comprehensive technical analysis with multiple indicators and probability scoring
---

# Technical Analysis Command

Perform comprehensive multi-timeframe technical analysis for forex and financial markets.

## Usage

Basic analysis:
```
/analyze EURUSD
```

Multiple symbols:
```
/analyze EURUSD GBPUSD XAUUSD
```

Specific timeframes:
```
/analyze EURUSD --timeframes H4,D1
```

## What It Does

Use the technical-analysis skill to:

1. **Multi-Timeframe Analysis** - Analyze at least 3 timeframes for context (typically M15, H1, H4, D1)
2. **Technical Indicators** - Calculate and evaluate:
   - Moving Averages (20, 50, 200 SMA/EMA)
   - MACD (12, 26, 9) for momentum
   - RSI (14) for overbought/oversold conditions
   - Bollinger Bands for volatility
   - Stochastic Oscillator for entry timing
   - ATR for volatility measurement
3. **Trend Analysis** - Identify higher timeframe trends and alignment
4. **Support/Resistance** - Key levels and price action zones
5. **Success Probability** - Calculate weighted probability score based on indicator confluence
6. **Trading Signals** - Generate actionable BUY/SELL/NEUTRAL signals with complete setup

## Output Format

Analysis includes:

**Market Overview:**
- Current price and trend direction
- Higher timeframe context (D1, W1)
- Market structure (uptrend/downtrend/range)

**Indicator Snapshot:**
- MA alignment and crosses
- MACD histogram and signal line
- RSI level and divergence
- Bollinger Band position
- Stochastic signals

**Trading Signal:**
- Direction (LONG/SHORT/NEUTRAL)
- Success probability (%)
- Entry zone
- Stop loss placement
- Take profit targets (1:1.5, 1:2, 1:3 R:R)
- Position size recommendation

**Risk Assessment:**
- Volatility analysis (ATR)
- Key support/resistance levels
- Risk factors and considerations

## Example

```
/analyze GBPUSD
```

Results in:
```
📊 GBPUSD Technical Analysis

🔍 Market Overview:
  Current: 1.2650
  Trend: Uptrend (D1, H4 aligned)
  Structure: Higher highs, higher lows

📈 Indicator Snapshot:
  MA (50/200): Bullish cross confirmed
  MACD: Positive histogram, above signal
  RSI: 58 (neutral, room to move up)
  Bollinger: Mid-band, expanding
  Stochastic: 45% (approaching buy zone)

🎯 Trading Signal: LONG
✅ Probability: 68%

💰 Trade Setup:
  Entry: 1.2640-1.2660
  Stop Loss: 1.2600 (50 pips)
  TP1: 1.2710 (1:1)
  TP2: 1.2760 (1:2)
  TP3: 1.2810 (1:3)

⚠️ Risk Factors:
  - High-impact GBP news tomorrow
  - Resistance at 1.2700
  - Volatility moderate (ATR: 45 pips)
```

## See Also

- `/scan` - Candlestick pattern detection
- `/risk` - Calculate position size for this setup
- `/backtest` - Test this strategy on historical data
