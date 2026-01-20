<!-- Parent: ../AGENTS.md -->
# base_agent_astock/

## Purpose
Specialized trading agent for A-share (Chinese stock market). Implements market-specific rules and constraints unique to Chinese stock trading.

## For AI Agents
A-share market specifics:
- Trading hours: 9:30 AM - 3:00 PM CST (with lunch break 11:30 AM - 1:00 PM)
- T+1 settlement (can only sell stocks bought the previous day)
- 10% daily price limit (5% for ST stocks)
- Circuit breaker mechanisms
- No after-hours trading
- Different order types and regulations

## Dependencies
- Extends base agent functionality
- Uses tools from `../../tools/`
- Configuration from `../../configs/`
- Data storage in `../../data/A_stock/` and `../../data/agent_data_astock_hour/`
