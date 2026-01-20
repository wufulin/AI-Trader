# AI-Trader

## Purpose
AI-Trader is a comprehensive AI-powered trading system that supports multiple markets (NASDAQ 100, A-share/Chinese stocks, and cryptocurrency) with various AI model agents. The system automates trading strategies, analyzes market data, and tracks performance metrics across different AI agents.

## Key Files
- `main.py` - Main entry point for the trading system
- `main_parrallel.py` - Parallel execution version for running multiple agents simultaneously
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variable template
- `README.md` / `README_CN.md` - Project documentation (English and Chinese)
- `fix_windows_paths.py` / `fix_windows_paths.sh` - Windows path compatibility fixes

## Subdirectories
- `agent/` - Trading agent implementations for different markets
- `agent_tools/` - Agent-specific tools and utilities
- `assets/` - Static assets (images, logos)
- `configs/` - Configuration files for markets and agents
- `data/` - Market data storage and trading results
- `docs/` - Project documentation
- `prompts/` - AI agent prompts and templates
- `tools/` - Core trading and analysis tools

## For AI Agents
This is a multi-market AI trading system. When working here:
- The system supports NASDAQ 100, A-share (Chinese stocks), and cryptocurrency markets
- Multiple AI agents are supported: Claude, GPT-5, Gemini, DeepSeek, MiniMax, Qwen
- Trading results are stored in `data/agent_data/` organized by AI model
- Configuration files in `configs/` control market-specific parameters
- The `tools/` directory contains reusable analysis functions

## Dependencies
- Python 3.x
- Various AI model APIs (Anthropic, OpenAI, Google, etc.)
- Market data APIs for different exchanges
- Data analysis libraries (pandas, numpy)
- Visualization libraries (matplotlib, plotly)

## Architecture
The system follows a modular architecture:
1. **Agents** (`agent/`) - Market-specific trading logic
2. **Tools** (`tools/`) - Core analysis and metrics calculation
3. **Agent Tools** (`agent_tools/`) - Agent-specific utilities
4. **Data** (`data/`) - Organized storage for market data and results
5. **Configs** (`configs/`) - Market and agent configuration
