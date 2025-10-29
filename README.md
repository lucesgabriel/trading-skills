# Trading Pattern Scanner for Claude Code

[![Status](https://img.shields.io/badge/status-production-green)]()
[![Python](https://img.shields.io/badge/python-3.10+-blue)]()
[![MetaTrader](https://img.shields.io/badge/MetaTrader-5-orange)]()

Professional candlestick pattern detection with **vibrant educational HTML reports**, multi-timeframe analysis, and comprehensive trading setups.

## Overview
This repository contains a suite of Claude Code skills tailored for discretionary and systematic traders. The centerpiece is the **Pattern Scanner**, which delivers weighted probability scoring, robust data validation, and a beautiful educational HTML experience with vibrant design. Companion skills cover technical analysis, opportunity scanning, risk management, and backtesting, all designed to work with MetaTrader 5 MCP servers.

## Skill Lineup
- **Pattern Scanner** – multi-timeframe candlestick detection, probability scoring, and HTML reporting
- **Technical Analysis** – indicator snapshots, confluence scoring, and trend diagnostics
- **Opportunity Scanner** – multi-symbol ranking with probability filters
- **Risk Management** – position sizing and trade management utilities
- **Backtesting & Advanced Analytics** – strategy validation and statistical tooling

## Features

### Pattern Detection
- **12 Candlestick Patterns**: Bullish/Bearish Engulfing, Morning/Evening Star, Hammer, Shooting Star, Doji, Harami, Three Soldiers/Crows, Spinning Top
- **Multi-Timeframe Analysis**: M15, H1, H4, D1 with weighted confluence
- **Probability Scoring**: Weighted confluence D1 (40%), H4 (30%), H1 (20%), M15 (10%)
- **Data Validation**: Ensures >= 50 candles before processing each timeframe

### Beautiful HTML Reports
- **Vibrant Design**: Purple/violet gradient background (#667eea → #764ba2) with white container
- **Educational Content**: Each pattern includes emoji and detailed explanation
- **Interactive Charts**: Chart.js candlestick visualization with pattern markers
- **Progress Bars**: Gradient-filled indicators for RSI, MACD, Stochastic
- **Comprehensive Sections**:
  - Summary Stats (4 stat boxes)
  - Pattern Cards with emojis and gradients (green for bullish, red for bearish)
  - Technical Indicators with visual progress bars
  - Support/Resistance table
  - Trading Signal (large, prominent box)
  - Complete Trading Setup (Entry/SL/TP1/TP2/TP3)
  - **Risk Management** (NEW: position sizing, rules)
  - **Warnings & Risk Factors** (NEW: invalidation signals)
  - **Executive Summary** (NEW: final recommendation)
  - Disclaimer

### Technical Analysis
- **Indicator Meters**: RSI, MACD, Stochastic, Trend analysis
- **Support/Resistance**: Auto-calculated S/R levels with pip distances
- **Trading Setup**: Auto-generated entry points, stop loss, take profits with risk:reward ratios
- **Position Sizing**: Calculated for different account sizes ($10k, $1k)

### Safety & Reliability
- **Unicode-Safe Output**: Prevents encoding errors on Windows terminals
- **Safe Print Function**: Automatic fallback for console incompatibilities
- **Error Handling**: Robust validation and graceful degradation

## Quick Start

### Via Claude Code (Recommended)
```
scan EURUSD for patterns
```

Claude will automatically:
1. Fetch live price data from MetaTrader 5
2. Analyze candlestick patterns across M15, H1, H4, D1 timeframes
3. Calculate confluence scores and probabilities
4. Generate a beautiful HTML report in `reports/`
5. Open the report automatically

### Via Python
```bash
# Quick analysis
python examples/quick_start.py EURUSD

# Advanced multi-symbol scan
python examples/advanced_example.py

# Batch scanning
python tools/batch_scanner.py EURUSD GBPUSD XAUUSD --open
```

### MCP Configuration
Enable required MCP permissions in `.claude/settings.local.json`:
```json
{
  "enableAllProjectMcpServers": true,
  "enabledMcpjsonServers": ["metatrader"],
  "permissions": {
    "allow": [
      "mcp__metatrader__get_symbol_price",
      "mcp__metatrader__get_candles_latest"
    ]
  }
}
```

Then restart Claude Code to load the updated skills.

## CLI Tools
- `python tools/standalone_scanner.py EURUSD --timeframes M15,H1,H4,D1`
  - Optional `--sample-data path/to/EURUSD.json` to run offline fixtures
- `python tools/batch_scanner.py EURUSD GBPUSD XAUUSD --open`
  - Optional `--sample-dir data/samples` for per-symbol JSON inputs

Both commands write reports to `reports/` and reuse the same core modules as the skill.

## Repository Layout
```
.claude/skills/
  pattern-scanner/       # Candlestick pattern detection (v2.2.1 - refined temp script approach)
    scripts/             # Core detection, confluence, HTML generation
    resources/           # Documentation and troubleshooting
  technical-analysis/    # Technical indicators and analysis
  opportunity-scanner/   # Multi-symbol market scanning
  risk-management/       # Position sizing and portfolio risk
  backtesting/          # Strategy validation with historical data
  advanced-analytics/    # Statistical analysis and correlations
examples/               # Usage examples (see examples/README.md)
  legacy/              # Historical examples for reference
reports/               # Generated HTML reports (gitignored)
tests/                 # Integration tests
tools/                 # Standalone CLI scanners (batch and single-symbol)
docs/                  # Project documentation
  development/         # Development notes and implementation details
  testing/             # Testing guides and validation
  examples/            # Example code and references
```

## Requirements
- Python 3.10+
- Dependencies: Install via `pip install -r requirements.txt`
  - pandas >= 2.0.0
  - numpy >= 1.24.0
- MetaTrader 5 terminal running and connected to the MCP server
- Claude Code CLI v2 or later

### Installation
```bash
# Install Python dependencies
pip install -r requirements.txt

# Configure MCP server
# Edit .claude/settings.local.json to enable MetaTrader MCP server
# See MCP Configuration section above

# Restart Claude Code to load skills
```

## Example Output

When you run a pattern scan, you'll get:

**Console Output:**
```
📊 Escaneando EURUSD para patrones de velas...
✅ Patrones detectados: 2
💡 Señal: BUY (LONG) - BULLISH
📈 Probabilidad: 68%
📊 Reporte HTML generado: reports/EURUSD_pattern_scan_20251029_140610.html
```

**HTML Report:**
- Vibrant purple/violet gradient background
- Large price display with color coding (green for up, red for down)
- 4 summary stat boxes
- Pattern cards with emojis (🔥 for Bullish Engulfing, 📈 for Bullish Harami, etc.)
- Interactive candlestick chart
- Progress bars with gradients for all indicators
- Complete trading setup with Entry/SL/TP1/TP2/TP3
- Risk management guidance
- Warnings and invalidation signals
- Executive summary with final recommendation

## Documentation

- `.claude/skills/pattern-scanner/SKILL.md` - Skill configuration and triggers
- `.claude/skills/pattern-scanner/resources/pattern_reference.md` - Pattern details
- `.claude/skills/pattern-scanner/resources/troubleshooting.md` - Common issues
- `examples/` - Example scripts and usage patterns

## Changelog

### 2025-10-29 (v2.2.1 - Pragmatic Refinement)
**Learning from v3.0 Failure + Project Optimization**
- ✅ **Temp script approach refined** - Added timestamps, robust cleanup, better error handling
- ✅ **Organized project structure** - Created docs/ hierarchy (development/, testing/, examples/)
- ✅ **Cleaned root directory** - Removed 4 obsolete test scripts
- ✅ **Consolidated examples** - Moved legacy examples to examples/legacy/
- ✅ **Added requirements.txt** - Proper dependency management
- ✅ **Updated .gitignore** - Added skills __pycache__ and temp files exclusions
- ✅ **Improved documentation** - Created examples/README.md, LESSONS_LEARNED.md
- 🎓 **Key learning:** v3.0 Python one-liner FAILED in production
  - Problems: Quote escaping, multiline data, shell incompatibility
  - Lesson: **Pragmatism > Theoretical Purity**
  - Reality: Temp files are acceptable when they're the best solution
- 📚 **Documentation reorganization** - All Spanish docs moved to docs/ structure

### 2025-10-29 (v3.0 - EXPERIMENT FAILED)
**Attempted:** Eliminate temp files with Python one-liners
**Result:** Failed due to bash quote escaping nightmares, multiline CSV issues, command length limits
**Lesson:** Don't chase theoretical purity. Use what works reliably.

### 2025-10-29 (v2.2 - Session 2)
**Complete HTML rewrite with vibrant design**
- Adopted purple/violet gradient background (#667eea → #764ba2)
- Added pattern emojis and educational explanations
- Implemented 3 NEW sections: Risk Management, Warnings, Executive Summary
- Progress bars now use gradients (90deg)
- Pattern cards with color gradients (green/red/orange)
- Large, prominent signal box
- Unicode-safe console output with safe_print()

### 2025-10-29 (v2.1 - Session 1)
**Reworked pattern-scanner architecture**
- Fixed Unicode encoding bugs
- Added examples (`quick_start.py`, `advanced_example.py`)
- Improved project structure
- Added `.gitignore`
- Optimized SKILL.md with Anthropic best practices

## Disclaimer

This analysis is for **educational purposes only** and does not constitute financial advice. Candlestick patterns and technical analysis are probabilistic, not guarantees. Forex trading involves significant risk of loss. Always trade with capital you can afford to lose and use proper risk management. Past results do not guarantee future performance. Consult with a qualified financial advisor before making investment decisions.
