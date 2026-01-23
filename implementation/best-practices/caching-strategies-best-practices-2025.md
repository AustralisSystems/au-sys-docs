# Caching Strategies Best Practices

**Version**: v1.0.0
**Last Updated**: 2025-01-14

This document provides comprehensive best practices for implementing caching strategies in FastAPI applications, covering multi-level caching, cache invalidation, cache warming, Redis patterns, cache decorators, cache key design, cache coherency, distributed caching, and cache metrics.

---

## Table of Contents

1. [Architecture Principles](#architecture-principles)
2. [Multi-Level Caching](#multi-level-caching)
3. [Cache Invalidation Strategies](#cache-invalidation-strategies)
4. [Cache Warming Patterns](#cache-warming-patterns)
5. [Redis Caching Patterns](#redis-caching-patterns)
6. [Cache Decorators and Patterns](#cache-decorators-and-patterns)
7. [Cache Key Design](#cache-key-design)
8. [Cache Coherency](#cache-coherency)
9. [Distributed Caching](#distributed-caching)
10. [Cache Metrics and Monitoring](#cache-metrics-and-monitoring)
11. [FastAPI Integration](#fastapi-integration)
12. [Performance Considerations](#performance-considerations)
13. [Production Deployment](#production-deployment)

---

## Architecture Principles

### Cache-Aside Pattern

**RECOMMENDED**: Use cache-aside (lazy loading) as the default pattern:

```python
async def get_user(user_id: int) -> User:
    """Get user with cache-aside pattern."""
    # Try cache first
    cache_key = f"user:{user_id}"
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

### Read-Through Pattern

**RECOMMENDED**: Use read-through for frequently accessed data:

```python
class ReadThroughCache:
    """Read-through cache implementation."""

    def __init__(self, cache_backend, data_source):
        self.cache = cache_backend
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

### Write-Through Pattern

**RECOMMENDED**: Use write-through for critical data consistency:

```python
class WriteThroughCache:
    """Write-through cache implementation."""

    def __init__(self, cache_backend, data_source):
        self.cache = cache_backend
        self.data_source = data_source

    async def set(self, key: str, value: Any, ttl: int = None) -> None:
        """Set value in both cache and data source."""
        # Write to data source first
        await self.data_source.save(key, value)

        # Then update cache
        await self.cache.set(key, value, ttl=ttl)
```

### Write-Behind Pattern

**ADVANCED**: Use write-behind for high-throughput write scenarios:

```python
import asyncio
from collections import deque

class WriteBehindCache:
    """Write-behind cache with batching."""

    def __init__(self, cache_backend, data_source, batch_size: int = 100):
        self.cache = cache_backend
        self.data_source = data_source
        self.batch_size = batch_size
        self.write_queue = deque()
        self._write_task = None

    async def set(self, key: str, value: Any, ttl: int = None) -> None:
        """Set value in cache immediately, queue for persistence."""
        # Write to cache immediately
        await self.cache.set(key, value, ttl=ttl)

        # Queue for background persistence
        self.write_queue.append((key, value))

        # Flush if queue is full
        if len(self.write_queue) >= self.batch_size:
            await self._flush_writes()

    async def _flush_writes(self) -> None:
        """Flush queued writes to data source."""
        if not self.write_queue:
            return

        batch = []
        while self.write_queue and len(batch) < self.batch_size:
            batch.append(self.write_queue.popleft())

        # Batch write to data source
        await self.data_source.batch_save(batch)
```

---

## Multi-Level Caching

### Three-Level Cache Architecture

**RECOMMENDED**: Implement L1 (memory), L2 (disk), L3 (distributed) caching:

```python
from typing import Optional, Any
import asyncio
import time

class MultiLevelCache:
    """Three-level cache with intelligent promotion/demotion."""

    def __init__(
        self,
        l1_cache: Any,  # In-memory cache (fastest)
        l2_cache: Any,  # Disk cache (persistent)
        l3_cache: Any,  # Distributed cache (Redis)
    ):
        self.l1_cache = l1_cache
        self.l2_cache = l2_cache
        self.l3_cache = l3_cache

        # Promotion thresholds
        self.l2_to_l1_threshold = 3  # Access count to promote L2 → L1
        self.l3_to_l2_threshold = 5  # Access count to promote L3 → L2

    async def get(self, key: str) -> Optional[Any]:
        """Get value from multi-level cache with automatic promotion."""
        # Try L1 (fastest)
        value = await self.l1_cache.get(key)
        if value is not None:
            return value

        # Try L2 (persistent)
        l2_entry = await self.l2_cache.get(key)
        if l2_entry is not None:
            # Promote to L1 if frequently accessed
            if l2_entry.access_count >= self.l2_to_l1_threshold:
                await self.l1_cache.set(key, l2_entry.value, ttl=l2_entry.ttl)

            return l2_entry.value

        # Try L3 (distributed)
        l3_entry = await self.l3_cache.get(key)
        if l3_entry is not None:
            # Promote to L2 if frequently accessed
            if l3_entry.access_count >= self.l3_to_l2_threshold:
                await self.l2_cache.set(key, l3_entry.value, ttl=l3_entry.ttl)

            return l3_entry.value

        return None

    async def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        """Set value in all cache levels."""
        # Store in all levels
        await asyncio.gather(
            self.l1_cache.set(key, value, ttl=ttl),
            self.l2_cache.set(key, value, ttl=ttl),
            self.l3_cache.set(key, value, ttl=ttl),
        )
```

### L1 Memory Cache

**REQUIRED**: Implement fast in-memory cache:

```python
from collections import OrderedDict
import asyncio
import time

class L1MemoryCache:
    """L1 in-memory cache with LRU eviction."""

    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[CacheEntry]:
        """Get entry from L1 cache."""
        async with self._lock:
            if key not in self._cache:
                return None

            entry = self._cache.pop(key)

            # Check expiration
            if entry.is_expired():
                return None

            # Update access time and move to end (most recently used)
            entry.last_accessed = time.time()
            entry.access_count += 1
            self._cache[key] = entry

            return entry

    async def set(self, entry: CacheEntry) -> None:
        """Set entry in L1 cache."""
        async with self._lock:
            # Evict if at capacity
            if len(self._cache) >= self.max_size and entry.key not in self._cache:
                # Remove least recently used
                self._cache.popitem(last=False)

            self._cache[entry.key] = entry
```

### L2 Disk Cache

**RECOMMENDED**: Implement persistent disk cache:

```python
import sqlite3
import pickle
import hashlib
from pathlib import Path
from typing import Optional

class L2DiskCache:
    """L2 disk cache with SQLite backend."""

    def __init__(self, cache_dir: str, max_size: int = 10000):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.cache_dir / "cache_index.db"
        self.max_size = max_size
        self._init_db()

    def _init_db(self) -> None:
        """Initialize SQLite database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cache_entries (
                    key TEXT PRIMARY KEY,
                    file_path TEXT NOT NULL,
                    expires_at REAL NOT NULL,
                    created_at REAL NOT NULL,
                    last_accessed REAL NOT NULL,
                    access_count INTEGER DEFAULT 0,
                    size INTEGER DEFAULT 0
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_expires_at ON cache_entries(expires_at)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_last_accessed ON cache_entries(last_accessed)")

    async def get(self, key: str) -> Optional[CacheEntry]:
        """Get entry from L2 disk cache."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT file_path, expires_at, created_at, last_accessed, access_count, size "
                "FROM cache_entries WHERE key = ?",
                (key,)
            )
            row = cursor.fetchone()

            if not row:
                return None

            file_path, expires_at, created_at, last_accessed, access_count, size = row

            # Check expiration
            if time.time() > expires_at:
                await self.delete(key)
                return None

            # Load value from file
            cache_file = self.cache_dir / file_path
            try:
                with open(cache_file, "rb") as f:
                    value = pickle.load(f)

                # Update access statistics
                conn.execute(
                    "UPDATE cache_entries SET last_accessed = ?, access_count = ? WHERE key = ?",
                    (time.time(), access_count + 1, key)
                )

                return CacheEntry(
                    key=key,
                    value=value,
                    expires_at=expires_at,
                    created_at=created_at,
                    last_accessed=time.time(),
                    access_count=access_count + 1,
                    size=size,
                )
            except Exception as e:
                self.logger.error(f"Failed to load L2 cache entry {key}: {e}")
                await self.delete(key)
                return None

    async def set(self, entry: CacheEntry) -> None:
        """Set entry in L2 disk cache."""
        # Generate file path
        file_hash = hashlib.md5(entry.key.encode()).hexdigest()
        file_path = f"{file_hash[:2]}/{file_hash}.cache"
        cache_file = self.cache_dir / file_path
        cache_file.parent.mkdir(parents=True, exist_ok=True)

        # Save value to file
        try:
            with open(cache_file, "wb") as f:
                pickle.dump(entry.value, f)

            # Update database
            with sqlite3.connect(self.db_path) as conn:
                # Check if we need to evict
                current_size = conn.execute("SELECT COUNT(*) FROM cache_entries").fetchone()[0]
                if current_size >= self.max_size and entry.key not in self._get_existing_keys(conn):
                    await self._evict_lru(conn)

                conn.execute(
                    """
                    INSERT OR REPLACE INTO cache_entries
                    (key, file_path, expires_at, created_at, last_accessed, access_count, size)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        entry.key,
                        file_path,
                        entry.expires_at,
                        entry.created_at,
                        entry.last_accessed,
                        entry.access_count,
                        entry.size,
                    )
                )
        except Exception as e:
            self.logger.error(f"Failed to save L2 cache entry {entry.key}: {e}")

    async def _evict_lru(self, conn: sqlite3.Connection) -> None:
        """Evict least recently used entry."""
        cursor = conn.execute(
            "SELECT key, file_path FROM cache_entries ORDER BY last_accessed ASC LIMIT 1"
        )
        row = cursor.fetchone()

        if row:
            key, file_path = row
            # Delete file
            cache_file = self.cache_dir / file_path
            cache_file.unlink(missing_ok=True)

            # Delete from database
            conn.execute("DELETE FROM cache_entries WHERE key = ?", (key,))
```

### L3 Distributed Cache (Redis)

**REQUIRED**: Implement distributed cache with Redis:

```python
import redis.asyncio as redis
from typing import Optional, Any
import json
import pickle

class L3RedisCache:
    """L3 distributed cache using Redis."""

    def __init__(self, redis_url: str, namespace: str = "app"):
        self.redis_client = redis.from_url(redis_url, decode_responses=False)
        self.namespace = namespace

    def _make_key(self, key: str) -> str:
        """Create namespaced cache key."""
        return f"{self.namespace}:{key}"

    async def get(self, key: str) -> Optional[CacheEntry]:
        """Get entry from Redis cache."""
        redis_key = self._make_key(key)

        # Get value and metadata
        value_data = await self.redis_client.get(redis_key)
        if value_data is None:
            return None

        # Get metadata from hash
        metadata = await self.redis_client.hgetall(f"{redis_key}:meta")

        if not metadata:
            return None

        # Deserialize value
        value = pickle.loads(value_data)

        # Check expiration
        expires_at = float(metadata.get(b"expires_at", b"0").decode())
        if time.time() > expires_at:
            await self.delete(key)
            return None

        # Update access statistics
        access_count = int(metadata.get(b"access_count", b"0").decode()) + 1
        await self.redis_client.hset(
            f"{redis_key}:meta",
            mapping={
                "last_accessed": str(time.time()),
                "access_count": str(access_count),
            }
        )

        return CacheEntry(
            key=key,
            value=value,
            expires_at=expires_at,
            created_at=float(metadata.get(b"created_at", b"0").decode()),
            last_accessed=time.time(),
            access_count=access_count,
            size=len(value_data),
        )

    async def set(self, entry: CacheEntry, ttl: int = None) -> None:
        """Set entry in Redis cache."""
        redis_key = self._make_key(entry.key)
        ttl = ttl or int(entry.expires_at - time.time())

        # Serialize value
        value_data = pickle.dumps(entry.value)

        # Store value with expiration
        await self.redis_client.setex(redis_key, ttl, value_data)

        # Store metadata in hash
        await self.redis_client.hset(
            f"{redis_key}:meta",
            mapping={
                "expires_at": str(entry.expires_at),
                "created_at": str(entry.created_at),
                "last_accessed": str(entry.last_accessed),
                "access_count": str(entry.access_count),
                "size": str(entry.size),
            }
        )
        await self.redis_client.expire(f"{redis_key}:meta", ttl)
```

### Intelligent Promotion/Demotion

**RECOMMENDED**: Implement automatic promotion based on access patterns:

```python
class IntelligentCachePromotion:
    """Intelligent cache promotion based on access patterns."""

    def __init__(self, multi_level_cache: MultiLevelCache):
        self.cache = multi_level_cache
        self.promotion_threshold = 3  # Access count threshold
        self.demotion_threshold = 100  # Time since last access (seconds)

    async def promote_if_needed(self, key: str, entry: CacheEntry) -> None:
        """Promote entry to higher cache level if frequently accessed."""
        if entry.level == 3 and entry.access_count >= self.promotion_threshold:
            # Promote L3 → L2
            await self.cache.l2_cache.set(entry)
            self.logger.info(f"Promoted {key} from L3 to L2")

        elif entry.level == 2 and entry.access_count >= self.promotion_threshold:
            # Promote L2 → L1
            await self.cache.l1_cache.set(entry)
            self.logger.info(f"Promoted {key} from L2 to L1")

    async def demote_if_needed(self, key: str, entry: CacheEntry) -> None:
        """Demote entry to lower cache level if rarely accessed."""
        time_since_access = time.time() - entry.last_accessed

        if entry.level == 1 and time_since_access > self.demotion_threshold:
            # Demote L1 → L2 (keep in L2, remove from L1)
            await self.cache.l1_cache.delete(key)
            self.logger.info(f"Demoted {key} from L1 to L2")
```

---

## Cache Invalidation Strategies

### Time-Based Expiration (TTL)

**MANDATORY**: Use TTL for automatic expiration:

```python
import time
from datetime import datetime, timedelta

class TTLCache:
    """Cache with time-to-live expiration."""

    def __init__(self, default_ttl: int = 3600):
        self.default_ttl = default_ttl
        self._cache: Dict[str, CacheEntry] = {}

    async def get(self, key: str) -> Optional[Any]:
        """Get value if not expired."""
        entry = self._cache.get(key)

        if entry is None:
            return None

        # Check expiration
        if entry.is_expired():
            del self._cache[key]
            return None

        return entry.value

    async def set(self, key: str, value: Any, ttl: int = None) -> None:
        """Set value with TTL."""
        ttl = ttl or self.default_ttl
        expires_at = time.time() + ttl

        self._cache[key] = CacheEntry(
            key=key,
            value=value,
            expires_at=expires_at,
            created_at=time.time(),
        )
```

### Tag-Based Invalidation

**RECOMMENDED**: Use tags for bulk invalidation:

```python
from collections import defaultdict
from typing import Set, Dict

class TagBasedCache:
    """Cache with tag-based invalidation."""

    def __init__(self):
        self._cache: Dict[str, CacheEntry] = {}
        self._tag_index: Dict[str, Set[str]] = defaultdict(set)  # tag → keys
        self._key_tags: Dict[str, Set[str]] = {}  # key → tags

    async def set(self, key: str, value: Any, tags: Set[str] = None, ttl: int = None) -> None:
        """Set value with tags."""
        # Remove old tags if key exists
        if key in self._key_tags:
            old_tags = self._key_tags[key]
            for tag in old_tags:
                self._tag_index[tag].discard(key)

        # Set new tags
        tags = tags or set()
        self._key_tags[key] = tags
        for tag in tags:
            self._tag_index[tag].add(key)

        # Store entry
        self._cache[key] = CacheEntry(
            key=key,
            value=value,
            tags=tags,
            expires_at=time.time() + (ttl or 3600),
        )

    async def invalidate_by_tag(self, tag: str) -> int:
        """Invalidate all keys with given tag."""
        keys_to_invalidate = self._tag_index.get(tag, set()).copy()

        count = 0
        for key in keys_to_invalidate:
            if await self.delete(key):
                count += 1

        # Clean up tag index
        del self._tag_index[tag]

        return count

    async def invalidate_by_tags(self, tags: Set[str]) -> int:
        """Invalidate all keys with any of the given tags."""
        keys_to_invalidate = set()

        for tag in tags:
            keys_to_invalidate.update(self._tag_index.get(tag, set()))

        count = 0
        for key in keys_to_invalidate:
            if await self.delete(key):
                count += 1

        return count
```

### Dependency-Based Invalidation

**RECOMMENDED**: Track dependencies for cascading invalidation:

```python
from collections import defaultdict
from typing import Set, Dict

class DependencyTrackingCache:
    """Cache with dependency tracking for cascading invalidation."""

    def __init__(self):
        self._cache: Dict[str, CacheEntry] = {}
        self._dependencies: Dict[str, Set[str]] = {}  # key → dependencies
        self._reverse_deps: Dict[str, Set[str]] = defaultdict(set)  # dep → dependents

    async def set(
        self,
        key: str,
        value: Any,
        dependencies: Set[str] = None,
        ttl: int = None
    ) -> None:
        """Set value with dependencies."""
        # Remove old dependencies
        if key in self._dependencies:
            old_deps = self._dependencies[key]
            for dep in old_deps:
                self._reverse_deps[dep].discard(key)

        # Set new dependencies
        dependencies = dependencies or set()
        self._dependencies[key] = dependencies
        for dep in dependencies:
            self._reverse_deps[dep].add(key)

        # Store entry
        self._cache[key] = CacheEntry(
            key=key,
            value=value,
            dependencies=dependencies,
            expires_at=time.time() + (ttl or 3600),
        )

    async def invalidate(self, key: str, cascade: bool = True) -> int:
        """Invalidate key and optionally cascade to dependents."""
        count = 0

        # Delete the key itself
        if key in self._cache:
            del self._cache[key]
            count += 1

        # Cascade to dependents
        if cascade:
            dependents = self._reverse_deps.get(key, set()).copy()
            for dependent in dependents:
                count += await self.invalidate(dependent, cascade=True)

        # Clean up dependency tracking
        if key in self._dependencies:
            deps = self._dependencies.pop(key)
            for dep in deps:
                self._reverse_deps[dep].discard(key)

        return count
```

### Pattern-Based Invalidation

**RECOMMENDED**: Support pattern-based invalidation:

```python
import fnmatch
from typing import List

class PatternBasedCache:
    """Cache with pattern-based invalidation."""

    def __init__(self):
        self._cache: Dict[str, CacheEntry] = {}

    async def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate all keys matching pattern."""
        matching_keys = [
            key for key in self._cache.keys()
            if fnmatch.fnmatch(key, pattern)
        ]

        count = 0
        for key in matching_keys:
            if await self.delete(key):
                count += 1

        return count

    async def invalidate_prefix(self, prefix: str) -> int:
        """Invalidate all keys with given prefix."""
        matching_keys = [
            key for key in self._cache.keys()
            if key.startswith(prefix)
        ]

        count = 0
        for key in matching_keys:
            if await self.delete(key):
                count += 1

        return count
```

### Event-Based Invalidation

**RECOMMENDED**: Use events for reactive invalidation:

```python
from typing import Callable, List
import asyncio

class EventBasedCache:
    """Cache with event-based invalidation."""

    def __init__(self):
        self._cache: Dict[str, CacheEntry] = {}
        self._event_handlers: Dict[str, List[Callable]] = defaultdict(list)

    def on_invalidation_event(self, event_type: str, handler: Callable) -> None:
        """Register handler for invalidation events."""
        self._event_handlers[event_type].append(handler)

    async def invalidate_on_event(self, event_type: str, key_pattern: str = None) -> int:
        """Invalidate cache based on event."""
        # Get handlers for this event type
        handlers = self._event_handlers.get(event_type, [])

        # Execute handlers
        for handler in handlers:
            await handler(event_type, key_pattern)

        # Pattern-based invalidation if pattern provided
        if key_pattern:
            return await self.invalidate_pattern(key_pattern)

        return 0

    # Example: Invalidate on database update
    async def on_database_update(self, table: str, record_id: str) -> None:
        """Handle database update event."""
        # Invalidate related cache keys
        patterns = [
            f"{table}:{record_id}:*",
            f"{table}:list:*",
            f"{table}:*",
        ]

        for pattern in patterns:
            await self.invalidate_pattern(pattern)
```

---

## Cache Warming Patterns

### Preload Strategy

**RECOMMENDED**: Preload frequently accessed data:

```python
class CacheWarmer:
    """Cache warming service."""

    def __init__(self, cache: MultiLevelCache, data_source: Any):
        self.cache = cache
        self.data_source = data_source
        self.warming_keys: Set[str] = set()

    async def warm_cache(self, keys: List[str]) -> Dict[str, bool]:
        """Warm cache with given keys."""
        results = {}

        for key in keys:
            try:
                # Load from data source
                value = await self.data_source.load(key)

                if value is not None:
                    # Store in cache
                    await self.cache.set(key, value, ttl=3600)
                    results[key] = True
                else:
                    results[key] = False
            except Exception as e:
                self.logger.error(f"Failed to warm cache for {key}: {e}")
                results[key] = False

        return results

    async def warm_frequently_accessed(self) -> None:
        """Warm cache with frequently accessed items."""
        # Get list of frequently accessed keys from metrics
        frequent_keys = await self.data_source.get_frequent_keys(limit=100)

        # Warm cache
        await self.warm_cache(frequent_keys)
```

### Background Warming

**RECOMMENDED**: Warm cache in background tasks:

```python
import asyncio
from datetime import datetime, timedelta

class BackgroundCacheWarmer:
    """Background cache warming service."""

    def __init__(self, cache: MultiLevelCache, data_source: Any, interval: int = 300):
        self.cache = cache
        self.data_source = data_source
        self.interval = interval
        self._warming_task: Optional[asyncio.Task] = None
        self._running = False

    async def start(self) -> None:
        """Start background warming."""
        self._running = True
        self._warming_task = asyncio.create_task(self._warming_loop())

    async def stop(self) -> None:
        """Stop background warming."""
        self._running = False
        if self._warming_task:
            self._warming_task.cancel()
            try:
                await self._warming_task
            except asyncio.CancelledError:
                pass

    async def _warming_loop(self) -> None:
        """Background warming loop."""
        while self._running:
            try:
                # Get keys that need warming
                keys_to_warm = await self._get_keys_to_warm()

                # Warm cache
                await self.cache.warm_cache(keys_to_warm)

                # Wait for next interval
                await asyncio.sleep(self.interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in cache warming loop: {e}")
                await asyncio.sleep(self.interval)

    async def _get_keys_to_warm(self) -> List[str]:
        """Get list of keys that should be warmed."""
        # Get frequently accessed keys
        frequent = await self.data_source.get_frequent_keys(limit=50)

        # Get keys about to expire
        expiring = await self.cache.get_expiring_keys(limit=50, time_window=300)

        # Combine and deduplicate
        return list(set(frequent + expiring))
```

### Predictive Warming

**ADVANCED**: Use predictive algorithms for cache warming:

```python
from collections import defaultdict
from datetime import datetime, timedelta

class PredictiveCacheWarmer:
    """Predictive cache warming based on access patterns."""

    def __init__(self, cache: MultiLevelCache, data_source: Any):
        self.cache = cache
        self.data_source = data_source
        self.access_patterns: Dict[str, List[datetime]] = defaultdict(list)
        self.pattern_window = timedelta(hours=24)

    def record_access(self, key: str) -> None:
        """Record cache access for pattern analysis."""
        self.access_patterns[key].append(datetime.now())

        # Keep only recent accesses
        cutoff = datetime.now() - self.pattern_window
        self.access_patterns[key] = [
            ts for ts in self.access_patterns[key]
            if ts > cutoff
        ]

    async def predict_and_warm(self) -> List[str]:
        """Predict keys that will be accessed and warm them."""
        predictions = []

        for key, access_times in self.access_patterns.items():
            # Analyze access pattern
            if self._will_be_accessed_soon(key, access_times):
                predictions.append(key)

        # Warm predicted keys
        if predictions:
            await self.cache.warm_cache(predictions[:100])  # Limit to 100

        return predictions

    def _will_be_accessed_soon(self, key: str, access_times: List[datetime]) -> bool:
        """Predict if key will be accessed soon based on pattern."""
        if len(access_times) < 3:
            return False

        # Calculate average interval between accesses
        intervals = [
            (access_times[i+1] - access_times[i]).total_seconds()
            for i in range(len(access_times) - 1)
        ]

        avg_interval = sum(intervals) / len(intervals)

        # Check if next access is expected soon
        last_access = access_times[-1]
        time_since_last = (datetime.now() - last_access).total_seconds()

        # Predict access if we're within 20% of average interval
        return time_since_last >= avg_interval * 0.8
```

---

## Redis Caching Patterns

### Basic Redis Operations

**REQUIRED**: Use Redis for distributed caching:

```python
import redis.asyncio as redis
from typing import Optional, Any
import json
import pickle

class RedisCache:
    """Redis-based cache implementation."""

    def __init__(self, redis_url: str, namespace: str = "app"):
        self.redis_client = redis.from_url(redis_url, decode_responses=False)
        self.namespace = namespace

    def _make_key(self, key: str) -> str:
        """Create namespaced cache key."""
        return f"{self.namespace}:{key}"

    async def get(self, key: str) -> Optional[Any]:
        """Get value from Redis."""
        redis_key = self._make_key(key)
        data = await self.redis_client.get(redis_key)

        if data is None:
            return None

        # Deserialize
        return pickle.loads(data)

    async def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        """Set value in Redis with TTL."""
        redis_key = self._make_key(key)
        data = pickle.dumps(value)

        await self.redis_client.setex(redis_key, ttl, data)

    async def delete(self, key: str) -> bool:
        """Delete key from Redis."""
        redis_key = self._make_key(key)
        result = await self.redis_client.delete(redis_key)
        return result > 0

    async def exists(self, key: str) -> bool:
        """Check if key exists."""
        redis_key = self._make_key(key)
        return await self.redis_client.exists(redis_key) > 0
```

### Redis Hash Operations

**RECOMMENDED**: Use Redis hashes for structured data:

```python
class RedisHashCache:
    """Redis hash-based cache for structured data."""

    def __init__(self, redis_client: redis.Redis, namespace: str = "app"):
        self.redis_client = redis_client
        self.namespace = namespace

    def _make_key(self, key: str) -> str:
        """Create namespaced hash key."""
        return f"{self.namespace}:hash:{key}"

    async def get_field(self, key: str, field: str) -> Optional[Any]:
        """Get specific field from hash."""
        hash_key = self._make_key(key)
        data = await self.redis_client.hget(hash_key, field)

        if data is None:
            return None

        return pickle.loads(data)

    async def set_field(self, key: str, field: str, value: Any) -> None:
        """Set field in hash."""
        hash_key = self._make_key(key)
        data = pickle.dumps(value)

        await self.redis_client.hset(hash_key, field, data)

    async def get_all(self, key: str) -> Dict[str, Any]:
        """Get all fields from hash."""
        hash_key = self._make_key(key)
        data = await self.redis_client.hgetall(hash_key)

        result = {}
        for field, value in data.items():
            result[field.decode()] = pickle.loads(value)

        return result

    async def set_mapping(self, key: str, mapping: Dict[str, Any], ttl: int = None) -> None:
        """Set multiple fields at once."""
        hash_key = self._make_key(key)

        # Serialize all values
        serialized = {
            field: pickle.dumps(value)
            for field, value in mapping.items()
        }

        await self.redis_client.hset(hash_key, mapping=serialized)

        if ttl:
            await self.redis_client.expire(hash_key, ttl)
```

### Redis Pipeline Operations

**RECOMMENDED**: Use pipelines for batch operations:

```python
class RedisPipelineCache:
    """Redis cache with pipeline support."""

    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client

    async def mget(self, keys: List[str]) -> Dict[str, Optional[Any]]:
        """Get multiple keys efficiently."""
        if not keys:
            return {}

        # Use pipeline for batch get
        pipe = self.redis_client.pipeline()
        for key in keys:
            pipe.get(key)

        results = await pipe.execute()

        # Deserialize and build result dict
        result = {}
        for key, data in zip(keys, results):
            if data is not None:
                result[key] = pickle.loads(data)
            else:
                result[key] = None

        return result

    async def mset(self, items: Dict[str, Any], ttl: int = None) -> None:
        """Set multiple keys efficiently."""
        if not items:
            return

        pipe = self.redis_client.pipeline()

        for key, value in items.items():
            data = pickle.dumps(value)
            pipe.setex(key, ttl or 3600, data)

        await pipe.execute()

    async def mdelete(self, keys: List[str]) -> int:
        """Delete multiple keys efficiently."""
        if not keys:
            return 0

        pipe = self.redis_client.pipeline()
        for key in keys:
            pipe.delete(key)

        results = await pipe.execute()
        return sum(results)
```

### Redis Pub/Sub for Invalidation

**RECOMMENDED**: Use Redis Pub/Sub for distributed invalidation:

```python
import asyncio

class RedisPubSubInvalidation:
    """Redis Pub/Sub based cache invalidation."""

    def __init__(self, redis_client: redis.Redis, cache: RedisCache):
        self.redis_client = redis_client
        self.cache = cache
        self.pubsub = redis_client.pubsub()
        self._listener_task: Optional[asyncio.Task] = None

    async def start_listening(self) -> None:
        """Start listening for invalidation events."""
        await self.pubsub.subscribe("cache:invalidate")
        self._listener_task = asyncio.create_task(self._listen())

    async def stop_listening(self) -> None:
        """Stop listening for invalidation events."""
        await self.pubsub.unsubscribe("cache:invalidate")
        if self._listener_task:
            self._listener_task.cancel()
            try:
                await self._listener_task
            except asyncio.CancelledError:
                pass

    async def _listen(self) -> None:
        """Listen for invalidation messages."""
        async for message in self.pubsub.listen():
            if message["type"] == "message":
                data = json.loads(message["data"])
                await self._handle_invalidation(data)

    async def _handle_invalidation(self, data: Dict[str, Any]) -> None:
        """Handle invalidation message."""
        invalidation_type = data.get("type")

        if invalidation_type == "key":
            key = data.get("key")
            await self.cache.delete(key)

        elif invalidation_type == "pattern":
            pattern = data.get("pattern")
            await self.cache.invalidate_pattern(pattern)

        elif invalidation_type == "tag":
            tag = data.get("tag")
            await self.cache.invalidate_by_tag(tag)

    async def publish_invalidation(self, invalidation_type: str, **kwargs) -> None:
        """Publish invalidation event."""
        message = {
            "type": invalidation_type,
            **kwargs,
        }

        await self.redis_client.publish(
            "cache:invalidate",
            json.dumps(message)
        )
```

### Redis Connection Pooling

**REQUIRED**: Use connection pooling for performance:

```python
import redis.asyncio as redis

class RedisPoolCache:
    """Redis cache with connection pooling."""

    def __init__(self, redis_url: str, max_connections: int = 50):
        # Create connection pool
        self.pool = redis.ConnectionPool.from_url(
            redis_url,
            max_connections=max_connections,
            decode_responses=False,
        )

        # Create Redis client with pool
        self.redis_client = redis.Redis(connection_pool=self.pool)

    async def close(self) -> None:
        """Close connection pool."""
        await self.pool.aclose()
```

---

## Cache Decorators and Patterns

### Function Decorator Pattern

**RECOMMENDED**: Use decorators for automatic caching:

```python
from functools import wraps
from typing import Callable, Any, Optional
import hashlib
import json

def cache_decorator(
    ttl: int = 3600,
    key_prefix: str = "",
    cache_backend: Any = None,
):
    """Decorator for caching function results."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            # Generate cache key
            cache_key = _generate_cache_key(
                func.__name__,
                key_prefix,
                *args,
                **kwargs
            )

            # Try cache first
            if cache_backend:
                cached_value = await cache_backend.get(cache_key)
                if cached_value is not None:
                    return cached_value

            # Cache miss - execute function
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)

            # Store in cache
            if cache_backend and result is not None:
                await cache_backend.set(cache_key, result, ttl=ttl)

            return result

        def sync_wrapper(*args, **kwargs) -> Any:
            # Generate cache key
            cache_key = _generate_cache_key(
                func.__name__,
                key_prefix,
                *args,
                **kwargs
            )

            # Try cache first
            if cache_backend:
                # For sync functions, run cache operations in event loop
                loop = asyncio.get_event_loop()
                cached_value = loop.run_until_complete(
                    cache_backend.get(cache_key)
                )
                if cached_value is not None:
                    return cached_value

            # Cache miss - execute function
            result = func(*args, **kwargs)

            # Store in cache
            if cache_backend and result is not None:
                loop = asyncio.get_event_loop()
                loop.run_until_complete(
                    cache_backend.set(cache_key, result, ttl=ttl)
                )

            return result

        # Return appropriate wrapper
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator

def _generate_cache_key(
    func_name: str,
    prefix: str,
    *args,
    **kwargs
) -> str:
    """Generate cache key from function arguments."""
    # Serialize arguments
    key_parts = [func_name]
    key_parts.extend(str(arg) for arg in args)
    key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))

    key_string = f"{prefix}:{':'.join(key_parts)}"

    # Hash if too long
    if len(key_string) > 200:
        key_string = hashlib.sha256(key_string.encode()).hexdigest()

    return key_string
```

### Method Decorator Pattern

**RECOMMENDED**: Cache method results:

```python
from cachetools import cachedmethod, LRUCache, TTLCache

class CachedService:
    """Service with cached methods."""

    def __init__(self):
        # Shared cache for all methods
        self.shared_cache = LRUCache(maxsize=1000)

        # Method-specific caches
        self.user_cache = TTLCache(maxsize=100, ttl=3600)
        self.product_cache = TTLCache(maxsize=500, ttl=1800)

    @cachedmethod(lambda self: self.user_cache)
    async def get_user(self, user_id: int) -> User:
        """Get user with caching."""
        return await db.get_user(user_id)

    @cachedmethod(lambda self: self.product_cache)
    async def get_product(self, product_id: int) -> Product:
        """Get product with caching."""
        return await db.get_product(product_id)
```

### Conditional Caching

**RECOMMENDED**: Cache conditionally based on context:

```python
def conditional_cache(
    condition: Callable[[Any], bool],
    ttl: int = 3600,
    cache_backend: Any = None,
):
    """Decorator for conditional caching."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            # Check if caching is enabled
            if not condition(*args, **kwargs):
                # Execute without caching
                if asyncio.iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                else:
                    return func(*args, **kwargs)

            # Use standard caching
            cache_key = _generate_cache_key(func.__name__, "", *args, **kwargs)

            if cache_backend:
                cached_value = await cache_backend.get(cache_key)
                if cached_value is not None:
                    return cached_value

            # Execute function
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)

            # Store in cache
            if cache_backend and result is not None:
                await cache_backend.set(cache_key, result, ttl=ttl)

            return result

        return wrapper

    return decorator

# Usage example
@conditional_cache(
    condition=lambda user_id: user_id > 1000,  # Only cache users with ID > 1000
    ttl=3600,
    cache_backend=redis_cache
)
async def get_user(user_id: int) -> User:
    return await db.get_user(user_id)
```

### Cache Stampede Prevention

**REQUIRED**: Prevent cache stampedes with locking:

```python
import asyncio
from typing import Dict, Optional

class StampedePreventionCache:
    """Cache with stampede prevention."""

    def __init__(self, cache_backend: Any):
        self.cache = cache_backend
        self._locks: Dict[str, asyncio.Lock] = {}
        self._pending_requests: Dict[str, asyncio.Event] = {}

    async def get_or_set(
        self,
        key: str,
        factory: Callable[[], Awaitable[Any]],
        ttl: int = 3600
    ) -> Any:
        """Get from cache or set using factory with stampede prevention."""
        # Try cache first
        value = await self.cache.get(key)
        if value is not None:
            return value

        # Get or create lock for this key
        if key not in self._locks:
            self._locks[key] = asyncio.Lock()

        lock = self._locks[key]

        async with lock:
            # Double-check cache (another request might have set it)
            value = await self.cache.get(key)
            if value is not None:
                return value

            # Check if another request is already computing
            if key in self._pending_requests:
                # Wait for pending request
                event = self._pending_requests[key]
                await event.wait()

                # Try cache again
                value = await self.cache.get(key)
                if value is not None:
                    return value

            # Create event for other requests
            event = asyncio.Event()
            self._pending_requests[key] = event

            try:
                # Compute value
                value = await factory()

                # Store in cache
                if value is not None:
                    await self.cache.set(key, value, ttl=ttl)

                return value
            finally:
                # Notify waiting requests
                event.set()
                del self._pending_requests[key]
```

---

## Cache Key Design

### Key Naming Conventions

**MANDATORY**: Use consistent key naming:

```python
class CacheKeyBuilder:
    """Builder for consistent cache keys."""

    @staticmethod
    def build_key(
        resource_type: str,
        resource_id: str,
        action: str = None,
        **kwargs
    ) -> str:
        """Build cache key with consistent format."""
        parts = [resource_type, resource_id]

        if action:
            parts.append(action)

        if kwargs:
            sorted_kwargs = sorted(kwargs.items())
            parts.extend(f"{k}={v}" for k, v in sorted_kwargs)

        return ":".join(parts)

    @staticmethod
    def user_key(user_id: int) -> str:
        """Build user cache key."""
        return CacheKeyBuilder.build_key("user", str(user_id))

    @staticmethod
    def user_list_key(page: int, per_page: int) -> str:
        """Build user list cache key."""
        return CacheKeyBuilder.build_key(
            "user",
            "list",
            action="page",
            page=str(page),
            per_page=str(per_page)
        )

    @staticmethod
    def product_key(product_id: int, variant: str = None) -> str:
        """Build product cache key."""
        key = CacheKeyBuilder.build_key("product", str(product_id))
        if variant:
            key += f":variant:{variant}"
        return key

# Usage
user_key = CacheKeyBuilder.user_key(123)
# Result: "user:123"

list_key = CacheKeyBuilder.user_list_key(page=1, per_page=20)
# Result: "user:list:page:page=1:per_page=20"
```

### Key Hashing

**REQUIRED**: Hash long keys to prevent issues:

```python
import hashlib

def hash_cache_key(key: str, max_length: int = 200) -> str:
    """Hash cache key if too long."""
    if len(key) <= max_length:
        return key

    # Hash long keys
    return hashlib.sha256(key.encode()).hexdigest()
```

### Namespace Isolation

**REQUIRED**: Use namespaces to isolate cache data:

```python
class NamespacedCache:
    """Cache with namespace isolation."""

    def __init__(self, cache_backend: Any, namespace: str = "app"):
        self.cache = cache_backend
        self.namespace = namespace

    def _make_key(self, key: str) -> str:
        """Create namespaced key."""
        return f"{self.namespace}:{key}"

    async def get(self, key: str) -> Any:
        """Get with namespace."""
        return await self.cache.get(self._make_key(key))

    async def set(self, key: str, value: Any, ttl: int = None) -> None:
        """Set with namespace."""
        await self.cache.set(self._make_key(key), value, ttl=ttl)

    async def clear_namespace(self) -> int:
        """Clear all keys in namespace."""
        pattern = f"{self.namespace}:*"
        return await self.cache.invalidate_pattern(pattern)
```

---

## Cache Coherency

### Cache Versioning

**RECOMMENDED**: Use versioning for cache invalidation:

```python
class VersionedCache:
    """Cache with versioning for coherency."""

    def __init__(self, cache_backend: Any):
        self.cache = cache_backend
        self._versions: Dict[str, int] = {}

    def _versioned_key(self, key: str) -> str:
        """Create versioned cache key."""
        version = self._versions.get(key, 1)
        return f"{key}:v{version}"

    async def get(self, key: str) -> Optional[Any]:
        """Get value using versioned key."""
        versioned_key = self._versioned_key(key)
        return await self.cache.get(versioned_key)

    async def set(self, key: str, value: Any, ttl: int = None) -> None:
        """Set value with versioned key."""
        versioned_key = self._versioned_key(key)
        await self.cache.set(versioned_key, value, ttl=ttl)

    async def invalidate(self, key: str) -> None:
        """Invalidate by incrementing version."""
        self._versions[key] = self._versions.get(key, 1) + 1

        # Old versioned key will expire naturally
        # New requests will use new version
```

### Cache Consistency Checks

**RECOMMENDED**: Implement consistency checks:

```python
class ConsistentCache:
    """Cache with consistency checking."""

    def __init__(self, cache_backend: Any, data_source: Any):
        self.cache = cache_backend
        self.data_source = data_source

    async def get_with_validation(
        self,
        key: str,
        validate: Callable[[Any], bool] = None
    ) -> Optional[Any]:
        """Get value with consistency validation."""
        cached_value = await self.cache.get(key)

        if cached_value is None:
            return None

        # Validate consistency if validator provided
        if validate and not validate(cached_value):
            # Invalidate and reload
            await self.cache.delete(key)
            return None

        return cached_value

    async def get_or_reload(self, key: str) -> Any:
        """Get from cache or reload from source."""
        cached_value = await self.cache.get(key)

        if cached_value is not None:
            # Verify with source (lightweight check)
            if await self.data_source.exists(key):
                return cached_value
            else:
                # Source says it doesn't exist - invalidate cache
                await self.cache.delete(key)
                return None

        # Reload from source
        value = await self.data_source.load(key)

        if value is not None:
            await self.cache.set(key, value, ttl=3600)

        return value
```

---

## Distributed Caching

### Redis Cluster Support

**RECOMMENDED**: Support Redis Cluster for scalability:

```python
from redis.cluster import RedisCluster

class RedisClusterCache:
    """Redis Cluster cache implementation."""

    def __init__(self, startup_nodes: List[Dict[str, str]]):
        self.cluster = RedisCluster(
            startup_nodes=startup_nodes,
            decode_responses=False,
            skip_full_coverage_check=True,
        )

    async def get(self, key: str) -> Optional[Any]:
        """Get value from Redis Cluster."""
        data = await self.cluster.get(key)
        if data is None:
            return None
        return pickle.loads(data)

    async def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        """Set value in Redis Cluster."""
        data = pickle.dumps(value)
        await self.cluster.setex(key, ttl, data)
```

### Cache Replication

**ADVANCED**: Implement cache replication:

```python
class ReplicatedCache:
    """Cache with replication support."""

    def __init__(self, primary_cache: Any, replica_caches: List[Any]):
        self.primary = primary_cache
        self.replicas = replica_caches

    async def get(self, key: str) -> Optional[Any]:
        """Get from primary, fallback to replicas."""
        # Try primary first
        value = await self.primary.get(key)
        if value is not None:
            return value

        # Try replicas
        for replica in self.replicas:
            value = await replica.get(key)
            if value is not None:
                # Promote to primary
                await self.primary.set(key, value, ttl=3600)
                return value

        return None

    async def set(self, key: str, value: Any, ttl: int = None) -> None:
        """Set in primary and replicate to replicas."""
        # Set in primary
        await self.primary.set(key, value, ttl=ttl)

        # Replicate to replicas (async, don't wait)
        for replica in self.replicas:
            asyncio.create_task(replica.set(key, value, ttl=ttl))
```

---

## Cache Metrics and Monitoring

### Cache Statistics

**REQUIRED**: Track cache performance metrics:

```python
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class CacheMetrics:
    """Cache performance metrics."""

    hits: int = 0
    misses: int = 0
    evictions: int = 0
    expirations: int = 0
    total_requests: int = 0
    total_size_bytes: int = 0
    avg_response_time_ms: float = 0.0

    @property
    def hit_rate(self) -> float:
        """Calculate hit rate percentage."""
        if self.total_requests == 0:
            return 0.0
        return (self.hits / self.total_requests) * 100

    @property
    def miss_rate(self) -> float:
        """Calculate miss rate percentage."""
        return 100.0 - self.hit_rate

class InstrumentedCache:
    """Cache with metrics instrumentation."""

    def __init__(self, cache_backend: Any):
        self.cache = cache_backend
        self.metrics = CacheMetrics()
        self._response_times: List[float] = []

    async def get(self, key: str) -> Optional[Any]:
        """Get with metrics tracking."""
        start_time = time.perf_counter()

        self.metrics.total_requests += 1

        value = await self.cache.get(key)

        response_time = (time.perf_counter() - start_time) * 1000

        if value is not None:
            self.metrics.hits += 1
        else:
            self.metrics.misses += 1

        # Update average response time
        self._update_avg_response_time(response_time)

        return value

    def _update_avg_response_time(self, response_time_ms: float) -> None:
        """Update average response time."""
        self._response_times.append(response_time_ms)

        # Keep only recent 1000 measurements
        if len(self._response_times) > 1000:
            self._response_times = self._response_times[-1000:]

        self.metrics.avg_response_time_ms = sum(self._response_times) / len(self._response_times)

    def get_metrics(self) -> Dict[str, Any]:
        """Get cache metrics."""
        return {
            "hits": self.metrics.hits,
            "misses": self.metrics.misses,
            "hit_rate": self.metrics.hit_rate,
            "miss_rate": self.metrics.miss_rate,
            "evictions": self.metrics.evictions,
            "expirations": self.metrics.expirations,
            "total_requests": self.metrics.total_requests,
            "avg_response_time_ms": self.metrics.avg_response_time_ms,
        }
```

### Prometheus Metrics Integration

**RECOMMENDED**: Export cache metrics to Prometheus:

```python
from prometheus_client import Counter, Histogram, Gauge

# Cache metrics
cache_hits_total = Counter(
    'cache_hits_total',
    'Total cache hits',
    ['cache_type', 'cache_level']
)

cache_misses_total = Counter(
    'cache_misses_total',
    'Total cache misses',
    ['cache_type', 'cache_level']
)

cache_operations_duration_seconds = Histogram(
    'cache_operations_duration_seconds',
    'Cache operation duration',
    ['operation', 'cache_type'],
    buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0]
)

cache_size_bytes = Gauge(
    'cache_size_bytes',
    'Cache size in bytes',
    ['cache_type', 'cache_level']
)

class PrometheusInstrumentedCache:
    """Cache with Prometheus metrics."""

    def __init__(self, cache_backend: Any, cache_type: str, cache_level: str):
        self.cache = cache_backend
        self.cache_type = cache_type
        self.cache_level = cache_level

    async def get(self, key: str) -> Optional[Any]:
        """Get with Prometheus metrics."""
        with cache_operations_duration_seconds.labels(
            operation="get",
            cache_type=self.cache_type
        ).time():
            value = await self.cache.get(key)

            if value is not None:
                cache_hits_total.labels(
                    cache_type=self.cache_type,
                    cache_level=self.cache_level
                ).inc()
            else:
                cache_misses_total.labels(
                    cache_type=self.cache_type,
                    cache_level=self.cache_level
                ).inc()

            return value

    async def set(self, key: str, value: Any, ttl: int = None) -> None:
        """Set with Prometheus metrics."""
        with cache_operations_duration_seconds.labels(
            operation="set",
            cache_type=self.cache_type
        ).time():
            await self.cache.set(key, value, ttl=ttl)

            # Update cache size metric
            size = await self.cache.get_size_bytes()
            cache_size_bytes.labels(
                cache_type=self.cache_type,
                cache_level=self.cache_level
            ).set(size)
```

---

## FastAPI Integration

### Cache Dependency Injection

**RECOMMENDED**: Use FastAPI dependencies for cache access:

```python
from fastapi import Depends
from functools import lru_cache

@lru_cache()
def get_cache_service() -> MultiLevelCache:
    """Get cache service singleton."""
    return MultiLevelCache(
        l1_cache=L1MemoryCache(max_size=1000),
        l2_cache=L2DiskCache(max_size=10000),
        l3_cache=L3RedisCache(redis_url="redis://localhost:6379"),
    )

@app.get("/users/{user_id}")
async def get_user(
    user_id: int,
    cache: MultiLevelCache = Depends(get_cache_service)
) -> User:
    """Get user with caching."""
    cache_key = f"user:{user_id}"

    # Try cache first
    cached_user = await cache.get(cache_key)
    if cached_user is not None:
        return cached_user

    # Cache miss - load from database
    user = await db.get_user(user_id)

    # Store in cache
    if user:
        await cache.set(cache_key, user, ttl=3600)

    return user
```

### Cache Middleware

**RECOMMENDED**: Implement cache middleware:

```python
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import hashlib

class CacheMiddleware(BaseHTTPMiddleware):
    """Middleware for HTTP response caching."""

    def __init__(self, app, cache_backend: Any, ttl: int = 300):
        super().__init__(app)
        self.cache = cache_backend
        self.ttl = ttl
        self.cacheable_methods = {"GET"}

    async def dispatch(self, request: Request, call_next):
        """Process request with caching."""
        # Only cache GET requests
        if request.method not in self.cacheable_methods:
            return await call_next(request)

        # Generate cache key from request
        cache_key = self._generate_cache_key(request)

        # Try cache first
        cached_response = await self.cache.get(cache_key)
        if cached_response is not None:
            return Response(
                content=cached_response["content"],
                status_code=cached_response["status_code"],
                headers=cached_response["headers"],
                media_type=cached_response["media_type"],
            )

        # Process request
        response = await call_next(request)

        # Cache successful responses
        if response.status_code == 200:
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk

            await self.cache.set(
                cache_key,
                {
                    "content": response_body,
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "media_type": response.media_type,
                },
                ttl=self.ttl
            )

            return Response(
                content=response_body,
                status_code=response.status_code,
                headers=response.headers,
                media_type=response.media_type,
            )

        return response

    def _generate_cache_key(self, request: Request) -> str:
        """Generate cache key from request."""
        key_parts = [
            request.method,
            request.url.path,
            str(sorted(request.query_params.items())),
        ]

        key_string = ":".join(key_parts)
        return hashlib.sha256(key_string.encode()).hexdigest()
```

### Cache Headers

**RECOMMENDED**: Use HTTP cache headers:

```python
from fastapi import Response
from datetime import datetime, timedelta

@app.get("/data/{item_id}")
async def get_data(
    item_id: int,
    cache: MultiLevelCache = Depends(get_cache_service)
) -> Response:
    """Get data with cache headers."""
    cache_key = f"data:{item_id}"

    # Try cache
    cached_data = await cache.get(cache_key)
    if cached_data is not None:
        return Response(
            content=json.dumps(cached_data),
            headers={
                "Cache-Control": "public, max-age=3600",
                "ETag": f'"{hash(cache_key)}"',
                "X-Cache": "HIT",
            }
        )

    # Load from source
    data = await db.get_data(item_id)

    # Cache for future requests
    if data:
        await cache.set(cache_key, data, ttl=3600)

    return Response(
        content=json.dumps(data),
        headers={
            "Cache-Control": "public, max-age=3600",
            "ETag": f'"{hash(cache_key)}"',
            "X-Cache": "MISS",
        }
    )
```

---

## Performance Considerations

### Cache Size Management

**CRITICAL**: Control cache size to prevent memory issues:

```python
class SizeLimitedCache:
    """Cache with size-based eviction."""

    def __init__(self, max_size_bytes: int = 100 * 1024 * 1024):  # 100MB
        self.max_size_bytes = max_size_bytes
        self.current_size_bytes = 0
        self._cache: Dict[str, CacheEntry] = {}

    def _calculate_size(self, value: Any) -> int:
        """Calculate size of value."""
        try:
            return len(pickle.dumps(value))
        except Exception:
            return 1024  # Default estimate

    async def set(self, key: str, value: Any, ttl: int = None) -> None:
        """Set value with size checking."""
        value_size = self._calculate_size(value)

        # Evict if necessary
        while (
            self.current_size_bytes + value_size > self.max_size_bytes
            and self._cache
        ):
            await self._evict_largest()

        # Store entry
        old_size = 0
        if key in self._cache:
            old_size = self._cache[key].size

        self._cache[key] = CacheEntry(
            key=key,
            value=value,
            size=value_size,
            expires_at=time.time() + (ttl or 3600),
        )

        self.current_size_bytes += value_size - old_size

    async def _evict_largest(self) -> None:
        """Evict largest entry."""
        if not self._cache:
            return

        # Find largest entry
        largest_key = max(
            self._cache.keys(),
            key=lambda k: self._cache[k].size
        )

        entry = self._cache.pop(largest_key)
        self.current_size_bytes -= entry.size
```

### Async Cache Operations

**REQUIRED**: Use async operations for non-blocking cache access:

```python
import asyncio
from typing import Optional

class AsyncCache:
    """Async cache implementation."""

    def __init__(self, cache_backend: Any):
        self.cache = cache_backend
        self._semaphore = asyncio.Semaphore(100)  # Limit concurrent operations

    async def get(self, key: str) -> Optional[Any]:
        """Get with concurrency limiting."""
        async with self._semaphore:
            return await self.cache.get(key)

    async def set(self, key: str, value: Any, ttl: int = None) -> None:
        """Set with concurrency limiting."""
        async with self._semaphore:
            await self.cache.set(key, value, ttl=ttl)

    async def mget(self, keys: List[str]) -> Dict[str, Optional[Any]]:
        """Batch get with concurrency control."""
        tasks = [self.get(key) for key in keys]
        results = await asyncio.gather(*tasks)

        return {
            key: value
            for key, value in zip(keys, results)
            if value is not None
        }
```

---

## Production Deployment

### Configuration

**REQUIRED**: Configure cache via environment variables:

```python
from pydantic_settings import BaseSettings

class CacheSettings(BaseSettings):
    """Cache configuration."""

    # Multi-level cache
    cache_enabled: bool = True
    l1_max_size: int = 1000
    l2_max_size: int = 10000
    l2_cache_dir: str = "/tmp/cache"
    l3_redis_url: str = "redis://localhost:6379"

    # TTL defaults
    default_ttl: int = 3600
    short_ttl: int = 300
    long_ttl: int = 86400

    # Cache warming
    enable_cache_warming: bool = True
    warming_interval: int = 300

    # Performance
    max_concurrent_operations: int = 100

    class Config:
        env_file = ".env"
        env_prefix = "CACHE_"

settings = CacheSettings()
```

### Health Checks

**REQUIRED**: Implement cache health checks:

```python
@app.get("/health/cache")
async def cache_health(cache: MultiLevelCache = Depends(get_cache_service)):
    """Cache health check endpoint."""
    health_status = {
        "status": "healthy",
        "l1": {
            "enabled": True,
            "size": await cache.l1_cache.get_size(),
            "hit_rate": cache.l1_cache.stats.hit_rate,
        },
        "l2": {
            "enabled": True,
            "size": await cache.l2_cache.get_size(),
            "hit_rate": cache.l2_cache.stats.hit_rate,
        },
        "l3": {
            "enabled": True,
            "connected": await cache.l3_cache.ping(),
            "hit_rate": cache.l3_cache.stats.hit_rate,
        },
    }

    # Check if any level is unhealthy
    if not health_status["l3"]["connected"]:
        health_status["status"] = "degraded"

    return health_status
```

### Production Checklist

- [ ] Multi-level caching configured (L1/L2/L3)
- [ ] Cache invalidation strategies implemented
- [ ] Cache warming enabled for critical data
- [ ] Redis connection pooling configured
- [ ] Cache metrics exported to Prometheus
- [ ] Cache health checks implemented
- [ ] Cache size limits configured
- [ ] Cache key naming conventions documented
- [ ] Cache decorators implemented
- [ ] Distributed cache invalidation configured
- [ ] Cache stampede prevention enabled
- [ ] Cache monitoring dashboards created
- [ ] Cache alerting rules configured

---

## Summary

### Key Takeaways

1. **Multi-Level Caching**: Implement L1 (memory), L2 (disk), L3 (distributed) for optimal performance
2. **Cache Patterns**: Use cache-aside, read-through, write-through, write-behind based on use case
3. **Invalidation Strategies**: Combine TTL, tags, dependencies, patterns, and events
4. **Cache Warming**: Preload frequently accessed data to improve hit rates
5. **Redis Patterns**: Use pipelines, pub/sub, and connection pooling for performance
6. **Cache Decorators**: Simplify caching with decorators
7. **Key Design**: Use consistent naming, namespaces, and hashing
8. **Cache Coherency**: Implement versioning and consistency checks
9. **Distributed Caching**: Support Redis Cluster and replication
10. **Metrics**: Track hit rates, response times, and cache size

### Resources

- [Redis Documentation](https://redis.io/docs/)
- [redis-py Documentation](https://redis-py.readthedocs.io/)
- [cachetools Documentation](https://cachetools.readthedocs.io/)
- [diskcache Documentation](https://grantjenks.com/docs/diskcache/)
- [FastAPI Caching](https://fastapi.tiangolo.com/advanced/caching/)

---

**Version**: v1.0.0
**Last Updated**: 2025-01-14
