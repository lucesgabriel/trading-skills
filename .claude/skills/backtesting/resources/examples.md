# Backtesting - Usage Examples

## Example 1: Basic Strategy Backtest

### Input
```
User: "Backtest EURUSD MA crossover strategy for 2024"
```

### Expected Output
```
BACKTEST RESULTS: MA Crossover Strategy (EURUSD 2024)

Strategy Parameters:
├─ Fast MA: EMA(12)
├─ Slow MA: EMA(26)
├─ Entry: MA crossover
├─ Exit: Opposite crossover or 50 pip stop/target
├─ Timeframe: H1
└─ Period: 2024-01-01 to 2024-12-31

PERFORMANCE METRICS:

Profitability:
├─ Total Trades: 156
├─ Winning Trades: 89 (57%)
├─ Losing Trades: 67 (43%)
├─ Net Profit: +$2,340
├─ Starting Capital: $10,000
└─ Return: +23.4%

Risk Metrics:
├─ Max Drawdown: -8.2% ($820)
├─ Avg Win: $85
├─ Avg Loss: -$52
├─ Profit Factor: 1.63
└─ Expectancy: +$15 per trade

Trade Distribution:
├─ Longest Win Streak: 7 trades
├─ Longest Loss Streak: 5 trades
├─ Average Trade Duration: 6.3 hours
└─ Max Single Loss: -$180

Risk-Adjusted Returns:
├─ Sharpe Ratio: 1.45 (Good)
├─ Sortino Ratio: 2.12 (Excellent)
├─ Calmar Ratio: 2.85
└─ Recovery Factor: 2.85

VERDICT: ✓ VIABLE STRATEGY
- Positive expectancy
- Reasonable win rate (>55%)
- Good profit factor (>1.5)
- Controlled drawdown (<10%)
```

## Example 2: Parameter Optimization

### Input
```
User: "Optimize RSI period for GBPUSD mean reversion strategy"
```

### Expected Output
```
RSI PARAMETER OPTIMIZATION - GBPUSD Mean Reversion

Testing: RSI periods from 10 to 20 (2-unit increments)
Entry: RSI crosses above 30 (oversold) or below 70 (overbought)
Dataset: GBPUSD H4, 2023-2024 (2 years)

RESULTS:

RSI(10): ⭐⭐
├─ Net Profit: +$1,200
├─ Win Rate: 48%
├─ Profit Factor: 1.12
├─ Max DD: -12%
└─ Sharpe: 0.85

RSI(12): ⭐⭐⭐
├─ Net Profit: +$1,840
├─ Win Rate: 52%
├─ Profit Factor: 1.38
├─ Max DD: -9.5%
└─ Sharpe: 1.22

RSI(14): ⭐⭐⭐⭐⭐ OPTIMAL
├─ Net Profit: +$2,650
├─ Win Rate: 56%
├─ Profit Factor: 1.68
├─ Max DD: -7.8%
└─ Sharpe: 1.58

RSI(16): ⭐⭐⭐⭐
├─ Net Profit: +$2,180
├─ Win Rate: 54%
├─ Profit Factor: 1.52
├─ Max DD: -8.2%
└─ Sharpe: 1.35

RSI(18): ⭐⭐⭐
├─ Net Profit: +$1,560
├─ Win Rate: 51%
├─ Profit Factor: 1.28
├─ Max DD: -9.8%
└─ Sharpe: 1.08

RSI(20): ⭐⭐
├─ Net Profit: +$980
├─ Win Rate: 49%
├─ Profit Factor: 1.15
├─ Max DD: -11.2%
└─ Sharpe: 0.92

RECOMMENDATION: Use RSI(14)
- Best overall performance
- Optimal balance of responsiveness and reliability
- Lowest drawdown in winning configurations
```

## Example 3: Walk-Forward Analysis

### Input
```
User: "Run walk-forward analysis on my breakout strategy"
```

### Expected Output
```
WALK-FORWARD ANALYSIS: Breakout Strategy

Configuration:
├─ In-Sample Period: 6 months
├─ Out-Sample Period: 2 months
├─ Total Duration: 2 years
└─ Walk-Forward Windows: 4

RESULTS BY WINDOW:

Window 1 (Q1-Q2 2024):
├─ In-Sample: +$1,200 (58% win rate)
├─ Out-Sample: +$320 (54% win rate)
├─ Degradation: 15% (Acceptable)
└─ Status: ✓ Strategy held up

Window 2 (Q2-Q3 2024):
├─ In-Sample: +$1,450 (61% win rate)
├─ Out-Sample: +$280 (52% win rate)
├─ Degradation: 18% (Acceptable)
└─ Status: ✓ Strategy held up

Window 3 (Q3-Q4 2024):
├─ In-Sample: +$980 (55% win rate)
├─ Out-Sample: -$120 (45% win rate)
├─ Degradation: -112% (Failed)
└─ Status: ✗ Strategy failed

Window 4 (Q4 2024):
├─ In-Sample: +$1,180 (57% win rate)
├─ Out-Sample: +$240 (51% win rate)
├─ Degradation: 20% (Acceptable)
└─ Status: ✓ Strategy recovered

OVERALL ASSESSMENT:

Walk-Forward Efficiency: 68%
├─ 3/4 windows profitable
├─ 1 window showed weakness
├─ Average degradation: 20%
└─ Verdict: ⚠️ PROCEED WITH CAUTION

FINDINGS:
✓ Strategy generally robust
⚠️ Failed during low volatility period (Q3)
✓ Recovered when volatility returned

RECOMMENDATIONS:
1. Add volatility filter (ATR>20 pips)
2. Reduce position size during Q3-type conditions
3. Monitor for similar market conditions
4. Consider trading only during higher volatility
```

