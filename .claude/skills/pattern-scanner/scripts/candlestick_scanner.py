# -*- coding: utf-8 -*-
"""
Candlestick Pattern Scanner - Core Detection Engine

This module provides the main pattern detection functionality,
integrating with MetaTrader data and technical analysis.
"""

import logging
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime, timezone
import pandas as pd
import numpy as np
from io import StringIO

try:
    from .console_utils import safe_console_output
except ImportError:  # pragma: no cover - standalone execution
    from console_utils import safe_console_output

logger = logging.getLogger("pattern_scanner")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("[pattern-scanner] %(levelname)s: %(message)s"))
    logger.addHandler(handler)
logger.setLevel(logging.INFO)
logger.propagate = False

# Add technical-analysis skill to path
skill_base = Path(__file__).parent.parent.parent / "technical-analysis" / "scripts"
sys.path.insert(0, str(skill_base))

try:
    from indicator_suite import (
        build_indicator_snapshot,
        score_direction
    )
    TECHNICAL_ANALYSIS_AVAILABLE = True
except ImportError:
    TECHNICAL_ANALYSIS_AVAILABLE = False
    safe_console_output("Warning: technical-analysis skill not available, using fallback")
    logger.warning("technical-analysis skill not available; using fallback indicators")

MIN_CANDLES_REQUIRED = 50


def parse_candles_from_csv(csv_data: str) -> pd.DataFrame:
    """Convert CSV string from MetaTrader to DataFrame."""
    df = pd.read_csv(StringIO(csv_data))
    df['time'] = pd.to_datetime(df['time'])
    df = df.sort_values('time', ascending=True).reset_index(drop=True)
    return df


def prepare_candle_frames(
    candles_data: Dict[str, str],
    timeframes: List[str],
    minimum_candles: int = MIN_CANDLES_REQUIRED
) -> Tuple[Dict[str, pd.DataFrame], Dict[str, Dict[str, str]]]:
    """
    Parse raw CSV strings into DataFrames and validate availability/length.

    Returns a tuple with:
        - Parsed DataFrames keyed by timeframe
        - Metadata describing the status for each timeframe
    """
    frames: Dict[str, pd.DataFrame] = {}
    status: Dict[str, Dict[str, str]] = {}

    for tf in timeframes:
        csv_data = candles_data.get(tf)
        if not csv_data:
            logger.warning("Missing candle data for timeframe %s", tf)
            status[tf] = {"status": "missing_data", "detail": "No candles provided"}
            continue

        try:
            df = parse_candles_from_csv(csv_data)
        except Exception as exc:  # pragma: no cover - defensive
            logger.error("Failed to parse candle data for %s timeframe: %s", tf, exc)
            status[tf] = {"status": "parse_error", "detail": str(exc)}
            continue

        total = len(df)
        if total < minimum_candles:
            logger.warning(
                "Insufficient candles for %s timeframe (received %s, expected >= %s)",
                tf,
                total,
                minimum_candles,
            )
            status[tf] = {
                "status": "insufficient_data",
                "detail": f"{total}/{minimum_candles} candles",
            }
            continue
        else:
            status[tf] = {"status": "ok", "detail": f"{total} candles"}

        frames[tf] = df

    return frames, status


def is_bullish(candle: pd.Series) -> bool:
    """Check if candle is bullish (close > open)."""
    return candle['close'] > candle['open']


def is_bearish(candle: pd.Series) -> bool:
    """Check if candle is bearish (close < open)."""
    return candle['close'] < candle['open']


def body_size(candle: pd.Series) -> float:
    """Calculate candle body size."""
    return abs(candle['close'] - candle['open'])


def upper_shadow(candle: pd.Series) -> float:
    """Calculate upper shadow length."""
    return candle['high'] - max(candle['open'], candle['close'])


def lower_shadow(candle: pd.Series) -> float:
    """Calculate lower shadow length."""
    return min(candle['open'], candle['close']) - candle['low']


def candle_range(candle: pd.Series) -> float:
    """Calculate total candle range."""
    r = candle['high'] - candle['low']
    return r if r > 0 else 0.00001  # Avoid division by zero


