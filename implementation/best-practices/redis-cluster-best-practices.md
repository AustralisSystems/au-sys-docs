# Redis Cluster Best Practices for Production

## Overview

This document outlines the Redis cluster configuration implemented for high availability and optimal performance in staging and production environments.

## Architecture

### Cluster Configuration
- **6-node cluster** (minimum recommended for production)
- **3 master nodes** (redis-cluster-0, redis-cluster-1, redis-cluster-2)
- **3 replica nodes** (redis-cluster-3, redis-cluster-4, redis-cluster-5)
- **Automatic failover** with election time ~5-10 seconds
- **Data replication** ensures all writes are replicated to replicas
- **Hash slot distribution** across 3 masters (16384 slots total, ~5461 slots per master)

### High Availability Features

1. **Automatic Failover**: If a master node fails, one of its replicas is automatically promoted to master
2. **Data Durability**: All writes are replicated to replicas before acknowledgment
3. **Horizontal Scaling**: Can add/remove nodes without downtime
4. **Zero-Downtime Maintenance**: Can perform maintenance on nodes without affecting cluster operations

## Cluster Topology

### Node Distribution

```
Master Nodes:
- redis-cluster-0: Hash slots 0-5460
- redis-cluster-1: Hash slots 5461-10922
- redis-cluster-2: Hash slots 10923-16383

Replica Nodes:
- redis-cluster-3: Replica of redis-cluster-0
- redis-cluster-4: Replica of redis-cluster-1
- redis-cluster-5: Replica of redis-cluster-2
```

### Port Configuration

- **Data Port**: `6379` (client connections)
- **Cluster Bus Port**: `16379` (node-to-node communication)
- **External Ports**: `6450-6455:6379` (staging/prod)

## High Availability Best Practices

### 1. Minimum Cluster Size

**Current Configuration**: ✅ 6 nodes (3 masters + 3 replicas)

**Best Practice**:
- Minimum 6 nodes for production (3 masters + 3 replicas)
- Can survive 1 master + 1 replica failure simultaneously
- Ensures majority quorum for cluster operations

**Scaling Guidelines**:
- Add nodes in pairs (1 master + 1 replica)
- Maintain odd number of masters for quorum
- Maximum recommended: 1000 nodes per cluster

### 2. Replication Factor

**Current Configuration**: ✅ 1 replica per master

**Best Practice**:
- **Production**: Minimum 1 replica per master
- **High Availability**: 2 replicas per master for critical workloads
- **Cost Optimization**: 1 replica per master for standard workloads

**Failover Capability**:
- With 1 replica: Can survive 1 master failure
- With 2 replicas: Can survive 1 master + 1 replica failure

### 3. Cluster Node Timeout

**Current Configuration**: `cluster-node-timeout=5000` (5 seconds)

**Best Practice**:
- **Production**: 5000-15000ms (5-15 seconds)
- **Low Latency**: 3000-5000ms (3-5 seconds)
- **High Latency Networks**: 15000-30000ms (15-30 seconds)

**Impact**:
- Lower timeout = faster failover but more false positives
- Higher timeout = slower failover but fewer false positives

### 4. Cluster Announce Configuration

**Current Configuration**: ✅ Properly configured
```yaml
cluster-announce-ip: redis-cluster-{0-5}
cluster-announce-port: 6379
cluster-announce-bus-port: 16379
```

**Best Practice**:
- Always configure `cluster-announce-ip` in containerized environments
- Use service names (not IPs) for dynamic environments
- Ensure bus port is accessible for cluster communication

## Performance Optimization

### 1. Memory Management

**Current Configuration**:
```yaml
maxmemory: 512mb (staging) / 1gb (production)
maxmemory-policy: allkeys-lru
```

**Best Practices**:
- Set `maxmemory` to 80-90% of available RAM
- Use appropriate eviction policy:
  - `allkeys-lru`: Best for caching (current)
  - `volatile-lru`: Only evict keys with TTL
  - `allkeys-lfu`: Least frequently used
  - `noeviction`: No eviction (use with caution)

