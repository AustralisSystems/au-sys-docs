# Redis Caching Best Practices for Production

## Overview

This document provides comprehensive best practices for implementing Redis caching in production environments, specifically tailored to this application's architecture. It covers Redis-specific caching patterns, performance optimization, memory management, key design, and integration strategies.

## Architecture

### Current Implementation

- **Multi-Level Cache**: L1 (memory) + L2 (Redis)
- **Redis Cluster**: 6-node cluster for high availability
- **Cache Patterns**: Cache-aside, write-through, write-behind
- **Invalidation**: Tag-based, pattern-based, dependency-based
- **Serialization**: JSON, Pickle, MessagePack with compression
- **Security**: Encrypted cache support
- **Monitoring**: Performance metrics, analytics, dashboards

## Redis Caching Patterns

### 1. Cache-Aside (Lazy Loading)

**RECOMMENDED**: Default pattern for most use cases

**Implementation**:
```python
from src.services.redis_cache.core.cache_manager import CacheManager

async def get_user(user_id: int) -> dict:
    """Get user with cache-aside pattern."""
    cache_key = f"user:{user_id}"

    # Try cache first
    cached_user = await cache.get(cache_key)
    if cached_user is not None:
        return cached_user

    # Cache miss - load from database
    user = await db.get_user(user_id)

    # Store in cache for future requests
    if user:
        await cache.set(cache_key, user, ttl=3600)

    return user
```

**Best Practices**:
- ✅ Check cache before database query
- ✅ Set appropriate TTL based on data freshness requirements
- ✅ Handle cache failures gracefully (fallback to database)
- ✅ Use consistent key naming conventions

**When to Use**:
- Frequently accessed data
- Data that doesn't change frequently
- Read-heavy workloads
- Data that can tolerate eventual consistency

### 2. Write-Through Pattern

**RECOMMENDED**: For critical data requiring immediate consistency

**Implementation**:
```python
async def update_user(user_id: int, user_data: dict) -> bool:
    """Update user with write-through pattern."""
    cache_key = f"user:{user_id}"

    # Update database first
    success = await db.update_user(user_id, user_data)

    if success:
        # Then update cache
        await cache.set(cache_key, user_data, ttl=3600)

    return success
```

