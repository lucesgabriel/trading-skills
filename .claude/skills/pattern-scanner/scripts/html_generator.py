# -*- coding: utf-8 -*-
"""
HTML Report Generator - Vibrant Educational Trading Reports
Generates beautiful, educational HTML reports with gradients, emojis, and comprehensive trading analysis.
"""

from __future__ import annotations

import json
from datetime import datetime
from math import isfinite
from pathlib import Path
from typing import Any, Dict, Iterable, List

try:
    from .console_utils import safe_print
except ImportError:  # pragma: no cover - standalone execution
    from console_utils import safe_print


# Pattern Emojis Mapping
PATTERN_EMOJIS = {
    'Bullish Engulfing': '🔥',
    'Bearish Engulfing': '❄️',
    'Morning Star': '🌅',
    'Evening Star': '🌆',
    'Hammer': '🔨',
    'Inverted Hammer': '🔨',
    'Shooting Star': '💫',
    'Hanging Man': '🎣',
    'Doji': '🎯',
    'Bullish Harami': '📈',
    'Bearish Harami': '📉',
    'Three White Soldiers': '🚀',
    'Three Black Crows': '🦅',
    'Spinning Top': '🔄',
    'Piercing Line': '⚡',
    'Dark Cloud Cover': '☁️',
}

# Pattern Educational Explanations
PATTERN_EXPLANATIONS = {
    'Bullish Engulfing': "Patrón muy fuerte de reversión alcista. La vela actual envuelve completamente la vela bajista anterior, indicando que los compradores han tomado el control.",
    'Bearish Engulfing': "Potente patrón de reversión bajista. La vela bajista envuelve la vela alcista anterior, señalando que los vendedores dominan el mercado.",
    'Morning Star': "Potente patrón de reversión alcista formado por tres velas. Indica el final de una tendencia bajista y el comienzo de una tendencia alcista.",
    'Evening Star': "Patrón de reversión bajista de tres velas que señala el final de una tendencia alcista. Indica que los vendedores están tomando control.",
    'Hammer': "Patrón de reversión alcista con cuerpo pequeño y mecha inferior larga. Muestra rechazo de precios más bajos y potencial rebote.",
    'Inverted Hammer': "Patrón alcista de reversión con mecha superior larga. Sugiere que los compradores están probando niveles más altos.",
    'Shooting Star': "Patrón bajista de reversión con mecha superior larga. Indica rechazo de precios más altos y potencial caída.",
    'Hanging Man': "Patrón bajista que aparece en tendencias alcistas. Similar al hammer pero con connotación bajista en contexto alcista.",
    'Doji': "Vela de indecisión donde apertura y cierre son casi iguales. Señal de posible reversión cuando aparece en tendencias.",
    'Bullish Harami': "Patrón de reversión alcista formado por una vela pequeña dentro del rango de la vela anterior. Confirma el cambio de sentimiento hacia alcista.",
    'Bearish Harami': "Patrón de reversión bajista con vela pequeña dentro de la anterior. Sugiere debilitamiento del momentum alcista.",
    'Three White Soldiers': "Patrón muy alcista de tres velas consecutivas al alza. Indica fuerte momentum comprador y continuación alcista probable.",
    'Three Black Crows': "Patrón muy bajista de tres velas consecutivas a la baja. Señala fuerte presión vendedora y continuación bajista.",
    'Spinning Top': "Vela de consolidación con mechas largas arriba y abajo. Indica indecisión del mercado y posible cambio de tendencia.",
    'Piercing Line': "Patrón alcista de dos velas donde la segunda cierra por encima del 50% de la primera. Sugiere reversión alcista.",
    'Dark Cloud Cover': "Patrón bajista de dos velas donde la segunda abre arriba pero cierra dentro de la primera. Indica presión vendedora.",
}

# Strength to reliability mapping (default values)
STRENGTH_RELIABILITY = {
    'very strong': 85,
    'strong': 70,
    'medium': 55,
    'weak': 40,
}


def _format_price(value: float) -> str:
    """Format price with appropriate decimal places."""
    if value is None or not isfinite(value):
        return "--"
    abs_value = abs(value)
    if abs_value >= 100:
        return f"{value:.2f}"
    if abs_value >= 10:
        return f"{value:.3f}"
    if abs_value >= 1:
        return f"{value:.5f}"
    return f"{value:.6f}"


def _pip_factor(price: float) -> int:
    """Determine pip factor based on price range."""
    if price >= 1:
        return 10000
    if price >= 0.1:
        return 1000
    if price >= 0.01:
        return 100
    return 10


def _has_data(value: Any) -> bool:
    """Check if value contains meaningful data."""
    if not value:
        return False
    if isinstance(value, dict):
        return any(_has_data(v) for v in value.values())
    if isinstance(value, list):
        return len(value) > 0
    return True


def _select_preferred_timeframe(data: Dict[str, Any], preferences: Iterable[str]) -> str | None:
    """Select the best available timeframe from preferences."""
    for tf in preferences:
        if _has_data(data.get(tf)):
            return tf
    for tf, payload in data.items():
        if _has_data(payload):
            return tf
    return None


def generate_summary_stats(
    patterns_by_timeframe: Dict[str, List[Dict[str, Any]]],
    confluence_results: Dict[str, Any],
    trading_setup: Dict[str, Any]
) -> str:
    """Generate 4 summary stat boxes."""
    total_patterns = sum(len(patterns) for patterns in patterns_by_timeframe.values())
    probability = confluence_results.get('primary_probability', 0)
    bias = confluence_results.get('bias', 'NEUTRAL')
    rr_ratio = trading_setup.get('risk_reward', 0)

    return f"""
    <div class="summary-stats">
        <div class="stat-box">
            <div class="stat-number">{total_patterns}</div>
            <div class="stat-label">Patrones Detectados</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">{probability:.0f}%</div>
            <div class="stat-label">Probabilidad de Éxito</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">{bias.upper()}</div>
            <div class="stat-label">Sesgo del Mercado</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">{f'1:{rr_ratio:.1f}' if rr_ratio else '--'}</div>
            <div class="stat-label">Riesgo/Recompensa</div>
        </div>
    </div>
    """


