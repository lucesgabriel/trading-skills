---
name: pattern-scanner
description: Detects candlestick patterns (Morning Star, Engulfing, Hammer, Doji, Harami, Three Soldiers/Crows, Shooting Star, Spinning Top) across M15/H1/H4/D1 timeframes with weighted probability scoring and generates educational HTML reports with vibrant design. Use when user asks to scan, analyze patterns, find signals, or assess trading opportunities for forex symbols like EURUSD, GBPUSD, XAUUSD.
---

# Pattern Scanner

Professional candlestick pattern detection system with AI-powered analysis and educational HTML reports.

## What This Skill Does

Automatically detects 12 classic candlestick patterns across multiple timeframes, calculates weighted confluence probability, and generates comprehensive educational HTML reports with:

- Colorful visual pattern cards with detailed explanations
- Interactive candlestick charts (Chart.js)
- Technical indicator analysis (RSI, MACD, trend)
- Complete trading setup (Entry/SL/TP1/TP2/TP3)
- Risk management guidance with position sizing
- Executive summary and step-by-step recommendations
- Professional vibrant design (purple/blue gradients)

## When Claude Should Use This

Trigger this skill when user:
- Requests: "scan [SYMBOL]" or "scan [SYMBOL] for patterns"
- Asks: "analyze [SYMBOL]" or "what patterns does [SYMBOL] have?"
- Wants: "trading signals for [SYMBOL]" or "[SYMBOL] technical analysis"
- Mentions: candlestick analysis, pattern detection, or trading opportunities for forex/commodities

## Pattern Types Detected

**Reversal Patterns**:
- Morning Star / Evening Star (80% reliability) - Very Strong
- Bullish / Bearish Engulfing (75% reliability) - Strong
- Hammer / Shooting Star (70% reliability) - Strong
- Bullish / Bearish Harami (65% reliability) - Medium

**Continuation Patterns**:
- Three White Soldiers / Three Black Crows (80% reliability) - Very Strong

**Indecision Patterns**:
- Doji (55% reliability) - Medium
- Spinning Top (50% reliability) - Weak

## Technical Capabilities

- **Multi-Timeframe Analysis**: M15, H1, H4, D1 (extensible to custom timeframes)
- **Weighted Confluence**: D1=40%, H4=30%, H1=20%, M15=10%
- **Probability Scoring**: Pattern strength adjustments (Very Strong +15%, Strong +12%, Medium +10%)
- **S/R Context Bonus**: +10% when patterns form near support/resistance levels
- **Range**: 25%-90% probability with intelligent clamping
- **Educational HTML Reports**: Vibrant purple/blue gradient design, detailed explanations
- **CLI Tools**: Standalone and batch scanners for automation
- **Safe Console Output**: Windows UTF-8 encoding handled automatically

## Usage
When the user requests automated pattern analysis (for example: "scan EURUSD for patterns", "analyse XAUUSD candlesticks", "generate pattern report for GBPUSD"), call this skill without further questions.

### Prompt Template
```
scan {SYMBOL} for candlestick patterns
```
Optional arguments:
- `timeframes`: comma separated string (default: `M15,H1,H4,D1`)
- `minCandles`: override minimum candles per timeframe (default: 50)

## Inputs
- `symbol` (str; required): trading symbol supported by MetaTrader
- `timeframes` (List[str]; optional): defaults to `['M15','H1','H4','D1']`
- `minCandles` (int; optional): minimum candles required per timeframe (default 50)

## Outputs

**Console Summary**:
- Signal direction (LONG/SHORT/NEUTRAL)
- Probability percentage (25%-90%)
- Pattern counts (bullish/bearish/neutral)
- Report file path

**HTML Report** (`reports/{symbol}_pattern_scan_{timestamp}.html`):
- **Vibrant Design**: Purple/blue gradient background, white container
- **Summary Stats**: Pattern count, probability, signal, R/R ratio
- **Pattern Cards**: Color-coded with emoji, explanations, timeframe badges
- **Candlestick Chart**: Interactive Chart.js visualization (last 100 candles)
- **Technical Indicators**: RSI, MACD, Stochastic, trend analysis with visual meters
- **S/R Table**: Support/resistance levels with distances in pips
- **Trading Signal**: Large signal box with probability
- **Trading Setup**: Entry, SL, TP1/TP2/TP3 with pip calculations
- **Risk Management**: Position sizing for different account sizes, risk rules
- **Warnings**: Risk factors and invalidation signals
- **Executive Summary**: Final recommendation with step-by-step guidance
- **Educational Content**: Detailed pattern explanations, confluence factors

