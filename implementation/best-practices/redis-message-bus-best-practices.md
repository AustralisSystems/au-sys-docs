# Redis Message Bus Best Practices for Production

## Overview

This document provides comprehensive best practices for implementing Redis as a message bus in production environments, specifically tailored to this application's architecture. It covers Redis pub/sub, Redis Streams, Redis Lists, message patterns, error handling, scalability, monitoring, and production deployment considerations.

## Architecture

### Current Implementation

- **Celery Broker**: Redis cluster for task queue messaging
- **WebSocket Pub/Sub**: Redis pub/sub for distributed WebSocket messaging
- **Redis Cluster**: 6-node cluster for high availability
- **Connection Pooling**: Efficient connection management
- **Automatic Failover**: Cluster failover and recovery
- **Message Routing**: Channel-based message routing

## Redis Messaging Patterns

### 1. Pub/Sub Pattern

**RECOMMENDED**: For real-time broadcasting and event notifications

**Current Implementation**:
```python
# WebSocket distributed messaging
import redis.asyncio as redis
from redis.asyncio.client import PubSub

# Create pubsub connection
self.pubsub = self.redis_client.pubsub()

# Subscribe to channels
await self.pubsub.subscribe(self.broadcast_channel, self.node_channel)

# Publish message
await self.redis_client.publish(channel, message)
```

**Best Practices**:
```python
import json
import asyncio
from typing import Any, Dict, Optional

class RedisPubSubManager:
    """Production-grade Redis pub/sub manager."""

    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client
        self.pubsub: Optional[PubSub] = None
        self.subscribed_channels: set = set()
        self.message_handlers: Dict[str, callable] = {}

    async def subscribe(self, channel: str, handler: callable) -> None:
        """Subscribe to a channel with message handler."""
        if not self.pubsub:
            self.pubsub = self.redis_client.pubsub()

        await self.pubsub.subscribe(channel)
        self.subscribed_channels.add(channel)
        self.message_handlers[channel] = handler

        # Start message listener
        asyncio.create_task(self._listen_messages())

    async def publish(self, channel: str, message: Dict[str, Any]) -> int:
        """Publish message to channel."""
        # Serialize message
        serialized = json.dumps(message)

        # Publish with error handling
        try:
            subscribers = await self.redis_client.publish(channel, serialized)
            return subscribers
        except Exception as e:
            logger.error(f"Failed to publish to {channel}: {e}")
            raise

    async def _listen_messages(self) -> None:
        """Listen for messages on subscribed channels."""
        while True:
            try:
                message = await self.pubsub.get_message(
                    ignore_subscribe_messages=True,
                    timeout=1.0
                )

                if message:
                    channel = message['channel'].decode()
                    data = json.loads(message['data'])

                    # Route to handler
                    if channel in self.message_handlers:
                        await self.message_handlers[channel](data)
            except Exception as e:
                logger.error(f"Error listening for messages: {e}")
                await asyncio.sleep(1)
```

**When to Use Pub/Sub**:
- ✅ Real-time event broadcasting
- ✅ One-to-many messaging
- ✅ Event notifications
- ✅ WebSocket message distribution
- ❌ Reliable message delivery (no guarantees)
- ❌ Message persistence (messages lost if no subscribers)

### 2. Redis Streams Pattern

**RECOMMENDED**: For reliable messaging with acknowledgments

