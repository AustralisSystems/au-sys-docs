# Celery Tasks Best Practices for Production

## Overview

This document provides comprehensive best practices for designing, implementing, and managing Celery tasks in production environments, specifically tailored to this application's architecture. It covers task design patterns, error handling, retry strategies, idempotency, performance optimization, monitoring, and production deployment considerations.

## Architecture

### Current Implementation

- **Celery App Factory**: Centralized Celery application factory
- **Task Registry**: Task registration and discovery system
- **Redis Broker**: Redis cluster for message broker and result backend
- **Task Routing**: Queue-based routing (sync, data, workflow, monitoring, high_priority)
- **Retry Logic**: Configurable retry with exponential backoff
- **Monitoring**: Flower integration for task monitoring
- **Production Config**: Optimized settings for production workloads

## Task Design Principles

### 1. Single Responsibility Principle

**RECOMMENDED**: Each task should perform a single, well-defined operation

**Good Example**:
```python
@celery_app.task(name="auth.rotate_encryption_key", bind=True, max_retries=3)
async def rotate_encryption_key_task(
    self,
    new_master_key: bytes,
    old_key_version: int,
    new_key_version: int,
    storage_provider_config: Dict[str, Any],
) -> Dict[str, Any]:
    """Rotate encryption keys and re-encrypt credentials."""
    # Task focuses solely on key rotation
    ...
```

**Bad Example**:
```python
@celery_app.task(name="auth.do_everything", bind=True)
async def do_everything_task(self, ...):
    """This task does too many things."""
    # Rotate keys
    # Send emails
    # Update database
    # Generate reports
    # Process payments
    # ... too many responsibilities
```

**Best Practices**:
- ✅ One task = one operation
- ✅ Extract business logic to service classes
- ✅ Keep tasks thin (wrappers around service methods)
- ✅ Make tasks testable in isolation

### 2. Idempotency

**REQUIRED**: Tasks must be idempotent (safe to retry)

**Good Example**:
```python
@celery_app.task(name="discovery.scan_platform", bind=True, max_retries=3)
def scan_platform_task(self, target: str, platform_type: Optional[str] = None):
    """Idempotent platform scan task."""
    # Check if scan already exists
    existing_scan = get_scan_by_target(target)
    if existing_scan and existing_scan.status == "completed":
        return {"status": "already_completed", "scan_id": existing_scan.id}

    # Perform scan
    scan = perform_scan(target, platform_type)
    return {"status": "completed", "scan_id": scan.id}
```

**Bad Example**:
```python
@celery_app.task(name="data.process_payment", bind=True)
def process_payment_task(self, user_id: int, amount: float):
    """Non-idempotent payment processing."""
    # This will charge the user multiple times if retried!
    charge_user(user_id, amount)
    create_transaction(user_id, amount)
```

**Idempotency Strategies**:
- Use unique identifiers (UUIDs) for operations
- Check for existing results before processing
- Use database transactions with unique constraints
- Implement idempotency keys/tokens
- Use conditional updates (e.g., `update_one` with conditions)

### 3. Avoid Passing ORM Objects

**REQUIRED**: Pass identifiers, not objects

**Good Example**:
```python
@celery_app.task(name="commands.execute_batch", bind=True)
def execute_batch_commands_task(
    self: Task,
    commands: List[Dict[str, Any]],  # Serializable data
    execute_parallel: bool = True
) -> Dict[str, Any]:
    """Execute batch commands."""
    # Commands are dictionaries, not ORM objects
    ...
```

**Bad Example**:
```python
@celery_app.task(name="users.process_user", bind=True)
def process_user_task(self, user: User):  # ORM object - BAD!
    """Process user."""
    # ORM objects don't serialize well
    # May become stale
    # Causes serialization errors
    ...
```

**Best Practices**:
- ✅ Pass primitive types (str, int, float, bool)
- ✅ Pass dictionaries/lists of primitives
- ✅ Pass identifiers and fetch objects in task
- ✅ Use Pydantic models for complex data
- ❌ Never pass ORM objects directly
- ❌ Avoid passing file handles or connections

### 4. Task Naming Conventions

**RECOMMENDED**: Use hierarchical namespace pattern

**Current Pattern**:
```python
# Good: Hierarchical namespace
"auth.rotate_encryption_key"
"auth.check_api_key_expiration"
"discovery.scan_platform"
"commands.execute_batch"

# Format: <module>.<operation>
```

