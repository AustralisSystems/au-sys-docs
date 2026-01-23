# FastAPI Best Practices 2025
**Version**: v1.0.0
**Last Updated**: 2025-01-14
**FastAPI Version**: 0.118.2+

This document compiles the latest FastAPI best practices based on official documentation, production code examples, and community recommendations for 2025.

---

## Table of Contents

1. [Architecture & Project Structure](#architecture--project-structure)
2. [Dependency Injection](#dependency-injection)
3. [Error Handling](#error-handling)
4. [Security](#security)
5. [Performance & Async Patterns](#performance--async-patterns)
6. [Middleware](#middleware)
7. [Data Validation & Serialization](#data-validation--serialization)
8. [Testing](#testing)
9. [Deployment & Production](#deployment--production)
10. [Documentation](#documentation)

---

## Architecture & Project Structure

### ✅ Best Practices

#### 1. Separation of Concerns
Organize code by functionality to enhance readability and maintainability:

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization
│   ├── config.py            # Configuration management
│   ├── models/              # Database models
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── __init__.py
│   │   └── user.py
│   ├── routers/             # API route handlers
│   │   ├── __init__.py
│   │   └── users.py
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   └── user_service.py
│   ├── dependencies/        # Shared dependencies
│   │   ├── __init__.py
│   │   └── database.py
│   └── core/                # Core utilities
│       ├── __init__.py
│       └── exceptions.py
├── tests/
├── requirements.txt
└── README.md
```

#### 2. Application Initialization with Lifespan

Use `lifespan` context manager for startup and shutdown logic:

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await initialize_database()
    await initialize_services()
    yield
    # Shutdown
    await cleanup_resources()

app = FastAPI(
    title="My API",
    version="1.0.0",
    lifespan=lifespan,
)
```

**Benefits:**
- Clean resource management
- Proper async initialization
- Guaranteed cleanup on shutdown

#### 3. Use APIRouter for Modular Routes

```python
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1", tags=["users"])

@router.get("/users/")
async def get_users():
    return {"users": []}

# In main.py
app.include_router(router)
```

---

## Dependency Injection

### ✅ Best Practices

#### 1. Use `Annotated` for Type Hints (Python 3.9+)

**Recommended (Python 3.9+):**
```python
from typing import Annotated
from fastapi import Depends, FastAPI

async def common_parameters(
    q: str | None = None,
    skip: int = 0,
    limit: int = 100
):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(
    commons: Annotated[dict, Depends(common_parameters)]
):
    return commons
```

**Alternative (Python 3.8):**
```python
from typing_extensions import Annotated
# ... rest same as above
```

#### 2. Database Session Management with Yield

**Critical:** Always use `yield` for database sessions and handle exceptions properly:

```python
from typing import Annotated, AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_sessionmaker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise  # Re-raise to ensure proper error handling
        finally:
            await session.close()

@app.get("/users/")
async def get_users(
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # Use db session
    return {"users": []}
```

**⚠️ Important:** Always re-raise exceptions in yield dependencies to prevent memory leaks and ensure proper error logging.

#### 3. Dependency Caching

FastAPI caches dependencies by default within a request. Disable if needed:

```python
from fastapi import Security

# Disable caching for this dependency
current_user = Security(get_current_user, use_cache=False)
```

#### 4. Class-based Dependencies

```python
from typing import Annotated
from fastapi import Depends

class CommonQueryParams:
    def __init__(
        self,
        q: str | None = None,
        skip: int = 0,
        limit: int = 100
    ):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/items/")
async def read_items(
    commons: Annotated[CommonQueryParams, Depends()]
):
    return commons
```

#### 5. Shared Dependencies

Create reusable dependencies for common operations:

```python
# dependencies/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
):
    # Validate token and return user
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
```

---

## Error Handling

### ✅ Best Practices

#### 1. Custom Exception Handlers

```python
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "body": exc.body
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.status_code,
                "message": exc.detail
            }
        }
    )

@app.exception_handler(Exception)
async def generic_exception_handler(
    request: Request,
    exc: Exception
):
    # Log exception with traceback
    logger.error(f"Unhandled error: {exc}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "error_id": str(uuid.uuid4())  # For tracking
        }
    )
```

#### 2. Custom Exception Classes

```python
from fastapi import HTTPException, status

class NotFoundError(HTTPException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

class ValidationError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )

# Usage
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    item = await get_item_from_db(item_id)
    if not item:
        raise NotFoundError(f"Item {item_id} not found")
    return item
```

#### 3. Error Response Models

```python
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    error: dict
    detail: str
    error_id: str | None = None

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    error_id = str(uuid.uuid4())
    logger.error(f"Error ID: {error_id}, Error: {exc}", exc_info=True)

    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error={"code": 500, "message": "Internal server error"},
            detail=str(exc),
            error_id=error_id
        ).model_dump()
    )
```

---

## Security

### ✅ Best Practices

#### 1. OAuth2 with Password Flow

```python
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
):
    # Validate token
    user = await validate_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user
```

#### 2. OAuth2 Scopes

```python
from fastapi import Security, SecurityScopes

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={
        "me": "Read information about the current user.",
        "items": "Read items."
    }
)

async def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)]
):
    # Validate token and check scopes
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    # Validate scopes
    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user

@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["items"])]
):
    return [{"item_id": "Foo", "owner": current_user.username}]
```

#### 3. API Key Authentication

```python
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import APIKeyHeader

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def verify_api_key(
    api_key: str | None = Depends(api_key_header)
):
    if api_key != "secret-api-key":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )
    return api_key

@app.get("/protected/")
async def protected_route(api_key: str = Depends(verify_api_key)):
    return {"message": "Access granted"}
```

#### 4. Environment Variables for Secrets

**Never hardcode secrets:**

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    database_url: str
    api_key: str

    class Config:
        env_file = ".env"

settings = Settings()
```

#### 5. HTTPS in Production

Always use HTTPS in production. Configure reverse proxy (nginx, Traefik) to handle SSL/TLS.

---

## Performance & Async Patterns

### ✅ Best Practices

#### 1. Use Async/Await for I/O Operations

```python
# ✅ Good: Async database operations
async def get_users():
    async with async_sessionmaker() as session:
        result = await session.execute(select(User))
        return result.scalars().all()

# ❌ Bad: Blocking operations
def get_users():
    with sessionmaker() as session:  # Blocking!
        result = session.execute(select(User))
        return result.scalars().all()
```

#### 2. Background Tasks

```python
from fastapi import BackgroundTasks

def write_log(message: str):
    with open("log.txt", "a") as f:
        f.write(message)

@app.post("/send-notification/{email}")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(write_log, f"Notification sent to {email}")
    return {"message": "Notification sent"}
```

#### 3. Connection Pooling

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before using
    echo=False
)

async_sessionmaker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)
```

#### 4. Caching Strategies

```python
from functools import lru_cache
from fastapi import Depends

@lru_cache()
def get_settings():
    return Settings()

# Or use Redis for distributed caching
from redis import asyncio as aioredis

redis_client = None

async def get_redis():
    global redis_client
    if redis_client is None:
        redis_client = await aioredis.from_url("redis://localhost")
    return redis_client

@app.get("/cached-data/{key}")
async def get_cached_data(
    key: str,
    redis: aioredis.Redis = Depends(get_redis)
):
    cached = await redis.get(key)
    if cached:
        return json.loads(cached)
    # Fetch and cache
    data = await fetch_data(key)
    await redis.setex(key, 3600, json.dumps(data))
    return data
```

---

## Middleware

### ✅ Best Practices

#### 1. Middleware Order Matters

**Execution order is REVERSE of addition order:**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI()

# Execution order: Security → CORS → Custom
app.add_middleware(CORSMiddleware, allow_origins=["*"])
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["example.com"])

@app.middleware("http")
async def custom_middleware(request: Request, call_next):
    # This executes FIRST (last added)
    response = await call_next(request)
    return response
```

#### 2. CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],  # Never use ["*"] in production
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count"],
)
```

#### 3. Custom Middleware

```python
from fastapi import Request
import time

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

#### 4. Security Headers Middleware

```python
@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response
```

---

## Data Validation & Serialization

### ✅ Best Practices

#### 1. Use Pydantic Models

```python
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2

@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate):
    # FastAPI automatically validates user data
    db_user = await create_user_in_db(user)
    return db_user
```

#### 2. Response Models

Always define response models for better API documentation:

```python
@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    return await get_user_from_db(user_id)
```

#### 3. Field Validation

```python
from pydantic import BaseModel, Field, validator

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0, description="Price must be positive")
    quantity: int = Field(..., ge=0)

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()
```

---

## Testing

### ✅ Best Practices

#### 1. TestClient for Integration Tests

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_user():
    response = client.post(
        "/users/",
        json={"email": "test@example.com", "username": "testuser"}
    )
    assert response.status_code == 201
```

#### 2. Async Testing

```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_read_users():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/users/")
    assert response.status_code == 200
```

#### 3. Dependency Overrides

```python
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_db

def override_get_db():
    # Return test database session
    return test_db_session

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
```

---

## Deployment & Production

### ✅ Best Practices

#### 1. Use Production ASGI Server

```bash
# Use Uvicorn with multiple workers
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Or Gunicorn with Uvicorn workers
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### 2. Environment Configuration

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    environment: str = "development"
    debug: bool = False
    database_url: str
    secret_key: str

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
```

#### 3. Health Check Endpoint

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }
```

#### 4. Logging Configuration

```python
import logging
from logging.config import dictConfig

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["default"],
    },
}

dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
```

#### 5. Docker Configuration

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Documentation

### ✅ Best Practices

#### 1. OpenAPI Configuration

```python
app = FastAPI(
    title="My API",
    description="Comprehensive API documentation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    openapi_tags=[
        {
            "name": "users",
            "description": "User management operations",
        },
    ],
)
```

#### 2. Route Documentation

```python
@app.post(
    "/users/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user with email and username",
    response_description="The created user",
    tags=["users"]
)
async def create_user(user: UserCreate):
    """Create a new user in the system."""
    return await create_user_in_db(user)
```

#### 3. Response Examples

```python
from fastapi.responses import JSONResponse

@app.get(
    "/users/{user_id}",
    responses={
        200: {
            "description": "User found",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "email": "user@example.com",
                        "username": "user"
                    }
                }
            }
        },
        404: {"description": "User not found"}
    }
)
async def get_user(user_id: int):
    return await get_user_from_db(user_id)
