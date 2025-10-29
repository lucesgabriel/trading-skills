# Architecture Overview

## Version 2.2.1 - Pragmatic Temp Script Approach

### Design Philosophy
Following **pragmatic engineering principles** learned from v3.0 failure:
- ✅ **Use what works** - Temp scripts with timestamps and robust cleanup
- ✅ **Debuggable** - Can inspect temp files when errors occur
- ✅ **Reliable** - No bash quote escaping nightmares
- ✅ **Modular design** - Reusable components across skills and tools
- ✅ **Clear separation** - Skills for Claude, tools for CLI
- 🎓 **Learned lesson** - Theoretical purity < Working code

## Data Flow (v2.2.1)

### 1. Market Data Acquisition
**Source:** MetaTrader 5 via MCP server
- `mcp__metatrader__get_symbol_price(symbol)` → Current price dict
- `mcp__metatrader__get_candles_latest(symbol, timeframe, count)` → CSV string (5 parallel calls)

### 2. Pattern Detection
**Module:** `candlestick_scanner.py`
- Parses CSV payloads into structured candle dictionaries
- Validates candle depth (minimum 50 candles per timeframe)
- Detects 12 candlestick patterns across M15/H1/H4/D1
- Computes support/resistance levels
- Captures technical analysis snapshots (RSI, MACD, trend)

### 3. Confluence Calculation
**Module:** `confluence_calculator.py`
- Merges technical scores with pattern counts
- Applies weighted timeframe scoring: D1 (40%), H4 (30%), H1 (20%), M15 (10%)
- Produces final signal (LONG/SHORT/NEUTRAL)
- Calculates probability (25%-90% range)
- Generates detailed breakdowns by timeframe

### 4. Report Generation
**Module:** `html_generator.py`
- Renders vibrant HTML with Tailwind CSS + Chart.js
- Interactive candlestick chart with pattern markers
- Technical indicator visualizations (progress bars with gradients)
- Complete trading setup (Entry/SL/TP1/TP2/TP3)
- Risk management guidance and warnings
- Executive summary with actionable recommendations

### 5. Execution Models

#### A. Claude Code Skill (v2.2.1 - Temp Script with Timestamp)
```python
# Step 1: Generate timestamp
from datetime import datetime
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

# Step 2: Create temp_scan_{timestamp}.py with Write tool
#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from run_scan import run_pattern_scan

mcp_data = {
    "price": {...},
    "candles_m15": """CSV DATA""",
    "candles_h1": """CSV DATA""",
    "candles_h4": """CSV DATA""",
    "candles_d1": """CSV DATA"""
}

report_path = run_pattern_scan("SYMBOL", mcp_data)
print(f"Report: {report_path}")

# Step 3: Execute with guaranteed cleanup
python .claude/skills/pattern-scanner/scripts/temp_scan_{timestamp}.py
del .claude\skills\pattern-scanner\scripts\temp_scan_{timestamp}.py  # Windows
# OR: rm .claude/skills/pattern-scanner/scripts/temp_scan_{timestamp}.py  # Unix
```

**Advantages:**
- ✅ **Works reliably** - No bash quote escaping issues
- ✅ **Handles multiline data** - CSV data stays clean
- ✅ **Debuggable** - Can inspect temp file if errors occur
- ✅ **No collisions** - Timestamp ensures unique filenames
- ✅ **Maintainable** - Clear Python code, not bash magic
- 🎓 **Pragmatic** - Uses what works best, not what's "theoretically pure"

#### B. CLI Tools (Standalone)
```bash
# Single symbol scan
python tools/standalone_scanner.py EURUSD --timeframes M15,H1,H4,D1

# Batch parallel scan
python tools/batch_scanner.py EURUSD GBPUSD XAUUSD --open
```

**Use cases:**
- Automation and scheduling
- Offline analysis with sample data
- Batch processing multiple symbols
- Integration with other systems

