#!/usr/bin/env python3
"""
Batch Pattern Scanner

Usage:
    python tools/batch_scanner.py EURUSD GBPUSD XAUUSD --timeframes H1,H4,D1
"""

from __future__ import annotations

import argparse
import concurrent.futures
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

TOOLS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOLS_DIR.parent
SKILL_PATH = REPO_ROOT / ".claude" / "skills" / "pattern-scanner" / "scripts"

sys.path.insert(0, str(SKILL_PATH))
sys.path.insert(0, str(TOOLS_DIR))

from console_utils import safe_console_output  # type: ignore  # noqa: E402
from standalone_scanner import run_scan  # type: ignore  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Batch Pattern Scanner")
    parser.add_argument("symbols", nargs="+", help="Symbols to scan (e.g., EURUSD GBPUSD)")
    parser.add_argument(
        "--timeframes",
        default="M15,H1,H4,D1",
        help="Comma-separated timeframes applied to every symbol",
    )
    parser.add_argument(
        "--output",
        default=str(REPO_ROOT / "reports"),
        help="Directory where HTML reports will be saved",
    )
    parser.add_argument(
        "--sample-dir",
        type=Path,
        help="Directory containing sample data JSON per symbol (SYMBOL.json)",
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="Open each generated report in the default browser",
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=4,
        help="Maximum number of concurrent workers (default: 4)",
    )
    return parser.parse_args()


def resolve_sample_path(sample_dir: Optional[Path], symbol: str) -> Optional[Path]:
    if not sample_dir:
        return None
    candidate = sample_dir / f"{symbol.upper()}.json"
    return candidate if candidate.exists() else None


def scan_symbol(
    symbol: str,
    timeframes: List[str],
    output_dir: Path,
    sample_dir: Optional[Path],
    open_browser: bool,
) -> Dict[str, Any]:
    try:
        sample_path = resolve_sample_path(sample_dir, symbol)
        report_path, confluence = run_scan(
            symbol=symbol,
            timeframes=timeframes,
            output_dir=output_dir,
            sample_data=sample_path,
            open_browser=open_browser,
        )
        return {
            "symbol": symbol,
            "status": "ok",
            "report": report_path,
            "signal": confluence.get("signal"),
            "probability": confluence.get("primary_probability"),
        }
    except Exception as exc:
        safe_console_output(f"[ERROR] {symbol}: {exc}")
        return {"symbol": symbol, "status": "error", "error": str(exc)}


def main() -> None:
    args = parse_args()
    timeframes = [tf.strip().upper() for tf in args.timeframes.split(",") if tf.strip()]
    if not timeframes:
        raise SystemExit("Debe especificar al menos un timeframe valido.")

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    safe_console_output(
        f"-> Ejecutando escaneo en lote para: {', '.join(sym.upper() for sym in args.symbols)}"
    )

    results: List[Dict[str, Any]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        futures = [
            executor.submit(
                scan_symbol,
                symbol=symbol.upper(),
                timeframes=timeframes,
                output_dir=output_dir,
                sample_dir=args.sample_dir,
                open_browser=args.open,
            )
            for symbol in args.symbols
        ]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    ok_results = [res for res in results if res["status"] == "ok"]
    safe_console_output("")
    safe_console_output("Resumen de resultados:")
    for idx, res in enumerate(ok_results, start=1):
        safe_console_output(
            f"  {idx:02d}. {res['symbol']} -> {res.get('signal')} ({res.get('probability'):.1f}%)"
        )
        safe_console_output(f"      Reporte: {res.get('report')}")

    if not ok_results:
        safe_console_output("[WARN] No se generaron reportes exitosos.")


if __name__ == "__main__":
    main()