**Memory Monitoring**:
```bash
# Check memory usage
redis-cli -h redis-cluster-0 INFO memory

# Check specific key memory
redis-cli -h redis-cluster-0 MEMORY USAGE key_name
```

### 2. Persistence Configuration

**Current Configuration**: ✅ AOF enabled
```yaml
appendonly: yes
appendfsync: everysec
```

**Best Practices**:
- **AOF (Append Only File)**: Recommended for durability
- **RDB Snapshots**: Use for backups, not primary persistence
- **appendfsync everysec**: Balance between performance and durability
- **appendfsync always**: Maximum durability (slower)

**Persistence Strategy**:
```yaml
# Production (current)
appendonly: yes
appendfsync: everysec
save: "900 1 300 10 60 10000"  # RDB snapshots for backups

# High Durability
appendonly: yes
appendfsync: always  # Slower but maximum durability
```

### 3. Connection Pooling

**Application Configuration**:
```python
# From RedisClusterManager
max_connections: 50
max_connections_per_node: 10
connection_timeout: 30
socket_timeout: 30
```

**Best Practices**:
- **Connection Pool Size**: 50-100 connections per application instance
- **Per-Node Connections**: 10-20 connections per node
- **Connection Timeout**: 30 seconds for production
- **Socket Keepalive**: Enable to detect dead connections

**Python (redis-py) Configuration**:
```python
from redis.cluster import RedisCluster

cluster = RedisCluster(
    startup_nodes=[
        {"host": "redis-cluster-0", "port": 6379},
        {"host": "redis-cluster-1", "port": 6379},
        {"host": "redis-cluster-2", "port": 6379},
    ],
    max_connections=50,
    max_connections_per_node=10,
    socket_timeout=30,
    socket_connect_timeout=30,
    socket_keepalive=True,
    retry_on_cluster_down=True,
    cluster_down_retry_attempts=3,
    reinitialize_steps=10,
)
```

### 4. Key Design and Hash Tags

**Best Practice**: Use hash tags for multi-key operations

**Hash Tag Syntax**: `{tag}key_name`

**Examples**:
```python
# Good: Keys hash to same slot
user:{1234}:profile
user:{1234}:settings
user:{1234}:preferences

# Bad: Keys hash to different slots
user:1234:profile
user:1234:settings
user:1234:preferences
```

**Multi-Key Operations**:
```python
# Works: All keys in same hash slot
cluster.mget("user:{1234}:profile", "user:{1234}:settings")

# Fails: Keys in different hash slots
cluster.mget("user:1234:profile", "user:5678:settings")
```

**Key Naming Conventions**:
- Use namespaces: `app:module:key`
- Use hash tags for related keys: `{namespace}:key`
- Avoid hot keys (keys with high access frequency)
- Distribute keys evenly across hash slots

### 5. Pipelining and Batching

**Best Practice**: Use pipelining for multiple commands

```python
# Good: Pipeline multiple commands
pipe = cluster.pipeline()
pipe.set("key1", "value1")
pipe.set("key2", "value2")
pipe.set("key3", "value3")
results = pipe.execute()

# Bad: Multiple round trips
cluster.set("key1", "value1")
cluster.set("key2", "value2")
cluster.set("key3", "value3")
```

**Batch Operations**:
```python
# Batch SET operations
def batch_set(cluster, key_values):
    pipe = cluster.pipeline()
    for key, value in key_values.items():
        pipe.set(key, value)
    return pipe.execute()

# Batch GET operations (same hash slot)
def batch_get(cluster, keys):
    if all_keys_same_slot(keys):
        return cluster.mget(keys)
    else:
        # Fallback to individual gets
        return [cluster.get(k) for k in keys]
```

### 6. Avoiding Hot Keys

**Problem**: Hot keys cause uneven load distribution

**Detection**:
```bash
# Find hot keys
redis-cli --hotkeys

# Monitor key access patterns
redis-cli --latency-history
```

**Solutions**:
- **Key Sharding**: Split hot keys across multiple keys
  ```python
  # Instead of: user:1234:data
  # Use: user:1234:data:shard0, user:1234:data:shard1
  ```