## Key Modules
- `candlestick_scanner.py`
  - `prepare_candle_frames`: parse + validate MCP candle data
  - `detect_patterns_all_timeframes`: reuse 12+ detection routines
  - `scan_symbol_for_patterns`: master orchestrator returning patterns, technical snapshots, S/R levels, and timeframe status metadata
- `confluence_calculator.py`
  - `_resolve_score`: backwards compatibility for historical score keys
  - `calculate_pattern_confluence`: per-timeframe adjustments with support/resistance context
  - `enhance_probability_with_patterns`: weighted aggregation plus timeframe breakdown used by HTML and CLI layers
- `html_generator.py`
  - Assembles Tailwind layout, Chart.js datasets, confluence insights, and trading setup cards
- `console_utils.py`
  - `safe_console_output` helper prevents UnicodeEncodeError on Windows consoles
- `tools/standalone_scanner.py`
  - Fetches data (MCP or local samples), runs the core pipeline, persists HTML, and optionally opens browsers
- `tools/batch_scanner.py`
  - Parallel wrapper over `run_scan` for multiple symbols with shared configuration

## Directory Structure (v2.2.1)
```
.claude/skills/
  pattern-scanner/          # v2.2.1 - Refined temp script approach
    SKILL.md               # Skill configuration (name, description, instructions)
    scripts/
      run_scan.py          # Main entry point (run_pattern_scan function)
      candlestick_scanner.py  # Pattern detection logic
      confluence_calculator.py # Weighted probability calculation
      html_generator.py    # HTML report generation
      console_utils.py     # Safe Windows console output
      multi_symbol_scanner.py # Batch scanning support
    resources/
      examples.md          # Usage examples
      pattern_reference.md # Pattern details and reliability
      troubleshooting.md   # Common issues
  technical-analysis/      # Technical indicators (MA, RSI, MACD, etc.)
  opportunity-scanner/     # Multi-symbol market ranking
  risk-management/         # Position sizing and portfolio risk
  backtesting/            # Strategy validation
  advanced-analytics/      # Statistical analysis and correlations

examples/                  # Usage examples
  README.md               # Examples documentation
  quick_start.py          # Minimal example
  quick_scan_example.py   # Quick scan demo
  advanced_example.py     # Advanced configuration
  advanced_analysis_example.py  # Advanced analytics demo
  eurusd_analysis_example.py   # EURUSD comprehensive analysis
  legacy/                 # Historical examples (archived)

tools/                    # Standalone CLI utilities
  standalone_scanner.py   # Single-symbol scanner
  batch_scanner.py        # Parallel multi-symbol scanner

reports/                  # Generated HTML reports (gitignored)

tests/                    # Integration tests
  test_pattern_scanner.py
  test_confluence_calculator.py

docs/                     # Project documentation
  development/            # Development notes
    IMPLEMENTACION_v2.2_COMPLETA.md
    OPTIMIZACION_FLUJO_v2.1.md
    FIX_SESIONES_NUEVAS_RESUMEN.md
    FLUJO_CORRECTO.md
    SOLUCION_SESIONES_NUEVAS.md
  testing/                # Testing guides
    COMO_PROBAR_v2.2.md
    VALIDACION_FINAL.md
  examples/               # Example code references
    example_temp_scan.py  # Historical temp script example (v2.2)
  RESUMEN_OPTIMIZACION.md

Root files:
  README.md               # Main project documentation
  ARCHITECTURE.md         # This file - architecture overview
  requirements.txt        # Python dependencies
  .gitignore             # Git exclusions (reports/, __pycache__, etc.)
  .claude/
    settings.local.json   # MCP server configuration
```

## Extensibility
- Add new patterns by extending the detection list in `candlestick_scanner.py`
- Introduce alternative weighting schemes by adjusting `TIMEFRAME_WEIGHTS` in `confluence_calculator.py`
- Custom HTML widgets can be added in `html_generator.py` (Tailwind utility classes + Chart.js datasets)
- CLI workflows can be scripted on top of `run_scan` to integrate into schedulers or dashboards

