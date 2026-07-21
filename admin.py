from sqlmodel.ext.asyncio.session import AsyncSession
from src.config.database import async_engine
from src.auth.models import CustomersDB 
from src.auth.utils_security import get_hash
from sqlalchemy.orm import sessionmaker
from src.config.config_env import password
import asyncio
async def create_Luis():
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


    
    