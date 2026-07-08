from fastapi import APIRouter
from .schemas import CologneClient,Cologne,UpdateCologne
from fastapi import status
from fastapi.responses import JSONResponse
from typing import List
from fastapi import Depends
from src.auth.user_dependencies import get_user_info,RoleChecker,verify_email
from src.shared.dependencies import get_cologne_service
from uuid import UUID
from src.cologne.service import ColognesService
from src.config.error_handling import CologneNotFound,DeleteCologne

cologne_router = APIRouter()
admin_role_checker = RoleChecker(["admin"])
user_role_checker = RoleChecker(["User","admin"])

@cologne_router.get("/",response_model=List[Cologne],status_code=status.HTTP_200_OK)
async def get_colognes(service:ColognesService = Depends(get_cologne_service),user_info = Depends(get_user_info),
role:str = Depends(admin_role_checker.check_role),is_verified = Depends(verify_email)):
    colognes = await service.get_colognes()
    if colognes is not None:
        return colognes
    else:
        raise CologneNotFound()
    
@cologne_router.post("/",response_model=Cologne,status_code=status.HTTP_201_CREATED)
async def create_cologne(raw_cologne_data:CologneClient,user_info = Depends(get_user_info),
role:str = Depends(admin_role_checker.check_role),service:ColognesService = Depends(get_cologne_service),is_verified=Depends(verify_email)):   
    new_cologne = await service.add_cologne(raw_cologne_data)
    return new_cologne

@cologne_router.get("/{cologne_name}",response_model=Cologne,status_code=status.HTTP_200_OK)
async def get_cologne(cologne_name:str,user_info = Depends(get_user_info),
role:str = Depends(user_role_checker.check_role),service:ColognesService = Depends(get_cologne_service),is_verified = Depends(verify_email)):
    
    cologne = await service.get_cologne(cologne_name)
    if cologne is not None:
        return cologne
    else:
        raise CologneNotFound()
    
@cologne_router.patch("/{cologne_uid}",response_model=CologneClient,status_code=status.HTTP_200_OK)
async def update_cologne(cologne_uid:UUID,raw_update_data:UpdateCologne,service:ColognesService = Depends(get_cologne_service),user_info = Depends(get_user_info),
role:str = Depends(admin_role_checker.check_role),is_verified = Depends(verify_email)):
    
    updated_cologne = await service.patch_cologne(cologne_uid,raw_update_data)
    return JSONResponse(
        status_code=200,
        content="Cologne has been succesfully updated!"
    )
    
    
@cologne_router.delete("/{cologne_uid}",response_model=dict,status_code=status.HTTP_200_OK)
async def remove_cologne(cologne_uid:UUID,user_info = Depends(get_user_info),
role:str = Depends(admin_role_checker.check_role),service:ColognesService = Depends(get_cologne_service)):
    
    delete_message = await service.delete_cologne(cologne_uid)
    if delete_message:
        return JSONResponse(
            status_code=200,
            content={
                "detail":"Cologne has been succesfully deleted."
            }
        )
    else:
        raise DeleteCologne()
