# Risk Management - Usage Examples

## Example 1: Basic Position Sizing

### Input
```
User: "I have $10,000. How much should I risk on EURUSD?"
or
User: "Calculate position size for EURUSD, I want to risk 2%"
```

### Expected Claude Actions
1. Ask for stop loss distance if not provided
2. Get symbol information (pip value, lot specs)
3. Calculate position size using risk-based formula
4. Provide multiple risk scenarios (1%, 1.5%, 2%)

### Output Example
```
POSITION SIZING CALCULATION - EURUSD

Account Information:
├─ Balance: $10,000
├─ Currency: USD
└─ Leverage: Assumed 1:100 (verify with broker)

Trade Setup:
├─ Symbol: EURUSD
├─ Current Price: 1.0825
├─ Entry: 1.0820
├─ Stop Loss: 1.0790
└─ Stop Distance: 30 pips

POSITION SIZE RECOMMENDATIONS:

Conservative (1% risk = $100):
├─ Position Size: 0.33 lots (33,000 units)
├─ Risk Amount: $100
├─ Margin Required: ~$350
└─ Potential Loss at SL: $100

Moderate (1.5% risk = $150):
├─ Position Size: 0.50 lots (50,000 units)
├─ Risk Amount: $150
├─ Margin Required: ~$540
└─ Potential Loss at SL: $150

Aggressive (2% risk = $200):
├─ Position Size: 0.67 lots (67,000 units)
├─ Risk Amount: $200
├─ Margin Required: ~$720
└─ Potential Loss at SL: $200

⚠️ RECOMMENDATION: Use 1-1.5% risk maximum
This allows 67-100 consecutive losses before ruin

RISK-REWARD ANALYSIS:
If Target: 1.0920 (100 pips)
├─ Risk: 30 pips ($100 @ 0.33 lots)
├─ Reward: 100 pips ($333 @ 0.33 lots)
└─ R:R Ratio: 1:3.33 ✓ EXCELLENT
```

## Example 2: Multiple Position Risk Management

### Input
```
User: "I already have 2 open trades. Can I open another position on GBPUSD?"
```

### Expected Claude Actions
1. Get current open positions
2. Calculate total portfolio risk
3. Assess if new trade violates 5-10% portfolio rule
4. Provide recommendation

### Output Example
```
PORTFOLIO RISK ASSESSMENT

Current Open Positions:
1. EURUSD BUY 0.50 lots
   ├─ Entry: 1.0820 | Stop: 1.0790
   ├─ Risk: 30 pips = $150 (1.5%)

2. XAUUSD BUY 0.10 lots
   ├─ Entry: $2,015 | Stop: $2,005
   ├─ Risk: $10 = $100 (1.0%)

Current Portfolio Exposure:
├─ Total Risk: $250
├─ Portfolio Risk %: 2.5%
├─ Account Balance: $10,000
└─ Status: HEALTHY ✓

Proposed New Trade: GBPUSD
├─ Suggested Risk: 1.5% ($150)
├─ NEW Total Risk: $400 (4.0%)
└─ Status: ACCEPTABLE ✓

RECOMMENDATION: ✓ SAFE TO PROCEED

You can open the GBPUSD position with:
├─ Maximum Position Size: 0.45 lots
├─ Risk: $150 (1.5%)
├─ Total Portfolio Risk: 4.0%
└─ Remaining Capacity: 1-2 more positions possible

⚠️ WARNINGS:
- Stay below 5% total portfolio risk
- Consider correlation (GBP/EUR often move together)
- Monitor margin usage
```

## Example 3: Stop Loss Optimization

### Input
```
User: "Where should I place my stop loss for GBPUSD buy at 1.2650?"
```

