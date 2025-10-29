# -*- coding: utf-8 -*-
"""
Console utilities for pattern-scanner skill.

Provides safe console output that never crashes due to encoding issues on Windows.
Includes UTF-8 initialization and intelligent unicode character replacement.
"""

from __future__ import annotations

import sys
import os
from typing import Any, TextIO

# Unicode to ASCII replacements for common trading symbols
UNICODE_REPLACEMENTS = {
    '✓': '[OK]',
    '✗': '[X]',
    '●': '*',
    '○': 'o',
    '⚠': '[!]',
    '➤': '>',
    '▪': '-',
    '►': '>',
    '◄': '<',
    '↑': '^',
    '↓': 'v',
    '📊': '[CHART]',
    '📈': '[UP]',
    '📉': '[DOWN]',
    '🔥': '[FIRE]',
    '💡': '[IDEA]',
    '⏰': '[TIME]',
    '💹': '[TREND]',
    '🕯️': '[CANDLE]',
    '🎯': '[TARGET]',
    '🛡️': '[SHIELD]',
    '🚀': '[ROCKET]',
    '🚨': '[ALERT]',
    '💰': '[MONEY]',
    '💎': '[GEM]',
    '📌': '[PIN]',
    '📝': '[NOTE]',
    '🤖': '[BOT]'
}


def init_console_encoding() -> None:
    """
    Force UTF-8 encoding on Windows console.

    Attempts to reconfigure stdout/stderr to use UTF-8 encoding on Windows systems.
    Fails silently if reconfiguration is not possible.
    """
    if sys.platform == 'win32':
        try:
            # Change Windows code page to UTF-8 (65001)
            os.system('chcp 65001 > nul 2>&1')

            # Reconfigure stdout/stderr if possible (Python 3.7+)
            if hasattr(sys.stdout, 'reconfigure'):
                sys.stdout.reconfigure(encoding='utf-8', errors='replace')
            if hasattr(sys.stderr, 'reconfigure'):
                sys.stderr.reconfigure(encoding='utf-8', errors='replace')
        except Exception:
            # Fail silently - fallback mechanisms will handle encoding issues
            pass


def safe_console_output(
    *values: Any,
    sep: str = " ",
    end: str = "\n",
    file: TextIO | None = None,
    flush: bool = False,
) -> None:
    """
    Write text to the console without crashing on UnicodeEncodeError.

    Three-level fallback strategy:
    1. Try direct output (works if UTF-8 is configured)
    2. Replace known unicode symbols with ASCII equivalents
    3. Encode with 'replace' error handling as last resort

    Args:
        *values: Pieces to render (identical to built-in print)
        sep: Separator between the values
        end: Trailing string appended at the end
        file: Stream to target (stdout by default)
        flush: Whether to flush the stream after writing
    """
    target = file or sys.stdout
    text = sep.join(str(value) for value in values)
    payload = text + (end or "")

    try:
        # First attempt: direct output
        target.write(payload)
    except UnicodeEncodeError:
        try:
            # Second attempt: replace known unicode symbols
            safe_text = text
            for unicode_char, ascii_replacement in UNICODE_REPLACEMENTS.items():
                safe_text = safe_text.replace(unicode_char, ascii_replacement)
            target.write(safe_text + (end or ""))
        except UnicodeEncodeError:
            # Final fallback: encode with replace
            fallback = text.encode("ascii", "replace").decode("ascii")
            target.write(fallback + (end or ""))

    if flush:
        target.flush()


# Shorter alias for convenience
safe_print = safe_console_output


# Auto-initialize console encoding when module is imported
init_console_encoding()
