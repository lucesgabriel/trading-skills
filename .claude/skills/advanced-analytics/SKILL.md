---
name: advanced-analytics
description: Use when analyzing performance metrics, detecting price patterns, or assessing correlations between trading instruments.
---

# Advanced Analytics Skill

## Purpose
Provide sophisticated analytical capabilities beyond basic technical indicators. This skill enables:
- **Statistical Analysis**: Sharpe ratio, Sortino ratio, risk-adjusted returns, Monte Carlo simulations
- **Pattern Recognition**: Automatic detection of candlestick patterns (hammer, engulfing, doji, etc.)
- **Correlation Analysis**: Identify correlated pairs, portfolio concentration risk, diversification opportunities

## When to Use This Skill

**Primary Triggers:**
- "calculate Sharpe ratio" or "risk-adjusted returns"
- "correlation between [PAIR1] and [PAIR2]"
- "Monte Carlo simulation for [STRATEGY]"
- "risk of ruin calculation"

**Use Cases:**
- User wants advanced performance metrics (Sharpe, Sortino, Calmar ratios)
- User asks about correlation between currency pairs for diversification
- User needs Monte Carlo simulation for strategy validation
- User wants sophisticated statistical analysis beyond basic indicators

**Example Inputs:**
```
✓ "calculate Sharpe ratio for my trades"
✓ "what's the correlation between EURUSD and GBPUSD?"
✓ "run Monte Carlo simulation for this strategy"
✓ "calculate risk of ruin"
✗ "scan EURUSD" → Use pattern-scanner skill instead
```

## Available Scripts

### 1. Advanced Statistics (`scripts/advanced_statistics.py`)

Calculates sophisticated performance metrics:

**Key Functions:**
- `calculate_sharpe_ratio()`: Risk-adjusted returns
- `calculate_sortino_ratio()`: Downside-only volatility measure
- `calculate_maximum_drawdown()`: Worst peak-to-trough decline
- `calculate_calmar_ratio()`: Return vs drawdown
- `calculate_win_loss_streaks()`: Longest winning/losing streaks
- `calculate_r_multiples()`: R-multiple distribution analysis
- `calculate_risk_of_ruin()`: Probability of catastrophic loss
- `monte_carlo_simulation()`: Simulate future outcomes
- `calculate_all_statistics()`: Comprehensive analysis

**When to Use:**
```
"Calculate my Sharpe ratio for last month"
"What's my risk-adjusted performance?"
"Run a Monte Carlo simulation on my strategy"
"Calculate risk of ruin with current parameters"
"Analyze my win/loss streaks"
"What are my R-multiples?"
```

**Implementation:**
```python
import sys
sys.path.append('C:/Users/luces/Downloads/trading-skills/scripts')
from advanced_statistics import calculate_all_statistics

# Get trades from MetaTrader
orders = metatrader.get_orders(from_date='2024-01-01', to_date='2024-10-28')
deals = metatrader.get_deals(from_date='2024-01-01', to_date='2024-10-28')

# Convert to DataFrame with required columns
import pandas as pd
trades_df = pd.DataFrame({
    'timestamp': pd.to_datetime(deals['time']),
    'profit': deals['profit'],
    'risk': deals['risk']  # Calculate from stop loss
})

# Calculate comprehensive statistics
stats = calculate_all_statistics(trades_df)

# Present results
print("=== ADVANCED PERFORMANCE STATISTICS ===")
print(f"\n📊 BASIC METRICS")
print(f"Total Trades: {stats['basic']['total_trades']}")
print(f"Win Rate: {stats['basic']['win_rate']:.1f}%")
print(f"Profit Factor: {stats['basic']['profit_factor']:.2f}")

print(f"\n📈 RISK-ADJUSTED RETURNS")
print(f"Sharpe Ratio: {stats['risk_adjusted']['sharpe_ratio']:.2f}")
print(f"Sortino Ratio: {stats['risk_adjusted']['sortino_ratio']:.2f}")
print(f"Calmar Ratio: {stats['risk_adjusted']['calmar_ratio']:.2f}")

print(f"\n⚠️ DRAWDOWN ANALYSIS")
print(f"Max Drawdown: {stats['drawdown']['max_drawdown_pct']:.2f}%")
print(f"Recovery Time: {stats['drawdown']['recovery_time_days']} days")

print(f"\n🎯 R-MULTIPLE ANALYSIS")
print(f"Average R: {stats['r_multiples']['avg_r_multiple']:.2f}")
print(f"Median R: {stats['r_multiples']['median_r_multiple']:.2f}")
print(f"Best Trade: {stats['r_multiples']['best_r_multiple']:.2f}R")
print(f"Worst Trade: {stats['r_multiples']['worst_r_multiple']:.2f}R")

print(f"\n🔄 MONTE CARLO SIMULATION")
print(f"Expected Outcome (100 trades): ${stats['monte_carlo']['mean_outcome']:.2f}")
print(f"95% Best Case: ${stats['monte_carlo']['best_case_95']:.2f}")
print(f"5% Worst Case: ${stats['monte_carlo']['worst_case_5']:.2f}")
print(f"Probability of Profit: {stats['monte_carlo']['probability_profitable']:.1f}%")

print(f"\n⚠️ RISK OF RUIN")
print(f"Probability of 30% Drawdown: {stats['risk_of_ruin']:.2f}%")
```