**Best Practices**:
- ✅ Write to database first, then cache
- ✅ Handle write failures (don't update cache if DB fails)
- ✅ Invalidate related cache entries
- ✅ Use transactions when possible

**When to Use**:
- Critical data requiring consistency
- Write-heavy workloads
- Data that must be immediately available after write

### 3. Write-Behind (Write-Back) Pattern

**RECOMMENDED**: For high-throughput write scenarios

**Implementation**:
```python
async def write_behind_update(user_id: int, user_data: dict):
    """Update with write-behind pattern."""
    cache_key = f"user:{user_id}"

    # Update cache immediately
    await cache.set(cache_key, user_data, ttl=3600)

    # Queue database update for async processing
    await queue.enqueue("update_user_db", user_id, user_data)
```

**Best Practices**:
- ✅ Update cache immediately for fast response
- ✅ Queue database updates for async processing
- ✅ Implement retry logic for failed DB updates
- ✅ Monitor queue depth and processing lag
- ✅ Handle cache eviction before DB write completes

**When to Use**:
- High write throughput requirements
- Data that can tolerate eventual consistency
- Write-heavy workloads with acceptable data loss risk

### 4. Read-Through Pattern

**RECOMMENDED**: For automatic cache population

**Implementation**:
```python
class ReadThroughCache:
    """Read-through cache implementation."""

    def __init__(self, cache: CacheManager, data_source):
        self.cache = cache
        self.data_source = data_source

    async def get(self, key: str) -> Any:
        """Get value with automatic loading on miss."""
        # Try cache first
        value = await self.cache.get(key)
        if value is not None:
            return value

        # Cache miss - load from source
        value = await self.data_source.load(key)

        # Store in cache
        if value is not None:
            await self.cache.set(key, value, ttl=3600)

        return value
```

**Best Practices**:
- ✅ Automatically populate cache on miss
- ✅ Use appropriate TTL based on data characteristics
- ✅ Handle data source failures gracefully
- ✅ Implement cache warming for frequently accessed data

## Key Design Best Practices

### 1. Key Naming Conventions

**RECOMMENDED**: Hierarchical namespace pattern

```python
# Good: Hierarchical namespace
"app:module:entity:id"
"app:module:entity:id:field"

# Examples
"orchestrator:users:123"
"orchestrator:users:123:profile"
"orchestrator:workflows:456:status"
"orchestrator:api:calls:789"

# Bad: Flat or inconsistent naming
"user123"
"user_123"
"User-123"
```

**Best Practices**:
- Use consistent separator (`:` recommended)
- Include namespace/application prefix
- Include entity type and identifier
- Use lowercase with underscores for readability
- Avoid special characters that require escaping

### 2. Hash Tags for Multi-Key Operations

**RECOMMENDED**: Use hash tags for related keys in Redis Cluster

```python
# Good: Keys hash to same slot
user_id = 1234
await cache.set(f"user:{{{user_id}}}:profile", profile_data)
await cache.set(f"user:{{{user_id}}}:settings", settings_data)
await cache.set(f"user:{{{user_id}}}:preferences", prefs_data)

# All keys with {1234} hash to same slot
# Can use MGET, MSET, transactions

# Bad: Keys hash to different slots
await cache.set(f"user:{user_id}:profile", profile_data)
await cache.set(f"user:{user_id}:settings", settings_data)
# Cannot use MGET in cluster mode
```

**Best Practices**:
- Use hash tags `{tag}` for related keys
- Group keys that are accessed together
- Use hash tags for multi-key operations (MGET, MSET, transactions)
- Keep hash tag consistent across related keys

### 3. Key Expiration (TTL)

**RECOMMENDED**: Set appropriate TTLs based on data characteristics

```python
# Short-lived data (sessions, locks)
await cache.set("session:abc123", session_data, ttl=1800)  # 30 minutes

# Frequently accessed data (user profiles)
await cache.set("user:123", user_data, ttl=3600)  # 1 hour

# Stable data (configuration, static content)
await cache.set("config:app", config_data, ttl=86400)  # 24 hours

# Long-lived data (reference data)
await cache.set("countries:list", countries_data, ttl=604800)  # 7 days
```

**TTL Guidelines**:
- **Sessions**: 30 minutes - 2 hours
- **User Data**: 1-4 hours
- **API Responses**: 5-15 minutes
- **Configuration**: 24 hours - 7 days
- **Reference Data**: 7-30 days

**Best Practices**:
- Always set TTL for cache entries
- Use shorter TTLs for frequently changing data
- Use longer TTLs for stable data
- Implement TTL extension on access (sliding expiration)
- Monitor cache hit rates to optimize TTLs

### 4. Key Versioning

**RECOMMENDED**: Version keys for schema changes

```python
# Versioned keys
await cache.set("user:v2:123", user_data_v2, ttl=3600)
await cache.set("config:v1:app", config_data_v1, ttl=86400)

# Benefits:
# - Gradual migration
# - Rollback capability
# - A/B testing
```

## Memory Management

### 1. Eviction Policies

**Current Configuration**: `allkeys-lru`

**Available Policies**:
- `allkeys-lru`: Evict least recently used keys (recommended for caching)
- `volatile-lru`: Evict least recently used keys with TTL
- `allkeys-lfu`: Evict least frequently used keys
- `volatile-lfu`: Evict least frequently used keys with TTL
- `allkeys-random`: Random eviction
- `volatile-random`: Random eviction with TTL
- `volatile-ttl`: Evict keys with shortest TTL
- `noeviction`: No eviction (use with caution)

**Best Practices**:
```python
# For caching (current)
maxmemory-policy: allkeys-lru

# For session storage
maxmemory-policy: volatile-lru

# For mixed workloads
maxmemory-policy: allkeys-lfu
```

### 2. Memory Limits

**Current Configuration**:
- Staging: 512MB per node
- Production: 1GB per node

**Best Practices**:
- Set `maxmemory` to 80-90% of available RAM
- Leave headroom for Redis overhead (~10-20%)
- Monitor memory usage and adjust limits
- Use `INFO memory` to track memory usage

**Memory Calculation**:
```bash
# Check memory usage
redis-cli INFO memory

# Check specific key memory
redis-cli MEMORY USAGE key_name

# Check memory usage by pattern
redis-cli --scan --pattern "user:*" | xargs redis-cli MEMORY USAGE
```

### 3. Memory Optimization

**Best Practices**:
- Use appropriate data structures (hashes vs strings)
- Compress large values
- Use TTL to expire unused data
- Monitor and remove large keys
- Use Redis memory profiler

**Data Structure Selection**:
```python
# Good: Use hash for related fields
await cache.hset("user:123", mapping={
    "name": "John",
    "email": "john@example.com",
    "age": "30"
})

# Bad: Multiple string keys
await cache.set("user:123:name", "John")
await cache.set("user:123:email", "john@example.com")
await cache.set("user:123:age", "30")

# Memory savings: ~50% with hash
```

## Performance Optimization

### 1. Pipelining

**RECOMMENDED**: Use pipelining for multiple operations

```python
# Good: Pipeline multiple commands
pipe = cache.pipeline()
pipe.set("key1", "value1")
pipe.set("key2", "value2")
pipe.set("key3", "value3")
results = await pipe.execute()

# Bad: Multiple round trips
await cache.set("key1", "value1")
await cache.set("key2", "value2")
await cache.set("key3", "value3")
```

**Best Practices**:
- Batch related operations in pipelines
- Use pipelines for bulk operations
- Limit pipeline size (100-1000 commands)
- Handle pipeline failures gracefully

### 2. Connection Pooling

**Current Configuration**:
```python
max_connections: 50
max_connections_per_node: 10
```

**Best Practices**:
- Reuse connections via connection pool
- Size pool based on concurrent requests
- Monitor connection pool usage
- Use async connections for async operations

**Pool Sizing Guidelines**:
- **Small Applications**: 10-20 connections
- **Medium Applications**: 50-100 connections
- **Large Applications**: 100-200 connections
- **Per Node**: 10-20 connections per Redis node

### 3. Compression

**Current Configuration**: ✅ Compression enabled

**Best Practices**:
```python
# Enable compression for large values
await cache.set(
    key="large:data",
    value=large_data,
    compress=True,
    compression_threshold=1024  # Compress if > 1KB
)
```

**Compression Guidelines**:
- Compress values > 1KB
- Use LZ4 for fastest compression
- Use gzip for best compression ratio
- Monitor compression overhead

### 4. Serialization Optimization

**Current Implementation**: JSON, Pickle, MessagePack

**Best Practices**:
```python
# JSON: Best for simple data structures (default)
await cache.set("key", data, serializer="json")

# MessagePack: Faster, smaller than JSON
await cache.set("key", data, serializer="msgpack")

# Pickle: For complex Python objects (use with caution)
await cache.set("key", complex_object, serializer="pickle")
```

**Serialization Selection**:
- **JSON**: Human-readable, widely supported, slower
- **MessagePack**: Binary format, faster, smaller, good for production
- **Pickle**: Python-specific, fastest, security concerns

## Cache Invalidation Strategies

### 1. Tag-Based Invalidation

**RECOMMENDED**: Use tags for related cache entries

```python
# Set cache with tags
await cache.set(
    key="user:123",
    value=user_data,
    tags=["user", "profile", "active"]
)

# Invalidate by tag
await cache.invalidate_by_tag("user")  # Invalidates all user:* keys

# Invalidate by multiple tags
await cache.invalidate_by_tags(["user", "active"])
```

**Best Practices**:
- Use descriptive tags
- Group related keys with same tags
- Invalidate tags on data updates
- Monitor tag invalidation performance

### 2. Pattern-Based Invalidation

**RECOMMENDED**: Use patterns for bulk invalidation

```python
# Invalidate by pattern
await cache.invalidate_pattern("user:*")
await cache.invalidate_pattern("user:123:*")
await cache.invalidate_pattern("workflow:*:status")
```

**Best Practices**:
- Use specific patterns to avoid over-invalidation
- Test patterns in development first
- Monitor invalidation performance
- Use SCAN for large pattern matches

### 3. Dependency-Based Invalidation

**RECOMMENDED**: Use dependencies for cascading invalidation

```python
# Set cache with dependencies
await cache.set(
    key="user:123:posts",
    value=posts_data,
    dependencies=["user:123"]
)

# When user:123 is invalidated, user:123:posts is automatically invalidated
await cache.delete("user:123")
```

**Best Practices**:
- Define clear dependency relationships
- Avoid circular dependencies
- Monitor dependency graph size
- Use for hierarchical data structures

### 4. TTL-Based Expiration

**RECOMMENDED**: Use TTL for automatic expiration

```python
# Set TTL based on data freshness requirements
await cache.set("session:abc", session_data, ttl=1800)  # 30 min
await cache.set("user:123", user_data, ttl=3600)  # 1 hour
await cache.set("config:app", config_data, ttl=86400)  # 24 hours
```

**Best Practices**:
- Always set TTL for cache entries
- Use shorter TTLs for frequently changing data
- Implement sliding expiration for active data
- Monitor cache hit rates to optimize TTLs

## Multi-Level Caching

### 1. L1 (Memory) Cache

**Current Configuration**:
```python
l1_max_size: 1000
l1_max_memory: 100MB
l1_default_ttl: 300  # 5 minutes
l1_eviction_policy: LRU
```

**Best Practices**:
- Use L1 for frequently accessed data
- Keep L1 size manageable (1000-5000 entries)
- Use shorter TTL for L1 (5-15 minutes)
- Monitor L1 hit rate

**When to Use L1**:
- Very frequently accessed data
- Small data objects
- Data that benefits from ultra-fast access
- Single-instance applications

### 2. L2 (Redis) Cache

**Current Configuration**:
```python
l2_default_ttl: 3600  # 1 hour
l2_max_size: 10000
```

**Best Practices**:
- Use L2 for distributed caching
- Use longer TTL for L2 (1-24 hours)
- Use Redis cluster for high availability
- Monitor L2 hit rate and memory usage

**When to Use L2**:
- Distributed applications
- Shared cache across instances
- Larger data objects
- Data that needs to persist across restarts

### 3. Cache Promotion Strategy

**Current Configuration**: ✅ Automatic promotion enabled

**Best Practices**:
```python
# Automatic promotion from L2 to L1
promotion_threshold: 3  # Access count for promotion
promotion_enabled: True
```

**Promotion Logic**:
- Track access count per key
- Promote to L1 after threshold accesses
- Demote from L1 when access decreases
- Monitor promotion/demotion rates

## Cache Warming

### 1. Preload Strategy

**RECOMMENDED**: Warm cache on application startup

```python
from src.services.redis_cache.strategies.warming_engine import WarmingEngine

warming_engine = WarmingEngine(cache)

# Warm cache with frequently accessed data
await warming_engine.warm_cache([
    "user:123",
    "user:456",
    "config:app",
    "countries:list"
])
```

**Best Practices**:
- Warm cache on startup for critical data
- Warm cache after deployments
- Use background tasks for cache warming
- Monitor warming performance

### 2. Predictive Warming

**RECOMMENDED**: Warm cache based on access patterns

```python
# Warm cache based on user access patterns
async def warm_user_cache(user_id: int):
    """Warm cache for user-related data."""
    keys = [
        f"user:{user_id}",
        f"user:{user_id}:profile",
        f"user:{user_id}:settings",
        f"user:{user_id}:preferences"
    ]
    await warming_engine.warm_cache(keys)
```

**Best Practices**:
- Analyze access patterns
- Warm cache proactively
- Use machine learning for prediction
- Monitor warming effectiveness

## Monitoring and Observability

### 1. Key Metrics

**Essential Metrics**:
- Cache hit rate (target: >80%)
- Cache miss rate
- Average access time
- Memory usage
- Eviction rate
- Invalidation rate

**Implementation**:
```python
from src.services.redis_cache.metrics.performance_monitor import CachePerformanceMonitor

monitor = CachePerformanceMonitor(cache)
metrics = await monitor.get_metrics()

print(f"Hit Rate: {metrics['hit_rate']:.2f}%")
print(f"Miss Rate: {metrics['miss_rate']:.2f}%")
print(f"Avg Access Time: {metrics['avg_access_time_ms']:.2f}ms")
```

### 2. Prometheus Integration

**Best Practices**:
```python
from prometheus_client import Counter, Histogram, Gauge

cache_hits = Counter(
    'redis_cache_hits_total',
    'Total cache hits',
    ['namespace', 'key_pattern']
)

cache_misses = Counter(
    'redis_cache_misses_total',
    'Total cache misses',
    ['namespace', 'key_pattern']
)

cache_operation_duration = Histogram(
    'redis_cache_operation_duration_seconds',
    'Cache operation duration',
    ['operation', 'namespace']
)
```

### 3. Alerting

**Recommended Alerts**:
- Cache hit rate < 70%
- Memory usage > 90%
- Eviction rate > 100/sec
- Average access time > 10ms
- Connection pool exhaustion

## Security Best Practices

### 1. Data Encryption

**Current Implementation**: ✅ Encrypted cache support

```python
from src.services.redis_cache.security.encrypted_cache import EncryptedCacheManager

# Use encrypted cache for sensitive data
await cache.set(
    key="sensitive:data",
    value=sensitive_data,
    encrypt=True
)
```

**Best Practices**:
- Encrypt sensitive data (PII, credentials)
- Use strong encryption algorithms (AES-256-GCM)
- Rotate encryption keys regularly
- Monitor encryption overhead

### 2. Access Control

**Best Practices**:
```python
# Set access control for cache operations
await cache.set_access_control(
    key_pattern="user:*",
    allowed_roles=["admin", "user"],
    denied_roles=["guest"]
)
```

### 3. Key Isolation

**Best Practices**:
- Use separate Redis databases for different applications
- Use key prefixes for namespace isolation
- Implement key validation
- Monitor key access patterns

## Error Handling and Resilience

### 1. Circuit Breaker Pattern

**Current Implementation**: ✅ Circuit breaker in RedisClusterManager

**Best Practices**:
```python
# Circuit breaker prevents cascading failures
circuit_breaker_threshold: 5  # Failures before opening
circuit_breaker_timeout: 60  # Seconds before retry
```

### 2. Graceful Degradation

**Best Practices**:
```python
async def get_user_with_fallback(user_id: int):
    """Get user with cache fallback."""
    try:
        # Try cache first
        cached_user = await cache.get(f"user:{user_id}")
        if cached_user:
            return cached_user
    except Exception as e:
        logger.warning(f"Cache error: {e}, falling back to database")

    # Fallback to database
    return await db.get_user(user_id)
```

### 3. Retry Logic

**Best Practices**:
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10)
)
async def cache_operation_with_retry(key: str, value: Any):
    """Cache operation with exponential backoff retry."""
    return await cache.set(key, value, ttl=3600)
