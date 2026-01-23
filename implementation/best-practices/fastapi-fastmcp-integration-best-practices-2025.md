# FastAPI + FastMCP Integration Best Practices

**Version**: v1.0.0  
**Last Updated**: 2025-01-14

This document provides comprehensive best practices for integrating FastAPI with FastMCP using the `fastapi-mcp` package (tadata-org/fastapi_mcp), which automatically maps FastAPI endpoints to Model Context Protocol (MCP) tools, enabling AI agents to discover and interact with your API.

---

## Table of Contents

1. [Architecture Principles](#architecture-principles)
2. [Basic Integration](#basic-integration)
3. [Selective Endpoint Exposure](#selective-endpoint-exposure)
4. [Authentication & Authorization](#authentication--authorization)
5. [Tool Naming & Documentation](#tool-naming--documentation)
6. [Dynamic Endpoint Management](#dynamic-endpoint-management)
7. [Transport Configuration](#transport-configuration)
8. [Advanced Configuration](#advanced-configuration)
9. [Testing & Debugging](#testing--debugging)
10. [Production Deployment](#production-deployment)

---

## Architecture Principles

### Integration Philosophy

**REQUIRED**: Understand the FastAPI-MCP integration:

1. **Automatic Discovery**: FastAPI-MCP automatically discovers FastAPI endpoints from OpenAPI schema
2. **Zero Configuration**: Minimal setup required - endpoints are auto-converted to MCP tools
3. **Schema Preservation**: Request/response schemas and documentation are preserved
4. **Type Safety**: Pydantic models ensure type-safe tool parameters
5. **Authentication Integration**: Leverage FastAPI's dependency injection for auth
6. **Selective Exposure**: Control which endpoints become MCP tools

### When to Use FastAPI-MCP

**REQUIRED**: Use FastAPI-MCP when:

- **AI Agent Integration**: Exposing APIs to LLMs/AI agents via MCP protocol
- **Automatic Tool Generation**: Want automatic conversion without manual tool definitions
- **Existing FastAPI APIs**: Have existing FastAPI endpoints to expose
- **Schema Preservation**: Need to preserve OpenAPI schemas and documentation
- **Minimal Overhead**: Want minimal code changes to existing FastAPI apps

**Consider alternatives when:**
- **Custom Tool Logic**: Need complex tool logic beyond simple endpoint mapping
- **Non-HTTP Protocols**: Need non-HTTP transport (use native FastMCP)
- **Fine-Grained Control**: Need complete control over tool definitions

---

## Basic Integration

### Minimal Setup

**REQUIRED**: Basic FastAPI-MCP integration:

```python
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

# Create FastAPI application
app = FastAPI(
    title="My API",
    description="API exposed as MCP tools",
)

# Define endpoints
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """Get user by ID."""
    return {"user_id": user_id, "name": "John Doe"}

@app.post("/users/")
async def create_user(name: str, email: str):
    """Create a new user."""
    return {"id": 1, "name": name, "email": email}

# Create MCP server from FastAPI app
mcp = FastApiMCP(app)

# Mount MCP server (defaults to /mcp)
mcp.mount_http()

# MCP server now available at http://localhost:8000/mcp
# All endpoints automatically converted to MCP tools
```

### Custom Mount Path

**REQUIRED**: Mount to custom path:

```python
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

app = FastAPI()

# Define endpoints...

# Mount to custom path
mcp = FastApiMCP(app)
mcp.mount_http(mount_path="/api/mcp")

# MCP server available at http://localhost:8000/api/mcp
```

### Server Metadata

**REQUIRED**: Set server name and description:

```python
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

app = FastAPI()

mcp = FastApiMCP(
    app,
    name="My API MCP Server",
    description="MCP interface for user management API",
)

mcp.mount_http()
```

---

## Selective Endpoint Exposure

### Include by Tags

**REQUIRED**: Expose only specific tagged endpoints:

```python
from fastapi import FastAPI, APIRouter
from fastapi_mcp import FastApiMCP

app = FastAPI()

# Public endpoints
@app.get("/public/data", tags=["public"])
async def get_public_data():
    """Public data endpoint."""
    return {"data": "public"}

# Admin endpoints
@app.get("/admin/users", tags=["admin"])
async def get_admin_users():
    """Admin-only endpoint."""
    return {"users": []}

# Expose only public endpoints
mcp = FastApiMCP(
    app,
    include_tags=["public"],
)

mcp.mount_http()
# Only /public/data is exposed as MCP tool
```

### Exclude by Tags

**REQUIRED**: Exclude specific tags:

```python
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

app = FastAPI()

@app.get("/public/data", tags=["public"])
async def get_public_data():
    return {"data": "public"}

@app.get("/internal/metrics", tags=["internal"])
async def get_internal_metrics():
    return {"metrics": {}}

# Exclude internal endpoints
mcp = FastApiMCP(
    app,
    exclude_tags=["internal", "admin"],
)

mcp.mount_http()
# /internal/metrics excluded from MCP tools
```

### Include by Operation ID

**REQUIRED**: Include specific operations:

```python
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

app = FastAPI()

@app.get("/users/{user_id}", operation_id="get_user")
async def get_user(user_id: int):
    return {"user_id": user_id}

@app.get("/users/", operation_id="list_users")
async def list_users():
    return {"users": []}

@app.delete("/users/{user_id}", operation_id="delete_user")
async def delete_user(user_id: int):
    return {"deleted": True}

# Include only specific operations
mcp = FastApiMCP(
    app,
    include_operations=["get_user", "list_users"],
)

mcp.mount_http()
# Only get_user and list_users exposed
```

### Exclude by Operation ID

**REQUIRED**: Exclude specific operations:

```python
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

app = FastAPI()

@app.get("/users/{user_id}", operation_id="get_user")
async def get_user(user_id: int):
    return {"user_id": user_id}

@app.delete("/users/{user_id}", operation_id="delete_user")
async def delete_user(user_id: int):
    return {"deleted": True}

# Exclude dangerous operations
mcp = FastApiMCP(
    app,
    exclude_operations=["delete_user", "update_user"],
)

mcp.mount_http()
# delete_user excluded from MCP tools
```

### Combined Filtering

**RECOMMENDED**: Combine operation and tag filtering:

```python
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

app = FastAPI()

# Include specific operations OR tags
mcp = FastApiMCP(
    app,
    include_operations=["user_login"],
    include_tags=["public"],
)

mcp.mount_http()
# Includes user_login OR any endpoint tagged "public"
```

---

## Authentication & Authorization

### Basic Authentication with Dependencies

**REQUIRED**: Use FastAPI dependencies for authentication:

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_mcp import FastApiMCP, AuthConfig

app = FastAPI()

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify authentication token."""
    token = credentials.credentials
    
    # Validate token (implement your logic)
    if not is_valid_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )
    
    return token

# Configure MCP with authentication
mcp = FastApiMCP(
    app,
    auth_config=AuthConfig(
        dependencies=[Depends(verify_token)],
    ),
)

mcp.mount_http()
```

### OAuth 2.0 Configuration

**REQUIRED**: OAuth 2.0 authentication:

```python
from fastapi import Depends
from fastapi_mcp import FastApiMCP, AuthConfig

mcp = FastApiMCP(
    app,
    name="MCP With OAuth",
    auth_config=AuthConfig(
        issuer="https://auth.example.com",
        authorize_url="https://auth.example.com/authorize",
        oauth_metadata_url="https://auth.example.com/.well-known/oauth-authorization-server",
        client_id="your-client-id",
        client_secret="your-client-secret",
        audience="your-api-audience",
        default_scope="openid profile email",
        dependencies=[Depends(verify_auth)],
        setup_proxies=True,
    ),
)

mcp.mount_http()
```

### Auth0 Integration

**RECOMMENDED**: Auth0 integration:

```python
from fastapi import Depends
from fastapi_mcp import FastApiMCP, AuthConfig
import os

mcp = FastApiMCP(
    app,
    auth_config=AuthConfig(
        issuer=f"https://{os.getenv('AUTH0_DOMAIN')}/",
        authorize_url=f"https://{os.getenv('AUTH0_DOMAIN')}/authorize",
        oauth_metadata_url=f"https://{os.getenv('AUTH0_DOMAIN')}/.well-known/oauth-authorization-server",
        client_id=os.getenv("AUTH0_CLIENT_ID"),
        client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
        audience=os.getenv("AUTH0_AUDIENCE"),
        dependencies=[Depends(verify_auth0_token)],
        setup_proxies=True,
    ),
)

mcp.mount_http()
```

### Custom OAuth Metadata

**RECOMMENDED**: Custom OAuth metadata:

```python
from fastapi import Depends
from fastapi_mcp import FastApiMCP, AuthConfig

mcp = FastApiMCP(
    app,
    auth_config=AuthConfig(
        custom_oauth_metadata={
            "issuer": "https://auth.example.com",
            "authorization_endpoint": "https://auth.example.com/authorize",
            "token_endpoint": "https://auth.example.com/token",
            "registration_endpoint": "https://auth.example.com/register",
            "scopes_supported": ["openid", "profile", "email"],
            "response_types_supported": ["code"],
            "grant_types_supported": ["authorization_code"],
            "token_endpoint_auth_methods_supported": ["none"],
            "code_challenge_methods_supported": ["S256"],
        },
        dependencies=[Depends(verify_auth)],
    ),
)

mcp.mount_http()
```

### Header-Based Authentication

**RECOMMENDED**: Pass authentication headers:

```python
from fastapi import Depends
from fastapi_mcp import FastApiMCP, AuthConfig

mcp = FastApiMCP(
    app,
    auth_config=AuthConfig(
        dependencies=[Depends(verify_token)],
    ),
    headers=["authorization", "x-api-key"],
)

mcp.mount_http()
```

---

## Tool Naming & Documentation

### Explicit Operation IDs

**REQUIRED**: Use explicit operation IDs for clear tool names:

```python
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

app = FastAPI()

# Auto-generated operation_id (verbose)
@app.get("/users/{user_id}")
async def read_user(user_id: int):
    return {"user_id": user_id}
# Tool name: "read_user_users__user_id__get"

# Explicit operation_id (clear)
@app.get("/users/{user_id}", operation_id="get_user_info")
async def read_user(user_id: int):
    return {"user_id": user_id}
# Tool name: "get_user_info"
```

### Tool Naming Best Practices

**REQUIRED**: Follow naming conventions:

```python
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

app = FastAPI()

# ✅ Good: Short, descriptive, snake_case
@app.get("/users/{user_id}", operation_id="get_user")
async def get_user(user_id: int):
    """Get user by ID."""
    return {"user_id": user_id}

# ✅ Good: Action-oriented names
@app.post("/users/", operation_id="create_user")
async def create_user(name: str, email: str):
    """Create a new user."""
    return {"id": 1, "name": name, "email": email}

# ❌ Bad: Too verbose
@app.get("/users/{user_id}", operation_id="get_user_by_id_from_database")
async def get_user(user_id: int):
    return {"user_id": user_id}

# ❌ Bad: Hyphens not allowed
@app.get("/users/", operation_id="get-all-users")
async def list_users():
    return {"users": []}
```

### Comprehensive Documentation

**REQUIRED**: Document endpoints thoroughly:

```python
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from fastapi_mcp import FastApiMCP

app = FastAPI()

class UserCreate(BaseModel):
    """User creation model."""
    name: str = Field(..., description="User's full name", example="John Doe")
    email: str = Field(..., description="User's email address", example="john@example.com")
    age: int = Field(None, description="User's age", ge=0, le=120)

class UserResponse(BaseModel):
    """User response model."""
    id: int = Field(..., description="User ID")
    name: str = Field(..., description="User's full name")
    email: str = Field(..., description="User's email address")

@app.post(
    "/users/",
    operation_id="create_user",
    response_model=UserResponse,
    summary="Create a new user",
    description="Creates a new user account with the provided information. Returns the created user object.",
    response_description="The created user object with assigned ID",
)
async def create_user(user: UserCreate) -> UserResponse:
    """
    Create a new user.
    
    This endpoint creates a new user account in the system.
    
    Args:
        user: User creation data
        
    Returns:
        Created user object
        
    Raises:
        HTTPException: If email already exists
    """
    # Implementation...
    return UserResponse(id=1, name=user.name, email=user.email)

mcp = FastApiMCP(app)
mcp.mount_http()
```

### Response Schema Descriptions

**RECOMMENDED**: Include full response schemas:

```python
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

app = FastAPI()

mcp = FastApiMCP(
    app,
    describe_all_responses=True,  # Include all possible response schemas
    describe_full_response_schema=True,  # Include full JSON schemas
)

mcp.mount_http()
```

---

## Dynamic Endpoint Management

### Re-registering Tools

**REQUIRED**: Re-register tools after adding endpoints:

```python
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

app = FastAPI()

# Initial MCP setup
mcp = FastApiMCP(app)
mcp.mount_http()

# Add initial endpoints
@app.get("/users/")
async def list_users():
    return {"users": []}

# Add new endpoint after MCP initialization
@app.get("/posts/", operation_id="list_posts")
async def list_posts():
    return {"posts": []}

# Re-register tools to include new endpoint
mcp.setup_server()

# Now list_posts is available as MCP tool
```

### Event-Driven Re-registration

**RECOMMENDED**: Re-register on endpoint changes:

```python
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from core.events.event_bus import EventBus

app = FastAPI()
event_bus = EventBus()
app.state.event_bus = event_bus

mcp = FastApiMCP(app)
mcp.mount_http()

async def on_endpoint_change(event_data: dict):
    """Handle endpoint change events."""
    action = event_data.get("action")
    endpoint_path = event_data.get("path")
    
    logger.info(f"Endpoint {action}: {endpoint_path}")
    
    # Re-register MCP tools
    mcp.setup_server()
    
    logger.info(f"MCP tools re-registered: {len(mcp.tools)} tools available")

# Subscribe to endpoint events
event_bus.subscribe("endpoint_registered", on_endpoint_change)
event_bus.subscribe("endpoint_unregistered", on_endpoint_change)
event_bus.subscribe("endpoint_updated", on_endpoint_change)
```

### Plugin-Based Integration

**RECOMMENDED**: Integrate as plugin:

```python
from typing import Any, Dict, Optional
from fastapi import FastAPI, Depends
from fastapi_mcp import FastApiMCP, AuthConfig
from core.interfaces import IPlugin, IPluginContext, PluginConfig

class APIMCPBridgePlugin(IPlugin):
    """Plugin that bridges FastAPI endpoints to MCP protocol."""
    
    def __init__(self):
        self.mcp: Optional[FastApiMCP] = None
    
    async def initialize(self, config: PluginConfig, context: IPluginContext) -> None:
        """Initialize MCP bridge."""
        app: FastAPI = context.app
        
        # Get configuration
        mcp_config = config.config_data or {}
        mcp_name = mcp_config.get("name", "API MCP Server")
        mount_path = mcp_config.get("mount_path", "/mcp")
        
        # Setup authentication
        from app.auth.dependencies import current_superuser
        
        auth_config = AuthConfig(
            dependencies=[Depends(current_superuser)],
        )
        
        # Initialize MCP
        self.mcp = FastApiMCP(
            fastapi=app,
            name=mcp_name,
            include_tags=["gateway-admin"],
            auth_config=auth_config,
            headers=["authorization", "x-api-key"],
            describe_full_response_schema=True,
        )
        
        # Mount HTTP transport
        self.mcp.mount_http(mount_path=mount_path)
        
        # Subscribe to endpoint changes
        event_bus = app.state.event_bus
        if event_bus:
            event_bus.subscribe("endpoint_registered", self._on_endpoint_change)
            event_bus.subscribe("endpoint_unregistered", self._on_endpoint_change)
    
    async def _on_endpoint_change(self, event_data: Dict[str, Any]) -> None:
        """Re-register tools on endpoint changes."""
        if self.mcp:
            self.mcp.setup_server()
```

---

## Transport Configuration

### HTTP Transport (Recommended)

**REQUIRED**: Use HTTP transport:

```python
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

app = FastAPI()

mcp = FastApiMCP(app)

# Mount HTTP transport (default)
mcp.mount_http()

# Or with custom path
mcp.mount_http(mount_path="/api/mcp")
```

### SSE Transport

**RECOMMENDED**: Server-Sent Events transport:

```python
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

app = FastAPI()

mcp = FastApiMCP(app)

# Mount SSE transport
mcp.mount_sse(mount_path="/mcp/sse")
```

### Custom HTTP Client

**RECOMMENDED**: Custom httpx client:

```python
import httpx
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

app = FastAPI()

# Custom HTTP client configuration
custom_client = httpx.AsyncClient(
    base_url="https://api.example.com",
    timeout=30.0,
    headers={"X-Custom-Header": "value"},
)

mcp = FastApiMCP(
    app,
    http_client=custom_client,
)

mcp.mount_http()
```

### HTTP Timeout Configuration

**RECOMMENDED**: Configure timeouts:

```python
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
import httpx

app = FastAPI()

# Custom timeout (10 seconds)
custom_client = httpx.AsyncClient(timeout=10.0)

mcp = FastApiMCP(
    app,
    http_client=custom_client,
)

mcp.mount_http()
```

---

## Advanced Configuration

### Custom Router Integration

**RECOMMENDED**: Use with APIRouter:

```python
from fastapi import FastAPI, APIRouter
from fastapi_mcp import FastApiMCP

app = FastAPI()
router = APIRouter(prefix="/api/v1")

@router.get("/users/")
async def list_users():
    return {"users": []}

app.include_router(router)

mcp = FastApiMCP(app)
mcp.mount_http()
```

### Separate Deployment

**RECOMMENDED**: Deploy MCP server separately:

```python
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

# Original API application
api_app = FastAPI()

@api_app.get("/users/")
async def list_users():
    return {"users": []}

# Separate MCP server application
mcp_app = FastAPI()

# Create MCP server from API app
mcp = FastApiMCP(api_app)

# Mount to separate app
mcp.mount_http(mcp_app)

# Run separately:
# uvicorn main:api_app --host 0.0.0.0 --port 8001
# uvicorn main:mcp_app --host 0.0.0.0 --port 8000
```

### Selective Exposure Pattern

**REQUIRED**: Best practice for selective exposure:

```python
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

app = FastAPI()

# ✅ Expose: Safe read operations
@app.get("/users/{user_id}", operation_id="get_user", tags=["public"])
async def get_user(user_id: int):
    """Get user information."""
    return {"user_id": user_id}

@app.get("/users/", operation_id="list_users", tags=["public"])
async def list_users():
    """List all users."""
    return {"users": []}

# ⚠️ Expose with caution: Write operations
@app.post("/users/", operation_id="create_user", tags=["admin"])
async def create_user(name: str, email: str):
    """Create a new user."""
    return {"id": 1, "name": name, "email": email}

# ❌ Don't expose: Dangerous operations
@app.delete("/users/{user_id}", operation_id="delete_user", tags=["admin"])
async def delete_user(user_id: int):
    """Delete a user."""
    return {"deleted": True}

# Only expose safe operations
mcp = FastApiMCP(
    app,
    include_tags=["public"],  # Only public read operations
    # OR
    # exclude_operations=["delete_user", "update_user"],
)

mcp.mount_http()
```

---

## Testing & Debugging

### MCP Inspector Usage

**REQUIRED**: Test with MCP Inspector:

```bash
# Install MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Start inspector
npx @modelcontextprotocol/inspector

# Connect to your MCP server
# URL: http://localhost:8000/mcp

# Navigate to Tools section
# Click "List Tools" to see available endpoints
# Select a tool and test it
```

### Client Configuration (SSE)

**REQUIRED**: Configure MCP client for SSE:

```json
{
  "mcpServers": {
    "fastapi-mcp": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

### Client Configuration (HTTP with Auth)

**REQUIRED**: Configure with authentication:

```json
{
  "mcpServers": {
    "fastapi-mcp": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://localhost:8000/mcp",
        "--header",
        "Authorization:${AUTH_HEADER}"
      ]
    },
    "env": {
      "AUTH_HEADER": "Bearer your-token-here"
    }
  }
}
```

### Testing Tool Registration

**REQUIRED**: Verify tool registration:

```python
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

app = FastAPI()

@app.get("/users/", operation_id="list_users")
async def list_users():
    return {"users": []}

mcp = FastApiMCP(app)
mcp.mount_http()

# Check registered tools
print(f"Registered {len(mcp.tools)} tools")
for tool in mcp.tools:
    print(f"  - {tool.name}: {tool.description}")
```

---

## Production Deployment

### Production Configuration

**REQUIRED**: Production-ready setup:

```python
from fastapi import FastAPI, Depends
from fastapi_mcp import FastApiMCP, AuthConfig
from app.config import get_settings
from app.auth.dependencies import current_superuser

settings = get_settings()

app = FastAPI(
    title=settings.service_name,
    version=settings.service_version,
)

# Production MCP configuration
mcp = FastApiMCP(
    app,
    name=f"{settings.service_name} MCP Server",
    description=f"MCP interface for {settings.service_name}",
    include_tags=["public", "admin"],  # Selective exposure
    exclude_tags=["internal"],  # Exclude internal endpoints
    auth_config=AuthConfig(
        dependencies=[Depends(current_superuser)],
    ),
    headers=["authorization", "x-api-key"],
    describe_full_response_schema=True,
)

# Mount to production path
mcp.mount_http(mount_path="/api/mcp")
```

### Security Best Practices

**REQUIRED**: Security considerations:

```python
from fastapi import FastAPI, Depends
from fastapi_mcp import FastApiMCP, AuthConfig

app = FastAPI()

# ✅ Good: Require authentication
mcp = FastApiMCP(
    app,
    auth_config=AuthConfig(
        dependencies=[Depends(verify_auth)],
    ),
)

# ✅ Good: Exclude dangerous operations
mcp = FastApiMCP(
    app,
    exclude_operations=["delete_user", "delete_data", "drop_table"],
)

# ✅ Good: Only expose safe endpoints
mcp = FastApiMCP(
    app,
    include_tags=["read-only", "public"],
)

# ❌ Bad: Expose everything without auth
mcp = FastApiMCP(app)  # No auth, exposes all endpoints

mcp.mount_http()
```

### Monitoring & Observability

**RECOMMENDED**: Add monitoring:

```python
from fastapi import FastAPI, Request
from fastapi_mcp import FastApiMCP
import logging

logger = logging.getLogger(__name__)

app = FastAPI()

mcp = FastApiMCP(app)

# Log tool registration
@app.on_event("startup")
async def startup_event():
    logger.info(f"MCP server initialized with {len(mcp.tools)} tools")
    for tool in mcp.tools:
        logger.debug(f"Registered tool: {tool.name}")

# Monitor tool calls
@app.middleware("http")
async def log_mcp_requests(request: Request, call_next):
    if request.url.path.startswith("/mcp"):
        logger.info(f"MCP request: {request.method} {request.url.path}")
    
    response = await call_next(request)
    
    if request.url.path.startswith("/mcp"):
        logger.info(f"MCP response: {response.status_code}")
    
    return response

mcp.mount_http()
```

### Performance Optimization

**RECOMMENDED**: Optimize for performance:

```python
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
import httpx

app = FastAPI()

# Optimize HTTP client
optimized_client = httpx.AsyncClient(
    timeout=30.0,
    limits=httpx.Limits(
        max_keepalive_connections=20,
        max_connections=100,
    ),
    http2=True,  # Enable HTTP/2
)

mcp = FastApiMCP(
    app,
    http_client=optimized_client,
)

mcp.mount_http()
```

---

## Summary

### Key Takeaways

1. **Selective Exposure**: Only expose safe, meaningful endpoints
2. **Explicit Operation IDs**: Use clear, descriptive operation IDs
3. **Authentication**: Always require authentication for MCP endpoints
4. **Documentation**: Provide comprehensive endpoint documentation
5. **Re-registration**: Re-register tools when endpoints change dynamically
6. **HTTP Transport**: Prefer HTTP transport for production
7. **Security**: Exclude dangerous operations (DELETE, DROP, etc.)
8. **Monitoring**: Add logging and monitoring for MCP requests
9. **Testing**: Use MCP Inspector for testing and debugging
10. **Performance**: Optimize HTTP client configuration

### Resources

- [FastAPI-MCP GitHub](https://github.com/tadata-org/fastapi_mcp)
- [FastAPI-MCP Documentation](https://fastapi-mcp.tadata.com/)
- [FastAPI-MCP PyPI](https://pypi.org/project/fastapi-mcp/)
- [MCP Specification](https://modelcontextprotocol.io/)

---

**Version**: v1.0.0  
**Last Updated**: 2025-01-14

