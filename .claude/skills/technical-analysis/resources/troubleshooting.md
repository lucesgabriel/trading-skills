# Technical Analysis - Troubleshooting

## Common Issues and Solutions

### Issue 1: "Cannot fetch candle data for symbol"

**Symptoms:**
- Error when requesting analysis
- Message: "Symbol not found" or "No data available"

**Causes & Solutions:**

**A. Symbol name incorrect**
```
❌ Wrong: EUR/USD, EUR USD, eurusd
✓ Correct: EURUSD (no spaces, no slashes, uppercase)
```

**B. Symbol not available in broker**
- Check available symbols: Call `mcp__metatrader__get_all_symbols`
- Use correct broker symbol name (e.g., some brokers use "EURUSD.a" or "EURUSDm")

**C. MetaTrader not connected**
- Verify MT5 is running
- Check MCP server status
- Restart MetaTrader if needed

---

### Issue 2: "Indicators showing conflicting signals"

**Symptoms:**
- RSI says buy, MACD says sell
- Different timeframes show opposite trends

**Solution:**
This is NORMAL and expected. Use these guidelines:

**A. Timeframe Priority**
```
Daily trend > H4 trend > H1 trend
Always trade in direction of higher timeframe
```

**B. Indicator Confluence**
- Need 3+ indicators agreeing for high-probability setup
- 2 indicators = moderate setup
- 1 indicator alone = wait for confirmation

**C. When Conflicted**
- DO NOT trade if major conflict
- Wait for clarity
- Better to miss trade than force low-probability setup

---

### Issue 3: "Analysis takes too long"

**Symptoms:**
- Waiting >30 seconds for analysis
- Timeout errors

**Causes & Solutions:**

**A. Requesting too many candles**
```
❌ Avoid: Requesting 1000+ candles
✓ Better: Use 100-200 candles per timeframe
```

**B. Too many timeframes**
```
✓ Standard: Analyze 3 timeframes (M15, H1, H4)
❌ Excessive: Analyzing 5+ timeframes
```

**C. Multiple symbols simultaneously**
- Analyze symbols one at a time
- Use opportunity-scanner for multi-symbol analysis

---

### Issue 4: "Python script errors"

**Symptoms:**
- "Module not found" errors
- Calculation failures

**Solutions:**

**A. Missing dependencies**
```bash
pip install pandas numpy
```

**B. Script path issues**
```python
# Ensure scripts are in correct location:
.claude/skills/technical-analysis/scripts/indicator_suite.py
```

**C. Data format issues**
- Verify candle data is in CSV format
- Check for missing/null values
- Ensure OHLC columns exist

---

### Issue 5: "Incorrect probability calculations"

**Symptoms:**
- Probability seems too high or too low
- All setups showing 50%

**Causes:**

**A. Missing context**
- Need multiple timeframe analysis
- Require support/resistance levels
- Check indicator confluence

**B. Probability Calibration**
Expected ranges:
```
75%+  = Excellent (rare, perfect alignment)
65-74% = Good (most high-probability setups)
55-64% = Moderate (acceptable with good R:R)
45-54% = Low (avoid or reduce size)
<45%   = Very low (do not trade)
```

**C. Verification**
- Check if all indicators calculated
- Verify trend alignment across timeframes
- Ensure support/resistance identified

---

### Issue 6: "Missing support/resistance levels"

**Symptoms:**
- Analysis doesn't show key levels
- No entry/exit recommendations

**Solution:**

**A. Manual identification**
- Look at recent swing highs/lows
- Identify previous consolidation zones
- Note psychological levels (round numbers)

**B. Increase candle history**
```
Need minimum 100 candles to identify levels
Optimal: 200-300 candles for better context
```

**C. Check multiple timeframes**
- H4/Daily levels are most significant
- H1 levels for fine-tuning entries
- M15 levels for scalping only

---

### Issue 7: "Divergence not detected"

**Symptoms:**
- Visual divergence present but not reported
- Skill doesn't mention divergence

**Explanation:**
Divergence detection requires:
- Minimum 3 swing points
- Clear trend in price
- Opposite trend in indicator (RSI/MACD)

**Manual Check:**
```
1. Identify 2 recent swing highs or lows
2. Compare RSI values at those points
3. If price lower low but RSI higher low = Bullish divergence
4. If price higher high but RSI lower high = Bearish divergence
```

---

### Issue 8: "Analysis different from other platforms"

**Symptoms:**
- Indicators show different values than TradingView
- Signals don't match other analysis

**Causes:**

**A. Different calculation periods**
```
Verify indicator settings match:
- RSI: 14 periods (standard)
- MACD: 12,26,9 (standard)
- MA: Same type (SMA vs EMA)
```

**B. Different data feeds**
- Each broker has slightly different prices
- Time zone differences
- This is NORMAL, focus on trend not exact values

**C. Timeframe alignment**
- Ensure comparing same timeframe
- H1 bar close times may differ between platforms

---

### Issue 9: "Too many false signals"

**Symptoms:**
- Setup looked good but failed quickly
- Consistent losses despite following analysis

**Solutions:**

**A. Add filters**
```
1. Only trade in direction of Daily trend
2. Require 3+ indicator confluence
3. Wait for confirmation candle close
4. Check for news events before entry
```

**B. Tighten criteria**
```
Only take setups with:
- Probability >65%
- R:R ratio >2:1
- Clear support/resistance
- Multiple timeframe alignment
```

**C. Improve timing**
```
- Wait for pullback in trend
- Enter on retest of breakout
- Use limit orders at key levels
- Avoid chasing price
```

---

### Issue 10: "Cannot execute technical-analysis script"

**Symptoms:**
- Permission denied errors
- Script not found

**Solutions:**

**A. Check `.claude/settings.local.json`**
```json
{
  "allowedTools": {
    "Bash": {"patterns": ["python .claude/skills/technical-analysis/scripts/*"]},
    "Read": {"patterns": [".claude/skills/**"]}
  }
}
```

**B. Verify file permissions**
```bash
# Windows
icacls ".claude\skills\technical-analysis\scripts\indicator_suite.py"

# Linux/Mac
chmod +x .claude/skills/technical-analysis/scripts/indicator_suite.py
```

**C. Python environment**
- Verify Python installed: `python --version`
- Check pip packages: `pip list | grep pandas`

---

## Quick Diagnostic Checklist

Before requesting support, verify:

- [ ] MetaTrader 5 is running
- [ ] Symbol name is correct format
- [ ] MCP server is connected
- [ ] Python dependencies installed
- [ ] Requesting reasonable amount of data
- [ ] Using standard indicator periods
- [ ] At least 100 candles available

## Getting Help

If issues persist:

1. Check [SKILLS_MCP_SETUP.md](../../../SKILLS_MCP_SETUP.md) for configuration
2. Review [examples.md](./examples.md) for correct usage
3. Verify MetaTrader connection with:
   ```
   User: "Get EURUSD current price"
   ```
4. Test basic functionality before complex analysis