- **Local Caching**: Cache hot keys in application memory
- **Read Replicas**: Distribute reads across replicas
- **Key Expiration**: Use TTL to limit key lifetime

## Application Integration

### Connection String Format

**For redis-py (Python)**:
```python
from redis.cluster import RedisCluster

startup_nodes = [
    {"host": "redis-cluster-0", "port": 6379},
    {"host": "redis-cluster-1", "port": 6379},
    {"host": "redis-cluster-2", "port": 6379},
]

cluster = RedisCluster(
    startup_nodes=startup_nodes,
    decode_responses=True,
    password="your_password",  # If authentication enabled
    ssl=True,  # If SSL enabled
)
```

**Environment Variables**:
```bash
REDIS_CLUSTER_ENABLED=true
REDIS_CLUSTER_NODES=redis-cluster-0:6379,redis-cluster-1:6379,redis-cluster-2:6379,redis-cluster-3:6379,redis-cluster-4:6379,redis-cluster-5:6379
```

### Client Configuration

**Current Implementation**: ✅ RedisClusterManager

**Features**:
- Automatic node discovery
- Connection pooling
- Health monitoring
- Circuit breaker pattern
- Automatic failover
- Load balancing

**Configuration Example**:
```python
config = {
    "startup_nodes": [
        {"host": "redis-cluster-0", "port": 6379},
        {"host": "redis-cluster-1", "port": 6379},
        {"host": "redis-cluster-2", "port": 6379},
    ],
    "max_connections": 50,
    "max_connections_per_node": 10,
    "connection_timeout": 30,
    "socket_timeout": 30,
    "health_check_interval": 30,
    "retry_on_cluster_down": True,
    "cluster_down_retry_attempts": 3,
}
```

### Error Handling

**Best Practices**:
```python
from redis.exceptions import (
    ClusterDownError,
    ConnectionError,
    TimeoutError,
    ResponseError,
)

try:
    result = cluster.get("key")
except ClusterDownError:
    # Cluster is down, wait and retry
    time.sleep(1)
    result = cluster.get("key")
except ConnectionError:
    # Connection failed, reconnect
    cluster = reconnect_cluster()
    result = cluster.get("key")
except TimeoutError:
    # Operation timed out, retry with backoff
    result = retry_with_backoff(cluster.get, "key")
```

## Security Best Practices

### 1. Authentication

**Current Configuration**: Not enabled (development)

**Production Recommendation**:
```yaml
# Enable authentication
requirepass: ${REDIS_PASSWORD}

# Use ACLs for fine-grained access control
aclfile: /etc/redis/users.acl
```

**ACL Configuration**:
```
# Create user with specific permissions
ACL SETUSER appuser on >password +@read +@write ~app:*

# Disable dangerous commands
ACL SETUSER appuser -@dangerous
```

### 2. Network Security

**Best Practices**:
- Use private networks for cluster communication
- Enable TLS/SSL for client connections
- Use firewall rules to restrict access
- Bind to specific interfaces (not 0.0.0.0 in production)

**TLS Configuration**:
```yaml
# Redis server
tls-port: 6380
tls-cert-file: /etc/redis/redis.crt
tls-key-file: /etc/redis/redis.key
tls-ca-cert-file: /etc/redis/ca.crt
```

**Client TLS Configuration**:
```python
import ssl

cluster = RedisCluster(
    startup_nodes=startup_nodes,
    ssl=True,
    ssl_cert_reqs=ssl.CERT_REQUIRED,
    ssl_ca_certs="/path/to/ca.crt",
    ssl_certfile="/path/to/client.crt",
    ssl_keyfile="/path/to/client.key",
)
```

### 3. Command Filtering

**Disable Dangerous Commands**:
```yaml
# redis.conf
rename-command FLUSHDB ""
rename-command FLUSHALL ""
rename-command CONFIG "CONFIG_9a7b8c5d3e2f1a0"
rename-command DEBUG ""
```

## Monitoring and Observability

### 1. Cluster Health Monitoring

**Key Metrics**:
- Cluster state (ok, fail, down)
- Node status (master, replica, fail)
- Hash slot coverage
- Replication lag
- Memory usage per node
- Connection count per node
- Command latency

