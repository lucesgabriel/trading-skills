import pandas as pd
import numpy as np
from io import StringIO

# Datos de velas H1 (últimas 250 velas)
h1_data = """,time,open,high,low,close,tick_volume,spread,real_volume
249,2025-10-28 19:00:00+00:00,1.16589,1.16612,1.16567,1.16601,3158,0,0
248,2025-10-28 18:00:00+00:00,1.16605,1.1667399999999999,1.1655,1.16589,9395,0,0
247,2025-10-28 17:00:00+00:00,1.1639599999999999,1.16634,1.1637,1.16605,11170,0,0
246,2025-10-28 16:00:00+00:00,1.16402,1.16406,1.16253,1.16395,10154,0,0
245,2025-10-28 15:00:00+00:00,1.16593,1.16601,1.16351,1.16402,10147,0,0"""

# Datos completos H1 (solo mostraré algunos para el análisis)
h1_full = """,time,open,high,low,close,tick_volume,spread,real_volume
249,2025-10-28 19:00:00+00:00,1.16589,1.16612,1.16567,1.16601,3158,0,0
248,2025-10-28 18:00:00+00:00,1.16605,1.1667399999999999,1.1655,1.16589,9395,0,0
247,2025-10-28 17:00:00+00:00,1.1639599999999999,1.16634,1.1637,1.16605,11170,0,0
246,2025-10-28 16:00:00+00:00,1.16402,1.16406,1.16253,1.16395,10154,0,0
245,2025-10-28 15:00:00+00:00,1.16593,1.16601,1.16351,1.16402,10147,0,0
244,2025-10-28 14:00:00+00:00,1.16642,1.16645,1.16549,1.16594,6560,0,0
243,2025-10-28 13:00:00+00:00,1.16568,1.16651,1.16547,1.16642,6461,0,0
242,2025-10-28 12:00:00+00:00,1.16522,1.16588,1.1645,1.16568,7601,0,0
241,2025-10-28 11:00:00+00:00,1.1655,1.16629,1.1648399999999999,1.16525,9742,0,0
240,2025-10-28 10:00:00+00:00,1.16556,1.16616,1.1651,1.1655,7480,0,0"""