**Best Practices**:
```python
import redis.asyncio as redis
from typing import Any, Dict, List, Optional

class RedisStreamsManager:
    """Production-grade Redis Streams manager."""

    def __init__(self, redis_client: redis.Redis, stream_name: str):
        self.redis_client = redis_client
        self.stream_name = stream_name
        self.consumer_group: Optional[str] = None

    async def add_message(
        self,
        message: Dict[str, Any],
        max_length: Optional[int] = None
    ) -> str:
        """Add message to stream."""
        # Serialize message fields
        fields = {
            k: json.dumps(v) if isinstance(v, (dict, list)) else str(v)
            for k, v in message.items()
        }

        # Add to stream with optional max length
        message_id = await self.redis_client.xadd(
            self.stream_name,
            fields,
            maxlen=max_length  # Optional: limit stream size
        )

        return message_id.decode() if isinstance(message_id, bytes) else message_id

    async def create_consumer_group(
        self,
        group_name: str,
        start_id: str = "0"
    ) -> None:
        """Create consumer group for stream."""
        try:
            await self.redis_client.xgroup_create(
                self.stream_name,
                group_name,
                id=start_id,
                mkstream=True
            )
            self.consumer_group = group_name
        except redis.ResponseError as e:
            if "BUSYGROUP" in str(e):
                # Group already exists
                logger.info(f"Consumer group {group_name} already exists")
            else:
                raise

    async def read_messages(
        self,
        consumer_name: str,
        count: int = 10,
        block: int = 1000
    ) -> List[Dict[str, Any]]:
        """Read messages from stream with consumer group."""
        if not self.consumer_group:
            raise ValueError("Consumer group not created")

        # Read messages
        messages = await self.redis_client.xreadgroup(
            self.consumer_group,
            consumer_name,
            {self.stream_name: ">"},
            count=count,
            block=block
        )

        # Parse messages
        result = []
        for stream, stream_messages in messages:
            for message_id, fields in stream_messages:
                parsed_message = {
                    "id": message_id.decode() if isinstance(message_id, bytes) else message_id,
                    "fields": {
                        k.decode() if isinstance(k, bytes) else k:
                        json.loads(v) if isinstance(v, bytes) and v.startswith(b'{') else v.decode() if isinstance(v, bytes) else v
                        for k, v in fields.items()
                    }
                }
                result.append(parsed_message)

        return result

    async def acknowledge_message(
        self,
        message_id: str
    ) -> None:
        """Acknowledge message processing."""
        await self.redis_client.xack(
            self.stream_name,
            self.consumer_group,
            message_id
        )

    async def claim_pending_messages(
        self,
        consumer_name: str,
        min_idle_time: int = 60000,
        count: int = 10
    ) -> List[Dict[str, Any]]:
        """Claim pending messages from other consumers."""
        pending = await self.redis_client.xpending_range(
            self.stream_name,
            self.consumer_group,
            min="-",
            max="+",
            count=count
        )

        if not pending:
            return []

        # Claim messages
        message_ids = [msg['message_id'] for msg in pending]
        claimed = await self.redis_client.xclaim(
            self.stream_name,
            self.consumer_group,
            consumer_name,
            min_idle_time,
            message_ids
        )

        # Parse claimed messages
        result = []
        for message_id, fields in claimed:
            parsed_message = {
                "id": message_id.decode() if isinstance(message_id, bytes) else message_id,
                "fields": {
                    k.decode() if isinstance(k, bytes) else k:
                    json.loads(v) if isinstance(v, bytes) and v.startswith(b'{') else v.decode() if isinstance(v, bytes) else v
                    for k, v in fields.items()
                }
            }
            result.append(parsed_message)

        return result
```

**When to Use Streams**:
- ✅ Reliable message delivery
- ✅ Message persistence
- ✅ Consumer groups for load balancing
- ✅ Message acknowledgments
- ✅ At-least-once delivery guarantees
- ✅ Ordered message processing

### 3. Redis Lists Pattern

**RECOMMENDED**: For simple work queues (use Celery for complex scenarios)

**Best Practices**:
```python
class RedisListQueue:
    """Simple Redis list-based queue."""

    def __init__(self, redis_client: redis.Redis, queue_name: str):
        self.redis_client = redis_client
        self.queue_name = queue_name

    async def enqueue(self, message: Dict[str, Any]) -> None:
        """Add message to queue."""
        serialized = json.dumps(message)
        await self.redis_client.rpush(self.queue_name, serialized)

    async def dequeue(self, timeout: int = 0) -> Optional[Dict[str, Any]]:
        """Remove and return message from queue."""
        if timeout > 0:
            # Blocking pop
            result = await self.redis_client.blpop(self.queue_name, timeout=timeout)
            if result:
                _, data = result
                return json.loads(data)
        else:
            # Non-blocking pop
            data = await self.redis_client.lpop(self.queue_name)
            if data:
                return json.loads(data)

        return None

    async def get_length(self) -> int:
        """Get queue length."""
        return await self.redis_client.llen(self.queue_name)
```

**When to Use Lists**:
- ✅ Simple FIFO queues
- ✅ Low-latency message processing
- ✅ Simple producer-consumer patterns
- ❌ Complex routing
- ❌ Message acknowledgments
- ❌ Consumer groups

## Pattern Selection Guidelines

### Decision Matrix

