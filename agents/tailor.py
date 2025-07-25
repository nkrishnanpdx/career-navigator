import json
import re
from simple_agents import Agent, Runner

INSTRUCTIONS = """
You are an expert career assistant. Given a base resume and a job description, create a tailored resume highlighting relevant skills and experiences, 
and write a concise cover letter for the job. Output JSON with fields: tailored_resume (string), cover_letter (string).
Make sure the JSON is valid and properly escaped.
"""

tailor_agent = Agent(
    name="TailorAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
)

def extract_json_from_markdown(response: str) -> dict:
    """
    Extract a JSON object from a markdown-formatted string, e.g.:
    ```json
    { ... }
    ```
    """
    match = re.search(r"```json\s*(\{.*?\})\s*```", response, re.DOTALL)
    if match:
        json_str = match.group(1)
    else:
        # fallback: try to parse raw string as JSON if no backticks
        json_str = response.strip()

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print("❌ Failed to parse JSON:", e)
        return {}

async def tailor_application(resume_text: str, job_description: str) -> dict:
    prompt = f"""Base Resume:
{resume_text}

Job Description:
{job_description}

Please generate the tailored documents as valid JSON."""
    
    response = await Runner.run(tailor_agent, prompt)
    print("📩 Tailor agent raw response:\n", repr(response))
    return extract_json_from_markdown(response)
