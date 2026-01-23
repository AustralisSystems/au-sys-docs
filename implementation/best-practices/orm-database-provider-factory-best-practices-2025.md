# ORM Database Provider & Factory Best Practices 2025
**Version**: v1.0.0
**Last Updated**: 2025-01-14
**Python Version**: 3.9+
**SQLAlchemy Version**: 2.0+
**Beanie Version**: Latest
**FastAPI Version**: Latest

This document compiles the latest best practices for building ORM database providers and factory patterns in Python/FastAPI applications based on official documentation, production code examples, and community recommendations.

---

## Table of Contents

1. [Architecture Principles](#architecture-principles)
2. [Factory Pattern](#factory-pattern)
3. [Database Provider Interfaces](#database-provider-interfaces)
4. [SQLAlchemy Provider](#sqlalchemy-provider)
5. [Beanie Provider (MongoDB)](#beanie-provider-mongodb)
6. [Connection Pooling](#connection-pooling)
7. [Async Patterns](#async-patterns)
8. [Multi-Tier Database Architecture](#multi-tier-database-architecture)
9. [Migration Management](#migration-management)
10. [FastAPI Integration](#fastapi-integration)
11. [Performance Optimization](#performance-optimization)
12. [Testing](#testing)

---

## Architecture Principles

### ✅ Core Design Principles

#### 1. Unified Factory Pattern (Recommended)

```python
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, Optional, Type

class DatabaseType(str, Enum):
    """Database tiers for different application concerns."""
    PRIMARY = "PRIMARY"      # Main application data
    USERS = "USERS"          # User accounts and profiles
    AUDIT = "AUDIT"          # Audit logs and compliance
    CACHE = "CACHE"          # Caching layer
    EMBEDDINGS = "EMBEDDINGS" # Vector embeddings for AI/ML
    GRAPH = "GRAPH"          # Graph database for relationships

class DatabaseFactory:
    """
    Unified factory for ALL database providers (SQL, NoSQL, Vector, Graph).

    Best Practice: Single factory with interface segregation (ISP).
    """

    _providers: Dict[str, Type[BaseDatabaseProvider]] = {
        # SQL databases (via SQLAlchemy ORM)
        'postgresql': SQLAlchemyProvider,
        'mysql': SQLAlchemyProvider,
        'sqlite': SQLAlchemyProvider,

        # NoSQL databases (ORM)
        'mongodb': BeanieProvider,

        # NoSQL databases (Raw)
        'mongodb_raw': MongoDBRawProvider,
        'redis': RedisProvider,
        'tinydb': TinyDBProvider,
    }

    _tier_instances: Dict[str, BaseDatabaseProvider] = {}

    @classmethod
    def create_provider(
        cls,
        provider_type: str,
        database_tier: DatabaseType,
        config: Optional[Dict[str, Any]] = None,
        use_orm: bool = True
    ) -> BaseDatabaseProvider:
        """
        Create database provider for specific tier.

        Args:
            provider_type: Database type (postgresql, mongodb, redis, etc.)
            database_tier: Database tier (PRIMARY, USERS, AUDIT, etc.)
            config: Optional configuration override
            use_orm: Whether to use ORM provider (if available)

        Returns:
            Configured database provider instance

        Examples:
            # PostgreSQL for users
            db = DatabaseFactory.create_provider('postgresql', DatabaseType.USERS)

            # MongoDB for documents
            db = DatabaseFactory.create_provider('mongodb', DatabaseType.PRIMARY)

            # Redis for caching
            cache = DatabaseFactory.create_provider('redis', DatabaseType.CACHE)
        """
        # Check tier instance cache
        tier_key = f"{provider_type}_{database_tier.value}"
        if tier_key in cls._tier_instances:
            return cls._tier_instances[tier_key]

        # Get provider class
        provider_class = cls._providers.get(provider_type)
        if not provider_class:
            raise ValueError(f"Unknown provider type: {provider_type}")

        # Load tier-specific configuration
        if config is None:
            config = cls._load_tier_config(provider_type, database_tier)

        # Create and cache provider instance
        provider = provider_class(config)
        cls._tier_instances[tier_key] = provider

        return provider

    @classmethod
    def _load_tier_config(
        cls,
        provider_type: str,
        tier: DatabaseType
    ) -> Dict[str, Any]:
        """Load tier-specific configuration."""
        # Load from environment or config file
        # Example: PRIMARY_POSTGRESQL_URL, USERS_POSTGRESQL_URL, etc.
        config_key = f"{tier.value}_{provider_type.upper()}_URL"
        url = os.getenv(config_key)

        if not url:
            raise ValueError(f"Configuration not found for {config_key}")

        return {
            "url": url,
            "tier": tier.value,
            "provider_type": provider_type
        }
```

**Why Unified Factory?**
- ✅ **DRY**: Factory logic in one place
- ✅ **KISS**: One factory to learn
- ✅ **OCP**: Easy to add new providers
- ✅ **DIP**: Application depends on abstraction, not concrete factories

#### 2. Interface Segregation (ISP)

```python
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Dict, Any

T = TypeVar('T')

class BaseDatabaseProvider(ABC):
    """Base interface for all database providers."""

    @abstractmethod
    async def connect(self) -> None:
        """Establish database connection."""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Close database connection."""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Check database health."""
        pass

class BaseORMProvider(BaseDatabaseProvider, Generic[T]):
    """ORM-specific interface (SQLAlchemy, Beanie)."""

    @abstractmethod
    async def create(self, model: Type[T], data: Dict[str, Any]) -> T:
        """Create record using ORM."""
        pass

    @abstractmethod
    async def get(self, model: Type[T], filters: Dict[str, Any]) -> Optional[T]:
        """Get single record."""
        pass

    @abstractmethod
    async def get_many(
        self,
        model: Type[T],
        filters: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[T]:
        """Get multiple records."""
        pass

    @abstractmethod
    async def update(
        self,
        model: Type[T],
        filters: Dict[str, Any],
        data: Dict[str, Any]
    ) -> Optional[T]:
        """Update record."""
        pass

    @abstractmethod
    async def delete(self, model: Type[T], filters: Dict[str, Any]) -> bool:
        """Delete record."""
        pass

class BaseRawProvider(BaseDatabaseProvider):
    """Raw driver interface (Redis, MongoDB motor)."""

    @abstractmethod
    async def execute(self, query: str, params: Optional[Dict] = None) -> Any:
        """Execute raw query."""
        pass
```

---

## Factory Pattern

### ✅ Best Practices

#### 1. Singleton Factory with Caching

```python
import threading
from typing import Dict, Optional

class DatabaseFactory:
    """Thread-safe singleton factory with instance caching."""

    _instance = None
    _lock = threading.Lock()
    _tier_instances: Dict[str, BaseDatabaseProvider] = {}

    def __new__(cls):
        """Ensure singleton pattern."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def get_provider(
        self,
        provider_type: str,
        tier: DatabaseType
    ) -> BaseDatabaseProvider:
        """Get or create provider instance."""
        tier_key = f"{provider_type}_{tier.value}"

        if tier_key not in self._tier_instances:
            with self._lock:
                if tier_key not in self._tier_instances:
                    self._tier_instances[tier_key] = self._create_provider(
                        provider_type, tier
                    )

        return self._tier_instances[tier_key]
```

#### 2. Factory with Dependency Injection

```python
from typing import Callable, Optional

class DatabaseFactory:
    """Factory with configurable provider creation."""

    def __init__(
        self,
        provider_registry: Optional[Dict[str, Type[BaseDatabaseProvider]]] = None,
        config_loader: Optional[Callable] = None
    ):
        self._providers = provider_registry or self._default_providers
        self._config_loader = config_loader or self._default_config_loader

    def create_provider(
        self,
        provider_type: str,
        tier: DatabaseType
    ) -> BaseDatabaseProvider:
        """Create provider using injected dependencies."""
        provider_class = self._providers.get(provider_type)
        if not provider_class:
            raise ValueError(f"Unknown provider: {provider_type}")

        config = self._config_loader(provider_type, tier)
        return provider_class(config)
```

#### 3. Factory with Builder Pattern

```python
class DatabaseProviderBuilder:
    """Builder for configuring database providers."""

    def __init__(self):
        self._provider_type: Optional[str] = None
        self._tier: Optional[DatabaseType] = None
        self._config: Dict[str, Any] = {}

    def with_provider(self, provider_type: str) -> 'DatabaseProviderBuilder':
        """Set provider type."""
        self._provider_type = provider_type
        return self

    def with_tier(self, tier: DatabaseType) -> 'DatabaseProviderBuilder':
        """Set database tier."""
        self._tier = tier
        return self

    def with_config(self, config: Dict[str, Any]) -> 'DatabaseProviderBuilder':
        """Set configuration."""
        self._config.update(config)
        return self

    def build(self) -> BaseDatabaseProvider:
        """Build provider instance."""
        if not self._provider_type or not self._tier:
            raise ValueError("Provider type and tier required")

        return DatabaseFactory.create_provider(
            self._provider_type,
            self._tier,
            self._config
        )

# Usage
provider = (
    DatabaseProviderBuilder()
    .with_provider('postgresql')
    .with_tier(DatabaseType.USERS)
    .with_config({'pool_size': 10})
    .build()
)
```

---

## Database Provider Interfaces

### ✅ Best Practices

#### 1. Base Provider Interface

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from contextlib import asynccontextmanager

class BaseDatabaseProvider(ABC):
    """Base interface for all database providers."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._connected = False

    @abstractmethod
    async def connect(self) -> None:
        """Establish database connection."""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Close database connection."""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Check database health."""
        pass

    @property
    @abstractmethod
    def provider_type(self) -> str:
        """Return provider type."""
        pass

    @property
    def is_connected(self) -> bool:
        """Check if provider is connected."""
        return self._connected

    @asynccontextmanager
    async def connection(self):
        """Context manager for database connection."""
        if not self._connected:
            await self.connect()
        try:
            yield self
        finally:
            # Don't disconnect here - connection pooling
            pass
```

#### 2. ORM Provider Interface

```python
from typing import Generic, TypeVar, List, Optional, Dict, Any, Type
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class BaseORMProvider(BaseDatabaseProvider, Generic[T]):
    """ORM-specific provider interface."""

    @abstractmethod
    async def create(self, model: Type[T], data: Dict[str, Any]) -> T:
        """Create new record."""
        pass

    @abstractmethod
    async def get(
        self,
        model: Type[T],
        filters: Dict[str, Any]
    ) -> Optional[T]:
        """Get single record."""
        pass

    @abstractmethod
    async def get_many(
        self,
        model: Type[T],
        filters: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None
    ) -> List[T]:
        """Get multiple records."""
        pass

    @abstractmethod
    async def update(
        self,
        model: Type[T],
        filters: Dict[str, Any],
        data: Dict[str, Any]
    ) -> Optional[T]:
        """Update record."""
        pass

    @abstractmethod
    async def delete(
        self,
        model: Type[T],
        filters: Dict[str, Any]
    ) -> bool:
        """Delete record."""
        pass

    @abstractmethod
    async def count(
        self,
        model: Type[T],
        filters: Optional[Dict[str, Any]] = None
    ) -> int:
        """Count records."""
        pass

    @abstractmethod
    async def exists(
        self,
        model: Type[T],
        filters: Dict[str, Any]
    ) -> bool:
        """Check if record exists."""
        pass
```

---

## SQLAlchemy Provider

### ✅ Best Practices

#### 1. Async Engine Creation

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

class SQLAlchemyProvider(BaseORMProvider):
    """SQLAlchemy ORM provider."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self._engine: Optional[AsyncEngine] = None
        self._session_factory: Optional[sessionmaker] = None

    async def connect(self) -> None:
        """Create async engine and session factory."""
        url = self.config.get("url")
        if not url:
            raise ValueError("Database URL required")

        # Ensure async driver
        if not url.startswith(("postgresql+asyncpg", "mysql+aiomysql", "sqlite+aiosqlite")):
            url = url.replace("postgresql://", "postgresql+asyncpg://")
            url = url.replace("mysql://", "mysql+aiomysql://")
            url = url.replace("sqlite://", "sqlite+aiosqlite://")

        # Create async engine with connection pooling
        self._engine = create_async_engine(
            url,
            poolclass=QueuePool,
            pool_size=self.config.get("pool_size", 5),
            max_overflow=self.config.get("max_overflow", 10),
            pool_pre_ping=True,  # Verify connections before use
            pool_recycle=3600,   # Recycle connections after 1 hour
            echo=self.config.get("echo", False),
            future=True
        )

        # Create session factory
        self._session_factory = sessionmaker(
            self._engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

        self._connected = True

    async def disconnect(self) -> None:
        """Close engine and dispose of connections."""
        if self._engine:
            await self._engine.dispose()
        self._connected = False
```

#### 2. Session Management

```python
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession

class SQLAlchemyProvider(BaseORMProvider):
    """SQLAlchemy provider with session management."""

    @asynccontextmanager
    async def get_session(self) -> AsyncSession:
        """Get database session."""
        if not self._session_factory:
            raise RuntimeError("Provider not connected")

        async with self._session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    async def create(self, model: Type[T], data: Dict[str, Any]) -> T:
        """Create record."""
        async with self.get_session() as session:
            instance = model(**data)
            session.add(instance)
            await session.flush()
            await session.refresh(instance)
            return instance

    async def get(
        self,
        model: Type[T],
        filters: Dict[str, Any]
    ) -> Optional[T]:
        """Get single record."""
        async with self.get_session() as session:
            query = session.query(model)
            for key, value in filters.items():
                query = query.filter(getattr(model, key) == value)
            result = await session.execute(query)
            return result.scalar_one_or_none()
```

#### 3. Query Optimization

```python
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

class SQLAlchemyProvider(BaseORMProvider):
    """SQLAlchemy provider with query optimization."""

    async def get_with_relations(
        self,
        model: Type[T],
        filters: Dict[str, Any],
        relations: List[str]
    ) -> Optional[T]:
        """Get record with eager-loaded relations."""
        async with self.get_session() as session:
            query = select(model)

            # Add filters
            for key, value in filters.items():
                query = query.where(getattr(model, key) == value)

            # Eager load relations
            for relation in relations:
                query = query.options(selectinload(getattr(model, relation)))

            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def get_many_optimized(
        self,
        model: Type[T],
        filters: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
        relations: Optional[List[str]] = None
    ) -> List[T]:
        """Get multiple records with optimizations."""
        async with self.get_session() as session:
            query = select(model)

            # Apply filters
            if filters:
                for key, value in filters.items():
                    query = query.where(getattr(model, key) == value)

            # Order by
            if order_by:
                query = query.order_by(getattr(model, order_by))

            # Eager load relations
            if relations:
                for relation in relations:
                    query = query.options(selectinload(getattr(model, relation)))

            # Pagination
            if offset:
                query = query.offset(offset)
            if limit:
                query = query.limit(limit)

            result = await session.execute(query)
            return result.scalars().all()
```

---

## Beanie Provider (MongoDB)

### ✅ Best Practices

#### 1. Beanie Initialization

```python
from beanie import init_beanie, Document
from pymongo import AsyncMongoClient
from typing import List, Type

class BeanieProvider(BaseORMProvider):
    """Beanie ODM provider for MongoDB."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self._client: Optional[AsyncMongoClient] = None
        self._database = None
        self._document_models: List[Type[Document]] = []

    async def connect(self) -> None:
        """Initialize Beanie with MongoDB."""
        url = self.config.get("url")
        database_name = self.config.get("database_name")

        if not url or not database_name:
            raise ValueError("MongoDB URL and database name required")

        # Create async MongoDB client
        self._client = AsyncMongoClient(url)
        self._database = self._client[database_name]

        # Initialize Beanie
        await init_beanie(
            database=self._database,
            document_models=self._document_models,
            allow_index_dropping=False,
            skip_indexes=False
        )

        self._connected = True

    def register_models(self, models: List[Type[Document]]) -> None:
        """Register document models."""
        self._document_models.extend(models)

    async def disconnect(self) -> None:
        """Close MongoDB connection."""
        if self._client:
            self._client.close()
        self._connected = False
```

#### 2. Beanie CRUD Operations

```python
from beanie import Document
from typing import Type, List, Optional, Dict, Any

class BeanieProvider(BaseORMProvider):
    """Beanie provider with CRUD operations."""

    async def create(self, model: Type[T], data: Dict[str, Any]) -> T:
        """Create document."""
        instance = model(**data)
        await instance.insert()
        return instance

    async def get(
        self,
        model: Type[T],
        filters: Dict[str, Any]
    ) -> Optional[T]:
        """Get single document."""
        query = model.find(filters)
        return await query.first()

    async def get_many(
        self,
        model: Type[T],
        filters: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None
    ) -> List[T]:
        """Get multiple documents."""
        query = model.find(filters or {})

        if order_by:
            query = query.sort(order_by)

        if offset:
            query = query.skip(offset)

        if limit:
            query = query.limit(limit)

        return await query.to_list()

    async def update(
        self,
        model: Type[T],
        filters: Dict[str, Any],
        data: Dict[str, Any]
    ) -> Optional[T]:
        """Update document."""
        instance = await self.get(model, filters)
        if instance:
            for key, value in data.items():
                setattr(instance, key, value)
            await instance.save()
        return instance

    async def delete(
        self,
        model: Type[T],
        filters: Dict[str, Any]
    ) -> bool:
        """Delete document."""
        instance = await self.get(model, filters)
        if instance:
            await instance.delete()
            return True
        return False
```

---

## Connection Pooling

### ✅ Best Practices

#### 1. SQLAlchemy Connection Pooling

```python
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import QueuePool, NullPool, StaticPool

class SQLAlchemyProvider(BaseORMProvider):
    """SQLAlchemy provider with optimized connection pooling."""

    async def connect(self) -> None:
        """Create engine with connection pooling."""
        url = self.config.get("url")

        # Determine pool class based on database type
        pool_class = self._get_pool_class(url)

        self._engine = create_async_engine(
            url,
            poolclass=pool_class,
            pool_size=self.config.get("pool_size", 5),
            max_overflow=self.config.get("max_overflow", 10),
            pool_timeout=self.config.get("pool_timeout", 30),
            pool_pre_ping=True,  # Verify connections before use
            pool_recycle=3600,   # Recycle connections after 1 hour
            echo=self.config.get("echo", False)
        )

    def _get_pool_class(self, url: str):
        """Get appropriate pool class for database."""
        if "sqlite" in url:
            # SQLite: Use StaticPool for in-memory, NullPool for file
            if ":memory:" in url:
                return StaticPool
            return NullPool
        else:
            # PostgreSQL, MySQL: Use QueuePool
            return QueuePool
```

#### 2. Connection Pool Monitoring

```python
class SQLAlchemyProvider(BaseORMProvider):
    """SQLAlchemy provider with pool monitoring."""

    async def get_pool_status(self) -> Dict[str, Any]:
        """Get connection pool status."""
        if not self._engine:
            return {}

        pool = self._engine.pool
        return {
            "size": pool.size(),
            "checked_in": pool.checkedin(),
            "checked_out": pool.checkedout(),
            "overflow": pool.overflow(),
            "invalid": pool.invalid()
        }

    async def health_check(self) -> bool:
        """Check database health via connection pool."""
        try:
            async with self._engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            return True
        except Exception:
            return False
```

---

## Async Patterns

### ✅ Best Practices

#### 1. Async Context Managers

```python
from contextlib import asynccontextmanager

class BaseORMProvider(BaseDatabaseProvider):
    """Base ORM provider with async context managers."""

    @asynccontextmanager
    async def transaction(self):
        """Transaction context manager."""
        async with self.get_session() as session:
            async with session.begin():
                yield session

    async def create_with_transaction(
        self,
        model: Type[T],
        data: Dict[str, Any]
    ) -> T:
        """Create record within transaction."""
        async with self.transaction() as session:
            instance = model(**data)
            session.add(instance)
            await session.flush()
            return instance
```

#### 2. Async Batch Operations

```python
class SQLAlchemyProvider(BaseORMProvider):
    """SQLAlchemy provider with batch operations."""

    async def create_many(
        self,
        model: Type[T],
        data_list: List[Dict[str, Any]]
    ) -> List[T]:
        """Create multiple records efficiently."""
        async with self.get_session() as session:
            instances = [model(**data) for data in data_list]
            session.add_all(instances)
            await session.flush()
            return instances

    async def update_many(
        self,
        model: Type[T],
        filters: Dict[str, Any],
        data: Dict[str, Any]
    ) -> int:
        """Update multiple records."""
        async with self.get_session() as session:
            query = session.query(model)
            for key, value in filters.items():
                query = query.filter(getattr(model, key) == value)

            result = await session.execute(
                query.update(data, synchronize_session=False)
            )
            return result.rowcount
```

---

## Multi-Tier Database Architecture

### ✅ Best Practices

#### 1. Tier-Based Configuration

```python
from enum import Enum
from typing import Dict, Any

class DatabaseType(str, Enum):
    """Database tiers."""
    PRIMARY = "PRIMARY"
    USERS = "USERS"
    AUDIT = "AUDIT"
    CACHE = "CACHE"
    EMBEDDINGS = "EMBEDDINGS"
    GRAPH = "GRAPH"

class DatabaseFactory:
    """Factory with multi-tier support."""

    @classmethod
    def create_provider(
        cls,
        provider_type: str,
        tier: DatabaseType,
        config: Optional[Dict[str, Any]] = None
    ) -> BaseDatabaseProvider:
        """Create provider for specific tier."""
        # Load tier-specific configuration
        tier_config = cls._load_tier_config(provider_type, tier)

        # Merge with provided config
        if config:
            tier_config.update(config)

        # Create provider
        provider_class = cls._providers[provider_type]
        return provider_class(tier_config)

    @classmethod
    def _load_tier_config(
        cls,
        provider_type: str,
        tier: DatabaseType
    ) -> Dict[str, Any]:
        """Load tier-specific configuration."""
        # Example: PRIMARY_POSTGRESQL_URL, USERS_POSTGRESQL_URL
        env_key = f"{tier.value}_{provider_type.upper()}_URL"
        url = os.getenv(env_key)

        return {
            "url": url,
            "tier": tier.value,
            "pool_size": cls._get_tier_pool_size(tier),
            "max_overflow": cls._get_tier_max_overflow(tier)
        }

    @classmethod
    def _get_tier_pool_size(cls, tier: DatabaseType) -> int:
        """Get pool size for tier."""
        tier_pool_sizes = {
            DatabaseType.PRIMARY: 10,
            DatabaseType.USERS: 5,
            DatabaseType.AUDIT: 3,
            DatabaseType.CACHE: 20,
            DatabaseType.EMBEDDINGS: 5,
            DatabaseType.GRAPH: 5
        }
        return tier_pool_sizes.get(tier, 5)
```

---

## Migration Management

### ✅ Best Practices

#### 1. Alembic Integration (SQLAlchemy)

```python
from alembic import config as alembic_config
from alembic import script
from alembic.runtime.migration import MigrationContext

class SQLAlchemyProvider(BaseORMProvider):
    """SQLAlchemy provider with migration support."""

    async def run_migrations(self, revision: str = "head") -> None:
        """Run database migrations."""
        alembic_cfg = alembic_config.Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", self.config["url"])

        # Run migrations
        from alembic import command
        command.upgrade(alembic_cfg, revision)

    async def get_current_revision(self) -> Optional[str]:
        """Get current database revision."""
        async with self._engine.connect() as conn:
            context = MigrationContext.configure(await conn.get_sync_connection())
            return context.get_current_revision()
```

#### 2. Beanie Migrations

```python
from beanie import MigrationController

class BeanieProvider(BaseORMProvider):
    """Beanie provider with migration support."""

    async def run_migrations(self) -> None:
        """Run Beanie migrations."""
        controller = MigrationController(
            connection_uri=self.config["url"],
            database_name=self.config["database_name"]
        )
        await controller.run()
```

---

## FastAPI Integration

### ✅ Best Practices

#### 1. Dependency Injection

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

def get_db_session(
    provider: BaseORMProvider = Depends(get_database_provider)
) -> AsyncSession:
    """Dependency for database session."""
    return provider.get_session()

@app.get("/users/{user_id}")
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_db_session)
):
    """Get user endpoint."""
    user = await session.get(User, user_id)
    return user
```

#### 2. Lifespan Events

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup: Initialize database providers
    primary_db = DatabaseFactory.create_provider(
        'postgresql',
        DatabaseType.PRIMARY
    )
    await primary_db.connect()

    app.state.primary_db = primary_db

    yield

    # Shutdown: Disconnect providers
    await primary_db.disconnect()

app = FastAPI(lifespan=lifespan)
```

---

## Performance Optimization

### ✅ Best Practices

#### 1. Query Optimization

```python
# Avoid N+1 queries
# Bad
users = await session.query(User).all()
for user in users:
    posts = await session.query(Post).filter(Post.user_id == user.id).all()

# Good
users = await session.query(User).options(selectinload(User.posts)).all()
```

#### 2. Connection Pool Tuning

```python
# Production settings
engine = create_async_engine(
    url,
    pool_size=20,          # Base pool size
    max_overflow=10,        # Additional connections
    pool_timeout=30,        # Wait time for connection
    pool_pre_ping=True,     # Verify connections
    pool_recycle=3600       # Recycle after 1 hour
)
```

---

## Testing

### ✅ Best Practices

#### 1. Test Database Provider

```python
import pytest
from sqlalchemy.ext.asyncio import create_async_engine

@pytest.fixture
async def test_db_provider():
    """Test database provider fixture."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    provider = SQLAlchemyProvider({"url": str(engine.url)})
    await provider.connect()
    yield provider
    await provider.disconnect()

@pytest.mark.asyncio
async def test_create_user(test_db_provider):
    """Test user creation."""
    user_data = {"name": "Test User", "email": "test@example.com"}
    user = await test_db_provider.create(User, user_data)
    assert user.id is not None
```

---

## Summary Checklist

### Factory Pattern
- [ ] Unified factory for all database types
- [ ] Interface segregation (ORM vs Raw)
- [ ] Instance caching per tier
- [ ] Configuration-driven provider selection

### Provider Interfaces
- [ ] Base provider interface
- [ ] ORM provider interface
- [ ] Raw provider interface
- [ ] Clear method contracts

### SQLAlchemy
- [ ] Async engine creation
- [ ] Connection pooling configured
- [ ] Session management
- [ ] Query optimization
- [ ] Migration support

### Beanie
- [ ] Async initialization
- [ ] Document model registration
- [ ] CRUD operations
- [ ] Migration support

### Connection Pooling
- [ ] Appropriate pool class selected
- [ ] Pool size configured
- [ ] Pool monitoring
- [ ] Health checks

### FastAPI Integration
- [ ] Dependency injection
- [ ] Lifespan events
- [ ] Session management
- [ ] Error handling

---

## References

- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Beanie Documentation](https://beanie-odm.dev/)
- [FastAPI Database Documentation](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)

---

**Note:** This document is based on Python 3.9+, SQLAlchemy 2.0+, Beanie latest, and FastAPI latest. Always refer to official documentation for the most up-to-date information.
