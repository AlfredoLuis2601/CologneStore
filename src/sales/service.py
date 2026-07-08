from src.cologne.interface import CologneRepoInterface
from src.auth.interface import UserRepoInterface
from src.sales.interface import SaleInterface
from src.config.error_handling import EmptyInventory
from src.cologne.schemas import Cologne
from src.sales.schemas import SaleClient
from src.config.error_handling import UserNotFound,CologneNotFound
from datetime import datetime
class OrderService():
    def __init__(self,user_repo_instance:UserRepoInterface,cologne_repo_instance:CologneRepoInterface,sales_repo_instance:SaleInterface):
        self.user_repo_instance = user_repo_instance
        self.cologne_repo_instance = cologne_repo_instance
        self.sales_repo_instance = sales_repo_instance
    async def create_order(self,raw_sale_data:SaleClient):
        db_cologne:Cologne = await self.cologne_repo_instance.get_by_id(raw_sale_data.uid)
        if db_cologne is not None:
            if db_cologne.amount<raw_sale_data.amount_bought:
                raise EmptyInventory()
            user_info = await self.user_repo_instance.get_by_email(raw_sale_data.email)
            if user_info is not None:
                sales_information = {
                  "uid": db_cologne.uid,"customer_id":user_info.customer_id,"amount_bought":raw_sale_data.amount_bought,"price":db_cologne.price,"sale_date": datetime.now()
              }
                response = await self.sales_repo_instance.sale_process(sales_information)
                await self.cologne_repo_instance.update_inventory(db_cologne.uid,raw_sale_data.amount_bought)
                return response
            else:
              raise UserNotFound()
        else:
           raise CologneNotFound()