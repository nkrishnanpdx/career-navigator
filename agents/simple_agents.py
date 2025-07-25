# simple_agents.py
import os
import openai
from dotenv import load_dotenv
import asyncio

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class Agent:
    def __init__(self, name, instructions, model="gpt-4o-mini"):
        self.name = name
        self.instructions = instructions
        self.model = model

    async def run(self, prompt: str) -> str:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._sync_run, prompt)

    def _sync_run(self, prompt: str) -> str:
        messages = [
            {"role": "system", "content": self.instructions},
            {"role": "user", "content": prompt}
        ]
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
        )
        return response.choices[0].message.content

class Runner:
    @staticmethod
    async def run(agent: Agent, prompt: str) -> str:
        return await agent.run(prompt)
