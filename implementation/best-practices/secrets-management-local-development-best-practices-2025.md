# Secrets Management: Local & Development Best Practices

**Version**: v1.0.0
**Last Updated**: 2025-11-18

This document provides comprehensive best practices for managing credentials and secrets in local and development environments for modern applications (Python/FastAPI, Node.js/Next.js/NestJS), covering central credential functions, service-specific credential separation, environment-based configuration, local execution patterns, and development credential management.

**Related Documentation**: For production secrets management with external key vaults, see [Secrets Management: External Key Vaults & Credential Managers Best Practices](./secrets-management-external-key-vaults-best-practices-2025.md).

---

## Table of Contents

1. [Architecture Principles](#architecture-principles)
2. [Central Credential Functions](#central-credential-functions)
3. [Service-Specific Credential Separation](#service-specific-credential-separation)
4. [Credential Hierarchy & Priority](#credential-hierarchy--priority)
5. [Environment-Based Configuration](#environment-based-configuration)
6. [Local Execution Patterns](#local-execution-patterns)
7. [Basic Credential Rotation](#basic-credential-rotation)
8. [Audit Logging & Monitoring](#audit-logging--monitoring)
9. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)

---

## Architecture Principles

### Single Source of Truth

**REQUIRED**: Understand credential management principles:

1. **Central Functions**: All credential access through central functions
2. **Service Separation**: Different credentials for different services
3. **Environment Hierarchy**: Credentials vary by environment (dev/staging/prod)
4. **Never Hardcode**: No credentials in source code
5. **Validated Access**: All credential access validated and logged
6. **Documented**: Clear documentation of where credentials are used

### When to Use Central Credential Management

**REQUIRED**: Use central credential management when:

- **Multiple Systems**: Application connects to multiple services (databases, caches, queues, APIs)
- **Multiple Environments**: Different credentials for dev/staging/production
- **Team Development**: Multiple developers need consistent credential access
- **Security Compliance**: Audit requirements for credential access
- **Credential Rotation**: Need to rotate credentials without code changes
- **12-Factor App**: Following 12-factor app principles

---

## Central Credential Functions

### Single Source of Truth Pattern

**REQUIRED**: Implement central credential functions:

#### Python/FastAPI Implementation

```python
# config/credentials.py
"""
Central credential management - SINGLE SOURCE OF TRUTH
All components MUST use these functions instead of directly calling os.getenv()
"""
import os
from typing import Tuple
from functools import lru_cache

# CRITICAL: Single default password for entire application
# DO NOT change this without updating ALL references
DEFAULT_ADMIN_PASSWORD = "admin123!"

@lru_cache()
def get_admin_credentials() -> Tuple[str, str, str]:
    """
    Get admin credentials from central configuration.

    SINGLE SOURCE OF TRUTH for admin credentials across the entire application.
    All components MUST use this function instead of directly calling os.getenv().

    Returns:
        Tuple of (username, password, email)

    Raises:
        ValueError: If credentials cannot be determined
    """
    try:
        # Priority 1: Try to get from validated Settings (preferred)
        from config.settings import settings
        if hasattr(settings, 'security') and settings.security:
            return (
                settings.security.admin_username,
                settings.security.admin_password,
                settings.security.admin_email
            )
    except (ImportError, AttributeError):
        pass

    # Priority 2: Environment variables (for initialization before Settings loads)
    admin_username = os.getenv("ADMIN_USERNAME", "admin")
    admin_password = os.getenv("ADMIN_PASSWORD", DEFAULT_ADMIN_PASSWORD)
    admin_email = os.getenv("ADMIN_EMAIL", "admin@application.local")

    return (admin_username, admin_password, admin_email)


def get_admin_username() -> str:
    """Get admin username from central configuration."""
    return get_admin_credentials()[0]


def get_admin_password() -> str:
    """Get admin password from central configuration."""
    return get_admin_credentials()[1]


def get_admin_email() -> str:
    """Get admin email from central configuration."""
    return get_admin_credentials()[2]
```

#### Node.js/TypeScript Implementation

```typescript
// config/credentials.ts
/**
 * Central credential management - SINGLE SOURCE OF TRUTH
 * All components MUST use these functions instead of directly accessing process.env
 */

// CRITICAL: Single default password for entire application
const DEFAULT_ADMIN_PASSWORD = "admin123!";

interface AdminCredentials {
  username: string;
  password: string;
  email: string;
}

let cachedCredentials: AdminCredentials | null = null;

export function getAdminCredentials(): AdminCredentials {
  if (cachedCredentials) {
    return cachedCredentials;
  }

  // Priority 1: Try to get from validated config (preferred)
  try {
    const config = require('./settings').settings;
    if (config?.security) {
      cachedCredentials = {
        username: config.security.adminUsername,
        password: config.security.adminPassword,
        email: config.security.adminEmail,
      };
      return cachedCredentials;
    }
  } catch (error) {
    // Fall through to environment variables
  }

  // Priority 2: Environment variables
  cachedCredentials = {
    username: process.env.ADMIN_USERNAME || "admin",
    password: process.env.ADMIN_PASSWORD || DEFAULT_ADMIN_PASSWORD,
    email: process.env.ADMIN_EMAIL || "admin@application.local",
  };

  return cachedCredentials;
}

export function getAdminUsername(): string {
  return getAdminCredentials().username;
}

export function getAdminPassword(): string {
  return getAdminCredentials().password;
}

export function getAdminEmail(): string {
  return getAdminCredentials().email;
}
```

### Usage Pattern

**REQUIRED**: All components use central functions:

```python
# ✅ Good: Use central function
from config.credentials import get_admin_credentials

def initialize_admin_user():
    username, password, email = get_admin_credentials()
    # Use credentials...

# ❌ Bad: Direct environment variable access
def initialize_admin_user():
    username = os.getenv("ADMIN_USERNAME", "admin")  # DON'T DO THIS
    password = os.getenv("ADMIN_PASSWORD", "admin123!")  # DON'T DO THIS
```

---

## Service-Specific Credential Separation

### Separate Credentials Per Service

**REQUIRED**: Different services use different credentials:

#### Python/FastAPI Implementation

```python
# config/credentials.py

def get_database_credentials() -> Tuple[str, str, str]:
    """
    Get database credentials (MongoDB, PostgreSQL, etc.).

    Returns:
        Tuple of (host, username, password)
    """
    try:
        from config.settings import settings
        if hasattr(settings, 'database') and settings.database:
            return (
                settings.database.host,
                settings.database.username,
                settings.database.password
            )
    except (ImportError, AttributeError):
        pass

    # Environment variables with NO defaults (must be set)
    host = os.getenv("DATABASE_HOST")
    username = os.getenv("DATABASE_USERNAME")
    password = os.getenv("DATABASE_PASSWORD")

    if not all([host, username, password]):
        raise ValueError(
            "Database credentials must be set via environment variables: "
            "DATABASE_HOST, DATABASE_USERNAME, DATABASE_PASSWORD"
        )

    return (host, username, password)


def get_cache_credentials() -> Tuple[str, Optional[str], Optional[str]]:
    """
    Get cache credentials (Redis, Memcached, etc.).

    Returns:
        Tuple of (host, username, password)
        Username and password are optional (some caches don't require auth)
    """
    try:
        from config.settings import settings
        if hasattr(settings, 'cache') and settings.cache:
            return (
                settings.cache.host,
                getattr(settings.cache, 'username', None),
                getattr(settings.cache, 'password', None)
            )
    except (ImportError, AttributeError):
        pass

    host = os.getenv("CACHE_HOST", "localhost")
    username = os.getenv("CACHE_USERNAME")  # Optional
    password = os.getenv("CACHE_PASSWORD")  # Optional

    return (host, username, password)


def get_queue_credentials() -> str:
    """
    Get message queue connection URL (Celery, RabbitMQ, etc.).

    Returns:
        Connection URL string
    """
    try:
        from config.settings import settings
        if hasattr(settings, 'queue') and settings.queue:
            return settings.queue.broker_url
    except (ImportError, AttributeError):
        pass

    broker_url = os.getenv("CELERY_BROKER_URL") or os.getenv("QUEUE_URL")
    if not broker_url:
        raise ValueError(
            "Queue broker URL must be set via CELERY_BROKER_URL or QUEUE_URL"
        )

    return broker_url


def get_external_api_credentials(service_name: str) -> Tuple[str, Optional[str]]:
    """
    Get external API credentials (third-party services).

    Args:
        service_name: Name of the external service (e.g., "vcenter", "nsx")

    Returns:
        Tuple of (api_key, api_secret)
    """
    # Service-specific environment variables
    api_key = os.getenv(f"{service_name.upper()}_API_KEY")
    api_secret = os.getenv(f"{service_name.upper()}_API_SECRET")

    if not api_key:
        raise ValueError(
            f"API key for {service_name} must be set via "
            f"{service_name.upper()}_API_KEY environment variable"
        )

    return (api_key, api_secret)
```

#### Node.js/TypeScript Implementation

```typescript
// config/credentials.ts

export interface DatabaseCredentials {
  host: string;
  username: string;
  password: string;
  database?: string;
}

export function getDatabaseCredentials(): DatabaseCredentials {
  try {
    const config = require('./settings').settings;
    if (config?.database) {
      return {
        host: config.database.host,
        username: config.database.username,
        password: config.database.password,
        database: config.database.database,
      };
    }
  } catch (error) {
    // Fall through to environment variables
  }

  const host = process.env.DATABASE_HOST;
  const username = process.env.DATABASE_USERNAME;
  const password = process.env.DATABASE_PASSWORD;

  if (!host || !username || !password) {
    throw new Error(
      "Database credentials must be set via environment variables: " +
      "DATABASE_HOST, DATABASE_USERNAME, DATABASE_PASSWORD"
    );
  }

  return { host, username, password, database: process.env.DATABASE_NAME };
}

export interface CacheCredentials {
  host: string;
  username?: string;
  password?: string;
}

export function getCacheCredentials(): CacheCredentials {
  try {
    const config = require('./settings').settings;
    if (config?.cache) {
      return {
        host: config.cache.host,
        username: config.cache.username,
        password: config.cache.password,
      };
    }
  } catch (error) {
    // Fall through to environment variables
  }

  return {
    host: process.env.CACHE_HOST || "localhost",
    username: process.env.CACHE_USERNAME,
    password: process.env.CACHE_PASSWORD,
  };
}

export function getQueueCredentials(): string {
  try {
    const config = require('./settings').settings;
    if (config?.queue?.brokerUrl) {
      return config.queue.brokerUrl;
    }
  } catch (error) {
    // Fall through to environment variables
  }

  const brokerUrl = process.env.CELERY_BROKER_URL || process.env.QUEUE_URL;
  if (!brokerUrl) {
    throw new Error(
      "Queue broker URL must be set via CELERY_BROKER_URL or QUEUE_URL"
    );
  }

  return brokerUrl;
}

export function getExternalApiCredentials(
  serviceName: string
): { apiKey: string; apiSecret?: string } {
  const apiKey = process.env[`${serviceName.toUpperCase()}_API_KEY`];
  const apiSecret = process.env[`${serviceName.toUpperCase()}_API_SECRET`];

  if (!apiKey) {
    throw new Error(
      `API key for ${serviceName} must be set via ` +
      `${serviceName.toUpperCase()}_API_KEY environment variable`
    );
  }

  return { apiKey, apiSecret };
}
```

---

## Credential Hierarchy & Priority

### Credential Source Priority (Local/Development)

**REQUIRED**: Credential resolution priority for local/development (highest to lowest):

```python
# config/credentials.py

def get_credential_with_priority(credential_name: str) -> str:
    """
    Get credential with priority-based resolution.

    Priority order (highest to lowest) for local/development:
    1. Environment Variables (.env files, container env vars)
    2. Encrypted Local Storage (SecretsManager with master password)
    3. Validated Config (Settings with validation)
    4. Development Defaults (ONLY for dev, NEVER for production)
    """
    environment = os.getenv("ENVIRONMENT", "development")

    # Priority 1: Environment Variables
    env_value = os.getenv(credential_name)
    if env_value:
        return env_value

    # Priority 2: Encrypted Local Storage
    try:
        from services.secrets.secrets_manager import SecretsManager
        secrets_manager = SecretsManager()
        await secrets_manager.initialize()
        secret = await secrets_manager.get_credential(credential_name)
        if secret:
            return secret
    except (ImportError, Exception):
        pass

    # Priority 3: Validated Config
    try:
        from config.settings import settings
        if hasattr(settings, credential_name.lower()):
            return getattr(settings, credential_name.lower())
    except (ImportError, AttributeError):
        pass

    # Priority 4: Development Defaults (ONLY for dev)
    if environment == "development":
        defaults = {
            "ADMIN_PASSWORD": DEFAULT_ADMIN_PASSWORD,
            # Add other development defaults here
        }
        if credential_name in defaults:
            return defaults[credential_name]

    raise ValueError(f"Credential '{credential_name}' not found")
```

**Note**: For production environments, external secrets managers take highest priority. See [External Key Vaults Best Practices](./secrets-management-external-key-vaults-best-practices-2025.md) for production patterns.

---

## Environment-Based Configuration

### Environment-Specific Credentials

**REQUIRED**: Different credentials for different environments:

#### Environment File Structure

```
config/
├── .env.example          # Template (committed to repo)
├── .env.dev              # Development (NOT committed)
├── .env.staging          # Staging (NOT committed)
└── credentials.enc       # Encrypted credentials (NOT committed)
```

#### .env.example Template

```bash
# ============================================
# Application Admin Credentials
# ============================================
ADMIN_USERNAME=admin
ADMIN_PASSWORD=CHANGE_ME_MIN_8_CHARS
ADMIN_EMAIL=admin@example.com

# ============================================
# Database Credentials
# ============================================
DATABASE_HOST=localhost
DATABASE_PORT=27017
DATABASE_USERNAME=admin
DATABASE_PASSWORD=CHANGE_ME
DATABASE_NAME=application
DATABASE_URL=mongodb://admin:CHANGE_ME@localhost:27017/application?authSource=admin

# ============================================
# Cache Credentials (Redis, Memcached, etc.)
# ============================================
CACHE_HOST=localhost
CACHE_PORT=6379
CACHE_USERNAME=          # Optional - leave empty if no auth
CACHE_PASSWORD=          # Optional - leave empty if no auth
CACHE_URL=redis://localhost:6379/0

# ============================================
# Message Queue Credentials (Celery, RabbitMQ, etc.)
# ============================================
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2
QUEUE_URL=redis://localhost:6379/1

# ============================================
# Security Keys
# ============================================
# Generate with: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
SECRET_KEY=CHANGE_ME_32_CHARS_MIN
JWT_SECRET_KEY=CHANGE_ME_32_CHARS_MIN
SESSION_SECRET_KEY=CHANGE_ME_32_CHARS_MIN
DATABASE_ENCRYPTION_KEY=CHANGE_ME_FERNET_KEY

# ============================================
# Master Password (for SecretsManager encryption)
# ============================================
CLI_MASTER_PASSWORD=CHANGE_ME_SECURE_PASSWORD

# ============================================
# External API Credentials
# ============================================
# Service-specific credentials (add as needed)
VCENTER_API_KEY=CHANGE_ME
VCENTER_API_SECRET=CHANGE_ME
NSX_API_KEY=CHANGE_ME
NSX_API_SECRET=CHANGE_ME

# ============================================
# Environment Configuration
# ============================================
ENVIRONMENT=development
DEBUG=true
PORT=8100
HOST=0.0.0.0
```

#### .env.dev (Development - NOT Committed)

```bash
# Development credentials (safe defaults for local dev)
ADMIN_USERNAME=devadmin
ADMIN_PASSWORD=devpass123
ADMIN_EMAIL=admin@development.local

DATABASE_HOST=localhost
DATABASE_PASSWORD=devpass
DATABASE_URL=mongodb://admin:devpass@localhost:27017/application

CACHE_HOST=localhost
CACHE_URL=redis://localhost:6379/0

CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

SECRET_KEY=dev-secret-key-not-for-production-32chars
JWT_SECRET_KEY=dev-jwt-secret-key-not-for-production-32chars
CLI_MASTER_PASSWORD=devmaster

ENVIRONMENT=development
DEBUG=true
PORT=8100
```

---

## Local Execution Patterns

### Python/FastAPI Local Execution

**REQUIRED**: Local execution setup:

#### 1. Environment Setup

```bash
# Create .env file from template
cp .env.example .env

# Edit .env with your credentials
# For development, you can use safe defaults
```

#### 2. Start Application

```bash
# Option 1: Direct Python execution
python app.py

# Option 2: Uvicorn with reload (development)
python -m uvicorn app:app --host 0.0.0.0 --port 8100 --reload

# Option 3: Uvicorn with custom port from config
python -m uvicorn app:app --host 0.0.0.0 --port ${PORT:-8100} --reload

# Option 4: Using environment-specific .env file
export ENV_FILE=.env.dev
python -m uvicorn app:app --host 0.0.0.0 --port 8100 --reload
```

#### 3. Credential Resolution Flow

```
Application Startup
    ↓
Load .env file (if exists)
    ↓
Initialize Settings (Pydantic validation)
    ↓
Central Credential Functions Called
    ↓
Priority Resolution:
    1. Settings.security.admin_username (validated)
    2. Environment variable ADMIN_USERNAME
    3. Development default "admin"
    ↓
Credentials Used Throughout Application
```

#### 4. Service Initialization

```python
# Example: Database initialization using central credentials
from config.credentials import get_database_credentials

def initialize_database():
    host, username, password = get_database_credentials()
    connection_string = f"mongodb://{username}:{password}@{host}:27017/database"
    # Initialize database connection...
```

### Node.js/Next.js/NestJS Local Execution

**REQUIRED**: Local execution setup:

#### 1. Environment Setup

```bash
# Create .env file from template
cp .env.example .env

# Edit .env with your credentials
# For development, you can use safe defaults
```

#### 2. Start Application

```bash
# Next.js
npm run dev
# or
yarn dev
# or
pnpm dev

# NestJS
npm run start:dev
# or
yarn start:dev
# or
pnpm start:dev

# Node.js (Express, etc.)
node server.js
# or with environment
NODE_ENV=development node server.js
```

#### 3. Credential Resolution Flow

```
Application Startup
    ↓
Load .env file (dotenv)
    ↓
Initialize Config (validation)
    ↓
Central Credential Functions Called
    ↓
Priority Resolution:
    1. Config.security.adminUsername (validated)
    2. process.env.ADMIN_USERNAME
    3. Development default "admin"
    ↓
Credentials Used Throughout Application
```

#### 4. Service Initialization

```typescript
// Example: Database initialization using central credentials
import { getDatabaseCredentials } from './config/credentials';

async function initializeDatabase() {
  const { host, username, password, database } = getDatabaseCredentials();
  const connectionString = `mongodb://${username}:${password}@${host}:27017/${database}`;
  // Initialize database connection...
}
```

---

## Basic Credential Rotation

### Zero-Downtime Rotation

**RECOMMENDED**: Support credential rotation without downtime:

```python
# config/credentials.py

def get_admin_password() -> str:
    """
    Get admin password with rotation support.

    During rotation period, accepts both old and new passwords.
    """
    # Try new password first (rotation period)
    new_password = os.getenv("ADMIN_PASSWORD_NEW")
    if new_password:
        # Migration period - log rotation
        logger.info("Using new admin password (rotation in progress)")
        return new_password

    # Fall back to current password
    current_password = os.getenv("ADMIN_PASSWORD")
    if current_password:
        return current_password

    # Development default
    if os.getenv("ENVIRONMENT") == "development":
        return DEFAULT_ADMIN_PASSWORD

    raise ValueError("ADMIN_PASSWORD must be set")
```

### Rotation Workflow

```bash
# Step 1: Set new password (old still works)
export ADMIN_PASSWORD_NEW=new_secure_password

# Step 2: Restart application (accepts both old and new)
# Application logs show "rotation in progress"

# Step 3: Update all services to use new password
# Verify all services working with new password

# Step 4: Remove old password, keep only new
export ADMIN_PASSWORD=new_secure_password
unset ADMIN_PASSWORD_NEW

# Step 5: Restart application (now only new password works)
```

**Note**: For production environments with external secrets managers, see [External Key Vaults Best Practices](./secrets-management-external-key-vaults-best-practices-2025.md) for advanced rotation strategies.

---

## Audit Logging & Monitoring

### Credential Access Logging

**REQUIRED**: Log all credential access:

```python
# config/credentials.py
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def get_admin_credentials() -> Tuple[str, str, str]:
    """Get admin credentials with audit logging."""
    credentials = # ... get credentials ...

    # Audit log (without exposing password)
    logger.info(
        "Admin credentials accessed",
        extra={
            "username": credentials[0],
            "source": "settings" if hasattr(settings, 'security') else "env",
            "environment": os.getenv("ENVIRONMENT", "development"),
            "timestamp": datetime.now().isoformat(),
            "credential_type": "admin",
            # DO NOT log password
        }
    )

    return credentials
```

### Monitoring Credential Usage

**RECOMMENDED**: Track credential access patterns:

```python
# config/credentials.py
from typing import Dict
from collections import defaultdict

_credential_access_count: Dict[str, int] = defaultdict(int)

def get_credential_with_monitoring(credential_name: str) -> str:
    """Get credential with usage monitoring."""
    credential = # ... get credential ...

    # Track access
    _credential_access_count[credential_name] += 1

    # Log if threshold exceeded
    if _credential_access_count[credential_name] > 1000:
        logger.warning(
            f"High credential access count for {credential_name}: "
            f"{_credential_access_count[credential_name]}"
        )

    return credential
```

---

## Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Hardcoded Credentials

```python
# ❌ BAD: Hardcoded credentials
def connect_to_database():
    username = "admin"
    password = "admin123!"
    # ...

# ✅ GOOD: Use central function
from config.credentials import get_database_credentials

def connect_to_database():
    host, username, password = get_database_credentials()
    # ...
```

### ❌ Anti-Pattern 2: Multiple Default Passwords

```python
# ❌ BAD: Different defaults in different places
# auth.py
admin_password = os.getenv("ADMIN_PASSWORD", "admin123!")

# database.py
admin_password = os.getenv("ADMIN_PASSWORD", "BaselineTest2025SecurePassword")

# init.py
admin_password = os.getenv("ADMIN_PASSWORD", "default123")

# ✅ GOOD: Single default in central function
from config.credentials import get_admin_password

admin_password = get_admin_password()  # Single source of truth
```

### ❌ Anti-Pattern 3: Direct Environment Variable Access

```python
# ❌ BAD: Direct os.getenv() calls everywhere
def initialize_service():
    username = os.getenv("ADMIN_USERNAME", "admin")
    password = os.getenv("ADMIN_PASSWORD", "admin123!")
    # ...

# ✅ GOOD: Use central function
from config.credentials import get_admin_credentials

def initialize_service():
    username, password, email = get_admin_credentials()
    # ...
```

### ❌ Anti-Pattern 4: Credentials in Version Control

```bash
# ❌ BAD: Committing .env files
git add .env
git commit -m "Add credentials"

# ✅ GOOD: Only commit .env.example
git add .env.example
# .env is in .gitignore
```

### ❌ Anti-Pattern 5: Same Credentials for All Services

```python
# ❌ BAD: Reusing admin password for everything
database_password = os.getenv("ADMIN_PASSWORD")
cache_password = os.getenv("ADMIN_PASSWORD")
queue_password = os.getenv("ADMIN_PASSWORD")

# ✅ GOOD: Service-specific credentials
from config.credentials import (
    get_database_credentials,
    get_cache_credentials,
    get_queue_credentials
)

db_host, db_user, db_pass = get_database_credentials()
cache_host, cache_user, cache_pass = get_cache_credentials()
queue_url = get_queue_credentials()
```

---

## Summary

### Key Takeaways

1. **Central Functions**: Single source of truth for all credentials
2. **Service Separation**: Different credentials for different services
3. **Environment Hierarchy**: Credentials vary by environment
4. **Never Hardcode**: No credentials in source code
5. **Validated Access**: All credential access validated and logged
6. **Local Execution**: Clear patterns for Python and Node.js
7. **Development Focus**: Safe defaults for local development

### Implementation Checklist

- [ ] Create central credential functions
- [ ] Implement service-specific credential functions
- [ ] Set up environment file structure (.env.example, .env.dev, etc.)
- [ ] Configure credential hierarchy and priority
- [ ] Add audit logging for credential access
- [ ] Document local execution patterns
- [ ] Update all components to use central functions
- [ ] Remove all hardcoded credentials
- [ ] Add .env files to .gitignore

### Next Steps

For production deployment with external secrets managers, see:
- [Secrets Management: External Key Vaults & Credential Managers Best Practices](./secrets-management-external-key-vaults-best-practices-2025.md)

---

**Version**: v1.0.0
**Last Updated**: 2025-11-18
