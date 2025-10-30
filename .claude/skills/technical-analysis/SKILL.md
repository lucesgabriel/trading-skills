---
name: technical-analysis
description: Use when analyzing market trends, evaluating technical indicators, or calculating success probabilities for forex trading signals.
version: 1.0.0
tags: [trading, indicators, technical-analysis, forex, RSI, MACD, moving-average, bollinger-bands, trend, momentum]
category: market-analysis
requires:
  mcp:
    - mcp__metatrader__get_symbol_price
    - mcp__metatrader__get_candles_latest
  skills: []
difficulty: intermediate
estimated_time: 20-40s
output_format: [console]
author: Gabriel Luces
repository: https://github.com/lucesgabriel/trading-skills
---

# Technical Analysis Skill

## Purpose
Comprehensive technical analysis for forex and financial markets using MetaTrader data and multiple indicators to identify trading opportunities with calculated success probabilities.

## When to Use This Skill

**Primary Triggers:**
- "analyze [SYMBOL]" or "technical analysis for [SYMBOL]"
- "what are the indicators showing for [SYMBOL]?"
- "is [SYMBOL] bullish or bearish?"
- "give me a trading signal for [SYMBOL]"

**Use Cases:**
- User wants comprehensive multi-indicator analysis
- User needs trend direction and market conditions
- User asks for success probability calculations
- User wants trading signals with entry/stop/target levels

**Example Inputs:**
```
✓ "analyze EURUSD"
✓ "what's the trend on GBPUSD?"
✓ "give me indicators for XAUUSD"
✓ "is USDJPY showing a buy signal?"
✗ "scan for patterns" → Use pattern-scanner skill instead
```

## Core Analysis Methodology

### 1. Multi-Timeframe Analysis
Always analyze at least 3 timeframes for context:
- **Higher Timeframe (H4/Daily)**: Overall trend direction
- **Trading Timeframe (H1)**: Entry signals and patterns
- **Lower Timeframe (M15)**: Precise entry timing

### 2. Essential Indicators to Calculate

#### Trend Indicators
- **Moving Averages**:
  - Calculate SMA(20), SMA(50), SMA(200) from candle data
  - EMA(12), EMA(26) for MACD
  - Price position relative to MAs indicates trend strength

- **MACD (Moving Average Convergence Divergence)**:
  - MACD Line = EMA(12) - EMA(26)
  - Signal Line = EMA(9) of MACD Line
  - Histogram = MACD Line - Signal Line
  - Crossovers indicate momentum shifts

#### Momentum Indicators
- **RSI (Relative Strength Index)**:
  - Calculate 14-period RSI from price data
  - RSI > 70: Overbought (potential reversal down)
  - RSI < 30: Oversold (potential reversal up)
  - RSI 40-60: Neutral zone
  - Divergences are powerful signals

- **Stochastic Oscillator**:
  - %K = (Close - Lowest Low) / (Highest High - Lowest Low) × 100
  - %D = SMA(3) of %K
  - Values > 80: Overbought
  - Values < 20: Oversold

#### Volatility Indicators
- **Bollinger Bands**:
  - Middle Band = SMA(20)
  - Upper Band = SMA(20) + (2 × Standard Deviation)
  - Lower Band = SMA(20) - (2 × Standard Deviation)
  - Price touching bands indicates potential reversals
  - Band squeeze indicates volatility expansion coming

- **ATR (Average True Range)**:
  - Measures market volatility
  - Use for stop-loss calculation
  - Higher ATR = wider stops needed

### 3. Analysis Workflow

```
STEP 1: GET MARKET DATA
→ Use metatrader:get_symbol_price for current price
→ Use metatrader:get_candles_latest for historical data (at least 200 candles)
→ Analyze multiple timeframes (M15, H1, H4, Daily)

STEP 2: CALCULATE INDICATORS
→ Process candle data to calculate all indicators
→ Use pandas/numpy for calculations if needed
→ Store indicator values for comparison

STEP 3: IDENTIFY TREND
→ Check MA alignment and slope
→ Verify with MACD direction
→ Confirm with price action (higher highs/lows)

STEP 4: DETECT SIGNALS
→ Look for indicator confluences
→ Identify support/resistance levels
→ Check for divergences (RSI/MACD vs Price)
→ Spot chart patterns

STEP 5: CALCULATE SUCCESS PROBABILITY
→ Count confluence factors (more = higher probability)
→ Check historical patterns
→ Assess risk/reward ratio
→ Consider market conditions (trending vs ranging)

STEP 6: PRESENT FINDINGS
→ Clear trend direction
→ Key support/resistance levels
→ Entry/exit suggestions
→ Stop loss recommendations based on ATR
→ Probability assessment (percentage)
```

