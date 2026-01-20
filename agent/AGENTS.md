<!-- Parent: ../AGENTS.md -->
# agent/

## Purpose
Contains trading agent implementations specialized for different markets. Each agent is tailored to specific market characteristics, trading hours, and data formats.

## Subdirectories
- `base_agent/` - Base trading agent for NASDAQ 100 and general markets
- `base_agent_astock/` - Specialized agent for A-share (Chinese stock market)
- `base_agent_crypto/` - Cryptocurrency trading agent

## For AI Agents
Each subdirectory contains a complete trading agent implementation:
- Agents are market-specific due to different trading hours, regulations, and data formats
- A-share market has unique constraints (T+1 trading, 10% price limits, circuit breakers)
- Crypto markets operate 24/7 with high volatility
- NASDAQ agent focuses on US market hours and regulations

## Dependencies
- Parent directory tools (`../tools/`)
- Configuration from `../configs/`
- Data storage in `../data/`
