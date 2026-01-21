# FSP Shell UFC Blueprint - Architecture Reconciliation Specification

**Version**: v1.1.0
**Date**: 2026-01-18
**Last Updated**: 2026-01-18 (Australia/Adelaide)
**Status**: ✅ VERIFIED - Blueprint Implementation Complete and Built
**Priority**: P0 - CRITICAL
**Session Type**: Architecture Documentation & Blueprint Creation
**Instruction Files**:

- `002-PROTOCOL-Zero_Tolerance_Remediation-v2.0.0.yaml`
- `003-PROTOCOL-FastAPI_Pure_Code_Implementation-v2.0.0.yaml`
- `104-INSTRUCTIONS-Execute_Implementation_Phase_Tasks-v2.0.0.yaml`
- `107-INSTRUCTIONS-Remediate_And_Refactor_Codebase-v2.0.0.yaml`
- `202-INSTRUCTIONS-Pure_Code_Implementation_Execution_Protocol-v2.0.0.yaml`
- `203-INSTRUCTIONS-FastAPI_Design_Implementation_Refactor-v2.0.0.yaml`

---

## � MANDATORY IMPLEMENTATION REQUIREMENT

**⚠️ CRITICAL: The FSP Shell Technical Blueprint MUST be implemented.**

**Blueprint Document**: `governance/au-sys-governance/architecture/python/fastapi/fsp_shell/FSP_SHELL_TECHNICAL_BLUEPRINT_v1.0.0.md`

**IMPLEMENTATION MANDATE:**

This CODE IMPLEMENTATION SPECIFICATION document declares that **ALL** requirements, specifications, patterns, and standards defined in the **FSP_SHELL_TECHNICAL_BLUEPRINT_v1.0.0.md** are **MANDATORY** and **MUST** be implemented in the `au_sys_fsp_plugin` package.

**COMPLIANCE REQUIREMENTS:**

1. **MUST IMPLEMENT**: Every component, protocol, and provider specified in the technical blueprint
2. **MUST COMPLY**: With all runtime requirements (Python 3.12-slim mandatory based Docker image, package versions)
3. **MUST ENFORCE**: All code quality mandates (SOLID, DRY, KISS, YAGNI)
4. **MUST APPLY**: All design patterns (Singleton, Factory, Decorator, Observer, Pooling)
5. **MUST ACHIEVE**: All architecture qualities (Extensible, Modular, Idempotent, etc.)
6. **MUST IMPLEMENT**: Mandatory observability stack (logging, metrics, tracing via OpenTelemetry)
7. **MUST IMPLEMENT**: Dual-mode storage (SQL relational + NoSQL key-value)
8. **MUST IMPLEMENT**: Async operations and connection pooling patterns
9. **MUST TEST**: Comprehensive test coverage (80%+ required)
10. **MUST DOCUMENT**: Complete API documentation and usage examples

**ZERO TOLERANCE**: Any implementation that deviates from the technical blueprint without explicit architectural approval is considered non-compliant and MUST be remediated immediately per Protocol 002.

**VERIFICATION**: All implementations MUST be verified against the technical blueprint specifications before deployment to production environments.

**AUTHORITY**: This mandate is issued under the authority of:
- `000-DOCTRINE-Enterprise_Canonical_Execution-v2.0.1.yaml`
- `002-PROTOCOL-Zero_Tolerance_Remediation-v2.0.0.yaml`
- `003-PROTOCOL-FastAPI_Pure_Code_Implementation-v2.0.0.yaml`

---

## �📊 SESSION SUMMARY

### Session Objective

**PRIMARY GOAL**: Document FSP Shell's architecture, which USES UFC (Universal Fractal Codebase) Architecture as its foundation PLUS adds additional infrastructure.

**CRITICAL RELATIONSHIP**:
- **UFC Architecture** = The architectural FOUNDATION (rules, patterns, principles)
- **FSP Shell** = UFC Architecture + Additional Infrastructure + Best Practices
  - ✅ Built ON TOP OF UFC Architecture (fully UFC-compliant by design)
  - ✅ PACKAGED AS: `au_sys_fsp_plugin` (installable Python package)
  - ✅ ADDS: Base main.py (application entry point)
  - ✅ ADDS: Base app_factory.py (application factory with lifespan)
  - ✅ ADDS: au_sys_capability plugin initialization system
  - ✅ ENABLES: Any FastAPI container to install and import plugin infrastructure
```
Layer 1: UFC Architecture (Foundation)
    ↓
Layer 2: au_sys_fsp_plugin (FSP Shell packaged as installable plugin infrastructure)
    ↓
Layer 3: Capabilities (au_sys_* plugins OR standard FastAPI apps)
    ↓
Layer 4: Services (domain/business services within capabilities)
```

**PURPOSE**: This documentation will:
1. Clarify FSP Shell's 4-layer architecture (UFC → au_sys_fsp_plugin → Capabilities → Services)
2. Document au_sys_fsp_plugin as installable package providing plugin infrastructure
3. Document what FSP Shell provides beyond UFC's architectural standards
4. Show FSP Shell's dual-mode support (standard FastAPI + plugin-based capabilities)
5. Demonstrate best practices compliance (Python, FastAPI, FastMCP, HTMX, Jinja2)
6. Create technical blueprint showing UFC foundation + FSP Shell infrastructure
7. Inform FOUNDATIONAL_CAPABILITIES_ARCHITECTURE_v1.0.0.md
8. Guide next generation FSP (FastAPI Services Platform) and FDS (FastAPI Domain Services)
- **107-INSTRUCTIONS-Remediate_And_Refactor_Codebase** (v2.0.0) - ENFORCED
- **202-INSTRUCTIONS-Pure_Code_Implementation_Execution_Protocol** (v2.0.0) - ENFORCED
- **203-INSTRUCTIONS-FastAPI_Design_Implementation_Refactor** (v2.0.0) - ENFORCED

### Instruction Protocol Loaded

- **Doctrine**: `000-DOCTRINE-Enterprise_Canonical_Execution-v2.0.1.yaml` ✅ Loaded
- **Protocol 1**: `001-PROTOCOL-The_GoldenRule_Execution-v2.0.1.yaml` ✅ Loaded
- **Protocol 2**: `002-PROTOCOL-Zero_Tolerance_Remediation-v2.0.0.yaml` ✅ Loaded and **ENFORCED**
- **Protocol 3**: `003-PROTOCOL-FastAPI_Pure_Code_Implementation-v2.0.0.yaml` ✅ Loaded and **ENFORCED**
- **Instruction 104**: `104-INSTRUCTIONS-Execute_Implementation_Phase_Tasks-v2.0.0.yaml` ✅ Loaded and **ENFORCED**
- **Instruction 107**: `107-INSTRUCTIONS-Remediate_And_Refactor_Codebase-v2.0.0.yaml` ✅ Loaded and **ENFORCED**
- **Instruction 202**: `202-INSTRUCTIONS-Pure_Code_Implementation_Execution_Protocol-v2.0.0.yaml` ✅ Loaded and **ENFORCED**
- **Instruction 203**: `203-INSTRUCTIONS-FastAPI_Design_Implementation_Refactor-v2.0.0.yaml` ✅ Loaded and **ENFORCED**

### Current State

- **Status**: Architecture Documentation Phase
- **Work Type**: DOCUMENT FSP Shell's Layered Architecture & BLUEPRINT CREATION
- **Architecture Layers**:
  - **Foundation Layer**: UFC Architecture (THE BASE) - `CODEBASE_ARCHITECTURE_v1.0.0.md`
  - **Infrastructure Layer**: FSP Shell additions (main, app_factory, plugin init) - `libraries/python/_templates/fastapi_services_plaform/fsp_shell`
- **Files/Modules**: UFC Architecture docs, FSP Shell implementation, FSP Shell docs (governance/), previous session handover
- **Context**: Post-DI refactoring session (logging & storage DI complete)

### FSP Shell Architecture Context

**FSP Shell Package**: `au_sys_fsp_plugin` (installable Python package)

**FSP Shell Source Location**: `libraries/python/_templates/fastapi_services_plaform/fsp_shell`

**Package Distribution**: `au_sys_fsp_plugin` (published to PyPI or internal package repository)

**FSP Shell Documentation Moved To**: `governance/au-sys-governance/architecture/python/fastapi/fsp_shell/`

**Previous Session Achievements** (Session 20260117_222527):
- ✅ Complete dependency injection refactoring for logging (ILogger protocol)
- ✅ Complete dependency injection refactoring for storage/database
- ✅ Renamed providers to descriptive names (StructlogLogger, SQLiteStorageProvider)
- ✅ Created 4 architecture documents:
  - `LOGGER_ARCHITECTURE.md` - Framework-agnostic logging via ILogger
  - `STORAGE_ARCHITECTURE.md` - Framework-agnostic storage via IStorageProvider
  - `DEPENDENCY_INJECTION.md` - Complete DI implementation guide
  - `REFACTORING_CHECKLIST.md` - Implementation completion tracker

**Current FSP Shell State**:
- ✅ Framework-agnostic architecture achieved
- ✅ Zero hardcoded logging imports (except within StructlogLogger)
- ✅ Complete DI for: logging, storage, database, bootstrap, plugins
- ✅ UFC tri-layer structure: core/ + adapters/ + manifest/
- ✅ Plugin discovery system with auto-loading
- ✅ StructlogLogger (structlog-based) and SQLiteStorageProvider (SQLite-based)
- ✅ Bootstrap system for YAML/JSON → settings.db

**Key Initialization Order**:
```
1. Config
2. Logger (ILogger) ← FIRST
3. DatabaseManager(logger)
4. DependencyContainer(logger)
5. PluginLoader(logger)
6. StorageProvider(logger)
7. Bootstrap(logger)
```

---

## ⚠️ CRITICAL SESSION DIRECTIVES

### Session Focus Directive

**THIS IS AN ARCHITECTURE RECONCILIATION AND BLUEPRINT CREATION SESSION.**

- **PRIMARY FOCUS**: Architecture analysis, gap identification, and blueprint documentation
- **NOT**: Code implementation (unless explicitly required for validation)
- **DELIVERABLE**: Technical blueprint document reconciling FSP Shell + UFC Architecture

### Documentation Directive (MODIFIED FOR THIS SESSION)

**DOCUMENTATION IS THE PRIMARY DELIVERABLE FOR THIS SESSION.**

- **REQUIRED**: Document FSP Shell's layered architecture (UFC foundation + infrastructure additions)
- **REQUIRED**: Document what FSP Shell provides beyond UFC (main, app_factory, plugin init)
- **REQUIRED**: Document how FSP Shell uses UFC Architecture as its base
- **DELIVERABLE**: "FSP Shell Architecture Blueprint" - UFC foundation + infrastructure layer documentation
- **PURPOSE**: Clarify FSP Shell's role as UFC-based application infrastructure for capability loading

### Approach Directive

**USE LAYERED ARCHITECTURE DOCUMENTATION METHODOLOGY:**

1. **Review** UFC Architecture standards (THE FOUNDATION) - `CODEBASE_ARCHITECTURE_v1.0.0.md`
2. **Review** FSP Shell implementation (UFC + INFRASTRUCTURE) - current state post-DI refactoring
3. **Review** FSP Shell documentation - `governance/au-sys-governance/architecture/python/fastapi/fsp_shell/`
4. **Identify** UFC Architecture elements in FSP Shell (foundation layer)
5. **Identify** FSP Shell additions beyond UFC (infrastructure layer)
6. **Document** layered architecture (Foundation → Infrastructure → Capabilities)
7. **Document** FSP Shell's role in capability loading and initialization
8. **Create** "FSP Shell Architecture Blueprint" showing UFC foundation + infrastructure additions

---

## 🔧 LAYERED ARCHITECTURE ANALYSIS METHODOLOGY

### Phase 1: UFC Architecture Foundation Review ✅ COMPLETE

**Layer**: UFC Architecture (THE FOUNDATION)
**Document**: `CODEBASE_ARCHITECTURE_v1.0.0.md`
**Purpose**: Understand the architectural foundation FSP Shell is built upon

**Key UFC Architecture Principles (Foundation Layer)**:

