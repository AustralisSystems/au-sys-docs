# UFC Capability Factory - Process Development Specification

**Version**: v2.0.0
**Date**: 2026-01-21
**Status**: 🔵 METHODOLOGY DEFINITION
**Priority**: P0 - CRITICAL
**Purpose**: Define reusable, templated workflow for UFC capability lifecycle automation

**🎯 PRIMARY OBJECTIVE**: Create the automated process and toolkit FIRST, then apply to reference implementation

---

## 🎯 EXECUTION PLAN (EXACT ORDER OF OPERATIONS)

### TASK 1: WRITE THE END-TO-END PROCESS DOCUMENT (THIS DOCUMENT)

**PRIORITY**: P0 - MUST BE COMPLETED FIRST
**STATUS**: 🟡 IN PROGRESS
**DURATION**: 2-4 hours

#### What This Means

**CREATE** the complete step-by-step process for transforming ANY **CODE** from legacy code to UFC-compliant, Software Factory-integrated capabilities and services.

#### Deliverables

- [ ] **Section 2.3: Detailed Stage Breakdown** - Every action, every validation, every decision point for all 9 stages
- [ ] **Section 2.4: Stage-by-Stage Tasks** - Granular task checklists for each stage
- [ ] **Section 2.5: Validation Checkpoints** - What to verify at each step
- [ ] **Section 2.6: Decision Points** - Where human judgment is required
- [ ] **Section 2.7: Rollback Procedures** - What to do when things fail
- [ ] **Section 2.8: Success Criteria** - How to know each stage is complete

#### Process Documentation Requirements

For EACH of the 9 stages, document:

1. **Inputs** - What files/data are required to start this stage
2. **Actions** - Every single step to perform (manual or automated)
3. **Tools** - Which scripts/commands execute each action
4. **Validations** - How to verify each action succeeded
5. **Outputs** - What artifacts are produced
6. **Exit Criteria** - When the stage is considered complete
7. **Error Handling** - What to do if validation fails
8. **Rollback** - How to undo changes if needed

#### Example: STAGE 1 Detail Level Required

```markdown
### STAGE 1: EXTRACT (Detailed Process)

**Duration**: 30-45 minutes
**Automation Level**: 80% automated

#### 1.1 Pre-Stage Validation
- [ ] Verify Python 3.12+ installed: `python --version`
- [ ] Verify virtual environment activated: check `VIRTUAL_ENV` variable
- [ ] Verify target package exists: `ls libraries/python/services/{capability_name}`
- [ ] Verify Git working tree clean: `git status --porcelain`

#### 1.2 Step 1: UFC Compliance Audit
**Tool**: `002_ufc_compliance_audit.py`
**Input**: Target package path
**Action**:
```bash
python tooling/au-sys-tools/ufc_capability_factory/_ai_agent/tools/002_ufc_compliance_audit.py \
  --target libraries/python/services/{capability_name} \
  --output-format markdown \
  --output-file outputs/{capability_name}_compliance_audit.md
```
**Validation**:
- [ ] Audit report generated: `outputs/{capability_name}_compliance_audit.md` exists
- [ ] Report contains 6 mandatory component checks (Core, Adapters, Manifest, Scaffold, Scripts, Tests)
- [ ] Violations categorized by severity (Critical, High, Medium, Low)
- [ ] Remediation steps listed for each violation

**Exit Criteria**: Audit report complete with actionable remediation plan

**On Failure**: Check script output for errors, verify target path correct, ensure package has pyproject.toml

#### 1.3 Step 2: Legacy Code Inventory
**Tool**: `003_legacy_code_inventory.py`
**Input**: Target package source directory
**Action**:
```bash
python tooling/au-sys-tools/ufc_capability_factory/_ai_agent/tools/003_legacy_code_inventory.py \
  --target libraries/python/services/{capability_name} \
  --legacy-dir src/{capability_name} \
  --output outputs/{capability_name}_inventory.json
