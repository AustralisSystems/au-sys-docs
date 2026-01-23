# Error Handling & Resilience Patterns Best Practices

**Version**: v1.0.0  
**Last Updated**: 2025-01-14

This document provides comprehensive best practices for implementing error handling and resilience patterns in FastAPI applications, covering exception handling, retry strategies, circuit breakers, timeout management, fallback mechanisms, graceful degradation, and comprehensive error recovery.

---

## Table of Contents

1. [Architecture Principles](#architecture-principles)
2. [Exception Handling Patterns](#exception-handling-patterns)
3. [Retry Strategies](#retry-strategies)
4. [Circuit Breaker Pattern](#circuit-breaker-pattern)
5. [Timeout Management](#timeout-management)
6. [Fallback Mechanisms](#fallback-mechanisms)
7. [Graceful Degradation](#graceful-degradation)
8. [Error Classification & Recovery](#error-classification--recovery)
9. [FastAPI Integration](#fastapi-integration)
10. [Monitoring & Observability](#monitoring--observability)
11. [Performance Considerations](#performance-considerations)
12. [Production Deployment](#production-deployment)

---

## Architecture Principles

### Fail-Fast Principle

**MANDATORY**: Fail fast to prevent cascading failures:

```python
from fastapi import HTTPException, status

async def validate_request(data: dict) -> None:
    """Fail fast on invalid input."""
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request body is required"
        )
    
    if "required_field" not in data:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Missing required field: required_field"
        )
```

### Defense in Depth

**REQUIRED**: Implement multiple layers of error handling:

```python
class ResilientService:
    """Service with multiple error handling layers."""
    
    def __init__(self):
        self.circuit_breaker = CircuitBreaker()
        self.retry_handler = RetryHandler()
        self.fallback_handler = FallbackHandler()
    
    async def process_request(self, request: dict) -> dict:
        """Process with multiple resilience layers."""
        # Layer 1: Input validation (fail fast)
        self._validate_input(request)
        
        # Layer 2: Circuit breaker check
        if not self.circuit_breaker.can_execute():
            return await self.fallback_handler.handle(request)
        
        # Layer 3: Retry with exponential backoff
        try:
            return await self.retry_handler.execute(
                lambda: self._execute_request(request)
            )
        except Exception as e:
            # Layer 4: Fallback on failure
            return await self.fallback_handler.handle(request, error=e)
```

### Error Isolation

**REQUIRED**: Isolate errors to prevent propagation:

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def error_isolation_context(operation: str):
    """Isolate errors to prevent cascading failures."""
    try:
        yield
    except Exception as e:
        # Log error but don't propagate
        logger.error(f"Error in {operation}: {e}", exc_info=True)
        # Return safe default or raise specific error
        raise IsolatedError(f"Operation {operation} failed: {e}")

# Usage
async def process_data(data: dict) -> dict:
    async with error_isolation_context("data_processing"):
        # Process data
        return await expensive_operation(data)
```

---

## Exception Handling Patterns

### Custom Exception Hierarchy

**REQUIRED**: Define a clear exception hierarchy:

```python
class ApplicationError(Exception):
    """Base exception for all application errors."""
    
    def __init__(self, message: str, status_code: int = 500, **kwargs):
        self.message = message
        self.status_code = status_code
        self.context = kwargs
        super().__init__(self.message)

class ValidationError(ApplicationError):
    """Validation error."""
    
    def __init__(self, message: str, field: str = None, **kwargs):
        super().__init__(
            message,
            status_code=400,
            field=field,
            **kwargs
        )

class NotFoundError(ApplicationError):
    """Resource not found error."""
    
    def __init__(self, resource_type: str, resource_id: str, **kwargs):
        super().__init__(
            f"{resource_type} '{resource_id}' not found",
            status_code=404,
            resource_type=resource_type,
            resource_id=resource_id,
            **kwargs
        )

class ServiceUnavailableError(ApplicationError):
    """Service unavailable error."""
    
    def __init__(self, service_name: str, **kwargs):
        super().__init__(
            f"Service '{service_name}' is temporarily unavailable",
            status_code=503,
            service_name=service_name,
            **kwargs
        )

class TimeoutError(ApplicationError):
    """Timeout error."""
    
    def __init__(self, operation: str, timeout: float, **kwargs):
        super().__init__(
            f"Operation '{operation}' timed out after {timeout}s",
            status_code=504,
            operation=operation,
            timeout=timeout,
            **kwargs
        )
```

### Exception Context Enrichment

**RECOMMENDED**: Enrich exceptions with context:

```python
from typing import Dict, Any
import traceback

class EnrichedException(Exception):
    """Exception with enriched context."""
    
    def __init__(
        self,
        message: str,
        context: Dict[str, Any] = None,
        cause: Exception = None
    ):
        self.message = message
        self.context = context or {}
        self.cause = cause
        self.traceback = traceback.format_exc() if cause else None
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary."""
        return {
            "message": self.message,
            "context": self.context,
            "cause": str(self.cause) if self.cause else None,
            "traceback": self.traceback,
        }

# Usage
try:
    result = await external_service.call()
except Exception as e:
    raise EnrichedException(
        "Failed to call external service",
        context={
            "service": "external_service",
            "operation": "call",
            "timestamp": datetime.now().isoformat(),
        },
        cause=e
    )
```

### Exception Handler Registration

**REQUIRED**: Register global exception handlers:

```python
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()

@app.exception_handler(ApplicationError)
async def application_error_handler(
    request: Request,
    exc: ApplicationError
) -> JSONResponse:
    """Handle application errors."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.message,
                "type": exc.__class__.__name__,
                "context": exc.context,
            }
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_error_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    """Handle validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "message": "Validation error",
                "type": "ValidationError",
                "details": exc.errors(),
            }
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    """Handle unexpected exceptions."""
    logger.exception("Unexpected error", exc_info=exc)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "message": "Internal server error",
                "type": "InternalError",
            }
        }
    )
```

---

## Retry Strategies

### Basic Retry with Tenacity

**REQUIRED**: Use Tenacity for retry logic:

```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    retry_if_result,
    before_sleep_log,
    after_log,
)
import logging

logger = logging.getLogger(__name__)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type((ConnectionError, TimeoutError)),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    after=after_log(logger, logging.ERROR),
    reraise=True
)
async def fetch_data(url: str) -> dict:
    """Fetch data with retry logic."""
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=10.0)
        response.raise_for_status()
        return response.json()
```

### Retry with Stop Conditions

**RECOMMENDED**: Combine multiple stop conditions:

```python
from tenacity import (
    retry,
    stop_after_attempt,
    stop_after_delay,
    stop_before_delay,
)

# Stop after 5 attempts OR 30 seconds
@retry(
    stop=(stop_after_attempt(5) | stop_after_delay(30)),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
async def operation_with_time_limit():
    """Operation with time and attempt limits."""
    pass

# Stop before exceeding 60 seconds
@retry(
    stop=stop_before_delay(60),
    wait=wait_exponential(multiplier=1, min=1, max=10)
)
async def operation_with_strict_time_limit():
    """Operation that must complete within time limit."""
    pass
```

### Retry with Wait Strategies

**REQUIRED**: Use appropriate wait strategies:

```python
from tenacity import (
    retry,
    wait_fixed,
    wait_random,
    wait_exponential,
    wait_random_exponential,
    wait_chain,
)

# Fixed wait
@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2)  # Wait 2 seconds between retries
)
async def fixed_wait_retry():
    pass

# Random wait (prevents thundering herd)
@retry(
    stop=stop_after_attempt(3),
    wait=wait_random(min=1, max=3)  # Random 1-3 seconds
)
async def random_wait_retry():
    pass

# Exponential backoff
@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=4, max=10)
    # Wait 4s, 8s, 10s, 10s, 10s
)
async def exponential_backoff_retry():
    pass

# Exponential backoff with jitter
@retry(
    stop=stop_after_attempt(5),
    wait=wait_random_exponential(multiplier=1, max=60)
    # Random wait up to 2^x seconds, capped at 60s
)
async def exponential_jitter_retry():
    pass

# Chained wait strategy
@retry(
    stop=stop_after_attempt(10),
    wait=wait_chain(
        *[wait_fixed(3) for _ in range(3)] +  # 3s for first 3 attempts
        [wait_fixed(7) for _ in range(2)] +   # 7s for next 2 attempts
        [wait_fixed(9)]                        # 9s for remaining attempts
    )
)
async def chained_wait_retry():
    pass
```

### Retry with Condition Checks

**RECOMMENDED**: Retry based on result conditions:

```python
from tenacity import (
    retry,
    retry_if_result,
    retry_if_exception_type,
    retry_if_not_exception_type,
)

def is_none(value):
    """Check if value is None."""
    return value is None

# Retry if result is None
@retry(
    stop=stop_after_attempt(3),
    retry=retry_if_result(is_none)
)
async def retry_on_none_result():
    """Retry if function returns None."""
    result = await fetch_data()
    return result if result else None

# Retry on specific exceptions
@retry(
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type((ConnectionError, TimeoutError))
)
async def retry_on_connection_errors():
    """Retry only on connection/timeout errors."""
    pass

# Retry on all exceptions except specific ones
@retry(
    stop=stop_after_attempt(3),
    retry=retry_if_not_exception_type(ValueError)
)
async def retry_except_value_error():
    """Retry on all errors except ValueError."""
    pass

# Combine multiple retry conditions
@retry(
    stop=stop_after_attempt(5),
    retry=(
        retry_if_exception_type(ConnectionError) |
        retry_if_result(is_none)
    )
)
async def retry_on_multiple_conditions():
    """Retry on connection errors OR None result."""
    pass
```

### Async Retry with Tenacity

**REQUIRED**: Use AsyncRetrying for async operations:

```python
from tenacity import AsyncRetrying, RetryError, stop_after_attempt

async def async_operation_with_retry():
    """Async operation with retry logic."""
    try:
        async for attempt in AsyncRetrying(stop=stop_after_attempt(3)):
            with attempt:
                result = await external_service.call()
                if result is None:
                    raise ValueError("Result is None")
                return result
    except RetryError as e:
        logger.error(f"Operation failed after retries: {e}")
        raise
```

### Retry Statistics

**RECOMMENDED**: Track retry statistics:

```python
from tenacity import retry, stop_after_attempt

@retry(stop=stop_after_attempt(3))
async def tracked_operation():
    """Operation with retry statistics tracking."""
    pass

# Access statistics
try:
    await tracked_operation()
except Exception:
    stats = tracked_operation.retry.statistics
    logger.info(f"Retry statistics: {stats}")
    # Statistics include:
    # - attempt_number: Number of attempts made
    # - outcome: Result of last attempt
    # - start_time: When retrying started
    # - etc.
```

---

## Circuit Breaker Pattern

### Basic Circuit Breaker Implementation

**REQUIRED**: Implement circuit breaker pattern:

```python
from enum import Enum
import time
from typing import Callable, Optional
import asyncio

class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing fast
    HALF_OPEN = "half_open"  # Testing recovery

class CircuitBreaker:
    """Circuit breaker implementation."""
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        success_threshold: int = 2,
        expected_exception: type = Exception,
    ):
        """Initialize circuit breaker.
        
        Args:
            failure_threshold: Number of failures before opening
            recovery_timeout: Seconds before attempting recovery
            success_threshold: Successes needed to close from half-open
            expected_exception: Exception type to track
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold
        self.expected_exception = expected_exception
        
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[float] = None
        self.state = CircuitState.CLOSED
        self._lock = asyncio.Lock()
    
    def can_execute(self) -> bool:
        """Check if circuit breaker allows execution."""
        async with self._lock:
            if self.state == CircuitState.CLOSED:
                return True
            
            elif self.state == CircuitState.OPEN:
                # Check if recovery timeout has passed
                if (
                    self.last_failure_time and
                    time.time() - self.last_failure_time >= self.recovery_timeout
                ):
                    self.state = CircuitState.HALF_OPEN
                    self.success_count = 0
                    return True
                return False
            
            else:  # HALF_OPEN
                return True
    
    def record_success(self) -> None:
        """Record successful execution."""
        async with self._lock:
            self.failure_count = 0
            
            if self.state == CircuitState.HALF_OPEN:
                self.success_count += 1
                if self.success_count >= self.success_threshold:
                    self.state = CircuitState.CLOSED
                    self.success_count = 0
    
    def record_failure(self) -> None:
        """Record failed execution."""
        async with self._lock:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.state == CircuitState.HALF_OPEN:
                # Any failure in half-open state opens circuit
                self.state = CircuitState.OPEN
                self.success_count = 0
            
            elif self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
    
    async def call(self, func: Callable, *args, **kwargs):
        """Execute function with circuit breaker protection."""
        if not self.can_execute():
            raise CircuitBreakerOpenError(
                f"Circuit breaker is OPEN (failures: {self.failure_count})"
            )
        
        try:
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
            
            self.record_success()
            return result
        
        except self.expected_exception as e:
            self.record_failure()
            raise
```

### Circuit Breaker Decorator

**RECOMMENDED**: Use circuit breaker as decorator:

```python
from functools import wraps
from typing import Callable

def circuit_breaker(
    failure_threshold: int = 5,
    recovery_timeout: int = 60,
    success_threshold: int = 2,
    expected_exception: type = Exception,
):
    """Circuit breaker decorator."""
    
    breaker = CircuitBreaker(
        failure_threshold=failure_threshold,
        recovery_timeout=recovery_timeout,
        success_threshold=success_threshold,
        expected_exception=expected_exception,
    )
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            return await breaker.call(func, *args, **kwargs)
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            return breaker.call(func, *args, **kwargs)
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator

# Usage
@circuit_breaker(failure_threshold=5, recovery_timeout=60)
async def external_service_call():
    """Call external service with circuit breaker."""
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
        response.raise_for_status()
        return response.json()
```

### Circuit Breaker with PyBreaker

**RECOMMENDED**: Use pybreaker library:

```python
import pybreaker

# Create circuit breaker
db_breaker = pybreaker.CircuitBreaker(
    fail_max=5,              # Open after 5 failures
    reset_timeout=60,        # Try recovery after 60 seconds
    success_threshold=2,     # Need 2 successes to close
    exclude=[ValueError],    # Don't count ValueError as failure
)

# Use as decorator
@db_breaker
async def database_operation():
    """Database operation with circuit breaker."""
    return await db.execute_query()

# Use as context manager
async def database_operation_context():
    """Database operation with context manager."""
    with db_breaker.calling():
        return await db.execute_query()

# Use with call() method
async def database_operation_call():
    """Database operation with call method."""
    return db_breaker.call_async(db.execute_query)

# Monitor state
print(db_breaker.current_state)  # 'closed', 'open', or 'half-open'
print(db_breaker.fail_counter)   # Current failure count
print(db_breaker.success_counter)  # Current success count
```

### Circuit Breaker with Redis Storage

**RECOMMENDED**: Use Redis for distributed circuit breakers:

```python
import pybreaker
import redis

# Redis connection
redis_client = redis.StrictRedis()

# Circuit breaker with Redis storage
db_breaker = pybreaker.CircuitBreaker(
    fail_max=5,
    reset_timeout=60,
    state_storage=pybreaker.CircuitRedisStorage(
        pybreaker.STATE_CLOSED,
        redis_client,
        namespace='database_service'
    )
)

# Multiple services can share circuit breaker state
api_breaker = pybreaker.CircuitBreaker(
    fail_max=5,
    reset_timeout=60,
    state_storage=pybreaker.CircuitRedisStorage(
        pybreaker.STATE_CLOSED,
        redis_client,
        namespace='api_service'  # Different namespace
    )
)
```

### Circuit Breaker Listeners

**RECOMMENDED**: Add listeners for monitoring:

```python
import pybreaker
import logging

logger = logging.getLogger(__name__)

class CircuitBreakerListener(pybreaker.CircuitBreakerListener):
    """Listener for circuit breaker events."""
    
    def state_change(self, cb, old_state, new_state):
        """Called when circuit breaker state changes."""
        logger.warning(
            f"Circuit breaker '{cb.name}' state changed: {old_state} -> {new_state}"
        )
    
    def failure(self, cb, exc):
        """Called when a failure occurs."""
        logger.error(
            f"Circuit breaker '{cb.name}' recorded failure: {exc}",
            exc_info=exc
        )
    
    def success(self, cb):
        """Called when a success occurs."""
        logger.debug(f"Circuit breaker '{cb.name}' recorded success")
    
    def before_call(self, cb, func, *args, **kwargs):
        """Called before function execution."""
        logger.debug(f"Circuit breaker '{cb.name}' calling {func.__name__}")

# Create circuit breaker with listener
db_breaker = pybreaker.CircuitBreaker(
    fail_max=5,
    reset_timeout=60,
    listeners=[CircuitBreakerListener()]
)
```

---

## Timeout Management

### HTTP Timeout Configuration

**REQUIRED**: Configure timeouts for HTTP requests:

```python
import httpx

# Granular timeout configuration
timeout = httpx.Timeout(
    connect=5.0,   # Time to establish connection
    read=10.0,     # Time to read response data
    write=5.0,     # Time to send request data
    pool=5.0       # Time to acquire connection from pool
)

# Client with default timeout
client = httpx.AsyncClient(timeout=timeout)

# Request-specific timeout
response = await client.get(
    'https://api.example.com/data',
    timeout=httpx.Timeout(30.0)  # Override for this request
)

# Handle timeout exceptions
try:
    response = await client.get('https://api.example.com/data', timeout=5.0)
except httpx.ConnectTimeout:
    logger.error("Connection timeout")
except httpx.ReadTimeout:
    logger.error("Read timeout")
except httpx.WriteTimeout:
    logger.error("Write timeout")
except httpx.PoolTimeout:
    logger.error("Pool timeout")
except httpx.TimeoutException:
    logger.error("Generic timeout")
```

### Operation Timeout with asyncio

**REQUIRED**: Use asyncio.wait_for for operation timeouts:

```python
import asyncio
from typing import TypeVar, Awaitable

T = TypeVar('T')

async def with_timeout(
    coro: Awaitable[T],
    timeout: float,
    timeout_error: Exception = None
) -> T:
    """Execute coroutine with timeout."""
    try:
        return await asyncio.wait_for(coro, timeout=timeout)
    except asyncio.TimeoutError:
        if timeout_error:
            raise timeout_error
        raise TimeoutError(f"Operation timed out after {timeout}s")

# Usage
try:
    result = await with_timeout(
        expensive_operation(),
        timeout=30.0,
        timeout_error=TimeoutError("Operation exceeded 30s")
    )
except TimeoutError as e:
    logger.error(f"Timeout: {e}")
    # Handle timeout
```

### Context Manager Timeout

**RECOMMENDED**: Use context manager for timeout:

```python
from contextlib import asynccontextmanager
import asyncio

@asynccontextmanager
async def timeout_context(timeout: float):
    """Context manager for operation timeout."""
    try:
        yield
    except asyncio.TimeoutError:
        raise TimeoutError(f"Operation timed out after {timeout}s")

# Usage
async def operation_with_timeout():
    async with timeout_context(30.0):
        await long_running_operation()
```

### Timeout Decorator

**RECOMMENDED**: Create timeout decorator:

```python
from functools import wraps
from typing import Callable

def timeout(seconds: float):
    """Timeout decorator."""
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            return await asyncio.wait_for(
                func(*args, **kwargs),
                timeout=seconds
            )
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            # For sync functions, run in executor
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(
                asyncio.wait_for(
                    asyncio.to_thread(func, *args, **kwargs),
                    timeout=seconds
                )
            )
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator

# Usage
@timeout(30.0)
async def timed_operation():
    """Operation with 30 second timeout."""
    await long_running_task()
```

---

## Fallback Mechanisms

### Fallback Function Pattern

**REQUIRED**: Implement fallback functions:

```python
from typing import Callable, Optional, TypeVar

T = TypeVar('T')

class FallbackHandler:
    """Handler for fallback mechanisms."""
    
    def __init__(self, fallback_func: Optional[Callable] = None):
        self.fallback_func = fallback_func
    
    async def execute_with_fallback(
        self,
        primary_func: Callable[[], Awaitable[T]],
        fallback_func: Optional[Callable[[], Awaitable[T]]] = None
    ) -> T:
        """Execute primary function with fallback."""
        fallback = fallback_func or self.fallback_func
        
        try:
            return await primary_func()
        except Exception as e:
            logger.warning(f"Primary operation failed: {e}, using fallback")
            
            if fallback:
                try:
                    return await fallback()
                except Exception as fallback_error:
                    logger.error(f"Fallback also failed: {fallback_error}")
                    raise FallbackError(
                        "Both primary and fallback operations failed",
                        primary_error=e,
                        fallback_error=fallback_error
                    )
            else:
                raise

# Usage
async def get_user_data(user_id: int) -> dict:
    """Get user data with fallback."""
    handler = FallbackHandler()
    
    return await handler.execute_with_fallback(
        primary_func=lambda: fetch_from_database(user_id),
        fallback_func=lambda: fetch_from_cache(user_id)
    )
```

### Fallback Chain Pattern

**RECOMMENDED**: Implement fallback chain:

```python
from typing import List, Callable, TypeVar

T = TypeVar('T')

class FallbackChain:
    """Fallback chain for multiple fallback options."""
    
    def __init__(self, fallbacks: List[Callable[[], Awaitable[T]]]):
        self.fallbacks = fallbacks
    
    async def execute(self) -> T:
        """Execute fallback chain."""
        last_error = None
        
        for i, fallback in enumerate(self.fallbacks):
            try:
                return await fallback()
            except Exception as e:
                logger.warning(
                    f"Fallback {i+1}/{len(self.fallbacks)} failed: {e}"
                )
                last_error = e
                continue
        
        raise FallbackChainExhaustedError(
            f"All {len(self.fallbacks)} fallbacks failed",
            last_error=last_error
        )

# Usage
async def get_data_with_chain() -> dict:
    """Get data with fallback chain."""
    chain = FallbackChain([
        lambda: fetch_from_primary_db(),
        lambda: fetch_from_replica_db(),
        lambda: fetch_from_cache(),
        lambda: get_default_data(),
    ])
    
    return await chain.execute()
```

### Fallback with Caching

**RECOMMENDED**: Use cache as fallback:

```python
class CachedFallback:
    """Fallback that uses cached data."""
    
    def __init__(self, cache_backend: Any):
        self.cache = cache_backend
    
    async def get_with_cache_fallback(
        self,
        key: str,
        fetch_func: Callable[[], Awaitable[Any]],
        ttl: int = 3600
    ) -> Any:
        """Get data with cache fallback."""
        # Try cache first
        cached_value = await self.cache.get(key)
        if cached_value is not None:
            return cached_value
        
        # Try primary source
        try:
            value = await fetch_func()
            # Cache for future use
            await self.cache.set(key, value, ttl=ttl)
            return value
        except Exception as e:
            logger.error(f"Primary fetch failed: {e}")
            
            # Try stale cache as fallback
            stale_value = await self.cache.get(key, allow_stale=True)
            if stale_value is not None:
                logger.warning(f"Using stale cache for {key}")
                return stale_value
            
            raise
```

---

## Graceful Degradation

### Feature Degradation Pattern

**RECOMMENDED**: Implement graceful feature degradation:

```python
from enum import Enum
from typing import Optional

class ServiceLevel(Enum):
    """Service degradation levels."""
    FULL = "full"              # All features available
    DEGRADED = "degraded"      # Some features disabled
    MINIMAL = "minimal"        # Only essential features
    OFFLINE = "offline"        # Service unavailable

class DegradableService:
    """Service with graceful degradation."""
    
    def __init__(self):
        self.service_level = ServiceLevel.FULL
        self.feature_flags = {
            "advanced_search": True,
            "real_time_updates": True,
            "analytics": True,
        }
    
    async def get_data(self, use_advanced: bool = True) -> dict:
        """Get data with degradation support."""
        # Check if advanced features are available
        if use_advanced and not self.feature_flags.get("advanced_search"):
            logger.info("Advanced search unavailable, using basic search")
            return await self._basic_search()
        
        try:
            return await self._advanced_search()
        except Exception as e:
            logger.warning(f"Advanced search failed: {e}, degrading to basic")
            self.feature_flags["advanced_search"] = False
            return await self._basic_search()
    
    def enable_degraded_mode(self) -> None:
        """Enable degraded mode."""
        self.service_level = ServiceLevel.DEGRADED
        self.feature_flags["advanced_search"] = False
        self.feature_flags["real_time_updates"] = False
        logger.info("Service degraded: advanced features disabled")
    
    def enable_minimal_mode(self) -> None:
        """Enable minimal mode."""
        self.service_level = ServiceLevel.MINIMAL
        for feature in self.feature_flags:
            self.feature_flags[feature] = False
        logger.warning("Service in minimal mode: only essential features")
```

### Response Degradation Pattern

**RECOMMENDED**: Degrade response quality:

```python
class ResponseDegradation:
    """Response degradation handler."""
    
    async def get_user_profile(
        self,
        user_id: int,
        include_details: bool = True
    ) -> dict:
        """Get user profile with degradation."""
        try:
            # Try full profile
            if include_details:
                return await self._get_full_profile(user_id)
            else:
                return await self._get_basic_profile(user_id)
        
        except Exception as e:
            logger.warning(f"Failed to get profile: {e}, using minimal")
            
            # Degrade to minimal profile
            return {
                "id": user_id,
                "status": "available",
                "degraded": True,
            }
    
    async def search_results(
        self,
        query: str,
        limit: int = 20
    ) -> dict:
        """Get search results with degradation."""
        try:
            # Try full search with ranking
            return await self._full_search(query, limit)
        
        except Exception as e:
            logger.warning(f"Full search failed: {e}, using basic")
            
            # Degrade to basic search (no ranking)
            try:
                return await self._basic_search(query, limit)
            except Exception as e2:
                logger.error(f"Basic search also failed: {e2}")
                
                # Degrade to cached results
                return await self._cached_search(query, limit)
```

---

## Error Classification & Recovery

### Error Classification System

**REQUIRED**: Classify errors for appropriate handling:

```python
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, Any

class ErrorCategory(Enum):
    """Error categories."""
    VALIDATION = "validation"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    NOT_FOUND = "not_found"
    CONFLICT = "conflict"
    RATE_LIMIT = "rate_limit"
    TIMEOUT = "timeout"
    NETWORK = "network"
    SERVICE_UNAVAILABLE = "service_unavailable"
    INTERNAL = "internal"

class ErrorSeverity(Enum):
    """Error severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class ClassifiedError:
    """Classified error with metadata."""
    error: Exception
    category: ErrorCategory
    severity: ErrorSeverity
    retryable: bool
    recoverable: bool
    context: Dict[str, Any]

class ErrorClassifier:
    """Error classification system."""
    
    def classify(self, error: Exception, context: Dict[str, Any] = None) -> ClassifiedError:
        """Classify an error."""
        context = context or {}
        
        # Classify by exception type
        if isinstance(error, ValueError):
            return ClassifiedError(
                error=error,
                category=ErrorCategory.VALIDATION,
                severity=ErrorSeverity.LOW,
                retryable=False,
                recoverable=True,
                context=context
            )
        
        elif isinstance(error, TimeoutError):
            return ClassifiedError(
                error=error,
                category=ErrorCategory.TIMEOUT,
                severity=ErrorSeverity.MEDIUM,
                retryable=True,
                recoverable=True,
                context=context
            )
        
        elif isinstance(error, ConnectionError):
            return ClassifiedError(
                error=error,
                category=ErrorCategory.NETWORK,
                severity=ErrorSeverity.HIGH,
                retryable=True,
                recoverable=True,
                context=context
            )
        
        # Default classification
        return ClassifiedError(
            error=error,
            category=ErrorCategory.INTERNAL,
            severity=ErrorSeverity.MEDIUM,
            retryable=False,
            recoverable=False,
            context=context
        )
```

### Recovery Strategy Selection

**REQUIRED**: Select recovery strategy based on error:

```python
from enum import Enum

class RecoveryStrategy(Enum):
    """Recovery strategies."""
    RETRY = "retry"
    FALLBACK = "fallback"
    DEGRADE = "degrade"
    CIRCUIT_BREAKER = "circuit_breaker"
    ESCALATE = "escalate"

class RecoverySelector:
    """Select recovery strategy based on error."""
    
    def select_strategy(self, classified_error: ClassifiedError) -> RecoveryStrategy:
        """Select recovery strategy."""
        # Retry for retryable errors
        if classified_error.retryable:
            return RecoveryStrategy.RETRY
        
        # Fallback for recoverable errors
        if classified_error.recoverable:
            return RecoveryStrategy.FALLBACK
        
        # Degrade for service issues
        if classified_error.category == ErrorCategory.SERVICE_UNAVAILABLE:
            return RecoveryStrategy.DEGRADE
        
        # Circuit breaker for repeated failures
        if classified_error.severity == ErrorSeverity.HIGH:
            return RecoveryStrategy.CIRCUIT_BREAKER
        
        # Escalate critical errors
        if classified_error.severity == ErrorSeverity.CRITICAL:
            return RecoveryStrategy.ESCALATE
        
        return RecoveryStrategy.ESCALATE
```

---

## FastAPI Integration

### Global Exception Handlers

**REQUIRED**: Register global exception handlers:

```python
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging

logger = logging.getLogger(__name__)

app = FastAPI()

@app.exception_handler(ApplicationError)
async def application_error_handler(
    request: Request,
    exc: ApplicationError
) -> JSONResponse:
    """Handle application errors."""
    logger.error(
        f"Application error: {exc.message}",
        extra={
            "status_code": exc.status_code,
            "context": exc.context,
        }
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.message,
                "type": exc.__class__.__name__,
                "context": exc.context,
            }
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_error_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    """Handle validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "message": "Validation error",
                "type": "ValidationError",
                "details": exc.errors(),
            }
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    """Handle unexpected exceptions."""
    logger.exception("Unexpected error", exc_info=exc)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "message": "Internal server error",
                "type": "InternalError",
            }
        }
    )
```

### Dependency Error Handling

**REQUIRED**: Handle errors in dependencies:

```python
from fastapi import Depends, HTTPException
from contextlib import asynccontextmanager

@asynccontextmanager
async def database_dependency():
    """Database dependency with error handling."""
    session = None
    try:
        session = await get_db_session()
        yield session
    except Exception as e:
        if session:
            await session.rollback()
        logger.error(f"Database error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed"
        )
    finally:
        if session:
            await session.close()

@app.get("/users/{user_id}")
async def get_user(
    user_id: int,
    db: Session = Depends(database_dependency)
):
    """Get user with error handling."""
    user = await db.get_user(user_id)
    if not user:
        raise NotFoundError("User", str(user_id))
    return user
```

### Route-Level Error Handling

**RECOMMENDED**: Handle errors at route level:

```python
from fastapi import HTTPException, status

@app.post("/users/")
async def create_user(user_data: UserCreate):
    """Create user with comprehensive error handling."""
    try:
        # Validate input
        validate_user_data(user_data)
        
        # Check for duplicates
        if await user_exists(user_data.email):
            raise ConflictError("User", "email", user_data.email)
        
        # Create user
        user = await create_user_in_db(user_data)
        return user
    
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    except ConflictError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    
    except Exception as e:
        logger.exception("Failed to create user", exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )
```

### Middleware Error Handling

**RECOMMENDED**: Add error handling middleware:

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import time

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware for error handling and logging."""
    
    async def dispatch(self, request: Request, call_next):
        """Process request with error handling."""
        start_time = time.time()
        
        try:
            response = await call_next(request)
            
            # Log slow requests
            duration = time.time() - start_time
            if duration > 1.0:
                logger.warning(
                    f"Slow request: {request.url.path} took {duration:.2f}s"
                )
            
            return response
        
        except HTTPException:
            # Re-raise HTTP exceptions
            raise
        
        except Exception as e:
            # Log unexpected errors
            logger.exception(
                f"Unexpected error in {request.url.path}",
                exc_info=e,
                extra={
                    "path": request.url.path,
                    "method": request.method,
                    "duration": time.time() - start_time,
                }
            )
            
            # Return generic error response
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": {
                        "message": "Internal server error",
                        "type": "InternalError",
                    }
                }
            )

app.add_middleware(ErrorHandlingMiddleware)
```

---

## Monitoring & Observability

### Error Metrics

**REQUIRED**: Track error metrics:

```python
from prometheus_client import Counter, Histogram

# Error metrics
error_counter = Counter(
    'application_errors_total',
    'Total application errors',
    ['error_type', 'category', 'severity']
)

error_duration = Histogram(
    'error_handling_duration_seconds',
    'Error handling duration',
    ['error_type']
)

class InstrumentedErrorHandler:
    """Error handler with metrics."""
    
    async def handle_error(self, error: Exception, context: Dict[str, Any]):
        """Handle error with metrics."""
        start_time = time.time()
        
        classified = self.classifier.classify(error, context)
        
        # Record metrics
        error_counter.labels(
            error_type=type(error).__name__,
            category=classified.category.value,
            severity=classified.severity.value
        ).inc()
        
        # Handle error
        try:
            await self._handle_classified_error(classified)
        finally:
            error_duration.labels(
                error_type=type(error).__name__
            ).observe(time.time() - start_time)
```

### Error Logging

**REQUIRED**: Comprehensive error logging:

```python
import structlog

logger = structlog.get_logger()

class StructuredErrorLogger:
    """Structured error logging."""
    
    def log_error(
        self,
        error: Exception,
        context: Dict[str, Any] = None,
        severity: str = "error"
    ) -> None:
        """Log error with structured data."""
        logger.error(
            "Error occurred",
            error_type=type(error).__name__,
            error_message=str(error),
            severity=severity,
            context=context or {},
            exc_info=error,
        )
    
    def log_retry(
        self,
        attempt: int,
        max_attempts: int,
        error: Exception
    ) -> None:
        """Log retry attempt."""
        logger.warning(
            "Retrying operation",
            attempt=attempt,
            max_attempts=max_attempts,
            error_type=type(error).__name__,
            error_message=str(error),
        )
    
    def log_circuit_breaker(
        self,
        breaker_name: str,
        state: str,
        failure_count: int
    ) -> None:
        """Log circuit breaker state change."""
        logger.warning(
            "Circuit breaker state changed",
            breaker_name=breaker_name,
            state=state,
            failure_count=failure_count,
        )
```

---

## Performance Considerations

### Async Error Handling

**REQUIRED**: Use async error handling:

```python
import asyncio
from typing import TypeVar, Awaitable

T = TypeVar('T')

async def safe_async_call(
    coro: Awaitable[T],
    default: T = None,
    timeout: float = None
) -> Optional[T]:
    """Safely call async function with error handling."""
    try:
        if timeout:
            return await asyncio.wait_for(coro, timeout=timeout)
        return await coro
    except asyncio.TimeoutError:
        logger.warning("Async operation timed out")
        return default
    except Exception as e:
        logger.error(f"Async operation failed: {e}", exc_info=e)
        return default
```

### Error Handling Overhead

**CRITICAL**: Minimize error handling overhead:

```python
# BAD: Expensive error handling in hot path
async def process_request(request: dict) -> dict:
    try:
        result = await expensive_operation(request)
        return result
    except Exception as e:
        # Expensive logging and classification
        classified = expensive_classification(e)
        await expensive_logging(classified)
        raise

# GOOD: Lightweight error handling
async def process_request(request: dict) -> dict:
    try:
        result = await expensive_operation(request)
        return result
    except Exception as e:
        # Lightweight error handling
        logger.error(f"Operation failed: {e}")
        raise
```

---

## Production Deployment

### Configuration

**REQUIRED**: Configure error handling via settings:

```python
from pydantic_settings import BaseSettings

class ErrorHandlingSettings(BaseSettings):
    """Error handling configuration."""
    
    # Retry configuration
    max_retries: int = 3
    retry_delay: float = 1.0
    retry_backoff_multiplier: float = 2.0
    
    # Circuit breaker configuration
    circuit_breaker_enabled: bool = True
    circuit_breaker_failure_threshold: int = 5
    circuit_breaker_recovery_timeout: int = 60
    circuit_breaker_success_threshold: int = 2
    
    # Timeout configuration
    default_timeout: float = 30.0
    connection_timeout: float = 5.0
    read_timeout: float = 10.0
    
    # Error handling
    enable_error_logging: bool = True
    enable_error_metrics: bool = True
    error_retention_days: int = 30
    
    class Config:
        env_file = ".env"
        env_prefix = "ERROR_HANDLING_"

settings = ErrorHandlingSettings()
```

### Health Checks

**REQUIRED**: Include error handling in health checks:

```python
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    health_status = {
        "status": "healthy",
        "circuit_breakers": {},
        "error_rates": {},
    }
    
    # Check circuit breakers
    for name, breaker in circuit_breakers.items():
        health_status["circuit_breakers"][name] = {
            "state": breaker.state.value,
            "failure_count": breaker.failure_count,
        }
    
    # Check error rates
    health_status["error_rates"] = {
        "last_hour": get_error_rate_last_hour(),
        "last_day": get_error_rate_last_day(),
    }
    
    # Determine overall health
    if any(
        cb["state"] == "open"
        for cb in health_status["circuit_breakers"].values()
    ):
        health_status["status"] = "degraded"
    
    return health_status
```

### Production Checklist

- [ ] Custom exception hierarchy defined
- [ ] Global exception handlers registered
- [ ] Retry strategies configured (Tenacity)
- [ ] Circuit breakers implemented for external services
- [ ] Timeout management configured
- [ ] Fallback mechanisms implemented
- [ ] Graceful degradation enabled
- [ ] Error classification system implemented
- [ ] Error logging configured (structured logging)
- [ ] Error metrics exported (Prometheus)
- [ ] Health checks include error handling status
- [ ] Error recovery strategies tested
- [ ] Circuit breaker monitoring configured
- [ ] Error alerting rules configured

---

## Summary

### Key Takeaways

1. **Exception Hierarchy**: Define clear exception hierarchy with custom exceptions
2. **Retry Strategies**: Use Tenacity for flexible retry logic with exponential backoff
3. **Circuit Breakers**: Implement circuit breakers to prevent cascading failures
4. **Timeout Management**: Configure granular timeouts for all operations
5. **Fallback Mechanisms**: Implement fallback chains for resilience
6. **Graceful Degradation**: Degrade features gracefully when services fail
7. **Error Classification**: Classify errors for appropriate handling strategies
8. **FastAPI Integration**: Register global exception handlers
9. **Monitoring**: Track error metrics and log errors comprehensively
10. **Performance**: Minimize error handling overhead in hot paths

### Resources

- [Tenacity Documentation](https://tenacity.readthedocs.io/)
- [PyBreaker Documentation](https://pybreaker.readthedocs.io/)
- [FastAPI Error Handling](https://fastapi.tiangolo.com/tutorial/handling-errors/)
- [HTTPX Error Handling](https://www.python-httpx.org/advanced/timeouts/)
- [Circuit Breaker Pattern](https://martinfowler.com/bliki/CircuitBreaker.html)

---

**Version**: v1.0.0  
**Last Updated**: 2025-01-14