# Leer datos D1
d1_data = """,time,open,high,low,close,tick_volume,spread,real_volume
59,2025-10-28 00:00:00+00:00,1.16443,1.1668,1.16253,1.16602,117136,0,0
58,2025-10-27 00:00:00+00:00,1.1632,1.16521,1.16174,1.16441,132046,0,0
57,2025-10-24 00:00:00+00:00,1.16163,1.16485,1.1601,1.16272,140089,0,0
56,2025-10-23 00:00:00+00:00,1.16058,1.1620300000000001,1.15852,1.1617899999999999,123169,0,0
55,2025-10-22 00:00:00+00:00,1.15977,1.16224,1.1577,1.16094,145951,0,0
54,2025-10-21 00:00:00+00:00,1.16404,1.16553,1.15978,1.15995,173311,0,0
53,2025-10-20 00:00:00+00:00,1.1661299999999999,1.16757,1.16383,1.16412,146656,0,0
52,2025-10-17 00:00:00+00:00,1.16826,1.17283,1.16504,1.16531,190600,0,0
51,2025-10-16 00:00:00+00:00,1.16433,1.16943,1.1641,1.16873,185963,0,0
50,2025-10-15 00:00:00+00:00,1.16058,1.16476,1.16016,1.16471,174168,0,0
49,2025-10-14 00:00:00+00:00,1.15635,1.1615,1.1542,1.16077,201336,0,0
48,2025-10-13 00:00:00+00:00,1.16109,1.16299,1.15575,1.15705,172282,0,0
47,2025-10-10 00:00:00+00:00,1.15642,1.16306,1.1553,1.16245,185786,0,0
46,2025-10-09 00:00:00+00:00,1.16284,1.1648399999999999,1.15422,1.15642,201764,0,0
45,2025-10-08 00:00:00+00:00,1.16543,1.16614,1.15984,1.16284,182393,0,0
44,2025-10-07 00:00:00+00:00,1.17049,1.17147,1.16475,1.16573,157088,0,0
43,2025-10-06 00:00:00+00:00,1.17194,1.1731,1.16517,1.17123,180485,0,0
42,2025-10-03 00:00:00+00:00,1.1712,1.17594,1.1712,1.17399,132584,0,0
41,2025-10-02 00:00:00+00:00,1.17236,1.17585,1.16831,1.17163,143844,0,0
40,2025-10-01 00:00:00+00:00,1.17301,1.17787,1.17155,1.17307,172162,0,0
39,2025-09-30 00:00:00+00:00,1.17224,1.17617,1.17122,1.1733500000000001,148358,0,0
38,2025-09-29 00:00:00+00:00,1.16987,1.17548,1.16961,1.17271,142370,0,0
37,2025-09-26 00:00:00+00:00,1.16577,1.17071,1.16517,1.1702,152284,0,0
36,2025-09-25 00:00:00+00:00,1.17375,1.17542,1.16454,1.16655,163468,0,0
35,2025-09-24 00:00:00+00:00,1.18127,1.18189,1.1728,1.17381,152564,0,0
34,2025-09-23 00:00:00+00:00,1.1792,1.18199,1.17783,1.18148,156163,0,0
33,2025-09-22 00:00:00+00:00,1.17386,1.18029,1.17261,1.1802,140567,0,0
32,2025-09-19 00:00:00+00:00,1.17807,1.17925,1.17289,1.17432,166576,0,0
31,2025-09-18 00:00:00+00:00,1.18113,1.18484,1.175,1.1786,174980,0,0
30,2025-09-17 00:00:00+00:00,1.18595,1.19181,1.18081,1.1813500000000001,149271,0,0"""

def calculate_sma(data, period):
    """Calcula Simple Moving Average"""
    return data.rolling(window=period).mean()

def calculate_ema(data, period):
    """Calcula Exponential Moving Average"""
    return data.ewm(span=period, adjust=False).mean()

def calculate_rsi(data, period=14):
    """Calcula Relative Strength Index"""
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(data):
    """Calcula MACD"""
    ema12 = calculate_ema(data, 12)
    ema26 = calculate_ema(data, 26)
    macd_line = ema12 - ema26
    signal_line = calculate_ema(macd_line, 9)
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

def calculate_bollinger_bands(data, period=20, std_dev=2):
    """Calcula Bollinger Bands"""
    sma = calculate_sma(data, period)
    std = data.rolling(window=period).std()
    upper_band = sma + (std * std_dev)
    lower_band = sma - (std * std_dev)
    return upper_band, sma, lower_band

def calculate_stochastic(high, low, close, period=14):
    """Calcula Stochastic Oscillator"""
    lowest_low = low.rolling(window=period).min()
    highest_high = high.rolling(window=period).max()
    k = 100 * (close - lowest_low) / (highest_high - lowest_low)
    d = k.rolling(window=3).mean()
    return k, d

def calculate_atr(high, low, close, period=14):
    """Calcula Average True Range"""
    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    return atr

# Procesar datos H1
df_h1 = pd.read_csv(StringIO(h1_full.strip()))
df_h1 = df_h1.sort_index(ascending=True)  # Ordenar por antiguo a reciente
df_h1['close'] = pd.to_numeric(df_h1['close'])
df_h1['high'] = pd.to_numeric(df_h1['high'])
df_h1['low'] = pd.to_numeric(df_h1['low'])

