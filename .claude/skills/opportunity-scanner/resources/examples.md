# Opportunity Scanner - Usage Examples

## Example 1: Basic Market Scan

### Input
```
User: "Scan the market for opportunities"
User: "What should I trade today?"
```

### Expected Claude Actions
1. Get list of available symbols from MetaTrader
2. For each major pair (EURUSD, GBPUSD, USDJPY, etc.):
   - Fetch latest candles (H1, H4, D1)
   - Calculate key indicators
   - Assess trend strength
   - Identify setup quality
3. Rank opportunities by probability score
4. Present top 5 opportunities

### Output Example
```
MARKET OPPORTUNITY SCAN (2025-10-28 14:30 UTC)
Scanned: 15 symbols | Found: 8 opportunities | High-probability: 3

TOP OPPORTUNITIES (Ranked by Probability):

1. GBPUSD - BUY Setup ⭐⭐⭐⭐⭐
   ├─ Probability: 75% (High)
   ├─ Type: Trend continuation
   ├─ Entry: 1.2640-1.2650
   ├─ Stop: 1.2600 (40 pips)
   ├─ Target: 1.2740 (100 pips)
   ├─ R:R: 1:2.5
   └─ Reason: Strong H4 breakout, all MAs aligned, RSI healthy

2. EURUSD - BUY Setup ⭐⭐⭐⭐
   ├─ Probability: 68% (Moderate-High)
   ├─ Type: Pullback entry
   ├─ Entry: 1.0820-1.0830
   ├─ Stop: 1.0790 (40 pips)
   ├─ Target: 1.0920 (90 pips)
   ├─ R:R: 1:2.25
   └─ Reason: Bull flag on H4, daily uptrend, good support

3. XAUUSD - BUY Setup ⭐⭐⭐⭐
   ├─ Probability: 65% (Moderate-High)
   ├─ Type: Reversal
   ├─ Entry: 2015-2018
   ├─ Stop: 2005 (10-13 pts)
   ├─ Target: 2045 (30 pts)
   ├─ R:R: 1:2.5
   └─ Reason: Bullish divergence H4, oversold bounce

MODERATE OPPORTUNITIES:

4. AUDUSD - SELL Setup ⭐⭐⭐
   Probability: 58% | Entry: 0.6580 | R:R: 1:2

5. USDJPY - SELL Setup ⭐⭐⭐
   Probability: 55% | Entry: 149.90 | R:R: 1:1.8

AVOID / WAIT:

❌ USDCHF: Choppy, no clear setup (32% prob)
❌ NZDUSD: Range-bound, low volatility
❌ EURJPY: Mixed signals, conflicting timeframes

MARKET OVERVIEW:
USD: Mixed (weakening vs EUR/GBP, strong vs JPY/AUD)
Risk Sentiment: Moderate bullish
Best Sector: European currencies
```

## Example 2: Filtered Scan (Specific Criteria)

### Input
```
User: "Scan for BUY opportunities with >70% probability"
```

### Output Example
```
FILTERED SCAN: BUY setups >70% probability

Found 2 matches:

1. GBPUSD - 75% ⭐⭐⭐⭐⭐
   Strong breakout setup, multiple confirmations
   Entry: 1.2640 | Stop: 1.2600 | Target: 1.2740

2. EURGBP - 72% ⭐⭐⭐⭐⭐
   Bullish engulfing at support zone
   Entry: 0.8560 | Stop: 0.8540 | Target: 0.8620

Recommendation: GBPUSD offers best risk-reward
```

## Example 3: Scan Specific Instrument Category

### Input
```
User: "Scan all EUR pairs"
User: "What are the best Gold/XAU opportunities?"
```

