---
description: Scan multiple symbols to find the best trading opportunities today
---

# Market Opportunity Scanner

Automatically scan multiple currency pairs, indices, and commodities to identify the best trading opportunities with ranked probability scores.

## Usage

Default scan (major forex pairs):
```
/opportunities
```

Custom symbol list:
```
/opportunities EURUSD GBPUSD USDJPY XAUUSD BTCUSD
```

Scan by category:
```
/opportunities --forex
/opportunities --commodities
/opportunities --indices
```

## What It Does

Use the opportunity-scanner skill to:

1. **Symbol Selection** - Scan default watchlist or custom symbols:
   - Major Forex: EURUSD, GBPUSD, USDJPY, USDCHF, AUDUSD, NZDUSD, USDCAD
   - Commodities: XAUUSD (Gold), XAGUSD (Silver), USOIL (Crude)
   - Indices: US30, SPX500, NAS100

2. **Parallel Analysis** - For each symbol, execute:
   - Technical analysis with multiple indicators
   - Pattern detection (if patterns present)
   - Probability calculation
   - Signal generation (LONG/SHORT/NEUTRAL)

3. **Ranking System** - Sort opportunities by:
   - Probability score (higher = better)
   - Signal strength
   - Risk:Reward ratio
   - Timeframe alignment

4. **Filtered Results** - Display only actionable setups:
   - Minimum 60% probability
   - Clear directional signal
   - Defined entry/stop/target

5. **Summary Report** - Console table with:
   - Symbol and signal direction
   - Probability score
   - Entry price
   - Risk:Reward ratio
   - Quick trade summary

## Output Format

Ranked table of opportunities:

```
🎯 Trading Opportunities - [DATE]

Scanned: 10 symbols | Found: 4 opportunities | Time: 45s

┌─────────┬────────┬──────────┬─────────┬─────┬──────────────────────────────┐
│ Symbol  │ Signal │ Prob (%) │ Entry   │ R:R │ Summary                      │
├─────────┼────────┼──────────┼─────────┼─────┼──────────────────────────────┤
│ GBPUSD  │ LONG   │ 72%      │ 1.2650  │ 1:2 │ MA cross, bullish engulfing  │
│ XAUUSD  │ LONG   │ 68%      │ 2045.50 │ 1:3 │ Trend continuation, RSI      │
│ EURUSD  │ SHORT  │ 65%      │ 1.0850  │ 1:2 │ Resistance rejection         │
│ USDJPY  │ LONG   │ 62%      │ 149.80  │ 1:2 │ Morning star pattern         │
└─────────┴────────┴──────────┴─────────┴─────┴──────────────────────────────┘

🥇 Best Opportunity: GBPUSD (72% probability)

💡 Recommended Action:
  1. GBPUSD - Long entry at 1.2650, SL: 1.2600, TP: 1.2750
  2. XAUUSD - Long entry at 2045.50, SL: 2035, TP: 2077
  3. EURUSD - Short entry at 1.0850, SL: 1.0880, TP: 1.0790
```

## Scanner Criteria

**Included if:**
- Probability ≥ 60%
- Clear signal (not NEUTRAL)
- Risk:Reward ≥ 1:1.5
- Valid entry/stop/target levels

**Excluded if:**
- Low probability (< 60%)
- Conflicting signals across timeframes
- Insufficient volatility (ATR too low)
- Major news events imminent

## Use Cases

**Daily Routine:**
```
/opportunities
```
Start your trading day by scanning the market for best setups.

**Diversification:**
```
/opportunities --forex --commodities
```
Find opportunities across different asset classes.

**Quick Check:**
```
/opportunities EURUSD GBPUSD XAUUSD
```
Focus on your preferred trading instruments.

## Workflow Integration

1. **Discovery** - `/opportunities` to find setups
2. **Deep Dive** - `/analyze GBPUSD` for best opportunity
3. **Pattern Confirmation** - `/scan GBPUSD` if needed
4. **Risk Calculation** - `/risk GBPUSD entry:X stop:Y`
5. **Execute Trade** - Place order in MetaTrader

## See Also

- `/analyze` - Deep analysis of top opportunity
- `/scan` - Pattern detection for specific symbol
- `/risk` - Calculate position size for chosen setup
