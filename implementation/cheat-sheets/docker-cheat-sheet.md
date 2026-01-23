# Docker Cheat Sheet Template

**Version**: v1.0.0
**Date**: 2025-12-24

## 📌 Configuration Variables

Replace these placeholders with your project-specific values:

- `{{CONTAINER_NAME}}` - Your container name (e.g., `my-app`, `web-server`)
- `{{IMAGE_NAME}}` - Your Docker image name (e.g., `my-app:latest`, `web:1.0.0`)
- `{{SERVICE_NAME}}` - Your docker-compose service name (e.g., `app`, `web`)
- `{{PORT}}` - Your application port (e.g., `8000`, `3000`, `8080`)
- `{{DOCKERFILE}}` - Your Dockerfile name (e.g., `Dockerfile`, `Dockerfile.prod`)

**Example**: If your container is `my-app`, image is `my-app:v1.0`, service is `app`, and port is `3000`, replace:

- `{{CONTAINER_NAME}}` → `my-app`
- `{{IMAGE_NAME}}` → `my-app:v1.0`
- `{{SERVICE_NAME}}` → `app`
- `{{PORT}}` → `3000`

---

## 🏗️ BUILD COMMANDS

### Build Docker Image

```bash
# Build image from Dockerfile in current directory (uses cache)
docker build -t {{IMAGE_NAME}} .

# Build with no cache (clean build - ignores all cache)
docker build --no-cache -t {{IMAGE_NAME}} .

# Build with cache (explicit - uses cache layers)
docker build --cache-from {{IMAGE_NAME}} -t {{IMAGE_NAME}} .

# Build with pull (always pull base images, but use cache for layers)
docker build --pull -t {{IMAGE_NAME}} .

# Build with specific Dockerfile
docker build -f {{DOCKERFILE}} -t {{IMAGE_NAME}} .

# Build with build arguments
docker build --build-arg KEY=value -t {{IMAGE_NAME}} .

# Build with progress output
docker build --progress=plain -t {{IMAGE_NAME}} .

# Build with cache from multiple sources
docker build --cache-from {{IMAGE_NAME}}:latest --cache-from {{IMAGE_NAME}}:previous -t {{IMAGE_NAME}} .
```

### Build with Docker Compose

```bash
# Build all services (uses cache)
docker-compose build

# Build specific service (uses cache)
docker-compose build {{SERVICE_NAME}}

# Build with no cache (clean build - ignores all cache)
docker-compose build --no-cache {{SERVICE_NAME}}

# Build with no cache for all services
docker-compose build --no-cache

# Build and start services (uses cache)
docker-compose up --build

# Build and start services with no cache
docker-compose up --build --no-cache

# Build with pull (always pull base images, but use cache for layers)
docker-compose build --pull {{SERVICE_NAME}}

# Build and start services, remove orphaned containers
docker-compose up --build --remove-orphans
```

---

## 🔍 CHECK/INSPECT COMMANDS

### Container Status

```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# List containers with format
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}"

# Show container resource usage
docker stats {{CONTAINER_NAME}}

# Show container resource usage (one-time)
docker stats --no-stream {{CONTAINER_NAME}}
```

### Container Information

```bash
# Inspect container details
docker inspect {{CONTAINER_NAME}}

# Inspect specific property
docker inspect -f '{{.State.Status}}' {{CONTAINER_NAME}}

# Show container logs size
docker inspect -f '{{.HostConfig.LogConfig}}' {{CONTAINER_NAME}}

# Show container environment variables
docker inspect -f '{{range .Config.Env}}{{println .}}{{end}}' {{CONTAINER_NAME}}

# Show container network settings
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' {{CONTAINER_NAME}}
```

### Container Health

```bash
# Check container health status
docker inspect --format='{{.State.Health.Status}}' {{CONTAINER_NAME}}

# Show container health check logs
docker inspect --format='{{json .State.Health}}' {{CONTAINER_NAME}} | jq
```

### Image Information

```bash
# List images
docker images

# Inspect image
docker inspect {{IMAGE_NAME}}

# Show image history
docker history {{IMAGE_NAME}}

# Show image size
docker images {{IMAGE_NAME}}
```

### Process Information

```bash
# Show processes running in container
docker top {{CONTAINER_NAME}}

# Show container resource usage
docker stats {{CONTAINER_NAME}}
```

---

## 📋 LOGS COMMANDS

### View Logs (One-Time)

