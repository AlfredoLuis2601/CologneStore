from src.auth.interface import UserRepoInterface
from src.shared.generic_repository import GenericSQLModelRepository
from src.auth.schemas import User,UserClient,UserUpdate,UserSignUp
from src.auth.models import CustomersDB
from pydantic import EmailStr
from sqlmodel import select
class AuthRepo(GenericSQLModelRepository[User,UserClient,int],UserRepoInterface):
    def __init__(self, session):
        super().__init__(session=session, cls_model=CustomersDB, cls_schema=User)
    
    async def add(self, user:UserSignUp):
        user_model = CustomersDB.model_validate(user)
        self.session.add(user_model)
        await self.session.commit()
        await self.session.refresh(user_model)
        return user_model
    async def get_by_email(self, email:EmailStr)->CustomersDB|None:
        command = select(CustomersDB).where(CustomersDB.email==email)
        result = await self.session.exec(command)
        user = result.first()
        return user
    async def get_by_token(self, token):
        command = select(CustomersDB).where(CustomersDB.token==token) #If it fails return None and call error handling
        result = await self.session.exec(command)
        user = result.first()
        return user
    async def get_by_reset_token(self,token):
        command = select(CustomersDB).where(CustomersDB.reset_password_token==token) #If it fails return None and call error handling
        result = await self.session.exec(command)
        user = result.first()
        return user
    async def activate_user(self, user):
        user.is_verified = True
        user.token = None
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
    async def save_verify_token(self, token, expiry_time, user):
        user.token = token
        user.expiry_token_time = expiry_time
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
    async def save_reset_token(self,token,expiry_time,user):
        user.reset_password_token = token
        user.expiry_reset_token_time = expiry_time
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return True
    async def save_password(self, user, new_password):
        user.hash_password = new_password
        user.reset_password_token = None
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

    
    