```
**Validation**:
- [ ] Inventory JSON generated
- [ ] Contains modules list with file paths
- [ ] Contains classes list with complexity metrics
- [ ] Contains functions list with cyclomatic complexity
- [ ] Contains imports analysis (internal vs external)
- [ ] Contains dependency graph

**Exit Criteria**: Complete code inventory in structured JSON format

#### 1.4 Step 3: Generate Migration Map
**Tool**: `004_generate_migration_map.py`
**Input**: Inventory JSON from step 1.3
**Action**:
```bash
python tooling/au-sys-tools/ufc_capability_factory/_ai_agent/tools/004_generate_migration_map.py \
  --inventory outputs/{capability_name}_inventory.json \
  --output outputs/{capability_name}_migration_map.md
```
**Validation**:
- [ ] Migration map generated
- [ ] All legacy files mapped to UFC target locations
- [ ] Complexity scores assigned to each file
- [ ] Migration priority determined (Critical, High, Medium, Low)
- [ ] Import dependencies identified

**Exit Criteria**: Complete migration strategy document

#### 1.5 Stage Exit Validation
- [ ] All 3 outputs generated (audit, inventory, migration map)
- [ ] No script execution errors
- [ ] Reports contain actionable data
- [ ] Migration complexity understood

**On Complete**: Proceed to STAGE 2
**On Failure**: Review errors, re-run failed scripts, escalate if unresolved
```

**THIS LEVEL OF DETAIL REQUIRED FOR ALL 9 STAGES**

---

### TASK 2: COPY AND SCAFFOLD SCRIPTS FROM au_sys_ufc_app

**PRIORITY**: P0 - STARTS AFTER TASK 1 COMPLETE
**STATUS**: ⚪ NOT STARTED
**DURATION**: 4-6 hours
**DEPENDENCY**: TASK 1 must be complete

#### What This Means

Take the proven automation scripts from `libraries/python/_templates/au_sys_ufc_app_template/scripts/dev/` and:

1. **Copy** them to `tooling/au-sys-tools/ufc_capability_factory/_ai_agent/tools/`
2. **Adapt** them to be parameterized (not hardcoded)
3. **Enhance** them to enforce UFC_CODEBASE_INTEGRITY_BLUEPRINT
4. **Validate** they pass all quality gates

#### Source Scripts Reference

| au_sys_ufc_app Script | New Script | Purpose |
|----------------------|------------|---------|
| `path_resolver.py` | `001_path_resolver.py` | ✅ DONE - Monorepo path resolution |
| `audit_ufc_compliance.py` | `002_ufc_compliance_audit.py` | ✅ DONE - UFC compliance checking |
| `inventory_legacy_code.py` | `003_legacy_code_inventory.py` | ✅ DONE - AST-based code analysis |
| `generate_migration_plan.py` | `004_generate_migration_map.py` | ✅ DONE - Migration planning |
| `scaffold_plugin.py` | `005_scaffold_ufc_structure.py` | ✅ DONE - Create UFC directories |
| `verify_syntax.py` | `015_verify_ast_quality.py` | ✅ DONE - Code quality validation |
| *(create new)* | `006_validate_ufc_structure.py` | ⚪ TODO - Verify directory structure |
| *(create new)* | `007_backup_legacy_source.py` | ⚪ TODO - Backup before migration |
| *(adapt from ufc_app)* | `008_migrate_and_rewrite.py` | ⚪ TODO - AST-based code migration |
| *(adapt from ufc_app)* | `009_validate_migrated_code.py` | ⚪ TODO - Post-migration validation |
| *(adapt from ufc_app)* | `010_generate_plugin_interface.py` | ⚪ TODO - Create plugin.py |
| *(adapt from ufc_app)* | `011_generate_config_schema.py` | ⚪ TODO - Generate Pydantic models |
| *(create new)* | `012_generate_config_yaml.py` | ⚪ TODO - Create config YAML |
| *(adapt from ufc_app)* | `013_add_plugin_entry_point.py` | ⚪ TODO - Update pyproject.toml |
| *(create new)* | `014_validate_plugin_interface.py` | ⚪ TODO - Test plugin loadable |
| *(adapt from ufc_app)* | `016_test_plugin_discovery.py` | ⚪ TODO - Verify discovery |
| *(adapt from ufc_app)* | `017_test_plugin_loading.py` | ⚪ TODO - Test loading |
| *(create new)* | `018_final_validation.py` | ⚪ TODO - Complete quality gates |

