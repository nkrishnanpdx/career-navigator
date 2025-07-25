import json
from simple_agents import Agent, Runner

INSTRUCTIONS = """
You are a profile analyzer that extracts the key skills, industries, roles, and tone from a user's resume or LinkedIn profile text.
Output a JSON with the following fields: skills (list of strings), industries (list), roles (list), tone (string).
Make sure the JSON is valid.
"""

profile_agent = Agent(
    name="ProfileAnalyzer",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
)

async def analyze_profile(profile_text: str) -> dict:
    response = await Runner.run(profile_agent, profile_text)
    try:
        data = json.loads(response)
        return data
    except json.JSONDecodeError:
        print("Failed to parse profile analysis JSON")
        return {}