def generate_pattern_cards(patterns_by_timeframe: Dict[str, List[Dict[str, Any]]]) -> str:
    """Generate pattern cards with emojis, gradients, and explanations."""
    cards = []

    for timeframe, patterns in patterns_by_timeframe.items():
        for pattern in patterns:
            name = pattern.get('name', 'Unknown')
            bias = (pattern.get('bias') or 'Neutral').lower()
            strength = (pattern.get('strength') or 'medium').lower()
            reliability = pattern.get('reliability', STRENGTH_RELIABILITY.get(strength, 50))
            price = _format_price(float(pattern.get('price', 0)))
            time = str(pattern.get('time', ''))

            # Get emoji and explanation
            emoji = PATTERN_EMOJIS.get(name, '🎯')
            explanation = PATTERN_EXPLANATIONS.get(name, 'Patrón de trading detectado por análisis técnico.')

            # Determine card class based on bias
            card_class = 'bullish' if bias == 'bullish' else 'bearish' if bias == 'bearish' else 'neutral'

            # Determine strength class
            strength_class = f'strength-{strength.replace(" ", "-")}'
            strength_text = strength.upper().replace('_', ' ')

            cards.append(f"""
            <div class="card pattern-card {card_class}">
                <span class="timeframe-badge">{timeframe}</span>
                <div class="pattern-name">{emoji} {name}</div>
                <div class="pattern-type">{pattern.get('type', 'Reversión')}</div>
                <div class="pattern-details">
                    <p><strong>Precio:</strong> {price}</p>
                    <p><strong>Hora:</strong> {time}</p>
                    <p style="margin-top: 10px; line-height: 1.6;">
                        {explanation}
                    </p>
                </div>
                <span class="pattern-strength {strength_class}">{strength_text}</span>
            </div>
            """)

    if not cards:
        return '<p style="text-align: center; color: #64748b;">No se detectaron patrones significativos en las últimas velas.</p>'

    return '<div class="grid">' + ''.join(cards) + '</div>'


def generate_indicators_section(
    technical_snapshots: Dict[str, Any],
    selected_timeframe: str | None
) -> str:
    """Generate technical indicators section with progress bars."""
    if not selected_timeframe or selected_timeframe not in technical_snapshots:
        return '<p>Indicadores técnicos no disponibles.</p>'

    snapshot_payload = technical_snapshots[selected_timeframe] or {}
    snapshot = snapshot_payload.get('snapshot') or {}
    scores = snapshot_payload.get('scores') or {}

    rsi_value = float(snapshot.get('rsi', 50.0))
    stoch_value = float(snapshot.get('stochastic_k', 50.0))

    macd_line = float(snapshot.get('macd_line', 0.0))
    macd_signal = float(snapshot.get('macd_signal', 0.0))
    macd_diff = macd_line - macd_signal
    macd_state = "Positivo" if macd_diff > 0 else "Negativo"
    macd_class = "progress-bullish" if macd_diff > 0 else "progress-bearish"

    # Determine RSI state
    if rsi_value > 70:
        rsi_state = "Sobrecompra"
        rsi_class = "progress-bearish"
    elif rsi_value < 30:
        rsi_state = "Sobreventa"
        rsi_class = "progress-bullish"
    else:
        rsi_state = "Neutral"
        rsi_class = "progress-neutral"

    # Determine Stochastic state
    if stoch_value > 80:
        stoch_state = "Sobrecompra"
        stoch_class = "progress-bearish"
    elif stoch_value < 20:
        stoch_state = "Sobreventa"
        stoch_class = "progress-bullish"
    else:
        stoch_state = "Alcista" if stoch_value > 50 else "Bajista"
        stoch_class = "progress-bullish" if stoch_value > 50 else "progress-bearish"

    # Trend indicators
    h4_trend = scores.get('h4_trend', 'Neutral')
    h1_trend = scores.get('h1_trend', 'Neutral')
    m15_trend = scores.get('m15_trend', 'Neutral')

    return f"""
    <div class="grid">
        <div class="card">
            <h3 style="margin-bottom: 15px; color: #1e3c72;">Momentum</h3>

            <div class="indicator-bar">
                <div class="indicator-label">
                    <span>RSI (14)</span>
                    <span class="indicator-value">{rsi_value:.0f}</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill {rsi_class}" style="width: {min(100, rsi_value)}%;">
                        {rsi_state}
                    </div>
                </div>
            </div>

            <div class="indicator-bar">
                <div class="indicator-label">
                    <span>Stochastic %K</span>
                    <span class="indicator-value">{stoch_value:.0f}</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill {stoch_class}" style="width: {min(100, stoch_value)}%;">
                        {stoch_state}
                    </div>
                </div>
            </div>

            <div class="indicator-bar">
                <div class="indicator-label">
                    <span>MACD</span>
                    <span class="indicator-value">{macd_state}</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill {macd_class}" style="width: {65 if macd_diff > 0 else 35}%;">
                        {'Alcista' if macd_diff > 0 else 'Bajista'}
                    </div>
                </div>
            </div>
        </div>

        <div class="card">
            <h3 style="margin-bottom: 15px; color: #1e3c72;">Tendencia</h3>

            <div class="indicator-bar">
                <div class="indicator-label">
                    <span>H4 Trend</span>
                    <span class="indicator-value">{h4_trend}</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill progress-neutral" style="width: 50%;">
                        Consolidación
                    </div>
                </div>
            </div>

            <div class="indicator-bar">
                <div class="indicator-label">
                    <span>H1 Trend</span>
                    <span class="indicator-value">{h1_trend}</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill progress-bullish" style="width: 70%;">
                        Alcista
                    </div>
                </div>
            </div>

            <div class="indicator-bar">
                <div class="indicator-label">
                    <span>M15 Trend</span>
                    <span class="indicator-value">{m15_trend}</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill progress-bullish" style="width: 85%;">
                        Muy Alcista
                    </div>
                </div>
            </div>
        </div>
    </div>
    """


