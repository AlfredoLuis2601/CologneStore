from fastapi.security import OAuth2PasswordBearer 
from .utils_security import decode_JWT
from src.db.database import get_session
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.db.models import CustomersDB
from fastapi import status, Depends
from src.tasks.redis_config import token_block_list
from typing import List
from pydantic import BaseModel
from src.config.error_handling import EmptyInventory,UserAlreadyExist,UserNotFound,TokenAlreadyInBlackList,InvalidToken,RefreshTokenToAccess,CologneNotFound,DeleteCologne,WrongPassword,RolePermission,GenerateRefresh,EmailNotVerified
token_bearer = OAuth2PasswordBearer(tokenUrl="/api/v1/cologne_store/users/signIn") #Busca o acesstoken no dicionario retornado pelo signIn
async def get_user_info(token:str = Depends(token_bearer)):
    token_data:dict = decode_JWT(token)
    jti = token_data.get("jti")
    check_token = await token_block_list.get(jti)
    if check_token is not None:
        raise TokenAlreadyInBlackList()
    elif token_data is None:
        raise InvalidToken()
    elif token_data["refresh"]:
        raise RefreshTokenToAccess()
    return token_data
def get_token_payload(token:str):
    token_data = decode_JWT(token)
    if token_data is None:
        raise InvalidToken()
def verify_refresh_token(token:str = Depends(token_bearer)):
    token_data = decode_JWT(token)
    if token_data is None:
        raise InvalidToken()
    elif token_data is not None and not token_data["refresh"]:
        raise GenerateRefresh()
class RoleChecker():   
  def __init__(self,roles:List[str]):
    self.roles = roles
  def check_role(self,payload:dict = Depends(get_user_info)):
    user_data:dict = payload.get("user_information")
    if user_data.get("role") in self.roles:
        return True
    else:
        raise RolePermission(
            required_role=self.roles,
            user_role=user_data.get("role")
        )
async def verify_email(session:AsyncSession = Depends(get_session),payload:dict = Depends(get_user_info)):
    user_info:dict = payload.get("user_information")
    email = user_info.get("username")
    command = select(CustomersDB.is_verified).where(email==CustomersDB.email)   
    result = await session.exec(command)
    verified = result.first()
    if verified:
        return True
    else:
        raise EmailNotVerified()
#Add the dependency in almost all routes
