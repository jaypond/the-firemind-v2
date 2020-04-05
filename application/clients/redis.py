import redis
from typing import List, Dict


class Redis:
    """
    Client library for communicating with redis instance.
    
    :param host: Redis host
    :param db: Redis db
    :param port: Redis port
    """
    def __init__(host, db: int=0, port: int=6379):
        self.host = host
        self.db = db
        self.port = port
    
    @property
    def client(self):
        return redis.StrictRedis(
            host=self.host,
            db=self.db,
            port=self.port
        )
    
    def get(self, key, default=None):
        return self.client.get(key) or default
    
    def set(self, key, value):
        return self.client.set(key, value)
