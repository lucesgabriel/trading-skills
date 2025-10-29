---
name: risk-management
description: Calculate optimal position sizes, manage risk exposure, and monitor portfolio health for sustainable trading. Use when user asks about position sizing, "how much should I risk", stop loss placement, portfolio risk assessment, or before placing any trade.
---

# Risk Management & Position Sizing Skill

## Purpose
Calculate optimal position sizes, manage risk exposure, and monitor portfolio health to ensure sustainable trading with proper capital preservation.

## When to Use This Skill
- Before placing any trade
- User asks "how much should I risk?"
- User wants to calculate position size
- User needs stop loss recommendations
- User requests portfolio risk assessment
- Before scaling into positions

## Core Risk Management Principles

### The 1-2% Rule
**NEVER risk more than 1-2% of your account on a single trade**

```
Example with $10,000 account:
- 1% risk = $100 maximum loss per trade
- 2% risk = $200 maximum loss per trade

This means you can survive 50-100 consecutive losses
before account is depleted (which is statistically unlikely)
```

### The 5-10% Portfolio Rule
**Total open risk across ALL positions should not exceed 5-10% of account**

```
With $10,000 account and 5% max portfolio risk:
- Maximum total risk exposure = $500
- If trading 3 positions = $166 risk each
- Or 2 positions = $250 risk each
```

## Position Sizing Calculator

### Formula 1: Risk-Based Position Sizing (Primary Method)

```python
def calculate_position_size(account_balance, risk_percent, entry_price,
                           stop_loss_price, symbol_info):
    """
    Calculate position size based on risk tolerance

    Args:
        account_balance: Total account equity ($)
        risk_percent: Percentage to risk (1-2%)
        entry_price: Planned entry price
        stop_loss_price: Planned stop loss price
        symbol_info: Contract size, pip value, etc.

    Returns:
        Position size in lots
    """

    # Calculate monetary risk
    risk_amount = account_balance * (risk_percent / 100)

    # Calculate price distance (in pips for forex)
    if is_forex(symbol):
        pip_value = get_pip_value(symbol)
        distance_pips = abs(entry_price - stop_loss_price) / pip_value

        # Position size in lots
        # risk_amount = position_size_lots × distance_pips × pip_value_per_lot
        position_size = risk_amount / (distance_pips × pip_value_per_lot)

    else:  # For other instruments
        # distance in price points
        distance = abs(entry_price - stop_loss_price)

        # Position size
        position_size = risk_amount / distance

    return round(position_size, 2)
```

### Example Calculations

#### Example 1: Forex (EURUSD)
```
Account: $10,000
Risk: 1% = $100
Entry: 1.0850
Stop Loss: 1.0820
Distance: 30 pips

For standard lot (100,000 units):
- Pip value = $10 per pip
- Risk per lot = 30 pips × $10 = $300
- Position size = $100 / $300 = 0.33 lots

Trade Setup:
- Buy 0.33 lots EURUSD at 1.0850
- Stop loss at 1.0820 (30 pips)
- Maximum loss if stopped: $100 (1% of account)
```

#### Example 2: Gold (XAUUSD)
```
Account: $10,000
Risk: 2% = $200
Entry: $2015
Stop Loss: $2005
Distance: $10

For 1 lot (100 oz):
- $1 move = $100
- Risk per lot = $10 × $100 = $1,000
- Position size = $200 / $1,000 = 0.20 lots

Trade Setup:
- Buy 0.20 lots XAUUSD at $2015
- Stop loss at $2005 ($10 distance)
- Maximum loss if stopped: $200 (2% of account)
```

### Formula 2: R-Multiple Position Sizing

```python
def r_multiple_sizing(account_balance, r_value, entry_price,
                      stop_loss_price, target_price):
    """
    Calculate position using R-multiples

    R = Distance from entry to stop loss
    Reward = Distance from entry to target
    R:R Ratio = Reward / R
    """

    # Calculate R (risk per share/lot)
    r = abs(entry_price - stop_loss_price)

    # Calculate reward
    reward = abs(target_price - entry_price)

    # Risk/Reward ratio
    rr_ratio = reward / r

    # Position size to risk 1R = 1% of account
    risk_amount = account_balance * 0.01
    position_size = risk_amount / r

    return {
        'position_size': position_size,
        'risk_amount': risk_amount,
        'rr_ratio': rr_ratio,
        'potential_profit': risk_amount * rr_ratio
    }
```

