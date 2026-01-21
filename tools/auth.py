"""
Authentication and authorization utilities for MCP endpoints.

Provides API key validation to protect trading operations from unauthorized access.
"""

import hmac
import os
from typing import Optional
from functools import wraps
from dotenv import load_dotenv

load_dotenv()


def validate_mcp_api_key(api_key: Optional[str] = None) -> bool:
    """
    Validate MCP API key for endpoint access.

    Args:
        api_key: API key to validate. If None, checks MCP_API_KEY environment variable.

    Returns:
        True if API key is valid or not configured, False otherwise.

    Note:
        If MCP_API_KEY is not set in environment, authentication is disabled (for development).
        In production, always set MCP_API_KEY to enable authentication.
    """
    # Get expected API key from environment
    expected_key = os.getenv("MCP_API_KEY")

    # If no API key is configured, allow access (development mode)
    if not expected_key:
        return True

    # If API key is provided, validate it using constant-time comparison
    if api_key and hmac.compare_digest(api_key, expected_key):
        return True

    return False


def require_mcp_auth(func):
    """
    Decorator to require MCP authentication for tool functions.

    Usage:
        @require_mcp_auth
        def my_trading_function(param1, param2, api_key=None):
            ...

    The decorator will check the api_key parameter and raise PermissionError if invalid.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Extract api_key from kwargs
        api_key = kwargs.pop('api_key', None)

        if not validate_mcp_api_key(api_key):
            raise PermissionError(
                "Invalid or missing MCP API key. "
                "Please provide a valid api_key parameter or set MCP_API_KEY environment variable."
            )

        return func(*args, **kwargs)

    return wrapper


def get_mcp_auth_help() -> str:
    """
    Get help text for MCP authentication setup.

    Returns:
        Help text explaining how to configure MCP authentication.
    """
    return """
🔐 MCP Authentication Setup

To enable MCP endpoint authentication:

1. Generate a secure API key:
   python -c "import secrets; print(secrets.token_urlsafe(32))"

2. Add to your .env file:
   MCP_API_KEY=your-generated-key-here

3. Include api_key parameter in tool calls:
   buy(symbol="AAPL", amount=10, api_key="your-generated-key-here")

⚠️  Security Warning:
- Never commit .env file with real API keys to version control
- Use strong, randomly generated keys (32+ characters)
- Rotate keys regularly in production
- Keep .env file permissions restricted (chmod 600 on Unix)
"""


if __name__ == "__main__":
    # Test authentication
    print(get_mcp_auth_help())

    # Test validation
    test_key = os.getenv("MCP_API_KEY", "test-key")
    if validate_mcp_api_key(test_key):
        print("✅ API key validation passed")
    else:
        print("❌ API key validation failed")
