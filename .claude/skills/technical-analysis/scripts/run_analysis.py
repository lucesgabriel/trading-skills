#!/usr/bin/env python3
"""
Main wrapper for technical-analysis skill.

Provides the primary entry point run_technical_analysis() which accepts
MCP data, processes it through indicator_suite.py, and generates a complete
multi-timeframe technical analysis with trading recommendations.
"""

from __future__ import annotations

import sys
from io import StringIO
from pathlib import Path
from typing import Dict, Optional

import pandas as pd

# Import from indicator_suite
from indicator_suite import generate_snapshot_from_candles


def parse_csv_candles(csv_string: str) -> list[Dict]:
    """
    Parse CSV string from MetaTrader MCP to list of candle dicts.

    Args:
        csv_string: CSV format from mcp__metatrader__get_candles_latest

    Returns:
        List of dicts with time, open, high, low, close, volume
    """
    df = pd.read_csv(StringIO(csv_string))

    # Convert to list of dicts
    candles = df.to_dict('records')

    return candles


def calculate_support_resistance(candles: list[Dict], num_levels: int = 3) -> Dict[str, list]:
    """
    Identify key support and resistance levels from recent candles.

    Args:
        candles: List of candle dicts
        num_levels: Number of S/R levels to identify

    Returns:
        Dict with 'support' and 'resistance' lists
    """
    if not candles:
        return {"support": [], "resistance": []}

    df = pd.DataFrame(candles)

    # Get recent highs and lows
    highs = df['high'].nlargest(num_levels * 2).values
    lows = df['low'].nsmallest(num_levels * 2).values

    # Cluster nearby levels
    resistance = []
    for high in highs:
        if not any(abs(high - r) < 0.0010 for r in resistance):
            resistance.append(float(high))
        if len(resistance) >= num_levels:
            break

    support = []
    for low in lows:
        if not any(abs(low - s) < 0.0010 for s in support):
            support.append(float(low))
        if len(support) >= num_levels:
            break

    return {
        "support": sorted(support, reverse=True),
        "resistance": sorted(resistance)
    }


def calculate_multi_timeframe_confluence(snapshots: Dict[str, Dict]) -> Dict:
    """
    Calculate confluence score across multiple timeframes.

    Args:
        snapshots: Dict of {timeframe: snapshot_dict}

    Returns:
        Dict with overall bias, confidence, and recommendation
    """
    if not snapshots:
        return {
            "bias": "NEUTRAL",
            "confidence": 50,
            "long_probability": 50,
            "short_probability": 50
        }

    # Weight by timeframe importance
    weights = {
        "M15": 0.1,
        "H1": 0.2,
        "H4": 0.3,
        "D1": 0.4
    }

    weighted_long = 0
    weighted_short = 0
    total_weight = 0

    for tf, snapshot in snapshots.items():
        if tf in weights:
            weight = weights[tf]
            weighted_long += snapshot.get("long_probability", 50) * weight
            weighted_short += snapshot.get("short_probability", 50) * weight
            total_weight += weight

    if total_weight > 0:
        final_long = weighted_long / total_weight
        final_short = weighted_short / total_weight
    else:
        final_long = 50
        final_short = 50

    # Determine bias
    if final_long > 60:
        bias = "BULLISH"
    elif final_short > 60:
        bias = "BEARISH"
    else:
        bias = "NEUTRAL"

    confidence = max(final_long, final_short)

    return {
        "bias": bias,
        "confidence": round(confidence, 1),
        "long_probability": round(final_long, 1),
        "short_probability": round(final_short, 1)
    }


