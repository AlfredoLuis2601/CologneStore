from sqlmodel import SQLModel,Column,Field
import sqlalchemy.dialects.postgresql as pg
import uuid

class CologneInformationDB(SQLModel,table=True):
    __tablename__ = "CologneInfo"
    uid:uuid.UUID = Field(sa_column=Column(pg.UUID,primary_key=True,nullable=False,unique=True),default_factory=uuid.uuid4)
    name:str = Field(index=True)
    brand:str = Field(index=True)
    type:str = Field(index=True)
    price:float = Field(nullable=False)
    amount:int = Field(default=0,ge=0)

