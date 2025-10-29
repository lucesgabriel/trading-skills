---
name: backtesting
description: Validate trading strategies using historical data to calculate real success probabilities, optimize parameters, and assess strategy viability before risking capital. Use when user wants to test strategy, asks "does this strategy work", needs historical performance data, or before deploying new trading approach.
---

# Backtesting & Strategy Validation Skill

## Purpose
Validate trading strategies using historical data to calculate real success probabilities, identify optimal parameters, and assess strategy viability before risking real capital.

## When to Use This Skill
- User wants to test a trading strategy
- User asks "does this strategy work?"
- User needs to validate indicator settings
- User wants historical performance data
- Before deploying any new trading approach
- To optimize entry/exit rules

## Backtesting Fundamentals

### What is Backtesting?
Testing a trading strategy against historical price data to see how it would have performed in the past. This helps predict future performance and identify strategy weaknesses.

### Key Metrics to Track
```python
PERFORMANCE METRICS:
- Win Rate: (Winning Trades / Total Trades) × 100
- Average Win: Average profit from winning trades
- Average Loss: Average loss from losing trades
- Profit Factor: Gross Profit / Gross Loss
- Expectancy: (Win Rate × Avg Win) - (Loss Rate × Avg Loss)
- Maximum Drawdown: Largest peak-to-trough decline
- Risk/Reward Ratio: Average of all trades
- Recovery Factor: Net Profit / Max Drawdown
- Sharpe Ratio: Risk-adjusted returns

QUALITY METRICS:
- Total Trades: Sample size (100+ for statistical significance)
- Consecutive Losses: Longest losing streak
- Consecutive Wins: Longest winning streak
- Time in Market: Percentage of time with open positions
```

## Backtesting Workflow

### STEP 1: Define Strategy Rules

```python
strategy = {
    'name': 'MA Crossover with RSI Filter',

    'entry_rules': {
        'long': [
            'SMA(20) crosses above SMA(50)',
            'RSI(14) > 50',
            'Price above SMA(200)'
        ],
        'short': [
            'SMA(20) crosses below SMA(50)',
            'RSI(14) < 50',
            'Price below SMA(200)'
        ]
    },

    'exit_rules': {
        'stop_loss': '2 × ATR(14)',
        'take_profit': '3 × ATR(14)',
        'trailing_stop': 'After 1.5R profit, trail at 1R',
        'time_stop': 'Exit if no profit after 5 days'
    },

    'filters': {
        'timeframe': 'H4',
        'market_conditions': 'Only during London/NY sessions',
        'volatility': 'ATR must be > average ATR(50)'
    },

    'risk_management': {
        'risk_per_trade': 1.5,  # Percentage
        'max_positions': 3,
        'max_daily_loss': 3,    # Percentage
        'position_sizing': 'Fixed fractional'
    }
}
```

### STEP 2: Get Historical Data

```python
def get_backtest_data(symbol, timeframe, lookback_days):
    """
    Get sufficient historical data for backtesting

    Recommended minimums:
    - Intraday strategies: 6-12 months
    - Swing strategies: 1-2 years
    - Position strategies: 3-5 years
    """

    # Calculate required candles
    candles_needed = calculate_candles(timeframe, lookback_days)

    # Get data from MetaTrader
    data = metatrader:get_candles_latest(
        symbol_name=symbol,
        timeframe=timeframe,
        count=min(candles_needed, 10000)  # API limit
    )

    return data
```

### STEP 3: Process Data & Calculate Indicators

