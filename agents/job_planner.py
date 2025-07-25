import json
import re
from simple_agents import Agent, Runner
from pydantic import BaseModel, Field

class JobSearchItem(BaseModel):
    reason: str = Field(description="Why this job title or search term is useful")
    query: str = Field(description="The job title + location to search")

class JobSearchPlan(BaseModel):
    searches: list[JobSearchItem] = Field(description="List of job search terms")

INSTRUCTIONS = """
You are a career coach planning job searches. Given a user profile with preferred roles, locations,
and industries, generate 3 effective search queries for job boards like LinkedIn or Indeed. 
Include reasoning for each search term.

Return the output as a valid JSON object with this format:
{
  "searches": [
    {
      "reason": "...",
      "query": "..."
    },
    ...
  ]
}
"""

planner_agent = Agent(
    name="JobPlanner",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
)

def clean_json_response(response: str) -> str:
    # Remove markdown code fences and language tags if present
    cleaned = re.sub(r"^```(?:json)?\n", "", response)
    cleaned = re.sub(r"\n```$", "", cleaned)
    return cleaned.strip()

async def plan_jobs(profile_summary: str):
    raw_response = await Runner.run(planner_agent, f"Profile: {profile_summary}")
    print("Raw response from planner_agent:")
    print(raw_response)

    cleaned_response = clean_json_response(raw_response)

    try:
        data = json.loads(cleaned_response)
    except json.JSONDecodeError as e:
        print(f"Failed to parse job search plan: {e}")
        data = {"searches": []}

    return data
