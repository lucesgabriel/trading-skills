"""
Currency Correlation Analysis
Identify correlated and inversely correlated currency pairs
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from itertools import combinations


def calculate_correlation_matrix(prices_dict: Dict[str, pd.Series]) -> pd.DataFrame:
    """
    Calculate correlation matrix for multiple currency pairs
    
    Args:
        prices_dict: Dictionary with symbol names as keys and price Series as values
    
    Returns:
        Correlation matrix DataFrame
    """
    df = pd.DataFrame(prices_dict)
    returns = df.pct_change().dropna()
    correlation_matrix = returns.corr()
    
    return correlation_matrix


def find_highly_correlated_pairs(correlation_matrix: pd.DataFrame, 
                                 threshold: float = 0.7) -> List[Tuple[str, str, float]]:
    """
    Find pairs with high correlation
    
    Args:
        correlation_matrix: Correlation matrix
        threshold: Minimum correlation to consider (default 0.7)
    
    Returns:
        List of tuples (symbol1, symbol2, correlation)
    """
    correlated_pairs = []
    
    for i in range(len(correlation_matrix.columns)):
        for j in range(i+1, len(correlation_matrix.columns)):
            symbol1 = correlation_matrix.columns[i]
            symbol2 = correlation_matrix.columns[j]
            corr = correlation_matrix.iloc[i, j]
            
            if abs(corr) >= threshold:
                correlated_pairs.append((symbol1, symbol2, corr))
    
    # Sort by absolute correlation
    correlated_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
    
    return correlated_pairs


def analyze_portfolio_correlation(positions: Dict[str, float], 
                                  correlation_matrix: pd.DataFrame) -> Dict:
    """
    Analyze correlation risk in current portfolio
    
    Args:
        positions: Dictionary with symbol as key and position size as value
        correlation_matrix: Correlation matrix
    
    Returns:
        Dictionary with correlation analysis
    """
    symbols = list(positions.keys())
    
    if len(symbols) < 2:
        return {
            'risk_level': 'LOW',
            'message': 'Only one position, no correlation risk',
            'correlations': []
        }
    
    correlations = []
    total_correlation = 0
    count = 0
    
    for symbol1, symbol2 in combinations(symbols, 2):
        if symbol1 in correlation_matrix.index and symbol2 in correlation_matrix.columns:
            corr = correlation_matrix.loc[symbol1, symbol2]
            weight1 = abs(positions[symbol1])
            weight2 = abs(positions[symbol2])
            weighted_corr = corr * weight1 * weight2
            
            correlations.append({
                'pair': f"{symbol1} - {symbol2}",
                'correlation': corr,
                'weighted_correlation': weighted_corr,
                'same_direction': (positions[symbol1] > 0) == (positions[symbol2] > 0)
            })
            
            total_correlation += abs(weighted_corr)
            count += 1
    
    avg_correlation = total_correlation / count if count > 0 else 0
    
    # Determine risk level
    if avg_correlation > 0.7:
        risk_level = 'HIGH'
        message = 'Portfolio is highly correlated. Consider diversification.'
    elif avg_correlation > 0.4:
        risk_level = 'MEDIUM'
        message = 'Moderate correlation. Some diversification present.'
    else:
        risk_level = 'LOW'
        message = 'Well diversified portfolio with low correlation.'
    
    return {
        'risk_level': risk_level,
        'avg_correlation': avg_correlation,
        'message': message,
        'correlations': correlations
    }


def suggest_diversification(current_symbols: List[str], 
                           correlation_matrix: pd.DataFrame,
                           min_correlation: float = 0.3) -> List[str]:
    """
    Suggest symbols for diversification
    
    Args:
        current_symbols: List of currently held symbols
        correlation_matrix: Full correlation matrix
        min_correlation: Minimum correlation threshold
    
    Returns:
        List of suggested symbols for diversification
    """
    suggestions = []
    
    all_symbols = correlation_matrix.columns.tolist()
    available_symbols = [s for s in all_symbols if s not in current_symbols]
    
    for symbol in available_symbols:
        correlations_with_current = []
        
        for current_symbol in current_symbols:
            if current_symbol in correlation_matrix.index:
                corr = abs(correlation_matrix.loc[current_symbol, symbol])
                correlations_with_current.append(corr)
        
        if correlations_with_current:
            avg_corr = np.mean(correlations_with_current)
            
            if avg_corr < min_correlation:
                suggestions.append({
                    'symbol': symbol,
                    'avg_correlation': avg_corr,
                    'reason': f'Low correlation ({avg_corr:.2f}) with current positions'
                })
    
    # Sort by lowest correlation
    suggestions.sort(key=lambda x: x['avg_correlation'])
    
    return suggestions[:5]  # Top 5 suggestions


def calculate_rolling_correlation(symbol1_prices: pd.Series, 
                                  symbol2_prices: pd.Series,
                                  window: int = 20) -> pd.Series:
    """
    Calculate rolling correlation between two symbols
    
    Args:
        symbol1_prices: Price series for symbol 1
        symbol2_prices: Price series for symbol 2
        window: Rolling window size
    
    Returns:
        Rolling correlation series
    """
    returns1 = symbol1_prices.pct_change()
    returns2 = symbol2_prices.pct_change()
    
    rolling_corr = returns1.rolling(window=window).corr(returns2)
    
    return rolling_corr


def identify_correlation_shifts(rolling_corr: pd.Series, 
                               threshold_change: float = 0.3) -> List[Dict]:
    """
    Identify significant shifts in correlation
    
    Args:
        rolling_corr: Rolling correlation series
        threshold_change: Minimum change to consider significant
    
    Returns:
        List of significant shift events
    """
    shifts = []
    
    # Calculate changes
    corr_changes = rolling_corr.diff().abs()
    
    significant_changes = corr_changes[corr_changes > threshold_change]
    
    for date, change in significant_changes.items():
        current_corr = rolling_corr.loc[date]
        previous_corr = rolling_corr.loc[date] - rolling_corr.diff().loc[date]
        
        shifts.append({
            'date': date,
            'previous_correlation': previous_corr,
            'current_correlation': current_corr,
            'change': change,
            'direction': 'increased' if current_corr > previous_corr else 'decreased'
        })
    
    return shifts


def create_correlation_heatmap_data(correlation_matrix: pd.DataFrame) -> Dict:
    """
    Prepare correlation data for heatmap visualization
    
    Args:
        correlation_matrix: Correlation matrix
    
    Returns:
        Dictionary with heatmap data
    """
    return {
        'symbols': correlation_matrix.columns.tolist(),
        'correlations': correlation_matrix.values.tolist(),
        'interpretation': {
            'strong_positive': 'Correlation > 0.7 (move together)',
            'moderate_positive': 'Correlation 0.3-0.7 (somewhat related)',
            'weak': 'Correlation -0.3 to 0.3 (little relationship)',
            'moderate_negative': 'Correlation -0.7 to -0.3 (somewhat opposite)',
            'strong_negative': 'Correlation < -0.7 (move opposite)'
        }
    }


def analyze_correlation_for_trading(symbol: str, 
                                   other_symbols: List[str],
                                   correlation_matrix: pd.DataFrame) -> Dict:
    """
    Analyze correlations relevant for trading decisions
    
    Args:
        symbol: Primary symbol to analyze
        other_symbols: Other symbols to check correlation with
        correlation_matrix: Correlation matrix
    
    Returns:
        Trading-relevant correlation analysis
    """
    if symbol not in correlation_matrix.index:
        return {'error': f'{symbol} not found in correlation matrix'}
    
    correlations = {}
    
    for other in other_symbols:
        if other in correlation_matrix.columns:
            corr = correlation_matrix.loc[symbol, other]
            correlations[other] = {
                'correlation': corr,
                'strength': 'strong' if abs(corr) > 0.7 else 'moderate' if abs(corr) > 0.3 else 'weak',
                'direction': 'positive' if corr > 0 else 'negative',
                'trading_implication': get_trading_implication(corr)
            }
    
    return {
        'symbol': symbol,
        'correlations': correlations,
        'strongest_positive': max(correlations.items(), key=lambda x: x[1]['correlation']) if correlations else None,
        'strongest_negative': min(correlations.items(), key=lambda x: x[1]['correlation']) if correlations else None
    }


def get_trading_implication(correlation: float) -> str:
    """
    Get trading implication based on correlation value
    
    Args:
        correlation: Correlation coefficient
    
    Returns:
        Trading implication string
    """
    if correlation > 0.7:
        return "Highly correlated - avoid multiple long positions to reduce concentration risk"
    elif correlation > 0.3:
        return "Moderately correlated - positions will somewhat move together"
    elif correlation > -0.3:
        return "Low correlation - good for diversification"
    elif correlation > -0.7:
        return "Moderately inversely correlated - can hedge with opposite positions"
    else:
        return "Highly inversely correlated - natural hedge, moves opposite"


if __name__ == "__main__":
    # Example usage
    dates = pd.date_range('2024-01-01', periods=100, freq='D')
    
    # Simulate price data
    np.random.seed(42)
    prices_dict = {
        'EURUSD': pd.Series(1.08 + np.cumsum(np.random.randn(100) * 0.001), index=dates),
        'GBPUSD': pd.Series(1.25 + np.cumsum(np.random.randn(100) * 0.001), index=dates),
        'USDJPY': pd.Series(145 + np.cumsum(np.random.randn(100) * 0.1), index=dates),
    }
    
    # Calculate correlations
    corr_matrix = calculate_correlation_matrix(prices_dict)
    
    print("=== CURRENCY CORRELATION ANALYSIS ===")
    print("\nCorrelation Matrix:")
    print(corr_matrix)
    
    print("\nHighly Correlated Pairs:")
    pairs = find_highly_correlated_pairs(corr_matrix, threshold=0.5)
    for symbol1, symbol2, corr in pairs:
        print(f"  {symbol1} - {symbol2}: {corr:.3f}")
