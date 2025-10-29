# Pattern Scanner - Troubleshooting Guide

## Common Issues and Solutions

### Issue 1: No Patterns Detected

**Symptom:**
```
EURUSD PATTERN SCAN COMPLETE
Patterns: 0 Bullish, 0 Bearish, 0 Neutral
```

**Possible Causes:**
1. Market is in tight consolidation (no clear patterns forming)
2. Insufficient candle data fetched from MetaTrader
3. Pattern thresholds too strict for current market conditions

**Solutions:**
- **Check Market Conditions**: Patterns form best after strong moves or at key levels
- **Verify Data**: Ensure at least 100 candles per timeframe
  ```
  Check candle count in scan results
  If < 50 candles, increase fetch count in MetaTrader
  ```
- **Try Different Timeframes**: Some timeframes may show patterns others don't
- **Wait for Active Session**: Patterns more frequent during London/NY sessions
- **Expected Behavior**: It's normal to have no patterns during low volatility periods

---

### Issue 2: HTML Report Won't Open

**Symptom:**
```
HTML report generated: D:\...\EURUSD_pattern_scan_20251029_150830.html
Error opening browser
```

**Possible Causes:**
1. Default browser not configured
2. File path contains special characters
3. Permission issues in output directory

**Solutions:**
- **Manual Open**: Navigate to the file path shown and double-click
- **Check Permissions**: Ensure write access to reports/ directory
- **Verify Path**: Check for spaces or special characters in directory name
- **Alternative Method**:
  ```python
  import webbrowser
  webbrowser.open('file:///' + filepath.replace('\\', '/'))
  ```
- **Windows Specific**: Try using `start ""` command:
  ```
  start "" "D:\path\to\report.html"
  ```

---

### Issue 3: Low Probability Scores (Always < 55%)

**Symptom:**
```
Probability: 48% (Low Confidence)
Signal: NEUTRAL (WAIT)
```

**Possible Causes:**
1. Conflicting patterns across timeframes
2. No technical indicator confirmation
3. Patterns forming mid-range (not at support/resistance)
4. Counter-trend patterns

**Solutions:**
- **Multi-Timeframe Alignment**: Best signals when patterns align across M15, H1, H4
- **Wait for Confluence**: Look for patterns at key support/resistance levels
- **Check Indicator Alignment**: MACD, RSI should confirm pattern direction
- **Avoid Counter-Trend**: Don't trade bullish patterns in strong downtrends
- **Expected Behavior**: Low probability = valid signal to WAIT, not an error

**Probability Breakdown:**
- 30-54% = Neutral (WAIT for better setup)
- 55-69% = Medium Confidence (consider with tight stops)
- 70-79% = High Confidence (good trade setup)
- 80-85% = Very High Confidence (excellent opportunity)

---

### Issue 4: MetaTrader Connection Errors

**Symptom:**
```
Error: Could not fetch candles for EURUSD
MCP connection failed
```

**Possible Causes:**
1. MetaTrader 5 not running
2. MCP server not configured
3. Symbol not available in broker
4. Network/connection issues

**Solutions:**
- **Start MT5**: Ensure MetaTrader 5 terminal is open and logged in
- **Check MCP Config**: Verify `.mcp.json` settings in project root
  ```json
  {
    "mcpServers": {
      "metatrader": {
        "command": "python",
        "args": ["-m", "mcp_server_metatrader"]
      }
    }
  }
  ```
- **Verify Symbol**: Check symbol exists in Market Watch (MT5)
- **Test Connection**: Try `mcp__metatrader__get_account_info` first
- **Restart Services**: Close and reopen both Claude Code and MT5

---

### Issue 5: Pattern Detection Inconsistencies

**Symptom:**
```
Same timeframe shows different patterns on successive scans
```

**Possible Causes:**
1. New candles forming (expected behavior)
2. Market volatility causing rapid pattern changes
3. Pattern invalidation from price movement

**Solutions:**
- **Expected Behavior**: Patterns change as new candles form
- **Pattern Invalidation**: Patterns become invalid if:
  - Bullish pattern: Price breaks below pattern low
  - Bearish pattern: Price breaks above pattern high
- **Use Latest Scan**: Always use most recent scan for decisions
- **Set Alerts**: Use pattern formation as alert, not guaranteed signal
- **Confirm Before Entry**: Verify pattern still valid before placing trade

---

### Issue 6: Indicator Calculation Warnings

**Symptom:**
```
Warning: Could not calculate indicators for H4: insufficient data
RSI: nan, MACD: nan
```

**Possible Causes:**
1. Less than 200 candles available
2. Data quality issues (missing candles)
3. Indicator calculation errors

**Solutions:**
- **Increase Candle Count**: Fetch minimum 250 candles per timeframe
  ```python
  # In candlestick_scanner.py
  # Default count is 100, increase to 250 for indicators
  ```
- **Check Data Quality**: Ensure no gaps in candle data
- **Fallback Behavior**: Skill continues with pattern-only analysis
- **Technical Analysis Skill**: Ensure technical-analysis skill is available
- **Expected Behavior**: Patterns still detected, but without indicator confluence

---

### Issue 7: Multi-Symbol Scan Takes Too Long

**Symptom:**
```
Scanning 10 symbols taking > 2 minutes
```

**Possible Causes:**
1. Too many symbols requested
2. Fetching too many candles per symbol
3. MetaTrader API rate limiting

