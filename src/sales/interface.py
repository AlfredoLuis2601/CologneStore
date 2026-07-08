from src.shared.generic_interface import GenericRepoInterface
from abc import ABC,abstractmethod
from src.sales.schemas import SaleClient,Sales

class SaleInterface(GenericRepoInterface[Sales,SaleClient,int]):
    
    @abstractmethod
    async def sale_process(self,sale_obj:dict)->Sales:
       pass