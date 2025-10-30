# Execution Instructions

When user requests a pattern scan (e.g., "scan EURUSD"), follow these 3 simple steps:

## Step 1: Fetch Market Data from MCP

Make 5 parallel MCP calls to fetch live data:
```
mcp__metatrader__get_symbol_price(symbol_name: "EURUSD")
mcp__metatrader__get_candles_latest(symbol_name: "EURUSD", timeframe: "M15", count: 100)
mcp__metatrader__get_candles_latest(symbol_name: "EURUSD", timeframe: "H1", count: 100)
mcp__metatrader__get_candles_latest(symbol_name: "EURUSD", timeframe: "H4", count: 100)
mcp__metatrader__get_candles_latest(symbol_name: "EURUSD", timeframe: "D1", count: 100)
```

## Step 2: Create Temporary Python Script

Create a temporary Python file with embedded MCP data. This is the most reliable method for large datasets.

**Use Write tool to create a temp file:**

```python
from datetime import datetime

# Generate unique timestamp
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
temp_file = f".claude/skills/pattern-scanner/scripts/temp_scan_{timestamp}.py"

# Prepare MCP data
mcp_data = {
    "price": {
        "bid": 1.16412,  # From get_symbol_price
        "ask": 1.16412,
        "last": 0.0,
        "volume": 0,
        "time": "2025-10-29T21:19:52Z"
    },
    "candles_m15": "FULL CSV STRING",  # From get_candles_latest M15
    "candles_h1": "FULL CSV STRING",   # From get_candles_latest H1
    "candles_h4": "FULL CSV STRING",   # From get_candles_latest H4
    "candles_d1": "FULL CSV STRING"    # From get_candles_latest D1
}

# Create temp script content
script_content = f'''#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from run_scan import run_pattern_scan

# MCP data embedded
mcp_data = {repr(mcp_data)}

# Run scanner
report_path = run_pattern_scan("EURUSD", mcp_data)
print(f"\\n✅ Report: {{report_path}}")
'''

# Write temp file using Write tool
# Write(temp_file, script_content)
```

**Important Notes:**
- ✅ **Timestamp:** Use unique timestamp to prevent file collisions
- ✅ **repr():** Use `repr(mcp_data)` to properly escape all strings
- ✅ **CSV Format:** MCP returns CSV in two formats - both are supported:
  ```python
  # Format 1: Direct string
  "candles_m15": ",time,open,high,low,close...\n99,2025-10-30..."

  # Format 2: Dict with 'result' key
  "candles_m15": {"result": ",time,open,high,low,close...\n99,2025-10-30..."}
  ```
- ✅ **Extract CSV:** If MCP returns dict format, extract the string:
  ```python
  csv_m15 = mcp_m15["result"] if isinstance(mcp_m15, dict) else mcp_m15
  ```

## Step 3: Execute Script and Cleanup

After creating the temp file, execute it and clean up:

```bash
# Execute the scanner (Windows)
python .claude/skills/pattern-scanner/scripts/temp_scan_20251030_123456.py

# Cleanup temp file (Windows)
del .claude\skills\pattern-scanner\scripts\temp_scan_20251030_123456.py
```

**Or in one line (Windows):**
```bash
python .claude/skills/pattern-scanner/scripts/temp_scan_20251030_123456.py && del .claude\skills\pattern-scanner\scripts\temp_scan_20251030_123456.py
```

**Linux/Mac:**
```bash
python .claude/skills/pattern-scanner/scripts/temp_scan_20251030_123456.py && rm .claude/skills/pattern-scanner/scripts/temp_scan_20251030_123456.py
```

**Programmatic cleanup (recommended):**
```python
import subprocess
import os

# Execute
result = subprocess.run(
    ["python", temp_file],
    capture_output=True,
    text=True,
    cwd="D:/Programing Language html css js php DB/28102025"
)

# Display output
print(result.stdout)
if result.stderr:
    print("Errors:", result.stderr)

# Cleanup
try:
    os.remove(temp_file)
except Exception as e:
    print(f"Warning: Could not delete temp file: {e}")
```

## Step 4: Display Results to User

The scanner outputs to console:
```
📊 Escaneando EURUSD para patrones de velas...
============================================================
💰 Precio actual: 1.16412
✓ M15: 100 velas cargadas
✓ H1: 100 velas cargadas
✓ H4: 100 velas cargadas
✓ D1: 100 velas cargadas

🔍 Detectando patrones...
🧮 Calculando confluencia...

============================================================
✅ Patrones detectados: 5
💡 Señal: LONG - ALCISTA
📈 Probabilidad: 68.5%
============================================================

📝 Generando reporte HTML...
✅ Reporte generado: D:\...\reports\EURUSD_pattern_scan_20251029_221303.html
```

**HTML Report Features:**
- 🎨 Vibrant purple/violet gradient design
- 📊 Pattern cards with emojis and detailed explanations
- 📈 Interactive candlestick charts (Chart.js)
- 🔍 Technical indicators (RSI, MACD, Stochastic)
- 💰 Complete trading setup (Entry/SL/TP1/TP2/TP3)
- 🛡️ Risk management recommendations
- ⚠️ Warning signals and invalidation conditions
- 📋 Executive summary with step-by-step guidance

## Alternative Method: Direct Python Import (Advanced)

For small datasets or scripting environments, you can use direct import:

```python
import sys
sys.path.insert(0, ".claude/skills/pattern-scanner/scripts")
from run_scan import run_pattern_scan

# Prepare MCP data (must be small enough for inline code)
mcp_data = {
    "price": {...},
    "candles_m15": "CSV string",
    "candles_h1": "CSV string",
    "candles_h4": "CSV string",
    "candles_d1": "CSV string"
}

report_path = run_pattern_scan("EURUSD", mcp_data)
print(f"✅ Report: {report_path}")
```

**Limitations:**
- ❌ Doesn't work well with large datasets (100+ candles × 4 timeframes)
- ❌ Can cause issues when executed via `bash -c python -c "..."`
- ❌ Quote escaping problems in shell environments

**Use temp file method instead for production use.**

## Error Handling

Common errors and solutions:

| Error | Cause | Solution |
|-------|-------|----------|
| `insufficient_data` | Less than 50 candles | Increase count to 100+ in MCP calls |
| `ImportError: run_pattern_scan` | Wrong import path | Use correct path: `.claude/skills/pattern-scanner/scripts` |
| `KeyError: 'candles_m15'` | Missing timeframe data | Ensure all 4 timeframes are provided |
| `UnicodeEncodeError` | Windows console encoding | Use `safe_print()` function (already handled) |
| Empty HTML report | Invalid CSV format | Verify CSV has header row and valid data |

## Timeframe Requirements

Minimum candles per timeframe:
- **M15:** 50 candles (≈12.5 hours of data)
- **H1:** 50 candles (≈2 days of data)
- **H4:** 50 candles (≈8 days of data)
- **D1:** 50 candles (≈2 months of data)

If a timeframe has insufficient data, it will be skipped with a warning.
