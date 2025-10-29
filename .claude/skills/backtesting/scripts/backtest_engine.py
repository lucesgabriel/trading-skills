"""
Lightweight backtest engine helpers for the backtesting skill.

Provides a simple vectorised backtester that can plug into the skill
workflow. Strategies are defined as callables that consume a candle
DataFrame and return a signal series (-1 short, 0 flat, 1 long).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Iterable, List, Optional, Protocol

import numpy as np
import pandas as pd


class StrategyFunction(Protocol):
    def __call__(self, candles: pd.DataFrame) -> pd.Series:
        ...


@dataclass
class BacktestResult:
    total_return_pct: float
    annualised_return_pct: float
    win_rate_pct: float
    profit_factor: float
    expectancy_r: float
    max_drawdown_pct: float
    sharpe_ratio: float
    trades: List[Dict]
    equity_curve: pd.Series


def candles_to_dataframe(candles: Iterable[Dict]) -> pd.DataFrame:
    if not candles:
        raise ValueError("No candles supplied")

    df = pd.DataFrame(list(candles))
    column_map = {
        "time": "timestamp",
        "Time": "timestamp",
        "open": "open",
        "high": "high",
        "low": "low",
        "close": "close",
        "volume": "volume",
        "tick_volume": "volume",
    }
    df = df.rename(columns={k: v for k, v in column_map.items() if k in df.columns})
    if "timestamp" not in df.columns:
        raise KeyError("Expected time field in candle payload")

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", unit="s")
    if df["timestamp"].isna().any():
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    df = df.sort_values("timestamp").set_index("timestamp")
    for col in ("open", "high", "low", "close"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.dropna()


def default_ma_crossover(candles: pd.DataFrame, fast: int = 20, slow: int = 50) -> pd.Series:
    fast_ma = candles["close"].rolling(fast).mean()
    slow_ma = candles["close"].rolling(slow).mean()
    signal = np.where(fast_ma > slow_ma, 1, -1)
    return pd.Series(signal, index=candles.index)


def run_backtest(
    candles: Iterable[Dict],
    strategy_fn: StrategyFunction,
    risk_per_trade: float = 1.0,
    starting_capital: float = 10_000.0,
    commission_per_trade: float = 0.0,
) -> BacktestResult:
    df = candles_to_dataframe(candles)
    if len(df) < 50:
        raise ValueError("Not enough data for backtest (minimum 50 candles)")

    signals = strategy_fn(df).fillna(0)
    signals = signals.clip(-1, 1)
    df["signal"] = signals.shift(1).fillna(0)  # act on next bar
    df["returns"] = df["close"].pct_change().fillna(0)
    df["strategy_returns"] = df["signal"] * df["returns"]

    df["net_returns"] = df["strategy_returns"] - (commission_per_trade / starting_capital)
    df["equity_curve"] = (1 + df["net_returns"]).cumprod() * starting_capital

    # Identify trades
    trades: List[Dict] = []
    position = 0
    entry_price = None
    entry_time = None

    for timestamp, row in df.iterrows():
        signal = row["signal"]
        price = row["close"]

        if position == 0 and signal != 0:
            position = int(signal)
            entry_price = price
            entry_time = timestamp
        elif position != 0 and signal != position:
            pnl = (price - entry_price) / entry_price if position == 1 else (entry_price - price) / entry_price
            risk = risk_per_trade / 100
            r_multiple = pnl / risk if risk else pnl
            trades.append(
                {
                    "entry": entry_time,
                    "exit": timestamp,
                    "direction": "LONG" if position == 1 else "SHORT",
                    "entry_price": entry_price,
                    "exit_price": price,
                    "pnl_pct": round(pnl * 100, 2),
                    "r_multiple": round(r_multiple, 2),
                }
            )
            position = int(signal)
            entry_price = price if position != 0 else None
            entry_time = timestamp if position != 0 else None

    returns = df["strategy_returns"]
    winning_returns = returns[returns > 0]
    losing_returns = returns[returns < 0]
    win_rate = len(winning_returns) / max(1, len(winning_returns) + len(losing_returns))

    profit_factor = (
        winning_returns.sum() / abs(losing_returns.sum()) if len(losing_returns) > 0 else np.inf
    )
    expectancy = (
        (winning_returns.mean() * win_rate) + (losing_returns.mean() * (1 - win_rate))
    )

    equity_curve = df["equity_curve"]
    running_max = equity_curve.cummax()
    drawdown = (equity_curve - running_max) / running_max
    max_drawdown = drawdown.min() * 100

    sharpe = np.sqrt(252) * returns.mean() / (returns.std() + 1e-9)

    total_return = (equity_curve.iloc[-1] / equity_curve.iloc[0]) - 1
    years = (equity_curve.index[-1] - equity_curve.index[0]).days / 365.25
    annualised_return = (1 + total_return) ** (1 / max(years, 1e-6)) - 1

    return BacktestResult(
        total_return_pct=round(total_return * 100, 2),
        annualised_return_pct=round(annualised_return * 100, 2),
        win_rate_pct=round(win_rate * 100, 2),
        profit_factor=round(float(profit_factor), 2),
        expectancy_r=round(float(expectancy) / (risk_per_trade / 100), 2),
        max_drawdown_pct=round(float(max_drawdown), 2),
        sharpe_ratio=round(float(sharpe), 2),
        trades=trades,
        equity_curve=equity_curve,
    )


if __name__ == "__main__":
    # Example using synthetic data and moving-average crossover strategy.
    index = pd.date_range("2024-01-01", periods=400, freq="H")
    base = np.cumsum(np.random.randn(len(index)) * 0.2) + 50
    candles = [
        {
            "time": ts.isoformat(),
            "open": float(base[idx - 1] if idx else base[idx]),
            "high": float(base[idx] + np.random.rand() * 0.3),
            "low": float(base[idx] - np.random.rand() * 0.3),
            "close": float(base[idx]),
            "tick_volume": int(np.random.randint(80, 250)),
        }
        for idx, ts in enumerate(index)
    ]

    result = run_backtest(candles, default_ma_crossover, risk_per_trade=1.0)
    print("=== BACKTEST SUMMARY ===")
    print(f"Total Return: {result.total_return_pct}%")
    print(f"Annualised Return: {result.annualised_return_pct}%")
    print(f"Win Rate: {result.win_rate_pct}%")
    print(f"Profit Factor: {result.profit_factor}")
    print(f"Expectancy (R): {result.expectancy_r}")
    print(f"Max Drawdown: {result.max_drawdown_pct}%")
    print(f"Sharpe Ratio: {result.sharpe_ratio}")
    print(f"Trades Executed: {len(result.trades)}")
