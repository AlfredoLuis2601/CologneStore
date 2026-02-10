from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid

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
    