```python
def prepare_backtest_data(candles):
    """
    Calculate all necessary indicators for strategy
    """

    import pandas as pd
    import numpy as np

    # Convert to DataFrame
    df = pd.DataFrame(candles)

    # Calculate Moving Averages
    df['sma_20'] = df['close'].rolling(window=20).mean()
    df['sma_50'] = df['close'].rolling(window=50).mean()
    df['sma_200'] = df['close'].rolling(window=200).mean()

    # Calculate RSI
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))

    # Calculate ATR
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = ranges.max(axis=1)
    df['atr'] = true_range.rolling(window=14).mean()

    # Calculate MACD
    ema_12 = df['close'].ewm(span=12, adjust=False).mean()
    ema_26 = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = ema_12 - ema_26
    df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
    df['macd_hist'] = df['macd'] - df['macd_signal']

    # Identify crossovers
    df['ma_cross_up'] = (df['sma_20'] > df['sma_50']) & \
                        (df['sma_20'].shift(1) <= df['sma_50'].shift(1))
    df['ma_cross_down'] = (df['sma_20'] < df['sma_50']) & \
                          (df['sma_20'].shift(1) >= df['sma_50'].shift(1))

    return df
```

### Scripts de Apoyo

El script `scripts/backtest_engine.py` ofrece un motor vectorizado listo para usar.

**Componentes principales:**
- `candles_to_dataframe()` normaliza velas crudas en un DataFrame ordenado.
- `run_backtest()` ejecuta el backtest y devuelve un `BacktestResult` con métricas clave.
- `default_ma_crossover()` ejemplo de estrategia (SMA rápida vs lenta) para pruebas rápidas.
- `BacktestResult` incluye retorno total/anualizado, win rate, profit factor, expectancy, drawdown, Sharpe y lista de trades.

**Ejemplo de uso:**
```python
import sys
from pathlib import Path

base = Path(r"C:/Users/luces/Downloads/trading-skills/.claude/skills/backtesting/scripts")
sys.path.append(str(base))

from backtest_engine import run_backtest, default_ma_crossover

candles = metatrader.get_candles_latest("EURUSD", "H1", 2000)
result = run_backtest(candles, strategy_fn=default_ma_crossover, risk_per_trade=1.0)

print(result.total_return_pct, result.win_rate_pct, result.profit_factor)
```

**Ventajas:**
- Acelera la preparación de resultados cuantitativos sin escribir loops manualmente.
- Produce métricas alineadas con la sección de "Key Metrics" del skill.
- La lista `result.trades` permite analizar cada operación y generar tablas/resúmenes.

### STEP 4: Run Backtest Simulation

```python
def run_backtest(df, strategy, initial_capital=10000):
    """
    Simulate trading strategy on historical data
    """

    results = {
        'trades': [],
        'equity_curve': [],
        'daily_returns': []
    }

    capital = initial_capital
    position = None
    equity = [initial_capital]

    for i in range(len(df)):
        current = df.iloc[i]

        # Skip if not enough history
        if pd.isna(current['sma_200']):
            continue

        # Check for exit signals if in position
        if position is not None:
            exit_price = None
            exit_reason = None

            # Check stop loss
            if position['type'] == 'long':
                if current['low'] <= position['stop_loss']:
                    exit_price = position['stop_loss']
                    exit_reason = 'Stop Loss'
            else:  # short
                if current['high'] >= position['stop_loss']:
                    exit_price = position['stop_loss']
                    exit_reason = 'Stop Loss'

            # Check take profit
            if position['type'] == 'long':
                if current['high'] >= position['take_profit']:
                    exit_price = position['take_profit']
                    exit_reason = 'Take Profit'
            else:  # short
                if current['low'] <= position['take_profit']:
                    exit_price = position['take_profit']
                    exit_reason = 'Take Profit'

            # Exit if signal found
            if exit_price:
                # Calculate P&L
                if position['type'] == 'long':
                    pnl = (exit_price - position['entry']) * position['size']
                else:  # short
                    pnl = (position['entry'] - exit_price) * position['size']

                capital += pnl

                # Record trade
                results['trades'].append({
                    'entry_date': position['entry_date'],
                    'exit_date': current['time'],
                    'type': position['type'],
                    'entry_price': position['entry'],
                    'exit_price': exit_price,
                    'exit_reason': exit_reason,
                    'pnl': pnl,
                    'pnl_percent': (pnl / position['risk']) * 100,
                    'duration': i - position['entry_index']
                })

                position = None

        # Check for entry signals if not in position
        if position is None:
            # Long entry
            if (current['ma_cross_up'] and
                current['rsi'] > 50 and
                current['close'] > current['sma_200']):

                # Calculate position size based on risk
                risk_amount = capital * (strategy['risk_management']['risk_per_trade'] / 100)
                stop_distance = 2 * current['atr']
                stop_loss = current['close'] - stop_distance
                take_profit = current['close'] + (3 * current['atr'])

                position = {
                    'type': 'long',
                    'entry': current['close'],
                    'entry_date': current['time'],
                    'entry_index': i,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit,
                    'size': risk_amount / stop_distance,
                    'risk': risk_amount
                }

            # Short entry
            elif (current['ma_cross_down'] and
                  current['rsi'] < 50 and
                  current['close'] < current['sma_200']):

                risk_amount = capital * (strategy['risk_management']['risk_per_trade'] / 100)
                stop_distance = 2 * current['atr']
                stop_loss = current['close'] + stop_distance
                take_profit = current['close'] - (3 * current['atr'])

                position = {
                    'type': 'short',
                    'entry': current['close'],
                    'entry_date': current['time'],
                    'entry_index': i,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit,
                    'size': risk_amount / stop_distance,
                    'risk': risk_amount
                }

        # Track equity
        if position:
            # Mark-to-market
            if position['type'] == 'long':
                unrealized = (current['close'] - position['entry']) * position['size']
            else:
                unrealized = (position['entry'] - current['close']) * position['size']
            equity.append(capital + unrealized)
        else:
            equity.append(capital)

    results['equity_curve'] = equity
    results['final_capital'] = capital

    return results
```

