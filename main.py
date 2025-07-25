# main.py
import asyncio
from tools.pdf_utils import extract_text_from_pdf
from agents.job_planner import plan_jobs
from agents.job_search import search_job  # You can implement real search later
from agents.tailor import tailor_application
from agents.email_agent import send_application_email
from agents.tracker import log_application

# Sample flow - orchestrate the agents
async def main():
    # Step 1: Load resume and extract profile text
    profile_path = "sample_resume.pdf"  # Replace with your file
    profile_text = extract_text_from_pdf(profile_path)

    # Step 2: Plan job search terms
    job_plan = await plan_jobs(profile_text)

    # Step 3: Perform job searches (mocked)
    for item in job_plan.searches:
        job_description = await search_job(item.query, item.reason)  # Replace with real scraping later

        # Step 4: Tailor application
        tailored_output = await tailor_application(profile_text, job_description)

        # Step 5: Email application (optional)
        await send_application_email(
            subject="Job Application - Tailored Submission",
            message=tailored_output  # Should include resume + cover letter
        )

        # Step 6: Track application
        log_application(
            company="[Mock Company]",  # You can extract from job_description
            title=item.query,
            notes="Auto-applied by Intelligent Career Navigator"
        )

    print("✅ Job applications processed!")

if __name__ == "__main__":
    asyncio.run(main())
