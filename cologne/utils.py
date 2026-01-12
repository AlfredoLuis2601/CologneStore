from sqlmodel import SQLModel
from passlib.context import CryptContext
import jwt
from jwt.exceptions import ExpiredSignatureError
from datetime import datetime,timedelta,timezone 
from .config_env import jwt_key,jwt_algorithm
import logging
import uuid
password_context = CryptContext(
    schemes=["argon2"]
)
def get_hash(password:str)->str:
    hash_password = password_context.hash(password)
    return hash_password

def get_password(hash:str,password:str)->bool:
    is_Verified = password_context.verify(hash=hash,secret=password)
    return is_Verified

DEFAULT_TIMEDELTA = 3600 # Time in minutes

def generate_JWT(user_data:dict,expiration_time:timedelta = None,is_refresh:bool = False)->str:
   if expiration_time is None:
       time = timedelta(seconds=DEFAULT_TIMEDELTA)
       expiry= datetime.now(timezone.utc) + time 
   else:
       expiry = datetime.now(timezone.utc) + expiration_time
   payload = {
       "user_information":user_data,
       "exp":expiry, # nome padrao da chave
       "refresh":is_refresh,
       "jti":str(uuid.uuid4()) #jti: Json Token Identifier
   }
   token = jwt.encode(
       payload= payload,
       key=jwt_key,
       algorithm=jwt_algorithm
   )
   
   return token 

def decode_JWT(token:str):
    try:
      payload = jwt.decode(
        jwt=token,
        algorithms=[jwt_algorithm],
        key=jwt_key
    )
      return payload
    except (jwt.PyJWKError,ExpiredSignatureError) as error: #Normally the error is that the token expirate
        logging.exception(error)
        return None 

     