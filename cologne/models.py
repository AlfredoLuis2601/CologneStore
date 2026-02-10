from sqlmodel import SQLModel,Column,Field,ForeignKey
import sqlalchemy.dialects.postgresql as pg
import uuid
from typing import Optional
from datetime import datetime 
class CologneInformationDB(SQLModel,table=True):
    __tablename__ = "CologneInfo"
    uid:uuid.UUID = Field(sa_column=Column(pg.UUID,primary_key=True,nullable=False,unique=True),default_factory=uuid.uuid4)
    name:str = Field(index=True)
    brand:str = Field(index=True)
    type:str = Field(index=True)
    price:float = Field(nullable=False)
    amount:int = Field(default=0,ge=0)

class CustomersDB(SQLModel,table=True):
    __tablename__ = "Customers"
    customer_id:Optional[int] = Field(primary_key=True,default=None)
    email:str = Field(unique=True,index=True)
    hash_password:str = Field(index=True,exclude=True)
    token:uuid.UUID = Field(sa_column=Column(pg.UUID),default_factory=uuid.uuid4)
    expiry_token_time:Optional[datetime] = Field(sa_column=Column(pg.TIMESTAMP),default=None)
    role:Optional[str] = Field(sa_column=Column(pg.VARCHAR,nullable=False,default="User"))
    is_verified:bool = Field(default=False)
    sign_up_date:datetime = Field(default_factory=datetime.now,sa_column=Column(pg.TIMESTAMP))
    last_update_at:datetime = Field(default_factory=datetime.now,sa_column=Column(pg.TIMESTAMP))
    reset_password_token:str | None = Field(default=None)
    expiry_reset_token_time:Optional[datetime] = Field(sa_column=Column(pg.TIMESTAMP),default=None)
class SalesDB(SQLModel,table=True):
    __tablename__ = "Sales"
    sales_id:Optional[int] = Field(primary_key=True,default=None)
    customer_id:int = Field(foreign_key="Customers.customer_id",nullable=False,unique=False)
    uid:uuid.UUID = Field(foreign_key="CologneInfo.uid")
    amount_bought:int = Field(nullable=False,gt=0)
    price:float = Field(nullable=False) 
    sale_date:datetime = Field(default_factory=datetime.now,sa_column=Column(pg.TIMESTAMP))