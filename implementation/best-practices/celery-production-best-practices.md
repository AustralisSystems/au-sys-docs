# Celery Production Best Practices for High Availability and Performance

## Overview

This document outlines best practices for deploying Celery in production with high availability and optimal performance, specifically tailored to this application's architecture.

## Current Architecture

### Infrastructure Components
- **Broker**: Redis Cluster (6 nodes: 3 masters + 3 replicas)
- **Result Backend**: Redis Cluster (same cluster, different DB)
- **Workers**: Docker containers with configurable replicas
- **Monitoring**: Flower (Celery monitoring tool)
- **Task Queues**: Multiple priority queues (high_priority, data, sync, workflow, monitoring, celery)

## High Availability Best Practices

### 1. Worker Replication

**Current State**: 1 replica per environment (staging/prod)

**Recommendation**: Deploy multiple worker replicas for redundancy

```yaml
# docker-compose.staging.yml / docker-compose.prod.yml
celery-worker:
  deploy:
    replicas: 3  # Minimum 3 workers for HA
    resources:
      limits:
        cpus: "2"
        memory: 2G
```

**Benefits**:
- Survives worker failures without service interruption
- Distributes load across multiple workers
- Enables zero-downtime deployments (rolling updates)

### 2. Redis Cluster Integration

**Current State**: Using Redis cluster for broker and result backend

**Best Practices**:
- ✅ Use Redis cluster for high availability
- ✅ Configure connection retries and heartbeat
- ✅ Use separate Redis DBs for broker (DB 1) and results (DB 2)

**Configuration**:
```python
# Already implemented in celery_app_factory.py
broker_connection_retry_on_startup=True
broker_connection_retry=True
broker_connection_max_retries=10
broker_heartbeat=30
```

### 3. Task Acknowledgment Strategy

**Current Configuration**: `task_acks_late=True`

**Best Practice**: ✅ Already configured correctly
- Tasks are acknowledged after completion, not when received
- Prevents task loss if worker crashes during execution
- Tasks are redelivered to other workers if worker fails

### 4. Graceful Shutdown

**Implementation**:
```python
# Add to worker startup script
import signal
import sys

def signal_handler(sig, frame):
    print('Shutting down gracefully...')
    # Allow current tasks to complete
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)
```

**Docker Configuration**:
```yaml
stop_grace_period: 60s  # Allow 60 seconds for graceful shutdown
```

## Performance Optimization

### 1. Worker Concurrency

**Current State**: Not explicitly configured (defaults to CPU count)

**Recommendation**: Configure based on task type

```yaml
# For CPU-bound tasks
command: celery worker --concurrency=4 --pool=prefork

# For I/O-bound tasks
command: celery worker --concurrency=50 --pool=gevent

# For mixed workloads (recommended)
command: celery worker --concurrency=8 --pool=prefork --autoscale=10,2
```

**Guidelines**:
- **CPU-bound tasks**: `concurrency = CPU cores`
- **I/O-bound tasks**: `concurrency = CPU cores * 4-8`
- **Mixed workloads**: Use autoscaling with min=2, max=CPU cores * 2

### 2. Prefetch Multiplier

**Current Configuration**: `worker_prefetch_multiplier=1` ✅

**Best Practice**: ✅ Already configured correctly
- Prevents workers from hoarding tasks
- Ensures fair distribution across workers
- Critical for high availability

### 3. Task Routing and Queue Prioritization

**Current State**: ✅ Multiple queues with priorities configured

**Queues**:
1. `high_priority_queue` (priority: 10)
2. `sync_queue` (priority: 7)
3. `workflow_queue` (priority: 6)
4. `data_queue` (priority: 5)
5. `monitoring_queue` (priority: 3)
6. `celery` (default, priority: 1)

**Best Practices**:
- ✅ Separate critical tasks from batch jobs
- ✅ Use dedicated workers for high-priority queues
- ✅ Scale workers per queue based on load

