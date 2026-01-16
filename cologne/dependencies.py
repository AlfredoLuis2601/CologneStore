#All the user (jwt) dependencies 

from fastapi.security import OAuth2PasswordBearer 
from .utils import decode_JWT
from fastapi.exceptions import HTTPException
from fastapi import status, Depends
from .redis_config import token_black_list
from typing import List
from pydantic import BaseModel
from .error_handling import EmptyInventory,UserAlreadyExist,UserNotFound,TokenAlreadyInBlackList,InvalidToken,RefreshTokenToAccess,CologneNotFound,DeleteCologne,WrongPassword,RolePermission,GenerateRefresh
token_bearer = OAuth2PasswordBearer(tokenUrl="/api/v1/cologne_store/users/signIn") #Busca o acesstoken no dicionario retornado pelo signIn
async def get_user_info(token:str = Depends(token_bearer)):
    token_data:dict = decode_JWT(token)
    jti = token_data.get("jti")
    check_token = await token_black_list.get(jti)
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
        

