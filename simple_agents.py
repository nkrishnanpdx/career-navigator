from openai import AsyncOpenAI

class Agent:
    def __init__(self, name, instructions, model="gpt-4o"):
        self.name = name
        self.instructions = instructions
        self.model = model
        self.client = AsyncOpenAI()  # Use env var OPENAI_API_KEY

    async def run(self, prompt):
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()


class Runner:
    @staticmethod
    async def run(agent: Agent, prompt: str) -> str:
        return await agent.run(prompt)
