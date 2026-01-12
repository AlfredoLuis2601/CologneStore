from redis import asyncio
from .config_env import redis_host,redis_door   

token_black_list = asyncio.Redis(
   host=redis_host,
   port=redis_door,
   db=0
)




