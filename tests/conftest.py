from fastapi.testclient import TestClient
from src import my_app
from src.auth.user_dependencies import get_user_info
from src.shared.dependencies import get_auth_service,get_order_service
from unittest.mock import Mock,AsyncMock,MagicMock
from src.config.database import get_session

import pytest

@pytest.fixture
async def fake_session():
    mock_session = AsyncMock()
    def get_mock_session():   
       yield mock_session  
    my_app.dependency_overrides[get_session] = get_mock_session   
    yield mock_session
    my_app.dependency_overrides.pop(get_session,None) 
    
@pytest.fixture(scope='session')
def get_client():
    with TestClient(my_app) as client:
        yield client
    my_app.dependency_overrides.clear()    
@pytest.fixture()
def fake_user_info():
    mock_user_info = Mock()
    def get_mock_user_info():
      yield mock_user_info
    my_app.dependency_overrides[get_user_info] = get_mock_user_info
    yield mock_user_info
    my_app.dependency_overrides.pop(get_user_info,None)


mock_cologne_repo = Mock()
mock_sales_repo = Mock()

@pytest.fixture()
async def fake_auth_service():
    mock_auth_service = AsyncMock()
    my_app.dependency_overrides[get_auth_service] = lambda:mock_auth_service
    yield mock_auth_service
    my_app.dependency_overrides.pop(get_auth_service,None)

@pytest.fixture()
async def fake_order_service():
    mock_order_service = AsyncMock()
    def get_mock_service():
        yield mock_order_service
    my_app.dependency_overrides[get_order_service] = get_mock_service
    yield mock_order_service
    my_app.dependency_overrides.pop(get_order_service,None)

#Create fake_role_dependency 
    