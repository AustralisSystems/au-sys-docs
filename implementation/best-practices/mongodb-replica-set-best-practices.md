# MongoDB Replica Set Best Practices for Production

## Overview

This document outlines the MongoDB replica set configuration implemented for high availability in staging and production environments.

## Architecture

### Replica Set Configuration
- **3-node replica set** (minimum recommended for production)
- **1 Primary node** (mongodb-replica-0) with priority 2
- **2 Secondary nodes** (mongodb-replica-1, mongodb-replica-2) with priority 1
- **Automatic failover** with election time ~10-30 seconds
- **Data replication** ensures all writes are replicated to secondaries

### High Availability Features

1. **Automatic Failover**: If the primary node fails, one of the secondaries is automatically promoted to primary
2. **Data Durability**: All writes are replicated to at least one secondary before being acknowledged (write concern: MAJORITY)
3. **Read Scaling**: Can distribute read operations across secondaries for better performance
4. **Zero-Downtime Maintenance**: Can perform maintenance on secondary nodes without affecting primary operations

## Connection String Format

### For PyMongo Applications

```python
# Replica Set Connection String
connection_string = (
    "mongodb://admin:password@"
    "mongodb-replica-0:27017,"
    "mongodb-replica-1:27017,"
    "mongodb-replica-2:27017/"
    "orchestrator"
    "?replicaSet=rs0"
    "&authSource=admin"
    "&readPreference=primaryPreferred"
    "&w=majority"
)
```

### Connection String Components

- **Hosts**: All 3 replica set members (PyMongo will discover others automatically)
- **replicaSet=rs0**: Replica set name (must match configuration)
- **authSource=admin**: Authentication database
- **readPreference**:
  - `primary` (default): Read only from primary
  - `primaryPreferred`: Read from primary, fallback to secondary
  - `secondaryPreferred`: Read from secondary, fallback to primary (for read scaling)
- **w=majority**: Write concern - wait for majority of nodes to acknowledge write

## Best Practices Implemented

### 1. Minimum 3 Nodes
- Provides redundancy and automatic failover
- Can survive 1 node failure without data loss
- Ensures majority quorum for elections

### 2. Priority Configuration
- Primary node has higher priority (2) to ensure it's elected first
- Secondary nodes have equal priority (1) for balanced failover

### 3. Health Checks
- Health checks configured for all nodes
- 10-second interval for fast failure detection
- 5 retries before marking unhealthy

### 4. Resource Allocation
- **Staging**: 1GB RAM per node (3GB total)
- **Production**: 2GB RAM per node (6GB total)
- CPU limits configured per environment

### 5. Security
- Authentication enabled on all nodes
- Admin user configured via environment variables
- Replica set name configured (rs0)

### 6. Data Durability
- Journal enabled for crash recovery
- Write concern set to MAJORITY for durability
- Automatic replication to secondaries

### 7. Monitoring
- Health checks configured
- Logging configured with rotation
- Prometheus metrics available

## Application Integration

### Updating Application Connection Strings

The application should use a connection string that includes all replica set members:

```python
# Example: Update src/services/storage/config.py
mongodb_url = (
    f"mongodb://{username}:{password}@"
    f"mongodb-replica-0:27017,"
    f"mongodb-replica-1:27017,"
    f"mongodb-replica-2:27017/"
    f"{database_name}"
    f"?replicaSet=rs0"
    f"&authSource=admin"
)
```

### PyMongo Client Configuration

```python
from pymongo import MongoClient

client = MongoClient(
    connection_string,
    serverSelectionTimeoutMS=5000,
    maxPoolSize=50,
    minPoolSize=10,
    read_preference="primaryPreferred",  # Read from primary, fallback to secondary
    w="majority",  # Write concern: wait for majority
    wtimeout=5000,  # Write timeout: 5 seconds
)
```

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

Check replica set status:
```bash
docker exec -it <mongodb-replica-0-container> mongosh --eval "rs.status()"
```

Expected output should show:
- 1 PRIMARY node
- 2 SECONDARY nodes
- All nodes healthy

## Monitoring

### Key Metrics to Monitor

1. **Replication Lag**: Time difference between primary and secondary writes
2. **Election Count**: Number of times a new primary was elected
3. **Connection Count**: Number of active connections per node
4. **Oplog Size**: Size of the operation log (affects replication window)

### Health Check Endpoints

- Health checks configured in Docker Compose
- Prometheus metrics available at `/metrics` endpoint
- MongoDB native monitoring via `db.serverStatus()`

## Backup and Recovery

### Backup Strategy

1. **Regular Backups**: Use `mongodump` on secondary nodes (doesn't impact primary)
2. **Point-in-Time Recovery**: Use oplog for point-in-time recovery
3. **Replica Set Snapshots**: Take snapshots of secondary nodes

### Recovery Procedures

1. **Single Node Failure**: Automatic failover, replace failed node
2. **Multiple Node Failure**: Restore from backup, reinitialize replica set
3. **Data Corruption**: Restore from backup, resync replica set

## Troubleshooting

### Common Issues

1. **Replica Set Not Initializing**
   - Check all nodes are healthy
   - Verify network connectivity between nodes
   - Check replica set name matches

2. **Primary Not Electing**
   - Ensure majority of nodes are available
   - Check priority configuration
   - Verify network partitions

3. **Replication Lag**
   - Check network latency
   - Monitor oplog size
   - Verify secondary node resources

### Useful Commands

```bash
# Check replica set status
mongosh --eval "rs.status()"

# Check replica set configuration
mongosh --eval "rs.conf()"

# Force reconfiguration (use with caution)
mongosh --eval "rs.reconfig(config)"

# Check replication lag
mongosh --eval "rs.printSlaveReplicationInfo()"
```

## References

- [MongoDB Replica Set Documentation](https://www.mongodb.com/docs/manual/replication/)
- [PyMongo Connection String Format](https://www.mongodb.com/docs/manual/reference/connection-string/)
- [MongoDB High Availability Best Practices](https://www.mongodb.com/docs/manual/administration/production-notes/)
