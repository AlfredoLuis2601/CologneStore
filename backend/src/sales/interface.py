from backend.src.shared.generic_interface import GenericRepoInterface
from abc import ABC,abstractmethod
from backend.src.sales.schemas import SaleClient,Sales
from typing import List
class SaleInterface(GenericRepoInterface[Sales,SaleClient,int]):
    
    @abstractmethod
    async def sale_process(self,sale_obj:dict)->Sales:
       pass
   
    @abstractmethod 
    async def get_sales_by_user(self, customer_id: int) -> List[Sales]:
        pass
