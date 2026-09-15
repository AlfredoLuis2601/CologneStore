from sqlmodel import SQLModel
import uuid
from datetime import datetime 
from sqlmodel import Column,Field
import sqlalchemy.dialects.postgresql as pg

class ItemDB(SQLModel, table= True):
    __tablename__ = "Items"
    item_id: uuid.UUID = Field(sa_column=Column(pg.UUID,primary_key=True,nullable=False,unique=True),default_factory=uuid.uuid4)
    uid: uuid.UUID = Field(foreign_key="CologneInfo.uid", nullable=False, unique=False)
    sales_id:int = Field(foreign_key="Sales.sales_id",unique=False, nullable=False)
    amount:int = Field(gt=0, nullable=False)
    delivery_date: datetime = Field(sa_column=Column(pg.TIMESTAMP)) 