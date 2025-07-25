from agents import Agent, Runner

INSTRUCTIONS = """
You are a job search assistant. Given a job search query like 'AI Security Engineer in Seattle',
return the job description and company info as text.
"""

search_agent = Agent(
    name="JobSearchAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini"
)

async def search_job(query: str, reason: str):
    input_text = f"Search: {query}\nWhy: {reason}"
    result = await Runner.run(search_agent, input_text)
    return result.final_output
