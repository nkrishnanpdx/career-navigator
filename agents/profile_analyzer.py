from agents import Agent, Runner, trace
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
"""

planner_agent = Agent(
    name="JobPlanner",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=JobSearchPlan
)

async def plan_jobs(profile_summary: str):
    result = await Runner.run(planner_agent, f"Profile: {profile_summary}")
    return result.final_output