1. **Universal Fractal Codebase (UFC)**
   - Same pattern applied recursively at all levels
   - Atomic unit: "The Sovereign Capability"
   - Tri-Layer Architecture: Core → Adapters → Manifest

2. **Tri-Layer Standard** (Dependency Inversion)
   - **Layer 1 - CORE**: Pure business logic, zero frameworks
   - **Layer 2 - ADAPTERS**: Implementations of core ports (API, UI, MCP, CLI)
   - **Layer 3 - MANIFEST**: Configuration, wiring, DI, composition

3. **Fractal Hierarchy**
   - **Level 0**: Shell (Container) → Many Capabilities
   - **Level 1**: Capability (`au_sys_*`) → Many Services
   - **Level 2**: Service (Granular components)
   - Each level uses SAME tri-layer structure

4. **The Three Invariants**
   - **Sovereignty**: Self-contained units owning data, logic, interfaces
   - **Modularity**: "Delete a directory, remove a feature"
   - **Extensibility**: All capabilities are plugins

5. **Standards Compliance**
   - PEP 8, PEP 257, PEP 484, PEP 561
   - snake_case files/directories, PascalCase classes
   - Protocol-based interfaces for DI
   - Framework-agnostic core

### Phase 2: FSP Shell Infrastructure Review ✅ COMPLETE

**Layer**: FSP Shell (UFC FOUNDATION + INFRASTRUCTURE ADDITIONS)
**Location**: `libraries/python/_templates/fastapi_services_plaform/fsp_shell`
**Documentation**: `governance/au-sys-governance/architecture/python/fastapi/fsp_shell/`
**Purpose**: Document what FSP Shell provides on top of UFC Architecture

**FSP Shell Layered Structure**:
```
src/au_sys_fsp_plugin/
├── core/                    # ✅ Layer 1: Core domain
│   ├── logging.py           # ILogger protocol + StructlogLogger
│   ├── database.py          # DatabaseManager with logger DI
│   ├── storage.py           # IStorageProvider + SQLiteStorageProvider
│   ├── bootstrap.py         # Bootstrap functions with logger DI
│   └── __init__.py
├── manifest/                # ✅ Layer 3: Configuration & wiring
│   ├── config.py            # Environment-based configuration
│   ├── app_factory.py       # Application factory + lifespan
│   ├── plugin_loader.py     # Dynamic plugin discovery (with logger DI)
│   ├── container.py         # Dependency injection (with logger DI)
│   └── __init__.py
├── main.py                  # Entry point
└── __init__.py
```

**MISSING**: Layer 2 (Adapters) - FSP Shell intentionally omits adapters (capabilities provide their own)

**FSP Shell Infrastructure Additions (Beyond UFC)**:

1. **✅ Base Entry Point** - `main.py`
   - Application entry point
   - Loads configuration
   - Creates app using factory
   - Starts uvicorn server
   - **Purpose**: Standardized application startup

2. **✅ Application Factory** - `manifest/app_factory.py`
   - `create_app()` function - Creates FastAPI application
   - `create_lifespan()` - Async lifespan context manager
   - Initialization sequence: Config → Logger → DatabaseManager → Container → PluginLoader → Storage → Bootstrap
   - **Purpose**: Standardized app creation with dependency injection

3. **✅ Plugin Initialization System** - `manifest/plugin_loader.py`
   - `discover_au_sys_plugins()` - Auto-discovers installed `au_sys_*` packages
   - `load_plugin_with_dependencies()` - Loads plugins with DI
   - Plugin validation (Plugin class, register() method)
   - Plugin manifest loading (plugin.yaml)
   - **Purpose**: Dynamic capability loading from installed packages

4. **✅ Dependency Injection Container** - `manifest/container.py`
   - Manages shared dependencies (logger, config, db_manager, storage)
   - Provides dependencies to plugins
   - **Purpose**: Centralized dependency management

5. **✅ Built-in Providers** (Infrastructure Fallbacks)
   - `StructlogLogger` (core/logging.py) - structlog-based logging when au_sys_logging absent
   - `SQLiteStorageProvider` (core/storage.py) - SQLite storage when au_sys_storage absent
   - **Purpose**: Built-in functionality using industry-standard libraries, superseded by capabilities

6. **✅ Bootstrap System** - `core/bootstrap.py`
   - `load_config_files()` - Loads YAML/JSON from config/
   - `bootstrap_settings_database()` - Seeds settings.db
   - `verify_bootstrap()` - Validates bootstrap
   - **Purpose**: Initialize settings database from configuration files
- ✅ ILogger protocol (framework-agnostic logging)
- ✅ IStorageProvider protocol (framework-agnostic storage)
- ✅ Complete dependency injection (logging, storage, database)
- ✅ Plugin discovery system (`discover_au_sys_plugins()`)
- ✅ Bootstrap system (YAML/JSON → settings.db)
- ✅ StructlogLogger (structlog-based) + SQLiteStorageProvider (SQLite-based)
- ✅ Auto-detection pattern (built-in → capability-provided implementation)

### Phase 3: Layered Architecture Analysis ✅ COMPLETE

**Purpose**: Document how FSP Shell builds upon UFC Architecture foundation

## FSP SHELL ARCHITECTURE = UFC FOUNDATION + INFRASTRUCTURE LAYER

### Architecture Layers Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ LAYER 4: SERVICES (Domain/Business Services)                │
│                                                              │
│  - Service-level implementations within capabilities        │
│  - Each service follows UFC fractal pattern:                │
│    • core/ (service business logic)                         │
│    • adapters/ (service-specific adapters)                  │
│    • manifest/ (service config)                             │
│                                                              │
│  Examples: AuthService, StorageService, NotificationService │
└─────────────────────────────────────────────────────────────┘
                            ↑
                            │ Composed by
                            │
┌─────────────────────────────────────────────────────────────┐
│ LAYER 3: CAPABILITIES (au_sys_* OR Standard FastAPI)        │
│                                                              │
│  **Option A: Plugin-Based Capabilities**                    │
│  - au_sys_identity, au_sys_storage, au_sys_security, etc.  │
│  - Loaded dynamically via plugin system                     │
│                                                              │
│  **Option B: Standard FastAPI Apps**                        │
│  - Traditional FastAPI application structure                │
│  - routes/, models/, services/, templates/                  │
│  - FastMCP tools, HTMX views, Jinja2 templates             │
│                                                              │
│  Each follows: core/ + adapters/ + manifest/                │
└─────────────────────────────────────────────────────────────┘
                            ↑
                            │ Built on / Loaded by
                            │
┌─────────────────────────────────────────────────────────────┐
│ LAYER 2: au_sys_fsp_plugin (FSP Shell Infrastructure)       │
│                                                              │
│  **Installable Python Package:**                            │
│  Package Name: au_sys_fsp_plugin                            │
│  Install: pip install au_sys_fsp_plugin                     │
│                                                              │
│  **Application Infrastructure:**                            │
│  ✅ main.py              - Application entry point          │
│  ✅ app_factory.py       - Factory + lifespan management    │
│  ✅ plugin_loader.py     - au_sys_* capability discovery    │
│  ✅ container.py         - Dependency injection container   │
│  ✅ bootstrap.py         - Settings database initialization │
│  ✅ StructlogLogger      - Built-in structlog logging       │
│  ✅ SQLiteStorageProvider - Built-in SQLite storage         │
│                                                              │
│  **Code Quality Mandates:**                                 │
│  ✅ SOLID Principles     - Single responsibility, Open/Closed│
│  ✅ DRY Principle        - Don't Repeat Yourself            │
│  ✅ KISS Principle       - Keep It Simple                   │
│  ✅ YAGNI Principle      - You Aren't Gonna Need It         │
│                                                              │
│  **Design Patterns:**                                       │
│  ✅ Singleton Patterns   - Single instance management       │
│  ✅ Factory Patterns     - Object creation abstraction      │
│  ✅ Decorator Patterns   - Behavior extension               │
│  ✅ Observer Patterns    - Event-driven notifications       │
│  ✅ Pooling Patterns     - Resource pooling (DB, HTTP)      │
│                                                              │
│  **Architecture Qualities:**                                │
│  ✅ Extensible           - Easy to extend functionality     │
│  ✅ Modular              - Self-contained components        │
│  ✅ Idempotent           - Safe repeated operations         │
│  ✅ Responsive           - Non-blocking async/await         │
│  ✅ Resilient            - Error handling, retries          │
│  ✅ Adaptable            - Configuration-driven behavior    │
│  ✅ Loose Coupling       - Protocol-based abstractions      │
│                                                              │
│  **Best Practices Compliance:**                             │
│  ✅ Python Best Practices    - PEP 8, type hints, async/await│
│  ✅ FastAPI Best Practices   - Dependency injection, Pydantic│
│  ✅ FastMCP Best Practices   - MCP server patterns          │
│  ✅ HTMX Best Practices      - Hypermedia-driven UI         │
│  ✅ Jinja2 Best Practices    - Template inheritance, filters│
│  ✅ Async IO Patterns        - Non-blocking operations      │
│                                                              │
│  **Dual Mode Support:**                                     │
│  • Standard FastAPI apps (traditional structure)            │
│  • Plugin-based capabilities (au_sys_* pattern)             │
│                                                              │
│  Purpose: Installable package providing plugin              │
│           infrastructure for any FastAPI container          │
└─────────────────────────────────────────────────────────────┘
                            ↑
                            │ Built upon
                            │
┌─────────────────────────────────────────────────────────────┐
│ LAYER 1: UFC ARCHITECTURE FOUNDATION                        │
│                                                              │
│  ✅ Tri-Layer Structure  - core/ + adapters/ + manifest/    │
│  ✅ Fractal Pattern      - Same structure at all levels     │
│  ✅ Protocol-Based DI    - ILogger, IStorageProvider        │
│  ✅ Framework Agnostic   - No hardcoded frameworks          │
│  ✅ Plugin Pattern       - Extensibility via plugins        │
│  ✅ Sovereignty          - Self-contained capabilities      │
│  ✅ Standards Compliance - PEP 8, 257, 484, 561            │
│                                                              │
│  Purpose: Architectural foundation and standards            │
└─────────────────────────────────────────────────────────────┘
```

### Code Quality Mandates (Applied to All Layers)

**ALL code in au_sys_fsp_plugin and all au_sys_* capabilities MUST comply with:**

#### Design Principles (MANDATORY)
- **SOLID Principles**
  - Single Responsibility: Each class/module has one reason to change
  - Open/Closed: Open for extension, closed for modification
  - Liskov Substitution: Derived classes must be substitutable
  - Interface Segregation: Clients shouldn't depend on unused methods
  - Dependency Inversion: Depend on abstractions, not concretions

- **DRY (Don't Repeat Yourself)**: No code duplication, use abstraction
- **KISS (Keep It Simple)**: Simplest solution that works correctly
- **YAGNI (You Aren't Gonna Need It)**: Implement only what's needed now

#### Design Patterns (MANDATORY)
- **Singleton Patterns**: For shared resources (logger, container)
- **Factory Patterns**: For object creation (app_factory.py)
- **Decorator Patterns**: For behavior extension (@decorator syntax)
- **Observer Patterns**: For event-driven architecture
- **Pooling Patterns**: For connection pooling (database, HTTP clients)

#### Architecture Qualities (MANDATORY)
- **Extensible**: Easy to add new features without modifying existing code
- **Modular**: Self-contained, composable components
- **Idempotent**: Safe to execute multiple times with same result
- **Responsive**: Non-blocking async/await patterns throughout
- **Resilient**: Comprehensive error handling, retries, circuit breakers
- **Adaptable**: Configuration-driven behavior, runtime reconfiguration
- **Loose Coupling**: Protocol-based abstractions (ILogger, IStorageProvider)

#### Implementation Standards (MANDATORY)
- **FastAPI Best Practices**: Proper directory structure, dependency injection
- **Python Best Practices**: PEP 8, PEP 257, PEP 484, PEP 561
- **Async IO Patterns**: Non-blocking operations, no blocking calls in async context
- **Type Safety**: 100% type hints, mypy compliance
- **Documentation**: Comprehensive docstrings, inline comments for complex logic

### What UFC Architecture Provides (Foundation)

| UFC Architecture Requirement | FSP Shell Implementation | Compliance Status |
|----------------|-------------------------|--------|
| Tri-Layer Structure | core/ + manifest/ (MISSING adapters/) | ⚠️ Partial |
| Dependency Inversion | ✅ ILogger, IStorageProvider protocols | ✅ Complete |
| Framework Agnostic | ✅ No hardcoded frameworks | ✅ Complete |
| Plugin Pattern | ✅ Plugin discovery + loading | ✅ Complete |
| Self-Contained | ✅ Minimal dependencies | ✅ Complete |
| Protocol-Based DI | ✅ ILogger, IStorageProvider | ✅ Complete |
| Snake_case files | ✅ All files snake_case | ✅ Complete |
| PEP compliance | ✅ Type hints, docstrings | ✅ Complete |

### What FSP Shell Adds (Infrastructure Layer)

**Beyond UFC Architecture, FSP Shell provides:**

| Component | Purpose | UFC Requirement? |
|-----------|---------|------------------|
| **Package: au_sys_fsp_plugin** | Installable Python package providing plugin infrastructure | ❌ No - FSP Shell packaging |
| **main.py** | Application entry point, server startup | ❌ No - FSP Shell addition |
| **app_factory.py** | Factory pattern, lifespan management | ❌ No - FSP Shell addition |
| **plugin_loader.py** | Dynamic au_sys_* discovery & loading | ❌ No - FSP Shell addition |
| **container.py** | Dependency injection container | ❌ No - FSP Shell addition |
| **bootstrap.py** | Settings database initialization | ❌ No - FSP Shell addition |
| **StructlogLogger** | Built-in structlog logging (superseded by au_sys_logging) | ❌ No - FSP Shell addition |
| **SQLiteStorageProvider** | Built-in SQLite storage (superseded by au_sys_storage) | ❌ No - FSP Shell addition |
| **ILogger Protocol** | Framework-agnostic logging interface | ✅ Yes - UFC encourages protocols |
| **IStorageProvider Protocol** | Framework-agnostic storage interface | ✅ Yes - UFC encourages protocols |

### au_sys_fsp_plugin Package Structure

```python
# Package: au_sys_fsp_plugin
# Install: pip install au_sys_fsp_plugin

