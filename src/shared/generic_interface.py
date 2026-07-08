from abc import abstractmethod,ABC
from typing import Generic,TypeVar,List
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.responses import JSONResponse
#Project structure: Generic interface and generic repository(save,get_by_id,delete,update)
#Specific class of interface and repository for each functionality of application, which will have access through composition to the generic
#repositories and interfaces,however the specific ones will be able to nmodify the methods for their own particularities.
schema = TypeVar("T") #Criacao do schema generico
schema_client = TypeVar("schema_client")
id_type = TypeVar("id_type")
class GenericRepoInterface(ABC,Generic[schema,schema_client,id_type]): #Agora todas as interfaces herdam da generic automaticamente com especificacao de suas proprias entities   
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
   
    
    