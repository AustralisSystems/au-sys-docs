# Object Pooling & Resource Management Best Practices

**Version**: v1.0.0  
**Last Updated**: 2025-01-14

This document provides comprehensive best practices for implementing object pooling and resource management in FastAPI applications, covering generic object pools, database connection pooling, HTTP client pooling, resource lifecycle management, pool sizing strategies, health monitoring, performance optimization, and FastAPI integration.

---

## Table of Contents

1. [Architecture Principles](#architecture-principles)
2. [Generic Object Pooling](#generic-object-pooling)
3. [Database Connection Pooling](#database-connection-pooling)
4. [HTTP Client Pooling](#http-client-pooling)
5. [Resource Lifecycle Management](#resource-lifecycle-management)
6. [Pool Sizing Strategies](#pool-sizing-strategies)
7. [Health Monitoring](#health-monitoring)
8. [Performance Optimization](#performance-optimization)
9. [FastAPI Integration](#fastapi-integration)
10. [Error Handling](#error-handling)
11. [Monitoring and Metrics](#monitoring-and-metrics)
12. [Production Deployment](#production-deployment)

---

## Architecture Principles

### Pool Philosophy

**REQUIRED**: Follow object pooling best practices:

1. **Reuse Over Create**: Reuse expensive-to-create objects rather than creating new ones
2. **Bounded Resources**: Set maximum pool sizes to prevent resource exhaustion
3. **Health Validation**: Validate objects before returning them from the pool
4. **Lifecycle Management**: Properly initialize, reset, and destroy pooled objects
5. **Thread Safety**: Ensure pools are thread-safe for concurrent access
6. **Graceful Degradation**: Handle pool exhaustion gracefully with timeouts

### When to Use Pooling

**REQUIRED**: Use pooling for:

- **Database Connections**: Expensive to create, limited by database server
- **HTTP Clients**: Connection overhead, keep-alive benefits
- **Parsers/Compilers**: Expensive initialization (XML parsers, regex compilers)
- **Cryptographic Objects**: Key generation, cipher initialization
- **File Handles**: Limited OS resources
- **Thread Pools**: Worker thread management

**AVOID**: Pooling for:

- **Simple Value Objects**: No creation overhead
- **Stateless Functions**: No state to manage
- **Short-Lived Objects**: Creation cost is negligible
- **Memory-Intensive Objects**: Pooling increases memory usage

---

## Generic Object Pooling

### Basic Pool Interface

**REQUIRED**: Define clear pool interface:

```python
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional
import asyncio

T = TypeVar("T")

class ObjectFactory(ABC, Generic[T]):
    """Abstract factory for creating and managing pooled objects."""
    
    @abstractmethod
    async def create_object(self) -> T:
        """Create a new object instance."""
        pass
    
    @abstractmethod
    async def reset_object(self, obj: T) -> bool:
        """Reset object to clean state for reuse.
        
        Returns:
            True if object was successfully reset, False if it should be discarded
        """
        pass
    
    @abstractmethod
    async def validate_object(self, obj: T) -> bool:
        """Validate that an object is healthy and usable.
        
        Returns:
            True if object is healthy, False if it should be discarded
        """
        pass
    
    async def destroy_object(self, obj: T) -> None:
        """Clean up and destroy an object."""
        if hasattr(obj, "close"):
            if asyncio.iscoroutinefunction(obj.close):
                await obj.close()
            else:
                obj.close()

class ObjectPool(Generic[T]):
    """Generic object pool for managing expensive-to-create objects."""
    
    async def acquire(self) -> T:
        """Acquire an object from the pool."""
        pass
    
    async def release(self, obj: T) -> None:
        """Release an object back to the pool."""
        pass
    
    async def close(self) -> None:
        """Close the pool and clean up all resources."""
        pass
```

### Pool Implementation

**REQUIRED**: Complete pool implementation:

```python
import asyncio
import time
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Deque, Dict, Optional

class ObjectState(str, Enum):
    """States for pooled objects."""
    AVAILABLE = "available"
    IN_USE = "in_use"
    UNHEALTHY = "unhealthy"
    EXPIRED = "expired"

@dataclass
class PooledObject(Generic[T]):
    """Wrapper for objects in the pool with metadata."""
    obj: T
    created_at: float = field(default_factory=time.time)
    last_used: float = field(default_factory=time.time)
    use_count: int = 0
    state: ObjectState = ObjectState.AVAILABLE
    max_uses: Optional[int] = None
    max_age: Optional[float] = None  # seconds
    
    def is_expired(self) -> bool:
        """Check if object is expired based on age or use count."""
        current_time = time.time()
        
        # Check age expiration
        if self.max_age and (current_time - self.created_at) > self.max_age:
            return True
        
        # Check use count expiration
        if self.max_uses and self.use_count >= self.max_uses:
            return True
        
        return False
    
    def mark_used(self) -> None:
        """Mark object as used and update statistics."""
        self.last_used = time.time()
        self.use_count += 1
        self.state = ObjectState.IN_USE
    
    def mark_available(self) -> None:
        """Mark object as available for reuse."""
        self.state = ObjectState.AVAILABLE

class ObjectPool(Generic[T]):
    """Generic object pool for managing expensive-to-create objects."""
    
    def __init__(
        self,
        factory: ObjectFactory[T],
        pool_name: str,
        min_size: int = 2,
        max_size: int = 20,
        max_idle_time: float = 300.0,  # 5 minutes
        max_object_age: float = 3600.0,  # 1 hour
        max_object_uses: Optional[int] = None,
        health_check_interval: float = 60.0,  # 1 minute
        acquire_timeout: float = 30.0,  # 30 seconds
    ):
        """Initialize object pool.
        
        Args:
            factory: Factory for creating and managing objects
            pool_name: Name for logging and monitoring
            min_size: Minimum number of objects to maintain
            max_size: Maximum number of objects allowed
            max_idle_time: Maximum idle time before object cleanup (seconds)
            max_object_age: Maximum age for objects before replacement (seconds)
            max_object_uses: Maximum uses per object before replacement
            health_check_interval: Interval between health checks (seconds)
            acquire_timeout: Timeout for acquiring objects (seconds)
        """
        self.factory = factory
        self.pool_name = pool_name
        self.min_size = min_size
        self.max_size = max_size
        self.max_idle_time = max_idle_time
        self.max_object_age = max_object_age
        self.max_object_uses = max_object_uses
        self.health_check_interval = health_check_interval
        self.acquire_timeout = acquire_timeout
        
        # Pool storage
        self._available_objects: Deque[PooledObject[T]] = deque()
        self._in_use_objects: Dict[id, PooledObject[T]] = {}
        self._pool_lock = asyncio.Lock()
        
        # Waiters for objects
        self._waiters: Deque[asyncio.Future] = deque()
        
        # Background tasks
        self._maintenance_task: Optional[asyncio.Task] = None
        self._health_check_task: Optional[asyncio.Task] = None
        self._shutdown = False
    
    async def initialize(self) -> None:
        """Initialize the object pool."""
        await self._pre_populate_pool()
        
        # Start background tasks
        self._maintenance_task = asyncio.create_task(self._maintenance_loop())
        self._health_check_task = asyncio.create_task(self._health_check_loop())
    
    async def acquire(self) -> T:
        """Acquire an object from the pool.
        
        Returns:
            Object from the pool
            
        Raises:
            asyncio.TimeoutError: If timeout exceeded waiting for object
            RuntimeError: If pool is shutdown
        """
        if self._shutdown:
            raise RuntimeError(f"Object pool '{self.pool_name}' is shutdown")
        
        start_time = time.perf_counter()
        
        try:
            # Try to get an available object immediately
            async with self._pool_lock:
                if self._available_objects:
                    pooled_obj = self._available_objects.popleft()
                    
                    # Validate object before returning
                    if await self._validate_pooled_object(pooled_obj):
                        pooled_obj.mark_used()
                        self._in_use_objects[id(pooled_obj.obj)] = pooled_obj
                        return pooled_obj.obj
                    else:
                        # Object is invalid, destroy it
                        await self._destroy_pooled_object(pooled_obj)
            
            # No available objects, try to create new one or wait
            return await self._acquire_or_wait(start_time)
            
        except asyncio.TimeoutError:
            raise
        except Exception as e:
            raise RuntimeError(f"Error acquiring object: {e}") from e
    
    async def release(self, obj: T) -> None:
        """Release an object back to the pool.
        
        Args:
            obj: Object to release
        """
        if self._shutdown:
            return
        
        async with self._pool_lock:
            obj_id = id(obj)
            
            if obj_id not in self._in_use_objects:
                return  # Unknown object, ignore
            
            pooled_obj = self._in_use_objects.pop(obj_id)
            
            # Check if object is still healthy and not expired
            if not pooled_obj.is_expired() and await self.factory.validate_object(obj):
                # Reset object for reuse
                if await self.factory.reset_object(obj):
                    pooled_obj.mark_available()
                    
                    # Return to pool if we have space
                    if len(self._available_objects) < self.max_size:
                        self._available_objects.append(pooled_obj)
                        
                        # Notify any waiters
                        if self._waiters:
                            waiter = self._waiters.popleft()
                            if not waiter.done():
                                waiter.set_result(pooled_obj)
                        return
            
            # Object is expired, invalid, or pool is full - destroy it
            await self._destroy_pooled_object(pooled_obj)
    
    async def _acquire_or_wait(self, start_time: float) -> T:
        """Try to create new object or wait for available one."""
        # Try to create new object if under max size
        async with self._pool_lock:
            total_count = len(self._available_objects) + len(self._in_use_objects)
            
            if total_count < self.max_size:
                try:
                    obj = await self.factory.create_object()
                    pooled_obj = PooledObject(
                        obj=obj,
                        max_uses=self.max_object_uses,
                        max_age=self.max_object_age,
                    )
                    pooled_obj.mark_used()
                    self._in_use_objects[id(obj)] = pooled_obj
                    return obj
                except Exception:
                    pass  # Fall through to waiting logic
        
        # Pool is at max size, wait for an available object
        future: asyncio.Future[PooledObject[T]] = asyncio.Future()
        
        async with self._pool_lock:
            self._waiters.append(future)
        
        try:
            timeout = self.acquire_timeout - (time.perf_counter() - start_time)
            pooled_obj = await asyncio.wait_for(future, timeout=timeout)
            
            # Validate the object we got
            if await self._validate_pooled_object(pooled_obj):
                pooled_obj.mark_used()
                async with self._pool_lock:
                    self._in_use_objects[id(pooled_obj.obj)] = pooled_obj
                return pooled_obj.obj
            else:
                # Object became invalid while waiting, destroy it and try again
                await self._destroy_pooled_object(pooled_obj)
                return await self._acquire_or_wait(start_time)
                
        except asyncio.TimeoutError:
            async with self._pool_lock:
                try:
                    self._waiters.remove(future)
                except ValueError:
                    pass
            raise
    
    async def _validate_pooled_object(self, pooled_obj: PooledObject[T]) -> bool:
        """Validate a pooled object."""
        # Check expiration
        if pooled_obj.is_expired():
            pooled_obj.state = ObjectState.EXPIRED
            return False
        
        # Check health
        try:
            if not await self.factory.validate_object(pooled_obj.obj):
                pooled_obj.state = ObjectState.UNHEALTHY
                return False
        except Exception:
            pooled_obj.state = ObjectState.UNHEALTHY
            return False
        
        return True
    
    async def _destroy_pooled_object(self, pooled_obj: PooledObject[T]) -> None:
        """Destroy a pooled object and clean up resources."""
        try:
            await self.factory.destroy_object(pooled_obj.obj)
        except Exception:
            pass  # Ignore cleanup errors
    
    async def _pre_populate_pool(self) -> None:
        """Pre-populate pool with minimum number of objects."""
        for _ in range(self.min_size):
            try:
                obj = await self.factory.create_object()
                pooled_obj = PooledObject(
                    obj=obj,
                    max_uses=self.max_object_uses,
                    max_age=self.max_object_age,
                )
                self._available_objects.append(pooled_obj)
            except Exception:
                break
    
    async def _maintenance_loop(self) -> None:
        """Background maintenance task for pool cleanup."""
        while not self._shutdown:
            try:
                await asyncio.sleep(60)  # Run every minute
                await self._cleanup_idle_objects()
                await self._ensure_minimum_size()
            except asyncio.CancelledError:
                break
            except Exception:
                pass  # Log error but continue
    
    async def _cleanup_idle_objects(self) -> None:
        """Clean up idle and expired objects."""
        current_time = time.time()
        objects_to_remove = []
        
        async with self._pool_lock:
            for pooled_obj in self._available_objects:
                idle_time = current_time - pooled_obj.last_used
                
                if (
                    idle_time > self.max_idle_time
                    or pooled_obj.is_expired()
                    or not await self.factory.validate_object(pooled_obj.obj)
                ):
                    objects_to_remove.append(pooled_obj)
            
            for pooled_obj in objects_to_remove:
                try:
                    self._available_objects.remove(pooled_obj)
                    await self._destroy_pooled_object(pooled_obj)
                except ValueError:
                    pass
    
    async def _ensure_minimum_size(self) -> None:
        """Ensure pool maintains minimum size."""
        async with self._pool_lock:
            available_count = len(self._available_objects)
            
            if available_count < self.min_size:
                needed = self.min_size - available_count
                
                for _ in range(needed):
                    try:
                        obj = await self.factory.create_object()
                        pooled_obj = PooledObject(
                            obj=obj,
                            max_uses=self.max_object_uses,
                            max_age=self.max_object_age,
                        )
                        self._available_objects.append(pooled_obj)
                    except Exception:
                        break
    
    async def _health_check_loop(self) -> None:
        """Background health check task."""
        while not self._shutdown:
            try:
                await asyncio.sleep(self.health_check_interval)
                await self._perform_health_checks()
            except asyncio.CancelledError:
                break
            except Exception:
                pass
    
    async def _perform_health_checks(self) -> None:
        """Perform health checks on available objects."""
        unhealthy_objects = []
        
        async with self._pool_lock:
            for pooled_obj in list(self._available_objects):
                if not await self._validate_pooled_object(pooled_obj):
                    unhealthy_objects.append(pooled_obj)
            
            for pooled_obj in unhealthy_objects:
                try:
                    self._available_objects.remove(pooled_obj)
                    await self._destroy_pooled_object(pooled_obj)
                except ValueError:
                    pass
    
    async def close(self) -> None:
        """Close the object pool and clean up all resources."""
        self._shutdown = True
        
        # Cancel background tasks
        if self._maintenance_task:
            self._maintenance_task.cancel()
            try:
                await self._maintenance_task
            except asyncio.CancelledError:
                pass
        
        if self._health_check_task:
            self._health_check_task.cancel()
            try:
                await self._health_check_task
            except asyncio.CancelledError:
                pass
        
        # Cancel all waiters
        async with self._pool_lock:
            while self._waiters:
                waiter = self._waiters.popleft()
                if not waiter.done():
                    waiter.cancel()
        
        # Destroy all objects
        async with self._pool_lock:
            while self._available_objects:
                pooled_obj = self._available_objects.popleft()
                await self._destroy_pooled_object(pooled_obj)
            
            for pooled_obj in list(self._in_use_objects.values()):
                await self._destroy_pooled_object(pooled_obj)
            self._in_use_objects.clear()
```

### Context Manager Support

**REQUIRED**: Add context manager support:

```python
from contextlib import asynccontextmanager

class ObjectPool(Generic[T]):
    """Generic object pool with context manager support."""
    
    @asynccontextmanager
    async def acquire_context(self):
        """Acquire object with automatic release."""
        obj = await self.acquire()
        try:
            yield obj
        finally:
            await self.release(obj)
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
```

### Usage Example

**REQUIRED**: Example usage:

```python
class HTTPClientFactory(ObjectFactory[httpx.AsyncClient]):
    """Factory for HTTP clients."""
    
    async def create_object(self) -> httpx.AsyncClient:
        """Create new HTTP client."""
        return httpx.AsyncClient(
            timeout=httpx.Timeout(30.0),
            limits=httpx.Limits(max_connections=10),
        )
    
    async def reset_object(self, obj: httpx.AsyncClient) -> bool:
        """Reset HTTP client for reuse."""
        # Clear cookies, reset state
        obj.cookies.clear()
        return True
    
    async def validate_object(self, obj: httpx.AsyncClient) -> bool:
        """Validate HTTP client is healthy."""
        return not obj.is_closed
    
    async def destroy_object(self, obj: httpx.AsyncClient) -> None:
        """Close HTTP client."""
        await obj.aclose()

# Create pool
factory = HTTPClientFactory()
pool = ObjectPool(
    factory=factory,
    pool_name="http_clients",
    min_size=2,
    max_size=10,
)

await pool.initialize()

# Use pool
async with pool.acquire_context() as client:
    response = await client.get("https://api.example.com/data")

# Or manual acquire/release
client = await pool.acquire()
try:
    response = await client.get("https://api.example.com/data")
finally:
    await pool.release(client)

# Cleanup
await pool.close()
```

---

## Database Connection Pooling

### SQLAlchemy Connection Pooling

**REQUIRED**: Configure SQLAlchemy connection pooling:

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.pool import QueuePool, NullPool, StaticPool

# PostgreSQL/MySQL: Use QueuePool
engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    poolclass=QueuePool,
    pool_size=20,              # Number of connections to maintain
    max_overflow=10,           # Additional connections when pool exhausted
    pool_timeout=30,           # Timeout waiting for connection (seconds)
    pool_recycle=3600,         # Recycle connections after 1 hour
    pool_pre_ping=True,        # Verify connection health before checkout
    pool_use_lifo=True,        # Last-In-First-Out retrieval
)

# SQLite: Use NullPool for file, StaticPool for in-memory
engine = create_async_engine(
    "sqlite+aiosqlite:///db.sqlite",
    poolclass=NullPool,  # No pooling for file-based SQLite
)

engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    poolclass=StaticPool,  # Single connection for in-memory
    connect_args={"check_same_thread": False},
)
```

### Pool Configuration by Database Type

**REQUIRED**: Configure pools based on database:

```python
def get_pool_class(url: str):
    """Get appropriate pool class for database."""
    if "sqlite" in url:
        if ":memory:" in url:
            return StaticPool
        return NullPool
    else:
        # PostgreSQL, MySQL: Use QueuePool
        return QueuePool

def create_database_engine(url: str, **kwargs):
    """Create database engine with appropriate pooling."""
    pool_class = get_pool_class(url)
    
    return create_async_engine(
        url,
        poolclass=pool_class,
        pool_size=kwargs.get("pool_size", 20),
        max_overflow=kwargs.get("max_overflow", 10),
        pool_timeout=kwargs.get("pool_timeout", 30),
        pool_pre_ping=kwargs.get("pool_pre_ping", True),
        pool_recycle=kwargs.get("pool_recycle", 3600),
    )
```

### Connection Pool Monitoring

**REQUIRED**: Monitor connection pool status:

```python
from sqlalchemy import event

@event.listens_for(engine, "connect")
def receive_connect(dbapi_conn, connection_record):
    """Log new connection creation."""
    logger.debug(f"New DBAPI connection: {dbapi_conn}")

@event.listens_for(engine, "checkout")
def receive_checkout(dbapi_conn, connection_record, connection_proxy):
    """Log connection checkout."""
    logger.debug("Connection checked out from pool")

@event.listens_for(engine, "checkin")
def receive_checkin(dbapi_conn, connection_record):
    """Log connection checkin."""
    logger.debug("Connection returned to pool")

# Get pool statistics
pool = engine.pool
stats = {
    "size": pool.size(),
    "checked_in": pool.checkedin(),
    "checked_out": pool.checkedout(),
    "overflow": pool.overflow(),
    "invalid": pool.invalid(),
}
```

### Connection Health Checks

**REQUIRED**: Implement connection health checks:

```python
from sqlalchemy import text

async def check_connection_health(engine: AsyncEngine) -> bool:
    """Check database connection health."""
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False

# Use pool_pre_ping for automatic health checks
engine = create_async_engine(
    url,
    pool_pre_ping=True,  # Automatically checks connection before use
)
```

### Connection Pool Event Listeners

**REQUIRED**: Use event listeners for monitoring:

```python
from sqlalchemy import event, exc

@event.listens_for(engine, "handle_error")
def handle_exception(context):
    """Handle connection errors."""
    if context.is_disconnect:
        logger.warning("Database connection lost, invalidating pool")
        # Pool will automatically create new connections
    return None
```

---

## HTTP Client Pooling

### httpx Connection Pooling

**REQUIRED**: Configure httpx connection pooling:

```python
import httpx

# Create HTTP client with connection pooling
client = httpx.AsyncClient(
    base_url="https://api.example.com",
    timeout=httpx.Timeout(30.0),
    limits=httpx.Limits(
        max_keepalive_connections=5,  # Keep connections alive
        max_connections=10,           # Maximum total connections
        keepalive_expiry=30.0,        # Keep-alive timeout
    ),
    http2=True,  # Enable HTTP/2 for better connection reuse
)

# Use client
async with client:
    response = await client.get("/endpoint")
```

### HTTP Client Pool Manager

**REQUIRED**: Implement HTTP client pool manager:

```python
from typing import Dict
import httpx

class HTTPClientPool:
    """Connection pool for HTTP clients with LRU eviction."""
    
    def __init__(self, max_connections: int = 10):
        self.max_connections = max_connections
        self.pools: Dict[str, httpx.AsyncClient] = {}
        self.pool_usage: Dict[str, int] = {}
    
    async def get_client(
        self,
        endpoint: str,
        headers: Dict[str, str],
        timeout: int = 30,
    ) -> httpx.AsyncClient:
        """Get HTTP client from pool."""
        pool_key = f"{endpoint}:{hash(frozenset(headers.items()))}"
        
        if pool_key not in self.pools:
            # Check if we need to evict a connection
            if len(self.pools) >= self.max_connections:
                # Remove least used connection
                lru_key = min(self.pool_usage, key=self.pool_usage.get)
                await self.pools[lru_key].aclose()
                del self.pools[lru_key]
                del self.pool_usage[lru_key]
            
            # Create new client with connection pooling
            client = httpx.AsyncClient(
                base_url=endpoint,
                headers=headers,
                timeout=httpx.Timeout(timeout),
                limits=httpx.Limits(
                    max_keepalive_connections=5,
                    max_connections=10,
                    keepalive_expiry=30.0,
                ),
            )
            self.pools[pool_key] = client
            self.pool_usage[pool_key] = 0
        
        self.pool_usage[pool_key] += 1
        return self.pools[pool_key]
    
    async def close_all(self) -> None:
        """Close all pooled connections."""
        for client in self.pools.values():
            await client.aclose()
        self.pools.clear()
        self.pool_usage.clear()
```

### Shared HTTP Client

**RECOMMENDED**: Use shared HTTP client for FastAPI:

```python
from fastapi import FastAPI
from contextlib import asynccontextmanager
import httpx

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan with shared HTTP client."""
    # Startup: Create shared HTTP client
    app.state.http_client = httpx.AsyncClient(
        timeout=httpx.Timeout(30.0),
        limits=httpx.Limits(
            max_keepalive_connections=5,
            max_connections=10,
            keepalive_expiry=30.0,
        ),
    )
    
    yield
    
    # Shutdown: Close HTTP client
    await app.state.http_client.aclose()

app = FastAPI(lifespan=lifespan)

@app.get("/external-api")
async def call_external_api():
    """Use shared HTTP client."""
    client = app.state.http_client
    response = await client.get("https://api.example.com/data")
    return response.json()
```

---

## Resource Lifecycle Management

### Resource Acquisition Pattern

**REQUIRED**: Use context managers for resource management:

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def acquire_resource(pool: ObjectPool[T]):
    """Acquire resource with automatic release."""
    resource = await pool.acquire()
    try:
        yield resource
    finally:
        await pool.release(resource)

# Usage
async with acquire_resource(pool) as resource:
    # Use resource
    await resource.do_work()
```

### Resource Cleanup

**REQUIRED**: Ensure proper resource cleanup:

```python
class ResourceManager:
    """Manages resource lifecycle."""
    
    def __init__(self):
        self._resources: List[Any] = []
        self._cleanup_callbacks: List[Callable] = []
    
    def register_resource(self, resource: Any, cleanup: Callable) -> None:
        """Register resource with cleanup callback."""
        self._resources.append(resource)
        self._cleanup_callbacks.append(cleanup)
    
    async def cleanup_all(self) -> None:
        """Clean up all registered resources."""
        for resource, cleanup in zip(self._resources, self._cleanup_callbacks):
            try:
                if asyncio.iscoroutinefunction(cleanup):
                    await cleanup(resource)
                else:
                    cleanup(resource)
            except Exception as e:
                logger.error(f"Error cleaning up resource: {e}")
        
        self._resources.clear()
        self._cleanup_callbacks.clear()
```

---

## Pool Sizing Strategies

### Dynamic Pool Sizing

**RECOMMENDED**: Implement dynamic pool sizing:

```python
class AdaptivePool(ObjectPool[T]):
    """Object pool with adaptive sizing."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._target_utilization = 0.7  # 70% utilization target
        self._adjustment_interval = 300  # 5 minutes
        self._min_adjustment = 2
    
    async def _adjust_pool_size(self) -> None:
        """Adjust pool size based on utilization."""
        async with self._pool_lock:
            total = len(self._available_objects) + len(self._in_use_objects)
            utilization = len(self._in_use_objects) / total if total > 0 else 0
            
            if utilization > self._target_utilization:
                # Increase pool size
                new_max = min(
                    self.max_size + self._min_adjustment,
                    self.max_size * 2,  # Cap at 2x
                )
                self.max_size = new_max
            elif utilization < self._target_utilization * 0.5:
                # Decrease pool size
                new_max = max(
                    self.max_size - self._min_adjustment,
                    self.min_size,  # Don't go below min
                )
                self.max_size = new_max
```

### Pool Size Calculation

**REQUIRED**: Calculate pool size based on workload:

```python
def calculate_pool_size(
    concurrent_requests: int,
    avg_request_duration: float,
    target_utilization: float = 0.7,
) -> int:
    """Calculate optimal pool size.
    
    Args:
        concurrent_requests: Expected concurrent requests
        avg_request_duration: Average request duration in seconds
        target_utilization: Target pool utilization (0.0-1.0)
    
    Returns:
        Recommended pool size
    """
    # Little's Law: L = λW
    # L = average number of requests in system
    # λ = arrival rate (requests/second)
    # W = average time in system
    
    # Simplified: pool_size = concurrent_requests * utilization
    pool_size = int(concurrent_requests * target_utilization)
    
    # Add buffer for spikes
    pool_size = int(pool_size * 1.2)
    
    return max(pool_size, 2)  # Minimum 2
```

---

## Health Monitoring

### Pool Health Checks

**REQUIRED**: Implement pool health monitoring:

```python
@dataclass
class PoolHealth:
    """Pool health status."""
    is_healthy: bool
    available_count: int
    in_use_count: int
    total_count: int
    utilization: float
    waiters_count: int
    error_count: int

class ObjectPool(Generic[T]):
    """Object pool with health monitoring."""
    
    async def get_health(self) -> PoolHealth:
        """Get pool health status."""
        async with self._pool_lock:
            available_count = len(self._available_objects)
            in_use_count = len(self._in_use_objects)
            total_count = available_count + in_use_count
            utilization = in_use_count / total_count if total_count > 0 else 0
            
            is_healthy = (
                not self._shutdown
                and total_count >= self.min_size
                and total_count <= self.max_size
                and len(self._waiters) < 10  # Not too many waiters
            )
            
            return PoolHealth(
                is_healthy=is_healthy,
                available_count=available_count,
                in_use_count=in_use_count,
                total_count=total_count,
                utilization=utilization,
                waiters_count=len(self._waiters),
                error_count=self.stats.health_check_failures,
            )
```

### Health Check Endpoint

**REQUIRED**: Expose health check endpoint:

```python
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/health/pools")
async def pool_health():
    """Get pool health status."""
    pool_manager = app.state.pool_manager
    
    health_status = {}
    for pool_name, pool in pool_manager.get_all_pools().items():
        health = await pool.get_health()
        health_status[pool_name] = {
            "healthy": health.is_healthy,
            "available": health.available_count,
            "in_use": health.in_use_count,
            "utilization": health.utilization,
        }
    
    all_healthy = all(h["healthy"] for h in health_status.values())
    
    return JSONResponse(
        status_code=status.HTTP_200_OK if all_healthy else status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"pools": health_status, "overall": "healthy" if all_healthy else "degraded"},
    )
```

---

## Performance Optimization

### Pool Statistics

**REQUIRED**: Track pool performance metrics:

```python
@dataclass
class PoolStatistics:
    """Statistics for object pool performance monitoring."""
    pool_name: str
    created_objects: int = 0
    destroyed_objects: int = 0
    borrowed_objects: int = 0
    returned_objects: int = 0
    health_check_failures: int = 0
    expired_objects: int = 0
    peak_pool_size: int = 0
    total_wait_time_ms: float = 0.0
    average_wait_time_ms: float = 0.0
    
    @property
    def active_objects(self) -> int:
        """Calculate currently active objects."""
        return self.borrowed_objects - self.returned_objects
    
    @property
    def object_reuse_rate(self) -> float:
        """Calculate object reuse efficiency."""
        if self.created_objects == 0:
            return 0.0
        return (self.borrowed_objects / self.created_objects) * 100
```

### Performance Monitoring

**RECOMMENDED**: Integrate with Prometheus:

```python
from prometheus_client import Counter, Histogram, Gauge

pool_acquire_total = Counter(
    "pool_acquire_total",
    "Total number of pool acquisitions",
    ["pool_name"],
)

pool_acquire_duration = Histogram(
    "pool_acquire_duration_seconds",
    "Time spent acquiring from pool",
    ["pool_name"],
)

pool_size = Gauge(
    "pool_size",
    "Current pool size",
    ["pool_name", "state"],  # state: available, in_use
)

class InstrumentedPool(ObjectPool[T]):
    """Object pool with Prometheus instrumentation."""
    
    async def acquire(self) -> T:
        """Acquire with instrumentation."""
        with pool_acquire_duration.labels(pool_name=self.pool_name).time():
            obj = await super().acquire()
            pool_acquire_total.labels(pool_name=self.pool_name).inc()
            return obj
```

---

## FastAPI Integration

### Dependency Injection

**REQUIRED**: Use FastAPI dependency injection for pools:

```python
from fastapi import Depends, FastAPI
from contextlib import asynccontextmanager

app = FastAPI()

# Initialize pools at startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan."""
    # Create pools
    http_pool = ObjectPool(
        factory=HTTPClientFactory(),
        pool_name="http_clients",
        min_size=2,
        max_size=10,
    )
    await http_pool.initialize()
    
    app.state.http_pool = http_pool
    
    yield
    
    # Cleanup
    await http_pool.close()

app = FastAPI(lifespan=lifespan)

async def get_http_client():
    """Dependency to get HTTP client from pool."""
    pool = app.state.http_pool
    client = await pool.acquire()
    try:
        yield client
    finally:
        await pool.release(client)

@app.get("/external")
async def call_external(client: httpx.AsyncClient = Depends(get_http_client)):
    """Use pooled HTTP client."""
    response = await client.get("https://api.example.com/data")
    return response.json()
```

### Pool Manager

**RECOMMENDED**: Create pool manager for multiple pools:

```python
class PoolManager:
    """Manager for multiple object pools."""
    
    def __init__(self):
        self._pools: Dict[str, ObjectPool] = {}
        self._pools_lock = asyncio.Lock()
    
    async def create_pool(
        self,
        pool_name: str,
        factory: ObjectFactory[T],
        **pool_config,
    ) -> ObjectPool[T]:
        """Create and register a new object pool."""
        async with self._pools_lock:
            if pool_name in self._pools:
                raise ValueError(f"Pool '{pool_name}' already exists")
            
            pool = ObjectPool(factory, pool_name, **pool_config)
            await pool.initialize()
            
            self._pools[pool_name] = pool
            return pool
    
    async def get_pool(self, pool_name: str) -> Optional[ObjectPool]:
        """Get an existing object pool."""
        async with self._pools_lock:
            return self._pools.get(pool_name)
    
    async def close_all(self) -> None:
        """Close all object pools."""
        async with self._pools_lock:
            for pool in self._pools.values():
                await pool.close()
            self._pools.clear()

# Use in FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan."""
    pool_manager = PoolManager()
    
    # Create pools
    await pool_manager.create_pool(
        "http_clients",
        HTTPClientFactory(),
        min_size=2,
        max_size=10,
    )
    
    app.state.pool_manager = pool_manager
    
    yield
    
    await pool_manager.close_all()

app = FastAPI(lifespan=lifespan)
```

---

## Error Handling

### Pool Exhaustion Handling

**REQUIRED**: Handle pool exhaustion gracefully:

```python
from fastapi import HTTPException, status

async def get_pooled_resource(pool: ObjectPool[T]):
    """Get resource from pool with error handling."""
    try:
        resource = await pool.acquire()
        return resource
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Resource pool exhausted, please try again later",
        )
    except RuntimeError as e:
        if "shutdown" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Resource pool is shutting down",
            )
        raise
```

### Retry Logic

**RECOMMENDED**: Add retry logic for pool operations:

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
)
async def acquire_with_retry(pool: ObjectPool[T]) -> T:
    """Acquire resource with retry logic."""
    return await pool.acquire()
```

---

## Monitoring and Metrics

### Pool Metrics

**REQUIRED**: Track key pool metrics:

```python
@dataclass
class PoolMetrics:
    """Pool performance metrics."""
    pool_name: str
    current_size: int
    available_count: int
    in_use_count: int
    utilization: float
    waiters_count: int
    acquire_timeout_count: int
    health_check_failures: int
    average_acquire_time_ms: float
    object_reuse_rate: float

class ObjectPool(Generic[T]):
    """Object pool with metrics tracking."""
    
    async def get_metrics(self) -> PoolMetrics:
        """Get pool metrics."""
        async with self._pool_lock:
            available_count = len(self._available_objects)
            in_use_count = len(self._in_use_objects)
            total_count = available_count + in_use_count
            utilization = in_use_count / total_count if total_count > 0 else 0
            
            return PoolMetrics(
                pool_name=self.pool_name,
                current_size=total_count,
                available_count=available_count,
                in_use_count=in_use_count,
                utilization=utilization,
                waiters_count=len(self._waiters),
                acquire_timeout_count=self.stats.acquire_timeout_count,
                health_check_failures=self.stats.health_check_failures,
                average_acquire_time_ms=self.stats.average_wait_time_ms,
                object_reuse_rate=self.stats.object_reuse_rate,
            )
```

---

## Production Deployment

### Production Configuration

**REQUIRED**: Production pool configuration:

```python
# Database connection pool
DATABASE_POOL_CONFIG = {
    "pool_size": 20,
    "max_overflow": 10,
    "pool_timeout": 30,
    "pool_pre_ping": True,
    "pool_recycle": 3600,
}

# HTTP client pool
HTTP_CLIENT_POOL_CONFIG = {
    "min_size": 5,
    "max_size": 20,
    "max_idle_time": 300.0,
    "max_object_age": 3600.0,
    "health_check_interval": 60.0,
    "acquire_timeout": 30.0,
}

# Create pools with production config
database_pool = create_async_engine(
    DATABASE_URL,
    **DATABASE_POOL_CONFIG,
)

http_pool = ObjectPool(
    factory=HTTPClientFactory(),
    pool_name="http_clients",
    **HTTP_CLIENT_POOL_CONFIG,
)
```

### Monitoring Checklist

**REQUIRED**: Monitor pool health:

- [ ] Pool utilization (target: 60-80%)
- [ ] Average acquire time (< 10ms)
- [ ] Timeout rate (< 0.1%)
- [ ] Health check failures (< 1%)
- [ ] Object reuse rate (> 80%)
- [ ] Peak pool size (within limits)
- [ ] Waiters count (< 5)

---

## Summary

### Key Takeaways

1. **Generic Pools**: Use generic object pools for expensive-to-create objects
2. **Connection Pooling**: Configure database and HTTP client connection pooling
3. **Lifecycle Management**: Properly initialize, reset, and destroy pooled objects
4. **Health Monitoring**: Implement health checks and monitoring
5. **Pool Sizing**: Calculate pool sizes based on workload
6. **Error Handling**: Handle pool exhaustion and errors gracefully
7. **FastAPI Integration**: Use dependency injection for pool access
8. **Metrics**: Track pool performance metrics
9. **Production**: Configure pools for production workloads
10. **Monitoring**: Monitor pool health and performance

### Resources

- [SQLAlchemy Connection Pooling](https://docs.sqlalchemy.org/en/20/core/pooling.html)
- [httpx Connection Pooling](https://www.python-httpx.org/advanced/#connection-pooling)
- [Object Pool Pattern](https://en.wikipedia.org/wiki/Object_pool_pattern)
- [FastAPI Dependency Injection](https://fastapi.tiangolo.com/tutorial/dependencies/)

---

**Version**: v1.0.0  
**Last Updated**: 2025-01-14