def generate_signal_box(signal: str, probability: float, bias: str) -> str:
    """Generate large, prominent signal box."""
    signal_class = 'bullish' if bias.lower() == 'bullish' else 'bearish' if bias.lower() == 'bearish' else 'neutral'

    if 'BUY' in signal.upper() or 'LONG' in signal.upper():
        signal_icon = '🚀'
        signal_text = 'SEÑAL: COMPRA (LONG)'
    elif 'SELL' in signal.upper() or 'SHORT' in signal.upper():
        signal_icon = '📉'
        signal_text = 'SEÑAL: VENTA (SHORT)'
    else:
        signal_icon = '⏸️'
        signal_text = 'SEÑAL: ESPERAR'

    return f"""
    <div class="signal-box {signal_class}">
        <div class="signal-title">{signal_icon} {signal_text}</div>
        <div class="signal-probability">{probability:.0f}%</div>
        <div class="signal-details">
            Probabilidad de Éxito Basada en Confluencias Múltiples
        </div>
    </div>
    """


def generate_trading_setup(
    trading_setup: Dict[str, Any],
    current_price: float,
    pip_factor: int
) -> str:
    """Generate complete trading setup with Entry/SL/TP1/TP2/TP3."""
    entry = trading_setup.get('entry', current_price)
    stop_loss = trading_setup.get('stop_loss', entry)
    take_profits = trading_setup.get('take_profits', [])
    risk_pips = trading_setup.get('risk_pips', 0)
    rr_ratio = trading_setup.get('risk_reward', 0)
    bias = trading_setup.get('bias', 'Neutral')

    # Generate TP rows
    tp_rows_html = ""
    for idx, tp_data in enumerate(take_profits[:3], start=1):
        tp_price = tp_data.get('price', entry)
        tp_pips = tp_data.get('pips', 0)
        tp_rows_html += f"""
        <div class="trade-row">
            <span class="trade-label">Take Profit {idx}:</span>
            <span class="trade-value" style="color: #10b981;">{_format_price(tp_price)} (+{tp_pips:.0f} pips)</span>
        </div>
        """

    # Entry recommendations
    if bias.lower() == 'bullish':
        entry_aggressive = f"{_format_price(entry)} - {_format_price(entry + 20/pip_factor)}"
        entry_conservative = f"Esperar ruptura > {_format_price(entry + 40/pip_factor)}"
    elif bias.lower() == 'bearish':
        entry_aggressive = f"{_format_price(entry)} - {_format_price(entry - 20/pip_factor)}"
        entry_conservative = f"Esperar ruptura < {_format_price(entry - 40/pip_factor)}"
    else:
        entry_aggressive = f"{_format_price(entry)}"
        entry_conservative = "Esperar confirmación de tendencia"

    return f"""
    <div class="trade-setup">
        <h3 style="margin-bottom: 20px; color: #1e3c72; font-size: 1.4em;">
            📋 Configuración del Trade
        </h3>

        <div class="trade-row">
            <span class="trade-label">Entrada Agresiva:</span>
            <span class="trade-value">{entry_aggressive}</span>
        </div>
        <div class="trade-row">
            <span class="trade-label">Entrada Conservadora:</span>
            <span class="trade-value">{entry_conservative}</span>
        </div>
        <div class="trade-row">
            <span class="trade-label">Stop Loss:</span>
            <span class="trade-value" style="color: #ef4444;">{_format_price(stop_loss)} (-{risk_pips:.0f} pips)</span>
        </div>
        {tp_rows_html}
        <div class="trade-row">
            <span class="trade-label">Riesgo/Recompensa:</span>
            <span class="trade-value">{f'1:{rr_ratio:.1f}' if rr_ratio else '--'}</span>
        </div>
    </div>
    """


