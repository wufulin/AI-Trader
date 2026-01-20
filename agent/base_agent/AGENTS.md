<!-- Parent: ../AGENTS.md -->
# base_agent/

## Purpose
Base trading agent implementation for NASDAQ 100 and general markets. This agent serves as the foundation for trading in US markets with standard trading hours and regulations.

## For AI Agents
This is the primary agent for:
- NASDAQ 100 stocks trading
- US market hours (9:30 AM - 4:00 PM ET)
- Standard settlement (T+2)
- No price limits (unlike A-share)
- Pre-market and after-hours trading support

## Dependencies
- Extends base agent functionality
- Uses tools from `../../tools/`
- Configuration from `../../configs/`
- Data storage in `../../data/`