| Requirement | Pub/Sub | Streams | Lists |
|------------|---------|---------|-------|
| Real-time broadcasting | ✅ | ⚠️ | ❌ |
| Reliable delivery | ❌ | ✅ | ⚠️ |
| Message persistence | ❌ | ✅ | ✅ |
| Consumer groups | ❌ | ✅ | ❌ |
| Message acknowledgments | ❌ | ✅ | ❌ |
| Ordered processing | ⚠️ | ✅ | ✅ |
| One-to-many | ✅ | ⚠️ | ❌ |
| Simple implementation | ✅ | ⚠️ | ✅ |

### Use Case Examples

**Pub/Sub**:
- WebSocket message broadcasting
- Real-time notifications
- Event distribution
- Cache invalidation signals

**Streams**:
- Task queue (alternative to Celery)
- Event sourcing
- Audit logging
- Reliable message processing

**Lists**:
- Simple work queues
- Rate limiting queues
- Priority queues (with sorted sets)

## Channel and Stream Naming Conventions

### 1. Hierarchical Naming

**RECOMMENDED**: Use hierarchical namespace pattern

```python
# Good: Hierarchical namespace
"app:module:entity:action"
"app:module:entity:id:event"

# Examples
"orchestrator:websocket:broadcast"
"orchestrator:websocket:node:node-123:status"
"orchestrator:events:user:123:updated"
"orchestrator:events:workflow:456:completed"
"orchestrator:cache:invalidation:user:*"

# Bad: Flat or inconsistent naming
"broadcast"
"node_status"
"user_update"
```

**Best Practices**:
- Use consistent separator (`:` recommended)
- Include namespace/application prefix
- Include entity type and identifier
- Use lowercase with underscores
- Avoid special characters

### 2. Channel Patterns

**RECOMMENDED**: Use patterns for subscription

```python
# Subscribe to all user events
await pubsub.psubscribe("orchestrator:events:user:*")

# Subscribe to specific user events
await pubsub.subscribe("orchestrator:events:user:123:updated")

# Subscribe to all workflow events
await pubsub.psubscribe("orchestrator:events:workflow:*")
```

## Message Serialization

### 1. JSON Serialization

**RECOMMENDED**: Use JSON for most messages

```python
import json
from typing import Any, Dict

def serialize_message(message: Dict[str, Any]) -> str:
    """Serialize message to JSON."""
    return json.dumps(message, default=str)

def deserialize_message(data: str) -> Dict[str, Any]:
    """Deserialize message from JSON."""
    return json.loads(data)
```

**Best Practices**:
- Use JSON for human-readable messages
- Handle datetime serialization
- Validate message schema
- Keep messages small (< 1MB)

### 2. MessagePack Serialization

**RECOMMENDED**: Use MessagePack for performance-critical scenarios

```python
import msgpack
from typing import Any, Dict

def serialize_message_pack(message: Dict[str, Any]) -> bytes:
    """Serialize message with MessagePack."""
    return msgpack.packb(message, use_bin_type=True)

def deserialize_message_pack(data: bytes) -> Dict[str, Any]:
    """Deserialize message from MessagePack."""
    return msgpack.unpackb(data, raw=False)
```

**Best Practices**:
- Use MessagePack for binary efficiency
- Faster than JSON
- Smaller message size
- Less human-readable

### 3. Message Schema Validation

**REQUIRED**: Validate message schemas

```python
from pydantic import BaseModel, ValidationError

class MessageSchema(BaseModel):
    """Message schema validation."""
    event_type: str
    timestamp: str
    data: Dict[str, Any]
    source: str

def validate_message(message: Dict[str, Any]) -> MessageSchema:
    """Validate message against schema."""
    try:
        return MessageSchema(**message)
    except ValidationError as e:
        raise ValueError(f"Invalid message schema: {e}")
```

## Error Handling and Resilience

### 1. Connection Retry Logic

**REQUIRED**: Implement retry logic for connections

```python
import asyncio
from typing import Optional

class ResilientRedisPubSub:
    """Redis pub/sub with automatic reconnection."""

    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client
        self.pubsub: Optional[PubSub] = None
        self.connected = False
        self.retry_delay = 1
        self.max_retry_delay = 60

    async def connect(self) -> None:
        """Connect with retry logic."""
        retry_count = 0

        while not self.connected:
            try:
                self.pubsub = self.redis_client.pubsub()
                await self.pubsub.ping()
                self.connected = True
                self.retry_delay = 1
                logger.info("Redis pub/sub connected")
            except Exception as e:
                retry_count += 1
                logger.warning(f"Connection failed (attempt {retry_count}): {e}")

                # Exponential backoff
                await asyncio.sleep(self.retry_delay)
                self.retry_delay = min(self.retry_delay * 2, self.max_retry_delay)

    async def ensure_connected(self) -> None:
        """Ensure connection is active."""
        if not self.connected or not self.pubsub:
            await self.connect()

        try:
            await self.pubsub.ping()
        except Exception:
            self.connected = False
            await self.connect()
```

