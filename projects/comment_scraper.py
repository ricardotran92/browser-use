"""
Chương trình này sử dụng AI để lấy các bình luận từ các bài viết trên mạng xã hội.
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
import time

# API keys
# load_dotenv() # load biến môi trường từ file .env
os.environ['GOOGLE_API_KEY_1'] = "AIzaSyDXSbFjir7LIPEQgWCI-wWC-cVFrPR08b0"
os.environ['GOOGLE_API_KEY_2'] = "AIzaSyAIN3n8oLvnJQLA7Wrix8xgmR6K2aQyywc"
os.environ['GOOGLE_API_KEY_3'] = "AIzaSyAz8q7IjtRfAXZaaiT7fom34-n-zF60Vsc"
os.environ['GOOGLE_API_KEY_4'] = "AIzaSyA8p3jiEtXWInt-FbjBcQwPG02cGZYHb2s"
os.environ['GOOGLE_API_KEY_5'] = "AIzaSyAXgfR7KfcE4qEgGcpKG8V2FXZJ1_5NsjU"

API_KEYS = [
	os.environ.get('GOOGLE_API_KEY_1'),
	os.environ.get('GOOGLE_API_KEY_2'),
	os.environ.get('GOOGLE_API_KEY_3'),
	os.environ.get('GOOGLE_API_KEY_4'),
	os.environ.get('GOOGLE_API_KEY_5')
]

current_key_index = 1

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
async def main(task, i, api_key):
	model = ChatGoogleGenerativeAI(model='gemini-2.0-flash', api_key=api_key)
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
	df.to_csv(f'output_{i}.csv', index=False)
	await browser.close()



# Chạy chương trình
if __name__ == '__main__':
	link = pd.read_csv('links.csv', encoding='utf-8', header=None).squeeze().tolist() # output: dataframe -> numpy.ndarray -> lists
	stop_index = 2 # default: len(link)
	for i in range(0, stop_index): 
		api_key = API_KEYS[current_key_index]
		task = f'Go to {link[i]} to get available comments (limit scrolls: 2)' # task: yêu cầu AI thực hiện
		asyncio.run(main(task, i, api_key))
		if i != len(link) - 1:
			current_key_index = (current_key_index + 1) % len(API_KEYS)
			print(f'Change to API key No.: {current_key_index + 1}')
			sleep_time = 30
			print(f'Sleeping for {sleep_time} seconds...')
			time.sleep(sleep_time)

