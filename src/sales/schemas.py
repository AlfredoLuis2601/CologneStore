from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

class SaleClient(BaseModel):#Request to the db and see if there is any cologne with this name 
    uid:uuid.UUID        #and if it is available.
    amount_bought:int        #Update the sales table and the cologne table
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
    