import asyncio
import os
from tools.pdf_utils import extract_text_from_pdf
from agents.job_planner import plan_jobs
from agents.deep_search_agent import RealJobSearchAgent 
from agents.tailor import tailor_application
from agents.email_agent import send_application_email
from agents.tracker import log_application
from tools.db import create_tables, insert_application
# Orchestrate the agents
async def main():
    # Initialize the database tables
    create_tables()

    # Step 1: Load resume and extract profile text
    # Assuming sample_resume.pdf is in the same directory as main.py
    #Change path and also name of pdf here
    profile_path = os.path.join(os.path.dirname(__file__), "sample_resume.pdf")
    if not os.path.exists(profile_path):
        print(f"Error: sample_resume.pdf not found at {profile_path}")
        print("Please ensure 'sample_resume.pdf' is in the same directory as 'main.py' for testing.")
        return

    try:
        profile_text = extract_text_from_pdf(profile_path)
        print("✅ Resume text extracted successfully.")
    except Exception as e:
        print(f"❌ Error extracting text from PDF: {e}")
        return

    # Step 2: Plan job search terms
    print("⏳ Planning job search terms...")
    job_plan = await plan_jobs(profile_text)
    if not job_plan or not job_plan.get("searches"):
        print("⚠️ No job search plans generated. Exiting.")
        return
    print(f"✅ Job search plan generated: {len(job_plan['searches'])} queries.")

    # Initialize the real job search agent
    real_job_searcher = RealJobSearchAgent()

    # Step 3: Perform real job searches and process applications
    for i, item in enumerate(job_plan["searches"]):
        query = item["query"]
        reason = item["reason"]
        print(f"\n--- Processing Search Query {i+1}/{len(job_plan['searches'])}: '{query}' ---")
        print(f"Reason: {reason}")

        try:
            # Use the real job search agent
            job_results = await real_job_searcher.search(query)
            if not job_results:
                print(f"⚠️ No real job results found for query: '{query}'. Skipping tailoring and emailing.")
                continue
            print(f"✅ Found {len(job_results)} real job postings for '{query}'.")

            # Process the first few results (or all, depending on desired behavior)
            for j, job_info in enumerate(job_results[:3]): # Process up to 3 jobs per query for demonstration
                job_title = job_info.get("title", "N/A")
                company_name = job_info.get("company", "N/A")
                job_url = job_info.get("url", "N/A")
                job_location = job_info.get("location", "N/A") # Assuming location is available

                print(f"\n--- Processing Job Listing {j+1}: {job_title} at {company_name} ({job_location}) ---")
                print(f"Job URL: {job_url}")

                # For tailoring, we need the full job description.
                # In a real scenario, you would fetch the job description from job_url.
                # For this example, we will use a placeholder or a simplified description.
                # If deep_search_agent could return snippets, we'd use that.
                # For now, let's create a mock job description for tailoring.
                mock_job_description = f"Job Title: {job_title}\nCompany: {company_name}\nLocation: {job_location}\n\nThis is a placeholder job description for a {job_title} role. Key responsibilities include [responsibilities] and required skills include [skills]."
                print("⏳ Tailoring application...")
                tailored_output = await tailor_application(profile_text, mock_job_description)

                if not tailored_output:
                    print("⚠️ Skipping due to tailoring failure for this job listing.")
                    continue

                tailored_resume = tailored_output.get('tailored_resume', 'N/A')
                cover_letter = tailored_output.get('cover_letter', 'N/A')

                print("✅ Application tailored.")

                # Format HTML email body
                html_body = f"""
                <html>
                <head>
                    <style>
                        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                        h2 {{ color: #0056b3; border-bottom: 1px solid #eee; padding-bottom: 5px; }}
                        pre {{ background-color: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; white-space: pre-wrap; word-wrap: break-word; }}
                        p {{ margin-bottom: 10px; }}
                        .job-details {{ background-color: #e6f2ff; padding: 10px; border-left: 5px solid #007bff; margin-bottom: 20px; }}
                    </style>
                </head>
                <body>
                    <div class="job-details">
                        <p><strong>Applying for:</strong> {job_title} at {company_name}</p>
                        <p><strong>Location:</strong> {job_location}</p>
                        <p><strong>Job Link:</strong> <a href="{job_url}">{job_url}</a></p>
                    </div>

                    <h2>Cover Letter</h2>
                    <p>{cover_letter.replace('\n', '<br>')}</p>

                    <h2>Tailored Resume</h2>
                    <pre>{tailored_resume}</pre>
                </body>
                </html>
                """

                # Step 5: Email application
                email_subject = f"Application for {job_title} at {company_name}"
                print(f"⏳ Sending email for {job_title}...")
                email_status = await send_application_email(
                    subject=email_subject,
                    html_body=html_body
                )
                if email_status.get("status") == "success":
                    print(f"✅ Email sent successfully for {job_title} (Status Code: {email_status.get('code')}).")
                else:
                    print(f"❌ Error sending email for {job_title}: {email_status.get('reason')}")

                # Step 6: Track application using the unified db.py
                print("⏳ Logging application...")
                try:
                    insert_application(
                        company=company_name,
                        title=job_title,
                        date_applied=datetime.now().isoformat(),
                        status="Applied",
                        notes=f"Auto-applied by Intelligent Career Navigator via query: '{query}'"
                    )
                    print("✅ Application logged successfully.")
                except Exception as e:
                    print(f"❌ Error logging application: {e}")

        except Exception as e:
            print(f"❌ An error occurred during processing query '{query}': {e}")
            continue

    print("\n--- All job application processes completed! ---")

if __name__ == "__main__":
    from datetime import datetime # Import datetime here for log_application
    asyncio.run(main())
