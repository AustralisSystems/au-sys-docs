# Python & FastAPI Templatized Codebases: Foundational Scaffolding Best Practices 2025
**Version**: v1.0.0
**Last Updated**: 2025-01-14
**Python Version**: 3.9+
**FastAPI Version**: Latest
**Cookiecutter Version**: Latest

This document compiles the latest best practices for creating templatized codebases and foundational scaffolding applications for Python and FastAPI projects, based on official documentation, production code examples, and industry recommendations.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Template Structure](#template-structure)
3. [Variable System](#variable-system)
4. [Scaffolding Tools](#scaffolding-tools)
5. [Project Organization](#project-organization)
6. [Code Generation Patterns](#code-generation-patterns)
7. [FastAPI-Specific Scaffolding](#fastapi-specific-scaffolding)
8. [Template Best Practices](#template-best-practices)
9. [Testing Templates](#testing-templates)
10. [Documentation & Examples](#documentation--examples)

---

## Architecture Overview

### ✅ Template vs Scaffolding

**Template:** A reusable project structure with placeholders that can be instantiated multiple times.

**Scaffolding:** The process of generating a new project from a template with user-specific values.

### ✅ Core Components

```python
# Template structure
template-project/
├── {{cookiecutter.project_slug}}/     # Generated project directory
│   ├── app/
│   │   ├── main.py                    # FastAPI app
│   │   ├── config.py                  # Configuration
│   │   └── ...
│   ├── tests/
│   ├── requirements.txt
│   └── README.md
├── cookiecutter.json                  # Template variables
├── hooks/                             # Pre/post generation hooks
│   ├── pre_gen_project.py
│   └── post_gen_project.py
└── README.md                          # Template documentation
```

---

## Template Structure

### ✅ Best Practices

#### 1. Directory Organization

```
template-project/
├── {{cookiecutter.project_slug}}/     # Main template directory
│   ├── app/                           # Application code
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── api/                       # API routes
│   │   │   ├── __init__.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       └── endpoints/
│   │   ├── core/                      # Core functionality
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   ├── models/                    # Database models
│   │   │   ├── __init__.py
│   │   │   └── base.py
│   │   ├── schemas/                   # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   └── base.py
│   │   ├── services/                  # Business logic
│   │   │   ├── __init__.py
│   │   │   └── base.py
│   │   └── db/                        # Database
│   │       ├── __init__.py
│   │       ├── base.py
│   │       └── session.py
│   ├── tests/                         # Tests
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   └── test_api/
│   ├── alembic/                       # Migrations
│   │   └── versions/
│   ├── scripts/                       # Utility scripts
│   ├── docs/                          # Documentation
│   ├── .env.example                   # Environment template
│   ├── .gitignore
│   ├── pyproject.toml                 # Project config
│   ├── requirements.txt               # Dependencies
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── README.md
├── cookiecutter.json                  # Template variables
├── hooks/                             # Generation hooks
│   ├── pre_gen_project.py
│   └── post_gen_project.py
└── README.md                          # Template docs
```

#### 2. File Naming Conventions

```python
# Use template variables in filenames
{{cookiecutter.project_slug}}/
├── {{cookiecutter.app_name}}/
│   └── main.py
├── tests/
│   └── test_{{cookiecutter.app_name}}.py
└── {{cookiecutter.project_slug}}.py
```

---

## Variable System

### ✅ Best Practices

#### 1. cookiecutter.json Structure

```json
{
  "project_name": "My FastAPI Project",
  "project_slug": "{{ cookiecutter.project_name.lower().replace(' ', '-') }}",
  "app_name": "{{ cookiecutter.project_slug }}",
  "author_name": "Your Name",
  "author_email": "your.email@example.com",
  "description": "A FastAPI application",
  "version": "0.1.0",
  "python_version": "3.11",
  "use_postgres": "yes",
  "use_redis": "no",
  "use_docker": "yes",
  "use_github_actions": "yes",
  "license": "MIT",
  "_extensions": ["jinja2_time.TimeExtension"],
  "_copy_without_render": [
    "*.pyc",
    "__pycache__",
    "*.db"
  ]
}
```

#### 2. Variable Naming Conventions

```json
{
  "project_name": "Human-readable name",
  "project_slug": "URL-safe identifier",
  "package_name": "Python package name",
  "author_name": "Author full name",
  "author_email": "Author email",
  "description": "Project description",
  "version": "Semantic version",
  "python_version": "Python version",
  "use_<feature>": "yes/no flags",
  "database": "postgres|sqlite|mysql",
  "license": "MIT|Apache|GPL"
}
```

#### 3. Conditional Variables

```json
{
  "use_postgres": "yes",
  "use_redis": "no",
  "database_url": "{% if cookiecutter.use_postgres == 'yes' %}postgresql://...{% else %}sqlite:///...{% endif %}"
}
```

---

## Scaffolding Tools

### ✅ Best Practices

#### 1. Cookiecutter

```python
# Programmatic usage
from cookiecutter.main import cookiecutter

# Generate from local template
cookiecutter('cookiecutter-fastapi/')

# Generate from GitHub
cookiecutter('gh:audreyfeldroy/cookiecutter-fastapi')

# Generate with extra context
cookiecutter(
    'cookiecutter-fastapi/',
    extra_context={
        'project_name': 'My API',
        'use_postgres': 'yes'
    },
    no_input=True  # Use defaults
)

# Replay previous generation
cookiecutter('cookiecutter-fastapi/', replay=True)
```

#### 2. Template Configuration

```json
{
  "project_name": "My FastAPI Project",
  "project_slug": "{{ cookiecutter.project_name.lower().replace(' ', '-') }}",
  "app_name": "{{ cookiecutter.project_slug }}",
  "author_name": "Your Name",
  "author_email": "your.email@example.com",
  "description": "A FastAPI application",
  "version": "0.1.0",
  "python_version": "3.11",
  "use_postgres": "yes",
  "use_redis": "no",
  "use_docker": "yes",
  "use_github_actions": "yes",
  "license": "MIT"
}
```

#### 3. Pre-Generation Hooks

```python
# hooks/pre_gen_project.py
import sys
import re

def validate_project_name(project_name: str) -> bool:
    """Validate project name."""
    if not re.match(r'^[a-zA-Z0-9_-]+$', project_name):
        print(f"ERROR: Project name '{project_name}' contains invalid characters")
        print("Project name must contain only letters, numbers, underscores, and hyphens")
        return False
    return True

def validate_python_version(version: str) -> bool:
    """Validate Python version."""
    if not re.match(r'^3\.(9|10|11|12)$', version):
        print(f"ERROR: Python version '{version}' is not supported")
        print("Supported versions: 3.9, 3.10, 3.11, 3.12")
        return False
    return True

# Get variables from cookiecutter
project_name = "{{ cookiecutter.project_name }}"
python_version = "{{ cookiecutter.python_version }}"

# Validate
if not validate_project_name(project_name):
    sys.exit(1)

if not validate_python_version(python_version):
    sys.exit(1)

print(f"✓ Project name '{project_name}' is valid")
print(f"✓ Python version '{python_version}' is supported")
```

#### 4. Post-Generation Hooks

```python
# hooks/post_gen_project.py
import os
import subprocess
import sys

def run_command(command: str, cwd: str = None) -> bool:
    """Run a shell command."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {e.stderr}")
        return False

def initialize_git_repo(project_dir: str) -> bool:
    """Initialize git repository."""
    if not run_command("git init", cwd=project_dir):
        return False

    if not run_command("git add .", cwd=project_dir):
        return False

    if not run_command('git commit -m "Initial commit from template"', cwd=project_dir):
        return False

    return True

def create_virtual_environment(project_dir: str) -> bool:
    """Create virtual environment."""
    python_version = "{{ cookiecutter.python_version }}"
    venv_path = os.path.join(project_dir, "venv")

    if not run_command(f"python{python_version} -m venv venv", cwd=project_dir):
        return False

    return True

# Get project directory
project_dir = os.getcwd()

# Initialize git
if "{{ cookiecutter.use_git }}" == "yes":
    print("Initializing git repository...")
    initialize_git_repo(project_dir)

# Create virtual environment
if "{{ cookiecutter.create_venv }}" == "yes":
    print("Creating virtual environment...")
    create_virtual_environment(project_dir)

print("✓ Project generation complete!")
print(f"✓ Project directory: {project_dir}")
print("\nNext steps:")
print("1. cd into the project directory")
print("2. Activate virtual environment: source venv/bin/activate")
print("3. Install dependencies: pip install -r requirements.txt")
print("4. Run the application: uvicorn app.main:app --reload")
```

---

## Project Organization

### ✅ Best Practices

#### 1. FastAPI Project Structure

```
{{cookiecutter.project_slug}}/
├── app/
│   ├── __init__.py
│   ├── main.py                        # FastAPI app
│   ├── config.py                      # Configuration
│   ├── api/                           # API routes
│   │   ├── __init__.py
│   │   ├── deps.py                    # Dependencies
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── api.py                 # API router
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── items.py
│   │           └── users.py
│   ├── core/                          # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py                  # Settings
│   │   ├── security.py                # Security utilities
│   │   └── database.py               # Database setup
│   ├── models/                        # SQLAlchemy models
│   │   ├── __init__.py
│   │   └── base.py
│   ├── schemas/                       # Pydantic schemas
│   │   ├── __init__.py
│   │   └── base.py
│   ├── services/                      # Business logic
│   │   ├── __init__.py
│   │   └── base.py
│   └── db/                            # Database
│       ├── __init__.py
│       ├── base.py
│       └── session.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_api/
│       ├── __init__.py
│       └── test_endpoints.py
├── alembic/
│   └── versions/
├── scripts/
├── docs/
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

#### 2. Template Files

```python
# app/main.py template
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.api import api_router

app = FastAPI(
    title="{{ cookiecutter.project_name }}",
    description="{{ cookiecutter.description }}",
    version="{{ cookiecutter.version }}",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# CORS middleware
if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include API router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "Welcome to {{ cookiecutter.project_name }}",
        "version": "{{ cookiecutter.version }}"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

```python
# app/core/config.py template
from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    """Application settings."""

    # Application
    PROJECT_NAME: str = "{{ cookiecutter.project_name }}"
    VERSION: str = "{{ cookiecutter.version }}"
    DEBUG: bool = False

    # API
    API_V1_PREFIX: str = "/api/v1"

    # CORS
    CORS_ORIGINS: List[str] = []

    # Database
    {% if cookiecutter.use_postgres == "yes" %}
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/dbname"
    {% else %}
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"
    {% endif %}

    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    {% if cookiecutter.use_redis == "yes" %}
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    {% endif %}

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

---

## Code Generation Patterns

### ✅ Best Practices

#### 1. Conditional Code Generation

```python
# app/db/session.py template
{% if cookiecutter.use_postgres == "yes" %}
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
{% else %}
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
{% endif %}
```

#### 2. Feature Flag Generation

```python
# app/core/features.py template
from enum import Enum

class FeatureFlags:
    """Feature flags for the application."""

    {% if cookiecutter.use_postgres == "yes" %}
    POSTGRES_ENABLED = True
    {% else %}
    POSTGRES_ENABLED = False
    {% endif %}

    {% if cookiecutter.use_redis == "yes" %}
    REDIS_ENABLED = True
    {% else %}
    REDIS_ENABLED = False
    {% endif %}

    {% if cookiecutter.use_docker == "yes" %}
    DOCKER_ENABLED = True
    {% else %}
    DOCKER_ENABLED = False
    {% endif %}
```

#### 3. Dependency Generation

```txt
# requirements.txt template
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0

{% if cookiecutter.use_postgres == "yes" %}
sqlalchemy==2.0.23
asyncpg==0.29.0
alembic==1.12.1
{% else %}
sqlalchemy==2.0.23
aiosqlite==0.19.0
alembic==1.12.1
{% endif %}

{% if cookiecutter.use_redis == "yes" %}
redis==5.0.1
hiredis==2.2.3
{% endif %}

# Development
pytest==7.4.3
pytest-asyncio==0.21.1
black==23.11.0
isort==5.12.0
flake8==6.1.0
mypy==1.7.1
```

---

## FastAPI-Specific Scaffolding

### ✅ Best Practices

#### 1. API Router Template

```python
# app/api/v1/api.py template
from fastapi import APIRouter

from app.api.v1.endpoints import items, users

api_router = APIRouter()

{% if cookiecutter.include_items_api == "yes" %}
api_router.include_router(items.router, prefix="/items", tags=["items"])
{% endif %}

{% if cookiecutter.include_users_api == "yes" %}
api_router.include_router(users.router, prefix="/users", tags=["users"])
{% endif %}
```

#### 2. Endpoint Template

```python
# app/api/v1/endpoints/items.py template
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from app.services.item import ItemService

router = APIRouter()

@router.get("/", response_model=list[ItemResponse])
async def list_items(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all items."""
    service = ItemService(db)
    return await service.list_items(skip=skip, limit=limit)

@router.post("/", response_model=ItemResponse, status_code=201)
async def create_item(
    item: ItemCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new item."""
    service = ItemService(db)
    return await service.create_item(item)

@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get item by ID."""
    service = ItemService(db)
    item = await service.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    item: ItemUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update item."""
    service = ItemService(db)
    updated = await service.update_item(item_id, item)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated

@router.delete("/{item_id}", status_code=204)
async def delete_item(
    item_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete item."""
    service = ItemService(db)
    success = await service.delete_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
```

#### 3. Service Template

```python
# app/services/item.py template
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate

class ItemService:
    """Item service."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_items(self, skip: int = 0, limit: int = 100):
        """List items."""
        result = await self.db.execute(
            select(Item).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def get_item(self, item_id: int):
        """Get item by ID."""
        result = await self.db.execute(
            select(Item).where(Item.id == item_id)
        )
        return result.scalar_one_or_none()

    async def create_item(self, item: ItemCreate):
        """Create item."""
        db_item = Item(**item.dict())
        self.db.add(db_item)
        await self.db.commit()
        await self.db.refresh(db_item)
        return db_item

    async def update_item(self, item_id: int, item: ItemUpdate):
        """Update item."""
        db_item = await self.get_item(item_id)
        if not db_item:
            return None

        for key, value in item.dict(exclude_unset=True).items():
            setattr(db_item, key, value)

        await self.db.commit()
        await self.db.refresh(db_item)
        return db_item

    async def delete_item(self, item_id: int):
        """Delete item."""
        db_item = await self.get_item(item_id)
        if not db_item:
            return False

        await self.db.delete(db_item)
        await self.db.commit()
        return True
```

---

## Template Best Practices

### ✅ Best Practices

#### 1. Keep Templates DRY

```python
# Use includes for repeated patterns
# templates/_base_endpoint.py.jinja
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.{{ model_name }} import {{ ModelName }}Create, {{ ModelName }}Update, {{ ModelName }}Response
from app.services.{{ model_name }} import {{ ModelName }}Service

router = APIRouter()

@router.get("/", response_model=list[{{ ModelName }}Response])
async def list_{{ model_name }}s(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all {{ model_name }}s."""
    service = {{ ModelName }}Service(db)
    return await service.list_{{ model_name }}s(skip=skip, limit=limit)
```

#### 2. Provide Sensible Defaults

```json
{
  "project_name": "My FastAPI Project",
  "project_slug": "{{ cookiecutter.project_name.lower().replace(' ', '-') }}",
  "python_version": "3.11",
  "use_postgres": "yes",
  "use_redis": "no",
  "use_docker": "yes"
}
```

#### 3. Validate Inputs

```python
# hooks/pre_gen_project.py
import sys
import re

def validate_project_slug(slug: str) -> bool:
    """Validate project slug."""
    if not re.match(r'^[a-z0-9-]+$', slug):
        print(f"ERROR: Project slug '{slug}' is invalid")
        print("Project slug must be lowercase and contain only letters, numbers, and hyphens")
        return False
    return True

project_slug = "{{ cookiecutter.project_slug }}"
if not validate_project_slug(project_slug):
    sys.exit(1)
```

#### 4. Document Template Variables

```markdown
# Template Variables

## Required Variables

- `project_name`: Human-readable project name
- `project_slug`: URL-safe project identifier (auto-generated from project_name)
- `author_name`: Author full name
- `author_email`: Author email address

## Optional Variables

- `use_postgres`: Enable PostgreSQL support (yes/no, default: yes)
- `use_redis`: Enable Redis support (yes/no, default: no)
- `use_docker`: Include Docker files (yes/no, default: yes)
- `python_version`: Python version (3.9/3.10/3.11/3.12, default: 3.11)
```

---

## Testing Templates

### ✅ Best Practices

#### 1. Template Testing

```python
# tests/test_template.py
import pytest
from cookiecutter.main import cookiecutter
import tempfile
import shutil
from pathlib import Path

def test_template_generation():
    """Test template generation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Generate project
        cookiecutter(
            'cookiecutter-fastapi/',
            extra_context={
                'project_name': 'Test Project',
                'project_slug': 'test-project',
                'use_postgres': 'yes',
                'use_redis': 'no'
            },
            output_dir=tmpdir,
            no_input=True
        )

        project_dir = Path(tmpdir) / 'test-project'

        # Verify structure
        assert (project_dir / 'app' / 'main.py').exists()
        assert (project_dir / 'app' / 'config.py').exists()
        assert (project_dir / 'tests').exists()
        assert (project_dir / 'requirements.txt').exists()

        # Verify content
        main_content = (project_dir / 'app' / 'main.py').read_text()
        assert 'Test Project' in main_content
```

#### 2. Integration Testing

```python
# tests/test_generated_project.py
import subprocess
import sys
from pathlib import Path

def test_generated_project_imports():
    """Test that generated project imports work."""
    project_dir = Path(__file__).parent.parent / 'test-project'

    # Install dependencies
    subprocess.run(
        [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
        cwd=project_dir,
        check=True
    )

    # Test imports
    result = subprocess.run(
        [sys.executable, '-c', 'import app.main'],
        cwd=project_dir,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
```

---

## Documentation & Examples

### ✅ Best Practices

#### 1. Template README

```markdown
# FastAPI Project Template

A production-ready FastAPI project template with best practices.

## Features

- FastAPI with async/await
- SQLAlchemy with async support
- Pydantic v2 for validation
- Alembic for migrations
- Pytest for testing
- Docker support
- GitHub Actions CI/CD

## Usage

```bash
cookiecutter gh:your-org/cookiecutter-fastapi
```

## Template Variables

See [VARIABLES.md](VARIABLES.md) for complete variable documentation.

## Examples

See [examples/](examples/) for example projects generated from this template.
```

#### 2. Example Projects

```
template-project/
├── examples/
│   ├── minimal-api/
│   │   └── README.md
│   ├── full-stack-app/
│   │   └── README.md
│   └── microservice/
│       └── README.md
```

---

## Summary Checklist

### Template Structure
- [ ] Clear directory organization
- [ ] Consistent naming conventions
- [ ] Template variables properly used
- [ ] Conditional code generation

### Variables
- [ ] Sensible defaults provided
- [ ] Input validation in hooks
- [ ] Variable documentation
- [ ] Conditional variables

### Scaffolding Tools
- [ ] Cookiecutter configured
- [ ] Pre-generation hooks
- [ ] Post-generation hooks
- [ ] Template testing

### FastAPI-Specific
- [ ] Project structure follows FastAPI best practices
- [ ] API router organization
- [ ] Dependency injection patterns
- [ ] Service layer patterns
- [ ] Database session management

### Documentation
- [ ] Template README
- [ ] Variable documentation
- [ ] Usage examples
- [ ] Generated project README

---

## References

- [Cookiecutter Documentation](https://cookiecutter.readthedocs.io/)
- [FastAPI Best Practices](./fastapi-best-practices-2025.md)
- [Python Project Structure Best Practices](https://docs.python-guide.org/writing/structure/)

---

**Note:** This document is based on latest best practices for templatized codebases and scaffolding applications. Always refer to official documentation for the most up-to-date information.
