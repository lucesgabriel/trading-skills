# Pattern Scanner - Usage Examples

## Example 1: Basic Single Symbol Scan

**User Input:**
```
scan EURUSD for candlestick patterns
```

**Expected Output:**
- Detailed chat analysis showing all detected patterns across M15, H1, H4, D1 timeframes
- Technical indicators summary
- Trading signal with probability
- Complete trade setup with entry, stop loss, take profits
- Confluence factors breakdown
- HTML report generated and opened automatically

**Use Case:** Quick comprehensive analysis of a single currency pair

---

## Example 2: Multi-Symbol Comparison

**User Input:**
```
scan EURUSD, GBPUSD, and XAUUSD for patterns
```

**Expected Output:**
- Parallel scanning of all 3 symbols
- Comparative summary table
- Ranking by probability (best opportunity first)
- 3 separate HTML reports
- Recommendation on which symbol to trade

**Use Case:** Finding the best trading opportunity among multiple options

---

## Example 3: Custom Timeframes

**User Input:**
```
scan EURUSD on H4 and Daily only
```

**Expected Output:**
- Focused analysis on H4 and D1 timeframes only
- Higher timeframe perspective (swing/position trading)
- Simplified report with less noise
- HTML report with only H4 and D1 sections

**Use Case:** Longer-term trading focus, avoiding intraday noise

---

## Example 4: Pattern Type Filter

**User Input:**
```
find reversal patterns in GBPUSD
```

**Expected Output:**
- Only reversal patterns shown (Engulfing, Stars, Hammers, etc.)
- Continuation patterns filtered out
- Focus on potential turning points
- HTML report highlighting reversal signals

**Use Case:** Looking specifically for trend reversal opportunities

---

## Example 5: Quick Multi-Pair Check

**User Input:**
```
quick pattern scan on major pairs
```

**Expected Output:**
- Scans EURUSD, GBPUSD, USDJPY, USDCHF, AUDUSD, NZDUSD
- Quick summary table with key metrics
- Detailed HTML for top 2 opportunities only
- Time-efficient overview

**Use Case:** Morning market scan to identify daily trading opportunities

---

## Example Output Format

```
🔍 EURUSD PATTERN SCAN COMPLETE

📊 SUMMARY:
- Patterns: 5 Bullish, 0 Bearish, 1 Neutral
- Probability: 72% (High Confidence)
- Signal: LONG (BUY)

🕯️ KEY PATTERNS DETECTED:

M15 Timeframe:
✓ Bullish Engulfing (Very Strong) at 1.16433
✓ Three White Soldiers (Strong)

H1 Timeframe:
✓ Bullish Harami (Medium) at 1.16433
✓ Hammer (Strong) at support 1.16187

H4 Timeframe:
✓ Morning Star (Very Strong) completed

📈 TECHNICAL INDICATORS:
- RSI: 52 (Neutral, room to rise)
- MACD: Bullish crossover confirmed
- Trend: Multi-TF bullish alignment

🎯 SUPPORT & RESISTANCE:
Resistance: 1.16689 (+258 pips)
---CURRENT: 1.16431---
Support: 1.16187 (-244 pips)

💡 RECOMMENDED TRADE SETUP:
Direction: LONG (BUY)
Entry: 1.16430-1.16450
Stop Loss: 1.16250 (-180 pips)
Take Profit 1: 1.16600 (+170 pips)
Take Profit 2: 1.16900 (+470 pips)

✅ CONFLUENCE FACTORS (+72%):
+ Bullish Engulfing M15: +15%
+ Multi-TF bullish patterns: +15%
+ MACD bullish: +10%
+ Pattern at support: +10%
+ Trend confirmation: +15%

📄 Full HTML Report:
D:\reports\EURUSD_scan_20251029_150830.html

🚀 Opening in browser...
```

---

## Tips for Best Results

1. **Use Multiple Timeframes**: Default M15, H1, H4, D1 gives best context
2. **Check During Active Sessions**: European/US overlap for best signals
3. **Combine with News**: Avoid trading during major announcements
4. **Validate with Volume**: Higher conviction when volume confirms
5. **Multi-Symbol Comparison**: Always check alternatives before trading

---

## Integration Examples

### With Risk Management
```
scan EURUSD
[After getting signal]
calculate position size for EURUSD with 1% risk
```

### With Backtesting
```
scan EURUSD
[After detecting Bullish Engulfing]
validate Bullish Engulfing pattern on EURUSD H1
```

### With Opportunity Scanner
```
scan EURUSD
[If probability > 70%]
rank opportunities across major pairs
```

---

See SKILL.md for complete workflow documentation.
