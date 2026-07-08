from src.shared.generic_interface import GenericRepoInterface
from src.cologne.schemas import Cologne,CologneClient,UpdateCologne
from abc import abstractmethod
class CologneRepoInterface(GenericRepoInterface[Cologne,CologneClient,int]):
    @abstractmethod
    async def update_cologne(self,id:str,raw_update_info:UpdateCologne)->bool:
        pass
    @abstractmethod
    async def get_by_name(self,cologne_name:str)->Cologne:
        pass
    @abstractmethod
    async def update_inventory(self,id:str,amount:int)->bool:
        pass