def detect_bullish_engulfing(df: pd.DataFrame, idx: int) -> Dict[str, Any]:
    """Detect Bullish Engulfing pattern."""
    if idx < 1:
        return None

    prev = df.iloc[idx - 1]
    curr = df.iloc[idx]

    if is_bearish(prev) and is_bullish(curr):
        if curr['close'] > prev['open'] and curr['open'] < prev['close']:
            return {
                'name': 'Bullish Engulfing',
                'type': 'Strong Bullish Reversal',
                'strength': 'Very Strong',
                'reliability': 75,
                'bias': 'Bullish',
                'candle_index': idx,
                'price': curr['close'],
                'time': curr['time']
            }
    return None


def detect_bearish_engulfing(df: pd.DataFrame, idx: int) -> Dict[str, Any]:
    """Detect Bearish Engulfing pattern."""
    if idx < 1:
        return None

    prev = df.iloc[idx - 1]
    curr = df.iloc[idx]

    if is_bullish(prev) and is_bearish(curr):
        if curr['close'] < prev['open'] and curr['open'] > prev['close']:
            return {
                'name': 'Bearish Engulfing',
                'type': 'Strong Bearish Reversal',
                'strength': 'Very Strong',
                'reliability': 75,
                'bias': 'Bearish',
                'candle_index': idx,
                'price': curr['close'],
                'time': curr['time']
            }
    return None


def detect_hammer(df: pd.DataFrame, idx: int) -> Dict[str, Any]:
    """Detect Hammer pattern (bullish reversal at support)."""
    candle = df.iloc[idx]

    body = body_size(candle)
    lower = lower_shadow(candle)
    upper = upper_shadow(candle)
    total_range = candle_range(candle)

    if lower > body * 2 and upper < body * 0.5 and body / total_range < 0.35:
        return {
            'name': 'Hammer',
            'type': 'Bullish Reversal',
            'strength': 'Strong',
            'reliability': 70,
            'bias': 'Bullish',
            'candle_index': idx,
            'price': candle['close'],
            'time': candle['time']
        }
    return None


def detect_shooting_star(df: pd.DataFrame, idx: int) -> Dict[str, Any]:
    """Detect Shooting Star pattern (bearish reversal at resistance)."""
    candle = df.iloc[idx]

    body = body_size(candle)
    lower = lower_shadow(candle)
    upper = upper_shadow(candle)
    total_range = candle_range(candle)

    if upper > body * 2 and lower < body * 0.5 and body / total_range < 0.35:
        return {
            'name': 'Shooting Star',
            'type': 'Bearish Reversal',
            'strength': 'Strong',
            'reliability': 70,
            'bias': 'Bearish',
            'candle_index': idx,
            'price': candle['close'],
            'time': candle['time']
        }
    return None


def detect_doji(df: pd.DataFrame, idx: int) -> Dict[str, Any]:
    """Detect Doji pattern (indecision)."""
    candle = df.iloc[idx]

    body = body_size(candle)
    total_range = candle_range(candle)

    if body / total_range < 0.1:
        return {
            'name': 'Doji',
            'type': 'Indecision/Reversal',
            'strength': 'Medium',
            'reliability': 55,
            'bias': 'Neutral',
            'candle_index': idx,
            'price': candle['close'],
            'time': candle['time']
        }
    return None


def detect_morning_star(df: pd.DataFrame, idx: int) -> Dict[str, Any]:
    """Detect Morning Star pattern (3-candle bullish reversal)."""
    if idx < 2:
        return None

    c1 = df.iloc[idx - 2]  # First candle (bearish)
    c2 = df.iloc[idx - 1]  # Middle candle (small)
    c3 = df.iloc[idx]      # Last candle (bullish)

    body1 = body_size(c1)
    body2 = body_size(c2)

    if is_bearish(c1) and body2 < body1 * 0.4 and is_bullish(c3):
        if c3['close'] > (c1['open'] + c1['close']) / 2:
            return {
                'name': 'Morning Star',
                'type': 'Strong Bullish Reversal',
                'strength': 'Very Strong',
                'reliability': 80,
                'bias': 'Bullish',
                'candle_index': idx,
                'price': c3['close'],
                'time': c3['time']
            }
    return None


