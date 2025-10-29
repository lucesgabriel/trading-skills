"""
Market scanner utilities for the opportunity-scanner skill.

Loads the indicator helpers from the technical-analysis skill and provides
ready-to-use functions to score multiple symbols, apply filters, and
produce ranked watchlists. Keeping this logic here avoids having to
rewrite scanning code inside the skill instructions each time.
"""

from __future__ import annotations

import importlib.util
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Protocol, Sequence

import numpy as np

_INDICATOR_MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "technical-analysis"
    / "scripts"
    / "indicator_suite.py"
)

if not _INDICATOR_MODULE_PATH.exists():
    raise FileNotFoundError(
        "indicator_suite.py not found. Ensure the technical-analysis scripts were generated."
    )

_spec = importlib.util.spec_from_file_location("indicator_suite", _INDICATOR_MODULE_PATH)
_module = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
assert _spec and _spec.loader
_spec.loader.exec_module(_module)  # type: ignore[union-attr]

generate_snapshot_from_candles = _module.generate_snapshot_from_candles  # type: ignore[attr-defined]


class MarketDataProvider(Protocol):
    """Minimal interface expected by the scanner."""

    def get_candles(self, symbol: str, timeframe: str, count: int) -> List[Dict]:
        ...

    def get_price(self, symbol: str) -> float:
        ...


@dataclass
class ScannerFilters:
    """Runtime filters to trim scanner output."""

    min_probability: float = 60.0
    direction: str = "BOTH"  # LONG, SHORT, BOTH
    risk_reward_min: Optional[float] = None
    symbols: Optional[Sequence[str]] = None
    max_results: int = 5


@dataclass
class Opportunity:
    symbol: str
    direction: str
    probability: float
    price: float
    confluence_score: float
    risk_reward: Optional[float]
    timeframe_summaries: Dict[str, Dict]
    notes: List[str] = field(default_factory=list)


def _aggregate_probabilities(timeframe_data: Dict[str, Dict]) -> Dict[str, float]:
    long_probs = np.array([frame["long_probability"] for frame in timeframe_data.values()])
    short_probs = np.array([frame["short_probability"] for frame in timeframe_data.values()])

    long_avg = float(np.nanmean(long_probs))
    short_avg = float(np.nanmean(short_probs))

    direction = "LONG" if long_avg >= short_avg else "SHORT"
    probability = long_avg if direction == "LONG" else short_avg
    confluence = float(np.abs(long_avg - short_avg))

    return {
        "direction": direction,
        "probability": probability,
        "confluence": confluence,
        "long_average": long_avg,
        "short_average": short_avg,
    }


def _describe_bias(symbol: str, timeframe_data: Dict[str, Dict], direction: str) -> List[str]:
    notes = []
    for timeframe, data in timeframe_data.items():
        bias = data["trend_bias"]
        regime = data["volatility_regime"]
        probability = data["long_probability"] if direction == "LONG" else data["short_probability"]
        notes.append(
            f"{timeframe}: {bias.upper()} bias, volatility {regime}, {direction} prob {probability:.1f}%"
        )
    return notes


def _mock_risk_reward(direction: str, confluence: float) -> float:
    """
    Placeholder risk/reward approximation.
    In production the skill should compute real targets from structure levels.
    """
    base_rr = 1.5 if direction == "LONG" else 1.6
    return round(base_rr + confluence / 40, 2)


