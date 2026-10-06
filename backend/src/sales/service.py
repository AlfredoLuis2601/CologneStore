from backend.src.cologne.interface import CologneRepoInterface
from backend.src.auth.interface import UserRepoInterface
from backend.src.sales.interface import SaleInterface
from backend.src.item.interface import ItemRepoInterface
from backend.src.config.error_handling import EmptyInventory
from backend.src.cologne.schemas import Cologne
from backend.src.sales.schemas import SaleClient
from backend.src.config.error_handling import UserNotFound,CologneNotFound
from datetime import datetime
from typing import List
from backend.src.item.schemas import ItemClient
class OrderService():
    
    def __init__(self, user_repo_instance: UserRepoInterface, cologne_repo_instance: CologneRepoInterface, sales_repo_instance: SaleInterface, item_repo_instance: ItemRepoInterface):
        self.user_repo_instance = user_repo_instance
        self.cologne_repo_instance = cologne_repo_instance
        self.sales_repo_instance = sales_repo_instance
        self.item_repo_instance = item_repo_instance
        
    async def create_order(self,raw_sale_data: SaleClient):
        items = raw_sale_data.items
        total_price = 0
        for item in items:            
          db_cologne:Cologne = await self.cologne_repo_instance.get_by_id(item.uid)
          if db_cologne is not None:
             if db_cologne.amount< item.amount:
                raise EmptyInventory()
             total_price += db_cologne.price * item.amount
          else:
              raise CologneNotFound()
        user_info = await self.user_repo_instance.get_by_email(raw_sale_data.email)
        if user_info is not None:
            sales_information = {
             "customer_id":user_info.customer_id,"total_price":total_price,"sale_date": datetime.now()
            }
            sales = await self.sales_repo_instance.sale_process(sales_information)
            for item in items:
               item_info = item.model_dump()
               item_info["sales_id"] = sales.sales_id               
               await self.item_repo_instance.add_item(item_info)             
               await self.cologne_repo_instance.update_inventory(item.uid,item.amount)
            return True
        else:
              raise UserNotFound()
          
