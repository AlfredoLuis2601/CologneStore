from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import create_engine,text,SQLModel
from sqlalchemy.exc import OperationalError 
from cologne.config_env import url_database
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from cologne.utils import get_hash
from cologne.config_env import password
import asyncio
from cologne.models import CustomersDB
async_engine = AsyncEngine(
    create_engine(
        url=url_database,
        echo=False
    )
)

async def start_db():
    try:
      async with async_engine.begin() as connect:
         print("Starting connection with the database.")
    except OperationalError as error:#OperationalError from sqlalchemy.exc handle all the operational database errors.
        print("Connection with the database failed.") 
    finally:
        print("Succesfull connection with the database.")                      
 
#Create my session class with sessionmaker in the get_session

async def get_session():
    Session = sessionmaker(
        bind=async_engine,
        expire_on_commit=False,
        class_=AsyncSession,
        autoflush=False
    )
    async with Session() as session: #Generator
        yield session #return de generators


       
