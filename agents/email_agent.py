from agents import Agent, Runner, function_tool
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
import os
from typing import Dict

@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """Send an email with the given subject and HTML body"""
    sg = SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))
    from_email = Email(os.getenv("FROM_EMAIL"))
    to_email = To(os.getenv("TO_EMAIL"))
    content = Content("text/html", html_body)
    mail = Mail(from_email, to_email, subject, content).get()
    sg.client.mail.send.post(request_body=mail)
    return {"status": "success"}

INSTRUCTIONS = """
You are a helpful assistant that formats job application content into a clean HTML email. 
Take the user's message (e.g., a cover letter or summary) and send it via email using your tool.
"""

email_agent = Agent(
    name="EmailAgent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini"
)

async def send_application_email(subject: str, message: str):
    result = await Runner.run(email_agent, message)
    return result.final_output