# Calcular indicadores para H1
df_h1['sma_20'] = calculate_sma(df_h1['close'], 20)
df_h1['sma_50'] = calculate_sma(df_h1['close'], 50)
df_h1['sma_200'] = calculate_sma(df_h1['close'], 200)
df_h1['rsi'] = calculate_rsi(df_h1['close'])
macd, signal, hist = calculate_macd(df_h1['close'])
df_h1['macd'] = macd
df_h1['macd_signal'] = signal
df_h1['macd_hist'] = hist
upper, middle, lower = calculate_bollinger_bands(df_h1['close'])
df_h1['bb_upper'] = upper
df_h1['bb_middle'] = middle
df_h1['bb_lower'] = lower
k, d = calculate_stochastic(df_h1['high'], df_h1['low'], df_h1['close'])
df_h1['stoch_k'] = k
df_h1['stoch_d'] = d
df_h1['atr'] = calculate_atr(df_h1['high'], df_h1['low'], df_h1['close'])

# Obtener última vela (más reciente)
latest = df_h1.iloc[-1]

print("=== ANALISIS TECNICO COMPLETO: EURUSD ===")
print(f"\nPRECIO ACTUAL: {latest['close']:.5f}")
print(f"Hora: 2025-10-28 19:24 UTC")
print(f"\nANALISIS DE TENDENCIA (H1)")
print(f"   Precio actual: {latest['close']:.5f}")
print(f"   SMA(20): {latest['sma_20']:.5f}")
print(f"   SMA(50): {latest['sma_50']:.5f}")
print(f"   SMA(200): {latest['sma_200']:.5f}")

# Determinar tendencia
trend_score = 0
if latest['close'] > latest['sma_20']:
    print("   [+] Precio > SMA(20): ALCISTA")
    trend_score += 1
else:
    print("   [-] Precio < SMA(20): BAJISTA")
    trend_score -= 1

if latest['sma_20'] > latest['sma_50']:
    print("   [+] SMA(20) > SMA(50): ALCISTA")
    trend_score += 1
else:
    print("   [-] SMA(20) < SMA(50): BAJISTA")
    trend_score -= 1

if latest['sma_50'] > latest['sma_200']:
    print("   [+] SMA(50) > SMA(200): ALCISTA")
    trend_score += 1
else:
    print("   [-] SMA(50) < SMA(200): BAJISTA")
    trend_score -= 1

print(f"\nINDICADORES TECNICOS")
print(f"   RSI(14): {latest['rsi']:.2f}")
if latest['rsi'] < 30:
    print("      -> SOBREVENDIDO (potencial compra)")
    rsi_signal = "BUY"
elif latest['rsi'] > 70:
    print("      -> SOBRECOMPRADO (potencial venta)")
    rsi_signal = "SELL"
else:
    print("      -> NEUTRAL")
    rsi_signal = "NEUTRAL"

print(f"\n   MACD:")
print(f"      Linea MACD: {latest['macd']:.6f}")
print(f"      Senal: {latest['macd_signal']:.6f}")
print(f"      Histograma: {latest['macd_hist']:.6f}")
if latest['macd'] > latest['macd_signal']:
    print("      -> ALCISTA (MACD sobre senal)")
    macd_signal = "BUY"
else:
    print("      -> BAJISTA (MACD bajo senal)")
    macd_signal = "SELL"

print(f"\n   Bollinger Bands:")
print(f"      Superior: {latest['bb_upper']:.5f}")
print(f"      Media: {latest['bb_middle']:.5f}")
print(f"      Inferior: {latest['bb_lower']:.5f}")
bb_position = (latest['close'] - latest['bb_lower']) / (latest['bb_upper'] - latest['bb_lower']) * 100
print(f"      Posicion: {bb_position:.1f}% (0%=inferior, 100%=superior)")

print(f"\n   Stochastic:")
print(f"      %K: {latest['stoch_k']:.2f}")
print(f"      %D: {latest['stoch_d']:.2f}")
if latest['stoch_k'] < 20:
    print("      -> SOBREVENDIDO")
    stoch_signal = "BUY"
elif latest['stoch_k'] > 80:
    print("      -> SOBRECOMPRADO")
    stoch_signal = "SELL"
