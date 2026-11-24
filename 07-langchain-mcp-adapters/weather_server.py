import logging

from mcp.server.fastmcp import FastMCP

# Ẩn ClosedResourceError vô hại khi client đóng session
logging.getLogger("mcp.server.streamable_http").setLevel(logging.CRITICAL)

mcp = FastMCP("Weather", port=8000, log_level="WARNING")


@mcp.tool()
async def get_weather(location: str) -> str:
    """Get weather for location."""
    return "It's always sunny in New York"


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