### 2. Pattern Recognition (`scripts/pattern_recognition.py`)

Automatically detects candlestick patterns:

**Patterns Detected:**
- **Reversal Patterns**: Hammer, Inverted Hammer, Shooting Star, Hanging Man
- **Engulfing Patterns**: Bullish/Bearish Engulfing
- **Star Patterns**: Morning Star, Evening Star
- **Continuation**: Three White Soldiers, Three Black Crows
- **Other**: Doji, Piercing Line, Dark Cloud Cover

**When to Use:**
```
"Detect patterns in EURUSD"
"Are there any bullish patterns on GBPJPY?"
"Scan for reversal patterns"
"What candlestick patterns formed today?"
```

**Implementation:**
```python
import sys
sys.path.append('C:/Users/luces/Downloads/trading-skills/scripts')
from pattern_recognition import CandlestickPattern, analyze_candles_for_symbol

# Get candle data from MetaTrader
candles = metatrader.get_candles_latest(
    symbol_name='EURUSD',
    timeframe='H1',
    count=50
)

# Convert to DataFrame
import pandas as pd
df = pd.DataFrame(candles)
df.columns = ['time', 'open', 'high', 'low', 'close', 'volume', 'spread']

# Detect patterns
detector = CandlestickPattern(df[['open', 'high', 'low', 'close']])
patterns = detector.detect_all_patterns()

# Get summary
summary = detector.get_pattern_summary(last_n=20)

# Present results
print("=== CANDLESTICK PATTERN ANALYSIS: EURUSD ===")

if summary['bullish']:
    print("\n🟢 BULLISH PATTERNS DETECTED:")
    for pattern in summary['bullish']:
        print(f"  ✓ {pattern}")

if summary['bearish']:
    print("\n🔴 BEARISH PATTERNS DETECTED:")
    for pattern in summary['bearish']:
        print(f"  ✓ {pattern}")

if summary['neutral']:
    print("\n⚪ NEUTRAL PATTERNS (INDECISION):")
    for pattern in summary['neutral']:
        print(f"  ✓ {pattern}")

# Provide trading implications
if len(summary['bullish']) > len(summary['bearish']):
    print("\n💡 IMPLICATION: Bullish patterns dominate - consider long positions")
elif len(summary['bearish']) > len(summary['bullish']):
    print("\n💡 IMPLICATION: Bearish patterns dominate - consider short positions")
else:
    print("\n💡 IMPLICATION: Mixed signals - wait for clearer pattern confirmation")
```

### 3. Correlation Analysis (`scripts/correlation_analysis.py`)

Analyzes relationships between currency pairs:

**Key Functions:**
- `calculate_correlation_matrix()`: Full correlation matrix
- `find_highly_correlated_pairs()`: Find strongly related pairs
- `analyze_portfolio_correlation()`: Check portfolio concentration
- `suggest_diversification()`: Recommend uncorrelated pairs
- `calculate_rolling_correlation()`: Time-varying correlations

**When to Use:**
```
"Are EURUSD and GBPUSD correlated?"
"Analyze correlation in my portfolio"
"Suggest pairs for diversification"
"What pairs move together?"
"Check my portfolio concentration risk"
```

**Implementation:**
```python
import sys
sys.path.append('C:/Users/luces/Downloads/trading-skills/scripts')
from correlation_analysis import (
    calculate_correlation_matrix,
    find_highly_correlated_pairs,
    analyze_portfolio_correlation,
    suggest_diversification
)

# Get price data for multiple symbols
symbols = ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'USDCAD']
prices_dict = {}

import pandas as pd
for symbol in symbols:
    candles = metatrader.get_candles_latest(
        symbol_name=symbol,
        timeframe='D1',
        count=100
    )
    df = pd.DataFrame(candles)
    prices_dict[symbol] = df['close']

# Calculate correlation matrix
corr_matrix = calculate_correlation_matrix(prices_dict)

# Find highly correlated pairs
high_corr_pairs = find_highly_correlated_pairs(corr_matrix, threshold=0.7)

# Analyze current portfolio
positions = metatrader.get_all_positions()
position_dict = {pos['symbol']: pos['volume'] for pos in positions}

portfolio_analysis = analyze_portfolio_correlation(position_dict, corr_matrix)

# Present results
print("=== CURRENCY CORRELATION ANALYSIS ===")

print("\n📊 CORRELATION MATRIX:")
print(corr_matrix.round(2))

print("\n🔗 HIGHLY CORRELATED PAIRS:")
for sym1, sym2, corr in high_corr_pairs:
    direction = "Positive" if corr > 0 else "Negative"
    strength = "Strong" if abs(corr) > 0.7 else "Moderate"
    print(f"  {sym1} ↔ {sym2}: {corr:.3f} ({strength} {direction})")

print(f"\n⚠️ PORTFOLIO CORRELATION RISK: {portfolio_analysis['risk_level']}")
print(f"Average Correlation: {portfolio_analysis['avg_correlation']:.2f}")
print(f"{portfolio_analysis['message']}")

if portfolio_analysis['risk_level'] == 'HIGH':
    print("\n💡 DIVERSIFICATION SUGGESTIONS:")
    suggestions = suggest_diversification(
        list(position_dict.keys()),
        corr_matrix,
        min_correlation=0.3
    )
    for sug in suggestions[:3]:
        print(f"  • {sug['symbol']}: {sug['reason']}")
```