def analyze_symbol(
    provider: MarketDataProvider,
    symbol: str,
    timeframes: Sequence[str],
    candles_per_timeframe: int = 200,
) -> Opportunity:
    timeframe_summaries: Dict[str, Dict] = {}

    for timeframe in timeframes:
        candles = provider.get_candles(symbol, timeframe, candles_per_timeframe)
        timeframe_summaries[timeframe] = generate_snapshot_from_candles(
            candles=candles,
            timeframe=timeframe,
        )

    aggregated = _aggregate_probabilities(timeframe_summaries)
    notes = _describe_bias(symbol, timeframe_summaries, aggregated["direction"])

    return Opportunity(
        symbol=symbol,
        direction=aggregated["direction"],
        probability=round(aggregated["probability"], 1),
        price=float(provider.get_price(symbol)),
        confluence_score=round(aggregated["confluence"], 2),
        risk_reward=_mock_risk_reward(aggregated["direction"], aggregated["confluence"]),
        timeframe_summaries=timeframe_summaries,
        notes=notes,
    )


def apply_filters(opportunities: Iterable[Opportunity], filters: ScannerFilters) -> List[Opportunity]:
    filtered: List[Opportunity] = []

    for opp in opportunities:
        if filters.symbols and opp.symbol not in filters.symbols:
            continue
        if opp.probability < filters.min_probability:
            continue
        if filters.direction != "BOTH" and opp.direction != filters.direction:
            continue
        if filters.risk_reward_min and (opp.risk_reward or 0) < filters.risk_reward_min:
            continue
        filtered.append(opp)

    filtered.sort(key=lambda item: item.probability, reverse=True)
    return filtered[: filters.max_results]


def scan_markets(
    provider: MarketDataProvider,
    symbols: Sequence[str],
    filters: Optional[ScannerFilters] = None,
    timeframes: Sequence[str] = ("H4", "H1", "M15"),
) -> List[Opportunity]:
    """
    High-level helper to scan multiple symbols and return ranked opportunities.
    """
    opportunities: List[Opportunity] = []
    for symbol in symbols:
        try:
            opportunity = analyze_symbol(provider, symbol, timeframes)
            opportunities.append(opportunity)
        except Exception as exc:
            fallback = Opportunity(
                symbol=symbol,
                direction="UNKNOWN",
                probability=0.0,
                price=0.0,
                confluence_score=0.0,
                risk_reward=None,
                timeframe_summaries={},
                notes=[f"Failed to analyze: {exc}"],
            )
            opportunities.append(fallback)

    return apply_filters(opportunities, filters or ScannerFilters())


# --- Example Usage ---

class _DummyProvider:
    """Quick demo provider using random walks (for local smoke tests only)."""

    def __init__(self) -> None:
        self._prices: Dict[str, float] = {}

    def get_candles(self, symbol: str, timeframe: str, count: int) -> List[Dict]:
        base_price = self._prices.get(symbol, random.uniform(1.0, 2.0))
        moves = np.cumsum(np.random.randn(count) * 0.001) + base_price
        highs = moves + np.random.rand(count) * 0.002
        lows = moves - np.random.rand(count) * 0.002
        self._prices[symbol] = float(moves[-1])

        candles: List[Dict] = []
        timestamps = np.arange(count, dtype=int)
        for idx in range(count):
            candles.append(
                {
                    "time": int(timestamps[idx]),
                    "open": float(moves[idx - 1] if idx else moves[idx]),
                    "high": float(highs[idx]),
                    "low": float(lows[idx]),
                    "close": float(moves[idx]),
                    "tick_volume": int(np.random.randint(50, 200)),
                }
            )
        return candles

    def get_price(self, symbol: str) -> float:
        return float(self._prices.get(symbol, random.uniform(1.0, 2.0)))


if __name__ == "__main__":
    provider = _DummyProvider()
    symbols = ["EURUSD", "GBPJPY", "XAUUSD", "US500", "USDCAD"]
    opportunities = scan_markets(
        provider=provider,
        symbols=symbols,
        filters=ScannerFilters(min_probability=55, max_results=3),
    )

    print("=== TOP OPPORTUNITIES ===")
    for opp in opportunities:
        print(f"{opp.symbol} | {opp.direction} | Prob {opp.probability:.1f}% | R:R {opp.risk_reward}")
        for note in opp.notes:
            print(f"  - {note}")