**Health Check Commands**:
```bash
# Cluster info
redis-cli -h redis-cluster-0 CLUSTER INFO

# Node status
redis-cli -h redis-cluster-0 CLUSTER NODES

# Check hash slot coverage
redis-cli -h redis-cluster-0 CLUSTER SLOTS

# Memory usage
redis-cli -h redis-cluster-0 INFO memory

# Replication info
redis-cli -h redis-cluster-0 INFO replication
```

### 2. Prometheus Metrics

**Integration**:
```python
from prometheus_client import Counter, Histogram, Gauge

redis_commands_total = Counter(
    'redis_commands_total',
    'Total Redis commands',
    ['command', 'node', 'status']
)

redis_command_duration = Histogram(
    'redis_command_duration_seconds',
    'Redis command duration',
    ['command', 'node']
)

redis_cluster_nodes = Gauge(
    'redis_cluster_nodes',
    'Number of nodes in cluster',
    ['state']
)
```

### 3. Logging

**Structured Logging**:
```python
import structlog

logger = structlog.get_logger()

logger.info(
    "redis_cluster_operation",
    operation="get",
    key="user:1234",
    node="redis-cluster-0",
    duration_ms=5.2,
    status="success"
)
```

## Resource Allocation

### Staging Environment

```yaml
redis-cluster-node:
  resources:
    limits:
      cpus: "0.5"
      memory: 512M
    reservations:
      cpus: "0.25"
      memory: 256M
```

### Production Environment

```yaml
redis-cluster-node:
  resources:
    limits:
      cpus: "1"
      memory: 1G
    reservations:
      cpus: "0.5"
      memory: 512M
```

**Scaling Guidelines**:
- Start with 512MB-1GB per node
- Monitor memory usage (should stay below 80%)
- Scale horizontally by adding nodes
- Scale vertically by increasing memory limits

## Deployment

### Staging Environment
```bash
docker compose -f docker-compose.base.yml -f docker-compose.staging.yml up -d
```

### Production Environment
```bash
docker compose -f docker-compose.base.yml -f docker-compose.prod.yml up -d
```

### Verification

**Check Cluster Status**:
```bash
# Cluster info
docker exec -it <redis-cluster-0-container> redis-cli CLUSTER INFO

# Node status
docker exec -it <redis-cluster-0-container> redis-cli CLUSTER NODES

# Test connection
docker exec -it <redis-cluster-0-container> redis-cli PING
```

**Expected Output**:
- `cluster_state:ok` - Cluster is healthy
- All nodes show `connected` status
- Hash slots evenly distributed (5461 slots per master)
- Replicas show `master` relationship

## Maintenance Operations

### 1. Adding Nodes

**Add Master Node**:
```bash
# Add new master node
redis-cli --cluster add-node \
  redis-cluster-6:6379 \
  redis-cluster-0:6379

# Reshard slots to new node
redis-cli --cluster reshard \
  redis-cluster-0:6379 \
  --cluster-from <node-id-1>,<node-id-2> \
  --cluster-to <new-node-id> \
  --cluster-slots 1638
```

**Add Replica Node**:
```bash
# Add replica node
redis-cli --cluster add-node \
  redis-cluster-6:6379 \
  redis-cluster-0:6379 \
  --cluster-slave \
  --cluster-master-id <master-node-id>
```

### 2. Removing Nodes

**Remove Replica Node**:
```bash
# Simply remove replica (no data migration needed)
redis-cli --cluster del-node \
  redis-cluster-0:6379 \
  <replica-node-id>
```

**Remove Master Node**:
```bash
# Reshard slots away from master first
redis-cli --cluster reshard \
  redis-cluster-0:6379 \
  --cluster-from <master-node-id> \
  --cluster-to <target-node-id> \
  --cluster-slots <slot-count>

# Then remove master
redis-cli --cluster del-node \
  redis-cluster-0:6379 \
  <master-node-id>
```

### 3. Rebalancing Cluster

