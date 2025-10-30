# Execution Instructions

When user requests a pattern scan (e.g., "scan EURUSD"), follow these 4 simple steps:

## Step 1: Fetch Market Data from MCP

Make 5 parallel MCP calls to fetch live data:
```
mcp__metatrader__get_symbol_price(symbol_name: "EURUSD")
mcp__metatrader__get_candles_latest(symbol_name: "EURUSD", timeframe: "M15", count: 100)
mcp__metatrader__get_candles_latest(symbol_name: "EURUSD", timeframe: "H1", count: 100)
mcp__metatrader__get_candles_latest(symbol_name: "EURUSD", timeframe: "H4", count: 100)
mcp__metatrader__get_candles_latest(symbol_name: "EURUSD", timeframe: "D1", count: 100)
```

## Step 2: Create Temporary Python Script with Timestamp

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

## Step 3: Execute Scanner with Guaranteed Cleanup

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

## Step 4: Report Results to User

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