### 4. Success Probability Calculation

Use this weighted scoring system:

```python
# Confluence Factors (each adds 10-15%)
- Trend alignment across timeframes: +15%
- Multiple indicator confirmation: +15%
- Support/resistance at entry: +10%
- RSI in favorable zone: +10%
- MACD alignment: +10%
- Bollinger band position: +10%
- Volume confirmation: +10%
- Chart pattern present: +15%

# Deduction Factors
- Counter-trend trade: -20%
- High volatility period: -10%
- News event nearby: -15%
- Divergence against position: -15%

# Base probability: 50%
# Final probability = Base + Sum(Positive Factors) - Sum(Negative Factors)
# Cap between 30% and 85% (no trade is guaranteed)
```

### Scripts de Apoyo

Se incluye el script `scripts/indicator_suite.py` para automatizar cálculos y scoring consistentes.

**Funciones clave:**
- `candles_to_dataframe()` transforma velas de MetaTrader en DataFrame ordenado.
- `build_indicator_snapshot()` calcula SMA, EMA, MACD, RSI, Stochastic, Bollinger Bands y ATR en un paso.
- `score_direction()` genera probabilidades LONG/SHORT en el rango 30%-85% según confluencias.
- `generate_snapshot_from_candles()` produce un resumen listo para redactar en la respuesta.

**Ejemplo de uso:**
```python
import sys
from pathlib import Path
base = Path(r"C:/Users/luces/Downloads/trading-skills/.claude/skills/technical-analysis/scripts")
sys.path.append(str(base))

from indicator_suite import generate_snapshot_from_candles

candles = metatrader.get_candles_latest("EURUSD", "H1", 250)
snapshot = generate_snapshot_from_candles(candles, timeframe="H1")

print(snapshot["trend_bias"], snapshot["long_probability"])
```

**Ventajas:**
- Evita reescribir lógica de indicadores en cada análisis.
- Mantiene alineado el cálculo de probabilidades con la tabla de confluencias.
- El snapshot devuelto puede compartirse con otros skills como `opportunity-scanner` o `risk-management`.

### 5. Trading Opportunity Types

#### High Probability Setups (70%+ success rate)
- Trend continuation with multiple confirmations
- Support/resistance bounces with divergence
- Breakouts with volume confirmation
- Three timeframe alignment

#### Medium Probability Setups (55-70%)
- Single indicator signals
- Counter-trend reversals with confirmation
- Range trading in clear boundaries

#### Low Probability Setups (<55%)
- Counter-trend without strong reversal signals
- Conflicting indicators
- Low volume breakouts

## Implementation with MetaTrader Tools

### Getting Data
```python
# Get current price
metatrader:get_symbol_price(symbol_name="EURUSD")

# Get candle data for analysis
metatrader:get_candles_latest(
    symbol_name="EURUSD",
    timeframe="H1",  # or "M15", "H4", "D1"
    count=200  # enough for 200-period MA
)
```

### Example Analysis Output Format