### STEP 5: Calculate Performance Metrics

```python
def calculate_metrics(results, initial_capital):
    """
    Calculate comprehensive performance statistics
    """

    trades = results['trades']

    if len(trades) == 0:
        return "No trades generated"

    # Basic stats
    total_trades = len(trades)
    winning_trades = [t for t in trades if t['pnl'] > 0]
    losing_trades = [t for t in trades if t['pnl'] < 0]

    win_rate = (len(winning_trades) / total_trades) * 100

    # P&L stats
    total_profit = sum(t['pnl'] for t in winning_trades)
    total_loss = abs(sum(t['pnl'] for t in losing_trades))
    net_profit = total_profit - total_loss

    avg_win = total_profit / len(winning_trades) if winning_trades else 0
    avg_loss = total_loss / len(losing_trades) if losing_trades else 0

    # Profit factor
    profit_factor = total_profit / total_loss if total_loss > 0 else float('inf')

    # Expectancy
    expectancy = (win_rate/100 * avg_win) - ((100-win_rate)/100 * avg_loss)

    # Drawdown calculation
    equity_curve = results['equity_curve']
    running_max = np.maximum.accumulate(equity_curve)
    drawdown = (equity_curve - running_max) / running_max * 100
    max_drawdown = np.min(drawdown)

    # Consecutive wins/losses
    consecutive_wins = max_consecutive(trades, 'win')
    consecutive_losses = max_consecutive(trades, 'loss')

    # Risk/Reward
    avg_rr = np.mean([abs(t['pnl']) / t['risk'] for t in winning_trades]) if winning_trades else 0

    return {
        'total_trades': total_trades,
        'win_rate': round(win_rate, 2),
        'profit_factor': round(profit_factor, 2),
        'net_profit': round(net_profit, 2),
        'net_profit_percent': round((net_profit / initial_capital) * 100, 2),
        'avg_win': round(avg_win, 2),
        'avg_loss': round(avg_loss, 2),
        'expectancy': round(expectancy, 2),
        'max_drawdown': round(max_drawdown, 2),
        'recovery_factor': round(net_profit / abs(max_drawdown), 2) if max_drawdown != 0 else 0,
        'consecutive_wins': consecutive_wins,
        'consecutive_losses': consecutive_losses,
        'avg_rr_ratio': round(avg_rr, 2),
        'winning_trades': len(winning_trades),
        'losing_trades': len(losing_trades)
    }
```

