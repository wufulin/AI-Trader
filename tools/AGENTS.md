<!-- Parent: ../AGENTS.md -->
# tools/

## Purpose
Core trading and analysis tools that provide foundational functionality for the entire system. These tools are market-agnostic and reusable across all agents.

## Key Files
- `calculate_metrics.py` - Performance metrics calculation (returns, Sharpe ratio, drawdown, etc.)
- `general_tools.py` - General utility functions and helpers
- `plot_metrics.py` - Visualization and plotting tools for trading results
- `price_tools.py` - Price data handling, analysis, and market data APIs

## For AI Agents
These are foundational tools used throughout the system:
- **calculate_metrics.py**: Computes trading performance metrics (P&L, win rate, Sharpe ratio, maximum drawdown)
- **general_tools.py**: Common utilities (date handling, data validation, logging)
- **plot_metrics.py**: Creates charts and visualizations for analysis
- **price_tools.py**: Fetches and processes market data from various sources

## Dependencies
- Used by all agents in `../agent/`
- Referenced by tools in `../agent_tools/`
- Output stored in `../data/`
- Configuration from `../configs/`
