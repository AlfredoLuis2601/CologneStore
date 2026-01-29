from sqlmodel.ext.asyncio.session import AsyncSession
from cologne.database import get_session,async_engine
from sqlmodel import SQLModel
from cologne.models import CustomersDB 
from cologne.utils import get_hash
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from cologne.config_env import password
import asyncio
async def create_Luis():
    print("oi")
    hash_password = get_hash(password)
    admin_information = {
        "email":"luisalfredoalvesdeandrade1010@gmail.com",
        "hash_password":hash_password,
        "role":"admin"
    }
    session = sessionmaker(
        bind=async_engine,
        autoflush=False,
        expire_on_commit=False,
        class_= AsyncSession
    )    
    async_session = session()
    admin = CustomersDB.model_validate(admin_information)
    async_session.add(admin)
    await async_session.commit()
    await async_session.refresh(admin)
    await async_session.close()

asyncio.run(create_Luis()) 



    
    