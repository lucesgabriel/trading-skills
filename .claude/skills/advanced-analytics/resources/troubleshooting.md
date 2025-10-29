# Advanced Analytics - Troubleshooting

## Common Issues

### Issue 1: "Sharpe Ratio seems incorrect"

**Symptoms:**
- Very high (>3) or negative Sharpe Ratio
- Doesn't match expected value

**Understanding Sharpe Ratio:**

**A. Formula**
```
Sharpe = (Return - Risk-Free Rate) / Standard Deviation of Returns

Typical values:
<1.0: Below average
1.0-2.0: Good
2.0-3.0: Very good
>3.0: Excellent (or possibly miscalculated)
```

**B. Common calculation errors**
```
❌ Using wrong timeframe for annualization
❌ Not subtracting risk-free rate
❌ Including outliers

✓ Use daily returns
✓ Annualize properly (√252 for daily)
✓ Verify data quality
```

**C. If negative**
- Strategy losing money
- Normal if in drawdown
- Need minimum profitability for positive Sharpe

---

### Issue 2: "Pattern recognition not finding patterns"

**Symptoms:**
- No candlestick patterns detected
- Analysis shows "No patterns found"

**Solutions:**

**A. Insufficient data**
```
Need minimum:
- 50 candles for single patterns
- 100 candles for complex patterns
- Recent data (last 24-48 hours)
```

**B. Timeframe too low/high**
```
M1-M5: Too noisy, false patterns
H1-H4: Optimal for pattern detection
D1: Fewer patterns but more significant
```

**C. Market conditions**
```
Ranging market: Fewer reversal patterns
Trending market: More continuation patterns

This is normal behavior
```

---

### Issue 3: "Correlation matrix shows unexpected values"

**Symptoms:**
- Correlations seem wrong
- Values outside -1 to +1 range (error)

**Verification:**

**A. Correlation period**
```
Different periods = Different results:
- 20-day: Recent correlation (volatile)
- 60-day: Standard (recommended)
- 252-day: Long-term (more stable)

Use 60-day for trading decisions
```

**B. Expected correlations**
```
EURUSD vs GBPUSD: +0.6 to +0.8 (normal)
EURUSD vs USDJPY: -0.4 to -0.6 (normal)
Gold vs USD pairs: Variable

If drastically different, verify:
- Data quality
- Date ranges match
- Symbols correct
```

**C. Correlation interpretation**
```
+0.8 to +1.0: Very strong positive
+0.5 to +0.8: Strong positive
+0.2 to +0.5: Moderate positive
-0.2 to +0.2: Weak/No correlation
-0.5 to -0.2: Moderate negative
-0.8 to -0.5: Strong negative
-1.0 to -0.8: Very strong negative
```

---

### Issue 4: "Monte Carlo simulation results too variable"

**Symptoms:**
- Running twice gives very different results
- Large variance in outcomes

**Explanation:**

**A. This is normal**
```
Monte Carlo uses randomness
Each run produces different sequence
This is the POINT - showing range of possibilities
```

**B. Increase simulation runs**
```
❌ 100 runs: Too few, high variance
✓ 1,000 runs: Acceptable
✓ 10,000 runs: Recommended
✓ 100,000 runs: Very precise (slow)
```

**C. Focus on distribution**
```
Don't look at single run
Look at:
- Median (50th percentile)
- 5th and 95th percentiles
- Probability of profit
- Risk of ruin
```

---

### Issue 5: "Sortino Ratio very different from Sharpe"

**Symptoms:**
- Sharpe: 1.2
- Sortino: 2.4
- Large difference

**Explanation:**

**A. This is often GOOD**
```
Sortino higher than Sharpe means:
- Downside volatility < Total volatility
- Returns asymmetric (good!)
- Larger wins than losses

Typical ratio: Sortino = 1.3-1.6x Sharpe
```

**B. If Sortino < Sharpe**
```
⚠️ Unusual situation
Means: More downside volatility than upside
Possible issues:
- Data error
- Large losses skewing results
- Check calculation
```

---

### Issue 6: "Advanced statistics calculation slow"

**Symptoms:**
- Long processing time
- Timeout errors

**Solutions:**

**A. Reduce data size**
```
✓ Last 3 months: Quick
✓ Last 6 months: Standard
⚠️ Last 2+ years: Slow
```

**B. Limit analyses**
```
Don't run all at once:
1. Performance stats first
2. Then pattern recognition
3. Then correlations
4. Monte Carlo last (slowest)
```

**C. Optimize timeframe**
```
Daily data: Faster calculation
Intraday data: Slower
Use daily for historical analysis
```