```
=== TECHNICAL ANALYSIS: EURUSD ===

📊 MARKET OVERVIEW
Current Price: 1.0850
Spread: 1.2 pips
Market Status: High volatility

🎯 TREND ANALYSIS
Daily Trend: BULLISH ↑ (above SMA 50, 200)
H4 Trend: BULLISH ↑ (MA alignment positive)
H1 Trend: CONSOLIDATING (sideways)

📈 INDICATORS (H1 Timeframe)
Moving Averages:
  - Price above SMA(20): BULLISH
  - SMA(20) above SMA(50): BULLISH
  - SMA(50) above SMA(200): BULLISH

MACD:
  - MACD Line: 0.0023 (above signal)
  - Histogram: Increasing
  - Status: BULLISH momentum

RSI (14):
  - Value: 58 (neutral zone)
  - No divergence detected
  - Status: Room to rise

Bollinger Bands:
  - Position: Middle band
  - Width: Normal
  - Status: Neutral

Stochastic:
  - %K: 62, %D: 58
  - Status: Rising in neutral zone

🎯 KEY LEVELS
Resistance: 1.0890 (previous high)
Support: 1.0820 (SMA 50)
Major Support: 1.0780 (SMA 200)

💡 TRADING OPPORTUNITY
Type: LONG (Buy)
Entry: 1.0850 - 1.0855
Stop Loss: 1.0820 (30 pips, based on ATR)
Take Profit 1: 1.0890 (40 pips)
Take Profit 2: 1.0920 (70 pips)
Risk/Reward: 1:2.3

✅ CONFLUENCE FACTORS
+ Uptrend across all timeframes (+15%)
+ MACD bullish (+10%)
+ Price above key MAs (+10%)
+ Support at SMA 50 (+10%)
+ RSI in buy zone (+10%)
+ Bullish momentum (+10%)

📊 SUCCESS PROBABILITY: 75%

Reasoning: Multiple timeframe alignment, strong MA support,
bullish momentum across indicators. Entry at key support level
with favorable risk/reward ratio.

⚠️ RISK FACTORS
- Watch for news events (ECB announcements)
- Monitor for RSI divergence at highs
- Respect stop loss (volatility possible)
```

## Advanced Techniques

### Pattern Recognition
Look for these high-probability patterns:
- **Head and Shoulders**: Reversal pattern
- **Double Top/Bottom**: Reversal signals
- **Triangles**: Continuation/breakout setups
- **Flags and Pennants**: Continuation patterns
- **Cup and Handle**: Bullish continuation

### Divergence Detection
- **Bullish Divergence**: Price makes lower low, RSI makes higher low
- **Bearish Divergence**: Price makes higher high, RSI makes lower high
- These are powerful reversal signals

### Volume Analysis
- Breakouts need volume confirmation
- Low volume rallies often fail
- Volume spikes indicate strong moves

## Risk Management Integration

### Position Sizing
```
Risk Per Trade = Account Balance × Risk % (usually 1-2%)
Position Size = Risk Per Trade / (Entry Price - Stop Loss Price)
```

### Stop Loss Calculation
```
ATR-based Stop: Entry ± (2 × ATR)
Support/Resistance Stop: Just beyond key level
Percentage Stop: 1-3% from entry
```

## Best Practices

1. **Never trade on single indicator**: Always look for confluence
2. **Respect the trend**: Trend trades have higher success rates
3. **Use multiple timeframes**: Avoid trading against higher TF trend
4. **Wait for confirmation**: Don't jump into trades early
5. **Manage risk**: Never risk more than 2% per trade
6. **Document everything**: Track your analysis accuracy
7. **Adapt to conditions**: Trending vs ranging markets need different approaches

## Common Mistakes to Avoid

❌ Over-relying on one indicator
❌ Ignoring higher timeframe context
❌ Trading during major news without protection
❌ Moving stops to avoid losses
❌ Averaging down on losing positions
❌ Revenge trading after losses
❌ Ignoring risk management rules

## Integration with Other Skills

- **Opportunity Scanner**: Use this analysis to screen multiple symbols
- **Trade Management**: Apply this analysis to open positions
- **Backtest Results**: Validate strategies with historical data
- **Risk Calculator**: Size positions based on this analysis

---

## Execution Instructions

When user requests technical analysis (e.g., "analyze EURUSD", "technical analysis for GBPUSD"), follow this workflow:

### 🔇 Silent Execution Mode

**CRITICAL**: User must see ONLY the final analysis output. No intermediate steps.

❌ **NEVER show to user:**
- Write tool operations
- "Creating files..."
- "Writing CSV..."
- "Executing script..."
- Intermediate Python code
- File paths or timestamps

✅ **ONLY show to user:**
- Final formatted analysis (from run_analysis.py)
- Error codes (ERR_TA_xxx) if validation fails

