# Risk Management - Troubleshooting

## Common Issues

### Issue 1: "Position size seems too small/large"

**Symptoms:**
- Calculated position size feels incorrect
- Risk amount doesn't match expectation

**Solutions:**

**A. Verify inputs**
```
Required:
- Account balance (correct currency?)
- Risk percentage (1-2% is standard)
- Stop loss distance (in pips)
- Symbol information (pip value)
```

**B. Check pip value**
```
EURUSD: $10 per pip per standard lot
USDJPY: Variable based on exchange rate
XAUUSD: $1 per point per 0.01 lot

Verify broker's contract specifications
```

**C. Account currency mismatch**
```
If account in EUR but calculating for USD pairs:
- Need currency conversion
- Position sizes will differ from USD account
```

---

### Issue 2: "Cannot calculate position size"

**Symptoms:**
- Errors during calculation
- Missing required data

**Common Causes:**

**A. Missing stop loss**
```
❌ Error: No stop loss specified
✓ Solution: Always provide stop loss distance

Example: "Calculate position size for EURUSD, 30 pip stop"
```

**B. Invalid risk percentage**
```
❌ Risk >5%: Too dangerous
❌ Risk <0.1%: Too conservative

✓ Standard range: 0.5% to 2%
```

**C. Symbol info unavailable**
```
Solution:
1. Check symbol name spelling
2. Verify symbol available in MetaTrader
3. Call: mcp__metatrader__get_symbol_price(symbol)
```

---

### Issue 3: "Risk calculations don't account for open positions"

**Symptoms:**
- New position calculated without considering existing risk
- Portfolio risk too high

**Solution:**

**A. Request portfolio assessment**
```
Correct: "I have 2 open trades, can I open another?"
Not just: "Calculate position size for GBPUSD"
```

**B. Check total portfolio risk**
```
Call: mcp__metatrader__get_all_positions()
Calculate total risk across all positions
Ensure total <5-10% of account
```

---

### Issue 4: "Stop loss recommendations unrealistic"

**Symptoms:**
- Stop too tight (hits immediately)
- Stop too wide (poor R:R)

**Understanding SL Types:**

**A. Technical Stop (Best)**
```
✓ Based on chart structure
✓ Below support/above resistance
✓ Respects market movement
⚠️ May be wider than desired

Accept wider stops, reduce position size
```

**B. ATR Stop (Good)**
```
✓ Adapts to volatility
✓ Mathematical consistency
⚠️ May not align with key levels

Use for volatile markets
```

**C. Fixed Pip Stop (Risky)**
```
⚠️ Ignores market structure
⚠️ Same stop every trade
✗ High chance of premature stop-out

Avoid except for scalping
```

---

### Issue 5: "Risk of Ruin seems wrong"

**Symptoms:**
- Low win rate but low RoR
- High win rate but high RoR

**Explanation:**

Risk of Ruin depends on:
- Win rate
- Risk % per trade
- Risk-Reward ratio
- Account size

**A. Verify assumptions**
```
Input your actual stats:
- Real win rate (not estimated)
- Actual R:R ratio achieved
- True risk % per trade
```

**B. Typical RoR values**
```
1% risk, 50% win rate, 1:2 R:R = ~5% RoR (Low ✓)
2% risk, 45% win rate, 1:1.5 R:R = ~15% RoR (Moderate ⚠️)
3% risk, 40% win rate, 1:1 R:R = ~45% RoR (High ❌)
```

**C. If RoR >10%**
- Reduce risk per trade
- Improve win rate
- Increase R:R ratio
- Reassess strategy

---

### Issue 6: "Recommended position violates margin"

**Symptoms:**
- "Insufficient margin" error
- Can't open calculated position size

**Causes:**

**A. Account leverage**
```
Check your leverage:
- 1:100 typical for retail
- 1:500 some brokers
- 1:30 EU regulated

Higher leverage = lower margin required
```

**B. Existing positions**
```
Open positions consume margin
Check free margin:
Call: mcp__metatrader__get_account_info()
```

