#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Direct entry point for pattern-scanner skill
Called by Claude Code when user requests pattern scanning
"""

import sys
import json
from pathlib import Path
from datetime import datetime
import pandas as pd

# Import scanner modules
try:
    from candlestick_scanner import scan_symbol_for_patterns
    from confluence_calculator import enhance_probability_with_patterns
    from html_generator import generate_html_report
    from console_utils import safe_print
except ImportError:
    # Add current directory to path
    sys.path.insert(0, str(Path(__file__).parent))
    from candlestick_scanner import scan_symbol_for_patterns
    from confluence_calculator import enhance_probability_with_patterns
    from html_generator import generate_html_report
    from console_utils import safe_print


def parse_mcp_candles(csv_string: str) -> list:
    """Parse MCP candle CSV format into list of dicts"""
    import io
    df = pd.read_csv(io.StringIO(csv_string))

    candles = []
    for _, row in df.iterrows():
        candles.append({
            'time': str(row['time']),
            'open': float(row['open']),
            'high': float(row['high']),
            'low': float(row['low']),
            'close': float(row['close']),
            'tick_volume': int(row['tick_volume'])
        })

    return candles


def run_pattern_scan(symbol: str, mcp_data: dict) -> str:
    """
    Main entry point for pattern scanning

    Args:
        symbol: Symbol name (e.g., 'EURUSD')
        mcp_data: Dict with keys:
            - price: Dict from mcp__metatrader__get_symbol_price
            - candles_m15: CSV string from get_candles_latest
            - candles_h1: CSV string
            - candles_h4: CSV string
            - candles_d1: CSV string

    Returns:
        Path to generated HTML report
    """

    safe_print(f"\n📊 Escaneando {symbol} para patrones de velas...")
    safe_print("=" * 60)

    # Parse current price
    current_price = float(mcp_data['price']['bid'])
    safe_print(f"💰 Precio actual: {current_price:.5f}")

    # Prepare candles data (as CSV strings for the scanner)
    candles_data = {}
    timeframes = ['M15', 'H1', 'H4', 'D1']

    for tf in timeframes:
        key = f'candles_{tf.lower()}'
        if key in mcp_data:
            try:
                # Accept both formats: {"result": "CSV"} or "CSV"
                data = mcp_data[key]
                if isinstance(data, dict) and 'result' in data:
                    # Format: {"result": "CSV string"}
                    csv_string = data['result']
                elif isinstance(data, str):
                    # Format: "CSV string" (direct)
                    csv_string = data
                else:
                    safe_print(f"⚠ {tf}: Formato de datos no reconocido")
                    candles_data[tf] = ""
                    continue

                candles_data[tf] = csv_string
                # Count lines for display
                num_candles = len(csv_string.split('\n')) - 2  # Subtract header and empty line
                safe_print(f"✓ {tf}: {num_candles} velas cargadas")
            except Exception as e:
                safe_print(f"⚠ {tf}: Error al parsear - {e}")
                candles_data[tf] = ""

    # Run pattern detection
    safe_print("\n🔍 Detectando patrones...")
    scan_results = scan_symbol_for_patterns(
        symbol=symbol,
        candles_data=candles_data,
        current_price=current_price
    )

    # Extract technical scores by timeframe
    technical_scores_by_tf = {}
    if 'technical_snapshots' in scan_results:
        for tf, snapshot_data in scan_results['technical_snapshots'].items():
            if snapshot_data and 'scores' in snapshot_data:
                technical_scores_by_tf[tf] = snapshot_data['scores']

    # Calculate confluence using multi-timeframe analysis
    safe_print("🧮 Calculando confluencia...")
    base_scores = {'long_probability': 50.0, 'short_probability': 50.0}
    confluence_results = enhance_probability_with_patterns(
        base_scores=base_scores,
        patterns_by_timeframe=scan_results['patterns_by_timeframe'],
        levels_by_timeframe=scan_results['support_resistance'],
        current_price=scan_results['current_price'],
        technical_scores_by_timeframe=technical_scores_by_tf if technical_scores_by_tf else None
    )

    # Display results
    total_patterns = scan_results.get('pattern_counts', {}).get('total', 0)
    signal = confluence_results.get('signal', 'NEUTRAL')
    probability = confluence_results.get('primary_probability', 0)
    bias = confluence_results.get('bias', 'Neutral')

    safe_print("\n" + "=" * 60)
    safe_print(f"✅ Patrones detectados: {total_patterns}")
    safe_print(f"💡 Señal: {signal} - {bias.upper()}")
    safe_print(f"📈 Probabilidad: {probability:.1f}%")
    safe_print("=" * 60)

    # Generate HTML report
    safe_print("\n📝 Generando reporte HTML...")
    report_path = generate_html_report(
        symbol=symbol,
        scan_results=scan_results,
        confluence_results=confluence_results
    )

    safe_print(f"\n✅ Reporte generado: {report_path}")
    safe_print("\n🌐 Para ver el reporte, abre el archivo HTML en tu navegador.")

    return report_path


if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) < 2:
        safe_print("Usage: python run_scan.py <symbol> <mcp_data_json>")
        sys.exit(1)

    symbol = sys.argv[1]

    # Read MCP data from stdin or file
    if len(sys.argv) > 2:
        mcp_data_path = sys.argv[2]
        with open(mcp_data_path, 'r') as f:
            mcp_data = json.load(f)
    else:
        # Read from stdin
        mcp_data = json.load(sys.stdin)

    try:
        report_path = run_pattern_scan(symbol, mcp_data)

        # Open in browser (Windows)
        import subprocess
        subprocess.Popen(['cmd', '/c', 'start', '', report_path], shell=True)

    except Exception as e:
        safe_print(f"\n❌ Error durante el escaneo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
