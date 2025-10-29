# -*- coding: utf-8 -*-
"""
Quick Start - Minimal Pattern Scanner Example
Usage: python examples/quick_start.py EURUSD

This is a minimal example showing how to use the pattern scanner skill.
For full functionality with live data, use Claude Code: "scan EURUSD for patterns"
"""
import sys
from pathlib import Path

# Add skill to path
skill_path = Path(__file__).parent.parent / ".claude" / "skills" / "pattern-scanner" / "scripts"
sys.path.insert(0, str(skill_path))

from console_utils import init_console_encoding, safe_print
init_console_encoding()

def quick_scan(symbol='EURUSD'):
    """Quick pattern scan demonstration for a symbol"""
    safe_print(f"\n[CANDLE] Quick Pattern Scanner Demo")
    safe_print("="*50)
    safe_print(f"[TARGET] Symbol: {symbol}")
    safe_print("\n[!] This example requires MetaTrader 5 MCP server running.")
    safe_print("[NOTE] For full functionality with live data, use Claude Code:")
    safe_print(f"       'scan {symbol} for patterns'\n")
    
    # Import scanner modules to verify they load correctly
    try:
        from candlestick_scanner import scan_symbol_for_patterns
        from confluence_calculator import enhance_probability_with_patterns
        from html_generator import generate_html_report
        safe_print("[OK] Pattern Scanner modules loaded successfully")
        safe_print("[OK] Ready to scan when MCP data is available")
    except ImportError as e:
        safe_print(f"[X] Error loading modules: {e}")
        return {'status': 'error', 'message': str(e)}
    
    safe_print("\n" + "="*50)
    safe_print("[OK] Setup complete!")
    safe_print("\nNext steps:")
    safe_print("  1. Ensure MetaTrader 5 is running")
    safe_print("  2. Configure MCP server in .claude/settings.local.json")
    safe_print("  3. Use Claude Code to run full scan with live data")
    
    return {
        'status': 'ready',
        'symbol': symbol,
        'message': 'Modules loaded successfully. Use Claude Code for live scanning.'
    }

if __name__ == "__main__":
    symbol = sys.argv[1] if len(sys.argv) > 1 else 'EURUSD'
    result = quick_scan(symbol)
    
    if result['status'] == 'error':
        sys.exit(1)
    safe_print(f"\n[OK] {result['message']}")
    sys.exit(0)
