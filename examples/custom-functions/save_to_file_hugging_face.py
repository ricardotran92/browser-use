import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from typing import List, Optional

# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel

from browser_use.agent.service import Agent
from browser_use.controller.service import Controller

# Initialize controller first
controller = Controller()


class Model(BaseModel):
	title: str
	url: str
	likes: int
	license: str


class Models(BaseModel):
	models: List[Model]


@controller.action('Save models', param_model=Models)
def save_models(params: Models):
	with open('models.txt', 'a') as f:
		for model in params.models:
			f.write(f'{model.title} ({model.url}): {model.likes} likes, {model.license}\n')


# video: https://preview.screen.studio/share/EtOhIk0P
async def main():
	task = f'Look up models with a license of cc-by-sa-4.0 and sort by most likes on Hugging face, save top 5 to file.'

	# model = ChatOpenAI(model='gpt-4o')
	model = ChatGoogleGenerativeAI(model='gemini-2.0-flash')
	agent = Agent(task=task, llm=model, controller=controller)

	await agent.run()


if __name__ == '__main__':
	asyncio.run(main())
