from pydantic import BaseModel
from typing import Optional,List
import uuid
from datetime import datetime
from backend.src.item.schemas import ItemClient
class SaleClient(BaseModel):
    items: List[ItemClient]    
    email:str
    model_config = {
        "from_attributes":True
    }
    
class Sales(BaseModel):
    sales_id:Optional[int]
    customer_id:int
    total_price:float 
    sale_date:datetime
    