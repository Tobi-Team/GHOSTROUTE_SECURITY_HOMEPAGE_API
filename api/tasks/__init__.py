from api.celery import celery_app
from utils.utils import EmailSchema, send_mail
import asyncio


@celery_app.task
def send_verification_code(email: str, code: str, username: str):
    print(f"Sending verification code {code} to {email}")
    subject = "Verification Code"
    body = f"{code}"
    mail_data: dict = {
        "email": email,
        "subject": subject,
        "message": body,
        "username": username,
    }
    mail_payload = EmailSchema(**mail_data)
    asyncio.run(send_mail(mail_payload))
