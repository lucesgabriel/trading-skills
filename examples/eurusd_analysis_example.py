"""
EURUSD Candlestick Pattern Analysis
Comprehensive technical analysis with pattern recognition
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
from io import StringIO

# Add technical-analysis scripts to path
skill_path = Path(r"D:\Programing Language html css js php DB\28102025\.claude\skills\technical-analysis\scripts")
sys.path.insert(0, str(skill_path))

from indicator_suite import generate_snapshot_from_candles

# Raw candle data from MetaTrader
M15_DATA = """,time,open,high,low,close,tick_volume,spread,real_volume
249,2025-10-29 06:00:00+00:00,1.16464,1.16468,1.16444,1.16448,644,0,0
248,2025-10-29 05:45:00+00:00,1.16433,1.16466,1.16433,1.16462,852,0,0
247,2025-10-29 05:30:00+00:00,1.16432,1.16443,1.16417,1.16433,796,0,0
246,2025-10-29 05:15:00+00:00,1.16464,1.16465,1.1643,1.16432,769,0,0
245,2025-10-29 05:00:00+00:00,1.16475,1.1648100000000001,1.16451,1.16464,885,0,0
244,2025-10-29 04:45:00+00:00,1.16472,1.16496,1.16471,1.16474,1253,0,0
243,2025-10-29 04:30:00+00:00,1.16502,1.16511,1.16462,1.16472,1733,0,0
242,2025-10-29 04:15:00+00:00,1.16531,1.16553,1.1649,1.16502,1377,0,0
241,2025-10-29 04:00:00+00:00,1.16545,1.16561,1.1652,1.16533,1248,0,0
240,2025-10-29 03:45:00+00:00,1.16559,1.166,1.16533,1.16545,2269,0,0
239,2025-10-29 03:30:00+00:00,1.16571,1.166,1.16531,1.16559,1893,0,0
238,2025-10-29 03:15:00+00:00,1.16571,1.16591,1.16541,1.16572,1859,0,0
237,2025-10-29 03:00:00+00:00,1.16572,1.16609,1.16561,1.1656900000000001,1839,0,0"""

H1_DATA = """,time,open,high,low,close,tick_volume,spread,real_volume
249,2025-10-29 06:00:00+00:00,1.16464,1.16468,1.16444,1.16448,644,0,0
248,2025-10-29 05:00:00+00:00,1.16475,1.1648100000000001,1.16417,1.16462,3302,0,0
247,2025-10-29 04:00:00+00:00,1.16545,1.16561,1.16462,1.16474,5611,0,0
246,2025-10-29 03:00:00+00:00,1.16572,1.16609,1.16531,1.16545,7860,0,0
245,2025-10-29 02:00:00+00:00,1.16505,1.16574,1.16486,1.16572,1888,0,0
244,2025-10-29 01:00:00+00:00,1.16511,1.16544,1.16498,1.16505,2205,0,0
243,2025-10-29 00:00:00+00:00,1.16501,1.16529,1.16501,1.16512,1082,12,0
242,2025-10-28 23:00:00+00:00,1.16524,1.16573,1.1651,1.16523,2744,0,0
241,2025-10-28 22:00:00+00:00,1.16621,1.16653,1.16519,1.16524,4290,0,0
240,2025-10-28 21:00:00+00:00,1.16633,1.16638,1.16561,1.1662,4427,0,0"""

H4_DATA = """,time,open,high,low,close,tick_volume,spread,real_volume
249,2025-10-29 04:00:00+00:00,1.16545,1.16561,1.16417,1.16448,9557,0,0
248,2025-10-29 00:00:00+00:00,1.16501,1.16609,1.16486,1.16545,13035,0,0
247,2025-10-28 20:00:00+00:00,1.16681,1.16689,1.1651,1.16523,18671,0,0
246,2025-10-28 16:00:00+00:00,1.16402,1.1668,1.16253,1.1668,39645,0,0
245,2025-10-28 12:00:00+00:00,1.16522,1.16651,1.16351,1.16402,30769,0,0
244,2025-10-28 08:00:00+00:00,1.16659,1.1668,1.1648399999999999,1.16525,26643,0,0
243,2025-10-28 04:00:00+00:00,1.16556,1.16678,1.16539,1.16659,15544,0,0
242,2025-10-28 00:00:00+00:00,1.16443,1.16588,1.16439,1.16556,10305,0,0"""


def parse_csv_data(csv_string):
    """Parse CSV string into list of dicts for indicator suite."""
    df = pd.read_csv(StringIO(csv_string))
    return df.to_dict('records')


def identify_candlestick_patterns(df):
    """
    Identify major candlestick patterns in the most recent candles.
    Returns list of pattern names found.
    """
    patterns = []

    if len(df) < 3:
        return patterns

    # Get last 3 candles for pattern analysis
    c0 = df.iloc[-1]  # Current candle
    c1 = df.iloc[-2]  # Previous candle
    c2 = df.iloc[-3]  # 2 candles ago

    # Calculate candle properties
    def body_size(candle):
        return abs(candle['close'] - candle['open'])

    def upper_shadow(candle):
        return candle['high'] - max(candle['open'], candle['close'])

    def lower_shadow(candle):
        return min(candle['open'], candle['close']) - candle['low']

    def is_bullish(candle):
        return candle['close'] > candle['open']

    def is_bearish(candle):
        return candle['close'] < candle['open']

    def candle_range(candle):
        return candle['high'] - candle['low']

    # DOJI - Open and close are very close
    if body_size(c0) / candle_range(c0) < 0.1 if candle_range(c0) > 0 else False:
        patterns.append("Doji (Indecision)")

    # HAMMER - Small body at top, long lower shadow
    body = body_size(c0)
    lower = lower_shadow(c0)
    upper = upper_shadow(c0)
    total_range = candle_range(c0)

    if total_range > 0:
        if lower > body * 2 and upper < body * 0.3 and body / total_range < 0.3:
            patterns.append("Hammer (Bullish Reversal)")

        # SHOOTING STAR - Small body at bottom, long upper shadow
        if upper > body * 2 and lower < body * 0.3 and body / total_range < 0.3:
            patterns.append("Shooting Star (Bearish Reversal)")

    # BULLISH ENGULFING
    if is_bearish(c1) and is_bullish(c0):
        if c0['close'] > c1['open'] and c0['open'] < c1['close']:
            patterns.append("Bullish Engulfing (Strong Buy)")

    # BEARISH ENGULFING
    if is_bullish(c1) and is_bearish(c0):
        if c0['close'] < c1['open'] and c0['open'] > c1['close']:
            patterns.append("Bearish Engulfing (Strong Sell)")

    # MORNING STAR (3-candle bullish reversal)
    if is_bearish(c2) and body_size(c1) < body_size(c2) * 0.3 and is_bullish(c0):
        if c0['close'] > (c2['open'] + c2['close']) / 2:
            patterns.append("Morning Star (Bullish Reversal)")

    # EVENING STAR (3-candle bearish reversal)
    if is_bullish(c2) and body_size(c1) < body_size(c2) * 0.3 and is_bearish(c0):
        if c0['close'] < (c2['open'] + c2['close']) / 2:
            patterns.append("Evening Star (Bearish Reversal)")

    # THREE WHITE SOLDIERS (strong bullish)
    if len(df) >= 3:
        if is_bullish(c2) and is_bullish(c1) and is_bullish(c0):
            if c1['close'] > c2['close'] and c0['close'] > c1['close']:
                if body_size(c0) > candle_range(c0) * 0.6:
                    patterns.append("Three White Soldiers (Strong Bullish)")

    # THREE BLACK CROWS (strong bearish)
    if is_bearish(c2) and is_bearish(c1) and is_bearish(c0):
        if c1['close'] < c2['close'] and c0['close'] < c1['close']:
            if body_size(c0) > candle_range(c0) * 0.6:
                patterns.append("Three Black Crows (Strong Bearish)")

    # SPINNING TOP - Small body with shadows on both sides
    if total_range > 0:
        if body / total_range < 0.25 and upper > body and lower > body:
            patterns.append("Spinning Top (Consolidation)")

    # MARUBOZU - Little to no shadows (strong directional move)
    if is_bullish(c0) and upper < body * 0.1 and lower < body * 0.1:
        patterns.append("Bullish Marubozu (Strong Momentum)")
    if is_bearish(c0) and upper < body * 0.1 and lower < body * 0.1:
        patterns.append("Bearish Marubozu (Strong Momentum)")

    return patterns


def analyze_timeframe(candles_csv, timeframe_name):
    """Analyze a single timeframe with indicators and patterns."""
    candles = parse_csv_data(candles_csv)

    # Get technical indicator snapshot
    snapshot = generate_snapshot_from_candles(candles, timeframe=timeframe_name)

    # Get DataFrame for pattern analysis
    df = pd.read_csv(StringIO(candles_csv))
    patterns = identify_candlestick_patterns(df)

    return snapshot, patterns


def main():
    print("=" * 70)
    print("EURUSD CANDLESTICK PATTERN & TECHNICAL ANALYSIS")
    print("=" * 70)
    print(f"Current Price: 1.16448")
    print(f"Time: 2025-10-29 06:10:12 UTC")
    print()

    # Analyze each timeframe
    timeframes = [
        ("M15", M15_DATA),
        ("H1", H1_DATA),
        ("H4", H4_DATA)
    ]

    all_patterns = {}
    all_snapshots = {}

    for tf_name, tf_data in timeframes:
        snapshot, patterns = analyze_timeframe(tf_data, tf_name)
        all_patterns[tf_name] = patterns
        all_snapshots[tf_name] = snapshot

    # Display patterns found
    print("CANDLESTICK PATTERNS DETECTED")
    print("-" * 70)
    pattern_count = 0
    for tf_name in ["M15", "H1", "H4"]:
        if all_patterns[tf_name]:
            print(f"\n{tf_name} Timeframe:")
            for pattern in all_patterns[tf_name]:
                print(f"  * {pattern}")
                pattern_count += 1
        else:
            print(f"\n{tf_name} Timeframe: No significant patterns")

    if pattern_count == 0:
        print("\n  No major candlestick patterns detected at this time")

    print("\n" + "=" * 70)
    print("MULTI-TIMEFRAME TECHNICAL ANALYSIS")
    print("=" * 70)

    # H4 Analysis (Higher Timeframe - Trend)
    h4 = all_snapshots["H4"]
    print("\nH4 TIMEFRAME (Trend Context)")
    print("-" * 70)
    print(f"Price: {h4['price']:.5f}")
    print(f"Trend Bias: {h4['trend_bias'].upper()}")
    print(f"Volatility: {h4['volatility_regime'].capitalize()}")
    print(f"\nMoving Averages:")
    print(f"  SMA 20:  {h4['sma'][20]:.5f}")
    print(f"  SMA 50:  {h4['sma'][50]:.5f}")
    print(f"  SMA 200: {h4['sma'][200]:.5f}")
    print(f"\nMACD:")
    print(f"  Line:   {h4['macd']['line']:.7f}")
    print(f"  Signal: {h4['macd']['signal']:.7f}")
    print(f"  Histogram: {h4['macd']['histogram']:.7f}")
    print(f"\nRSI: {h4['rsi']:.2f}")
    print(f"Stochastic: %K={h4['stochastic']['k']:.2f}, %D={h4['stochastic']['d']:.2f}")

    # H1 Analysis (Trading Timeframe)
    h1 = all_snapshots["H1"]
    print("\nH1 TIMEFRAME (Trading Signals)")
    print("-" * 70)
    print(f"Price: {h1['price']:.5f}")
    print(f"Trend Bias: {h1['trend_bias'].upper()}")
    print(f"\nBollinger Bands:")
    print(f"  Upper: {h1['bollinger']['upper']:.5f}")
    print(f"  Mid:   {h1['bollinger']['mid']:.5f}")
    print(f"  Lower: {h1['bollinger']['lower']:.5f}")
    print(f"  Position: ", end="")
    if h1['price'] > h1['bollinger']['upper']:
        print("Above upper band (Overbought)")
    elif h1['price'] < h1['bollinger']['lower']:
        print("Below lower band (Oversold)")
    else:
        print("Within bands")

    print(f"\nRSI: {h1['rsi']:.2f}", end=" ")
    if h1['rsi'] > 70:
        print("(Overbought)")
    elif h1['rsi'] < 30:
        print("(Oversold)")
    else:
        print("(Neutral)")

    print(f"ATR: {h1['atr']:.5f} ({h1['atr_percent']:.2f}%)")

    # M15 Analysis (Entry Timing)
    m15 = all_snapshots["M15"]
    print("\nM15 TIMEFRAME (Entry Timing)")
    print("-" * 70)
    print(f"Price: {m15['price']:.5f}")
    print(f"MACD Histogram: {m15['macd']['histogram']:.7f}")
    print(f"Stochastic: %K={m15['stochastic']['k']:.2f}, %D={m15['stochastic']['d']:.2f}")

    # Trading Decision
    print("\n" + "=" * 70)
    print("TRADING OPPORTUNITY ASSESSMENT")
    print("=" * 70)

    # Calculate overall bias
    long_prob = (h4['long_probability'] * 0.5 + h1['long_probability'] * 0.3 + m15['long_probability'] * 0.2)
    short_prob = (h4['short_probability'] * 0.5 + h1['short_probability'] * 0.3 + m15['short_probability'] * 0.2)

    print(f"\nWeighted Probability (H4 50%, H1 30%, M15 20%):")
    print(f"  LONG:  {long_prob:.1f}%")
    print(f"  SHORT: {short_prob:.1f}%")

    # Determine direction
    if long_prob > short_prob and long_prob > 55:
        direction = "LONG (BUY)"
        bias = "BULLISH"
        entry_zone = f"{h1['price'] - h1['atr'] * 0.5:.5f} - {h1['price']:.5f}"
        stop_loss = h1['price'] - (h1['atr'] * 2)
        take_profit_1 = h1['price'] + (h1['atr'] * 2)
        take_profit_2 = h1['price'] + (h1['atr'] * 3)
    elif short_prob > long_prob and short_prob > 55:
        direction = "SHORT (SELL)"
        bias = "BEARISH"
        entry_zone = f"{h1['price']:.5f} - {h1['price'] + h1['atr'] * 0.5:.5f}"
        stop_loss = h1['price'] + (h1['atr'] * 2)
        take_profit_1 = h1['price'] - (h1['atr'] * 2)
        take_profit_2 = h1['price'] - (h1['atr'] * 3)
    else:
        direction = "NO CLEAR SIGNAL"
        bias = "NEUTRAL"

    print(f"\nMarket Bias: {bias}")
    print(f"Recommended Direction: {direction}")

    if direction != "NO CLEAR SIGNAL":
        probability = max(long_prob, short_prob)
        print(f"Success Probability: {probability:.1f}%")
        print(f"\nEntry Zone: {entry_zone}")
        print(f"Stop Loss: {stop_loss:.5f}")
        print(f"Take Profit 1: {take_profit_1:.5f} (2x ATR)")
        print(f"Take Profit 2: {take_profit_2:.5f} (3x ATR)")
        print(f"Risk/Reward: 1:2 to 1:3")

        # Confluence factors
        print(f"\nConfluence Factors:")
        if h4['trend_bias'] == 'bullish' and direction == "LONG (BUY)":
            print("  * H4 uptrend alignment")
        if h4['trend_bias'] == 'bearish' and direction == "SHORT (SELL)":
            print("  * H4 downtrend alignment")
        if h1['macd']['histogram'] > 0 and direction == "LONG (BUY)":
            print("  * MACD bullish momentum")
        if h1['macd']['histogram'] < 0 and direction == "SHORT (SELL)":
            print("  * MACD bearish momentum")
        if h1['rsi'] < 70 and h1['rsi'] > 30:
            print("  * RSI in neutral zone (not overbought/oversold)")
        if pattern_count > 0:
            print(f"  * {pattern_count} candlestick pattern(s) detected")
    else:
        print(f"\nMarket Conditions:")
        print(f"  * Probabilities are too close or below threshold")
        print(f"  * Recommended to wait for clearer signals")
        print(f"  * Consider monitoring for pattern formation")

    print("\n" + "=" * 70)
    print("RISK WARNINGS")
    print("=" * 70)
    print("* Always use proper position sizing (1-2% risk per trade)")
    print("* Place stop loss BEFORE entering the trade")
    print("* Monitor for news events that may cause volatility")
    print("* Patterns provide probability, not certainty")
    print("* Past performance does not guarantee future results")
    print("=" * 70)


if __name__ == "__main__":
    main()
