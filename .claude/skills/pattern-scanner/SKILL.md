---
name: pattern-scanner
description: Use when detecting candlestick patterns, scanning forex symbols for trading signals, or analyzing chart formations across multiple timeframes.
version: 2.2.1
tags: [trading, patterns, candlestick, forex, technical-analysis, reversal, engulfing, doji, hammer]
category: market-analysis
requires:
  mcp:
    - mcp__metatrader__get_symbol_price
    - mcp__metatrader__get_candles_latest
  skills:
    - technical-analysis
difficulty: intermediate
estimated_time: 30-60s
output_format: [console, html]
author: Gabriel Luces
repository: https://github.com/lucesgabriel/trading-skills
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

## When to Use This Skill

**Primary Triggers:**
- "scan [SYMBOL]" or "scan [SYMBOL] for patterns"
- "detect patterns on [SYMBOL]"
- "what patterns are forming on [SYMBOL]?"
- "find candlestick setups for [SYMBOL]"

**Use Cases:**
- User wants to identify candlestick patterns across multiple timeframes
- User needs trading signals based on pattern formations
- User asks for pattern-based trading opportunities
- User wants visual HTML report with pattern analysis

**Example Inputs:**
```
✓ "scan EURUSD for patterns"
✓ "what candlestick patterns are on GBPUSD?"
✓ "detect reversal patterns in XAUUSD"
✓ "find trading setups for USDJPY"
✗ "analyze EURUSD indicators" → Use technical-analysis skill instead
```

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

When user requests a pattern scan, follow this 3-step workflow:

### Step 1: Fetch Market Data from MCP

Make 5 parallel MCP calls:
```
price_data = mcp__metatrader__get_symbol_price(symbol_name: "EURUSD")
m15_data = mcp__metatrader__get_candles_latest(symbol_name: "EURUSD", timeframe: "M15", count: 100)
h1_data = mcp__metatrader__get_candles_latest(symbol_name: "EURUSD", timeframe: "H1", count: 100)
h4_data = mcp__metatrader__get_candles_latest(symbol_name: "EURUSD", timeframe: "H4", count: 100)
d1_data = mcp__metatrader__get_candles_latest(symbol_name: "EURUSD", timeframe: "D1", count: 100)
```

### Step 2: Create Temporary Python Script

Use Write tool to create `.claude/skills/pattern-scanner/scripts/temp_scan_{timestamp}.py` with this **EXACT** template:

```python
#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from run_scan import run_pattern_scan

# Extract CSV strings from MCP responses
csv_m15 = m15_data["result"] if isinstance(m15_data, dict) else m15_data
csv_h1 = h1_data["result"] if isinstance(h1_data, dict) else h1_data
csv_h4 = h4_data["result"] if isinstance(h4_data, dict) else h4_data
csv_d1 = d1_data["result"] if isinstance(d1_data, dict) else d1_data

# Prepare MCP data in correct format
mcp_data = {
    "price": price_data,              # Full price dict from get_symbol_price
    "candles_m15": csv_m15,           # CSV string from get_candles_latest
    "candles_h1": csv_h1,             # CSV string from get_candles_latest
    "candles_h4": csv_h4,             # CSV string from get_candles_latest
    "candles_d1": csv_d1              # CSV string from get_candles_latest
}

# Run scanner - MUST pass symbol AND mcp_data
report_path = run_pattern_scan("EURUSD", mcp_data)
print(f"\\n✅ Report: {report_path}")
```

**CRITICAL:** Replace variables (m15_data, h1_data, etc.) with actual MCP response data using `repr()`.

### Step 3: Execute and Cleanup

```bash
# Execute (Windows)
python .claude/skills/pattern-scanner/scripts/temp_scan_{timestamp}.py

# Cleanup (Windows)
del .claude\skills\pattern-scanner\scripts\temp_scan_{timestamp}.py
```

**Important Notes:**
- ✅ Import is `from run_scan import run_pattern_scan` (NOT from pattern_scanner)
- ✅ Keys must be `candles_m15`, `candles_h1`, `candles_h4`, `candles_d1` (with candles_ prefix)
- ✅ Function call is `run_pattern_scan(symbol, mcp_data)` (pass symbol separately)
- ✅ MCP returns CSV in dict with "result" key - extract it first

For detailed explanation, see [Execution Guide](resources/execution-guide.md).

## Version History

See [CHANGELOG](resources/CHANGELOG.md) for complete version history.

**Current Version:** v2.2.1 (Optimized temp script approach with timestamp collision prevention)
