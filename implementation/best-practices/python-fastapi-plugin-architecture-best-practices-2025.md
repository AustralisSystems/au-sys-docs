# Python/FastAPI Plugin Architecture Best Practices 2025
**Version**: v1.0.0
**Last Updated**: 2025-01-14
**Python Version**: 3.9+
**FastAPI Version**: Latest

This document compiles the latest best practices for building plugin architectures in Python and FastAPI applications based on official documentation, production code examples, and community recommendations.

---

## Table of Contents

1. [Architecture Principles](#architecture-principles)
2. [Plugin Discovery](#plugin-discovery)
3. [Plugin Loading](#plugin-loading)
4. [Plugin Interfaces](#plugin-interfaces)
5. [Lifecycle Management](#lifecycle-management)
6. [Dependency Resolution](#dependency-resolution)
7. [Security & Isolation](#security--isolation)
8. [Plugin Registry](#plugin-registry)
9. [Hot Reload & Dynamic Loading](#hot-reload--dynamic-loading)
10. [Metadata Management](#metadata-management)
11. [FastAPI Integration](#fastapi-integration)
12. [Testing](#testing)
13. [Performance Optimization](#performance-optimization)

---

## Architecture Principles

### ✅ Core Design Principles

#### 1. SOLID Principles

```python
# Single Responsibility: Each plugin has one clear purpose
class DatabasePlugin(IPlugin):
    """Handles database operations only."""
    pass

# Open/Closed: Open for extension, closed for modification
class BasePlugin(IPlugin):
    """Base class that can be extended without modification."""
    pass

# Liskov Substitution: Plugins can be substituted
def process_plugin(plugin: IPlugin):
    """Works with any IPlugin implementation."""
    await plugin.initialize(context)

# Interface Segregation: Small, focused interfaces
class IWebPlugin(IPlugin):
    """Web-specific interface."""
    async def get_api_router(self) -> APIRouter:
        pass

# Dependency Inversion: Depend on abstractions
class PluginManager:
    def __init__(self, registry: IPluginRegistry):
        self._registry = registry  # Depend on interface, not concrete class
```

#### 2. DRY (Don't Repeat Yourself)

```python
# Shared base implementation
class BasePlugin(IPlugin):
    """Common functionality for all plugins."""

    def __init__(self, metadata: PluginMetadata):
        self._plugin_id = metadata.plugin_id
        self._version = metadata.version
        # Shared initialization logic

    async def initialize(self, context: PluginContext) -> None:
        """Common initialization pattern."""
        self._context = context
        await self._setup_logging()
        await self._validate_configuration()
        await self._custom_initialize(context)

    async def _custom_initialize(self, context: PluginContext) -> None:
        """Override in subclasses."""
        pass
```

#### 3. KISS (Keep It Simple)

```python
# Simple plugin interface
class IPlugin(ABC):
    """Minimal, clear interface."""

    @property
    @abstractmethod
    def plugin_id(self) -> str:
        pass

    @abstractmethod
    async def initialize(self, context: PluginContext) -> None:
        pass

    @abstractmethod
    async def start(self) -> None:
        pass

    @abstractmethod
    async def stop(self) -> None:
        pass
```

---

## Plugin Discovery

### ✅ Best Practices

#### 1. Entry Points Discovery (Recommended)

```python
from importlib.metadata import entry_points

class PluginDiscovery:
    """Discover plugins using setuptools entry points."""

    def discover_from_entry_points(self, group: str = "myapp.plugins") -> List[PluginMetadata]:
        """Discover plugins via entry points."""
        discovered = []

        try:
            for entry_point in entry_points(group=group):
                metadata = PluginMetadata(
                    plugin_id=entry_point.name,
                    name=entry_point.name,
                    version=self._get_version(entry_point),
                    entry_point=entry_point.value,
                    source="entry_point"
                )
                discovered.append(metadata)
        except Exception as e:
            logger.error(f"Entry point discovery failed: {e}")

        return discovered
```

**setup.py / pyproject.toml:**
```python
# setup.py
setup(
    name="my-plugin",
    entry_points={
        "myapp.plugins": [
            "my_plugin = my_plugin:MyPlugin",
        ],
    },
)

# pyproject.toml
[project.entry-points."myapp.plugins"]
my_plugin = "my_plugin:MyPlugin"
```

#### 2. File System Discovery

```python
import importlib.util
from pathlib import Path
from typing import List, Optional

class PluginDiscovery:
    """Discover plugins from file system."""

    def discover_from_directory(self, directory: Path) -> List[PluginMetadata]:
        """Discover plugins in directory."""
        discovered = []

        for plugin_path in directory.iterdir():
            if plugin_path.is_dir() and (plugin_path / "__init__.py").exists():
                metadata = self._discover_plugin_directory(plugin_path)
                if metadata:
                    discovered.append(metadata)
            elif plugin_path.suffix == ".py":
                metadata = self._discover_plugin_file(plugin_path)
                if metadata:
                    discovered.append(metadata)

        return discovered

    def _discover_plugin_directory(self, path: Path) -> Optional[PluginMetadata]:
        """Discover plugin from directory."""
        # Look for plugin.json or plugin.yaml
        metadata_file = self._find_metadata_file(path)
        if metadata_file:
            return self._load_metadata(metadata_file)

        # Try to load from __init__.py
        return self._discover_from_module(path / "__init__.py")
```

#### 3. Metadata File Discovery

```python
import json
import yaml
from pathlib import Path

class PluginDiscovery:
    """Discover plugins from metadata files."""

    METADATA_FILES = [
        "plugin.json",
        "plugin.yaml",
        "plugin.yml",
        "metadata.json",
    ]

    def discover_from_metadata(self, plugin_path: Path) -> Optional[PluginMetadata]:
        """Discover plugin from metadata file."""
        for metadata_file_name in self.METADATA_FILES:
            metadata_file = plugin_path / metadata_file_name
            if metadata_file.exists():
                return self._load_metadata_file(metadata_file)
        return None

    def _load_metadata_file(self, path: Path) -> Optional[PluginMetadata]:
        """Load metadata from file."""
        try:
            if path.suffix == ".json":
                with open(path) as f:
                    data = json.load(f)
            elif path.suffix in (".yaml", ".yml"):
                with open(path) as f:
                    data = yaml.safe_load(f)
            else:
                return None

            return PluginMetadata(**data)
        except Exception as e:
            logger.error(f"Failed to load metadata from {path}: {e}")
            return None
```

**plugin.json example:**
```json
{
    "plugin_id": "my_plugin",
    "name": "My Plugin",
    "version": "1.0.0",
    "description": "Plugin description",
    "author": "Author Name",
    "dependencies": ["plugin_a>=1.0.0", "plugin_b"],
    "optional_dependencies": ["plugin_c"],
    "entry_point": "my_plugin:MyPlugin",
    "security_level": "SANDBOXED",
    "required_permissions": ["READ_DATA", "WRITE_DATA"]
}
```

#### 4. Multi-Source Discovery

```python
class PluginDiscovery:
    """Discover plugins from multiple sources."""

    async def discover_all(
        self,
        entry_point_groups: List[str] = None,
        search_paths: List[Path] = None,
    ) -> List[PluginMetadata]:
        """Discover from all sources."""
        discovered = []

        # Entry points
        if entry_point_groups:
            for group in entry_point_groups:
                discovered.extend(self.discover_from_entry_points(group))

        # File system
        if search_paths:
            for path in search_paths:
                discovered.extend(self.discover_from_directory(path))

        # Deduplicate by plugin_id
        return self._deduplicate(discovered)

    def _deduplicate(self, plugins: List[PluginMetadata]) -> List[PluginMetadata]:
        """Remove duplicates, keeping first occurrence."""
        seen = set()
        unique = []
        for plugin in plugins:
            if plugin.plugin_id not in seen:
                seen.add(plugin.plugin_id)
                unique.append(plugin)
        return unique
```

---

## Plugin Loading

### ✅ Best Practices

#### 1. Dynamic Module Loading

```python
import importlib.util
import sys
from pathlib import Path
from typing import Optional, Type

class PluginLoader:
    """Load plugins dynamically."""

    def load_plugin_class(
        self,
        module_path: Path,
        class_name: str,
        module_name: Optional[str] = None
    ) -> Type[IPlugin]:
        """Load plugin class from file."""
        if module_name is None:
            module_name = f"plugin_{module_path.stem}"

        # Create module spec
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not create spec for {module_path}")

        # Load module
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        # Get plugin class
        plugin_class = getattr(module, class_name)
        if not issubclass(plugin_class, IPlugin):
            raise TypeError(f"{class_name} does not implement IPlugin")

        return plugin_class
```

#### 2. Entry Point Loading

```python
from importlib.metadata import entry_points

class PluginLoader:
    """Load plugins from entry points."""

    def load_from_entry_point(self, entry_point) -> IPlugin:
        """Load plugin from entry point."""
        try:
            # Load the plugin class
            plugin_class = entry_point.load()

            if not issubclass(plugin_class, IPlugin):
                raise TypeError(f"{entry_point.name} does not implement IPlugin")

            # Instantiate plugin
            return plugin_class()
        except Exception as e:
            raise PluginLoadError(f"Failed to load {entry_point.name}: {e}")
```

#### 3. Safe Loading with Error Handling

```python
class PluginLoader:
    """Safe plugin loading with error handling."""

    def load_plugin_safe(
        self,
        plugin_id: str,
        metadata: PluginMetadata
    ) -> Optional[IPlugin]:
        """Load plugin with comprehensive error handling."""
        try:
            # Validate plugin structure
            if not self._validate_plugin_structure(metadata):
                logger.warning(f"Invalid structure for {plugin_id}")
                return None

            # Load plugin class
            plugin_class = self._load_plugin_class(metadata)

            # Instantiate
            plugin = plugin_class()

            # Verify interface compliance
            if not isinstance(plugin, IPlugin):
                raise TypeError(f"{plugin_id} does not implement IPlugin")

            return plugin

        except ImportError as e:
            logger.error(f"Import error for {plugin_id}: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to load {plugin_id}: {e}", exc_info=True)
            return None
```

#### 4. Lazy Loading

```python
class PluginLoader:
    """Lazy loading of plugins."""

    def __init__(self):
        self._loaded_classes: Dict[str, Type[IPlugin]] = {}
        self._loaded_instances: Dict[str, IPlugin] = {}

    def get_plugin_class(self, plugin_id: str) -> Type[IPlugin]:
        """Get plugin class (lazy load if needed)."""
        if plugin_id not in self._loaded_classes:
            metadata = self._registry.get_metadata(plugin_id)
            self._loaded_classes[plugin_id] = self._load_class(metadata)
        return self._loaded_classes[plugin_id]

    def get_plugin_instance(self, plugin_id: str) -> IPlugin:
        """Get plugin instance (lazy load if needed)."""
        if plugin_id not in self._loaded_instances:
            plugin_class = self.get_plugin_class(plugin_id)
            self._loaded_instances[plugin_id] = plugin_class()
        return self._loaded_instances[plugin_id]
```

---

## Plugin Interfaces

### ✅ Best Practices

#### 1. Core Interface

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from enum import Enum

class PluginStatus(str, Enum):
    """Plugin status enumeration."""
    UNLOADED = "unloaded"
    LOADED = "loaded"
    INITIALIZED = "initialized"
    STARTED = "started"
    STOPPED = "stopped"
    ERROR = "error"

class IPlugin(ABC):
    """Core plugin interface."""

    @property
    @abstractmethod
    def plugin_id(self) -> str:
        """Unique plugin identifier."""
        pass

    @property
    @abstractmethod
    def plugin_name(self) -> str:
        """Human-readable plugin name."""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """Plugin version."""
        pass

    @property
    @abstractmethod
    def status(self) -> PluginStatus:
        """Current plugin status."""
        pass

    @abstractmethod
    async def initialize(self, context: PluginContext) -> None:
        """Initialize plugin."""
        pass

    @abstractmethod
    async def start(self) -> None:
        """Start plugin operations."""
        pass

    @abstractmethod
    async def stop(self) -> None:
        """Stop plugin operations."""
        pass

    @abstractmethod
    async def shutdown(self) -> None:
        """Shutdown and cleanup."""
        pass
```

#### 2. Interface Segregation

```python
# Web plugin interface
class IWebPlugin(IPlugin):
    """Plugin that provides web routes."""

    @abstractmethod
    async def get_api_router(self) -> APIRouter:
        """Get FastAPI router."""
        pass

    @abstractmethod
    async def get_static_mounts(self) -> List[StaticMount]:
        """Get static file mounts."""
        pass

# Event plugin interface
class IEventPlugin(IPlugin):
    """Plugin that handles events."""

    @abstractmethod
    async def handle_event(self, event: PluginEvent) -> EventResult:
        """Handle plugin event."""
        pass

    @abstractmethod
    def get_subscribed_events(self) -> List[str]:
        """Get list of subscribed event types."""
        pass

# Configurable plugin interface
class IConfigurablePlugin(IPlugin):
    """Plugin with configuration."""

    @abstractmethod
    async def configure(self, config: Dict[str, Any]) -> ConfigurationResult:
        """Configure plugin."""
        pass

    @abstractmethod
    def get_configuration_schema(self) -> Dict[str, Any]:
        """Get configuration schema."""
        pass

# Health monitoring interface
class IPluginHealth(IPlugin):
    """Plugin with health monitoring."""

    @abstractmethod
    async def health_check(self) -> HealthCheck:
        """Perform health check."""
        pass

    @abstractmethod
    def get_metrics(self) -> PerformanceMetrics:
        """Get performance metrics."""
        pass
```

#### 3. Composite Interfaces

```python
class IWebConfigurablePlugin(IWebPlugin, IConfigurablePlugin):
    """Plugin that provides web routes and configuration."""
    pass

# Usage
class MyPlugin(BasePlugin, IWebConfigurablePlugin):
    async def get_api_router(self) -> APIRouter:
        router = APIRouter()
        router.get("/endpoint")(self.my_endpoint)
        return router

    async def configure(self, config: Dict[str, Any]) -> ConfigurationResult:
        # Configuration logic
        return ConfigurationResult(success=True)
```

---

## Lifecycle Management

### ✅ Best Practices

#### 1. Lifecycle States

```python
from enum import Enum
from typing import Optional

class PluginStatus(str, Enum):
    """Plugin lifecycle states."""
    UNLOADED = "unloaded"      # Plugin discovered but not loaded
    LOADED = "loaded"          # Plugin class loaded
    INITIALIZED = "initialized" # Plugin initialized
    STARTED = "started"        # Plugin running
    STOPPED = "stopped"        # Plugin stopped
    ERROR = "error"            # Plugin in error state

class PluginLifecycleManager:
    """Manage plugin lifecycle."""

    async def load_plugin(self, plugin_id: str) -> bool:
        """Load plugin class."""
        try:
            metadata = self._registry.get_metadata(plugin_id)
            plugin_class = self._loader.load_plugin_class(metadata)
            plugin_instance = plugin_class()

            self._plugins[plugin_id] = plugin_instance
            plugin_instance._status = PluginStatus.LOADED
            return True
        except Exception as e:
            logger.error(f"Failed to load {plugin_id}: {e}")
            return False

    async def initialize_plugin(self, plugin_id: str) -> bool:
        """Initialize plugin."""
        plugin = self._plugins.get(plugin_id)
        if not plugin:
            return False

        try:
            context = self._create_context(plugin_id)
            await plugin.initialize(context)
            plugin._status = PluginStatus.INITIALIZED
            return True
        except Exception as e:
            logger.error(f"Failed to initialize {plugin_id}: {e}")
            plugin._status = PluginStatus.ERROR
            return False

    async def start_plugin(self, plugin_id: str) -> bool:
        """Start plugin."""
        plugin = self._plugins.get(plugin_id)
        if not plugin or plugin.status != PluginStatus.INITIALIZED:
            return False

        try:
            await plugin.start()
            plugin._status = PluginStatus.STARTED
            return True
        except Exception as e:
            logger.error(f"Failed to start {plugin_id}: {e}")
            plugin._status = PluginStatus.ERROR
            return False

    async def stop_plugin(self, plugin_id: str) -> bool:
        """Stop plugin."""
        plugin = self._plugins.get(plugin_id)
        if not plugin or plugin.status != PluginStatus.STARTED:
            return False

        try:
            await plugin.stop()
            plugin._status = PluginStatus.STOPPED
            return True
        except Exception as e:
            logger.error(f"Failed to stop {plugin_id}: {e}")
            return False

    async def shutdown_plugin(self, plugin_id: str) -> None:
        """Shutdown plugin."""
        plugin = self._plugins.get(plugin_id)
        if plugin:
            try:
                await plugin.shutdown()
            except Exception as e:
                logger.error(f"Error during shutdown of {plugin_id}: {e}")
            finally:
                del self._plugins[plugin_id]
```

#### 2. Lifecycle Hooks

```python
class BasePlugin(IPlugin):
    """Base plugin with lifecycle hooks."""

    async def initialize(self, context: PluginContext) -> None:
        """Initialize with hooks."""
        self._context = context
        await self.on_before_initialize(context)
        await self._do_initialize(context)
        await self.on_after_initialize(context)

    async def on_before_initialize(self, context: PluginContext) -> None:
        """Hook called before initialization."""
        pass

    async def _do_initialize(self, context: PluginContext) -> None:
        """Actual initialization logic."""
        # Override in subclasses
        pass

    async def on_after_initialize(self, context: PluginContext) -> None:
        """Hook called after initialization."""
        pass
```

#### 3. Graceful Shutdown

```python
class PluginManager:
    """Plugin manager with graceful shutdown."""

    async def shutdown_all(self) -> None:
        """Shutdown all plugins gracefully."""
        # Stop all plugins first
        for plugin_id in list(self._plugins.keys()):
            await self.stop_plugin(plugin_id)

        # Then shutdown
        shutdown_tasks = [
            self.shutdown_plugin(plugin_id)
            for plugin_id in list(self._plugins.keys())
        ]
        await asyncio.gather(*shutdown_tasks, return_exceptions=True)
```

---

## Dependency Resolution

### ✅ Best Practices

#### 1. Dependency Graph

```python
from typing import Dict, List, Set
from collections import defaultdict, deque

class DependencyResolver:
    """Resolve plugin dependencies."""

    def build_dependency_graph(
        self,
        plugins: Dict[str, PluginMetadata]
    ) -> Dict[str, Set[str]]:
        """Build dependency graph."""
        graph = defaultdict(set)

        for plugin_id, metadata in plugins.items():
            for dep in metadata.dependencies:
                graph[plugin_id].add(dep.plugin_id)

        return dict(graph)

    def resolve_load_order(
        self,
        plugins: Dict[str, PluginMetadata]
    ) -> List[str]:
        """Resolve load order using topological sort."""
        graph = self.build_dependency_graph(plugins)
        in_degree = defaultdict(int)

        # Calculate in-degrees
        for node in graph:
            in_degree[node] = 0
        for node, deps in graph.items():
            for dep in deps:
                in_degree[node] += 1

        # Topological sort
        queue = deque([node for node in in_degree if in_degree[node] == 0])
        load_order = []

        while queue:
            node = queue.popleft()
            load_order.append(node)

            # Reduce in-degree of dependents
            for dependent, deps in graph.items():
                if node in deps:
                    in_degree[dependent] -= 1
                    if in_degree[dependent] == 0:
                        queue.append(dependent)

        # Check for circular dependencies
        if len(load_order) != len(plugins):
            raise CircularDependencyError("Circular dependency detected")

        return load_order
```

#### 2. Circular Dependency Detection

```python
class DependencyResolver:
    """Detect circular dependencies."""

    def detect_circular_dependencies(
        self,
        plugins: Dict[str, PluginMetadata]
    ) -> List[List[str]]:
        """Detect circular dependencies."""
        graph = self.build_dependency_graph(plugins)
        cycles = []
        visited = set()
        rec_stack = set()

        def dfs(node: str, path: List[str]) -> None:
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for dep in graph.get(node, set()):
                if dep not in visited:
                    dfs(dep, path.copy())
                elif dep in rec_stack:
                    # Found cycle
                    cycle_start = path.index(dep)
                    cycles.append(path[cycle_start:] + [dep])

            rec_stack.remove(node)
            path.pop()

        for plugin_id in plugins:
            if plugin_id not in visited:
                dfs(plugin_id, [])

        return cycles
```

#### 3. Version Conflict Detection

```python
from packaging import version

class DependencyResolver:
    """Resolve version conflicts."""

    def check_version_conflicts(
        self,
        plugins: Dict[str, PluginMetadata]
    ) -> List[VersionConflict]:
        """Check for version conflicts."""
        conflicts = []
        required_versions: Dict[str, Set[str]] = defaultdict(set)

        # Collect version requirements
        for plugin_id, metadata in plugins.items():
            for dep in metadata.dependencies:
                required_versions[dep.plugin_id].add(dep.version_spec)

        # Check for conflicts
        for dep_id, versions in required_versions.items():
            if len(versions) > 1:
                # Try to find compatible version
                if not self._versions_compatible(list(versions)):
                    conflicts.append(VersionConflict(
                        plugin_id=dep_id,
                        required_versions=list(versions)
                    ))

        return conflicts

    def _versions_compatible(self, version_specs: List[str]) -> bool:
        """Check if version specs are compatible."""
        # Simplified - use packaging library for real implementation
        # This would need proper version range parsing
        return True
```

---

## Security & Isolation

### ✅ Best Practices

#### 1. Security Levels

```python
from enum import Enum

class SecurityLevel(str, Enum):
    """Plugin security levels."""
    UNRESTRICTED = "unrestricted"  # Full system access
    TRUSTED = "trusted"            # Trusted plugins
    SANDBOXED = "sandboxed"        # Sandboxed execution
    ISOLATED = "isolated"          # Complete isolation

class SecurityManager:
    """Manage plugin security."""

    def create_security_context(
        self,
        plugin_id: str,
        security_level: SecurityLevel,
        permissions: Set[Permission]
    ) -> SecurityContext:
        """Create security context for plugin."""
        context = SecurityContext(
            plugin_id=plugin_id,
            security_level=security_level,
            granted_permissions=self._validate_permissions(
                plugin_id, permissions, security_level
            ),
            resource_limits=self._get_resource_limits(security_level)
        )
        return context

    def _validate_permissions(
        self,
        plugin_id: str,
        requested: Set[Permission],
        level: SecurityLevel
    ) -> Set[Permission]:
        """Validate permissions based on security level."""
        if level == SecurityLevel.UNRESTRICTED:
            return requested
        elif level == SecurityLevel.TRUSTED:
            # Filter dangerous permissions
            return requested - DANGEROUS_PERMISSIONS
        elif level == SecurityLevel.SANDBOXED:
            # Only safe permissions
            return requested & SAFE_PERMISSIONS
        else:  # ISOLATED
            return set()  # No permissions
```

#### 2. Permission System

```python
from enum import Enum
from typing import Set

class Permission(str, Enum):
    """Plugin permissions."""
    READ_DATA = "read_data"
    WRITE_DATA = "write_data"
    DELETE_DATA = "delete_data"
    EXECUTE_CODE = "execute_code"
    NETWORK_ACCESS = "network_access"
    FILE_SYSTEM_ACCESS = "file_system_access"
    DATABASE_ACCESS = "database_access"

class PermissionManager:
    """Manage plugin permissions."""

    def validate_permission(
        self,
        plugin_id: str,
        permission: Permission
    ) -> bool:
        """Check if plugin has permission."""
        context = self._get_security_context(plugin_id)
        return permission in context.granted_permissions

    async def check_permission(
        self,
        plugin_id: str,
        permission: Permission
    ) -> None:
        """Raise exception if permission denied."""
        if not self.validate_permission(plugin_id, permission):
            raise PermissionDeniedError(
                f"Plugin {plugin_id} does not have {permission.value}"
            )
```

#### 3. Resource Limits

```python
from dataclasses import dataclass

@dataclass
class ResourceLimits:
    """Resource limits for plugins."""
    max_memory_mb: int = 512
    max_cpu_percent: float = 50.0
    max_execution_time_seconds: int = 30
    max_file_size_mb: int = 100
    max_network_requests: int = 100

class ResourceManager:
    """Manage plugin resources."""

    def __init__(self):
        self._plugin_resources: Dict[str, ResourceUsage] = {}

    async def check_resource_limits(
        self,
        plugin_id: str,
        limits: ResourceLimits
    ) -> bool:
        """Check if plugin is within resource limits."""
        usage = self._plugin_resources.get(plugin_id)
        if not usage:
            return True

        return (
            usage.memory_mb <= limits.max_memory_mb and
            usage.cpu_percent <= limits.max_cpu_percent and
            usage.execution_time <= limits.max_execution_time_seconds
        )
```

#### 4. Audit Logging

```python
class AuditLogger:
    """Audit plugin operations."""

    async def log_plugin_action(
        self,
        plugin_id: str,
        action: str,
        details: Dict[str, Any],
        severity: str = "info"
    ) -> None:
        """Log plugin action."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "plugin_id": plugin_id,
            "action": action,
            "details": details,
            "severity": severity
        }

        # Write to audit log
        await self._write_audit_log(log_entry)

        # Alert on security events
        if severity in ("warning", "error"):
            await self._alert_security_team(log_entry)
```

---

## Plugin Registry

### ✅ Best Practices

#### 1. Registry Implementation

```python
from typing import Dict, List, Optional

class PluginRegistry:
    """Plugin registry."""

    def __init__(self):
        self._plugins: Dict[str, IPlugin] = {}
        self._metadata: Dict[str, PluginMetadata] = {}
        self._by_capability: Dict[str, List[str]] = defaultdict(list)

    def register_plugin(
        self,
        plugin: IPlugin,
        metadata: PluginMetadata
    ) -> None:
        """Register plugin."""
        plugin_id = metadata.plugin_id

        if plugin_id in self._plugins:
            raise PluginAlreadyRegisteredError(f"Plugin {plugin_id} already registered")

        self._plugins[plugin_id] = plugin
        self._metadata[plugin_id] = metadata

        # Index by capabilities
        for capability in metadata.capabilities:
            self._by_capability[capability].append(plugin_id)

    def get_plugin(self, plugin_id: str) -> Optional[IPlugin]:
        """Get plugin by ID."""
        return self._plugins.get(plugin_id)

    def get_plugins_by_capability(self, capability: str) -> List[IPlugin]:
        """Get plugins by capability."""
        plugin_ids = self._by_capability.get(capability, [])
        return [self._plugins[pid] for pid in plugin_ids]

    def unregister_plugin(self, plugin_id: str) -> None:
        """Unregister plugin."""
        if plugin_id in self._plugins:
            metadata = self._metadata[plugin_id]
            # Remove from capability index
            for capability in metadata.capabilities:
                if plugin_id in self._by_capability[capability]:
                    self._by_capability[capability].remove(plugin_id)

            del self._plugins[plugin_id]
            del self._metadata[plugin_id]
```

#### 2. Plugin Metadata

```python
from pydantic import BaseModel, Field
from typing import List, Optional, Set, Dict, Any

class PluginMetadata(BaseModel):
    """Plugin metadata."""
    plugin_id: str = Field(..., description="Unique plugin identifier")
    name: str = Field(..., description="Plugin name")
    version: str = Field(..., description="Plugin version")
    description: str = Field(default="", description="Plugin description")
    author: str = Field(default="Unknown", description="Plugin author")

    # Dependencies
    dependencies: List[str] = Field(default_factory=list)
    optional_dependencies: List[str] = Field(default_factory=list)

    # Capabilities
    capabilities: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)

    # Entry point
    entry_point: Optional[str] = Field(None, description="Entry point string")

    # Security
    security_level: SecurityLevel = Field(
        default=SecurityLevel.SANDBOXED
    )
    required_permissions: List[Permission] = Field(default_factory=list)

    # Configuration
    default_configuration: Dict[str, Any] = Field(default_factory=dict)
    configuration_schema: Optional[Dict[str, Any]] = None

    # File information
    file_path: Optional[str] = None
    size_bytes: Optional[int] = None
    checksum: Optional[str] = None
```

---

## Hot Reload & Dynamic Loading

### ✅ Best Practices

#### 1. File Watching

```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path

class PluginFileWatcher(FileSystemEventHandler):
    """Watch for plugin file changes."""

    def __init__(self, plugin_manager: PluginManager):
        self._plugin_manager = plugin_manager
        self._observer = Observer()

    def on_modified(self, event):
        """Handle file modification."""
        if event.is_directory:
            return

        plugin_path = Path(event.src_path)
        if self._is_plugin_file(plugin_path):
            asyncio.create_task(
                self._plugin_manager.reload_plugin(plugin_path)
            )

    def start_watching(self, directory: Path):
        """Start watching directory."""
        self._observer.schedule(self, str(directory), recursive=True)
        self._observer.start()

    def stop_watching(self):
        """Stop watching."""
        self._observer.stop()
        self._observer.join()
```

#### 2. Hot Reload

```python
class PluginManager:
    """Plugin manager with hot reload."""

    async def reload_plugin(self, plugin_path: Path) -> bool:
        """Reload plugin on file change."""
        try:
            # Find plugin ID
            plugin_id = self._identify_plugin(plugin_path)
            if not plugin_id:
                return False

            # Stop plugin
            if plugin_id in self._plugins:
                await self.stop_plugin(plugin_id)
                await self.shutdown_plugin(plugin_id)

            # Reload module
            if plugin_id in sys.modules:
                del sys.modules[plugin_id]

            # Reload plugin
            return await self.load_plugin(plugin_id)

        except Exception as e:
            logger.error(f"Failed to reload {plugin_path}: {e}")
            return False
```

---

## FastAPI Integration

### ✅ Best Practices

#### 1. Plugin Router Integration

```python
from fastapi import FastAPI, APIRouter

class PluginManager:
    """Plugin manager integrated with FastAPI."""

    def __init__(self, app: FastAPI):
        self._app = app
        self._plugins: Dict[str, IPlugin] = {}

    async def initialize(self) -> None:
        """Initialize and mount plugin routers."""
        await self.discover_plugins()
        await self.load_all_plugins()

        # Mount plugin routers
        for plugin_id, plugin in self._plugins.items():
            if isinstance(plugin, IWebPlugin):
                router = await plugin.get_api_router()
                if router:
                    self._app.include_router(
                        router,
                        prefix=f"/plugins/{plugin_id}",
                        tags=[f"plugin:{plugin_id}"]
                    )

                # Mount static files
                static_mounts = await plugin.get_static_mounts()
                for mount in static_mounts:
                    self._app.mount(**mount)
```

#### 2. Plugin Dependency Injection

```python
from fastapi import Depends

def get_plugin_manager() -> PluginManager:
    """Dependency for plugin manager."""
    return app.state.plugin_manager

def get_plugin(plugin_id: str) -> IPlugin:
    """Dependency for specific plugin."""
    def _get_plugin(manager: PluginManager = Depends(get_plugin_manager)):
        plugin = manager.get_plugin(plugin_id)
        if not plugin:
            raise HTTPException(404, f"Plugin {plugin_id} not found")
        return plugin
    return _get_plugin

@app.get("/plugins/{plugin_id}/status")
async def get_plugin_status(
    plugin: IPlugin = Depends(get_plugin("my_plugin"))
):
    return {"status": plugin.status}
```

#### 3. Plugin Middleware

```python
from fastapi import Request

class PluginMiddleware:
    """Middleware for plugin integration."""

    def __init__(self, plugin_manager: PluginManager):
        self._plugin_manager = plugin_manager

    async def __call__(self, request: Request, call_next):
        # Add plugin manager to request state
        request.state.plugin_manager = self._plugin_manager

        # Process request through plugins
        for plugin in self._plugin_manager.get_all_plugins():
            if isinstance(plugin, IEventPlugin):
                await plugin.handle_request(request)

        response = await call_next(request)
        return response
```

---

## Testing

### ✅ Best Practices

#### 1. Mock Plugin

```python
class MockPlugin(BasePlugin):
    """Mock plugin for testing."""

    def __init__(self, plugin_id: str = "mock_plugin"):
        super().__init__(PluginMetadata(
            plugin_id=plugin_id,
            name="Mock Plugin",
            version="1.0.0"
        ))
        self.initialize_called = False
        self.start_called = False

    async def initialize(self, context: PluginContext) -> None:
        self.initialize_called = True

    async def start(self) -> None:
        self.start_called = True

    async def stop(self) -> None:
        pass

    async def shutdown(self) -> None:
        pass
```

#### 2. Plugin Testing

```python
import pytest

@pytest.fixture
def plugin_manager():
    """Plugin manager fixture."""
    manager = PluginManager()
    return manager

@pytest.mark.asyncio
async def test_plugin_loading(plugin_manager):
    """Test plugin loading."""
    metadata = PluginMetadata(
        plugin_id="test_plugin",
        name="Test Plugin",
        version="1.0.0"
    )

    success = await plugin_manager.load_plugin(metadata)
    assert success
    assert plugin_manager.get_plugin("test_plugin") is not None

@pytest.mark.asyncio
async def test_plugin_lifecycle(plugin_manager):
    """Test plugin lifecycle."""
    plugin = MockPlugin()
    await plugin_manager.register_plugin(plugin)

    await plugin_manager.initialize_plugin("mock_plugin")
    assert plugin.initialize_called

    await plugin_manager.start_plugin("mock_plugin")
    assert plugin.start_called
```

---

## Performance Optimization

### ✅ Best Practices

#### 1. Lazy Loading

```python
class PluginManager:
    """Lazy loading plugin manager."""

    def __init__(self):
        self._plugin_classes: Dict[str, Type[IPlugin]] = {}
        self._plugin_instances: Dict[str, IPlugin] = {}

    async def get_plugin(self, plugin_id: str) -> IPlugin:
        """Get plugin instance (lazy load)."""
        if plugin_id not in self._plugin_instances:
            await self._load_plugin(plugin_id)
        return self._plugin_instances[plugin_id]
```

#### 2. Plugin Pooling

```python
class PluginPool:
    """Pool plugin instances."""

    def __init__(self, max_size: int = 10):
        self._pool: Dict[str, List[IPlugin]] = defaultdict(list)
        self._max_size = max_size

    async def acquire(self, plugin_id: str) -> IPlugin:
        """Acquire plugin from pool."""
        if self._pool[plugin_id]:
            return self._pool[plugin_id].pop()
        return await self._create_plugin(plugin_id)

    def release(self, plugin_id: str, plugin: IPlugin) -> None:
        """Release plugin to pool."""
        if len(self._pool[plugin_id]) < self._max_size:
            self._pool[plugin_id].append(plugin)
```

---

## Summary Checklist

### Architecture
- [ ] SOLID principles applied
- [ ] DRY principles followed
- [ ] KISS principles maintained
- [ ] Clear separation of concerns

### Discovery
- [ ] Entry points discovery implemented
- [ ] File system discovery implemented
- [ ] Metadata file support
- [ ] Multi-source discovery

### Loading
- [ ] Dynamic module loading
- [ ] Safe loading with error handling
- [ ] Lazy loading where appropriate
- [ ] Entry point loading

### Interfaces
- [ ] Core IPlugin interface
- [ ] Segregated interfaces (IWebPlugin, IEventPlugin, etc.)
- [ ] Composite interfaces
- [ ] Clear interface contracts

### Lifecycle
- [ ] Proper state management
- [ ] Lifecycle hooks
- [ ] Graceful shutdown
- [ ] Error state handling

### Dependencies
- [ ] Dependency graph building
- [ ] Topological sort for load order
- [ ] Circular dependency detection
- [ ] Version conflict resolution

### Security
- [ ] Security levels implemented
- [ ] Permission system
- [ ] Resource limits
- [ ] Audit logging

### Registry
- [ ] Plugin registration
- [ ] Metadata management
- [ ] Capability indexing
- [ ] Query methods

### FastAPI Integration
- [ ] Router mounting
- [ ] Dependency injection
- [ ] Middleware integration
- [ ] Static file mounting

### Testing
- [ ] Mock plugins
- [ ] Unit tests
- [ ] Integration tests
- [ ] Lifecycle tests

---

## References

- [Python importlib Documentation](https://docs.python.org/3/library/importlib.html)
- [setuptools Entry Points](https://setuptools.pypa.io/en/latest/userguide/entry_point.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Plugin Architecture Patterns](https://en.wikipedia.org/wiki/Plugin_architecture)

---

**Note:** This document is based on Python 3.9+ and FastAPI latest. Always refer to official documentation for the most up-to-date information.