## Testing & Validation
- Smoke scripts under `tests/` exercise the pipeline end-to-end with sample data
- Use `python tools/standalone_scanner.py SYMBOL --sample-data` for deterministic regression checks
- Additional pytest fixtures can target `_resolve_score` and pattern detection helpers for unit coverage

## Evolution: v2.2 → v3.0 (Failed) → v2.2.1 (Current)

### v2.2 Approach (Original)
**Implementation:** Created temporary Python scripts
```python
# 1. Write temp_scan.py with embedded data
# 2. Execute: python temp_scan.py
# 3. Delete: del temp_scan.py
```
**Status:** Worked well, but had minor issues (no timestamps, potential collisions)

### v3.0 Approach (EXPERIMENT FAILED)
**Attempted:** Direct function calls via Python one-liner
```bash
# Single command with embedded data
python -c "
import sys
from pathlib import Path
sys.path.insert(0, str(Path('.claude/skills/pattern-scanner/scripts')))
from run_scan import run_pattern_scan

mcp_data = {
    'price': {...},
    'candles_m15': '''CSV DATA''',
    ...
}

report = run_pattern_scan('SYMBOL', mcp_data)
"
```

**Why It Failed (Production Reality):**
1. ❌ **Quote Escaping Hell**
   - Bash uses both ' and " quotes
   - CSV data contains both types of quotes
   - Nested escaping becomes exponentially complex
   - Error: `unexpected EOF while looking for matching quote`

2. ❌ **Multiline Data Problems**
   - CSV data spans 100+ lines per timeframe
   - Bash interprets newlines unpredictably
   - Triple quotes don't work in bash -c context
   - Command becomes unparseable

3. ❌ **Command Length Limits**
   - 100 candles × 4 timeframes = ~50KB of data
   - Bash has command length limits (varies by shell)
   - Unreadable and unmaintainable

4. ❌ **Shell Incompatibility**
   - bash, zsh, cmd.exe, PowerShell all differ
   - No universal syntax that works everywhere
   - Windows vs Unix path differences

**Key Learning:**
> **Dogmatic pursuit of "stateless purity" is wrong.**
> Temporary files that are cleaned up immediately don't violate statelessness.
> **Pragmatism > Theoretical Purity**

### v2.2.1 Approach (Current - Refined and Working)
**Solution:** Temp scripts with timestamps and robust cleanup
```python
# Step 1: Generate timestamp to prevent collisions
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

# Step 2: Create temp_scan_{timestamp}.py with Write tool
# (Clean Python code with embedded data)

# Step 3: Execute with guaranteed cleanup
try:
    subprocess.run(["python", temp_file], ...)
finally:
    os.remove(temp_file)  # Guaranteed cleanup
```

**Benefits:**
- ✅ **Works reliably** - No bash quote escaping issues
- ✅ **Handles multiline data** - CSV data stays clean in Python
- ✅ **Debuggable** - Can inspect temp file if errors occur
- ✅ **No collisions** - Timestamp ensures unique filenames
- ✅ **Maintainable** - Clear Python code, not bash magic
- ✅ **Robust cleanup** - Try-finally ensures deletion
- 🎓 **Pragmatic** - Uses what works best in practice

### Anthropic Best Practices - Reinterpreted

**Original interpretation (v3.0):** "Stateless" = Never create files
**Correct interpretation (v2.2.1):** "Stateless" = No persistent state between invocations

- Temporary files cleaned up immediately = Still stateless
- The Write tool exists precisely for creating temporary scripts
- Implementation details matter less than reliable execution

### Migration Notes
- v3.0 approach abandoned (doesn't work in production)
- v2.2.1 improves upon v2.2 with timestamps and better cleanup
- Existing `run_scan.py` unchanged (no code changes needed)
- Only SKILL.md instructions updated (execution flow)
- CLI tools unaffected (still use standalone_scanner.py)
- v3.0 failure documented in docs/LESSONS_LEARNED.md
