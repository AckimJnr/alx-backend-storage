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

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis.

        Args:
            key (str): The key under which the data is stored.
            fn (Callable, optional): A conversion function to apply to
            the retrieved data.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved data,
            possibly transformed by the conversion function.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            try:
                return fn(data)
            except ValueError:
                raise ValueError("Failed to convert data to the desired format")
        return data

    def get_str(self, key: str) -> Union[str, bytes, None]:
        """
        Retrieve data from Redis and decode it to a UTF-8 string.

        Args:
            key (str): The key under which the data is stored.

        Returns:
            Union[str, bytes, None]: The retrieved data as a UTF-8 string.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieve data from Redis and convert it to an integer.

        Args:
            key (str): The key under which the data is stored.

        Returns:
            Union[int, None]: The retrieved data as an integer.
        """
        return self.get(key, fn=lambda d: int(d))


if __name__ == "__main__":
    """ Execute if main module"""
    cache = Cache()
    data = b"hello"
    key = cache.store(data)
    print(key)

    local_redis = redis.Redis()
    print(local_redis.get(key))