**Worker Configuration per Queue**:
```yaml
# High-priority worker (dedicated)
celery-worker-high-priority:
  command: celery worker -Q high_priority_queue --concurrency=4
  deploy:
    replicas: 2

# Data processing worker
celery-worker-data:
  command: celery worker -Q data_queue --concurrency=8
  deploy:
    replicas: 3

# Default worker
celery-worker-default:
  command: celery worker -Q celery,monitoring_queue --concurrency=4
  deploy:
    replicas: 2
```

### 4. Task Serialization

**Current Configuration**: `task_serializer="pickle"`

**Recommendation**: Use JSON for security, pickle only when necessary

```python
# For most tasks (secure)
task_serializer="json"
accept_content=["json"]

# For complex objects (use with caution)
task_serializer="pickle"
accept_content=["pickle", "json"]
```

**Performance Impact**:
- JSON: Faster serialization, smaller messages, more secure
- Pickle: Slower, larger messages, security concerns

### 5. Result Backend Optimization

**Current Configuration**: ✅ Already optimized
- Result expiration: 7 days
- Result compression: gzip
- Result persistence: enabled

**Additional Optimizations**:
```python
# Disable results for fire-and-forget tasks
@app.task(ignore_result=True)
def fire_and_forget_task():
    pass

# Use result_expires for temporary results
@app.task(result_expires=3600)  # 1 hour
def temporary_task():
    pass
```

### 6. Worker Pool Selection

**Pool Types**:
- **prefork** (default): Best for CPU-bound tasks
- **gevent**: Best for I/O-bound tasks (async)
- **eventlet**: Alternative to gevent
- **threads**: For I/O-bound tasks (simpler than gevent)

**Recommendation**:
```python
# CPU-bound tasks
worker_pool = "prefork"
worker_concurrency = CPU_CORES

# I/O-bound tasks
worker_pool = "gevent"
worker_concurrency = CPU_CORES * 4

# Mixed workloads
worker_pool = "prefork"
worker_autoscale = f"{CPU_CORES * 2},{CPU_CORES}"
```

## Resource Allocation

### Staging Environment

```yaml
celery-worker:
  deploy:
    replicas: 2
    resources:
      limits:
        cpus: "1"
        memory: 1G
      reservations:
        cpus: "0.5"
        memory: 512M
```

### Production Environment

```yaml
celery-worker:
  deploy:
    replicas: 3  # Minimum for HA
    resources:
      limits:
        cpus: "2"
        memory: 2G
      reservations:
        cpus: "1"
        memory: 1G
```

**Scaling Guidelines**:
- Start with 3 replicas minimum
- Scale horizontally based on queue length
- Monitor CPU and memory usage
- Scale up when queue length > 100 tasks

## Monitoring and Observability

### 1. Flower Configuration

**Current State**: ✅ Flower configured

**Best Practices**:
- Enable authentication in production
- Monitor worker stats, task rates, queue lengths
- Set up alerts for worker failures

**Production Configuration**:
```yaml
celery-flower:
  environment:
    - FLOWER_BASIC_AUTH=admin:secure_password
    - FLOWER_URL_PREFIX=/flower
  ports:
    - "127.0.0.1:5555:5555"  # Bind to localhost only
```

### 2. Prometheus Metrics

**Integration**:
```python
# Enable Celery Prometheus exporter
from prometheus_client import Counter, Histogram

task_counter = Counter('celery_tasks_total', 'Total tasks', ['status'])
task_duration = Histogram('celery_task_duration_seconds', 'Task duration')
```

### 3. Health Checks

**Current State**: ✅ Health checks configured

**Enhancement**:
```python
# Custom health check endpoint
@app.route('/health/celery')
def celery_health():
    inspect = celery.control.inspect()
    stats = inspect.stats()
    active = inspect.active()

    return {
        'workers': len(stats or {}),
        'active_tasks': sum(len(tasks) for tasks in (active or {}).values()),
        'healthy': len(stats or {}) > 0
    }
```

## Error Handling and Resilience

### 1. Retry Configuration

