from fastapi.routing import APIRouter
from typing import List,Dict
from fastapi.exceptions import HTTPException
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from .database import get_session
from .models import CustomersDB
from .schemas import UserClient,SaleClient,User,ResponseToken,UserBearer
from .db_crud import CologneCRUD
from .dependencies import verify_refresh_token,get_user_info
from .utils import decode_JWT,generate_JWT
from fastapi.security import OAuth2PasswordRequestForm
from .dependencies import RoleChecker
from .error_handling import EmptyInventory,UserAlreadyExist,UserNotFound,TokenAlreadyInBlackList,InvalidToken,RefreshTokenToAccess,CologneNotFound,DeleteCologne,WrongPassword,RolePermission,GenerateRefresh
customer_routes = APIRouter()
crud = CologneCRUD()
user_role_checker = RoleChecker(["User","admin"])
admin_role_checker = RoleChecker(["admin"])
@customer_routes.get("/",response_model=List[UserClient],status_code=status.HTTP_200_OK)
async def get_users(session:AsyncSession = Depends(get_session),role:str = Depends(admin_role_checker.check_role)):
    users = await crud.load_users(session=session)
    if users:
        return users
    else:
        raise UserNotFound()

@customer_routes.post("/sign_up",response_model=CustomersDB,status_code=status.HTTP_201_CREATED)
async def sign_up_users(user_data:UserClient,session:AsyncSession = Depends(get_session),role:str = Depends(user_role_checker.check_role)):
    user= await crud.signUp(user_data,session)
    if user is not None:
        return user
    else:
        raise UserAlreadyExist()

@customer_routes.post("/signIn",response_model=dict,status_code=status.HTTP_200_OK)
async def sign_in_users(user_data:OAuth2PasswordRequestForm = Depends(),session:AsyncSession = Depends(get_session)):
    approved = await crud.signIn(session=session,raw_user_data=user_data)
    if approved:
        return approved
    else:
        raise WrongPassword()
@customer_routes.post("/refresh_token",response_model=dict,status_code=status.HTTP_201_CREATED)
async def new_access_token(token_data:dict = Depends(verify_refresh_token),check_role:str = Depends(admin_role_checker.check_role)):
    username = token_data.get("username")
    user_id = token_data.get("user_id")
    refresh_acess_token = generate_JWT(user_data={"username":username,"user_id":user_id},is_refresh=False)
    return {
        "access_token":refresh_acess_token,
        "token_type":"bearer"
    }
@customer_routes.post("/logout",response_model=dict,status_code=status.HTTP_200_OK)
async def logout(payload:dict = Depends(get_user_info),role:str = Depends(user_role_checker.check_role))->dict:
    response = await crud.add_access_token_blacklist(payload)
    return response   

@customer_routes.get("/current_user",response_model=dict,status_code=status.HTTP_200_OK)
async def get_current_user(payload:dict = Depends(get_user_info),role:str = Depends(admin_role_checker.check_role)):
    return payload 