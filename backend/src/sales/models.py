from sqlmodel import SQLModel,Column,Field,ForeignKey
import sqlalchemy.dialects.postgresql as pg
import uuid
from typing import Optional
from datetime import datetime 


class SalesDB(SQLModel,table=True):
    __tablename__ = "Sales"
    sales_id:Optional[int] = Field(primary_key=True,default=None)
    customer_id:int = Field(foreign_key="Customers.customer_id",nullable=False,unique=False)
    uid:uuid.UUID = Field(foreign_key="CologneInfo.uid")
    amount_bought:int = Field(nullable=False,gt=0)
    price:float = Field(nullable=False) 
    sale_date:datetime = Field(default_factory=datetime.now,sa_column=Column(pg.TIMESTAMP))