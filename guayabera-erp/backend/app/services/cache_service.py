"""
Cache Service: Redis caching for performance optimization
Improves response times for frequently accessed data
"""

import json
import redis
from typing import Optional, Any, Union
from datetime import timedelta
from app.core.config import settings


class CacheService:
    """
    Service class to handle Redis caching operations
    """
    
    def __init__(self):
        """
        Initialize Redis connection
        """
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=0,
            decode_responses=True,
            password=settings.REDIS_PASSWORD
        )
    
    def set(
        self, 
        key: str, 
        value: Any, 
        expire: Optional[Union[int, timedelta]] = None
    ) -> bool:
        """
        Set a value in cache
        :param key: Cache key
        :param value: Value to cache
        :param expire: Expiration time in seconds
        :return: True if successful, False otherwise
        """
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            else:
                value = str(value)
            
            if expire:
                return self.redis_client.setex(key, expire, value)
            else:
                return self.redis_client.set(key, value)
        except Exception as e:
            print(f"Error setting cache: {str(e)}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from cache
        :param key: Cache key
        :return: Value if exists, None otherwise
        """
        try:
            value = self.redis_client.get(key)
            if value is None:
                return None
            
            # Try to deserialize JSON, fall back to string
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        except Exception as e:
            print(f"Error getting cache: {str(e)}")
            return None
    
    def delete(self, key: str) -> bool:
        """
        Delete a key from cache
        :param key: Cache key
        :return: True if deleted, False otherwise
        """
        try:
            return bool(self.redis_client.delete(key))
        except Exception as e:
            print(f"Error deleting cache: {str(e)}")
            return False
    
    def exists(self, key: str) -> bool:
        """
        Check if a key exists in cache
        :param key: Cache key
        :return: True if exists, False otherwise
        """
        try:
            return bool(self.redis_client.exists(key))
        except Exception as e:
            print(f"Error checking cache existence: {str(e)}")
            return False
    
    def flush_all(self) -> bool:
        """
        Flush all keys in cache
        :return: True if successful, False otherwise
        """
        try:
            self.redis_client.flushall()
            return True
        except Exception as e:
            print(f"Error flushing cache: {str(e)}")
            return False
    
    def set_json(self, key: str, value: Any, expire: Optional[Union[int, timedelta]] = None) -> bool:
        """
        Set a JSON serializable value in cache
        :param key: Cache key
        :param value: JSON serializable value
        :param expire: Expiration time in seconds
        :return: True if successful, False otherwise
        """
        try:
            serialized_value = json.dumps(value, default=str)
            if expire:
                return self.redis_client.setex(key, expire, serialized_value)
            else:
                return self.redis_client.set(key, serialized_value)
        except Exception as e:
            print(f"Error setting JSON cache: {str(e)}")
            return False
    
    def get_json(self, key: str) -> Optional[Any]:
        """
        Get a JSON value from cache
        :param key: Cache key
        :return: Deserialized value if exists, None otherwise
        """
        try:
            value = self.redis_client.get(key)
            if value is None:
                return None
            
            return json.loads(value)
        except Exception as e:
            print(f"Error getting JSON cache: {str(e)}")
            return None


# Global instance
cache_service = CacheService()