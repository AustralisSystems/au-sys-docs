# FastMCP Best Practices 2025
**Version**: v1.0.0
**Last Updated**: 2025-01-14
**FastMCP Version**: Latest (jlowin/fastmcp)
**MCP Protocol Version**: 2024-11-05 / 2025-06-18

This document compiles the latest FastMCP (Model Context Protocol) best practices based on official documentation, production code examples, and community recommendations for 2025.

---

## Table of Contents

1. [Server Setup & Initialization](#server-setup--initialization)
2. [Tools Implementation](#tools-implementation)
3. [Resources Management](#resources-management)
4. [Prompts & Templates](#prompts--templates)
5. [Authentication & Security](#authentication--security)
6. [Transport Configuration](#transport-configuration)
7. [Middleware & Extensions](#middleware--extensions)
8. [Error Handling](#error-handling)
9. [Testing](#testing)
10. [Deployment & Production](#deployment--production)
11. [Performance Optimization](#performance-optimization)

---

## Server Setup & Initialization

### ✅ Best Practices

#### 1. Basic Server Initialization

```python
from fastmcp import FastMCP

# Simple initialization
mcp = FastMCP(name="My MCP Server")

# With configuration
mcp = FastMCP(
    name="My MCP Server",
    version="1.0.0",
    log_level="INFO"
)
```

#### 2. Server with Authentication

```python
from fastmcp import FastMCP
from fastmcp.server.auth.providers import BearerTokenProvider

# Configure authentication
auth_provider = BearerTokenProvider({
    "secret-token": "user-id",
    "another-token": "another-user-id"
})

mcp = FastMCP(
    name="Protected Server",
    auth=auth_provider
)
```

#### 3. Environment-Based Configuration

```python
import os
from fastmcp import FastMCP

# Authentication automatically configured from environment variables
# Set FASTMCP_AUTH_PROVIDER, FASTMCP_AUTH_SECRET, etc.
mcp = FastMCP(name="Environment Configured Server")
```

**Environment Variables:**
- `FASTMCP_AUTH_PROVIDER`: Auth provider type
- `FASTMCP_AUTH_SECRET`: Secret key for JWT
- `FASTMCP_LOG_LEVEL`: Logging level
- `FASTMCP_HOST`: Server host
- `FASTMCP_PORT`: Server port

#### 4. Server Composition

```python
from fastmcp import FastMCP

# Create subservers
weather_service = FastMCP("WeatherService")

@weather_service.tool
def get_forecast(city: str) -> dict:
    return {"city": city, "temp": 72}

# Compose into main server
main_app = FastMCP("MainApp")
await main_app.import_server(weather_service, prefix="weather")
# Tools become: weather_get_forecast
```

---

## Tools Implementation

### ✅ Best Practices

#### 1. Basic Tool Definition

```python
from fastmcp import FastMCP

mcp = FastMCP()

@mcp.tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b
    """
    return a + b
```

#### 2. Async Tools

```python
@mcp.tool
async def fetch_data(url: str) -> dict:
    """Fetch data from a URL."""
    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
```

#### 3. Tools with Context

```python
from fastmcp import FastMCP, Context

mcp = FastMCP()

@mcp.tool
async def tool_with_context(ctx: Context, param: str) -> str:
    """Tool that accesses server context."""
    # Access resources
    resource = await ctx.fastmcp.get_resource("resource://data")

    # Access other tools
    result = await ctx.fastmcp.call_tool("another_tool", {})

    return f"Processed: {param}"
```

#### 4. Tools with Annotations

```python
from fastmcp import FastMCP
from fastmcp.tools import ToolAnnotations

@mcp.tool(
    annotations=ToolAnnotations(
        title="Convert Temperature",
        description="Convert Celsius to Fahrenheit",
        tags=["temperature", "conversion"]
    )
)
def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9 / 5) + 32
```

#### 5. Tools with Pydantic Models

```python
from pydantic import BaseModel, Field
from fastmcp import FastMCP

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: int = Field(..., ge=0, le=150)

@mcp.tool
def create_user(user: UserCreate) -> dict:
    """Create a new user."""
    return {
        "id": "123",
        "name": user.name,
        "email": user.email
    }
```

#### 6. Protected Tools

```python
from fastmcp import FastMCP, Context

mcp = FastMCP()

@mcp.tool(require_auth=True)
async def protected_action(ctx: Context) -> str:
    """Tool that requires authentication."""
    # User info available in context if authenticated
    user_id = ctx.user_id if hasattr(ctx, 'user_id') else None
    return f"Action performed by user: {user_id}"
```

#### 7. Tool Error Handling

```python
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

@mcp.tool
async def risky_operation(param: str) -> str:
    """Tool with proper error handling."""
    try:
        # Perform operation
        result = await perform_operation(param)
        return result
    except ValueError as e:
        raise ToolError(f"Invalid parameter: {e}")
    except Exception as e:
        raise ToolError(f"Operation failed: {e}")
```

---

## Resources Management

### ✅ Best Practices

#### 1. Basic Resource Definition

```python
from fastmcp import FastMCP

mcp = FastMCP()

@mcp.resource("resource://data")
def get_data() -> str:
    """Provide data resource."""
    return "Resource content"
```

#### 2. Resource with URI Template

```python
@mcp.resource("file:///{path}")
def get_file(path: str) -> str:
    """Get file content by path."""
    with open(path, 'r') as f:
        return f.read()
```

#### 3. Resource with MIME Type

```python
@mcp.resource("resource://image.png", mime_type="image/png")
def get_image() -> bytes:
    """Get image resource."""
    return Path("image.png").read_bytes()
```

#### 4. Resource with Annotations

```python
@mcp.resource(
    "resource://config",
    name="configuration",
    annotations={
        "audience": ["assistant"],
        "priority": 0.9
    }
)
def get_config() -> dict:
    """Get configuration resource."""
    return {"setting": "value"}
```

#### 5. Async Resources

```python
@mcp.resource("resource://async-data")
async def get_async_data() -> dict:
    """Get data asynchronously."""
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
        return response.json()
```

#### 6. Resource Templates

```python
@mcp.resource("project://{component}/{file}")
def get_project_file(component: str, file: str) -> str:
    """Get project file by component and filename."""
    path = Path(f"project/{component}/{file}")
    return path.read_text()
```

#### 7. Resource Subscriptions

```python
from fastmcp import FastMCP

mcp = FastMCP()

# Declare resource capability with subscriptions
mcp.capabilities.resources.subscribe = True
mcp.capabilities.resources.listChanged = True

@mcp.resource("resource://live-data")
def get_live_data() -> str:
    """Resource that can be subscribed to."""
    return get_current_data()

# Notify subscribers when resource changes
async def update_resource():
    await mcp.notify_resource_changed("resource://live-data")
```

---

## Prompts & Templates

### ✅ Best Practices

#### 1. Basic Prompt Definition

```python
from fastmcp import FastMCP

mcp = FastMCP()

@mcp.prompt
def code_review_prompt(code: str) -> list[dict]:
    """Prompt for code review."""
    return [
        {
            "role": "user",
            "content": {
                "type": "text",
                "text": f"Please review this code:\n\n{code}"
            }
        }
    ]
```

#### 2. Prompt with Arguments

```python
@mcp.prompt
def generate_summary_prompt(
    title: str,
    content: str,
    max_length: int = 200
) -> list[dict]:
    """Generate a summary prompt."""
    return [
        {
            "role": "user",
            "content": {
                "type": "text",
                "text": f"Summarize this article in {max_length} words:\n\nTitle: {title}\n\n{content}"
            }
        }
    ]
```

#### 3. Prompt with Resource References

```python
@mcp.prompt
def analyze_document_prompt(document_uri: str) -> list[dict]:
    """Prompt that references a resource."""
    return [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Analyze this document:"
                },
                {
                    "type": "resource",
                    "resource": {
                        "uri": document_uri,
                        "mimeType": "text/plain"
                    }
                }
            ]
        }
    ]
```

#### 4. Prompt List Changed Notifications

```python
# Declare prompt capability
mcp.capabilities.prompts.listChanged = True

# Notify when prompts change
async def update_prompts():
    await mcp.notify_prompts_list_changed()
```

---

## Authentication & Security

### ✅ Best Practices

#### 1. Bearer Token Authentication

```python
from fastmcp import FastMCP
from fastmcp.server.auth.providers import BearerTokenProvider

auth_provider = BearerTokenProvider({
    "token-1": "user-1",
    "token-2": "user-2"
})

mcp = FastMCP(name="Protected Server", auth=auth_provider)

@mcp.tool(require_auth=True)
def protected_tool() -> str:
    return "Access granted"
```

#### 2. OAuth2 Providers

```python
from fastmcp import FastMCP
from fastmcp.server.auth.providers.github import GitHubProvider

auth_provider = GitHubProvider(
    client_id="your-client-id",
    client_secret="your-client-secret"
)

mcp = FastMCP(name="GitHub Protected Server", auth=auth_provider)
```

#### 3. Auth0 Integration

```python
from fastmcp import FastMCP
from fastmcp.server.auth.providers.auth0 import Auth0Provider

auth_provider = Auth0Provider(
    config_url="https://your-domain.auth0.com/.well-known/openid-configuration",
    client_id="your-client-id",
    client_secret="your-client-secret",
    audience="your-api-audience",
    base_url="https://your-api.com"
)

mcp = FastMCP(name="Auth0 Protected Server", auth=auth_provider)
```

#### 4. AWS Cognito Integration

```python
from fastmcp import FastMCP
from fastmcp.server.auth.providers.aws import AWSCognitoProvider

auth_provider = AWSCognitoProvider(
    user_pool_id="us-east-1_XXXXXXXXX",
    domain_prefix="your-domain",
    client_id="your-client-id",
    client_secret="your-client-secret"
)

mcp = FastMCP(name="Cognito Protected Server", auth=auth_provider)
```

#### 5. Google OAuth Integration

```python
from fastmcp import FastMCP
from fastmcp.server.auth.providers.google import GoogleProvider

auth_provider = GoogleProvider(
    client_id="your-client-id.apps.googleusercontent.com",
    client_secret="your-client-secret"
)

mcp = FastMCP(name="Google Protected Server", auth=auth_provider)
```

#### 6. Custom Authentication Middleware

```python
from fastmcp.server.middleware import Middleware, MiddlewareContext

class CustomAuthMiddleware(Middleware):
    async def on_call_tool(self, context: MiddlewareContext, call_next):
        # Check authentication
        if not self.is_authenticated(context):
            raise AuthenticationError("Not authenticated")

        return await call_next(context)

    def is_authenticated(self, context: MiddlewareContext) -> bool:
        # Custom authentication logic
        return True

mcp.add_middleware(CustomAuthMiddleware())
```

---

## Transport Configuration

### ✅ Best Practices

#### 1. Stdio Transport (Default)

```python
from fastmcp import FastMCP

# Stdio is the default transport
mcp = FastMCP(name="Stdio Server")

# Run server
if __name__ == "__main__":
    mcp.run()
```

#### 2. HTTP/SSE Transport

```python
from fastmcp import FastMCP
from fastmcp.server.transports import HttpSseTransport

mcp = FastMCP(name="HTTP Server")

# Configure HTTP/SSE transport
transport = HttpSseTransport(
    host="0.0.0.0",
    port=8000
)

mcp.run(transport=transport)
```

#### 3. WebSocket Transport

```python
from fastmcp import FastMCP
from fastmcp.server.transports import WebSocketTransport

mcp = FastMCP(name="WebSocket Server")

transport = WebSocketTransport(
    host="0.0.0.0",
    port=8000
)

mcp.run(transport=transport)
```

#### 4. Client Transport Configuration

```python
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport, SSETransport

# Streamable HTTP Transport
client = Client(
    transport=StreamableHttpTransport(
        url="https://api.example.com/mcp",
        headers={"Authorization": "Bearer token"}
    )
)

# Legacy SSE Transport
client = Client(
    transport=SSETransport(
        url="https://api.example.com/sse",
        headers={"Authorization": "Bearer token"}
    )
)
```

---

## Middleware & Extensions

### ✅ Best Practices

#### 1. Custom Middleware

```python
from fastmcp.server.middleware import Middleware, MiddlewareContext

class LoggingMiddleware(Middleware):
    async def on_call_tool(self, context: MiddlewareContext, call_next):
        logger.info(f"Calling tool: {context.message.name}")
        try:
            result = await call_next(context)
            logger.info(f"Tool {context.message.name} succeeded")
            return result
        except Exception as e:
            logger.error(f"Tool {context.message.name} failed: {e}")
            raise

mcp.add_middleware(LoggingMiddleware())
```

#### 2. Access Control Middleware

```python
from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.exceptions import ResourceError, PromptError

class AccessControlMiddleware(Middleware):
    async def on_read_resource(self, context: MiddlewareContext, call_next):
        if context.fastmcp_context:
            resource = await context.fastmcp_context.fastmcp.get_resource(
                context.message.uri
            )
            if "restricted" in resource.tags:
                if not self.has_permission(context):
                    raise ResourceError("Access denied: restricted resource")

        return await call_next(context)

    def has_permission(self, context: MiddlewareContext) -> bool:
        # Check user permissions
        return True

mcp.add_middleware(AccessControlMiddleware())
```

#### 3. Tool Injection Middleware

```python
from fastmcp.server.middleware.tool_injection import (
    ResourceToolMiddleware,
    PromptToolMiddleware
)

# Enable tool-based access to resources
mcp.add_middleware(ResourceToolMiddleware())

# Enable tool-based access to prompts
mcp.add_middleware(PromptToolMiddleware())
```

#### 4. Rate Limiting Middleware

```python
from fastmcp.server.middleware import Middleware, MiddlewareContext
from collections import defaultdict
from datetime import datetime, timedelta

class RateLimitMiddleware(Middleware):
    def __init__(self, max_requests: int = 100, window: int = 60):
        self.max_requests = max_requests
        self.window = window
        self.requests = defaultdict(list)

    async def on_call_tool(self, context: MiddlewareContext, call_next):
        client_id = self.get_client_id(context)
        now = datetime.now()

        # Clean old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < timedelta(seconds=self.window)
        ]

        # Check rate limit
        if len(self.requests[client_id]) >= self.max_requests:
            raise RateLimitError("Rate limit exceeded")

        # Record request
        self.requests[client_id].append(now)

        return await call_next(context)

    def get_client_id(self, context: MiddlewareContext) -> str:
        # Extract client identifier
        return "default"

mcp.add_middleware(RateLimitMiddleware(max_requests=100, window=60))
```

---

## Error Handling

### ✅ Best Practices

#### 1. Tool Error Handling

```python
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

@mcp.tool
async def risky_tool(param: str) -> str:
    """Tool with comprehensive error handling."""
    try:
        # Validate input
        if not param:
            raise ValueError("Parameter cannot be empty")

        # Perform operation
        result = await perform_operation(param)
        return result

    except ValueError as e:
        raise ToolError(f"Invalid input: {e}")
    except ConnectionError as e:
        raise ToolError(f"Connection failed: {e}")
    except Exception as e:
        logger.error(f"Unexpected error in risky_tool: {e}", exc_info=True)
        raise ToolError("An unexpected error occurred")
```

#### 2. Resource Error Handling

```python
from fastmcp.exceptions import ResourceError

@mcp.resource("resource://data")
def get_resource() -> str:
    """Resource with error handling."""
    try:
        return read_resource_data()
    except FileNotFoundError:
        raise ResourceError("Resource not found", code=-32002)
    except PermissionError:
        raise ResourceError("Access denied", code=-32003)
```

#### 3. Prompt Error Handling

```python
from fastmcp.exceptions import PromptError

@mcp.prompt
def get_prompt(name: str) -> list[dict]:
    """Prompt with error handling."""
    if name not in AVAILABLE_PROMPTS:
        raise PromptError(f"Prompt '{name}' not found")

    return AVAILABLE_PROMPTS[name]
```

#### 4. Global Error Handler

```python
from fastmcp import FastMCP
from fastmcp.exceptions import MCPError

mcp = FastMCP()

@mcp.error_handler
async def handle_error(error: MCPError, context: dict) -> dict:
    """Global error handler."""
    logger.error(f"MCP Error: {error}", extra=context)

    return {
        "error": {
            "code": error.code,
            "message": str(error),
            "data": context
        }
    }
```

---

## Testing

### ✅ Best Practices

#### 1. Basic Tool Testing

```python
import pytest
from fastmcp import FastMCP, Client

@pytest.fixture
def test_server():
    mcp = FastMCP("TestServer")

    @mcp.tool
    def add(a: int, b: int) -> int:
        return a + b

    return mcp

@pytest.mark.asyncio
async def test_add_tool(test_server):
    async with Client(test_server) as client:
        result = await client.call_tool("add", {"a": 2, "b": 3})
        assert result.data == 5
```

#### 2. Testing with Authentication

```python
from fastmcp import FastMCP, Client
from fastmcp.client.auth import BearerAuth

@pytest.mark.asyncio
async def test_authenticated_tool():
    mcp = FastMCP("TestServer")
    mcp.auth = BearerTokenProvider({"token": "user"})

    @mcp.tool(require_auth=True)
    def protected() -> str:
        return "success"

    async with Client(mcp, auth=BearerAuth("token")) as client:
        result = await client.call_tool("protected", {})
        assert result.content[0].text == "success"
```

#### 3. Testing Resources

```python
@pytest.mark.asyncio
async def test_resource():
    mcp = FastMCP()

    @mcp.resource("resource://data")
    def get_data() -> str:
        return "test data"

    async with Client(mcp) as client:
        result = await client.read_resource("resource://data")
        assert result[0].text == "test data"
```

#### 4. Testing Prompts

```python
@pytest.mark.asyncio
async def test_prompt():
    mcp = FastMCP()

    @mcp.prompt
    def test_prompt(arg: str) -> list[dict]:
        return [{"role": "user", "content": {"type": "text", "text": arg}}]

    async with Client(mcp) as client:
        result = await client.get_prompt("test_prompt", {"arg": "test"})
        assert len(result.messages) == 1
```

---

## Deployment & Production

### ✅ Best Practices

#### 1. Environment Configuration

```python
import os
from fastmcp import FastMCP
from fastmcp.server.auth.providers import BearerTokenProvider

# Load configuration from environment
AUTH_TOKENS = os.getenv("FASTMCP_AUTH_TOKENS", "").split(",")
LOG_LEVEL = os.getenv("FASTMCP_LOG_LEVEL", "INFO")
HOST = os.getenv("FASTMCP_HOST", "0.0.0.0")
PORT = int(os.getenv("FASTMCP_PORT", "8000"))

# Configure authentication
auth_provider = BearerTokenProvider({
    token: f"user-{i}" for i, token in enumerate(AUTH_TOKENS)
})

mcp = FastMCP(
    name="Production Server",
    auth=auth_provider,
    log_level=LOG_LEVEL
)
```

#### 2. Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir fastmcp

COPY . .

CMD ["python", "-m", "mcp_server"]
```

#### 3. Health Check Endpoint

```python
from fastmcp import FastMCP

mcp = FastMCP()

@mcp.tool
def health_check() -> dict:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }
```

#### 4. Logging Configuration

```python
import logging
from fastmcp import FastMCP

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("mcp_server.log"),
        logging.StreamHandler()
    ]
)

mcp = FastMCP(name="Logged Server", log_level="INFO")
```

---

## Performance Optimization

### ✅ Best Practices

#### 1. Async Operations

```python
# ✅ Good: Use async for I/O operations
@mcp.tool
async def fetch_data(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        return await client.get(url).json()

# ❌ Bad: Blocking I/O
@mcp.tool
def fetch_data_blocking(url: str) -> dict:
    import requests
    return requests.get(url).json()  # Blocks!
```

#### 2. Resource Caching

```python
from functools import lru_cache
from datetime import datetime, timedelta

class CachedResource:
    def __init__(self, ttl: int = 300):
        self.cache = {}
        self.ttl = ttl

    def get(self, key: str):
        if key in self.cache:
            value, timestamp = self.cache[key]
            if datetime.now() - timestamp < timedelta(seconds=self.ttl):
                return value
        return None

    def set(self, key: str, value: any):
        self.cache[key] = (value, datetime.now())

cache = CachedResource(ttl=300)

@mcp.resource("resource://cached-data")
def get_cached_data() -> str:
    cached = cache.get("data")
    if cached:
        return cached

    data = fetch_expensive_data()
    cache.set("data", data)
    return data
```

#### 3. Connection Pooling

```python
import httpx
from fastmcp import FastMCP

# Create shared HTTP client
http_client = httpx.AsyncClient(
    limits=httpx.Limits(max_keepalive_connections=20, max_connections=100),
    timeout=httpx.Timeout(10.0)
)

mcp = FastMCP()

@mcp.tool
async def fetch_with_pool(url: str) -> dict:
    """Use shared connection pool."""
    response = await http_client.get(url)
    return response.json()
```

#### 4. Batch Operations

```python
@mcp.tool
async def batch_process(items: list[str]) -> list[dict]:
    """Process multiple items efficiently."""
    # Use asyncio.gather for parallel processing
    results = await asyncio.gather(*[
        process_item(item) for item in items
    ])
    return results
```

---

## Summary Checklist

### Server Setup
- [ ] Proper server initialization with name and version
- [ ] Environment-based configuration
- [ ] Authentication configured if needed
- [ ] Logging properly configured

### Tools
- [ ] Tools use async/await for I/O operations
- [ ] Proper type hints and Pydantic models
- [ ] Comprehensive docstrings
- [ ] Error handling implemented
- [ ] Protected tools use authentication

### Resources
- [ ] Resources properly defined with URIs
- [ ] MIME types specified
- [ ] Resource templates for parameterized access
- [ ] Subscriptions enabled if needed
- [ ] List change notifications configured

### Prompts
- [ ] Prompts properly structured
- [ ] Arguments clearly defined
- [ ] Resource references used when appropriate
- [ ] List change notifications enabled

### Authentication
- [ ] Appropriate auth provider selected
- [ ] Tokens/secrets stored in environment variables
- [ ] Protected endpoints require authentication
- [ ] User context accessible in tools

### Transport
- [ ] Appropriate transport selected (stdio/HTTP/WebSocket)
- [ ] Headers configured for authentication
- [ ] CORS configured if needed

### Middleware
- [ ] Logging middleware added
- [ ] Access control middleware implemented
- [ ] Rate limiting configured
- [ ] Error handling middleware added

### Testing
- [ ] Unit tests for tools
- [ ] Integration tests with Client
- [ ] Authentication tests
- [ ] Error handling tests

### Deployment
- [ ] Environment variables configured
- [ ] Docker containerization
- [ ] Health check endpoint
- [ ] Logging configured
- [ ] Monitoring set up

---

## References

- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/specification)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [FastMCP GitHub Repository](https://github.com/jlowin/fastmcp)

---

**Note:** This document is based on the latest FastMCP implementation and MCP Protocol specifications (2024-11-05 / 2025-06-18). Always refer to the official documentation for the most up-to-date information.