**Best Practices**:
- Use dot notation for namespaces (`module.operation`)
- Use snake_case for operation names
- Keep names descriptive and consistent
- Group related tasks under same namespace
- Avoid abbreviations unless widely understood

## Error Handling and Retry Strategies

### 1. Retry Configuration

**Current Configuration**:
```python
@celery_app.task(
    name="discovery.scan_platform",
    bind=True,
    max_retries=3,
    default_retry_delay=60
)
def scan_platform_task(self, ...):
    ...
```

**Best Practices**:
```python
from celery.exceptions import Retry, MaxRetriesExceededError

@celery_app.task(
    name="task.example",
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(ConnectionError, TimeoutError),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True
)
def example_task(self, ...):
    """Task with comprehensive retry configuration."""
    try:
        # Task logic
        result = perform_operation()
        return result
    except ConnectionError as exc:
        # Automatic retry for ConnectionError
        raise self.retry(exc=exc, countdown=60 * (self.request.retries + 1))
    except ValueError as exc:
        # Don't retry for ValueError (permanent error)
        logger.error(f"Permanent error: {exc}")
        return {"status": "failed", "error": str(exc)}
    except Exception as exc:
        # Retry for other transient errors
        if self.request.retries < self.max_retries:
            raise self.retry(exc=exc, countdown=60 * (self.request.retries + 1))
        else:
            # Max retries exceeded
            logger.error(f"Max retries exceeded: {exc}")
            return {"status": "failed", "error": str(exc)}
```

### 2. Exponential Backoff

**RECOMMENDED**: Use exponential backoff for retries

**Implementation**:
```python
@celery_app.task(name="task.with_backoff", bind=True, max_retries=5)
def task_with_backoff(self, ...):
    """Task with exponential backoff."""
    try:
        result = perform_operation()
        return result
    except TransientError as exc:
        # Exponential backoff: 60s, 120s, 240s, 480s, 960s
        countdown = 60 * (2 ** self.request.retries)
        raise self.retry(exc=exc, countdown=countdown)
```

**Backoff Strategies**:
- **Exponential**: `countdown = base * (2 ** retries)`
- **Linear**: `countdown = base * (retries + 1)`
- **Fixed**: `countdown = base`
- **Jitter**: Add randomness to prevent thundering herd

### 3. Error Classification

**REQUIRED**: Classify errors as transient vs permanent

**Transient Errors** (should retry):
- `ConnectionError`, `TimeoutError`
- `TemporaryFailure`, `ServiceUnavailable`
- Database connection errors
- Network errors
- Rate limiting (with backoff)