**Solutions:**
- **Reduce Symbols**: Scan 3-5 most important pairs first
- **Optimize Candle Count**: Use 100 candles for speed, 250 for accuracy
- **Sequential vs Parallel**: Current implementation is sequential
- **Use Opportunity Scanner**: For quick multi-pair overview, use opportunity-scanner skill instead
- **Expected Performance**:
  - 1 symbol: 10-15 seconds
  - 3 symbols: 30-45 seconds
  - 6+ symbols: 60-120 seconds

---

### Issue 8: HTML Report Shows "NaN" or Missing Values

**Symptom:**
```
Current Price: NaN
Probability: NaN%
```

**Possible Causes:**
1. Price data not provided correctly
2. Calculation errors in confluence
3. Missing technical snapshots

**Solutions:**
- **Check Input Data**: Verify `current_price` parameter is valid float
- **Verify Candle Data**: Ensure CSV data is properly formatted
- **Debug Confluence**: Check confluence_calculator.py output
- **Fallback Values**: Skill should use defaults (50% base probability)
- **Report Issue**: If persistent, check candlestick_scanner.py data flow

---

### Issue 9: Pattern Names Not Displaying Correctly

**Symptom:**
```
Pattern detected but no name shown in report
```

**Possible Causes:**
1. Pattern dictionary missing 'name' key
2. HTML template rendering issue
3. Pattern detection returning None

**Solutions:**
- **Check Pattern Structure**: All patterns should return:
  ```python
  {
      'name': 'Bullish Engulfing',
      'type': 'Strong Bullish Reversal',
      'strength': 'Very Strong',
      'reliability': 75,
      'bias': 'Bullish',
      'price': 1.16430,
      'time': '2025-10-29 15:00:00'
  }
  ```
- **Verify HTML Generator**: Check `generate_pattern_cards_html()` function
- **Debug Output**: Print pattern dictionary before HTML generation

---

## Performance Optimization Tips

### Speed Up Scans

1. **Reduce Timeframes**: Use H1 and H4 only for faster scans
   ```
   scan EURUSD on H1 and H4 only
   ```

2. **Optimize Candle Count**: Balance between speed and accuracy
   - Fast scan: 50 candles
   - Balanced: 100 candles
   - Accurate: 250 candles

3. **Cache Results**: Results valid for duration of current candle
   - M15: Valid for up to 15 minutes
   - H1: Valid for up to 1 hour
   - H4: Valid for up to 4 hours

### Improve Detection Accuracy

1. **Use Multiple Timeframes**: Default M15, H1, H4, D1 gives best results
2. **Check Higher Timeframes First**: D1 and H4 patterns more reliable
3. **Combine with Volume**: Higher volume = stronger confirmation
4. **Wait for Candle Close**: Patterns most reliable after candle closes
5. **Verify at Key Levels**: Patterns at support/resistance = higher probability

---

## Integration Troubleshooting

### Risk Management Integration

**Issue**: Position size calculation fails after pattern scan

**Solution**:
```
scan EURUSD
[Wait for scan completion]
calculate position size for EURUSD with 1% risk
[Use stop loss from pattern scan]
```

### Backtesting Integration

**Issue**: Want to validate detected pattern historically

**Solution**:
```
scan EURUSD
[If Bullish Engulfing detected on H1]
validate Bullish Engulfing pattern on EURUSD H1 timeframe
```

### Opportunity Scanner Integration

**Issue**: Need broader market context

**Solution**:
```
scan market opportunities
[Shows top 3 pairs with highest probability]
scan EURUSD
[Detailed pattern analysis for comparison]
```

---

## Debug Mode

### Enable Detailed Logging

To debug pattern detection issues, add print statements:

```python
# In candlestick_scanner.py
def detect_all_patterns(df, current_price, support_levels, resistance_levels):
    print(f"DEBUG: DataFrame shape: {df.shape}")
    print(f"DEBUG: Last candle: {df.iloc[-1]}")

    patterns = []
    for detector in PATTERN_DETECTORS:
        result = detector(df, len(df) - 1, support_levels, resistance_levels)
        if result:
            print(f"DEBUG: Pattern detected: {result['name']}")
            patterns.append(result)

    return patterns
```

### Validate Data Quality

```python
# Check candle data integrity
def validate_candles(df):
    print(f"Total candles: {len(df)}")
    print(f"Date range: {df['time'].min()} to {df['time'].max()}")
    print(f"Missing values: {df.isnull().sum().sum()}")
    print(f"Price range: {df['low'].min()} to {df['high'].max()}")
```

---

## When to Contact Support

If you experience:
- Consistent crashes when scanning
- Patterns detected that don't match candles
- HTML reports with corrupted layout
- Integration errors with other skills

**Steps Before Reporting:**
1. Check this troubleshooting guide
2. Verify MetaTrader 5 connection
3. Test with single symbol on single timeframe
4. Note exact error messages
5. Check Claude Code version and logs

---

## Best Practices to Avoid Issues

1. **Always verify MT5 is running** before scanning
2. **Use standard symbols** (EURUSD, GBPUSD, etc.) for testing
3. **Scan during active market hours** for best results
4. **Start with single symbol** before multi-symbol scans
5. **Check HTML output directory** has write permissions
6. **Keep skill files updated** from repository
7. **Combine with other skills** for comprehensive analysis
8. **Don't over-rely on automation** - verify signals manually

---

For usage examples, see examples.md
For pattern details, see pattern_reference.md