### STEP 6: Present Results

```
╔═══════════════════════════════════════════════════════════════╗
║            BACKTEST RESULTS - MA CROSSOVER STRATEGY           ║
╚═══════════════════════════════════════════════════════════════╝

📊 TEST PARAMETERS
Symbol: EURUSD
Timeframe: H4 (4-Hour)
Period: 2023-01-01 to 2024-10-27 (22 months)
Initial Capital: $10,000
Risk Per Trade: 1.5%

═══════════════════════════════════════════════════════════════

📈 PERFORMANCE SUMMARY

Net Profit: $3,245 (+32.45%)
Total Trades: 87
Win Rate: 58.62%

Winning Trades: 51 (58.62%)
  - Average Win: $156.40
  - Total Profit: $7,976

Losing Trades: 36 (41.38%)
  - Average Loss: $131.42
  - Total Loss: $4,731

───────────────────────────────────────────────────────────────

💯 KEY METRICS

Profit Factor: 1.69 ✅ (>1.5 is good)
Expectancy: $37.30 per trade ✅
Average R:R Ratio: 1.84:1 ✅

Maximum Drawdown: -12.3% ⚠️ (Manageable)
Recovery Factor: 2.64 ✅ (>2 is excellent)

Consecutive Wins: 7
Consecutive Losses: 5

───────────────────────────────────────────────────────────────

📊 MONTHLY BREAKDOWN

2023 Q1: +$420 (+4.2%)  - 12 trades, 58% win rate
2023 Q2: +$680 (+6.8%)  - 15 trades, 60% win rate
2023 Q3: -$150 (-1.5%)  - 11 trades, 45% win rate ⚠️
2023 Q4: +$890 (+8.9%)  - 18 trades, 61% win rate
2024 Q1: +$580 (+5.8%)  - 13 trades, 54% win rate
2024 Q2: +$510 (+5.1%)  - 10 trades, 60% win rate
2024 Q3: +$315 (+3.2%)  - 8 trades, 62% win rate

───────────────────────────────────────────────────────────────

📉 EQUITY CURVE ANALYSIS

Starting: $10,000
Peak: $13,580 (reached Aug 2024)
Current: $13,245
From Peak: -2.5%

Best Month: +$890 (Q4 2023)
Worst Month: -$150 (Q3 2023)

Smooth Curve: YES ✅
Consistent Growth: YES ✅

───────────────────────────────────────────────────────────────

✅ STRENGTHS

1. Positive Expectancy ($37 per trade)
   → Strategy has mathematical edge

2. Good Profit Factor (1.69)
   → Profits significantly exceed losses

3. Acceptable Win Rate (58.6%)
   → More wins than losses

4. Controlled Drawdown (-12.3%)
   → Risk is manageable

5. Consistent Performance
   → Profitable in 6 out of 7 quarters

───────────────────────────────────────────────────────────────

⚠️ WEAKNESSES

1. Moderate Drawdown (12.3%)
   → Requires psychological resilience
   → Consider reducing risk to 1% per trade

2. Consecutive Losses (5 in a row)
   → Can happen, need strong discipline
   → Daily loss limits recommended

3. Q3 2023 Negative Performance
   → Strategy struggled in ranging market
   → Consider volatility filter

───────────────────────────────────────────────────────────────

🎯 OPTIMIZATION SUGGESTIONS

1. Add Volatility Filter
   → Only trade when ATR > 20-period average
   → Should improve win rate in trends

2. Reduce Position Size to 1%
   → Would reduce drawdown to ~8%
   → Still profitable with better risk profile

3. Add Market Regime Filter
   → Only trade when price above SMA(200)
   → Eliminates choppy ranging trades

4. Improve Exit Strategy
   → Consider trailing stop at 2R
   → Could increase average win

───────────────────────────────────────────────────────────────

💡 PROBABILITY ASSESSMENT

Based on backtest results:

Win Probability: 58-60% ✅
Average R:R: 1.8:1 ✅
Expectancy: $37 per trade ✅

REAL SUCCESS PROBABILITY: 65-70%

This accounts for:
+ Positive historical performance
+ Consistent across different periods
- Some optimization needed
- Market conditions may vary

───────────────────────────────────────────────────────────────

📋 FORWARD TESTING RECOMMENDATION

Status: APPROVED FOR PAPER TRADING ✅

Next Steps:
1. Paper trade for 3 months
2. Apply suggested optimizations
3. Track actual vs. expected results
4. Compare to backtest performance

If paper trading matches backtest:
→ Ready for live trading with small size

If paper trading underperforms:
→ Re-optimize or consider different strategy

═══════════════════════════════════════════════════════════════

⚠️ IMPORTANT DISCLAIMERS

• Past performance ≠ future results
• Backtests can be over-optimized
• Real trading includes slippage/spread
• Emotional discipline required
• Market conditions change
• Always use proper risk management

This backtest provides guidance, not guarantees.
```

