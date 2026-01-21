# UFC App Integration Addendum
**For**: CODE_IMPLEMENTATION_SPEC_2026-01-21_Unified_Storage_Refactor.md
**Date**: 2026-01-21
**Purpose**: UFC App Blueprint v1.1.0 Integration Requirements

---

## UFC App Integration Requirements

### Mandatory Compliance Checklist
- [ ] **IPlugin Protocol**: Implement `manifest/plugin.py` with proper interface signature
- [ ] **Dependency Declaration**: Declare `provides` attribute listing provided interfaces
- [ ] **Provider Registration**: Register storage providers in DI container during initialize()
- [ ] **Configuration Schema**: Provide `au_sys_unified_storage_settings.yaml` template
- [ ] **Observability Integration**: Use ILogger protocol, emit metrics/traces via OpenTelemetry
- [ ] **Lifecycle Hooks**: Implement initialize(), startup(), shutdown() with proper async
- [ ] **Type Safety**: 100% mypy compliance for container injection signatures
- [ ] **Discovery Pattern**: Package name must be `au_sys_*` for auto-discovery
- [ ] **Entry Point**: Register plugin in pyproject.toml [project.entry-points."au_sys_plugins"]
- [ ] **Zero Host Dependencies**: No imports from consumer applications

---

## Plugin Implementation Template

```python
"""Unified Storage Plugin for au_sys_ufc_app."""
from typing import Dict, Any, List, TYPE_CHECKING
from fastapi import FastAPI

if TYPE_CHECKING:
    from au_sys_ufc_app.core.logging import ILogger
    from au_sys_ufc_app.core.observability import IObservabilityProvider
    from au_sys_ufc_app.manifest.container import DIContainer

class UnifiedStoragePlugin:
    """Unified storage capability plugin."""

    # Declare provided interfaces for intelligent loader
    provides: List[str] = [
        "IStorageProvider",
        "IKVStorageProvider",
        "IDocumentStorageProvider",
        "StorageFactory"
    ]

    async def initialize(
        self,
        app: FastAPI,
        container: "DIContainer",
        logger: "ILogger",
        observability: "IObservabilityProvider",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Initialize plugin and register providers.

        Args:
            app: FastAPI application instance
            container: DI container for provider registration
            logger: Structured logger instance (ILogger protocol)
            observability: Observability provider for metrics/traces
            **kwargs: Additional configuration

        Returns:
            Dict of initialized components for other plugins
        """
        # Import here to avoid circular dependencies
        from ..core.services.factory import StorageFactory
        from ..core.storage.providers.sqlite_kv_provider import SQLiteKVProvider
        from ..core.storage.providers.mongodb_provider import MongoDBProvider

        # Get configuration from kwargs or container
        config = kwargs.get("config", {}).get("storage", {})

        # Create providers
        logger.info("initializing_storage_providers", provider_count=2)

        factory = StorageFactory(logger=logger)
        sqlite_provider = SQLiteKVProvider(
            logger=logger,
            db_path=config.get("sqlite", {}).get("database_path", "data/storage.db")
        )
        mongo_provider = MongoDBProvider(
            logger=logger,
            connection_url=config.get("mongodb", {}).get("connection_url")
        )

        # Register in container for other plugins to consume
        container.register("IStorageProvider", sqlite_provider, lifetime="singleton")
        container.register("IKVStorageProvider", sqlite_provider, lifetime="singleton")
        container.register("IDocumentStorageProvider", mongo_provider, lifetime="singleton")
        container.register("StorageFactory", factory, lifetime="singleton")

        # Emit metrics
        observability.increment_counter(
            "plugin_initialized_total",
            {"plugin": "unified_storage"}
        )

        logger.info(
            "unified_storage_plugin_initialized",
            providers=["SQLite", "MongoDB"],
            registered_interfaces=self.provides
        )

        # Return for direct access if needed
        return {
            "factory": factory,
            "sqlite_provider": sqlite_provider,
            "mongo_provider": mongo_provider
        }

    async def startup(self) -> None:
        """
        Execute startup logic after all plugins loaded.

        Use for:
        - Database connection establishment
        - Cache warming
        - Health checks
        """
        # Connect to databases
        # await self.sqlite_provider.connect()
        # await self.mongo_provider.connect()
        pass

    async def shutdown(self) -> None:
        """
        Cleanup resources on application shutdown.

        Use for:
        - Close database connections
        - Flush buffers
        - Release resources
        """
        # Close connections
        # await self.sqlite_provider.disconnect()
        # await self.mongo_provider.disconnect()
        pass
```

---

## Configuration Template

Create `src/au_sys_unified_storage/config/au_sys/au_sys_unified_storage_settings.yaml`:

```yaml
# Unified Storage Configuration
# Ejectable via: python -m au_sys_unified_storage.scripts.au_sys_scaffold.config

storage:
  # Default provider to use
  default_provider: "sqlite"  # Options: sqlite | mongodb

  # SQLite Configuration
  sqlite:
    database_path: "data/storage.db"
    connection_pool_size: 5
    enable_wal: true  # Write-Ahead Logging for better concurrency
    timeout_seconds: 30

  # MongoDB Configuration
  mongodb:
    # Use environment variable with fallback
    connection_url: "${MONGODB_URL:mongodb://localhost:27017}"
    database_name: "unified_storage"
    max_pool_size: 10
    min_pool_size: 1
    timeout_ms: 5000
    retry_writes: true

  # Performance Tuning
  performance:
    query_timeout_seconds: 30
    batch_size: 100
    cache_ttl_seconds: 300
    enable_query_cache: true

  # Observability
  observability:
    log_queries: false  # Set true for debugging
    emit_query_metrics: true
    trace_operations: true
```