```

## Performance Tuning Checklist

- [ ] Configure appropriate `maxmemory` (80-90% of RAM)
- [ ] Set appropriate eviction policy (`allkeys-lru` for caching)
- [ ] Use hash tags for multi-key operations in cluster
- [ ] Implement connection pooling (50-100 connections)
- [ ] Use pipelining for batch operations
- [ ] Enable compression for large values (>1KB)
- [ ] Use appropriate serialization (MessagePack for production)
- [ ] Set TTL for all cache entries
- [ ] Implement tag-based invalidation
- [ ] Use multi-level caching (L1 + L2)
- [ ] Configure cache warming for critical data
- [ ] Monitor cache hit rate (target >80%)
- [ ] Set up Prometheus metrics
- [ ] Configure alerting for cache issues
- [ ] Test failover scenarios
- [ ] Optimize key naming conventions
- [ ] Use appropriate data structures (hashes vs strings)
- [ ] Monitor memory usage and eviction rates
- [ ] Implement graceful degradation
- [ ] Use circuit breaker for resilience

## Recommended Production Configuration

```python
cache_config = {
    "redis": {
        "cluster_enabled": True,
        "startup_nodes": [
            {"host": "redis-cluster-0", "port": 6379},
            {"host": "redis-cluster-1", "port": 6379},
            {"host": "redis-cluster-2", "port": 6379},
        ],
        "max_connections": 50,
        "max_connections_per_node": 10,
        "socket_timeout": 30,
        "retry_on_cluster_down": True,
    },
    "multi_level": {
        "enabled": True,
        "l1_max_size": 1000,
        "l1_max_memory": 100 * 1024 * 1024,  # 100MB
        "l1_default_ttl": 300,  # 5 minutes
        "l1_eviction_policy": "lru",
        "l2_default_ttl": 3600,  # 1 hour
        "promotion_threshold": 3,
    },
    "serialization": {
        "default_serializer": "msgpack",
        "compression_enabled": True,
        "compression_threshold": 1024,  # 1KB
        "compression_algorithm": "lz4",
    },
    "invalidation": {
        "tag_based": True,
        "pattern_based": True,
        "dependency_based": True,
    },
    "monitoring": {
        "enabled": True,
        "metrics_collection": True,
        "alerting_enabled": True,
    },
}
```

## Common Anti-Patterns to Avoid

### 1. Cache Stampede

**Problem**: Multiple requests miss cache simultaneously, all query database

**Solution**: Use distributed locks or probabilistic early expiration

```python
# Good: Use distributed lock
async def get_user_with_lock(user_id: int):
    lock_key = f"lock:user:{user_id}"
    async with distributed_lock(lock_key, timeout=5):
        user = await cache.get(f"user:{user_id}")
        if not user:
            user = await db.get_user(user_id)
            await cache.set(f"user:{user_id}", user, ttl=3600)
        return user
