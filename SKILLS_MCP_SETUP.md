# ✅ Trading Skills + MetaTrader MCP - Configuración Completa

## 📊 Resumen de Cambios

### ✅ Skills Organizados
Todos los skills han sido reorganizados según las **buenas prácticas de Anthropic** para Claude Code:

```
.claude/skills/
├── technical-analysis/      ✅ Con frontmatter YAML
│   └── SKILL.md
├── opportunity-scanner/     ✅ Con frontmatter YAML
│   └── SKILL.md
├── risk-management/         ✅ Con frontmatter YAML
│   └── SKILL.md
├── backtesting/             ✅ Con frontmatter YAML
│   └── SKILL.md
├── advanced-analytics/      ✅ Con frontmatter YAML
│   ├── SKILL.md
│   └── scripts/
│       ├── advanced_statistics.py
│       ├── pattern_recognition.py
│       ├── correlation_analysis.py
│       └── volatility_analysis.py
└── README.md
```

### ✅ Mejoras Implementadas

#### 1. **Frontmatter YAML Correcto**
Todos los skills ahora tienen el formato correcto:
```yaml
---
name: skill-name
description: Descripción específica con términos de activación...
---
```

#### 2. **Descripciones Optimizadas**
- Incluyen términos clave que el usuario mencionaría
- Especifican claramente cuándo usar cada skill
- Máximo 1024 caracteres, concisos y precisos

#### 3. **Estructura Claude Code**
- Cada skill en su propio subdirectorio
- Archivo SKILL.md en cada skill
- Scripts organizados en subdirectorio `scripts/`

### ✅ MetaTrader MCP Configurado

#### Archivo `.mcp.json` creado
```json
{
  "mcpServers": {
    "metatrader": {
      "command": "metatrader-mcp-server",
      "args": [
        "--login", "61424388",
        "--password", "Ve17648947##",
        "--server", "Pepperstone-Demo",
        "--path", "C:\\Program Files\\Pepperstone MetaTrader 5\\terminal64.exe"
      ]
    }
  }
}
```

#### Servidor Instalado
- **Paquete**: metatrader-mcp-server v0.2.9 ✅
- **Ubicación**: `C:\Users\luces\AppData\Local\Programs\Python\Python313\Scripts\`
- **MetaTrader5**: v5.0.5370 ✅

## 🚀 Cómo Usar

### 1. Verificar que los Skills están activos
```bash
# Los skills deberían cargarse automáticamente desde .claude/skills/
# Claude Code detectará el directorio y cargará los skills
```

### 2. Probar un Skill
```bash
# En Claude Code CLI, simplemente di:
"Analiza EURUSD técnicamente"
# Claude automáticamente usará el skill technical-analysis
```

### 3. Verificar MCP Server
```bash
# Listar servidores MCP configurados
claude mcp list

# Debería mostrar el servidor "metatrader" configurado
```

### 4. Probar Integración MetaTrader
```bash
# En Claude Code, prueba:
"Obtén el precio actual de EURUSD"
# Claude usará el servidor MCP de MetaTrader para obtener datos reales
```

## 📝 Ejemplos de Uso Completo

### Ejemplo 1: Análisis Matutino Completo
```
"Buenos días. Necesito:
1. Escaneo del mercado completo
2. Análisis detallado de las top 3 oportunidades
3. Cálculo de tamaño de posición para cada una
4. Evaluación de mi riesgo actual de portfolio"
```

**Claude ejecutará:**
- ✅ opportunity-scanner → Top 3 oportunidades
- ✅ technical-analysis → Análisis detallado de cada una
- ✅ risk-management → Sizing para cada posición
- ✅ Reporte completo en minutos

### Ejemplo 2: Validación de Estrategia
```
"Quiero validar mi estrategia de MA crossover:
- Testea en EURUSD últimos 2 años
- Calcula métricas avanzadas (Sharpe, Sortino)
- Simula 1000 escenarios con Monte Carlo
- Dame probabilidad real de éxito"
```

**Claude ejecutará:**
- ✅ backtesting → Validación histórica
- ✅ advanced-analytics → Métricas avanzadas + Simulación
- ✅ Decisión ultra-informada

### Ejemplo 3: Gestión de Riesgo en Vivo
```
"Tengo 3 posiciones abiertas. Analiza:
- Riesgo total actual
- Correlación entre posiciones
- ¿Puedo abrir otra posición en GBPJPY?"
```

**Claude ejecutará:**
- ✅ risk-management → Portfolio risk assessment
- ✅ advanced-analytics → Correlation analysis
- ✅ Recomendación basada en límites

## 🎯 Próximos Pasos Recomendados

### 1. Probar cada Skill
```bash
# Technical Analysis
"Analiza EURUSD técnicamente"