### 2. Message Processing Error Handling

**REQUIRED**: Handle message processing errors gracefully

```python
async def process_message_with_error_handling(
    message: Dict[str, Any],
    handler: callable
) -> None:
    """Process message with comprehensive error handling."""
    try:
        # Validate message
        validated_message = validate_message(message)

        # Process message
        await handler(validated_message)

    except ValidationError as e:
        # Invalid message - log and skip
        logger.error(f"Invalid message: {e}")
        # Optionally send to dead letter queue

    except Exception as e:
        # Processing error - log and handle
        logger.error(f"Error processing message: {e}", exc_info=True)

        # Retry logic
        if should_retry(e):
            await retry_message(message, handler)
        else:
            # Send to dead letter queue
            await send_to_dlq(message, str(e))
```

### 3. Dead Letter Queue

**RECOMMENDED**: Implement dead letter queue for failed messages

```python
class DeadLetterQueue:
    """Dead letter queue for failed messages."""

    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client
        self.dlq_stream = "dlq:messages"

    async def add_failed_message(
        self,
        original_message: Dict[str, Any],
        error: str,
        retry_count: int
    ) -> None:
        """Add failed message to DLQ."""
        dlq_message = {
            "original_message": json.dumps(original_message),
            "error": error,
            "retry_count": retry_count,
            "timestamp": datetime.utcnow().isoformat(),
            "source_channel": original_message.get("channel", "unknown")
        }

        await self.redis_client.xadd(
            self.dlq_stream,
            {k: json.dumps(v) if isinstance(v, dict) else str(v)
             for k, v in dlq_message.items()}
        )
```

## Performance Optimization

### 1. Connection Pooling

**REQUIRED**: Use connection pooling

**Current Implementation**:
```python
# Create connection pool
pool = redis.ConnectionPool(
    max_connections=pool_size,
    decode_responses=False,
    password=redis_password,
    db=redis_db,
)

# Create Redis client
self.redis_client = redis.Redis.from_url(
    redis_url,
    connection_pool=pool,
    decode_responses=False
)
```

**Best Practices**:
- Size pool based on concurrent operations
- Reuse connections
- Monitor pool usage
- Set appropriate max connections

**Pool Sizing Guidelines**:
- **Small Applications**: 10-20 connections
- **Medium Applications**: 50-100 connections
- **Large Applications**: 100-200 connections

### 2. Batch Operations

**RECOMMENDED**: Use pipelines for batch operations

```python
async def publish_batch(
    redis_client: redis.Redis,
    messages: List[Tuple[str, Dict[str, Any]]]
) -> None:
    """Publish multiple messages in batch."""
    pipe = redis_client.pipeline()

    for channel, message in messages:
        serialized = json.dumps(message)
        pipe.publish(channel, serialized)

    await pipe.execute()
```

### 3. Message Compression

**RECOMMENDED**: Compress large messages

```python
import gzip
import base64

def compress_message(message: str) -> str:
    """Compress message for large payloads."""
    compressed = gzip.compress(message.encode())
    return base64.b64encode(compressed).decode()

def decompress_message(compressed: str) -> str:
    """Decompress message."""
    decoded = base64.b64decode(compressed)
    return gzip.decompress(decoded).decode()
```

**Best Practices**:
- Compress messages > 1KB
- Use gzip for text messages
- Use lz4 for binary messages
- Monitor compression overhead

## Scalability and High Availability

### 1. Redis Cluster Configuration

**Current Configuration**: 6-node cluster (3 masters, 3 replicas)

**Best Practices**:
- Use Redis Cluster for horizontal scaling
- Distribute channels across cluster nodes
- Use hash tags for related channels
- Monitor cluster health

**Hash Tags for Channels**:
```python
# Good: Channels hash to same slot
channel = f"orchestrator:websocket:{{{node_id}}}:broadcast"
channel = f"orchestrator:websocket:{{{node_id}}}:status"

# All channels with {node_id} hash to same slot
# Can use transactions and multi-key operations
```

### 2. Consumer Group Scaling

**RECOMMENDED**: Use consumer groups for Streams

