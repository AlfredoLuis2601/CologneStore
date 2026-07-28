from redis import asyncio
from backend.src.config.config_env import redis_url

token_block_list = asyncio.from_url(redis_url)



