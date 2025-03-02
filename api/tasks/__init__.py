from api.celery import celery_app
from utils.utils import EmailSchema, send_mail


@celery_app.task
def send_verification_code(email: str, code: str, username: str):
    print(f"Sending verification code {code} to {email}")
    subject = "Verification Code"
    body = f"Hello {username}, your verification code is {code}"
    mail_data: dict = {
        "email": email,
        "subject": subject,
        "message": body,
        "username": username,
    }
    mail_payload = EmailSchema(**mail_data)
    send_mail(mail_payload)
