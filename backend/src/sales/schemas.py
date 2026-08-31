from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

class SaleClient(BaseModel):
    uid:uuid.UUID        
    amount_bought:int        
    email:str
    model_config = {
        "from_attributes":True
    }
class Sales(BaseModel):
    sales_id:Optional[int]
    uid:uuid.UUID
    customer_id:int
    amount_bought:int 
    price:float 
    sale_date:datetime
    