```

---

## Summary Checklist

### Architecture
- [ ] Organized by functionality (models, schemas, routers, services)
- [ ] Used APIRouter for modular routes
- [ ] Implemented lifespan for startup/shutdown

### Dependency Injection
- [ ] Used `Annotated` for type hints (Python 3.9+)
- [ ] Proper database session management with yield
- [ ] Re-raise exceptions in yield dependencies
- [ ] Created reusable shared dependencies

### Error Handling
- [ ] Custom exception handlers registered
- [ ] Consistent error response format
- [ ] Proper logging of errors

### Security
- [ ] OAuth2 or API key authentication
- [ ] Environment variables for secrets
- [ ] HTTPS in production
- [ ] CORS properly configured
- [ ] Security headers middleware

### Performance
- [ ] Async/await for I/O operations
- [ ] Connection pooling configured
- [ ] Background tasks for long operations
- [ ] Caching strategy implemented

### Testing
- [ ] Integration tests with TestClient
- [ ] Dependency overrides for testing
- [ ] Async test support

### Deployment
- [ ] Production ASGI server configured
- [ ] Environment-based configuration
- [ ] Health check endpoint
- [ ] Proper logging configuration
- [ ] Docker containerization

### Documentation
- [ ] OpenAPI configuration
- [ ] Route documentation with descriptions
- [ ] Response examples provided

---

## References

- [Official FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FastAPI GitHub Repository](https://github.com/tiangolo/fastapi)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [SQLAlchemy Async Documentation](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)

---

**Note:** This document is based on FastAPI 0.118.2+ and Python 3.9+. Always refer to the official documentation for the most up-to-date information.
