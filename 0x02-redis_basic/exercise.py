#!/usr/bin/env python3
""" module: exercise """
import redis
import uuid
from typing import Union


class Cache:
    """
    Implements redis caching
    """
    def __init__(self):
        """ Constructor
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store element in cache"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key


if __name__ == "__main__":
    """ Execute if main module"""
    cache = Cache()
    data = b"hello"
    key = cache.store(data)
    print(key)

    local_redis = redis.Redis()
    print(local_redis.get(key))