---

## Entry Point Registration

Add to `pyproject.toml`:

```toml
[project.entry-points."au_sys_plugins"]
unified_storage = "au_sys_unified_storage.manifest.plugin:UnifiedStoragePlugin"
```

---

## Integration Test Suite

Create `tests/test_ufc_app_integration.py`:

```python
"""UFC App integration tests."""
import pytest
from au_sys_ufc_app.manifest.plugin_loader import discover_plugins, load_plugin
from au_sys_ufc_app.manifest.container import DIContainer
from au_sys_ufc_app.core.logging import StructlogLogger


@pytest.mark.asyncio
async def test_plugin_discovery():
    """Test plugin is discoverable by au_sys_ufc_app."""
    plugins = discover_plugins()
    plugin_names = [p["name"] for p in plugins]

    assert "au_sys_unified_storage" in plugin_names


@pytest.mark.asyncio
async def test_plugin_loading():
    """Test plugin loads successfully."""
    container = DIContainer()
    logger = StructlogLogger()

    result = await load_plugin(
        "au_sys_unified_storage",
        container,
        logger=logger
    )

    assert result is not None
    assert "factory" in result


@pytest.mark.asyncio
async def test_provider_registration():
    """Test providers registered in container."""
    container = DIContainer()
    logger = StructlogLogger()

    await load_plugin("au_sys_unified_storage", container, logger=logger)

    # Verify providers registered
    assert container.is_registered("IStorageProvider")
    assert container.is_registered("StorageFactory")

    # Resolve providers
    provider = container.resolve("IStorageProvider")
    assert provider is not None


@pytest.mark.asyncio
async def test_cross_plugin_injection():
    """Test provider can be injected into another plugin."""
    container = DIContainer()
    logger = StructlogLogger()

    # Load storage plugin
    await load_plugin("au_sys_unified_storage", container, logger=logger)

    # Simulate another plugin requesting storage
    storage = container.resolve("IStorageProvider")

    # Should get same instance (singleton)
    storage2 = container.resolve("IStorageProvider")
    assert storage is storage2


def test_configuration_schema():
    """Test configuration schema valid."""
    from au_sys_unified_storage.manifest.config import UnifiedStorageConfig

    config = UnifiedStorageConfig(
        default_provider="sqlite",
        sqlite={"database_path": "data/test.db"}
    )

    assert config.default_provider == "sqlite"
    assert config.sqlite.database_path == "data/test.db"
```

---

## Validation Commands

```bash
# 1. Plugin Discovery Test
python -c "from au_sys_ufc_app.manifest.plugin_loader import discover_plugins; print([p['name'] for p in discover_plugins()])"
# Expected: List contains 'au_sys_unified_storage'

# 2. Entry Point Verification
python -c "from importlib.metadata import entry_points; eps = entry_points(); print([ep.name for ep in eps.select(group='au_sys_plugins')])"
# Expected: List contains 'unified_storage'

# 3. Plugin Load Test
python -c "
from au_sys_unified_storage.manifest.plugin import UnifiedStoragePlugin
plugin = UnifiedStoragePlugin()
print(plugin.provides)
"
# Expected: List of provided interfaces

# 4. Type Safety Check
mypy --strict src/au_sys_unified_storage/manifest/plugin.py
# Expected: Success: no issues found

# 5. Import Chain Test
python -c "
from au_sys_unified_storage.manifest.plugin import UnifiedStoragePlugin
from au_sys_unified_storage.core.services.factory import StorageFactory
from au_sys_unified_storage.core.storage.providers.sqlite_kv_provider import SQLiteKVProvider
print('✅ All imports successful')
"
```

---

## Success Criteria for UFC App Integration

- [ ] Plugin discoverable: `discover_plugins()` returns package
- [ ] Plugin loadable: `load_plugin()` executes without errors
- [ ] Providers registered: Container has all declared providers
- [ ] Dependency injection works: Other plugins can resolve providers
- [ ] Configuration tiering functional: Settings loaded from hierarchy
- [ ] Observability integrated: Logs/metrics/traces emit correctly
- [ ] Type safety verified: Mypy strict passes
- [ ] Cross-package compatible: Works with other au_sys_* packages
- [ ] No circular dependencies: Topological sort succeeds
- [ ] Lifecycle hooks functional: initialize/startup/shutdown execute

---

## Common Integration Issues & Solutions

### Issue 1: Plugin Not Discovered
**Symptom**: `discover_plugins()` doesn't list package
**Cause**: Package name doesn't match `au_sys_*` pattern
**Solution**: Ensure package name starts with `au_sys_`

### Issue 2: Import Errors During Load
**Symptom**: Plugin loading fails with ImportError
**Cause**: Absolute imports instead of relative
**Solution**: Use relative imports: `from ..core.services import factory`

### Issue 3: Type Errors in Container
**Symptom**: Mypy errors on container.resolve()
**Cause**: Missing type annotations in initialize()
**Solution**: Add proper type hints, use TYPE_CHECKING imports

### Issue 4: Configuration Not Found
**Symptom**: Plugin can't read configuration
**Cause**: Config file not in expected location
**Solution**: Place in `config/au_sys/au_sys_unified_storage_settings.yaml`

### Issue 5: Circular Dependencies
**Symptom**: Topological sort fails
**Cause**: Plugin depends on itself indirectly
**Solution**: Review `provides` list, ensure no self-references

---

This addendum provides all necessary details for achieving 100% UFC App compatibility.