def detect_evening_star(df: pd.DataFrame, idx: int) -> Dict[str, Any]:
    """Detect Evening Star pattern (3-candle bearish reversal)."""
    if idx < 2:
        return None

    c1 = df.iloc[idx - 2]  # First candle (bullish)
    c2 = df.iloc[idx - 1]  # Middle candle (small)
    c3 = df.iloc[idx]      # Last candle (bearish)

    body1 = body_size(c1)
    body2 = body_size(c2)

    if is_bullish(c1) and body2 < body1 * 0.4 and is_bearish(c3):
        if c3['close'] < (c1['open'] + c1['close']) / 2:
            return {
                'name': 'Evening Star',
                'type': 'Strong Bearish Reversal',
                'strength': 'Very Strong',
                'reliability': 80,
                'bias': 'Bearish',
                'candle_index': idx,
                'price': c3['close'],
                'time': c3['time']
            }
    return None


def detect_bullish_harami(df: pd.DataFrame, idx: int) -> Dict[str, Any]:
    """Detect Bullish Harami pattern (small bullish inside large bearish)."""
    if idx < 1:
        return None

    prev = df.iloc[idx - 1]
    curr = df.iloc[idx]

    body_prev = body_size(prev)
    body_curr = body_size(curr)

    if is_bearish(prev) and is_bullish(curr) and body_curr < body_prev * 0.7:
        if curr['high'] <= prev['high'] and curr['low'] >= prev['low']:
            return {
                'name': 'Bullish Harami',
                'type': 'Bullish Reversal',
                'strength': 'Medium',
                'reliability': 65,
                'bias': 'Bullish',
                'candle_index': idx,
                'price': curr['close'],
                'time': curr['time']
            }
    return None


def detect_bearish_harami(df: pd.DataFrame, idx: int) -> Dict[str, Any]:
    """Detect Bearish Harami pattern (small bearish inside large bullish)."""
    if idx < 1:
        return None

    prev = df.iloc[idx - 1]
    curr = df.iloc[idx]

    body_prev = body_size(prev)
    body_curr = body_size(curr)

    if is_bullish(prev) and is_bearish(curr) and body_curr < body_prev * 0.7:
        if curr['high'] <= prev['high'] and curr['low'] >= prev['low']:
            return {
                'name': 'Bearish Harami',
                'type': 'Bearish Reversal',
                'strength': 'Medium',
                'reliability': 65,
                'bias': 'Bearish',
                'candle_index': idx,
                'price': curr['close'],
                'time': curr['time']
            }
    return None


def detect_three_white_soldiers(df: pd.DataFrame, idx: int) -> Dict[str, Any]:
    """Detect Three White Soldiers pattern (strong bullish continuation)."""
    if idx < 2:
        return None

    c1 = df.iloc[idx - 2]
    c2 = df.iloc[idx - 1]
    c3 = df.iloc[idx]

    if is_bullish(c1) and is_bullish(c2) and is_bullish(c3):
        if c2['close'] > c1['close'] and c3['close'] > c2['close']:
            if body_size(c3) > candle_range(c3) * 0.6:
                return {
                    'name': 'Three White Soldiers',
                    'type': 'Strong Bullish Continuation',
                    'strength': 'Very Strong',
                    'reliability': 80,
                    'bias': 'Bullish',
                    'candle_index': idx,
                    'price': c3['close'],
                    'time': c3['time']
                }
    return None


def detect_three_black_crows(df: pd.DataFrame, idx: int) -> Dict[str, Any]:
    """Detect Three Black Crows pattern (strong bearish continuation)."""
    if idx < 2:
        return None

    c1 = df.iloc[idx - 2]
    c2 = df.iloc[idx - 1]
    c3 = df.iloc[idx]

    if is_bearish(c1) and is_bearish(c2) and is_bearish(c3):
        if c2['close'] < c1['close'] and c3['close'] < c2['close']:
            if body_size(c3) > candle_range(c3) * 0.6:
                return {
                    'name': 'Three Black Crows',
                    'type': 'Strong Bearish Continuation',
                    'strength': 'Very Strong',
                    'reliability': 80,
                    'bias': 'Bearish',
                    'candle_index': idx,
                    'price': c3['close'],
                    'time': c3['time']
                }
    return None