## Example 4: Multi-Symbol Backtest

### Input
```
User: "Test my strategy across all major pairs"
```

### Expected Output
```
MULTI-SYMBOL BACKTEST RESULTS (2024)

Strategy: Trend Following (MA + MACD)

BEST PERFORMERS:

1. GBPUSD: +$3,240 ⭐⭐⭐⭐⭐
   ├─ Win Rate: 62%
   ├─ Profit Factor: 1.95
   ├─ Max DD: -6.5%
   └─ Best pair for this strategy

2. EURUSD: +$2,680 ⭐⭐⭐⭐
   ├─ Win Rate: 58%
   ├─ Profit Factor: 1.72
   ├─ Max DD: -7.2%

3. AUDUSD: +$1,920 ⭐⭐⭐⭐
   ├─ Win Rate: 56%
   ├─ Profit Factor: 1.58
   ├─ Max DD: -8.1%

MODERATE PERFORMERS:

4. USDJPY: +$840 ⭐⭐⭐
5. USDCAD: +$620 ⭐⭐

POOR PERFORMERS:

6. USDCHF: -$180 ⭐
   ├─ Win Rate: 44%
   ├─ Issue: Choppy trends
   └─ Recommendation: Exclude

7. NZDUSD: -$420 ✗
   ├─ Win Rate: 41%
   ├─ Issue: Low liquidity, false signals
   └─ Recommendation: Exclude

PORTFOLIO APPROACH:

If trading all profitable pairs (Top 5):
├─ Combined Profit: +$9,300
├─ Diversification benefit
├─ Reduced single-pair risk
└─ Smoother equity curve

RECOMMENDATION:
Focus on GBPUSD, EURUSD, AUDUSD (top 3)
Avoid USDCHF and NZDUSD
```

## Example 5: Strategy Comparison

### Input
```
User: "Compare trend following vs mean reversion on EURUSD"
```

### Expected Output
```
STRATEGY COMPARISON: EURUSD (2024)

TREND FOLLOWING (MA Crossover):
├─ Total Trades: 45
├─ Win Rate: 54%
├─ Net Profit: +$2,150
├─ Profit Factor: 1.68
├─ Max DD: -8.5%
├─ Avg Trade Duration: 2.3 days
├─ Best Period: Strong trending markets
└─ Worst Period: Choppy consolidations

MEAN REVERSION (RSI):
├─ Total Trades: 128
├─ Win Rate: 61%
├─ Net Profit: +$1,980
├─ Profit Factor: 1.45
├─ Max DD: -6.2%
├─ Avg Trade Duration: 8.5 hours
├─ Best Period: Range-bound markets
└─ Worst Period: Strong breakouts

MARKET CONDITION ANALYSIS:

Trending Markets (45% of time):
├─ Trend Following: +$1,850 ✓ WINNER
└─ Mean Reversion: +$420

Range-Bound Markets (40% of time):
├─ Trend Following: +$180
└─ Mean Reversion: +$1,750 ✓ WINNER

Volatile/Mixed (15% of time):
├─ Trend Following: +$120
└─ Mean Reversion: -$190

RECOMMENDATION: HYBRID APPROACH

Use Market Regime Filter:
├─ ADX > 25: Trade Trend Following
├─ ADX < 25: Trade Mean Reversion
└─ Combined potential: +$3,600 (+82% better)

This adapts to market conditions automatically
```

## Best Practices for Backtesting

### Data Requirements
- **Minimum**: 1 year of data
- **Recommended**: 2-3 years
- **Optimal**: 5+ years (includes various market conditions)

### Validation Steps
1. **In-Sample Test** (60% of data): Develop/optimize strategy
2. **Out-Sample Test** (20% of data): Validate parameters
3. **Forward Test** (20% of data): Final verification
4. **Live Paper Trading**: Real-time validation

### Red Flags to Watch
- Win rate >75% (likely overfitted)
- Profit factor >3.0 (too good to be true)
- Max drawdown <3% (not realistic)
- Very few trades (<20 per year)
- Perfect equity curve (overfitted)

### Realistic Expectations
- Win rate: 45-65% is normal
- Profit factor: 1.5-2.5 is good
- Max drawdown: 10-25% is typical
- Sharpe ratio: >1.0 is acceptable, >1.5 is good

### Include in Backtest
- Spreads/commissions
- Slippage (1-3 pips typical)
- Swap/overnight fees
- Realistic fill prices
- Account size constraints
