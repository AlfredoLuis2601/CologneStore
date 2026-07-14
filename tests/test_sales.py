from unittest.mock import MagicMock,AsyncMock
from src.sales.service import OrderService
import pytest
import uuid
service_path = "src.sales.service"
@pytest.fixture()
async def get_order_service():
    mock_sales_repo = MagicMock()
    mock_auth_repo = MagicMock()
    mock_cologne_repo = MagicMock()
    order_service = OrderService(mock_auth_repo,mock_cologne_repo,mock_sales_repo)
    return mock_sales_repo,mock_auth_repo,mock_cologne_repo,order_service

async def test_order_process(get_order_service):
    sales_repo,auth_repo,cologne_repo,service = get_order_service
    fake_uuid =  uuid.uuid4()
    mock_sale_data = {
        "uid": fake_uuid,
        "amount_bought":2,
        "email":"blob@gmail.com"
    }
    mock_cologne_data = {
        "uid":fake_uuid,
        "amount":3,
        "price":50
    }
    mock_sales_dto = MagicMock(**mock_sale_data)
    cologne_repo.get_by_id = AsyncMock()
    cologne_repo.update_inventory = AsyncMock()
    cologne_repo.get_by_id.return_value = MagicMock(**mock_cologne_data)
    auth_repo.get_by_email = AsyncMock()
    auth_repo.get_by_email.return_value = MagicMock(**{
        "customer_id":1
    })
    sales_repo.sale_process = AsyncMock()
    sales_repo.sale_process.return_value = MagicMock(**{
        "sales_id":2
    })
    response = await service.create_order(mock_sales_dto)
    assert response is not None
    assert response.sales_id == 2
    cologne_repo.get_by_id.assert_called_once_with(fake_uuid)
    auth_repo.get_by_email.assert_called_once_with("blob@gmail.com")
    sales_repo.sale_process.assert_called_once()
    cologne_repo.update_inventory.assert_called_once_with(fake_uuid, 2)
    
    
    
    