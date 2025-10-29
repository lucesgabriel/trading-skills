"""
Advanced Statistical Analysis for Trading
Provides deeper insights beyond basic indicators
"""

import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, List, Tuple


def calculate_sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.02) -> float:
    """
    Calculate Sharpe Ratio for a series of returns
    
    Args:
        returns: Series of percentage returns
        risk_free_rate: Annual risk-free rate (default 2%)
    
    Returns:
        Sharpe ratio (annualized)
    """
    excess_returns = returns - (risk_free_rate / 252)  # Daily risk-free rate
    return np.sqrt(252) * excess_returns.mean() / excess_returns.std()


def calculate_sortino_ratio(returns: pd.Series, risk_free_rate: float = 0.02) -> float:
    """
    Calculate Sortino Ratio (like Sharpe but only considers downside volatility)
    
    Args:
        returns: Series of percentage returns
        risk_free_rate: Annual risk-free rate
    
    Returns:
        Sortino ratio (annualized)
    """
    excess_returns = returns - (risk_free_rate / 252)
    downside_returns = excess_returns[excess_returns < 0]
    downside_std = downside_returns.std()
    
    if downside_std == 0:
        return np.inf
    
    return np.sqrt(252) * excess_returns.mean() / downside_std


def calculate_maximum_drawdown(equity_curve: pd.Series) -> Dict[str, float]:
    """
    Calculate maximum drawdown and related metrics
    
    Args:
        equity_curve: Series of cumulative equity/balance
    
    Returns:
        Dictionary with max_drawdown, max_drawdown_pct, recovery_time
    """
    cumulative_max = equity_curve.expanding().max()
    drawdown = equity_curve - cumulative_max
    drawdown_pct = (drawdown / cumulative_max) * 100
    
    max_dd = drawdown.min()
    max_dd_pct = drawdown_pct.min()
    
    # Find recovery time
    max_dd_idx = drawdown.idxmin()
    recovery_idx = equity_curve[equity_curve.index > max_dd_idx]
    recovery_idx = recovery_idx[recovery_idx >= equity_curve.loc[max_dd_idx]].index
    
    if len(recovery_idx) > 0:
        recovery_time = (recovery_idx[0] - max_dd_idx).days
    else:
        recovery_time = None  # Not recovered yet
    
    return {
        'max_drawdown': max_dd,
        'max_drawdown_pct': max_dd_pct,
        'recovery_time_days': recovery_time,
        'drawdown_start': max_dd_idx
    }


def calculate_calmar_ratio(returns: pd.Series, max_drawdown_pct: float) -> float:
    """
    Calculate Calmar Ratio (Annual Return / Max Drawdown)
    
    Args:
        returns: Series of returns
        max_drawdown_pct: Maximum drawdown percentage
    
    Returns:
        Calmar ratio
    """
    annual_return = returns.mean() * 252 * 100  # Annualized percentage
    
    if max_drawdown_pct == 0:
        return np.inf
    
    return annual_return / abs(max_drawdown_pct)


def calculate_win_loss_streaks(trades: pd.DataFrame) -> Dict[str, int]:
    """
    Analyze winning and losing streaks
    
    Args:
        trades: DataFrame with 'profit' column
    
    Returns:
        Dictionary with streak statistics
    """
    wins = (trades['profit'] > 0).astype(int)
    
    # Calculate streaks
    streaks = []
    current_streak = 0
    current_type = None
    
    for win in wins:
        if current_type is None:
            current_type = win
            current_streak = 1
        elif win == current_type:
            current_streak += 1
        else:
            streaks.append((current_type, current_streak))
            current_type = win
            current_streak = 1
    
    if current_streak > 0:
        streaks.append((current_type, current_streak))
    
    win_streaks = [s[1] for s in streaks if s[0] == 1]
    loss_streaks = [s[1] for s in streaks if s[0] == 0]
    
    return {
        'max_win_streak': max(win_streaks) if win_streaks else 0,
        'max_loss_streak': max(loss_streaks) if loss_streaks else 0,
        'avg_win_streak': np.mean(win_streaks) if win_streaks else 0,
        'avg_loss_streak': np.mean(loss_streaks) if loss_streaks else 0
    }


