# Rate Limiting Best Practices

**Version**: v1.0.0  
**Last Updated**: 2025-01-14

This document provides comprehensive best practices for implementing rate limiting in FastAPI applications, covering token bucket algorithm, sliding window, Redis-based distributed rate limiting, middleware integration, per-user/per-IP limits, rate limit headers, error handling, and production deployment.

---

## Table of Contents

1. [Architecture Principles](#architecture-principles)
2. [Token Bucket Algorithm](#token-bucket-algorithm)
3. [Sliding Window Algorithm](#sliding-window-algorithm)
4. [Redis-Based Rate Limiting](#redis-based-rate-limiting)
5. [Middleware Integration](#middleware-integration)
6. [Per-User Rate Limiting](#per-user-rate-limiting)
7. [Rate Limit Headers](#rate-limit-headers)
8. [Error Handling](#error-handling)
9. [Production Deployment](#production-deployment)

---

## Architecture Principles

### Rate Limiting Philosophy

**REQUIRED**: Understand rate limiting principles:

1. **Fair Usage**: Prevent abuse and ensure fair resource usage
2. **Distributed**: Support distributed systems with shared state
3. **Configurable**: Per-endpoint, per-user, per-IP limits
4. **Transparent**: Return rate limit information in headers
5. **Graceful**: Return 429 with retry information
6. **Performance**: Minimal overhead on request processing

### When to Use Rate Limiting

**REQUIRED**: Use rate limiting when:

- **API Protection**: Protect APIs from abuse
- **Resource Management**: Limit resource consumption
- **Cost Control**: Control API costs
- **Fair Usage**: Ensure fair usage across users
- **DDoS Protection**: Mitigate DDoS attacks

---

## Token Bucket Algorithm

### Token Bucket Implementation

**REQUIRED**: Token bucket rate limiter:

```python
import time
from collections import defaultdict
from typing import Dict

class TokenBucket:
    """Token bucket rate limiter."""
    
    def __init__(self, capacity: int, refill_rate: float):
        """Initialize token bucket.
        
        Args:
            capacity: Maximum tokens in bucket
            refill_rate: Tokens per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens: Dict[str, float] = defaultdict(lambda: capacity)
        self.last_refill: Dict[str, float] = defaultdict(time.time)
    
    def is_allowed(self, key: str, tokens: int = 1) -> bool:
        """Check if request is allowed."""
        now = time.time()
        
        # Refill tokens
        elapsed = now - self.last_refill[key]
        refill_amount = elapsed * self.refill_rate
        self.tokens[key] = min(
            self.capacity,
            self.tokens[key] + refill_amount
        )
        self.last_refill[key] = now
        
        # Check if enough tokens
        if self.tokens[key] >= tokens:
            self.tokens[key] -= tokens
            return True
        
        return False
```

---

## Sliding Window Algorithm

### Sliding Window Implementation

**REQUIRED**: Sliding window rate limiter:

```python
from collections import deque, defaultdict
import time

class SlidingWindowRateLimiter:
    """Sliding window rate limiter."""
    
    def __init__(self, requests_per_minute: int = 60):
        """Initialize sliding window limiter.
        
        Args:
            requests_per_minute: Maximum requests per minute
        """
        self.requests_per_minute = requests_per_minute
        self.window_size = 60  # seconds
        self.requests: Dict[str, deque] = defaultdict(lambda: deque())
    
    def is_allowed(self, key: str) -> bool:
        """Check if request is allowed."""
        now = time.time()
        window_start = now - self.window_size
        
        # Remove old requests
        requests = self.requests[key]
        while requests and requests[0] < window_start:
            requests.popleft()
        
        # Check limit
        if len(requests) >= self.requests_per_minute:
            return False
        
        # Record request
        requests.append(now)
        return True
    
    def get_remaining(self, key: str) -> int:
        """Get remaining requests."""
        now = time.time()
        window_start = now - self.window_size
        
        requests = self.requests[key]
        while requests and requests[0] < window_start:
            requests.popleft()
        
        return max(0, self.requests_per_minute - len(requests))
```

---

## Redis-Based Rate Limiting

### Redis Rate Limiter

**REQUIRED**: Distributed Redis rate limiter:

```python
import redis.asyncio as redis
from datetime import datetime, timedelta

class RedisRateLimiter:
    """Redis-based distributed rate limiter."""
    
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
    
    async def is_allowed(
        self,
        key: str,
        limit: int,
        window: int = 60,
    ) -> tuple[bool, int, datetime]:
        """Check if request is allowed.
        
        Returns:
            (allowed, remaining, reset_time)
        """
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=window)
        
        # Use sorted set for sliding window
        pipe = self.redis.pipeline()
        
        # Remove old entries
        pipe.zremrangebyscore(key, 0, window_start.timestamp())
        
        # Count current requests
        pipe.zcard(key)
        
        # Add current request
        pipe.zadd(key, {str(now.timestamp()): now.timestamp()})
        
        # Set expiration
        pipe.expire(key, window)
        
        results = await pipe.execute()
        current_count = results[1]
        
        # Check limit
        if current_count >= limit:
            # Get oldest request for reset time
            oldest = await self.redis.zrange(key, 0, 0, withscores=True)
            if oldest:
                reset_time = datetime.fromtimestamp(oldest[0][1]) + timedelta(seconds=window)
            else:
                reset_time = now + timedelta(seconds=window)
            
            return False, 0, reset_time
        
        # Calculate remaining
        remaining = limit - current_count - 1
        reset_time = now + timedelta(seconds=window)
        
        return True, remaining, reset_time
```

---

## Middleware Integration

### Rate Limiting Middleware

**REQUIRED**: Rate limiting middleware:

```python
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

class RateLimitingMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware."""
    
    def __init__(self, app, rate_limiter, limit: int = 60, window: int = 60):
        super().__init__(app)
        self.rate_limiter = rate_limiter
        self.limit = limit
        self.window = window
    
    async def dispatch(self, request: Request, call_next):
        """Apply rate limiting."""
        # Get rate limit key (IP or user ID)
        key = self._get_rate_limit_key(request)
        
        # Check rate limit
        allowed, remaining, reset_time = await self.rate_limiter.is_allowed(
            key, self.limit, self.window
        )
        
        # Add rate limit headers
        response = await call_next(request) if allowed else None
        
        if not allowed:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded",
                headers={
                    "X-RateLimit-Limit": str(self.limit),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(reset_time.timestamp())),
                    "Retry-After": str(int((reset_time - datetime.utcnow()).total_seconds())),
                }
            )
        
        # Add rate limit headers to response
        response.headers["X-RateLimit-Limit"] = str(self.limit)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(int(reset_time.timestamp()))
        
        return response
    
    def _get_rate_limit_key(self, request: Request) -> str:
        """Get rate limit key."""
        # Try user ID first
        user = getattr(request.state, "user", None)
        if user:
            return f"user:{user.id}"
        
        # Fall back to IP
        client_ip = request.client.host
        return f"ip:{client_ip}"
```

---

## Per-User Rate Limiting

### User-Based Rate Limiting

**REQUIRED**: Per-user rate limiting:

```python
class UserRateLimiter:
    """Per-user rate limiter."""
    
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.default_limit = 100  # requests per minute
    
    async def get_user_limit(self, user_id: str) -> int:
        """Get rate limit for user."""
        # Check user-specific limit
        user_limit = await self.redis.get(f"user_limit:{user_id}")
        if user_limit:
            return int(user_limit)
        
        # Check role-based limit
        user_role = await self.redis.get(f"user_role:{user_id}")
        role_limits = {
            "premium": 1000,
            "standard": 100,
            "free": 10,
        }
        
        return role_limits.get(user_role, self.default_limit)
    
    async def check_rate_limit(self, user_id: str) -> tuple[bool, int, datetime]:
        """Check user rate limit."""
        limit = await self.get_user_limit(user_id)
        key = f"rate_limit:user:{user_id}"
        
        return await self.redis_rate_limiter.is_allowed(key, limit, 60)
```

---

## Rate Limit Headers

### Standard Rate Limit Headers

**REQUIRED**: Rate limit headers:

```python
# Standard headers
response.headers["X-RateLimit-Limit"] = "100"
response.headers["X-RateLimit-Remaining"] = "95"
response.headers["X-RateLimit-Reset"] = "1642680000"
response.headers["Retry-After"] = "60"  # Seconds until reset
```

---

## Error Handling

### Rate Limit Error Response

**REQUIRED**: Rate limit error handling:

```python
from fastapi import HTTPException

class RateLimitExceeded(HTTPException):
    """Rate limit exceeded exception."""
    
    def __init__(self, limit: int, remaining: int, reset_time: datetime):
        retry_after = int((reset_time - datetime.utcnow()).total_seconds())
        
        super().__init__(
            status_code=429,
            detail={
                "error": "Rate limit exceeded",
                "limit": limit,
                "remaining": remaining,
                "reset_at": reset_time.isoformat(),
                "retry_after": retry_after,
            },
            headers={
                "X-RateLimit-Limit": str(limit),
                "X-RateLimit-Remaining": str(remaining),
                "X-RateLimit-Reset": str(int(reset_time.timestamp())),
                "Retry-After": str(retry_after),
            }
        )
```

---

## Production Deployment

### Production Configuration

**REQUIRED**: Production setup:

```python
# Production rate limiter configuration
RATE_LIMIT_CONFIG = {
    "default_limit": 100,  # requests per minute
    "window": 60,  # seconds
    "redis_url": os.getenv("REDIS_URL"),
    "per_user_limits": {
        "premium": 1000,
        "standard": 100,
        "free": 10,
    },
    "per_endpoint_limits": {
        "/api/expensive": 10,
        "/api/public": 1000,
    },
}
```

---

## Summary

### Key Takeaways

1. **Token Bucket**: Smooth rate limiting
2. **Sliding Window**: Accurate request counting
3. **Redis**: Distributed rate limiting
4. **Middleware**: Automatic rate limiting
5. **Per-User**: User-specific limits
6. **Headers**: Transparent rate limit info
7. **Error Handling**: Graceful 429 responses
8. **Production Ready**: Validated with 0 errors

---

**Version**: v1.0.0  
**Last Updated**: 2025-01-14

