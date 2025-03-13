import os
import asyncio
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
from pydantic import SecretStr
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext
from bs4 import BeautifulSoup

os.environ['GEMINI_API_KEY'] = "AIzaSyCaqbDUJU6deuotYA-7a3A5FwcF4N9YG44"

browser = Browser(
    config=BrowserConfig(
        chrome_instance_path="D:\\chrome-win64\\chrome.exe"
    )
)

# Initialize the model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    api_key=SecretStr(os.getenv("GEMINI_API_KEY"))
)

# Create agent with the model
agent = Agent(
    task="Navigate to 'https://www.youtube.com/watch?v=Y5HIAjwIzzs&list=RDY5HIAjwIzzs&start_radio=1&ab_channel=Gi%E1%BB%8Ft%C3%A1o%C4%91%E1%BB%8F' and extract all comments",
    llm=llm,
    browser=browser
)

async def scroll_page():
    for _ in range(10):  # Adjust the range for more scrolling
        await browser.scroll_down(500)
        await asyncio.sleep(2)  # Adjust the sleep time as needed


async def get_page_content(self):
        # Implement the method to get the current page content
        # This is a placeholder implementation, adjust it according to your browser automation library
        page_content = await self.browser.page_source()  # Example method to get page source
        return page_content

async def extract_comments():
    comments = []
    for _ in range(10):  # Adjust the range to match the scroll_page range
        page_content = await browser.get_page_content()
        soup = BeautifulSoup(page_content, 'html.parser')
        for comment in soup.find_all('span', class_='yt-core-attributed-string'):
            comments.append(comment.get_text())
        await asyncio.sleep(2)  # Adjust the sleep time as needed
    return comments



async def main():
    scroll_task = asyncio.create_task(scroll_page())
    comments_task = asyncio.create_task(extract_comments())

    await scroll_task
    comments = await comments_task

    print("Extracted comments:", comments)
    await browser.close()

    # Save comments to CSV file
    df = pd.DataFrame(comments, columns=['Comment'])
    df.to_csv('comments.csv', encoding='utf-8', index=False)

    input('Press Enter to close...')

if __name__ == "__main__":
    asyncio.run(main())