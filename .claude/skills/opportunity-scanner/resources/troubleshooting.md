# Opportunity Scanner - Troubleshooting

## Common Issues and Solutions

### Issue 1: "Scanner returns no opportunities"

**Symptoms:**
- Scan completes but shows 0 opportunities
- Message: "No setups found"

**Causes & Solutions:**

**A. Filter criteria too strict**
```
If filtering for >70% probability:
- May only find 0-2 opportunities
- Try lowering to >55% for more results
```

**B. Low volatility market**
- Choppy/ranging markets = fewer clear setups
- Check ATR - if <30 pips, market is quiet
- Wait for better market conditions

**C. Scan timing**
```
Best times to scan:
✓ London open (8:00-12:00 GMT)
✓ NY open (13:00-17:00 GMT)
✓ After major news releases

Poor times:
❌ Asian session (low volatility)
❌ Friday afternoon (weekend approaching)
❌ Major holidays
```

---

### Issue 2: "Scanner takes too long"

**Symptoms:**
- Scan running >2 minutes
- Timeout errors

**Solutions:**

**A. Reduce symbol list**
```
❌ Scanning 50+ symbols: Too many
✓ Focus on: 10-15 major pairs
✓ Optimal: 7-8 most liquid pairs
```

**B. Optimize timeframe analysis**
```
✓ Standard: H1 + H4 (fast scan)
⚠️ Thorough: M15 + H1 + H4 (slower)
❌ Excessive: M5 + M15 + H1 + H4 + D1 (very slow)
```

**C. Reduce candle history**
```
✓ Quick scan: 50-100 candles
✓ Standard: 100-150 candles
❌ Slow: 500+ candles
```

---

### Issue 3: "Scanner shows conflicting opportunities"

**Symptoms:**
- EURUSD shows both BUY and SELL setups
- Opposite signals for same symbol

**Explanation:**
This can be NORMAL if:
- Different timeframes show different trends
- Multiple potential setups exist

**How to Handle:**

**A. Check timeframe**
```
Example:
- H1: SELL setup (short-term pullback)
- H4: BUY setup (overall uptrend)

Resolution: Follow higher timeframe (H4 BUY)
```

**B. Check probability scores**
```
EURUSD BUY: 68% probability
EURUSD SELL: 45% probability

Resolution: Take higher probability (BUY)
```

**C. Wait for clarity**
- If similar probabilities, skip the symbol
- Look for clearer opportunities

---

### Issue 4: "Recommended trades keep losing"

**Symptoms:**
- Scanner finds setups but they fail
- Consistent losses despite good probabilities

**Analysis:**

**A. Probability misunderstanding**
```
65% probability means:
✓ 65 out of 100 trades win
✗ NOT "this specific trade has 65% chance"

Even 75% setups lose 25% of the time!
```

**B. Execution issues**
- Entering too late (price moved)
- Not using recommended stops
- Moving stops too early
- Taking profit too early

**C. Market conditions changed**
```
Scanner shows snapshot in time.
By the time you enter (minutes/hours later):
- Setup may no longer be valid
- Price may have moved significantly
- Confirm setup still exists before entry
```

