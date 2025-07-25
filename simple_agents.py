import os
import openai
import asyncio
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class Agent:
    def __init__(self, name, instructions, model="gpt-4o-mini", output_type=str):
        self.name = name
        self.instructions = instructions
        self.model = model
        self.output_type = output_type

    async def run(self, prompt: str) -> str:
        messages = [
            {"role": "system", "content": self.instructions},
            {"role": "user", "content": prompt}
        ]
        response = await openai.ChatCompletion.acreate(
            model=self.model,
            messages=messages,
            temperature=0.7,
        )
        content = response.choices[0].message.content
        if self.output_type == str:
            return content
        try:
            return self.output_type.model_validate_json(content)
        except Exception as e:
            print("Failed to parse structured output, returning raw text.")
            return content

class Runner:
    @staticmethod
    async def run(agent: Agent, prompt: str):
        return await agent.run(prompt)