def generate_risk_management(risk_pips: float, pip_factor: int) -> str:
    """Generate NEW risk management section."""
    # Position sizing calculations
    account_10k = 10000
    account_1k = 1000
    risk_percent = 2.0

    # Calculate position sizes (simplified)
    pip_value = 10  # USD per pip for 1 standard lot
    risk_amount_10k = account_10k * (risk_percent / 100)
    risk_amount_1k = account_1k * (risk_percent / 100)

    position_10k = risk_amount_10k / (risk_pips * pip_value) if risk_pips > 0 else 0
    position_1k = risk_amount_1k / (risk_pips * pip_value) if risk_pips > 0 else 0

    return f"""
    <div class="section">
        <h2 class="section-title">
            <span class="icon">⚠️</span>
            Gestión de Riesgo
        </h2>

        <div class="warning-box">
            <div class="warning-title">🛡️ Reglas de Gestión de Riesgo</div>
            <ul class="warning-list">
                <li><strong>Nunca arriesgue más del 2% de su cuenta por operación</strong></li>
                <li>Siempre use stop loss antes de entrar al trade</li>
                <li>Escale salidas en cada nivel de Take Profit (33% cada uno)</li>
                <li>Mueva el stop loss a breakeven después de alcanzar TP1</li>
                <li>Use trailing stop de 80 pips después de TP2</li>
                <li>Verifique el calendario económico antes de operar</li>
                <li>No opere durante anuncios importantes (ECB, Fed, NFP)</li>
            </ul>
        </div>

        <div class="card" style="margin-top: 20px;">
            <h3 style="margin-bottom: 15px; color: #1e3c72;">💰 Cálculo de Posición</h3>

            <div class="trade-row">
                <span class="trade-label">Cuenta de ${account_10k:,.0f} ({risk_percent}% riesgo):</span>
                <span class="trade-value">{position_10k:.2f} lotes estándar</span>
            </div>
            <div class="trade-row">
                <span class="trade-label">Cuenta de ${account_1k:,.0f} ({risk_percent}% riesgo):</span>
                <span class="trade-value">{position_1k:.3f} lotes estándar</span>
            </div>
            <div class="trade-row">
                <span class="trade-label">Distancia del Stop Loss:</span>
                <span class="trade-value">{risk_pips:.0f} pips</span>
            </div>
            <div class="trade-row">
                <span class="trade-label">Riesgo en dólares (${account_10k:,.0f} cuenta):</span>
                <span class="trade-value">${risk_amount_10k:.0f}</span>
            </div>
        </div>
    </div>
    """


def generate_warnings(bias: str, current_price: float, pip_factor: int) -> str:
    """Generate NEW warnings and risk factors section."""
    # Calculate invalidation level
    if bias.lower() == 'bullish':
        invalidation = current_price - (100 / pip_factor)
    else:
        invalidation = current_price + (100 / pip_factor)

    return f"""
    <div class="section">
        <h2 class="section-title">
            <span class="icon">🚨</span>
            Advertencias y Factores de Riesgo
        </h2>

        <div class="warning-box" style="background: #fee2e2; border-left-color: #dc2626;">
            <div class="warning-title" style="color: #991b1b;">⚠️ Factores de Alto Riesgo</div>
            <ul class="warning-list" style="color: #991b1b;">
                <li>H4 todavía en estructura bajista (máximos más bajos)</li>
                <li>Fase de consolidación puede ser volátil</li>
                <li>Eventos noticiosos pueden invalidar patrones técnicos</li>
                <li>Períodos de baja liquidez pueden causar deslizamiento</li>
                <li>Spread puede ampliarse durante noticias importantes</li>
            </ul>
        </div>

        <div class="card" style="margin-top: 20px; background: #fffbeb; border: 2px solid #f59e0b;">
            <h3 style="margin-bottom: 15px; color: #78350f;">👁️ Monitorear Señales de Invalidación</h3>
            <ul style="line-height: 2; color: #78350f;">
                <li>❌ Ruptura por {'debajo' if bias.lower() == 'bullish' else 'encima'} de {_format_price(invalidation)} (invalida configuración {bias.lower()})</li>
                <li>❌ {'Bearish' if bias.lower() == 'bullish' else 'Bullish'} Engulfing en H1 (señal de reversión)</li>
                <li>❌ Divergencia {'bajista' if bias.lower() == 'bullish' else 'alcista'} del RSI</li>
                <li>❌ MACD cruce {'bajista' if bias.lower() == 'bullish' else 'alcista'}</li>
                <li>❌ Volumen decreciente en la {'subida' if bias.lower() == 'bullish' else 'bajada'}</li>
            </ul>
        </div>
    </div>
    """


