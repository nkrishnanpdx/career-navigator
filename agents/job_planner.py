import os
import json
from pydantic import BaseModel, Field, ValidationError
from simple_agents import Agent, Runner  # your minimal classes

class JobSearchItem(BaseModel):
    reason: str = Field(description="Why this job title or search term is useful")
    query: str = Field(description="The job title + location to search")

class JobSearchPlan(BaseModel):
    searches: list[JobSearchItem] = Field(description="List of job search terms")

INSTRUCTIONS = """
You are a career coach planning job searches. Given a user profile with preferred roles, locations,
and industries, generate 3 effective search queries for job boards like LinkedIn or Indeed. 
Include reasoning for each search term.

Output the results as a JSON array like this:

{
  \"searches\": [
    {\"reason\": \"Reason 1\", \"query\": \"job title 1, location\"},
    {\"reason\": \"Reason 2\", \"query\": \"job title 2, location\"},
    {\"reason\": \"Reason 3\", \"query\": \"job title 3, location\"}
  ]
}

Make sure the output is valid JSON.
"""

planner_agent = Agent(
    name="JobPlanner",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
)

async def plan_jobs(profile_summary: str) -> JobSearchPlan:
    response = await Runner.run(planner_agent, f"Profile: {profile_summary}")
    # The response is a string with JSON inside — parse it:
    try:
        data = json.loads(response)
        plan = JobSearchPlan(**data)
        return plan
    except (json.JSONDecodeError, ValidationError) as e:
        print("Failed to parse job search plan:", e)
        # Optionally return empty or partial result, or raise
        return JobSearchPlan(searches=[])
