from fastapi import APIRouter
from typing import Dict
from fastapi import status,Depends
from src.sales.service import OrderService
from src.shared.dependencies import get_order_service
from src.auth.user_dependencies import get_user_info,RoleChecker
from src.sales.schemas import SaleClient
from fastapi.responses import JSONResponse

user_role_checker = RoleChecker(["User"])
sales_router = APIRouter()
@sales_router.post("/order",response_model=Dict,status_code=status.HTTP_201_CREATED)
async def sale_process(sale_data:SaleClient,service:OrderService = Depends(get_order_service),user_info = Depends(get_user_info),
role:str = Depends(user_role_checker.check_role)):
    
    approved = await service.create_order(sale_data)
    return JSONResponse(
        status_code=200,
        content={
            "message":"Sale has been succesfully done!"
        }      
    )