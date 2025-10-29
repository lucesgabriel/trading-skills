import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = REPO_ROOT / ".claude" / "skills" / "pattern-scanner" / "scripts"
sys.path.insert(0, str(SKILL_PATH))  # noqa: E402, N806

from confluence_calculator import enhance_probability_with_patterns  # type: ignore  # noqa: E402


def test_enhance_probability_handles_legacy_scores():
    base_scores = {
        "bullish_score": 55.0,
        "bearish_score": 45.0,
    }
    patterns_by_timeframe = {
        "H1": [
            {
                "name": "Bullish Engulfing",
                "type": "Reversal",
                "strength": "Very Strong",
                "bias": "Bullish",
                "reliability": 80,
                "price": 1.12345,
                "time": "2025-10-29 16:00:00",
            }
        ],
    }
    levels_by_timeframe = {
        "H1": {
            "resistance": [1.13000],
            "support": [1.11500],
            "pivot": 1.12200,
        }
    }

    result = enhance_probability_with_patterns(
        base_scores=base_scores,
        patterns_by_timeframe=patterns_by_timeframe,
        levels_by_timeframe=levels_by_timeframe,
        current_price=1.12340,
    )

    assert result["long_probability"] >= 55.0
    assert result["short_probability"] >= 45.0
    assert result["signal"] in {"LONG (BUY)", "NEUTRAL (WAIT)"}
