from pydantic_ai import Agent

agent = Agent('anthropic:claude-3-5-sonnet-latest')

async def main():
    result = await agent.run("hello!")
    while True:
        print(f"\n{result.data}")
        user_input = input("\n> ")
        result = await agent.run(user_input, 
                                 message_history=result.new_messages(),
                                 )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
    