```python
# Create multiple consumers in same group
consumer1 = RedisStreamsManager(redis_client, "events:stream")
await consumer1.create_consumer_group("processors", "0")

consumer2 = RedisStreamsManager(redis_client, "events:stream")
await consumer2.create_consumer_group("processors", "0")

# Each consumer processes different messages
# Automatic load balancing
```

**Best Practices**:
- Use consumer groups for parallel processing
- Scale consumers horizontally
- Monitor consumer lag
- Handle consumer failures

### 3. Message Partitioning

**RECOMMENDED**: Partition messages by entity ID

```python
def get_stream_for_entity(entity_id: str, num_partitions: int = 10) -> str:
    """Get stream partition for entity."""
    partition = hash(entity_id) % num_partitions
    return f"events:stream:partition:{partition}"

# Ensures messages for same entity go to same partition
# Maintains ordering per entity
```

## Monitoring and Observability

### 1. Message Metrics

**REQUIRED**: Track message metrics

```python
from prometheus_client import Counter, Histogram, Gauge

messages_published = Counter(
    'redis_messages_published_total',
    'Total messages published',
    ['channel', 'status']
)

messages_consumed = Counter(
    'redis_messages_consumed_total',
    'Total messages consumed',
    ['channel', 'status']
)

message_processing_duration = Histogram(
    'redis_message_processing_duration_seconds',
    'Message processing duration',
    ['channel']
)

queue_length = Gauge(
    'redis_queue_length',
    'Queue length',
    ['queue_name']
)
```

### 2. Channel Monitoring

**RECOMMENDED**: Monitor channel activity

```python
async def get_channel_stats(
    redis_client: redis.Redis,
    channel: str
) -> Dict[str, Any]:
    """Get statistics for a channel."""
    # Get number of subscribers
    subscribers = await redis_client.pubsub_numsub(channel)

    # Get stream length (if using streams)
    stream_length = await redis_client.xlen(channel)

    return {
        "channel": channel,
        "subscribers": subscribers.get(channel, 0),
        "stream_length": stream_length
    }
```

### 3. Consumer Lag Monitoring

**REQUIRED**: Monitor consumer lag for Streams

```python
async def get_consumer_lag(
    redis_client: redis.Redis,
    stream_name: str,
    group_name: str
) -> Dict[str, Any]:
    """Get consumer group lag."""
    # Get pending messages
    pending = await redis_client.xpending(stream_name, group_name)

    # Get stream length
    stream_length = await redis_client.xlen(stream_name)

    return {
        "pending_count": pending.get("pending", 0),
        "stream_length": stream_length,
        "lag": stream_length - pending.get("pending", 0)
    }
```

## Security Best Practices

### 1. Channel Access Control

**REQUIRED**: Implement channel access control

```python
class SecurePubSubManager:
    """Pub/sub manager with access control."""

    def __init__(self, redis_client: redis.Redis, access_control: Dict[str, List[str]]):
        self.redis_client = redis_client
        self.access_control = access_control  # channel -> allowed_roles

    async def publish(
        self,
        channel: str,
        message: Dict[str, Any],
        user_role: str
    ) -> int:
        """Publish with access control."""
        # Check access
        if channel not in self.access_control:
            raise PermissionError(f"Channel {channel} not found")

        if user_role not in self.access_control[channel]:
            raise PermissionError(f"Access denied to {channel}")

        # Publish
        return await self.redis_client.publish(channel, json.dumps(message))
```

### 2. Message Encryption

**RECOMMENDED**: Encrypt sensitive messages

```python
from cryptography.fernet import Fernet

class EncryptedPubSubManager:
    """Pub/sub manager with message encryption."""

    def __init__(self, redis_client: redis.Redis, encryption_key: bytes):
        self.redis_client = redis_client
        self.cipher = Fernet(encryption_key)

    async def publish_encrypted(
        self,
        channel: str,
        message: Dict[str, Any]
    ) -> int:
        """Publish encrypted message."""
        # Serialize and encrypt
        serialized = json.dumps(message)
        encrypted = self.cipher.encrypt(serialized.encode())

        # Publish encrypted message
        return await self.redis_client.publish(channel, encrypted)

    async def subscribe_encrypted(
        self,
        channel: str,
        handler: callable
    ) -> None:
        """Subscribe and decrypt messages."""
        pubsub = self.redis_client.pubsub()
        await pubsub.subscribe(channel)

        async for message in pubsub.listen():
            if message['type'] == 'message':
                # Decrypt message
                decrypted = self.cipher.decrypt(message['data'])
                message_data = json.loads(decrypted)
                await handler(message_data)
```

