from src.shared.generic_interface import GenericRepoInterface,schema,schema_client,id_type
from sqlmodel import SQLModel,select
from typing import Type,List
from sqlmodel.ext.asyncio.session import AsyncSession


class GenericSQLModelRepository(GenericRepoInterface[schema,schema_client,id_type]): 
    
    def __init__(self,session:AsyncSession,cls_model:Type[SQLModel],cls_schema:Type[schema]):
        self.session = session
        self.cls_model = cls_model 
        self.cls_schema = cls_schema
    
    async def add(self, object:schema_client)->schema:
        new_object = self.cls_model.model_validate(object) #Validation from the table 
        self.session.add(new_object)
        await self.session.commit() 
        await self.session.refresh(new_object) 
        return self.cls_schema.model_validate(new_object)
    async def get_by_id(self, id)->List[schema]:
        object = await self.session.get(self.cls_model,id)
        return self.cls_schema.model_validate(object)
    async def get_all(self):
        command = select(self.cls_model)
        result = await self.session.exec(command)
        objects = result.all()
        return [self.cls_schema.model_validate(obj) for obj in objects]
    async def delete(self, id)->bool:
       object_to_be_deleted = await self.session.get(self.cls_model,id) 
       if object_to_be_deleted is not None:
           await self.session.delete(object_to_be_deleted)
           await self.session.commit()
           return True
       else:
           return False
    
        
    
    
        
        