**Progress**: 6/18 scripts complete (33%)

#### Script Requirements (ALL SCRIPTS MUST COMPLY)

**Parameterization**:
```python
parser = argparse.ArgumentParser()
parser.add_argument("--target", required=True, help="Target capability path")
parser.add_argument("--output", help="Output file path")
# NO hardcoded paths to au_sys_unified_storage
```

**Quality Gates** (EVERY SCRIPT):
```bash
mypy --strict {script}.py  # MUST pass with 0 errors
ruff check {script}.py     # MUST pass with 0 errors
bandit -r {script}.py      # MUST pass with 0 High/Medium/Critical
black --check {script}.py  # MUST be formatted
isort --check {script}.py  # MUST have sorted imports
```

**Docstring Coverage** (100%):
- Module docstring explaining purpose
- Every function with Google-style docstring
- Every class with docstring
- Every public method with docstring

**Complexity Limits**:
- Max cyclomatic complexity: 15 per function
- Max function length: 75 lines
- Max file length: 1500 lines
- Max parameters: 5 per function

#### Deliverables

- [ ] 12 new/adapted scripts created (006-014, 016-018)
- [ ] All 18 scripts pass quality gates
- [ ] All scripts enforce UFC_CODEBASE_INTEGRITY_BLUEPRINT
- [ ] All scripts parameterized (accept --target argument)
- [ ] All scripts have 100% docstring coverage
- [ ] Integration tests created for each script

---

### TASK 3: CREATE AI AGENT INSTRUCTION FILES

**PRIORITY**: P0 - STARTS AFTER TASK 2 COMPLETE
**STATUS**: ⚪ NOT STARTED
**DURATION**: 2-3 hours
**DEPENDENCY**: TASK 2 must be complete (scripts exist to reference)

#### What This Means

Create 6 MCP-style YAML instruction files that guide AI agents through each stage using the automation scripts.

#### Files to Create

**Current Status**: 4/6 complete (005, 006 TODO)

1. ✅ `001-ufc-capability-audit-and-analysis.yaml` - STAGE 1 guidance
2. ✅ `002-ufc-structure-scaffolding.yaml` - STAGE 2 guidance
3. ✅ `003-legacy-code-migration.yaml` - STAGE 3 guidance
4. ✅ `004-ufc-app-plugin-integration.yaml` - STAGE 4 guidance
5. ⚪ `005-build-and-deploy.yaml` - STAGE 5 guidance (TODO)
6. ⚪ `006-test-validate-integrate.yaml` - STAGES 6-9 guidance (TODO)

#### Instruction File Schema

