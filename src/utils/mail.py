
from typing import List

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType, NameEmail
from pydantic import BaseModel

class EmailSchema(BaseModel):
    email: List[NameEmail]


conf = ConnectionConfig(
    MAIL_USERNAME="psudha6654@gmail.com",
    MAIL_PASSWORD="smwu pdyb koht eoev".replace(" ", ""),
    MAIL_FROM="psudha6654@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
) 

async def send_email(emails: List[str]):
    message = MessageSchema(
        subject="Registration Successful",
        recipients=emails,
        body="<p>Thanks for registering! hi our team will contact you soon.</p>",
        subtype=MessageType.html,
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})