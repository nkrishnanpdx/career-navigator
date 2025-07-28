import os
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To
import asyncio
from concurrent.futures import ThreadPoolExecutor
import certifi


os.environ['SSL_CERT_FILE'] = certifi.where()

executor = ThreadPoolExecutor()

async def send_application_email(subject: str, html_body: str) -> dict:
    sg_api_key = os.getenv("SENDGRID_API_KEY")
    if not sg_api_key:
        return {"status": "fail", "reason": "SENDGRID_API_KEY not set in environment"}

    from_email = Email("FROM_EMAIL") # Change this to your email
    to_email = To("TO_EMAIL") # Change this to the email you want to send the email to

    mail = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=html_body
    )

    sg = sendgrid.SendGridAPIClient(api_key=sg_api_key)
    # Disable SSL verification for debugging, NOT FOR PRODUCTION
    sg.client._session.verify = False

    def send_mail_sync():
        return sg.client.mail.send.post(request_body=mail.get())

    try:
        response = await asyncio.get_event_loop().run_in_executor(executor, send_mail_sync)
        print(f"Email sent! Status code: {response.status_code}")
        return {"status": "success", "code": response.status_code}
    except Exception as e:
        print(f"Error sending email: {e}")
        return {"status": "fail", "reason": str(e)}
