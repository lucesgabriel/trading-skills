---
description: Calculate optimal position sizes and assess risk before placing trades
---

# Risk Management Calculator

Calculate optimal position sizes, manage risk exposure, and ensure sustainable trading.

## Usage

Quick calculation (will ask for details):
```
/risk EURUSD
```

With trade parameters:
```
/risk EURUSD entry:1.0850 stop:1.0820
```

Portfolio risk assessment:
```
/risk --portfolio
```

## What It Does

Use the risk-management skill to:

1. **Get Account Information** - Retrieve current account balance, equity, margin level
2. **Calculate Position Size** - Based on:
   - Account balance
   - Risk percentage (default: 1-2%)
   - Stop loss distance (in pips)
   - Symbol pip value
3. **Risk/Reward Analysis** - Evaluate trade viability
4. **Portfolio Assessment** - Monitor overall exposure and correlation risk
5. **Position Sizing Recommendations** - Conservative, standard, aggressive options

## Core Risk Principles

**1% Rule:**
- Maximum 1% of account balance per trade (conservative)
- Maximum 2% for standard risk tolerance
- Never exceed 5% total portfolio exposure

**Position Sizing Formula:**
```
Lot Size = (Account Balance × Risk %) / (Stop Loss Pips × Pip Value)
```

**Risk:Reward Targets:**
- Minimum: 1:1.5
- Target: 1:2 or 1:3
- Conservative: 1:3+

## Output Format

**Account Summary:**
- Balance and equity
- Available margin
- Current exposure (%)

**Position Size Calculation:**
- Recommended lot size (conservative/standard/aggressive)
- Risk amount in account currency
- Potential profit at TP levels
- Risk:Reward ratio

**Risk Assessment:**
- Overall portfolio risk (%)
- Correlation with open positions
- Margin requirements
- Risk warnings if excessive

## Example

```
/risk EURUSD entry:1.0850 stop:1.0820
```

Results in:
```
🛡️ Risk Management Calculator - EURUSD

📊 Account Summary:
  Balance: $10,000
  Equity: $10,200
  Free Margin: $8,500
  Current Exposure: 15%

📏 Trade Parameters:
  Entry: 1.0850
  Stop Loss: 1.0820
  Distance: 30 pips
  Take Profit: 1.0910 (60 pips)
  Risk:Reward: 1:2 ✅

💰 Position Size Recommendations:

  Conservative (1% risk):
    Lot Size: 0.33 lots
    Risk Amount: $100
    Potential Profit: $200

  Standard (2% risk):
    Lot Size: 0.67 lots
    Risk Amount: $200
    Potential Profit: $400

  Aggressive (3% risk):
    Lot Size: 1.00 lots
    Risk Amount: $300
    Potential Profit: $600

⚠️ Risk Assessment:
  ✅ R:R ratio acceptable (1:2)
  ✅ Stop loss appropriate (30 pips)
  ⚠️ Total exposure will be 18% (consider reducing)
  ✅ Sufficient margin available

💡 Recommendation:
  Use 0.33-0.50 lots (1-1.5% risk)
  Current 15% exposure is already moderate
  Consider closing other positions if adding this trade
```

## Position Sizing Tips

1. **Never risk more than 1-2% per trade**
2. **Keep total portfolio exposure under 20%**
3. **Account for correlation** - Don't trade multiple correlated pairs simultaneously
4. **Scale in gradually** - Split position across multiple entries
5. **Adjust for volatility** - Wider stops in volatile markets = smaller position

## See Also

- `/analyze` - Get stop loss recommendations from technical analysis
- `/scan` - Find high-probability setups worth risking capital on
