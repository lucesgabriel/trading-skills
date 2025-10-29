# -*- coding: utf-8 -*-
"""
Multi-Symbol Scanner - Compare pattern opportunities across multiple symbols
"""

from typing import List, Dict, Any
from .candlestick_scanner import scan_symbol_for_patterns
from .confluence_calculator import enhance_probability_with_patterns

try:
    from .console_utils import safe_console_output
except ImportError:  # pragma: no cover - standalone execution
    from console_utils import safe_console_output


def scan_multiple_symbols(
    symbols: List[str],
    candles_data_by_symbol: Dict[str, Dict[str, str]],
    prices_by_symbol: Dict[str, float],
    timeframes: List[str] = ['M15', 'H1', 'H4', 'D1']
) -> List[Dict[str, Any]]:
    """
    Scan multiple symbols and return results for each.

    Args:
        symbols: List of trading symbols
        candles_data_by_symbol: Nested dict: symbol -> timeframe -> CSV data
        prices_by_symbol: Dict mapping symbol to current price
        timeframes: List of timeframes to analyze

    Returns:
        List of scan results for each symbol
    """
    all_results = []

    for symbol in symbols:
        if symbol in candles_data_by_symbol and symbol in prices_by_symbol:
            scan_result = scan_symbol_for_patterns(
                symbol=symbol,
                candles_data=candles_data_by_symbol[symbol],
                current_price=prices_by_symbol[symbol],
                timeframes=timeframes
            )

            # Calculate confluence
            base_scores = {'long_probability': 50.0, 'short_probability': 50.0}
            if scan_result['technical_snapshots']:
                # Use H1 or first available timeframe scores
                for tf in timeframes:
                    if tf in scan_result['technical_snapshots'] and scan_result['technical_snapshots'][tf]:
                        base_scores = scan_result['technical_snapshots'][tf].get('scores', base_scores)
                        break
            tf_scores_map = {
                tf: snapshot.get('scores', {})
                for tf, snapshot in (scan_result.get('technical_snapshots') or {}).items()
                if snapshot and snapshot.get('scores')
            }

            confluence = enhance_probability_with_patterns(
                base_scores=base_scores,
                patterns_by_timeframe=scan_result['patterns_by_timeframe'],
                levels_by_timeframe=scan_result['support_resistance'],
                current_price=scan_result['current_price'],
                technical_scores_by_timeframe=tf_scores_map
            )

            scan_result['confluence_analysis'] = confluence
            all_results.append(scan_result)

    return all_results


def rank_opportunities(
    scan_results: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Rank trading opportunities by probability score.

    Args:
        scan_results: List of scan results with confluence analysis

    Returns:
        Sorted list with highest probability opportunities first
    """
    # Sort by primary probability (descending)
    ranked = sorted(
        scan_results,
        key=lambda x: x['confluence_analysis']['primary_probability'],
        reverse=True
    )

    # Add rank numbers
    for i, result in enumerate(ranked, 1):
        result['rank'] = i

    return ranked


if __name__ == "__main__":
    safe_console_output("Multi-Symbol Scanner Module Loaded Successfully")