**Browser**: Automatically opened (CLI tools) or path displayed (Claude Code)

## Dependencies
- MetaTrader 5 MCP server with permissions:
  - `mcp__metatrader__get_symbol_price`
  - `mcp__metatrader__get_candles_latest`
- `.claude/skills/technical-analysis` for indicator snapshots
- Python packages: `pandas`, `numpy`, `chart.js` via CDN (HTML)

## Side Effects
- Creates timestamped HTML files under `reports/`
- Prints warnings when data is missing or fails validation
- Optional browser open via `webbrowser.open` (CLI tools)

## Error Handling
- Timeframes with fewer than 50 candles are skipped and annotated in `timeframe_status`
- Fallback to 50/50 probabilities if technical-analysis snapshots are unavailable
- Safe console printing prevents UnicodeEncodeError on Windows terminals

## CLI Utilities
- `python tools/standalone_scanner.py EURUSD --timeframes M15,H1,H4` (single symbol)
- `python tools/batch_scanner.py EURUSD GBPUSD XAUUSD --open` (parallel scan)
Both commands accept `--sample-data` or `--sample-dir` for offline fixtures.

## Troubleshooting
| Issue | Cause | Resolution |
| --- | --- | --- |
| `insufficient_data` status | MCP returned fewer candles than required | Increase `minCandles` or request more history from MetaTrader |
| No technical snapshots | `technical-analysis` skill missing | Install dependencies then reload the skill |
| HTML lacks candles | Market data missing for chosen timeframe | Confirm MCP permissions and that MetaTrader terminal is connected |

## Execution Instructions

When user requests a pattern scan (e.g., "scan EURUSD"), follow these 4 simple steps:

### Step 1: Fetch Market Data from MCP
Make 5 parallel MCP calls to fetch live data:
```
mcp__metatrader__get_symbol_price(symbol_name: "EURUSD")
mcp__metatrader__get_candles_latest(symbol_name: "EURUSD", timeframe: "M15", count: 100)
mcp__metatrader__get_candles_latest(symbol_name: "EURUSD", timeframe: "H1", count: 100)
mcp__metatrader__get_candles_latest(symbol_name: "EURUSD", timeframe: "H4", count: 100)
mcp__metatrader__get_candles_latest(symbol_name: "EURUSD", timeframe: "D1", count: 100)
```

### Step 2: Create Temporary Python Script with Timestamp
Use Write tool to create `.claude/skills/pattern-scanner/scripts/temp_scan_{timestamp}.py`:

**Generate timestamp first:**
```python
from datetime import datetime
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
```

**Then create the temp script:**
```python
#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from run_scan import run_pattern_scan

# MCP data embedded directly (no JSON file needed)
mcp_data = {
    "price": {"bid": 1.16412, "ask": 1.16412, "last": 0.0, "volume": 0, "time": "2025-10-29T21:19:52Z"},
    "candles_m15": """time,open,high,low,close,tick_volume,spread,real_volume
99,2025-10-29 21:15:00+00:00,1.16354,1.16441,1.1635,1.16412,1204,0,0
...INSERT FULL M15 CSV DATA HERE...""",
    "candles_h1": """time,open,high,low,close,tick_volume,spread,real_volume
99,2025-10-29 21:00:00+00:00,1.16468,1.16511,1.16343,1.16412,5930,0,0
...INSERT FULL H1 CSV DATA HERE...""",
    "candles_h4": """time,open,high,low,close,tick_volume,spread,real_volume
99,2025-10-29 20:00:00+00:00,1.16573,1.16591,1.16343,1.16411,12297,0,0
...INSERT FULL H4 CSV DATA HERE...""",
    "candles_d1": """time,open,high,low,close,tick_volume,spread,real_volume
99,2025-10-29 00:00:00+00:00,1.16501,1.16659,1.16187,1.16409,136741,0,0
...INSERT FULL D1 CSV DATA HERE..."""
}

report_path = run_pattern_scan("EURUSD", mcp_data)
print(f"\n✅ Scan complete! Report: {report_path}")
```