```

### 2. Thundering Herd

**Problem**: Cache expires, all requests hit database simultaneously

**Solution**: Use probabilistic early expiration or cache warming

```python
# Good: Probabilistic early expiration
import random

def get_ttl_with_jitter(base_ttl: int, jitter_percent: float = 0.1) -> int:
    """Add jitter to TTL to prevent thundering herd."""
    jitter = int(base_ttl * jitter_percent * random.uniform(-1, 1))
    return base_ttl + jitter

ttl = get_ttl_with_jitter(3600, jitter_percent=0.1)  # 3240-3960 seconds
```

### 3. Cache Invalidation Storms

**Problem**: Invalidating too many keys at once causes performance issues

**Solution**: Batch invalidations or use TTL instead

```python
# Good: Batch invalidations
async def invalidate_users_batch(user_ids: List[int]):
    """Invalidate users in batches."""
    batch_size = 100
    for i in range(0, len(user_ids), batch_size):
        batch = user_ids[i:i + batch_size]
        await asyncio.gather(*[
            cache.delete(f"user:{uid}") for uid in batch
        ])
        await asyncio.sleep(0.1)  # Small delay between batches
```

### 4. Stale Data

**Problem**: Cache contains outdated data

**Solution**: Use appropriate TTLs and invalidation strategies

```python
# Good: Invalidate on update
async def update_user(user_id: int, user_data: dict):
    """Update user and invalidate cache."""
    await db.update_user(user_id, user_data)
    await cache.delete(f"user:{user_id}")
    # Or update cache immediately
    await cache.set(f"user:{user_id}", user_data, ttl=3600)
```

## References

- [Redis Caching Patterns](https://redis.io/docs/manual/patterns/)
- [Redis Performance Optimization](https://redis.io/docs/manual/optimization/)
- [redis-py Documentation](https://redis-py.readthedocs.io/)
- [Caching Strategies Best Practices](./caching-strategies-best-practices-2025.md)
- [Redis Cluster Best Practices](./redis-cluster-best-practices.md)