**C. Solution**
- Close some positions
- Reduce position size
- Increase account balance

---

### Issue 7: "Correlation warnings but want to trade both"

**Symptoms:**
- Want to trade EURUSD and GBPUSD
- System warns of high correlation

**Understanding:**

**A. Why correlation matters**
```
EURUSD and GBPUSD correlation 0.78 means:
- 78% of movement is shared
- Trading both ≈ 1.78x exposure to USD
- NOT true diversification
```

**B. Options**
```
Option 1: Trade only one (Best)
- Choose higher probability setup
- Use full risk allocation

Option 2: Split risk (Acceptable)
- 1% on EURUSD
- 1% on GBPUSD
- But know effective risk ≈1.78%

Option 3: Ignore warning (Risky)
- Concentrated exposure
- Higher risk than appears
- Can amplify losses
```

---

### Issue 8: "Take profit vs trailing stop decision"

**Symptoms:**
- Unsure when to use fixed TP vs trailing
- Missing big moves or giving back profit

**Guidelines:**

**A. Fixed Take Profit**
```
Use when:
✓ Clear resistance level exists
✓ Target based on measured move
✓ Time-sensitive trade
✓ You won't monitor trade
```

**B. Trailing Stop**
```
Use when:
✓ Strong trending market
✓ No obvious resistance near
✓ Can monitor trade actively
✓ Want to maximize runners
```

**C. Hybrid Approach (Best)**
```
1. Close 50% at first target
2. Trail stop on remaining 50%
3. Guarantees some profit
4. Catches extended moves
```

---

### Issue 9: "Drawdown advice contradictory"

**Symptoms:**
- Told to reduce risk but also to recover losses
- Conflicting recommendations

**Clear Guidance:**

**During Drawdown:**
```
Drawdown 0-5%: Normal, maintain risk
Drawdown 5-10%: Slight caution, consider 1.5%→1%
Drawdown 10-15%: Reduce risk to 0.5-1%
Drawdown 15-20%: STOP, review strategy
Drawdown >20%: PAUSE trading, major review
```

**Never:**
```
❌ Increase risk to recover faster
❌ "Double down" on losses
❌ Revenge trade
❌ Abandon risk management

✗ This leads to blown accounts
```

**Always:**
```
✓ Reduce position sizes in drawdown
✓ Focus on high-probability setups only
✓ Take break if needed
✓ Recovery is slow and steady
```

---

### Issue 10: "Risk management makes returns too slow"

**Symptoms:**
- 1-2% risk feels too conservative
- Want faster account growth

**Reality Check:**

**A. Mathematics of compounding**
```
$10,000 account, 1% risk, 60% win rate, 1:2 R:R:
- Average expectancy: +$12 per trade
- 100 trades: +$1,200 (12% return)
- 200 trades: +$2,645 (26.4% return with compounding)

This is EXCELLENT annual return!
```

**B. Higher risk consequences**
```
3% risk instead of 1%:
- 3x faster gains in wins
- 3x faster losses in losses
- 3x higher Risk of Ruin
- 33 consecutive losses to ruin (vs 100)
```

**C. Professional traders**
```
Hedge funds: 0.5-1% risk per trade
Prop firms: 1-2% risk maximum
Retail (suggested): 1-2% risk

If 1% too slow, issue is:
- Strategy win rate too low
- R:R ratio too small
- Not enough trades

Fix strategy, not risk management!
```

---

## Risk Management Checklist

Before every trade:
- [ ] Position size calculated
- [ ] Risk ≤2% of account
- [ ] Total portfolio risk ≤10%
- [ ] Stop loss placed
- [ ] Margin available
- [ ] Correlation checked
- [ ] R:R ratio >1.5:1

## Getting Help

1. Verify account information accurate
2. Check [examples.md](./examples.md) for calculation methods
3. Use position sizing calculator consistently
4. Keep trade journal to track actual risk vs planned
5. Review [SKILLS_MCP_SETUP.md](../../../SKILLS_MCP_SETUP.md) for MCP connection issues
