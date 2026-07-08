from fastapi_mail import FastMail,ConnectionConfig,MessageSchema,MessageType
from pydantic import BaseModel,EmailStr
from typing import List
from src.config.config_env import mail_username,mail_password,mail_port,mail_server,mail_from,mail_from_name,base_url


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

class FastMailProvider():
    def __init__(self):
        self.mail_setup = FastMail(config=config)
    async def create_email(self, email:EmailStr, subject: str, html: str) -> None:
        message = MessageSchema(
            subject=subject,
            recipients=[email], 
            body=html,
            subtype=MessageType.html
        )
        await self.mail_setup.send_message(message)

#Garantir que o usuario so possa acessar as rotas se seu email for verificado, injecao de dependencia.
#Fazer meu email ser verificado manualmente