### Output Example
```
STOP LOSS PLACEMENT ANALYSIS - GBPUSD

Entry Price: 1.2650
Current Market: Uptrend on H4

STOP LOSS OPTIONS:

1. Technical Stop (RECOMMENDED) ⭐⭐⭐⭐⭐
   ├─ Price: 1.2610
   ├─ Distance: 40 pips
   ├─ Logic: Below recent swing low at 1.2615
   ├─ Probability of hit: 25% (Good)
   └─ For $100 risk: Use 0.25 lots

2. ATR-Based Stop ⭐⭐⭐⭐
   ├─ ATR(14): 35 pips
   ├─ 1.5× ATR: 53 pips
   ├─ Price: 1.2597
   ├─ Logic: Gives room for volatility
   └─ For $100 risk: Use 0.19 lots

3. Percentage Stop ⭐⭐⭐
   ├─ 1% of price: 12.6 pips
   ├─ Price: 1.2637
   ├─ Logic: Simple calculation
   ⚠️ WARNING: Too tight, high probability of being hit
   └─ Not recommended for this pair

4. Support Level Stop ⭐⭐⭐⭐
   ├─ Price: 1.2620
   ├─ Distance: 30 pips
   ├─ Logic: Below H4 support zone
   ├─ Probability of hit: 30%
   └─ For $100 risk: Use 0.33 lots

RECOMMENDED APPROACH:
Use Technical Stop at 1.2610 (40 pips)

REASONING:
✓ Respects market structure
✓ Below significant swing low
✓ Not too tight (reduces whipsaw risk)
✓ Not too wide (keeps R:R favorable)
✓ Aligns with H4 timeframe

With Target at 1.2750 (100 pips):
├─ Risk: 40 pips
├─ Reward: 100 pips
└─ R:R: 1:2.5 ✓ EXCELLENT
```

## Example 4: Take Profit Strategy

### Input
```
User: "I'm in EURUSD buy at 1.0820, it's now at 1.0860. Should I take profit or let it run?"
```

### Output Example
```
TAKE PROFIT DECISION ANALYSIS - EURUSD

Trade Details:
├─ Entry: 1.0820
├─ Current: 1.0860
├─ Profit: 40 pips
├─ Original Target: 1.0920 (100 pips)
└─ Progress: 40% to target

Market Analysis:
├─ H4 Trend: Still bullish ↗
├─ H1 Trend: Bullish ↗
├─ RSI: 62 (Not overbought)
├─ Key Resistance: 1.0880, 1.0920
└─ No major reversal signals

RECOMMENDATION: PARTIAL PROFIT + TRAILING

Suggested Action Plan:

STEP 1: Take 50% Profit Now
├─ Close: 0.5 of position at 1.0860
├─ Lock in: $200 profit (assuming 1.0 lot)
├─ Remaining: 0.5 lots to target
└─ Psychology: Guaranteed win

STEP 2: Move Stop to Breakeven
├─ Move stop from 1.0790 → 1.0820
├─ Remaining position: Risk-free
└─ Can't lose now ✓

STEP 3: Set Trailing Stop for Remaining
├─ Trail: 25 pips below price
├─ Current trailing stop: 1.0835
├─ Adjusts as price rises
└─ Locks in more profit automatically

STEP 4: Final Target
├─ Let remaining 0.5 lots run to 1.0920
├─ Potential additional profit: $300
└─ Total potential: $500

RISK-REWARD OUTCOME:
├─ Minimum Secured: $200 (Even if trade reverses)
├─ Maximum Possible: $500 (If reaches target)
├─ Original Risk: $300
└─ Minimum R:R Achieved: 1:0.67 (Acceptable)

Alternative (More Conservative):
Close 100% at 1.0880 (next resistance)
├─ Profit: 60 pips = $300
├─ R:R: 1:2 ✓
└─ Re-enter on pullback if opportunity
```

## Example 5: Account Drawdown Management

### Input
```
User: "I'm down 15% this month. Should I keep trading?"
```

