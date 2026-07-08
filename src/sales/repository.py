from src.sales.interface import SaleInterface
from src.shared.generic_repository import GenericSQLModelRepository
from src.sales.schemas import SaleClient,Sales
from src.sales.models import SalesDB

class SalesRepo(GenericSQLModelRepository[Sales,SaleClient,int],SaleInterface):
    def __init__(self, session):
        super().__init__(session=session, cls_model=SalesDB, cls_schema=SaleClient)
    async def sale_process(self, sale_obj:dict):
        sales_update_db = self.cls_model.model_validate(sale_obj)
        self.session.add(sales_update_db)
        await self.session.commit()
        await self.session.refresh(sales_update_db)
        return True
    
    