---

### Issue 7: "Risk of Ruin calculation seems off"

**Symptoms:**
- RoR 50% but winning consistently
- RoR 1% but losing money

**Understanding RoR:**

**A. Required inputs**
```
Must provide:
✓ Accurate win rate (historical)
✓ Actual R:R ratio achieved
✓ True risk % per trade
✓ Starting capital

Estimates produce inaccurate results
```

**B. RoR interpretation**
```
Based on:
- Running strategy infinite times
- Probability of hitting $0
- Under current parameters

Current losing ≠ High RoR
Current winning ≠ Low RoR

RoR is long-term probability
```

**C. Typical values**
```
<5%: Very safe ✓
5-10%: Acceptable ✓
10-20%: Elevated risk ⚠️
>20%: High risk ❌
>50%: Very dangerous ❌
```

---

### Issue 8: "Pattern detected but trade failed"

**Symptoms:**
- Bullish Engulfing detected
- Price went down instead

**Reality Check:**

**A. Patterns are probabilities**
```
Bullish Engulfing success rate: ~70%
This means:
✓ 70 out of 100 work
✗ 30 out of 100 fail

Single pattern failure is NORMAL
```

**B. Context matters**
```
Pattern success depends on:
- Trend direction
- Volume confirmation
- Support/resistance location
- Overall market conditions

Pattern + Context = Higher probability
Pattern alone = Lower probability
```

**C. Use as confirmation**
```
Don't trade pattern alone
Use with:
- Technical analysis
- Indicator confluence
- Proper risk management
```

---

### Issue 9: "Calmar Ratio negative"

**Symptoms:**
- Calmar showing negative value

**Explanation:**

**A. Formula**
```
Calmar = Annual Return / Max Drawdown

If annual return negative:
Result = Negative Calmar

This indicates losing strategy
```

**B. What it means**
```
Negative Calmar = Strategy losing money
Focus on:
1. Fixing strategy first
2. Then worry about Calmar ratio
```

---

### Issue 10: "Statistics for different periods inconsistent"

**Symptoms:**
- Last month: Sharpe 2.5
- Last 3 months: Sharpe 1.2
- Different values

**Explanation:**

**A. This is normal**
```
Short periods: More volatile metrics
Longer periods: More stable metrics

Recent performance can differ from historical
```

**B. Which to trust?**
```
For evaluation:
✓ Use longer period (3-6 months minimum)
✓ More statistically significant
✓ Less affected by lucky/unlucky streaks

Recent period shows:
- Current form
- Recent market conditions
- May not be sustainable
```

**C. Look for consistency**
```
Good strategy:
✓ Positive across all periods
✓ Similar Sharpe ratios
✓ Drawdowns within expected range

Red flags:
❌ Great last month, terrible before
❌ Wildly varying statistics
❌ Recent metrics drastically better (luck?)
```

---

## Advanced Analytics Checklist

Before running analytics:
- [ ] Minimum 3 months data (preferably 6-12)
- [ ] At least 30 trades completed
- [ ] Data quality verified (no gaps/errors)
- [ ] Accurate trade history imported
- [ ] Realistic trading costs included

## Interpretation Guidelines

**Sharpe Ratio:**
- >2.0: Excellent
- 1.0-2.0: Good
- 0.5-1.0: Acceptable
- <0.5: Poor

**Sortino Ratio:**
- Usually 1.3-1.6x Sharpe
- Higher is better
- >2.5: Very good downside protection

**Calmar Ratio:**
- >3.0: Excellent
- 2.0-3.0: Good
- 1.0-2.0: Acceptable
- <1.0: Poor

**Max Drawdown:**
- <10%: Excellent
- 10-15%: Good
- 15-25%: Acceptable
- >25%: High (risky)

**Risk of Ruin:**
- <5%: Safe
- 5-10%: Acceptable
- >10%: Too high

## Common Mistakes

1. **Over-interpreting short periods**
   - Need 3+ months minimum
   - More data = more reliable

2. **Ignoring context**
   - Market conditions matter
   - Trend vs range affects metrics

3. **Comparing incomparable**
   - Different timeframes
   - Different strategies
   - Different market conditions

4. **Expecting perfection**
   - All metrics have limitations
   - Use multiple metrics together
   - Focus on trends, not absolute values

## Getting Help

1. Verify input data quality
2. Check [examples.md](./examples.md) for interpretation
3. Compare against industry benchmarks
4. Use multiple time periods for validation
5. Consult [SKILLS_MCP_SETUP.md](../../../SKILLS_MCP_SETUP.md) for setup issues
