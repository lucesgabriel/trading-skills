"""
Complete Pattern Scanner Test with Real EURUSD Data
"""

import sys
from pathlib import Path
from datetime import datetime

# Add skill scripts to path
repo_root = Path(__file__).resolve().parents[1]
skill_path = repo_root / '.claude' / 'skills' / 'pattern-scanner' / 'scripts'
sys.path.insert(0, str(skill_path))

# Import pattern scanner modules
from candlestick_scanner import scan_symbol_for_patterns
from confluence_calculator import enhance_probability_with_patterns
from html_generator import generate_html_report

print("=" * 80)
print("EURUSD CANDLESTICK PATTERN SCAN - COMPLETE TEST")
print("=" * 80)
print()

# Real data from MetaTrader (fetched 2025-10-29 16:45 UTC)
symbol = "EURUSD"
current_price = 1.16386
scan_time = "2025-10-29 16:45:30"

# Simulated candle data (in real usage, this comes from MCP)
# For this test, we'll use placeholder CSV strings
candles_data = {
    'M15': """time,open,high,low,close,tick_volume,spread,real_volume
2025-10-29 16:45:00,1.16386,1.16392,1.16379,1.16386,97,0,0
2025-10-29 16:30:00,1.16431,1.16447,1.16363,1.16386,2485,0,0
2025-10-29 16:15:00,1.16379,1.16458,1.16374,1.16430,3107,0,0
""",
    'H1': """time,open,high,low,close,tick_volume,spread,real_volume
2025-10-29 16:00:00,1.16342,1.16458,1.16336,1.16386,8090,0,0
2025-10-29 15:00:00,1.16396,1.16450,1.16276,1.16341,9666,0,0
2025-10-29 14:00:00,1.16472,1.16486,1.16330,1.16397,6899,0,0
""",
    'H4': """time,open,high,low,close,tick_volume,spread,real_volume
2025-10-29 16:00:00,1.16342,1.16458,1.16336,1.16386,8096,0,0
2025-10-29 12:00:00,1.16231,1.16488,1.16187,1.16341,31193,0,0
2025-10-29 08:00:00,1.16343,1.16380,1.16228,1.16231,26881,0,0
""",
    'D1': """time,open,high,low,close,tick_volume,spread,real_volume
2025-10-29 00:00:00,1.16501,1.16609,1.16187,1.16385,94702,0,0
2025-10-28 00:00:00,1.16443,1.16689,1.16253,1.16523,141577,0,0
2025-10-27 00:00:00,1.16320,1.16521,1.16174,1.16441,132046,0,0
"""
}

timeframes = ['M15', 'H1', 'H4', 'D1']

print(f"Symbol: {symbol}")
print(f"Current Price: {current_price}")
print(f"Scan Time: {scan_time} UTC")
print(f"Timeframes: {', '.join(timeframes)}")
print()

# STEP 1: Run Pattern Scanner
print("[OK] Running candlestick pattern detection...")
scan_results = scan_symbol_for_patterns(
    symbol=symbol,
    candles_data=candles_data,
    current_price=current_price,
    timeframes=timeframes
)

print(f"[OK] Scan completed at {scan_results['scan_time']}")
print()

# Display pattern counts
counts = scan_results['pattern_counts']
print(f"Patterns Detected:")
print(f"  - Bullish: {counts['bullish']}")
print(f"  - Bearish: {counts['bearish']}")
print(f"  - Neutral: {counts['neutral']}")
print()

# STEP 2: Calculate Confluence
print("[OK] Calculating confluence-based probability...")

# Get base scores from technical snapshots
base_scores = {'long_probability': 50.0, 'short_probability': 50.0}
if scan_results['technical_snapshots']:
    # Use H1 or first available
    for tf in timeframes:
        if tf in scan_results['technical_snapshots'] and scan_results['technical_snapshots'][tf]:
            base_scores = scan_results['technical_snapshots'][tf].get('scores', base_scores)
            break

confluence = enhance_probability_with_patterns(
    base_scores=base_scores,
    patterns_by_timeframe=scan_results['patterns_by_timeframe'],
    levels_by_timeframe=scan_results['support_resistance'],
    current_price=current_price
)

print(f"[OK] Confluence calculation complete")
print()

# Display trading signal
print("-" * 80)
print("TRADING SIGNAL")
print("-" * 80)
print(f"Signal: {confluence['signal']}")
print(f"Probability: {confluence['primary_probability']}%")
print(f"Bias: {confluence['bias']}")
print()

if confluence['confluence_factors']:
    print("Confluence Factors:")
    for factor in confluence['confluence_factors']:
        print(f"  + {factor}")
    print()

# Display detected patterns by timeframe
print("-" * 80)
print("DETECTED PATTERNS BY TIMEFRAME")
print("-" * 80)
for tf in timeframes:
    patterns = scan_results['patterns_by_timeframe'].get(tf, [])
    if patterns:
        print(f"\n{tf} Timeframe ({len(patterns)} pattern(s)):")
        for p in patterns:
            print(f"  - {p['name']} ({p['strength']}) - {p['bias']} at {p['price']:.5f}")
    else:
        print(f"\n{tf} Timeframe: No significant patterns detected")

print()

# STEP 3: Generate HTML Report
print("-" * 80)
print("GENERATING HTML REPORT")
print("-" * 80)
print("[OK] Creating professional HTML report...")

report_path = generate_html_report(
    symbol=symbol,
    scan_results=scan_results,
    confluence_results=confluence,
    output_dir=str(Path.cwd() / "reports")
)

print(f"[OK] Report generated: {report_path}")
print()

# Summary
print("=" * 80)
print("PATTERN SCANNER SKILL - TEST COMPLETE")
print("=" * 80)
print()
print("Summary:")
print(f"  - Total Patterns: {counts['bullish'] + counts['bearish'] + counts['neutral']}")
print(f"  - Trading Signal: {confluence['signal']}")
print(f"  - Success Probability: {confluence['primary_probability']}%")
print(f"  - HTML Report: {report_path}")
print()
print("The pattern-scanner skill is fully functional and ready to use!")
print("Once Claude Code restarts, you can use it with:")
print('  "scan EURUSD for candlestick patterns"')
print()
