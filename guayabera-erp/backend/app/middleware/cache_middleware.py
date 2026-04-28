"""
Cache Middleware: Implements caching for API responses and database queries
Optimizes performance by reducing redundant computations and database hits
"""

import hashlib
import json
import time
from typing import Callable, Any
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from fastapi import HTTPException

from app.services.cache_service import cache_service


class CacheMiddleware(BaseHTTPMiddleware):
    """
    Middleware to implement caching for API endpoints
    """
    
    def __init__(
        self, 
        app, 
        cache_ttl: int = 300,  # 5 minutes default TTL
        exclude_patterns: list = None
    ):
        super().__init__(app)
        self.cache_ttl = cache_ttl
        self.exclude_patterns = exclude_patterns or []
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip caching for POST, PUT, DELETE requests
        if request.method in ["POST", "PUT", "DELETE"]:
            return await call_next(request)
        
        # Check if path should be excluded from caching
        path = request.url.path
        for pattern in self.exclude_patterns:
            if pattern in path:
                return await call_next(request)
        
        # Create cache key based on path and query params
        query_string = str(sorted(request.query_params.items()))
        cache_key = self._generate_cache_key(path, query_string)
        
        # Try to get cached response
        cached_response = cache_service.get(cache_key)
        if cached_response:
            # Create response from cached data
            response_body = cached_response['body']
            headers = cached_response['headers']
            status_code = cached_response['status_code']
            
            # Create response with cached content
            response = Response(
                content=response_body,
                status_code=status_code,
                headers=headers
            )
            response.headers["X-Cache"] = "HIT"
            return response
        
        # Execute the request
        start_time = time.time()
        response = await call_next(request)
        processing_time = time.time() - start_time
        
        # Only cache successful responses
        if response.status_code == 200 and processing_time > 0.1:  # Only cache if processing took > 100ms
            # Read response body for caching
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk
            
            # Create new response since we consumed the body iterator
            response = Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
            
            # Add to cache
            cache_data = {
                "body": response_body.decode(),
                "headers": dict(response.headers),
                "status_code": response.status_code
            }
            cache_service.set_json(cache_key, cache_data, expire=self.cache_ttl)
            response.headers["X-Cache"] = "MISS"
        else:
            response.headers["X-Cache"] = "SKIP"
        
        return response
    
    def _generate_cache_key(self, path: str, query_string: str) -> str:
        """
        Generate a unique cache key based on path and query parameters
        """
        key_input = f"{path}:{query_string}"
        return f"api_cache:{hashlib.md5(key_input.encode()).hexdigest()}"


def get_cache_key_for_entity(entity_type: str, entity_id: str) -> str:
    """
    Generate a cache key for a specific entity
    :param entity_type: Type of entity (e.g., 'product', 'customer', 'invoice')
    :param entity_id: ID of the entity
    :return: Cache key for the entity
    """
    return f"entity:{entity_type}:{entity_id}"


def cache_entity(entity_type: str, entity_id: str, data: Any, ttl: int = 300) -> bool:
    """
    Cache a specific entity
    :param entity_type: Type of entity (e.g., 'product', 'customer', 'invoice')
    :param entity_id: ID of the entity
    :param data: Data to cache
    :param ttl: Time to live in seconds
    :return: True if cached successfully, False otherwise
    """
    cache_key = get_cache_key_for_entity(entity_type, entity_id)
    return cache_service.set_json(cache_key, data, expire=ttl)


def get_cached_entity(entity_type: str, entity_id: str) -> Any:
    """
    Get a cached entity
    :param entity_type: Type of entity (e.g., 'product', 'customer', 'invoice')
    :param entity_id: ID of the entity
    :return: Cached data if exists, None otherwise
    """
    cache_key = get_cache_key_for_entity(entity_type, entity_id)
    return cache_service.get_json(cache_key)


def invalidate_entity_cache(entity_type: str, entity_id: str) -> bool:
    """
    Invalidate cache for a specific entity
    :param entity_type: Type of entity (e.g., 'product', 'customer', 'invoice')
    :param entity_id: ID of the entity
    :return: True if invalidated successfully, False otherwise
    """
    cache_key = get_cache_key_for_entity(entity_type, entity_id)
    return cache_service.delete(cache_key)


def invalidate_pattern(pattern: str) -> int:
    """
    Invalidate all cache keys matching a pattern
    :param pattern: Pattern to match (supports Redis patterns)
    :return: Number of keys deleted
    """
    # Note: This implementation assumes direct Redis access
    # In production, you might want to use a more sophisticated approach
    try:
        # This is a simplified implementation - in production, 
        # you'd likely want to store keys in a set for easier pattern invalidation
        return 0  # Placeholder implementation
    except Exception as e:
        print(f"Error invalidating cache pattern {pattern}: {str(e)}")
        return 0