def detect_spinning_top(df: pd.DataFrame, idx: int) -> Dict[str, Any]:
    """Detect Spinning Top pattern (consolidation)."""
    candle = df.iloc[idx]

    body = body_size(candle)
    upper = upper_shadow(candle)
    lower = lower_shadow(candle)
    total_range = candle_range(candle)

    if 0.1 < body / total_range < 0.3 and upper > body * 0.5 and lower > body * 0.5:
        return {
            'name': 'Spinning Top',
            'type': 'Consolidation/Indecision',
            'strength': 'Weak',
            'reliability': 50,
            'bias': 'Neutral',
            'candle_index': idx,
            'price': candle['close'],
            'time': candle['time']
        }
    return None


def detect_all_patterns(df: pd.DataFrame, lookback: int = 5) -> List[Dict[str, Any]]:
    """
    Detect all candlestick patterns in recent candles.

    Args:
        df: DataFrame with OHLC data
        lookback: Number of recent candles to check

    Returns:
        List of detected patterns
    """
    patterns = []
    start_idx = max(0, len(df) - lookback)

    detection_functions = [
        detect_bullish_engulfing,
        detect_bearish_engulfing,
        detect_hammer,
        detect_shooting_star,
        detect_doji,
        detect_morning_star,
        detect_evening_star,
        detect_bullish_harami,
        detect_bearish_harami,
        detect_three_white_soldiers,
        detect_three_black_crows,
        detect_spinning_top
    ]

    for idx in range(start_idx, len(df)):
        for detect_func in detection_functions:
            pattern = detect_func(df, idx)
            if pattern:
                patterns.append(pattern)

    return patterns


def identify_support_resistance(df: pd.DataFrame, lookback: int = 50) -> Dict[str, List[float]]:
    """
    Identify key support and resistance levels from swing highs/lows.

    Args:
        df: DataFrame with OHLC data
        lookback: Number of candles to analyze

    Returns:
        Dictionary with support and resistance levels
    """
    if len(df) < lookback:
        lookback = len(df)

    recent_df = df.tail(lookback)

    # Find swing highs (local maxima)
    highs = []
    for i in range(1, len(recent_df) - 1):
        if recent_df.iloc[i]['high'] > recent_df.iloc[i-1]['high'] and \
           recent_df.iloc[i]['high'] > recent_df.iloc[i+1]['high']:
            highs.append(recent_df.iloc[i]['high'])

    # Find swing lows (local minima)
    lows = []
    for i in range(1, len(recent_df) - 1):
        if recent_df.iloc[i]['low'] < recent_df.iloc[i-1]['low'] and \
           recent_df.iloc[i]['low'] < recent_df.iloc[i+1]['low']:
            lows.append(recent_df.iloc[i]['low'])

    # Get top 3 resistance and support levels
    resistance_levels = sorted(set(highs), reverse=True)[:3]
    support_levels = sorted(set(lows))[:3]

    return {
        'resistance': resistance_levels,
        'support': support_levels,
        'pivot': (recent_df.iloc[-1]['high'] + recent_df.iloc[-1]['low'] + recent_df.iloc[-1]['close']) / 3
    }


