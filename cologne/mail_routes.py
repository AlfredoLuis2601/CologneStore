from fastapi import APIRouter,status,Depends
from fastapi.responses import JSONResponse
from .schemas import User
from .database import get_session
from .mail import Email,creating_email,mail_setup
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .models import CustomersDB
mail_router = APIRouter()


@mail_router.get("/validate_email/{key}",status_code=status.HTTP_201_CREATED)
async def validate_mail(key:str,session:AsyncSession = Depends(get_session)):
   command = select(CustomersDB).where(CustomersDB.token==key) 
   result = await session.exec(command)
   user:User = result.first()
   user.is_verified = True
   session.add(user)
   await session.commit()
   await session.refresh(user)
   return JSONResponse(
       content="User has been succesfully verified.",
       status_code=status.HTTP_201_CREATED
   )
   
@mail_router.post("/send_email")
async def sending_email(email:Email):
    html = "<h1>Welcome to the Cologne Store Website"   
    message = creating_email(email=email,subject="Cologne Store Website",body=html)
    await mail_setup.send_message(message)
    return JSONResponse(
        content={
            "message":"Email sent succesfully."
        }
    )
    
     
    


