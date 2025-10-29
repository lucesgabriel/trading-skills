"""
Pattern Scanner Skill - Scripts Package
Automated candlestick pattern detection and HTML report generation
"""

__version__ = "1.0.0"
__author__ = "Claude Code"

from .candlestick_scanner import (
    scan_symbol_for_patterns,
    detect_patterns_all_timeframes,
    identify_support_resistance
)

from .confluence_calculator import (
    calculate_pattern_confluence,
    enhance_probability_with_patterns
)

from .html_generator import (
    generate_html_report,
    save_report_to_file
)

from .multi_symbol_scanner import (
    scan_multiple_symbols,
    rank_opportunities
)

from .console_utils import safe_console_output

__all__ = [
    'scan_symbol_for_patterns',
    'detect_patterns_all_timeframes',
    'identify_support_resistance',
    'calculate_pattern_confluence',
    'enhance_probability_with_patterns',
    'generate_html_report',
    'save_report_to_file',
    'scan_multiple_symbols',
    'rank_opportunities',
    'safe_console_output'
]
