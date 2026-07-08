from src.cologne.repository import CologneRepo
from src.auth.repository import AuthRepo
from src.sales.repository import SalesRepo
from src.cologne.service import ColognesService
from src.auth.service import AuthService
from src.sales.service import OrderService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.config.database import get_session
from fastapi import Depends


def get_cologne_service(session:AsyncSession = Depends(get_session))->ColognesService:
    repo = CologneRepo(session)
    service = ColognesService(repo)
    return service

def get_order_service(session:AsyncSession = Depends(get_session))->OrderService:
    sales_repo = SalesRepo(session)
    auth_repo = AuthRepo(session)
    cologne_repo = CologneRepo(session)
    service = OrderService(auth_repo,cologne_repo,sales_repo)
    return service

def get_auth_service(session:AsyncSession = Depends(get_session))->AuthService:
    auth_repo = AuthRepo(session)
    service = AuthService(auth_repo)
    return service