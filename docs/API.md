# AI-Trader API Documentation

## Overview

AI-Trader exposes MCP (Model Context Protocol) endpoints for autonomous trading operations. All tools follow the standard MCP specification for easy integration with AI agents.

## Security

### Authentication

AI-Trader supports optional API key authentication for all trading endpoints:

```python
# Enable authentication by setting MCP_API_KEY in .env
MCP_API_KEY=your-secure-api-key-here

# Generate a secure key:
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Authentication Flow:**
1. Tools check `MCP_API_KEY` environment variable
2. If empty, authentication is disabled (development mode)
3. If set, tools validate the `api_key` parameter using constant-time comparison
4. Invalid keys return `PermissionError`

**Security Best Practices:**
- Always set `MCP_API_KEY` in production
- Use strong, randomly generated keys (32+ characters)
- Rotate keys regularly
- Never commit `.env` with real keys to version control

---

## Trading Tools

### Stock Trading (US & A-Shares)

#### `buy(symbol: str, amount: int) -> Dict[str, Any]`

Buy stocks with automatic market type detection.

**Parameters:**
- `symbol` (str): Stock symbol (e.g., "AAPL", "600519.SH")
- `amount` (int): Number of shares to buy (must be multiple of 100 for Chinese A-shares)

**Returns:**
```python
{
    "AAPL": 10,           # Updated position
    "MSFT": 5,
    "CASH": 9737.60,      # Remaining cash
    # ... other positions
}
```

**Error Responses:**
```python
# Insufficient funds
{
    "error": "Insufficient cash! This action will not be allowed.",
    "required_cash": 262.40,
    "cash_available": 200.00,
    "symbol": "AAPL",
    "date": "2025-01-20"
}

# Invalid lot size for Chinese A-shares
{
    "error": "Chinese A-shares must be traded in multiples of 100 shares...",
    "symbol": "600519.SH",
    "amount": 150,
    "suggestion": "Please use 100 or 200 shares instead."
}

# T+1 restriction violation (Chinese A-shares)
{
    "error": "T+1 restriction violated! You bought 100 shares today...",
    "symbol": "600519.SH",
    "bought_today": 100,
    "sellable_today": 0
}
```

**Market Rules:**
- **US Stocks**: T+0 settlement, any integer amount
- **Chinese A-Shares**: T+1 settlement, 100-share lots, cannot sell same-day purchases
- **Market Detection**: Automatic based on symbol suffix (`.SH`/`.SZ` = A-shares)

---

#### `sell(symbol: str, amount: int) -> Dict[str, Any]`

Sell stocks with position validation.

**Parameters:**
- `symbol` (str): Stock symbol to sell
- `amount` (int): Number of shares to sell

**Returns:**
Same format as `buy()` with updated positions.

**Error Responses:**
```python
# No position
{
    "error": "No position for AAPL! This action will not be allowed.",
    "symbol": "AAPL",
    "date": "2025-01-20"
}