### Output Example for EUR pairs:
```
EUR PAIRS SCAN (7 pairs analyzed)

BEST EUR OPPORTUNITIES:

1. EURUSD - BUY (68% prob) ⭐⭐⭐⭐
   EUR strengthening vs USD
   Entry: 1.0825 | R:R: 1:2.25

2. EURJPY - BUY (63% prob) ⭐⭐⭐⭐
   Breakout from consolidation
   Entry: 162.40 | R:R: 1:2.0

3. EURGBP - SELL (45% prob) ⭐⭐
   GBP relatively stronger
   Entry: 0.8580 | R:R: 1:1.5

EUR STRENGTH INDEX: +0.45 (Moderate bullish)
Best EUR trade: EURUSD
```

## Example 4: Commodity Scan

### Input
```
User: "Scan commodities"
```

### Output Example
```
COMMODITY SCAN

XAUUSD (Gold) - BUY ⭐⭐⭐⭐
├─ Price: $2,015
├─ Setup: Reversal from support
├─ Probability: 65%
└─ Target: $2,045 (+$30)

XAGUSD (Silver) - No clear setup ⭐⭐
├─ Price: $23.50
├─ Status: Range-bound
└─ Wait for breakout

XBRUSD (Brent Oil) - SELL ⭐⭐⭐
├─ Price: $85.20
├─ Setup: Breakdown continuation
├─ Probability: 58%
└─ Target: $83.50

BEST COMMODITY TRADE: Gold (XAUUSD)
```

## Example 5: Time-Specific Scan

### Input
```
User: "Scan for quick scalp opportunities (M15/H1)"
```

### Output Example
```
SCALPING OPPORTUNITIES (M15/H1 focus)

FAST SETUPS (Target: 20-40 pips, Duration: 1-4 hours):

1. GBPUSD - BUY M15 ⭐⭐⭐⭐
   Entry: 1.2645 | Stop: 1.2630 (15 pips)
   Target: 1.2675 (30 pips) | R:R: 1:2
   Probability: 62%

2. EURUSD - SELL H1 ⭐⭐⭐
   Entry: 1.0835 | Stop: 1.0850 (15 pips)
   Target: 1.0805 (30 pips) | R:R: 1:2
   Probability: 58%

Note: Lower timeframes = lower probability
Risk management critical for scalping
```

## Example 6: Market Watchlist

### Input
```
User: "Create a watchlist for today"
```

### Output Example
```
TODAY'S TRADING WATCHLIST (2025-10-28)

ACTIVE NOW (Trade immediately):
✓ GBPUSD - BUY @ 1.2640-1.2650
✓ EURUSD - BUY @ 1.0820-1.0830

WATCH FOR ENTRY (Monitor these):
👁 XAUUSD - Waiting for break above 2018
👁 USDJPY - Waiting for retest of 149.50
👁 AUDUSD - Watch 0.6580 breakdown

LONGER TERM (Next 24-48 hours):
📅 GBPJPY - Triangle breakout pending
📅 EURGBP - Range support test likely

AVOID TODAY:
❌ USDCHF, NZDUSD, CADCHF - No setups
```

## Scanner Configuration Tips

### For Best Results:

**High Probability Focus** (Conservative):
- Filter: >65% probability
- Focus: Major pairs only
- Timeframe: H4/D1
- Expected: 1-3 opportunities

**Balanced Approach** (Moderate):
- Filter: >55% probability
- Include: Major + minor pairs
- Timeframe: H1/H4
- Expected: 3-5 opportunities

**Active Trading** (Aggressive):
- Filter: >45% probability
- Include: All available symbols
- Timeframe: M15/H1/H4
- Expected: 5-10 opportunities

### When to Rescan:

- Every 4 hours (new candle formations)
- After major news events
- When existing setups trigger or fail
- At market open (Asia, London, NY sessions)

### Understanding Probability Scores:

- **75%+**: Excellent setup, multiple confirmations
- **65-74%**: Good setup, some minor concerns
- **55-64%**: Moderate setup, requires caution
- **45-54%**: Lower probability, only for experienced
- **<45%**: Avoid or wait for better entry
