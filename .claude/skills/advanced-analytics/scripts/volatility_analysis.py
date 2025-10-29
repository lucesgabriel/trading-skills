"""
Advanced Volatility Analysis
Measure and predict market volatility using multiple methods
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from scipy import stats


def calculate_historical_volatility(prices: pd.Series, window: int = 20) -> pd.Series:
    """
    Calculate historical volatility (standard deviation of returns)
    
    Args:
        prices: Price series
        window: Rolling window for calculation
    
    Returns:
        Annualized historical volatility series
    """
    returns = prices.pct_change()
    volatility = returns.rolling(window=window).std() * np.sqrt(252)
    return volatility


def calculate_parkinson_volatility(high: pd.Series, low: pd.Series, 
                                   window: int = 20) -> pd.Series:
    """
    Parkinson volatility (uses high-low range)
    More efficient than close-to-close volatility
    
    Args:
        high: High prices
        low: Low prices
        window: Rolling window
    
    Returns:
        Annualized Parkinson volatility
    """
    hl_ratio = np.log(high / low)
    parkinson = np.sqrt(hl_ratio ** 2 / (4 * np.log(2)))
    rolling_parkinson = parkinson.rolling(window=window).mean() * np.sqrt(252)
    return rolling_parkinson


def calculate_garman_klass_volatility(open_price: pd.Series, high: pd.Series,
                                     low: pd.Series, close: pd.Series,
                                     window: int = 20) -> pd.Series:
    """
    Garman-Klass volatility estimator
    Uses OHLC data for better estimation
    
    Args:
        open_price: Open prices
        high: High prices
        low: Low prices
        close: Close prices
        window: Rolling window
    
    Returns:
        Annualized Garman-Klass volatility
    """
    log_hl = np.log(high / low)
    log_co = np.log(close / open_price)
    
    rs = 0.5 * log_hl ** 2 - (2 * np.log(2) - 1) * log_co ** 2
    
    rolling_gk = np.sqrt(rs.rolling(window=window).mean() * 252)
    return rolling_gk


def identify_volatility_regime(current_vol: float, 
                               vol_series: pd.Series,
                               threshold: float = 1.5) -> Dict:
    """
    Identify current volatility regime (low, normal, high)
    
    Args:
        current_vol: Current volatility value
        vol_series: Historical volatility series
        threshold: Standard deviations for regime classification
    
    Returns:
        Dictionary with regime information
    """
    mean_vol = vol_series.mean()
    std_vol = vol_series.std()
    
    z_score = (current_vol - mean_vol) / std_vol
    
    if z_score > threshold:
        regime = 'HIGH'
        description = 'Volatility significantly above normal'
        action = 'Consider reducing position sizes and widening stops'
    elif z_score < -threshold:
        regime = 'LOW'
        description = 'Volatility significantly below normal'
        action = 'Volatility expansion likely - prepare for larger moves'
    else:
        regime = 'NORMAL'
        description = 'Volatility within normal range'
        action = 'Standard risk management applies'
    
    return {
        'regime': regime,
        'current_volatility': current_vol,
        'mean_volatility': mean_vol,
        'z_score': z_score,
        'description': description,
        'recommended_action': action,
        'percentile': stats.percentileofscore(vol_series, current_vol)
    }


def calculate_volatility_cone(prices: pd.DataFrame, 
                              windows: List[int] = [5, 10, 20, 30, 60]) -> Dict:
    """
    Calculate volatility cone (realized vol at different horizons)
    
    Args:
        prices: DataFrame with OHLC data
        windows: List of windows to calculate
    
    Returns:
        Dictionary with volatility statistics for each window
    """
    results = {}
    
    for window in windows:
        vol_series = calculate_historical_volatility(prices['close'], window=window)
        
        results[f'{window}d'] = {
            'current': vol_series.iloc[-1],
            'min': vol_series.min(),
            'max': vol_series.max(),
            'mean': vol_series.mean(),
            'median': vol_series.median(),
            'percentile_10': vol_series.quantile(0.10),
            'percentile_25': vol_series.quantile(0.25),
            'percentile_75': vol_series.quantile(0.75),
            'percentile_90': vol_series.quantile(0.90)
        }
    
    return results


def detect_volatility_breakout(volatility: pd.Series, 
                               window: int = 20,
                               std_threshold: float = 2.0) -> pd.Series:
    """
    Detect volatility breakouts (expansion events)
    
    Args:
        volatility: Volatility series
        window: Rolling window for mean/std calculation
        std_threshold: Standard deviations for breakout
    
    Returns:
        Boolean series indicating breakout points
    """
    rolling_mean = volatility.rolling(window=window).mean()
    rolling_std = volatility.rolling(window=window).std()
    
    upper_band = rolling_mean + (std_threshold * rolling_std)
    
    breakouts = volatility > upper_band
    
    return breakouts


def calculate_volatility_skew(options_data: Dict[str, float] = None,
                             returns: pd.Series = None) -> Dict:
    """
    Calculate volatility skew (asymmetry in volatility expectations)
    Can use either options data or return distribution
    
    Args:
        options_data: Dictionary with strike:implied_vol pairs
        returns: Return series if options data not available
    
    Returns:
        Skew analysis
    """
    if options_data:
        # Use options implied volatility
        strikes = sorted(options_data.keys())
        vols = [options_data[k] for k in strikes]
        
        if len(vols) >= 3:
            # Simple skew: (Put IV - Call IV) / ATM IV
            put_vol = vols[0]  # Lowest strike (put)
            call_vol = vols[-1]  # Highest strike (call)
            atm_vol = vols[len(vols)//2]  # Middle (ATM)
            
            skew = (put_vol - call_vol) / atm_vol
        else:
            skew = 0
    else:
        # Use return distribution
        skew = stats.skew(returns.dropna())
    
    if skew > 0:
        interpretation = 'Positive skew: Higher demand for downside protection (bearish sentiment)'
    elif skew < 0:
        interpretation = 'Negative skew: Higher demand for upside calls (bullish sentiment)'
    else:
        interpretation = 'Neutral skew: Balanced volatility expectations'
    
    return {
        'skew_value': skew,
        'interpretation': interpretation,
        'magnitude': 'high' if abs(skew) > 0.5 else 'moderate' if abs(skew) > 0.2 else 'low'
    }


def forecast_volatility_garch(returns: pd.Series, horizon: int = 5) -> Dict:
    """
    Simple GARCH-like volatility forecast
    (Simplified version - for full GARCH use arch library)
    
    Args:
        returns: Return series
        horizon: Forecast horizon in periods
    
    Returns:
        Volatility forecast
    """
    # Calculate realized volatility
    realized_vol = returns.std() * np.sqrt(252)
    
    # Simple exponentially weighted moving average
    ewma_vol = returns.ewm(span=20).std() * np.sqrt(252)
    current_ewma = ewma_vol.iloc[-1]
    
    # Mean reversion forecast
    long_term_vol = returns.std() * np.sqrt(252)
    
    # Blend current and long-term (simple mean reversion)
    reversion_speed = 0.1  # 10% per period
    forecast = []
    
    current = current_ewma
    for i in range(horizon):
        # Mean revert towards long-term
        next_vol = current + reversion_speed * (long_term_vol - current)
        forecast.append(next_vol)
        current = next_vol
    
    return {
        'current_volatility': current_ewma,
        'long_term_volatility': long_term_vol,
        'forecast_horizon': horizon,
        'forecast': forecast,
        'trend': 'increasing' if forecast[-1] > current_ewma else 'decreasing'
    }


def calculate_volatility_adjusted_position_size(base_size: float,
                                               current_vol: float,
                                               target_vol: float) -> float:
    """
    Adjust position size based on volatility
    
    Args:
        base_size: Normal position size
        current_vol: Current market volatility
        target_vol: Target/normal volatility level
    
    Returns:
        Adjusted position size
    """
    # Inverse volatility scaling
    adjustment_factor = target_vol / current_vol
    adjusted_size = base_size * adjustment_factor
    
    # Cap adjustment at reasonable limits
    adjusted_size = max(adjusted_size, base_size * 0.25)  # Min 25% of base
    adjusted_size = min(adjusted_size, base_size * 2.0)   # Max 200% of base
    
    return adjusted_size


def analyze_intraday_volatility_pattern(prices: pd.DataFrame) -> Dict:
    """
    Analyze volatility patterns throughout the trading day
    
    Args:
        prices: DataFrame with datetime index and OHLC data
    
    Returns:
        Intraday volatility pattern analysis
    """
    # Extract hour of day
    prices['hour'] = prices.index.hour
    
    # Calculate hourly returns
    prices['returns'] = prices['close'].pct_change()
    
    # Group by hour and calculate volatility
    hourly_vol = prices.groupby('hour')['returns'].std() * np.sqrt(252)
    
    most_volatile_hour = hourly_vol.idxmax()
    least_volatile_hour = hourly_vol.idxmin()
    
    return {
        'hourly_volatility': hourly_vol.to_dict(),
        'most_volatile_hour': most_volatile_hour,
        'least_volatile_hour': least_volatile_hour,
        'volatility_range': hourly_vol.max() - hourly_vol.min(),
        'recommendation': f"Highest volatility typically occurs at hour {most_volatile_hour}. " \
                         f"Consider tighter stops during this period."
    }


def calculate_comprehensive_volatility_metrics(prices: pd.DataFrame) -> Dict:
    """
    Calculate all volatility metrics in one function
    
    Args:
        prices: DataFrame with OHLC data and datetime index
    
    Returns:
        Comprehensive volatility analysis
    """
    # Calculate different volatility measures
    hist_vol = calculate_historical_volatility(prices['close'])
    parkinson_vol = calculate_parkinson_volatility(prices['high'], prices['low'])
    gk_vol = calculate_garman_klass_volatility(
        prices['open'], prices['high'], prices['low'], prices['close']
    )
    
    # Current values
    current_hist_vol = hist_vol.iloc[-1]
    current_parkinson = parkinson_vol.iloc[-1]
    current_gk = gk_vol.iloc[-1]
    
    # Regime identification
    regime = identify_volatility_regime(current_hist_vol, hist_vol)
    
    # Volatility cone
    cone = calculate_volatility_cone(prices)
    
    # Detect breakouts
    breakouts = detect_volatility_breakout(hist_vol)
    recent_breakout = breakouts.iloc[-5:].any()
    
    # Calculate returns for skew
    returns = prices['close'].pct_change()
    skew = calculate_volatility_skew(returns=returns)
    
    # Forecast
    forecast = forecast_volatility_garch(returns)
    
    return {
        'current_metrics': {
            'historical_volatility': current_hist_vol,
            'parkinson_volatility': current_parkinson,
            'garman_klass_volatility': current_gk,
            'average_of_methods': np.mean([current_hist_vol, current_parkinson, current_gk])
        },
        'regime': regime,
        'volatility_cone': cone,
        'recent_breakout': recent_breakout,
        'skew': skew,
        'forecast': forecast,
        'trading_implications': generate_volatility_trading_implications(
            regime, recent_breakout, forecast
        )
    }


def generate_volatility_trading_implications(regime: Dict, 
                                            recent_breakout: bool,
                                            forecast: Dict) -> List[str]:
    """
    Generate trading implications based on volatility analysis
    
    Args:
        regime: Volatility regime information
        recent_breakout: Whether there was a recent volatility breakout
        forecast: Volatility forecast
    
    Returns:
        List of trading implications
    """
    implications = []
    
    # Regime-based implications
    if regime['regime'] == 'HIGH':
        implications.append("⚠️ High volatility regime: Use wider stops and smaller positions")
        implications.append("💡 Consider short-term strategies - moves can be fast")
    elif regime['regime'] == 'LOW':
        implications.append("⚠️ Low volatility regime: Expansion likely coming")
        implications.append("💡 Prepare for breakouts - tighten stops or wait for expansion")
    
    # Breakout implications
    if recent_breakout:
        implications.append("📢 Recent volatility breakout detected")
        implications.append("💡 Increased risk of large moves - adjust risk management")
    
    # Forecast implications
    if forecast['trend'] == 'increasing':
        implications.append("📈 Volatility forecast: INCREASING")
        implications.append("💡 Gradually reduce position sizes over next few days")
    else:
        implications.append("📉 Volatility forecast: DECREASING")
        implications.append("💡 Conditions may improve for position taking")
    
    return implications


if __name__ == "__main__":
    # Example usage
    dates = pd.date_range('2024-01-01', periods=100, freq='D')
    
    # Simulate OHLC data
    np.random.seed(42)
    base_price = 1.08
    volatility = 0.01
    
    prices = pd.DataFrame({
        'open': base_price + np.random.randn(100) * volatility,
        'high': base_price + abs(np.random.randn(100)) * volatility * 1.5,
        'low': base_price - abs(np.random.randn(100)) * volatility * 1.5,
        'close': base_price + np.random.randn(100) * volatility
    }, index=dates)
    
    # Calculate comprehensive metrics
    metrics = calculate_comprehensive_volatility_metrics(prices)
    
    print("=== COMPREHENSIVE VOLATILITY ANALYSIS ===")
    print(f"\nCurrent Volatility: {metrics['current_metrics']['average_of_methods']:.2%}")
    print(f"Regime: {metrics['regime']['regime']}")
    print(f"Forecast Trend: {metrics['forecast']['trend']}")
    
    print("\n💡 Trading Implications:")
    for implication in metrics['trading_implications']:
        print(f"  {implication}")
