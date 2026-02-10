from fastapi_mail import FastMail,ConnectionConfig,MessageSchema,MessageType
from pydantic import BaseModel,EmailStr
from typing import List
from cologne.config_env import mail_username,mail_password,mail_port,mail_server,mail_from,mail_from_name,base_url
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import status
from cologne.schemas import User
from sqlmodel import select
from cologne.models import CustomersDB
from sqlmodel.ext.asyncio.session import AsyncSession

class Email(BaseModel):
    email:List[EmailStr]
class PasswordReset(BaseModel):
    new_password:str
    confirm_new_password:str
    
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
        recipients=email,
        body=body,
        subtype=MessageType.html
    )
    return message
    
    


#Garantir que o usuario so possa acessar as rotas se seu email for verificado, injecao de dependencia.
#Fazer meu email ser verificado manualmente



