from backend.src.shared.generic_repository import GenericSQLModelRepository
from .interface import ItemRepoInterface
from .schemas import Item,ItemClient
from .model import ItemDB
from sqlmodel.ext.asyncio.session import AsyncSession

class ItemRepository(GenericSQLModelRepository[Item,ItemClient], ItemRepoInterface):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, cls_schema=Item, cls_model=ItemDB)
    
    async def get_items_by_sale(self, sales_id):
        return await super().get_all_by_fields("sales_id",sales_id)
    
    async def add_item(self, item_info):
        return await super().add_with_payload(payload= item_info)
    
    