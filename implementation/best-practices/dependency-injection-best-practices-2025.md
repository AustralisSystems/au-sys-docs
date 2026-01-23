# Dependency Injection Best Practices

**Version**: v1.0.0  
**Last Updated**: 2025-01-14

This document provides comprehensive best practices for implementing dependency injection in FastAPI applications, covering Depends patterns, dependency scopes (function, request, application), dependencies with yield for cleanup, sub-dependencies, dependency caching, class-based dependencies, dependency overrides for testing, global dependencies, and production deployment.

---

## Table of Contents

1. [Architecture Principles](#architecture-principles)
2. [Basic Dependency Injection](#basic-dependency-injection)
3. [Dependency Scopes](#dependency-scopes)
4. [Dependencies with Yield](#dependencies-with-yield)
5. [Sub-Dependencies](#sub-dependencies)
6. [Dependency Caching](#dependency-caching)
7. [Class-Based Dependencies](#class-based-dependencies)
8. [Dependency Overrides](#dependency-overrides)
9. [Global Dependencies](#global-dependencies)
10. [Advanced Patterns](#advanced-patterns)
11. [Testing Dependencies](#testing-dependencies)
12. [Production Deployment](#production-deployment)

---

## Architecture Principles

### Dependency Injection Philosophy

**REQUIRED**: Understand dependency injection principles:

1. **Inversion of Control (IoC)**: Dependencies are provided rather than created
2. **Separation of Concerns**: Business logic separated from infrastructure
3. **Testability**: Dependencies can be easily mocked/replaced
4. **Reusability**: Common logic extracted into reusable dependencies
5. **Type Safety**: Type hints ensure correct dependency usage
6. **Lifecycle Management**: Proper resource cleanup with yield
7. **Scope Management**: Appropriate dependency lifetimes

### When to Use Dependency Injection

**REQUIRED**: Use dependency injection for:

- **Authentication/Authorization**: User validation, permission checks
- **Database Sessions**: Connection management, transaction handling
- **Service Layer**: Business logic services, repositories
- **Configuration**: Settings, environment variables
- **External Clients**: HTTP clients, message queues, caches
- **Request Context**: Request ID, user context, correlation IDs
- **Validation**: Input validation, data transformation
- **Logging**: Structured logging, request logging

**Avoid dependency injection for:**
- **Simple values**: Use query/path parameters directly
- **Static configuration**: Use module-level constants
- **Pure functions**: No need for DI if no dependencies

---

## Basic Dependency Injection

### Using Annotated (Recommended)

**REQUIRED**: Use `Annotated` for type hints (Python 3.9+):

```python
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

async def common_parameters(
    q: str | None = None,
    skip: int = 0,
    limit: int = 100,
):
    """Common query parameters dependency."""
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(
    commons: Annotated[dict, Depends(common_parameters)]
):
    """Read items with common parameters."""
    return {"items": [], **commons}

@app.get("/users/")
async def read_users(
    commons: Annotated[dict, Depends(common_parameters)]
):
    """Read users with common parameters."""
    return {"users": [], **commons}
```

### Using Depends Directly (Python 3.8)

**REQUIRED**: For Python 3.8 compatibility:

```python
from typing_extensions import Annotated
from fastapi import Depends, FastAPI

# Same as above, but use typing_extensions.Annotated
```

### Simple Dependency Function

**REQUIRED**: Basic dependency function:

```python
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

def get_settings():
    """Get application settings."""
    return {"app_name": "MyApp", "version": "1.0.0"}

@app.get("/info")
async def get_info(
    settings: Annotated[dict, Depends(get_settings)]
):
    """Get application info."""
    return settings
```

### Async Dependency Function

**REQUIRED**: Async dependencies for async operations:

```python
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

async def get_current_user_id(request: Request) -> int:
    """Get current user ID from request."""
    # Async operation (e.g., database lookup)
    user_id = await extract_user_id(request)
    return user_id

@app.get("/profile")
async def get_profile(
    user_id: Annotated[int, Depends(get_current_user_id)]
):
    """Get user profile."""
    return {"user_id": user_id}
```

---

## Dependency Scopes

### Function Scope (Default)

**REQUIRED**: Function scope closes dependency before sending response:

```python
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

def get_resource():
    """Resource with function scope."""
    resource = setup_resource()
    try:
        yield resource
    finally:
        cleanup_resource(resource)

@app.get("/")
async def endpoint(
    resource: Annotated[dict, Depends(get_resource, scope="function")]
):
    """Endpoint with function-scoped dependency."""
    return {"message": "ok"}
    # Resource cleaned up BEFORE response is sent
```

### Request Scope

**REQUIRED**: Request scope closes dependency after sending response:

```python
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

async def get_db_session():
    """Database session with request scope."""
    session = create_session()
    try:
        yield session
    finally:
        await session.close()

@app.get("/items/")
async def read_items(
    db: Annotated[Session, Depends(get_db_session, scope="request")]
):
    """Read items with request-scoped database session."""
    return db.query(Item).all()
    # Session closed AFTER response is sent
```

### Application Scope

**RECOMMENDED**: Application scope for singletons:

```python
from typing import Annotated
from fastapi import Depends, FastAPI
from functools import lru_cache

app = FastAPI()

@lru_cache()
def get_settings():
    """Application-scoped settings (singleton)."""
    return Settings()

@app.get("/config")
async def get_config(
    settings: Annotated[Settings, Depends(get_settings)]
):
    """Get application configuration."""
    return settings
```

### Scope Comparison

**REQUIRED**: Understand scope differences:

| Scope | Lifetime | Cleanup Timing | Use Case |
|-------|----------|----------------|----------|
| `function` | Per function call | Before response | Resources needed only during handler execution |
| `request` | Per HTTP request | After response | Database sessions, request context |
| `application` | Per application | Never (or on shutdown) | Singletons, configuration |

---

## Dependencies with Yield

### Database Session with Yield

**REQUIRED**: Database session with proper cleanup:

```python
from typing import Annotated, AsyncGenerator
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

app = FastAPI()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session with automatic cleanup."""
    async with async_sessionmaker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise  # Re-raise to ensure proper error handling
        finally:
            await session.close()

@app.post("/items/")
async def create_item(
    db: Annotated[AsyncSession, Depends(get_db)],
    item_data: ItemCreate,
):
    """Create item with database session."""
    item = Item(**item_data.dict())
    db.add(item)
    # Session automatically committed or rolled back
    return item
```

### Resource Management with Yield

**REQUIRED**: Resource management pattern:

```python
from typing import Annotated, AsyncGenerator
from fastapi import Depends, FastAPI
from contextlib import asynccontextmanager

app = FastAPI()

async def get_file_handler() -> AsyncGenerator[FileHandler, None]:
    """File handler with proper cleanup."""
    handler = FileHandler()
    try:
        await handler.open()
        yield handler
    finally:
        await handler.close()

@app.post("/upload")
async def upload_file(
    handler: Annotated[FileHandler, Depends(get_file_handler)],
    file: UploadFile,
):
    """Upload file with managed handler."""
    return await handler.save(file)
```

### Exception Handling in Yield Dependencies

**REQUIRED**: Proper exception handling:

```python
from typing import Annotated, AsyncGenerator
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Database session with exception handling."""
    async with async_sessionmaker() as session:
        try:
            yield session
            await session.commit()
        except HTTPException:
            # Re-raise HTTP exceptions immediately
            await session.rollback()
            raise
        except Exception as exc:
            # Log and handle other exceptions
            await session.rollback()
            logger.error(f"Database error: {exc}")
            raise HTTPException(
                status_code=500,
                detail="Database error occurred"
            )
        finally:
            await session.close()
```

### Multiple Yield Dependencies

**RECOMMENDED**: Multiple dependencies with cleanup:

```python
from typing import Annotated, AsyncGenerator
from fastapi import Depends, FastAPI

app = FastAPI()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Database session."""
    async with async_sessionmaker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def get_cache() -> AsyncGenerator[Redis, None]:
    """Cache connection."""
    cache = await create_redis_connection()
    try:
        yield cache
    finally:
        await cache.close()

@app.get("/items/{item_id}")
async def get_item(
    db: Annotated[AsyncSession, Depends(get_db)],
    cache: Annotated[Redis, Depends(get_cache)],
    item_id: int,
):
    """Get item with database and cache."""
    # Both dependencies cleaned up properly
    cached = await cache.get(f"item:{item_id}")
    if cached:
        return cached
    
    item = await db.get(Item, item_id)
    await cache.set(f"item:{item_id}", item)
    return item
```

---

## Sub-Dependencies

### Nested Dependencies

**REQUIRED**: Sub-dependencies pattern:

```python
from typing import Annotated, Optional
from fastapi import Depends, FastAPI, Cookie

app = FastAPI()

def query_extractor(q: Optional[str] = None) -> Optional[str]:
    """Extract query parameter."""
    return q

async def query_or_cookie_extractor(
    q: Annotated[Optional[str], Depends(query_extractor)],
    last_query: Optional[str] = Cookie(None),
) -> str:
    """Extract from query or cookie (sub-dependency)."""
    if not q:
        return last_query or ""
    return q

@app.get("/items/")
async def read_items(
    query: Annotated[str, Depends(query_or_cookie_extractor)]
):
    """Read items with nested dependency."""
    return {"query": query}
```

### Dependency Chain

**RECOMMENDED**: Dependency chain pattern:

```python
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status

app = FastAPI()

async def get_db() -> AsyncSession:
    """Get database session."""
    return await create_session()

async def get_user_repository(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> UserRepository:
    """Get user repository (depends on db)."""
    return UserRepository(db)

async def get_user_service(
    repo: Annotated[UserRepository, Depends(get_user_repository)]
) -> UserService:
    """Get user service (depends on repository)."""
    return UserService(repo)

@app.get("/users/{user_id}")
async def get_user(
    service: Annotated[UserService, Depends(get_user_service)],
    user_id: int,
):
    """Get user (depends on service)."""
    return await service.get_user(user_id)
```

### Conditional Sub-Dependencies

**RECOMMENDED**: Conditional dependencies:

```python
from typing import Annotated, Optional
from fastapi import Depends, FastAPI, Header

app = FastAPI()

def get_api_key(
    x_api_key: Optional[str] = Header(None)
) -> Optional[str]:
    """Extract API key."""
    return x_api_key

async def get_authenticated_user(
    api_key: Annotated[Optional[str], Depends(get_api_key)]
) -> Optional[User]:
    """Get authenticated user if API key provided."""
    if not api_key:
        return None
    return await validate_api_key(api_key)

@app.get("/items/")
async def read_items(
    user: Annotated[Optional[User], Depends(get_authenticated_user)]
):
    """Read items (optional authentication)."""
    if user:
        return {"items": await get_user_items(user.id)}
    return {"items": await get_public_items()}
```

---

## Dependency Caching

### Default Caching Behavior

**REQUIRED**: Understand dependency caching:

```python
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

def get_value():
    """Dependency that returns a value."""
    print("get_value called")
    return "some_value"

@app.get("/item1")
async def read_item1(
    value: Annotated[str, Depends(get_value)]
):
    """First endpoint."""
    return {"value": value}

@app.get("/item2")
async def read_item2(
    value: Annotated[str, Depends(get_value)]
):
    """Second endpoint (uses cached value)."""
    return {"value": value}

# If both endpoints called in same request:
# get_value called only once (cached)
```

### Disabling Cache

**REQUIRED**: Disable caching when needed:

```python
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

def get_fresh_value():
    """Dependency that should be called every time."""
    return str(uuid.uuid4())

@app.get("/item")
async def read_item(
    fresh_value: Annotated[
        str,
        Depends(get_fresh_value, use_cache=False)
    ]
):
    """Endpoint with non-cached dependency."""
    return {"value": fresh_value}
    # get_fresh_value called every time, even if used multiple times
```

### Cache Scope

**REQUIRED**: Cache is per-request:

```python
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

call_count = 0

def get_counter():
    """Counter dependency."""
    global call_count
    call_count += 1
    return call_count

@app.get("/item")
async def read_item(
    counter1: Annotated[int, Depends(get_counter)],
    counter2: Annotated[int, Depends(get_counter)],
):
    """Endpoint with cached counter."""
    return {"counter1": counter1, "counter2": counter2}
    # Both counter1 and counter2 are 1 (cached within request)
    # Next request: both are 2
```

---

## Class-Based Dependencies

### Class Dependency

**REQUIRED**: Class-based dependency:

```python
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

class CommonQueryParams:
    """Common query parameters class."""
    
    def __init__(
        self,
        q: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/items/")
async def read_items(
    commons: Annotated[CommonQueryParams, Depends()]
):
    """Read items with class dependency."""
    return {
        "items": [],
        "query": commons.q,
        "skip": commons.skip,
        "limit": commons.limit,
    }
```

### Class with Methods

**RECOMMENDED**: Class dependency with methods:

```python
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

class PaginationParams:
    """Pagination parameters."""
    
    def __init__(self, skip: int = 0, limit: int = 100):
        self.skip = skip
        self.limit = limit
    
    def to_sqlalchemy(self):
        """Convert to SQLAlchemy pagination."""
        return {"offset": self.skip, "limit": self.limit}
    
    def to_dict(self):
        """Convert to dictionary."""
        return {"skip": self.skip, "limit": self.limit}

@app.get("/items/")
async def read_items(
    pagination: Annotated[PaginationParams, Depends()]
):
    """Read items with pagination."""
    return {
        "items": [],
        "pagination": pagination.to_dict(),
    }
```

---

## Dependency Overrides

### Testing with Overrides

**REQUIRED**: Override dependencies for testing:

```python
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

def get_database():
    """Production database dependency."""
    return get_production_db()

@app.get("/items/")
async def read_items(db = Depends(get_database)):
    """Read items endpoint."""
    return db.get_items()

# Test with dependency override
def get_test_database():
    """Test database dependency."""
    return get_test_db()

# Override dependency
app.dependency_overrides[get_database] = get_test_database

client = TestClient(app)

def test_read_items():
    """Test with overridden dependency."""
    response = client.get("/items/")
    assert response.status_code == 200
    # Uses test database, not production

# Cleanup
def teardown():
    """Cleanup after tests."""
    app.dependency_overrides.clear()
```

### Multiple Overrides

**RECOMMENDED**: Override multiple dependencies:

```python
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

def get_db():
    return get_production_db()

def get_cache():
    return get_production_cache()

@app.get("/items/")
async def read_items(
    db = Depends(get_db),
    cache = Depends(get_cache),
):
    return {"items": []}

# Override multiple dependencies
app.dependency_overrides[get_db] = get_test_db
app.dependency_overrides[get_cache] = get_test_cache

client = TestClient(app)

def test_read_items():
    """Test with multiple overrides."""
    response = client.get("/items/")
    assert response.status_code == 200
```

### Context Manager for Overrides

**RECOMMENDED**: Use context manager for overrides:

```python
from contextlib import contextmanager
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@contextmanager
def override_dependencies(**overrides):
    """Context manager for dependency overrides."""
    original_overrides = app.dependency_overrides.copy()
    app.dependency_overrides.update(overrides)
    try:
        yield
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(original_overrides)

def test_with_overrides():
    """Test with context manager."""
    with override_dependencies(
        get_db=get_test_db,
        get_cache=get_test_cache,
    ):
        client = TestClient(app)
        response = client.get("/items/")
        assert response.status_code == 200
```

---

## Global Dependencies

### Application-Level Dependencies

**REQUIRED**: Global dependencies for all endpoints:

```python
from fastapi import Depends, FastAPI

app = FastAPI(
    dependencies=[
        Depends(verify_token),
        Depends(verify_key),
    ]
)

@app.get("/users/")
async def read_users():
    """All endpoints require token and key."""
    return [{"username": "rick"}]

@app.get("/items/")
async def read_items():
    """All endpoints require token and key."""
    return [{"item": "portal gun"}]
```

### Router-Level Dependencies

**REQUIRED**: Dependencies for router:

```python
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/api/v1",
    dependencies=[Depends(verify_token)],
)

@router.get("/users/")
async def read_users():
    """Requires token (from router)."""
    return [{"username": "rick"}]

@router.get("/items/")
async def read_items():
    """Requires token (from router)."""
    return [{"item": "portal gun"}]
```

### Endpoint-Level Override

**REQUIRED**: Override global dependencies:

```python
from fastapi import Depends, FastAPI

app = FastAPI(
    dependencies=[Depends(verify_token)],
)

@app.get("/public/", dependencies=[])
async def public_endpoint():
    """Public endpoint (no token required)."""
    return {"message": "public"}

@app.get("/private/")
async def private_endpoint():
    """Private endpoint (token required)."""
    return {"message": "private"}
```

---

## Advanced Patterns

### Dependency Factory

**RECOMMENDED**: Factory pattern for dependencies:

```python
from typing import Annotated, Callable
from fastapi import Depends, FastAPI

app = FastAPI()

def create_user_service_factory(
    db_url: str,
    cache_url: str,
) -> Callable[[], UserService]:
    """Create user service factory."""
    def get_user_service() -> UserService:
        db = create_db_connection(db_url)
        cache = create_cache_connection(cache_url)
        return UserService(db, cache)
    return get_user_service

# Register factory
get_user_service = create_user_service_factory(
    db_url="postgresql://...",
    cache_url="redis://...",
)

@app.get("/users/")
async def read_users(
    service: Annotated[UserService, Depends(get_user_service)]
):
    """Read users with factory-created service."""
    return await service.get_all_users()
```

### Conditional Dependency

**RECOMMENDED**: Conditional dependency based on request:

```python
from typing import Annotated, Optional
from fastapi import Depends, FastAPI, Request

app = FastAPI()

async def get_user_optional(request: Request) -> Optional[User]:
    """Get user if authenticated."""
    token = request.headers.get("Authorization")
    if not token:
        return None
    return await validate_token(token)

async def get_user_required(
    user: Annotated[Optional[User], Depends(get_user_optional)]
) -> User:
    """Get user (required)."""
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

@app.get("/public/")
async def public_endpoint(
    user: Annotated[Optional[User], Depends(get_user_optional)]
):
    """Public endpoint (optional user)."""
    return {"user": user}

@app.get("/private/")
async def private_endpoint(
    user: Annotated[User, Depends(get_user_required)]
):
    """Private endpoint (required user)."""
    return {"user": user}
```

### Dependency with State

**RECOMMENDED**: Dependency that uses application state:

```python
from typing import Annotated
from fastapi import Depends, FastAPI, Request

app = FastAPI()

async def get_plugin_framework(request: Request) -> PluginFramework:
    """Get plugin framework from application state."""
    framework = getattr(request.app.state, "plugin_framework", None)
    if not framework:
        raise HTTPException(
            status_code=503,
            detail="Plugin framework not available"
        )
    return framework

@app.get("/plugins/")
async def list_plugins(
    framework: Annotated[PluginFramework, Depends(get_plugin_framework)]
):
    """List plugins."""
    return framework.list_plugins()
```

---

## Testing Dependencies

### Unit Testing Dependencies

**REQUIRED**: Test dependencies independently:

```python
import pytest
from fastapi import Depends

def get_value() -> str:
    """Simple dependency."""
    return "test_value"

def test_dependency():
    """Test dependency function."""
    value = get_value()
    assert value == "test_value"
```

### Integration Testing with Overrides

**REQUIRED**: Test endpoints with dependency overrides:

```python
import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

def get_db():
    return get_production_db()

@app.get("/items/")
async def read_items(db = Depends(get_db)):
    return db.get_items()

@pytest.fixture
def test_client():
    """Test client with overrides."""
    app.dependency_overrides[get_db] = get_test_db
    yield TestClient(app)
    app.dependency_overrides.clear()

def test_read_items(test_client):
    """Test endpoint with overridden dependency."""
    response = test_client.get("/items/")
    assert response.status_code == 200
```

### Testing Yield Dependencies

**REQUIRED**: Test dependencies with yield:

```python
import pytest
from typing import AsyncGenerator
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

async def get_db() -> AsyncGenerator[Session, None]:
    """Database session dependency."""
    session = create_session()
    try:
        yield session
    finally:
        session.close()

@app.get("/items/")
async def read_items(db = Depends(get_db)):
    return db.query(Item).all()

def test_yield_dependency():
    """Test yield dependency."""
    # Test that cleanup happens
    with TestClient(app) as client:
        response = client.get("/items/")
        assert response.status_code == 200
    # Session should be closed
```

---

## Production Deployment

### Dependency Organization

**REQUIRED**: Organize dependencies in modules:

```python
# app/dependencies/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(
    token: str = Depends(oauth2_scheme)
) -> User:
    """Get current authenticated user."""
    user = await validate_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return user

# app/dependencies/database.py
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session."""
    async with async_sessionmaker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

### Performance Considerations

**REQUIRED**: Optimize dependency performance:

```python
from functools import lru_cache
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

# Cache expensive dependency
@lru_cache()
def get_settings() -> Settings:
    """Cached settings (singleton)."""
    return Settings()

# Use async for I/O-bound dependencies
async def get_user_from_db(user_id: int) -> User:
    """Async database lookup."""
    return await db.get(User, user_id)

# Avoid heavy computation in dependencies
def get_expensive_computation():
    """BAD: Heavy computation in dependency."""
    return expensive_calculation()  # Don't do this

# Use background tasks instead
from fastapi import BackgroundTasks

async def process_data(
    background_tasks: BackgroundTasks,
    data: Data,
):
    """Use background tasks for heavy work."""
    background_tasks.add_task(expensive_calculation, data)
    return {"status": "processing"}
```

### Error Handling

**REQUIRED**: Proper error handling in dependencies:

```python
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
import logging

logger = logging.getLogger(__name__)

async def get_database():
    """Database dependency with error handling."""
    try:
        db = await create_connection()
        yield db
    except ConnectionError as exc:
        logger.error(f"Database connection error: {exc}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable"
        )
    except Exception as exc:
        logger.error(f"Unexpected database error: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    finally:
        if 'db' in locals():
            await db.close()
```

---

## Summary

### Key Takeaways

1. **Use Annotated**: Prefer `Annotated` for type hints (Python 3.9+)
2. **Yield for Cleanup**: Always use `yield` for resources requiring cleanup
3. **Proper Scopes**: Choose appropriate scopes (function, request, application)
4. **Exception Handling**: Re-raise exceptions in yield dependencies
5. **Dependency Overrides**: Use overrides for testing
6. **Global Dependencies**: Apply dependencies at app/router level when appropriate
7. **Sub-Dependencies**: Build dependency chains for complex scenarios
8. **Caching**: Understand and control dependency caching
9. **Organization**: Organize dependencies in separate modules
10. **Performance**: Optimize dependencies for production

### Resources

- [FastAPI Dependencies Documentation](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [FastAPI Dependency Scopes](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/)
- [FastAPI Sub-Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/)

---

**Version**: v1.0.0  
**Last Updated**: 2025-01-14
