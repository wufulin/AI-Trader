<!-- Parent: ../AGENTS.md -->
# configs/

## Purpose
Configuration files for different markets, agents, and trading parameters. These files control system behavior without requiring code changes.

## For AI Agents
Configuration files typically include:
- Market-specific parameters (trading hours, tick sizes, limits)
- Agent behavior settings (risk tolerance, position sizing)
- API credentials and endpoints
- Data source configurations
- Trading strategy parameters

## Dependencies
- Used by all agents in `../agent/`
- Referenced by tools in `../tools/`
- Affects data storage in `../data/`