# Insufficient shares
{
    "error": "Insufficient shares! This action will not be allowed.",
    "have": 5,
    "want_to_sell": 10,
    "symbol": "AAPL"
}
```

---

### Cryptocurrency Trading

#### `buy_crypto(symbol: str, amount: float) -> Dict[str, Any]`

Buy cryptocurrencies with support for decimal amounts.

**Parameters:**
- `symbol` (str): Crypto symbol (e.g., "BTC-USDT", "ETH-USDT")
- `amount` (float): Amount to buy (supports 4 decimal places)

**Supported Cryptocurrencies:**
- BTC-USDT (Bitcoin)
- ETH-USDT (Ethereum)
- XRP-USDT, SOL-USDT, ADA-USDT, SUI-USDT, LINK-USDT, AVAX-USDT, LTC-USDT, DOT-USDT

**Returns:**
```python
{
    "BTC-USDT": 0.05,
    "ETH-USDT": 1.2,
    "CASH": 47500.0000,
    # ... other positions
}
```

---

#### `sell_crypto(symbol: str, amount: float) -> Dict[str, Any]`

Sell cryptocurrencies with 4-decimal precision.

**Parameters:**
- `symbol` (str): Crypto symbol to sell
- `amount` (float): Amount to sell (supports 4 decimal places)

**Returns:**
Same format as `buy_crypto()` with updated positions.

---

## Price Tools

### `get_price_local(symbols: List[str], date: Optional[str] = None) -> Dict[str, Any]`

Query historical prices for stocks and cryptocurrencies.

**Parameters:**
- `symbols` (List[str]): List of symbols to query
- `date` (Optional[str]): Target date (defaults to current trading date)

**Returns:**
```python
{
    "AAPL": {
        "date": "2025-01-20",
        "open": 255.88,
        "high": 264.37,
        "low": 255.63,
        "close": 262.24,
        "volume": 90483029
    },
    # ... other symbols
}
```

**Market Auto-Detection:**
- Symbols ending in `.SH`/`.SZ` → Chinese A-shares
- Symbols containing `-USDT` → Cryptocurrencies
- All others → US stocks

---

## Search Tools

### `get_information(query: str) -> str`

Search and retrieve market information from the web.

**Parameters:**
- `query` (str): Search query (e.g., "AAPL news today", "Bitcoin price analysis")

**Returns:**
```text
URL: https://example.com/article
Title: AAPL Stock Surges to New Highs
Description: Apple Inc. reached record levels today...
Publish Time: 2025-01-20 14:30:00
Content: Apple Inc. shares climbed to new heights...
```

**Features:**
- Jina AI-powered search and scraping
- Automatic date filtering (respects `TODAY_DATE`)
- Future information prevention for historical replay
- Returns top 3 relevant results

---

## Math Tools

### `calculate(expression: str) -> float`

Evaluate mathematical expressions.

**Parameters:**
- `expression` (str): Mathematical expression (e.g., "100 * 1.05 + 50")

**Returns:**
```python
155.0
```

**Supported Operations:**
- Basic arithmetic: `+`, `-`, `*`, `/`, `**`
- Parentheses: `( )`
- Functions: `sqrt()`, `abs()`, `min()`, `max()`

---

## Error Handling

All tools implement comprehensive error handling:

### File I/O Errors
```python
{
    "error": "Failed to write transaction to file: [Errno 28] No space left on device",
    "symbol": "AAPL",
    "date": "2025-01-20",
    "positions": {...},
    "note": "Position updated in memory but not persisted to disk"
}
```

### Lock Acquisiton Errors
- Cross-platform file locking (portalocker)
- Automatic retry on lock conflicts
- Timeout after 30 seconds

### Network Errors
- Automatic retry with exponential backoff
- Timeout after 10 seconds per request
- Detailed error messages for debugging

---

## Rate Limiting

**Current Status:** No rate limiting enforced

**Recommendation:** Implement rate limiting for production:
```python
# Example: Max 10 trades per minute per API key
@require_mcp_auth
@rate_limit(max_calls=10, period=60)
def buy(symbol: str, amount: int):
    ...
```

---

## Endpoint Configuration

All MCP endpoints run as HTTP services:

| Service | Default Port | Transport |
|---------|--------------|-----------|
| Math | 8000 | streamable-http |
| Search | 8001 | streamable-http |
| Trade (Stocks) | 8002 | streamable-http |
| Price | 8003 | streamable-http |
| Trade (Crypto) | 8005 | streamable-http |

**Environment Variables:**
```bash
MATH_HTTP_PORT=8000
SEARCH_HTTP_PORT=8001
TRADE_HTTP_PORT=8002
GETPRICE_HTTP_PORT=8003
CRYPTO_HTTP_PORT=8005
```

---

## Integration Examples

### Python (MCP Client)

```python
from langchain_mcp_adapters import MCPClient

# Connect to trading endpoint
client = MCPClient("http://localhost:8002/mcp")

# Buy stock
result = client.call_tool("buy", {
    "symbol": "AAPL",
    "amount": 10
})
print(result)

# Sell stock
result = client.call_tool("sell", {
    "symbol": "AAPL",
    "amount": 5
})
```

### cURL (Direct HTTP)

```bash
# Buy stock
curl -X POST http://localhost:8002/mcp/tools/buy \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "amount": 10
  }'
```

---

## Version History

### v1.1.0 (Current)
- ✅ Added MCP API authentication
- ✅ Cross-platform file locking (Windows/Unix)
- ✅ Enhanced error handling
- ✅ Security improvements (timing attack prevention)
- ✅ Dependency version pinning

### v1.0.0
- Initial release
- Basic trading operations
- US stocks, A-shares, and crypto support

---

## Support

For API issues or questions:
- GitHub Issues: [https://github.com/HKUDS/AI-Trader/issues](https://github.com/HKUDS/AI-Trader/issues)
- Documentation: [https://github.com/HKUDS/AI-Trader](https://github.com/HKUDS/AI-Trader)
