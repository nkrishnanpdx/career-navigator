# tailor.py
import json
from simple_agents import Agent, Runner

INSTRUCTIONS = """
You are an expert career assistant. Given a base resume and a job description, create a tailored resume highlighting relevant skills and experiences, 
and write a concise cover letter for the job. Output JSON with fields: tailored_resume (string), cover_letter (string).
Make sure the JSON is valid.
"""

tailor_agent = Agent(
    name="TailorAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
)

async def tailor_application(resume_text: str, job_description: str) -> dict:
    prompt = f\"\"\"Base Resume:
{resume_text}

Job Description:
{job_description}

Please generate the tailored documents.\"\"\"
    response = await Runner.run(tailor_agent, prompt)
    try:
        data = json.loads(response)
        return data
    except json.JSONDecodeError:
        print("Failed to parse tailoring JSON")
        return {}
