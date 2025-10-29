# -*- coding: utf-8 -*-
"""
Confluence Calculator - Enhance probability scores with multi-timeframe analysis.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List

try:
    from .console_utils import safe_console_output
except ImportError:  # pragma: no cover - standalone execution
    from console_utils import safe_console_output


TIMEFRAME_WEIGHTS: Dict[str, float] = {
    "D1": 0.40,
    "H4": 0.30,
    "H1": 0.20,
    "M15": 0.10,
}
DEFAULT_TIMEFRAME_WEIGHT = 0.08
PROBABILITY_MIN = 25.0
PROBABILITY_MAX = 90.0
SUPPORT_RESISTANCE_BONUS = 10.0


def _resolve_score(scores: Dict[str, float], modern_key: str, legacy_key: str, default: float) -> float:
    """
    Resolve probability scores supporting both modern and legacy keys.

    Anthropic's early pattern-scanner prototypes emitted `bullish_score` /
    `bearish_score`. Later iterations renamed them to `long_probability` /
    `short_probability`. This helper keeps the skill backward compatible so
    existing users do not hit KeyError when older cached data is present.
    """
    if modern_key in scores and scores[modern_key] is not None:
        return float(scores[modern_key])
    if legacy_key in scores and scores[legacy_key] is not None:
        return float(scores[legacy_key])
    return float(default)


def _prefix(timeframe: str | None) -> str:
    return f"[{timeframe}] " if timeframe else ""


def _pattern_strength_counts(patterns: Iterable[Dict[str, Any]]) -> Dict[str, int]:
    counts = {
        "very_strong_bullish": 0,
        "strong_bullish": 0,
        "medium_bullish": 0,
        "very_strong_bearish": 0,
        "strong_bearish": 0,
        "medium_bearish": 0,
    }
    for pattern in patterns:
        strength = pattern.get("strength", "").title()
        bias = pattern.get("bias", "").title()
        key = f"{strength.replace(' ', '_').lower()}_{bias.lower()}"
        if key in counts:
            counts[key] += 1
    return counts


def _aggregate_pattern_counts(patterns_by_timeframe: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
    bullish = bearish = neutral = 0
    strength_totals = _pattern_strength_counts(
        pattern for patterns in patterns_by_timeframe.values() for pattern in patterns
    )

    for patterns in patterns_by_timeframe.values():
        for pattern in patterns:
            bias = pattern.get("bias", "Neutral")
            if bias == "Bullish":
                bullish += 1
            elif bias == "Bearish":
                bearish += 1
            else:
                neutral += 1

    total = bullish + bearish + neutral
    return {
        "bullish": bullish,
        "bearish": bearish,
        "neutral": neutral,
        "total": total,
        "by_strength": strength_totals,
    }


def _prioritised_timeframes(patterns_by_timeframe: Dict[str, List[Dict[str, Any]]]) -> List[str]:
    ordered = [tf for tf in TIMEFRAME_WEIGHTS.keys() if tf in patterns_by_timeframe]
    extras = sorted(set(patterns_by_timeframe.keys()) - set(ordered))
    ordered.extend(extras)
    return ordered or list(TIMEFRAME_WEIGHTS.keys())


def _resolve_levels(
    timeframe: str,
    levels_by_timeframe: Dict[str, Dict[str, List[float]]],
    current_price: float,
) -> Dict[str, Any]:
    levels = levels_by_timeframe.get(timeframe)
    if levels:
        return levels

    fallback = levels_by_timeframe.get("H4") or levels_by_timeframe.get("H1")
    if fallback:
        return fallback

    return {"resistance": [], "support": [], "pivot": current_price}


def calculate_pattern_confluence(
    patterns: List[Dict[str, Any]],
    technical_scores: Dict[str, float],
    support_resistance: Dict[str, List[float]],
    current_price: float,
    *,
    timeframe: str | None = None,
    timeframe_weight: float = 1.0,
) -> Dict[str, Any]:
    """
    Calculate enhanced probability scores based on pattern confluence.
    """
    weight = max(float(timeframe_weight), 0.0)
    base_long = _resolve_score(
        scores=technical_scores,
        modern_key="long_probability",
        legacy_key="bullish_score",
        default=50.0,
    )
    base_short = _resolve_score(
        scores=technical_scores,
        modern_key="short_probability",
        legacy_key="bearish_score",
        default=50.0,
    )

    long_adjustment = 0.0
    short_adjustment = 0.0
    confluence_factors: List[str] = []
    counts = _pattern_strength_counts(patterns)
    prefix = _prefix(timeframe)

    # Bullish contributions
    if counts["very_strong_bullish"]:
        boost = min(15.0, counts["very_strong_bullish"] * 15.0) * weight
        long_adjustment += boost
        confluence_factors.append(f"{prefix}Very Strong Bullish Pattern(s): +{boost:.1f}%")

    if counts["strong_bullish"]:
        boost = min(12.0, counts["strong_bullish"] * 12.0) * weight
        long_adjustment += boost
        confluence_factors.append(f"{prefix}Strong Bullish Pattern(s): +{boost:.1f}%")

    if counts["medium_bullish"]:
        boost = min(10.0, counts["medium_bullish"] * 10.0) * weight
        long_adjustment += boost
        confluence_factors.append(f"{prefix}Medium Bullish Pattern(s): +{boost:.1f}%")

    # Bearish contributions
    if counts["very_strong_bearish"]:
        boost = min(15.0, counts["very_strong_bearish"] * 15.0) * weight
        short_adjustment += boost
        confluence_factors.append(f"{prefix}Very Strong Bearish Pattern(s): +{boost:.1f}%")

    if counts["strong_bearish"]:
        boost = min(12.0, counts["strong_bearish"] * 12.0) * weight
        short_adjustment += boost
        confluence_factors.append(f"{prefix}Strong Bearish Pattern(s): +{boost:.1f}%")

    if counts["medium_bearish"]:
        boost = min(10.0, counts["medium_bearish"] * 10.0) * weight
        short_adjustment += boost
        confluence_factors.append(f"{prefix}Medium Bearish Pattern(s): +{boost:.1f}%")

    resistance_levels = support_resistance.get("resistance", [])
    support_levels = support_resistance.get("support", [])

    near_resistance = any(abs(current_price - r) / current_price < 0.002 for r in resistance_levels)
    near_support = any(abs(current_price - s) / current_price < 0.002 for s in support_levels)

    if near_support and (counts["very_strong_bullish"] or counts["strong_bullish"]):
        boost = SUPPORT_RESISTANCE_BONUS * weight
        long_adjustment += boost
        confluence_factors.append(f"{prefix}Pattern at Support Level: +{boost:.1f}%")

    if near_resistance and (counts["very_strong_bearish"] or counts["strong_bearish"]):
        boost = SUPPORT_RESISTANCE_BONUS * weight
        short_adjustment += boost
        confluence_factors.append(f"{prefix}Pattern at Resistance Level: +{boost:.1f}%")

    long_probability = max(PROBABILITY_MIN, min(PROBABILITY_MAX, base_long + long_adjustment))
    short_probability = max(PROBABILITY_MIN, min(PROBABILITY_MAX, base_short + short_adjustment))

    if long_probability > short_probability and long_probability > 55:
        signal = "LONG (BUY)"
        primary_probability = long_probability
        bias = "Bullish"
    elif short_probability > long_probability and short_probability > 55:
        signal = "SHORT (SELL)"
        primary_probability = short_probability
        bias = "Bearish"
    else:
        signal = "NEUTRAL (WAIT)"
        primary_probability = max(long_probability, short_probability)
        bias = "Neutral"

    return {
        "signal": signal,
        "bias": bias,
        "primary_probability": round(primary_probability, 1),
        "long_probability": round(long_probability, 1),
        "short_probability": round(short_probability, 1),
        "long_adjustment": round(long_adjustment, 2),
        "short_adjustment": round(short_adjustment, 2),
        "timeframe": timeframe,
        "timeframe_weight": round(weight, 3),
        "base_scores": {
            "long_probability": round(base_long, 1),
            "short_probability": round(base_short, 1),
        },
        "confluence_factors": confluence_factors,
        "pattern_counts": counts,
    }


def enhance_probability_with_patterns(
    base_scores: Dict[str, float],
    patterns_by_timeframe: Dict[str, List[Dict[str, Any]]],
    levels_by_timeframe: Dict[str, Dict[str, List[float]]],
    current_price: float,
    technical_scores_by_timeframe: Dict[str, Dict[str, float]] | None = None,
) -> Dict[str, Any]:
    """
    Enhance probability scores with multi-timeframe pattern analysis.
    """
    technical_scores_by_timeframe = technical_scores_by_timeframe or {}

    base_long = _resolve_score(
        scores=base_scores,
        modern_key="long_probability",
        legacy_key="bullish_score",
        default=50.0,
    )
    base_short = _resolve_score(
        scores=base_scores,
        modern_key="short_probability",
        legacy_key="bearish_score",
        default=50.0,
    )

    breakdown: List[Dict[str, Any]] = []
    combined_factors: List[str] = []
    total_long = base_long
    total_short = base_short

    for timeframe in _prioritised_timeframes(patterns_by_timeframe):
        patterns = patterns_by_timeframe.get(timeframe, [])
        if not patterns and timeframe not in levels_by_timeframe:
            # Skip completely empty timeframes to avoid noise in the breakdown
            continue

        weight = TIMEFRAME_WEIGHTS.get(timeframe, DEFAULT_TIMEFRAME_WEIGHT)
        sr_levels = _resolve_levels(timeframe, levels_by_timeframe, current_price)
        tf_scores = technical_scores_by_timeframe.get(timeframe, base_scores)

        tf_result = calculate_pattern_confluence(
            patterns=patterns,
            technical_scores=tf_scores,
            support_resistance=sr_levels,
            current_price=current_price,
            timeframe=timeframe,
            timeframe_weight=weight,
        )

        total_long += tf_result["long_adjustment"]
        total_short += tf_result["short_adjustment"]
        combined_factors.extend(tf_result["confluence_factors"])

        breakdown.append(
            {
                "timeframe": timeframe,
                "weight": round(weight, 3),
                "long_adjustment": tf_result["long_adjustment"],
                "short_adjustment": tf_result["short_adjustment"],
                "long_probability": tf_result["long_probability"],
                "short_probability": tf_result["short_probability"],
                "signal": tf_result["signal"],
                "patterns_detected": sum(tf_result["pattern_counts"].values()),
                "confluence_factors": tf_result["confluence_factors"],
            }
        )

    raw_long = total_long
    raw_short = total_short

    long_probability = max(PROBABILITY_MIN, min(PROBABILITY_MAX, raw_long))
    short_probability = max(PROBABILITY_MIN, min(PROBABILITY_MAX, raw_short))

    if long_probability > short_probability and long_probability > 55:
        signal = "LONG (BUY)"
        primary_probability = long_probability
        bias = "Bullish"
    elif short_probability > long_probability and short_probability > 55:
        signal = "SHORT (SELL)"
        primary_probability = short_probability
        bias = "Bearish"
    else:
        signal = "NEUTRAL (WAIT)"
        primary_probability = max(long_probability, short_probability)
        bias = "Neutral"

    aggregate_counts = _aggregate_pattern_counts(patterns_by_timeframe)

    return {
        "signal": signal,
        "bias": bias,
        "primary_probability": round(primary_probability, 1),
        "long_probability": round(long_probability, 1),
        "short_probability": round(short_probability, 1),
        "long_adjustment": round(long_probability - base_long, 2),
        "short_adjustment": round(short_probability - base_short, 2),
        "base_scores": {
            "long_probability": round(base_long, 1),
            "short_probability": round(base_short, 1),
        },
        "confluence_factors": combined_factors,
        "pattern_counts": aggregate_counts,
        "timeframe_breakdown": breakdown,
    }


if __name__ == "__main__":
    safe_console_output("Confluence Calculator Module Loaded Successfully")
