#!/usr/bin/env python3
"""
Standalone Pattern Scanner

Usage:
    python tools/standalone_scanner.py EURUSD --timeframes M15,H1,H4,D1

The script attempts to fetch market data via an optional MetaTrader connector.
Provide --sample-data pointing to a JSON file with candle CSV payloads to run
without MCP connectivity.
"""

from __future__ import annotations

import argparse
import json
import sys
import webbrowser
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = REPO_ROOT / ".claude" / "skills" / "pattern-scanner" / "scripts"
sys.path.insert(0, str(SKILL_PATH))

from candlestick_scanner import (  # noqa: E402
    parse_candles_from_csv,
    scan_symbol_for_patterns,
)
from confluence_calculator import enhance_probability_with_patterns  # noqa: E402
from console_utils import safe_console_output  # noqa: E402
from html_generator import generate_html_report  # noqa: E402

try:  # Optional MetaTrader connector
    from mt5_connector import get_symbol_data  # type: ignore  # noqa: E402

    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False


def _infer_price_from_candles(candles: Dict[str, str], timeframes: List[str]) -> float:
    for timeframe in timeframes:
        csv_data = candles.get(timeframe)
        if not csv_data:
            continue
        df = parse_candles_from_csv(csv_data)
        if not df.empty:
            return float(df.iloc[-1]["close"])
    raise ValueError("Unable to infer current price from provided candles.")


def _load_sample_payload(path: Path) -> Tuple[Dict[str, str], float]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict) and "candles" in payload:
        candles = payload["candles"]
        price = float(payload.get("current_price") or 0)
    else:
        candles = payload
        price = 0.0
    if not price:
        price = _infer_price_from_candles(candles, list(candles.keys()))
    return candles, price


def fetch_market_data(
    symbol: str,
    timeframes: List[str],
    sample_path: Path | None = None,
) -> Tuple[Dict[str, str], float]:
    if sample_path:
        return _load_sample_payload(sample_path)

    if not MCP_AVAILABLE:
        raise RuntimeError(
            "MetaTrader connector not configured. Provide --sample-data or install mt5_connector."
        )

    result = get_symbol_data(symbol, timeframes)
    if isinstance(result, tuple):
        candles, price = result
    else:
        candles = result.get("candles") if isinstance(result, dict) else result
        price = result.get("current_price") if isinstance(result, dict) else 0.0

    if not price:
        price = _infer_price_from_candles(candles, timeframes)
    return candles, float(price)


def run_scan(
    symbol: str,
    timeframes: List[str],
    output_dir: Path,
    sample_data: Path | None,
    open_browser: bool,
) -> Tuple[str, Dict[str, Any]]:
    safe_console_output(f"-> Scanning {symbol} across {', '.join(timeframes)}")
    candles, current_price = fetch_market_data(symbol, timeframes, sample_data)

    scan_results = scan_symbol_for_patterns(
        symbol=symbol,
        candles_data=candles,
        current_price=current_price,
        timeframes=timeframes,
    )

    technical_snapshots = scan_results.get("technical_snapshots") or {}
    technical_scores_by_tf = {
        tf: payload.get("scores", {})
        for tf, payload in technical_snapshots.items()
        if payload and payload.get("scores")
    }

    base_scores = next(iter(technical_scores_by_tf.values()), {"long_probability": 50.0, "short_probability": 50.0})

    confluence = enhance_probability_with_patterns(
        base_scores=base_scores,
        patterns_by_timeframe=scan_results["patterns_by_timeframe"],
        levels_by_timeframe=scan_results.get("support_resistance", {}),
        current_price=current_price,
        technical_scores_by_timeframe=technical_scores_by_tf,
    )

    report_path = generate_html_report(
        symbol=symbol,
        scan_results=scan_results,
        confluence_results=confluence,
        output_dir=str(output_dir),
    )

    safe_console_output(f"[OK] Reporte generado en: {report_path}")
    safe_console_output(
        f"-> Señal principal: {confluence['signal']} ({confluence['primary_probability']:.1f}%)"
    )

    if open_browser:
        webbrowser.open(f"file://{report_path}")
    return report_path, confluence


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Standalone Pattern Scanner")
    parser.add_argument("symbol", help="Trading symbol (e.g., EURUSD)")
    parser.add_argument(
        "--timeframes",
        default="M15,H1,H4,D1",
        help="Comma-separated list of timeframes (default: M15,H1,H4,D1)",
    )
    parser.add_argument(
        "--output",
        default=str(REPO_ROOT / "reports"),
        help="Directory where the HTML report will be stored",
    )
    parser.add_argument(
        "--sample-data",
        type=Path,
        help="Path to JSON file with sample candle data (fallback without MCP)",
    )
    parser.add_argument(
        "--no-open",
        action="store_true",
        help="Do not open the generated report in the default browser",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    timeframes = [tf.strip().upper() for tf in args.timeframes.split(",") if tf.strip()]
    if not timeframes:
        raise SystemExit("Debe especificar al menos un timeframe valido.")

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        run_scan(
            symbol=args.symbol.upper(),
            timeframes=timeframes,
            output_dir=output_dir,
            sample_data=args.sample_data,
            open_browser=not args.no_open,
        )
    except Exception as exc:  # pragma: no cover - CLI friendly
        safe_console_output(f"[ERROR] Error durante el escaneo: {exc}")
        raise SystemExit(1) from exc

if __name__ == "__main__":
    main()