**HOW TO ACHIEVE SILENT EXECUTION:**

Use **single Bash command** that performs all operations internally:
1. Validates data (silent - only shows errors)
2. Writes CSV files (silent)
3. Writes Python script (silent)
4. Executes analysis (prints only final output)

**Bash tool configuration:**
- `description`: "" (empty string for complete silence)
- `command`: See Step 2 template below

---

### Step 1: Fetch Market Data from MCP

Make 5 parallel MCP calls to get comprehensive data:

```python
price_data = mcp__metatrader__get_symbol_price(symbol_name: "EURUSD")
m15_data = mcp__metatrader__get_candles_latest(symbol_name: "EURUSD", timeframe: "M15", count: 250)
h1_data = mcp__metatrader__get_candles_latest(symbol_name: "EURUSD", timeframe: "H1", count: 250)
h4_data = mcp__metatrader__get_candles_latest(symbol_name: "EURUSD", timeframe: "H4", count: 250)
d1_data = mcp__metatrader__get_candles_latest(symbol_name: "EURUSD", timeframe: "D1", count: 250)
```

**Important:** Request 250 candles to ensure enough data for 200-period moving averages.

**Extract CSV strings:**
```python
csv_m15 = m15_data["result"] if isinstance(m15_data, dict) else m15_data
csv_h1 = h1_data["result"] if isinstance(h1_data, dict) else h1_data
csv_h4 = h4_data["result"] if isinstance(h4_data, dict) else h4_data
csv_d1 = d1_data["result"] if isinstance(d1_data, dict) else d1_data
```

### Step 2: Execute Silent Analysis (Single Command)

**CRITICAL:** Use this exact approach - do NOT use Write tool or show intermediate steps.

**Detect Python command:**
```python
import shutil
python_cmd = "python3" if shutil.which("python3") else "python"
```

**Execute analysis in single Bash command:**

```bash
{python_cmd} << 'ANALYSIS_SCRIPT'
import sys
from pathlib import Path
from datetime import datetime

# Setup paths
scripts_dir = Path(r"D:\Programing Language html css js php DB\28102025\.claude\skills\technical-analysis\scripts")
sys.path.insert(0, str(scripts_dir))

# Import modules
from validation import validate_all_timeframes, ValidationError
from run_analysis import run_technical_analysis, cleanup_old_analyses

# MCP data (insert actual values)
price_data = {PRICE_DATA}
csv_m15 = r"""{CSV_M15}"""
csv_h1 = r"""{CSV_H1}"""
csv_h4 = r"""{CSV_H4}"""
csv_d1 = r"""{CSV_D1}"""

# Step 1: Pre-flight validation (silent - only shows errors)
try:
    validate_all_timeframes({
        "candles_m15": csv_m15,
        "candles_h1": csv_h1,
        "candles_h4": csv_h4,
        "candles_d1": csv_d1
    })
except ValidationError as e:
    print(f"[!] {e}")
    print(f"\nSolution:")
    if e.code == "ERR_TA_001":
        print("  - Check MetaTrader connection")
        print("  - Verify symbol has historical data")
        print("  - Try count=100 instead of 250")
    elif e.code == "ERR_TA_002":
        print("  - Verify MCP server is responding")
    elif e.code == "ERR_TA_003":
        print("  - Update MetaTrader to latest version")
    sys.exit(1)

# Step 2: Setup temp directory and cleanup old files (silent)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
temp_dir = scripts_dir / "temp"
temp_dir.mkdir(exist_ok=True)
cleanup_old_analyses(temp_dir, keep=3)

# Step 3: Write CSV files (silent)
(temp_dir / f"m15_{timestamp}.csv").write_text(csv_m15)
(temp_dir / f"h1_{timestamp}.csv").write_text(csv_h1)
(temp_dir / f"h4_{timestamp}.csv").write_text(csv_h4)
(temp_dir / f"d1_{timestamp}.csv").write_text(csv_d1)

# Step 4: Write analysis script (silent)
analysis_script = f'''#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from run_analysis import run_technical_analysis

price_data = {price_data}
temp_dir = Path(__file__).parent

mcp_data = {{
    "price": price_data,
    "candles_m15": (temp_dir / "m15_{timestamp}.csv").read_text(),
    "candles_h1": (temp_dir / "h1_{timestamp}.csv").read_text(),
    "candles_h4": (temp_dir / "h4_{timestamp}.csv").read_text(),
    "candles_d1": (temp_dir / "d1_{timestamp}.csv").read_text()
}}

result = run_technical_analysis("{SYMBOL}", mcp_data)
print(result["formatted_output"])
'''

script_path = temp_dir / f"analysis_{timestamp}.py"
script_path.write_text(analysis_script)

# Step 5: Execute analysis (prints only final output)
exec(compile(script_path.read_text(), str(script_path), 'exec'))
ANALYSIS_SCRIPT
```