## Strategy Optimization Process

### Parameter Optimization
```python
def optimize_parameters(symbol, timeframe, data):
    """
    Test multiple parameter combinations
    """

    # Parameters to test
    ma_periods = [(10,20), (20,50), (50,100), (50,200)]
    rsi_thresholds = [(30,70), (40,60), (45,55)]
    atr_multipliers = [(1.5,2.5), (2,3), (2.5,4)]

    results = []

    for ma in ma_periods:
        for rsi in rsi_thresholds:
            for atr in atr_multipliers:
                # Run backtest with these parameters
                strategy_result = run_backtest_with_params(
                    data, ma, rsi, atr
                )

                results.append({
                    'params': {'ma': ma, 'rsi': rsi, 'atr': atr},
                    'metrics': calculate_metrics(strategy_result)
                })

    # Sort by profit factor or expectancy
    results.sort(key=lambda x: x['metrics']['profit_factor'],
                 reverse=True)

    return results[:5]  # Top 5 combinations
```

### Walk-Forward Analysis
```
Instead of testing on all historical data:

1. Split data into chunks:
   - Training period: 12 months
   - Testing period: 3 months
   - Repeat rolling forward

2. Optimize on training period
3. Test on out-of-sample data
4. Verify consistency across periods

This prevents over-fitting!
```

## Integration with MetaTrader

```python
# Complete backtest workflow

# 1. Get historical data
symbol = "EURUSD"
timeframe = "H4"
candles = metatrader:get_candles_latest(
    symbol_name=symbol,
    timeframe=timeframe,
    count=2000  # ~330 days of H4 data
)

# 2. Prepare data
df = prepare_backtest_data(candles)

# 3. Define strategy
strategy = define_strategy()

# 4. Run backtest
results = run_backtest(df, strategy, initial_capital=10000)

# 5. Calculate metrics
metrics = calculate_metrics(results, 10000)

# 6. Present results
display_backtest_report(metrics, results)

# 7. Optimize if needed
optimized = optimize_parameters(symbol, timeframe, df)
```

## Best Practices

1. **Sufficient Data**: At least 1-2 years minimum
2. **Out-of-Sample Testing**: Always reserve 20-30% for validation
3. **Multiple Symbols**: Test on different pairs
4. **Multiple Timeframes**: Verify across timeframes
5. **Include Costs**: Factor in spread/commission
6. **Avoid Curve-Fitting**: Don't over-optimize
7. **Monte Carlo**: Run 1000+ simulations
8. **Paper Trade**: Always paper trade first

## Common Pitfalls

❌ **Overfitting**: Strategy works perfectly on past data but fails live
❌ **Look-Ahead Bias**: Using future information
❌ **Survivorship Bias**: Only testing on currently traded symbols
❌ **Data-Mining Bias**: Testing too many strategies until one works
❌ **Ignoring Costs**: Forgetting spread/commission
❌ **Small Sample Size**: Not enough trades to be statistically significant

---

**Remember**: Backtesting is just the first step. Paper trading and live testing with small sizes are essential before full deployment.
