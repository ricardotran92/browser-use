"""
Show how to use custom outputs.

@dev You need to add OPENAI_API_KEY to your environment variables.
"""

import os
import sys
from typing import List # khai báo danh sách trong Pydantic
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio # hỗ trợ chương trình bất đồng bộ (async/await)
from dotenv import load_dotenv # đọc biến môi trường từ file .env
# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel # kiểm tra và chuyển đổi dữ liệu
from browser_use import ActionResult, Agent, Controller # ActionResult: kết quả trả về từ controller. Agent: đại diện cho tác nhân AI, thực hiện nhiêm vụ. Controller: điều khiển và đảm bảo các kết quả từ AI có đúng định dạng mong muốn
import pandas as pd
from browser_use.browser.browser import Browser, BrowserConfig

load_dotenv() # load biến môi trường từ file .env

# Khởi tạo trình duyệt
browser = Browser(
	config=BrowserConfig(
		chrome_instance_path="D:\\chrome-win64\\chrome.exe" # đường dẫn đến trình duyệt Chrome
	)
)



# Định nghĩa cấu trúc dữ liệu. Post: bài viết trên Hacker News
class Post(BaseModel): # BaseModel: lớp cơ sở của Pydantic
	author: str
	comment: str


# Posts: danh sách các bài viết
class Posts(BaseModel):
	posts: List[Post]


# controller: điều khiển và đảm bảo các kết quả từ AI có đúng định dạng mong muốn.
controller = Controller(output_model=Posts) # output_model: AI model sẽ trả về kết quả đúng với định dạng Posts (danh sách các bài đăng). Nếu sai dịnh dạng, Pydantic sẽ báo lỗi.

# Hàm chính. Main() là hàm bất đồng bộ.
async def main():
	task = 'Go to "https://www.youtube.com/watch?v=Q12Kk0ihrZk&ab_channel=GiangH%E1%BB%93ngNg%E1%BB%8Dc" to get available comments (limit scroll down: 2 times)'
	# model = ChatOpenAI(model='gpt-4o')
	model = ChatGoogleGenerativeAI(model='gemini-2.0-flash')
	# Tạo Agent và chạy nhiệm vụ
	agent = Agent(task=task, llm=model, controller=controller, browser=browser) # task: yêu cầu AI thực hiện. llm: model AI sử dụng. Controller: điều khiển và đảm bảo kết quả đúng định dạng Posts.

	history = await agent.run() # agent.run() chạy AI để thực nhiệm vụ. history chứa toàn bộ lịch sử của quá trình AI thực hiện nhiệm vụ.
	# Kiểm tra kết quả
	result = history.final_result() # Lấy kết quả cuối cùng dưới dạng JSON.
	if result:
		parsed: Posts = Posts.model_validate_json(result) # chuyển JSON thành đối tượng Posts, giúp dễ thao tác. parsed là đối tượng thuộc lớp Posts.

		for post in parsed.posts:
			print('\n--------------------------------')
			print(f'Author:              {post.author}')
			print(f'Comment:             {post.comment}')
	else:
		print('No result')

	df = pd.DataFrame(parsed.model_dump()['posts']) # converting a model to a dictionary. Sub-models will be recursively converted to dictionaries.
	df.to_csv('custom_output.csv', index=False)
	await browser.close()
	input('Press Enter to close...')

# Chạy chương trình
if __name__ == '__main__':
	asyncio.run(main()) # Chạy main() trong môi trường async.

