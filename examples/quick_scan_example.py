"""
Quick pattern scan example using sample data.
"""

from __future__ import annotations

import sys
from pathlib import Path

EXAMPLES_DIR = Path(__file__).resolve().parent
REPO_ROOT = EXAMPLES_DIR.parent
SKILL_PATH = REPO_ROOT / ".claude" / "skills" / "pattern-scanner" / "scripts"

sys.path.insert(0, str(SKILL_PATH))

from candlestick_scanner import scan_symbol_for_patterns  # type: ignore  # noqa: E402
from confluence_calculator import enhance_probability_with_patterns  # type: ignore  # noqa: E402

SAMPLE_CANDLES = {
    'M15': """time,open,high,low,close,tick_volume,spread,real_volume\n2025-10-29 16:45:00,1.16386,1.16392,1.16379,1.16386,97,0,0\n2025-10-29 16:30:00,1.16431,1.16447,1.16363,1.16386,2485,0,0\n2025-10-29 16:15:00,1.16379,1.16458,1.16374,1.16430,3107,0,0\n""",
    'H1': """time,open,high,low,close,tick_volume,spread,real_volume\n2025-10-29 16:00:00,1.16342,1.16458,1.16336,1.16386,8090,0,0\n2025-10-29 15:00:00,1.16396,1.16450,1.16276,1.16341,9666,0,0\n2025-10-29 14:00:00,1.16472,1.16486,1.16330,1.16397,6899,0,0\n""",
    'H4': """time,open,high,low,close,tick_volume,spread,real_volume\n2025-10-29 16:00:00,1.16342,1.16458,1.16336,1.16386,8096,0,0\n2025-10-29 12:00:00,1.16231,1.16488,1.16187,1.16341,31193,0,0\n2025-10-29 08:00:00,1.16343,1.16380,1.16228,1.16231,26881,0,0\n""",
    'D1': """time,open,high,low,close,tick_volume,spread,real_volume\n2025-10-29 00:00:00,1.16501,1.16609,1.16187,1.16385,94702,0,0\n2025-10-28 00:00:00,1.16443,1.16689,1.16253,1.16523,141577,0,0\n2025-10-27 00:00:00,1.16320,1.16521,1.16174,1.16441,132046,0,0\n""",
}


def main() -> None:
    symbol = "EURUSD"
    timeframes = ['M15', 'H1', 'H4', 'D1']

    scan_results = scan_symbol_for_patterns(
        symbol=symbol,
        candles_data=SAMPLE_CANDLES,
        current_price=1.16386,
        timeframes=timeframes,
    )

    technical_snapshots = scan_results.get('technical_snapshots') or {}
    technical_scores_by_tf = {
        tf: payload.get('scores', {})
        for tf, payload in technical_snapshots.items()
        if payload and payload.get('scores')
    }
    base_scores = next(iter(technical_scores_by_tf.values()), {'long_probability': 50.0, 'short_probability': 50.0})

    confluence = enhance_probability_with_patterns(
        base_scores=base_scores,
        patterns_by_timeframe=scan_results['patterns_by_timeframe'],
        levels_by_timeframe=scan_results['support_resistance'],
        current_price=scan_results['current_price'],
        technical_scores_by_timeframe=technical_scores_by_tf,
    )

    print("=== QUICK SCAN SUMMARY ===")
    print(f"Symbol: {symbol}")
    print(f"Signal: {confluence['signal']}")
    print(f"Probability: {confluence['primary_probability']:.1f}%")
    print(f"Patterns detected: {scan_results['pattern_counts']['total']}")
    if confluence['confluence_factors']:
        print("Factors:")
        for factor in confluence['confluence_factors']:
            print(f"  - {factor}")


if __name__ == "__main__":
    main()
