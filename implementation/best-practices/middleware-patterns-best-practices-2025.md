# Middleware Patterns Best Practices

**Version**: v1.0.0  
**Last Updated**: 2025-01-14

This document provides comprehensive best practices for implementing middleware in FastAPI applications, covering BaseHTTPMiddleware patterns, middleware execution order, CORS middleware, security middleware (TrustedHost, HTTPS redirect, security headers), logging middleware, authentication middleware, performance middleware (timing, compression), error handling middleware, custom middleware patterns, middleware testing, and production deployment.

---

## Table of Contents

1. [Architecture Principles](#architecture-principles)
2. [BaseHTTPMiddleware Patterns](#basehttpmiddleware-patterns)
3. [Middleware Execution Order](#middleware-execution-order)
4. [CORS Middleware](#cors-middleware)
5. [Security Middleware](#security-middleware)
6. [Logging Middleware](#logging-middleware)
7. [Authentication Middleware](#authentication-middleware)
8. [Performance Middleware](#performance-middleware)
9. [Error Handling Middleware](#error-handling-middleware)
10. [Custom Middleware Patterns](#custom-middleware-patterns)
11. [Middleware Testing](#middleware-testing)
12. [Production Deployment](#production-deployment)

---

## Architecture Principles

### Middleware Philosophy

**REQUIRED**: Understand middleware principles:

1. **Request Processing Pipeline**: Middleware executes in a stack (LIFO - Last In, First Out)
2. **Request Phase**: Code before `await call_next(request)` runs on request
3. **Response Phase**: Code after `await call_next(request)` runs on response
4. **Error Handling**: Middleware can catch and handle errors
5. **State Management**: Use `request.state` for request-scoped data
6. **Performance**: Keep middleware lightweight and efficient
7. **Ordering**: Middleware order matters - add in reverse execution order

### When to Use Middleware

**REQUIRED**: Use middleware for:

- **Cross-cutting concerns**: Logging, authentication, CORS, security headers
- **Request/response transformation**: Adding headers, modifying responses
- **Global error handling**: Catching and transforming errors
- **Performance monitoring**: Timing, metrics collection
- **Request validation**: Pre-route validation
- **Feature flags**: Route-level feature control

**Avoid middleware for:**
- **Business logic**: Use route handlers or dependencies
- **Route-specific logic**: Use dependencies or decorators
- **Complex state management**: Use dependencies with yield

---

## BaseHTTPMiddleware Patterns

### Basic Middleware

**REQUIRED**: Basic middleware structure:

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import time

class TimingMiddleware(BaseHTTPMiddleware):
    """Middleware to add process time header."""
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """Process request and add timing header."""
        start_time = time.perf_counter()
        
        # Process request
        response = await call_next(request)
        
        # Add timing header
        process_time = time.perf_counter() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        
        return response

# Add middleware
from fastapi import FastAPI

app = FastAPI()
app.add_middleware(TimingMiddleware)
```

### Middleware with Configuration

**REQUIRED**: Configurable middleware:

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from typing import Optional

class ConfigurableMiddleware(BaseHTTPMiddleware):
    """Middleware with configuration."""
    
    def __init__(self, app, header_name: str = "X-Custom-Header", header_value: str = "default"):
        """Initialize middleware with configuration.
        
        Args:
            app: FastAPI application
            header_name: Name of header to add
            header_value: Value of header
        """
        super().__init__(app)
        self.header_name = header_name
        self.header_value = header_value
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """Process request and add custom header."""
        response = await call_next(request)
        response.headers[self.header_name] = self.header_value
        return response

# Add middleware with configuration
app.add_middleware(
    ConfigurableMiddleware,
    header_name="X-API-Version",
    header_value="1.0.0",
)
```

### Middleware with Request State

**REQUIRED**: Use request state:

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import uuid

class RequestIDMiddleware(BaseHTTPMiddleware):
    """Middleware to add request ID."""
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """Add request ID to request state and response."""
        # Generate request ID
        request_id = str(uuid.uuid4())
        
        # Store in request state
        request.state.request_id = request_id
        
        # Process request
        response = await call_next(request)
        
        # Add to response header
        response.headers["X-Request-ID"] = request_id
        
        return response

# Access request ID in route handlers
@app.get("/items/")
async def read_items(request: Request):
    """Endpoint that uses request ID."""
    request_id = request.state.request_id
    return {"request_id": request_id, "items": []}
```

### Middleware with Path Filtering

**REQUIRED**: Filter middleware by path:

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from typing import List

class SelectiveMiddleware(BaseHTTPMiddleware):
    """Middleware that only applies to specific paths."""
    
    def __init__(self, app, include_paths: Optional[List[str]] = None, exclude_paths: Optional[List[str]] = None):
        """Initialize selective middleware.
        
        Args:
            app: FastAPI application
            include_paths: Paths to include (None = all)
            exclude_paths: Paths to exclude
        """
        super().__init__(app)
        self.include_paths = include_paths or []
        self.exclude_paths = exclude_paths or []
    
    def _should_process(self, path: str) -> bool:
        """Check if path should be processed."""
        # Exclude paths take precedence
        for exclude_path in self.exclude_paths:
            if path.startswith(exclude_path):
                return False
        
        # If include_paths specified, only process those
        if self.include_paths:
            return any(path.startswith(include_path) for include_path in self.include_paths)
        
        # Process all paths
        return True
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """Process request if path matches."""
        if not self._should_process(request.url.path):
            return await call_next(request)
        
        # Process request
        response = await call_next(request)
        response.headers["X-Processed-By"] = "SelectiveMiddleware"
        
        return response

# Add middleware with path filtering
app.add_middleware(
    SelectiveMiddleware,
    include_paths=["/api/"],
    exclude_paths=["/docs", "/redoc", "/openapi.json"],
)
```

---

## Middleware Execution Order

### Understanding Execution Order

**REQUIRED**: Middleware executes in reverse order of addition:

```python
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

class MiddlewareA(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        print("A: Before")
        response = await call_next(request)
        print("A: After")
        return response

class MiddlewareB(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        print("B: Before")
        response = await call_next(request)
        print("B: After")
        return response

class MiddlewareC(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        print("C: Before")
        response = await call_next(request)
        print("C: After")
        return response

# Add middleware in order
app.add_middleware(MiddlewareA)  # Added first
app.add_middleware(MiddlewareB)  # Added second
app.add_middleware(MiddlewareC)  # Added third

# Execution order:
# Request: C: Before -> B: Before -> A: Before -> Handler -> A: After -> B: After -> C: After
# Response: C: After -> B: After -> A: After
```

### Recommended Middleware Order

**REQUIRED**: Recommended middleware order:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app = FastAPI()

# 1. Security middleware (outermost - executes last on request, first on response)
app.add_middleware(HTTPSRedirectMiddleware)  # Redirect HTTP to HTTPS
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["example.com"])  # Validate host

# 2. CORS middleware (early in chain)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Request processing middleware (logging, timing, etc.)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(TimingMiddleware)

# 4. Authentication/authorization middleware (before route handlers)
app.add_middleware(AuthenticationMiddleware)

# 5. Business logic middleware (feature flags, etc.)
app.add_middleware(FeatureFlagMiddleware)

# Execution order on request:
# HTTPSRedirect -> TrustedHost -> CORS -> RequestID -> Timing -> Auth -> FeatureFlag -> Handler

# Execution order on response:
# Handler -> FeatureFlag -> Auth -> Timing -> RequestID -> CORS -> TrustedHost -> HTTPSRedirect
```

### Middleware Order Documentation

**REQUIRED**: Document middleware order:

```python
from fastapi import FastAPI

app = FastAPI()

# Middleware execution order (LIFO - Last In, First Out):
# Request: FeatureFlag -> Auth -> Timing -> CORS -> Security
# Response: Security -> CORS -> Timing -> Auth -> FeatureFlag
#
# Add middleware in REVERSE order of desired execution:
# 1. Security (add last, executes first on request)
# 2. CORS (add second-to-last)
# 3. Timing (add third-to-last)
# 4. Auth (add fourth-to-last)
# 5. FeatureFlag (add first, executes last on request)

# Security middleware
app.add_middleware(HTTPSRedirectMiddleware)

# CORS middleware
app.add_middleware(CORSMiddleware, ...)

# Timing middleware
app.add_middleware(TimingMiddleware)

# Authentication middleware
app.add_middleware(AuthenticationMiddleware)

# Feature flag middleware (add first, executes last before handler)
app.add_middleware(FeatureFlagMiddleware)
```

---

## CORS Middleware

### Basic CORS Configuration

**REQUIRED**: Basic CORS setup:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://example.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

### Advanced CORS Configuration

**REQUIRED**: Advanced CORS configuration:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Get allowed origins from environment
allowed_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:3000,https://example.com"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "X-Request-ID",
    ],
    expose_headers=[
        "X-Request-ID",
        "X-Process-Time",
    ],
    max_age=3600,  # Cache preflight requests for 1 hour
)
```

### CORS with Environment-Based Configuration

**RECOMMENDED**: Environment-based CORS:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings

settings = get_settings()

app = FastAPI()

# Development: Allow all origins
# Production: Restrict to specific origins
if settings.environment == "development":
    allow_origins = ["*"]
else:
    allow_origins = settings.cors_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Security Middleware

### TrustedHost Middleware

**REQUIRED**: TrustedHost middleware:

```python
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.config import get_settings

settings = get_settings()

app = FastAPI()

# Development: Allow all hosts
# Production: Restrict to specific hosts
if settings.environment == "development":
    allowed_hosts = ["*"]
else:
    allowed_hosts = [
        "example.com",
        "www.example.com",
        "api.example.com",
    ]

app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)
```

### HTTPS Redirect Middleware

**REQUIRED**: HTTPS redirect middleware:

```python
from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from app.config import get_settings

settings = get_settings()

app = FastAPI()

# Only redirect in production
if settings.environment == "production":
    app.add_middleware(HTTPSRedirectMiddleware)
```

### Security Headers Middleware

**REQUIRED**: Security headers middleware:

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware to add security headers."""
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """Add security headers to response."""
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        # Content Security Policy
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )
        
        return response

app.add_middleware(SecurityHeadersMiddleware)
```

### Rate Limiting Middleware

**RECOMMENDED**: Rate limiting middleware:

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, Tuple
import time

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware."""
    
    def __init__(self, app, requests_per_minute: int = 60):
        """Initialize rate limiting middleware.
        
        Args:
            app: FastAPI application
            requests_per_minute: Maximum requests per minute per IP
        """
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = defaultdict(list)
    
    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address."""
        # Check X-Forwarded-For header (from proxy)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        # Check X-Real-IP header
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fallback to direct client
        if request.client:
            return request.client.host
        
        return "unknown"
    
    def _is_rate_limited(self, client_ip: str) -> bool:
        """Check if client is rate limited."""
        now = time.time()
        minute_ago = now - 60
        
        # Clean old requests
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if req_time > minute_ago
        ]
        
        # Check limit
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            return True
        
        # Record request
        self.requests[client_ip].append(now)
        return False
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """Check rate limit before processing request."""
        client_ip = self._get_client_ip(request)
        
        if self._is_rate_limited(client_ip):
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Rate limit exceeded",
                    "retry_after": 60,
                },
                headers={
                    "Retry-After": "60",
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                },
            )
        
        response = await call_next(request)
        
        # Add rate limit headers
        remaining = self.requests_per_minute - len(self.requests[client_ip])
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        
        return response

app.add_middleware(RateLimitMiddleware, requests_per_minute=60)
```

---

## Logging Middleware

### Request Logging Middleware

**REQUIRED**: Request logging middleware:

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import logging
import time
import uuid

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for request/response logging."""
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """Log request and response."""
        # Generate request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Log request
        start_time = time.perf_counter()
        logger.info(
            "Request started",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "query_params": str(request.query_params),
                "client_ip": request.client.host if request.client else None,
            },
        )
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate process time
            process_time = time.perf_counter() - start_time
            
            # Log response
            logger.info(
                "Request completed",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "process_time": process_time,
                },
            )
            
            # Add headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
            
        except Exception as exc:
            # Log error
            process_time = time.perf_counter() - start_time
            logger.error(
                "Request failed",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "error": str(exc),
                    "process_time": process_time,
                },
                exc_info=True,
            )
            raise

app.add_middleware(RequestLoggingMiddleware)
```

### Structured Logging Middleware

**RECOMMENDED**: Structured logging with structlog:

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import structlog
import time
import uuid

logger = structlog.get_logger()

class StructuredLoggingMiddleware(BaseHTTPMiddleware):
    """Structured logging middleware."""
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """Log request/response with structured logging."""
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Bind context
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
        )
        
        start_time = time.perf_counter()
        
        logger.info(
            "request_started",
            client_ip=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )
        
        try:
            response = await call_next(request)
            process_time = time.perf_counter() - start_time
            
            logger.info(
                "request_completed",
                status_code=response.status_code,
                process_time=process_time,
            )
            
            response.headers["X-Request-ID"] = request_id
            return response
            
        except Exception as exc:
            process_time = time.perf_counter() - start_time
            logger.error(
                "request_failed",
                error=str(exc),
                process_time=process_time,
                exc_info=True,
            )
            raise

app.add_middleware(StructuredLoggingMiddleware)
```

---

## Authentication Middleware

### Authentication Middleware

**REQUIRED**: Authentication middleware:

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from fastapi import HTTPException, status
from typing import Optional

class AuthenticationMiddleware(BaseHTTPMiddleware):
    """Middleware for authentication."""
    
    def __init__(self, app, exclude_paths: Optional[list] = None):
        """Initialize authentication middleware.
        
        Args:
            app: FastAPI application
            exclude_paths: Paths to exclude from authentication
        """
        super().__init__(app)
        self.exclude_paths = exclude_paths or [
            "/docs",
            "/redoc",
            "/openapi.json",
            "/health",
            "/auth/login",
            "/auth/register",
        ]
    
    def _is_excluded(self, path: str) -> bool:
        """Check if path is excluded from authentication."""
        return any(path.startswith(excluded) for excluded in self.exclude_paths)
    
    async def _authenticate(self, request: Request) -> Optional[dict]:
        """Authenticate request.
        
        Returns:
            User dict if authenticated, None otherwise
        """
        # Extract token from header
        authorization = request.headers.get("Authorization")
        if not authorization:
            return None
        
        # Parse Bearer token
        if not authorization.startswith("Bearer "):
            return None
        
        token = authorization[7:]
        
        # Validate token (implement your token validation)
        user = await validate_token(token)
        return user
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """Authenticate request before processing."""
        # Skip authentication for excluded paths
        if self._is_excluded(request.url.path):
            return await call_next(request)
        
        # Authenticate
        user = await self._authenticate(request)
        
        if not user:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Not authenticated"},
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Store user in request state
        request.state.user = user
        
        # Process request
        response = await call_next(request)
        return response

app.add_middleware(AuthenticationMiddleware)
```

### Authorization Middleware

**RECOMMENDED**: Authorization middleware:

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from fastapi import HTTPException, status
from typing import List, Optional

class AuthorizationMiddleware(BaseHTTPMiddleware):
    """Middleware for authorization."""
    
    def __init__(self, app, role_requirements: Optional[dict] = None):
        """Initialize authorization middleware.
        
        Args:
            app: FastAPI application
            role_requirements: Dict mapping paths to required roles
        """
        super().__init__(app)
        self.role_requirements = role_requirements or {}
    
    def _get_required_roles(self, path: str) -> Optional[List[str]]:
        """Get required roles for path."""
        for pattern, roles in self.role_requirements.items():
            if path.startswith(pattern):
                return roles
        return None
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """Check authorization before processing."""
        # Get user from request state (set by auth middleware)
        user = getattr(request.state, "user", None)
        
        if not user:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Not authenticated"},
            )
        
        # Get required roles for path
        required_roles = self._get_required_roles(request.url.path)
        
        if required_roles:
            user_roles = user.get("roles", [])
            
            # Check if user has required role
            if not any(role in user_roles for role in required_roles):
                return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content={"detail": "Insufficient permissions"},
                )
        
        # Process request
        response = await call_next(request)
        return response

# Configure role requirements
role_requirements = {
    "/admin": ["admin"],
    "/api/users": ["admin", "user_manager"],
    "/api/data": ["admin", "data_viewer"],
}

app.add_middleware(AuthorizationMiddleware, role_requirements=role_requirements)
```

---

## Performance Middleware

### Timing Middleware

**REQUIRED**: Timing middleware:

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import time

class TimingMiddleware(BaseHTTPMiddleware):
    """Middleware to measure request processing time."""
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """Measure and add timing header."""
        start_time = time.perf_counter()
        
        response = await call_next(request)
        
        process_time = time.perf_counter() - start_time
        response.headers["X-Process-Time"] = f"{process_time:.4f}"
        
        return response

app.add_middleware(TimingMiddleware)
```

### Compression Middleware

**RECOMMENDED**: Compression middleware:

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import gzip
from io import BytesIO

class CompressionMiddleware(BaseHTTPMiddleware):
    """Middleware for response compression."""
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """Compress response if client supports it."""
        # Check if client accepts gzip
        accept_encoding = request.headers.get("Accept-Encoding", "")
        supports_gzip = "gzip" in accept_encoding
        
        response = await call_next(request)
        
        # Compress if supported and content type is compressible
        if supports_gzip and self._should_compress(response):
            content = await response.body()
            
            # Compress content
            compressed = gzip.compress(content)
            
            # Create new response
            from starlette.responses import Response as StarletteResponse
            compressed_response = StarletteResponse(
                content=compressed,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type,
            )
            compressed_response.headers["Content-Encoding"] = "gzip"
            compressed_response.headers["Content-Length"] = str(len(compressed))
            
            return compressed_response
        
        return response
    
    def _should_compress(self, response: Response) -> bool:
        """Check if response should be compressed."""
        content_type = response.headers.get("Content-Type", "")
        
        # Don't compress already compressed content
        if response.headers.get("Content-Encoding"):
            return False
        
        # Compress text-based content
        compressible_types = [
            "text/",
            "application/json",
            "application/javascript",
            "application/xml",
        ]
        
        return any(content_type.startswith(ct) for ct in compressible_types)

app.add_middleware(CompressionMiddleware)
```

### Cache Control Middleware

**RECOMMENDED**: Cache control middleware:

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from typing import Dict

class CacheControlMiddleware(BaseHTTPMiddleware):
    """Middleware for cache control headers."""
    
    def __init__(self, app, cache_rules: Optional[Dict[str, str]] = None):
        """Initialize cache control middleware.
        
        Args:
            app: FastAPI application
            cache_rules: Dict mapping path patterns to cache directives
        """
        super().__init__(app)
        self.cache_rules = cache_rules or {
            "/static/": "public, max-age=31536000",  # 1 year
            "/api/public/": "public, max-age=3600",  # 1 hour
            "/api/": "no-cache, no-store, must-revalidate",  # No cache
        }
    
    def _get_cache_directive(self, path: str) -> Optional[str]:
        """Get cache directive for path."""
        for pattern, directive in self.cache_rules.items():
            if path.startswith(pattern):
                return directive
        return None
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """Add cache control headers."""
        response = await call_next(request)
        
        # Only add cache headers for GET requests
        if request.method == "GET":
            cache_directive = self._get_cache_directive(request.url.path)
            if cache_directive:
                response.headers["Cache-Control"] = cache_directive
        
        return response

app.add_middleware(CacheControlMiddleware)
```

---

## Error Handling Middleware

### Global Error Handling Middleware

**REQUIRED**: Global error handling:

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware for global error handling."""
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """Handle errors globally."""
        try:
            response = await call_next(request)
            return response
            
        except HTTPException as exc:
            # FastAPI HTTP exceptions
            logger.warning(
                "HTTP exception",
                extra={
                    "status_code": exc.status_code,
                    "detail": exc.detail,
                    "path": request.url.path,
                },
            )
            return JSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail},
                headers=exc.headers,
            )
            
        except Exception as exc:
            # Unexpected errors
            logger.error(
                "Unexpected error",
                extra={
                    "path": request.url.path,
                    "method": request.method,
                },
                exc_info=True,
            )
            
            # Don't expose internal errors in production
            if settings.environment == "production":
                detail = "Internal server error"
            else:
                detail = str(exc)
            
            return JSONResponse(
                status_code=500,
                content={"detail": detail},
            )

app.add_middleware(ErrorHandlingMiddleware)
```

### Error Transformation Middleware

**RECOMMENDED**: Error transformation:

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from fastapi import HTTPException
from typing import Dict, Type

class ErrorTransformationMiddleware(BaseHTTPMiddleware):
    """Middleware to transform errors."""
    
    def __init__(self, app, error_mappings: Optional[Dict[Type[Exception], dict]] = None):
        """Initialize error transformation middleware.
        
        Args:
            app: FastAPI application
            error_mappings: Dict mapping exception types to error responses
        """
        super().__init__(app)
        self.error_mappings = error_mappings or {}
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """Transform errors before returning."""
        try:
            response = await call_next(request)
            return response
            
        except Exception as exc:
            # Check if we have a mapping for this exception type
            exc_type = type(exc)
            
            if exc_type in self.error_mappings:
                mapping = self.error_mappings[exc_type]
                return JSONResponse(
                    status_code=mapping.get("status_code", 500),
                    content={
                        "detail": mapping.get("detail", str(exc)),
                        "error_code": mapping.get("error_code", "UNKNOWN_ERROR"),
                    },
                )
            
            # Default error handling
            raise

# Configure error mappings
error_mappings = {
    ValueError: {
        "status_code": 400,
        "detail": "Invalid input",
        "error_code": "VALIDATION_ERROR",
    },
    PermissionError: {
        "status_code": 403,
        "detail": "Permission denied",
        "error_code": "PERMISSION_DENIED",
    },
}

app.add_middleware(ErrorTransformationMiddleware, error_mappings=error_mappings)
```

---

## Custom Middleware Patterns

### Feature Flag Middleware

**RECOMMENDED**: Feature flag middleware:

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from fastapi import HTTPException, status

class FeatureFlagMiddleware(BaseHTTPMiddleware):
    """Middleware for feature flag checking."""
    
    def __init__(self, app, feature_flags: Optional[dict] = None):
        """Initialize feature flag middleware.
        
        Args:
            app: FastAPI application
            feature_flags: Dict mapping paths to feature flag names
        """
        super().__init__(app)
        self.feature_flags = feature_flags or {}
    
    async def _is_feature_enabled(self, feature_name: str, request: Request) -> bool:
        """Check if feature is enabled."""
        # Get feature flag manager
        from core.feature_flags.feature_flag_manager import get_feature_flag_manager
        
        manager = get_feature_flag_manager()
        return manager.is_feature_enabled(feature_name)
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """Check feature flags before processing."""
        # Check if path has feature flag requirement
        for path_pattern, feature_name in self.feature_flags.items():
            if request.url.path.startswith(path_pattern):
                if not await self._is_feature_enabled(feature_name, request):
                    raise HTTPException(
                        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        detail=f"Feature '{feature_name}' is not enabled",
                    )
        
        response = await call_next(request)
        return response

app.add_middleware(FeatureFlagMiddleware)
```

### Request Validation Middleware

**RECOMMENDED**: Request validation middleware:

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from fastapi import HTTPException, status
import json

class RequestValidationMiddleware(BaseHTTPMiddleware):
    """Middleware for request validation."""
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """Validate request before processing."""
        # Validate content type for POST/PUT/PATCH
        if request.method in ["POST", "PUT", "PATCH"]:
            content_type = request.headers.get("Content-Type", "")
            
            if not content_type.startswith("application/json"):
                return JSONResponse(
                    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                    content={"detail": "Content-Type must be application/json"},
                )
            
            # Validate JSON body
            try:
                body = await request.body()
                if body:
                    json.loads(body)
            except json.JSONDecodeError:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"detail": "Invalid JSON in request body"},
                )
        
        response = await call_next(request)
        return response

app.add_middleware(RequestValidationMiddleware)
```

### Metrics Middleware

**RECOMMENDED**: Metrics middleware:

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from prometheus_client import Counter, Histogram
import time

# Prometheus metrics
http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status_code"],
)

http_request_duration = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration",
    ["method", "path"],
)

class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware for Prometheus metrics."""
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """Collect metrics."""
        start_time = time.perf_counter()
        
        response = await call_next(request)
        
        process_time = time.perf_counter() - start_time
        
        # Record metrics
        http_requests_total.labels(
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
        ).inc()
        
        http_request_duration.labels(
            method=request.method,
            path=request.url.path,
        ).observe(process_time)
        
        return response

app.add_middleware(MetricsMiddleware)
```

---

## Middleware Testing

### Testing Middleware

**REQUIRED**: Test middleware:

```python
from fastapi.testclient import TestClient
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

app = FastAPI()

class TestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        response.headers["X-Test"] = "test"
        return response

app.add_middleware(TestMiddleware)

@app.get("/test")
async def test_endpoint():
    return {"message": "test"}

def test_middleware():
    """Test middleware."""
    client = TestClient(app)
    
    response = client.get("/test")
    
    assert response.status_code == 200
    assert response.headers["X-Test"] == "test"
    assert response.json() == {"message": "test"}
```

### Testing Middleware Order

**RECOMMENDED**: Test middleware order:

```python
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

app = FastAPI()

class MiddlewareA(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request.state.order = getattr(request.state, "order", [])
        request.state.order.append("A")
        response = await call_next(request)
        request.state.order.append("A")
        return response

class MiddlewareB(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request.state.order = getattr(request.state, "order", [])
        request.state.order.append("B")
        response = await call_next(request)
        request.state.order.append("B")
        return response

app.add_middleware(MiddlewareA)
app.add_middleware(MiddlewareB)

@app.get("/test")
async def test_endpoint(request: Request):
    request.state.order.append("Handler")
    return {"order": request.state.order}

def test_middleware_order():
    """Test middleware execution order."""
    client = TestClient(app)
    
    response = client.get("/test")
    
    # Execution order: B -> A -> Handler -> A -> B
    assert response.json()["order"] == ["B", "A", "Handler", "A", "B"]
```

---

## Production Deployment

### Production Middleware Stack

**REQUIRED**: Production middleware configuration:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from app.config import get_settings

settings = get_settings()
app = FastAPI()

# Production middleware stack (add in reverse execution order)

# 1. Security middleware (outermost)
if settings.environment == "production":
    app.add_middleware(HTTPSRedirectMiddleware)
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.allowed_hosts,
    )

# 2. CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Security headers
app.add_middleware(SecurityHeadersMiddleware)

# 4. Rate limiting
app.add_middleware(RateLimitMiddleware, requests_per_minute=100)

# 5. Request logging
app.add_middleware(RequestLoggingMiddleware)

# 6. Timing
app.add_middleware(TimingMiddleware)

# 7. Authentication (innermost, executes last on request)
app.add_middleware(AuthenticationMiddleware)
```

### Middleware Performance Considerations

**REQUIRED**: Performance best practices:

```python
# 1. Keep middleware lightweight
# Avoid heavy operations in middleware

# 2. Use async operations
# Middleware should be async

# 3. Cache expensive operations
from functools import lru_cache

@lru_cache(maxsize=100)
def expensive_operation(key: str) -> str:
    """Expensive operation with caching."""
    # Expensive computation
    return result

# 4. Skip middleware for excluded paths
class SelectiveMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, exclude_paths: list):
        super().__init__(app)
        self.exclude_paths = set(exclude_paths)
    
    async def dispatch(self, request: Request, call_next) -> Response:
        if request.url.path in self.exclude_paths:
            return await call_next(request)
        # Process request
        return await call_next(request)
```

---

## Summary

### Key Takeaways

1. **BaseHTTPMiddleware**: Use for custom middleware
2. **Execution Order**: Middleware executes in reverse order (LIFO)
3. **Request State**: Use `request.state` for request-scoped data
4. **CORS**: Configure CORS middleware properly
5. **Security**: Add security headers and middleware
6. **Logging**: Implement structured logging middleware
7. **Authentication**: Use middleware for global authentication
8. **Performance**: Keep middleware lightweight
9. **Error Handling**: Handle errors globally
10. **Testing**: Test middleware thoroughly

### Resources

- [FastAPI Middleware Documentation](https://fastapi.tiangolo.com/tutorial/middleware/)
- [Starlette Middleware Documentation](https://www.starlette.io/middleware/)
- [ASGI Middleware Specification](https://asgi.readthedocs.io/en/latest/specs/main.html)

---

**Version**: v1.0.0  
**Last Updated**: 2025-01-14
