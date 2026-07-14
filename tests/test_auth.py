from src.auth.schemas import UserClient,User
from src.auth.service import AuthService
from unittest.mock import Mock,AsyncMock,MagicMock,patch
import pytest
from uuid import UUID
from datetime import datetime,timezone,timedelta

base_url = "/api/v1/cologne_store/users"
service_path = "src.auth.service"
@pytest.fixture()
async def get_service():
      mock_auth_repo = MagicMock()
      service = AuthService(mock_auth_repo)
      return mock_auth_repo,service
async def test_user_creation(fake_auth_service,fake_session,get_client)->None:
    fake_auth_service.sign_up.return_value = {"id":1,"status":201}
    payload = {
        "email":"joao@gmail.com",
        "hash_password":"joao123"
    }
    response = get_client.post(
        url=f"{base_url}/sign_up",
        json=payload
    )
    assert response.status_code == 201
    expected_user = UserClient(email="joao@gmail.com", hash_password="joao123")
    fake_auth_service.sign_up.assert_called_once()
    fake_auth_service.sign_up.assert_called_once_with(expected_user)

async def test_user_login(fake_auth_service,fake_session,get_client)->None:
    fake_auth_service.sign_in.return_value = {"access_token":"32323232","refresh_token":"3434354353"}
    payload = {
        "email":"alfredoluis2601@gmail.com",
        "hash_password":"joao3433"
    }
    response = get_client.post(
        url=f"{base_url}/signIn",
        json=payload
    )
    assert response.status_code == 200
    expected_user = UserClient(email="alfredoluis2601@gmail.com", hash_password="joao3433")
    fake_auth_service.sign_in.assert_called_once()
    fake_auth_service.sign_in.assert_called_once_with(expected_user)


async def test_service_login(get_service)->None:
    repo,service = get_service
    user_info = UserClient(email="alfredoluis2601@gmail.com",hash_password="luis27")
    repo.get_by_email = AsyncMock()
    mock_user = {
        "email":"alfredoluis2601@gmail.com",
        "hash_password" :"$argon2id$v=19$m=65536,t=3,p=4$zBkjxPj/n3OulRLCOAdgjA$zmcyJjSZdI0qfyHiAnru3Bh8CzxT4ELpx5XfTiASyQA",
        "customer_id":1,
        "sign_up_date":"2026-07-09T22:45:30.123456+00:00",
        "last_update_at":"2026-07-09T22:45:30.123456+00:00",
        "is_verified":True,
        "role":"User"
    }
    repo.get_by_email.return_value = MagicMock(**mock_user)
    with (patch(f"{service_path}.generate_JWT") as mock_token, patch(f"{service_path}.get_password") as mock_password):
        mock_password.return_value = True
        mock_token.side_effect = ["access_token","refresh_token"]      
        response = await service.sign_in(user_info)
        assert response == {
        "message":"Login has been successfully done!",
        "access_token":"access_token",
        "refresh_token":"refresh_token",
        "token_type":"bearer"
       }
        repo.get_by_email.assert_called_once()
        repo.get_by_email.assert_called_once_with(user_info.email)

async def test_send_verify_email(get_service)->None:
    repo,service = get_service
    util_user_model = {
        "email":"mock_mail"
    }
    repo.save_verify_token = AsyncMock()
    with  patch(f"{service_path}.email_task_queue") as mock_task:
         response = await service.verify_account_email(MagicMock(**util_user_model))
         assert response == True
         repo.save_verify_token.assert_called_once()
         
async def test_verify_email(get_service)->None:
    repo,service = get_service 
    repo.get_by_token = AsyncMock()
    repo.activate_user = AsyncMock()
    gt_datetime = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(minutes=30)
    mock_user_info = {
        "expiry_token_time":gt_datetime
    }
    repo.get_by_token.return_value = MagicMock(**mock_user_info)
    fake_uuid_str = "12345678-1234-5678-1234-567812345678"
    response = await service.verify_account(fake_uuid_str)
    assert response == True
    repo.get_by_token.assert_called_once_with(UUID(fake_uuid_str))
           
async def test_password_reset_email(get_service)->None:
   repo,service = get_service
   repo.get_by_email = AsyncMock() 
   fake_email = "blob@gmail.com"
   repo.save_reset_token = AsyncMock()   
   with patch(f"{service_path}.email_task_queue") as mock_task:
       await service.password_reset_email(fake_email)
       repo.save_reset_token.assert_called_once()
       repo.get_by_email.assert_called_once_with(fake_email)
async def test_password_reset(get_service)->None:
   repo,service = get_service
   fake_uuid_str = "12345678-1234-5678-1234-567812345678"
   password_payload = {
       "new_password":"fake123",
       "confirm_new_password":"fake123"
   }
   mock_password_dto = MagicMock(**password_payload)
   repo.get_by_reset_token = AsyncMock()
   gt_datetime_now = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(minutes=30)
   mock_expiry_payload = {
       "expiry_reset_token_time":gt_datetime_now
   }
   mock_user_dto = MagicMock(**mock_expiry_payload)
   repo.get_by_reset_token.return_value = mock_user_dto
   repo.save_password = AsyncMock()
   with patch(f"{service_path}.get_hash") as mock_hashing:
       mock_hashing.return_value = "hashed123"
       await service.password_reset(mock_password_dto,fake_uuid_str)
       repo.get_by_reset_token.assert_called_once_with(fake_uuid_str)
       repo.save_password.assert_called_once_with(mock_user_dto,"hashed123")

#


