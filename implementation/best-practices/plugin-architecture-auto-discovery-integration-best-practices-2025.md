# Plugin Architecture: Auto-Discovery & Auto-Integration Best Practices 2025
**Version**: v1.0.0
**Last Updated**: 2025-01-14
**Python Version**: 3.9+
**FastAPI Version**: Latest

This document compiles the latest best practices for implementing plugin architectures with automatic discovery and integration capabilities, based on official documentation, production code examples, and industry recommendations.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Auto-Discovery Patterns](#auto-discovery-patterns)
3. [Auto-Loading Mechanisms](#auto-loading-mechanisms)
4. [Auto-Integration Strategies](#auto-integration-strategies)
5. [Plugin Registry](#plugin-registry)
6. [Dependency Resolution](#dependency-resolution)
7. [Hot Reload & Dynamic Loading](#hot-reload--dynamic-loading)
8. [Lifecycle Management](#lifecycle-management)
9. [Performance Optimization](#performance-optimization)
10. [FastAPI Integration](#fastapi-integration)

---

## Architecture Overview

### ✅ Core Components

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Any
from enum import Enum

class PluginState(str, Enum):
    """Plugin lifecycle states."""
    DISCOVERED = "discovered"
    REGISTERED = "registered"
    LOADED = "loaded"
    INITIALIZED = "initialized"
    STARTED = "started"
    STOPPED = "stopped"
    FAILED = "failed"

@dataclass
class PluginInfo:
    """Plugin discovery information."""
    metadata: 'PluginMetadata'
    path: Path
    discovered_at: datetime
    checksum: str
    state: PluginState = PluginState.DISCOVERED

class IPluginDiscovery(ABC):
    """Plugin discovery interface."""

    @abstractmethod
    async def discover_plugins(self, search_paths: List[Path]) -> List[PluginInfo]:
        """Discover plugins in specified paths."""
        pass

class IPluginRegistry(ABC):
    """Plugin registry interface."""

    @abstractmethod
    async def register_plugin(self, plugin_info: PluginInfo) -> bool:
        """Register discovered plugin."""
        pass

    @abstractmethod
    async def get_plugin(self, plugin_id: str) -> Optional[PluginInfo]:
        """Get plugin by ID."""
        pass

class IPluginLoader(ABC):
    """Plugin loader interface."""

    @abstractmethod
    async def load_plugin(self, plugin_id: str) -> bool:
        """Load plugin into runtime."""
        pass

    @abstractmethod
    async def unload_plugin(self, plugin_id: str) -> bool:
        """Unload plugin from runtime."""
        pass

class PluginManager:
    """Integrated plugin management system."""

    def __init__(
        self,
        discovery: IPluginDiscovery,
        registry: IPluginRegistry,
        loader: IPluginLoader
    ):
        self._discovery = discovery
        self._registry = registry
        self._loader = loader
        self._auto_load_enabled = True

    async def auto_discover_and_load(self, search_paths: List[Path]) -> List[str]:
        """Auto-discover and load plugins."""
        # Discover plugins
        discovered = await self._discovery.discover_plugins(search_paths)

        # Register discovered plugins
        registered_ids = []
        for plugin_info in discovered:
            if await self._registry.register_plugin(plugin_info):
                registered_ids.append(plugin_info.metadata.plugin_id)

        # Auto-load if enabled
        if self._auto_load_enabled:
            for plugin_id in registered_ids:
                await self._loader.load_plugin(plugin_id)

        return registered_ids
```

---

## Auto-Discovery Patterns

### ✅ Best Practices

#### 1. Filesystem-Based Discovery

```python
from pathlib import Path
import importlib.util
import json
from typing import List, Optional
import hashlib

class FilesystemPluginDiscovery(IPluginDiscovery):
    """Filesystem-based plugin discovery."""

    def __init__(self):
        self._plugin_patterns = [
            "*/main.py",
            "*_plugin.py",
            "*/plugin.py",
            "*/__init__.py",
        ]
        self._metadata_files = [
            "plugin.json",
            "manifest.json",
            "metadata.json",
        ]

    async def discover_plugins(self, search_paths: List[Path]) -> List[PluginInfo]:
        """Discover plugins in filesystem paths."""
        discovered = []

        for search_path in search_paths:
            if not search_path.exists():
                continue

            path_plugins = await self._discover_in_path(search_path)
            discovered.extend(path_plugins)

        return discovered

    async def _discover_in_path(self, search_path: Path) -> List[PluginInfo]:
        """Discover plugins in a single path."""
        plugins = []

        # Search for Python files matching plugin patterns
        for pattern in self._plugin_patterns:
            for plugin_file in search_path.rglob(pattern):
                plugin_info = await self._extract_plugin_info(plugin_file)
                if plugin_info:
                    plugins.append(plugin_info)

        return plugins

    async def _extract_plugin_info(self, plugin_file: Path) -> Optional[PluginInfo]:
        """Extract plugin information from file."""
        plugin_dir = plugin_file.parent

        # Try metadata file first
        metadata = await self._load_metadata_file(plugin_dir)

        # Fallback to Python file extraction
        if not metadata:
            metadata = await self._extract_metadata_from_python(plugin_file)

        if not metadata:
            return None

        # Calculate checksum
        checksum = await self._calculate_checksum(plugin_file)

        return PluginInfo(
            metadata=metadata,
            path=plugin_file,
            discovered_at=datetime.now(timezone.utc),
            checksum=checksum
        )

    async def _load_metadata_file(self, plugin_dir: Path) -> Optional[PluginMetadata]:
        """Load metadata from JSON files."""
        for metadata_file in self._metadata_files:
            metadata_path = plugin_dir / metadata_file
            if metadata_path.exists():
                try:
                    with open(metadata_path, "r") as f:
                        data = json.load(f)
                    return self._parse_metadata(data)
                except Exception as e:
                    logger.warning(f"Failed to parse {metadata_path}: {e}")
        return None

    async def _extract_metadata_from_python(self, plugin_file: Path) -> Optional[PluginMetadata]:
        """Extract metadata from Python file."""
        try:
            spec = importlib.util.spec_from_file_location("temp_plugin", plugin_file)
            if not spec or not spec.loader:
                return None

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Look for PLUGIN_METADATA constant
            if hasattr(module, "PLUGIN_METADATA"):
                metadata_dict = getattr(module, "PLUGIN_METADATA")
                if isinstance(metadata_dict, dict):
                    return self._parse_metadata(metadata_dict)
        except Exception as e:
            logger.debug(f"Could not extract metadata from {plugin_file}: {e}")

        return None

    async def _calculate_checksum(self, file_path: Path) -> str:
        """Calculate file checksum."""
        hasher = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
```

#### 2. Entry Points Discovery

```python
from importlib.metadata import entry_points
from typing import List

class EntryPointsPluginDiscovery(IPluginDiscovery):
    """Entry points-based plugin discovery."""

    def __init__(self, entry_point_group: str = "myapp.plugins"):
        self._entry_point_group = entry_point_group

    async def discover_plugins(self, search_paths: List[Path]) -> List[PluginInfo]:
        """Discover plugins via entry points."""
        discovered = []

        try:
            eps = entry_points(group=self._entry_point_group)
            for ep in eps:
                try:
                    plugin_class = ep.load()
                    metadata = self._extract_metadata_from_class(plugin_class)
                    if metadata:
                        discovered.append(PluginInfo(
                            metadata=metadata,
                            path=Path(ep.value),
                            discovered_at=datetime.now(timezone.utc),
                            checksum=""
                        ))
                except Exception as e:
                    logger.error(f"Failed to load entry point {ep.name}: {e}")
        except Exception as e:
            logger.error(f"Entry point discovery failed: {e}")

        return discovered

    def _extract_metadata_from_class(self, plugin_class: type) -> Optional[PluginMetadata]:
        """Extract metadata from plugin class."""
        if hasattr(plugin_class, "PLUGIN_METADATA"):
            return self._parse_metadata(plugin_class.PLUGIN_METADATA)
        return None
```

#### 3. Metadata File Discovery

```python
class MetadataFileDiscovery(IPluginDiscovery):
    """Metadata file-based discovery."""

    async def discover_plugins(self, search_paths: List[Path]) -> List[PluginInfo]:
        """Discover plugins from metadata files."""
        discovered = []

        for search_path in search_paths:
            for metadata_file in search_path.rglob("plugin.json"):
                try:
                    with open(metadata_file, "r") as f:
                        data = json.load(f)

                    metadata = self._parse_metadata(data)
                    plugin_file = metadata_file.parent / data.get("main", "main.py")

                    discovered.append(PluginInfo(
                        metadata=metadata,
                        path=plugin_file,
                        discovered_at=datetime.now(timezone.utc),
                        checksum=await self._calculate_checksum(plugin_file)
                    ))
                except Exception as e:
                    logger.warning(f"Failed to process {metadata_file}: {e}")

        return discovered
```

#### 4. Multi-Source Discovery

```python
class MultiSourcePluginDiscovery(IPluginDiscovery):
    """Multi-source plugin discovery."""

    def __init__(self):
        self._discoverers = [
            FilesystemPluginDiscovery(),
            EntryPointsPluginDiscovery(),
            MetadataFileDiscovery(),
        ]

    async def discover_plugins(self, search_paths: List[Path]) -> List[PluginInfo]:
        """Discover from all sources."""
        all_discovered = []

        for discoverer in self._discoverers:
            discovered = await discoverer.discover_plugins(search_paths)
            all_discovered.extend(discovered)

        # Deduplicate by plugin_id
        return self._deduplicate(all_discovered)

    def _deduplicate(self, plugins: List[PluginInfo]) -> List[PluginInfo]:
        """Remove duplicate plugins."""
        seen = {}
        for plugin in plugins:
            plugin_id = plugin.metadata.plugin_id
            if plugin_id not in seen:
                seen[plugin_id] = plugin
            # Keep the most recently discovered
            elif plugin.discovered_at > seen[plugin_id].discovered_at:
                seen[plugin_id] = plugin
        return list(seen.values())
```

---

## Auto-Loading Mechanisms

### ✅ Best Practices

#### 1. Automatic Plugin Loading

```python
class AutoLoadingPluginManager:
    """Plugin manager with auto-loading."""

    def __init__(
        self,
        discovery: IPluginDiscovery,
        registry: IPluginRegistry,
        loader: IPluginLoader
    ):
        self._discovery = discovery
        self._registry = registry
        self._loader = loader
        self._auto_load_enabled = True
        self._auto_start_enabled = False

    async def auto_discover_and_load(
        self,
        search_paths: List[Path],
        auto_start: bool = False
    ) -> List[str]:
        """Auto-discover and load plugins."""
        # Discover plugins
        discovered = await self._discovery.discover_plugins(search_paths)

        loaded_ids = []
        for plugin_info in discovered:
            try:
                # Register plugin
                if await self._registry.register_plugin(plugin_info):
                    plugin_id = plugin_info.metadata.plugin_id

                    # Auto-load
                    if self._auto_load_enabled:
                        if await self._loader.load_plugin(plugin_id):
                            loaded_ids.append(plugin_id)

                            # Auto-start if enabled
                            if auto_start or self._auto_start_enabled:
                                await self._loader.start_plugin(plugin_id)
            except Exception as e:
                logger.error(f"Failed to auto-load {plugin_info.metadata.plugin_id}: {e}")

        return loaded_ids
```

#### 2. Conditional Auto-Loading

```python
class ConditionalAutoLoader:
    """Conditional auto-loading based on criteria."""

    async def auto_load_with_criteria(
        self,
        plugin_info: PluginInfo,
        criteria: Dict[str, Any]
    ) -> bool:
        """Auto-load plugin if criteria met."""
        # Check environment
        if "environment" in criteria:
            if plugin_info.metadata.environment != criteria["environment"]:
                return False

        # Check feature flags
        if "feature_flags" in criteria:
            for flag in criteria["feature_flags"]:
                if not await self._check_feature_flag(flag):
                    return False

        # Check dependencies
        if "check_dependencies" in criteria and criteria["check_dependencies"]:
            if not await self._check_dependencies(plugin_info):
                return False

        return await self._loader.load_plugin(plugin_info.metadata.plugin_id)
```

#### 3. Lazy Loading

```python
class LazyLoadingPluginManager:
    """Lazy loading plugin manager."""

    def __init__(self, registry: IPluginRegistry, loader: IPluginLoader):
        self._registry = registry
        self._loader = loader
        self._loaded_plugins: Set[str] = set()

    async def get_plugin(self, plugin_id: str) -> Optional[Any]:
        """Get plugin instance, loading if necessary."""
        if plugin_id not in self._loaded_plugins:
            plugin_info = await self._registry.get_plugin(plugin_id)
            if plugin_info:
                if await self._loader.load_plugin(plugin_id):
                    self._loaded_plugins.add(plugin_id)
                else:
                    return None

        return await self._loader.get_plugin_instance(plugin_id)
```

---

## Auto-Integration Strategies

### ✅ Best Practices

#### 1. Automatic FastAPI Integration

```python
from fastapi import FastAPI
from fastapi.routing import APIRoute

class FastAPIPluginIntegrator:
    """Automatic FastAPI plugin integration."""

    def __init__(self, app: FastAPI):
        self._app = app
        self._integrated_plugins: Set[str] = set()

    async def auto_integrate_plugin(self, plugin_id: str, plugin_instance: Any) -> bool:
        """Automatically integrate plugin into FastAPI."""
        try:
            # Check if plugin provides FastAPI router
            if hasattr(plugin_instance, "get_router"):
                router = plugin_instance.get_router()
                if router:
                    self._app.include_router(router)
                    self._integrated_plugins.add(plugin_id)
                    return True

            # Check if plugin provides routes
            if hasattr(plugin_instance, "get_routes"):
                routes = plugin_instance.get_routes()
                for route in routes:
                    self._app.add_api_route(**route)
                self._integrated_plugins.add(plugin_id)
                return True

            # Check if plugin provides middleware
            if hasattr(plugin_instance, "get_middleware"):
                middleware = plugin_instance.get_middleware()
                if middleware:
                    self._app.add_middleware(middleware)
                    self._integrated_plugins.add(plugin_id)
                    return True

            return False
        except Exception as e:
            logger.error(f"Failed to integrate plugin {plugin_id}: {e}")
            return False
```

#### 2. Automatic Dependency Injection Integration

```python
class DependencyInjectionIntegrator:
    """Automatic dependency injection integration."""

    def __init__(self, container: Any):
        self._container = container

    async def auto_integrate_plugin(self, plugin_id: str, plugin_instance: Any) -> bool:
        """Automatically register plugin in DI container."""
        try:
            # Register plugin instance
            self._container.register(plugin_id, plugin_instance)

            # Register plugin services
            if hasattr(plugin_instance, "get_services"):
                services = plugin_instance.get_services()
                for service_name, service_class in services.items():
                    self._container.register(service_name, service_class)

            return True
        except Exception as e:
            logger.error(f"Failed to integrate plugin {plugin_id}: {e}")
            return False
```

#### 3. Automatic Event Bus Integration

```python
class EventBusIntegrator:
    """Automatic event bus integration."""

    def __init__(self, event_bus: Any):
        self._event_bus = event_bus

    async def auto_integrate_plugin(self, plugin_id: str, plugin_instance: Any) -> bool:
        """Automatically register plugin event handlers."""
        try:
            # Register event handlers
            if hasattr(plugin_instance, "get_event_handlers"):
                handlers = plugin_instance.get_event_handlers()
                for event_type, handler in handlers.items():
                    self._event_bus.subscribe(event_type, handler)

            # Register event emitters
            if hasattr(plugin_instance, "get_event_emitters"):
                emitters = plugin_instance.get_event_emitters()
                for event_type in emitters:
                    self._event_bus.register_emitter(event_type, plugin_id)

            return True
        except Exception as e:
            logger.error(f"Failed to integrate plugin {plugin_id}: {e}")
            return False
```

---

## Plugin Registry

### ✅ Best Practices

#### 1. Dynamic Plugin Registry

```python
class DynamicPluginRegistry(IPluginRegistry):
    """Dynamic plugin registry with auto-registration."""

    def __init__(self):
        self._plugins: Dict[str, PluginInfo] = {}
        self._plugin_paths: Dict[str, Path] = {}
        self._dependency_graph: Dict[str, Set[str]] = {}

    async def register_plugin(self, plugin_info: PluginInfo) -> bool:
        """Register discovered plugin."""
        plugin_id = plugin_info.metadata.plugin_id

        # Check if already registered
        if plugin_id in self._plugins:
            # Update if newer version
            existing = self._plugins[plugin_id]
            if plugin_info.metadata.version > existing.metadata.version:
                await self._update_plugin(plugin_id, plugin_info)
            return True

        # Validate dependencies
        if not await self._validate_dependencies(plugin_info):
            return False

        # Register plugin
        self._plugins[plugin_id] = plugin_info
        self._plugin_paths[plugin_id] = plugin_info.path

        # Update dependency graph
        for dep in plugin_info.metadata.dependencies:
            if dep.plugin_id not in self._dependency_graph:
                self._dependency_graph[dep.plugin_id] = set()
            self._dependency_graph[dep.plugin_id].add(plugin_id)

        return True

    async def _validate_dependencies(self, plugin_info: PluginInfo) -> bool:
        """Validate plugin dependencies."""
        for dep in plugin_info.metadata.dependencies:
            if dep.plugin_id not in self._plugins:
                if not dep.optional:
                    logger.warning(
                        f"Plugin {plugin_info.metadata.plugin_id} "
                        f"requires {dep.plugin_id} which is not available"
                    )
                    return False
        return True

    async def get_plugin(self, plugin_id: str) -> Optional[PluginInfo]:
        """Get plugin by ID."""
        return self._plugins.get(plugin_id)

    async def get_all_plugins(self) -> List[PluginInfo]:
        """Get all registered plugins."""
        return list(self._plugins.values())

    async def get_load_order(self) -> List[str]:
        """Get topological sort of plugins based on dependencies."""
        return self._topological_sort()

    def _topological_sort(self) -> List[str]:
        """Topological sort of dependency graph."""
        in_degree = {plugin_id: 0 for plugin_id in self._plugins}

        # Calculate in-degrees
        for plugin_id, deps in self._dependency_graph.items():
            for dep in deps:
                if dep in in_degree:
                    in_degree[dep] += 1

        # Kahn's algorithm
        queue = [plugin_id for plugin_id, degree in in_degree.items() if degree == 0]
        result = []

        while queue:
            plugin_id = queue.pop(0)
            result.append(plugin_id)

            if plugin_id in self._dependency_graph:
                for dependent in self._dependency_graph[plugin_id]:
                    in_degree[dependent] -= 1
                    if in_degree[dependent] == 0:
                        queue.append(dependent)

        return result
```

---

## Dependency Resolution

### ✅ Best Practices

#### 1. Dependency Resolver

```python
class DependencyResolver:
    """Plugin dependency resolver."""

    def __init__(self, registry: IPluginRegistry):
        self._registry = registry

    async def resolve_dependencies(
        self,
        plugin_id: str
    ) -> Tuple[List[str], List[str]]:
        """Resolve plugin dependencies.

        Returns:
            Tuple of (satisfied_deps, missing_deps)
        """
        plugin_info = await self._registry.get_plugin(plugin_id)
        if not plugin_info:
            return [], []

        satisfied = []
        missing = []

        for dep in plugin_info.metadata.dependencies:
            dep_info = await self._registry.get_plugin(dep.plugin_id)
            if dep_info:
                # Check version compatibility
                if self._check_version_compatibility(dep, dep_info.metadata.version):
                    satisfied.append(dep.plugin_id)
                else:
                    missing.append(f"{dep.plugin_id} (version mismatch)")
            else:
                if not dep.optional:
                    missing.append(dep.plugin_id)

        return satisfied, missing

    def _check_version_compatibility(
        self,
        dependency: PluginDependency,
        installed_version: PluginVersion
    ) -> bool:
        """Check if installed version satisfies requirement."""
        # Simple version check (can be enhanced with semver)
        if dependency.version_requirement == "*":
            return True

        # Parse version requirement and compare
        # Implementation depends on versioning scheme
        return True
```

---

## Hot Reload & Dynamic Loading

### ✅ Best Practices

#### 1. Hot Reload Manager

```python
import watchdog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class HotReloadManager:
    """Hot reload manager for plugins."""

    def __init__(
        self,
        plugin_manager: PluginManager,
        watch_paths: List[Path]
    ):
        self._plugin_manager = plugin_manager
        self._watch_paths = watch_paths
        self._observer = Observer()
        self._event_handler = PluginFileHandler(self)

    def start(self):
        """Start watching for file changes."""
        for path in self._watch_paths:
            if path.exists():
                self._observer.schedule(self._event_handler, str(path), recursive=True)
        self._observer.start()

    def stop(self):
        """Stop watching."""
        self._observer.stop()
        self._observer.join()

    async def handle_file_change(self, file_path: Path):
        """Handle file change event."""
        # Check if it's a plugin file
        plugin_info = await self._plugin_manager._discovery._extract_plugin_info(file_path)
        if plugin_info:
            plugin_id = plugin_info.metadata.plugin_id

            # Reload plugin
            await self._plugin_manager.reload_plugin(plugin_id)

class PluginFileHandler(FileSystemEventHandler):
    """File system event handler for plugins."""

    def __init__(self, manager: HotReloadManager):
        self._manager = manager

    def on_modified(self, event):
        """Handle file modification."""
        if not event.is_directory:
            file_path = Path(event.src_path)
            if file_path.suffix == ".py":
                asyncio.create_task(self._manager.handle_file_change(file_path))
```

#### 2. Dynamic Plugin Loading

```python
import importlib
import sys

class DynamicPluginLoader(IPluginLoader):
    """Dynamic plugin loader."""

    def __init__(self):
        self._loaded_modules: Dict[str, Any] = {}
        self._plugin_instances: Dict[str, Any] = {}

    async def load_plugin(self, plugin_id: str) -> bool:
        """Dynamically load plugin."""
        try:
            plugin_info = await self._registry.get_plugin(plugin_id)
            if not plugin_info:
                return False

            # Load module dynamically
            spec = importlib.util.spec_from_file_location(
                plugin_id,
                plugin_info.path
            )
            if not spec or not spec.loader:
                return False

            module = importlib.util.module_from_spec(spec)
            sys.modules[plugin_id] = module
            spec.loader.exec_module(module)

            self._loaded_modules[plugin_id] = module

            # Instantiate plugin
            plugin_class = self._find_plugin_class(module)
            if plugin_class:
                instance = plugin_class()
                self._plugin_instances[plugin_id] = instance

                # Initialize plugin
                if hasattr(instance, "initialize"):
                    await instance.initialize()

                return True

            return False
        except Exception as e:
            logger.error(f"Failed to load plugin {plugin_id}: {e}")
            return False

    async def unload_plugin(self, plugin_id: str) -> bool:
        """Unload plugin dynamically."""
        try:
            # Stop plugin
            if plugin_id in self._plugin_instances:
                instance = self._plugin_instances[plugin_id]
                if hasattr(instance, "shutdown"):
                    await instance.shutdown()
                del self._plugin_instances[plugin_id]

            # Remove module
            if plugin_id in self._loaded_modules:
                del self._loaded_modules[plugin_id]

            if plugin_id in sys.modules:
                del sys.modules[plugin_id]

            return True
        except Exception as e:
            logger.error(f"Failed to unload plugin {plugin_id}: {e}")
            return False

    def _find_plugin_class(self, module: Any) -> Optional[type]:
        """Find plugin class in module."""
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, type) and issubclass(obj, BasePlugin):
                return obj
        return None
```

---

## Lifecycle Management

### ✅ Best Practices

#### 1. Plugin Lifecycle Manager

```python
class PluginLifecycleManager:
    """Plugin lifecycle manager."""

    def __init__(self, loader: IPluginLoader):
        self._loader = loader
        self._plugin_states: Dict[str, PluginState] = {}

    async def initialize_plugin(self, plugin_id: str) -> bool:
        """Initialize plugin lifecycle."""
        try:
            # Load plugin
            if await self._loader.load_plugin(plugin_id):
                self._plugin_states[plugin_id] = PluginState.LOADED

                # Initialize
                instance = await self._loader.get_plugin_instance(plugin_id)
                if instance and hasattr(instance, "initialize"):
                    await instance.initialize()
                    self._plugin_states[plugin_id] = PluginState.INITIALIZED
                    return True

            return False
        except Exception as e:
            logger.error(f"Failed to initialize {plugin_id}: {e}")
            self._plugin_states[plugin_id] = PluginState.FAILED
            return False

    async def start_plugin(self, plugin_id: str) -> bool:
        """Start plugin."""
        if self._plugin_states.get(plugin_id) != PluginState.INITIALIZED:
            await self.initialize_plugin(plugin_id)

        try:
            instance = await self._loader.get_plugin_instance(plugin_id)
            if instance and hasattr(instance, "start"):
                await instance.start()
                self._plugin_states[plugin_id] = PluginState.STARTED
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to start {plugin_id}: {e}")
            return False

    async def stop_plugin(self, plugin_id: str) -> bool:
        """Stop plugin."""
        try:
            instance = await self._loader.get_plugin_instance(plugin_id)
            if instance and hasattr(instance, "stop"):
                await instance.stop()
                self._plugin_states[plugin_id] = PluginState.STOPPED
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to stop {plugin_id}: {e}")
            return False

    async def shutdown_plugin(self, plugin_id: str) -> bool:
        """Shutdown plugin."""
        await self.stop_plugin(plugin_id)

        try:
            instance = await self._loader.get_plugin_instance(plugin_id)
            if instance and hasattr(instance, "shutdown"):
                await instance.shutdown()

            await self._loader.unload_plugin(plugin_id)
            self._plugin_states[plugin_id] = PluginState.STOPPED
            return True
        except Exception as e:
            logger.error(f"Failed to shutdown {plugin_id}: {e}")
            return False
```

---

## Performance Optimization

### ✅ Best Practices

#### 1. Cached Discovery

```python
from datetime import datetime, timedelta

class CachedPluginDiscovery(IPluginDiscovery):
    """Cached plugin discovery."""

    def __init__(self, base_discovery: IPluginDiscovery, cache_ttl: int = 3600):
        self._base_discovery = base_discovery
        self._cache_ttl = cache_ttl
        self._cache: Dict[str, Tuple[List[PluginInfo], datetime]] = {}

    async def discover_plugins(self, search_paths: List[Path]) -> List[PluginInfo]:
        """Discover plugins with caching."""
        cache_key = str(sorted(search_paths))

        # Check cache
        if cache_key in self._cache:
            cached_result, cached_time = self._cache[cache_key]
            age = (datetime.now() - cached_time).total_seconds()
            if age < self._cache_ttl:
                return cached_result

        # Discover and cache
        result = await self._base_discovery.discover_plugins(search_paths)
        self._cache[cache_key] = (result, datetime.now())

        return result
```

#### 2. Parallel Discovery

```python
import asyncio

class ParallelPluginDiscovery(IPluginDiscovery):
    """Parallel plugin discovery."""

    def __init__(self, base_discovery: IPluginDiscovery, max_concurrent: int = 10):
        self._base_discovery = base_discovery
        self._max_concurrent = max_concurrent
        self._semaphore = asyncio.Semaphore(max_concurrent)

    async def discover_plugins(self, search_paths: List[Path]) -> List[PluginInfo]:
        """Discover plugins in parallel."""
        tasks = []
        for path in search_paths:
            task = self._discover_path(path)
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        all_plugins = []
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Discovery failed: {result}")
            else:
                all_plugins.extend(result)

        return all_plugins

    async def _discover_path(self, path: Path) -> List[PluginInfo]:
        """Discover plugins in a single path."""
        async with self._semaphore:
            return await self._base_discovery.discover_plugins([path])
```

---

## FastAPI Integration

### ✅ Best Practices

#### 1. FastAPI Plugin Manager Integration

```python
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan with plugin auto-discovery."""
    # Initialize plugin system
    discovery = MultiSourcePluginDiscovery()
    registry = DynamicPluginRegistry()
    loader = DynamicPluginLoader()
    integrator = FastAPIPluginIntegrator(app)

    plugin_manager = PluginManager(discovery, registry, loader)

    # Auto-discover and load plugins
    search_paths = [
        Path("plugins"),
        Path("app/plugins"),
    ]

    loaded_plugins = await plugin_manager.auto_discover_and_load(search_paths)

    # Auto-integrate plugins
    for plugin_id in loaded_plugins:
        plugin_instance = await loader.get_plugin_instance(plugin_id)
        if plugin_instance:
            await integrator.auto_integrate_plugin(plugin_id, plugin_instance)

    # Store in app state
    app.state.plugin_manager = plugin_manager

    yield

    # Shutdown plugins
    for plugin_id in loaded_plugins:
        await plugin_manager.shutdown_plugin(plugin_id)

app = FastAPI(lifespan=lifespan)
```

---

## Summary Checklist

### Auto-Discovery
- [ ] Filesystem-based discovery implemented
- [ ] Entry points discovery implemented
- [ ] Metadata file discovery implemented
- [ ] Multi-source discovery implemented
- [ ] Discovery caching implemented
- [ ] Parallel discovery implemented

### Auto-Loading
- [ ] Automatic plugin loading
- [ ] Conditional auto-loading
- [ ] Lazy loading
- [ ] Dependency-aware loading
- [ ] Load order resolution

### Auto-Integration
- [ ] FastAPI router integration
- [ ] Dependency injection integration
- [ ] Event bus integration
- [ ] Middleware integration
- [ ] Static file integration

### Registry
- [ ] Dynamic plugin registry
- [ ] Dependency graph management
- [ ] Version management
- [ ] Plugin metadata storage

### Hot Reload
- [ ] File system watching
- [ ] Dynamic module reloading
- [ ] State preservation
- [ ] Graceful reload

### Lifecycle
- [ ] Plugin initialization
- [ ] Plugin startup
- [ ] Plugin shutdown
- [ ] State management

---

## References

- [Fastify Autoload](https://github.com/fastify/fastify-autoload)
- [Python Plugin Architecture Best Practices](./python-fastapi-plugin-architecture-best-practices-2025.md)

---

**Note:** This document is based on latest best practices for plugin architectures with auto-discovery and auto-integration. Always refer to official documentation for the most up-to-date information.