### Scripts de Apoyo

El archivo `scripts/position_sizing.py` centraliza los cálculos anteriores.

**Funciones destacadas:**
- `calculate_position_size()` devuelve lotes, unidades y riesgo monetario según % de cuenta.
- `atr_adjusted_position_size()` permite stops basados en ATR sin recalcular manualmente.
- `portfolio_risk_snapshot()` agrega el riesgo abierto y valida límites de cartera.
- `dynamic_risk_allocation()` ajusta el riesgo base de acuerdo con volatilidad y convicción del setup.

**Ejemplo con MetaTrader MCP:**
```python
import sys
from pathlib import Path

base = Path(r"C:/Users/luces/Downloads/trading-skills/.claude/skills/risk-management/scripts")
sys.path.append(str(base))

from position_sizing import (
    calculate_position_size,
    portfolio_risk_snapshot,
    PositionExposure,
)

info = metatrader.get_account_info()
position = calculate_position_size(
    account_balance=info["balance"],
    risk_percent=1.25,
    entry_price=1.0850,
    stop_price=1.0815,
    symbol="EURUSD",
    is_buy=True,
)

open_positions = [
    PositionExposure("EURUSD", "LONG", risk_amount=120, risk_percent=1.2, account_balance=info["balance"]),
    PositionExposure("GBPJPY", "SHORT", risk_amount=150, risk_percent=1.5, account_balance=info["balance"]),
]
risk_view = portfolio_risk_snapshot(open_positions, max_portfolio_risk_percent=6.0)
```

**Ventajas:**
- Evita errores en pip values o tamaños de contrato al responder en vivo.
- Permite entregar cifras exactas (USD, lotes, % riesgo) sin derivar fórmulas cada vez.
- Facilita validar límites de cartera antes de sugerir nuevas posiciones.

## Stop Loss Strategies

### 1. ATR-Based Stop Loss (Dynamic)
```python
def atr_stop_loss(current_price, atr_value, multiplier=2, direction='buy'):
    """
    Calculate stop loss based on ATR (Average True Range)

    multiplier: 1.5-2.5 (2 is standard)
    - Tighter (1.5) for less volatile markets
    - Wider (2.5) for more volatile markets
    """

    if direction == 'buy':
        stop_loss = current_price - (atr_value * multiplier)
    else:  # sell
        stop_loss = current_price + (atr_value * multiplier)

    return round(stop_loss, 5)

# Example:
# EURUSD at 1.0850, ATR = 0.0015 (15 pips)
# Buy stop loss = 1.0850 - (0.0015 × 2) = 1.0820
```

### 2. Support/Resistance Stop Loss (Technical)
```python
def technical_stop_loss(entry_price, key_level, buffer_pips=5,
                        direction='buy'):
    """
    Place stop just beyond support/resistance

    buffer_pips: Safety buffer (3-10 pips typical)
    """

    pip_size = 0.0001 if 'JPY' not in symbol else 0.01
    buffer = buffer_pips * pip_size

    if direction == 'buy':
        # Place stop below support
        stop_loss = key_level - buffer
    else:  # sell
        # Place stop above resistance
        stop_loss = key_level + buffer

    return stop_loss

# Example:
# Buying EURUSD at 1.0850
# Support at 1.0820
# Stop = 1.0820 - (5 pips) = 1.0815
```

### 3. Percentage Stop Loss (Simple)
```python
def percentage_stop_loss(entry_price, percent=2, direction='buy'):
    """
    Simple percentage-based stop

    percent: 1-3% typically (2% standard)
    """

    if direction == 'buy':
        stop_loss = entry_price * (1 - percent/100)
    else:  # sell
        stop_loss = entry_price * (1 + percent/100)

    return round(stop_loss, 5)

# Example:
# EURUSD buy at 1.0850
# 2% stop = 1.0850 × 0.98 = 1.0633
```

### 4. Time-Based Stop Loss
```
If trade doesn't move favorably within X time:
- Scalping: 30-60 minutes
- Day trading: 4-8 hours
- Swing trading: 2-3 days

Exit to free up capital for better opportunities
```

## Take Profit Strategies

