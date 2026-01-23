# WebSockets & Server-Sent Events Best Practices 2025
**Version**: v1.0.0
**Last Updated**: 2025-01-14
**FastAPI Version**: 0.118.2+
**Starlette Version**: 0.41.0+

This document compiles the latest best practices for implementing WebSockets and Server-Sent Events (SSE) in FastAPI applications, based on official documentation, production code examples, and industry recommendations for 2025.

---

## Table of Contents

1. [Architecture & Design Patterns](#architecture--design-patterns)
2. [WebSocket Implementation](#websocket-implementation)
3. [Server-Sent Events (SSE) Implementation](#server-sent-events-sse-implementation)
4. [Connection Management](#connection-management)
5. [Authentication & Authorization](#authentication--authorization)
6. [Error Handling & Resilience](#error-handling--resilience)
7. [Performance Optimization](#performance-optimization)
8. [Security Best Practices](#security-best-practices)
9. [Message Patterns & Protocols](#message-patterns--protocols)
10. [Monitoring & Observability](#monitoring--observability)
11. [Testing Strategies](#testing-strategies)
12. [Production Deployment](#production-deployment)

---

## Architecture & Design Patterns

### ✅ Best Practices

#### 1. Connection Manager Pattern

Implement a centralized connection manager to handle WebSocket connections:

```python
from typing import Dict, Set, Optional
from fastapi import WebSocket
from fastapi.websockets import WebSocketState
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    """Manages WebSocket connections with subscription support."""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.subscriptions: Dict[str, Set[str]] = {}  # connection_id -> set of topics
        self.user_connections: Dict[str, Set[str]] = {}  # user_id -> set of connection_ids
    
    async def connect(
        self, 
        websocket: WebSocket, 
        connection_id: str, 
        user_id: Optional[str] = None
    ) -> None:
        """Accept and register a new WebSocket connection."""
        await websocket.accept()
        self.active_connections[connection_id] = websocket
        self.subscriptions[connection_id] = set()
        
        if user_id:
            if user_id not in self.user_connections:
                self.user_connections[user_id] = set()
            self.user_connections[user_id].add(connection_id)
        
        logger.info(f"WebSocket connected: {connection_id} (user: {user_id})")
    
    def disconnect(self, connection_id: str, user_id: Optional[str] = None) -> None:
        """Remove a WebSocket connection."""
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]
        
        if connection_id in self.subscriptions:
            del self.subscriptions[connection_id]
        
        if user_id and user_id in self.user_connections:
            self.user_connections[user_id].discard(connection_id)
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]
        
        logger.info(f"WebSocket disconnected: {connection_id}")
    
    async def send_personal_message(
        self, 
        connection_id: str, 
        message: dict
    ) -> bool:
        """Send a message to a specific connection."""
        if connection_id not in self.active_connections:
            return False
        
        websocket = self.active_connections[connection_id]
        try:
            if websocket.client_state == WebSocketState.CONNECTED:
                await websocket.send_json(message)
                return True
            else:
                logger.warning(f"WebSocket {connection_id} not connected")
                self.disconnect(connection_id)
                return False
        except Exception as e:
            logger.error(f"Error sending message to {connection_id}: {e}")
            self.disconnect(connection_id)
            return False
    
    async def broadcast_to_subscribers(
        self, 
        topic: str, 
        message: dict
    ) -> int:
        """Broadcast a message to all connections subscribed to a topic."""
        sent_count = 0
        disconnected = []
        
        for connection_id, subscribed_topics in self.subscriptions.items():
            if topic in subscribed_topics or "*" in subscribed_topics:
                if await self.send_personal_message(connection_id, message):
                    sent_count += 1
                else:
                    disconnected.append(connection_id)
        
        # Clean up disconnected connections
        for connection_id in disconnected:
            self.disconnect(connection_id)
        
        return sent_count
    
    def subscribe(self, connection_id: str, topic: str) -> None:
        """Subscribe a connection to a topic."""
        if connection_id in self.subscriptions:
            self.subscriptions[connection_id].add(topic)
            logger.info(f"Connection {connection_id} subscribed to: {topic}")
    
    def unsubscribe(self, connection_id: str, topic: str) -> None:
        """Unsubscribe a connection from a topic."""
        if connection_id in self.subscriptions:
            self.subscriptions[connection_id].discard(topic)
            logger.info(f"Connection {connection_id} unsubscribed from: {topic}")
```

**Benefits:**
- Centralized connection management
- Topic-based subscriptions
- Automatic cleanup of disconnected connections
- User-based connection tracking

#### 2. Separation of Concerns

Separate WebSocket/SSE logic from business logic:

```python
# websocket_manager.py - Connection management
class ConnectionManager:
    # ... connection management logic ...

# websocket_handler.py - Message handling
class MessageHandler:
    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager
    
    async def handle_message(self, connection_id: str, message: dict) -> None:
        # Route messages to appropriate handlers
        message_type = message.get("type")
        if message_type == "subscribe":
            await self._handle_subscribe(connection_id, message)
        elif message_type == "ping":
            await self._handle_ping(connection_id)
        # ... other handlers ...

# websocket_service.py - Business logic
class WebSocketService:
    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager
    
    async def notify_event(self, event_type: str, data: dict) -> None:
        """Notify all subscribers about an event."""
        message = {
            "type": "event",
            "event_type": event_type,
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await self.connection_manager.broadcast_to_subscribers(
            event_type, 
            message
        )
```

#### 3. Event-Driven Architecture

Use an event bus for decoupled communication:

```python
from typing import Callable, Dict, List
import asyncio

class EventBus:
    """Event bus for decoupled event handling."""
    
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_type: str, handler: Callable) -> None:
        """Subscribe a handler to an event type."""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)
    
    async def publish(self, event_type: str, data: dict) -> None:
        """Publish an event to all subscribers."""
        if event_type in self.subscribers:
            tasks = [
                handler(event_type, data) 
                for handler in self.subscribers[event_type]
            ]
            await asyncio.gather(*tasks, return_exceptions=True)

# Usage
event_bus = EventBus()

# Subscribe WebSocket manager to events
event_bus.subscribe("feature_flag_changed", websocket_service.notify_event)
event_bus.subscribe("user_status_changed", websocket_service.notify_event)
```

---

## WebSocket Implementation

### ✅ Best Practices

#### 1. Basic WebSocket Endpoint

```python
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.websockets import WebSocketState
import json
import uuid
from datetime import datetime, timezone

router = APIRouter(prefix="/ws", tags=["websocket"])

# Global connection manager
manager = ConnectionManager()

@router.websocket("/{connection_id}")
async def websocket_endpoint(
    websocket: WebSocket, 
    connection_id: str
) -> None:
    """WebSocket endpoint with connection management."""
    user_id = websocket.query_params.get("user_id")
    
    try:
        await manager.connect(websocket, connection_id, user_id)
        
        # Send initial connection confirmation
        await manager.send_personal_message(
            connection_id,
            {
                "type": "connection_established",
                "connection_id": connection_id,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        )
        
        # Message loop
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            await handle_client_message(connection_id, message)
    
    except WebSocketDisconnect:
        manager.disconnect(connection_id, user_id)
    except Exception as e:
        logger.error(f"WebSocket error for {connection_id}: {e}")
        manager.disconnect(connection_id, user_id)
```

#### 2. WebSocket with Dependency Injection

```python
from fastapi import Depends, WebSocket
from app.dependencies import get_current_user

@router.websocket("/authenticated/{connection_id}")
async def authenticated_websocket(
    websocket: WebSocket,
    connection_id: str,
    current_user: dict = Depends(get_current_user_websocket)
) -> None:
    """WebSocket endpoint with authentication."""
    await manager.connect(websocket, connection_id, current_user["id"])
    # ... rest of implementation ...
```

#### 3. WebSocket State Management

Always check WebSocket state before operations:

```python
async def send_message_safe(
    websocket: WebSocket, 
    message: dict
) -> bool:
    """Safely send a message with state checking."""
    if websocket.client_state != WebSocketState.CONNECTED:
        return False
    
    try:
        await websocket.send_json(message)
        return True
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        return False
```

#### 4. Heartbeat/Ping-Pong Pattern

Implement heartbeat to detect dead connections:

```python
import asyncio
from datetime import datetime, timezone

class HeartbeatManager:
    """Manages heartbeat/ping-pong for WebSocket connections."""
    
    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager
        self.ping_interval = 30  # seconds
        self.pong_timeout = 10  # seconds
        self.pending_pongs: Dict[str, asyncio.Task] = {}
    
    async def start_heartbeat(self, connection_id: str) -> None:
        """Start heartbeat for a connection."""
        while connection_id in self.connection_manager.active_connections:
            try:
                await asyncio.sleep(self.ping_interval)
                
                # Send ping
                await self.connection_manager.send_personal_message(
                    connection_id,
                    {
                        "type": "ping",
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                )
                
                # Set timeout for pong
                self.pending_pongs[connection_id] = asyncio.create_task(
                    self._wait_for_pong(connection_id)
                )
            
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Heartbeat error for {connection_id}: {e}")
                break
    
    async def _wait_for_pong(self, connection_id: str) -> None:
        """Wait for pong response."""
        await asyncio.sleep(self.pong_timeout)
        if connection_id in self.pending_pongs:
            logger.warning(f"No pong received for {connection_id}, disconnecting")
            self.connection_manager.disconnect(connection_id)
    
    def handle_pong(self, connection_id: str) -> None:
        """Handle pong response."""
        if connection_id in self.pending_pongs:
            self.pending_pongs[connection_id].cancel()
            del self.pending_pongs[connection_id]
```

#### 5. Binary Message Support

Handle both text and binary messages:

```python
@router.websocket("/binary/{connection_id}")
async def binary_websocket(
    websocket: WebSocket,
    connection_id: str
) -> None:
    """WebSocket endpoint supporting binary messages."""
    await websocket.accept()
    
    try:
        while True:
            # Check message type
            message = await websocket.receive()
            
            if "text" in message:
                data = message["text"]
                await handle_text_message(websocket, data)
            elif "bytes" in message:
                data = message["bytes"]
                await handle_binary_message(websocket, data)
    
    except WebSocketDisconnect:
        logger.info(f"WebSocket {connection_id} disconnected")
```

---

## Server-Sent Events (SSE) Implementation

### ✅ Best Practices

#### 1. Basic SSE Endpoint

```python
from sse_starlette.sse import EventSourceResponse, ServerSentEvent
from fastapi import Request
import asyncio
from datetime import datetime, timezone

@router.get("/events")
async def sse_events(request: Request) -> EventSourceResponse:
    """Server-Sent Events endpoint."""
    
    async def event_generator() -> ServerSentEvent:
        """Generate SSE events."""
        try:
            # Send initial connection event
            yield ServerSentEvent(
                event="connected",
                data=json.dumps({
                    "message": "Connected to event stream",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                })
            )
            
            # Send heartbeat periodically
            while True:
                # Check if client disconnected
                if await request.is_disconnected():
                    break
                
                # Send heartbeat
                yield ServerSentEvent(
                    event="ping",
                    data=json.dumps({
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    })
                )
                
                await asyncio.sleep(30)
        
        except asyncio.CancelledError:
            logger.info("SSE connection closed")
    
    return EventSourceResponse(event_generator())
```

#### 2. SSE with Event Subscription

```python
from typing import AsyncGenerator
from collections import deque

class SSEManager:
    """Manages SSE connections and event broadcasting."""
    
    def __init__(self):
        self.connections: Dict[str, deque] = {}  # connection_id -> event queue
        self.subscriptions: Dict[str, Set[str]] = {}  # connection_id -> topics
    
    async def create_stream(
        self, 
        connection_id: str,
        request: Request
    ) -> AsyncGenerator[ServerSentEvent, None]:
        """Create an SSE stream for a connection."""
        self.connections[connection_id] = deque(maxlen=100)
        self.subscriptions[connection_id] = set()
        
        try:
            # Send initial event
            yield ServerSentEvent(
                event="connected",
                data=json.dumps({"connection_id": connection_id})
            )
            
            # Stream events
            while not await request.is_disconnected():
                if self.connections[connection_id]:
                    event = self.connections[connection_id].popleft()
                    yield event
                else:
                    # Send heartbeat if no events
                    yield ServerSentEvent(
                        event="ping",
                        data=json.dumps({
                            "timestamp": datetime.now(timezone.utc).isoformat()
                        })
                    )
                    await asyncio.sleep(1)
        
        except asyncio.CancelledError:
            pass
        finally:
            self.disconnect(connection_id)
    
    async def send_event(
        self, 
        connection_id: str, 
        event_type: str, 
        data: dict
    ) -> None:
        """Send an event to a specific connection."""
        if connection_id in self.connections:
            event = ServerSentEvent(
                event=event_type,
                data=json.dumps(data)
            )
            self.connections[connection_id].append(event)
    
    async def broadcast_event(
        self, 
        topic: str, 
        event_type: str, 
        data: dict
    ) -> None:
        """Broadcast an event to all subscribers."""
        for connection_id, topics in self.subscriptions.items():
            if topic in topics or "*" in topics:
                await self.send_event(connection_id, event_type, data)
    
    def subscribe(self, connection_id: str, topic: str) -> None:
        """Subscribe a connection to a topic."""
        if connection_id in self.subscriptions:
            self.subscriptions[connection_id].add(topic)
    
    def disconnect(self, connection_id: str) -> None:
        """Disconnect an SSE connection."""
        if connection_id in self.connections:
            del self.connections[connection_id]
        if connection_id in self.subscriptions:
            del self.subscriptions[connection_id]

# Usage
sse_manager = SSEManager()

@router.get("/events/{connection_id}")
async def sse_endpoint(
    request: Request,
    connection_id: str
) -> EventSourceResponse:
    """SSE endpoint with connection management."""
    return EventSourceResponse(
        sse_manager.create_stream(connection_id, request)
    )
```

#### 3. SSE with Redis Pub/Sub

For distributed systems, use Redis for event distribution:

```python
import redis.asyncio as redis
from typing import AsyncGenerator

class RedisSSEManager:
    """SSE manager with Redis pub/sub for distributed events."""
    
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client
        self.pubsub = redis_client.pubsub()
        self.subscriptions: Dict[str, Set[str]] = {}
    
    async def create_stream(
        self,
        connection_id: str,
        request: Request,
        topics: List[str]
    ) -> AsyncGenerator[ServerSentEvent, None]:
        """Create SSE stream with Redis subscription."""
        # Subscribe to Redis channels
        for topic in topics:
            await self.pubsub.subscribe(f"sse:{topic}")
            if connection_id not in self.subscriptions:
                self.subscriptions[connection_id] = set()
            self.subscriptions[connection_id].add(topic)
        
        try:
            # Send initial event
            yield ServerSentEvent(
                event="connected",
                data=json.dumps({"connection_id": connection_id})
            )
            
            # Listen for Redis messages
            while not await request.is_disconnected():
                message = await self.pubsub.get_message(
                    ignore_subscribe_messages=True,
                    timeout=1.0
                )
                
                if message:
                    event_data = json.loads(message["data"])
                    yield ServerSentEvent(
                        event=event_data.get("event_type", "message"),
                        data=json.dumps(event_data)
                    )
                else:
                    # Send heartbeat
                    yield ServerSentEvent(
                        event="ping",
                        data=json.dumps({
                            "timestamp": datetime.now(timezone.utc).isoformat()
                        })
                    )
        
        except asyncio.CancelledError:
            pass
        finally:
            # Unsubscribe
            for topic in topics:
                await self.pubsub.unsubscribe(f"sse:{topic}")
            if connection_id in self.subscriptions:
                del self.subscriptions[connection_id]
    
    async def publish_event(
        self,
        topic: str,
        event_type: str,
        data: dict
    ) -> None:
        """Publish an event to Redis."""
        await self.redis_client.publish(
            f"sse:{topic}",
            json.dumps({
                "event_type": event_type,
                "data": data,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
        )
```

---

## Connection Management

### ✅ Best Practices

#### 1. Connection Limits

Implement connection limits to prevent resource exhaustion:

```python
from typing import Optional
from fastapi import HTTPException

class ConnectionManager:
    def __init__(self, max_connections: int = 1000):
        self.max_connections = max_connections
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(
        self,
        websocket: WebSocket,
        connection_id: str
    ) -> None:
        """Connect with connection limit enforcement."""
        if len(self.active_connections) >= self.max_connections:
            await websocket.close(code=1008, reason="Server at capacity")
            raise HTTPException(
                status_code=503,
                detail="Maximum connections reached"
            )
        
        await websocket.accept()
        self.active_connections[connection_id] = websocket
```

#### 2. Connection Timeout

Implement connection timeout for idle connections:

```python
import asyncio
from datetime import datetime, timedelta

class ConnectionManager:
    def __init__(self, idle_timeout: int = 300):
        self.active_connections: Dict[str, WebSocket] = {}
        self.last_activity: Dict[str, datetime] = {}
        self.idle_timeout = idle_timeout
    
    async def connect(self, websocket: WebSocket, connection_id: str) -> None:
        await websocket.accept()
        self.active_connections[connection_id] = websocket
        self.last_activity[connection_id] = datetime.now()
        
        # Start timeout task
        asyncio.create_task(self._check_idle_timeout(connection_id))
    
    async def update_activity(self, connection_id: str) -> None:
        """Update last activity timestamp."""
        if connection_id in self.last_activity:
            self.last_activity[connection_id] = datetime.now()
    
    async def _check_idle_timeout(self, connection_id: str) -> None:
        """Check and disconnect idle connections."""
        while connection_id in self.active_connections:
            await asyncio.sleep(60)  # Check every minute
            
            if connection_id in self.last_activity:
                idle_time = datetime.now() - self.last_activity[connection_id]
                if idle_time.total_seconds() > self.idle_timeout:
                    logger.info(f"Disconnecting idle connection: {connection_id}")
                    await self.disconnect(connection_id)
                    break
```

#### 3. Graceful Shutdown

Handle graceful shutdown of connections:

```python
from contextlib import asynccontextmanager

class ConnectionManager:
    async def shutdown(self) -> None:
        """Gracefully shutdown all connections."""
        logger.info("Shutting down connections...")
        
        # Send shutdown notification
        shutdown_message = {
            "type": "shutdown",
            "message": "Server is shutting down",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        for connection_id in list(self.active_connections.keys()):
            try:
                await self.send_personal_message(
                    connection_id,
                    shutdown_message
                )
                await self.active_connections[connection_id].close()
            except Exception as e:
                logger.error(f"Error closing connection {connection_id}: {e}")
            finally:
                self.disconnect(connection_id)
        
        logger.info("All connections closed")

# In FastAPI lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown
    await manager.shutdown()
```

---

## Authentication & Authorization

### ✅ Best Practices

#### 1. WebSocket Authentication

Authenticate WebSocket connections:

```python
from fastapi import Depends, WebSocket, WebSocketException, status
from app.dependencies import verify_token

async def get_current_user_websocket(
    websocket: WebSocket,
    token: str = None
) -> dict:
    """Authenticate WebSocket connection."""
    if token is None:
        token = websocket.query_params.get("token")
    
    if not token:
        await websocket.close(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="Authentication required"
        )
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION
        )
    
    try:
        user = await verify_token(token)
        return user
    except Exception as e:
        await websocket.close(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="Invalid token"
        )
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION
        )

@router.websocket("/authenticated/{connection_id}")
async def authenticated_websocket(
    websocket: WebSocket,
    connection_id: str,
    current_user: dict = Depends(get_current_user_websocket)
) -> None:
    """Authenticated WebSocket endpoint."""
    await manager.connect(websocket, connection_id, current_user["id"])
    # ... rest of implementation ...
```

#### 2. SSE Authentication

Authenticate SSE connections:

```python
from fastapi import Depends, Request, HTTPException
from app.dependencies import get_current_user

@router.get("/events/{connection_id}")
async def authenticated_sse(
    request: Request,
    connection_id: str,
    current_user: dict = Depends(get_current_user)
) -> EventSourceResponse:
    """Authenticated SSE endpoint."""
    return EventSourceResponse(
        sse_manager.create_stream(connection_id, request, current_user["id"])
    )
```

#### 3. Authorization Checks

Implement authorization checks for message handling:

```python
from app.dependencies import check_permission

async def handle_client_message(
    connection_id: str,
    message: dict,
    user_id: str
) -> None:
    """Handle client messages with authorization."""
    message_type = message.get("type")
    
    # Check authorization based on message type
    if message_type == "admin_broadcast":
        if not await check_permission(user_id, "admin:broadcast"):
            await manager.send_personal_message(
                connection_id,
                {
                    "type": "error",
                    "message": "Unauthorized"
                }
            )
            return
    
    # Process authorized message
    # ... handle message ...
```

---

## Error Handling & Resilience

### ✅ Best Practices

#### 1. Comprehensive Error Handling

```python
from fastapi import WebSocketDisconnect
from fastapi.websockets import WebSocketState
import logging

logger = logging.getLogger(__name__)

@router.websocket("/{connection_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    connection_id: str
) -> None:
    """WebSocket endpoint with comprehensive error handling."""
    user_id = None
    
    try:
        user_id = websocket.query_params.get("user_id")
        await manager.connect(websocket, connection_id, user_id)
        
        while True:
            try:
                data = await websocket.receive_text()
                message = json.loads(data)
                await handle_client_message(connection_id, message)
            
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON from {connection_id}: {e}")
                await manager.send_personal_message(
                    connection_id,
                    {
                        "type": "error",
                        "message": "Invalid JSON format"
                    }
                )
            
            except ValueError as e:
                logger.error(f"Invalid message format from {connection_id}: {e}")
                await manager.send_personal_message(
                    connection_id,
                    {
                        "type": "error",
                        "message": str(e)
                    }
                )
            
            except Exception as e:
                logger.error(f"Error processing message from {connection_id}: {e}")
                await manager.send_personal_message(
                    connection_id,
                    {
                        "type": "error",
                        "message": "Internal server error"
                    }
                )
    
    except WebSocketDisconnect:
        logger.info(f"WebSocket {connection_id} disconnected")
        manager.disconnect(connection_id, user_id)
    
    except Exception as e:
        logger.error(f"WebSocket error for {connection_id}: {e}")
        manager.disconnect(connection_id, user_id)
```

#### 2. Retry Logic

Implement retry logic for failed message sends:

```python
from tenacity import retry, stop_after_attempt, wait_exponential

class ConnectionManager:
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10)
    )
    async def send_personal_message(
        self,
        connection_id: str,
        message: dict
    ) -> bool:
        """Send message with retry logic."""
        # ... implementation ...
```

#### 3. Circuit Breaker Pattern

Implement circuit breaker for external dependencies:

```python
from circuitbreaker import circuit

class MessageHandler:
    @circuit(failure_threshold=5, recovery_timeout=60)
    async def process_external_message(self, message: dict) -> dict:
        """Process message with circuit breaker."""
        # Call external service
        # ...
```

---

## Performance Optimization

### ✅ Best Practices

#### 1. Message Batching

Batch messages to reduce overhead:

```python
from collections import deque
import asyncio

class BatchedConnectionManager:
    """Connection manager with message batching."""
    
    def __init__(self, batch_size: int = 10, batch_interval: float = 0.1):
        self.active_connections: Dict[str, WebSocket] = {}
        self.message_queues: Dict[str, deque] = {}
        self.batch_size = batch_size
        self.batch_interval = batch_interval
    
    async def start_batching(self, connection_id: str) -> None:
        """Start batching messages for a connection."""
        while connection_id in self.active_connections:
            if connection_id in self.message_queues:
                queue = self.message_queues[connection_id]
                
                if queue:
                    # Batch messages
                    batch = []
                    while queue and len(batch) < self.batch_size:
                        batch.append(queue.popleft())
                    
                    if batch:
                        await self._send_batch(connection_id, batch)
            
            await asyncio.sleep(self.batch_interval)
    
    async def _send_batch(self, connection_id: str, batch: List[dict]) -> None:
        """Send a batch of messages."""
        websocket = self.active_connections.get(connection_id)
        if websocket and websocket.client_state == WebSocketState.CONNECTED:
            await websocket.send_json({
                "type": "batch",
                "messages": batch
            })
```

#### 2. Connection Pooling

Use connection pooling for external services:

```python
from app.core.pooling import ConnectionPool

class WebSocketService:
    def __init__(self):
        self.redis_pool = ConnectionPool(
            factory=lambda: redis.Redis(...),
            max_size=10
        )
    
    async def publish_event(self, topic: str, data: dict) -> None:
        """Publish event using connection pool."""
        async with self.redis_pool.acquire() as redis_client:
            await redis_client.publish(topic, json.dumps(data))
```

#### 3. Async Message Processing

Process messages asynchronously:

```python
import asyncio
from asyncio import Queue

class AsyncMessageProcessor:
    """Process messages asynchronously."""
    
    def __init__(self, max_workers: int = 10):
        self.message_queue: Queue = Queue()
        self.max_workers = max_workers
        self.workers: List[asyncio.Task] = []
    
    async def start(self) -> None:
        """Start worker tasks."""
        for _ in range(self.max_workers):
            self.workers.append(
                asyncio.create_task(self._worker())
            )
    
    async def _worker(self) -> None:
        """Worker task for processing messages."""
        while True:
            try:
                message = await self.message_queue.get()
                await self.process_message(message)
                self.message_queue.task_done()
            except Exception as e:
                logger.error(f"Error processing message: {e}")
    
    async def enqueue(self, message: dict) -> None:
        """Enqueue a message for processing."""
        await self.message_queue.put(message)
    
    async def process_message(self, message: dict) -> None:
        """Process a single message."""
        # ... message processing logic ...
```

---

## Security Best Practices

### ✅ Best Practices

#### 1. Input Validation

Validate all WebSocket messages:

```python
from pydantic import BaseModel, ValidationError

class WebSocketMessage(BaseModel):
    type: str
    data: dict
    timestamp: Optional[str] = None

async def handle_client_message(
    connection_id: str,
    raw_message: str
) -> None:
    """Handle client message with validation."""
    try:
        message_data = json.loads(raw_message)
        message = WebSocketMessage(**message_data)
        
        # Additional validation
        if message.type not in ALLOWED_MESSAGE_TYPES:
            raise ValueError(f"Invalid message type: {message.type}")
        
        # Process validated message
        await process_message(connection_id, message)
    
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        await manager.send_personal_message(
            connection_id,
            {"type": "error", "message": "Invalid message format"}
        )
```

#### 2. Rate Limiting

Implement rate limiting for WebSocket connections:

```python
from collections import defaultdict
from datetime import datetime, timedelta

class RateLimiter:
    """Rate limiter for WebSocket connections."""
    
    def __init__(self, max_messages: int = 100, window_seconds: int = 60):
        self.max_messages = max_messages
        self.window_seconds = window_seconds
        self.message_counts: Dict[str, deque] = defaultdict(deque)
    
    async def check_rate_limit(self, connection_id: str) -> bool:
        """Check if connection is within rate limit."""
        now = datetime.now()
        window_start = now - timedelta(seconds=self.window_seconds)
        
        # Clean old messages
        counts = self.message_counts[connection_id]
        while counts and counts[0] < window_start:
            counts.popleft()
        
        # Check limit
        if len(counts) >= self.max_messages:
            return False
        
        # Record message
        counts.append(now)
        return True

# Usage
rate_limiter = RateLimiter()

async def handle_client_message(connection_id: str, message: dict) -> None:
    """Handle message with rate limiting."""
    if not await rate_limiter.check_rate_limit(connection_id):
        await manager.send_personal_message(
            connection_id,
            {
                "type": "error",
                "message": "Rate limit exceeded"
            }
        )
        return
    
    # Process message
    # ...
```

#### 3. Origin Validation

Validate WebSocket origins:

```python
from fastapi import WebSocket, WebSocketException, status

ALLOWED_ORIGINS = ["https://example.com", "https://app.example.com"]

async def validate_origin(websocket: WebSocket) -> bool:
    """Validate WebSocket origin."""
    origin = websocket.headers.get("origin")
    
    if origin not in ALLOWED_ORIGINS:
        await websocket.close(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="Origin not allowed"
        )
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION
        )
    
    return True

@router.websocket("/{connection_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    connection_id: str
) -> None:
    """WebSocket endpoint with origin validation."""
    await validate_origin(websocket)
    # ... rest of implementation ...
```

#### 4. Message Size Limits

Enforce message size limits:

```python
MAX_MESSAGE_SIZE = 1024 * 1024  # 1MB

async def handle_client_message(
    connection_id: str,
    raw_message: str
) -> None:
    """Handle message with size validation."""
    if len(raw_message.encode('utf-8')) > MAX_MESSAGE_SIZE:
        await manager.send_personal_message(
            connection_id,
            {
                "type": "error",
                "message": "Message too large"
            }
        )
        return
    
    # Process message
    # ...
```

---

## Message Patterns & Protocols

### ✅ Best Practices

#### 1. Standardized Message Format

Use a standardized message format:

```python
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime, timezone

class WebSocketMessage(BaseModel):
    """Standard WebSocket message format."""
    id: Optional[str] = None  # Message ID for request/response correlation
    type: str  # Message type
    action: Optional[str] = None  # Action within type
    data: Optional[dict] = None  # Message payload
    timestamp: str = None  # ISO timestamp
    
    def __init__(self, **data):
        if "timestamp" not in data:
            data["timestamp"] = datetime.now(timezone.utc).isoformat()
        super().__init__(**data)

# Usage
message = WebSocketMessage(
    id="msg_123",
    type="subscribe",
    action="add",
    data={"topic": "notifications"}
)
```

#### 2. Request-Response Pattern

Implement request-response pattern:

```python
from typing import Dict
import uuid
from asyncio import Future

class RequestResponseManager:
    """Manages request-response correlation."""
    
    def __init__(self):
        self.pending_requests: Dict[str, Future] = {}
    
    async def send_request(
        self,
        connection_id: str,
        message_type: str,
        data: dict,
        timeout: float = 30.0
    ) -> dict:
        """Send a request and wait for response."""
        request_id = str(uuid.uuid4())
        future = asyncio.Future()
        self.pending_requests[request_id] = future
        
        request_message = {
            "id": request_id,
            "type": message_type,
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        await manager.send_personal_message(connection_id, request_message)
        
        try:
            response = await asyncio.wait_for(future, timeout=timeout)
            return response
        except asyncio.TimeoutError:
            del self.pending_requests[request_id]
            raise TimeoutError("Request timeout")
    
    def handle_response(self, message: dict) -> None:
        """Handle response message."""
        request_id = message.get("id")
        if request_id and request_id in self.pending_requests:
            future = self.pending_requests.pop(request_id)
            if not future.done():
                future.set_result(message)
```

#### 3. Pub/Sub Pattern

Implement pub/sub pattern:

```python
class PubSubManager:
    """Pub/sub manager for WebSocket connections."""
    
    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager
        self.topics: Dict[str, Set[str]] = defaultdict(set)  # topic -> connection_ids
    
    def subscribe(self, connection_id: str, topic: str) -> None:
        """Subscribe connection to topic."""
        self.topics[topic].add(connection_id)
        self.connection_manager.subscribe(connection_id, topic)
    
    def unsubscribe(self, connection_id: str, topic: str) -> None:
        """Unsubscribe connection from topic."""
        self.topics[topic].discard(connection_id)
        self.connection_manager.unsubscribe(connection_id, topic)
    
    async def publish(self, topic: str, message: dict) -> int:
        """Publish message to topic subscribers."""
        sent_count = 0
        for connection_id in self.topics[topic]:
            if await self.connection_manager.send_personal_message(
                connection_id,
                {
                    "type": "pubsub",
                    "topic": topic,
                    "data": message,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            ):
                sent_count += 1
        
        return sent_count
```

---

## Monitoring & Observability

### ✅ Best Practices

#### 1. Connection Metrics

Track connection metrics:

```python
from prometheus_client import Counter, Gauge, Histogram

# Metrics
websocket_connections_total = Gauge(
    "websocket_connections_total",
    "Total active WebSocket connections"
)

websocket_messages_total = Counter(
    "websocket_messages_total",
    "Total WebSocket messages",
    ["type", "direction"]
)

websocket_message_size = Histogram(
    "websocket_message_size_bytes",
    "WebSocket message size in bytes",
    buckets=[100, 500, 1000, 5000, 10000, 50000]
)

websocket_connection_duration = Histogram(
    "websocket_connection_duration_seconds",
    "WebSocket connection duration in seconds"
)

class InstrumentedConnectionManager(ConnectionManager):
    """Connection manager with metrics."""
    
    async def connect(self, websocket: WebSocket, connection_id: str) -> None:
        await super().connect(websocket, connection_id)
        websocket_connections_total.inc()
        websocket_connection_duration.observe(0)  # Start timer
    
    def disconnect(self, connection_id: str) -> None:
        super().disconnect(connection_id)
        websocket_connections_total.dec()
    
    async def send_personal_message(
        self,
        connection_id: str,
        message: dict
    ) -> bool:
        message_size = len(json.dumps(message).encode('utf-8'))
        websocket_message_size.observe(message_size)
        websocket_messages_total.labels(
            type=message.get("type", "unknown"),
            direction="outbound"
        ).inc()
        
        return await super().send_personal_message(connection_id, message)
```

#### 2. Structured Logging

Use structured logging:

```python
import structlog

logger = structlog.get_logger()

@router.websocket("/{connection_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    connection_id: str
) -> None:
    """WebSocket endpoint with structured logging."""
    user_id = websocket.query_params.get("user_id")
    
    logger.info(
        "websocket_connecting",
        connection_id=connection_id,
        user_id=user_id,
        remote_addr=websocket.client.host
    )
    
    try:
        await manager.connect(websocket, connection_id, user_id)
        
        logger.info(
            "websocket_connected",
            connection_id=connection_id,
            user_id=user_id
        )
        
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            logger.debug(
                "websocket_message_received",
                connection_id=connection_id,
                message_type=message.get("type")
            )
            
            await handle_client_message(connection_id, message)
    
    except WebSocketDisconnect:
        logger.info(
            "websocket_disconnected",
            connection_id=connection_id,
            user_id=user_id
        )
        manager.disconnect(connection_id, user_id)
    
    except Exception as e:
        logger.error(
            "websocket_error",
            connection_id=connection_id,
            user_id=user_id,
            error=str(e),
            exc_info=True
        )
        manager.disconnect(connection_id, user_id)
```

#### 3. Health Checks

Implement health check endpoints:

```python
@router.get("/health/websockets")
async def websocket_health() -> dict:
    """Health check for WebSocket service."""
    return {
        "status": "healthy",
        "active_connections": len(manager.active_connections),
        "total_subscriptions": sum(
            len(subs) for subs in manager.subscriptions.values()
        ),
        "unique_users": len(manager.user_connections)
    }
```

---

## Testing Strategies

### ✅ Best Practices

#### 1. WebSocket Testing

Test WebSocket endpoints:

```python
import pytest
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket

@pytest.mark.asyncio
async def test_websocket_connection():
    """Test WebSocket connection."""
    client = TestClient(app)
    
    with client.websocket_connect("/ws/test_connection") as websocket:
        # Test connection
        data = websocket.receive_json()
        assert data["type"] == "connection_established"
        
        # Test sending message
        websocket.send_json({
            "type": "ping"
        })
        response = websocket.receive_json()
        assert response["type"] == "pong"

@pytest.mark.asyncio
async def test_websocket_subscription():
    """Test WebSocket subscription."""
    client = TestClient(app)
    
    with client.websocket_connect("/ws/test_connection") as websocket:
        # Subscribe
        websocket.send_json({
            "type": "subscribe",
            "topic": "notifications"
        })
        response = websocket.receive_json()
        assert response["type"] == "subscription_confirmed"
        
        # Publish event (from another connection or background task)
        await manager.publish("notifications", {"message": "test"})
        
        # Receive event
        event = websocket.receive_json()
        assert event["type"] == "pubsub"
        assert event["topic"] == "notifications"
```

#### 2. SSE Testing

Test SSE endpoints:

```python
@pytest.mark.asyncio
async def test_sse_endpoint():
    """Test SSE endpoint."""
    client = TestClient(app)
    
    response = client.get("/events/test_connection")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream"
    
    # Parse SSE events
    events = []
    for line in response.text.split("\n"):
        if line.startswith("data:"):
            data = json.loads(line[5:])
            events.append(data)
    
    assert len(events) > 0
    assert events[0]["type"] == "connected"
```

#### 3. Integration Testing

Test WebSocket/SSE integration:

```python
@pytest.mark.asyncio
async def test_websocket_integration():
    """Test WebSocket integration with business logic."""
    client = TestClient(app)
    
    with client.websocket_connect("/ws/test_connection?user_id=test_user") as websocket:
        # Trigger business event
        await trigger_feature_flag_change("test_flag")
        
        # Receive notification
        notification = websocket.receive_json()
        assert notification["type"] == "flag_change"
        assert notification["flag_name"] == "test_flag"
```

---

## Production Deployment

### ✅ Best Practices

#### 1. Production Configuration

Configure for production:

```python
from app.config import settings

class ConnectionManager:
    def __init__(self):
        self.max_connections = settings.WEBSOCKET_MAX_CONNECTIONS
        self.idle_timeout = settings.WEBSOCKET_IDLE_TIMEOUT
        self.ping_interval = settings.WEBSOCKET_PING_INTERVAL
        self.message_queue_size = settings.WEBSOCKET_QUEUE_SIZE
        # ... rest of initialization ...
```

#### 2. Load Balancing Considerations

Handle load balancing:

```python
# Use Redis for distributed connection management
import redis.asyncio as redis

class DistributedConnectionManager:
    """Connection manager for distributed deployments."""
    
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client
        self.local_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, connection_id: str) -> None:
        await websocket.accept()
        self.local_connections[connection_id] = websocket
        
        # Register in Redis
        await self.redis_client.setex(
            f"ws:connection:{connection_id}",
            3600,  # TTL
            json.dumps({
                "server_id": settings.SERVER_ID,
                "connected_at": datetime.now(timezone.utc).isoformat()
            })
        )
    
    async def broadcast_distributed(self, topic: str, message: dict) -> None:
        """Broadcast to all servers."""
        await self.redis_client.publish(
            f"ws:broadcast:{topic}",
            json.dumps(message)
        )
```

#### 3. Production Checklist

- [ ] Connection limits configured
- [ ] Rate limiting enabled
- [ ] Authentication/authorization implemented
- [ ] Input validation on all messages
- [ ] Error handling comprehensive
- [ ] Monitoring and metrics configured
- [ ] Structured logging enabled
- [ ] Health checks implemented
- [ ] Graceful shutdown handling
- [ ] Load balancing considerations
- [ ] Security headers configured
- [ ] Message size limits enforced
- [ ] Connection timeouts configured
- [ ] Heartbeat/ping-pong implemented
- [ ] Resource cleanup on disconnect

---

## Summary

### Key Takeaways

1. **Connection Management**: Use a centralized connection manager with subscription support
2. **Authentication**: Always authenticate WebSocket/SSE connections
3. **Error Handling**: Implement comprehensive error handling and recovery
4. **Performance**: Use batching, pooling, and async processing
5. **Security**: Validate inputs, enforce rate limits, check origins
6. **Monitoring**: Track metrics and use structured logging
7. **Testing**: Test WebSocket/SSE endpoints thoroughly
8. **Production**: Configure for scale and reliability

### When to Use WebSockets vs SSE

**Use WebSockets when:**
- Bidirectional communication needed
- Low latency critical
- Real-time gaming or chat
- Binary data transmission
- Complex message protocols

**Use SSE when:**
- Server-to-client only
- Simpler implementation needed
- HTTP/2 benefits desired
- Browser auto-reconnection needed
- Event streaming use cases

---

## References

- [FastAPI WebSockets Documentation](https://fastapi.tiangolo.com/advanced/websockets/)
- [Starlette WebSockets](https://www.starlette.io/websockets/)
- [Server-Sent Events Specification](https://html.spec.whatwg.org/multipage/server-sent-events.html)
- [sse-starlette Library](https://github.com/sysid/sse-starlette)
- [WebSocket Protocol RFC 6455](https://tools.ietf.org/html/rfc6455)

---

**Version**: v1.0.0  
**Last Updated**: 2025-01-14
