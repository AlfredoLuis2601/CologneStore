from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.exc import OperationalError 
from backend.src.config.config_env import DATABASE_URL
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
async_engine = create_async_engine(
    url=DATABASE_URL,
    echo=False
)

async def start_db():
    try:
      async with async_engine.begin() as connect:
         print("Starting connection with the database.")
    except OperationalError as error:
        print("Connection with the database failed.") 
    finally:
        print("Succesfull connection with the database.")                      
 


async def get_session():
    Session = sessionmaker(
        bind=async_engine,
        expire_on_commit=False,
        class_=AsyncSession,
        autoflush=False
    )
    async with Session() as session: 
        yield session 


       
