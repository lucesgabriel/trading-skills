"""
Utility helpers for the technical-analysis skill.

Provides reusable functions to convert MetaTrader candle payloads into
DataFrames, calculate core indicators, and derive confluence-driven
probability scores for both long and short scenarios. Designed so the
skill can respond quickly without having to recreate indicator code for
each query.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd


@dataclass
class IndicatorSnapshot:
    """Container with the latest indicator readings plus context windows."""

    price: float
    sma: Dict[int, float]
    ema: Dict[int, float]
    macd_line: float
    macd_signal: float
    macd_histogram: float
    rsi: float
    stochastic_k: float
    stochastic_d: float
    bollinger_mid: float
    bollinger_upper: float
    bollinger_lower: float
    atr: float
    atr_percent: float
    candle_timestamp: pd.Timestamp


def candles_to_dataframe(candles: Iterable[Dict], timeframe: str = "H1") -> pd.DataFrame:
    """
    Convert MetaTrader candle payloads into a pandas DataFrame.

    Args:
        candles: Iterable with dicts containing at least time/open/high/low/close/volume.
        timeframe: Optional timeframe label stored in the resulting DataFrame.

    Returns:
        DataFrame indexed by timestamp with numeric OHLCV columns.
    """
    if not candles:
        raise ValueError("No candle data provided")

    df = pd.DataFrame(list(candles))

    renamed_columns = {
        "time": "timestamp",
        "Time": "timestamp",
        "time_msc": "timestamp",
        "open": "open",
        "Open": "open",
        "high": "high",
        "High": "high",
        "low": "low",
        "Low": "low",
        "close": "close",
        "Close": "close",
        "tick_volume": "volume",
        "volume": "volume",
    }
    df = df.rename(columns={k: v for k, v in renamed_columns.items() if k in df.columns})

    if "timestamp" not in df.columns:
        raise KeyError("Expected a 'time' field in candle payload")

    # MetaTrader often returns timestamps as seconds since epoch or ISO8601 strings.
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", unit="s")
    if df["timestamp"].isna().any():
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    df = df.sort_values("timestamp").set_index("timestamp")
    numeric_cols = ["open", "high", "low", "close", "volume"]

    for column in numeric_cols:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")
        else:
            raise KeyError(f"Missing '{column}' in candle payload")

    df["timeframe"] = timeframe
    df = df.dropna(subset=["open", "high", "low", "close"])
    return df


def _ema(series: pd.Series, span: int) -> pd.Series:
    return series.ewm(span=span, adjust=False).mean()


def calculate_moving_averages(df: pd.DataFrame, periods: Iterable[int] = (10, 20, 50, 100, 200)) -> Tuple[pd.DataFrame, Dict[int, float]]:
    """
    Calculate SMA values for the requested periods.

    Returns:
        Tuple with DataFrame (one column per SMA) and dictionary with latest values.
    """
    sma_data = {}
    for period in periods:
        column = f"sma_{period}"
        df[column] = df["close"].rolling(window=period, min_periods=period).mean()
        sma_data[period] = df[column].iloc[-1]
    return df, sma_data


def calculate_ema(df: pd.DataFrame, periods: Iterable[int]) -> Tuple[pd.DataFrame, Dict[int, float]]:
    ema_data = {}
    for period in periods:
        column = f"ema_{period}"
        df[column] = _ema(df["close"], period)
        ema_data[period] = df[column].iloc[-1]
    return df, ema_data


def calculate_macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[pd.DataFrame, Dict[str, float]]:
    ema_fast = _ema(df["close"], fast)
    ema_slow = _ema(df["close"], slow)
    macd_line = ema_fast - ema_slow
    signal_line = _ema(macd_line, signal)
    histogram = macd_line - signal_line

    df["macd_line"] = macd_line
    df["macd_signal"] = signal_line
    df["macd_histogram"] = histogram

    return df, {
        "macd_line": macd_line.iloc[-1],
        "macd_signal": signal_line.iloc[-1],
        "macd_histogram": histogram.iloc[-1],
    }


def calculate_rsi(df: pd.DataFrame, period: int = 14) -> Tuple[pd.DataFrame, float]:
    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    rs = avg_gain / avg_loss.replace(to_replace=0, value=np.nan)
    rsi = 100 - (100 / (1 + rs))
    df["rsi"] = rsi
    return df, float(rsi.iloc[-1])


def calculate_stochastic(df: pd.DataFrame, k_period: int = 14, d_period: int = 3) -> Tuple[pd.DataFrame, Dict[str, float]]:
    lowest_low = df["low"].rolling(window=k_period, min_periods=k_period).min()
    highest_high = df["high"].rolling(window=k_period, min_periods=k_period).max()
    denominator = (highest_high - lowest_low).replace(to_replace=0, value=np.nan)

    percent_k = ((df["close"] - lowest_low) / denominator) * 100
    percent_d = percent_k.rolling(window=d_period, min_periods=d_period).mean()

    df["stochastic_k"] = percent_k
    df["stochastic_d"] = percent_d

    return df, {
        "stochastic_k": float(percent_k.iloc[-1]),
        "stochastic_d": float(percent_d.iloc[-1]),
    }


def calculate_bollinger_bands(df: pd.DataFrame, period: int = 20, std_dev: float = 2.0) -> Tuple[pd.DataFrame, Dict[str, float]]:
    middle_band = df["close"].rolling(window=period, min_periods=period).mean()
    rolling_std = df["close"].rolling(window=period, min_periods=period).std()

    upper_band = middle_band + std_dev * rolling_std
    lower_band = middle_band - std_dev * rolling_std

    df["bb_mid"] = middle_band
    df["bb_upper"] = upper_band
    df["bb_lower"] = lower_band

    latest = {
        "bollinger_mid": float(middle_band.iloc[-1]),
        "bollinger_upper": float(upper_band.iloc[-1]),
        "bollinger_lower": float(lower_band.iloc[-1]),
    }
    return df, latest


def calculate_atr(df: pd.DataFrame, period: int = 14) -> Tuple[pd.DataFrame, Dict[str, float]]:
    high_low = df["high"] - df["low"]
    high_close = (df["high"] - df["close"].shift()).abs()
    low_close = (df["low"] - df["close"].shift()).abs()

    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = true_range.rolling(window=period, min_periods=period).mean()

    df["atr"] = atr
    latest_atr = float(atr.iloc[-1])
    return df, {
        "atr": latest_atr,
        "atr_percent": (latest_atr / df["close"].iloc[-1]) * 100 if df["close"].iloc[-1] else np.nan,
    }


def build_indicator_snapshot(df: pd.DataFrame) -> IndicatorSnapshot:
    """
    Calculate all core indicators and return them in an IndicatorSnapshot.
    """
    df, sma = calculate_moving_averages(df.copy(), periods=(20, 50, 100, 200))
    df, ema = calculate_ema(df, periods=(12, 26))
    df, macd = calculate_macd(df)
    df, rsi_value = calculate_rsi(df)
    df, stochastic = calculate_stochastic(df)
    df, bollinger = calculate_bollinger_bands(df)
    df, atr = calculate_atr(df)

    latest = df.iloc[-1]

    return IndicatorSnapshot(
        price=float(latest["close"]),
        sma=sma,
        ema=ema,
        macd_line=float(macd["macd_line"]),
        macd_signal=float(macd["macd_signal"]),
        macd_histogram=float(macd["macd_histogram"]),
        rsi=float(rsi_value),
        stochastic_k=float(stochastic["stochastic_k"]),
        stochastic_d=float(stochastic["stochastic_d"]),
        bollinger_mid=float(bollinger["bollinger_mid"]),
        bollinger_upper=float(bollinger["bollinger_upper"]),
        bollinger_lower=float(bollinger["bollinger_lower"]),
        atr=float(atr["atr"]),
        atr_percent=float(atr["atr_percent"]),
        candle_timestamp=df.index[-1],
    )


def _trend_alignment(snapshot: IndicatorSnapshot) -> str:
    close = snapshot.price
    sma20 = snapshot.sma.get(20)
    sma50 = snapshot.sma.get(50)
    sma200 = snapshot.sma.get(200)

    if np.isnan([close, sma20, sma50, sma200]).any():
        return "neutral"

    if close > sma20 > sma50 > sma200:
        return "bullish"
    if close < sma20 < sma50 < sma200:
        return "bearish"
    return "neutral"


def _volatility_regime(snapshot: IndicatorSnapshot) -> str:
    if snapshot.atr_percent is np.nan:
        return "normal"
    if snapshot.atr_percent > 1.5:
        return "elevated"
    if snapshot.atr_percent < 0.6:
        return "compressed"
    return "normal"


def score_direction(snapshot: IndicatorSnapshot) -> Dict[str, float]:
    """
    Build probability scores for both bullish and bearish cases based on
    indicator confluence. Output is clamped between 30 and 85.
    """
    trend = _trend_alignment(snapshot)
    volatility = _volatility_regime(snapshot)

    long_points = 0.0
    short_points = 0.0
    long_penalties = 0.0
    short_penalties = 0.0

    # Trend alignment
    if trend == "bullish":
        long_points += 15
        short_penalties += 20
    elif trend == "bearish":
        short_points += 15
        long_penalties += 20

    # MACD momentum
    if snapshot.macd_line > snapshot.macd_signal:
        long_points += 10
    else:
        short_points += 10

    # RSI zones
    if snapshot.rsi < 30:
        long_points += 10
    elif snapshot.rsi > 70:
        short_points += 10
    elif 45 <= snapshot.rsi <= 60:
        long_points += 5
        short_points += 5

    # Bollinger positioning
    if snapshot.price <= snapshot.bollinger_lower:
        long_points += 10
    elif snapshot.price >= snapshot.bollinger_upper:
        short_points += 10
    else:
        long_points += 5
        short_points += 5

    # Stochastic momentum
    if snapshot.stochastic_k > snapshot.stochastic_d and snapshot.stochastic_k < 80:
        long_points += 8
    elif snapshot.stochastic_k < snapshot.stochastic_d and snapshot.stochastic_k > 20:
        short_points += 8

    # Volatility penalties
    if volatility == "elevated":
        long_penalties += 10
        short_penalties += 10
    elif volatility == "compressed":
        long_points += 5
        short_points += 5

    def clamp_score(base: float, points: float, penalties: float) -> float:
        score = 50 + points - penalties
        return float(max(30, min(85, score)))

    return {
        "long_probability": clamp_score(50, long_points, short_penalties),
        "short_probability": clamp_score(50, short_points, long_penalties),
        "volatility_regime": volatility,
        "trend_bias": trend,
    }


def generate_snapshot_from_candles(candles: Iterable[Dict], timeframe: str = "H1") -> Dict[str, object]:
    """
    High-level helper used inside the skill flow.

    Args:
        candles: MetaTrader candle list.
        timeframe: Label for diagnostics.

    Returns:
        Dict ready to be rendered or combined with natural language.
    """
    df = candles_to_dataframe(candles, timeframe=timeframe)
    snapshot = build_indicator_snapshot(df)
    scores = score_direction(snapshot)

    return {
        "timeframe": timeframe,
        "timestamp": snapshot.candle_timestamp.isoformat(),
        "price": snapshot.price,
        "sma": snapshot.sma,
        "ema": snapshot.ema,
        "macd": {
            "line": snapshot.macd_line,
            "signal": snapshot.macd_signal,
            "histogram": snapshot.macd_histogram,
        },
        "rsi": snapshot.rsi,
        "stochastic": {
            "k": snapshot.stochastic_k,
            "d": snapshot.stochastic_d,
        },
        "bollinger": {
            "mid": snapshot.bollinger_mid,
            "upper": snapshot.bollinger_upper,
            "lower": snapshot.bollinger_lower,
        },
        "atr": snapshot.atr,
        "atr_percent": snapshot.atr_percent,
        "trend_bias": scores["trend_bias"],
        "volatility_regime": scores["volatility_regime"],
        "long_probability": scores["long_probability"],
        "short_probability": scores["short_probability"],
    }


if __name__ == "__main__":
    # Minimal smoke test using synthetic candles
    index = pd.date_range("2024-01-01", periods=250, freq="H")
    price = np.cumsum(np.random.randn(len(index)) * 0.1) + 1.10
    high = price + np.random.rand(len(index)) * 0.05
    low = price - np.random.rand(len(index)) * 0.05
    candles = [
        {
            "time": ts.isoformat(),
            "open": float(price[idx - 1] if idx else price[idx]),
            "high": float(high[idx]),
            "low": float(low[idx]),
            "close": float(price[idx]),
            "tick_volume": int(np.random.randint(80, 250)),
        }
        for idx, ts in enumerate(index)
    ]

    snapshot = generate_snapshot_from_candles(candles)
    print("=== TECHNICAL SNAPSHOT ===")
    print(f"Timeframe: {snapshot['timeframe']}")
    print(f"Timestamp: {snapshot['timestamp']}")
    print(f"Price: {snapshot['price']:.5f}")
    print(f"Trend Bias: {snapshot['trend_bias']}")
    print(f"Volatility Regime: {snapshot['volatility_regime']}")
    print(f"Long Probability: {snapshot['long_probability']:.1f}%")
    print(f"Short Probability: {snapshot['short_probability']:.1f}%")