# Scanner
"Escanea el mercado"

# Risk Management
"Calcula mi riesgo de portfolio"

# Backtesting
"Testea MA crossover en GBPUSD"

# Advanced Analytics
"Calcula mi Sharpe ratio"
```

### 2. Personalizar Configuración (Opcional)

#### Ajustar Probabilidades
Edita `.claude/skills/technical-analysis/SKILL.md`:
```python
# Línea ~104: Ajustar pesos de scoring
score += 15  # Trend alignment (más/menos agresivo)
```

#### Cambiar Símbolos de Escaneo
Edita `.claude/skills/opportunity-scanner/SKILL.md`:
```python
# Línea ~17-25: Agregar tus pares favoritos
priority_list = ['EURUSD', 'TU_PAR_FAVORITO']
```

#### Ajustar Límites de Riesgo
Edita `.claude/skills/risk-management/SKILL.md`:
```python
# Línea ~17-18: Cambiar límites
risk_per_trade = 1.0  # Más conservador
max_portfolio_risk = 5.0
```

### 3. Validar Integración MetaTrader

Ejecuta este test:
```bash
# En Claude Code CLI
"Obtén información de mi cuenta de MetaTrader"
"Muestra mis posiciones abiertas"
"¿Cuál es el precio actual de EURUSD?"
```

Si los comandos funcionan → ✅ MCP configurado correctamente

## 🔧 Troubleshooting

### Skills no se cargan
```bash
# Verificar estructura
ls -la .claude/skills/

# Cada skill debe tener:
# - Subdirectorio propio
# - SKILL.md con frontmatter YAML
```

### MCP Server no conecta
```bash
# Verificar instalación
pip list | grep metatrader

# Debe mostrar: metatrader-mcp-server 0.2.9

# Verificar config
cat .mcp.json

# Probar conexión manual
metatrader-mcp-server --login 61424388 --server Pepperstone-Demo
```

### MetaTrader5 error
```bash
# Verificar que MT5 está instalado
ls "C:\Program Files\Pepperstone MetaTrader 5\terminal64.exe"

# Habilitar trading algorítmico:
# 1. Abrir MT5
# 2. Tools → Options
# 3. Expert Advisors → Enable algorithmic trading
```

## 📚 Documentación Adicional

- **Skills README**: `.claude/skills/README.md`
- **Ejemplos Python**: `trading-skills/PYTHON-EXAMPLES-UPDATED.md`
- **Documentación oficial**: https://docs.claude.com/en/docs/claude-code/skills

## ⚠️ Notas Importantes

1. **Trading en Demo**: La configuración actual usa cuenta demo de Pepperstone
2. **Seguridad**: El archivo `.mcp.json` contiene credenciales - NO compartir públicamente
3. **Backup**: Se recomienda hacer backup del directorio `trading-skills/` original
4. **Skills Personalizados**: Puedes modificar los skills según tus necesidades

## ✅ Checklist de Verificación

- [x] Skills organizados en `.claude/skills/`
- [x] Todos los skills tienen frontmatter YAML
- [x] Scripts Python copiados a `advanced-analytics/scripts/`
- [x] README.md consolidado creado
- [x] Archivo `.mcp.json` configurado
- [x] metatrader-mcp-server instalado (v0.2.9)
- [x] MetaTrader5 instalado (v5.0.5370)
- [ ] Skills probados en Claude Code CLI
- [ ] Conexión MCP validada

---

**Configuración completada el**: 28 de Octubre, 2025
**Siguiente paso**: Probar skills y validar integración MCP