def format_trading_setup(
    symbol: str,
    current_price: float,
    bias: str,
    atr: float,
    support_levels: list,
    resistance_levels: list
) -> Dict:
    """
    Generate trading setup with entry, SL, TP based on analysis.

    Args:
        symbol: Trading symbol
        current_price: Current market price
        bias: BULLISH, BEARISH, or NEUTRAL
        atr: Average True Range value
        support_levels: List of support prices
        resistance_levels: List of resistance prices

    Returns:
        Dict with entry, stop_loss, take_profit levels
    """
    setup = {
        "symbol": symbol,
        "current_price": current_price,
        "signal": "WAIT"
    }

    if bias == "BULLISH" and support_levels:
        # Long setup
        entry = current_price
        stop_loss = support_levels[0] if support_levels else current_price - (atr * 2)
        take_profit_1 = current_price + (atr * 2)
        take_profit_2 = resistance_levels[0] if resistance_levels else current_price + (atr * 3)

        setup.update({
            "signal": "LONG",
            "entry": round(entry, 5),
            "stop_loss": round(stop_loss, 5),
            "take_profit_1": round(take_profit_1, 5),
            "take_profit_2": round(take_profit_2, 5),
            "risk_pips": int(abs(entry - stop_loss) * 10000),
            "reward_pips_1": int(abs(take_profit_1 - entry) * 10000),
            "reward_pips_2": int(abs(take_profit_2 - entry) * 10000),
            "risk_reward": round((take_profit_2 - entry) / (entry - stop_loss), 2) if entry != stop_loss else 0
        })

    elif bias == "BEARISH" and resistance_levels:
        # Short setup
        entry = current_price
        stop_loss = resistance_levels[0] if resistance_levels else current_price + (atr * 2)
        take_profit_1 = current_price - (atr * 2)
        take_profit_2 = support_levels[0] if support_levels else current_price - (atr * 3)

        setup.update({
            "signal": "SHORT",
            "entry": round(entry, 5),
            "stop_loss": round(stop_loss, 5),
            "take_profit_1": round(take_profit_1, 5),
            "take_profit_2": round(take_profit_2, 5),
            "risk_pips": int(abs(stop_loss - entry) * 10000),
            "reward_pips_1": int(abs(entry - take_profit_1) * 10000),
            "reward_pips_2": int(abs(entry - take_profit_2) * 10000),
            "risk_reward": round((entry - take_profit_2) / (stop_loss - entry), 2) if stop_loss != entry else 0
        })

    return setup


def format_analysis_output(
    symbol: str,
    snapshots: Dict[str, Dict],
    confluence: Dict,
    support_resistance: Dict,
    trading_setup: Dict
) -> str:
    """
    Format complete analysis as readable console output.

    Args:
        symbol: Trading symbol
        snapshots: Dict of timeframe snapshots
        confluence: Multi-timeframe confluence analysis
        support_resistance: S/R levels
        trading_setup: Trading setup recommendation

    Returns:
        Formatted string for console output
    """
    output = []

    # Header
    output.append("=" * 70)
    output.append(f"📊 TECHNICAL ANALYSIS: {symbol}")
    output.append("=" * 70)

    # Current situation
    if "H1" in snapshots:
        h1 = snapshots["H1"]
        output.append(f"\n💹 CURRENT SITUATION")
        output.append(f"Price: {h1['price']:.5f}")
        output.append(f"ATR: {h1['atr']:.5f} ({int(h1['atr'] * 10000)} pips)")
        output.append(f"Volatility: {h1['volatility_regime']}")

    # Multi-timeframe analysis
    output.append(f"\n📈 MULTI-TIMEFRAME ANALYSIS")

    for tf in ["D1", "H4", "H1", "M15"]:
        if tf in snapshots:
            snap = snapshots[tf]
            trend_icon = "↑" if snap.get("trend_bias", 0) > 0 else "↓" if snap.get("trend_bias", 0) < 0 else "→"
            output.append(f"\n{tf}:")
            output.append(f"  Trend: {trend_icon} {snap.get('trend_bias', 'NEUTRAL')}")
            output.append(f"  RSI: {snap['rsi']:.1f}")
            output.append(f"  MACD: {snap['macd']['histogram']:.5f}")
            output.append(f"  Long probability: {snap['long_probability']:.1f}%")
            output.append(f"  Short probability: {snap['short_probability']:.1f}%")

    # Confluence
    output.append(f"\n🎯 CONFLUENCE ANALYSIS")
    output.append(f"Overall Bias: {confluence['bias']}")
    output.append(f"Confidence: {confluence['confidence']:.1f}%")
    output.append(f"Long Probability: {confluence['long_probability']:.1f}%")
    output.append(f"Short Probability: {confluence['short_probability']:.1f}%")

    # Support/Resistance
    output.append(f"\n📍 KEY LEVELS")
    output.append(f"Resistance:")
    for i, level in enumerate(support_resistance["resistance"][:3], 1):
        output.append(f"  R{i}: {level:.5f}")
    output.append(f"Support:")
    for i, level in enumerate(support_resistance["support"][:3], 1):
        output.append(f"  S{i}: {level:.5f}")

    # Trading setup
    output.append(f"\n💡 TRADING RECOMMENDATION")
    output.append(f"Signal: {trading_setup['signal']}")

    if trading_setup['signal'] in ["LONG", "SHORT"]:
        output.append(f"\nSetup:")
        output.append(f"  Entry: {trading_setup['entry']:.5f}")
        output.append(f"  Stop Loss: {trading_setup['stop_loss']:.5f} ({trading_setup['risk_pips']} pips)")
        output.append(f"  Take Profit 1: {trading_setup['take_profit_1']:.5f} ({trading_setup['reward_pips_1']} pips)")
        output.append(f"  Take Profit 2: {trading_setup['take_profit_2']:.5f} ({trading_setup['reward_pips_2']} pips)")
        output.append(f"  Risk:Reward: 1:{trading_setup['risk_reward']}")

        output.append(f"\n📋 EXECUTION:")
        if trading_setup['signal'] == "LONG":
            output.append(f"  • Wait for confirmation or enter at current price")
            output.append(f"  • Place stop loss below support at {trading_setup['stop_loss']:.5f}")
            output.append(f"  • Target TP1 for 50% position, let TP2 run")
        else:
            output.append(f"  • Wait for confirmation or enter at current price")
            output.append(f"  • Place stop loss above resistance at {trading_setup['stop_loss']:.5f}")
            output.append(f"  • Target TP1 for 50% position, let TP2 run")
    else:
        output.append(f"\n⚠️  No clear setup at this moment")
        output.append(f"  • Signals are mixed or weak")
        output.append(f"  • Wait for better confluence")
        output.append(f"  • Monitor key levels for breakouts")

    # Risk warning
    output.append(f"\n⚠️  RISK MANAGEMENT:")
    output.append(f"  • Never risk more than 1-2% of account per trade")
    output.append(f"  • Always use stop loss")
    output.append(f"  • Consider news events and market hours")

    output.append("\n" + "=" * 70)

    return "\n".join(output)


