from fastapi import APIRouter,status,Depends
from fastapi.responses import JSONResponse
from fastapi_mail import MessageSchema
from .schemas import User
from typing import List
from .database import get_session
from .mail import Email,creating_email,mail_setup,PasswordReset
from sqlmodel.ext.asyncio.session import AsyncSession
from .error_handling import UserNotFound,WrongPassword,EmailTokenExpired,DifferentPassword
from sqlmodel import select
from .models import CustomersDB
from .utils import get_hash
from datetime import datetime,timezone
import uuid
from datetime import timedelta
from .db_crud import STANDARD_TOKEN_EXPIRATION_TIME
from .config_env import base_url
from .background_tasks import email_task_queue
mail_router = APIRouter()

#@mail_router.get("/validate_email{key}")
#async def show_validate_email_page(key:str):
   # return None #So acessa pagina com essa rota, depois que tiver o front nessa rota posso excluir essa rota da api e tera um botao com texto na pagina criada para acessar a rota post e fazer tudo aquilo
@mail_router.post("/validate_email/{key}",status_code=status.HTTP_200_OK)
async def validate_mail(key:str,session:AsyncSession = Depends(get_session)):
   command = select(CustomersDB).where(CustomersDB.token==key) 
   result = await session.exec(command)
   user:User = result.first()
   time_now = datetime.now(timezone.utc).replace(tzinfo=None)
   if user.expiry_token_time>time_now:
    user.is_verified = True
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return JSONResponse(
       content="User has been succesfully verified.",
       status_code=status.HTTP_201_CREATED
    )
   else:
     raise EmailTokenExpired() #Depois chamar o more_welcome_email no front para mandar o novo email.
@mail_router.post("/send_another_mail_verification",status_code=status.HTTP_202_ACCEPTED)
async def more_welcome_email(email:Email,session:AsyncSession = Depends(get_session)):
    token = uuid.uuid4()
    command = select(CustomersDB).where(email.email[0]==CustomersDB.email)
    result = await session.exec(command)
    user = result.first()
    user.token = token
    user.expiry_token_time = timedelta(minutes=STANDARD_TOKEN_EXPIRATION_TIME) + datetime.now(timezone.utc).replace(tzinfo=None)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    
    link = f"{base_url}/validate_email/{token}"
    html = f"""<h1>Welcome to the Cologne Store!</h1>
    <p>Click on the link to verify your account <a href ="{link}">VerifyAccount</a></p>"""
    email_task_queue.delay("Validate your email",[user.email],html)
    return JSONResponse(
      content={
        "message":"Email request sent succesfully to the redis broker."
      }
    )
    
    
    
    
    
    
    
@mail_router.post("/send_email")
async def sending_email(email:Email,body:str,subject:str,session:AsyncSession = Depends(get_session)):  
    command = select(CustomersDB.email).where(email==CustomersDB.email)
    result = await session.exec(command)
    user = result.first()
    if user is not None:
      message = creating_email(email=email,subject=subject,body=body)
      await mail_setup.send_message(message)
      return JSONResponse(
         content={
            "message":"Email sent succesfully."
        }
      )
    else:
      raise UserNotFound()

@mail_router.post("/send_password_reset_mail")
async def password_reset_mail(email:Email,session:AsyncSession = Depends(get_session)):
   reset_token = str(uuid.uuid4())
   expiry_reset_token = timedelta(minutes=STANDARD_TOKEN_EXPIRATION_TIME) + datetime.now(timezone.utc).replace(tzinfo=None)
   command = select(CustomersDB).where(CustomersDB.email==email.email[0])
   result = await session.exec(command)
   user = result.first()
   link = f"{base_url}/change_password/{reset_token}"
   if user is not None:
       user.reset_password_token = reset_token
       user.expiry_reset_token_time = expiry_reset_token
       session.add(user)
       await session.commit()
       await session.refresh(user)
       html = f"""<h1>Hello customer!</h1>
       <p>Click on the link to reset your password safely: <a href="{link}">ResetPassword</a></p>"""
       subject = f"Reset password email for {user.email}"
       email_task_queue.delay(subject,[user.email],html)
       return JSONResponse(
         content={
           "message":"Password reset email request send succesfully to the broker."
         }
       )
   else:
       raise UserNotFound()

#@mail_router.get("/change_password{key}")
#async def show_page(key:str):
 #   return None #So acessa pagina com essa rota, depois que tiver o front nessa rota posso excluir essa rota da api e tera um botao com texto na pagina criada para acessar a rota post e fazer tudo aquilo

@mail_router.post("/change_password/{key}",status_code=status.HTTP_200_OK)
async def change_password_route(key:str,password_info:PasswordReset,session:AsyncSession = Depends(get_session)):
    new_password = password_info.new_password
    confirm_new_password = password_info.confirm_new_password
    if new_password==confirm_new_password:
      command = select(CustomersDB).where(CustomersDB.reset_password_token==key)
      result = await session.exec(command)
      user:User = result.first()
      if user is not None:
         current_time = datetime.now(timezone.utc).replace(tzinfo=None)
         if current_time<user.expiry_reset_token_time:
           user.hash_password = password_info.new_password
           session.add(user)
           await session.commit()
           await session.refresh(user)
           return JSONResponse(
            content={
                "message":"Password has been succesfully reset."
            }
          )
         else:
             raise EmailTokenExpired() #chamar password resetmail novamente pelo front
      else:
        raise WrongPassword() 
    else:
      raise DifferentPassword()  
    
#Adicionar reset_token_expiry para adicionar tempo para o email de redefinicao de senha     

    
     
    