```yaml
---
name: "Stage Name"
version: "1.0.0"
type: "ai_agent_instruction"
category: "ufc_capability_factory"
phase: "STAGE_N"
estimated_duration: "X-Y minutes"
requires_judgment: true/false
automation_level: "fully_automated|semi_automated|manual_review"

description: |
  What this stage accomplishes

prerequisites:
  - "Prerequisite 1"
  - "Prerequisite 2"

inputs:
  - name: capability_name
    type: string
    required: true
    description: "Name of capability (e.g., au_sys_unified_storage)"
    pattern: "^au_sys_[a-z_]+$"

execution_steps:
  - step: "1"
    name: "Step name"
    type: "automated|validation|manual"
    commands:
      - "python tooling/au-sys-tools/ufc_capability_factory/_ai_agent/tools/XXX.py --target {capability_name}"
    validation:
      - "Check output file exists"
      - "Verify no errors in output"
    on_failure:
      action: "rollback|retry|escalate"
      steps:
        - "What to do if fails"

outputs:
  - name: "output_name"
    path: "outputs/{capability_name}_*.{ext}"
    description: "What this output contains"

validation_criteria:
  - "Criteria 1"
  - "Criteria 2"

rollback_procedure:
  - "How to undo changes"

references:
  - "UFC_ARCHITECTURE_BLUEPRINT_v1.0.0.md#section"
  - "UFC_CODEBASE_INTEGRITY_BLUEPRINT_v1.0.0.md"
```

---

### TASK 4: CREATE JINJA2 CODE GENERATION TEMPLATES

**PRIORITY**: P1 - STARTS AFTER TASK 2 COMPLETE
**STATUS**: ⚪ NOT STARTED
**DURATION**: 2-3 hours
**DEPENDENCY**: TASK 2 (need to know what code to generate)

#### Templates Required

Location: `tooling/au-sys-tools/ufc_capability_factory/templates/`

- [ ] `plugin_interface.py.j2` - Generate plugin.py
- [ ] `di_container.py.j2` - Generate container.py
- [ ] `config_schema.py.j2` - Generate config.py Pydantic models
- [ ] `config_defaults.yaml.j2` - Generate default config YAML
- [ ] `__init__.py.j2` - Generate package __init__ files

#### Template Requirements

All templates MUST:
- Accept variables: `capability_name`, `description`, `author`, `version`
- Generate code passing ALL UFC_CODEBASE_INTEGRITY quality gates
- Include 100% type hints
- Include Google-style docstrings
- Be Black-formatted (line-length=120)

---

### TASK 5: VALIDATE ON au_sys_unified_storage (REFERENCE IMPLEMENTATION)

**PRIORITY**: P0 - STARTS AFTER TASKS 1-4 COMPLETE
**STATUS**: ⚪ NOT STARTED
**DURATION**: 4-8 hours
**DEPENDENCY**: All toolkit components complete

#### What This Means

**Apply the complete automated process** to `au_sys_unified_storage` to:
1. Prove the methodology works
2. Identify gaps in automation
3. Refine scripts based on real-world usage
4. Document lessons learned

#### Success Criteria

- [ ] All 18 scripts execute successfully on au_sys_unified_storage
- [ ] au_sys_unified_storage achieves 100% UFC compliance
- [ ] Plugin loads in au_sys_ufc_app without errors
- [ ] All quality gates pass (MyPy, Ruff, Bandit)
- [ ] SBOM generated
- [ ] Integration tests pass

---

## Table of Contents

