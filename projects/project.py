import os
import asyncio
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
from pydantic import SecretStr
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext

os.environ['GEMINI_API_KEY'] = "AIzaSyCaqbDUJU6deuotYA-7a3A5FwcF4N9YG44"

browser = Browser(
    config=BrowserConfig(
        # chrome_instance_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        chrome_instance_path="D:\\chrome-win64\\chrome.exe"
    )
)

# Initialize the model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    api_key = SecretStr(os.getenv("GEMINI_API_KEY"))
)

# Create agent with the model
agent = Agent(
    # task="Navigate to 'https://en.wikipedia.org/wiki/Internet' and scroll to the string 'The vast majority of computer'",
    task="Naviate to 'https://www.youtube.com/watch?v=Y5HIAjwIzzs&list=RDY5HIAjwIzzs&start_radio=1&ab_channel=Gi%E1%BB%8Ft%C3%A1o%C4%91%E1%BB%8F' to scroll and get all comments",
    llm=llm,
    browser=browser
)

async def main():
    comments = await agent.run()
    print(comments)
    await browser.close()

    
    # Save comments to CSV file
    df = pd.DataFrame(comments)
    df.to_csv('comments.csv', encoding='utf-8', index=False)

    input('Press Enter to close...')


if __name__ == "__main__":
    asyncio.run(main())

