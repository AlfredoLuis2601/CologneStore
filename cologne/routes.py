from fastapi import APIRouter
from cologne.schemas import CologneClient,Cologne,UpdateCologne,UserClient,UserUpdate,SaleClient
from fastapi import status
from fastapi.exceptions import HTTPException
from typing import Optional,List,Dict
from fastapi import Depends
from .db_crud import CologneCRUD
from sqlmodel.ext.asyncio.session import AsyncSession
from .database import get_session
from .dependencies import get_user_info,RoleChecker
cologne_routes = APIRouter()
crud = CologneCRUD()
admin_role_checker = RoleChecker(["admin"])
user_role_checker = RoleChecker(["User","admin"])

@cologne_routes.get("/",response_model=List[CologneClient],status_code=status.HTTP_200_OK)
async def get_colognes(session:AsyncSession = Depends(get_session),user_info = Depends(get_user_info),
role:str = Depends(admin_role_checker.check_role)):
    
    colognes = await crud.pick_colognes(session)
    if colognes is not None:
        return colognes
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Could not return any cologne, the inventory is empty.")
    
@cologne_routes.post("/",response_model=CologneClient,status_code=status.HTTP_201_CREATED)
async def create_cologne(raw_cologne_data:CologneClient,session:AsyncSession = Depends(get_session),user_info = Depends(get_user_info),
role:str = Depends(admin_role_checker.check_role)):
    
    new_cologne = await crud.add_cologne(raw_cologne_data,session)
    return new_cologne

@cologne_routes.get("/{cologne_name}",response_model=CologneClient,status_code=status.HTTP_200_OK)
async def get_cologne(cologne_name:str,session:AsyncSession = Depends(get_session),user_info = Depends(get_user_info),
role:str = Depends(admin_role_checker.check_role)):
    
    cologne = await crud.pick_cologne(cologne_name,session=session)
    if cologne is not None:
        return cologne
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Cologne not found.")
    
@cologne_routes.patch("/{cologne_name}",response_model=CologneClient,status_code=status.HTTP_200_OK)
async def update_cologne(cologne_name:str,raw_update_data:UpdateCologne,session:AsyncSession = Depends(get_session),user_info = Depends(get_user_info),
role:str = Depends(admin_role_checker.check_role)):
    
    updated_cologne = await crud.fresh_cologne(cologne_name,raw_update_data,session)
    if updated_cologne is not None:
        return updated_cologne
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Cologne not found in the inventory.")
    
@cologne_routes.delete("/{cologne_name}",response_model=dict,status_code=status.HTTP_200_OK)
async def remove_cologne(cologne_name:str,session:AsyncSession = Depends(get_session),user_info = Depends(get_user_info),
role:str = Depends(admin_role_checker.check_role)):
    
    delete_message = await crud.delete_cologne(cologne_name=cologne_name,session=session)
    if delete_message is not None:
        return delete_message
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Cologne could not be deleted,because it was not found.")

@cologne_routes.post("/sales",response_model=Dict,status_code=status.HTTP_201_CREATED)
async def sale_process(sale_data:SaleClient,session:AsyncSession = Depends(get_session),user_info = Depends(get_user_info),
role:str = Depends(user_role_checker.check_role)):
    
    approved = await crud.purchase_process(sale_data,session)
    return {"data":"Sale has been approved."}