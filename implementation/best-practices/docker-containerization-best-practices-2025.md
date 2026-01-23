# Docker & Containerization Best Practices

**Version**: v1.0.0
**Last Updated**: 2025-01-14

This document provides comprehensive best practices for Docker containerization in FastAPI applications, covering Dockerfile optimization, multi-stage builds, security hardening, docker-compose orchestration, image optimization, health checks, resource management, and production deployment.

**Key Principle**: All configuration, secrets, URLs, and DNS settings must come from `.env` files as the single source of truth, enabling dynamic deployment across multiple environments (development, staging, production) without modifying Docker Compose files.

---

## Table of Contents

1. [Architecture Principles](#architecture-principles)
2. [Dockerfile Best Practices](#dockerfile-best-practices)
3. [Multi-Stage Builds](#multi-stage-builds)
4. [Security Best Practices](#security-best-practices)
5. [Image Optimization](#image-optimization)
6. [Docker Compose Orchestration](#docker-compose-orchestration)
7. [Health Checks](#health-checks)
8. [Resource Management](#resource-management)
9. [Networking](#networking)
10. [Volume Management](#volume-management)
11. [Environment Configuration](#environment-configuration)
12. [Production Deployment](#production-deployment)
13. [CI/CD Integration](#cicd-integration)
14. [Monitoring and Logging](#monitoring-and-logging)

---

## Architecture Principles

### Container Philosophy

**REQUIRED**: Follow container best practices:

1. **Single Responsibility**: Each container should run a single process
2. **Stateless**: Containers should be stateless and ephemeral
3. **Immutable**: Containers should be immutable (no runtime modifications)
4. **Minimal**: Use minimal base images to reduce attack surface
5. **Reproducible**: Builds should be reproducible and deterministic

### Image Layers

**REQUIRED**: Optimize layer caching:

- Order instructions from least to most frequently changing
- Copy dependency files before source code
- Combine related RUN commands to reduce layers
- Use `.dockerignore` to exclude unnecessary files

---

## Dockerfile Best Practices

### Base Image Selection

**REQUIRED**: Use official, minimal base images:

```dockerfile
# GOOD: Use official slim/alpine images
FROM python:3.11-slim

# BETTER: Pin to specific version
FROM python:3.11-slim@sha256:abc123...

# BEST: Use Alpine for minimal size
FROM python:3.11-alpine
```

### Environment Variables

**REQUIRED**: Set Python environment variables:

```dockerfile
# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Set Python path
ENV PYTHONPATH=/app

# Disable pip cache
ENV PIP_NO_CACHE_DIR=1

# Disable pip version check
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
```

### Working Directory

**REQUIRED**: Set working directory early:

```dockerfile
WORKDIR /app
```

### Dependency Installation

**REQUIRED**: Optimize dependency installation and prefer prebuilt wheels:

```dockerfile
# Copy dependency files first (leverages Docker cache)
COPY requirements.lock.txt pyproject.toml ./

# Use BuildKit cache for pip to speed wheel builds/downloads
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip install -r requirements.lock.txt
```

### Wheelhouse & BuildKit wheel caching (recommended)

Use a builder stage to produce a wheelhouse and install in the runtime stage from local wheels. This avoids repeated resolver work in CI and local builds and makes installs deterministic.

- Builder: build wheels into `/wheels` with cache mounts for pip and apt when building source extensions.
- Runtime: install using `--no-index --find-links /wheels` to ensure only pinned wheels are used.

Example pattern:

```dockerfile
# Builder: build wheels (uses BuildKit cache)
FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.lock.txt /build/
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip wheel --wheel-dir=/wheels -r requirements.lock.txt

# Runtime: install from local wheelhouse
FROM python:3.12-slim AS runtime
COPY --from=builder /wheels /wheels
COPY requirements.lock.txt /app/
RUN python -m pip install --no-index --find-links /wheels -r /app/requirements.lock.txt
```

Makefile targets (recommended, see `Makefile`):
- `make lock-deps` — generate `requirements.lock.txt`.
- `make wheelhouse-build` — build local `wheels/` using `pip wheel`.
- `make wheelhouse-check` — verify which packages have prebuilt wheels (`pip download --only-binary=:all:`).

CI snippet (prepare-wheels job):
```yaml
jobs:
  prepare-wheels:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install build deps
        run: python -m pip install --upgrade pip setuptools wheel
      - name: Build wheelhouse
        run: make wheelhouse-build
      - name: Upload wheelhouse
        uses: actions/upload-artifact@v4
        with:
          name: wheelhouse-${{ github.sha }}
          path: wheels/
```

Notes:
- For heavy media / native libs, add a build-arg `SKIP_MEDIA_PACKAGES=true` to skip apt installs and reduce image size and build time when not needed.
- Some packages require platform-specific wheels (grpcio, opencv, pillow); if targeting multi-arch, build wheels per-arch or use a maintained internal package registry.
- Check which packages need source builds with `make wheelhouse-check` and add build deps (libjpeg-dev, ffmpeg, poppler, build-essential) in the builder stage as required.

Checklist for templating into other repos:
1. Add `lock-deps`, `wheelhouse-build`, and `wheelhouse-check` Makefile targets.
2. Add `prepare-wheels` workflow that uploads `wheelhouse-${{ IMAGE_TAG }}` artifact.
3. Update `build-and-push-container.yml` to download the wheelhouse artifact and add `--mount=type=cache,target=/root/.cache/pip` & `/wheels` as cache mounts in your Dockerfile.
4. Document `SKIP_MEDIA_PACKAGES` usage and local validation steps in your repo `README.md`.

### Source Code Copying

**REQUIRED**: Copy source code after dependencies:

```dockerfile
# Copy source code (changes more frequently)
COPY . .
```

### Non-Root User

**REQUIRED**: Create and use non-root user:

```dockerfile
# Create non-root user
RUN groupadd -g 1000 appuser && \
    useradd -r -u 1000 -g appuser appuser

# Create necessary directories
RUN mkdir -p /app/uploads /app/temp /app/storage /app/logs && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser
```

### Port Exposure

**REQUIRED**: Expose application port:

```dockerfile
EXPOSE 8000
```

### Health Check

**REQUIRED**: Add health check:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
```

### Complete Dockerfile Example

**REQUIRED**: Complete optimized Dockerfile:

```dockerfile
# syntax=docker/dockerfile:1

FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create non-root user
RUN groupadd -g 1000 appuser && \
    useradd -r -u 1000 -g appuser appuser

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy dependency files
COPY requirements.txt pyproject.toml ./

# Install Python dependencies with cache
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Development stage
FROM base as development
RUN pip install -e ".[dev]"
COPY . .
RUN chown -R appuser:appuser /app
USER appuser
CMD ["python", "main.py"]

# Production stage
FROM base as production

# Install production dependencies only
RUN pip install -e ".[production]"

# Copy source code
COPY . ./

# Create necessary directories
RUN mkdir -p /app/uploads /app/temp /app/storage /app/logs && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Default command for production
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--timeout", "30", "--keep-alive", "2", "--access-logfile", "-", "--error-logfile", "-", "main:app"]
```

---

## Multi-Stage Builds

### Basic Multi-Stage Pattern

**REQUIRED**: Use multi-stage builds for optimization:

```dockerfile
# Stage 1: Builder stage
FROM python:3.11-slim as builder

WORKDIR /build

# Install build dependencies
RUN pip install --user --no-cache-dir \
    setuptools wheel

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime stage
FROM python:3.11-slim as runtime

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local

# Ensure local packages are in PATH
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY . .

# Run application
CMD ["python", "main.py"]
```

### Multi-Stage with Virtual Environment

**RECOMMENDED**: Use virtual environment in multi-stage:

```dockerfile
# Stage 1: Builder
FROM python:3.11-slim as builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/venv/bin:$PATH"

WORKDIR /app

# Create virtual environment
RUN python -m venv /app/venv

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim as runtime

ENV PYTHONUNBUFFERED=1 \
    PATH="/app/venv/bin:$PATH"

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/venv /app/venv

# Copy application code
COPY . .

# Run application
CMD ["python", "main.py"]
```

### Multi-Stage with Security Scanning

**RECOMMENDED**: Add security scanning stage:

```dockerfile
# Stage 1: Builder
FROM python:3.11-slim as builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: Security scanning
FROM builder as security
RUN pip install safety bandit && \
    safety check && \
    bandit -r /build

# Stage 3: Runtime
FROM python:3.11-slim as runtime
WORKDIR /app
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
COPY . .
CMD ["python", "main.py"]
```

---

## Security Best Practices

### Non-Root User

**REQUIRED**: Always run as non-root user:

```dockerfile
# Create user with specific UID/GID
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

USER appuser
```

### Minimal Base Images

**REQUIRED**: Use minimal base images:

```dockerfile
# Use slim or alpine variants
FROM python:3.11-slim

# Or Alpine for even smaller size
FROM python:3.11-alpine
```

### Image Pinning

**RECOMMENDED**: Pin images to specific digests:

```dockerfile
# Pin to specific digest for reproducibility
FROM python:3.11-slim@sha256:a8560b36e8b8210634f77d9f7f9efd7ffa463e380b75e2e74aff4511df3ef88c
```

### Remove Build Dependencies

**REQUIRED**: Remove build dependencies in final stage:

```dockerfile
# Builder stage with build tools
FROM python:3.11-slim as builder
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential

# Runtime stage without build tools
FROM python:3.11-slim as runtime
# Only runtime dependencies, no gcc/g++
```

### Clean Package Cache

**REQUIRED**: Clean package manager cache:

```dockerfile
# Combine apt-get commands and clean cache
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*
```

### Secrets Management

**REQUIRED**: Never commit secrets in Dockerfile:

```dockerfile
# BAD: Secrets in Dockerfile
ENV API_KEY=secret123

# GOOD: Use build args (not for secrets)
ARG BUILD_VERSION
ENV VERSION=$BUILD_VERSION

# BEST: Use Docker secrets or environment variables at runtime
# Pass secrets via docker-compose or Kubernetes secrets
```

### .dockerignore File

**REQUIRED**: Use .dockerignore to exclude files:

```dockerfile
# .dockerignore
# Git
.git/
.gitignore

# Documentation
*.md
docs/
LICENSE

# Environment files
.env
.env.*

# IDE files
.vscode/
.idea/
*.swp

# Python
__pycache__/
*.py[cod]
*.so
.Python
build/
dist/
*.egg-info/

# Virtual environments
venv/
env/
.venv/

# Testing
.pytest_cache/
.coverage
htmlcov/

# Logs
*.log
logs/

# Docker files
Dockerfile*
docker-compose*.yml
.dockerignore
```

---

## Image Optimization

### Layer Caching

**REQUIRED**: Optimize layer caching:

```dockerfile
# GOOD: Copy dependencies first (changes less frequently)
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Then copy source code (changes more frequently)
COPY . .
```

### BuildKit Cache Mounts

**RECOMMENDED**: Use BuildKit cache mounts:

```dockerfile
# syntax=docker/dockerfile:1

# Cache pip packages
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Cache apt packages
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y curl
```

### Multi-Line RUN Optimization

**REQUIRED**: Combine RUN commands:

```dockerfile
# BAD: Multiple RUN commands
RUN apt-get update
RUN apt-get install -y curl
RUN rm -rf /var/lib/apt/lists/*

# GOOD: Single RUN command
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*
```

### Sort Package Lists

**RECOMMENDED**: Sort package lists for readability:

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*
```

---

## Docker Compose Orchestration

### Basic Compose File

**REQUIRED**: Structure docker-compose.yml properly:

```yaml
# docker-compose.base.yml (base configuration)
services:
  app:
    build:
      context: .
      target: production
    container_name: myapp
    ports:
      - "${API_PORT:-8000}:8000"
    environment:
      # URLs and DNS from .env
      - BASE_URL=${BASE_URL:-http://localhost:8000}
      - API_BASE_URL=${API_BASE_URL:-${BASE_URL}/api}
      # Service URLs built from .env components
      - DATABASE_URL=postgresql://${DB_USER:-postgres}:${DB_PASSWORD:?required}@${DB_HOST:-postgres}:${DB_PORT:-5432}/${DB_NAME:-mydb}
      - REDIS_URL=${REDIS_URL:-redis://${REDIS_HOST:-redis}:${REDIS_PORT:-6379}}
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - app-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  postgres:
    image: postgres:15-alpine
    env_file:
      - .env.dev  # Database credentials from .env
    environment:
      - POSTGRES_DB=${DB_NAME:-mydb}
      - POSTGRES_USER=${DB_USER:-postgres}
      - POSTGRES_PASSWORD=${DB_PASSWORD:?DB_PASSWORD environment variable is required}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-postgres}"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    env_file:
      - .env.dev  # Redis configuration from .env
    command: >
      redis-server
      --requirepass ${REDIS_PASSWORD:?REDIS_PASSWORD environment variable is required}
      --appendonly yes
      --maxmemory ${REDIS_MAXMEMORY:-256mb}
      --maxmemory-policy ${REDIS_MAXMEMORY_POLICY:-allkeys-lru}
    volumes:
      - redis_data:/data
    networks:
      - app-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "--raw", "incr", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local

networks:
  app-network:
    driver: bridge
```

**Usage:**
```bash
# Development
docker compose -f docker-compose.base.yml -f docker-compose.dev.yml up

# Production
docker compose -f docker-compose.base.yml -f docker-compose.prod.yml up
```

### Service Dependencies

**REQUIRED**: Use depends_on with health checks:

```yaml
services:
  app:
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
```

### Environment Variables

**REQUIRED**: Use environment files as single source of truth:

```yaml
services:
  app:
    env_file:
      - .env.dev  # Single source of truth for all configuration
    environment:
      # URLs and DNS from .env
      - BASE_URL=${BASE_URL:?BASE_URL environment variable is required}
      - API_BASE_URL=${API_BASE_URL:-${BASE_URL}/api}
      # Service URLs from .env
      - REDIS_URL=${REDIS_URL:-redis://${REDIS_HOST:-redis}:${REDIS_PORT:-6379}}
      - MONGODB_URL=${MONGODB_URL:-mongodb://${MONGODB_USERNAME:-admin}:${MONGODB_PASSWORD:?required}@${MONGODB_HOST:-mongodb}:${MONGODB_PORT:-27017}/${MONGODB_DATABASE:-orchestrator}}
      # Application config from .env
      - DEBUG=${DEBUG:-false}
      - LOG_LEVEL=${LOG_LEVEL:-info}
      # Secrets from .env
      - SECRET_KEY=${SECRET_KEY:?SECRET_KEY environment variable is required}
```

### Restart Policies

**REQUIRED**: Set appropriate restart policies:

```yaml
services:
  app:
    # Always restart unless explicitly stopped
    restart: unless-stopped

    # Or use:
    # restart: always        # Always restart
    # restart: on-failure    # Restart on failure
    # restart: no           # Never restart
```

### Resource Limits

**REQUIRED**: Set resource limits:

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

### Profiles

**RECOMMENDED**: Use profiles for optional services:

```yaml
services:
  app:
    # Always runs
    image: myapp:latest

  mailhog:
    image: mailhog/mailhog:latest
    profiles:
      - dev

  pgadmin:
    image: dpage/pgadmin4:latest
    profiles:
      - dev
```

### Compose File Overrides

**RECOMMENDED**: Use override files:

```yaml
# docker-compose.base.yml (base)
services:
  app:
    build: .
    environment:
      # Base URLs from .env
      - BASE_URL=${BASE_URL:-http://localhost:8150}
      # Service URLs built from .env components
      - DATABASE_URL=postgresql://${DB_USER:-postgres}:${DB_PASSWORD:?required}@${DB_HOST:-postgres}:${DB_PORT:-5432}/${DB_NAME:-mydb}

# docker-compose.dev.yml (development)
services:
  app:
    extends:
      file: docker-compose.base.yml
      service: app
    env_file:
      - .env.dev  # Single source of truth
    volumes:
      - .:/app
    environment:
      - DEBUG=${DEBUG:-true}
      - RELOAD=${RELOAD:-true}
      # Override base URL for development
      - BASE_URL=${BASE_URL:-http://localhost:8150}
```

---

## Health Checks

### Dockerfile Health Check

**REQUIRED**: Add health check to Dockerfile:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
```

### Compose Health Check

**REQUIRED**: Define health checks in compose:

```yaml
services:
  app:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Health Check Endpoint

**REQUIRED**: Implement health check endpoint:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health_check():
    """Health check endpoint for Docker."""
    return {"status": "healthy"}
```

### Database Health Check

**REQUIRED**: Health check for database:

```yaml
services:
  postgres:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
```

### Redis Health Check

**REQUIRED**: Health check for Redis:

```yaml
services:
  redis:
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5
```

---

## Resource Management

### CPU Limits

**REQUIRED**: Set CPU limits:

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '2'
        reservations:
          cpus: '1'
```

### Memory Limits

**REQUIRED**: Set memory limits:

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 1G
```

### Gunicorn Workers

**REQUIRED**: Configure workers based on resources:

```dockerfile
# Calculate workers: (2 * CPU cores) + 1
CMD ["gunicorn", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "main:app"]
```

### ulimits

**RECOMMENDED**: Set ulimits:

```yaml
services:
  app:
    ulimits:
      nofile:
        soft: 65536
        hard: 65536
```

---

## Networking

### Custom Networks

**REQUIRED**: Use custom networks:

```yaml
networks:
  app-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

### Service Discovery

**REQUIRED**: Use service names for discovery, configured via `.env` files:

```yaml
services:
  app:
    env_file:
      - .env.dev
    environment:
      # Service URLs built from .env variables
      - DATABASE_URL=postgresql://${DB_USER:-postgres}:${DB_PASSWORD:?required}@${DB_HOST:-postgres}:${DB_PORT:-5432}/${DB_NAME:-mydb}
      # 'postgres' is the service name, but hostname comes from .env
      - DB_HOST=${DB_HOST:-postgres}  # Service name or external hostname
      - REDIS_HOST=${REDIS_HOST:-redis}  # Service name or external hostname
      - MONGODB_HOST=${MONGODB_HOST:-mongodb}  # Service name or external hostname
```

### Port Mapping

**REQUIRED**: Map ports correctly:

```yaml
services:
  app:
    ports:
      - "8000:8000"  # host:container
      - "127.0.0.1:8000:8000"  # Bind to specific interface
```

---

## Volume Management

### Named Volumes

**REQUIRED**: Use named volumes for data persistence:

```yaml
services:
  postgres:
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
    driver: local
```

### Bind Mounts

**RECOMMENDED**: Use bind mounts for development:

```yaml
services:
  app:
    volumes:
      - .:/app
      - /app/venv  # Anonymous volume to preserve venv
```

### Volume Permissions

**REQUIRED**: Set correct permissions:

```dockerfile
RUN mkdir -p /app/uploads /app/storage && \
    chown -R appuser:appuser /app
```

---

## Environment Configuration

### Environment Files as Single Source of Truth

**REQUIRED**: Use `.env` files as the **single source of truth** for all secrets, configuration, DNS, URLs, and deployment settings:

**Best Practices:**
- ✅ One `.env` file per environment (`.env.dev`, `.env.staging`, `.env.prod`)
- ✅ All secrets come from `.env` files, never hardcoded in compose files
- ✅ All base configurations (ports, hosts, DNS) come from `.env` files
- ✅ All URLs and service endpoints come from `.env` files
- ✅ Use `env_file` directive in docker-compose for centralized loading
- ✅ Enable dynamic deployment by making all deployment-specific values configurable
- ✅ Support multiple deployment targets (local, cloud, on-premises) via configuration
- ✅ Never commit `.env.*` files to version control (use `.env.*.example` templates)
- ✅ Build connection strings from environment variables, don't hardcode them

**Structure:**
```bash
# Project root
.env.dev.example      # Template for development
.env.staging.example  # Template for staging
.env.prod.example     # Template for production

# Actual files (in .gitignore)
.env.dev              # Development configuration (never commit)
.env.staging          # Staging configuration (never commit)
.env.prod             # Production configuration (never commit)
```

### Comprehensive Environment File Organization

**REQUIRED**: Organize `.env` files with comprehensive configuration including URLs and DNS:

```bash
# .env.dev.example
# ============================================
# Application Configuration
# ============================================
ENVIRONMENT=development
DEBUG=true
API_PORT=8150
PORT=8100

# ============================================
# Base URLs and DNS Configuration
# ============================================
# Base URL for the application (used for links, redirects, etc.)
BASE_URL=http://localhost:8150

# API endpoints
API_BASE_URL=http://localhost:8150/api
EXTERNAL_API_URL=http://localhost:8150
INTERNAL_API_URL=http://api:8100

# UI endpoints
WEBUI_BASE_URL=http://localhost:8150/ui

# External service URLs (for integrations)
EXTERNAL_SERVICE_URL=https://api.external-service.com
WEBHOOK_BASE_URL=https://your-domain.com/webhooks
CALLBACK_BASE_URL=https://your-domain.com/callbacks

# ============================================
# Service Discovery URLs
# ============================================
# These URLs are built from components below, but can be overridden
REDIS_URL=redis://redis:6379
MONGODB_URL=mongodb://admin:${MONGODB_PASSWORD}@mongodb:27017/orchestrator?authSource=admin
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/2

# ============================================
# MongoDB Configuration
# ============================================
MONGODB_HOST=mongodb
MONGODB_PORT=27017
MONGODB_USERNAME=admin
MONGODB_PASSWORD=CHANGE_ME_DEV_PASSWORD
MONGODB_DATABASE=orchestrator
MONGODB_DEPLOYMENT_TYPE=container

# ============================================
# Redis Configuration
# ============================================
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_CLUSTER_ENABLED=false
REDIS_CLUSTER_NODES=

# ============================================
# Celery Configuration
# ============================================
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/2

# ============================================
# Security Secrets (REQUIRED - Change these!)
# ============================================
SECRET_KEY=CHANGE_ME_DEV_SECRET_KEY_MIN_32_CHARS
JWT_SECRET_KEY=CHANGE_ME_DEV_JWT_SECRET_KEY_MIN_32_CHARS
SESSION_SECRET_KEY=CHANGE_ME_DEV_SESSION_SECRET_KEY_MIN_32_CHARS
DATABASE_ENCRYPTION_KEY=CHANGE_ME_DEV_ENCRYPTION_KEY_BASE64

# ============================================
# Admin User Configuration
# ============================================
ADMIN_USERNAME=admin
ADMIN_PASSWORD=CHANGE_ME_DEV_ADMIN_PASSWORD
ADMIN_EMAIL=admin@development.local
CLI_MASTER_PASSWORD=CHANGE_ME_DEV_CLI_MASTER_PASSWORD

# ============================================
# CORS Configuration
# ============================================
CORS_ORIGINS=http://localhost:3000,http://localhost:8080,http://localhost:8150
```

**Key Principles:**
- ✅ **Base URLs**: Define all base URLs (API, UI, external services)
- ✅ **DNS/Hostnames**: All hostnames and DNS names come from `.env`
- ✅ **Service Discovery**: Use service names for internal communication
- ✅ **External URLs**: Configure external-facing URLs for webhooks, callbacks
- ✅ **Deployment Flexibility**: Change deployment target by updating `.env` only

### Docker Compose Environment Configuration

**REQUIRED**: Use `env_file` directive for centralized configuration:

```yaml
# docker-compose.base.yml (base configuration)
services:
  api:
    # Base configuration without secrets - uses env vars from .env files
    environment:
      - PORT=${PORT:-8100}
      - REDIS_HOST=${REDIS_HOST:-redis}
      - REDIS_PORT=${REDIS_PORT:-6379}
      - BASE_URL=${BASE_URL:-http://localhost:8150}
      - API_BASE_URL=${API_BASE_URL:-${BASE_URL:-http://localhost:8150}/api}
      - WEBUI_BASE_URL=${WEBUI_BASE_URL:-${BASE_URL:-http://localhost:8150}/ui}

# docker-compose.dev.yml (development overrides)
services:
  api:
    extends:
      file: docker-compose.base.yml
      service: api
    env_file:
      - .env.dev  # Single source of truth for ALL configuration
    environment:
      - ENVIRONMENT=development
      - DEBUG=${DEBUG:-true}
      # URLs and DNS from .env
      - BASE_URL=${BASE_URL:-http://localhost:8150}
      - API_BASE_URL=${API_BASE_URL:-${BASE_URL}/api}
      - WEBUI_BASE_URL=${WEBUI_BASE_URL:-${BASE_URL}/ui}
      - EXTERNAL_API_URL=${EXTERNAL_API_URL:-${BASE_URL}}
      - INTERNAL_API_URL=${INTERNAL_API_URL:-http://api:8100}
      # Service URLs from .env
      - REDIS_URL=${REDIS_URL:-redis://${REDIS_HOST:-redis}:${REDIS_PORT:-6379}}
      - MONGODB_URL=${MONGODB_URL:-mongodb://${MONGODB_USERNAME:-admin}:${MONGODB_PASSWORD:?required}@${MONGODB_HOST:-mongodb}:${MONGODB_PORT:-27017}/${MONGODB_DATABASE:-orchestrator}?authSource=admin}
      - CELERY_BROKER_URL=${CELERY_BROKER_URL:-redis://${REDIS_HOST:-redis}:${REDIS_PORT:-6379}/1}
      - CELERY_RESULT_BACKEND=${CELERY_RESULT_BACKEND:-redis://${REDIS_HOST:-redis}:${REDIS_PORT:-6379}/2}
      # Secrets from .env
      - MONGODB_PASSWORD=${MONGODB_PASSWORD:?MONGODB_PASSWORD environment variable is required}
      - SECRET_KEY=${SECRET_KEY:?SECRET_KEY environment variable is required}
```

**Benefits:**
- ✅ **Dynamic Deployment**: Change deployment target by updating `.env` only
- ✅ **Environment Portability**: Same compose files work across environments
- ✅ **Service Discovery**: URLs automatically adapt to service names
- ✅ **External Integration**: Webhooks and callbacks use configured URLs
- ✅ **DNS Flexibility**: Support different DNS configurations per environment

### Environment Variable Substitution

**REQUIRED**: Use proper variable substitution syntax:

```yaml
# With default value (optional)
- PORT=${PORT:-8100}

# Required variable (will error if not set)
- PASSWORD=${PASSWORD:?PASSWORD environment variable is required}

# No default (uses value from .env or system)
- HOST=${HOST}

# Building connection strings from components
- DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD:?required}@${DB_HOST}:${DB_PORT:-5432}/${DB_NAME}

# Building URLs from base URL
- API_BASE_URL=${BASE_URL}/api
- WEBHOOK_URL=${BASE_URL}/webhooks
```

**Best Practices:**
- ✅ Use `${VAR:-default}` for optional values with sensible defaults
- ✅ Use `${VAR:?error message}` for required variables (enforces validation)
- ✅ Build connection strings from components, never hardcode full URLs
- ✅ Use descriptive error messages for required variables
- ✅ Build derived URLs from base URLs for consistency

### Dynamic Deployment Configuration

**REQUIRED**: Enable dynamic deployment through comprehensive configuration:

**Deployment Scenarios:**

1. **Local Development:**
   ```bash
   BASE_URL=http://localhost:8150
   MONGODB_HOST=mongodb
   REDIS_HOST=redis
   EXTERNAL_API_URL=http://localhost:8150
   ```

2. **Cloud Deployment (AWS/GCP/Azure):**
   ```bash
   BASE_URL=https://api.yourcompany.com
   MONGODB_HOST=mongodb-replica-0.your-namespace.svc.cluster.local
   REDIS_HOST=redis-cluster-0.your-namespace.svc.cluster.local
   EXTERNAL_API_URL=https://api.yourcompany.com
   WEBHOOK_BASE_URL=https://api.yourcompany.com/webhooks
   ```

3. **On-Premises Deployment:**
   ```bash
   BASE_URL=https://api.internal.company.com
   MONGODB_HOST=mongodb.internal.company.com
   REDIS_HOST=redis.internal.company.com
   EXTERNAL_API_URL=https://api.internal.company.com
   WEBHOOK_BASE_URL=https://api.internal.company.com/webhooks
   ```

**Benefits:**
- ✅ **Single Compose File**: Same compose files work everywhere
- ✅ **Environment Portability**: Deploy to any environment by changing `.env`
- ✅ **DNS Flexibility**: Support different DNS configurations
- ✅ **Service Discovery**: Automatic adaptation to service names
- ✅ **URL Management**: All URLs centralized in one place
- ✅ **Easy Migration**: Move between environments by updating `.env` only

### URL and DNS Best Practices

**REQUIRED**: Follow URL and DNS configuration best practices:

```bash
# ✅ GOOD: Base URLs defined in .env
BASE_URL=https://api.yourcompany.com
API_BASE_URL=${BASE_URL}/api
WEBUI_BASE_URL=https://app.yourcompany.com

# ✅ GOOD: Service discovery URLs
REDIS_URL=redis://${REDIS_HOST}:${REDIS_PORT}
MONGODB_URL=mongodb://${MONGODB_USERNAME}:${MONGODB_PASSWORD}@${MONGODB_HOST}:${MONGODB_PORT}/${MONGODB_DATABASE}

# ✅ GOOD: External service URLs
WEBHOOK_BASE_URL=${BASE_URL}/webhooks
CALLBACK_BASE_URL=${BASE_URL}/callbacks

# ❌ BAD: Hardcoded URLs in compose files
environment:
  - API_URL=https://api.yourcompany.com  # Hardcoded!

# ❌ BAD: Hardcoded service names
environment:
  - REDIS_HOST=redis-cluster-0  # Should come from .env
```

### Secrets Management

**REQUIRED**: Never hardcode secrets in compose files:

```yaml
# BAD: Hardcoded secrets
services:
  app:
    environment:
      - MONGODB_PASSWORD=MyPassword123
      - SECRET_KEY=hardcoded-secret-key

# GOOD: From .env file
services:
  app:
    env_file:
      - .env.dev
    environment:
      - MONGODB_PASSWORD=${MONGODB_PASSWORD:?MONGODB_PASSWORD environment variable is required}
      - SECRET_KEY=${SECRET_KEY:?SECRET_KEY environment variable is required}
```

**Production Secrets:**
```yaml
# For production, use secret management systems:
# - AWS Secrets Manager
# - HashiCorp Vault
# - Azure Key Vault
# - Kubernetes Secrets

# Example with Docker Swarm secrets:
services:
  app:
    secrets:
      - db_password
    environment:
      - DB_PASSWORD_FILE=/run/secrets/db_password

secrets:
  db_password:
    external: true
```

### Required vs Optional Variables

**REQUIRED**: Distinguish between required and optional variables:

```yaml
# Required variables (will fail if not set)
environment:
  - MONGODB_PASSWORD=${MONGODB_PASSWORD:?MONGODB_PASSWORD environment variable is required}
  - SECRET_KEY=${SECRET_KEY:?SECRET_KEY environment variable is required}
  - BASE_URL=${BASE_URL:?BASE_URL environment variable is required}

# Optional variables (use defaults if not set)
environment:
  - PORT=${PORT:-8100}
  - DEBUG=${DEBUG:-false}
  - LOG_LEVEL=${LOG_LEVEL:-info}
  - API_BASE_URL=${API_BASE_URL:-${BASE_URL}/api}
```

### Connection String Construction

**REQUIRED**: Build connection strings from environment variables:

```yaml
# BAD: Hardcoded connection string
environment:
  - MONGODB_URL=mongodb://admin:password@mongodb:27017/orchestrator

# GOOD: Built from components
environment:
  - MONGODB_URL=mongodb://${MONGODB_USERNAME:-admin}:${MONGODB_PASSWORD:?required}@${MONGODB_HOST:-mongodb}:${MONGODB_PORT:-27017}/${MONGODB_DATABASE:-orchestrator}?authSource=admin
```

### Environment File Validation

**REQUIRED**: Validate required environment variables:

```bash
# Docker Compose will validate required variables:
# If ${VAR:?error} is used and VAR is not set, compose will fail with error message

# Example error:
ERROR: Missing required environment variable: MONGODB_PASSWORD
```

### .gitignore Configuration

**REQUIRED**: Ensure `.env` files are ignored:

```gitignore
# Environment files - NEVER commit these!
.env
.env.*
!.env.*.example  # Allow example files
```

---

## Production Deployment

### Production Dockerfile

**REQUIRED**: Optimized production Dockerfile:

```dockerfile
# syntax=docker/dockerfile:1

FROM python:3.11-slim as base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PIP_NO_CACHE_DIR=1

# Create non-root user
RUN groupadd -g 1000 appuser && \
    useradd -r -u 1000 -g appuser appuser

WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

# Production stage
FROM base as production

COPY . .

RUN mkdir -p /app/uploads /app/storage /app/logs && \
    chown -R appuser:appuser /app

USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--timeout", "30", "--keep-alive", "2", "--access-logfile", "-", "--error-logfile", "-", "main:app"]
```

### Production Compose

**REQUIRED**: Production docker-compose.yml using `.env` files:

```yaml
# docker-compose.prod.yml
services:
  app:
    build:
      context: .
      target: production
    image: myapp:latest
    env_file:
      - .env.prod  # Single source of truth for production config
    restart: unless-stopped
    environment:
      # URLs and DNS from .env.prod
      - BASE_URL=${BASE_URL:?BASE_URL environment variable is required}
      - API_BASE_URL=${API_BASE_URL:-${BASE_URL}/api}
      - WEBUI_BASE_URL=${WEBUI_BASE_URL:-${BASE_URL}/ui}
      - EXTERNAL_API_URL=${EXTERNAL_API_URL:-${BASE_URL}}
      # Service URLs from .env.prod
      - REDIS_URL=${REDIS_URL:-redis://${REDIS_HOST:-redis}:${REDIS_PORT:-6379}}
      - MONGODB_URL=${MONGODB_URL:-mongodb://${MONGODB_USERNAME:-admin}:${MONGODB_PASSWORD:?required}@${MONGODB_HOST:-mongodb}:${MONGODB_PORT:-27017}/${MONGODB_DATABASE:-orchestrator}}
      # Secrets from .env.prod
      - SECRET_KEY=${SECRET_KEY:?SECRET_KEY environment variable is required}
      - MONGODB_PASSWORD=${MONGODB_PASSWORD:?MONGODB_PASSWORD environment variable is required}
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

**Usage:**
```bash
# Deploy to production
docker compose -f docker-compose.base.yml -f docker-compose.prod.yml up -d

# All configuration comes from .env.prod
# Change deployment target by updating .env.prod only
```

### Gunicorn Configuration

**REQUIRED**: Optimize Gunicorn for production:

```python
# gunicorn_config.py
import multiprocessing

bind = "0.0.0.0:8000"
workers = (multiprocessing.cpu_count() * 2) + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 50
preload_app = True
accesslog = "-"
errorlog = "-"
loglevel = "info"
```

---

## CI/CD Integration

### Build Arguments

**REQUIRED**: Use build arguments:

```dockerfile
ARG BUILD_VERSION
ARG BUILD_DATE
ARG GIT_COMMIT

LABEL version=$BUILD_VERSION \
      build-date=$BUILD_DATE \
      git-commit=$GIT_COMMIT
```

### Multi-Architecture Builds

**RECOMMENDED**: Build for multiple architectures:

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t myapp:latest .
```

### Image Tagging

**REQUIRED**: Tag images properly:

```bash
# Tag with version
docker build -t myapp:v1.0.0 .

# Tag with commit SHA
docker build -t myapp:$(git rev-parse --short HEAD) .

# Tag latest
docker build -t myapp:latest .
```

---

## Monitoring and Logging

### Logging Configuration

**REQUIRED**: Configure logging:

```yaml
services:
  app:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
        labels: "production"
```

### Log Aggregation

**RECOMMENDED**: Use log aggregation:

```yaml
services:
  app:
    logging:
      driver: "fluentd"
      options:
        fluentd-address: localhost:24224
        tag: "app.logs"
```

---

## Summary

### Key Takeaways

1. **Multi-Stage Builds**: Use multi-stage builds to reduce image size
2. **Non-Root User**: Always run containers as non-root user
3. **Layer Caching**: Optimize layer order for better caching
4. **Health Checks**: Implement health checks for all services
5. **Resource Limits**: Set CPU and memory limits
6. **Security**: Use minimal base images and scan for vulnerabilities
7. **Compose**: Use docker-compose for multi-service orchestration
8. **Logging**: Configure proper logging and log rotation
9. **Environment Files**: Use `.env` files as single source of truth for all secrets, configuration, URLs, and DNS
   - One `.env` file per environment (`.env.dev`, `.env.staging`, `.env.prod`)
   - Use `env_file` directive in docker-compose for centralized loading
   - Never hardcode secrets, URLs, or DNS in compose files
   - Configure all base URLs, API endpoints, and service URLs in `.env`
   - Enable dynamic deployment by making all deployment-specific values configurable
   - Support multiple deployment targets (local, cloud, on-premises) via `.env` configuration
   - Use base + override compose pattern for multi-environment deployments
   - Build connection strings from environment variables, never hardcode them
   - Use `${VAR:?error}` for required variables, `${VAR:-default}` for optional
10. **Production**: Optimize for production with proper Gunicorn configuration and `.env`-based configuration

### Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Multi-Stage Builds](https://docs.docker.com/build/building/multi-stage/)

---

**Version**: v1.0.0
**Last Updated**: 2025-01-14
