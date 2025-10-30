---
description: Validate trading strategies using historical data before risking real capital
---

# Strategy Backtesting Command

Test trading strategies on historical data to calculate real success probabilities, optimize parameters, and assess viability before live trading.

## Usage

Test a strategy:
```
/backtest "MA crossover with RSI filter"
```

With specific parameters:
```
/backtest "MACD crossover" --symbol EURUSD --timeframe H4 --period 500
```

Quick test for current pattern:
```
/backtest "Bullish Engulfing pattern"
```

## What It Does

Use the backtesting skill to:

1. **Define Strategy** - Clearly specify entry/exit rules:
   - Entry conditions (indicator values, pattern requirements)
   - Exit conditions (take profit, stop loss, trailing stop)
   - Position sizing rules
   - Filters (time of day, volatility, trend)

2. **Load Historical Data** - Retrieve candles from MetaTrader:
   - Default: Last 500 candles
   - Adjustable period and timeframe
   - Multiple symbols supported

3. **Simulate Trades** - Execute strategy on historical data:
   - Identify entry signals
   - Track open positions
   - Apply exit rules
   - Record all trades

4. **Calculate Performance Metrics**:
   - **Win Rate** - Percentage of profitable trades
   - **Average R:R** - Risk:Reward ratio achieved
   - **Profit Factor** - Gross profit / gross loss
   - **Max Drawdown** - Largest peak-to-trough decline
   - **Sharpe Ratio** - Risk-adjusted returns
   - **Total Return** - Net profit/loss over period

5. **Generate Report**:
   - Trade-by-trade breakdown
   - Equity curve visualization
   - Performance statistics
   - Optimization suggestions
   - Viability assessment

## Strategy Examples

**Moving Average Crossover:**
```
Entry: 50 SMA crosses above 200 SMA
Exit: 50 SMA crosses below 200 SMA, or -2% stop loss
```

**RSI Reversal:**
```
Entry: RSI < 30 and bullish candlestick pattern
Exit: RSI > 70, or +3% take profit, or -1.5% stop loss
```

**MACD + Bollinger:**
```
Entry: MACD crosses above signal AND price touches lower BB
Exit: Price reaches upper BB or -50 pips stop loss
```

**Pattern-Based:**
```
Entry: Morning Star or Bullish Engulfing on D1
Exit: 1:2 R:R target or opposite pattern appears
```

## Output Format

```
📊 Backtest Results - [STRATEGY NAME]

⚙️ Configuration:
  Symbol: EURUSD
  Timeframe: H4
  Period: 500 candles (≈3 months)
  Data Range: 2024-07-15 to 2024-10-29

📈 Performance Summary:
  Total Trades: 42
  Winners: 27 (64.3%)
  Losers: 15 (35.7%)

  Average Win: +85 pips
  Average Loss: -42 pips
  Average R:R: 1:2.02 ✅

  Profit Factor: 2.15
  Max Drawdown: -320 pips (8.5%)
  Total Return: +1,245 pips

📊 Risk-Adjusted Metrics:
  Sharpe Ratio: 1.85 (Good)
  Sortino Ratio: 2.34
  Calmar Ratio: 3.89

💡 Key Insights:
  ✅ Win rate above 60% is excellent
  ✅ Consistent R:R ratio (1:2+)
  ⚠️ Drawdown acceptable but monitor closely
  ✅ Profit factor > 2 indicates edge

📈 Best Trades:
  1. 2024-08-15: +156 pips (Entry: 1.0892, Exit: 1.1048)
  2. 2024-09-03: +134 pips (Entry: 1.1023, Exit: 1.1157)
  3. 2024-09-28: +128 pips (Entry: 1.0745, Exit: 1.0873)

📉 Worst Trades:
  1. 2024-07-22: -68 pips (Stopped out in choppy market)
  2. 2024-08-30: -52 pips (False signal, news event)
  3. 2024-10-05: -48 pips (Overnight gap against position)

🎯 Viability Assessment: ✅ VIABLE

  This strategy demonstrates a clear edge:
  - Consistent profitability over 3 months
  - Good risk management (R:R > 1:2)
  - Acceptable drawdown (< 10%)
  - Suitable for live trading with 1-2% risk per trade

⚠️ Recommendations:
  1. Test on additional symbols (GBPUSD, USDJPY)
  2. Optimize stop loss placement (-5% improvement possible)
  3. Consider adding volatility filter (ATR)
  4. Backtest on longer period (6-12 months)
  5. Paper trade for 1 month before going live

📄 Detailed report saved: reports/backtest_[STRATEGY]_[DATE].csv
```

## Backtesting Best Practices

1. **Test Sufficient Data** - Minimum 200 trades or 6 months
2. **Avoid Overfitting** - Don't optimize until perfect
3. **Account for Spreads** - Include realistic trading costs
4. **Test Multiple Symbols** - Ensure strategy is robust
5. **Forward Testing** - Paper trade before live
6. **Consider Market Regimes** - Test in trending/ranging markets

## Common Pitfalls

❌ **Curve Fitting** - Optimizing parameters to fit historical data perfectly
✅ **Solution**: Use simple rules, test on multiple symbols and periods

❌ **Insufficient Data** - Testing only 50-100 trades
✅ **Solution**: Use at least 6-12 months of data

❌ **Ignoring Costs** - Not accounting for spreads, commissions, slippage
✅ **Solution**: Include realistic 1-2 pip spread per trade

❌ **Survivorship Bias** - Testing only on current market conditions
✅ **Solution**: Test across different market regimes

## Workflow

1. **Develop Strategy** - Define clear entry/exit rules
2. **Initial Test** - `/backtest "strategy"` on 500 candles
3. **Analyze Results** - Review win rate, R:R, drawdown
4. **Optimize** - Refine parameters if needed
5. **Extended Test** - Backtest on 1000+ candles, multiple symbols
6. **Forward Test** - Paper trade for 1 month
7. **Live Trading** - Start with minimal risk (0.5% per trade)

## See Also

- `/analyze` - Get current market conditions for strategy
- `/risk` - Calculate position size for backtest-validated strategy
- `advanced-analytics` skill - For Monte Carlo simulations and advanced metrics
