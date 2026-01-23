# Authentication & Authorization: Multi-Strategy Best Practices

**Version**: v1.0.0
**Last Updated**: 2025-01-14

This document provides comprehensive best practices for implementing multi-strategy authentication and authorization in FastAPI applications, covering JWT, OAuth2, Auth0, and API Keys.

---

## Table of Contents

1. [Architecture Principles](#architecture-principles)
2. [JWT Authentication](#jwt-authentication)
3. [OAuth2 Authentication](#oauth2-authentication)
4. [Auth0 Integration](#auth0-integration)
5. [API Key Authentication](#api-key-authentication)
6. [Multi-Strategy Authentication](#multi-strategy-authentication)
7. [Authorization Patterns](#authorization-patterns)
8. [Security Best Practices](#security-best-practices)
9. [FastAPI Integration](#fastapi-integration)
10. [Testing Strategies](#testing-strategies)
11. [Performance Considerations](#performance-considerations)

---

## Architecture Principles

### 1. Separation of Concerns

**Authentication vs Authorization:**
- **Authentication**: Verifying who the user is (identity verification)
- **Authorization**: Determining what the user can do (permission checking)

```python
# Good: Separate authentication and authorization
class AuthenticationManager:
    """Handles ONLY authentication concerns."""
    async def authenticate(self, credentials: str) -> AuthResult:
        # Verify identity only
        pass

class AuthorizationManager:
    """Handles ONLY authorization concerns."""
    async def authorize(self, user: User, resource: str, action: str) -> bool:
        # Check permissions only
        pass
```

### 2. Strategy Pattern for Multiple Auth Methods

Use the Strategy pattern to support multiple authentication methods:

```python
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional

class AuthenticationMethod(str, Enum):
    """Supported authentication methods."""
    JWT = "jwt"
    OAUTH2 = "oauth2"
    AUTH0 = "auth0"
    API_KEY = "api_key"
    BASIC = "basic"

class IAuthenticationStrategy(ABC):
    """Abstract authentication strategy interface."""

    @abstractmethod
    async def authenticate(self, credentials: str) -> Optional[AuthResult]:
        """Authenticate using this strategy."""
        pass

    @abstractmethod
    def get_method(self) -> AuthenticationMethod:
        """Return the authentication method this strategy handles."""
        pass

class AuthenticationManager:
    """Unified authentication manager supporting multiple strategies."""

    def __init__(self):
        self._strategies: dict[AuthenticationMethod, IAuthenticationStrategy] = {}

    def register_strategy(self, strategy: IAuthenticationStrategy):
        """Register an authentication strategy."""
        self._strategies[strategy.get_method()] = strategy

    async def authenticate(
        self,
        credentials: str,
        method: AuthenticationMethod
    ) -> Optional[AuthResult]:
        """Authenticate using the specified method."""
        strategy = self._strategies.get(method)
        if not strategy:
            raise ValueError(f"Unsupported authentication method: {method}")
        return await strategy.authenticate(credentials)
```

### 3. Dependency Injection

Use FastAPI's dependency injection system for clean, testable authentication:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Dependency to get current authenticated user."""
    # Validate token and return user
    pass

@app.get("/protected")
async def protected_route(user: User = Depends(get_current_user)):
    """Protected route using dependency injection."""
    return {"user": user.email}
```

---

## JWT Authentication

### 1. Token Generation

**Best Practices:**
- Use strong secret keys (minimum 32 bytes, preferably 64+)
- Set appropriate expiration times (15-60 minutes for access tokens)
- Include standard claims (`sub`, `exp`, `iat`, `iss`, `aud`)
- Use secure algorithms (HS256 for symmetric, RS256 for asymmetric)

```python
from datetime import datetime, timedelta, timezone
from jose import jwt
import secrets

# Generate secure secret key
SECRET_KEY = secrets.token_urlsafe(64)  # 64 bytes = 86 characters
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token with proper claims."""
    to_encode = data.copy()

    # Set expiration
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Standard claims
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "iss": "your-api",
        "aud": "your-audience",
        "sub": data.get("sub"),  # Subject (user ID)
    })

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

### 2. Token Validation

**Best Practices:**
- Always validate signature
- Check expiration (`exp`)
- Verify issuer (`iss`) and audience (`aud`)
- Validate subject (`sub`)
- Handle all JWT exceptions properly

```python
from jose import jwt, JWTError, ExpiredSignatureError, JWTClaimsError
from fastapi import HTTPException, status

def verify_token(token: str) -> dict:
    """Verify and decode JWT token with comprehensive validation."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode with full validation
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            audience="your-audience",
            issuer="your-api",
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_aud": True,
                "verify_iss": True,
                "require_exp": True,
                "require_iat": True,
                "leeway": 10  # 10 seconds leeway for clock skew
            }
        )

        # Validate subject
        sub: str = payload.get("sub")
        if sub is None:
            raise credentials_exception

        return payload

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTClaimsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token claims: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise credentials_exception
```

### 3. FastAPI Users Integration

**Best Practices:**
- Use FastAPI Users for JWT authentication
- Configure both Bearer and Cookie transports
- Set appropriate token lifetimes
- Use secure cookie settings

```python
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    CookieTransport,
    JWTStrategy,
)
from fastapi_users import FastAPIUsers

# JWT Strategy
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=SECRET_KEY,
        lifetime_seconds=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        algorithm=ALGORITHM,
    )

# Bearer Transport (for API clients)
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

# Cookie Transport (for web browsers)
cookie_transport = CookieTransport(
    cookie_name="auth_cookie",
    cookie_max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    cookie_secure=True,  # HTTPS only in production
    cookie_httponly=True,  # Prevent XSS
    cookie_samesite="lax",  # CSRF protection
)

# JWT Backend
jwt_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

# Cookie Backend
cookie_backend = AuthenticationBackend(
    name="cookie",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

# FastAPI Users instance
fastapi_users = FastAPIUsers[UserTable, UUID](
    get_user_manager,
    [jwt_backend, cookie_backend],  # Support both transports
)

# Dependencies
current_active_user = fastapi_users.current_user(active=True)
current_verified_user = fastapi_users.current_user(active=True, verified=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
```

### 4. RSA Key Pair (RS256)

For distributed systems, use RS256 with RSA key pairs:

```python
from fastapi_users.authentication import JWTStrategy

# RSA private key (keep secure!)
PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
...
-----END RSA PRIVATE KEY-----"""

# RSA public key (can be shared)
PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
...
-----END PUBLIC KEY-----"""

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=PRIVATE_KEY,
        lifetime_seconds=3600,
        algorithm="RS256",
        public_key=PUBLIC_KEY,
    )
```

---

## OAuth2 Authentication

### 1. OAuth2 Password Flow

**Best Practices:**
- Use OAuth2PasswordBearer for token extraction
- Hash passwords with bcrypt or argon2
- Implement proper password validation
- Support refresh tokens for long-lived sessions

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash password."""
    return pwd_context.hash(password)

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Login endpoint
@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Token:
    """OAuth2 password flow login."""
    # Authenticate user
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")
```

### 2. OAuth2 with FastAPI Users

**Best Practices:**
- Use httpx-oauth for OAuth providers
- Support multiple providers (Google, GitHub, etc.)
- Associate OAuth accounts with existing users by email
- Handle OAuth callbacks securely

```python
from httpx_oauth.clients.google import GoogleOAuth2
from httpx_oauth.clients.github import GitHubOAuth2
from fastapi_users import FastAPIUsers

# OAuth clients
google_oauth_client = GoogleOAuth2(
    settings.oauth_google_client_id,
    settings.oauth_google_client_secret
)

github_oauth_client = GitHubOAuth2(
    settings.oauth_github_client_id,
    settings.oauth_github_client_secret
)

# OAuth routers
app.include_router(
    fastapi_users.get_oauth_router(
        google_oauth_client,
        jwt_backend,
        STATE_SECRET,
        associate_by_email=True,  # Link by email if user exists
        is_verified_by_default=True,  # Trust OAuth provider email verification
    ),
    prefix="/auth/oauth/google",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_oauth_router(
        github_oauth_client,
        jwt_backend,
        STATE_SECRET,
        associate_by_email=True,
        is_verified_by_default=True,
    ),
    prefix="/auth/oauth/github",
    tags=["auth"],
)

# OAuth association router (for linking accounts)
app.include_router(
    fastapi_users.get_oauth_associate_router(
        google_oauth_client,
        jwt_backend,
        STATE_SECRET,
    ),
    prefix="/auth/oauth/google/associate",
    tags=["auth"],
)
```

### 3. OAuth2 Scopes

**Best Practices:**
- Define clear scopes for fine-grained access control
- Validate scopes in authorization checks
- Include scopes in token claims

```python
from fastapi.security import SecurityScopes

# Define scopes
SCOPES = {
    "me": "Read information about the current user",
    "items:read": "Read items",
    "items:write": "Create and update items",
    "admin": "Administrative access",
}

# OAuth2 scheme with scopes
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes=SCOPES,
)

# Dependency with scope checking
async def get_current_user_with_scopes(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
) -> User:
    """Get current user and validate scopes."""
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    payload = verify_token(token)
    user = get_user(payload.get("sub"))

    # Validate scopes
    token_scopes = payload.get("scopes", [])
    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Not enough permissions. Required scope: {scope}",
                headers={"WWW-Authenticate": authenticate_value},
            )

    return user

@app.get("/items/", dependencies=[Depends(get_current_user_with_scopes)])
async def read_items(
    security_scopes: SecurityScopes,
    user: User = Depends(get_current_user_with_scopes),
):
    """Endpoint requiring 'items:read' scope."""
    return {"items": []}
```

---

## Auth0 Integration

### 1. Auth0 Setup

**Best Practices:**
- Use Auth0 Python SDK
- Validate tokens against Auth0 JWKS
- Configure proper audience and issuer
- Handle token refresh

```python
from auth0.authentication import GetToken
from auth0.authentication.token_verifier import TokenVerifier, AsymmetricSignatureVerifier
from fastapi_auth0 import Auth0, Auth0User
from fastapi import Security

# Auth0 configuration
AUTH0_DOMAIN = "your-domain.auth0.com"
AUTH0_AUDIENCE = "your-api-identifier"
AUTH0_CLIENT_ID = "your-client-id"
AUTH0_CLIENT_SECRET = "your-client-secret"

# Auth0 client
auth0 = Auth0(AUTH0_DOMAIN, AUTH0_AUDIENCE)

# Token verifier
jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
issuer = f"https://{AUTH0_DOMAIN}/"

signature_verifier = AsymmetricSignatureVerifier(jwks_url)
token_verifier = TokenVerifier(
    signature_verifier=signature_verifier,
    issuer=issuer,
    audience=AUTH0_AUDIENCE,
)

# Dependency to get Auth0 user
async def get_auth0_user(
    security_scopes: SecurityScopes,
    user: Optional[Auth0User] = Security(auth0.get_user),
) -> Auth0User:
    """Get authenticated Auth0 user."""
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing Auth0 credentials",
        )

    # Validate scopes if required
    if security_scopes.scopes:
        token_scopes = user.permissions or []
        for scope in security_scopes.scopes:
            if scope not in token_scopes:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Not enough permissions. Required scope: {scope}",
                )

    return user

@app.get("/protected")
async def protected_route(user: Auth0User = Depends(get_auth0_user)):
    """Protected route using Auth0 authentication."""
    return {"user_id": user.id, "email": user.email}
```

### 2. Auth0 Management API

**Best Practices:**
- Use Management API for user management
- Cache Management API tokens
- Handle token expiration

```python
from auth0.management import Auth0
from auth0.authentication import GetToken

# Get Management API token
get_token = GetToken(
    AUTH0_DOMAIN,
    AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
)

token_response = get_token.client_credentials(
    f"https://{AUTH0_DOMAIN}/api/v2/"
)
mgmt_api_token = token_response["access_token"]

# Management API client
auth0_management = Auth0(AUTH0_DOMAIN, mgmt_api_token)

# Use Management API
users = auth0_management.users.all()
user = auth0_management.users.get(user_id)
```

---

## API Key Authentication

### 1. API Key Generation

**Best Practices:**
- Use cryptographically secure random generation
- Prefix keys for identification (e.g., `sk_`, `pk_`)
- Hash keys before storage (never store plain keys)
- Include metadata (client_id, permissions, expiration)

```python
import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass
from typing import Optional, Set

@dataclass
class APIKeyInfo:
    """API key information."""
    key_id: str
    client_id: str
    permissions: Set[str]
    created_at: datetime
    expires_at: Optional[datetime] = None
    last_used: Optional[datetime] = None
    usage_count: int = 0
    is_active: bool = True
    key_hash: str = ""

    def is_valid(self) -> bool:
        """Check if API key is valid."""
        if not self.is_active:
            return False
        if self.expires_at and datetime.now(timezone.utc) > self.expires_at:
            return False
        return True

def generate_api_key(client_id: str, prefix: str = "sk_") -> tuple[str, APIKeyInfo]:
    """Generate a new API key."""
    # Generate random part
    random_part = secrets.token_urlsafe(32)
    key_id = secrets.token_hex(8)

    # Create full key
    full_key = f"{prefix}{key_id}_{random_part}"

    # Hash for storage
    key_hash = hashlib.sha256(full_key.encode()).hexdigest()

    # Create key info
    key_info = APIKeyInfo(
        key_id=key_id,
        client_id=client_id,
        permissions=set(),
        created_at=datetime.now(timezone.utc),
        expires_at=datetime.now(timezone.utc) + timedelta(days=365),
        key_hash=key_hash,
    )

    return full_key, key_info
```

### 2. API Key Validation

**Best Practices:**
- Validate key format before hashing
- Check key status (active, expired)
- Record usage for monitoring
- Support key rotation

```python
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(
    api_key: Optional[str] = Security(api_key_header),
) -> APIKeyInfo:
    """Verify API key from header."""
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key",
        )

    # Validate format
    if not api_key.startswith("sk_") or len(api_key.split("_")) < 3:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key format",
        )

    # Hash and lookup
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()
    key_info = await get_api_key_by_hash(key_hash)

    if not key_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    if not key_info.is_valid():
        status_msg = "expired" if key_info.expires_at and datetime.now(timezone.utc) > key_info.expires_at else "inactive"
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"API key is {status_msg}",
        )

    # Record usage
    key_info.record_usage()
    await update_api_key(key_info)

    return key_info

@app.get("/api/data")
async def get_data(key_info: APIKeyInfo = Depends(verify_api_key)):
    """Protected endpoint using API key."""
    return {"data": "protected data", "client_id": key_info.client_id}
```

### 3. Plugin-Based API Key Management

**Best Practices:**
- Use plugin system for extensibility
- Support multiple key stores
- Implement key rotation policies

```python
from fastapi import Request, HTTPException, status

async def require_plugin_api_key(request: Request) -> AuthContext:
    """Validate API key using plugin system."""
    api_key = request.headers.get("X-API-Key")
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-API-Key header",
        )

    # Get auth manager from plugin system
    plugin_framework = request.app.state.plugin_framework
    auth_manager = await plugin_framework.call_plugin_method(
        "security_authentication",
        "get_auth_manager"
    )

    # Authenticate
    context = auth_manager.authenticate(api_key)
    if not context or not context.is_valid():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or inactive API key",
        )

    request.state.auth_context = context
    return context
```

---

## Multi-Strategy Authentication

### 1. Unified Authentication Manager

**Best Practices:**
- Single entry point for all authentication methods
- Strategy pattern for extensibility
- Consistent error handling
- Comprehensive logging

```python
from enum import Enum
from typing import Optional
from abc import ABC, abstractmethod

class AuthenticationMethod(str, Enum):
    """Supported authentication methods."""
    JWT = "jwt"
    OAUTH2 = "oauth2"
    AUTH0 = "auth0"
    API_KEY = "api_key"

class IAuthenticationStrategy(ABC):
    """Authentication strategy interface."""

    @abstractmethod
    async def authenticate(self, credentials: str, request: Request) -> Optional[AuthResult]:
        """Authenticate credentials."""
        pass

    @abstractmethod
    def get_method(self) -> AuthenticationMethod:
        """Return authentication method."""
        pass

    @abstractmethod
    def can_handle(self, request: Request) -> bool:
        """Check if this strategy can handle the request."""
        pass

class UnifiedAuthenticationManager:
    """Unified manager for multiple authentication strategies."""

    def __init__(self):
        self._strategies: list[IAuthenticationStrategy] = []
        self.logger = get_logger("auth.manager")

    def register_strategy(self, strategy: IAuthenticationStrategy):
        """Register authentication strategy."""
        self._strategies.append(strategy)
        self.logger.info(f"Registered authentication strategy: {strategy.get_method()}")

    async def authenticate(self, request: Request) -> Optional[AuthResult]:
        """Try all strategies until one succeeds."""
        for strategy in self._strategies:
            if not strategy.can_handle(request):
                continue

            try:
                credentials = self._extract_credentials(request, strategy.get_method())
                if not credentials:
                    continue

                result = await strategy.authenticate(credentials, request)
                if result and result.success:
                    self.logger.info(
                        f"Authentication successful using {strategy.get_method()}",
                        extra={"client_id": result.client_id}
                    )
                    return result
            except Exception as e:
                self.logger.warning(
                    f"Authentication strategy {strategy.get_method()} failed: {e}"
                )
                continue

        return None

    def _extract_credentials(self, request: Request, method: AuthenticationMethod) -> Optional[str]:
        """Extract credentials based on method."""
        if method == AuthenticationMethod.JWT:
            auth_header = request.headers.get("Authorization", "")
            if auth_header.startswith("Bearer "):
                return auth_header[7:]
        elif method == AuthenticationMethod.API_KEY:
            return request.headers.get("X-API-Key")
        elif method == AuthenticationMethod.AUTH0:
            auth_header = request.headers.get("Authorization", "")
            if auth_header.startswith("Bearer "):
                return auth_header[7:]
        return None

# Dependency for FastAPI
async def get_current_user_unified(
    request: Request,
    auth_manager: UnifiedAuthenticationManager = Depends(get_auth_manager),
) -> User:
    """Unified authentication dependency."""
    auth_result = await auth_manager.authenticate(request)
    if not auth_result or not auth_result.success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await get_user_by_id(auth_result.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user
```

### 2. Priority-Based Strategy Selection

**Best Practices:**
- Define strategy priority
- Try strategies in order
- Cache successful authentication results

```python
class PriorityAuthenticationManager:
    """Authentication manager with priority-based strategy selection."""

    def __init__(self):
        # Ordered by priority (first = highest priority)
        self._strategies: list[tuple[int, IAuthenticationStrategy]] = []

    def register_strategy(self, strategy: IAuthenticationStrategy, priority: int = 100):
        """Register strategy with priority."""
        self._strategies.append((priority, strategy))
        self._strategies.sort(key=lambda x: x[0])  # Sort by priority

    async def authenticate(self, request: Request) -> Optional[AuthResult]:
        """Try strategies in priority order."""
        for priority, strategy in self._strategies:
            if not strategy.can_handle(request):
                continue

            try:
                credentials = self._extract_credentials(request, strategy.get_method())
                if credentials:
                    result = await strategy.authenticate(credentials, request)
                    if result and result.success:
                        return result
            except Exception:
                continue

        return None
```

---

## Authorization Patterns

### 1. Role-Based Access Control (RBAC)

**Best Practices:**
- Define clear role hierarchy
- Check roles at endpoint level
- Support role inheritance
- Cache role checks

```python
from enum import Enum
from typing import List, Set

class Role(str, Enum):
    """User roles."""
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
    GUEST = "guest"

# Role hierarchy (higher = more permissions)
ROLE_HIERARCHY = {
    Role.ADMIN: [Role.ADMIN, Role.MODERATOR, Role.USER, Role.GUEST],
    Role.MODERATOR: [Role.MODERATOR, Role.USER, Role.GUEST],
    Role.USER: [Role.USER, Role.GUEST],
    Role.GUEST: [Role.GUEST],
}

def has_role(user: User, required_role: Role) -> bool:
    """Check if user has required role."""
    user_role = Role(user.role)
    return required_role in ROLE_HIERARCHY.get(user_role, [])

def require_role(required_role: Role):
    """Dependency factory for role-based authorization."""
    async def role_checker(user: User = Depends(get_current_user)) -> User:
        if not has_role(user, required_role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required role: {required_role.value}",
            )
        return user
    return role_checker

@app.get("/admin/users")
async def list_users(user: User = Depends(require_role(Role.ADMIN))):
    """Admin-only endpoint."""
    return {"users": []}
```

### 2. Permission-Based Authorization

**Best Practices:**
- Define granular permissions
- Check permissions at resource level
- Support permission inheritance
- Cache permission checks

```python
from typing import Set

class Permission(str, Enum):
    """Resource permissions."""
    # User permissions
    USER_READ = "user:read"
    USER_WRITE = "user:write"
    USER_DELETE = "user:delete"

    # Item permissions
    ITEM_READ = "item:read"
    ITEM_WRITE = "item:write"
    ITEM_DELETE = "item:delete"

    # Admin permissions
    ADMIN_ALL = "admin:all"

# Role to permissions mapping
ROLE_PERMISSIONS = {
    Role.ADMIN: {
        Permission.ADMIN_ALL,
        Permission.USER_READ,
        Permission.USER_WRITE,
        Permission.USER_DELETE,
        Permission.ITEM_READ,
        Permission.ITEM_WRITE,
        Permission.ITEM_DELETE,
    },
    Role.MODERATOR: {
        Permission.USER_READ,
        Permission.ITEM_READ,
        Permission.ITEM_WRITE,
    },
    Role.USER: {
        Permission.USER_READ,
        Permission.ITEM_READ,
    },
}

def has_permission(user: User, permission: Permission) -> bool:
    """Check if user has permission."""
    user_role = Role(user.role)
    user_permissions = ROLE_PERMISSIONS.get(user_role, set())

    # Admin has all permissions
    if Permission.ADMIN_ALL in user_permissions:
        return True

    return permission in user_permissions

def require_permission(permission: Permission):
    """Dependency factory for permission-based authorization."""
    async def permission_checker(user: User = Depends(get_current_user)) -> User:
        if not has_permission(user, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required: {permission.value}",
            )
        return user
    return permission_checker

@app.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    user: User = Depends(require_permission(Permission.USER_DELETE)),
):
    """Delete user endpoint requiring permission."""
    # Delete user logic
    pass
```

### 3. Policy-Based Authorization

**Best Practices:**
- Define policies as data structures
- Evaluate policies dynamically
- Support complex conditions
- Cache policy evaluations

```python
from dataclasses import dataclass
from typing import Dict, List, Any, Optional

@dataclass
class RBACPolicy:
    """RBAC policy definition."""
    id: str
    name: str
    roles: List[str]
    resource_pattern: str  # e.g., "/users/*"
    actions: List[str]  # e.g., ["GET", "POST"]
    conditions: Optional[Dict[str, Any]] = None
    enabled: bool = True

class PolicyBasedAuthorization:
    """Policy-based authorization engine."""

    def __init__(self):
        self._policies: Dict[str, RBACPolicy] = {}

    def add_policy(self, policy: RBACPolicy):
        """Add authorization policy."""
        self._policies[policy.id] = policy

    async def authorize(
        self,
        user: Optional[User],
        resource: str,
        action: str,
        policy_ids: List[str],
    ) -> bool:
        """Check if user is authorized."""
        for policy_id in policy_ids:
            policy = self._policies.get(policy_id)
            if not policy or not policy.enabled:
                continue

            if self._evaluate_policy(user, resource, action, policy):
                return True

        return False

    def _evaluate_policy(
        self,
        user: Optional[User],
        resource: str,
        action: str,
        policy: RBACPolicy,
    ) -> bool:
        """Evaluate single policy."""
        # Check roles
        if not self._check_roles(user, policy.roles):
            return False

        # Check resource pattern
        if not fnmatch.fnmatch(resource, policy.resource_pattern):
            return False

        # Check actions
        if action.upper() not in [a.upper() for a in policy.actions]:
            return False

        # Check conditions
        if policy.conditions:
            if not self._evaluate_conditions(user, policy.conditions):
                return False

        return True

    def _check_roles(self, user: Optional[User], required_roles: List[str]) -> bool:
        """Check if user has required role."""
        if not user:
            return "anonymous" in required_roles

        if user.is_superuser:
            return True

        user_role = getattr(user, "role", "user").lower()
        return user_role in [r.lower() for r in required_roles]

    def _evaluate_conditions(self, user: Optional[User], conditions: Dict[str, Any]) -> bool:
        """Evaluate policy conditions."""
        # IP whitelist/blacklist
        if "ip_whitelist" in conditions:
            # Check IP
            pass

        # Time-based access
        if "time_range" in conditions:
            # Check time
            pass

        # User attributes
        if "user_attributes" in conditions and user:
            for attr, expected_value in conditions["user_attributes"].items():
                actual_value = getattr(user, attr, None)
                if actual_value != expected_value:
                    return False

        return True
```

---

## Security Best Practices

### 1. Password Security

**Best Practices:**
- Use bcrypt or argon2 for hashing
- Require strong passwords (min 12 characters, complexity)
- Implement password reset with secure tokens
- Never store plain passwords

```python
from passlib.context import CryptContext

# Use argon2 (preferred) or bcrypt
pwd_context = CryptContext(
    schemes=["argon2"],  # or ["bcrypt"]
    deprecated="auto",
    argon2__memory_cost=65536,  # 64 MB
    argon2__time_cost=3,  # 3 iterations
    argon2__parallelism=4,  # 4 threads
)

def hash_password(password: str) -> str:
    """Hash password securely."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password."""
    return pwd_context.verify(plain_password, hashed_password)

def validate_password_strength(password: str) -> tuple[bool, str]:
    """Validate password strength."""
    if len(password) < 12:
        return False, "Password must be at least 12 characters"

    if not any(c.isupper() for c in password):
        return False, "Password must contain uppercase letters"

    if not any(c.islower() for c in password):
        return False, "Password must contain lowercase letters"

    if not any(c.isdigit() for c in password):
        return False, "Password must contain digits"

    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        return False, "Password must contain special characters"

    return True, "Password is strong"
```

### 2. Token Security

**Best Practices:**
- Use HTTPS for all token transmission
- Set short token expiration times
- Implement token refresh mechanism
- Support token revocation/blacklisting
- Use secure cookie settings

```python
from datetime import datetime, timedelta, timezone
from typing import Set

class TokenBlacklist:
    """Token blacklist for revocation."""

    def __init__(self):
        self._blacklisted_tokens: Set[str] = set()
        self._expired_tokens: Set[str] = set()  # Auto-cleanup

    def blacklist_token(self, token: str, expires_at: datetime):
        """Add token to blacklist."""
        self._blacklisted_tokens.add(token)
        # Schedule cleanup
        if expires_at:
            self._expired_tokens.add(token)

    def is_blacklisted(self, token: str) -> bool:
        """Check if token is blacklisted."""
        return token in self._blacklisted_tokens

    def cleanup_expired(self):
        """Remove expired tokens from blacklist."""
        self._blacklisted_tokens -= self._expired_tokens
        self._expired_tokens.clear()

# Secure cookie settings
cookie_transport = CookieTransport(
    cookie_name="auth_cookie",
    cookie_max_age=3600,
    cookie_secure=True,  # HTTPS only
    cookie_httponly=True,  # Prevent XSS
    cookie_samesite="lax",  # CSRF protection
    cookie_domain=None,  # Use default domain
)
```

### 3. Rate Limiting

**Best Practices:**
- Implement rate limiting per authentication method
- Different limits for different user tiers
- Track failed authentication attempts
- Lock accounts after too many failures

```python
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Rate limits per authentication method
AUTH_RATE_LIMITS = {
    "login": "5/minute",
    "token_refresh": "10/minute",
    "password_reset": "3/hour",
    "api_key": "1000/hour",
}

@app.post("/auth/login")
@limiter.limit(AUTH_RATE_LIMITS["login"])
async def login(request: Request):
    """Login with rate limiting."""
    # Login logic
    pass

# Failed attempt tracking
class FailedAttemptTracker:
    """Track failed authentication attempts."""

    def __init__(self, max_attempts: int = 5, lockout_duration: timedelta = timedelta(minutes=15)):
        self._attempts: Dict[str, List[datetime]] = defaultdict(list)
        self.max_attempts = max_attempts
        self.lockout_duration = lockout_duration

    def record_failure(self, identifier: str):
        """Record failed attempt."""
        now = datetime.now(timezone.utc)
        self._attempts[identifier].append(now)

        # Clean old attempts
        cutoff = now - self.lockout_duration
        self._attempts[identifier] = [
            attempt for attempt in self._attempts[identifier]
            if attempt > cutoff
        ]

    def is_locked(self, identifier: str) -> bool:
        """Check if identifier is locked."""
        attempts = self._attempts.get(identifier, [])
        return len(attempts) >= self.max_attempts

    def clear_attempts(self, identifier: str):
        """Clear failed attempts."""
        self._attempts.pop(identifier, None)
```

### 4. Security Headers

**Best Practices:**
- Set security headers on all responses
- Use CORS properly
- Implement CSRF protection
- Set secure cookie flags

```python
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["example.com", "*.example.com"],
)

# Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add security headers to all responses."""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response
```

---

## FastAPI Integration

### 1. Dependency Injection Pattern

**Best Practices:**
- Use FastAPI dependencies for authentication
- Create reusable dependency functions
- Support optional authentication
- Chain dependencies for authorization

```python
from fastapi import Depends, HTTPException, status
from typing import Optional

# Base authentication dependency
async def get_current_user_optional(
    token: Optional[str] = Depends(oauth2_scheme),
) -> Optional[User]:
    """Get current user (optional - returns None if not authenticated)."""
    if not token:
        return None

    try:
        payload = verify_token(token)
        user = await get_user(payload.get("sub"))
        return user
    except HTTPException:
        return None

# Required authentication dependency
async def get_current_user(
    user: Optional[User] = Depends(get_current_user_optional),
) -> User:
    """Get current user (required - raises exception if not authenticated)."""
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# Active user dependency
async def get_current_active_user(
    user: User = Depends(get_current_user),
) -> User:
    """Get current active user."""
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return user

# Superuser dependency
async def get_current_superuser(
    user: User = Depends(get_current_active_user),
) -> User:
    """Get current superuser."""
    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return user

# Usage
@app.get("/public")
async def public_endpoint():
    """Public endpoint - no authentication required."""
    return {"message": "Public data"}

@app.get("/protected")
async def protected_endpoint(user: User = Depends(get_current_active_user)):
    """Protected endpoint - authentication required."""
    return {"user": user.email}

@app.get("/admin")
async def admin_endpoint(user: User = Depends(get_current_superuser)):
    """Admin endpoint - superuser required."""
    return {"admin": True}
```

### 2. Multiple Authentication Backends

**Best Practices:**
- Support multiple backends simultaneously
- Let FastAPI Users try backends in order
- Use appropriate backend for each route type

```python
from fastapi_users import FastAPIUsers

# Multiple backends
fastapi_users = FastAPIUsers[UserTable, UUID](
    get_user_manager,
    [jwt_backend, cookie_backend],  # Try JWT first, then cookie
)

# Current user dependency (tries all backends)
current_active_user = fastapi_users.current_user(active=True)

# Dynamic backend selection
async def get_enabled_backends(request: Request):
    """Return enabled backends based on request."""
    # API routes use JWT only
    if request.url.path.startswith("/api/"):
        return [jwt_backend]
    # Web routes use cookie
    elif request.url.path.startswith("/web/"):
        return [cookie_backend]
    # Default: try both
    else:
        return [jwt_backend, cookie_backend]

current_user_dynamic = fastapi_users.current_user(
    active=True,
    get_enabled_backends=get_enabled_backends,
)
```

### 3. Middleware Integration

**Best Practices:**
- Use middleware for cross-cutting concerns
- Log authentication events
- Track authentication metrics
- Handle authentication errors consistently

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import time

class AuthenticationMiddleware(BaseHTTPMiddleware):
    """Middleware for authentication logging and metrics."""

    async def dispatch(self, request: Request, call_next):
        """Process request with authentication tracking."""
        start_time = time.time()

        # Try to get user (don't fail if not authenticated)
        try:
            user = await get_current_user_optional(request)
            request.state.user = user
        except Exception:
            request.state.user = None

        # Process request
        response = await call_next(request)

        # Log authentication event
        duration = time.time() - start_time
        self.log_auth_event(request, response, duration)

        return response

    def log_auth_event(self, request: Request, response: Response, duration: float):
        """Log authentication event."""
        user = getattr(request.state, "user", None)
        logger.info(
            "Authentication event",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "user_id": user.id if user else None,
                "authenticated": user is not None,
                "duration_ms": duration * 1000,
            }
        )

app.add_middleware(AuthenticationMiddleware)
```

---

## Testing Strategies

### 1. Unit Testing

**Best Practices:**
- Test each authentication strategy independently
- Mock external dependencies (Auth0, OAuth providers)
- Test error cases
- Test token validation logic

```python
import pytest
from unittest.mock import Mock, patch, AsyncMock
from jose import jwt, ExpiredSignatureError

@pytest.fixture
def mock_user():
    """Mock user for testing."""
    user = Mock()
    user.id = "user-123"
    user.email = "test@example.com"
    user.is_active = True
    user.is_superuser = False
    return user

@pytest.mark.asyncio
async def test_jwt_token_creation():
    """Test JWT token creation."""
    token = create_access_token({"sub": "user-123"})
    assert token is not None
    assert isinstance(token, str)

    # Verify token can be decoded
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == "user-123"
    assert "exp" in payload

@pytest.mark.asyncio
async def test_jwt_token_expiration():
    """Test JWT token expiration."""
    # Create expired token
    expired_token = create_access_token(
        {"sub": "user-123"},
        expires_delta=timedelta(seconds=-1)  # Already expired
    )

    # Verify expiration is caught
    with pytest.raises(HTTPException) as exc_info:
        verify_token(expired_token)

    assert exc_info.value.status_code == 401

@pytest.mark.asyncio
async def test_api_key_validation():
    """Test API key validation."""
    key, key_info = generate_api_key("client-123")

    # Valid key
    result = await verify_api_key(key)
    assert result.client_id == "client-123"

    # Invalid key
    with pytest.raises(HTTPException):
        await verify_api_key("invalid_key")

@pytest.mark.asyncio
async def test_auth0_integration(mock_user):
    """Test Auth0 integration."""
    with patch("auth0.authentication.token_verifier.TokenVerifier") as mock_verifier:
        mock_verifier.verify = Mock(return_value={"sub": "auth0|123"})

        # Test Auth0 authentication
        result = await authenticate_auth0("auth0_token")
        assert result.success is True
```

### 2. Integration Testing

**Best Practices:**
- Test full authentication flows
- Test multiple strategies together
- Test error handling
- Test authorization checks

```python
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    """Test client."""
    return TestClient(app)

def test_login_flow(client):
    """Test complete login flow."""
    # Login
    response = client.post(
        "/auth/jwt/login",
        data={"username": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Use token for protected endpoint
    response = client.get(
        "/protected",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

def test_oauth_flow(client):
    """Test OAuth flow."""
    # Get authorization URL
    response = client.get("/auth/oauth/google/authorize")
    assert response.status_code == 200
    auth_url = response.json()["authorization_url"]
    assert "google.com" in auth_url

    # Simulate callback (in real test, would redirect)
    # ...

def test_api_key_authentication(client):
    """Test API key authentication."""
    # Create API key
    key, _ = generate_api_key("test-client")
    await store_api_key(key, key_info)

    # Use API key
    response = client.get(
        "/api/data",
        headers={"X-API-Key": key}
    )
    assert response.status_code == 200

def test_authorization_rbac(client):
    """Test RBAC authorization."""
    # Login as regular user
    token = get_user_token("user@example.com")

    # Try to access admin endpoint
    response = client.get(
        "/admin/users",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403  # Forbidden
```

### 3. Security Testing

**Best Practices:**
- Test token tampering
- Test expired tokens
- Test invalid credentials
- Test rate limiting
- Test CSRF protection

```python
def test_token_tampering(client):
    """Test token tampering detection."""
    token = create_access_token({"sub": "user-123"})

    # Tamper with token
    tampered_token = token[:-5] + "xxxxx"

    # Verify tampered token is rejected
    response = client.get(
        "/protected",
        headers={"Authorization": f"Bearer {tampered_token}"}
    )
    assert response.status_code == 401

def test_rate_limiting(client):
    """Test rate limiting."""
    # Make multiple login attempts
    for _ in range(6):  # Exceed limit of 5
        response = client.post(
            "/auth/login",
            data={"username": "test@example.com", "password": "wrong"}
        )

    # Should be rate limited
    assert response.status_code == 429

def test_account_lockout(client):
    """Test account lockout after failed attempts."""
    # Make multiple failed login attempts
    for _ in range(6):  # Exceed limit of 5
        client.post(
            "/auth/login",
            data={"username": "test@example.com", "password": "wrong"}
        )

    # Account should be locked
    response = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "correct"}
    )
    assert response.status_code == 423  # Locked
```

---

## Performance Considerations

### 1. Token Caching

**Best Practices:**
- Cache validated tokens
- Cache user lookups
- Set appropriate cache TTLs
- Invalidate cache on token revocation

```python
from functools import lru_cache
from datetime import datetime, timedelta
import redis.asyncio as aioredis

class TokenCache:
    """Token validation cache."""

    def __init__(self, redis_client: aioredis.Redis):
        self.redis = redis_client
        self.ttl = 300  # 5 minutes

    async def get_cached_user(self, token: str) -> Optional[User]:
        """Get cached user for token."""
        cache_key = f"token:{hashlib.sha256(token.encode()).hexdigest()}"
        user_data = await self.redis.get(cache_key)
        if user_data:
            return User.parse_raw(user_data)
        return None

    async def cache_user(self, token: str, user: User):
        """Cache user for token."""
        cache_key = f"token:{hashlib.sha256(token.encode()).hexdigest()}"
        await self.redis.setex(
            cache_key,
            self.ttl,
            user.json()
        )

    async def invalidate_token(self, token: str):
        """Invalidate cached token."""
        cache_key = f"token:{hashlib.sha256(token.encode()).hexdigest()}"
        await self.redis.delete(cache_key)
```

### 2. Database Query Optimization

**Best Practices:**
- Use database indexes on authentication fields
- Batch user lookups
- Use connection pooling
- Cache frequently accessed data

```python
# Database indexes
# CREATE INDEX idx_user_email ON users(email);
# CREATE INDEX idx_api_key_hash ON api_keys(key_hash);
# CREATE INDEX idx_user_active ON users(is_active);

# Batch user lookups
async def get_users_batch(user_ids: List[str]) -> Dict[str, User]:
    """Get multiple users in one query."""
    users = await db.execute(
        select(User).where(User.id.in_(user_ids))
    )
    return {user.id: user for user in users.scalars().all()}
```

### 3. Async Operations

**Best Practices:**
- Use async/await for all I/O operations
- Parallelize independent operations
- Use connection pooling
- Avoid blocking operations

```python
import asyncio

async def authenticate_with_parallel_checks(
    token: str,
    api_key: Optional[str] = None,
) -> Optional[AuthResult]:
    """Authenticate with parallel strategy checks."""
    # Run strategies in parallel
    tasks = []

    if token:
        tasks.append(jwt_strategy.authenticate(token))

    if api_key:
        tasks.append(api_key_strategy.authenticate(api_key))

    if not tasks:
        return None

    # Wait for first successful authentication
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for result in results:
        if isinstance(result, AuthResult) and result.success:
            return result

    return None
```

---

## Summary

### Key Takeaways

1. **Separation of Concerns**: Keep authentication and authorization separate
2. **Strategy Pattern**: Use strategy pattern for multiple authentication methods
3. **Security First**: Always validate tokens, hash passwords, use HTTPS
4. **FastAPI Integration**: Leverage FastAPI's dependency injection system
5. **Testing**: Comprehensive testing for all authentication flows
6. **Performance**: Cache tokens and optimize database queries
7. **Monitoring**: Log all authentication events for security monitoring

### Recommended Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  FastAPI Application                      │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────┐   │
│  │      Unified Authentication Manager               │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐         │   │
│  │  │  JWT     │ │  OAuth2  │ │  Auth0   │         │   │
│  │  │ Strategy │ │ Strategy │ │ Strategy │         │   │
│  │  └──────────┘ └──────────┘ └──────────┘         │   │
│  └──────────────────────────────────────────────────┘   │
│                          │                               │
│                          ▼                               │
│  ┌──────────────────────────────────────────────────┐   │
│  │      Authorization Manager (RBAC/Permissions)     │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## References

- [FastAPI Security Documentation](https://fastapi.tiangolo.com/tutorial/security/)
- [FastAPI Users Documentation](https://fastapi-users.github.io/fastapi-users/)
- [Python-JOSE Documentation](https://python-jose.readthedocs.io/)
- [Auth0 Python SDK](https://github.com/auth0/auth0-python)
- [OAuth2 Specification](https://oauth.net/2/)
- [JWT Best Practices](https://datatracker.ietf.org/doc/html/rfc8725)

---

**Version**: v1.0.0
**Last Updated**: 2025-01-14
