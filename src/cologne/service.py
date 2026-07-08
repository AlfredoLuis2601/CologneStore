from src.cologne.interface import CologneRepoInterface
from src.cologne.schemas import Cologne,CologneClient,UpdateCologne
from src.config.error_handling import CologneNotFound,DeleteCologne,EmptyInventory
from typing import List
from uuid import UUID
class ColognesService():
    def __init__(self,repo_instance:CologneRepoInterface):
        self.repo_instance = repo_instance
    
    async def add_cologne(self,cologne_client:CologneClient):
        response = await self.repo_instance.add(cologne_client)
        return response
    async def get_colognes(self)->List[Cologne]:
        response = await self.repo_instance.get_all()
        if response is not None:
            return response
        raise CologneNotFound()
    async def get_cologne(self,name:str)->Cologne:
        response = await self.repo_instance.get_by_name(name)
        if not response:
            raise CologneNotFound
        else:
            return response
    async def patch_cologne(self,id:UUID,raw_update_info:UpdateCologne)->bool:
        response = await self.repo_instance.update_cologne(id,raw_update_info)
        if response:
            return response
        raise CologneNotFound()
    async def delete_cologne(self,id:UUID)->bool:
        response = await self.repo_instance.delete(id)
        if response:
            return response
        raise DeleteCologne()
   
            
            
            
                
        
        