## Advanced Workflows

### Workflow 1: Complete Strategy Validation

```
User: "Validate my trading strategy comprehensively"

Claude:
1. Get historical trades (last 3 months)
2. Run advanced_statistics.calculate_all_statistics()
3. Calculate:
   - Sharpe & Sortino ratios
   - Maximum drawdown
   - Win/loss streaks
   - R-multiples
   - Risk of ruin
   - Monte Carlo simulation
4. Present comprehensive report with:
   - Risk-adjusted performance
   - Probability of future success
   - Weaknesses to address
   - Recommendations
```

### Workflow 2: Entry Confirmation with Patterns

```
User: "I want to buy EURUSD at 1.0850. Confirm with pattern analysis."

Claude:
1. Get last 50 H1 candles
2. Run pattern_recognition.detect_all_patterns()
3. Check for:
   - Bullish reversal patterns
   - Support at key levels
   - Confirmation from multiple patterns
4. Provide verdict:
   - Strong confirmation: 3+ bullish patterns
   - Moderate: 1-2 patterns
   - Weak: No clear patterns
5. Calculate probability based on pattern strength
```

### Workflow 3: Portfolio Optimization

```
User: "Optimize my current portfolio for better diversification"

Claude:
1. Get all open positions
2. Get price history for all symbols
3. Run correlation_analysis.calculate_correlation_matrix()
4. Run analyze_portfolio_correlation()
5. If high correlation detected:
   - Identify clusters of correlated positions
   - Calculate weighted risk exposure
   - Suggest which positions to reduce
   - Recommend uncorrelated alternatives
6. Present optimization plan with expected risk reduction
```

## Scoring and Probability Enhancement

When using this skill with other technical analysis:

### Pattern-Based Probability Boost
```
Base Technical Probability: 65%

+ Bullish Engulfing detected: +10%
+ Hammer at support: +8%
+ No bearish patterns: +5%
= Enhanced Probability: 88%
```

### Risk-Adjusted Confidence
```
Strategy Win Rate: 62%
Sharpe Ratio: 1.8 (Excellent)
Max Drawdown: 8% (Good)
Risk of Ruin: 2% (Low)

→ High confidence in strategy sustainability
→ Recommend continuing with current parameters
```

### Correlation-Adjusted Sizing
```
Want to risk 2% on EURUSD
Already have 2% risk on GBPUSD
Correlation: 0.85 (Very High)

Effective Risk = 2% + (2% × 0.85) = 3.7%

→ Reduce EURUSD position to 1% to maintain 3% total risk
```

## Best Practices

### 1. Statistical Analysis
- Run monthly to track performance degradation
- Compare Sharpe ratio to benchmark (>1.0 is good, >2.0 is excellent)
- Monitor drawdown duration as much as magnitude
- Use Monte Carlo to stress-test strategies

### 2. Pattern Recognition
- Combine with technical indicators for confirmation
- Patterns work best at key support/resistance levels
- Multiple patterns > single pattern
- Wait for pattern completion before acting

### 3. Correlation Analysis
- Update correlation matrix weekly (correlations change)
- Avoid >3 highly correlated positions simultaneously
- Use negative correlations for natural hedging
- Consider correlation in position sizing

## Interpretation Guide

### Sharpe Ratio
- < 1.0: Poor risk-adjusted returns
- 1.0 - 2.0: Good
- 2.0 - 3.0: Very Good
- > 3.0: Excellent (rare in trading)

### Sortino Ratio
- Usually higher than Sharpe (only counts downside)
- > 2.0: Good downside risk management

### Calmar Ratio
- > 1.0: Returns exceed max drawdown
- > 3.0: Excellent

### R-Multiples
- Average > 1.0: Winning more than risking
- Median > Average: Consistent wins
- Best/Worst ratio indicates outliers

### Correlation Strength
- 0.0 - 0.3: Weak (good for diversification)
- 0.3 - 0.7: Moderate
- 0.7 - 1.0: Strong (high concentration risk)
- Negative: Inverse relationship (natural hedge)

## Error Handling

If scripts fail:
1. **Missing Data**: Ensure sufficient candles/trades (min 30)
2. **Import Errors**: Check Python path is correct
3. **Calculation Errors**: Verify data format matches expected schema

## Integration with Other Skills

- **Technical Analysis**: Use patterns to enhance technical signals
- **Risk Management**: Use statistics for position sizing
- **Opportunity Scanner**: Filter by correlation to avoid concentration
- **Backtesting**: Validate with Monte Carlo simulations

---

Remember: Advanced analytics complement, not replace, fundamental analysis and risk management. Always use proper stop losses and position sizing regardless of statistical indicators.
