from sqlmodel import SQLModel,Column,Field,ForeignKey
import sqlalchemy.dialects.postgresql as pg
import uuid
from typing import Optional
from datetime import datetime 


class CustomersDB(SQLModel,table=True):
    __tablename__ = "Customers"
    customer_id:Optional[int] = Field(primary_key=True,default=None)
    email:str = Field(unique=True,index=True)
    hash_password:str = Field(index=True,exclude=True)
    token:uuid.UUID = Field(sa_column=Column(pg.UUID),default_factory=uuid.uuid4)
    expiry_token_time:Optional[datetime] = Field(sa_column=Column(pg.TIMESTAMP),default=None)
    role:Optional[str] = Field(sa_column=Column(pg.VARCHAR,nullable=False,server_default="User"),default="User")
    is_verified:bool = Field(default=False)
    sign_up_date:datetime = Field(default_factory=datetime.now,sa_column=Column(pg.TIMESTAMP))
    last_update_at:datetime = Field(default_factory=datetime.now,sa_column=Column(pg.TIMESTAMP))
    reset_password_token:str | None = Field(default=None)
    expiry_reset_token_time:Optional[datetime] = Field(sa_column=Column(pg.TIMESTAMP),default=None)