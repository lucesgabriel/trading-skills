# Examples Directory

This directory contains example scripts demonstrating how to use the Trading Skills System.

## Quick Start Examples

### 🚀 quick_start.py
**Minimal pattern scanner demo**
```bash
python examples/quick_start.py EURUSD
```
Perfect for beginners. Shows basic pattern scanning with minimal configuration.

### 📊 quick_scan_example.py
**Quick pattern scan example**
```bash
python examples/quick_scan_example.py
```
Demonstrates rapid pattern detection across multiple timeframes.

## Advanced Examples

### 🔬 advanced_example.py
**Advanced usage patterns**
```bash
python examples/advanced_example.py
```
Shows advanced configuration options, custom timeframes, and filtering.

### 📈 advanced_analysis_example.py
**Advanced analytics demonstration**
```bash
python examples/advanced_analysis_example.py
```
Demonstrates the advanced-analytics skill with statistical analysis, correlations, and risk metrics.

### 💱 eurusd_analysis_example.py
**EURUSD-specific comprehensive analysis**
```bash
python examples/eurusd_analysis_example.py
```
Complete analysis workflow for EURUSD including:
- Multi-timeframe technical analysis
- Pattern detection
- Trading setup generation
- Risk management calculations

## Legacy Examples

The `legacy/` folder contains older examples and alternative implementations kept for reference:
- Historical pattern scanner implementations
- Sample data files
- Development experiments

These are not actively maintained but may be useful for understanding the evolution of the system.

## Usage Tips

1. **Install dependencies first:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Ensure MetaTrader 5 is running** (for live data examples)

3. **Check MCP configuration** in `.claude/settings.local.json`

4. **Start with quick_start.py** if you're new to the system

5. **Use sample data** by passing `--sample-data` flag (for supported examples)

## Creating Your Own Examples

When creating new examples:
1. Import from `.claude/skills/*/scripts/` modules
2. Use clear docstrings and comments
3. Include error handling
4. Provide sample output in comments
5. Follow the naming pattern: `{symbol}_{feature}_example.py`

## Need Help?

- Check the main README.md for setup instructions
- Review skill documentation in `.claude/skills/*/SKILL.md`
- See troubleshooting guides in `.claude/skills/*/resources/troubleshooting.md`