```bash
# View all logs
docker logs {{CONTAINER_NAME}}

# View logs with timestamps
docker logs --timestamps {{CONTAINER_NAME}}

# View last N lines
docker logs --tail 100 {{CONTAINER_NAME}}

# View logs since specific time
docker logs --since 5m {{CONTAINER_NAME}}
docker logs --since 1h {{CONTAINER_NAME}}
docker logs --since 2025-12-24T10:00:00 {{CONTAINER_NAME}}

# View logs until specific time
docker logs --until 5m {{CONTAINER_NAME}}
```

### Follow Logs (Real-Time)

```bash
# Follow logs (watch in real-time)
docker logs -f {{CONTAINER_NAME}}

# Follow logs with timestamps
docker logs -f --timestamps {{CONTAINER_NAME}}

# Follow logs with tail limit
docker logs -f --tail 100 {{CONTAINER_NAME}}

# Follow logs with all options (RECOMMENDED)
docker logs -f --timestamps --tail 200 {{CONTAINER_NAME}}
```

### Logs with Filters

```bash
# Follow logs and grep for specific text
docker logs -f {{CONTAINER_NAME}} | grep ERROR

# Follow logs and grep case-insensitive
docker logs -f {{CONTAINER_NAME}} | grep -i error

# Follow logs and highlight matches
docker logs -f {{CONTAINER_NAME}} | grep --color=always ERROR

# Follow logs and show context around matches
docker logs -f {{CONTAINER_NAME}} | grep -A 5 -B 5 ERROR
```

---

## 🚀 RUN/START/STOP COMMANDS

### Run Container

```bash
# Run container
docker run {{IMAGE_NAME}}

# Run container with port mapping
docker run -p {{PORT}}:{{PORT}} {{IMAGE_NAME}}

# Run container in detached mode
docker run -d --name {{CONTAINER_NAME}} {{IMAGE_NAME}}

# Run container with environment variables
docker run -e KEY=value {{IMAGE_NAME}}

# Run container with volume mount
docker run -v $(pwd):/app {{IMAGE_NAME}}
```

### Start/Stop Container

```bash
# Start container
docker start {{CONTAINER_NAME}}

# Stop container
docker stop {{CONTAINER_NAME}}

# Restart container
docker restart {{CONTAINER_NAME}}

# Stop container gracefully (with timeout)
docker stop -t 30 {{CONTAINER_NAME}}
```

### Docker Compose

```bash
# Start services
docker-compose up

# Start services in detached mode
docker-compose up -d

# Start specific service
docker-compose up {{SERVICE_NAME}}

# Start services and remove orphaned containers
docker-compose up --remove-orphans

# Start services in detached mode and remove orphaned containers
docker-compose up -d --remove-orphans

# Stop services
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop and remove containers with volumes
docker-compose down -v

# Stop and remove containers, remove orphaned containers
docker-compose down --remove-orphans

# Stop and remove containers with volumes, remove orphaned containers
docker-compose down -v --remove-orphans
```

---

## 🧹 CLEANUP COMMANDS

### Remove Containers

```bash
# Remove stopped container
docker rm {{CONTAINER_NAME}}

# Remove container forcefully
docker rm -f {{CONTAINER_NAME}}

# Remove all stopped containers
docker container prune

# Remove all containers
docker rm $(docker ps -aq)
```

### Remove Images

```bash
# Remove image
docker rmi {{IMAGE_NAME}}

# Remove image forcefully
docker rmi -f {{IMAGE_NAME}}

# Remove unused images
docker image prune

# Remove all unused images
docker image prune -a
```

### Cleanup All

```bash
# Remove all unused containers, networks, images
docker system prune

# Remove all unused containers, networks, images, volumes
docker system prune -a --volumes
```

---

## 🔧 DEBUGGING COMMANDS

### Execute Commands in Container

```bash
# Execute command in running container
docker exec {{CONTAINER_NAME}} ls -la

# Execute interactive shell
docker exec -it {{CONTAINER_NAME}} /bin/bash
docker exec -it {{CONTAINER_NAME}} /bin/sh

# Execute command as specific user
docker exec -u root {{CONTAINER_NAME}} whoami

# Execute command in detached mode
docker exec -d {{CONTAINER_NAME}} command
```

### Copy Files

```bash
# Copy file from container to host
docker cp {{CONTAINER_NAME}}:/app/file.txt ./file.txt

# Copy file from host to container
docker cp ./file.txt {{CONTAINER_NAME}}:/app/file.txt

# Copy directory from container to host
docker cp {{CONTAINER_NAME}}:/app/logs ./logs
```

