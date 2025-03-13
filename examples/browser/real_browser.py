import os
import sys
from pathlib import Path

from browser_use.agent.views import ActionResult

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio

# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from browser_use import Agent, Controller
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext

browser = Browser(
	config=BrowserConfig(
		# NOTE: you need to close your chrome browser - so that this can open your browser in debug mode
		# chrome_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
		chrome_instance_path="D:\\chrome-win64\\chrome.exe",
	)
)


async def main():
	agent = Agent(
		task='In docs.google.com write my Papa a quick letter',
		# llm=ChatOpenAI(model='gpt-4o'),
		llm=ChatGoogleGenerativeAI(model='gemini-2.0-flash'),
		browser=browser,
	)

	await agent.run()
	await browser.close()

	input('Press Enter to close...')


if __name__ == '__main__':
	asyncio.run(main())
