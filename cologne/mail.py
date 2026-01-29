from fastapi_mail import FastMail,ConnectionConfig,MessageSchema,MessageType
from pydantic import BaseModel,EmailStr
from typing import List
from cologne.config_env import mail_username,mail_password,mail_port,mail_server,mail_from,mail_from_name
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import status
from cologne.schemas import User
from sqlmodel import select
from cologne.models import CustomersDB
from sqlmodel.ext.asyncio.session import AsyncSession
class Email(BaseModel):
    email:List[EmailStr]

config = ConnectionConfig(
    MAIL_USERNAME=mail_username,
    MAIL_PASSWORD=mail_password,
    MAIL_PORT=mail_port, #starttls port
    MAIL_SERVER=mail_server,
    MAIL_FROM=mail_from,
    MAIL_STARTTLS=True, #Connection via starttls protocol
    MAIL_SSL_TLS=False,
    MAIL_FROM_NAME=mail_from_name
)
mail_setup = FastMail(config=config)


def creating_email(email:Email,subject:str,body:str)->JSONResponse:
    message = MessageSchema(
        subject=subject,
        recipients=email.__dict__.get("email"),
        body=body,
        subtype=MessageType.html
    )
    return message
    
    
async def welcome_email(email:Email,user:User,session:AsyncSession):
    token = user.token
    link = f"http://127.0.0.1:8000/validate_email/{token}"
    html = f"""<h1>Welcome to the Cologne Store Website</h1>
    <p>Click on the link to verify your account: <a href="{link}">link</a></p>"""
    message = MessageSchema(
        subject="Cologne Store website",
        body=html,
        recipients=email,
        subtype=MessageType.html 
    )
    await mail_setup.send_message(message)
    return JSONResponse(
        content={
            "message":"Email sent succesfully!"
        }
    )