def run_technical_analysis(symbol: str, mcp_data: Dict) -> Dict:
    """
    Main entry point for technical analysis skill.

    Args:
        symbol: Trading symbol (e.g., "EURUSD")
        mcp_data: Dictionary containing:
            - price: dict from mcp__metatrader__get_symbol_price
            - candles_m15: CSV string from mcp__metatrader__get_candles_latest
            - candles_h1: CSV string
            - candles_h4: CSV string
            - candles_d1: CSV string

    Returns:
        Dictionary with:
            - formatted_output: String for console display
            - snapshots: Raw indicator snapshots per timeframe
            - confluence: Multi-timeframe analysis
            - trading_setup: Recommended setup
    """
    # Parse current price
    price_info = mcp_data.get("price", {})
    current_price = price_info.get("bid", 0.0)

    # Process each timeframe
    snapshots = {}
    all_candles = {}

    timeframes = {
        "M15": mcp_data.get("candles_m15"),
        "H1": mcp_data.get("candles_h1"),
        "H4": mcp_data.get("candles_h4"),
        "D1": mcp_data.get("candles_d1")
    }

    for tf, csv_data in timeframes.items():
        if csv_data:
            try:
                candles = parse_csv_candles(csv_data)
                all_candles[tf] = candles
                snapshot = generate_snapshot_from_candles(candles, timeframe=tf)
                snapshots[tf] = snapshot
            except Exception as e:
                print(f"Warning: Could not process {tf} data: {e}", file=sys.stderr)

    # Calculate confluence across timeframes
    confluence = calculate_multi_timeframe_confluence(snapshots)

    # Identify support and resistance (using H1 candles as reference)
    h1_candles = all_candles.get("H1", [])
    support_resistance = calculate_support_resistance(h1_candles)

    # Generate trading setup
    atr = snapshots.get("H1", {}).get("atr", 0.0015)
    trading_setup = format_trading_setup(
        symbol=symbol,
        current_price=current_price,
        bias=confluence["bias"],
        atr=atr,
        support_levels=support_resistance["support"],
        resistance_levels=support_resistance["resistance"]
    )

    # Format output
    formatted_output = format_analysis_output(
        symbol=symbol,
        snapshots=snapshots,
        confluence=confluence,
        support_resistance=support_resistance,
        trading_setup=trading_setup
    )

    return {
        "formatted_output": formatted_output,
        "snapshots": snapshots,
        "confluence": confluence,
        "support_resistance": support_resistance,
        "trading_setup": trading_setup
    }


if __name__ == "__main__":
    print("run_analysis.py: Use this module via import, not direct execution")
    print("Example:")
    print("  from run_analysis import run_technical_analysis")
    print("  result = run_technical_analysis('EURUSD', mcp_data)")
    print("  print(result['formatted_output'])")
