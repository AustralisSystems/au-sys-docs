# Session Initialization - Protocol Enforcement Code Implementation Specification

**Version**: v1.0.0
**Date**: 2026-01-23
**Last Updated**: 2026-01-24 17:30:00 (Australia/Adelaide)
**Status**: � Analysis Complete - Ready for Implementation
**Priority**: P0 - CRITICAL
**Session Type**: Code Implementation and Remediation Session
**Instruction Files**:

- `docs/implementation/instructions/v2/002-PROTOCOL-Zero_Tolerance_Remediation-v2.0.0.yaml`
- `docs/implementation/instructions/v2/003-PROTOCOL-FastAPI_Pure_Code_Implementation-v2.0.0.yaml`
- `docs/implementation/instructions/v2/004-PROTOCOL-Validate_Remediate_Codebase-v2.0.0.yaml`
- `docs/implementation/instructions/v2/104-INSTRUCTIONS-Execute_Implementation_Phase_Tasks-v2.0.0.yaml`
- `docs/implementation/instructions/v2/107-INSTRUCTIONS-Remediate_And_Refactor_Codebase-v2.0.0.yaml`
- `docs/implementation/instructions/v2/202-INSTRUCTIONS-Pure_Code_Implementation_Execution_Protocol-v2.0.0.yaml`
- `docs/implementation/instructions/v2/203-INSTRUCTIONS-FastAPI_Design_Implementation_Refactor-v2.0.0.yaml`

---

## 📊 SESSION SUMMARY

### Session Objective

This session focuses on the **continued development and implementation of the UFC Capability Factory**, building upon the retrospective findings and baseline established in the previous session (`CODE_IMPLEMENTATION_SPEC_2026-01-22_UFC_RETROSPECTIVE_AND_FASTAPI_REMEDIATION_SESSION_20260122_2042.md`).

**Strategic Goal**: Harden the capability factory tooling, specifically addressing brownfield remediation risks (Smart Merge support) and standardizing the container-aware validation pipeline.

### Core Philosophy: "Manufacturing Fidelity & High-Accuracy Automation"
- **Manufacturing Fidelity**: Ensuring synchronization between factory blueprints and global library templates.
- **Smart Remediation**: Moving from "dumb sync" (overwrite) to "smart merge" for brownfield targets.
- **Identity of Construction**: Maintaining zero-variance between local development and containerized artifacts.

