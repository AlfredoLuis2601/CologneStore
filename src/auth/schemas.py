from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid

class UserClient(BaseModel):
    email:str
    hash_password:str
class User(UserClient):
    customer_id:Optional[int]
    sign_up_date:datetime
    last_update_at:datetime
    is_verified:bool = False
    role:Optional[str]
    token:uuid.UUID
    expiry_token_time:datetime
    reset_password_token:str | None
    expiry_reset_token_time:datetime |None
class UserUpdate(BaseModel):
    email:str
    hash_password:str
    
class ResponseToken(BaseModel):
    message:str
    access_token:str
    refresh_token:str
    token_type:str
    
class UserBearer(BaseModel):
    username:str
    password:str