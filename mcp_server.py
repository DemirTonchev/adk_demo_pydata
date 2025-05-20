# server.py
from fastmcp import FastMCP
import asyncio

mcp = FastMCP("FastMCP Demo Server")


@mcp.tool()
def say_goodbye() -> str:
    """Provides a farewell message to conclude the conversation and shows customer current new products."""
    print("GOODBYE USED!!!!")
    return "Goodbye! Have a great day. Currently we have a special offer for you: credit card with 0% interest rate!"


if __name__ == "__main__":
    asyncio.run(mcp.run(transport='sse', host="0.0.0.0", port=8080))
    # asyncio.run(mcp.run(transport='streamable-http', host="0.0.0.0", port=8080))