**Solutions:**
1. Enter immediately when setup found
2. Always use recommended stop loss
3. Let trades reach target (don't exit early)
4. Track win rate over 20+ trades, not 1-2

---

### Issue 5: "Cannot scan specific symbol group"

**Symptoms:**
- "Scan EUR pairs" shows no results
- Filter not working

**Solutions:**

**A. Symbol availability**
```bash
# First, check what symbols are available:
Call: mcp__metatrader__get_symbols(group="*EUR*")

# Then scan only available symbols
```

**B. Broker-specific names**
```
Some brokers use:
- EURUSD.a (OANDA)
- EURUSDm (micro lots)
- EURUSD# (某些 brokers)

Verify exact symbol names first
```

**C. Manual symbol list**
```
If automatic detection fails:
Provide explicit list: "Scan EURUSD, GBPUSD, USDJPY"
```

---

### Issue 6: "Scan results inconsistent"

**Symptoms:**
- Running same scan twice shows different results
- Probability scores change

**Explanation:**
This is EXPECTED behavior:

**A. Market moves**
```
Between scans (even minutes apart):
- New candles form
- Indicators update
- Setups evolve or disappear
```

**B. Data updates**
- MetaTrader receives new ticks
- Latest candle may not be closed yet
- Signals update in real-time

**Best Practice:**
- Trust the most recent scan
- Re-scan every 1-4 hours
- After major price moves, re-scan

---

### Issue 7: "Scan finds low-probability setups only"

**Symptoms:**
- All opportunities show 45-55%
- No high-probability setups

**Causes:**

**A. Market environment**
```
Choppy/ranging markets = Low probability setups
- Conflicting signals
- No clear trends
- Indecision candles

Solution: Wait for better market conditions
```

**B. Scan timing**
```
Low volatility periods:
- Asian session
- Low volume times
- Pre-holiday periods

Solution: Scan during high activity times
```

**C. This is normal sometimes**
- Not every day has A+ setups
- Better to wait than force trades
- Quality over quantity

---

### Issue 8: "Missing expected opportunities"

**Symptoms:**
- Manual analysis shows good setup
- Scanner doesn't identify it

**Possible Reasons:**

**A. Threshold filters**
```
Scanner may filter out if:
- Probability <50% (even if looks good visually)
- R:R ratio <1.5:1
- Stop loss too wide
- Conflicting timeframes
```

**B. Pattern recognition vs indicators**
```
Humans see: Chart patterns, visual trends
Scanner sees: Indicator values, mathematical signals

Both valid, but may disagree
```

**C. Request specific symbol**
```
Instead of: "Scan all pairs"
Try: "Analyze GBPUSD" (for detailed check)
```

---

### Issue 9: "Too many opportunities"

**Symptoms:**
- Scanner returns 15+ opportunities
- Overwhelming to choose

**Solutions:**

**A. Filter by probability**
```
"Scan for opportunities >70%"
Result: 2-4 high-quality setups
```

**B. Filter by R:R**
```
"Scan for setups with R:R >2:1"
Result: Better risk-reward only
```

**C. Focus on top 3**
```
Scanner ranks by probability
Always focus on top 3-5 opportunities
Ignore lower-ranked setups
```

**D. Limit symbols**
```
"Scan major pairs only" (7-8 symbols)
vs
"Scan all available" (30+ symbols)
```

---

### Issue 10: "Scanner and technical-analysis disagree"

**Symptoms:**
- Scanner: EURUSD 68% BUY
- Technical-analysis: EURUSD moderate setup
- Different assessments

**Explanation:**

**A. Different focus**
```
Scanner:
- Quick overview
- Comparative ranking
- Multi-symbol prioritization

Technical-Analysis:
- Deep dive single symbol
- More detailed indicator analysis
- Multiple timeframe depth
```

**B. Both are valid**
- Use scanner for discovery
- Use technical-analysis for validation
- Combine both for best results

**Workflow:**
```
1. Scanner: Find top 3 opportunities
2. Technical-analysis: Deep dive each
3. Trade the one with best detailed analysis
```

---

## Quick Diagnostic Checklist

- [ ] Scanner completed without errors
- [ ] Scanned during high-volume session
- [ ] Using realistic filters (>55% probability)
- [ ] Scanning 10-15 symbols maximum
- [ ] Market showing normal volatility
- [ ] Results updated in last 1-4 hours

## Performance Expectations

**Typical scan results:**
- High volatility market: 5-8 opportunities
- Normal market: 3-5 opportunities
- Low volatility: 0-2 opportunities
- Very quiet: 0 opportunities (normal!)

**Don't expect:**
- Opportunities every single scan
- All setups >70% probability
- Perfect consistency

## Getting Help

1. Try scanning major pairs only first
2. Check examples.md for proper usage
3. Verify individual symbol analysis works
4. Confirm MetaTrader connection active
