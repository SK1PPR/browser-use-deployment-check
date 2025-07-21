from langchain_openai import ChatOpenAI
from browser import Agent
from dotenv import load_dotenv
load_dotenv()

import asyncio

llm = ChatOpenAI(model="gpt-4.1")

async def main():
    agent = Agent(
        task="Compare the price of gpt-4o and DeepSeek-V3",
        llm=llm,
    )
    result = await agent.run()
    print(result)

asyncio.run(main())