def generate_executive_summary(
    signal: str,
    probability: float,
    bias: str,
    patterns_count: int,
    current_price: float,
    pip_factor: int
) -> str:
    """Generate NEW executive summary section."""
    # Determine confidence level
    if probability >= 70:
        confidence = "Alta confianza"
    elif probability >= 60:
        confidence = "Confianza moderada"
    else:
        confidence = "Confianza baja"

    # Generate action recommendation
    if bias.lower() == 'bullish':
        action_text = f"""
        ⏰ ESPERAR CONFIRMACIÓN antes de entrar:<br>
        ✓ Cierre de vela M15 por encima de {_format_price(current_price + 20/pip_factor)}<br>
        ✓ Aumento de volumen en la ruptura<br>
        ✓ Sin patrones bajistas formándose<br>
        ✓ Verificar calendario de noticias
        """
        best_entry = f"Retroceso a {_format_price(current_price - 10/pip_factor)}-{_format_price(current_price)} con vela alcista M15"
    elif bias.lower() == 'bearish':
        action_text = f"""
        ⏰ ESPERAR CONFIRMACIÓN antes de entrar:<br>
        ✓ Cierre de vela M15 por debajo de {_format_price(current_price - 20/pip_factor)}<br>
        ✓ Aumento de volumen en la ruptura<br>
        ✓ Sin patrones alcistas formándose<br>
        ✓ Verificar calendario de noticias
        """
        best_entry = f"Retroceso a {_format_price(current_price)}-{_format_price(current_price + 10/pip_factor)} con vela bajista M15"
    else:
        action_text = """
        ⏰ MANTENERSE AL MARGEN:<br>
        ✓ Esperar señal clara alcista o bajista<br>
        ✓ Monitorear para ruptura de consolidación<br>
        ✓ No operar en ambigüedad<br>
        ✓ Preservar capital
        """
        best_entry = "Esperar definición clara del mercado"

    return f"""
    <div class="section">
        <h2 class="section-title">
            <span class="icon">📝</span>
            Resumen Ejecutivo
        </h2>

        <div class="card" style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border: 2px solid #3b82f6;">
            <h3 style="color: #1e40af; margin-bottom: 20px; font-size: 1.5em;">
                🎯 Recomendación Final
            </h3>

            <div style="font-size: 1.1em; line-height: 2; color: #1e3c72;">
                <p style="margin-bottom: 15px;">
                    <strong>Estado Actual del Mercado:</strong><br>
                    {f'Reversión {bias.lower()} formándose con {patterns_count} patrón{"es" if patterns_count != 1 else ""} detectado{"s" if patterns_count != 1 else ""}'}
                </p>

                <p style="margin-bottom: 15px;">
                    <strong>Señal:</strong><br>
                    <span style="color: {'#10b981' if bias.lower() == 'bullish' else '#ef4444' if bias.lower() == 'bearish' else '#f59e0b'}; font-weight: bold; font-size: 1.2em;">
                        {signal.upper()} - SESGO {bias.upper()}
                    </span>
                </p>

                <p style="margin-bottom: 15px;">
                    <strong>Probabilidad de Éxito:</strong><br>
                    <span style="color: #3b82f6; font-weight: bold; font-size: 1.2em;">{probability:.0f}%</span>
                    ({confidence} basada en múltiples confluencias)
                </p>

                <p style="margin-bottom: 15px;">
                    <strong>Acción Recomendada:</strong><br>
                    <span style="background: #fef3c7; padding: 10px; border-radius: 5px; display: inline-block; margin-top: 5px;">
                        {action_text}
                    </span>
                </p>

                <p style="margin-bottom: 15px;">
                    <strong>Mejor Entrada:</strong><br>
                    {best_entry}
                </p>

                <p style="background: {'#dcfce7' if probability >= 65 else '#fef3c7'}; padding: 15px; border-radius: 10px; margin-top: 20px; border-left: 5px solid {'#10b981' if probability >= 65 else '#f59e0b'};">
                    <strong style="color: {'#166534' if probability >= 65 else '#78350f'};">💎 Veredicto Final:</strong><br>
                    <span style="color: {'#15803d' if probability >= 65 else '#78350f'};">
                        Configuración de {'ALTA' if probability >= 70 else 'MODERADA' if probability >= 60 else 'BAJA'} PROBABILIDAD con gestión de riesgo adecuada.
                        {'La combinación de patrones fuertes, confirmación de indicadores y buen ratio riesgo/recompensa hacen que esta sea una operación atractiva.' if probability >= 65 else 'Se recomienda precaución y esperar confirmaciones adicionales antes de entrar.'}
                    </span>
                </p>
            </div>
        </div>
    </div>
    """


def generate_chart_javascript(chart_data: List[Dict[str, Any]], timeframe: str) -> str:
    """Generate Chart.js initialization script."""
    return f"""
    <script>
        // Candlestick Chart
        const ctx = document.getElementById('candlestickChart').getContext('2d');

        // Price data from analysis
        const priceData = {json.dumps(chart_data[-50:], ensure_ascii=False)};

        new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: priceData.map(d => d.time),
                datasets: [{{
                    label: '{timeframe}',
                    data: priceData.map(d => [d.l, d.o, d.c, d.h]),
                    backgroundColor: priceData.map(d =>
                        d.c >= d.o ? 'rgba(16, 185, 129, 0.8)' : 'rgba(239, 68, 68, 0.8)'
                    ),
                    borderColor: priceData.map(d =>
                        d.c >= d.o ? 'rgb(16, 185, 129)' : 'rgb(239, 68, 68)'
                    ),
                    borderWidth: 2,
                    barThickness: 30
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: true,
                        position: 'top'
                    }},
                    title: {{
                        display: true,
                        text: 'Últimas Velas - {timeframe}',
                        font: {{
                            size: 16
                        }}
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                const data = priceData[context.dataIndex];
                                return [
                                    'Apertura: ' + data.o.toFixed(5),
                                    'Máximo: ' + data.h.toFixed(5),
                                    'Mínimo: ' + data.l.toFixed(5),
                                    'Cierre: ' + data.c.toFixed(5)
                                ];
                            }}
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: false,
                        ticks: {{
                            callback: function(value) {{
                                return value.toFixed(5);
                            }}
                        }}
                    }}
                }}
            }}
        }});
    </script>
    """


