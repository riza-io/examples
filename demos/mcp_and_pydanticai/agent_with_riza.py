from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerHTTP
import logfire
from os import getenv
logfire.configure(token=getenv('LOGFIRE_TOKEN'))

# Follow the steps here to get your Riza remote MCP server URL: https://docs.riza.io/getting-started/mcp-servers
riza_server = MCPServerHTTP(url="https://mcp.riza.io/code-interpreter?secret=YOUR_SECRET_HERE")

agent = Agent('anthropic:claude-3-5-sonnet-latest', mcp_servers=[riza_server], instrument=True)

async def main():
    async with agent.run_mcp_servers():
        result = await agent.run("hello!")
        while True:
            print(f"\n{result.data}")
            user_input = input("\n> ")
            result = await agent.run(user_input, message_history=result.new_messages())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())