import os

from dotenv import load_dotenv
from fastapi import BackgroundTasks
from fastapi_mail import (FastMail,
                          MessageSchema,
                          ConnectionConfig)


load_dotenv()


conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv('EMAIL_USER'),
    MAIL_PASSWORD=os.getenv('EMAIL_PASSWORD'),
    MAIL_FROM=os.getenv('EMAIL_FROM'),
    MAIL_PORT=os.getenv('EMAIL_PORT'),
    MAIL_SERVER=os.getenv('EMAIL_HOST'),
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True
)


def send_email(background_tasks: BackgroundTasks,
               subject: str,
               email: str,
               body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[email],
        body=body
    )
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)