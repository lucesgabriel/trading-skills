# Technical Analysis - Usage Examples

## Example 1: Basic Analysis for EURUSD

### Input
```
User: "Analyze EURUSD"
```

### Expected Claude Actions
1. Call `mcp__metatrader__get_symbol_price` for EURUSD current price
2. Call `mcp__metatrader__get_candles_latest` for H1 (100 candles)
3. Call `mcp__metatrader__get_candles_latest` for H4 (100 candles)
4. Call `mcp__metatrader__get_candles_latest` for D1 (100 candles)
5. Calculate indicators using scripts/indicator_suite.py
6. Analyze trend confluence across timeframes
7. Generate probability score

### Output Example
```
EURUSD Technical Analysis (2025-10-28 14:30 UTC)
Current Price: 1.0825

TREND ANALYSIS:
├─ Daily (D1): BULLISH ↗ (Strong)
│  └─ Price above SMA20, SMA50, SMA200
├─ 4-Hour (H4): BULLISH ↗ (Moderate)
│  └─ Recent pullback, respecting SMA50
└─ 1-Hour (H1): CONSOLIDATING ↔
   └─ Forming bull flag pattern

KEY INDICATORS:
├─ RSI(14): 58.2 (Neutral, room for upside)
├─ MACD: Bullish crossover on H4
├─ Stochastic: 45.3 (Neutral zone)
└─ Bollinger Bands: Price at middle band

SETUP IDENTIFIED:
Type: BUY continuation after pullback
Entry: 1.0820-1.0830
Stop Loss: 1.0790 (40 pips, below recent swing low)
Take Profit 1: 1.0880 (50 pips, R:R 1.25:1)
Take Profit 2: 1.0920 (90 pips, R:R 2.25:1)

Success Probability: 68% (Moderate-High)
Risk-Reward Ratio: 1:2.25
Timeframe: 4-12 hours

REASONING:
- Strong daily uptrend provides context
- H4 pullback offers value entry
- Multiple timeframe alignment
- RSI not overbought
- Clean support level
```

## Example 2: Multi-Symbol Comparison

### Input
```
User: "Compare EURUSD and GBPUSD technical setups"
```

### Expected Output
```
COMPARATIVE ANALYSIS: EURUSD vs GBPUSD

EURUSD (1.0825):
├─ Trend: BULLISH (3/3 timeframes aligned)
├─ Setup: Pullback entry
├─ Probability: 68%
└─ Risk-Reward: 1:2.25

GBPUSD (1.2645):
├─ Trend: MIXED (2/3 timeframes aligned)
├─ Setup: Range-bound
├─ Probability: 45%
└─ Risk-Reward: 1:1.5

RECOMMENDATION:
EURUSD offers superior setup due to:
1. Stronger trend alignment
2. Better risk-reward ratio
3. Higher success probability
4. Clearer support/resistance levels
```

## Example 3: Divergence Detection

### Input
```
User: "Check XAUUSD for divergences"
```

### Expected Output
```
XAUUSD Divergence Analysis

BULLISH DIVERGENCE DETECTED (H4):
Price: Making lower lows (2,015 → 2,008)
RSI: Making higher lows (35.2 → 38.5)

Significance: STRONG
- Indicates weakening selling pressure
- Potential reversal signal
- Confirmed across 3 RSI periods

Action: Wait for confirmation
- Entry trigger: Break above 2,018
- Stop below recent low: 2,005
- Target resistance: 2,035
- Probability: 62% (Moderate)
```

## Example 4: Timeframe-Specific Query

### Input
```
User: "What's the H1 trend for USDJPY?"
```

### Expected Output
```
USDJPY H1 Trend Analysis

Current: 149.85
Trend: BEARISH ↘ (Moderate strength)

Key Observations:
- Price below SMA20, SMA50
- Series of lower highs, lower lows
- MACD histogram negative
- RSI at 42 (weak momentum)

Immediate Levels:
Resistance: 150.10 (recent high)
Support: 149.50 (swing low)

Note: H4 and Daily show stronger downtrend
Recommendation: Align trades with higher timeframe bias
```

## Example 5: Pattern Recognition Request

### Input
```
User: "Find chart patterns on GBPJPY"
```

### Expected Output
```
GBPJPY Pattern Analysis (H4 Chart)

PATTERN IDENTIFIED: Ascending Triangle
├─ Formation: Last 48 hours
├─ Horizontal Resistance: 189.50 (tested 3x)
├─ Rising Support Line: 188.20 → 188.80
└─ Pattern completion: 75%

TRADING IMPLICATIONS:
Bullish Pattern (70% success rate)

Breakout Trade Setup:
├─ Entry: Above 189.60 (confirmed break + retest)
├─ Stop: Below 188.70 (pattern invalidation)
├─ Target 1: 190.40 (measured move)
├─ Target 2: 191.20 (extended target)
└─ R:R Ratio: 1:2.5

Alternative (if breakout fails):
Wait for breakdown below 188.20
```

## Tips for Best Results

### 1. Specify Timeframe When Relevant
- "Analyze EURUSD on H4"
- "What's the daily trend for XAUUSD?"

### 2. Mention Specific Indicators If Needed
- "Check RSI divergence on GBPUSD"
- "What's the MACD signal for USDJPY?"

### 3. Request Comparison for Context
- "Compare all USD pairs"
- "Which EUR pair has best setup?"

### 4. Ask for Specific Setup Types
- "Find reversal setups"
- "Show me breakout opportunities"
- "Any pullback entries available?"