**Permanent Errors** (don't retry):
- `ValueError`, `TypeError`
- `AuthenticationError`, `PermissionDenied`
- `ValidationError`
- Business logic errors
- Invalid input data

**Implementation**:
```python
from celery.exceptions import Retry

TRANSIENT_ERRORS = (ConnectionError, TimeoutError, ServiceUnavailable)
PERMANENT_ERRORS = (ValueError, TypeError, AuthenticationError)

@celery_app.task(name="task.classified_errors", bind=True, max_retries=3)
def task_with_classified_errors(self, ...):
    """Task with error classification."""
    try:
        result = perform_operation()
        return result
    except TRANSIENT_ERRORS as exc:
        # Retry transient errors
        raise self.retry(exc=exc, countdown=60)
    except PERMANENT_ERRORS as exc:
        # Don't retry permanent errors
        logger.error(f"Permanent error: {exc}")
        return {"status": "failed", "error": str(exc)}
    except Exception as exc:
        # Unknown error - retry once
        if self.request.retries < 1:
            raise self.retry(exc=exc, countdown=60)
        else:
            return {"status": "failed", "error": str(exc)}
```

### 4. Task State Updates

**RECOMMENDED**: Update task state for long-running tasks

**Current Implementation**:
```python
@celery_app.task(name="discovery.scan_platform", bind=True, max_retries=3)
def scan_platform_task(self, target: str, ...):
    """Task with state updates."""
    # Update state at start
    self.update_state(
        state=ScanStatus.RUNNING.value,
        meta={"progress": 0, "message": "Starting scan"}
    )

    # Update state during processing
    self.update_state(
        state=ScanStatus.RUNNING.value,
        meta={"progress": 50, "message": "Scanning platform"}
    )

    # Update state on completion
    self.update_state(
        state=ScanStatus.COMPLETED.value,
        meta={"progress": 100, "message": "Scan completed"}
    )
```

**Best Practices**:
- Update state at key milestones
- Include progress percentage (0-100)
- Include descriptive messages
- Include relevant metadata (counts, IDs, etc.)
- Update state on errors

## Task Patterns

### 1. Batch Processing Pattern

**RECOMMENDED**: Process items in batches for efficiency

**Current Implementation**:
```python
@celery_app.task(name="auth.rotate_encryption_key", bind=True, max_retries=3)
async def rotate_encryption_key_task(self, ...):
    """Batch processing example."""
    batch_size = 50

    # Process credentials in batches
    for i in range(0, len(credentials), batch_size):
        batch = credentials[i:i + batch_size]
        batch_num = (i // batch_size) + 1

        # Process batch
        for credential in batch:
            await rotate_credential(credential)

        # Update progress
        progress = int((i + batch_size) / len(credentials) * 100)
        self.update_state(
            state="PROGRESS",
            meta={"progress": progress, "batch": batch_num}
        )
```

**Best Practices**:
- Use appropriate batch sizes (50-100 items)
- Update progress after each batch
- Handle batch failures gracefully
- Consider parallel batch processing
- Monitor batch processing time

### 2. Chunking Pattern

**RECOMMENDED**: Break large tasks into smaller chunks

**Implementation**:
```python
from celery import group

@celery_app.task(name="data.process_chunk", bind=True)
def process_chunk_task(self, chunk: List[Dict[str, Any]]):
    """Process a single chunk."""
    results = []
    for item in chunk:
        result = process_item(item)
        results.append(result)
    return results

@celery_app.task(name="data.process_large_dataset", bind=True)
def process_large_dataset_task(self, dataset: List[Dict[str, Any]]):
    """Process large dataset by chunking."""
    chunk_size = 100
    chunks = [dataset[i:i + chunk_size] for i in range(0, len(dataset), chunk_size)]

    # Process chunks in parallel
    job = group(
        process_chunk_task.s(chunk) for chunk in chunks
    )
    result = job.apply_async()

    return {"task_ids": [task.id for task in result.children]}
```

**Best Practices**:
- Chunk size: 50-500 items (depending on processing time)
- Process chunks in parallel when possible
- Track chunk processing progress
- Handle partial failures gracefully
- Aggregate chunk results

### 3. Chain Pattern

**RECOMMENDED**: Execute tasks sequentially

**Implementation**:
```python
from celery import chain

@celery_app.task(name="workflow.step1", bind=True)
def step1_task(self, data: Dict[str, Any]):
    """First step in workflow."""
    result = process_step1(data)
    return {"step1_result": result, "data": data}

@celery_app.task(name="workflow.step2", bind=True)
def step2_task(self, step1_result: Dict[str, Any]):
    """Second step in workflow."""
    result = process_step2(step1_result["step1_result"])
    return {"step2_result": result, **step1_result}

# Execute chain
workflow = chain(
    step1_task.s(data),
    step2_task.s()
)
result = workflow.apply_async()
```

**Best Practices**:
- Use chains for sequential dependencies
- Pass results between steps
- Handle failures at each step
- Consider rollback for failed chains
- Monitor chain progress

### 4. Group Pattern

**RECOMMENDED**: Execute tasks in parallel

**Implementation**:
```python
from celery import group

@celery_app.task(name="data.process_item", bind=True)
def process_item_task(self, item: Dict[str, Any]):
    """Process single item."""
    return process_item(item)

# Execute group
items = [{"id": 1}, {"id": 2}, {"id": 3}]
job = group(
    process_item_task.s(item) for item in items
)
result = job.apply_async()

# Wait for results
results = result.get()
```

**Best Practices**:
- Use groups for independent parallel tasks
- Monitor group progress
- Handle partial failures
- Consider group size limits
- Use callback for group completion

### 5. Chord Pattern

**RECOMMENDED**: Execute tasks in parallel, then callback

**Implementation**:
```python
from celery import chord

@celery_app.task(name="data.process_item", bind=True)
def process_item_task(self, item: Dict[str, Any]):
    """Process single item."""
    return process_item(item)

@celery_app.task(name="data.aggregate_results", bind=True)
def aggregate_results_task(self, results: List[Dict[str, Any]]):
    """Aggregate results from parallel tasks."""
    return aggregate(results)

# Execute chord
items = [{"id": 1}, {"id": 2}, {"id": 3}]
workflow = chord(
    (process_item_task.s(item) for item in items),
    aggregate_results_task.s()
)
result = workflow.apply_async()
```

**Best Practices**:
- Use chords for map-reduce patterns
- Ensure callback handles all results
- Handle callback failures
- Monitor chord progress
- Consider timeout for callback

## Task Timeouts

### 1. Soft Time Limit

**RECOMMENDED**: Set soft time limit for graceful shutdown

**Current Configuration**:
```python
task_soft_time_limit=3600  # 1 hour soft limit
```

**Implementation**:
```python
from celery.exceptions import SoftTimeLimitExceeded

@celery_app.task(
    name="task.with_timeout",
    bind=True,
    soft_time_limit=300,  # 5 minutes
    time_limit=600  # 10 minutes hard limit
)
def task_with_timeout(self, ...):
    """Task with timeout handling."""
    try:
        result = long_running_operation()
        return result
    except SoftTimeLimitExceeded:
        # Cleanup and save progress
        save_progress()
        logger.warning("Task exceeded soft time limit")
        raise self.retry(countdown=60)
```

**Best Practices**:
- Set soft limit to 80-90% of expected time
- Handle `SoftTimeLimitExceeded` gracefully
- Save progress before raising exception
- Retry with longer timeout if needed
- Log timeout events

### 2. Hard Time Limit

**REQUIRED**: Set hard time limit to prevent runaway tasks

**Current Configuration**:
```python
task_time_limit=3900  # 65 minutes hard limit
```

**Best Practices**:
- Set hard limit to soft limit + buffer (10-20%)
- Hard limit kills task immediately
- No cleanup possible on hard limit
- Use for safety, not normal operation
- Monitor hard limit kills

## Task Routing and Queues

### 1. Queue Configuration

**Current Configuration**:
```python
task_routes={
    "sync.*": {"queue": "sync_queue"},
    "data.*": {"queue": "data_queue"},
    "workflow.*": {"queue": "workflow_queue"},
    "monitoring.*": {"queue": "monitoring_queue"},
    "high_priority.*": {"queue": "high_priority_queue"},
}
```

**Best Practices**:
- Route by task type/priority
- Use descriptive queue names
- Separate queues by resource requirements
- Use priority queues for urgent tasks
- Monitor queue depths

### 2. Task Priority

**RECOMMENDED**: Use priority queues for urgent tasks

**Implementation**:
```python
@celery_app.task(
    name="high_priority.process_urgent",
    bind=True,
    queue="high_priority_queue"
)
def process_urgent_task(self, ...):
    """High priority task."""
    ...

@celery_app.task(
    name="data.process_normal",
    bind=True,
    queue="data_queue"
)
def process_normal_task(self, ...):
    """Normal priority task."""
    ...
```

**Best Practices**:
- Use priority queues sparingly
- Reserve high priority for critical operations
- Monitor priority queue usage
- Avoid priority inversion
- Document priority decisions

## Performance Optimization

### 1. Worker Concurrency

**Current Configuration**:
```python
worker_prefetch_multiplier=1  # Disable prefetching for fair distribution
```

**Best Practices**:
- Set concurrency based on task types
- CPU-bound tasks: `concurrency = CPU cores`
- I/O-bound tasks: `concurrency = CPU cores * 2-4`
- Monitor worker utilization
- Adjust based on workload

**Configuration**:
```bash
# CPU-bound tasks
celery -A app worker --concurrency=4

# I/O-bound tasks
celery -A app worker --concurrency=16

# Mixed workload
celery -A app worker --concurrency=8
```

### 2. Prefetch Multiplier

**Current Configuration**: `prefetch_multiplier=1`

**Best Practices**:
- `prefetch_multiplier=1`: Fair distribution, no prefetching
- `prefetch_multiplier=4`: Prefetch 4 tasks per worker
- Higher values: Better throughput, less fair distribution
- Lower values: More fair, lower throughput
- Use 1 for long-running tasks
- Use 4-8 for short-running tasks

### 3. Task Serialization

**Current Configuration**:
```python
task_serializer="pickle"  # Use pickle for complex objects
accept_content=["pickle", "json"]
```

**Best Practices**:
- **JSON**: Simple, safe, human-readable (default)
- **Pickle**: Complex objects, faster, security concerns
- **MessagePack**: Binary, faster than JSON, smaller
- Use JSON when possible
- Use Pickle only for complex objects
- Validate serialized data

### 4. Result Backend Optimization

**Current Configuration**: Redis cluster

**Best Practices**:
- Use Redis for fast result retrieval
- Set appropriate result expiration
- Don't store large results
- Use `ignore_result=True` when results not needed
- Monitor result backend usage

**Configuration**:
```python
@celery_app.task(
    name="task.no_result",
    bind=True,
    ignore_result=True  # Don't store result
)
def task_no_result(self, ...):
    """Task that doesn't need result storage."""
    ...
```

## Monitoring and Observability

### 1. Task Logging

**RECOMMENDED**: Comprehensive logging for tasks

**Current Implementation**:
```python
import logging

logger = logging.getLogger(__name__)

@celery_app.task(name="task.with_logging", bind=True)
def task_with_logging(self, ...):
    """Task with comprehensive logging."""
    logger.info(f"Task started: {self.request.id}")

    try:
        result = perform_operation()
        logger.info(f"Task completed: {self.request.id}")
        return result
    except Exception as e:
        logger.error(f"Task failed: {self.request.id}, error: {e}", exc_info=True)
        raise
```

**Best Practices**:
- Log task start/completion
- Log errors with full traceback
- Include task ID in logs
- Use structured logging
- Log performance metrics

### 2. Task Metrics

**RECOMMENDED**: Track task metrics

**Metrics to Track**:
- Task execution time
- Task success/failure rate
- Task queue depth
- Worker utilization
- Retry rate
- Timeout rate

**Implementation**:
```python
from prometheus_client import Counter, Histogram, Gauge

task_executions = Counter(
    'celery_task_executions_total',
    'Total task executions',
    ['task_name', 'status']
)

task_duration = Histogram(
    'celery_task_duration_seconds',
    'Task execution duration',
    ['task_name']
)

task_queue_depth = Gauge(
    'celery_task_queue_depth',
    'Task queue depth',
    ['queue_name']
)

@celery_app.task(name="task.with_metrics", bind=True)
def task_with_metrics(self, ...):
    """Task with metrics tracking."""
    start_time = time.time()

    try:
        result = perform_operation()
        task_executions.labels(task_name=self.name, status='success').inc()
        return result
    except Exception as e:
        task_executions.labels(task_name=self.name, status='failure').inc()
        raise
    finally:
        duration = time.time() - start_time
        task_duration.labels(task_name=self.name).observe(duration)
```

### 3. Flower Integration

**Current Implementation**: ✅ Flower configured

**Best Practices**:
- Monitor task execution in real-time
- Track worker status
- View task history
- Monitor queue depths
- Set up alerts for failures

## Security Best Practices

### 1. Input Validation

**REQUIRED**: Validate all task inputs

**Implementation**:
```python
from pydantic import BaseModel, ValidationError

class TaskInput(BaseModel):
    user_id: int
    data: Dict[str, Any]

@celery_app.task(name="task.with_validation", bind=True)
def task_with_validation(self, input_data: Dict[str, Any]):
    """Task with input validation."""
    try:
        validated_input = TaskInput(**input_data)
    except ValidationError as e:
        logger.error(f"Invalid input: {e}")
        return {"status": "failed", "error": "Invalid input"}

    # Process validated input
    ...
```

**Best Practices**:
- Validate all inputs
- Use Pydantic models for validation
- Reject invalid inputs immediately
- Log validation errors
- Don't retry on validation errors

### 2. Access Control

**REQUIRED**: Restrict task execution

**Best Practices**:
- Validate user permissions
- Check resource access
- Use task-level authentication
- Audit task execution
- Monitor unauthorized access attempts

### 3. Sensitive Data Handling

**REQUIRED**: Handle sensitive data securely

**Best Practices**:
- Don't log sensitive data
- Encrypt sensitive data in transit
- Use secure storage for credentials
- Rotate encryption keys regularly
- Audit sensitive data access

## Production Deployment Checklist

- [ ] All tasks are idempotent
- [ ] Tasks use appropriate retry strategies
- [ ] Error handling is comprehensive
- [ ] Task timeouts are configured
- [ ] Tasks update state for long operations
- [ ] Tasks use appropriate queues
- [ ] Worker concurrency is optimized
- [ ] Prefetch multiplier is configured
- [ ] Task serialization is appropriate
- [ ] Result backend is optimized
- [ ] Task logging is comprehensive
- [ ] Task metrics are tracked
- [ ] Flower monitoring is configured
- [ ] Input validation is implemented
- [ ] Access control is enforced
- [ ] Sensitive data is handled securely
- [ ] Task naming follows conventions
- [ ] Tasks don't pass ORM objects
- [ ] Tasks are testable
- [ ] Documentation is up-to-date

## Common Anti-Patterns to Avoid

### 1. Long-Running Tasks Without Progress Updates

**Problem**: No visibility into task progress

**Solution**: Update task state regularly

```python
# Good
@celery_app.task(name="task.with_progress", bind=True)
def task_with_progress(self, items: List[Any]):
    total = len(items)
    for i, item in enumerate(items):
        process_item(item)
        self.update_state(
            state="PROGRESS",
            meta={"progress": int((i + 1) / total * 100)}
        )
```

### 2. Retrying Permanent Errors

**Problem**: Wasting resources on permanent errors

**Solution**: Classify errors correctly

```python
# Good
try:
    result = perform_operation()
except ValueError as exc:  # Permanent error
    logger.error(f"Permanent error: {exc}")
    return {"status": "failed", "error": str(exc)}
except ConnectionError as exc:  # Transient error
    raise self.retry(exc=exc)
```

### 3. Passing Large Objects

**Problem**: Serialization overhead and memory usage

**Solution**: Pass identifiers and fetch objects

```python
# Good
@celery_app.task(name="users.process_user", bind=True)
def process_user_task(self, user_id: int):
    user = get_user_by_id(user_id)
    process_user(user)
```

### 4. No Error Handling

**Problem**: Tasks fail silently

**Solution**: Comprehensive error handling

```python
# Good
@celery_app.task(name="task.with_errors", bind=True, max_retries=3)
def task_with_errors(self, ...):
    try:
        result = perform_operation()
        return result
    except TransientError as exc:
        raise self.retry(exc=exc)
    except PermanentError as exc:
        logger.error(f"Permanent error: {exc}")
        return {"status": "failed", "error": str(exc)}
    except Exception as exc:
        logger.error(f"Unexpected error: {exc}", exc_info=True)
        raise
```

### 5. Blocking Operations

**Problem**: Blocking worker threads

**Solution**: Use async operations

```python
# Good
@celery_app.task(name="task.async_operation", bind=True)
async def async_task(self, ...):
    result = await async_operation()
    return result
```

## Recommended Production Configuration

```python
# celery_app_factory.py
app.conf.update(
    # Task execution
    task_always_eager=False,
    task_eager_propagates=True,
    task_ignore_result=False,
    task_store_eager_result=True,
    task_track_started=True,
    task_reject_on_worker_lost=True,
    task_acks_late=True,

    # Serialization
    task_serializer="pickle",
    accept_content=["pickle", "json"],
    result_serializer="json",

    # Timeouts
    task_soft_time_limit=3600,  # 1 hour
    task_time_limit=3900,  # 65 minutes

    # Retry settings
    task_retry_delay=60,
    task_max_retries=3,
    task_default_retry_delay=60,

    # Routing
    task_routes={
        "sync.*": {"queue": "sync_queue"},
        "data.*": {"queue": "data_queue"},
        "workflow.*": {"queue": "workflow_queue"},
        "monitoring.*": {"queue": "monitoring_queue"},
        "high_priority.*": {"queue": "high_priority_queue"},
    },

    # Worker settings
    worker_prefetch_multiplier=1,
    worker_disable_rate_limits=False,
    worker_enable_remote_control=True,
    worker_send_task_events=True,

    # Result backend
    result_backend="redis://redis-cluster:6379/0",
    result_expires=3600,  # 1 hour
)
```

## References

- [Celery Best Practices](https://docs.celeryproject.org/en/stable/userguide/tasks.html#best-practices)
- [Celery Task Patterns](https://docs.celeryproject.org/en/stable/userguide/tasks.html#task-patterns)
- [Background Tasks & Celery Best Practices](./background-tasks-celery-best-practices-2025.md)
- [Celery Production Best Practices](./celery-production-best-practices.md)
