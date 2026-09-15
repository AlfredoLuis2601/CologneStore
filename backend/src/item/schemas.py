from pydantic import BaseModel
import uuid
from datetime import datetime

class ItemClient(BaseModel):
    uid:uuid.UUID
    amount: int
    delivery_date: datetime
    model_config ={
        "from_attributes":True
    }
class Item(ItemClient):
    item_id: uuid.UUID
    sales_id: int
    