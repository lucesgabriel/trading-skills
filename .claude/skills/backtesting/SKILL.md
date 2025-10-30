---
name: backtesting
description: Use when validating trading strategies with historical data, optimizing parameters, or assessing strategy viability before live trading.
version: 1.0.0
tags: [trading, backtesting, strategy-validation, historical-data, win-rate, profit-factor, optimization, testing]
category: strategy-validation
requires:
  mcp:
    - mcp__metatrader__get_candles_latest
    - mcp__metatrader__get_deals
    - mcp__metatrader__get_orders
  skills:
    - technical-analysis
difficulty: advanced
estimated_time: 60-180s
output_format: [console]
author: Gabriel Luces
repository: https://github.com/lucesgabriel/trading-skills
---

# Backtesting & Strategy Validation Skill

## Purpose
Validate trading strategies using historical data to calculate real success probabilities, identify optimal parameters, and assess strategy viability before risking real capital.

## When to Use This Skill

**Primary Triggers:**
- "backtest [STRATEGY]" or "test this strategy"
- "does this strategy work?"
- "validate [STRATEGY] on historical data"
- "what's the win rate of [STRATEGY]?"

**Use Cases:**
- User wants to test a trading strategy on historical data
- User needs to validate indicator settings or parameters
- User asks for historical performance metrics (win rate, profit factor, drawdown)
- User wants to assess strategy viability before live trading

**Example Inputs:**
```
✓ "backtest MA crossover strategy"
✓ "does RSI reversal strategy work?"
✓ "test Bullish Engulfing pattern on EURUSD"
✓ "validate this strategy on 6 months of data"
✗ "analyze EURUSD" → Use technical-analysis skill instead
```

## Backtesting Fundamentals

### What is Backtesting?
Testing a trading strategy against historical price data to see how it would have performed in the past. This helps predict future performance and identify strategy weaknesses before risking real capital.

### Key Metrics
- **Win Rate**: % of winning trades
- **Profit Factor**: Gross profit / Gross loss (>1.5 is good)
- **Expectancy**: Average profit per trade
- **Max Drawdown**: Largest equity decline (target: <20%)
- **Sharpe Ratio**: Risk-adjusted returns (>1.0 is acceptable)

Minimum: 30 trades for statistical significance, 100+ trades ideal.

📖 *See [resources/reference.md](resources/reference.md) for complete metric formulas*

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
# Get data from MetaTrader
candles = mcp__metatrader__get_candles_latest(
    symbol_name="EURUSD",
    timeframe="H4",
    count=2000  # ~330 days of H4 data
)
```

**Data Requirements:**
- Intraday: 6-12 months minimum
- Swing: 1-2 years minimum
- Position: 3-5 years minimum

### STEP 3: Process Data & Calculate Indicators

Convert candles to DataFrame and calculate all required indicators (MA, RSI, ATR, MACD, etc.).

📖 *See [resources/reference.md](resources/reference.md) for complete `prepare_backtest_data()` function*

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

Iterate through historical candles, check entry/exit conditions, track positions, and record all trades with P&L.

Use the `scripts/backtest_engine.py` which provides:
- `run_backtest()`: Vectorized backtest execution
- `default_ma_crossover()`: Example strategy
- Automatic metrics calculation

📖 *See [resources/reference.md](resources/reference.md) for complete `run_backtest()` implementation*

### STEP 5: Calculate Performance Metrics

Calculate all key metrics from trade results:
- Win rate, profit factor, expectancy
- Max drawdown, recovery factor
- Consecutive wins/losses
- Average R:R ratio

📖 *See [resources/reference.md](resources/reference.md) for complete `calculate_metrics()` function*

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

## Strategy Optimization

### Parameter Optimization
Test multiple parameter combinations (MA periods, RSI thresholds, ATR multipliers) to find optimal settings. Sort results by profit factor or expectancy.

⚠️ **Avoid overfitting**: Test on out-of-sample data, use walk-forward analysis.

### Walk-Forward Analysis
Prevents overfitting by testing strategy robustness:
1. Split data: 12-month training + 3-month testing
2. Optimize on training period
3. Test on out-of-sample period
4. Roll forward and repeat
5. Calculate Walk-Forward Efficiency (WFE)

**Acceptable degradation**: 10-30% between in-sample and out-sample

📖 *See [resources/reference.md](resources/reference.md) for optimization code & WFE calculations*

## Complete Workflow Example

```python
# 1. Get data
candles = mcp__metatrader__get_candles_latest("EURUSD", "H4", 2000)

# 2. Prepare & run
df = prepare_backtest_data(candles)
results = run_backtest(df, strategy, initial_capital=10000)

# 3. Calculate & present
metrics = calculate_metrics(results, 10000)
display_backtest_report(metrics, results)
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
