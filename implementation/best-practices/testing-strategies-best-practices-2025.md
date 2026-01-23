# Testing Strategies Best Practices

**Version**: v1.0.0  
**Last Updated**: 2025-01-14

This document provides comprehensive best practices for implementing testing strategies in FastAPI applications, covering unit testing, integration testing, async testing, test fixtures, mocking, coverage reporting, test organization, and CI/CD integration.

---

## Table of Contents

1. [Architecture Principles](#architecture-principles)
2. [Test Organization](#test-organization)
3. [Pytest Configuration](#pytest-configuration)
4. [Test Fixtures](#test-fixtures)
5. [Async Testing](#async-testing)
6. [FastAPI Testing](#fastapi-testing)
7. [Mocking and Stubbing](#mocking-and-stubbing)
8. [Test Coverage](#test-coverage)
9. [Test Markers and Parametrization](#test-markers-and-parametrization)
10. [Database Testing](#database-testing)
11. [API Testing](#api-testing)
12. [Performance Testing](#performance-testing)
13. [Test Data Management](#test-data-management)
14. [CI/CD Integration](#cicd-integration)
15. [Production Deployment](#production-deployment)

---

## Architecture Principles

### Test Pyramid

**REQUIRED**: Follow the test pyramid structure:

```
        /\
       /  \      E2E Tests (Few)
      /____\     
     /      \    Integration Tests (Some)
    /________\   
   /          \  Unit Tests (Many)
  /____________\
```

**Distribution**:
- **70% Unit Tests**: Fast, isolated, test individual functions/classes
- **20% Integration Tests**: Test component interactions
- **10% E2E Tests**: Test complete user workflows

### Test Isolation

**REQUIRED**: Ensure tests are independent and isolated:

```python
import pytest

# BAD: Tests depend on shared state
counter = 0

def test_increment():
    global counter
    counter += 1
    assert counter == 1

def test_decrement():
    global counter
    counter -= 1
    assert counter == 0  # Fails if test_increment ran first

# GOOD: Tests are isolated
def test_increment():
    counter = 0
    counter += 1
    assert counter == 1

def test_decrement():
    counter = 0
    counter -= 1
    assert counter == -1
```

### Test Naming Conventions

**REQUIRED**: Use descriptive test names:

```python
# BAD: Vague names
def test_user():
    pass

def test_api():
    pass

# GOOD: Descriptive names
def test_create_user_with_valid_data_returns_201():
    """Test that creating a user with valid data returns 201 Created."""
    pass

def test_get_user_by_id_returns_404_when_not_found():
    """Test that getting a non-existent user returns 404 Not Found."""
    pass

def test_update_user_with_invalid_email_returns_422():
    """Test that updating a user with invalid email returns 422 Validation Error."""
    pass
```

### Arrange-Act-Assert Pattern

**REQUIRED**: Structure tests using AAA pattern:

```python
def test_user_creation():
    # Arrange: Set up test data and dependencies
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepassword123"
    }
    db_session = create_test_db_session()
    
    # Act: Execute the code under test
    user = create_user(db_session, user_data)
    
    # Assert: Verify the results
    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "test@example.com"
```

---

## Test Organization

### Directory Structure

**REQUIRED**: Organize tests following this structure:

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures and configuration
├── unit/                    # Unit tests
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_utils.py
├── integration/             # Integration tests
│   ├── __init__.py
│   ├── test_api_integration.py
│   ├── test_database_integration.py
│   └── test_plugin_integration.py
├── e2e/                     # End-to-end tests
│   ├── __init__.py
│   └── test_user_workflows.py
├── fixtures/                # Test data fixtures
│   ├── __init__.py
│   ├── user_fixtures.py
│   └── database_fixtures.py
└── security/                # Security tests
    ├── __init__.py
    └── test_authentication.py
```

### Test File Naming

**REQUIRED**: Follow naming conventions:

- Test files: `test_*.py` or `*_test.py`
- Test classes: `Test*`
- Test functions: `test_*`

```python
# File: tests/unit/test_user_service.py

class TestUserService:
    """Test suite for UserService."""
    
    def test_create_user(self):
        """Test user creation."""
        pass
    
    def test_get_user_by_id(self):
        """Test retrieving user by ID."""
        pass
```

### conftest.py Organization

**REQUIRED**: Organize shared fixtures in conftest.py:

```python
# tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from typing import Generator

# Application fixtures
@pytest.fixture(scope="session")
def app():
    """Create FastAPI app for testing."""
    from main import app
    return app

@pytest.fixture
def client(app):
    """Create test client."""
    return TestClient(app)

# Database fixtures
@pytest.fixture
def db_session():
    """Create database session."""
    # Setup
    session = create_test_session()
    yield session
    # Teardown
    session.rollback()
    session.close()

# Mock fixtures
@pytest.fixture
def mock_external_service():
    """Mock external service."""
    with patch('services.external_service.call') as mock:
        yield mock
```

---

## Pytest Configuration

### pyproject.toml Configuration

**REQUIRED**: Configure pytest in pyproject.toml:

```toml
[tool.pytest.ini_options]
# Test discovery
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

# Markers
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "e2e: End-to-end tests",
    "slow: Slow running tests",
    "async: Async tests",
    "database: Tests requiring database",
    "security: Security tests",
]

# Output options
addopts = [
    "-v",                    # Verbose output
    "--strict-markers",      # Strict marker validation
    "--strict-config",       # Strict configuration validation
    "--tb=short",           # Short traceback format
    "-ra",                  # Show extra test summary info
]

# Coverage options
[tool.pytest.ini_options.addopts]
cov = ["src", "app"]
cov_report = ["term-missing", "html"]
cov_fail_under = 80
cov_branch = true

# Asyncio configuration
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"
asyncio_default_test_loop_scope = "function"

# Logging
log_cli = true
log_cli_level = "INFO"
log_cli_format = "%(asctime)s [%(levelname)8s] %(name)s: %(message)s"
log_cli_date_format = "%Y-%m-%d %H:%M:%S"
```

### pytest.ini Configuration (Alternative)

**ALTERNATIVE**: Use pytest.ini for configuration:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow running tests
    async: Async tests
    database: Tests requiring database
    security: Security tests

addopts =
    -v
    --strict-markers
    --strict-config
    --tb=short
    -ra
    --cov=src
    --cov=app
    --cov-report=term-missing
    --cov-report=html
    --cov-fail-under=80
    --cov-branch

asyncio_mode = auto
asyncio_default_fixture_loop_scope = function
asyncio_default_test_loop_scope = function

log_cli = true
log_cli_level = INFO
```

---

## Test Fixtures

### Fixture Scopes

**REQUIRED**: Use appropriate fixture scopes:

```python
import pytest

# Function scope (default): Created fresh for each test
@pytest.fixture
def function_scoped_fixture():
    """Fixture created for each test function."""
    return {"data": "function"}

# Class scope: Created once per test class
@pytest.fixture(scope="class")
def class_scoped_fixture():
    """Fixture created once per test class."""
    return {"data": "class"}

# Module scope: Created once per test module
@pytest.fixture(scope="module")
def module_scoped_fixture():
    """Fixture created once per test module."""
    return {"data": "module"}

# Package scope: Created once per package
@pytest.fixture(scope="package")
def package_scoped_fixture():
    """Fixture created once per package."""
    return {"data": "package"}

# Session scope: Created once per test session
@pytest.fixture(scope="session")
def session_scoped_fixture():
    """Fixture created once per test session."""
    return {"data": "session"}
```

### Fixture with Setup and Teardown

**REQUIRED**: Use yield for setup/teardown:

```python
import pytest
from typing import Generator

@pytest.fixture
def database_connection() -> Generator:
    """Database connection with cleanup."""
    # Setup
    conn = create_connection()
    conn.execute("BEGIN")
    
    yield conn
    
    # Teardown
    conn.execute("ROLLBACK")
    conn.close()

# Usage
def test_database_operation(database_connection):
    database_connection.execute("INSERT INTO users ...")
    # Teardown runs automatically after test
```

### Parametrized Fixtures

**REQUIRED**: Use parametrized fixtures for multiple test scenarios:

```python
import pytest

@pytest.fixture(params=["postgresql", "mysql", "sqlite"])
def database_type(request):
    """Parametrized fixture for different database types."""
    return request.param

def test_database_connection(database_type):
    """Test runs for each database type."""
    conn = connect_database(database_type)
    assert conn.is_connected()

# Apply marks to specific parameters
@pytest.fixture(params=[
    0,
    1,
    pytest.param(2, marks=pytest.mark.skip(reason="Not implemented")),
    pytest.param(3, marks=pytest.mark.xfail(reason="Known issue")),
])
def test_value(request):
    """Parametrized fixture with conditional marks."""
    return request.param
```

### Fixture Dependencies

**REQUIRED**: Use fixture dependencies properly:

```python
import pytest

@pytest.fixture
def database():
    """Database fixture."""
    return create_database()

@pytest.fixture
def user_service(database):  # Depends on database fixture
    """User service fixture depends on database."""
    return UserService(database)

@pytest.fixture
def authenticated_user(user_service):  # Depends on user_service
    """Authenticated user depends on user_service."""
    return user_service.create_user("testuser", "password")

def test_user_operation(authenticated_user):
    """Test uses authenticated_user which depends on other fixtures."""
    assert authenticated_user.username == "testuser"
```

### Autouse Fixtures

**RECOMMENDED**: Use autouse fixtures for automatic setup:

```python
import pytest

@pytest.fixture(autouse=True)
def reset_state():
    """Automatically reset state before each test."""
    # Setup
    reset_global_state()
    yield
    # Teardown
    cleanup_global_state()

# All tests automatically use this fixture
def test_one():
    # reset_state fixture runs automatically
    pass

def test_two():
    # reset_state fixture runs automatically
    pass
```

### Fixture Override

**RECOMMENDED**: Override fixtures in test modules:

```python
# tests/conftest.py
@pytest.fixture
def database():
    return create_production_database()

# tests/test_specific.py
@pytest.fixture
def database():  # Override conftest fixture
    return create_test_database()

def test_specific(database):
    """Uses test database, not production."""
    pass
```

---

## Async Testing

### Basic Async Tests

**REQUIRED**: Use pytest-asyncio for async tests:

```python
import pytest
import asyncio

@pytest.mark.asyncio
async def test_async_function():
    """Basic async test."""
    result = await async_function()
    assert result == expected_value

@pytest.mark.asyncio
async def test_multiple_async_operations():
    """Test multiple async operations."""
    task1 = asyncio.create_task(operation1())
    task2 = asyncio.create_task(operation2())
    
    results = await asyncio.gather(task1, task2)
    assert len(results) == 2
```

### Async Fixtures

**REQUIRED**: Use @pytest_asyncio.fixture for async fixtures:

```python
import pytest
import pytest_asyncio

@pytest_asyncio.fixture
async def async_database():
    """Async database fixture."""
    # Setup
    db = await create_async_database()
    yield db
    # Teardown
    await db.close()

@pytest_asyncio.fixture(scope="module")
async def shared_async_resource():
    """Module-scoped async fixture."""
    resource = await create_expensive_resource()
    yield resource
    await resource.cleanup()

@pytest.mark.asyncio
async def test_with_async_fixture(async_database):
    """Test using async fixture."""
    result = await async_database.query("SELECT 1")
    assert result == 1
```

### Event Loop Scopes

**RECOMMENDED**: Configure event loop scopes:

```python
import pytest

# Function scope (default): New loop for each test
@pytest.mark.asyncio
async def test_function_scope():
    """Runs in function-scoped event loop."""
    await async_operation()

# Module scope: Shared loop for all tests in module
pytestmark = pytest.mark.asyncio(loop_scope="module")

async def test_module_scope_one():
    """Runs in module-scoped event loop."""
    await async_operation()

async def test_module_scope_two():
    """Runs in same module-scoped event loop."""
    await async_operation()

# Class scope: Shared loop for all tests in class
@pytest.mark.asyncio(loop_scope="class")
class TestClassScoped:
    async def test_one(self):
        """Runs in class-scoped event loop."""
        await async_operation()
    
    async def test_two(self):
        """Runs in same class-scoped event loop."""
        await async_operation()
```

### Async Context Managers

**REQUIRED**: Use async context managers in tests:

```python
import pytest
from contextlib import asynccontextmanager

@asynccontextmanager
async def async_resource():
    """Async context manager."""
    resource = await create_resource()
    try:
        yield resource
    finally:
        await resource.cleanup()

@pytest.mark.asyncio
async def test_with_async_context():
    """Test using async context manager."""
    async with async_resource() as resource:
        result = await resource.operation()
        assert result is not None
```

---

## FastAPI Testing

### TestClient for Synchronous Tests

**REQUIRED**: Use TestClient for synchronous API tests:

```python
from fastapi.testclient import TestClient
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

# Test
client = TestClient(app)

def test_read_item():
    """Test GET endpoint with TestClient."""
    response = client.get("/items/42?q=test")
    assert response.status_code == 200
    assert response.json() == {"item_id": 42, "q": "test"}

def test_read_item_invalid():
    """Test validation error."""
    response = client.get("/items/invalid")
    assert response.status_code == 422  # Validation error
```

### AsyncClient for Async Tests

**REQUIRED**: Use AsyncClient for async API tests:

```python
import pytest
from httpx import AsyncClient
from fastapi import FastAPI

app = FastAPI()

@pytest.mark.asyncio
async def test_async_endpoint():
    """Test async endpoint with AsyncClient."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/items/42")
        assert response.status_code == 200
        assert response.json()["item_id"] == 42
```

### Dependency Overrides

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
    return db.get_items()

# Test with dependency override
def get_test_database():
    """Test database dependency."""
    return get_test_db()

app.dependency_overrides[get_database] = get_test_database

client = TestClient(app)

def test_read_items():
    """Test with overridden dependency."""
    response = client.get("/items/")
    assert response.status_code == 200
    # Uses test database, not production

# Cleanup
def teardown():
    app.dependency_overrides.clear()
```

### Testing Lifespan Events

**REQUIRED**: Test lifespan events properly:

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.state.database = await connect_database()
    yield
    # Shutdown
    await app.state.database.close()

app = FastAPI(lifespan=lifespan)

# Test lifespan events
def test_lifespan_events():
    """Test that lifespan events run."""
    with TestClient(app) as client:
        # Startup events run automatically
        assert hasattr(app.state, "database")
        response = client.get("/items/")
        assert response.status_code == 200
    # Shutdown events run automatically when exiting 'with' block
```

### Testing WebSockets

**REQUIRED**: Test WebSocket endpoints:

```python
from fastapi import FastAPI, WebSocket
from fastapi.testclient import TestClient

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

# Test WebSocket
def test_websocket():
    """Test WebSocket endpoint."""
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        websocket.send_text("Hello")
        data = websocket.receive_text()
        assert data == "Message text was: Hello"
```

---

## Mocking and Stubbing

### unittest.mock Basics

**REQUIRED**: Use unittest.mock for mocking:

```python
from unittest.mock import Mock, MagicMock, patch, AsyncMock
import pytest

def test_with_mock():
    """Test with Mock object."""
    mock_service = Mock()
    mock_service.get_data.return_value = {"key": "value"}
    
    result = use_service(mock_service)
    assert result == {"key": "value"}
    mock_service.get_data.assert_called_once()

@pytest.mark.asyncio
async def test_with_async_mock():
    """Test with AsyncMock."""
    mock_service = AsyncMock()
    mock_service.fetch_data.return_value = {"key": "value"}
    
    result = await use_service(mock_service)
    assert result == {"key": "value"}
    await mock_service.fetch_data.assert_called_once()
```

### patch Decorator

**REQUIRED**: Use patch decorator for mocking:

```python
from unittest.mock import patch
import pytest

@patch('module.external_service')
def test_with_patch_decorator(mock_service):
    """Test with patch decorator."""
    mock_service.call.return_value = "mocked"
    
    result = function_using_service()
    assert result == "mocked"

@patch('module.external_service.call')
@patch('module.another_service.fetch')
def test_multiple_patches(mock_fetch, mock_call):
    """Test with multiple patches."""
    mock_call.return_value = "call_result"
    mock_fetch.return_value = "fetch_result"
    
    result = function_using_services()
    assert result == "combined"
```

### patch Context Manager

**REQUIRED**: Use patch as context manager:

```python
from unittest.mock import patch

def test_with_patch_context():
    """Test with patch context manager."""
    with patch('module.external_service') as mock_service:
        mock_service.call.return_value = "mocked"
        
        result = function_using_service()
        assert result == "mocked"
    
    # Patch is automatically removed after 'with' block
```

### pytest-httpx for HTTP Mocking

**REQUIRED**: Use pytest-httpx for HTTP request mocking:

```python
import pytest
import httpx
from pytest_httpx import HTTPXMock

def test_http_request(httpx_mock: HTTPXMock):
    """Test HTTP request with pytest-httpx."""
    httpx_mock.add_response(
        url="https://api.example.com/data",
        json={"key": "value"},
        status_code=200
    )
    
    response = httpx.get("https://api.example.com/data")
    assert response.status_code == 200
    assert response.json() == {"key": "value"}

@pytest.mark.asyncio
async def test_async_http_request(httpx_mock: HTTPXMock):
    """Test async HTTP request."""
    httpx_mock.add_response(
        url="https://api.example.com/data",
        json={"key": "value"}
    )
    
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
        assert response.json() == {"key": "value"}
```

### Dynamic Mock Responses

**RECOMMENDED**: Use callbacks for dynamic responses:

```python
import httpx
from pytest_httpx import HTTPXMock

def test_dynamic_response(httpx_mock: HTTPXMock):
    """Test with dynamic response callback."""
    def custom_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={"url": str(request.url), "method": request.method}
        )
    
    httpx_mock.add_callback(custom_response)
    
    response = httpx.get("https://api.example.com/data")
    assert response.json()["method"] == "GET"
```

### Mock Assertions

**REQUIRED**: Assert mock calls:

```python
from unittest.mock import Mock, call

def test_mock_assertions():
    """Test mock call assertions."""
    mock_service = Mock()
    
    use_service(mock_service, "arg1", "arg2")
    
    # Assert called
    mock_service.method.assert_called()
    
    # Assert called once
    mock_service.method.assert_called_once()
    
    # Assert called with specific arguments
    mock_service.method.assert_called_with("arg1", "arg2")
    
    # Assert called once with arguments
    mock_service.method.assert_called_once_with("arg1", "arg2")
    
    # Assert call count
    assert mock_service.method.call_count == 1
    
    # Assert multiple calls
    mock_service.method.assert_has_calls([
        call("arg1", "arg2"),
        call("arg3", "arg4")
    ])
```

---

## Test Coverage

### Coverage Configuration

**REQUIRED**: Configure coverage in pyproject.toml:

```toml
[tool.coverage.run]
branch = true
source = ["src", "app"]
omit = [
    "*/tests/*",
    "*/migrations/*",
    "*/__pycache__/*",
    "*/venv/*",
    "*/env/*",
]

[tool.coverage.report]
precision = 2
show_missing = true
skip_covered = false
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "@abstractmethod",
]

[tool.coverage.html]
directory = "htmlcov"
show_contexts = true
```

### Coverage Reporting

**REQUIRED**: Generate multiple coverage reports:

```bash
# Terminal report with missing lines
pytest --cov=src --cov=app --cov-report=term-missing

# HTML report
pytest --cov=src --cov=app --cov-report=html

# XML report for CI/CD
pytest --cov=src --cov=app --cov-report=xml:coverage.xml

# Multiple reports
pytest --cov=src --cov=app \
    --cov-report=term-missing \
    --cov-report=html:htmlcov \
    --cov-report=xml:coverage.xml \
    --cov-report=json:coverage.json
```

### Coverage Thresholds

**REQUIRED**: Enforce coverage thresholds:

```bash
# Fail if coverage below threshold
pytest --cov=src --cov=app --cov-fail-under=80

# Configure in pyproject.toml
[tool.pytest.ini_options]
addopts = [
    "--cov-fail-under=80",
]
```

### Per-Test Coverage Contexts

**RECOMMENDED**: Track per-test coverage:

```bash
# Enable per-test coverage tracking
pytest --cov=src --cov=app --cov-context=test

# View in HTML report
pytest --cov=src --cov=app --cov-context=test --cov-report=html
```

### Coverage Branch Analysis

**REQUIRED**: Enable branch coverage:

```bash
# Enable branch coverage
pytest --cov=src --cov=app --cov-branch

# Configure in pyproject.toml
[tool.coverage.run]
branch = true
```

---

## Test Markers and Parametrization

### Custom Markers

**REQUIRED**: Define and use custom markers:

```python
import pytest

@pytest.mark.unit
def test_unit_function():
    """Unit test marked with @pytest.mark.unit."""
    pass

@pytest.mark.integration
def test_integration_function():
    """Integration test marked with @pytest.mark.integration."""
    pass

@pytest.mark.slow
def test_slow_function():
    """Slow test marked with @pytest.mark.slow."""
    pass

# Run specific markers
# pytest -m unit          # Run only unit tests
# pytest -m "not slow"    # Run all except slow tests
# pytest -m "unit and not slow"  # Run unit tests that are not slow
```

### Parametrization

**REQUIRED**: Use parametrization for multiple test cases:

```python
import pytest

@pytest.mark.parametrize("input_value,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_multiply_by_two(input_value, expected):
    """Test runs for each parameter set."""
    assert input_value * 2 == expected

@pytest.mark.parametrize("status_code", [200, 201, 204])
def test_status_codes(status_code):
    """Test different status codes."""
    response = client.get(f"/endpoint/{status_code}")
    assert response.status_code == status_code

# Parametrize with marks
@pytest.mark.parametrize("value", [
    1,
    2,
    pytest.param(3, marks=pytest.mark.skip(reason="Not implemented")),
    pytest.param(4, marks=pytest.mark.xfail(reason="Known issue")),
])
def test_with_marks(value):
    """Parametrized test with conditional marks."""
    assert value > 0
```

### Parametrized Fixtures

**RECOMMENDED**: Combine parametrization with fixtures:

```python
import pytest

@pytest.fixture(params=["postgresql", "mysql", "sqlite"])
def database(request):
    """Parametrized database fixture."""
    return create_database(request.param)

@pytest.mark.parametrize("user_type", ["admin", "user", "guest"])
def test_user_access(database, user_type):
    """Test runs for each database and user type combination."""
    user = create_user(database, user_type)
    assert user.has_access()
```

---

## Database Testing

### Database Fixtures

**REQUIRED**: Create database fixtures with transactions:

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

@pytest.fixture(scope="session")
def test_engine():
    """Create test database engine."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    return engine

@pytest.fixture(scope="session")
def test_session_factory(test_engine):
    """Create session factory."""
    Base.metadata.create_all(test_engine)
    return sessionmaker(bind=test_engine)

@pytest.fixture
def db_session(test_session_factory):
    """Create database session with transaction rollback."""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = test_session_factory(bind=connection)
    
    yield session
    
    # Rollback transaction
    session.close()
    transaction.rollback()
    connection.close()
```

### Database Testing Patterns

**REQUIRED**: Use transaction rollback for isolation:

```python
import pytest

@pytest.fixture
def db_session():
    """Database session with automatic rollback."""
    session = create_session()
    transaction = session.begin()
    
    yield session
    
    # Rollback after test
    transaction.rollback()
    session.close()

def test_create_user(db_session):
    """Test user creation with automatic rollback."""
    user = create_user(db_session, "testuser", "password")
    assert user.id is not None
    # Transaction automatically rolled back after test
```

### Test Data Factories

**RECOMMENDED**: Use factories for test data:

```python
import factory
from factory.alchemy import SQLAlchemyModelFactory

class UserFactory(SQLAlchemyModelFactory):
    """Factory for creating test users."""
    class Meta:
        model = User
        sqlalchemy_session = None  # Set in fixture
    
    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.Faker("password")

# Usage in tests
def test_user_creation(db_session):
    """Test using factory."""
    UserFactory._meta.sqlalchemy_session = db_session
    user = UserFactory()
    assert user.username.startswith("user")
```

---

## API Testing

### Endpoint Testing

**REQUIRED**: Test all HTTP methods:

```python
from fastapi.testclient import TestClient

def test_get_endpoint(client: TestClient):
    """Test GET endpoint."""
    response = client.get("/items/42")
    assert response.status_code == 200
    assert response.json()["id"] == 42

def test_post_endpoint(client: TestClient):
    """Test POST endpoint."""
    response = client.post(
        "/items/",
        json={"name": "Item", "price": 10.0}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Item"

def test_put_endpoint(client: TestClient):
    """Test PUT endpoint."""
    response = client.put(
        "/items/42",
        json={"name": "Updated Item", "price": 20.0}
    )
    assert response.status_code == 200

def test_delete_endpoint(client: TestClient):
    """Test DELETE endpoint."""
    response = client.delete("/items/42")
    assert response.status_code == 204
```

### Authentication Testing

**REQUIRED**: Test authentication endpoints:

```python
def test_login_success(client: TestClient):
    """Test successful login."""
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_credentials(client: TestClient):
    """Test login with invalid credentials."""
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == 401

def test_protected_endpoint(client: TestClient):
    """Test protected endpoint."""
    # Login first
    login_response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "password123"}
    )
    token = login_response.json()["access_token"]
    
    # Access protected endpoint
    response = client.get(
        "/protected",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
```

### Error Response Testing

**REQUIRED**: Test error responses:

```python
def test_404_not_found(client: TestClient):
    """Test 404 Not Found response."""
    response = client.get("/items/99999")
    assert response.status_code == 404
    assert "detail" in response.json()

def test_422_validation_error(client: TestClient):
    """Test 422 Validation Error."""
    response = client.post(
        "/items/",
        json={"name": "Item"}  # Missing required field
    )
    assert response.status_code == 422
    assert "detail" in response.json()

def test_500_internal_error(client: TestClient):
    """Test 500 Internal Server Error."""
    with patch('services.external_service') as mock:
        mock.call.side_effect = Exception("Internal error")
        response = client.get("/endpoint")
        assert response.status_code == 500
```

---

## Performance Testing

### Benchmark Testing

**RECOMMENDED**: Use pytest-benchmark for performance tests:

```python
import pytest

def test_performance(benchmark):
    """Benchmark test."""
    result = benchmark(expensive_function, arg1, arg2)
    assert result is not None

# Run benchmarks
# pytest --benchmark-only
# pytest --benchmark-compare
```

### Load Testing

**RECOMMENDED**: Test under load:

```python
import pytest
import asyncio

@pytest.mark.asyncio
async def test_concurrent_requests():
    """Test concurrent request handling."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        tasks = [
            client.get("/items/1") for _ in range(100)
        ]
        responses = await asyncio.gather(*tasks)
        
        assert all(r.status_code == 200 for r in responses)
```

---

## Test Data Management

### Test Data Fixtures

**REQUIRED**: Organize test data in fixtures:

```python
import pytest

@pytest.fixture
def sample_user_data():
    """Sample user data fixture."""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepassword123"
    }

@pytest.fixture
def sample_users_data():
    """Multiple users data fixture."""
    return [
        {"username": "user1", "email": "user1@example.com"},
        {"username": "user2", "email": "user2@example.com"},
        {"username": "user3", "email": "user3@example.com"},
    ]

def test_with_sample_data(sample_user_data):
    """Test using sample data."""
    user = create_user(**sample_user_data)
    assert user.username == "testuser"
```

### Test Data Files

**RECOMMENDED**: Load test data from files:

```python
import json
import pytest
from pathlib import Path

@pytest.fixture
def test_data():
    """Load test data from JSON file."""
    data_file = Path(__file__).parent / "fixtures" / "test_data.json"
    with open(data_file) as f:
        return json.load(f)

def test_with_file_data(test_data):
    """Test using data from file."""
    user_data = test_data["user"]
    user = create_user(**user_data)
    assert user.username == user_data["username"]
```

---

## CI/CD Integration

### GitHub Actions Example

**REQUIRED**: Configure CI/CD for testing:

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-asyncio pytest-cov pytest-httpx
      
      - name: Run tests
        run: |
          pytest \
            --cov=src \
            --cov=app \
            --cov-report=xml \
            --cov-report=html \
            --cov-fail-under=80 \
            -v
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

### Test Execution Strategies

**REQUIRED**: Organize test execution:

```bash
# Run all tests
pytest

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run tests in parallel
pytest -n auto

# Run tests with coverage
pytest --cov=src --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_user_service.py

# Run specific test
pytest tests/unit/test_user_service.py::TestUserService::test_create_user

# Run tests matching pattern
pytest -k "test_user"

# Run tests with verbose output
pytest -v

# Run tests stopping at first failure
pytest -x

# Run tests with detailed output
pytest -vv
```

---

## Production Deployment

### Test Configuration Checklist

- [ ] pytest configured in pyproject.toml or pytest.ini
- [ ] Test markers defined and documented
- [ ] Coverage thresholds configured (minimum 80%)
- [ ] Async testing configured (pytest-asyncio)
- [ ] Test fixtures organized in conftest.py
- [ ] Database fixtures with transaction rollback
- [ ] HTTP mocking configured (pytest-httpx)
- [ ] Dependency overrides for testing
- [ ] Test data factories implemented
- [ ] CI/CD pipeline configured
- [ ] Test execution strategies defined
- [ ] Performance benchmarks configured
- [ ] Security tests implemented
- [ ] E2E tests implemented

### Best Practices Summary

1. **Test Organization**: Follow test pyramid (70% unit, 20% integration, 10% E2E)
2. **Test Isolation**: Ensure tests are independent and isolated
3. **Fixtures**: Use appropriate fixture scopes and organize in conftest.py
4. **Async Testing**: Use pytest-asyncio for async tests and fixtures
5. **FastAPI Testing**: Use TestClient for sync, AsyncClient for async
6. **Dependency Overrides**: Override dependencies for testing
7. **Mocking**: Use unittest.mock and pytest-httpx for HTTP mocking
8. **Coverage**: Enforce minimum coverage thresholds (80%+)
9. **Parametrization**: Use parametrization for multiple test cases
10. **CI/CD**: Integrate tests into CI/CD pipeline

---

## Summary

### Key Takeaways

1. **Test Pyramid**: Follow 70/20/10 distribution (unit/integration/E2E)
2. **Test Isolation**: Ensure tests are independent and isolated
3. **Fixtures**: Use appropriate scopes and organize in conftest.py
4. **Async Testing**: Use pytest-asyncio with proper event loop scopes
5. **FastAPI Testing**: Use TestClient and AsyncClient appropriately
6. **Dependency Overrides**: Override dependencies for testing
7. **Mocking**: Use unittest.mock and pytest-httpx for HTTP requests
8. **Coverage**: Enforce minimum thresholds and generate multiple reports
9. **Parametrization**: Use markers and parametrization for efficiency
10. **CI/CD**: Integrate comprehensive testing into CI/CD pipeline

### Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio Documentation](https://pytest-asyncio.readthedocs.io/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [pytest-httpx Documentation](https://pytest-httpx.readthedocs.io/)
- [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)

---

**Version**: v1.0.0  
**Last Updated**: 2025-01-14

