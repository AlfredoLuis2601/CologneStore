from src.shared.generic_interface import GenericRepoInterface
from abc import abstractmethod
from src.auth.schemas import User,UserClient,UserUpdate,UserSignUp
from src.auth.models import CustomersDB
from pydantic import EmailStr
from uuid import UUID
from datetime import datetime
class UserRepoInterface(GenericRepoInterface[User,UserClient,int]):
    @abstractmethod
    async def add(self,user:UserSignUp)->CustomersDB:
        pass
    @abstractmethod
    async def get_by_email(self,email:EmailStr)->CustomersDB:
        pass
    @abstractmethod
    async def get_by_token(self,token:UUID)->CustomersDB:
        pass
    @abstractmethod
    async def get_by_reset_token(self,token:str)->CustomersDB:
        pass
    @abstractmethod
    async def activate_user(self,user:CustomersDB)->None:
        pass
    #Call get_by_token
    @abstractmethod
    async def save_verify_token(self,token:UUID,expiry_time:datetime,user:CustomersDB)->None:
      pass
    @abstractmethod
    async def save_reset_token(self,token:str,expiry_time:datetime,user:CustomersDB)->bool:
        pass
    @abstractmethod
    async def save_password(self,user:CustomersDB,new_password:str)->bool:
        pass