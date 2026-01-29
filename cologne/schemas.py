from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid
#Schemas for cologneInformation table

class CologneClient(BaseModel):
   name:str
   brand:str
   type:str
   amount:int = 0
   price:float 
class Cologne(CologneClient):
   uid:uuid.UUID  
class UpdateCologne(BaseModel):
    price:float
      
#Standard Schemas for user table:

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
class UserUpdate(BaseModel):
    email:str
    hash_password:str
    
#The sales table wont be affected by request body,so it doesnt need a schema.

class SaleClient(BaseModel):#Request to the db and see if there is any cologne with this name 
    cologne_name:str        #and if it is available.
    amountBought:int        #Update the sales table and the cologne table
    email:str
class Sales(BaseModel):
    sales_id:Optional[int]
    uid:uuid.UUID
    customer_id:int
    amount_required:int 
    price:float 
    sale_date:datetime
    
class ResponseToken(BaseModel):
    message:str
    access_token:str
    refresh_token:str
    token_type:str
    
class UserBearer(BaseModel):
    username:str
    password:str