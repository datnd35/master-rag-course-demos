from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b


@mcp.tool()
def divide(a: int, b: int) -> float:
    """Divide a by b (fails when b == 0)"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


@mcp.prompt()
def math_helper(problem: str) -> str:
    """Prompt giải toán"""
    return f"Solve step by step using the math tools: {problem}"


@mcp.resource("config://math")
def math_config() -> str:
    """Math server config"""
    return "precision=2"


if __name__ == "__main__":
    mcp.run(transport="stdio")