**Template variables to replace:**
- `{python_cmd}`: "python3" or "python"
- `{PRICE_DATA}`: price_data dictionary
- `{CSV_M15}`: csv_m15 string
- `{CSV_H1}`: csv_h1 string
- `{CSV_H4}`: csv_h4 string
- `{CSV_D1}`: csv_d1 string
- `{SYMBOL}`: "EURUSD" or requested symbol

**Bash tool parameters:**
- `command`: Above template with variables replaced
- `description`: "" (empty string - NO description shown to user)
- `timeout`: 30000 (30 seconds)

**User experience:**
```
[User sees ONLY this - no intermediate steps]

======================================================================
TECHNICAL ANALYSIS: EURUSD
======================================================================

CURRENT SITUATION
Price: 1.15802
ATR: 0.00141 (14 pips)
Volatility: compressed

[... complete analysis output ...]

======================================================================
```

**Expected Output:**
```
======================================================================
TECHNICAL ANALYSIS: EURUSD
======================================================================

CURRENT SITUATION
Price: 1.15747
ATR: 0.00141 (14 pips)
Volatility: compressed

MULTI-TIMEFRAME ANALYSIS
[... complete analysis ...]

TRADING RECOMMENDATION
Signal: LONG
Entry: 1.15747
Stop Loss: 1.15470 (27 pips)
Take Profit 1: 1.16029 (28 pips)
Take Profit 2: 1.16689 (94 pips)
Risk:Reward: 1:3.4

[... execution instructions and risk warnings ...]
======================================================================
```

---

## Workflow Summary

```
User: "analyze EURUSD"

Step 1: Fetch MCP data (5 parallel calls) → price + 4 timeframes
Step 2: Execute silent analysis (single Bash command)
  ├─ Validate data (fail-fast if issues)
  ├─ Write 4 CSV files + analysis script
  ├─ Execute analysis
  └─ Print formatted output

User sees: → [Only final analysis output]
```

**Implementation:**
- 1 MCP call batch (Step 1)
- 1 Bash command with heredoc (Step 2)
- 0 Write tool operations visible
- 0 intermediate messages shown

**Before Phase 2.7 (verbose):**
- Write tool showing 251-line CSV diffs
- Multiple failed Bash attempts
- Read/Update operations visible
- 7+ intermediate messages
- Manual text fallback

**After Phase 2.7 (clean):**
- Single Bash heredoc execution
- All file operations internal (silent)
- Validation integrated (only shows errors)
- User sees only final formatted analysis
- Only final output shown
- Errors caught early with clear codes
- Scripts ~1KB + 4 CSV files

---

## Troubleshooting

| Error Code | Meaning | Solution |
|------------|---------|----------|
| `ERR_TA_001` | Insufficient data | Check MetaTrader connection, verify symbol availability |
| `ERR_TA_002` | Invalid CSV format | Verify MCP server is responding correctly |
| `ERR_TA_003` | Missing columns | Update MetaTrader, check MCP server compatibility |
| `ModuleNotFoundError` | Import failed | Ensure script is in correct directory with run_analysis.py |

**Debugging:**
- Last 3 analyses are kept in `scripts/temp/` directory
- Can inspect CSV files: `m15_YYYYMMDD_HHMMSS.csv`
- Can inspect scripts: `analysis_YYYYMMDD_HHMMSS.py`

---

Remember: No analysis guarantees success. Always use proper risk management and never risk more than you can afford to lose.