### 1. Risk/Reward Take Profit
```python
def rr_take_profit(entry_price, stop_loss, rr_ratio=2, direction='buy'):
    """
    Set take profit based on risk/reward ratio

    Standard R:R ratios:
    - Conservative: 1.5:1
    - Standard: 2:1
    - Aggressive: 3:1+
    """

    risk = abs(entry_price - stop_loss)
    reward = risk * rr_ratio

    if direction == 'buy':
        take_profit = entry_price + reward
    else:  # sell
        take_profit = entry_price - reward

    return take_profit

# Example:
# Entry: 1.0850, Stop: 1.0820, R:R = 2:1
# Risk: 30 pips
# Reward: 60 pips
# Take Profit: 1.0910
```

### 2. Multiple Take Profits (Scaling Out)
```python
def multiple_take_profits(entry, stop, position_size):
    """
    Scale out of position at multiple levels

    Recommended split:
    - 50% at 1.5R (secure profit)
    - 30% at 2.5R (good profit)
    - 20% at 3.5R (runner)
    """

    risk = abs(entry - stop)

    return {
        'tp1': {
            'price': entry + (risk × 1.5),
            'size': position_size × 0.5,
            'note': 'First profit take'
        },
        'tp2': {
            'price': entry + (risk × 2.5),
            'size': position_size × 0.3,
            'note': 'Main profit take'
        },
        'tp3': {
            'price': entry + (risk × 3.5),
            'size': position_size × 0.2,
            'note': 'Runner for big moves'
        }
    }
```

### 3. Trailing Stop
```python
def trailing_stop(current_price, highest_price, trail_pips=20):
    """
    Lock in profits as price moves favorably

    trail_pips: Distance to trail (15-30 pips typical)
    """

    pip_size = 0.0001
    trail_distance = trail_pips * pip_size

    trailing_stop = highest_price - trail_distance

    return trailing_stop

# Example:
# Entered at 1.0850
# Price now at 1.0920 (highest)
# Trailing stop 20 pips = 1.0900
# If price drops to 1.0900, exit with profit
```

## Portfolio Risk Management

### Current Exposure Calculator

```python
def calculate_portfolio_risk():
    """
    Get all open positions and calculate total risk
    """

    # Get account info
    account = metatrader:get_account_info()
    balance = account['balance']
    equity = account['equity']

    # Get all positions
    positions = metatrader:get_all_positions()

    total_risk = 0
    position_details = []

    for pos in positions:
        # Calculate risk per position
        entry = pos['price_open']
        current = pos['price_current']
        sl = pos['sl']
        volume = pos['volume']

        if sl > 0:
            # Risk in pips
            risk_pips = abs(entry - sl)
            # Convert to money
            risk_money = risk_pips × volume × pip_value

            total_risk += risk_money

            position_details.append({
                'symbol': pos['symbol'],
                'type': pos['type'],
                'volume': volume,
                'risk_money': risk_money,
                'risk_percent': (risk_money / balance) * 100,
                'profit': pos['profit']
            })

    portfolio_risk_percent = (total_risk / balance) * 100

    return {
        'balance': balance,
        'equity': equity,
        'total_risk_money': total_risk,
        'total_risk_percent': portfolio_risk_percent,
        'positions': position_details,
        'available_risk': max(0, (balance × 0.05) - total_risk)
    }
```

### Output Format

```
╔══════════════════════════════════════════════════════════╗
║              PORTFOLIO RISK ASSESSMENT                   ║
╚══════════════════════════════════════════════════════════╝

💰 ACCOUNT STATUS
Balance: $10,000
Equity: $10,235
Unrealized P&L: +$235 (+2.35%)
Free Margin: $8,500

⚠️ RISK EXPOSURE
Current Risk: $450 (4.5% of balance)
Maximum Allowed: $500 (5% limit)
Available Risk: $50 (0.5%)

📊 OPEN POSITIONS (3)

1. EURUSD - BUY
   Volume: 0.50 lots
   Entry: 1.0850 | Current: 1.0880
   Stop Loss: 1.0820 (30 pips)
   Risk: $150 (1.5%)
   Current P&L: +$150 (+1.5%)
   Status: ✅ In profit, consider trailing stop

2. GBPJPY - SELL
   Volume: 0.20 lots
   Entry: 195.50 | Current: 195.20
   Stop Loss: 196.00 (50 pips)
   Risk: $200 (2.0%)
   Current P&L: +$60 (+0.6%)
   Status: ✅ Approaching TP1

3. XAUUSD - BUY
   Volume: 0.10 lots
   Entry: 2015 | Current: 2020
   Stop Loss: 2005 ($10)
   Risk: $100 (1.0%)
   Current P&L: +$50 (+0.5%)
   Status: ⚡ Just entered, monitoring

───────────────────────────────────────────────────────────

📈 RISK DISTRIBUTION
By Symbol Type:
  - Forex: $350 (77.8%)
  - Commodities: $100 (22.2%)

By Direction:
  - Long positions: $250 (55.6%)
  - Short positions: $200 (44.4%)

⚠️ CORRELATION WARNING
EURUSD and XAUUSD often correlated
Consider reducing exposure if correlation high

───────────────────────────────────────────────────────────

✅ RECOMMENDATIONS

1. Portfolio Health: GOOD
   - Risk within safe limits (4.5% < 5%)
   - Profitable positions being managed well

2. Available Capacity: LOW
   - Only $50 (0.5%) risk available
   - Can open 1 small position OR wait for exits

3. Actions:
   ✓ Move EURUSD stop to breakeven
   ✓ Consider taking partial profit on GBPJPY
   ✓ Monitor XAUUSD for first 4 hours

4. Do NOT:
   ✗ Open new positions >0.5% risk
   ✗ Average down on any position
   ✗ Move stops further away
```

