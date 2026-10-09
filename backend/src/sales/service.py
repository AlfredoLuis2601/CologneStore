from backend.src.cologne.interface import CologneRepoInterface
from backend.src.auth.interface import UserRepoInterface
from backend.src.sales.interface import SaleInterface
from backend.src.item.interface import ItemRepoInterface
from backend.src.config.error_handling import EmptyInventory
from backend.src.cologne.schemas import Cologne
from backend.src.sales.schemas import SaleClient,Sales
from backend.src.config.error_handling import UserNotFound,CologneNotFound,InvalidToken
from datetime import datetime, timezone
from typing import List
from backend.src.item.schemas import ItemClient, Item

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
             "customer_id":user_info.customer_id,"total_price":total_price,"sale_date": datetime.now(timezone.utc).replace(tzinfo=None)
            }
            sales = await self.sales_repo_instance.sale_process(sales_information)
            for item in items:
               item.delivery_date = item.delivery_date.replace(tzinfo=None)
               item_info = item.model_dump()
               item_info["sales_id"] = sales.sales_id              
               await self.item_repo_instance.add_item(item_info)             
               await self.cologne_repo_instance.update_inventory(item.uid,item.amount)
            return True
        else:
              raise UserNotFound()
    
    async def get_items(self, token_data: dict) -> List[List[Item]]:
        payload = token_data.get("user_information", None)
        user_id = int(payload.get("user_id"))
        if not user_id:
            raise InvalidToken()
        all_items: List[List[Item]] = []
        sales: List[Sales] = await self.sales_repo_instance.get_sales_by_user(user_id)
        for sale in sales:
            items = await self.item_repo_instance.get_items_by_sale(sale.sales_id)
            all_items.append(items)
        return all_items
        
        
        
          
