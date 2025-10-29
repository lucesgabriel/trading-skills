"""
Candlestick Pattern Recognition for Trading
Identifies bullish and bearish patterns automatically
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple


class CandlestickPattern:
    """Detect candlestick patterns in OHLC data"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Args:
            df: DataFrame with columns: open, high, low, close
        """
        self.df = df.copy()
        self._calculate_candle_properties()
    
    def _calculate_candle_properties(self):
        """Calculate basic candle properties"""
        self.df['body'] = abs(self.df['close'] - self.df['open'])
        self.df['upper_shadow'] = self.df['high'] - self.df[['open', 'close']].max(axis=1)
        self.df['lower_shadow'] = self.df[['open', 'close']].min(axis=1) - self.df['low']
        self.df['range'] = self.df['high'] - self.df['low']
        self.df['is_bullish'] = self.df['close'] > self.df['open']
        self.df['body_pct'] = (self.df['body'] / self.df['range']) * 100
        
    def detect_doji(self, threshold: float = 0.1) -> pd.Series:
        """
        Detect Doji patterns (indecision)
        Small body with upper and lower shadows
        """
        return self.df['body_pct'] < (threshold * 100)
    
    def detect_hammer(self) -> pd.Series:
        """
        Detect Hammer pattern (bullish reversal)
        Small body at top, long lower shadow
        """
        conditions = (
            (self.df['lower_shadow'] >= 2 * self.df['body']) &
            (self.df['upper_shadow'] <= self.df['body'] * 0.3) &
            (self.df['body_pct'] >= 10) &
            (self.df['body_pct'] <= 30)
        )
        return conditions
    
    def detect_inverted_hammer(self) -> pd.Series:
        """
        Detect Inverted Hammer (bullish reversal)
        Small body at bottom, long upper shadow
        """
        conditions = (
            (self.df['upper_shadow'] >= 2 * self.df['body']) &
            (self.df['lower_shadow'] <= self.df['body'] * 0.3) &
            (self.df['body_pct'] >= 10) &
            (self.df['body_pct'] <= 30)
        )
        return conditions
    
    def detect_shooting_star(self) -> pd.Series:
        """
        Detect Shooting Star (bearish reversal)
        Small body at bottom, long upper shadow
        """
        conditions = (
            (self.df['upper_shadow'] >= 2 * self.df['body']) &
            (self.df['lower_shadow'] <= self.df['body'] * 0.3) &
            (~self.df['is_bullish']) &
            (self.df['body_pct'] >= 10) &
            (self.df['body_pct'] <= 30)
        )
        return conditions
    
    def detect_hanging_man(self) -> pd.Series:
        """
        Detect Hanging Man (bearish reversal)
        Small body at top, long lower shadow, appears at top of uptrend
        """
        conditions = (
            (self.df['lower_shadow'] >= 2 * self.df['body']) &
            (self.df['upper_shadow'] <= self.df['body'] * 0.3) &
            (~self.df['is_bullish']) &
            (self.df['body_pct'] >= 10) &
            (self.df['body_pct'] <= 30)
        )
        return conditions
    
    def detect_engulfing_bullish(self) -> pd.Series:
        """
        Detect Bullish Engulfing (reversal)
        Large bullish candle engulfs previous bearish candle
        """
        result = pd.Series(False, index=self.df.index)
        
        for i in range(1, len(self.df)):
            prev = self.df.iloc[i-1]
            curr = self.df.iloc[i]
            
            if (not prev['is_bullish'] and curr['is_bullish'] and
                curr['open'] < prev['close'] and curr['close'] > prev['open']):
                result.iloc[i] = True
        
        return result
    
    def detect_engulfing_bearish(self) -> pd.Series:
        """
        Detect Bearish Engulfing (reversal)
        Large bearish candle engulfs previous bullish candle
        """
        result = pd.Series(False, index=self.df.index)
        
        for i in range(1, len(self.df)):
            prev = self.df.iloc[i-1]
            curr = self.df.iloc[i]
            
            if (prev['is_bullish'] and not curr['is_bullish'] and
                curr['open'] > prev['close'] and curr['close'] < prev['open']):
                result.iloc[i] = True
        
        return result
    
    def detect_morning_star(self) -> pd.Series:
        """
        Detect Morning Star (bullish reversal)
        3-candle pattern: bearish, small body, bullish
        """
        result = pd.Series(False, index=self.df.index)
        
        for i in range(2, len(self.df)):
            c1 = self.df.iloc[i-2]  # Bearish
            c2 = self.df.iloc[i-1]  # Small body
            c3 = self.df.iloc[i]    # Bullish
            
            if (not c1['is_bullish'] and c3['is_bullish'] and
                c2['body'] < c1['body'] * 0.5 and
                c3['close'] > c1['open'] + (c1['body'] * 0.5)):
                result.iloc[i] = True
        
        return result
    
    def detect_evening_star(self) -> pd.Series:
        """
        Detect Evening Star (bearish reversal)
        3-candle pattern: bullish, small body, bearish
        """
        result = pd.Series(False, index=self.df.index)
        
        for i in range(2, len(self.df)):
            c1 = self.df.iloc[i-2]  # Bullish
            c2 = self.df.iloc[i-1]  # Small body
            c3 = self.df.iloc[i]    # Bearish
            
            if (c1['is_bullish'] and not c3['is_bullish'] and
                c2['body'] < c1['body'] * 0.5 and
                c3['close'] < c1['open'] - (c1['body'] * 0.5)):
                result.iloc[i] = True
        
        return result
    
    def detect_three_white_soldiers(self) -> pd.Series:
        """
        Detect Three White Soldiers (strong bullish continuation)
        3 consecutive bullish candles with higher closes
        """
        result = pd.Series(False, index=self.df.index)
        
        for i in range(2, len(self.df)):
            c1 = self.df.iloc[i-2]
            c2 = self.df.iloc[i-1]
            c3 = self.df.iloc[i]
            
            if (c1['is_bullish'] and c2['is_bullish'] and c3['is_bullish'] and
                c2['close'] > c1['close'] and c3['close'] > c2['close'] and
                c1['body_pct'] > 60 and c2['body_pct'] > 60 and c3['body_pct'] > 60):
                result.iloc[i] = True
        
        return result
    
    def detect_three_black_crows(self) -> pd.Series:
        """
        Detect Three Black Crows (strong bearish continuation)
        3 consecutive bearish candles with lower closes
        """
        result = pd.Series(False, index=self.df.index)
        
        for i in range(2, len(self.df)):
            c1 = self.df.iloc[i-2]
            c2 = self.df.iloc[i-1]
            c3 = self.df.iloc[i]
            
            if (not c1['is_bullish'] and not c2['is_bullish'] and not c3['is_bullish'] and
                c2['close'] < c1['close'] and c3['close'] < c2['close'] and
                c1['body_pct'] > 60 and c2['body_pct'] > 60 and c3['body_pct'] > 60):
                result.iloc[i] = True
        
        return result
    
    def detect_piercing_line(self) -> pd.Series:
        """
        Detect Piercing Line (bullish reversal)
        Bearish candle followed by bullish that closes above midpoint
        """
        result = pd.Series(False, index=self.df.index)
        
        for i in range(1, len(self.df)):
            prev = self.df.iloc[i-1]
            curr = self.df.iloc[i]
            
            midpoint = prev['close'] + (prev['body'] / 2)
            
            if (not prev['is_bullish'] and curr['is_bullish'] and
                curr['open'] < prev['low'] and
                curr['close'] > midpoint and curr['close'] < prev['open']):
                result.iloc[i] = True
        
        return result
    
    def detect_dark_cloud_cover(self) -> pd.Series:
        """
        Detect Dark Cloud Cover (bearish reversal)
        Bullish candle followed by bearish that closes below midpoint
        """
        result = pd.Series(False, index=self.df.index)
        
        for i in range(1, len(self.df)):
            prev = self.df.iloc[i-1]
            curr = self.df.iloc[i]
            
            midpoint = prev['open'] + (prev['body'] / 2)
            
            if (prev['is_bullish'] and not curr['is_bullish'] and
                curr['open'] > prev['high'] and
                curr['close'] < midpoint and curr['close'] > prev['open']):
                result.iloc[i] = True
        
        return result
    
    def detect_all_patterns(self) -> Dict[str, pd.Series]:
        """
        Detect all patterns and return dictionary
        
        Returns:
            Dictionary with pattern name as key and boolean Series as value
        """
        patterns = {
            'doji': self.detect_doji(),
            'hammer': self.detect_hammer(),
            'inverted_hammer': self.detect_inverted_hammer(),
            'shooting_star': self.detect_shooting_star(),
            'hanging_man': self.detect_hanging_man(),
            'engulfing_bullish': self.detect_engulfing_bullish(),
            'engulfing_bearish': self.detect_engulfing_bearish(),
            'morning_star': self.detect_morning_star(),
            'evening_star': self.detect_evening_star(),
            'three_white_soldiers': self.detect_three_white_soldiers(),
            'three_black_crows': self.detect_three_black_crows(),
            'piercing_line': self.detect_piercing_line(),
            'dark_cloud_cover': self.detect_dark_cloud_cover()
        }
        
        return patterns
    
    def get_pattern_summary(self, last_n: int = 10) -> Dict[str, List[str]]:
        """
        Get summary of patterns found in last N candles
        
        Args:
            last_n: Number of recent candles to check
        
        Returns:
            Dictionary with bullish and bearish patterns found
        """
        all_patterns = self.detect_all_patterns()
        recent_idx = self.df.index[-last_n:]
        
        bullish_patterns = []
        bearish_patterns = []
        
        pattern_types = {
            'bullish': ['hammer', 'inverted_hammer', 'engulfing_bullish', 
                       'morning_star', 'three_white_soldiers', 'piercing_line'],
            'bearish': ['shooting_star', 'hanging_man', 'engulfing_bearish',
                       'evening_star', 'three_black_crows', 'dark_cloud_cover'],
            'neutral': ['doji']
        }
        
        for pattern_name, pattern_series in all_patterns.items():
            for idx in recent_idx:
                if pattern_series.loc[idx]:
                    if pattern_name in pattern_types['bullish']:
                        bullish_patterns.append(f"{pattern_name} at {idx}")
                    elif pattern_name in pattern_types['bearish']:
                        bearish_patterns.append(f"{pattern_name} at {idx}")
        
        return {
            'bullish': bullish_patterns,
            'bearish': bearish_patterns,
            'neutral': [f"doji at {idx}" for idx in recent_idx if all_patterns['doji'].loc[idx]]
        }


def analyze_candles_for_symbol(candles_data: List[Dict]) -> Dict:
    """
    Analyze candlestick patterns from MetaTrader candle data
    
    Args:
        candles_data: List of candle dictionaries from MetaTrader
    
    Returns:
        Dictionary with pattern analysis
    """
    # Convert to DataFrame
    df = pd.DataFrame(candles_data)
    df.columns = ['time', 'open', 'high', 'low', 'close', 'volume', 'spread']
    
    # Create pattern detector
    detector = CandlestickPattern(df[['open', 'high', 'low', 'close']])
    
    # Get recent patterns
    summary = detector.get_pattern_summary(last_n=20)
    
    return {
        'recent_bullish_patterns': summary['bullish'],
        'recent_bearish_patterns': summary['bearish'],
        'neutral_patterns': summary['neutral'],
        'pattern_count': {
            'bullish': len(summary['bullish']),
            'bearish': len(summary['bearish']),
            'neutral': len(summary['neutral'])
        }
    }


if __name__ == "__main__":
    # Example usage
    example_data = {
        'open': [1.0850, 1.0860, 1.0855, 1.0840, 1.0835],
        'high': [1.0870, 1.0880, 1.0870, 1.0860, 1.0850],
        'low': [1.0840, 1.0850, 1.0845, 1.0830, 1.0820],
        'close': [1.0865, 1.0870, 1.0850, 1.0835, 1.0845]
    }
    
    df = pd.DataFrame(example_data)
    detector = CandlestickPattern(df)
    
    patterns = detector.detect_all_patterns()
    print("=== CANDLESTICK PATTERN DETECTION ===")
    for pattern_name, pattern_series in patterns.items():
        if pattern_series.any():
            print(f"{pattern_name}: Found at indices {pattern_series[pattern_series].index.tolist()}")