**Current Configuration**: ✅ Already configured
```python
task_max_retries=3
task_default_retry_delay=60
```

**Best Practice**: Exponential backoff
```python
@app.task(bind=True, max_retries=3)
def task_with_retry(self, arg):
    try:
        # Task logic
        pass
    except Exception as exc:
        # Exponential backoff: 60s, 120s, 240s
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))
```

### 2. Dead Letter Queue

**Configuration**:
```python
# Configure dead letter queue
task_reject_on_worker_lost=True
task_acks_late=True

# Custom dead letter handler
@app.task(queue='dead_letter')
def handle_dead_letter(task_id, reason):
    logger.error(f"Task {task_id} failed: {reason}")
    # Store in database for manual review
```

### 3. Circuit Breaker Pattern

**Implementation**:
```python
from celery.exceptions import Retry

class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure_time = None

    def call(self, func, *args, **kwargs):
        if self.is_open():
            raise Exception("Circuit breaker is open")

        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise
```

## Deployment Recommendations

### 1. Rolling Updates

**Docker Swarm Configuration**:
```yaml
deploy:
  update_config:
    parallelism: 1
    delay: 10s
    order: start-first
    failure_action: rollback
```

**Benefits**:
- Zero-downtime deployments
- Automatic rollback on failure
- Gradual worker replacement

### 2. Worker Startup Sequence

**Current Script**: ✅ `celery_startup_purge.sh`

**Enhancement**:
```bash
#!/bin/bash
# Wait for Redis cluster to be ready
until redis-cli -h redis-cluster-0 ping; do
  echo "Waiting for Redis..."
  sleep 2
done

# Wait for MongoDB replica set
until mongosh --host mongodb-replica-0:27017 --eval "rs.status()" > /dev/null; do
  echo "Waiting for MongoDB..."
  sleep 2
done

# Start worker
exec celery worker "$@"
```

### 3. Environment-Specific Configuration

**Staging**:
- Lower concurrency (test performance)
- More verbose logging
- Shorter result expiration

**Production**:
- Optimized concurrency
- Structured logging
- Longer result expiration
- Enhanced monitoring

## Performance Tuning Checklist

- [ ] Configure worker concurrency based on task type
- [ ] Use autoscaling for variable workloads
- [ ] Separate high-priority tasks into dedicated queues
- [ ] Deploy multiple worker replicas (minimum 3)
- [ ] Monitor queue lengths and worker utilization
- [ ] Optimize task serialization (JSON vs pickle)
- [ ] Configure result expiration appropriately
- [ ] Enable task compression for large results
- [ ] Use prefetch_multiplier=1 for fair distribution
- [ ] Implement exponential backoff for retries
- [ ] Set up dead letter queue handling
- [ ] Configure graceful shutdown (60s grace period)
- [ ] Enable Flower monitoring with authentication
- [ ] Integrate Prometheus metrics
- [ ] Set up alerts for worker failures

## Recommended Production Configuration

```yaml
# docker-compose.prod.yml
celery-worker:
  command: >
    celery worker
    -A src.services.celery_service.celery_app_factory
    --loglevel=info
    --concurrency=8
    --pool=prefork
    --autoscale=10,2
    --max-tasks-per-child=1000
    --time-limit=3600
    --soft-time-limit=3300
    -Q high_priority_queue,data_queue,sync_queue,workflow_queue,monitoring_queue,celery
  deploy:
    replicas: 3
    resources:
      limits:
        cpus: "2"
        memory: 2G
      reservations:
        cpus: "1"
        memory: 1G
    update_config:
      parallelism: 1
      delay: 10s
      order: start-first
  stop_grace_period: 60s
```

## References

- [Celery Best Practices](https://docs.celeryq.dev/en/stable/userguide/optimizing.html)
- [Celery Production Guide](https://docs.celeryq.dev/en/stable/userguide/deploying.html)
- [Redis Cluster Best Practices](https://redis.io/docs/manual/scaling/)
- [Flower Monitoring](https://flower.readthedocs.io/)