**Important Notes:**
- Replace `{timestamp}` with actual timestamp value (e.g., `20251029_163045`)
- Replace `"EURUSD"` with actual symbol
- Replace price dict with actual MCP price data
- Replace CSV placeholders with full CSV strings from MCP (including header)
- Use triple quotes `"""..."""` for multiline CSV strings
- Do NOT remove the header row from CSV data

**Why Temp Files (Not Python One-Liner):**
- ✅ **Works reliably** - No bash quote escaping nightmares
- ✅ **Handles multiline data** - CSV data stays clean
- ✅ **Debuggable** - Can inspect temp file if errors occur
- ✅ **Maintainable** - Clear Python code, not bash magic
- ✅ **No collisions** - Timestamp ensures unique filenames
- 📚 **Pragmatic** - Temp files are fine when they work best

### Step 3: Execute Scanner with Guaranteed Cleanup
Use a try-finally pattern to ensure cleanup happens:

```python
# Store the temp file path
temp_file = f".claude/skills/pattern-scanner/scripts/temp_scan_{timestamp}.py"

try:
    # Execute the scanner
    import subprocess
    result = subprocess.run(
        ["python", temp_file],
        capture_output=True,
        text=True,
        timeout=120
    )

    # Display output
    print(result.stdout)

    if result.returncode != 0:
        print("Error:", result.stderr)

finally:
    # Guaranteed cleanup - delete temp file
    import os
    try:
        os.remove(temp_file)
    except Exception as e:
        print(f"Warning: Could not delete temp file: {e}")
```

**Or simpler bash approach (Windows):**
```bash
python .claude/skills/pattern-scanner/scripts/temp_scan_20251029_163045.py
del .claude\skills\pattern-scanner\scripts\temp_scan_20251029_163045.py
```

**Or bash (Linux/Mac):**
```bash
python .claude/skills/pattern-scanner/scripts/temp_scan_20251029_163045.py && rm .claude/skills/pattern-scanner/scripts/temp_scan_20251029_163045.py
```

### Step 4: Report Results to User
The scanner will output:
- ✅ Patterns detected count
- 💡 Signal (LONG/SHORT/NEUTRAL) with bias
- 📈 Probability percentage
- 📁 HTML report path

The HTML report opens automatically in the browser with:
- Vibrant purple/violet design
- Pattern cards with emojis and explanations
- Interactive candlestick chart
- Technical indicators
- Trading setup (Entry/SL/TP)
- Risk management guidance
- Executive summary

## Change Log
- 2025-10-29 (v2.2.1): **Temp script approach refined with robust improvements**
  - Added timestamp to temp filenames: `temp_scan_{timestamp}.py` (prevents collisions)
  - Documented try-finally cleanup pattern for guaranteed file deletion
  - Improved error handling and debugging capability
  - **Lesson learned:** v3.0 Python one-liner approach FAILED in production
    - Problems: Quote escaping hell, multiline data issues, shell incompatibility
    - Reality: Temp files are pragmatic and acceptable when they work best
    - Philosophy: **Pragmatism > Theoretical Purity**
- 2025-10-29 (v3.0): **EXPERIMENT FAILED** - Python one-liner doesn't work in practice
  - Attempted: Direct function call without temp files
  - Failed due to: bash quote escaping, multiline CSV data, command length limits
  - Key learning: Dogmatic "stateless" purity is wrong. Use what works.
- 2025-10-29 (v2.2): Fixed new session failures - Temp Python script approach
- 2025-10-29 (v2.1): Flow Optimization - run_scan.py accepts both JSON formats
- 2025-10-29 (v2.0): Complete redesign - Vibrant HTML reports, 3 new sections
- 2025-10-29: Added run_scan.py direct entry point
- 2025-10-29: Complete HTML rewrite with vibrant design (purple/violet gradients)
- 2025-10-29: Added 3 NEW sections (Risk Management, Warnings, Executive Summary)
- 2025-10-29: Added timeframe weighting, revamped HTML report (Chart.js + Tailwind)
- 2025-10-29: Introduced safe console output and backward compatibility