## Risk Management Rules

### Golden Rules
1. **Never risk more than 1-2% per trade**
2. **Total portfolio risk < 5-10%**
3. **Always use stop losses**
4. **Don't move stops against you**
5. **Take partial profits when available**
6. **Never average down on losing trades**
7. **Risk less on lower probability setups**

### Daily Loss Limit
```python
def check_daily_loss_limit(account_balance, daily_start_balance):
    """
    Stop trading if daily loss exceeds 3-5%
    """

    current_loss = daily_start_balance - account_balance
    loss_percent = (current_loss / daily_start_balance) * 100

    if loss_percent >= 3:
        return {
            'stop_trading': True,
            'message': f'Daily loss limit reached: {loss_percent:.1f}%'
        }

    return {'stop_trading': False}
```

### Weekly/Monthly Limits
```
Weekly Loss Limit: 10% of account
Monthly Loss Limit: 20% of account

If limits hit:
- Stop trading
- Review what went wrong
- Analyze trades
- Reset next period
```

## Position Sizing Examples

### Conservative Trader Profile
```
Account: $10,000
Risk per trade: 1%
Max positions: 3
Max portfolio risk: 3%

Typical position:
- Risk: $100 per trade
- Position size: Based on stop loss
- Take profit: 2:1 R:R minimum
```

### Moderate Trader Profile
```
Account: $10,000
Risk per trade: 1.5%
Max positions: 4
Max portfolio risk: 6%

Typical position:
- Risk: $150 per trade
- Position size: Based on stop loss
- Take profit: 1.5:1 R:R minimum
```

### Aggressive Trader Profile
```
Account: $10,000
Risk per trade: 2%
Max positions: 5
Max portfolio risk: 10%

Typical position:
- Risk: $200 per trade
- Position size: Based on stop loss
- Take profit: 1:1 R:R minimum (but aim for more)
```

## Integration with MetaTrader

```python
# Before placing trade, always calculate:

# 1. Get account info
account = metatrader:get_account_info()
balance = account['balance']

# 2. Check current exposure
current_risk = calculate_portfolio_risk()

# 3. Calculate new position size
position = calculate_position_size(
    account_balance=balance,
    risk_percent=1.5,
    entry_price=1.0850,
    stop_loss_price=1.0820,
    symbol='EURUSD'
)

# 4. Verify within limits
if current_risk['total_risk_percent'] + 1.5 <= 5.0:
    # Safe to trade
    metatrader:place_market_order(
        symbol='EURUSD',
        type='BUY',
        volume=position['size']
    )

    # Set stop loss immediately
    metatrader:modify_position(
        id=position_id,
        stop_loss=1.0820,
        take_profit=1.0910
    )
else:
    print("❌ Cannot open position: Portfolio risk limit reached")
```

## Common Mistakes to Avoid

❌ **Over-leveraging**: Using too much leverage
❌ **No stop loss**: Trading without protection
❌ **Risking too much**: >2% per trade
❌ **Moving stops**: Moving SL away from price
❌ **Averaging down**: Adding to losers
❌ **Ignoring correlation**: Multiple correlated positions
❌ **Emotional sizing**: Bigger size after losses
❌ **All-in mentality**: Putting all capital in one trade

---

**Remember**: Proper risk management is what separates successful traders from those who blow up their accounts. Always size positions correctly and use stop losses.
