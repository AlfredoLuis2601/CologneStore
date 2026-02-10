from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel,select
from fastapi.exceptions import HTTPException
from fastapi import status,Depends
from datetime import datetime,timedelta,timezone
from .models  import CologneInformationDB,CustomersDB,SalesDB
from src.cologne.schemas import CologneClient,UpdateCologne,Cologne,SaleClient,Sales
from src.auth.schemas import User,UserClient,UserUpdate
from src.auth.utils_security import get_hash,get_password
from src.auth.utils_security import generate_JWT
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from src.auth.user_dependencies import get_user_info
from src.auth.user_dependencies import token_bearer
import uuid
from src.tasks.redis_config import token_block_list
from src.config.error_handling import EmptyInventory,UserAlreadyExist,UserNotFound,TokenAlreadyInBlackList,InvalidToken,RefreshTokenToAccess,CologneNotFound,DeleteCologne,WrongPassword,RolePermission,GenerateRefresh
STANDARD_EXPIRATION_JWT_TIME = 2
STANDARD_TOKEN_EXPIRATION_TIME = 30
#CRUD requests:
#Funcao update_cologne_sale: Chama a funcao get_cologne para retornar a qtd em estoque e diminuir pela quantidade comprada
#passada como parametro.
class CologneCRUD():
    # Here, are the functions related to the cologneDB, not involving customers neither sales,they are related to the management
    #of the database.
   async def add_cologne(self,client_info:CologneClient,session:AsyncSession):
       new_cologne = CologneInformationDB.model_validate(client_info) #Validation from the table 
       session.add(new_cologne)
       await session.commit() 
       await session.refresh(new_cologne) 
       return new_cologne
   async def pick_colognes(self,session:AsyncSession):
       command = select(CologneInformationDB)
       result = await session.exec(command)
       colognes = result.all()
       if colognes is not None:
          return colognes
       else:
           None
   async def pick_cologne(self,cologne_name:str,session:AsyncSession):
       command = select(CologneInformationDB).where(CologneInformationDB.name==cologne_name)
       result = await session.exec(command)
       cologne = result.first()
       if cologne is not None:
           return cologne
       else:
           return None
       
   async def fresh_cologne(self,cologne_name:str,raw_update_info:UpdateCologne,session:AsyncSession):
       toBeUpdatedCologne = {}
       toBeUpdatedCologne = await self.pick_cologne(cologne_name,session)
       if toBeUpdatedCologne is not None:
           update_info = raw_update_info.model_dump()
           for k,v in update_info.items():
               setattr(toBeUpdatedCologne,k,v)
           session.add(toBeUpdatedCologne)
           await session.commit()
           await session.refresh(toBeUpdatedCologne)
           return toBeUpdatedCologne
       else:
           return None 
   async def delete_cologne(self,cologne_name:str,session:AsyncSession):
       to_be_deleted_cologne = await self.pick_cologne(cologne_name,session)
       if to_be_deleted_cologne is not None:
         await session.delete(to_be_deleted_cologne)
         await session.commit()
         return {"data":"Cologne has been removed from the database."}
       else:
           return None
   #All the None returns have to handled after in the routes.
   #Customers functions:
   async def load_users(self,session:AsyncSession):
       command = select(CustomersDB)
       result = await session.exec(command)
       users = result.all()
       if users:
           return users
       else:
           return None
   async def user_exists(self,email:str,session:AsyncSession):
       command = select(CustomersDB).where(CustomersDB.email==email)
       result = await session.exec(command)
       user = result.first()
       if user is not None:
           return user
       else:
           return None
   async def signUp(self,raw_user_data:UserClient,session:AsyncSession):
       #mudar esse password pelo verify
       user = await self.user_exists(raw_user_data.email,session)
       if user is None:
           raw_user_data.hash_password = get_hash(raw_user_data.hash_password)
           user_data = raw_user_data.model_dump()
           user_data["role"] = "User"
           user_data["expiry_token_time"] = timedelta(minutes=STANDARD_TOKEN_EXPIRATION_TIME) + datetime.now(timezone.utc).replace(tzinfo=None)
           new_user = CustomersDB.model_validate(user_data)
           session.add(new_user)
           await session.commit()
           await session.refresh(new_user)
           return new_user
       else:
           return None
   async def signIn(self,session:AsyncSession,raw_user_data:OAuth2PasswordRequestForm):
       email = raw_user_data.username
       user:User = await self.user_exists(email,session)
       if user is not None:
           is_password_correct = get_password(hash=user.hash_password,password=raw_user_data.password)
           if is_password_correct:
               acess_token = generate_JWT(user_data={
                   "username":user.email,
                   "user_id":str(user.customer_id),
                   "role":user.role
               },is_refresh=False)
               
               refresh_token = generate_JWT(
                   user_data={
                       "username":user.email,
                       "user_id":user.customer_id,
                       "role":user.role
                   },expiration_time= timedelta(days=STANDARD_EXPIRATION_JWT_TIME),is_refresh=True
               )
               return {
                   "message":"Login has been successfully done!",
                   "access_token":acess_token,
                   "refresh_token":refresh_token,
                   "token_type":"bearer"
               }
           else:
               return False
       else:
           raise UserNotFound()
    
   async def update_customer(self,raw_user_data:UserClient,raw_update_data:UserUpdate,session:AsyncSession):
        user_to_be_updated:User = await self.signIn(raw_user_data,session)
        if user_to_be_updated is not None:
            is_Unique = await self.user_exists(raw_update_data.email,session)
            if is_Unique is None:
                raw_update_data.hash_password = get_hash(raw_update_data.hash_password)
                update_information = raw_update_data.model_dump()
                for k,v in update_information.items():
                    setattr(user_to_be_updated,k,v)
                session.add(user_to_be_updated)
                await session.commit()
                await session.refresh(user_to_be_updated)
                return user_to_be_updated
            else:
                raise UserAlreadyExist()
        else:
            raise UserNotFound()
                
   async def delete_user(self,email:str,password:str,session:AsyncSession):
       deleted_user = await self.user_exists(email,password,session)
       if deleted_user is not None:
           await session.delete(deleted_user)
           await session.commit()
           return "User was succesfully deleted."
       else:
           return None
       

   async def check_inventory(self,cologne_name:str,amount:int,session:AsyncSession):
       command = select(CologneInformationDB.amount).where(CologneInformationDB.name==cologne_name)
       result = await session.exec(command)
       amount_in_stock = result.first()
       if amount_in_stock <amount:
           raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,detail="Amount in stock is lower than the desired quantity.")
   async def update_inventory(self,amount_bought:int,cologne:Cologne,session:AsyncSession):
       new_amount = cologne.amount - amount_bought
       cologne.amount = new_amount
       session.add(cologne)
       await session.commit()
       await session.refresh(cologne)
   async def purchase_process(self,raw_sale_data:SaleClient,session:AsyncSession):
       existent_cologne = await self.pick_cologne(raw_sale_data.cologne_name,session)
       if existent_cologne is not None:
          await self.check_inventory(existent_cologne.name,raw_sale_data.amountBought,session)
          command = select(CustomersDB.customer_id).where(raw_sale_data.email==CustomersDB.email)
          result = await session.exec(command)
          customer_id = result.first()
          if customer_id is not None:
              sales_information = {
                  "uid": existent_cologne.uid,"customer_id":customer_id,"amount_bought":raw_sale_data.amountBought,"price":existent_cologne.price,"sale_date": datetime.now()
              }
              sales_update_db = SalesDB.model_validate(sales_information)
              session.add(sales_update_db)
              await session.commit()
              await session.refresh(sales_update_db)
              await self.update_inventory(raw_sale_data.amountBought,existent_cologne,session)
              return True
          else:
              raise UserNotFound()
       else:
           raise CologneNotFound()
           
   async def add_access_token_blacklist(self,payload:dict):
       jti = payload.get("jti")
       exp = payload.get("exp")
       time_now = datetime.now(timezone.utc).timestamp()  
       remaining_time = exp - time_now
       await token_block_list.set(name=jti,ex=remaining_time,value="")  
       return JSONResponse(
           status_code=201,
           content={
               "message":"Logout has been successfully done!"
           }
       )
       
        

   