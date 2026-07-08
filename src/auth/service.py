from src.auth.interface import UserRepoInterface
from src.auth.schemas import User,UserClient,UserUpdate
from src.auth.models import CustomersDB
from typing import List
from datetime import datetime,timedelta,timezone
from src.config.config_env import standard_token_time,base_url,standard_expire_jwt
from src.tasks.background_tasks import email_task_queue
from src.config.redis_config import token_block_list
import uuid
from pydantic import EmailStr
from src.auth.utils_security import get_hash,get_password,generate_JWT
from uuid import UUID
from src.config.mail import PasswordReset
from src.config.error_handling import UserAlreadyExist,EmailTokenExpired,UserAlreadyVerified,UserNotFound,WrongPassword,InvalidToken


class AuthService():
    def __init__(self,user_repo_instance:UserRepoInterface):
       self.user_repo_instance = user_repo_instance
    async def sign_up(self,raw_user_info:UserClient)->CustomersDB:
       already_exist = await self.user_repo_instance.get_by_email(raw_user_info.email)
       if already_exist is None:
          user_info = raw_user_info.model_dump()
          user_info["hash_password"] = get_hash(raw_user_info.hash_password)
          response = await self.user_repo_instance.add(user_info)
          return response
       else:
          raise UserAlreadyExist()
    async def verify_account_email(self,user:CustomersDB)->bool:
       token = uuid.uuid4()
       expiry_token_time = timedelta(minutes=standard_token_time) + datetime.now(timezone.utc).replace(tzinfo=None)
       await self.user_repo_instance.save_verify_token(token,expiry_token_time,user)
       link = f"{base_url}/api/v1/cologne_store/users/validate_account/{str(token)}"
       subject = "Verify account"
       body = f"""<h1>Welcome to the Cologne Store Website!</h1>
             <p>To finish your sign up, click on the link</p>
             <a href="{link}">{link}</a>
          """
       email_task_queue.delay(subject,user.email,body)
       return True
    async def verify_account(self,key:str)->bool:
       time_now = datetime.now(timezone.utc).replace(tzinfo=None) 
       try:
        key_uuid = UUID(key)
       except ValueError:
         raise InvalidToken()
       user = await self.user_repo_instance.get_by_token(key_uuid)  
       if user is None:
          raise UserAlreadyVerified()
       elif user.expiry_token_time<time_now:
          raise EmailTokenExpired()
       await self.user_repo_instance.activate_user(user)
       return True
    async def sign_in(self,raw_user_info:UserClient)->dict:
       user = await self.user_repo_instance.get_by_email(raw_user_info.email)
       if user is None:
          raise UserNotFound
       correct_password = get_password(user.hash_password,raw_user_info.hash_password)
       if correct_password:
          access_token = generate_JWT(user_data={
                   "username":user.email,
                   "user_id":str(user.customer_id),
                   "role":user.role
               },is_refresh=False)
               
          refresh_token = generate_JWT(
                   user_data={
                       "username":user.email,
                       "user_id":user.customer_id,
                       "role":user.role
                   },expiration_time= timedelta(days=standard_expire_jwt),is_refresh=True
               )
          return {
                   "message":"Login has been successfully done!",
                   "access_token":access_token,
                   "refresh_token":refresh_token,
                   "token_type":"bearer"
               }
       else:
         raise WrongPassword() 
    async def get_users(self)->List[User]:
       users = await self.user_repo_instance.get_all()
       return users
    async def delete_user(self,id:int):
       response = await self.user_repo_instance.delete(id)
       if response:
          return True
       raise UserNotFound()
    async def new_access_token(self,token_data:dict)->dict:
       user_info = token_data.get("user_information")
       username = user_info.get("username")
       user_id = user_info.get("user_id")
       role = user_info.get("role")
       refresh_acess_token = generate_JWT(user_data={"username":username,"user_id":user_id,"role":role},is_refresh=False)
       return {
        "access_token":refresh_acess_token,
        "token_type":"bearer"
       }
    async def add_token_to_block_list(self,token_data:dict)->dict:
        exp = token_data.get("exp")
        jti = token_data.get("jti")
        time_now = datetime.now(timezone.utc).timestamp()  
        remaining_time = int(exp - time_now)
        await token_block_list.set(name=jti,ex=remaining_time,value="")  
        return {
           "status_code":200,
           "content":"Logout has been succesfully done!"
        }
    async def password_reset_email(self,email:EmailStr)->bool:
       user = await self.user_repo_instance.get_by_email(email)
       if user is None:
          return False
       token = str(uuid.uuid4())
       expiry_time = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(minutes=standard_token_time)
       await self.user_repo_instance.save_reset_token(token,expiry_time,user)
       link = f"{base_url}/change_password/{token}"
       body = f"""
         <h1>Password reset email</h1>
         <p>Hello dear customer, having trouble with your current password?</p>
         <p>Click on the link to change your password safely: <a href="{link}">{link}</a></p>
       """
       subject = "Password reset"
       email_task_queue.delay(subject,email,body)
       return True
    async def password_reset(self,password_info:PasswordReset,key:str)->bool:
       if password_info.confirm_new_password!=password_info.new_password:
          raise WrongPassword()
       user = await self.user_repo_instance.get_by_reset_token(key)
       time_now = datetime.now(timezone.utc).replace(tzinfo=None)
       if user is None:
          raise UserAlreadyVerified()   
       elif time_now> user.expiry_reset_token_time:
          raise EmailTokenExpired()
       hash_password = get_hash(password_info.new_password)
       await self.user_repo_instance.save_password(user,hash_password)
       return True
       
    
    
    
    
    
       


