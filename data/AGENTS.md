<!-- Parent: ../AGENTS.md -->
# data/

## Purpose
Centralized data storage for market data and trading results. Organized by market type and AI model for easy analysis and comparison.

## Subdirectories
- `A_stock/` - A-share (Chinese stock market) historical and real-time data
- `crypto/` - Cryptocurrency market data
- `agent_data/` - Trading results organized by AI model (Claude, GPT-5, Gemini, DeepSeek, MiniMax, Qwen)
- `agent_data_astock_hour/` - Hourly A-share trading data

## For AI Agents
When working with data:
- Market data is separated by type (A_stock, crypto)
- Trading results are organized by AI model in `agent_data/`
- Each AI model has its own subdirectory for performance tracking
- Data formats vary by market (tick data, OHLCV, order book)
- Hourly data is stored separately for A-share market

## Dependencies
- Populated by agents in `../agent/`
- Processed by tools in `../tools/`
- Configured by files in `../configs/`
