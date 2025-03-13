import asyncio

from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from browser_use import Agent

load_dotenv()

# Initialize the model
# llm = ChatOpenAI(
# 	model='gpt-4o',
# 	temperature=0.0,
# )
llm =  ChatGoogleGenerativeAI(
	model='gemini-2.0-flash',
	temperature=0.0,
)
task = 'Find the founders of browser-use and draft them a short personalized message'

agent = Agent(task=task, llm=llm)


async def main():
	await agent.run()


if __name__ == '__main__':
	asyncio.run(main())
