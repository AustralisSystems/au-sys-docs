# Background Tasks & Celery Best Practices

**Version**: v1.0.0  
**Last Updated**: 2025-01-14

This document provides comprehensive best practices for implementing background tasks in FastAPI applications, covering FastAPI BackgroundTasks (simple background operations), Celery distributed task queue (task definition, workers, brokers, result backends), Celery Beat (periodic task scheduling), task retries and error handling, task monitoring and observability, FastAPI integration patterns, performance optimization, and production deployment.

---

## Table of Contents

1. [Architecture Principles](#architecture-principles)
2. [FastAPI BackgroundTasks](#fastapi-backgroundtasks)
3. [Celery Setup & Configuration](#celery-setup--configuration)
4. [Celery Task Definition](#celery-task-definition)
5. [Celery Workers](#celery-workers)
6. [Celery Beat (Periodic Tasks)](#celery-beat-periodic-tasks)
7. [Result Backends](#result-backends)
8. [Task Retries & Error Handling](#task-retries--error-handling)
9. [Task Monitoring & Observability](#task-monitoring--observability)
10. [FastAPI Integration](#fastapi-integration)
11. [Performance Optimization](#performance-optimization)
12. [Production Deployment](#production-deployment)

---

## Architecture Principles

### When to Use BackgroundTasks vs Celery

**REQUIRED**: Choose the right technology:

**Use FastAPI BackgroundTasks when:**
- **Simple operations** that don't need persistence
- **Request-scoped tasks** tied to HTTP request lifecycle
- **No distributed execution** needed (single server)
- **No task retries** or complex error handling required
- **No task scheduling** needed
- **Lightweight operations** (logging, notifications, cleanup)

**Use Celery when:**
- **Long-running tasks** (> 30 seconds)
- **Distributed execution** across multiple workers
- **Task persistence** and retry logic needed
- **Periodic/scheduled tasks** (Celery Beat)
- **Task result tracking** and retrieval
- **Complex task workflows** (chains, groups, chords)
- **High-volume task processing**
- **Task prioritization** and routing

### Task Processing Patterns

**REQUIRED**: Follow task processing patterns:

1. **Fire-and-Forget**: Execute task without waiting for result
2. **Async Result**: Execute task and retrieve result later
3. **Synchronous Result**: Execute task and wait for result (not recommended for long tasks)
4. **Periodic Tasks**: Schedule tasks to run at intervals
5. **Task Chains**: Execute tasks sequentially
6. **Task Groups**: Execute tasks in parallel
7. **Task Chords**: Execute tasks in parallel, then callback

---

## FastAPI BackgroundTasks

### Basic Background Task

**REQUIRED**: Basic background task:

```python
from fastapi import FastAPI, BackgroundTasks
import logging

logger = logging.getLogger(__name__)

app = FastAPI()

def write_log(message: str):
    """Background task function."""
    logger.info(f"Background task: {message}")

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    """Endpoint with background task."""
    background_tasks.add_task(write_log, f"Notification sent to {email}")
    return {"message": "Notification sent"}

@app.post("/send-notification/{email}")
async def send_notification_with_message(
    email: str,
    message: str,
    background_tasks: BackgroundTasks,
):
    """Endpoint with background task and parameters."""
    background_tasks.add_task(write_log, f"Notification to {email}: {message}")
    return {"message": "Notification scheduled"}
```

### Async Background Tasks

**REQUIRED**: Async background tasks:

```python
import asyncio
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

async def send_email_async(email: str, subject: str, body: str):
    """Async background task."""
    # Simulate async email sending
    await asyncio.sleep(1)
    logger.info(f"Email sent to {email}: {subject}")

@app.post("/send-email/{email}")
async def send_email(
    email: str,
    subject: str,
    body: str,
    background_tasks: BackgroundTasks,
):
    """Endpoint with async background task."""
    background_tasks.add_task(send_email_async, email, subject, body)
    return {"message": "Email scheduled"}
```

### Multiple Background Tasks

**REQUIRED**: Multiple background tasks:

```python
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

def log_action(action: str):
    """Log action."""
    logger.info(f"Action: {action}")

def send_notification(email: str, message: str):
    """Send notification."""
    logger.info(f"Notification to {email}: {message}")

def update_analytics(event: str):
    """Update analytics."""
    logger.info(f"Analytics: {event}")

@app.post("/process/{user_id}")
async def process_user(
    user_id: str,
    background_tasks: BackgroundTasks,
):
    """Endpoint with multiple background tasks."""
    background_tasks.add_task(log_action, f"process_user_{user_id}")
    background_tasks.add_task(send_notification, f"{user_id}@example.com", "Processed")
    background_tasks.add_task(update_analytics, f"user_processed_{user_id}")
    
    return {"message": "Processing started", "user_id": user_id}
```

### Background Tasks with Dependency Injection

**REQUIRED**: Background tasks with dependency injection:

```python
from fastapi import Depends, BackgroundTasks
from typing import Annotated

def get_background_tasks() -> BackgroundTasks:
    """Dependency for background tasks."""
    return BackgroundTasks()

def log_query(background_tasks: BackgroundTasks, q: str | None = None):
    """Dependency that adds background task."""
    if q:
        background_tasks.add_task(log_action, f"query: {q}")
    return q

@app.post("/search")
async def search(
    query: str,
    background_tasks: Annotated[BackgroundTasks, Depends(get_background_tasks)],
    q: Annotated[str | None, Depends(log_query)] = None,
):
    """Endpoint with background tasks from dependencies."""
    background_tasks.add_task(log_action, f"search: {query}")
    return {"results": []}
```

### Background Tasks Error Handling

**REQUIRED**: Error handling in background tasks:

```python
from fastapi import FastAPI, BackgroundTasks
import logging

logger = logging.getLogger(__name__)

app = FastAPI()

def safe_background_task(data: str):
    """Background task with error handling."""
    try:
        # Process data
        logger.info(f"Processing: {data}")
        # Simulate potential error
        if data == "error":
            raise ValueError("Simulated error")
    except Exception as e:
        logger.error(f"Background task error: {e}", exc_info=True)
        # Optionally: send error notification, update database, etc.

@app.post("/process")
async def process_data(
    data: str,
    background_tasks: BackgroundTasks,
):
    """Endpoint with error-handled background task."""
    background_tasks.add_task(safe_background_task, data)
    return {"message": "Processing started"}
```

---

## Celery Setup & Configuration

### Basic Celery Configuration

**REQUIRED**: Basic Celery setup:

```python
from celery import Celery
import os

# Create Celery app
celery_app = Celery(
    "tasks",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=4,
    worker_max_tasks_per_child=1000,
)
```

### Advanced Celery Configuration

**REQUIRED**: Advanced Celery configuration:

```python
from celery import Celery
from celery.schedules import crontab

celery_app = Celery("tasks")

# Broker and backend
celery_app.conf.broker_url = "redis://localhost:6379/0"
celery_app.conf.result_backend = "redis://localhost:6379/0"

# Task settings
celery_app.conf.update(
    # Serialization
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    
    # Timezone
    timezone="UTC",
    enable_utc=True,
    
    # Task execution
    task_acks_late=True,  # Acknowledge after task completion
    task_reject_on_worker_lost=True,  # Reject tasks if worker dies
    task_track_started=True,  # Track when task starts
    task_time_limit=30 * 60,  # Hard time limit
    task_soft_time_limit=25 * 60,  # Soft time limit
    
    # Worker settings
    worker_prefetch_multiplier=4,  # Prefetch 4 tasks per worker
    worker_max_tasks_per_child=1000,  # Restart worker after 1000 tasks
    worker_disable_rate_limits=False,
    
    # Result backend
    result_expires=3600,  # Results expire after 1 hour
    result_extended=True,  # Store additional metadata
    result_compression="gzip",  # Compress results
    
    # Redis settings
    broker_transport_options={
        "visibility_timeout": 43200,  # 12 hours
        "retry_policy": {
            "timeout": 5.0,
        },
    },
    result_backend_transport_options={
        "visibility_timeout": 43200,
        "retry_policy": {
            "timeout": 5.0,
        },
    },
    
    # Beat schedule (periodic tasks)
    beat_schedule={
        "periodic-task": {
            "task": "tasks.periodic_task",
            "schedule": crontab(minute="*/5"),  # Every 5 minutes
        },
    },
)
```

### Celery with Redis Sentinel

**RECOMMENDED**: Redis Sentinel for high availability:

```python
from celery import Celery

celery_app = Celery("tasks")

# Redis Sentinel configuration
celery_app.conf.broker_url = (
    "sentinel://localhost:26379;"
    "sentinel://localhost:26380;"
    "sentinel://localhost:26381"
)
celery_app.conf.broker_transport_options = {
    "master_name": "mymaster",
    "sentinel_kwargs": {
        "password": "sentinel_password",
    },
}

celery_app.conf.result_backend = (
    "sentinel://localhost:26379;"
    "sentinel://localhost:26380;"
    "sentinel://localhost:26381"
)
celery_app.conf.result_backend_transport_options = {
    "master_name": "mymaster",
}
```

---

## Celery Task Definition

### Basic Task

**REQUIRED**: Basic Celery task:

```python
from celery import Celery

celery_app = Celery("tasks")

@celery_app.task
def add(x: int, y: int) -> int:
    """Add two numbers."""
    return x + y

# Execute task
result = add.delay(4, 4)
print(result.get())  # 8
```

### Async Task

**REQUIRED**: Async Celery task:

```python
from celery import Celery
import asyncio

celery_app = Celery("tasks")

@celery_app.task
async def async_task(data: dict) -> dict:
    """Async Celery task."""
    # Async operations
    await asyncio.sleep(1)
    return {"processed": data}

# Execute async task
result = async_task.delay({"key": "value"})
print(result.get())  # {"processed": {"key": "value"}}
```

### Task with Options

**REQUIRED**: Task with options:

```python
from celery import Celery
from datetime import timedelta

celery_app = Celery("tasks")

@celery_app.task(
    bind=True,  # Pass task instance as first argument
    name="tasks.process_data",  # Custom task name
    max_retries=3,  # Maximum retries
    default_retry_delay=60,  # Retry delay in seconds
    soft_time_limit=300,  # Soft time limit (5 minutes)
    time_limit=600,  # Hard time limit (10 minutes)
    ignore_result=False,  # Store result
    track_started=True,  # Track when task starts
    acks_late=True,  # Acknowledge after completion
    reject_on_worker_lost=True,  # Reject if worker dies
)
def process_data(self, data: dict) -> dict:
    """Task with options."""
    try:
        # Process data
        return {"status": "success", "data": data}
    except Exception as exc:
        # Retry on failure
        raise self.retry(exc=exc, countdown=60)
```

### Task with Retry Logic

**REQUIRED**: Task with retry logic:

```python
from celery import Celery
from celery.exceptions import Retry
import time

celery_app = Celery("tasks")

@celery_app.task(bind=True, max_retries=3)
def process_with_retry(self, data: dict) -> dict:
    """Task with retry logic."""
    try:
        # Simulate processing
        if data.get("should_fail"):
            raise ValueError("Processing failed")
        
        return {"status": "success", "data": data}
        
    except ValueError as exc:
        # Retry with exponential backoff
        retry_count = self.request.retries
        countdown = 2 ** retry_count  # Exponential backoff: 1s, 2s, 4s
        
        if retry_count < self.max_retries:
            raise self.retry(exc=exc, countdown=countdown)
        else:
            # Max retries reached
            return {"status": "failed", "error": str(exc)}
```

### Task Routing

**REQUIRED**: Task routing to specific queues:

```python
from celery import Celery

celery_app = Celery("tasks")

@celery_app.task(queue="high_priority")
def high_priority_task(data: dict) -> dict:
    """High priority task."""
    return {"processed": data}

@celery_app.task(queue="low_priority")
def low_priority_task(data: dict) -> dict:
    """Low priority task."""
    return {"processed": data}

# Configure queue routing
celery_app.conf.task_routes = {
    "tasks.high_priority_task": {"queue": "high_priority"},
    "tasks.low_priority_task": {"queue": "low_priority"},
}
```

### Task Priorities

**REQUIRED**: Task priorities:

```python
from celery import Celery

celery_app = Celery("tasks")

@celery_app.task
def process_task(data: dict, priority: int = 5) -> dict:
    """Task with priority."""
    return {"processed": data}

# Execute with priority
result = process_task.apply_async(
    args=[{"key": "value"}],
    priority=10,  # High priority
)
```

---

## Celery Workers

### Starting Workers

**REQUIRED**: Start Celery workers:

```bash
# Basic worker
celery -A tasks worker --loglevel=info

# Worker with concurrency
celery -A tasks worker --loglevel=info --concurrency=4

# Worker for specific queue
celery -A tasks worker --loglevel=info --queues=high_priority,low_priority

# Worker with pool type
celery -A tasks worker --loglevel=info --pool=prefork --concurrency=4

# Worker with max tasks per child
celery -A tasks worker --loglevel=info --max-tasks-per-child=1000
```

### Worker Configuration

**REQUIRED**: Worker configuration:

```python
from celery import Celery

celery_app = Celery("tasks")

celery_app.conf.update(
    # Worker pool
    worker_pool="prefork",  # or "solo", "threads", "gevent", "eventlet"
    worker_concurrency=4,  # Number of worker processes/threads
    
    # Task prefetching
    worker_prefetch_multiplier=4,  # Prefetch 4 tasks per worker
    
    # Worker lifecycle
    worker_max_tasks_per_child=1000,  # Restart worker after 1000 tasks
    worker_max_memory_per_child=200000,  # Restart if memory exceeds 200MB
    
    # Task acknowledgment
    task_acks_late=True,  # Acknowledge after task completion
    task_reject_on_worker_lost=True,  # Reject tasks if worker dies
    
    # Time limits
    task_time_limit=30 * 60,  # Hard time limit (30 minutes)
    task_soft_time_limit=25 * 60,  # Soft time limit (25 minutes)
)
```

### Multiple Workers

**RECOMMENDED**: Run multiple workers for different queues:

```bash
# High priority worker
celery -A tasks worker --loglevel=info --queues=high_priority --concurrency=8 --hostname=worker1@%h

# Low priority worker
celery -A tasks worker --loglevel=info --queues=low_priority --concurrency=2 --hostname=worker2@%h

# Default queue worker
celery -A tasks worker --loglevel=info --queues=default --concurrency=4 --hostname=worker3@%h
```

### Worker Monitoring

**REQUIRED**: Monitor workers:

```python
from celery import Celery
from celery.events.state import State
from celery.events import Events

celery_app = Celery("tasks")

def monitor_workers():
    """Monitor Celery workers."""
    state = State()
    
    def on_event(event):
        """Handle worker events."""
        state.event(event)
        
        # Get worker stats
        for worker_name, worker in state.workers.items():
            print(f"Worker: {worker_name}")
            print(f"  Active: {len(worker.active)}")
            print(f"  Processed: {worker.stats.get('total', {}).get('tasks.succeeded', 0)}")
    
    with Events(celery_app).connect() as connection:
        connection.itersafe(on_event, timeout=1)

# Use Flower for web-based monitoring
# pip install flower
# celery -A tasks flower
```

---

## Celery Beat (Periodic Tasks)

### Basic Periodic Task

**REQUIRED**: Basic periodic task:

```python
from celery import Celery
from celery.schedules import crontab

celery_app = Celery("tasks")

@celery_app.task
def periodic_task():
    """Periodic task."""
    print("Running periodic task")

# Configure beat schedule
celery_app.conf.beat_schedule = {
    "periodic-task": {
        "task": "tasks.periodic_task",
        "schedule": crontab(minute="*/5"),  # Every 5 minutes
    },
}
```

### Periodic Task Schedules

**REQUIRED**: Various schedule types:

```python
from celery import Celery
from celery.schedules import crontab, solar
from datetime import timedelta

celery_app = Celery("tasks")

celery_app.conf.beat_schedule = {
    # Every 30 seconds
    "every-30-seconds": {
        "task": "tasks.every_30_seconds",
        "schedule": 30.0,
    },
    
    # Every minute
    "every-minute": {
        "task": "tasks.every_minute",
        "schedule": crontab(minute="*"),
    },
    
    # Every 5 minutes
    "every-5-minutes": {
        "task": "tasks.every_5_minutes",
        "schedule": crontab(minute="*/5"),
    },
    
    # Every hour
    "every-hour": {
        "task": "tasks.every_hour",
        "schedule": crontab(minute=0),
    },
    
    # Daily at midnight
    "daily-midnight": {
        "task": "tasks.daily_task",
        "schedule": crontab(hour=0, minute=0),
    },
    
    # Weekly on Monday at 9 AM
    "weekly-monday": {
        "task": "tasks.weekly_task",
        "schedule": crontab(day_of_week=1, hour=9, minute=0),
    },
    
    # Monthly on 1st at midnight
    "monthly": {
        "task": "tasks.monthly_task",
        "schedule": crontab(day_of_month=1, hour=0, minute=0),
    },
    
    # Using timedelta
    "every-hour-timedelta": {
        "task": "tasks.hourly_task",
        "schedule": timedelta(hours=1),
    },
}
```

### Starting Celery Beat

**REQUIRED**: Start Celery Beat:

```bash
# Start beat scheduler
celery -A tasks beat --loglevel=info

# Start beat with database scheduler (for persistence)
celery -A tasks beat --loglevel=info --scheduler=django_celery_beat.schedulers:DatabaseScheduler
```

### Dynamic Periodic Tasks

**RECOMMENDED**: Dynamic periodic tasks with database:

```python
from celery import Celery
from celery.schedules import crontab
from django_celery_beat.models import PeriodicTask, CrontabSchedule

celery_app = Celery("tasks")

def create_periodic_task(name: str, task: str, schedule: dict):
    """Create dynamic periodic task."""
    # Create crontab schedule
    crontab_schedule, _ = CrontabSchedule.objects.get_or_create(
        minute=schedule.get("minute", "*"),
        hour=schedule.get("hour", "*"),
        day_of_week=schedule.get("day_of_week", "*"),
        day_of_month=schedule.get("day_of_month", "*"),
        month_of_year=schedule.get("month_of_year", "*"),
    )
    
    # Create periodic task
    periodic_task, created = PeriodicTask.objects.get_or_create(
        name=name,
        defaults={
            "task": task,
            "crontab": crontab_schedule,
            "enabled": True,
        },
    )
    
    return periodic_task
```

---

## Result Backends

### Redis Result Backend

**REQUIRED**: Redis result backend:

```python
from celery import Celery

celery_app = Celery("tasks")

# Configure Redis result backend
celery_app.conf.result_backend = "redis://localhost:6379/0"

# Configure result backend options
celery_app.conf.result_backend_transport_options = {
    "visibility_timeout": 43200,  # 12 hours
    "retry_policy": {
        "timeout": 5.0,
    },
    "global_keyprefix": "myapp:",  # Key prefix
}

# Configure result expiration
celery_app.conf.result_expires = 3600  # 1 hour

# Configure result compression
celery_app.conf.result_compression = "gzip"

# Configure extended metadata
celery_app.conf.result_extended = True
```

### Database Result Backend

**RECOMMENDED**: Database result backend:

```python
from celery import Celery

celery_app = Celery("tasks")

# PostgreSQL result backend
celery_app.conf.result_backend = "db+postgresql://user:pass@localhost/celery_results"

# SQLAlchemy result backend
celery_app.conf.result_backend = "db+sqlite:///celery_results.db"
```

### RPC Result Backend

**RECOMMENDED**: RPC result backend (for development):

```python
from celery import Celery

celery_app = Celery("tasks")

# RPC result backend
celery_app.conf.result_backend = "rpc://"
celery_app.conf.result_persistent = False
```

### Task Result Retrieval

**REQUIRED**: Retrieve task results:

```python
from celery.result import AsyncResult

# Execute task
result = process_task.delay({"key": "value"})

# Get task ID
task_id = result.id

# Check if task is ready
if result.ready():
    print(result.get())  # Get result
else:
    print("Task not ready")

# Get result with timeout
try:
    result_value = result.get(timeout=10)  # Wait up to 10 seconds
except TimeoutError:
    print("Task timeout")

# Check task state
print(result.state)  # PENDING, STARTED, SUCCESS, FAILURE, RETRY, REVOKED

# Get result info
print(result.info)  # Result or exception info

# Forget result (delete from backend)
result.forget()
```

---

## Task Retries & Error Handling

### Task Retry Configuration

**REQUIRED**: Task retry configuration:

```python
from celery import Celery
from celery.exceptions import Retry

celery_app = Celery("tasks")

@celery_app.task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(ValueError, ConnectionError),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
)
def process_with_retry(self, data: dict) -> dict:
    """Task with retry configuration."""
    try:
        # Process data
        if data.get("should_fail"):
            raise ValueError("Processing failed")
        
        return {"status": "success", "data": data}
        
    except (ValueError, ConnectionError) as exc:
        # Auto-retry on these exceptions
        raise self.retry(exc=exc)
```

### Manual Retry Logic

**REQUIRED**: Manual retry logic:

```python
from celery import Celery
from celery.exceptions import Retry

celery_app = Celery("tasks")

@celery_app.task(bind=True, max_retries=3)
def process_with_manual_retry(self, data: dict) -> dict:
    """Task with manual retry logic."""
    try:
        # Process data
        result = process_data(data)
        return {"status": "success", "result": result}
        
    except ValueError as exc:
        # Calculate exponential backoff
        retry_count = self.request.retries
        countdown = min(2 ** retry_count, 600)  # Max 10 minutes
        
        if retry_count < self.max_retries:
            raise self.retry(exc=exc, countdown=countdown)
        else:
            # Max retries reached, log and return failure
            logger.error(f"Task failed after {self.max_retries} retries: {exc}")
            return {"status": "failed", "error": str(exc)}
```

### Task Error Handling

**REQUIRED**: Comprehensive error handling:

```python
from celery import Celery
from celery.signals import task_failure, task_success

celery_app = Celery("tasks")

@celery_app.task(bind=True)
def process_task(self, data: dict) -> dict:
    """Task with error handling."""
    try:
        # Process data
        result = process_data(data)
        return {"status": "success", "result": result}
        
    except ValueError as exc:
        # Handle specific error
        logger.error(f"Value error in task: {exc}")
        raise
    except Exception as exc:
        # Handle unexpected errors
        logger.error(f"Unexpected error in task: {exc}", exc_info=True)
        raise

# Error signal handler
@task_failure.connect
def task_failure_handler(sender=None, task_id=None, exception=None, **kwargs):
    """Handle task failures."""
    logger.error(f"Task {task_id} failed: {exception}")

# Success signal handler
@task_success.connect
def task_success_handler(sender=None, result=None, **kwargs):
    """Handle task success."""
    logger.info(f"Task {sender.name} succeeded: {result}")
```

---

## Task Monitoring & Observability

### Flower Monitoring

**REQUIRED**: Use Flower for monitoring:

```bash
# Install Flower
pip install flower

# Start Flower
celery -A tasks flower --port=5555

# Access Flower UI
# http://localhost:5555
```

### Prometheus Metrics

**RECOMMENDED**: Prometheus metrics:

```python
from celery import Celery
from prometheus_client import Counter, Histogram, Gauge

celery_app = Celery("tasks")

# Metrics
task_total = Counter(
    "celery_tasks_total",
    "Total Celery tasks",
    ["task_name", "status"],
)

task_duration = Histogram(
    "celery_task_duration_seconds",
    "Celery task duration",
    ["task_name"],
)

active_tasks = Gauge(
    "celery_active_tasks",
    "Active Celery tasks",
)

@celery_app.task(bind=True)
def monitored_task(self, data: dict) -> dict:
    """Task with Prometheus metrics."""
    task_name = self.name
    
    with task_duration.labels(task_name=task_name).time():
        try:
            result = process_data(data)
            task_total.labels(task_name=task_name, status="success").inc()
            return {"status": "success", "result": result}
        except Exception as exc:
            task_total.labels(task_name=task_name, status="failure").inc()
            raise
```

### Structured Logging

**REQUIRED**: Structured logging:

```python
from celery import Celery
import structlog

celery_app = Celery("tasks")

logger = structlog.get_logger()

@celery_app.task(bind=True)
def logged_task(self, data: dict) -> dict:
    """Task with structured logging."""
    task_id = self.request.id
    task_name = self.name
    
    logger.info(
        "task_started",
        task_id=task_id,
        task_name=task_name,
        data=data,
    )
    
    try:
        result = process_data(data)
        
        logger.info(
            "task_completed",
            task_id=task_id,
            task_name=task_name,
            result=result,
        )
        
        return {"status": "success", "result": result}
        
    except Exception as exc:
        logger.error(
            "task_failed",
            task_id=task_id,
            task_name=task_name,
            error=str(exc),
            exc_info=True,
        )
        raise
```

---

## FastAPI Integration

### Celery Task from FastAPI

**REQUIRED**: Call Celery tasks from FastAPI:

```python
from fastapi import FastAPI, HTTPException
from celery.result import AsyncResult
from tasks import process_task

app = FastAPI()

@app.post("/process")
async def process_endpoint(data: dict):
    """FastAPI endpoint that calls Celery task."""
    # Execute Celery task
    task = process_task.delay(data)
    
    return {
        "task_id": task.id,
        "status": "processing",
        "check_status_url": f"/tasks/{task.id}",
    }

@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    """Get task status."""
    result = AsyncResult(task_id, app=celery_app)
    
    if result.ready():
        if result.successful():
            return {
                "task_id": task_id,
                "status": "completed",
                "result": result.get(),
            }
        else:
            return {
                "task_id": task_id,
                "status": "failed",
                "error": str(result.info),
            }
    else:
        return {
            "task_id": task_id,
            "status": result.state,
        }
```

### FastAPI with Celery Dependency

**RECOMMENDED**: Celery dependency injection:

```python
from fastapi import FastAPI, Depends
from celery import Celery

celery_app = Celery("tasks")

def get_celery() -> Celery:
    """Dependency for Celery app."""
    return celery_app

@app.post("/process")
async def process_endpoint(
    data: dict,
    celery: Celery = Depends(get_celery),
):
    """FastAPI endpoint with Celery dependency."""
    task = celery.send_task("tasks.process_task", args=[data])
    
    return {"task_id": task.id}
```

### BackgroundTasks vs Celery Decision

**REQUIRED**: Choose based on requirements:

```python
from fastapi import FastAPI, BackgroundTasks
from celery import Celery

app = FastAPI()
celery_app = Celery("tasks")

def simple_log(message: str):
    """Simple logging task - use BackgroundTasks."""
    logger.info(message)

@celery_app.task
def complex_processing(data: dict) -> dict:
    """Complex processing - use Celery."""
    # Long-running, needs retry, etc.
    return process_data(data)

@app.post("/simple")
async def simple_endpoint(
    message: str,
    background_tasks: BackgroundTasks,
):
    """Use BackgroundTasks for simple operations."""
    background_tasks.add_task(simple_log, message)
    return {"message": "Logged"}

@app.post("/complex")
async def complex_endpoint(data: dict):
    """Use Celery for complex operations."""
    task = complex_processing.delay(data)
    return {"task_id": task.id}
```

---

## Performance Optimization

### Task Batching

**RECOMMENDED**: Batch tasks for efficiency:

```python
from celery import Celery, group, chord

celery_app = Celery("tasks")

@celery_app.task
def process_item(item: dict) -> dict:
    """Process single item."""
    return {"processed": item}

@app.post("/process-batch")
async def process_batch_endpoint(items: list[dict]):
    """Process batch of items."""
    # Create group of tasks
    job = group(process_item.s(item) for item in items)
    
    # Execute group
    result = job.apply_async()
    
    # Wait for all tasks to complete
    results = result.get()
    
    return {"results": results}
```

### Task Chaining

**RECOMMENDED**: Chain tasks sequentially:

```python
from celery import Celery, chain

celery_app = Celery("tasks")

@celery_app.task
def step1(data: dict) -> dict:
    """First step."""
    return {"step1": "done", **data}

@celery_app.task
def step2(data: dict) -> dict:
    """Second step."""
    return {"step2": "done", **data}

@celery_app.task
def step3(data: dict) -> dict:
    """Third step."""
    return {"step3": "done", **data}

@app.post("/process-chain")
async def process_chain_endpoint(data: dict):
    """Process data through chain."""
    # Create chain
    workflow = chain(
        step1.s(data),
        step2.s(),
        step3.s(),
    )
    
    # Execute chain
    result = workflow.apply_async()
    
    return {"task_id": result.id}
```

### Task Chords

**RECOMMENDED**: Parallel tasks with callback:

```python
from celery import Celery, chord, group

celery_app = Celery("tasks")

@celery_app.task
def process_item(item: dict) -> dict:
    """Process single item."""
    return {"processed": item}

@celery_app.task
def aggregate_results(results: list[dict]) -> dict:
    """Aggregate results."""
    return {"total": len(results), "results": results}

@app.post("/process-chord")
async def process_chord_endpoint(items: list[dict]):
    """Process items in parallel, then aggregate."""
    # Create chord (parallel tasks + callback)
    workflow = chord(
        group(process_item.s(item) for item in items),
        aggregate_results.s(),
    )
    
    # Execute chord
    result = workflow.apply_async()
    
    return {"task_id": result.id}
```

---

## Production Deployment

### Docker Compose Configuration

**REQUIRED**: Docker Compose for Celery:

```yaml
version: '3.8'

services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  web:
    build: .
    command: uvicorn main:app --host 0.0.0.0 --port 8000
    ports:
      - "8000:8000"
    depends_on:
      - redis
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0

  worker:
    build: .
    command: celery -A tasks worker --loglevel=info --concurrency=4
    depends_on:
      - redis
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0

  beat:
    build: .
    command: celery -A tasks beat --loglevel=info
    depends_on:
      - redis
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0

  flower:
    build: .
    command: celery -A tasks flower --port=5555
    ports:
      - "5555:5555"
    depends_on:
      - redis
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0

volumes:
  redis_data:
```

### Production Configuration

**REQUIRED**: Production Celery configuration:

```python
from celery import Celery
import os

celery_app = Celery("tasks")

# Production settings
celery_app.conf.update(
    # Broker and backend
    broker_url=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    result_backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
    
    # Security
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    
    # Performance
    worker_prefetch_multiplier=4,
    worker_max_tasks_per_child=1000,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    
    # Reliability
    task_time_limit=30 * 60,
    task_soft_time_limit=25 * 60,
    broker_transport_options={
        "visibility_timeout": 43200,
        "retry_policy": {
            "timeout": 5.0,
        },
    },
    
    # Results
    result_expires=3600,
    result_compression="gzip",
    result_extended=True,
)
```

### Health Checks

**REQUIRED**: Health check endpoints:

```python
from fastapi import FastAPI
from celery import Celery
from celery.result import AsyncResult

app = FastAPI()
celery_app = Celery("tasks")

@app.get("/health/celery")
async def celery_health():
    """Celery health check."""
    try:
        # Check broker connection
        inspect = celery_app.control.inspect()
        stats = inspect.stats()
        
        if stats:
            return {
                "status": "healthy",
                "workers": len(stats),
                "worker_stats": stats,
            }
        else:
            return {
                "status": "unhealthy",
                "error": "No workers available",
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
        }
```

---

## Summary

### Key Takeaways

1. **BackgroundTasks**: Use for simple, request-scoped operations
2. **Celery**: Use for distributed, long-running, scheduled tasks
3. **Task Definition**: Define tasks with proper options and error handling
4. **Workers**: Configure workers for optimal performance
5. **Beat**: Use Celery Beat for periodic tasks
6. **Result Backends**: Configure appropriate result backend
7. **Retries**: Implement retry logic with exponential backoff
8. **Monitoring**: Use Flower and Prometheus for observability
9. **FastAPI Integration**: Integrate Celery with FastAPI endpoints
10. **Production**: Configure for production workloads

### Resources

- [FastAPI Background Tasks Documentation](https://fastapi.tiangolo.com/tutorial/background-tasks/)
- [Celery Documentation](https://docs.celeryq.dev/)
- [Celery Best Practices](https://docs.celeryq.dev/en/stable/userguide/tasks.html#best-practices)
- [Flower Monitoring](https://flower.readthedocs.io/)

---

**Version**: v1.0.0  
**Last Updated**: 2025-01-14