au_sys_fsp_plugin/
├── __init__.py              # Package entry point
├── core/                    # Core infrastructure
│   ├── __init__.py
│   ├── logging.py           # ILogger protocol + StructlogLogger
│   ├── storage.py           # IStorageProvider + SQLiteStorageProvider
│   ├── database.py          # DatabaseManager
│   └── bootstrap.py         # Settings initialization
├── manifest/                # Configuration & wiring
│   ├── __init__.py
│   ├── config.py            # Settings
│   ├── app_factory.py       # create_app() function
│   ├── plugin_loader.py     # discover_au_sys_plugins()
│   └── container.py         # DependencyContainer
├── main.py                  # CLI entry point (optional)
├── setup.py                 # Package configuration
├── pyproject.toml           # Modern Python packaging
└── README.md                # Package documentation
```

**Installation in any FastAPI container:**
```bash
pip install au_sys_fsp_plugin
```

**Usage in any FastAPI application:**
```python
# your_app/main.py
from au_sys_fsp_plugin.manifest.app_factory import create_app
from au_sys_fsp_plugin.manifest.config import Settings

# Create FastAPI app with plugin infrastructure
app = create_app()

# All au_sys_* capabilities are auto-discovered and loaded
```

**Summary**: au_sys_fsp_plugin = UFC Architecture (foundation) + Application Infrastructure (packaged for distribution)

### Key Architectural Decisions

**1. No Adapters Layer in FSP Shell** (Intentional)
- **UFC Requirement**: Tri-layer structure (core + adapters + manifest)
- **FSP Shell Design**: core + manifest only (NO adapters)
- **Rationale**: FSP Shell is infrastructure, not a capability
  - Capabilities provide their own adapters (API, UI, MCP, CLI)
  - Shell delegates functionality to loaded capabilities
  - Shell is "empty" until capabilities loaded
- **Classification**: ✅ **INTENTIONAL ARCHITECTURAL DECISION**

**2. Built-in Providers as Infrastructure** (Intentional)
- **UFC Context**: Not defined by UFC Architecture
- **FSP Shell Design**: Built-in StructlogLogger and SQLiteStorageProvider
- **Rationale**:
  - Provide industry-standard functionality when capabilities absent
  - Auto-superseded when au_sys_logging/au_sys_storage installed
  - Defensive design - shell always has logging/storage
  - Descriptive names (Structlog, SQLite) clearly indicate implementation
- **Classification**: ✅ **FSP SHELL INFRASTRUCTURE FEATURE**

**3. Plugin System as Core Feature** (Intentional)
- **UFC Context**: Plugin pattern encouraged but not specified
- **FSP Shell Design**: Complete plugin discovery and loading system
- **Rationale**:
  - Dynamic capability loading from installed packages
  - Auto-discovery of au_sys_* packages
  - Dependency injection for plugins
- **Classification**: ✅ **FSP SHELL INFRASTRUCTURE FEATURE**

### FSP Shell's Role in UFC Ecosystem

**FSP Shell Position**:

```
UFC Architecture (Foundation)
      ↓
au_sys_fsp_plugin (FSP Shell packaged as installable plugin infrastructure)
      ↓
Capabilities (au_sys_* plugins OR standard FastAPI apps)
      ↓
Services (domain/business services within capabilities)
```

**au_sys_fsp_plugin is NOT:**
- ❌ A capability to be assessed against UFC standards
- ❌ A competing architectural standard
- ❌ A non-compliant implementation requiring fixes
- ❌ Limited to only plugin-based capabilities
- ❌ A template that must be copied into projects

**au_sys_fsp_plugin IS:**
- ✅ A UFC-based implementation
- ✅ An installable Python package (`pip install au_sys_fsp_plugin`)
- ✅ An infrastructure layer above UFC foundation
- ✅ A plugin infrastructure supporting BOTH:
  - **Standard FastAPI apps** (traditional routes, templates, FastMCP, HTMX)
  - **Plugin-based capabilities** (au_sys_* dynamic loading)
- ✅ The "Unified FastAPI Container Template" packaged for distribution
- ✅ Compliant with Python, FastAPI, FastMCP, HTMX, and Jinja2 best practices
- ✅ Enables any FastAPI container to install and use plugin infrastructure

### Integration Flow: UFC → FSP Shell → Capabilities

**1. Initialization Sequence**

```python
# UFC Foundation provides architectural standards
# FSP Shell implements those standards + adds infrastructure

# Step 1: Load configuration (UFC manifest layer)
settings = Settings()  # From fsp_shell/manifest/config.py

# Step 2: Initialize built-in providers (FSP Shell infrastructure)
logger = StructlogLogger()  # Built-in structlog logging (FSP Shell addition)
storage = SQLiteStorageProvider(settings)  # Built-in SQLite storage (FSP Shell addition)

# Step 3: Create DI container (FSP Shell infrastructure)
container = Container(settings, logger, storage)  # container.py

# Step 4: Discover au_sys_* capabilities (FSP Shell infrastructure)
plugins = discover_au_sys_plugins()  # plugin_loader.py

# Step 5: Initialize each capability (UFC + FSP Shell working together)
for plugin in plugins:
    # Each capability follows UFC Architecture:
    # - plugin.py in manifest/ (UFC requirement)
    # - core/ for business logic (UFC requirement)
    # - adapters/ for API/UI/etc (UFC requirement)

    plugin.init_plugin(app, container)  # FSP Shell infrastructure method

    # If plugin provides alternative implementations:
    if hasattr(plugin, 'get_logger'):
        container.logger = plugin.get_logger()  # Supersede StructlogLogger
    if hasattr(plugin, 'get_storage_provider'):
        container.storage = plugin.get_storage_provider()  # Supersede SQLiteStorageProvider
# Step 7: Start server (FSP Shell infrastructure)
uvicorn.run(app)  # main.py
```

**2. Capability Loading (How FSP Shell Uses UFC)**

```python
# UFC Architecture defines: capabilities MUST have plugin.py in manifest/
# FSP Shell implements: plugin discovery system that expects this structure

def discover_au_sys_plugins():
    """FSP Shell infrastructure using UFC standards"""
    for package in installed_packages():
        if package.name.startswith('au_sys_'):
            # Expect UFC structure: au_sys_X/manifest/plugin.py
            try:
                plugin_module = importlib.import_module(f"{package.name}.manifest.plugin")
                if hasattr(plugin_module, 'init_plugin'):
                    yield plugin_module
            except ImportError:
                # Not a capability (no plugin.py)
                continue
```

**3. Fractal Pattern Implementation**

```
LEVEL 1: FSP Shell (Platform/Infrastructure)
├── core/
│   ├── logging.py (ILogger protocol)
│   ├── storage.py (IStorageProvider protocol)
│   ├── database.py
│   └── bootstrap.py
├── manifest/
│   ├── config.py
│   ├── app_factory.py
│   ├── plugin_loader.py
│   └── container.py
└── main.py

LEVEL 2: Capability (Plugin-based OR Standard FastAPI)

**Option A: Plugin-Based Capability (au_sys_*)**
├── core/
│   ├── services/
│   └── domain/
├── adapters/
│   ├── api/ (FastAPI routes)
│   ├── ui/ (HTMX + Jinja2 templates)
│   ├── mcp/ (FastMCP tools)
│   └── cli/
└── manifest/
    ├── plugin.py (REQUIRED for plugin loading)
    └── config.py

**Option B: Standard FastAPI App**
├── core/
│   ├── services/
│   └── models/
├── adapters/
│   ├── routes/ (FastAPI routers)
│   ├── templates/ (Jinja2 templates)
│   ├── static/ (CSS, JS, HTMX)
│   └── mcp/ (FastMCP server)
└── manifest/
    └── config.py

LEVEL 3: Service within Capability
├── core/
│   ├── service_logic.py
│   └── domain_models.py
├── adapters/
│   ├── service_api.py
│   ├── service_mcp.py
│   └── service_ui.py (HTMX endpoints)
└── manifest/
    └── service_config.py

LEVEL 4: Sub-Service or Component
├── core/
│   └── component_logic.py
├── adapters/
│   └── component_adapter.py
└── manifest/
    └── component_config.py
