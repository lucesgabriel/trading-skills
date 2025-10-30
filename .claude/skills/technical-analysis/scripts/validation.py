#!/usr/bin/env python3
"""
Validation module for technical-analysis skill.

Provides data validation functions with structured error codes.
"""

from typing import Dict


class ValidationError(ValueError):
    """Custom exception for validation errors with error codes"""
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


def validate_candle_count(csv_data: str, timeframe: str, min_candles: int = 50) -> bool:
    """
    Validate that CSV data has minimum number of candles.

    Args:
        csv_data: CSV string from MetaTrader
        timeframe: Timeframe name (M15, H1, H4, D1)
        min_candles: Minimum required candles (default 50)

    Returns:
        True if valid

    Raises:
        ValidationError: If validation fails
    """
    if not csv_data or len(csv_data) < 100:
        raise ValidationError(
            "ERR_TA_001",
            f"No data received for {timeframe} timeframe"
        )

    # Count lines (excluding header)
    lines = csv_data.strip().split('\n')
    candle_count = len(lines) - 1  # Subtract header line

    if candle_count < min_candles:
        raise ValidationError(
            "ERR_TA_001",
            f"Insufficient data for {timeframe}: {candle_count} candles (need {min_candles}+)"
        )

    return True


def validate_csv_format(csv_data: str, timeframe: str) -> bool:
    """
    Validate CSV has required columns.

    Args:
        csv_data: CSV string from MetaTrader
        timeframe: Timeframe name for error messages

    Returns:
        True if valid

    Raises:
        ValidationError: If validation fails
    """
    if not csv_data or len(csv_data) < 20:
        raise ValidationError(
            "ERR_TA_002",
            f"Invalid CSV format for {timeframe}: empty or too short"
        )

    # Check for required columns in header
    required_columns = ['time', 'open', 'high', 'low', 'close']
    header_line = csv_data.split('\n')[0].lower()

    missing_columns = [col for col in required_columns if col not in header_line]

    if missing_columns:
        raise ValidationError(
            "ERR_TA_003",
            f"Missing required columns in {timeframe}: {', '.join(missing_columns)}"
        )

    return True


def validate_timeframe_data(csv_data: str, timeframe: str, min_candles: int = 50) -> bool:
    """
    Run all validations for a single timeframe.

    Args:
        csv_data: CSV string from MetaTrader
        timeframe: Timeframe name (M15, H1, H4, D1)
        min_candles: Minimum required candles

    Returns:
        True if all validations pass

    Raises:
        ValidationError: If any validation fails
    """
    validate_csv_format(csv_data, timeframe)
    validate_candle_count(csv_data, timeframe, min_candles)
    return True


def validate_all_timeframes(mcp_data: Dict[str, str]) -> bool:
    """
    Validate all timeframe data before analysis.

    Args:
        mcp_data: Dictionary with keys: candles_m15, candles_h1, candles_h4, candles_d1

    Returns:
        True if all validations pass

    Raises:
        ValidationError: If any validation fails (fail-fast)
    """
    timeframes = {
        "candles_m15": "M15",
        "candles_h1": "H1",
        "candles_h4": "H4",
        "candles_d1": "D1"
    }

    for key, tf_name in timeframes.items():
        if key not in mcp_data:
            raise ValidationError(
                "ERR_TA_001",
                f"Missing data for {tf_name} timeframe"
            )

        csv_data = mcp_data[key]
        validate_timeframe_data(csv_data, tf_name)

    return True


# Error code reference
ERROR_CODES = {
    "ERR_TA_001": "Insufficient or missing data",
    "ERR_TA_002": "Invalid CSV format",
    "ERR_TA_003": "Missing required columns"
}


if __name__ == "__main__":
    # Test validation
    print("Validation module loaded successfully")
    print("\nError codes:")
    for code, desc in ERROR_CODES.items():
        print(f"  {code}: {desc}")
