from backend.src.shared.generic_interface import GenericRepoInterface
from backend.src.item.schemas import Item,ItemClient
from abc import abstractmethod
from typing import List

class ItemRepoInterface(GenericRepoInterface[Item,ItemClient, int]):
    @abstractmethod
    async def get_items_by_sale(self, sales_id: int)-> List[Item]:
        pass
    @abstractmethod
    async def add_item(self, item_info: dict):
        pass
    
    