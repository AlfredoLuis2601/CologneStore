from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from typing import List
from fastapi import status
from fastapi import Depends
from .schemas import UserClient,User,ResponseToken,UserBearer,PasswordReset
from .user_dependencies import verify_refresh_token,get_user_info,RoleChecker
from fastapi.security import OAuth2PasswordRequestForm
from src.shared.dependencies import get_auth_service
from src.auth.service import AuthService
from pydantic import EmailStr

customer_routes = APIRouter()
user_role_checker = RoleChecker(["User","admin"])
admin_role_checker = RoleChecker(["admin"])
@customer_routes.get("/",response_model=List[User],status_code=status.HTTP_200_OK)
async def get_users(service:AuthService = Depends(get_auth_service),role:str = Depends(admin_role_checker.check_role)):
    users = await service.get_users()
    return users

@customer_routes.post("/sign_up",status_code=status.HTTP_201_CREATED)
async def sign_up_users(user_data:UserClient,service:AuthService = Depends(get_auth_service)):
    user = await service.sign_up(user_data)
    response = await service.verify_account_email(user)
    if response:
      return JSONResponse(
            content={
                "message":"Account created succesfully."
            },
            status_code=201
        )
      
@customer_routes.post("/signIn",response_model=dict,status_code=status.HTTP_200_OK)
async def sign_in_users(user_data:UserClient,service:AuthService = Depends(get_auth_service)):
    approved = await service.sign_in(user_data)
    return approved

@customer_routes.post("/sign_in_swagger",status_code=status.HTTP_200_OK)
async def sign_swagger(user_data:OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),service:AuthService = Depends(get_auth_service)):
    obj_user = UserClient(email=user_data.username,hash_password=user_data.password)
    approved = await service.sign_in(obj_user)
    return approved

@customer_routes.get("/validate_account/{token}", status_code=status.HTTP_200_OK) #Option without the frontend
@customer_routes.post("/validate_account/{token}",status_code=status.HTTP_200_OK)
async def verify_account(token:str,service:AuthService = Depends(get_auth_service)):
    response = await service.verify_account(token)
    return JSONResponse(
        content= "Account verified succesfully",
        status_code=200
    )
    
@customer_routes.post("/refresh_token",response_model=dict,status_code=status.HTTP_201_CREATED)
async def new_access_token(token_data:dict = Depends(verify_refresh_token),check_role:str = Depends(admin_role_checker.check_role),service:AuthService = Depends(get_auth_service)):
    token_response = await service.new_access_token(token_data)
    return token_response

@customer_routes.post("/logout",response_model=dict,status_code=status.HTTP_200_OK)
async def logout(payload:dict = Depends(get_user_info),role:str = Depends(user_role_checker.check_role),service:AuthService = Depends(get_auth_service))->dict:
    response = await service.add_token_to_block_list(payload)
    return response   

@customer_routes.get("/current_user",response_model=dict,status_code=status.HTTP_200_OK)
async def get_current_user(payload:dict = Depends(get_user_info),role:str = Depends(admin_role_checker.check_role)):
    return payload 

@customer_routes.post("/delete_user",status_code=status.HTTP_201_CREATED)
async def delete_user(id:int,service:AuthService = Depends(get_auth_service),role:str = Depends(admin_role_checker.check_role)):
    response = await service.delete_user(id)   
    return JSONResponse(
            content={
                "message":"User deleted successfully."
            }
        )
@customer_routes.post("/password_reset",status_code=status.HTTP_200_OK) 
async def send_mail_reset(email:EmailStr,service:AuthService = Depends(get_auth_service),role:str = Depends(user_role_checker.check_role))->JSONResponse:
    await service.password_reset_email(email)
    return JSONResponse(
        content={
            "message":"Email has been sent succesfully!"
        },
        status_code=200
    )
    
@customer_routes.get("/password_reset/{token}",status_code=status.HTTP_200_OK)
@customer_routes.post("/password_reset/{token}",status_code=status.HTTP_200_OK)
async def change_password(token:str,password_info:PasswordReset,service:AuthService = Depends(get_auth_service),role:str = Depends(admin_role_checker.check_role)):
    response = await service.password_reset(password_info=password_info,key=token)
    if response:
        return {
            "data": "Password reset succeeded!"
        }