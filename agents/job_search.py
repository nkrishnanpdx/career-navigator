from simple_agents import Agent, Runner
from pydantic import BaseModel, Field

class JobInfo(BaseModel):
    title: str = Field(description="Job title")
    location: str = Field(description="Job location")
    link: str = Field(description="Link to job posting")

class JobSearchResults(BaseModel):
    results: list[JobInfo] = Field(description="Search results for a job query")

INSTRUCTIONS = """
You are a job search agent. Given a job title and location, return 3 realistic-looking job listings.
Use fictional links, and make sure they look like real jobs from LinkedIn or Indeed.
"""

search_agent = Agent(
    name="JobSearch",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=JobSearchResults
)

async def search_job(query: str):
    return await Runner.run(search_agent, f"Query: {query}")
