# Change Log

## Version History

### v2.2.1 (2025-10-29)
**Temp script approach refined with robust improvements**

- Added timestamp to temp filenames: `temp_scan_{timestamp}.py` (prevents collisions)
- Documented try-finally cleanup pattern for guaranteed file deletion
- Improved error handling and debugging capability
- **Lesson learned:** v3.0 Python one-liner approach FAILED in production
  - Problems: Quote escaping hell, multiline data issues, shell incompatibility
  - Reality: Temp files are pragmatic and acceptable when they work best
  - Philosophy: **Pragmatism > Theoretical Purity**

### v3.0 (2025-10-29)
**EXPERIMENT FAILED - Python one-liner doesn't work in practice**

- Attempted: Direct function call without temp files
- Failed due to: bash quote escaping, multiline CSV data, command length limits
- Key learning: Dogmatic "stateless" purity is wrong. Use what works.

### v2.2 (2025-10-29)
**Fixed new session failures - Temp Python script approach**

- Implemented temporary Python script creation
- Reliable execution across sessions

### v2.1 (2025-10-29)
**Flow Optimization**

- run_scan.py accepts both JSON formats
- Improved data handling flexibility

### v2.0 (2025-10-29)
**Complete redesign - Vibrant HTML reports**

- Added 3 NEW sections (Risk Management, Warnings, Executive Summary)
- Complete HTML rewrite with vibrant design (purple/violet gradients)
- Added run_scan.py direct entry point
- Added timeframe weighting
- Revamped HTML report with Chart.js + Tailwind
- Introduced safe console output and backward compatibility

### Earlier versions
- Initial implementation with basic pattern detection
- Multi-timeframe support
- Probability scoring system