**Rebalance Hash Slots**:
```bash
# Automatic rebalancing
redis-cli --cluster rebalance \
  redis-cluster-0:6379 \
  --cluster-weight <node-id-1>=1 <node-id-2>=1 <node-id-3>=1
```

### 4. Failover Testing

**Manual Failover**:
```bash
# Test failover on replica
redis-cli -h redis-cluster-3 CLUSTER FAILOVER

# Force failover (even if master is healthy)
redis-cli -h redis-cluster-3 CLUSTER FAILOVER FORCE
```

## Troubleshooting

### Common Issues

1. **Cluster State: fail**
   - **Cause**: Not enough nodes available for quorum
   - **Solution**: Ensure majority of masters are available

2. **MOVED Redirections**
   - **Cause**: Key moved to different node
   - **Solution**: Client should automatically follow redirects (redis-py handles this)

3. **ASK Redirections**
   - **Cause**: Key is being migrated
   - **Solution**: Client should follow ASK redirects (redis-py handles this)

4. **Replication Lag**
   - **Cause**: Network issues or high write load
   - **Solution**: Check network latency, reduce write load, increase replica resources

5. **Memory Pressure**
   - **Cause**: High memory usage, eviction policy not working
   - **Solution**: Increase maxmemory, adjust eviction policy, optimize key sizes

### Useful Commands

```bash
# Check cluster state
redis-cli CLUSTER INFO

# List all nodes
redis-cli CLUSTER NODES

# Check hash slot distribution
redis-cli CLUSTER SLOTS

# Check key location
redis-cli CLUSTER KEYSLOT key_name

# Get node for key
redis-cli CLUSTER GETKEYSINSLOT <slot> <count>

# Check replication lag
redis-cli INFO replication

# Monitor commands
redis-cli MONITOR

# Check slow commands
redis-cli SLOWLOG GET 10
```

## Performance Tuning Checklist

- [ ] Configure appropriate `maxmemory` (80-90% of RAM)
- [ ] Set appropriate eviction policy (`allkeys-lru` for caching)
- [ ] Enable AOF persistence (`appendonly yes`)
- [ ] Configure `cluster-node-timeout` (5000-15000ms)
- [ ] Use hash tags for multi-key operations
- [ ] Implement connection pooling (50-100 connections)
- [ ] Use pipelining for batch operations
- [ ] Monitor and avoid hot keys
- [ ] Enable health checks (10s interval)
- [ ] Configure proper resource limits
- [ ] Set up monitoring and alerting
- [ ] Enable authentication in production
- [ ] Configure TLS/SSL for client connections
- [ ] Disable dangerous commands
- [ ] Plan for horizontal scaling
- [ ] Test failover scenarios regularly

## Recommended Production Configuration

```yaml
# docker-compose.prod.yml
redis-cluster-node:
  image: redis:7-alpine
  command: >
    redis-server
    --cluster-enabled yes
    --cluster-config-file nodes.conf
    --cluster-node-timeout 5000
    --cluster-announce-ip ${NODE_NAME}
    --cluster-announce-port 6379
    --cluster-announce-bus-port 16379
    --appendonly yes
    --appendfsync everysec
    --maxmemory 1gb
    --maxmemory-policy allkeys-lru
    --requirepass ${REDIS_PASSWORD}
    --tls-port 6380
    --tls-cert-file /etc/redis/redis.crt
    --tls-key-file /etc/redis/redis.key
    --tls-ca-cert-file /etc/redis/ca.crt
  resources:
    limits:
      cpus: "1"
      memory: 1G
  healthcheck:
    test: ["CMD", "redis-cli", "--tls", "ping"]
    interval: 10s
    timeout: 3s
    retries: 5
```

## References

- [Redis Cluster Specification](https://redis.io/docs/reference/cluster-spec/)
- [Redis Cluster Tutorial](https://redis.io/docs/manual/scaling/)
- [redis-py Cluster Documentation](https://redis-py.readthedocs.io/en/stable/commands.html#cluster-commands)
- [Redis Best Practices](https://redis.io/docs/manual/patterns/)
- [Redis Performance Optimization](https://redis.io/docs/manual/optimization/)