### Network Commands

```bash
# List networks
docker network ls

# Inspect network
docker network inspect bridge

# Show container network connections
docker network inspect bridge | grep {{CONTAINER_NAME}}
```

---

## 📊 MONITORING COMMANDS

### Resource Usage

```bash
# Show container stats (continuous)
docker stats {{CONTAINER_NAME}}

# Show container stats (one-time)
docker stats --no-stream {{CONTAINER_NAME}}

# Show stats for all containers
docker stats

# Show stats with specific format
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

### Events

```bash
# Show container events
docker events

# Show events for specific container
docker events --filter container={{CONTAINER_NAME}}

# Show events since specific time
docker events --since 5m
```

---

## 🐳 DOCKER COMPOSE SPECIFIC

### Logs

```bash
# Follow logs for all services
docker-compose logs -f

# Follow logs for specific service
docker-compose logs -f {{SERVICE_NAME}}

# Follow logs with timestamps
docker-compose logs -f --timestamps {{SERVICE_NAME}}

# Follow logs with tail limit
docker-compose logs -f --tail 100 {{SERVICE_NAME}}

# Follow logs since specific time
docker-compose logs --since 5m {{SERVICE_NAME}}
```

### Status

```bash
# Show service status
docker-compose ps

# Show service status with format
docker-compose ps --format json
```

### Execute Commands

```bash
# Execute command in service container
docker-compose exec {{SERVICE_NAME}} ls -la

# Execute interactive shell
docker-compose exec {{SERVICE_NAME}} /bin/bash
```

---

## 🎯 QUICK REFERENCE

### Most Common Commands

```bash
# Build image (with cache)
docker build -t {{IMAGE_NAME}} .

# Build image (no cache - clean build)
docker build --no-cache -t {{IMAGE_NAME}} .

# Run container
docker run -d --name {{CONTAINER_NAME}} -p {{PORT}}:{{PORT}} {{IMAGE_NAME}}

# View logs (follow)
docker logs -f --timestamps --tail 200 {{CONTAINER_NAME}}

# Check status
docker ps

# Stop container
docker stop {{CONTAINER_NAME}}

# Remove container
docker rm {{CONTAINER_NAME}}

# Docker Compose: Start
docker-compose up -d

# Docker Compose: Start with remove orphans
docker-compose up -d --remove-orphans

# Docker Compose: Build and start (with cache)
docker-compose up --build -d

# Docker Compose: Build and start (no cache)
docker-compose up --build --no-cache -d

# Docker Compose: Logs
docker-compose logs -f {{SERVICE_NAME}}

# Docker Compose: Stop
docker-compose down

# Docker Compose: Stop and remove orphans
docker-compose down --remove-orphans
```

### Recommended Debugging Command

```bash
# Follow logs with timestamps and tail (best for debugging)
docker logs -f --timestamps --tail 200 {{CONTAINER_NAME}}
```

---

## 📝 USAGE INSTRUCTIONS

1. **Copy this template** to your project directory
2. **Replace all placeholders** with your project-specific values:
   - `{{CONTAINER_NAME}}` → Your container name
   - `{{IMAGE_NAME}}` → Your Docker image name
   - `{{SERVICE_NAME}}` → Your docker-compose service name
   - `{{PORT}}` → Your application port
   - `{{DOCKERFILE}}` → Your Dockerfile name (if different from `Dockerfile`)

3. **Use find-and-replace** in your editor:
   - Find: `{{CONTAINER_NAME}}` → Replace: `my-app`
   - Find: `{{IMAGE_NAME}}` → Replace: `my-app:latest`
   - Find: `{{SERVICE_NAME}}` → Replace: `app`
   - Find: `{{PORT}}` → Replace: `8000`
   - Find: `{{DOCKERFILE}}` → Replace: `Dockerfile`

### Example Project Values

**For a Node.js app:**

- `{{CONTAINER_NAME}}` → `node-app`
- `{{IMAGE_NAME}}` → `node-app:latest`
- `{{SERVICE_NAME}}` → `app`
- `{{PORT}}` → `3000`

**For a Python FastAPI app:**

- `{{CONTAINER_NAME}}` → `api-server`
- `{{IMAGE_NAME}}` → `api-server:v1.0`
- `{{SERVICE_NAME}}` → `api`
- `{{PORT}}` → `8000`

---

**Last Updated**: 2025-12-24