def detect_patterns_all_timeframes(
    candle_frames: Dict[str, pd.DataFrame],
    timeframes: List[str] = None,
    lookback: int = 10
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Detect patterns across multiple timeframes.

    Args:
        candle_frames: Dictionary mapping timeframe to pre-parsed candle DataFrames
        timeframes: List of timeframes to analyze
        lookback: Number of recent candles to check per timeframe

    Returns:
        Dictionary mapping timeframe to list of detected patterns
    """
    all_patterns: Dict[str, List[Dict[str, Any]]] = {}
    timeframes = timeframes or list(candle_frames.keys())

    for tf in timeframes:
        df = candle_frames.get(tf)
        if df is None or df.empty:
            all_patterns[tf] = []
            continue

        effective_lookback = min(lookback, len(df))
        patterns = detect_all_patterns(df, lookback=effective_lookback)
        all_patterns[tf] = patterns

    return all_patterns


def scan_symbol_for_patterns(
    symbol: str,
    candles_data: Dict[str, str],
    current_price: float,
    timeframes: List[str] = ['M15', 'H1', 'H4', 'D1']
) -> Dict[str, Any]:
    """
    Complete pattern scan for a symbol.

    Args:
        symbol: Trading symbol (e.g., "EURUSD")
        candles_data: Dictionary mapping timeframe to CSV candle data
        current_price: Current market price
        timeframes: List of timeframes to analyze

    Returns:
        Complete scan results including patterns, indicators, and levels.
    """
    candle_frames, timeframe_status = prepare_candle_frames(candles_data, timeframes)

    if not candle_frames:
        logger.error("No valid candle data was provided for symbol %s", symbol)

    patterns_by_tf = detect_patterns_all_timeframes(candle_frames, timeframes=timeframes)

    technical_snapshots: Dict[str, Any] = {}
    if TECHNICAL_ANALYSIS_AVAILABLE:
        for tf in timeframes:
            df = candle_frames.get(tf)
            if df is None or df.empty:
                continue
            try:
                snapshot = build_indicator_snapshot(df)
                scores = score_direction(snapshot)
                technical_snapshots[tf] = {
                    'snapshot': snapshot.__dict__,
                    'scores': scores
                }
            except Exception as exc:  # pragma: no cover - defensive
                logger.error("Failed to compute indicators for %s timeframe: %s", tf, exc)
                timeframe_status.setdefault(tf, {"status": "indicator_error", "detail": str(exc)})
                technical_snapshots[tf] = None
    else:
        logger.info("technical-analysis integration disabled; skipping indicator snapshots")

    levels_by_tf: Dict[str, Dict[str, Any]] = {}
    for tf in timeframes:
        df = candle_frames.get(tf)
        if df is None or df.empty:
            continue
        try:
            levels_by_tf[tf] = identify_support_resistance(df)
        except Exception as exc:  # pragma: no cover - defensive
            logger.error("Failed to derive support/resistance for %s timeframe: %s", tf, exc)
            levels_by_tf[tf] = {'resistance': [], 'support': [], 'pivot': current_price}
            timeframe_status.setdefault(tf, {"status": "levels_error", "detail": str(exc)})

    bullish_count = sum(
        1 for tf_patterns in patterns_by_tf.values()
        for p in tf_patterns if p['bias'] == 'Bullish'
    )
    bearish_count = sum(
        1 for tf_patterns in patterns_by_tf.values()
        for p in tf_patterns if p['bias'] == 'Bearish'
    )
    neutral_count = sum(
        1 for tf_patterns in patterns_by_tf.values()
        for p in tf_patterns if p['bias'] == 'Neutral'
    )

    if bullish_count > bearish_count:
        overall_bias = 'Bullish'
    elif bearish_count > bullish_count:
        overall_bias = 'Bearish'
    else:
        overall_bias = 'Neutral'

    serialized_candles: Dict[str, List[Dict[str, Any]]] = {}
    for tf, df in candle_frames.items():
        if df is None or df.empty:
            continue
        trimmed = df.tail(200)
        candles_payload = []
        for _, row in trimmed.iterrows():
            time_value = row['time'] if isinstance(row['time'], datetime) else pd.to_datetime(row['time'])
            candles_payload.append({
                'time': time_value.isoformat(),
                'open': float(row['open']),
                'high': float(row['high']),
                'low': float(row['low']),
                'close': float(row['close'])
            })
        serialized_candles[tf] = candles_payload

    return {
        'symbol': symbol,
        'current_price': current_price,
        'scan_time': datetime.now(timezone.utc).isoformat(),
        'timeframes': timeframes,
        'patterns_by_timeframe': patterns_by_tf,
        'technical_snapshots': technical_snapshots,
        'support_resistance': levels_by_tf,
        'timeframe_status': timeframe_status,
        'candles': serialized_candles,
        'pattern_counts': {
            'bullish': bullish_count,
            'bearish': bearish_count,
            'neutral': neutral_count,
            'total': bullish_count + bearish_count + neutral_count
        },
        'overall_bias': overall_bias
    }


if __name__ == "__main__":
    # Simple test
    safe_console_output("Candlestick Scanner Module Loaded Successfully")
    safe_console_output(f"Technical Analysis Integration: {TECHNICAL_ANALYSIS_AVAILABLE}")