### 3. Input Validation

**REQUIRED**: Validate all messages

```python
def validate_message_input(
    message: Dict[str, Any],
    schema: BaseModel
) -> BaseModel:
    """Validate message input."""
    try:
        return schema(**message)
    except ValidationError as e:
        raise ValueError(f"Invalid message: {e}")
```

## Production Deployment Checklist

- [ ] Redis Cluster configured for high availability
- [ ] Connection pooling configured appropriately
- [ ] Channel naming follows conventions
- [ ] Message serialization standardized
- [ ] Error handling implemented
- [ ] Dead letter queue configured
- [ ] Retry logic implemented
- [ ] Consumer groups configured (for Streams)
- [ ] Message metrics tracked
- [ ] Channel monitoring enabled
- [ ] Consumer lag monitored (for Streams)
- [ ] Access control implemented
- [ ] Message encryption enabled (for sensitive data)
- [ ] Input validation implemented
- [ ] Message compression enabled (for large messages)
- [ ] Batch operations used where appropriate
- [ ] Connection retry logic implemented
- [ ] Health checks configured
- [ ] Alerting configured
- [ ] Documentation up-to-date

## Common Anti-Patterns to Avoid

### 1. Using Pub/Sub for Reliable Delivery

**Problem**: Pub/Sub doesn't guarantee delivery

**Solution**: Use Redis Streams for reliable delivery

```python
# Bad: Using pub/sub for critical messages
await redis_client.publish("critical:payment", payment_data)

# Good: Using streams for critical messages
await redis_client.xadd("critical:payment:stream", payment_data)
```

### 2. Not Handling Connection Failures

**Problem**: No reconnection logic

**Solution**: Implement automatic reconnection

```python
# Bad: No reconnection
pubsub = redis_client.pubsub()
await pubsub.subscribe(channel)

# Good: With reconnection
class ResilientPubSub:
    async def ensure_connected(self):
        if not self.connected:
            await self.connect()
```

### 3. Large Messages Without Compression

**Problem**: Large messages cause performance issues

**Solution**: Compress large messages

```python
# Bad: Large uncompressed message
await redis_client.publish(channel, large_json_string)

# Good: Compressed message
compressed = compress_message(large_json_string)
await redis_client.publish(channel, compressed)
```

### 4. No Message Validation

**Problem**: Invalid messages cause errors

**Solution**: Validate all messages

```python
# Bad: No validation
await handler(message)

# Good: With validation
validated = validate_message(message)
await handler(validated)
```

### 5. Not Monitoring Consumer Lag

**Problem**: Messages pile up without detection

**Solution**: Monitor consumer lag

```python
# Good: Monitor lag
lag = await get_consumer_lag(stream_name, group_name)
if lag > threshold:
    alert("High consumer lag detected")
```

## Recommended Production Configuration

```python
# Redis message bus configuration
redis_message_bus_config = {
    "redis": {
        "cluster_enabled": True,
        "startup_nodes": [
            {"host": "redis-cluster-0", "port": 6379},
            {"host": "redis-cluster-1", "port": 6379},
            {"host": "redis-cluster-2", "port": 6379},
        ],
        "max_connections": 50,
        "socket_timeout": 30,
        "retry_on_cluster_down": True,
    },
    "pubsub": {
        "connection_pool_size": 20,
        "message_timeout": 30,
        "reconnect_delay": 1,
        "max_reconnect_delay": 60,
    },
    "streams": {
        "consumer_group": "message_processors",
        "batch_size": 10,
        "block_timeout": 1000,
        "max_pending_time": 60000,
        "claim_interval": 30000,
    },
    "serialization": {
        "format": "json",  # or "msgpack"
        "compress_threshold": 1024,  # 1KB
        "compression": "gzip",
    },
    "monitoring": {
        "metrics_enabled": True,
        "lag_monitoring": True,
        "health_check_interval": 30,
    },
    "security": {
        "encryption_enabled": False,  # Enable for sensitive data
        "access_control_enabled": True,
    },
}
```

## References

- [Redis Pub/Sub Documentation](https://redis.io/docs/manual/pubsub/)
- [Redis Streams Documentation](https://redis.io/docs/data-types/streams/)
- [Redis Lists Documentation](https://redis.io/docs/data-types/lists/)
- [Redis Cluster Best Practices](./redis-cluster-best-practices.md)
- [Celery Production Best Practices](./celery-production-best-practices.md)
