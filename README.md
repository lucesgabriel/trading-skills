# Trading Skills - Professional Trading Analysis System

A comprehensive trading analysis and automation system built for Claude Code CLI with MetaTrader 5 integration. This project provides 5 specialized skills for technical analysis, market scanning, risk management, backtesting, and advanced analytics.

## Features

### 5 Professional Trading Skills

1. **Technical Analysis** 📊
   - Multi-timeframe analysis (M15, H1, H4, Daily)
   - Multiple indicators: MA, EMA, MACD, RSI, Stochastic, Bollinger Bands, ATR
   - Success probability calculation (30-85%)
   - Support/resistance level identification
   - Entry/exit recommendations with risk-reward ratios

2. **Opportunity Scanner** 🔍
   - Automatic scanning of 15+ symbols (EURUSD, GBPUSD, XAUUSD, etc.)
   - Probability-based ranking
   - Customizable filters
   - High-probability setup identification (>70%)

3. **Risk Management** 🛡️
   - Automatic position sizing calculation
   - Optimal stop loss placement (ATR-based, technical, percentage)
   - Multiple take profit strategies (R:R, scaling, trailing)
   - Portfolio exposure evaluation

4. **Backtesting** 📈
   - Historical strategy validation
   - Key metrics: Win Rate, Profit Factor, Expectancy, Drawdown
   - Parameter optimization
   - Walk-forward analysis

5. **Advanced Analytics** 🎯
   - Advanced statistics: Sharpe, Sortino, Calmar ratios
   - 13+ candlestick pattern detection
   - Portfolio correlation analysis
   - Monte Carlo simulations
   - Risk of Ruin calculations

## Requirements

- **Claude Code CLI** - [Download](https://docs.claude.com/claude-code)
- **MetaTrader 5** - Trading platform
- **Python 3.8+** - For analytics scripts
- **MetaTrader MCP Server** - Integration bridge

### Python Dependencies

```bash
pip install pandas numpy
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/lucesgabriel/trading-skills.git
cd trading-skills
```

### 2. Install MetaTrader MCP Server

```bash
npm install -g metatrader-mcp-server
```

### 3. Configure MetaTrader Connection

Copy the example configuration and edit with your credentials:

```bash
cp .mcp.json.example .mcp.json
```

Then edit `.mcp.json` with your MetaTrader credentials:

```json
{
  "mcpServers": {
    "metatrader": {
      "command": "metatrader-mcp-server",
      "args": [
        "--login", "YOUR_ACCOUNT_NUMBER",
        "--password", "YOUR_PASSWORD",
        "--server", "YOUR_BROKER_SERVER",
        "--path", "PATH_TO_MT5_TERMINAL"
      ]
    }
  }
}
```

**IMPORTANT**: The `.mcp.json` file is in `.gitignore` to protect your credentials. Never commit this file with real credentials.

### 4. Copy Skills to Claude Code

The `.claude/skills/` directory contains all skills. Claude Code will automatically detect them.

### 5. Configure Permissions

Edit `.claude/settings.local.json` to grant necessary permissions for the skills to access MetaTrader data.

## Usage

### Using Skills in Claude Code

Once installed, you can invoke skills directly in Claude Code CLI:

```bash
# Technical analysis
/technical-analysis EURUSD

# Scan market for opportunities
/opportunity-scanner

# Calculate position size
/risk-management GBPUSD 1000 2

# Backtest a strategy
/backtesting XAUUSD "2023-01-01" "2023-12-31"

# Advanced analytics
/advanced-analytics
```

### Running Example Scripts

The `examples/` directory contains sample analysis scripts:

```bash
# Analyze EURUSD
python examples/eurusd_full_analysis.py

# Analyze GBPUSD
python examples/gbpusd_full_analysis.py
```

## Project Structure

```
trading-skills/
├── .claude/
│   ├── settings.local.json      # Claude Code permissions
│   └── skills/                  # 5 trading skills
│       ├── README.md            # Skills overview
│       ├── technical-analysis/
│       │   ├── SKILL.md
│       │   └── scripts/
│       │       └── indicator_suite.py
│       ├── opportunity-scanner/
│       │   ├── SKILL.md
│       │   └── scripts/
│       │       └── market_scanner.py
│       ├── risk-management/
│       │   ├── SKILL.md
│       │   └── scripts/
│       │       └── position_sizing.py
│       ├── backtesting/
│       │   ├── SKILL.md
│       │   └── scripts/
│       │       └── backtest_engine.py
│       └── advanced-analytics/
│           ├── SKILL.md
│           └── scripts/
│               ├── advanced_statistics.py
│               ├── pattern_recognition.py
│               ├── correlation_analysis.py
│               └── volatility_analysis.py
├── examples/
│   ├── eurusd_analysis.py       # Basic EURUSD analysis
│   ├── eurusd_full_analysis.py  # Complete EURUSD analysis
│   └── gbpusd_full_analysis.py  # Complete GBPUSD analysis
├── .gitignore
├── .mcp.json                    # MetaTrader MCP configuration
├── README.md                    # This file
├── PROYECTO_COMPLETADO.md       # Project completion report
└── SKILLS_MCP_SETUP.md          # Detailed setup guide

```

## Documentation

- **[PROYECTO_COMPLETADO.md](PROYECTO_COMPLETADO.md)** - Complete project report with objectives and metrics
- **[SKILLS_MCP_SETUP.md](SKILLS_MCP_SETUP.md)** - Detailed configuration guide with troubleshooting
- **[.claude/skills/README.md](.claude/skills/README.md)** - Skills overview and usage

## Configuration

### MetaTrader 5 Setup

1. Install MetaTrader 5 from your broker
2. Create a demo or real account
3. Note your account credentials
4. Update `.mcp.json` with your details

### Claude Code Skills

Skills are automatically loaded from `.claude/skills/`. Each skill has:
- `SKILL.md` - Skill definition with YAML frontmatter
- `scripts/` - Python scripts for calculations

## Examples

### Basic Technical Analysis

```bash
# Get technical analysis for EURUSD
/technical-analysis EURUSD
```

Expected output:
- Trend analysis across multiple timeframes
- Indicator signals (MA, MACD, RSI, etc.)
- Success probability
- Entry/exit recommendations
- Risk-reward ratios

### Market Scanning

```bash
# Scan all major pairs
/opportunity-scanner
```

Gets ranked list of trading opportunities sorted by probability.

### Position Sizing

```bash
# Calculate position size
# Symbol: GBPUSD, Account: $10000, Risk: 2%
/risk-management GBPUSD 10000 2
```

Returns optimal lot size and stop loss placement.

## Troubleshooting

### MetaTrader Connection Issues

1. Verify MT5 is running
2. Check credentials in `.mcp.json`
3. Ensure `metatrader-mcp-server` is installed
4. Check firewall settings

### Skills Not Loading

1. Verify `.claude/skills/` directory structure
2. Check YAML frontmatter in `SKILL.md` files
3. Review `.claude/settings.local.json` permissions

### Python Script Errors

1. Install required dependencies: `pip install pandas numpy`
2. Verify Python 3.8+ is installed
3. Check MetaTrader connection

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is for educational and research purposes. Always backtest strategies before using real capital.

## Disclaimer

Trading involves risk. This software is provided "as is" without warranty. Always use proper risk management and never risk more than you can afford to lose.

---

**Author**: Gabriel Luces
**Repository**: [github.com/lucesgabriel/trading-skills](https://github.com/lucesgabriel/trading-skills)
**Date**: October 2025

For detailed configuration and troubleshooting, see [SKILLS_MCP_SETUP.md](SKILLS_MCP_SETUP.md)
