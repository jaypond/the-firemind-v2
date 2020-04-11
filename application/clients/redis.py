import aioredis
import json
from typing import List, Dict
from async_property import async_cached_property

class Redis:
    """
    Client library for communicating with redis instance asynchronously
    :param host: Redis host
    :param db: Redis db
    :param port: Redis port
    """
    def __init__(self, host, db: int=0, port: int=6379):
        self.host = host
        self.db = db
        self.port = port

    @async_cached_property
    async def client(self):
        return await aioredis.create_redis_pool(
            f'redis://{self.host}:{self.port}/{self.db}'
        )
    
    async def get(self, key, default=None):
        client = await self.client
        return await client.get(key, encoding='utf-8') or default
    
    async def exists(self, key):
        client = await self.client
        return await client.exists(key)
    
    async def flushdb(self):
        client = await self.client
        return await client.flushdb()
    
    async def set(self, key, value):
        client = await self.client
        return await client.set(key, json.dumps(value))