def calculate_r_multiples(trades: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate R-multiple statistics (Profit/Risk ratio per trade)
    
    Args:
        trades: DataFrame with 'profit' and 'risk' columns
    
    Returns:
        Dictionary with R-multiple statistics
    """
    trades['r_multiple'] = trades['profit'] / trades['risk']
    
    return {
        'avg_r_multiple': trades['r_multiple'].mean(),
        'median_r_multiple': trades['r_multiple'].median(),
        'best_r_multiple': trades['r_multiple'].max(),
        'worst_r_multiple': trades['r_multiple'].min(),
        'expectancy': trades['r_multiple'].mean(),  # Same as avg R
        'pct_positive_r': (trades['r_multiple'] > 0).sum() / len(trades) * 100
    }


def calculate_trade_distribution(trades: pd.DataFrame) -> Dict:
    """
    Analyze the distribution of trade results
    
    Args:
        trades: DataFrame with 'profit' column
    
    Returns:
        Dictionary with distribution statistics
    """
    profits = trades['profit']
    
    # Separate wins and losses
    wins = profits[profits > 0]
    losses = profits[profits < 0]
    
    return {
        'mean_win': wins.mean() if len(wins) > 0 else 0,
        'mean_loss': losses.mean() if len(losses) > 0 else 0,
        'median_win': wins.median() if len(wins) > 0 else 0,
        'median_loss': losses.median() if len(losses) > 0 else 0,
        'largest_win': wins.max() if len(wins) > 0 else 0,
        'largest_loss': losses.min() if len(losses) > 0 else 0,
        'std_dev_wins': wins.std() if len(wins) > 0 else 0,
        'std_dev_losses': losses.std() if len(losses) > 0 else 0,
        'skewness': stats.skew(profits),
        'kurtosis': stats.kurtosis(profits)
    }


def calculate_risk_of_ruin(win_rate: float, avg_win: float, avg_loss: float, 
                           risk_per_trade: float = 0.02, target_drawdown: float = 0.30) -> float:
    """
    Calculate risk of ruin (probability of losing a certain % of capital)
    
    Args:
        win_rate: Win rate as decimal (0.60 for 60%)
        avg_win: Average win size (R-multiple)
        avg_loss: Average loss size (R-multiple, should be negative)
        risk_per_trade: Risk per trade as decimal (0.02 for 2%)
        target_drawdown: Target drawdown threshold (0.30 for 30%)
    
    Returns:
        Probability of ruin as percentage
    """
    # Kelly Criterion
    kelly = (win_rate * avg_win + (1 - win_rate) * avg_loss) / avg_win
    
    # If Kelly is negative, risk of ruin is very high
    if kelly <= 0:
        return 100.0
    
    # Simplified risk of ruin calculation
    # This is an approximation
    u = (1 + avg_win) * win_rate + (1 + avg_loss) * (1 - win_rate)
    
    if u <= 1:
        return 100.0
    
    # Number of trades until target drawdown
    n = target_drawdown / risk_per_trade
    
    # Risk of ruin formula
    ror = ((1 - u) / (1 + u)) ** n * 100
    
    return min(ror, 100.0)


def monte_carlo_simulation(trades: pd.DataFrame, num_simulations: int = 1000, 
                           num_trades: int = 100) -> Dict:
    """
    Run Monte Carlo simulation on historical trades
    
    Args:
        trades: DataFrame with 'profit' column
        num_simulations: Number of simulations to run
        num_trades: Number of trades per simulation
    
    Returns:
        Dictionary with simulation results
    """
    results = []
    
    for _ in range(num_simulations):
        # Random sample with replacement
        sample_trades = trades['profit'].sample(n=num_trades, replace=True)
        cumulative_return = sample_trades.sum()
        results.append(cumulative_return)
    
    results = np.array(results)
    
    return {
        'mean_outcome': results.mean(),
        'median_outcome': np.median(results),
        'std_dev': results.std(),
        'best_case_95': np.percentile(results, 95),
        'worst_case_5': np.percentile(results, 5),
        'probability_profitable': (results > 0).sum() / num_simulations * 100,
        'value_at_risk_95': np.percentile(results, 5)
    }


def calculate_all_statistics(trades: pd.DataFrame) -> Dict:
    """
    Calculate comprehensive statistics for a trading history
    
    Args:
        trades: DataFrame with columns: 'profit', 'risk', 'timestamp'
    
    Returns:
        Dictionary with all statistics
    """
    # Calculate returns
    trades = trades.sort_values('timestamp')
    trades['cumulative_profit'] = trades['profit'].cumsum()
    trades['equity'] = 10000 + trades['cumulative_profit']  # Assuming $10k starting
    trades['returns'] = trades['profit'] / trades['equity'].shift(1)
    
    # Win rate
    win_rate = (trades['profit'] > 0).sum() / len(trades)
    
    # Average win/loss
    wins = trades[trades['profit'] > 0]['profit']
    losses = trades[trades['profit'] < 0]['profit']
    avg_win = wins.mean() if len(wins) > 0 else 0
    avg_loss = losses.mean() if len(losses) > 0 else 0
    
    stats = {
        'basic': {
            'total_trades': len(trades),
            'win_rate': win_rate * 100,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'profit_factor': abs(wins.sum() / losses.sum()) if len(losses) > 0 else np.inf
        },
        'risk_adjusted': {
            'sharpe_ratio': calculate_sharpe_ratio(trades['returns'].dropna()),
            'sortino_ratio': calculate_sortino_ratio(trades['returns'].dropna()),
            'calmar_ratio': 0  # Will calculate after drawdown
        },
        'drawdown': calculate_maximum_drawdown(trades['equity']),
        'streaks': calculate_win_loss_streaks(trades),
        'r_multiples': calculate_r_multiples(trades),
        'distribution': calculate_trade_distribution(trades),
        'risk_of_ruin': calculate_risk_of_ruin(win_rate, avg_win, avg_loss),
        'monte_carlo': monte_carlo_simulation(trades)
    }
    
    # Update Calmar ratio
    stats['risk_adjusted']['calmar_ratio'] = calculate_calmar_ratio(
        trades['returns'].dropna(), 
        stats['drawdown']['max_drawdown_pct']
    )
    
    return stats


if __name__ == "__main__":
    # Example usage
    example_trades = pd.DataFrame({
        'timestamp': pd.date_range('2024-01-01', periods=100, freq='D'),
        'profit': np.random.randn(100) * 100,  # Random profits/losses
        'risk': [100] * 100  # Fixed risk per trade
    })
    
    stats = calculate_all_statistics(example_trades)
    
    print("=== COMPREHENSIVE TRADING STATISTICS ===")
    print(f"\nBasic Stats:")
    print(f"  Win Rate: {stats['basic']['win_rate']:.2f}%")
    print(f"  Profit Factor: {stats['basic']['profit_factor']:.2f}")
    
    print(f"\nRisk-Adjusted:")
    print(f"  Sharpe Ratio: {stats['risk_adjusted']['sharpe_ratio']:.2f}")
    print(f"  Sortino Ratio: {stats['risk_adjusted']['sortino_ratio']:.2f}")
    
    print(f"\nDrawdown:")
    print(f"  Max DD: {stats['drawdown']['max_drawdown_pct']:.2f}%")
    
    print(f"\nR-Multiples:")
    print(f"  Average R: {stats['r_multiples']['avg_r_multiple']:.2f}")
