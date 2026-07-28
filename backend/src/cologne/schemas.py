from pydantic import BaseModel
import uuid

class CologneClient(BaseModel):
   name:str
   brand:str
   type:str
   amount:int = 0
   price:float 
   model_config = {
        "from_attributes": True
    }
class Cologne(CologneClient):
   uid:uuid.UUID  
class UpdateCologne(BaseModel):
    price:float
    