def _build_chart_dataset(candles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Build chart dataset from candles."""
    dataset: List[Dict[str, Any]] = []
    for candle in candles[-120:]:
        try:
            dataset.append({
                "time": candle.get("time"),
                "o": float(candle.get("open")),
                "h": float(candle.get("high")),
                "l": float(candle.get("low")),
                "c": float(candle.get("close")),
            })
        except (TypeError, ValueError):
            continue
    return dataset


def _compute_trading_setup(
    confluence_results: Dict[str, Any],
    current_price: float,
    support_resistance: Dict[str, Dict[str, Any]],
    pip_factor: int,
) -> Dict[str, Any]:
    """Compute trading setup with entry, SL, and TPs."""
    bias = confluence_results.get("bias", "Neutral")
    signal = confluence_results.get("signal", "NEUTRAL (WAIT)")
    preferred_tf = _select_preferred_timeframe(support_resistance, ("H1", "M15", "H4", "D1"))
    levels = support_resistance.get(preferred_tf or "", {})

    resistances = sorted(
        [float(level) for level in levels.get("resistance", []) if isinstance(level, (int, float))]
    )
    supports = sorted(
        [float(level) for level in levels.get("support", []) if isinstance(level, (int, float))]
    )
    pivot = levels.get("pivot")
    entry = current_price

    def _fallback_tp(direction: str) -> List[float]:
        offsets = (20, 40, 60)
        if direction == "Bullish":
            return [entry + off / pip_factor for off in offsets]
        return [entry - off / pip_factor for off in offsets]

    if bias == "Bullish":
        downside = [level for level in supports if level < current_price]
        upside = [level for level in resistances if level > current_price]
        stop_loss = downside[-1] if downside else current_price - (150 / pip_factor)
        take_profits = upside[:3] if upside else _fallback_tp("Bullish")
    elif bias == "Bearish":
        upside = [level for level in resistances if level > current_price]
        downside = [level for level in supports if level < current_price]
        stop_loss = upside[0] if upside else current_price + (150 / pip_factor)
        take_profits = (
            list(reversed(sorted(downside)[-3:])) if downside else _fallback_tp("Bearish")
        )
    else:
        stop_loss = pivot if isinstance(pivot, (int, float)) else current_price
        take_profits = resistances[:1] + list(reversed(sorted(supports)[-1:])) or _fallback_tp("Bullish")

    risk_pips = abs(entry - stop_loss) * pip_factor
    primary_tp = take_profits[0] if take_profits else entry
    reward_pips = abs(primary_tp - entry) * pip_factor
    risk_reward = reward_pips / risk_pips if risk_pips else None

    tp_rows = []
    for idx, level in enumerate(take_profits[:3], start=1):
        diff_pips = (level - entry) * pip_factor if bias == "Bullish" else (entry - level) * pip_factor
        tp_rows.append({
            "label": f"TP{idx}",
            "price": level,
            "pips": abs(diff_pips),
        })

    return {
        "signal": signal,
        "bias": bias,
        "entry": entry,
        "stop_loss": stop_loss,
        "take_profits": tp_rows,
        "risk_pips": risk_pips,
        "risk_reward": risk_reward,
        "timeframe": preferred_tf,
    }


def _render_sr_table(
    support_resistance: Dict[str, Dict[str, Any]],
    current_price: float,
    pip_factor: int
) -> str:
    """Render support/resistance table."""
    rows = []

    for timeframe, levels in support_resistance.items():
        resistances = sorted(
            [float(level) for level in levels.get("resistance", []) if isinstance(level, (int, float))]
        )
        supports = sorted(
            [float(level) for level in levels.get("support", []) if isinstance(level, (int, float))]
        )

        for idx, level in enumerate(resistances[:3], start=1):
            distance = (level - current_price) * pip_factor
            rows.append({
                'type': f'R{idx}',
                'level': level,
                'distance': distance,
                'timeframe': timeframe,
            })

        for idx, level in enumerate(reversed(supports[-3:]), start=1):
            distance = (level - current_price) * pip_factor
            rows.append({
                'type': f'S{idx}',
                'level': level,
                'distance': distance,
                'timeframe': timeframe,
            })

    if not rows:
        return '<p style="text-align: center; color: #64748b;">Sin niveles claros de soporte/resistencia.</p>'

    # Sort by absolute distance
    rows.sort(key=lambda x: abs(x['distance']))
    rows = rows[:7]  # Top 7 nearest levels

    table_html = """
    <table class="levels-table">
        <thead>
            <tr>
                <th>Nivel</th>
                <th>Precio</th>
                <th>Tipo</th>
                <th>Distancia</th>
            </tr>
        </thead>
        <tbody>
    """

    for row in rows:
        level_class = 'level-resistance' if 'R' in row['type'] else 'level-support'
        table_html += f"""
            <tr>
                <td><span class="{level_class}">{row['type']} ({row['timeframe']})</span></td>
                <td>{_format_price(row['level'])}</td>
                <td>{'Resistencia' if 'R' in row['type'] else 'Soporte'}</td>
                <td>{row['distance']:+.0f} pips</td>
            </tr>
        """

    # Current price row
    table_html += f"""
            <tr class="level-current">
                <td><strong>ACTUAL</strong></td>
                <td><strong>{_format_price(current_price)}</strong></td>
                <td>Precio Actual</td>
                <td>-</td>
            </tr>
        </tbody>
    </table>
    """

    return table_html


def _render_confluence_factors(confluence_results: Dict[str, Any]) -> str:
    """Render confluence factors list."""
    factors = confluence_results.get('confluence_factors', [])

    if not factors:
        return '<p>Sin factores de confluencia disponibles.</p>'

    items_html = ""
    for factor in factors:
        items_html += f'<li>✓ {factor}</li>'

    probability = confluence_results.get('primary_probability', 0)

    return f"""
    <div style="margin-top: 20px; padding: 20px; background: #f0fdf4; border-radius: 10px;">
        <h4 style="color: #166534; margin-bottom: 15px; font-size: 1.2em;">
            ✅ Factores de Confluencia (+{probability:.0f}%)
        </h4>
        <ul style="line-height: 2; color: #15803d;">
            {items_html}
        </ul>
    </div>
    """


def generate_html_report(
    symbol: str,
    scan_results: Dict[str, Any],
    confluence_results: Dict[str, Any],
    output_dir: str | None = None
) -> str:
    """
    Generate complete vibrant HTML report from scan and confluence results.
    Adopts the beautiful design from the preferred HTML template.
    """
    output_path = Path(output_dir) if output_dir else Path.cwd() / "reports"
    output_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"{symbol}_pattern_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    filepath = output_path / filename

    current_price = float(scan_results.get("current_price", 0.0))
    pip_factor = _pip_factor(current_price)

    candles_map = scan_results.get("candles", {})
    patterns_by_tf = scan_results.get("patterns_by_timeframe", {})

    # Select preferred timeframe for chart
    chart_timeframe = _select_preferred_timeframe(candles_map, ("H1", "M15", "H4", "D1"))
    chart_dataset = _build_chart_dataset(candles_map.get(chart_timeframe, [])) if chart_timeframe else []

    # Compute trading setup
    trading_setup = _compute_trading_setup(
        confluence_results,
        current_price,
        scan_results.get("support_resistance", {}),
        pip_factor,
    )

    # Select indicator timeframe
    indicator_tf = _select_preferred_timeframe(scan_results.get("technical_snapshots", {}), ("H1", "H4", "M15", "D1"))

    # Get signal and probability
    signal = confluence_results.get('signal', 'NEUTRAL (WAIT)')
    probability = confluence_results.get('primary_probability', 50)
    bias = confluence_results.get('bias', 'Neutral')

    # Count patterns
    total_patterns = sum(len(patterns) for patterns in patterns_by_tf.values())

    # Determine price direction class
    price_class = 'up' if bias.lower() == 'bullish' else 'down'

    # Generate all sections
    summary_stats_html = generate_summary_stats(patterns_by_tf, confluence_results, trading_setup)
    pattern_cards_html = generate_pattern_cards(patterns_by_tf)
    indicators_html = generate_indicators_section(scan_results.get("technical_snapshots", {}), indicator_tf)
    signal_box_html = generate_signal_box(signal, probability, bias)
    trading_setup_html = generate_trading_setup(trading_setup, current_price, pip_factor)
    sr_table_html = _render_sr_table(scan_results.get("support_resistance", {}), current_price, pip_factor)
    confluence_factors_html = _render_confluence_factors(confluence_results)
    risk_management_html = generate_risk_management(trading_setup.get('risk_pips', 0), pip_factor)
    warnings_html = generate_warnings(bias, current_price, pip_factor)
    executive_summary_html = generate_executive_summary(signal, probability, bias, total_patterns, current_price, pip_factor)
    chart_script = generate_chart_javascript(chart_dataset, chart_timeframe or 'H1')

    # Build complete HTML with embedded CSS (copied from preferred template)
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{symbol} - Análisis Técnico y Patrones de Velas</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}

        .header .price {{
            font-size: 3em;
            font-weight: bold;
            margin: 20px 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}

        .header .price.up {{
            color: #4ade80;
        }}

        .header .price.down {{
            color: #f87171;
        }}

        .header .meta {{
            font-size: 1.1em;
            opacity: 0.9;
        }}

        .content {{
            padding: 30px;
        }}

        .section {{
            margin-bottom: 40px;
        }}

        .section-title {{
            font-size: 1.8em;
            color: #1e3c72;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .icon {{
            font-size: 1.2em;
        }}

        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .card {{
            background: #f8fafc;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}

        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 12px rgba(0,0,0,0.15);
        }}

        .pattern-card {{
            border-left: 5px solid #667eea;
        }}

        .pattern-card.bullish {{
            border-left-color: #10b981;
            background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        }}

        .pattern-card.bearish {{
            border-left-color: #ef4444;
            background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        }}

        .pattern-card.neutral {{
            border-left-color: #f59e0b;
            background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        }}

        .pattern-name {{
            font-size: 1.4em;
            font-weight: bold;
            margin-bottom: 10px;
            color: #1e3c72;
        }}

        .pattern-type {{
            font-size: 1.1em;
            color: #64748b;
            margin-bottom: 5px;
        }}

        .pattern-strength {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
            margin-top: 10px;
        }}

        .strength-very-strong {{
            background: #10b981;
            color: white;
        }}

        .strength-strong {{
            background: #3b82f6;
            color: white;
        }}

        .strength-medium {{
            background: #f59e0b;
            color: white;
        }}

        .strength-weak {{
            background: #94a3b8;
            color: white;
        }}

        .timeframe-badge {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 3px 10px;
            border-radius: 15px;
            font-size: 0.85em;
            font-weight: bold;
            margin-right: 10px;
        }}

        .indicator-bar {{
            margin: 15px 0;
        }}

        .indicator-label {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 5px;
            font-weight: 600;
        }}

        .indicator-value {{
            color: #667eea;
        }}

        .progress-bar {{
            height: 25px;
            background: #e2e8f0;
            border-radius: 12px;
            overflow: hidden;
            position: relative;
        }}

        .progress-fill {{
            height: 100%;
            transition: width 1s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 0.9em;
        }}

        .progress-bullish {{
            background: linear-gradient(90deg, #10b981 0%, #059669 100%);
        }}

        .progress-bearish {{
            background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%);
        }}

        .progress-neutral {{
            background: linear-gradient(90deg, #f59e0b 0%, #d97706 100%);
        }}

        .levels-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}

        .levels-table th,
        .levels-table td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
        }}

        .levels-table th {{
            background: #f1f5f9;
            font-weight: 600;
            color: #1e3c72;
        }}

        .level-resistance {{
            color: #ef4444;
            font-weight: bold;
        }}

        .level-support {{
            color: #10b981;
            font-weight: bold;
        }}

        .level-current {{
            background: #fef3c7;
            font-weight: bold;
        }}

        .signal-box {{
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            margin: 30px 0;
        }}

        .signal-box.bullish {{
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
        }}

        .signal-box.bearish {{
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            color: white;
        }}

        .signal-box.neutral {{
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            color: white;
        }}

        .signal-title {{
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 15px;
        }}

        .signal-probability {{
            font-size: 3em;
            font-weight: bold;
            margin: 20px 0;
        }}

        .signal-details {{
            font-size: 1.2em;
            line-height: 1.8;
        }}

        .trade-setup {{
            background: #f8fafc;
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #e2e8f0;
        }}

        .trade-row {{
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid #e2e8f0;
        }}

        .trade-row:last-child {{
            border-bottom: none;
        }}

        .trade-label {{
            font-weight: 600;
            color: #64748b;
        }}

        .trade-value {{
            font-weight: bold;
            color: #1e3c72;
        }}

        .chart-container {{
            position: relative;
            height: 400px;
            margin: 20px 0;
        }}

        .warning-box {{
            background: #fef3c7;
            border-left: 5px solid #f59e0b;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }}

        .warning-title {{
            font-weight: bold;
            color: #92400e;
            margin-bottom: 10px;
            font-size: 1.2em;
        }}

        .warning-list {{
            list-style-position: inside;
            color: #78350f;
            line-height: 1.8;
        }}

        .summary-stats {{
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            gap: 20px;
            margin: 30px 0;
        }}

        .stat-box {{
            flex: 1;
            min-width: 200px;
            text-align: center;
            padding: 20px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }}

        .stat-label {{
            font-size: 1em;
            color: #64748b;
            margin-top: 5px;
        }}

        .footer {{
            background: #1e3c72;
            color: white;
            padding: 20px;
            text-align: center;
            font-size: 0.9em;
        }}

        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 1.8em;
            }}

            .header .price {{
                font-size: 2em;
            }}

            .grid {{
                grid-template-columns: 1fr;
            }}

            .summary-stats {{
                flex-direction: column;
            }}
        }}

        @media print {{
            body {{
                background: white;
            }}

            .container {{
                box-shadow: none;
            }}

            .card:hover {{
                transform: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>📊 {symbol} - Análisis Técnico Completo</h1>
            <div class="price {price_class}">{_format_price(current_price)}</div>
            <div class="meta">
                ⏰ {timestamp} UTC | 💹 Spread: 0 pips
            </div>
        </div>

        <!-- Content -->
        <div class="content">
            <!-- Summary Stats -->
            {summary_stats_html}

            <!-- Candlestick Patterns Section -->
            <div class="section">
                <h2 class="section-title">
                    <span class="icon">🕯️</span>
                    Patrones de Velas Detectados
                </h2>
                {pattern_cards_html}
            </div>

            <!-- Candlestick Chart -->
            <div class="section">
                <h2 class="section-title">
                    <span class="icon">📊</span>
                    Gráfico de Velas ({chart_timeframe or '--'})
                </h2>
                <div class="chart-container">
                    <canvas id="candlestickChart"></canvas>
                </div>
            </div>

            <!-- Technical Indicators -->
            <div class="section">
                <h2 class="section-title">
                    <span class="icon">📈</span>
                    Indicadores Técnicos
                </h2>
                {indicators_html}
            </div>

            <!-- Support & Resistance -->
            <div class="section">
                <h2 class="section-title">
                    <span class="icon">🎯</span>
                    Niveles Clave de Soporte y Resistencia
                </h2>
                {sr_table_html}
            </div>

            <!-- Trading Signal -->
            <div class="section">
                <h2 class="section-title">
                    <span class="icon">💡</span>
                    Señal de Trading
                </h2>
                {signal_box_html}
                {trading_setup_html}
                {confluence_factors_html}
            </div>

            <!-- Risk Management (NEW) -->
            {risk_management_html}

            <!-- Warnings (NEW) -->
            {warnings_html}

            <!-- Executive Summary (NEW) -->
            {executive_summary_html}

            <!-- Disclaimer -->
            <div class="warning-box" style="margin-top: 30px;">
                <div class="warning-title">📌 Descargo de Responsabilidad</div>
                <p style="color: #78350f; line-height: 1.8;">
                    Este análisis es de naturaleza educativa y no constituye asesoramiento financiero.
                    Los patrones de velas y análisis técnico son probabilísticos, no garantías.
                    El trading de divisas implica un riesgo significativo de pérdida. Siempre opere
                    con capital que pueda permitirse perder y use una gestión de riesgo adecuada.
                    Los resultados pasados no garantizan resultados futuros. Consulte con un asesor
                    financiero calificado antes de tomar decisiones de inversión.
                </p>
            </div>
        </div>

        <!-- Footer -->
        <div class="footer">
            <p>🤖 Generado por Claude Code - Sistema de Análisis Técnico Automatizado</p>
            <p style="margin-top: 10px; opacity: 0.8;">
                © 2025 | Reporte generado el {timestamp} UTC
            </p>
        </div>
    </div>

    {chart_script}

    <script>
        // Add animation on load
        document.addEventListener('DOMContentLoaded', function() {{
            const cards = document.querySelectorAll('.card');
            cards.forEach((card, index) => {{
                setTimeout(() => {{
                    card.style.opacity = '0';
                    card.style.transform = 'translateY(20px)';
                    card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                    setTimeout(() => {{
                        card.style.opacity = '1';
                        card.style.transform = 'translateY(0)';
                    }}, 50);
                }}, index * 100);
            }});
        }});
    </script>
</body>
</html>"""

    filepath.write_text(html_content, encoding="utf-8")

    safe_print(f"✅ Reporte HTML generado: {filepath}")

    return str(filepath)


def save_report_to_file(html_content: str, symbol: str, output_dir: str | None = None) -> str:
    """Save pre-rendered HTML content to disk."""
    output_path = Path(output_dir) if output_dir else Path.cwd() / "reports"
    output_path.mkdir(parents=True, exist_ok=True)

    filename = f"{symbol}_pattern_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    filepath = output_path / filename
    filepath.write_text(html_content, encoding="utf-8")

    safe_print(f"✅ Reporte guardado: {filepath}")

    return str(filepath)


if __name__ == "__main__":
    safe_print("HTML Generator Module Loaded Successfully - Vibrant Mode Enabled")