### Related Documentation & Context
- **Previous Session SPEC**: [SPEC_2026-01-22_SESSION_2042](file:///c:/github_development/AustralisSystems/docs\implementation\in_progress\CODE_IMPLEMENTATION_SPEC_2026-01-22_UFC_RETROSPECTIVE_AND_FASTAPI_REMEDIATION_SESSION_20260122_2042.md)
- **Handover Doc**: [Handover_20260123](file:///c:/github_development/AustralisSystems/docs\implementation\handovers\20260123_123500_session_docs.md)
- **Process Guide**: [PROCESS_GUIDE](file:///c:/github_development/AustralisSystems/tooling\au-sys-tools\ufc_capability_factory\UFC_CAPABILITY_FACTORY_PROCESS_GUIDE.md)
- **Master Runbook**: [MASTER_RUNBOOK](file:///c:/github_development/AustralisSystems/tooling\au-sys-tools\ufc_capability_factory\runbooks\MASTER_RUNBOOK.md)

---

## 🏗️ IMPLEMENTATION PLAN (PHASE 2 CONTINUED)

### PHASE 6: Tooling Hardening & Brownfield Remediation Support
- [ ] **ACTION 6.1: Upgrade `scaffold_target.py` for Smart Merging**
  - [ ] TASK 6.1.1: Implement TOML merging logic to preserve existing `pyproject.toml` dependencies.
  - [ ] TASK 6.1.2: Add manifestation protection (avoid overwriting `plugin.py`, `container.py` if present).
  - [ ] TASK 6.1.3: Verify "Smart Merge" behavior on a dummy test repository.
- [ ] **ACTION 6.2: Execute Remediation on `au_sys_unified_storage`**
  - [ ] TASK 6.2.1: Run upgraded `scaffold_target.py` on the storage capability.
  - [ ] TASK 6.2.2: Verify `validation/` suite is injected without breaking existing persistence drivers.
  - [ ] TASK 6.2.3: Run the standardized `validation.runner` on `au_sys_unified_storage`.

### PHASE 7: Template Synchronization & Compliance
- [ ] **ACTION 7.1: Global Blueprint Alignment**
  - [ ] TASK 7.1.1: Sync `au_sys_ufc_app_template` with the latest OVS infrastructure.
  - [ ] TASK 7.1.2: Ensure `ufc_blueprint_template` contains the latest `path_resolver.py` logic.

---

## 🛡️ PROTOCOL ENFORCEMENT

- **Doctrine**: `000-DOCTRINE-Enterprise_Canonical_Execution-v2.0.1.yaml` ✅ Loaded
- **Protocol 1**: `001-PROTOCOL-The_GoldenRule_Execution-v2.0.1.yaml` ✅ Loaded
- **Protocol 2**: `002-PROTOCOL-Zero_Tolerance_Remediation-v2.0.0.yaml` ✅ Loaded and **ENFORCED**
- **Protocol 3**: `003-PROTOCOL-FastAPI_Pure_Code_Implementation-v2.0.0.yaml` ✅ Loaded and **ENFORCED**
- **Protocol 6**: `006-PROTOCOL-RFC2119_Requirements_Language-v1.0.0.yaml` ✅ Loaded and **ENFORCED**

---

## 🤖 CAPABILITY ANALYSIS: AI AGENT TOOLS
**Path**: `tooling/au-sys-tools/ufc_capability_factory/blueprint/library_ai_agent/tools`

This subsystem provides the automation engine for harvesting legacy repositories and transforming them into standardized UFC services using AST-based analysis and Tri-Layer mapping.

### Tool Catalog & Purpose

| Script | Purpose | Key Features |
| :--- | :--- | :--- |
| `extract_code.py` | **Harvesting** | Extracts target code from repositories, filtering for production logic. |
| `analyze_repo_structure.py`| **Forensics** | Maps source repo layouts to identify package patterns and tech stacks. |
| `adapt_extracted_code.py` | **Refactoring** | **AST-Powered**: Classifies code into models, services, routers, and CLI. |
| `standstandardize_service.py`| **Canonization** | Wraps adapted code into the Tri-Layer (Core/Interface/Manifest) pattern. |
| `scaffold_capability.py` | **Automation** | Top-level orchestrator for generating new capabilities from blueprints. |
| `capability_generator.py` | **Synthesis** | Generates boilerplate for new features within an existing capability. |
| `discover_capabilities.py` | **Inventory** | Scans the monorepo to identify and catalog active capabilities. |
| `build_services.py` | **Lifecycle** | Handles local build and wheel generation for remediated services. |
| `verify_capability.py` | **Compliance** | Runs integrity checks to ensure Tri-Layer adherence and import safety. |
| `prepare_onboarding.py` | **Ops** | Sets up the environment for new service contribution. |

### Technical Capabilities
- **AST Classification**: Tools like `adapt_extracted_code.py` use Python's `ast` module to detect `FastAPI` routers, `Pydantic` models, and `Typer` CLIs without running the code.
- **Tri-Layer Mapping**: Automated migration from flat or irregular structures into `core/`, `interface/`, and `manifest/` directories.
- **Idempotent Scaffolding**: Ensuring re-runs do not destroy manual customizations (aligned with Phase 6 hardening).

### End-to-End Transformation Lifecycle (E2E)

The following sequence defines the complete conversion of legacy code into the UFC architecture. Each step is governed by the Software Factory's automated tooling to ensure "Identity of Construction" and protocol adherence.

| Order | Lifecycle Stage | Primary Task | Automated Script |
| :--- | :--- | :--- | :--- |
| **1** | **Forensics** | Extract legacy logic and analyze source repo patterns. | `extract_code.py`, `analyze_repo_structure.py` |
| **2** | **Scaffolding** | Initialize the sanitized UFC Tri-Layer directory structure. | `scaffold_capability.py` |
| **3** | **Adaptation** | Auto-map code into `core/`, `interface/`, and `manifest/` groups. | `adapt_extracted_code.py` |
| **4** | **Standardize** | Finalize metadata, apply doc templates, and fix common linting issues. | `standardize_service.py` |
| **5** | **Build** | Execute the standard build pipeline (RUFF/MYPY/Wheels). | `build_services.py` |
| **6** | **Deployment** | Prepare for monorepo onboarding and move artifacts to production paths. | `prepare_onboarding.py` |
| **7** | **Validation** | Perform 100% compliance check against UFC integrity blueprints. | `verify_capability.py` |
| **8** | **Finalize** | Tag version, create handover, and register in discovery. | `discover_capabilities.py` |

---

## 🛠️ PRODUCTION TOOLING: UFC CAPABILITY FACTORY
**Path**: `tooling/au-sys-tools/ufc_capability_factory/`

This directory contains the core sequence of production-grade scripts used for the industrialization of "Brownfield" code into the Sovereign UFC Architecture.

### Tool Catalog & Purpose (Production Sequence)

| Order | Script | Purpose | Key Features |
| :--- | :--- | :--- | :--- |
| **001** | `001_path_resolver.py` | **Workspace Recovery** | Standardizes path discovery across monorepo/container boundaries. |
| **002** | `002_ufc_compliance_audit.py` | **Gap Analysis** | Audits target against the 6 mandatory UFC components. |
| **003** | `003_legacy_code_inventory.py` | **Forensics** | Deep AST analysis of legacy code (complexity, dependencies). |
| **004** | `004_generate_migration_map.py` | **Planning** | Generates a source-to-UFC-layer migration matrix. |
| **005** | `005_scaffold_ufc_structure.py` | **Sanitization** | Initializes the Tri-Layer directory structure. |
| **006** | `006_validate_ufc_structure.py` | **Verification** | Ensures scaffolded structure meets structural integrity standards. |
| **007** | `007_backup_legacy_code.py` | **Safety** | Creates an immutable backup of source before destructive operations. |
| **008** | `008_migrate_and_rewrite.py` | **Migration** | The "Meat": Moves files into layers and rewrites internal imports. |
| **009** | `009_validate_imports.py` | **Remediation** | Identifies and auto-fixes broken internal module references. |
| **010** | `010_generate_plugin_interface.py` | **Manifesting** | Generates the mandatory `plugin.py` for dynamic loading. |
| **011** | `011_generate_di_container.py` | **Manifesting** | Generates the `container.py` (Dependency Injection) manifest. |
| **012** | `012_generate_config_schema.py` | **Manifesting** | Generates the `config.py` Pydantic schema for validation. |
| **013** | `013_configure_entry_points.py` | **Interface** | Sets up FastAPI/Typer entry points in the `interface/` layer. |
| **014** | `014_generate_service_manifest.py` | **BOM Generation** | Finalizes the `bom.json` and `SERVICE_MANIFEST.yaml`. |
| **015** | `015_build_capability.py` | **Packaging** | Executes Poetry-based build and wheel generation (`.whl`). |
| **016** | `016_run_unit_tests.py` | **Quality** | Executes the Pytest suite in the industrialized environment. |
| **017** | `017_zero_tolerance_check.py` | **Compliance** | Final Zero-Tolerance gate before mono-repo inclusion. |
| **018** | `018_integrate_plugin.py` | **Orchestration** | Auto-registers the plugin with the Central Coordination Service. |
| **019** | `019_auto_remediate.py` | **Self-Healing** | Fixes minor protocol violations automatically. |
| **020** | `020_remediate_core_violations.py`| **Self-Healing** | Addresses complex, multi-module architectural violations. |

### End-to-End Transformation Lifecycle (Production Flow)

This sequence defines the correct order of operations for a professional legacy-to-UFC conversion.

| Phase | Order | Task | Script | Called Modules / Engines | Output / Artifact |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Phase 0** | 1 | Define Paths | `001_path_resolver.py` | (Self-Contained) | `UFCPaths` state |
| | 2 | Discovery Audit | `002_ufc_compliance_audit.py` | `path_resolver.py` | `AUDIT_REPORT.md` |
| | 3 | Inventory Code | `003_legacy_code_inventory.py` | `path_resolver.py`, `ast` | `CODE_INVENTORY.json` |
| | 4 | Map Migration | `004_generate_migration_map.py` | `path_resolver.py` | `MIGRATION_MAP.yaml` |
| **Phase 1** | 5 | Scaffold | `005_scaffold_ufc_structure.py` | `scaffold_target.py`, `pyproject_merger.py` | UFC Dir Structure |
| | 6 | Verify Scaffold | `006_validate_ufc_structure.py` | `ufc_verify_ast.py`, `path_resolver.py` | Readiness Signal |
| | 7 | Backup Source | `007_backup_legacy_code.py` | `path_resolver.py`, `shutil` | Archive (.zip/tar) |
| **Phase 2** | 8 | Migrate | `008_migrate_and_rewrite.py` | `ufc_sync_from_blueprint.py`, `path_resolver.py` | Code in Layers |
| | 9 | Fix Imports | `009_validate_imports.py` | `path_resolver.py`, `ast` | Clean Import Tree |
| **Phase 3** | 10 | Gen Plugin | `010_generate_plugin_interface.py` | `capability_generator.py`, `path_resolver.py` | `plugin.py` |
| | 11 | Gen Container | `011_generate_di_container.py` | `capability_generator.py`, `path_resolver.py` | `container.py` |
| | 12 | Gen Config | `012_generate_config_schema.py` | `capability_generator.py`, `path_resolver.py` | `config.py` |
| | 13 | Entry Points | `013_configure_entry_points.py` | `capability_generator.py`, `path_resolver.py` | `main.py` / `cli.py` |
| | 14 | Manifest | `014_generate_service_manifest.py` | `path_resolver.py` | `bom.json` |
| **Phase 4** | 15 | Build | `015_build_capability.py` | `ufc_build_pipeline.py`, `path_resolver.py` | `.whl` Artifact |
| | 16 | Test | `016_run_unit_tests.py` | `pytest`, `path_resolver.py` | `TEST_REPORT.xml` |
| | 17 | Final Check | `017_zero_tolerance_check.py` | `ufc_verify_ast.py`, `path_resolver.py` | Compliance Cert |
| **Phase 5** | 18 | Integrate | `018_integrate_plugin.py` | `path_resolver.py` | Active Service |
| | 19-20 | Remediate | `019_auto_remediate.py` / `020_...` | `path_resolver.py`, `009_validate_imports.py` | Clean Baseline |

*Note: Utilities such as `scaffold_target.py` and `pyproject_merger.py` (Smart Merge) are used in Phase 1 to ensure existing project dependencies are preserved during structural injection.*

---

## ⚙️ SUPPORTING INFRASTRUCTURE & ENGINE MODULES
**Location**: `tooling/au-sys-tools/ufc_capability_factory/`

Beyond the primary production sequence, the factory relies on a suite of infrastructure modules and internal engine components to handle path resolution, sync logic, and build orchestration.

### Root Infrastructure Utilities

| Module | Role | Description |
| :--- | :--- | :--- |
| `path_resolver.py` | **Omniscience** | Critical base class for resolving monorepo paths across all dev environments. |
| `smart_sync.py` | **Mirroring** | Hash-based (MD5) directory synchronization tool used for template updates. |
| `pyproject_merger.py`| **Merging** | (New) Smart dependency merger to prevent overwriting custom brownfield deps. |
| `scaffold_target.py` | **Scaffolding** | The foundational project generator that combines blueprint templates. |

### Internal Lifecycle Engine (Blueprint/Dev)
**Path**: `blueprint/dev/`

These modules provide the low-level "Engine" logic that supports the high-level `001-020` scripts.

| Module | Purpose | Key Feature |
| :--- | :--- | :--- |
| `ufc_build_pipeline.py` | **Packaging** | Standardized build pipeline (Linting -> Type Check -> Build). |
| `ufc_sync_from_blueprint.py`| **Synchronization**| Core transform logic for renaming placeholders in templates. |
| `ufc_verify_ast.py` | **Validation** | Performs static code analysis to ensure architecture compliance. |
| `ufc_check_capability_alignment.py`| **Audit** | Audits internal service alignment with UFC library standards. |
| `piprap.py` | **Registry** | Generates a PEP 503 compliant local index for built wheels. |
| `version_manager.py` | **Versioning** | Automates version bumping and semantic version enforcement. |
| `ufc_deploy_wheels.py` | **Distribution** | Pushes built artifacts to target environments or local registries. |

---

## ⚖️ TOOL FUNCTIONality COMPARISON (Direct Mapping)

This table provides a high-level mapping between the **Production Software Factory Tools** and the **Blueprint/AI Agent Tools** to identify functional parity and overlap.

| Production Category | Production Tool (`ufc_capability_factory/`) | Comparable AI Agent Tool (`library_ai_agent/tools/`) |
| :--- | :--- | :--- |
| **Foundation** | `001_path_resolver.py` / `path_resolver.py` | `path_resolver.py` |
| **Audit** | `002_ufc_compliance_audit.py` | `verify_capability.py` |
| **Forensics** | `003_legacy_code_inventory.py` | `analyze_repo_structure.py` |
| **Planning** | `004_generate_migration_map.py` | `adapt_extracted_code.py` (Mapping) |
| **Scaffolding** | `005_scaffold_ufc_structure.py` / `scaffold_target.py` | `scaffold_capability.py` |
| **Sanity Check** | `006_validate_ufc_structure.py` | `verify_capability.py` |
| **Safety** | `007_backup_legacy_code.py` | `prepare_onboarding.py` (Backup sub-routine) |
| **Migration** | `008_migrate_and_rewrite.py` | `adapt_extracted_code.py` / `standardize_service.py` |
| **Remediation** | `009_validate_imports.py` | `standardize_service.py` (Import logic) |
| **Manifesting** | `010` - `014` (Plugin/Container/Config) | `capability_generator.py` |
| **Building** | `015_build_capability.py` | `build_services.py` |
| **Testing** | `016_run_unit_tests.py` | `build_services.py` (Test stage) |
| **Compliance** | `017_zero_tolerance_check.py` | `verify_capability.py` |
| **Integration** | `018_integrate_plugin.py` | (Implicit in Scaffolding/Ops) |
| **Self-Healing** | `019_auto_remediate.py` / `020_...` | `standardize_service.py` (Cleanup logic) |
| **Syncing** | `smart_sync.py` / `pyproject_merger.py` | (Implicit Library Logic) |
| **Operations** | `prepare_onboarding.py` | `prepare_onboarding.py` |
| **Inventory** | `discover_capabilities.py` | `discover_capabilities.py` |

---

## 🧭 DEEP DIVE: CLASSIFICATION & MAPPING LOGIC
**Analysis**: The library scripts (`adapt_extracted_code.py`) demonstrate significantly more advanced heuristics for mapping legacy code to the UFC architecture than the current factory scripts.

### 1. Analysis & Classification Logic
**Superior Tool**: `library_ai_agent/tools/adapt_extracted_code.py`

The `FileClassifier` class in this script uses sophisticated AST pattern matching to identify the *intent* of a file, not just its name.

| Logic Feature | `adapt_extracted_code.py` (AI Tool) | `003_legacy_code_inventory.py` (Factory Tool) |
| :--- | :--- | :--- |
| **Logic Engine** | **AST Visitor (Deep Inspection)** | Basic File Extension / Name Regex |
| **Framework Detection** | Detecting specific imports (`APIRouter`, `BaseModel`) to classify as `interface` or `core`. | Generic dependency listing only. |
| **Tri-Layer Mapping** | **Context-Aware**: Maps `*models.py` -> `core/models`, `*router.py` -> `interface/api`. | **Linear**: Basic copy or manual mapping required. |
| **Import Parsing** | Resolves `from . import x` relative usage to determine module coupling. | Simple string matching. |

**Key Code Block (The "Brain"):**
```python
# From adapt_extracted_code.py
class FileClassifier:
    FRAMEWORK_PATTERNS = {
        'fastapi': ['FastAPI', 'APIRouter', 'Depends'],
        'pydantic': ['BaseModel', 'Field'],
        'sqlalchemy': ['Column', 'declarative_base'],
        'typer': ['Typer', '@app.command'],
    }

    def classify_file(self, content):
        # Uses ast.parse(content) to find matches in FRAMEWORK_PATTERNS
        # Returns: 'service', 'model', 'router', 'cli', or 'utility'
```

### 2. Execution & Scaffolding Logic
**Superior Tool**: `ufc_capability_factory/008_migrate_and_rewrite.py` (with LibCST)

While the AI tool is better at *decision making* (where things go), the Factory tool is better at *execution* (rewriting the code safely).

| Logic Feature | `migrate_and_rewrite.py` (Factory Tool) | `adapt_extracted_code.py` (AI Tool) |
| :--- | :--- | :--- |
| **Rewrite Engine** | **LibCST (Concrete Syntax Tree)** | Standard `ast` (loses comments/formatting) |
| **Safety** | Preserves comments, whitespace, and formatting during import rewrites. | Risk of stripping formatting due to AST round-trip. |
| **Refactoring** | Powerful `ImportRewriter` class to change `au_sys_old` -> `au_sys_new`. | Basic string replacement. |


### Feature 6.3: API Endpoint Reverse Engineering (Planned)

**Requirement**: Generate an `openapi.json` approximation or Endpoint Map from static code analysis (without running dependencies).

**Design**: Enhance `analyze_repo_structure.py` with an `EndpointDetector` class.

**Planned Logic:**
1.  **AST Visitor**: Write a specialized visitor to find Decorator nodes.
2.  **Pattern Matching**:
    *   **FastAPI**: Match `@app.get(...)`, `@router.post(...)`, `@*.api_route(...)`.
    *   **Flask**: Match `@app.route(...)`.
3.  **Extraction**: Parse arguments to extract:
    *   **Path**: `/users/{id}`
    *   **Method**: `GET`, `POST`, etc.
    *   **Function Name**: To link back to code location.
4.  **Reporting**: Add an `api_endpoints` section to the analysis YAML report.

### Feature 6.4: Unify Migration Logic ("Best of Breed")

**Requirement**: Create a single, industry-leading migration engine by merging the classification smarts of the AI tools with the execution safety of the Factory tools.

**Design**:
1.  **Extract Classification Logic**: Detect frameworks and map files using `library_ai_agent/tools/adapt_extracted_code.py`'s `FileClassifier`.
    *   *Refactor*: Move `FileClassifier` to `tooling/au-sys-tools/ufc_capability_factory/blueprint/dev/classification_engine.py`.
2.  **Enhance Migration Planner**: Update `004_generate_migration_map.py` to use `classification_engine.py`.
    *   *Result*: The migration map JSON will now be "Smart", correctly identifying `routers/` vs `services/` based on code content, not just names.
3.  **Execute with LibCST**: Keep `008_migrate_and_rewrite.py` as is (it reads the JSON map).
    *   *Benefit*: We get the correct *Architecture* (from AI logic) with safe *Rewriting* (from LibCST).

### Feature 6.5: Universal Data Inventory ("The Rosetta Stone")

**Requirement**: Extract all data models (Pydantic, SQLAlchemy, Dataclasses) from legacy code and convert them into a "Universal" JSON Schema inventory.

**Design**:
1.  **Enhance Analysis Tool**: Upgrade `analyze_repo_structure.py` with a `ModelExtractor` visitor.
2.  **Logic**:
    *   **Visit ClassDef**: Check bases (`BaseModel`, `Base`, `dataclass`).
    *   **Parse Fields**: Visit `AnnAssign` (Annotated Assignments) to get field names and types.
    *   **Resolve Types**: detailed mapping of `int` -> `integer`, `str` -> `string`, `List[T]` -> `array`.
3.  **Output**: Generate individual JSON files per model in an `inventory/schemas` directory.
    *   **Naming Convention**: `[package]_[module]_[ClassName].json` (e.g., `shipping_orders_Order.json`) to guarantee uniqueness.
    *   **Content**: Standard JSON Schema (Draft 2020-12).

---

## 📝 IMPLEMENTATION FINDINGS

### Initial Findings (2026-01-23)
1. **Critical Tooling Gap**: Current `scaffold_target.py` uses `shutil.copytree` or similar overwrite logic, which is high-risk for existing ("Brownfield") services.
2. **Standardization Status**: Validation runner and path resolver are ready but not yet universally active in the `au_sys_unified_storage` capability.

### New Task (2026-01-24): Digital Angels Storage & Sync Comparison Analysis
**Status**: [COMPLETE]
**Target**: `apps/digital-angels/src/services/storage` & `apps/digital-angels/src/services/sync`

**Comparative Analysis Results**:
- **Storage Intent**: The local `beanie_tinydb_adapter.py` and `tinydb_doc_ids.py` use a deterministic ID strategy (`blake2b`) that could solve concurrency issues in V2's `TinyDBProvider`.
- **Sync Intent (Universal DB Mobility)**: Digital Angels demonstrates a modular pattern (`UniversalSyncManager`) that V2 must adopt to enable "True Universal Storage" — specifically syncing and migrating between SQL (ORM) and NoSQL (ODM) stores.
- **Sync Architecture**: The current V2 monolithic sync cannot handle schema transformation (Table <-> Document). Adopting the DA "Engine" pattern is mandatory to implement the required `SchemaMapperEngine`.
- **Failover Logic**: Local `dynamic_manager.py` tracks specific failure counts per operation type, providing richer telemetry than V2's current state.

**🔍 V2 ENHANCEMENT OPPORTUNITIES (Based on Comparison)**:
- [ ] **Universal DB Sync Engine**: Refactor V2's `SyncManager` into a modular system capable of plugging in `SchemaMapperEngine` for ORM-to-ODM translation.
- [ ] **Postgres JSONB Provider**: Implement a new `PostgresJSONBProvider` to serve as a high-performance bridge between Relational and Document paradigms.
- [ ] **Deterministic Concurrency**: Port the `blake2b` doc_id logic from `digital-angels` to `au_sys_unified_storage_v2`.
- [ ] **Telemetry Enrichment**: Enhance V2's `PerformanceMonitor` and `HealthCheckOptimizer` with granular backend metrics.

## 💡 V2 ENHANCEMENT RECOMMENDATIONS (Derived from Analysis)

The analysis of `digital-angels` has identified several "Intents" that can further optimize the global `au_sys_unified_storage_v2` library:

### 1. Model-Aware "Smart" Providers
- **Source**: `beanie_tinydb_adapter.py` / `tinydb_doc_ids.py`
- **Enhancement**: Add a `ModelProvider` decorator to V2 that automates Pydantic serialization and enforces deterministic hash-based IDs (using `blake2b`) to prevent race conditions in concurrent TinyDB/SQLite writes.

### 2. General Target Synchronization
- **Source**: `differential_analysis_engine.py`
- **Enhancement**: Extend V2's `SyncAlgorithmOptimizer` to support non-storage "Sync Targets" (e.g., REST APIs, Webhooks) for mirroring configurations across varied platforms.

### 3. Step-Based Sync Workflows
- **Source**: `workflow_engine.py`
- **Enhancement**: Implement a `SyncWorkflowEngine` in V2 to handle multi-stage synchronization sequences (Pre-check -> Analyze -> Resolve -> Apply -> Verify) as first-class citizens.

### 4. Failover Logic "Reasoning" Engine
- **Source**: `dynamic_manager.py` / `factory.py`
- **Enhancement**: Formalize "Failover Recommendations" in `HealthCheckOptimizer` to provide structured JSON reasons for state transitions, improving observability during high-availability events.

---

**Session Status**: 🟡 In Progress - Session Initialized

**Last Updated**: 2026-01-24 16:30:00 (Australia/Adelaide)