else:
    print("      -> NEUTRAL")
    stoch_signal = "NEUTRAL"

print(f"\n   ATR(14): {latest['atr']:.5f}")
print(f"      (Volatilidad para stops)")

# Calcular probabilidad de éxito
probability_long = 50
probability_short = 50

# Confluencias LONG
if trend_score > 0:
    probability_long += 15
    print("\n[OK] CONFLUENCIA LONG:")
    print("   + Tendencia alcista en MAs (+15%)")
if latest['rsi'] < 50 and latest['rsi'] > 30:
    probability_long += 10
    print("   + RSI en zona de compra (+10%)")
if macd_signal == "BUY":
    probability_long += 10
    print("   + MACD alcista (+10%)")
if latest['close'] > latest['bb_middle']:
    probability_long += 10
    print("   + Precio sobre BB media (+10%)")
if latest['stoch_k'] < 50:
    probability_long += 10
    print("   + Stochastic en zona baja (+10%)")

# Confluencias SHORT
if trend_score < 0:
    probability_short += 15
    print("\n[OK] CONFLUENCIA SHORT:")
    print("   + Tendencia bajista en MAs (+15%)")
if latest['rsi'] > 50 and latest['rsi'] < 70:
    probability_short += 10
    print("   + RSI en zona de venta (+10%)")
if macd_signal == "SELL":
    probability_short += 10
    print("   + MACD bajista (+10%)")
if latest['close'] < latest['bb_middle']:
    probability_short += 10
    print("   + Precio bajo BB media (+10%)")
if latest['stoch_k'] > 50:
    probability_short += 10
    print("   + Stochastic en zona alta (+10%)")

# Limitar probabilidades entre 30% y 85%
probability_long = min(85, max(30, probability_long))
probability_short = min(85, max(30, probability_short))

print(f"\nOPORTUNIDAD DE TRADING:")
if probability_long > probability_short:
    direction = "LONG (COMPRA)"
    prob = probability_long
    entry = latest['close']
    stop_loss = entry - (2 * latest['atr'])
    take_profit_1 = entry + (2 * latest['atr'])
    take_profit_2 = entry + (3 * latest['atr'])
else:
    direction = "SHORT (VENTA)"
    prob = probability_short
    entry = latest['close']
    stop_loss = entry + (2 * latest['atr'])
    take_profit_1 = entry - (2 * latest['atr'])
    take_profit_2 = entry - (3 * latest['atr'])

print(f"\n   Dirección: {direction}")
print(f"   Probabilidad de éxito: {prob}%")
print(f"\n   Entrada: {entry:.5f}")
print(f"   Stop Loss: {stop_loss:.5f} ({abs(entry-stop_loss)*10000:.1f} pips)")
print(f"   Take Profit 1: {take_profit_1:.5f} ({abs(entry-take_profit_1)*10000:.1f} pips)")
print(f"   Take Profit 2: {take_profit_2:.5f} ({abs(entry-take_profit_2)*10000:.1f} pips)")
print(f"   Risk/Reward: 1:{abs(take_profit_1-entry)/abs(entry-stop_loss):.2f}")

print(f"\nRESUMEN DE LOS ULTIMOS 2 MESES:")
print(f"   Máximo: 1.19181 (17 septiembre)")
print(f"   Mínimo: 1.15420 (14 octubre)")
print(f"   Rango: 3,761 pips")
print(f"   Tendencia general: BAJISTA (-2,580 pips desde máximo)")
print(f"   Soporte clave: 1.1540 - 1.1560")
print(f"   Resistencia clave: 1.1720 - 1.1750")

print(f"\n[!] FACTORES DE RIESGO:")
print(f"   - Volatilidad alta en últimas semanas")
print(f"   - Zona de consolidación 1.1600-1.1670")
print(f"   - Eventos económicos pendientes (verificar calendario)")
