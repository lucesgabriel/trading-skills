# Backtesting - Troubleshooting

## Common Issues

### Issue 1: "Backtest results too good to be true"

**Symptoms:**
- 80%+ win rate
- Profit factor >3.0
- Perfect equity curve
- Max drawdown <3%

**Reality:**
⚠️ **LIKELY OVERFITTED**

**Causes:**

**A. Curve fitting**
```
❌ Optimized parameters to fit historical data exactly
✓ Parameters work on past data only
✗ Will fail in live trading

Solution: Use walk-forward analysis
```

**B. Look-ahead bias**
```
❌ Using future data in calculations
Example: Using close price before bar closes
Result: Impossible to replicate live

Solution: Ensure data available at decision time
```

**C. Unrealistic assumptions**
```
❌ No spreads/commissions
❌ Perfect fills at exact price
❌ Zero slippage

Solution: Add realistic trading costs
```

---

### Issue 2: "Backtest takes too long"

**Symptoms:**
- Running hours without completion
- System becoming unresponsive

**Solutions:**

**A. Reduce data range**
```
❌ 10 years: Very slow
✓ 2-3 years: Optimal balance
✓ 1 year minimum: Quick test

Start with 1 year, expand if needed
```

**B. Higher timeframe**
```
✓ M15: Many trades, slower
✓ H1: Balanced
✓ H4/Daily: Fast, fewer trades

Test on H4 first, then lower timeframes
```

**C. Simplify strategy**
```
Complex strategy = Slow backtest
Start simple, add complexity gradually
```

---

### Issue 3: "Results don't match forward testing"

**Symptoms:**
- Backtest: +$5,000
- Forward test: -$500
- Live trading: Losses

**Common Causes:**

**A. Overfitting (Most common)**
```
Backtest optimized for past data
Future market behaves differently

Solution:
- Use out-of-sample testing
- Walk-forward analysis
- Avoid over-optimization
```

**B. Execution differences**
```
Backtest: Perfect fills
Reality: Slippage, partial fills, requotes

Solution:
- Add slippage (2-3 pips)
- Model realistic fills
- Account for rejected orders
```

**C. Market regime change**
```
Backtest period: Trending market
Current market: Range-bound

Solution:
- Test across different conditions
- Use longer backtest period
- Add market filters
```

---

### Issue 4: "Insufficient data for backtest"

**Symptoms:**
- "Not enough candles" error
- Only few trades generated

**Solutions:**

**A. Data availability**
```
Check: mcp__metatrader__get_candles_latest(symbol, timeframe, count)

MetaTrader limits:
- M1: ~2 months
- M15: ~6 months
- H1: ~2 years
- H4/D1: ~10 years
```

**B. Workaround**
```
If limited data:
1. Use higher timeframe
2. Export historical data from other source
3. Focus on recent period (more relevant anyway)
```

---

### Issue 5: "Walk-forward analysis showing degradation"

**Symptoms:**
- In-sample: +$2,000
- Out-sample: +$200
- Degradation: 90%

**Analysis:**

**A. Acceptable degradation**
```
✓ 10-30%: Normal, expected
⚠️ 30-50%: Strategy may be overfit
❌ >50%: Likely overfitted, unreliable
```

**B. Consistent failure**
```
If multiple windows fail:
- Strategy not robust
- Market conditions changed
- Reconsider approach
```

**C. Solutions**
- Simplify strategy (fewer parameters)
- Test longer in-sample periods
- Use more conservative parameters
- Accept lower in-sample performance for better robustness

---

### Issue 6: "Cannot optimize parameters"

**Symptoms:**
- Optimization not finding better values
- All variations perform similarly

**Possible Reasons:**

**A. Parameters not significant**
```
Testing: RSI 12 vs 14 vs 16
Result: Minimal difference

This is GOOD!
Means strategy robust to parameter changes
```

**B. Optimization range too narrow**
```
❌ Testing RSI 13-15 (too narrow)
✓ Testing RSI 10-20 (better range)
```

**C. Local optima**
```
May have found local maximum
Try different parameter ranges
Test completely different values
```

---

### Issue 7: "Backtest shows profit but high drawdown"

**Symptoms:**
- Net profit: +$3,000
- Max drawdown: -25%

**Assessment:**

**A. Is this acceptable?**
```
Calmar Ratio = Annual Return / Max Drawdown

Example: 30% return / 25% DD = 1.2
✓ >1.5: Good
⚠️ 1.0-1.5: Acceptable
❌ <1.0: Poor
```

**B. Solutions if unacceptable**
- Reduce position size
- Add filters (only trade best setups)
- Implement stop loss optimization
- Use risk management overlay

**C. Drawdown expectations**
```
Realistic drawdowns:
- Scalping: 5-10%
- Day trading: 10-15%
- Swing trading: 15-25%
- Position trading: 20-30%

Higher timeframe = Higher DD usually
```

---

### Issue 8: "Few trades in backtest"

**Symptoms:**
- Only 10-20 trades in 1 year
- Not statistically significant

**Causes:**

**A. Strategy too selective**
```
Filters too strict
Entry criteria too specific

Solutions:
- Relax some filters
- Test on multiple symbols
- Consider lower timeframe
```

**B. Low volatility period**
```
Some strategies need volatility
Test in different market conditions
```

**C. Is this bad?**
```
No! If:
- High win rate achieved
- Good profit factor
- Large R:R ratio

Quality > Quantity
```

**Minimum trades needed:**
- 30 trades: Minimum acceptable
- 50 trades: Good sample
- 100+ trades: Statistical confidence

---

### Issue 9: "Inconsistent results between runs"

**Symptoms:**
- Same backtest, different results each time

**Causes:**

**A. Using incomplete candle data**
```
Latest candle still forming
Solution: Only use closed candles
```

**B. Random elements in strategy**
```
If strategy uses randomness:
- Set random seed for consistency
- Or this is expected behavior
```

**C. Data updates**
```
MetaTrader data updated between runs
Minor tick data differences
Usually negligible if using OHLC
```

---

### Issue 10: "Backtest crashes or errors"

**Symptoms:**
- Python errors
- Data processing failures

**Solutions:**

**A. Data quality**
```
Check for:
- Missing candles (gaps)
- Null/NaN values
- Incorrect OHLC data (H<L, etc.)

Clean data before backtest
```

**B. Memory issues**
```
Too much data loaded:
- Use chunking
- Process in batches
- Reduce candle count
```

**C. Script errors**
```python
# Verify pandas/numpy installed:
pip install pandas numpy

# Check script syntax
# Verify data format correct
```

---

## Backtest Validation Checklist

- [ ] Included spreads/commissions
- [ ] Added realistic slippage (2-3 pips)
- [ ] Used closed candles only (no look-ahead)
- [ ] Tested minimum 1 year data
- [ ] Generated >30 trades
- [ ] Out-of-sample testing done
- [ ] Walk-forward analysis performed
- [ ] Results realistic (not too perfect)
- [ ] Max drawdown acceptable (<25%)
- [ ] Profit factor 1.5-2.5 range

## Red Flags

Questionable if:
- Win rate >75%
- Profit factor >3
- Max DD <3%
- Zero losing months
- Perfect straight-line equity

These suggest overfitting or unrealistic assumptions

## Getting Help

1. Start with simple strategy first
2. Verify data quality
3. Use realistic parameters (spreads, slippage)
4. Check [examples.md](./examples.md) for proper methodology
5. Compare results with industry benchmarks
