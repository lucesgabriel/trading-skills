"""
Position sizing helpers for the risk-management skill.

Implements common sizing formulas (fixed % risk, volatility adjusted,
Kelly/optimal f estimates) plus quick portfolio exposure checks. The goal
is to make it easy for the skill to produce numeric answers without
re-deriving each equation programmatically.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Literal, Optional

import numpy as np


ForexSymbol = Literal[
    "AUDCAD",
    "AUDCHF",
    "AUDJPY",
    "AUDNZD",
    "AUDUSD",
    "CADCHF",
    "CADJPY",
    "CHFJPY",
    "EURAUD",
    "EURCAD",
    "EURCHF",
    "EURGBP",
    "EURJPY",
    "EURNZD",
    "EURUSD",
    "GBPAUD",
    "GBPCAD",
    "GBPCHF",
    "GBPJPY",
    "GBPNZD",
    "GBPUSD",
    "NZDCAD",
    "NZDCHF",
    "NZDJPY",
    "NZDUSD",
    "USDCAD",
    "USDCHF",
    "USDJPY",
    "USDMXN",
    "USDZAR",
]


@dataclass
class SymbolMeta:
    """Meta information required to convert price distance into monetary risk."""

    pip_value_per_standard_lot: float
    contract_size: float = 100_000.0
    asset_type: str = "forex"  # forex, metal, index, crypto, stock


# Reference pip values for majors (per standard lot, 100k units)
DEFAULT_SYMBOL_META: Dict[str, SymbolMeta] = {
    "EURUSD": SymbolMeta(pip_value_per_standard_lot=10.0),
    "GBPUSD": SymbolMeta(pip_value_per_standard_lot=10.0),
    "AUDUSD": SymbolMeta(pip_value_per_standard_lot=10.0),
    "NZDUSD": SymbolMeta(pip_value_per_standard_lot=10.0),
    "USDCAD": SymbolMeta(pip_value_per_standard_lot=7.97),
    "USDCHF": SymbolMeta(pip_value_per_standard_lot=11.09),
    "USDJPY": SymbolMeta(pip_value_per_standard_lot=9.17),
    "EURJPY": SymbolMeta(pip_value_per_standard_lot=9.17),
    "GBPJPY": SymbolMeta(pip_value_per_standard_lot=9.17),
    "XAUUSD": SymbolMeta(pip_value_per_standard_lot=100.0, contract_size=100.0, asset_type="metal"),
    "XAGUSD": SymbolMeta(pip_value_per_standard_lot=50.0, contract_size=5_000.0, asset_type="metal"),
    "US30": SymbolMeta(pip_value_per_standard_lot=1.0, contract_size=1.0, asset_type="index"),
    "US500": SymbolMeta(pip_value_per_standard_lot=50.0, contract_size=50.0, asset_type="index"),
}


def get_symbol_meta(symbol: str) -> SymbolMeta:
    return DEFAULT_SYMBOL_META.get(symbol.upper(), SymbolMeta(pip_value_per_standard_lot=10.0))


def calculate_position_size(
    account_balance: float,
    risk_percent: float,
    entry_price: float,
    stop_price: float,
    symbol: str,
    is_buy: bool = True,
) -> Dict[str, float]:
    """
    Standard fixed-percentage risk position sizing.

    Returns lots, units, and monetary risk so the skill can render a full explanation.
    """
    if account_balance <= 0:
        raise ValueError("Account balance must be positive")
    if risk_percent <= 0 or risk_percent > 10:
        raise ValueError("Risk percent should be between 0 and 10")

    meta = get_symbol_meta(symbol)
    risk_amount = account_balance * (risk_percent / 100)
    pip_distance = abs(entry_price - stop_price)

    if pip_distance == 0:
        raise ValueError("Stop loss must be different from entry price")

    # For forex pairs price distance in pips depends on decimals
    if meta.asset_type == "forex":
        pip_size = 0.01 if symbol.endswith("JPY") else 0.0001
        distance_in_pips = pip_distance / pip_size
        risk_per_standard_lot = distance_in_pips * meta.pip_value_per_standard_lot
    elif meta.asset_type == "metal":
        risk_per_standard_lot = pip_distance * meta.pip_value_per_standard_lot
    else:
        risk_per_standard_lot = pip_distance * meta.pip_value_per_standard_lot

    position_size_lots = risk_amount / risk_per_standard_lot
    position_size_units = position_size_lots * meta.contract_size

    direction = "BUY" if is_buy else "SELL"

    return {
        "symbol": symbol.upper(),
        "direction": direction,
        "risk_amount": round(risk_amount, 2),
        "pip_distance": round(pip_distance, 5),
        "position_size_lots": round(position_size_lots, 3),
        "position_size_units": round(position_size_units, 2),
        "risk_per_standard_lot": round(risk_per_standard_lot, 2),
    }


def atr_adjusted_position_size(
    account_balance: float,
    risk_percent: float,
    symbol: str,
    atr_value: float,
    atr_multiplier: float,
    tick_value: Optional[float] = None,
) -> Dict[str, float]:
    """
    Position sizing by volatility (ATR).

    Useful when stop loss is defined as ATR multiple and we want sizing directly from volatility.
    """
    meta = get_symbol_meta(symbol)
    risk_amount = account_balance * (risk_percent / 100)
    effective_tick = tick_value or meta.pip_value_per_standard_lot
    stop_distance_value = atr_value * atr_multiplier * effective_tick

    lots = risk_amount / stop_distance_value
    units = lots * meta.contract_size

    return {
        "symbol": symbol.upper(),
        "risk_amount": round(risk_amount, 2),
        "atr_value": atr_value,
        "atr_multiplier": atr_multiplier,
        "position_size_lots": round(lots, 3),
        "position_size_units": round(units, 2),
        "assumed_tick_value": round(effective_tick, 2),
    }


def kelly_fraction(win_rate: float, reward_risk: float) -> float:
    """
    Compute Kelly fraction for optimal bet sizing.

    Args:
        win_rate: Probability of winning (0-1).
        reward_risk: Average reward-to-risk ratio.

    Returns:
        Fraction of account to risk.
    """
    if reward_risk <= 0:
        raise ValueError("reward_risk must be positive")
    if not 0 < win_rate < 1:
        raise ValueError("win_rate must be between 0 and 1")

    edge = (win_rate * (reward_risk + 1)) - 1
    fraction = edge / reward_risk
    return max(0.0, fraction)


def half_kelly(win_rate: float, reward_risk: float) -> float:
    return kelly_fraction(win_rate, reward_risk) / 2


@dataclass
class PositionExposure:
    symbol: str
    direction: Literal["LONG", "SHORT"]
    risk_amount: float
    risk_percent: float
    account_balance: float


def portfolio_risk_snapshot(
    positions: Iterable[PositionExposure],
    max_portfolio_risk_percent: float = 8.0,
) -> Dict[str, float]:
    """
    Aggregate current open-trade risk for sanity checks.
    """
    positions = list(positions)
    total_risk = sum(pos.risk_amount for pos in positions)
    if not positions:
        return {
            "total_risk_amount": 0.0,
            "total_risk_percent": 0.0,
            "max_portfolio_risk_percent": max_portfolio_risk_percent,
            "ok": True,
        }

    balance = positions[0].account_balance
    total_percent = (total_risk / balance) * 100
    concentration = {}
    for pos in positions:
        concentration.setdefault(pos.symbol, 0.0)
        concentration[pos.symbol] += pos.risk_percent

    return {
        "total_risk_amount": round(total_risk, 2),
        "total_risk_percent": round(total_percent, 2),
        "max_portfolio_risk_percent": max_portfolio_risk_percent,
        "ok": total_percent <= max_portfolio_risk_percent,
        "concentration": concentration,
    }


def dynamic_risk_allocation(
    base_risk_percent: float,
    volatility_regime: str,
    conviction: Literal["LOW", "MEDIUM", "HIGH"] = "MEDIUM",
) -> float:
    """
    Suggest risk adjustments based on volatility and conviction.
    """
    adjustment = 0.0
    if volatility_regime == "elevated":
        adjustment -= 0.5
    elif volatility_regime == "compressed":
        adjustment += 0.25

    if conviction == "HIGH":
        adjustment += 0.25
    elif conviction == "LOW":
        adjustment -= 0.25

    return max(0.25, base_risk_percent + adjustment)


if __name__ == "__main__":
    # Quick demonstration
    position = calculate_position_size(
        account_balance=25_000,
        risk_percent=1.0,
        entry_price=1.0850,
        stop_price=1.0815,
        symbol="EURUSD",
        is_buy=True,
    )
    print("=== POSITION SIZING (EURUSD) ===")
    for key, value in position.items():
        print(f"{key}: {value}")

    positions = [
        PositionExposure("EURUSD", "LONG", risk_amount=250, risk_percent=1.0, account_balance=25_000),
        PositionExposure("GBPJPY", "SHORT", risk_amount=375, risk_percent=1.5, account_balance=25_000),
    ]
    risk_snapshot = portfolio_risk_snapshot(positions, max_portfolio_risk_percent=6.0)
    print("\n=== PORTFOLIO RISK ===")
    for key, value in risk_snapshot.items():
        print(f"{key}: {value}")