1. [Session Objectives](#1-session-objectives)
2. [Methodology Architecture](#2-methodology-architecture)
3. [Toolkit Development Requirements](#3-toolkit-development-requirements)
4. [Reference Implementation](#4-reference-implementation)
5. [Execution Workflow](#5-execution-workflow)
6. [Quality Assurance](#6-quality-assurance)
7. [Appendices](#7-appendices)

---

## Authoritative Standards (MANDATORY COMPLIANCE)

- **UFC_ARCHITECTURE_BLUEPRINT_v1.0.0.md** - UFC Structure Blueprint
- **UFC_CODEBASE_INTEGRITY_BLUEPRINT_v1.0.0.md** - Code Quality & Security Standards (**ENFORCED IN ALL SCRIPTS**)
- **UFC_APP_BLUEPRINT_v1.0.0.md** (v1.1.0) - UFC App Integration Standard
- **Toolkit Location**: `tooling/au-sys-tools/ufc_capability_factory/`
- **Reference Example**: `au_sys_unified_storage` (ONE example, NOT the only target)

---

## 🛡️ CODE QUALITY MANDATE (ABSOLUTE AUTHORITY)

> [!CRITICAL]
> **ALL AUTOMATION SCRIPTS AND GENERATED CODE MUST ENFORCE UFC_CODEBASE_INTEGRITY_BLUEPRINT_v1.0.0**

### The Five Quality Pillars (MANDATORY IN ALL SCRIPTS)

1. **Consistency**: Black (line-length=120), Isort
2. **Correctness**: MyPy (strict mode), Ruff, AST validation
3. **Security**: Bandit (0 High/Medium/Critical), Semgrep
4. **Simplicity**: McCabe Complexity ≤15, Functions ≤75 lines, Files ≤1500 lines, Parameters ≤5
5. **Documentation**: Google-style docstrings (100% coverage)

### Zero Tolerance Items (IMMEDIATE SCRIPT REJECTION)

- Print statements in production code
- Hardcoded secrets
- TODO/FIXME/HACK in main branch
- Mocking in production code
- Empty implementations (`pass`, `NotImplementedError`)

### Script Validation Requirements

Every automation script MUST:
- ✅ Pass `mypy --strict`
- ✅ Pass `ruff check` (0 errors)
- ✅ Pass `bandit -r` (0 High/Medium/Critical)
- ✅ Pass `black --check --line-length 120`
- ✅ Pass `isort --check-only`
- ✅ Cyclomatic complexity ≤15 per function
- ✅ 100% type hints coverage

---

## 1. SESSION OBJECTIVES

### 1.1 Primary Goal: CREATE THE AUTOMATED PROCESS

**NOT**: Execute phases for one package
**YES**: Build a reusable, templated methodology that works for ANY au_sys_* capability

**Deliverables**:

1. **Process Documentation** - Complete methodology document defining each phase
2. **Automation Scripts** - 18 Python scripts enforcing UFC_CODEBASE_INTEGRITY standards
3. **AI Agent Instructions** - 6 MCP-style YAML instruction files for guided execution
4. **Runbooks** - Step-by-step execution guides with examples
5. **Templates** - Jinja2 code generation templates for UFC-compliant code
6. **Validation Framework** - Automated compliance checking against all blueprints
7. **Reference Implementation** - Apply to `au_sys_unified_storage` to prove methodology

### 1.2 Secondary Goal: Template Generalization

The process MUST be:

- **Parameterized** - Works for any `{capability_name}`, not hardcoded to one package
- **Reusable** - Apply to hundreds of capabilities without modification
- **Self-Validating** - Scripts automatically check compliance against blueprints
- **Zero-Manual** - Human intervention only for strategic decisions, not edits

### 1.3 Success Criteria

**Process Creation**:
- [ ] Complete methodology document published
- [ ] 18/18 automation scripts complete and validated
- [ ] 6/6 AI agent instruction files created
- [ ] Master runbook with phase-by-phase guidance
- [ ] Jinja2 templates for all UFC components

**Reference Implementation**:
- [ ] `au_sys_unified_storage` 100% UFC compliant
- [ ] All scripts successfully applied without manual edits
- [ ] Plugin loads in au_sys_ufc_app
- [ ] Passes all quality gates (MyPy, Ruff, Bandit)

---

## 2. METHODOLOGY ARCHITECTURE

### 2.1 The Nine Lifecycle Stages

The UFC Capability Factory automates nine distinct stages for ANY capability:

```
STAGE 1: EXTRACT     → Inventory legacy code, analyze dependencies
STAGE 2: SCAFFOLD    → Create UFC-compliant directory structure
STAGE 3: DEVELOP     → Migrate code with AST-based transformation
STAGE 4: PACKAGE     → Generate manifest, plugin interface, DI container
STAGE 5: BUILD       → Create wheel distributions
STAGE 6: DEPLOY      → Install to local/remote environments
STAGE 7: TEST        → Run integration tests with au_sys_ufc_app
STAGE 8: VALIDATE    → Verify UFC compliance and code quality
STAGE 9: INTEGRATE   → Register with Software Factory plugin system
```

### 2.2 Process Flow

```
┌─────────────────────────────────────────────────────────────────┐
│  INPUT: Legacy Capability (any au_sys_* package)                │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  STAGE 1: EXTRACT     │  Scripts: 001, 002, 003, 004
         │  - Audit compliance   │  Duration: 30-45 min
         │  - Inventory code     │  AI Instructions: 001
         │  - Map migration      │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  STAGE 2: SCAFFOLD    │  Scripts: 005, 006
         │  - Create UFC struct  │  Duration: 15-20 min
         │  - Validate dirs      │  AI Instructions: 002
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  STAGE 3: DEVELOP     │  Scripts: 007, 008, 009
         │  - Backup legacy      │  Duration: 60-90 min
         │  - Migrate & rewrite  │  AI Instructions: 003
         │  - Validate imports   │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  STAGE 4: PACKAGE     │  Scripts: 010, 011, 012, 013, 014
         │  - Plugin interface   │  Duration: 45-60 min
         │  - DI container       │  AI Instructions: 004
         │  - Config schema      │
         │  - Entry points       │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  STAGE 5: BUILD       │  Scripts: 015
         │  - Build wheel        │  Duration: 10-15 min
         │  - SBOM generation    │  AI Instructions: 005
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  STAGES 6-9: DEPLOY   │  Scripts: 016, 017, 018
         │  TEST, VALIDATE,      │  Duration: 30-45 min
         │  INTEGRATE            │  AI Instructions: 006
         └───────────┬───────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────────┐
│  OUTPUT: UFC-Compliant Capability registered in Software       │
│  Factory, passing all quality gates, ready for production      │
└────────────────────────────────────────────────────────────────┘
```

---

## 3. TOOLKIT DEVELOPMENT REQUIREMENTS

### 3.1 Automation Scripts (18 Total)

All scripts MUST:

- Be placed in `tooling/au-sys-tools/ufc_capability_factory/_ai_agent/tools/`
- Accept `--target {capability_path}` parameter (NOT hardcoded to one package)
- Use monorepo-aware PathResolver for all path operations
- Enforce UFC_CODEBASE_INTEGRITY_BLUEPRINT_v1.0.0 standards
- Pass all quality gates: MyPy strict, Ruff, Bandit, Black, Isort
- Include comprehensive docstrings (Google style, 100% coverage)
- Have cyclomatic complexity ≤15 per function
- Support both relative and absolute paths
- Generate structured output (JSON/YAML/Markdown)

#### Script Catalog

**STAGE 1: EXTRACT (Scripts 001-004)**

- `001_path_resolver.py` - Monorepo workspace detection and path resolution
- `002_ufc_compliance_audit.py` - Audit against UFC_ARCHITECTURE_BLUEPRINT
- `003_legacy_code_inventory.py` - AST-based code analysis and cataloging
- `004_generate_migration_map.py` - Strategic migration planning with complexity scoring

**STAGE 2: SCAFFOLD (Scripts 005-006)**

- `005_scaffold_ufc_structure.py` - Create UFC directory structure from blueprint
- `006_validate_ufc_structure.py` - Verify all required directories and files exist

**STAGE 3: DEVELOP (Scripts 007-009)**

- `007_backup_legacy_source.py` - Backup legacy code before migration
- `008_migrate_and_rewrite.py` - AST-based code migration with import rewriting
- `009_validate_migrated_code.py` - Syntax, import, and quality validation

**STAGE 4: PACKAGE (Scripts 010-014)**

- `010_generate_plugin_interface.py` - Create plugin.py from template
- `011_generate_config_schema.py` - Generate Pydantic config models
- `012_generate_config_yaml.py` - Create default config YAML
- `013_add_plugin_entry_point.py` - Update pyproject.toml with entry points
- `014_validate_plugin_interface.py` - Verify plugin loadable by au_sys_ufc_app

**STAGE 5: BUILD (Script 015)**

- `015_build_package.py` - Build wheel + SBOM generation

**STAGES 6-9: DEPLOY/TEST/VALIDATE/INTEGRATE (Scripts 016-018)**

- `016_test_plugin_discovery.py` - Verify plugin discovery works
- `017_test_plugin_loading.py` - Test plugin loads without errors
- `018_final_validation.py` - Complete UFC compliance + quality gate validation

### 3.2 AI Agent Instructions (6 YAML Files)

Location: `tooling/au-sys-tools/ufc_capability_factory/_ai_agent/instructions/`

Each instruction file MUST:

- Follow MCP-style schema with name, version, type, category
- Define clear prerequisites and inputs (parameterized, not hardcoded)
- List execution steps with tool paths
- Specify validation criteria
- Include rollback procedures
- Reference UFC blueprints for compliance checking

**Instruction Files**:

1. `001-ufc-capability-audit-and-analysis.yaml` - STAGE 1 guidance
2. `002-ufc-structure-scaffolding.yaml` - STAGE 2 guidance
3. `003-legacy-code-migration.yaml` - STAGE 3 guidance
4. `004-ufc-package-manifest.yaml` - STAGE 4 guidance
5. `005-build-and-deploy.yaml` - STAGE 5 guidance
6. `006-test-validate-integrate.yaml` - STAGES 6-9 guidance

### 3.3 Code Generation Templates (Jinja2)

Location: `tooling/au-sys-tools/ufc_capability_factory/templates/`

Required templates:

- `plugin_interface.py.j2` - Plugin class template
- `di_container.py.j2` - Dependency injection container
- `config_schema.py.j2` - Pydantic configuration models
- `config_defaults.yaml.j2` - Default configuration YAML
- `__init__.py.j2` - Package initialization files

All templates MUST:

- Accept parameters: `capability_name`, `description`, `author`, `version`
- Generate code passing all UFC_CODEBASE_INTEGRITY quality gates
- Include proper type hints (100% coverage)
- Have Google-style docstrings
- Follow Black formatting (line-length=120)

---

## 4. REFERENCE IMPLEMENTATION: au_sys_unified_storage

**Purpose**: Validate the automated process works end-to-end

**THIS IS ONE EXAMPLE** - Not the only target, used to prove the methodology

### 4.1 Example Application Commands

```bash
# STAGE 1: EXTRACT
python tooling/au-sys-tools/ufc_capability_factory/_ai_agent/tools/002_ufc_compliance_audit.py \
  --target libraries/python/services/au_sys_unified_storage

# STAGE 2: SCAFFOLD
python tooling/au-sys-tools/ufc_capability_factory/_ai_agent/tools/005_scaffold_ufc_structure.py \
  --target libraries/python/services/au_sys_unified_storage

# STAGE 3: DEVELOP
python tooling/au-sys-tools/ufc_capability_factory/_ai_agent/tools/008_migrate_and_rewrite.py \
  --target libraries/python/services/au_sys_unified_storage \
  --source legacy_source

# ... continue through all 9 stages
```

---

## 5. EXECUTION WORKFLOW

### Step 1: Build Toolkit Infrastructure (PRIMARY TASK)

Create the 18 scripts, 6 instruction files, templates, and runbooks

### Step 2: Validate on Reference Implementation

Apply to `au_sys_unified_storage` as proof of concept

### Step 3: Generalize and Document

Ensure process works for ANY capability, not just the example

---

## 6. QUALITY ASSURANCE

All scripts MUST pass:
- MyPy --strict (0 errors)
- Ruff (0 errors)
- Bandit (0 High/Medium/Critical)
- Black + Isort (formatted)
- Complexity ≤15
- Docstring coverage 100%

---

**END OF SPECIFICATION**
