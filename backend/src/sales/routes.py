from fastapi import APIRouter
from typing import Dict
from fastapi import status,Depends
from backend.src.sales.service import OrderService
from backend.src.shared.dependencies import get_order_service
from backend.src.auth.user_dependencies import get_user_info,RoleChecker
from backend.src.sales.schemas import SaleClient
from fastapi.responses import JSONResponse
from typing import List
from backend.src.item.schemas import Item
user_role_checker = RoleChecker(["User", "admin"])
sales_router = APIRouter()

@sales_router.post("/order",response_model=Dict,status_code=status.HTTP_201_CREATED)
async def sale_process(sale_data:SaleClient,service:OrderService = Depends(get_order_service),user_info = Depends(get_user_info),
role: str = Depends(user_role_checker.check_role)):    
    approved = await service.create_order(sale_data)
    return JSONResponse(
        status_code=200,
        content={
            "message":"Sale has been succesfully done!"
        }      
    )
    
@sales_router.get("/order", response_model= List[List[Item]],status_code=status.HTTP_200_OK)
async def get_items(service: OrderService = Depends(get_order_service), user_payload = Depends(get_user_info),
role: str = Depends(user_role_checker.check_role)) -> List[List[Item]]:
    
    all_items = await service.get_items(user_payload)
    return all_items