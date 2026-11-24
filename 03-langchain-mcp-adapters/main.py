import asyncio
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

MATH_SERVER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "math_server.py")


async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": [MATH_SERVER],
                "transport": "stdio",
            },
        }
    )
    tools = await client.get_tools()
    agent = create_agent("openai:gpt-4.1", tools)
    response = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})
    print(response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
