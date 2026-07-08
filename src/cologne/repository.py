from src.shared.generic_repository import GenericSQLModelRepository
from src.cologne.interface import CologneRepoInterface
from src.cologne.models import CologneInformationDB
from src.cologne.schemas import Cologne,CologneClient,UpdateCologne
from sqlmodel import select
from uuid import UUID
class CologneRepo(GenericSQLModelRepository[Cologne,CologneClient,UUID],CologneRepoInterface):
    def __init__(self, session):
        super().__init__(session=session, cls_model=CologneInformationDB, cls_schema=Cologne)
        
    async def update_cologne(self, id:UUID, raw_update_info:UpdateCologne):
         update_info = raw_update_info.model_dump()
         to_update_cologne = await self.session.get(self.cls_model,id)
         if to_update_cologne is not None:
            for k,v in update_info.items():
                setattr(to_update_cologne,k,v)
            self.session.add(to_update_cologne)
            await self.session.commit()
            await self.session.refresh(to_update_cologne)
            return True
         else:
             return False
    async def get_by_name(self,cologne_name:str)->Cologne:
        command = select(self.cls_model).where(cologne_name==self.cls_model.name)
        result = await self.session.exec(command)
        cologne = result.first()
        if cologne is not None:
          return self.cls_schema.model_validate(cologne)
        return False
    async def update_inventory(self, id:UUID, amount)->None:
       db_cologne = await self.session.get(self.cls_model, id)
       db_cologne.amount = db_cologne.amount - amount
       self.session.add(db_cologne)
       await self.session.commit()
       await self.session.refresh(db_cologne)
       
       
    