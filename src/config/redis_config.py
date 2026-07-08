from redis import asyncio
from src.config.config_env import redis_url

token_block_list = asyncio.from_url(redis_url)