### Output Example
```
DRAWDOWN ASSESSMENT & RECOVERY PLAN

Account Status:
├─ Starting Balance: $10,000
├─ Current Balance: $8,500
├─ Drawdown: -$1,500 (-15%)
└─ Status: ⚠️ ELEVATED RISK

IMMEDIATE ACTIONS REQUIRED:

1. REDUCE RISK PER TRADE ⚠️
   FROM: 2% per trade ($170 current balance)
   TO: 0.5-1% per trade ($42-85)

   Reasoning: Protect remaining capital

2. REDUCE POSITION SIZE
   ├─ Max positions: 2 (down from 3-4)
   ├─ Max portfolio risk: 2% total
   └─ Focus on highest probability setups (>70%)

3. REVIEW TRADING HISTORY
   ├─ Get last 20 trades: /risk-management review-history
   ├─ Identify: What went wrong?
   ├─ Common patterns: Over-trading? Wrong direction?
   └─ Fix: Adjust strategy accordingly

4. TAKE A BREAK (1-3 days)
   ├─ Step away from charts
   ├─ Clear emotional state
   ├─ Review trading plan
   └─ Return with fresh perspective

RECOVERY PLAN:

To return to $10,000 from $8,500:
├─ Required gain: +17.6%
├─ At 1% risk per trade: Need ~18-20 winning trades
├─ At 2:1 R:R: Need 60% win rate
├─ Conservative timeline: 2-3 months

⚠️ DO NOT:
❌ Increase position size to "recover faster"
❌ Revenge trade after losses
❌ Deviate from trading plan
❌ Trade outside your strategy

✓ DO:
✓ Stick to 0.5-1% risk per trade
✓ Only take A+ setups (>70% probability)
✓ Keep detailed trade journal
✓ Focus on process, not profit

RISK OF RUIN CALCULATION:
├─ Current: 15% drawdown
├─ With 1% risk: Low risk of ruin (~5%)
├─ With 2% risk: Moderate risk (~18%)
└─ RECOMMENDATION: Stay at 1% until recovered to $9,500
```

## Example 6: Correlation Risk Assessment

### Input
```
User: "I want to trade EURUSD, GBPUSD, and EURGBP at the same time"
```

### Output Example
```
CORRELATION RISK ASSESSMENT

Proposed Positions:
1. EURUSD - BUY
2. GBPUSD - BUY
3. EURGBP - ?

⚠️ HIGH CORRELATION ALERT

Correlation Matrix (60-day):
├─ EURUSD vs GBPUSD: +0.78 (Strong positive)
├─ EURUSD vs EURGBP: +0.42 (Moderate)
└─ GBPUSD vs EURGBP: -0.35 (Weak negative)

RISK ANALYSIS:

If EURUSD BUY + GBPUSD BUY:
├─ Effective Exposure: 1.78x (Not 2x)
├─ Diversification: Limited
├─ USD weakness: Both profit ✓
├─ USD strength: Both lose ✗
└─ Verdict: CORRELATED RISK

RECOMMENDATIONS:

Option 1: Trade only ONE (BEST)
├─ Choose EURUSD or GBPUSD
├─ Better setup: GBPUSD (75% prob vs 68%)
├─ Risk: 2% on single position
└─ True diversification: None needed

Option 2: Reduce position sizes (ACCEPTABLE)
├─ EURUSD: 0.5% risk (instead of 1.5%)
├─ GBPUSD: 0.5% risk (instead of 1.5%)
├─ Total risk: 1% (but correlated)
└─ Effective risk: Similar to single 1% trade

Option 3: Add EURGBP SELL (NOT RECOMMENDED)
├─ Creates offsetting positions
├─ EURUSD BUY + EURGBP SELL = Synthetic GBPUSD BUY
├─ Unnecessary complexity
├─ Higher spreads/costs
└─ Same result as just trading GBPUSD

⚠️ REMEMBER:
Trading correlated pairs doesn't diversify risk.
It concentrates exposure to USD movements.

For TRUE diversification, consider:
- EURUSD (USD exposure)
- AUDJPY (AUD/JPY exposure)
- XAUUSD (Gold/safe haven)
- Different asset classes
```

## Risk Management Checklist

Before Every Trade, Verify:

**Account Level:**
- [ ] Total portfolio risk <5-10%
- [ ] Account not in drawdown >10%
- [ ] Sufficient margin available
- [ ] No over-leveraging

**Position Level:**
- [ ] Risk per trade: 1-2% maximum
- [ ] Stop loss placed (no exceptions)
- [ ] Position size calculated correctly
- [ ] R:R ratio minimum 1:1.5 (prefer 1:2+)

**Correlation Level:**
- [ ] Check correlation with existing positions
- [ ] Avoid multiple highly correlated trades
- [ ] Consider currency exposure balance

**Psychological Level:**
- [ ] Trading plan followed
- [ ] No emotional decision-making
- [ ] No revenge trading
- [ ] Clear mind and focus
