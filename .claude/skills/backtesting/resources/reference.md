# Backtesting - Technical Reference

## Complete Python Implementation

### Data Preparation Function

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

### Complete Backtest Simulation

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

### Performance Metrics Calculation

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

## Complete Strategy Definition Template

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

## Walk-Forward Analysis Implementation

```
Walk-Forward Testing Process:

1. Split data into chunks:
   - Training period: 12 months
   - Testing period: 3 months
   - Repeat rolling forward

2. For each window:
   a. Optimize parameters on training period
   b. Test optimized params on out-of-sample data
   c. Record performance degradation

3. Acceptable degradation:
   ✓ 10-30%: Normal, expected
   ⚠️ 30-50%: Strategy may be overfit
   ❌ >50%: Likely overfitted, unreliable

4. Calculate Walk-Forward Efficiency:
   WFE = Out-Sample Performance / In-Sample Performance

   ✓ WFE > 0.5: Good
   ⚠️ WFE 0.3-0.5: Acceptable
   ❌ WFE < 0.3: Poor
```

## MetaTrader Integration Example

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

## Performance Metrics Formulas

### Win Rate
```
Win Rate = (Number of Winning Trades / Total Trades) × 100
```

### Profit Factor
```
Profit Factor = Gross Profit / Gross Loss

Interpretation:
>3.0: Excellent
2.0-3.0: Very good
1.5-2.0: Good
1.0-1.5: Acceptable
<1.0: Losing strategy
```

### Expectancy
```
Expectancy = (Win Rate × Average Win) - (Loss Rate × Average Loss)

Positive expectancy = Edge in market
Negative expectancy = No edge, will lose over time
```

### Maximum Drawdown
```
Drawdown at time T = (Equity at T - Maximum Equity before T) / Maximum Equity before T

Max Drawdown = Minimum value of all drawdowns

Interpretation:
<10%: Excellent
10-15%: Good
15-25%: Acceptable
>25%: High risk
```

### Recovery Factor
```
Recovery Factor = Net Profit / Maximum Drawdown

Interpretation:
>3.0: Excellent recovery
2.0-3.0: Good recovery
1.0-2.0: Acceptable
<1.0: Poor (drawdown > profit)
```

### Sharpe Ratio
```
Sharpe = (Average Return - Risk Free Rate) / Standard Deviation of Returns

Annualized: multiply by √(number of periods per year)

Interpretation:
>2.0: Excellent
1.0-2.0: Good
0.5-1.0: Acceptable
<0.5: Poor
```

### Calmar Ratio
```
Calmar = Annualized Return / Maximum Drawdown

Interpretation:
>3.0: Excellent
2.0-3.0: Good
1.0-2.0: Acceptable
<1.0: Poor
```

## Data Requirements by Strategy Type

### Intraday/Scalping
- Minimum: 6 months
- Recommended: 12 months
- Optimal: 18-24 months
- Timeframes: M5, M15, M30

### Day Trading
- Minimum: 12 months
- Recommended: 18-24 months
- Optimal: 2-3 years
- Timeframes: H1, H4

### Swing Trading
- Minimum: 2 years
- Recommended: 3-4 years
- Optimal: 5+ years
- Timeframes: H4, Daily

### Position Trading
- Minimum: 3 years
- Recommended: 5 years
- Optimal: 10+ years
- Timeframes: Daily, Weekly

## MetaTrader Data Availability

```
Typical MetaTrader 5 Historical Data:

M1:  ~2 months (~80,000 candles)
M5:  ~3 months (~26,000 candles)
M15: ~6 months (~17,000 candles)
M30: ~1 year (~17,000 candles)
H1:  ~2 years (~17,000 candles)
H4:  ~7 years (~15,000 candles)
D1:  ~20 years (~5,000 candles)
W1:  ~40 years (~2,000 candles)

Note: Varies by broker and symbol
Some brokers offer extended history downloads
```

## Statistical Significance

### Minimum Trade Requirements

```
Statistical Confidence Levels:

30 trades:   Minimum acceptable
50 trades:   Reasonable confidence
100 trades:  Good confidence
200+ trades: High confidence

Formula for required sample size:
n = (Z × σ / E)²

Where:
Z = Z-score for confidence level (1.96 for 95%)
σ = Standard deviation of returns
E = Margin of error (desired precision)
```

### Avoiding Overfitting

```
Signs of Overfitting:
❌ Win rate >75%
❌ Profit factor >3.5
❌ Max drawdown <3%
❌ Perfect equity curve
❌ Too many parameters optimized
❌ Strategy works on one symbol only
❌ Performance degrades in forward testing

Prevention:
✓ Use out-of-sample testing (20-30% of data)
✓ Walk-forward analysis
✓ Test on multiple symbols
✓ Minimize number of parameters
✓ Avoid excessive optimization
✓ Paper trade before going live
✓ Accept realistic metrics
```

## Common Backtesting Biases

### Look-Ahead Bias
```
Using information not available at decision time

Example:
❌ Using close price before bar closes
❌ Using tomorrow's high/low
❌ Peeking at future candles

Solution:
✓ Only use data available at bar open
✓ Implement realistic order fills
✓ Account for execution delay
```

### Survivorship Bias
```
Testing only symbols that still exist

Example:
❌ Backtesting only current S&P 500 members
❌ Ignoring delisted companies
❌ Testing only active forex pairs

Solution:
✓ Include delisted/removed symbols
✓ Use complete historical universe
✓ Account for symbol changes
```

### Data-Mining Bias
```
Testing too many strategies until one works by chance

Example:
❌ Testing 100 strategies, using the 1 that worked
❌ Over-optimizing parameters
❌ P-hacking statistical results

Solution:
✓ Have hypothesis before testing
✓ Limit number of tests
✓ Use proper statistical validation
✓ Bonferroni correction for multiple tests
```

## Realistic Performance Expectations

### Professional Trading Returns

```
Hedge Funds: 10-20% annual return (considered good)
Proprietary Firms: 15-30% annual return
Top Retail Traders: 20-50% annual return

Realistic Backtest Metrics:
Win Rate: 45-65%
Profit Factor: 1.3-2.5
Max Drawdown: 10-25%
Sharpe Ratio: 0.5-2.0
Monthly Return: 2-5%
```

### Red Flags in Backtest Results

```
Too Good To Be True Metrics:
❌ Win rate 80%+ consistently
❌ Profit factor >4.0
❌ Max drawdown <5%
❌ Sharpe ratio >3.0
❌ Every month profitable
❌ Zero losing weeks

These suggest:
- Overfitting
- Look-ahead bias
- Unrealistic assumptions
- Calculation errors
```

This reference provides complete technical implementations and formulas for all backtesting operations. For usage examples and workflows, see the main SKILL.md file.
