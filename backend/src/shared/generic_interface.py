from abc import abstractmethod,ABC
from typing import Generic,TypeVar,List
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.responses import JSONResponse

schema = TypeVar("T") 
schema_client = TypeVar("schema_client")
id_type = TypeVar("id_type")

class GenericRepoInterface(ABC,Generic[schema,schema_client,id_type]): 
     
    @abstractmethod
    async def add(self,object:schema_client)->schema:
        pass
    
    @abstractmethod
    async def get_by_id(self,id:id_type)->schema:
        pass 
    
    @abstractmethod
    async def delete(self,id:id_type)->bool:
        pass
    
    @abstractmethod
    async def get_all(self)->List[schema]:
        pass
    
    @abstractmethod
    async def get_all_by_fields(self, field_name: str, value):
        pass
    
    @abstractmethod
    async def add_with_payload(self, payload: dict):
        pass
    
    