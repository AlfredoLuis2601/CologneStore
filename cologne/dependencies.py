#All the user (jwt) dependencies 

from fastapi.security import OAuth2PasswordBearer 
from .utils import decode_JWT
from fastapi.exceptions import HTTPException
from fastapi import status, Depends
from .redis_config import token_black_list
from typing import List
from pydantic import BaseModel
token_bearer = OAuth2PasswordBearer(tokenUrl="/api/v1/cologne_store/users/signIn") #Busca o acesstoken no dicionario retornado pelo signIn
async def get_user_info(token:str = Depends(token_bearer)):
    token_data:dict = decode_JWT(token)
    jti = token_data.get("jti")
    check_token = await token_black_list.get(jti)
    if check_token is not None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User has already done the logout.")
    elif token_data is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid or expired token.")
    elif token_data["refresh"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="A refresh token cannot be used as an access token.")
    return token_data
def get_token_payload(token:str):
    token_data = decode_JWT(token)
    if token_data is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid or expired token.")
    return token_data
def verify_access_token(token:str = Depends(token_bearer)):
    token_data = get_token_payload(token)
    if token_data is not None and token_data["refresh"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Please generate an access token.")
    return token_data
def verify_refresh_token(token:str = Depends(token_bearer)):
    token_data = decode_JWT(token)
    if token_data is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid or expired token.")
    elif token_data is not None and not token_data["refresh"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Please generate a refresh token")
    return token_data 
class RoleChecker():   
  def __init__(self,roles:List[str]):
    self.roles = roles
  def check_role(self,payload:dict = Depends(get_user_info)):
    user_data:dict = payload.get("user_information")
    if user_data.get("role") in self.roles:
        return True
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You don't have permition.")
        

