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

## Step 2: Run Scanner with Python Import

Use Python directly to call the `run_pattern_scan()` function:

```python
import sys
sys.path.insert(0, ".claude/skills/pattern-scanner/scripts")
from run_scan import run_pattern_scan

# Prepare MCP data in the correct format
mcp_data = {
    "price": {
        "bid": 1.16412,  # From get_symbol_price
        "ask": 1.16412,
        "last": 0.0,
        "volume": 0,
        "time": "2025-10-29T21:19:52Z"
    },
    "candles_m15": """time,open,high,low,close,tick_volume,spread,real_volume
0,2025-10-29 15:00:00+00:00,1.16354,1.16441,1.1635,1.16412,1204,0,0
...""",  # Full CSV string from get_candles_latest
    "candles_h1": """time,open,high,low,close,tick_volume,spread,real_volume
0,2025-10-29 15:00:00+00:00,1.16468,1.16511,1.16343,1.16412,5930,0,0
...""",  # Full CSV string from get_candles_latest
    "candles_h4": """time,open,high,low,close,tick_volume,spread,real_volume
0,2025-10-29 12:00:00+00:00,1.16573,1.16591,1.16343,1.16411,12297,0,0
...""",  # Full CSV string from get_candles_latest
    "candles_d1": """time,open,high,low,close,tick_volume,spread,real_volume
0,2025-10-29 00:00:00+00:00,1.16501,1.16659,1.16187,1.16409,136741,0,0
..."""   # Full CSV string from get_candles_latest
}

# Run the scanner
report_path = run_pattern_scan("EURUSD", mcp_data)
print(f"✅ Report: {report_path}")
```

**Important Notes:**
- ✅ **CSV Format:** MCP returns CSV as a string - use it directly (don't parse or modify)
- ✅ **Price Data:** Use the full price dict from `get_symbol_price`
- ✅ **Triple Quotes:** Use `"""..."""` for multiline CSV strings
- ✅ **Include Header:** Do NOT remove the CSV header row (`time,open,high,low,...`)
- ✅ **Symbol Case:** Symbol can be any case (EURUSD, eurusd) - it will be normalized

**Data Format Flexibility:**
The scanner accepts two CSV formats:
```python
# Format 1: Direct CSV string (preferred)
"candles_m15": "time,open,high,low,close,tick_volume,spread,real_volume\n0,2025..."

# Format 2: Dict with 'result' key (also supported)
"candles_m15": {"result": "time,open,high,low,close,tick_volume,spread,real_volume\n0,2025..."}
```

## Step 3: Display Results to User

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

## Alternative Method: Temp Script (If Python Import Fails)

If the direct import method doesn't work in your environment, use temp scripts:

```python
from datetime import datetime

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
temp_script = f".claude/skills/pattern-scanner/scripts/temp_scan_{timestamp}.py"

# Write temp script
with open(temp_script, 'w', encoding='utf-8') as f:
    f.write('''#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from run_scan import run_pattern_scan

mcp_data = ''' + repr(mcp_data) + '''

report_path = run_pattern_scan("EURUSD", mcp_data)
print(f"✅ Report: {report_path}")
''')

# Execute
import subprocess
result = subprocess.run(['python', temp_script], capture_output=True, text=True)
print(result.stdout)

# Cleanup
import os
os.remove(temp_script)
```

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