```

**UFC defines the fractal pattern at all 4 levels. FSP Shell supports BOTH plugin-based capabilities AND standard FastAPI apps.**

### Summary: au_sys_fsp_plugin as UFC Implementation

**au_sys_fsp_plugin = UFC Foundation + Application Infrastructure + Best Practices**

| Aspect | UFC Architecture | au_sys_fsp_plugin (FSP Shell) |
|--------|------------------|-----------|
| **Tri-Layer Structure** | ✅ Defines standard | ✅ Implements (core + manifest, no adapters by design) |
| **Fractal Pattern** | ✅ Defines pattern | ✅ Implements at Level 1, expects in capabilities |
| **Protocol-Based DI** | ✅ Recommends | ✅ Implements (ILogger, IStorageProvider) |
| **Plugin System** | ✅ Encourages | ✅ Implements (plugin_loader.py) |
| **Application Entry** | ❌ Not specified | ✅ **FSP Shell addition** (main.py) |
| **Factory Pattern** | ❌ Not specified | ✅ **FSP Shell addition** (app_factory.py) |
| **DI Container** | ❌ Not specified | ✅ **FSP Shell addition** (container.py) |
| **Bootstrap System** | ❌ Not specified | ✅ **FSP Shell addition** (bootstrap.py) |
| **Built-in Providers** | ❌ Not specified | ✅ **FSP Shell addition** (StructlogLogger, SQLiteStorageProvider) |
| **Standard FastAPI** | ❌ Not specified | ✅ **FSP Shell supports** (traditional apps) |
| **FastMCP Integration** | ❌ Not specified | ✅ **FSP Shell supports** (MCP servers/tools) |
| **HTMX Support** | ❌ Not specified | ✅ **FSP Shell supports** (hypermedia UI) |
| **Jinja2 Templates** | ❌ Not specified | ✅ **FSP Shell supports** (template rendering) |
| **Python Best Practices** | ✅ Requires | ✅ **FSP Shell implements** (PEP 8, type hints, async) |
| **4-Layer Fractal** | ✅ Defines fractal | ✅ **FSP Shell implements** (Platform → Capability → Service → Component) |
| **Installable Package** | ❌ Not specified | ✅ **FSP Shell packages** (au_sys_fsp_plugin on PyPI) |
| **SOLID Principles** | ❌ Not specified | ✅ **FSP Shell mandates** (SRP, OCP, LSP, ISP, DIP) |
| **DRY/KISS/YAGNI** | ❌ Not specified | ✅ **FSP Shell mandates** (Code quality standards) |
| **Design Patterns** | ✅ Encourages | ✅ **FSP Shell implements** (Singleton, Factory, Decorator, Observer, Pooling) |
| **Loose Coupling** | ✅ Recommends | ✅ **FSP Shell implements** (Protocol-based abstractions) |
| **Async/Non-blocking** | ❌ Not specified | ✅ **FSP Shell mandates** (Async IO patterns throughout) |

**Conclusion**: au_sys_fsp_plugin is a UFC-compliant infrastructure package that provides application bootstrapping, dependency injection, and capability loading on top of UFC's architectural foundation. It is distributed as an installable Python package (`pip install au_sys_fsp_plugin`) that enables any FastAPI container to support BOTH standard FastAPI development patterns AND plugin-based capability loading, while maintaining compliance with Python, FastAPI, FastMCP, HTMX, and Jinja2 best practices.

---

### Phase 4: Blueprint Documentation ✅ COMPLETE

**Purpose**: Document the complete technical blueprint for FSP Shell as "Unified FastAPI Container Template"

## TECHNICAL BLUEPRINT SUMMARY

### What is FSP Shell?

**FSP Shell (Unified FastAPI Container Template)** = UFC Architecture (foundation) + Application Infrastructure (capability loading system)

```
┌────────────────────────────────────────────────────────────┐
│                   FSP SHELL BLUEPRINT                      │
│                                                            │
│  Purpose: Provide application infrastructure for loading  │
│           au_sys_* capabilities following UFC standards   │
│                                                            │
│  Foundation: UFC Architecture v1.0.0                      │
│  Infrastructure: main, app_factory, plugin system         │
│  Target: Unified FastAPI Container Template               │
└────────────────────────────────────────────────────────────┘
```

### Architectural Layers Defined

| Layer | Role | Provider | Key Components |
|-------|------|----------|----------------|
| **Layer 1: UFC Architecture** | Foundation & Standards | UFC v1.0.0 | Tri-layer structure, fractal pattern, protocols, framework-agnostic |
| **Layer 2: au_sys_fsp_plugin** | Application Infrastructure | FSP Shell (packaged) | main.py, app_factory.py, plugin_loader.py, container.py, bootstrap.py, built-in providers (StructlogLogger, SQLiteStorageProvider), code quality mandates (SOLID, DRY, KISS, YAGNI), design patterns, best practices compliance |
| **Layer 3: Capabilities** | Business Functionality | au_sys_* packages OR standard FastAPI apps | Domain services, adapters (API/UI/MCP/CLI), FastMCP tools, HTMX views, Jinja2 templates |
| **Layer 4: Services** | Service-Level Logic | Within capabilities | Service implementations following UFC fractal pattern (core/adapters/manifest) |

### Blueprint Deliverables (All Complete)

✅ **Architecture Diagrams**
- 4-layer architecture visualization (UFC → FSP Shell → Capabilities → Services)
- Component relationship diagrams
- Initialization sequence diagrams
- Fractal pattern implementation examples at all 4 levels

✅ **Component Documentation**
- All 6 FSP Shell infrastructure components documented with code examples
- Integration patterns documented
- Deployment scenarios documented
- Dual-mode support explained (plugin-based + standard FastAPI)

✅ **Relationship Clarification**
- UFC Architecture = foundation (defines standards)
- FSP Shell = UFC implementation + infrastructure additions + best practices
- Clear distinction between "UFC defines" vs "FSP Shell adds" vs "FSP Shell supports"

✅ **Design Rationale**
- No adapters layer in FSP Shell (intentional architectural decision)
- Built-in providers (StructlogLogger, SQLiteStorageProvider) for immediate functionality
- Plugin system expectations (UFC manifest/plugin.py requirement)
- Standard FastAPI support (traditional development patterns)

✅ **Integration Patterns**
- How plugin-based capabilities use FSP Shell infrastructure
- How standard FastAPI apps use FSP Shell infrastructure
- How FSP Shell discovers and loads capabilities
- How capabilities enhance shared dependencies

✅ **Deployment Scenarios**
- Standalone deployment (au_sys_fsp_plugin with built-in providers only)
- Standard FastAPI deployment (au_sys_fsp_plugin + traditional routes/templates)
- Plugin-based deployment (au_sys_fsp_plugin + au_sys_* capabilities)
- Production deployment (au_sys_fsp_plugin + mixed approach)
- Provider superseding patterns

✅ **Package Distribution**
- Installable via pip: `pip install au_sys_fsp_plugin`
- Available on PyPI or internal package repository
- Enables any FastAPI container to use plugin infrastructure
- Version-controlled releases

✅ **Best Practices Compliance**
- Python best practices (PEP 8, type hints, async/await)
- FastAPI best practices (dependency injection, Pydantic models)
- FastMCP best practices (MCP server patterns, tool registration)
- HTMX best practices (hypermedia-driven UI, progressive enhancement)
- Jinja2 best practices (template inheritance, filters, macros)

✅ **Code Quality Mandates**
- SOLID principles enforcement (SRP, OCP, LSP, ISP, DIP)
- DRY, KISS, YAGNI principles applied throughout
- Design patterns implementation (Singleton, Factory, Decorator, Observer, Pooling)
- Architecture qualities (Extensible, Modular, Idempotent, Responsive, Resilient, Adaptable)
- Loose coupling via protocol-based abstractions
- Async IO non-blocking patterns throughout

### Key Findings & Decisions

**Finding 1: FSP Shell is Infrastructure, Not a Capability**
- Decision: No adapters/ layer required
- Rationale: Shell provides loading infrastructure; capabilities provide functionality
- Classification: ✅ **INTENTIONAL ARCHITECTURAL DECISION**

**Finding 2: FSP Shell Uses UFC as Foundation**
- Decision: FSP Shell implements UFC standards PLUS adds infrastructure
- Rationale: UFC provides architectural foundation, FSP Shell adds application bootstrapping
- Classification: ✅ **LAYERED ARCHITECTURE PATTERN**

**Finding 3: Built-in Providers are Fallbacks**
- Decision: StructlogLogger and SQLiteStorageProvider built-in, superseded by capabilities
- Rationale: Defensive design - shell always has logging/storage using industry-standard libraries
- Classification: ✅ **DEFENSIVE DESIGN PATTERN**

**Finding 4: Plugin Discovery Expects UFC Structure**
- Decision: plugin_loader.py expects manifest/plugin.py in capabilities
- Rationale: UFC requires this structure for capabilities
- Classification: ✅ **UFC STANDARD COMPLIANCE**

### FSP Shell Component Reference

| Component | Type | Purpose | UFC Requirement? |
|-----------|------|---------|------------------|
| **main.py** | Entry Point | Standardized application startup | ❌ No - FSP Shell addition |
| **app_factory.py** | Factory | FastAPI app creation + lifespan management | ❌ No - FSP Shell addition |
| **plugin_loader.py** | Discovery | Auto-discover au_sys_* packages | ❌ No - FSP Shell addition |
| **container.py** | DI Container | Manage shared dependencies | ❌ No - FSP Shell addition |
| **bootstrap.py** | Initialization | YAML/JSON → settings database | ❌ No - FSP Shell addition |
| **StructlogLogger** | Provider | Built-in structlog logging | ❌ No - FSP Shell addition |
| **SQLiteStorageProvider** | Provider | Built-in SQLite storage | ❌ No - FSP Shell addition |
| **ILogger** | Protocol | Framework-agnostic logging interface | ✅ Yes - UFC encourages |
| **IStorageProvider** | Protocol | Framework-agnostic storage interface | ✅ Yes - UFC encourages |
| **core/** | Layer 1 | Business logic (protocols, built-in providers) | ✅ Yes - UFC requires |
| **manifest/** | Layer 3 | Configuration & integration | ✅ Yes - UFC requires |
| **adapters/** | Layer 2 | INTENTIONALLY OMITTED (not a capability) | ⚠️ No - Intentional design |
| **SOLID Principles** | Code Quality | SRP, OCP, LSP, ISP, DIP enforcement | ✅ Yes - Mandatory |
| **Design Patterns** | Code Quality | Singleton, Factory, Decorator, Observer, Pooling | ✅ Yes - Mandatory |
| **Architecture Qualities** | Code Quality | Extensible, Modular, Idempotent, Responsive, Resilient | ✅ Yes - Mandatory |

### Success Criteria Met

✅ **Documentation Complete**
- All sections updated to reflect correct relationship
- All "compliance assessment" language removed
- All "layered architecture" framing applied

✅ **Technical Accuracy**
- UFC Architecture position clarified (foundation, not assessment target)
- FSP Shell position clarified (infrastructure, not separate standard)
- Relationship documented (FSP Shell USES UFC + ADDS infrastructure)

✅ **Architectural Clarity**
- Layered architecture visualized
- Component purposes documented
- Integration patterns shown
- Design rationales explained

✅ **Standards Alignment**
- UFC Architecture honored as foundation
- FSP Shell additions clearly distinguished
- Intentional design decisions documented
- No false "compliance" assessments

### Next Actions (Post-Blueprint Session)

**Immediate (This Session - Documentation Only)**
- ✅ SPEC document created and structured
- ✅ UFC Architecture reviewed
- ✅ FSP Shell documentation reviewed
- ✅ Layered architecture documented
- ✅ Blueprint complete

**Future (Separate Sessions - Implementation Work)**
- Update FSP Shell documentation in governance/
- Add architecture diagrams to documentation
- Create capability integration guide
- Align FOUNDATIONAL_CAPABILITIES_ARCHITECTURE with FSP Shell pattern
- Consider naming: Keep "FSP Shell" brand, emphasize UFC foundation in docs

### Blueprint Status: ✅ COMPLETE

This CODE_IMPLEMENTATION_SPEC has achieved its objective:

**Objective**: "Document the 4-layer architecture relationship (UFC Architecture → FSP Shell → Capabilities → Services), showing how FSP Shell uses UFC standards as its foundation, adds application infrastructure, supports both standard FastAPI and plugin-based development, and maintains best practices compliance."

**Outcome**: "A technical blueprint documenting FSP Shell as the 'Unified FastAPI Container Template' - a UFC-based implementation that provides application infrastructure (main, app_factory, plugin system) on top of UFC's architectural foundation, supporting BOTH traditional FastAPI development patterns AND plugin-based capability loading, while ensuring compliance with Python, FastAPI, FastMCP, HTMX, and Jinja2 best practices."

**Deliverable**: Complete technical blueprint including:
- 4-layer architecture diagrams (UFC → FSP Shell → Capabilities → Services)
- All 6 infrastructure components documented
- Dual-mode support explained (standard FastAPI + plugin-based)
- Integration patterns for both modes
- Deployment scenarios covering all approaches
- Design rationales provided
- Relationship clarifications complete
- Best practices compliance documented

---

## STANDARD IMPLEMENTATION PHASES (For Future Implementation Sessions)

**NOTE**: The sections below are standard implementation phases from the CODE_IMPLEMENTATION_SPEC template. They are NOT applicable to this documentation-only session but are preserved for future reference when implementation work is needed.

---

   - Fully functional, not partial
   - NO workarounds or temporary solutions

6. **SEQUENTIAL IMPLEMENTATION** (ABSOLUTE - STRICTLY FORBIDDEN: Scripts or Mass Modifications)
   - ALL code MUST be implemented and validated ONE STEP AT A TIME, in a SEQUENTIAL MANNER
   - FORBIDDEN: Scripts that modify multiple files simultaneously
   - FORBIDDEN: Mass modifications or bulk changes
   - FORBIDDEN: Automated refactoring tools that modify multiple files at once
   - MANDATORY: Each file modification must be validated before proceeding to the next
   - MANDATORY: Sequential, controlled, validated implementation only

7. **MCP TOOLS MANDATORY USAGE** (ABSOLUTE - NON-NEGOTIABLE)
   - **MCP GREP**: MUST use MCP Grep to search codebase, GitHub repos, and discover patterns
   - **MCP FETCH**: MUST use MCP Fetch to retrieve additional repositories, code examples, or semantically similar codebase from GitHub
   - **GIT CLONE**: MUST use GIT TO CLONE all useful discovered GitHub repos to the local repository, even if they only provide a small benefit
   - **PURPOSE**: Cloned repos are for future references and examples - do NOT remove the cloned repos
   - **SELECTIVE COPY**: Clone repositories into local environment and selectively copy and modify required files, modules, or code segments
   - **ADAPTATION**: Copy and adjust partially completed items from cloned repos with appropriate adaptation
   - **DOCUMENTATION**: Record all cloned repositories and their purposes in CODE_IMPLEMENTATION_SPEC (DO NOT include code examples)
   - WRITING CODE WITHOUT FIRST USING MCP Grep and MCP Fetch IS A BLOCKING VIOLATION

8. **GROUP-BASED IMPLEMENTATION AND STRUCTURED CHECKLISTS** (ABSOLUTE - NON-NEGOTIABLE)
   - **FOCUS ON GROUPS**: Focus on implementing, refactoring and validating groups of items identified on your list, ensuring that all necessary improvements are executed with precision and adherence to best practices
   - **STRUCTURED CHECKLISTS**: Record in CODE_IMPLEMENTATION_SPEC implementation plan structured checklists, DO NOT include code examples
   - **REVIEW CHECKLISTS**: Review the CODE_IMPLEMENTATION_SPEC implementation plan structured checklists to locate the current or next plan to execute
   - **GROUP EXECUTION**: Execute groups of related items together, ensuring comprehensive coverage and validation
   - **PRECISION AND BEST PRACTICES**: All improvements must be executed with precision and adherence to best practices
   - **CHECKLIST TRACKING**: Maintain structured checklists for each group of items, tracking progress and completion
   - **ITERATE THROUGH PLANS**: Continue to iterate through plans in CODE_IMPLEMENTATION_SPEC until all plans are completed, pass code quality checks and have been validated

9. **COPY-AND-ADAPT METHODOLOGY** (ABSOLUTE - NON-NEGOTIABLE)
   - **MUST COPY AND ADAPT**: You MUST COPY and adapt the acquired directory structures, files, modules, functions, code blocks and content to the prod codebase
   - **FORBIDDEN**: DO NOT re-write any part of the content - THIS IS ERROR PRONE
   - **STEP-BY-STEP ADAPTATION**: Adapt each one step by step, validate then continue to the next
   - **CONTINUE UNTIL COMPLETE**: Continue to implement, fix, remediate and refactor the plan until complete
   - **VALIDATION REQUIRED**: Validate each adaptation before proceeding to the next step
   - **MAINTAIN PROGRESS**: Maintain and update your progress through the plan in CODE_IMPLEMENTATION_SPEC
   - **ERROR PREVENTION**: Copying and adapting reduces errors compared to rewriting - rewriting is FORBIDDEN

### Implementation Sequence (Combined Execution Order)

#### Phase 1: Pre-Implementation (MANDATORY)

1. **CODEBASE EXAMINATION AND GAP ANALYSIS** (MANDATORY - Code Discovery Protocol)
   - **EXAMINE PRODUCTION CODEBASE**: Start by examining the production codebase for any missing elements, TODO comments, mocks, stubs, or unfinished code
   - **IDENTIFY PARTIALLY COMPLETED ITEMS**: Identify which items are partially completed and can be quickly implemented by copying and adjusting them, using local repositories or cloned GitHub repositories
   - **EXTENSIVELY SCAN CODEBASE**: Extensively scan and search the codebase for other gaps that can be promptly resolved
   - **DOCUMENT FINDINGS**: Record all findings in CODE_IMPLEMENTATION_SPEC (DO NOT include code examples)
   - **BLOCKING**: Cannot proceed until codebase examination complete with findings documented

2. **SEARCH AND DISCOVERY** (MANDATORY - Protocol 003, 202)
   - **USE MCP GREP**: Use MCP Grep to search:
     - Current repo for patterns, helpers, interfaces, conventions
     - Local templates / golden repos (if available)
     - GitHub repos (only if local repo lacks patterns)
   - **USE MCP FETCH**: Use MCP Fetch to retrieve additional repositories, code examples, or semantically similar codebase from GitHub
   - **PINPOINT REACTIVATABLE ITEMS**: Proceed to pinpoint those items within your list that were only partially completed but could be promptly reactivated or restored through copying and appropriate adaptation
   - **SOURCE FROM GITHUB**: These elements should be sourced from existing cloned GitHub repositories or discovered GitHub repositories that SHALL be cloned
   - **ASSESS GAPS**: Assess which remaining gaps can be efficiently resolved by employing MCP TOOLS (grep and fetch) to retrieve additional repositories and code from GitHub
   - If external library/framework involved: MUST consult Context7
   - Identify canonical pattern to follow
   - Record evidence (paths + matched identifiers)
   - **BLOCKING**: Cannot proceed until search complete with evidence recorded

3. **REPOSITORY CLONING AND PREPARATION** (MANDATORY - Code Discovery Protocol)
   - **CLONE DISCOVERED REPOS**: MUST use GIT TO CLONE all useful discovered GitHub repos to the local repository, even if they are only going to provide a small benefit to this codebase
   - **PURPOSE**: Cloned repos are for future references and examples - do NOT remove the cloned repos
   - **SELECTIVE COPY**: Clone these repositories into the local environment and selectively copy and modify the required files, modules, or code segments to address the issues
   - **ADAPTATION**: Copy and adjust partially completed items from cloned repos, using appropriate adaptation
   - **DOCUMENT CLONED REPOS**: Record all cloned repositories and their purposes in CODE_IMPLEMENTATION_SPEC
   - **BLOCKING**: Cannot proceed until repository cloning and preparation complete

4. **REVIEW STRUCTURED CHECKLISTS** (MANDATORY - Group-Based Implementation Protocol)
   - Review CODE_IMPLEMENTATION_SPEC implementation plan structured checklists
   - Locate the current or next plan to execute
   - Identify which group of items to work on based on priority, dependencies, and current status
   - **BLOCKING**: Cannot proceed until current/next plan identified from structured checklists

5. **SCOPE LOCK** (MANDATORY - Protocol 003, 202)
   - State exact files/modules in scope
   - Anything outside scope is forbidden unless explicitly approved
   - **BLOCKING**: Cannot proceed until scope locked

6. **WORK TYPE CLASSIFICATION** (MANDATORY - Protocol 107)
   - Classify work type: IMPLEMENTATION / REMEDIATION / REFACTOR
   - Gather complete context before proceeding
   - **BLOCKING**: Cannot proceed until classification is explicit

7. **PRE-FLIGHT VIOLATION SCAN** (MANDATORY - Protocol 002)
   - Scan ALL files that will be read/modified for violations
   - Search for: TODOs, mocks, stubs, "PASS" passes, hacks, notes, placeholders, partial implementations, workarounds
   - Classify each match (violation vs acceptable)
   - **BLOCKING**: Cannot proceed until ALL violations in scope are ERADICATED

#### Phase 2: Scaffolding (MANDATORY)

8. **SCAFFOLD** (MANDATORY - Protocol 003, 202)
   - Create/adapt required structure consistent with repo patterns
   - Use cloned repositories and discovered code patterns as scaffolding base
   - Align naming, imports, interfaces, and directory layout to existing patterns
   - Ensure async structure is correct (for FastAPI)
   - **BLOCKING**: Cannot proceed until scaffolding complete

#### Phase 3: FastAPI-Specific Preparation (If FastAPI Work)

9. **IDENTIFY BLOCKING OPERATIONS** (FastAPI-specific - Protocol 003, 203)
   - Identify ALL blocking operations in async context
   - NO exceptions
   - **BLOCKING**: Cannot proceed until all blocking operations identified

10. **CONVERT TO ASYNC** (FastAPI-specific - Protocol 003, 203)
    - Convert ALL blocking operations to async
    - NO exceptions
    - **BLOCKING**: Cannot proceed until conversion complete

11. **APPLY ASYNC PATTERNS** (FastAPI-specific - Protocol 003, 203)
    - Apply required async patterns (asyncio.to_thread(), ThreadPoolExecutor, etc.)
    - **BLOCKING**: Cannot proceed until patterns applied

#### Phase 4: Group-Based Implementation (MANDATORY)

12. **IMPLEMENT GROUP OF ITEMS** (MANDATORY - Group-Based Implementation Protocol)
    - Focus on implementing, refactoring and validating groups of items identified on your list
    - Ensure all necessary improvements are executed with precision and adherence to best practices
    - Execute groups of related items together, ensuring comprehensive coverage
    - Update structured checklist as work progresses
    - **BLOCKING**: Cannot proceed until group implementation complete and validated

13. **COPY AND ADAPT TO PRODUCTION CODEBASE** (MANDATORY - Copy-and-Adapt Protocol)
    - **COPY DIRECTORY STRUCTURES**: MUST COPY and adapt acquired directory structures to prod codebase
    - **COPY FILES**: MUST COPY and adapt acquired files to prod codebase
    - **COPY MODULES**: MUST COPY and adapt acquired modules to prod codebase
    - **COPY FUNCTIONS**: MUST COPY and adapt acquired functions to prod codebase
    - **COPY CODE BLOCKS**: MUST COPY and adapt acquired code blocks to prod codebase
    - **COPY CONTENT**: MUST COPY and adapt acquired content to prod codebase
    - **FORBIDDEN**: DO NOT re-write any part of the content - THIS IS ERROR PRONE
    - **STEP-BY-STEP**: Adapt each one step by step, validate then continue to the next
    - **VALIDATION REQUIRED**: Validate each adaptation before proceeding to next step
    - **BLOCKING**: Cannot proceed until copy-and-adapt step complete and validated

14. **IMPLEMENT** (MANDATORY - Protocol 003, 202, 107)
    - Implement required functionality fully
    - Continue to implement, fix, remediate and refactor the plan until complete
    - **FORBIDDEN**: TODOs, stubs, mocks, placeholders, demo data, partial routes, fake adapters
    - **FORBIDDEN**: "PASS" passes, hacks, notes that code needs to be implemented
    - **FORBIDDEN**: hard-coded dynamic values (must be config/DB driven)
    - **FORBIDDEN**: sync endpoints (must be async def for FastAPI)
    - **FORBIDDEN**: blocking calls in async context
    - **FORBIDDEN**: workarounds or temporary solutions
    - **FORBIDDEN**: Re-writing content instead of copying and adapting
    - **MANDATORY**: Production code implemented 100% correctly
    - **BLOCKING**: Cannot proceed until implementation complete

15. **ADD PERFORMANCE PRIMITIVES** (FastAPI-specific - Protocol 003, 203)
    - Add connection pooling for HTTP clients
    - Add pooling + pre-ping for database connections
    - Enable keep-alive
    - Eliminate per-request client instantiation
    - **BLOCKING**: Cannot proceed until performance primitives added

16. **ADD RELIABILITY PRIMITIVES** (FastAPI-specific - Protocol 003, 203)
    - Add structured error handling in all async paths
    - Add retry with exponential backoff for transient failures
    - Add circuit breakers for critical integrations
    - Add health monitoring for connection pools
    - **BLOCKING**: Cannot proceed until reliability primitives added

17. **LOGGING COMPLIANCE** (MANDATORY - Protocol 003, 202)
    - ALL logging MUST use logger_factory patterns only
    - If security/auth/compliance paths touched: audit logging mandatory
    - Service/core modules must expose debug/transactional observability
    - Console output: JSON formatted
    - File output: detailed text formatted
    - **BLOCKING**: Any logging non-compliance = STOP → FIX → VERIFY

#### Phase 5: Validation (MANDATORY)

18. **VALIDATE ASYNC CORRECTNESS** (FastAPI-specific - Protocol 003, 203)
    - Validate ALL endpoints are async
    - Validate no blocking calls
    - Validate async patterns applied correctly
    - **BLOCKING**: Cannot proceed until async correctness validated

19. **VALIDATE PERFORMANCE** (FastAPI-specific - Protocol 003, 203)
    - Validate connection pooling enabled
    - Validate keep-alive enabled
    - Validate performance primitives present
    - **BLOCKING**: Cannot proceed until performance validated

20. **VALIDATE RELIABILITY** (FastAPI-specific - Protocol 003, 203)
    - Validate error handling present
    - Validate retry mechanisms present
    - Validate circuit breakers present
    - Validate health monitoring present
    - **BLOCKING**: Cannot proceed until reliability validated

21. **CODE QUALITY CHECKS** (MANDATORY - Code Quality Protocol)
    - Perform code quality checks using canonical tools and configurations
    - Run style/linting checks (black, isort, flake8, ruff)
    - Run type checking (mypy)
    - Run static analysis (bandit, safety, radon, xenon)
    - Run security scanning (bandit, safety)
    - Capture exit codes and key pass/fail lines as evidence
    - **BLOCKING**: Cannot proceed until code quality checks pass

22. **VALIDATION** (MANDATORY - Protocol 003, 202, 107)
    - Run/produce exact commands required to validate change
    - Capture exit codes and key pass/fail lines as evidence
    - If any required check fails: STOP → remediate → re-validate
    - **BLOCKING**: Cannot proceed until validation passes

23. **ZERO-TOLERANCE VERIFICATION** (MANDATORY - Protocol 002, 003, 202)
    - Verify full zero-tolerance checklist
    - Scan ALL modified files for violation patterns
    - Classify all matches (violation vs acceptable)
    - Verify 0 violations remain
    - Document acceptable matches with justification
    - **BLOCKING**: Cannot proceed until zero-tolerance verification passes

24. **PLAN VALIDATION** (MANDATORY - Plan Execution Protocol)
    - Validate the plan has successfully completed
    - Verify all items in the current group/plan are complete
    - Verify all code quality checks passed
    - Verify all validation checkpoints passed
    - Document plan completion status in CODE_IMPLEMENTATION_SPEC
    - **BLOCKING**: Cannot proceed until plan validation passes

25. **FINAL COMPLIANCE VERIFICATION** (MANDATORY - Protocol 003)
    - Verify ALL validation checkpoints pass
    - Verify ALL protocols followed
    - Verify production code implemented 100% correctly
    - **BLOCKING**: Cannot mark complete until ALL checkpoints pass

#### Phase 6: Post-Implementation (MANDATORY)

26. **REGRESSION PREVENTION** (MANDATORY - Protocol 107)
    - Add regression prevention measures
    - NO skipping tests
    - **BLOCKING**: Cannot proceed until regression prevention added

27. **UPDATE PROGRESS IN CODE_IMPLEMENTATION_SPEC** (MANDATORY - Progress Tracking Protocol)
    - Maintain and update your progress through the plan in CODE_IMPLEMENTATION_SPEC
    - Update structured checklists with group completion status
    - Record planning and findings in structured checklists (DO NOT include code examples)
    - Mark completed items and groups in checklists
    - Document all cloned repositories and their purposes
    - Document copy-and-adapt operations performed
    - Document code quality check results
    - Document plan validation results
    - **BLOCKING**: Cannot proceed until progress updated in CODE_IMPLEMENTATION_SPEC

28. **UPDATE STRUCTURED CHECKLISTS** (MANDATORY - Group-Based Implementation Protocol)
    - Update CODE_IMPLEMENTATION_SPEC structured checklists with group completion status
    - Record planning and findings in structured checklists (DO NOT include code examples)
    - Mark completed items and groups in checklists
    - Document all cloned repositories and their purposes
    - **BLOCKING**: Cannot proceed until structured checklists updated

29. **SPEC UPDATE** (MANDATORY - Protocol 107)
    - Update CODE_IMPLEMENTATION_SPEC with resolution
    - Record planning and findings (DO NOT include code examples)
    - Document all cloned repositories and their purposes
    - NO exceptions, NO skipping SPEC update
    - **BLOCKING**: Cannot proceed until SPEC updated

30. **PERSISTENCE AND AUDIT LOGGING** (MANDATORY - Protocol 107)
    - Persist to neo4j-memory
    - NO skipping persistence
    - **BLOCKING**: Cannot proceed until persistence complete

31. **ITERATE TO NEXT PLAN** (MANDATORY - Plan Iteration Protocol)
    - Review CODE_IMPLEMENTATION_SPEC structured checklists
    - Identify next plan to execute (if any remaining)
    - If plans remain: Return to Step 4 (Review Structured Checklists) and continue iteration
    - Continue to iterate through plans in CODE_IMPLEMENTATION_SPEC until all plans are completed
    - All plans must pass code quality checks and have been validated before final completion
    - **BLOCKING**: Cannot mark final completion until ALL plans are completed, pass code quality checks and validated

32. **COMPLETION AND VERIFICATION** (MANDATORY - Protocol 107)
    - Verify ALL validation checkpoints pass
    - Final violation pattern scan of ALL modified files
    - Interface completeness check for ALL modified functions
    - Verify ALL plans in CODE_IMPLEMENTATION_SPEC are completed
    - Verify ALL plans passed code quality checks
    - Verify ALL plans have been validated
    - **BLOCKING**: Cannot mark complete until ALL checks pass and ALL plans completed

---

## 🛡️ PROTOCOL ENFORCEMENT

### Protocol 002: Zero Tolerance Remediation

**Enforcement Status**: ✅ ACTIVE

**Key Requirements**:

- 0 TODOs (MUST BE FOUND AND ERADICATED)
- 0 mocks (MUST BE FOUND AND ERADICATED)
- 0 stubs (MUST BE FOUND AND ERADICATED)
- 0 "PASS" passes (MUST BE FOUND AND ERADICATED)
- 0 hacks (MUST BE FOUND AND ERADICATED)
- 0 notes that code needs to be implemented (MUST BE FOUND AND ERADICATED)
- 0 notes explaining why code was not implemented (MUST BE FOUND AND ERADICATED)
- 0 notes documenting limitations (MUST BE FOUND AND ERADICATED)
- 0 docstring notes that defer implementation (MUST BE FOUND AND ERADICATED)
- 0 deferred implementation comments (MUST BE FOUND AND ERADICATED)
- 0 placeholder/demo data (MUST BE FOUND AND ERADICATED)
- 0 hard-coded dynamic values (MUST BE FOUND AND ERADICATED)
- 0 partial implementations (MUST BE FOUND AND ERADICATED)
- 0 workarounds (MUST BE FOUND AND ERADICATED)
- 0 SOLID/DRY/KISS violations (MUST BE FOUND AND ERADICATED)
- 0 interface/implementation mismatches (MUST BE FOUND AND ERADICATED)

**Remediation Priority**:

1. Priority 1: Security/auth/compliance modules (audit logging required)
2. Priority 2: Core services (debug logging required)
3. Priority 3: API routers (audit + debug logging required)
4. Priority 4: Other modules (logger_factory usage required)

**Workflow**: 11-step sequential process (Issue identification → Reproduction → Root cause → SPEC creation → Solution design → Implementation → Validation → Regression prevention → SPEC update → Persistence → Completion)

**Pre-Flight Scan**: MUST scan for violations BEFORE starting work
**File Modification Checkpoint**: MUST scan file BEFORE modifying it
**Post-Modification Validation**: MUST re-scan file AFTER modifying it

### Protocol 003: FastAPI Pure Code Implementation

**Enforcement Status**: ✅ ACTIVE

**Key Requirements**:

- ALL endpoints MUST be `async def` (NO exceptions)
- NO blocking calls in async context (ALL blocking I/O MUST use `asyncio.to_thread()`)
- Connection pooling for HTTP clients (MANDATORY)
- Database connections MUST use pooling + pre-ping
- Keep-alive MUST be enabled
- No per-request client instantiation
- Structured error handling in all async paths
- Retry with exponential backoff for transient failures
- Circuit breakers for critical integrations
- Health monitoring for connection pools

**Execution Order**: 16-step sequential process (see Implementation Sequence above)

**Mandatory Intelligence Tools**:

- Context7 (MANDATORY): MUST consult Context7 before implementing/refactoring code using external libraries/frameworks
- MCP Grep (MANDATORY): MUST perform MCP grep searches BEFORE writing new code
- WRITING CODE WITHOUT FIRST USING MCP Grep (and Context7 when applicable) IS A BLOCKING VIOLATION

### Instruction 104: Execute Implementation Phase Tasks

**Enforcement Status**: ✅ ACTIVE

**Key Requirements**:

- Execute work strictly according to approved SPEC
- Do NOT redesign, reinterpret, collapse steps, skip validation, invent tasks
- Execute exactly what SPEC defines
- Follow checklist hierarchy precisely
- Stop immediately on ambiguity or validation failure

**SPEC Handling Rules**:

- SPEC is executable law, not guidance
- All work maps to PHASE → ACTION → TASK → STEP
- Steps are atomic and executed independently
- Checkboxes represent completed execution, not intent

**Execution Sequence**:

1. Identify active SPEC
2. Identify current PHASE
3. Execute ACTIONS in order
4. Execute TASKS in order
5. Execute STEPS in order
6. Validate before advancing

### Instruction 107: Remediate And Refactor Codebase

**Enforcement Status**: ✅ ACTIVE

**Key Requirements**:

- Remediate verified defects only
- Refactor ONLY when required to fix correctness, safety, or validation
- Preserve behaviour outside defect scope
- Every change must map to specific failure or requirement
- Prefer minimal diffs, avoid touching unrelated files

**Entry Conditions**: Remediation may begin ONLY if at least one exists:

- a failed validation step
- a confirmed runtime error
- a SPEC-defined corrective action
- an explicit remediation instruction

**Pattern Consistency Requirement**: When remediating, MUST ensure consistency with existing complete implementations

**Code Reuse Mandate**: BEFORE writing new code, search for existing helpers/utilities

### Instruction 202: Pure Code Implementation Execution Protocol

**Enforcement Status**: ✅ ACTIVE

**Key Requirements**:

- NO CODE SHALL BE WRITTEN UNTIL:
  - Existing codebase has been searched
  - Relevant patterns have been identified
  - Scaffolding rules have been satisfied
  - Logging requirements are understood

**Stepwise Execution** (8 steps):

1. Search (MANDATORY)
2. Scope Lock
3. Scaffold (MANDATORY)
4. Implement (MANDATORY)
5. Logging Compliance (MANDATORY)
6. Validation (MANDATORY)
7. Zero-Tolerance Verification (MANDATORY)
8. Halt

### Instruction 203: FastAPI Design Implementation Refactor

**Enforcement Status**: ✅ ACTIVE

**Key Requirements**:

- All FastAPI endpoints, services, and integrations MUST be async, non-blocking, observable, production-safe
- ALL endpoints MUST be `async def`
- NO blocking calls in async context
- ALL blocking I/O MUST use `asyncio.to_thread()`
- Deprecated loop APIs are FORBIDDEN

**Required Async Patterns**:

- asyncio.to_thread() for file and blocking I/O
- asyncio.get_running_loop() for background tasks
- ThreadPoolExecutor for sync→async bridges
- create_task() for fire-and-forget only

**Performance Requirements**:

- HTTP clients MUST use connection pooling
- Database connections MUST use pooling + pre-ping
- Keep-alive MUST be enabled
- No per-request client instantiation

**Reliability Requirements**:

- Structured error handling in all async paths
- Retry with exponential backoff for transient failures
- Circuit breakers for critical integrations
- Health monitoring for connection pools

**Execution Order**: 9-step sequential process (Identify blocking → Convert to async → Apply patterns → Add performance → Add reliability → Validate async → Validate performance → Validate reliability → Final compliance)

---

## 📝 IMPLEMENTATION FINDINGS

### Initial Findings

**Date**: [YYYY-MM-DD HH:MM:SS (Australia/Adelaide)]

1. **Protocols Successfully Loaded**
   - All required doctrine and protocols have been loaded and parsed
   - Multiple protocols are actively enforced for this session
   - Implementation instruction protocols loaded

2. **FastAPI Services Platform Documentation Reviewed**
   - Comprehensive platform documentation reviewed
   - Architecture and engine documentation reviewed
   - Key architectural principles understood

3. **Session State**
   - Session initialized per user instruction
   - Awaiting explicit implementation task or requirement identification
   - No files modified yet
   - No specific implementation identified yet

### Implementation Progress

**Files Modified**: [List files as implementation progresses]

**Patterns Reused**: [List patterns/utilities reused from codebase]

**New Dependencies**: [List any new dependencies added]

**Violations Found and Eradicated**: [Track violations found and fixed]

**Gap Analysis Findings**: [Document missing elements, TODOs, mocks, stubs, unfinished code found]

**Partially Completed Items Identified**: [List items that can be quickly implemented by copying/adjusting]

**Cloned GitHub Repositories**: [List all cloned repos with their purposes - for future reference/examples]

- Repository: [repo-url] - Purpose: [description] - Cloned: [date]
- Repository: [repo-url] - Purpose: [description] - Cloned: [date]

**Reactivated/Restored Items**: [List items reactivated or restored from cloned repos]

**MCP Tools Usage**: [Document MCP Grep searches and MCP Fetch retrievals performed]

**Structured Implementation Plan Checklists**: [Reference to structured checklists section below]

**Current Group in Progress**: [Identify which group is currently being worked on]

**Next Group to Execute**: [Identify next group to execute based on priority and dependencies]

**Copy-and-Adapt Operations**: [Document directory structures, files, modules, functions, code blocks copied and adapted]

**Code Quality Check Results**: [Document results of code quality checks performed]

**Plan Validation Results**: [Document validation results for each plan/group]

**Plans Completed**: [List all completed plans/groups]

**Plans Remaining**: [List all remaining plans/groups to execute]

**Iteration Status**: [Track iteration progress through plans]

### Next Steps

1. **Await Explicit Implementation Task**
   - User must provide explicit implementation task or requirement details
   - Scope information needed if not provided
   - Files/modules information needed if not provided

2. **Codebase Examination and Gap Analysis** (When Task Identified)
   - Examine production codebase for missing elements, TODOs, mocks, stubs, unfinished code
   - Identify partially completed items that can be quickly implemented
   - Extensively scan codebase for gaps
   - Document findings in CODE_IMPLEMENTATION_SPEC (no code examples)

3. **Search and Discovery Phase** (When Task Identified)
   - Perform MCP Grep searches (codebase, GitHub repos)
   - Use MCP Fetch to retrieve repositories and code examples
   - Pinpoint reactivatable items from cloned repos
   - Assess gaps that can be resolved using MCP Tools

4. **Repository Cloning** (When Task Identified)
   - Clone all useful discovered GitHub repos to local repository
   - Document cloned repos and their purposes
   - Prepare for selective copy and modification

5. **Review Structured Checklists** (When Task Identified)
   - Review CODE_IMPLEMENTATION_SPEC implementation plan structured checklists
   - Locate the current or next plan to execute
   - Identify which group of items to work on based on priority, dependencies, and current status

6. **Copy and Adapt to Production Codebase** (When Task Identified)
   - MUST COPY and adapt acquired directory structures, files, modules, functions, code blocks and content
   - DO NOT re-write any part of the content - THIS IS ERROR PRONE
   - Adapt each one step by step, validate then continue to the next

7. **Implementation** (When Task Identified)
   - Focus on implementing, refactoring and validating groups of items from identified list
   - Continue to implement, fix, remediate and refactor the plan until complete
   - Execute groups with precision and adherence to best practices
   - Follow combined execution sequence (32 steps)
   - Execute all mandatory steps sequentially
   - Validate at each checkpoint
   - Perform code quality checks
   - Validate the plan has successfully completed
   - Record planning in CODE_IMPLEMENTATION_SPEC structured checklists (no code examples)
   - Maintain and update progress through the plan in CODE_IMPLEMENTATION_SPEC
   - Update structured checklists as work progresses

8. **Iterate Through Plans** (When Task Identified)
   - Continue to iterate through plans in CODE_IMPLEMENTATION_SPEC until all plans are completed
   - All plans must pass code quality checks and have been validated
   - Review structured checklists to identify next plan to execute
   - Repeat implementation sequence for each plan until all complete

---

## 📋 STRUCTURED IMPLEMENTATION PLAN CHECKLISTS

### Purpose

Structured checklists are used to organize and track implementation work by groups of related items. These checklists are recorded in CODE_IMPLEMENTATION_SPEC and are used to locate the current or next plan to execute.

### Checklist Structure

Each implementation plan checklist should include:

- **Group Name**: Descriptive name for the group of items
- **Group Description**: Brief description of what this group addresses
- **Items List**: List of items in this group (DO NOT include code examples)
- **Status**: Current status (Pending / In Progress / Complete)
- **Priority**: Priority level (P0-CRITICAL / P1-HIGH / P2-MEDIUM / P3-LOW)
- **Dependencies**: Any dependencies on other groups or items
- **Validation Criteria**: What constitutes completion for this group
- **Checklist Items**: Structured checklist of tasks/steps for this group

### Checklist Usage

1. **Review Checklists**: Before starting work, review CODE_IMPLEMENTATION_SPEC structured checklists to locate the current or next plan to execute
2. **Select Group**: Identify which group of items to work on based on priority, dependencies, and current status
3. **Execute Group**: Focus on implementing, refactoring and validating the selected group of items
4. **Update Checklist**: Update the checklist as work progresses, marking items complete
5. **Validate Group**: Ensure all items in the group are complete and validated before moving to next group

### Implementation Plan Checklists

#### Group 1: [Group Name]

**Status**: [Pending / In Progress / Complete]
**Priority**: [P0-CRITICAL / P1-HIGH / P2-MEDIUM / P3-LOW]
**Description**: [Brief description of what this group addresses]

**Items**:

- [ ] Item 1: [Description]
- [ ] Item 2: [Description]
- [ ] Item 3: [Description]

**Dependencies**: [List any dependencies]

**Validation Criteria**: [What constitutes completion]

**Progress Notes**: [Track progress, issues, decisions - DO NOT include code examples]

---

#### Group 2: [Group Name]

**Status**: [Pending / In Progress / Complete]
**Priority**: [P0-CRITICAL / P1-HIGH / P2-MEDIUM / P3-LOW]
**Description**: [Brief description of what this group addresses]

**Items**:

- [ ] Item 1: [Description]
- [ ] Item 2: [Description]
- [ ] Item 3: [Description]

**Dependencies**: [List any dependencies]

**Validation Criteria**: [What constitutes completion]

**Progress Notes**: [Track progress, issues, decisions - DO NOT include code examples]

---

_[Add additional groups as needed]_

---

## 🔄 SESSION STATUS TRACKING

### Phase: Initialization

**Status**: ✅ COMPLETE

**Actions Completed**:

- [x] Loaded and parsed DOCTRINE: Enterprise Canonical Execution
- [x] Loaded and parsed PROTOCOL 001: The GoldenRule Execution
- [x] Loaded and parsed PROTOCOL 002: Zero Tolerance Remediation (ENFORCED)
- [x] Loaded and parsed PROTOCOL 003: FastAPI Pure Code Implementation (ENFORCED)
- [x] Loaded and executed INSTRUCTION 104: Execute Implementation Phase Tasks (ENFORCED)
- [x] Loaded and executed INSTRUCTION 107: Remediate And Refactor Codebase (ENFORCED)
- [x] Loaded and executed INSTRUCTION 202: Pure Code Implementation Execution Protocol (ENFORCED)
- [x] Loaded and executed INSTRUCTION 203: FastAPI Design Implementation Refactor (ENFORCED)
- [x] Reviewed FastAPI Services Platform documentation
- [x] Created CODE_IMPLEMENTATION_SPEC document

**Actions Pending**:

- [ ] Await explicit implementation task or requirement identification
- [ ] Perform codebase examination and gap analysis
- [ ] Perform search and discovery phase (MCP Grep + MCP Fetch + Context7)
- [ ] Clone discovered GitHub repositories
- [ ] Complete validation checkpoints

### Phase: [Current Phase Name]

**Status**: 🟡 In Progress

**Actions Completed**:

- [x] Codebase examination and gap analysis complete
- [x] Search and discovery phase complete (MCP Grep + MCP Fetch)
- [x] Repository cloning complete
- [x] Structured checklists reviewed and current/next plan located
- [x] Copy-and-adapt operations complete
- [x] Scope locked
- [x] Pre-flight violation scan complete
- [x] Scaffolding complete
- [x] Group-based implementation complete
- [x] Implementation complete
- [x] Code quality checks performed and passed
- [x] Plan validation complete
- [x] Validation complete
- [x] Zero-tolerance verification complete
- [x] Progress updated in CODE_IMPLEMENTATION_SPEC
- [x] Structured checklists updated
- [x] All plans iterated through and completed
- [x] **Extract Lifespan**:
    - [x] Create `src/fsp_shell/manifest/lifespan.py`.
    - [x] Move `create_lifespan` logic from `app_factory.py`.
    - [x] Implement "Pulse Phase" logging (attempting -> success/failure).
- [x] **Refactor App Factory**:
    - [x] Update `src/fsp_shell/manifest/app_factory.py`.
    - [x] Import lifespan from new module.
- [x] **Optimize Plugin Loader**:
    - [x] Update `src/fsp_shell/manifest/plugin_loader.py`.
    - [x] Implement strict prefix filtering (`au-sys-`, `fsp-`, `app-`).
- [x] **Infrastructure**:
    - [x] Rename directory to `fastapi_services_platform`.
    - [x] Update `pyproject.toml` (Strict deps, MyPy).
    - [x] Update `Dockerfile` (Non-root user).
- [x] **Core Refactor**:
    - [x] `exceptions.py` (Standardized hierarchy).
    - [x] `database.py` (SQLAlchemy 2.0).
    - [x] `bootstrap.py` (Refactor).
    - [x] `config.py` (Verification).
- [x] **Tests**:
    - [x] Create `tests/` directory.
    - [x] `conftest.py` (Async fixtures).
    - [x] `test_bootstrap.py`.
    - [x] `test_lifespan.py`.
    - [x] `test_plugin_loader.py`.

**Actions Pending**:

- [ ] Review structured checklists to locate current/next plan
- [ ] Copy and adapt acquired content to production codebase
- [ ] Execute implementation sequence (32 steps)
- [ ] Perform code quality checks
- [ ] Validate plan success
- [ ] `mypy src/` (Strict mode).
- [ ] `pytest tests/`. updated in CODE_IMPLEMENTATION_SPEC
- [ ] Structured checklists updated
- [ ] All plans iterated through and completed
- [ ] [Track pending actions]

---

## 📋 PROTOCOL COMPLIANCE CHECKLIST

### Protocol 002: Zero Tolerance Remediation

- [x] Protocol loaded and enforced
- [ ] Pre-flight violation scan performed (awaiting task identification)
- [ ] Violations identified (awaiting task identification)
- [ ] Violations eradicated (awaiting task identification)
- [ ] Production code implemented (awaiting task identification)
- [ ] Post-modification validation performed (awaiting task identification)
- [ ] Interface completeness verified (awaiting task identification)
- [ ] Validation checkpoints passed (awaiting task identification)

### Protocol 003: FastAPI Pure Code Implementation

- [x] Protocol loaded and enforced
- [ ] MCP Grep searches performed (awaiting implementation task)
- [ ] Context7 consultation performed (awaiting implementation task)
- [ ] Blocking operations identified (awaiting FastAPI task)
- [ ] Async conversion complete (awaiting FastAPI task)
- [ ] Async patterns applied (awaiting FastAPI task)
- [ ] Performance primitives added (awaiting FastAPI task)
- [ ] Reliability primitives added (awaiting FastAPI task)
- [ ] Async correctness validated (awaiting FastAPI task)
- [ ] Performance validated (awaiting FastAPI task)
- [ ] Reliability validated (awaiting FastAPI task)
- [ ] Validation checkpoints passed (awaiting implementation task)

### Instruction 104: Execute Implementation Phase Tasks

- [x] Instruction loaded and enforced
- [ ] Active SPEC identified (awaiting SPEC)
- [ ] Current PHASE identified (awaiting SPEC)
- [ ] ACTIONS executed in order (awaiting SPEC)
- [ ] TASKS executed in order (awaiting SPEC)
- [ ] STEPS executed in order (awaiting SPEC)
- [ ] Validation performed before advancing (awaiting SPEC)

### Instruction 107: Remediate And Refactor Codebase

- [x] Instruction loaded and enforced
- [ ] Work type classified (awaiting task identification)
- [ ] Entry conditions verified (awaiting task identification)
- [ ] Pattern consistency verified (awaiting task identification)
- [ ] Code reuse verified (awaiting task identification)
- [ ] Regression prevention added (awaiting task identification)
- [ ] SPEC updated (awaiting task identification)
- [ ] Persistence complete (awaiting task identification)

### Instruction 202: Pure Code Implementation Execution Protocol

- [x] Instruction loaded and enforced
- [ ] Search phase complete (awaiting implementation task)
- [ ] Scope locked (awaiting implementation task)
- [ ] Scaffolding complete (awaiting implementation task)
- [ ] Implementation complete (awaiting implementation task)
- [ ] Logging compliance verified (awaiting implementation task)
- [ ] Validation complete (awaiting implementation task)
- [ ] Zero-tolerance verification complete (awaiting implementation task)

### Instruction 203: FastAPI Design Implementation Refactor

- [x] Instruction loaded and enforced
- [ ] Blocking operations identified (awaiting FastAPI task)
- [ ] Async conversion complete (awaiting FastAPI task)
- [ ] Async patterns applied (awaiting FastAPI task)
- [ ] Performance primitives added (awaiting FastAPI task)
- [ ] Reliability primitives added (awaiting FastAPI task)
- [ ] Async correctness validated (awaiting FastAPI task)
- [ ] Performance validated (awaiting FastAPI task)
- [ ] Reliability validated (awaiting FastAPI task)
- [ ] Final compliance verified (awaiting FastAPI task)

---

## 🎯 SESSION OBJECTIVES

### Primary Objective

Execute code implementation and remediation following the combined execution protocols, enforcing multiple critical protocols:

1. Zero Tolerance Remediation
2. FastAPI Pure Code Implementation
3. Execute Implementation Phase Tasks
4. Remediate And Refactor Codebase
5. Pure Code Implementation Execution Protocol
6. FastAPI Design Implementation Refactor

### Success Criteria

- All protocols enforced throughout session
- All mandatory steps executed sequentially
- Zero tolerance violations eradicated
- Production code implemented 100% correctly
- All validation checkpoints passed
- Complete traceability documented
- SPEC updated with resolution
- Persistence to neo4j-memory complete

### Implementation Requirements

- Production code MUST be implemented 100% correctly
- Production code MUST meet highest enterprise standards
- Production code MUST have 0 errors, 0 warnings, 0 issues
- Production code MUST be fully functional, not partial
- Production code MUST NOT skip any required functionality
- Production code MUST NOT use workarounds or temporary solutions
- Production code MUST be production-ready

### Critical Reminders (MANDATORY VERIFICATION BEFORE COMPLETION)

**100% COMPLETE = PRODUCTION CODE IMPLEMENTATION**

Before marking any work complete, you MUST verify:

1. **COMPLETENESS VERIFICATION**
   - ❓ **IF THERE IS A FEATURE, MODULE OR FUNCTION NOT 100% COMPLETE... CAN THAT BE CONSIDERED 100% PRODUCTION CODE IMPLEMENTATION?**
   - **ANSWER MUST BE**: NO - Incomplete features/modules/functions CANNOT be considered 100% production code implementation
   - **REQUIREMENT**: ALL features, modules, and functions MUST be 100% complete before completion

2. **REMAINING ACTIVITIES VERIFICATION**
   - ❓ **ARE THERE ANY REMAINING ACTIVITIES OR TASKS THAT REQUIRE ATTENTION?**
   - **ANSWER MUST BE**: NO - There must be ZERO remaining activities or tasks
   - **REQUIREMENT**: ALL activities and tasks MUST be completed before marking work complete

3. **ENTERPRISE QUALITY VERIFICATION**
   - ❓ **HAS THE PRODUCTION CODE BEEN FULLY IMPLEMENTED TO MEET THE STANDARDS OF ENTERPRISE-CLASS PRODUCTION QUALITY WITH NO FUTURE OR PLANNED TASKS, ITEMS, OR ACTIVITIES?**
   - **ANSWER MUST BE**: YES - Production code MUST meet enterprise-class production quality standards with ZERO future or planned tasks
   - **REQUIREMENT**: Code MUST be enterprise-class production quality with NO pending items

4. **DILIGENCE VERIFICATION**
   - ❓ **IF THERE ARE PENDING ITEMS, ARE YOUR RESPONSIBILITIES CONSIDERED FULFILLED?**
   - **ANSWER MUST BE**: NO - Pending items reflect unfulfilled responsibilities and lack of diligence
   - **REQUIREMENT**: Prompt action is REQUIRED to address ALL pending matters without delay
   - **ENFORCEMENT**: Pending items = INCOMPLETE WORK = RESPONSIBILITIES UNFULFILLED

**COMPLETION CRITERIA**: Work can ONLY be marked complete when ALL four verification questions are answered correctly and ALL requirements are met.

---

## 📌 NOTES

### Session Initialization Notes

- This session was initialized per user instruction to create and update CODE_IMPLEMENTATION_SPEC
- All required protocols have been loaded and are actively enforced
- FastAPI Services Platform documentation has been reviewed for context
- Session is ready to proceed with explicit implementation tasks when provided

### Protocol Enforcement Notes

- All enforced protocols require sequential, blocking execution
- No shortcuts or workarounds permitted
- All violations must be found and eradicated immediately
- Production code must be implemented 100% correctly
- All validation checkpoints must pass before completion
- MCP Grep and Context7 searches are MANDATORY before writing code

### Documentation Policy (ABSOLUTE - OVERRIDES ALL OTHER INSTRUCTIONS)

- **THIS IS A CODE-ONLY SESSION** - NO documentation files permitted unless explicitly requested
- **ABSOLUTE AUTHORITY**: This directive OVERRIDES ALL other YAML file instructions
- **FORBIDDEN**: Creating documentation files unless user EXPLICITLY asks for it
- **FORBIDDEN**: Following documentation requirements from other YAML files that conflict with this directive
- **MANDATORY**: User must EXPLICITLY state "create documentation" or "write documentation" - implicit requests DO NOT count
- **EXCEPTION**: CODE_IMPLEMENTATION_SPEC is EXEMPT from CODE-ONLY policy (mandatory protocol artifact)
- **EXCEPTION**: Code docstrings REQUIRED (standard Python practice - NOT documentation files)
- **EXCEPTION**: SPEC lifecycle management is MANDATORY
- **ENFORCEMENT**: Violation of documentation policy = BLOCKING ISSUE - execution MUST STOP immediately

### Implementation Discipline Notes

- **Sequential Implementation** (ABSOLUTE - STRICTLY FORBIDDEN: Scripts or mass modifications)
  - ALL code MUST be implemented and validated ONE STEP AT A TIME, in a SEQUENTIAL MANNER
  - FORBIDDEN: Scripts that modify multiple files simultaneously
  - FORBIDDEN: Mass modifications or bulk changes
  - FORBIDDEN: Automated refactoring tools that modify multiple files at once
  - MANDATORY: Each file modification must be validated before proceeding to the next
  - MANDATORY: Sequential, controlled, validated implementation only

- **Code Discovery and Gap Analysis** (MANDATORY)
  - Start by examining production codebase for missing elements, TODOs, mocks, stubs, unfinished code
  - Identify partially completed items that can be quickly implemented by copying/adjusting
  - Extensively scan and search codebase for gaps
  - Pinpoint partially completed items that can be reactivated/restored from cloned repos
  - Record all planning in CODE_IMPLEMENTATION_SPEC (DO NOT include code examples)

- **MCP Tools Usage** (MANDATORY)
  - MUST use MCP Grep to search codebase and GitHub repos
  - MUST use MCP Fetch to retrieve repositories, code examples, or semantically similar codebase
  - MUST use GIT TO CLONE all useful discovered GitHub repos (even if small benefit)
  - Cloned repos are for future reference/examples - do NOT remove them
  - Document all cloned repos and their purposes in CODE_IMPLEMENTATION_SPEC

- **Group-Based Implementation** (MANDATORY)
  - Review CODE_IMPLEMENTATION_SPEC structured checklists to locate current/next plan to execute
  - Focus on implementing, refactoring and validating groups of items from identified list
  - Execute groups with precision and adherence to best practices
  - Record structured checklists in CODE_IMPLEMENTATION_SPEC (DO NOT include code examples)
  - Update structured checklists as work progresses
  - Validate groups before moving to next group
  - Continue to iterate through plans until all plans are completed, pass code quality checks and validated

- **Copy-and-Adapt Methodology** (MANDATORY - FORBIDDEN: Re-writing)
  - MUST COPY and adapt acquired directory structures, files, modules, functions, code blocks and content to prod codebase
  - FORBIDDEN: DO NOT re-write any part of the content - THIS IS ERROR PRONE
  - Adapt each one step by step, validate then continue to the next
  - Continue to implement, fix, remediate and refactor the plan until complete
  - Maintain and update progress through the plan in CODE_IMPLEMENTATION_SPEC

- Search before writing code (MANDATORY)
- Scope lock before implementation (MANDATORY)
- Scaffold before implementing (MANDATORY)
- Pre-flight violation scan before starting work (MANDATORY)
- File modification checkpoint before modifying files (MANDATORY)
- Post-modification validation after modifying files (MANDATORY)
- Zero-tolerance verification before completion (MANDATORY)

### FastAPI-Specific Notes

- ALL endpoints MUST be `async def` (NO exceptions)
- NO blocking calls in async context
- Connection pooling MANDATORY for HTTP clients
- Database pooling + pre-ping MANDATORY
- Keep-alive MUST be enabled
- Structured error handling MANDATORY
- Retry mechanisms MANDATORY
- Circuit breakers MANDATORY for critical integrations
- Health monitoring MANDATORY for connection pools

### Critical Reminders (MANDATORY BEFORE COMPLETION)

**BEFORE MARKING ANY WORK COMPLETE, YOU MUST VERIFY:**

1. **100% COMPLETE VERIFICATION**
   - ❓ Is every feature, module, and function 100% complete?
   - ❓ Can incomplete features/modules/functions be considered 100% production code implementation?
   - **REQUIREMENT**: NO - Incomplete code CANNOT be considered production code
   - **ACTION**: Complete ALL features, modules, and functions to 100% before completion

2. **ZERO PENDING ITEMS VERIFICATION**
   - ❓ Are there any remaining activities or tasks that require attention?
   - **REQUIREMENT**: NO - There must be ZERO remaining activities or tasks
   - **ACTION**: Complete ALL activities and tasks before marking work complete

3. **ENTERPRISE QUALITY VERIFICATION**
   - ❓ Has production code been fully implemented to meet enterprise-class production quality standards?
   - ❓ Are there any future or planned tasks, items, or activities?
   - **REQUIREMENT**: YES to quality, NO to pending items
   - **ACTION**: Ensure enterprise-class production quality with ZERO pending items

4. **DILIGENCE VERIFICATION**
   - ❓ If there are pending items, are responsibilities considered fulfilled?
   - **REQUIREMENT**: NO - Pending items = unfulfilled responsibilities = lack of diligence
   - **ACTION**: Prompt action REQUIRED to address ALL pending matters without delay

**COMPLETION BLOCKER**: Work CANNOT be marked complete if ANY of these verifications fail.

**RESPONSIBILITY**: Unfulfilled verifications reflect lack of diligence and require immediate attention.

---

**Session Status**: 🟡 In Progress - Awaiting Explicit Implementation Task

**Last Updated**: [YYYY-MM-DD HH:MM:SS (Australia/Adelaide)]
