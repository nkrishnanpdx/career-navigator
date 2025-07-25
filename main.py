import asyncio
import os
from tools.pdf_utils import extract_text_from_pdf
from agents.job_planner import plan_jobs
from agents.job_search import search_job
from agents.tailor import tailor_application
from agents.email_agent import send_application_email
from agents.tracker import log_application

#orchestrate the agents
async def main():
    # Step 1: Load resume and extract profile text
    profile_path = os.path.join(os.path.dirname(__file__), "sample_resume.pdf")
    profile_text = extract_text_from_pdf(profile_path)

    # Step 2: Plan job search terms
    job_plan = await plan_jobs(profile_text)

    # Step 3: Perform job searches (mocked)
    for item in job_plan["searches"]:
        job_description = await search_job(item["query"])

        # Step 4: Tailor application
        tailored_output = await tailor_application(profile_text, job_description)

        if not tailored_output:
            print("⚠️ Skipping due to tailoring failure.")
            continue

        # Format HTML email body
        html_body = f"""
        <h2>Tailored Resume</h2>
        <pre>{tailored_output.get('tailored_resume', 'N/A')}</pre>

        <h2>Cover Letter</h2>
        <p>{tailored_output.get('cover_letter', 'N/A').replace('\n', '<br>')}</p>
        """

        # Step 5: Email application
        await send_application_email(
            subject=f"Job Application - {item['query']}",
            html_body=html_body
        )

        # Step 6: Track application
        log_application(
            company="[Mock Company]",  # You can extract from job_description
            title=item["query"],
            notes="Auto-applied by Intelligent Career Navigator"
        )

    print("Job applications processed!")

if __name__ == "__main__":
    asyncio.run(main())
