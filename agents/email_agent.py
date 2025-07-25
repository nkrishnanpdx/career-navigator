# email_agent.py
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")
TO_EMAIL = os.getenv("TO_EMAIL")

async def send_application_email(subject: str, message: str) -> bool:
    if not SENDGRID_API_KEY or not FROM_EMAIL or not TO_EMAIL:
        print("SendGrid API key or emails not configured.")
        return False

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        mail = Mail(
            from_email=FROM_EMAIL,
            to_emails=TO_EMAIL,
            subject=subject,
            html_content=message,
        )
        response = sg.send(mail)
        print(f"Email sent with status code: {response.status_code}")
        return response.status_code in (200, 202)
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
