<!-- Parent: ../AGENTS.md -->
# base_agent_crypto/

## Purpose
Cryptocurrency trading agent designed for 24/7 crypto markets with high volatility and unique market dynamics.

## For AI Agents
Crypto market characteristics:
- 24/7 trading (no market close)
- High volatility and rapid price movements
- No circuit breakers or price limits
- Different order types (limit, market, stop-limit)
- Multiple exchanges with different APIs
- Lower liquidity on smaller tokens
- Higher risk/reward profile

## Dependencies
- Extends base agent functionality
- Uses tools from `../../tools/`
- Configuration from `../../configs/`
- Data storage in `../../data/crypto/`
