# job_search.py
import asyncio

async def search_job(query: str, reason: str) -> str:
    """
    Mock job search that returns a dummy job description.
    Replace this with real scraping or API calls later.
    """
    await asyncio.sleep(0.5)  # Simulate network delay
    return f\"\"\"Job Title: {query}
Company: Acme Corp
Location: Remote
Description: We are looking for a talented professional for {query}.
Requirements: Relevant skills and experience in the field.
\"\"\"
