from agents import Agent, Runner

INSTRUCTIONS = """
You are a resume and cover letter writer. Given a user resume summary and a job description,
generate a tailored resume (as text) and a concise, compelling cover letter (as text).
Keep formatting markdown-compatible.
"""

tailor_agent = Agent(
    name="ApplicationTailor",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini"
)

async def tailor_application(profile: str, job_description: str):
    input_text = f"Candidate Profile:\n{profile}\n\nJob Description:\n{job_description}"
    result = await Runner.run(tailor_agent, input_text)
    return result.final_output
