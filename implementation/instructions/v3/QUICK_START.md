# Quick Start Guide - Instruction System v2

**Version**: v2.0.1
**Last Updated**: 2025-12-20
**Purpose**: Copy-paste templates for executing structured instruction prompts

---

## 🏗️ THREE-TIER SYSTEM OVERVIEW

The instruction system follows a **three-tier hierarchical structure**:

```
DOCTRINE (Tier 1) → PROTOCOLS (Tier 2) → INSTRUCTIONS (Tier 3)
```

### Quick Understanding

- **DOCTRINE**: Foundational rules (HOW to operate) - Only one file
- **PROTOCOLS**: Validation/compliance rules (HOW to validate) - Multiple files
- **INSTRUCTIONS**: Execution workflows (WHAT to do) - Multiple files

### Precedence Rules

1. **DOCTRINE** governs PROTOCOLS and INSTRUCTIONS
2. **PROTOCOLS** govern INSTRUCTIONS
3. **INSTRUCTIONS** execute within DOCTRINE and PROTOCOL constraints

### Execution Flow

```
1. LOAD_AND_PARSE: DOCTRINE → PROTOCOLS (load foundational rules first)
2. EXECUTE: INSTRUCTIONS (run workflows after rules are understood)
```

---

## 🎯 THREE-TIER USAGE EXAMPLES

### Example 1: Full Three-Tier Stack (Recommended)

**Use Case**: Complete workflow with all foundational rules

```yaml
LOAD_AND_PARSE:
  DOCTRINE: "000-DOCTRINE-Enterprise_Canonical_Execution"
  PROTOCOLS:
    - "001-PROTOCOL-The_GoldenRule_Execution"
    - "002-PROTOCOL-Zero_Tolerance_Remediation"
    - "006-PROTOCOL-RFC2119_Requirements_Language"

EXECUTE:
  - "106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance"
  - "107-INSTRUCTIONS-Remediate_And_Refactor_Codebase"

INPUT:
  SPECS:
    SPEC_1:
      SPEC: "docs/implementation/in_progress/YOUR_SPEC_v1.0.0.md"
      PHASES: ["ALL"]
      TASKS: ["ALL"]

REMEMBER:
  - THIS IS A CODE ONLY SESSION.
  - NO DOCUMENTATION OF ANY KIND IS PERMITTED UNLESS I EXPLICITLY ASK FOR IT
```

**What Happens**:
1. **DOCTRINE** loads → Establishes core operational principles (log-first, evidence-based, production code mandate)
2. **PROTOCOLS** load → Apply Golden Rule workflow, Zero Tolerance remediation, RFC 2119 terminology
3. **INSTRUCTIONS** execute → Run validation and remediation workflows within DOCTRINE/PROTOCOL constraints

### Example 2: DOCTRINE + PROTOCOLS Only (No Instructions)

**Use Case**: Understanding foundational rules without execution

```yaml
LOAD_AND_PARSE:
  DOCTRINE: "000-DOCTRINE-Enterprise_Canonical_Execution"
  PROTOCOLS:
    - "001-PROTOCOL-The_GoldenRule_Execution"
    - "002-PROTOCOL-Zero_Tolerance_Remediation"
    - "008-PROTOCOL-Production_Code_Quality"
    - "009-PROTOCOL-Test_Implementation"

# No EXECUTE section - just loading rules for reference
```

**What Happens**:
- DOCTRINE establishes core principles
- PROTOCOLS provide domain-specific validation rules
- System understands constraints but doesn't execute workflows

### Example 3: PROTOCOLS + INSTRUCTIONS (No DOCTRINE)

**Use Case**: Quick execution with specific protocols only

```yaml
LOAD_AND_PARSE:
  - "002-PROTOCOL-Zero_Tolerance_Remediation"
  - "008-PROTOCOL-Production_Code_Quality"

EXECUTE:
  - "202-INSTRUCTIONS-Pure_Code_Implementation_Execution_Protocol"

INPUT: |
  Requirement: Fix async issues in storage factory
  Files: src/services/storage/factory.py
  Mode: refactor
```

**What Happens**:
- PROTOCOLS load → Zero Tolerance and Production Code Quality rules apply
- INSTRUCTIONS execute → Pure Code Implementation runs with protocol constraints
- **Note**: DOCTRINE principles still apply implicitly (they're universal)

### Example 4: INSTRUCTIONS Only (Minimal)

**Use Case**: Quick single-instruction execution

```yaml
EXECUTE:
  - "203-INSTRUCTIONS-FastAPI_Design_Implementation_Refactor"

INPUT:
  FOCUS: |
    - Files, modules, codeblocks implemented in this session
    - AST-defined upstream and downstream dependencies

REMEMBER:
  - THIS IS A CODE ONLY SESSION.
```

**What Happens**:
- INSTRUCTIONS execute → FastAPI refactoring workflow runs
- **Note**: DOCTRINE and PROTOCOLS still apply (they're always active)

### Example 5: Multiple PROTOCOLS with Single INSTRUCTION

**Use Case**: Comprehensive validation with multiple protocol layers

```yaml
LOAD_AND_PARSE:
  DOCTRINE: "000-DOCTRINE-Enterprise_Canonical_Execution"
  PROTOCOLS:
    - "001-PROTOCOL-The_GoldenRule_Execution"
    - "002-PROTOCOL-Zero_Tolerance_Remediation"
    - "004-PROTOCOL-Validate_Remediate_Codebase"
    - "006-PROTOCOL-RFC2119_Requirements_Language"
    - "007-PROTOCOL-MCP_Tools_Workflow"
    - "008-PROTOCOL-Production_Code_Quality"

EXECUTE:
  - "106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance"

INPUT:
  ACTIVE_SPEC: |
    docs/implementation/in_progress/YOUR_SPEC_v1.0.0.md
    Focus areas:
    - Files implemented in this session

  VALIDATION_TOOLS: |
    python -m flake8 src/
    python -m mypy src/
    python -m bandit -r src/

  POLICY_NOTES: |
    ZERO-WARNING / STRICT MODE
```

**What Happens**:
1. **DOCTRINE** → Core principles (production code mandate, no deprecation, etc.)
2. **PROTOCOLS** → Multiple validation layers:
   - Golden Rule (7-step workflow)
   - Zero Tolerance (violation detection)
   - Validate/Remediate (codebase checks)
   - RFC 2119 (terminology enforcement)
   - MCP Tools (tool usage patterns)
   - Production Code Quality (12 metrics)
3. **INSTRUCTIONS** → Validation runs with all protocol constraints

### Example 6: Protocol-Specific Workflow

**Use Case**: Using a specific protocol's procedures

```yaml
LOAD_AND_PARSE:
  DOCTRINE: "000-DOCTRINE-Enterprise_Canonical_Execution"
  PROTOCOLS:
    - "002-PROTOCOL-Zero_Tolerance_Remediation"

EXECUTE:
  - "107-INSTRUCTIONS-Remediate_And_Refactor_Codebase"

INPUT:
  TRIGGERING_FAILURES: |
    flake8: FAILED (15 errors, 3 warnings)
    - src/services/api/routers/auth.py:15: F401 'unused_import'

    mypy: FAILED (8 type errors)
    - src/services/api/routers/auth.py:45: Argument type incompatible

  ALLOWED_REMEDIATION_SCOPE: |
    Focus areas:
    - Files implemented in this session
    - AST-defined dependencies

  VALIDATION_TO_RE_RUN: |
    python -m flake8 src/services/api/routers/auth.py
    python -m mypy src/services/api/routers/auth.py
```

**What Happens**:
- **DOCTRINE** → Production code mandate, implementation consistency
- **Zero Tolerance Protocol** → Pre-flight scans, violation detection, interface completeness checks
- **Remediation Instruction** → Executes remediation with protocol enforcement

### Example 7: Chained Instructions with Protocols

**Use Case**: Multiple instructions with protocol enforcement throughout

```yaml
LOAD_AND_PARSE:
  DOCTRINE: "000-DOCTRINE-Enterprise_Canonical_Execution"
  PROTOCOLS:
    - "001-PROTOCOL-The_GoldenRule_Execution"
    - "002-PROTOCOL-Zero_Tolerance_Remediation"
    - "008-PROTOCOL-Production_Code_Quality"

EXECUTE:
  - "106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance"
  - "107-INSTRUCTIONS-Remediate_And_Refactor_Codebase"
  - "106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance"

INPUT:
  OUTPUT_FROM:
    FROM_INSTRUCTION: "106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance-v2.0.0.yaml"
    TO_INSTRUCTION: "107-INSTRUCTIONS-Remediate_And_Refactor_Codebase-v2.0.0.yaml"
    MAP:
      FAILURES: "TRIGGERING_FAILURES"
      BLOCKERS: "BLOCKERS"
      VALIDATION_COMMANDS: "VALIDATION_TO_RE_RUN"

  ACTIVE_SPEC: |
    docs/implementation/in_progress/YOUR_SPEC_v1.0.0.md

  TRIGGERING_FAILURES: |
    # Will be populated from instruction 1 output

  ALLOWED_REMEDIATION_SCOPE: |
    Focus areas:
    - Files implemented in this session

REMEMBER:
  - THIS IS A CODE ONLY SESSION.
```

**What Happens**:
1. **DOCTRINE + PROTOCOLS** load → All foundational rules established
2. **Instruction 1** (Validate) → Runs with protocol constraints, produces output
3. **Instruction 2** (Remediate) → Receives output from Instruction 1, runs with protocol constraints
4. **Instruction 3** (Validate) → Re-validates after remediation, runs with protocol constraints

### Example 8: Domain-Specific Protocol Stack

**Use Case**: Using domain-specific protocols for specialized work

```yaml
LOAD_AND_PARSE:
  DOCTRINE: "000-DOCTRINE-Enterprise_Canonical_Execution"
  PROTOCOLS:
    - "001-PROTOCOL-The_GoldenRule_Execution"
    - "003-PROTOCOL-FastAPI_Pure_Code_Implementation"
    - "004-PROTOCOL-Validate_Remediate_Codebase"
    - "008-PROTOCOL-Production_Code_Quality"

EXECUTE:
  - "203-INSTRUCTIONS-FastAPI_Design_Implementation_Refactor"

INPUT:
  FOCUS: |
    - FastAPI routers and endpoints
    - Pydantic models and validation
    - Async/await patterns
    - OpenAPI specifications

REMEMBER:
  - THIS IS A CODE ONLY SESSION.
```

**What Happens**:
- **DOCTRINE** → Core principles
- **FastAPI Protocol** → FastAPI-specific rules (async compliance, OpenAPI-first, etc.)
- **Validate/Remediate Protocol** → Codebase validation rules
- **Production Code Quality** → 12 mandatory metrics
- **FastAPI Instruction** → Refactoring runs with all protocol constraints

---

## 🚀 BASIC TEMPLATE

### Simplified Format (Recommended)

**Base Directory**: `docs/implementation/instructions/v2/`
**File Extension**: `.yaml` (automatically added)

```yaml
LOAD_AND_PARSE:
  DOCTRINE: "000-DOCTRINE-Enterprise_Canonical_Execution"
  PROTOCOLS:
    - "001-PROTOCOL-The_GoldenRule_Execution"
    - "002-PROTOCOL-Zero_Tolerance_Remediation"

EXECUTE:
  - "104-INSTRUCTIONS-Execute_Implementation_Phase_Tasks"

INPUT:
  SPECS:
    SPEC_1:
      SPEC: "docs/implementation/in_progress/YOUR_SPEC_v1.0.0.md"
      PHASES: ["ALL"]
      TASKS: ["ALL"]

REMEMBER:
  - THIS IS A CODE ONLY SESSION.
  - NO DOCUMENTATION OF ANY KIND IS PERMITTED UNLESS I EXPLICITLY ASK FOR IT
  - NO OTHER INSTRUCTIONS FROM ANY OTHER YAML FILES OVERRIDE THIS DIRECTIVE
```

**File Discovery**:
- System automatically prepends base directory: `docs/implementation/instructions/v2/`
- System automatically appends extension: `.yaml`
- Example: `"000-DOCTRINE-Enterprise_Canonical_Execution"` → `docs/implementation/instructions/v2/000-DOCTRINE-Enterprise_Canonical_Execution.yaml`
- Version numbers in filenames are ignored (matches latest version)

### Full Path Format (Also Supported)

You can still use full paths if needed:

```yaml
LOAD_AND_PARSE:
  DOCTRINE: "docs/implementation/instructions/v2/000-DOCTRINE-Enterprise_Canonical_Execution-v2.0.1.yaml"
  PROTOCOLS:
    - docs/implementation/instructions/v2/001-PROTOCOL-The_GoldenRule_Execution-v2.0.1.yaml
    - docs/implementation/instructions/v2/002-PROTOCOL-Zero_Tolerance_Remediation-v2.0.0.yaml

EXECUTE:
  - docs/implementation/instructions/v2/104-INSTRUCTIONS-Execute_Implementation_Phase_Tasks-v2.0.0.yaml
```

---

## ⚡ SIMPLER FORMATS

### Overview

For quick execution, you can use simpler formats that reduce boilerplate. These formats work when:
- You only need protocols (no doctrine)
- The instruction accepts free text input
- You want minimal structure

### Format 1: Simple List (LOAD_AND_PARSE as List)

When you only need protocols and no doctrine:

**Simplified Format**:
```yaml
LOAD_AND_PARSE:
  - "002-PROTOCOL-Zero_Tolerance_Remediation"

EXECUTE:
  - "202-INSTRUCTIONS-Pure_Code_Implementation_Execution_Protocol"

INPUT: |
  Your free text here
  Can be multiple lines
  File path: docs/implementation/in_progress/YOUR_SPEC_v1.0.0.md
```

**Full Path Format** (also supported):
```yaml
LOAD_AND_PARSE:
  - docs/implementation/instructions/v2/002-PROTOCOL-Zero_Tolerance_Remediation-v2.0.0.yaml

EXECUTE:
  - docs/implementation/instructions/v2/202-INSTRUCTIONS-Pure_Code_Implementation_Execution_Protocol-v2.0.0.yaml
```

**Note**: `LOAD_AND_PARSE` as a list works when you only need protocols. For doctrine + protocols, use the standard dict format.

### Format 2: Free Text After YAML (No INPUT Wrapper)

Some instruction files define `input:` as free text. You can paste text directly after the YAML structure:

**Simplified Format**:
```yaml
LOAD_AND_PARSE:
  - "002-PROTOCOL-Zero_Tolerance_Remediation"

EXECUTE:
  - "202-INSTRUCTIONS-Pure_Code_Implementation_Execution_Protocol"

Requirement: Implement Redis storage factory
Files in scope: src/services/storage/factory.py
Constraints: Must be async, no blocking calls
```

**Full Path Format** (also supported):
```yaml
LOAD_AND_PARSE:
  - docs/implementation/instructions/v2/002-PROTOCOL-Zero_Tolerance_Remediation-v2.0.0.yaml

EXECUTE:
  - docs/implementation/instructions/v2/202-INSTRUCTIONS-Pure_Code_Implementation_Execution_Protocol-v2.0.0.yaml
```

**How it works**:
- YAML structure is parsed first
- Any text after YAML (outside structure) is treated as INPUT
- Instruction file's `input:` section receives this free text

### Format 3: INPUT at the End

You can place `INPUT:` at the end of the structure (YAML key order doesn't matter):

**Simplified Format**:
```yaml
LOAD_AND_PARSE:
  DOCTRINE: "000-DOCTRINE-Enterprise_Canonical_Execution"
  PROTOCOLS:
    - "001-PROTOCOL-The_GoldenRule_Execution"

EXECUTE:
  - "203-INSTRUCTIONS-FastAPI_Design_Implementation_Refactor"

REMEMBER:
  - THIS IS A CODE ONLY SESSION.
  - NO DOCUMENTATION OF ANY KIND IS PERMITTED UNLESS I EXPLICITLY ASK FOR IT
  - NO OTHER INSTRUCTIONS FROM ANY OTHER YAML FILES OVERRIDE THIS DIRECTIVE

INPUT:
  FOCUS: |
    - THE FILES, MODULES, CODEBLOCKS, CONFIGS, DATA STRUCTURES AND ALL CONTENT AND ALL RELATED TO WHAT WAS IMPLEMENTED IN THIS SESSION
    - AST DEFINED UPSTREAM AND DOWNSTREAM DEPENDENCIES ON THE CODE YOU IMPLEMENTED IN THIS SESSION
```

**Full Path Format** (also supported):
```yaml
LOAD_AND_PARSE:
  DOCTRINE: "docs/implementation/instructions/v2/000-DOCTRINE-Enterprise_Canonical_Execution-v2.0.1.yaml"
  PROTOCOLS:
    - docs/implementation/instructions/v2/001-PROTOCOL-The_GoldenRule_Execution-v2.0.1.yaml

EXECUTE:
  - docs/implementation/instructions/v2/203-INSTRUCTIONS-FastAPI_Design_Implementation_Refactor-v2.0.0.yaml
```

**Benefits**:
- Keeps execution flow together (LOAD → EXECUTE → REMEMBER)
- Input details come last
- Easier to append/modify input

### Format 4: Minimal Single Instruction

For quick single-instruction execution:

**Simplified Format**:
```yaml
EXECUTE:
  - "203-INSTRUCTIONS-FastAPI_Design_Implementation_Refactor"

INPUT:
  FOCUS: |
    - Files, modules, codeblocks implemented in this session
    - AST-defined upstream and downstream dependencies

REMEMBER:
  - THIS IS A CODE ONLY SESSION.
  - NO DOCUMENTATION OF ANY KIND IS PERMITTED UNLESS I EXPLICITLY ASK FOR IT
```

**Full Path Format** (also supported):
```yaml
EXECUTE:
  - docs/implementation/instructions/v2/203-INSTRUCTIONS-FastAPI_Design_Implementation_Refactor-v2.0.0.yaml
```

**When to use**: Quick execution without loading doctrine/protocols first.

### Format 5: Protocol List + Free Text

Simplest format for instructions that accept free text:

**Simplified Format**:
```yaml
LOAD_AND_PARSE:
  - "002-PROTOCOL-Zero_Tolerance_Remediation"

EXECUTE:
  - "202-INSTRUCTIONS-Pure_Code_Implementation_Execution_Protocol"

{{ user free text or file path here }}
```

**In practice**:
```yaml
LOAD_AND_PARSE:
  - "002-PROTOCOL-Zero_Tolerance_Remediation"

EXECUTE:
  - "202-INSTRUCTIONS-Pure_Code_Implementation_Execution_Protocol"

Requirement: Fix async issues in storage factory
Files: src/services/storage/factory.py
Mode: refactor
```

**Full Path Format** (also supported):
```yaml
LOAD_AND_PARSE:
  - docs/implementation/instructions/v2/002-PROTOCOL-Zero_Tolerance_Remediation-v2.0.0.yaml

EXECUTE:
  - docs/implementation/instructions/v2/202-INSTRUCTIONS-Pure_Code_Implementation_Execution_Protocol-v2.0.0.yaml
```

### When to Use Simpler Formats

**Use simpler formats when**:
- ✅ Quick single-instruction execution
- ✅ Instruction accepts free text input
- ✅ No need for doctrine/protocols
- ✅ Minimal structure needed

**Use standard format when**:
- ✅ Multiple instructions with chaining
- ✅ Need doctrine + protocols
- ✅ Complex SPEC dependencies
- ✅ OUTPUT_FROM mappings required

---

## 📁 FILE DISCOVERY

### How It Works

**Base Directory**: `docs/implementation/instructions/v2/`
**File Extension**: `.yaml` (automatically added)

### Simplified File References

Instead of full paths, you can use just the file name (without path and extension):

**Simplified**:
```yaml
EXECUTE:
  - "108-INSTRUCTIONS-Debug_And_Troubleshoot_Codebase"
```

**Resolves to**:
```
docs/implementation/instructions/v2/108-INSTRUCTIONS-Debug_And_Troubleshoot_Codebase.yaml
```

### Version Matching

If multiple versions exist, the system automatically finds the latest:
- `"000-DOCTRINE-Enterprise_Canonical_Execution"` matches:
  - `000-DOCTRINE-Enterprise_Canonical_Execution-v2.0.1.yaml` ✅ (latest)
  - `000-DOCTRINE-Enterprise_Canonical_Execution-v2.0.0.yaml`

### Partial Matching

You can use partial names (matches first found):
- `"Debug_And_Troubleshoot"` → matches `108-INSTRUCTIONS-Debug_And_Troubleshoot_Codebase-v2.0.0.yaml`
- `"Zero_Tolerance"` → matches `002-PROTOCOL-Zero_Tolerance_Remediation-v2.0.0.yaml`

**Note**: Partial matching is less precise. Use full names when possible.

### Custom Base Directory

You can override the base directory by providing a full path:
```yaml
EXECUTE:
  - "108-INSTRUCTIONS-Debug_And_Troubleshoot_Codebase"  # Uses default base
  - "custom/path/to/instruction.yaml"  # Uses custom path
```

---

## 📋 AVAILABLE OPTIONS

### DOCTRINE (Required - Only One)

**Simplified Format**:
```yaml
DOCTRINE: "000-DOCTRINE-Enterprise_Canonical_Execution"
```

**Full Path Format** (also supported):
```yaml
DOCTRINE: "docs/implementation/instructions/v2/000-DOCTRINE-Enterprise_Canonical_Execution-v2.0.1.yaml"
```

**Available Files**:
- `000-DOCTRINE-Enterprise_Canonical_Execution-v2.0.1.yaml` (only one)

**File Discovery**:
- Base directory: `docs/implementation/instructions/v2/`
- Extension: `.yaml` (auto-added)
- Version matching: Automatically finds latest version if multiple exist

---

### PROTOCOLS (Optional - Multiple)

**Simplified Format**:
```yaml
PROTOCOLS:
  - "001-PROTOCOL-The_GoldenRule_Execution"
  - "002-PROTOCOL-Zero_Tolerance_Remediation"
```

**Full Path Format** (also supported):
```yaml
PROTOCOLS:
  - docs/implementation/instructions/v2/001-PROTOCOL-The_GoldenRule_Execution-v2.0.1.yaml
  - docs/implementation/instructions/v2/002-PROTOCOL-Zero_Tolerance_Remediation-v2.0.0.yaml
```

**Available Files** (001-099 range):
- `001-PROTOCOL-The_GoldenRule_Execution-v2.0.1.yaml`
- `002-PROTOCOL-Zero_Tolerance_Remediation-v2.0.0.yaml`

**File Discovery**:
- Base directory: `docs/implementation/instructions/v2/`
- Extension: `.yaml` (auto-added)
- Version matching: Automatically finds latest version if multiple exist

---

### EXECUTE (Required - Multiple)

**Simplified Format**:
```yaml
EXECUTE:
  - "104-INSTRUCTIONS-Execute_Implementation_Phase_Tasks"
  - "107-INSTRUCTIONS-Remediate_And_Refactor_Codebase"
```

**Full Path Format** (also supported):
```yaml
EXECUTE:
  - docs/implementation/instructions/v2/104-INSTRUCTIONS-Execute_Implementation_Phase_Tasks-v2.0.0.yaml
  - docs/implementation/instructions/v2/107-INSTRUCTIONS-Remediate_And_Refactor_Codebase-v2.0.0.yaml
```

**Available Files** (100-199 range):
- `104-INSTRUCTIONS-Execute_Implementation_Phase_Tasks-v2.0.0.yaml`
- `105-INSTRUCTIONS-Run_Locally_and_Test_API_WebUI-v2.0.0.yaml`
- `106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance-v2.0.0.yaml`
- `107-INSTRUCTIONS-Remediate_And_Refactor_Codebase-v2.0.0.yaml`
- `108-INSTRUCTIONS-Debug_And_Troubleshoot_Codebase-v2.0.0.yaml`
- `110-INSTRUCTIONS-Build_Deploy_Test_and_Document_REST_API-v2.0.0.yaml`

**Available Files** (200-299 range):
- `202-INSTRUCTIONS-Pure_Code_Implementation_Execution_Protocol-v2.0.0.yaml`
- `203-INSTRUCTIONS-FastAPI_Design_Implementation_Refactor-v2.0.0.yaml`
- `204-INSTRUCTIONS-Live-Debugging-and-Remedation-v2.0.0.yaml`

**File Discovery**:
- Base directory: `docs/implementation/instructions/v2/`
- Extension: `.yaml` (auto-added)
- Version matching: Automatically finds latest version if multiple exist
- Partial matching: Can use just the name part (e.g., `"Debug_And_Troubleshoot"` matches `108-INSTRUCTIONS-Debug_And_Troubleshoot_Codebase`)

---

### INPUT.SPECS Options

#### Single SPEC (No Dependencies)

```yaml
INPUT:
  SPECS:
    SPEC_1:
      SPEC: "docs/implementation/in_progress/YOUR_SPEC_v1.0.0.md"
      PHASES: ["ALL"]
      TASKS: ["ALL"]
```

#### Multiple SPECs (No Dependencies)

```yaml
INPUT:
  SPECS:
    SPEC_1:
      SPEC: "docs/implementation/in_progress/SPEC_1_v1.0.0.md"
      PHASES: ["ALL"]
      TASKS: ["ALL"]

    SPEC_2:
      SPEC: "docs/implementation/in_progress/SPEC_2_v1.0.0.md"
      PHASES: ["ALL"]
      TASKS: ["ALL"]
```

#### SPEC with Dependency (Wait for Phase)

```yaml
INPUT:
  SPECS:
    SPEC_1:
      SPEC: "docs/implementation/in_progress/SPEC_1_v1.0.0.md"
      PHASES: ["ALL"]
      TASKS: ["ALL"]

    SPEC_2:
      SPEC: "docs/implementation/in_progress/SPEC_2_v1.0.0.md"
      DEPENDENCIES: ["SPEC_1"]
      WAIT_FOR:
        SPEC: "SPEC_1"
        CHECKPOINT: "PHASE_3"
      PHASES: ["ALL"]
      TASKS: ["ALL"]
```

#### SPEC with Dependency (Wait for Action)

```yaml
INPUT:
  SPECS:
    SPEC_2:
      SPEC: "docs/implementation/in_progress/SPEC_2_v1.0.0.md"
      DEPENDENCIES: ["SPEC_1"]
      WAIT_FOR:
        SPEC: "SPEC_1"
        CHECKPOINT: "ACTION_2.1"
      PHASES: ["ALL"]
      TASKS: ["ALL"]
```

#### SPEC with Dependency (Wait for Task)

```yaml
INPUT:
  SPECS:
    SPEC_2:
      SPEC: "docs/implementation/in_progress/SPEC_2_v1.0.0.md"
      DEPENDENCIES: ["SPEC_1"]
      WAIT_FOR:
        SPEC: "SPEC_1"
        CHECKPOINT: "TASK_1.1.1"
      PHASES: ["ALL"]
      TASKS: ["ALL"]
```

#### SPEC with Dependency (Wait for Step)

```yaml
INPUT:
  SPECS:
    SPEC_2:
      SPEC: "docs/implementation/in_progress/SPEC_2_v1.0.0.md"
      DEPENDENCIES: ["SPEC_1"]
      WAIT_FOR:
        SPEC: "SPEC_1"
        CHECKPOINT: "STEP_1.1.1.1"
      PHASES: ["ALL"]
      TASKS: ["ALL"]
```

#### SPEC with Multiple Dependencies

```yaml
INPUT:
  SPECS:
    SPEC_1:
      SPEC: "docs/implementation/in_progress/SPEC_1_v1.0.0.md"
      PHASES: ["ALL"]
      TASKS: ["ALL"]

    SPEC_2:
      SPEC: "docs/implementation/in_progress/SPEC_2_v1.0.0.md"
      DEPENDENCIES: ["SPEC_1"]
      WAIT_FOR:
        - SPEC: "SPEC_1"
          CHECKPOINT: "PHASE_3"
        - SPEC: "SPEC_1"
          CHECKPOINT: "ACTION_4.1"
      PHASES: ["ALL"]
      TASKS: ["ALL"]
```

#### SPEC with Dependency Policy

```yaml
INPUT:
  SPECS:
    SPEC_2:
      SPEC: "docs/implementation/in_progress/SPEC_2_v1.0.0.md"
      DEPENDENCIES: ["SPEC_1"]
      WAIT_FOR:
        SPEC: "SPEC_1"
        CHECKPOINT: "PHASE_3"
      ON_BLOCKED: "CONTINUE"  # Options: SKIP, CONTINUE, ERROR, WAIT
      PHASES: ["ALL"]
      TASKS: ["ALL"]
```

#### SPEC with Specific Phases/Tasks

```yaml
INPUT:
  SPECS:
    SPEC_1:
      SPEC: "docs/implementation/in_progress/SPEC_1_v1.0.0.md"
      PHASES: ["PHASE_1", "PHASE_2"]  # Only these phases
      TASKS: ["TASK_1.1.1", "TASK_1.1.2"]  # Only these tasks
```

---

### REMEMBER Options

#### Code Only Session

```yaml
REMEMBER:
  - THIS IS A CODE ONLY SESSION.
  - NO DOCUMENTATION OF ANY KIND IS PERMITTED UNLESS I EXPLICITLY ASK FOR IT
  - NO OTHER INSTRUCTIONS FROM ANY OTHER YAML FILES OVERRIDE THIS DIRECTIVE
```

#### Allow Documentation

```yaml
REMEMBER:
  - DOCUMENTATION IS PERMITTED.
  - CREATE DOCUMENTATION AS REQUIRED BY PROTOCOLS.
```

#### Custom Directives

```yaml
REMEMBER:
  - YOUR CUSTOM DIRECTIVE HERE
  - ANOTHER DIRECTIVE HERE
```

---

## 🎯 COMMON SCENARIOS

### Scenario 1: Execute Single SPEC

```yaml
LOAD_AND_PARSE:
  DOCTRINE: "docs/implementation/instructions/v2/000-DOCTRINE-Enterprise_Canonical_Execution-v2.0.1.yaml"
  PROTOCOLS:
    - docs/implementation/instructions/v2/001-PROTOCOL-The_GoldenRule_Execution-v2.0.1.yaml

EXECUTE:
  - docs/implementation/instructions/v2/104-INSTRUCTIONS-Execute_Implementation_Phase_Tasks-v2.0.0.yaml

INPUT:
  SPECS:
    SPEC_1:
      SPEC: "docs/implementation/in_progress/YOUR_SPEC_v1.0.0.md"
      PHASES: ["ALL"]
      TASKS: ["ALL"]

REMEMBER:
  - THIS IS A CODE ONLY SESSION.
  - NO DOCUMENTATION OF ANY KIND IS PERMITTED UNLESS I EXPLICITLY ASK FOR IT
```

---

### Scenario 2: Execute SPEC After Dependency Completes

```yaml
LOAD_AND_PARSE:
  DOCTRINE: "docs/implementation/instructions/v2/000-DOCTRINE-Enterprise_Canonical_Execution-v2.0.1.yaml"
  PROTOCOLS:
    - docs/implementation/instructions/v2/001-PROTOCOL-The_GoldenRule_Execution-v2.0.1.yaml
    - docs/implementation/instructions/v2/002-PROTOCOL-Zero_Tolerance_Remediation-v2.0.0.yaml

EXECUTE:
  - docs/implementation/instructions/v2/104-INSTRUCTIONS-Execute_Implementation_Phase_Tasks-v2.0.0.yaml

INPUT:
  SPECS:
    SPEC_1:
      SPEC: "docs/implementation/in_progress/STORAGE_FACTORY_SPEC_v1.0.0.md"
      PHASES: ["ALL"]
      TASKS: ["ALL"]

    SPEC_2:
      SPEC: "docs/implementation/in_progress/API_ROUTER_SPEC_v1.0.0.md"
      DEPENDENCIES: ["SPEC_1"]
      WAIT_FOR:
        SPEC: "SPEC_1"
        CHECKPOINT: "PHASE_3"
      PHASES: ["ALL"]
      TASKS: ["ALL"]

REMEMBER:
  - THIS IS A CODE ONLY SESSION.
  - NO DOCUMENTATION OF ANY KIND IS PERMITTED UNLESS I EXPLICITLY ASK FOR IT
```

---

### Scenario 3: Remediate Codebase

```yaml
LOAD_AND_PARSE:
  DOCTRINE: "docs/implementation/instructions/v2/000-DOCTRINE-Enterprise_Canonical_Execution-v2.0.1.yaml"
  PROTOCOLS:
    - docs/implementation/instructions/v2/001-PROTOCOL-The_GoldenRule_Execution-v2.0.1.yaml
    - docs/implementation/instructions/v2/002-PROTOCOL-Zero_Tolerance_Remediation-v2.0.0.yaml

EXECUTE:
  - docs/implementation/instructions/v2/107-INSTRUCTIONS-Remediate_And_Refactor_Codebase-v2.0.0.yaml

INPUT:
  SPECS:
    SPEC_1:
      SPEC: "docs/implementation/in_progress/YOUR_SPEC_v1.0.0.md"
      PHASES: ["ALL"]
      TASKS: ["ALL"]

REMEMBER:
  - THIS IS A CODE ONLY SESSION.
  - NO DOCUMENTATION OF ANY KIND IS PERMITTED UNLESS I EXPLICITLY ASK FOR IT
```

---

### Scenario 4: Debug and Troubleshoot

```yaml
LOAD_AND_PARSE:
  DOCTRINE: "docs/implementation/instructions/v2/000-DOCTRINE-Enterprise_Canonical_Execution-v2.0.1.yaml"
  PROTOCOLS:
    - docs/implementation/instructions/v2/001-PROTOCOL-The_GoldenRule_Execution-v2.0.1.yaml

EXECUTE:
  - docs/implementation/instructions/v2/108-INSTRUCTIONS-Debug_And_Troubleshoot_Codebase-v2.0.0.yaml

INPUT:
  SPECS:
    SPEC_1:
      SPEC: "docs/implementation/in_progress/YOUR_SPEC_v1.0.0.md"
      PHASES: ["ALL"]
      TASKS: ["ALL"]

REMEMBER:
  - THIS IS A CODE ONLY SESSION.
  - NO DOCUMENTATION OF ANY KIND IS PERMITTED UNLESS I EXPLICITLY ASK FOR IT
```

---

### Scenario 5: Validate Code Quality

```yaml
LOAD_AND_PARSE:
  DOCTRINE: "docs/implementation/instructions/v2/000-DOCTRINE-Enterprise_Canonical_Execution-v2.0.1.yaml"
  PROTOCOLS:
    - docs/implementation/instructions/v2/001-PROTOCOL-The_GoldenRule_Execution-v2.0.1.yaml

EXECUTE:
  - docs/implementation/instructions/v2/106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance-v2.0.0.yaml

INPUT:
  SPECS:
    SPEC_1:
      SPEC: "docs/implementation/in_progress/YOUR_SPEC_v1.0.0.md"
      PHASES: ["ALL"]
      TASKS: ["ALL"]

REMEMBER:
  - THIS IS A CODE ONLY SESSION.
  - NO DOCUMENTATION OF ANY KIND IS PERMITTED UNLESS I EXPLICITLY ASK FOR IT
```

---

## 📝 CHECKPOINT IDENTIFIERS

### Format
- **PHASE**: `"PHASE_X"` (e.g., `"PHASE_3"`)
- **ACTION**: `"ACTION_X.Y"` (e.g., `"ACTION_3.1"`)
- **TASK**: `"TASK_X.Y.Z"` (e.g., `"TASK_3.1.1"`)
- **STEP**: `"STEP_X.Y.Z.W"` (e.g., `"STEP_3.1.1.1"`)

### Examples
```yaml
CHECKPOINT: "PHASE_3"      # Wait for Phase 3 complete
CHECKPOINT: "ACTION_2.1"   # Wait for Action 2.1 complete
CHECKPOINT: "TASK_1.1.1"   # Wait for Task 1.1.1 complete
CHECKPOINT: "STEP_1.1.1.1" # Wait for Step 1.1.1.1 complete
```

---

## 🔧 DEPENDENCY POLICY OPTIONS

```yaml
ON_BLOCKED: "SKIP"     # Skip this SPEC if dependency blocked
ON_BLOCKED: "CONTINUE" # Continue anyway (ignore dependency)
ON_BLOCKED: "ERROR"    # Stop execution with error
ON_BLOCKED: "WAIT"     # Wait indefinitely (default)
```

---

## ✅ VALIDATION CHECKLIST

Before copying, verify:
- [ ] DOCTRINE path is correct
- [ ] PROTOCOL paths exist
- [ ] EXECUTE instruction paths exist
- [ ] SPEC file paths are correct
- [ ] CHECKPOINT identifiers match SPEC structure
- [ ] YAML syntax is valid (indentation, quotes)

---

## 🚨 COMMON MISTAKES

❌ **Wrong**: Missing quotes around paths
```yaml
DOCTRINE: docs/implementation/instructions/v2/000-DOCTRINE-Enterprise_Canonical_Execution-v2.0.1.yaml
```

✅ **Correct**: Quotes around paths
```yaml
DOCTRINE: "docs/implementation/instructions/v2/000-DOCTRINE-Enterprise_Canonical_Execution-v2.0.1.yaml"
```

❌ **Wrong**: Missing indentation
```yaml
SPECS:
SPEC_1:
  SPEC: "path/to/spec.md"
```

✅ **Correct**: Proper indentation
```yaml
SPECS:
  SPEC_1:
    SPEC: "path/to/spec.md"
```

❌ **Wrong**: Wrong checkpoint format
```yaml
CHECKPOINT: "Phase 3"  # Should be PHASE_3
```

✅ **Correct**: Proper checkpoint format
```yaml
CHECKPOINT: "PHASE_3"
```

---

## 📥 INSTRUCTION-SPECIFIC INPUT FIELDS

### Overview

Each instruction file defines its own `input:` template. You can provide instruction-specific input fields in the `INPUT:` section to guide execution. These fields complement `SPECS` and `OUTPUT_FROM` mappings.

### How to Use

1. **Check Instruction File**: Review the instruction file's `input:` section to see what fields it expects
2. **Add Fields to INPUT**: Add matching field names to your `INPUT:` section
3. **Provide Values**: Use YAML multiline strings (`|`) for multi-line content

### Common Instruction Input Fields

#### Validation (106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance)

```yaml
INPUT:
  # Active SPEC / compliance references:
  ACTIVE_SPEC: |
    docs/implementation/in_progress/YOUR_SPEC_v1.0.0.md

  # Validation tools / commands (if known):
  VALIDATION_TOOLS: |
    python -m flake8 src/
    python -m mypy src/
    python -m bandit -r src/

  # Policy notes (if relevant):
  POLICY_NOTES: |
    ZERO-WARNING / STRICT MODE
```

#### Remediation (107-INSTRUCTIONS-Remediate_And_Refactor_Codebase)

```yaml
INPUT:
  # Triggering failure(s):
  TRIGGERING_FAILURES: |
    flake8: FAILED (15 errors, 3 warnings)
    - src/services/api/routers/auth.py:15: F401 'unused_import' imported but unused
    - src/services/api/routers/auth.py:23: E501 line too long (125 > 120)

    mypy: FAILED (8 type errors)
    - src/services/api/routers/auth.py:45: Argument 1 has incompatible type

  # Allowed remediation scope (if constrained):
  ALLOWED_REMEDIATION_SCOPE: |
    Focus areas:
    - Files, modules, codeblocks implemented in this session
    - AST-defined upstream and downstream dependencies

  # Validation(s) to re-run:
  VALIDATION_TO_RE_RUN: |
    python -m flake8 src/services/api/routers/auth.py --select=E,F
    python -m mypy src/services/api/routers/auth.py --config-file mypy.ini
```

#### Debug (108-INSTRUCTIONS-Debug_And_Troubleshoot_Codebase)

```yaml
INPUT:
  # Observed failure / error:
  OBSERVED_FAILURE: |
    RedisConnectionError: Connection refused
    Application fails to initialize during StorageFactory startup

  # Runtime/platform (if known):
  RUNTIME_PLATFORM: docker

  # Logs (if available):
  LOGS: |
    [2025-12-18 10:15:23] ERROR: Redis connection failed
    [2025-12-18 10:15:23] ERROR: StorageFactory initialization failed

  # Code under investigation:
  CODE_UNDER_INVESTIGATION: |
    src/services/fastapi_services_platform/engine/services/storage/factory.py:731

  # Reproduction notes (if any):
  REPRODUCTION_NOTES: |
    - Occurs on application startup
    - Redis container not running or not accessible
```

#### Implementation (104-INSTRUCTIONS-Execute_Implementation_Phase_Tasks)

```yaml
INPUT:
  # Active SPEC file path:
  ACTIVE_SPEC_PATH: |
    docs/implementation/in_progress/YOUR_SPEC_v1.0.0.md

  # Execution scope:
  EXECUTION_SCOPE: full execution

  # Current status (if resuming):
  CURRENT_STATUS: |
    PHASE_3 / ACTION_3.1 / TASK_3.1.1
```

### Combining with OUTPUT_FROM

You can combine instruction-specific fields with `OUTPUT_FROM` chaining:

```yaml
EXECUTE:
  - docs/implementation/instructions/v2/106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance-v2.0.0.yaml
  - docs/implementation/instructions/v2/107-INSTRUCTIONS-Remediate_And_Refactor_Codebase-v2.0.0.yaml

INPUT:
  # Input for instruction 1 (Validation)
  ACTIVE_SPEC: |
    docs/implementation/in_progress/YOUR_SPEC_v1.0.0.md

  VALIDATION_TOOLS: |
    python -m flake8 src/
    python -m mypy src/

  POLICY_NOTES: |
    ZERO-WARNING / STRICT MODE

  # Output chaining: instruction 1 → instruction 2
  OUTPUT_FROM:
    FROM_INSTRUCTION: "106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance-v2.0.0.yaml"
    TO_INSTRUCTION: "107-INSTRUCTIONS-Remediate_And_Refactor_Codebase-v2.0.0.yaml"
    MAP:
      FAILURES: "TRIGGERING_FAILURES"
      BLOCKERS: "BLOCKERS"
      VALIDATION_COMMANDS: "VALIDATION_TO_RE_RUN"

  # Input for instruction 2 (Remediation)
  # Will be populated from instruction 1 output via OUTPUT_FROM mapping
  TRIGGERING_FAILURES: |
    # Will be populated from instruction 1 output
    # Focus areas:
    - Files, modules, codeblocks implemented in this session
    - AST-defined upstream and downstream dependencies

  ALLOWED_REMEDIATION_SCOPE: |
    Focus areas:
    - Files, modules, codeblocks implemented in this session
    - AST-defined upstream and downstream dependencies

  VALIDATION_TO_RE_RUN: |
    # Will be populated from instruction 1 output
```

### Complete Example: Validate → Remediate with Focus Areas

```yaml
LOAD_AND_PARSE:
  DOCTRINE: "docs/implementation/instructions/v2/000-DOCTRINE-Enterprise_Canonical_Execution-v2.0.1.yaml"
  PROTOCOLS:
    - docs/implementation/instructions/v2/001-PROTOCOL-The_GoldenRule_Execution-v2.0.1.yaml
    - docs/implementation/instructions/v2/002-PROTOCOL-Zero_Tolerance_Remediation-v2.0.0.yaml

EXECUTE:
  - docs/implementation/instructions/v2/106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance-v2.0.0.yaml
  - docs/implementation/instructions/v2/107-INSTRUCTIONS-Remediate_And_Refactor_Codebase-v2.0.0.yaml

INPUT:
  # Input for instruction 1 (Validation)
  ACTIVE_SPEC: |
    # Focus areas:
    - THE FILES, MODULES, CODEBLOCKS, CONFIGS, DATA STRUCTURES AND ALL CONTENT AND ALL RELATED TO WHAT WAS IMPLEMENTED IN THIS SESSION
    - AST DEFINED UPSTREAM AND DOWNSTREAM DEPENDENCIES ON THE CODE YOU IMPLEMENTED IN THIS SESSION

  VALIDATION_TOOLS: |
    # Standard validation commands will be used
    # Focus on files/modules implemented in this session

  POLICY_NOTES: |
    ZERO-WARNING / STRICT MODE

  # Output chaining: instruction 1 → instruction 2
  OUTPUT_FROM:
    FROM_INSTRUCTION: "106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance-v2.0.0.yaml"
    TO_INSTRUCTION: "107-INSTRUCTIONS-Remediate_And_Refactor_Codebase-v2.0.0.yaml"
    MAP:
      FAILURES: "TRIGGERING_FAILURES"
      BLOCKERS: "BLOCKERS"
      VALIDATION_COMMANDS: "VALIDATION_TO_RE_RUN"

  # Input for instruction 2 (Remediation)
  TRIGGERING_FAILURES: |
    # Will be populated from instruction 1 output via OUTPUT_FROM mapping
    # Focus areas:
    - THE FILES, MODULES, CODEBLOCKS, CONFIGS, DATA STRUCTURES AND ALL CONTENT AND ALL RELATED TO WHAT WAS IMPLEMENTED IN THIS SESSION
    - AST DEFINED UPSTREAM AND DOWNSTREAM DEPENDENCIES ON THE CODE YOU IMPLEMENTED IN THIS SESSION

  ALLOWED_REMEDIATION_SCOPE: |
    # Focus areas:
    - THE FILES, MODULES, CODEBLOCKS, CONFIGS, DATA STRUCTURES AND ALL CONTENT AND ALL RELATED TO WHAT WAS IMPLEMENTED IN THIS SESSION
    - AST DEFINED UPSTREAM AND DOWNSTREAM DEPENDENCIES ON THE CODE YOU IMPLEMENTED IN THIS SESSION

  VALIDATION_TO_RE_RUN: |
    # Will be populated from instruction 1 output via OUTPUT_FROM mapping

REMEMBER:
  - THIS IS A CODE ONLY SESSION.
  - NO DOCUMENTATION OF ANY KIND IS PERMITTED UNLESS I EXPLICITLY ASK FOR IT
  - NO OTHER INSTRUCTIONS FROM ANY OTHER YAML FILES OVERRIDE THIS DIRECTIVE
```

### Field Name Reference

**Validation Instruction (106)**:
- `ACTIVE_SPEC` - SPEC/compliance references
- `VALIDATION_TOOLS` - Validation commands/tools
- `POLICY_NOTES` - Policy flags (ZERO-WARNING, STRICT MODE)

**Remediation Instruction (107)**:
- `TRIGGERING_FAILURES` - Errors/failed checks/SPEC references
- `ALLOWED_REMEDIATION_SCOPE` - Constrained files/modules
- `VALIDATION_TO_RE_RUN` - Commands to re-run after remediation

**Debug Instruction (108)**:
- `OBSERVED_FAILURE` - Failure description
- `RUNTIME_PLATFORM` - Runtime environment (docker, k8s, local, etc.)
- `LOGS` - Log output
- `CODE_UNDER_INVESTIGATION` - Files/snippets to investigate
- `REPRODUCTION_NOTES` - Steps/conditions to reproduce

**Implementation Instruction (104)**:
- `ACTIVE_SPEC_PATH` - SPEC file path
- `EXECUTION_SCOPE` - full execution, continuation, or specific key
- `CURRENT_STATUS` - Current phase/action/task if resuming

### Tips

1. **Check Instruction Files**: Always review the instruction file's `input:` section to see exact field names
2. **Use Comments**: Add comments explaining which instruction each field applies to
3. **Combine Fields**: You can provide both instruction-specific fields AND `SPECS` in the same `INPUT:` section
4. **Multiline Strings**: Use `|` for multi-line content, `>` for folded strings
5. **Focus Areas**: Use consistent focus area descriptions across related fields

---

## 🔗 CHAINING OUTPUTS BETWEEN INSTRUCTIONS

### Overview

When executing multiple instructions sequentially, you can pass output from one instruction to the next using the `OUTPUT_FROM` field in the INPUT section.

### Basic Pattern

```yaml
EXECUTE:
  - docs/implementation/instructions/v2/106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance-v2.0.0.yaml
  - docs/implementation/instructions/v2/107-INSTRUCTIONS-Remediate_And_Refactor_Codebase-v2.0.0.yaml

INPUT:
  OUTPUT_FROM:
    INSTRUCTION_1: "106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance-v2.0.0.yaml"
    MAP_TO: "107-INSTRUCTIONS-Remediate_And_Refactor_Codebase-v2.0.0.yaml"
    MAPPING:
      FAILURES: "TRIGGERING_FAILURES"
      VALIDATION_RESULTS: "VALIDATION_RESULTS"
      BLOCKERS: "BLOCKERS"
  SPECS:
    SPEC_1:
      SPEC: "docs/implementation/in_progress/YOUR_SPEC_v1.0.0.md"
      PHASES: ["ALL"]
      TASKS: ["ALL"]
```

### Example 1: Validate → Remediate

**Step 1: Validation Output**
```yaml
EXECUTE:
  - docs/implementation/instructions/v2/106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance-v2.0.0.yaml

INPUT:
  SPECS:
    SPEC_1:
      SPEC: "docs/implementation/in_progress/YOUR_SPEC_v1.0.0.md"
      PHASES: ["ALL"]
      TASKS: ["ALL"]
```

**Output from Validation** (captured):
```
VALIDATION RESULTS:
- flake8: FAILED (15 errors, 3 warnings)
- mypy: FAILED (8 type errors)
- bandit: PASSED (0 issues)

FAILURES:
- src/services/api/routers/auth.py:15: F401 'unused_import' imported but unused
- src/services/api/routers/auth.py:23: E501 line too long (125 > 120)
- src/services/api/routers/auth.py:45: mypy error: Argument 1 has incompatible type

BLOCKERS:
- flake8 errors must be resolved
- mypy type errors must be resolved
```

**Step 2: Remediation Input** (chained):
```yaml
EXECUTE:
  - docs/implementation/instructions/v2/107-INSTRUCTIONS-Remediate_And_Refactor_Codebase-v2.0.0.yaml

INPUT:
  OUTPUT_FROM:
    INSTRUCTION: "106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance-v2.0.0.yaml"
    TRIGGERING_FAILURES: |
      # FAILURES from validation:
      - flake8: FAILED (15 errors, 3 warnings)
        - src/services/api/routers/auth.py:15: F401 'unused_import' imported but unused
        - src/services/api/routers/auth.py:23: E501 line too long (125 > 120)
      - mypy: FAILED (8 type errors)
        - src/services/api/routers/auth.py:45: mypy error: Argument 1 has incompatible type

      # BLOCKERS:
      - flake8 errors must be resolved
      - mypy type errors must be resolved

      # VALIDATION(S) TO RE-RUN:
      - python -m flake8 src/services/api/routers/auth.py --select=E,F
      - python -m mypy src/services/api/routers/auth.py --config-file mypy.ini
  SPECS:
    SPEC_1:
      SPEC: "docs/implementation/in_progress/YOUR_SPEC_v1.0.0.md"
      PHASES: ["ALL"]
      TASKS: ["ALL"]
```

### Example 2: Execute → Debug

**Step 1: Implementation Output**
```yaml
EXECUTE:
  - docs/implementation/instructions/v2/104-INSTRUCTIONS-Execute_Implementation_Phase_Tasks-v2.0.0.yaml
```

**Output from Implementation** (captured):
```
IMPLEMENTATION COMPLETE:
- Phase 3: Redis Integration - COMPLETE
- Phase 4: Per API Host Databases - COMPLETE

RUNTIME ERROR OBSERVED:
- Error: RedisConnectionError: Connection refused
- File: src/services/fastapi_services_platform/engine/services/storage/factory.py:731
- Traceback: [full traceback]

BLOCKERS:
- Redis not available at startup
- Application fails to initialize
```

**Step 2: Debug Input** (chained):
```yaml
EXECUTE:
  - docs/implementation/instructions/v2/108-INSTRUCTIONS-Debug_And_Troubleshoot_Codebase-v2.0.0.yaml

INPUT:
  OUTPUT_FROM:
    INSTRUCTION: "104-INSTRUCTIONS-Execute_Implementation_Phase_Tasks-v2.0.0.yaml"
    OBSERVED_FAILURE: |
      # Observed failure / error:
      RedisConnectionError: Connection refused
      Application fails to initialize during StorageFactory startup

      # Runtime/platform:
      docker

      # Code under investigation:
      src/services/fastapi_services_platform/engine/services/storage/factory.py:731

      # Traceback:
      [full traceback from implementation output]

      # Reproduction notes:
      - Occurs on application startup
      - Redis container not running or not accessible
  SPECS:
    SPEC_1:
      SPEC: "docs/implementation/in_progress/YOUR_SPEC_v1.0.0.md"
      PHASES: ["ALL"]
      TASKS: ["ALL"]
```

### Example 3: Validate → Remediate → Validate (Full Cycle)

```yaml
LOAD_AND_PARSE:
  DOCTRINE: "docs/implementation/instructions/v2/000-DOCTRINE-Enterprise_Canonical_Execution-v2.0.1.yaml"
  PROTOCOLS:
    - docs/implementation/instructions/v2/001-PROTOCOL-The_GoldenRule_Execution-v2.0.1.yaml

EXECUTE:
  - docs/implementation/instructions/v2/106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance-v2.0.0.yaml
  - docs/implementation/instructions/v2/107-INSTRUCTIONS-Remediate_And_Refactor_Codebase-v2.0.0.yaml
  - docs/implementation/instructions/v2/106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance-v2.0.0.yaml

INPUT:
  OUTPUT_FROM:
    STEP_1_TO_2:
      FROM: "106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance-v2.0.0.yaml"
      TO: "107-INSTRUCTIONS-Remediate_And_Refactor_Codebase-v2.0.0.yaml"
      MAPPING:
        FAILURES: "TRIGGERING_FAILURES"
        BLOCKERS: "BLOCKERS"
        VALIDATION_COMMANDS: "VALIDATION_TO_RE_RUN"
    STEP_2_TO_3:
      FROM: "107-INSTRUCTIONS-Remediate_And_Refactor_Codebase-v2.0.0.yaml"
      TO: "106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance-v2.0.0.yaml"
      MAPPING:
        FILES_MODIFIED: "VALIDATION_SCOPE"
        RE_VALIDATION_COMMANDS: "VALIDATION_TOOLS"
  SPECS:
    SPEC_1:
      SPEC: "docs/implementation/in_progress/YOUR_SPEC_v1.0.0.md"
      PHASES: ["ALL"]
      TASKS: ["ALL"]
```

### Output Mapping Reference

#### Validation → Remediation
```yaml
OUTPUT_FROM:
  FAILURES → TRIGGERING_FAILURES
  BLOCKERS → BLOCKERS
  VALIDATION_COMMANDS → VALIDATION_TO_RE_RUN
  FILES_WITH_ISSUES → ALLOWED_REMEDIATION_SCOPE
```

#### Remediation → Validation
```yaml
OUTPUT_FROM:
  FILES_MODIFIED → VALIDATION_SCOPE
  RE_VALIDATION_COMMANDS → VALIDATION_TOOLS
  REMEDIATION_RESULTS → VALIDATION_CONTEXT
```

#### Implementation → Debug
```yaml
OUTPUT_FROM:
  RUNTIME_ERROR → OBSERVED_FAILURE
  TRACEBACK → TRACEBACK
  FAILING_CODE → CODE_UNDER_INVESTIGATION
  ENVIRONMENT → RUNTIME_PLATFORM
```

#### Debug → Remediation
```yaml
OUTPUT_FROM:
  ROOT_CAUSE → TRIGGERING_FAILURE
  EVIDENCE → EVIDENCE
  FIX_REQUIRED → REMEDIATION_SCOPE
```

### Simplified Format (Recommended)

Instead of complex mappings, use direct paste format:

```yaml
EXECUTE:
  - docs/implementation/instructions/v2/106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance-v2.0.0.yaml
  - docs/implementation/instructions/v2/107-INSTRUCTIONS-Remediate_And_Refactor_Codebase-v2.0.0.yaml

INPUT:
  # Output from instruction 1 (paste here):
  TRIGGERING_FAILURES: |
    # Paste validation failures here
    # Format: [ERROR_TYPE]: [DESCRIPTION]
    # - File: [PATH]:[LINE]: [ERROR]

  VALIDATION_TO_RE_RUN: |
    # Paste validation commands to re-run here
    # Format: [COMMAND]

  SPECS:
    SPEC_1:
      SPEC: "docs/implementation/in_progress/YOUR_SPEC_v1.0.0.md"
      PHASES: ["ALL"]
      TASKS: ["ALL"]
```

### Manual Chaining (Step-by-Step)

**Step 1**: Execute first instruction
```yaml
EXECUTE:
  - docs/implementation/instructions/v2/106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance-v2.0.0.yaml
```

**Step 2**: Copy output from Step 1

**Step 3**: Execute second instruction with output as input
```yaml
EXECUTE:
  - docs/implementation/instructions/v2/107-INSTRUCTIONS-Remediate_And_Refactor_Codebase-v2.0.0.yaml

INPUT:
  TRIGGERING_FAILURES: |
    # Paste output from Step 1 here
    [PASTE VALIDATION FAILURES]

  VALIDATION_TO_RE_RUN: |
    # Paste validation commands from Step 1
    [PASTE COMMANDS]
```

### Automatic Chaining (If Supported)

```yaml
EXECUTE:
  - docs/implementation/instructions/v2/106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance-v2.0.0.yaml
  - docs/implementation/instructions/v2/107-INSTRUCTIONS-Remediate_And_Refactor_Codebase-v2.0.0.yaml

INPUT:
  CHAIN_OUTPUTS: true
  OUTPUT_MAPPING:
    FROM_INSTRUCTION: "106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance-v2.0.0.yaml"
    TO_INSTRUCTION: "107-INSTRUCTIONS-Remediate_And_Refactor_Codebase-v2.0.0.yaml"
    MAP:
      FAILURES: "TRIGGERING_FAILURES"
      BLOCKERS: "BLOCKERS"
  SPECS:
    SPEC_1:
      SPEC: "docs/implementation/in_progress/YOUR_SPEC_v1.0.0.md"
      PHASES: ["ALL"]
      TASKS: ["ALL"]
```

---

---

## 📚 THREE-TIER QUICK REFERENCE

### When to Use Each Tier

**Always Load DOCTRINE When**:
- ✅ You need foundational operational principles
- ✅ You want explicit enforcement of core rules
- ✅ You're doing production code work
- ✅ You need consistency across multiple sessions

**Load PROTOCOLS When**:
- ✅ You need specific validation methodologies
- ✅ You want domain-specific enforcement (FastAPI, testing, etc.)
- ✅ You need compliance checkpoints
- ✅ You want enhanced violation detection

**Execute INSTRUCTIONS When**:
- ✅ You have a specific task to complete
- ✅ You need step-by-step workflow guidance
- ✅ You want to implement, validate, or remediate

### Tier Combination Patterns

**Pattern 1: Full Stack** (Most Comprehensive)
```
DOCTRINE + Multiple PROTOCOLS + INSTRUCTIONS
```
Use for: Production work, complex workflows, comprehensive validation

**Pattern 2: Protocol Stack** (Domain-Specific)
```
DOCTRINE + Domain PROTOCOLS + INSTRUCTIONS
```
Use for: FastAPI work, testing, documentation, specific domains

**Pattern 3: Minimal Stack** (Quick Tasks)
```
INSTRUCTIONS only
```
Use for: Quick fixes, simple tasks, when DOCTRINE/PROTOCOLS are already understood

**Pattern 4: Rules Only** (Reference)
```
DOCTRINE + PROTOCOLS (no INSTRUCTIONS)
```
Use for: Understanding constraints, reference, planning

### Protocol Selection Guide

**For Code Quality**:
- `001-PROTOCOL-The_GoldenRule_Execution` (mandatory workflow)
- `002-PROTOCOL-Zero_Tolerance_Remediation` (violation detection)
- `008-PROTOCOL-Production_Code_Quality` (12 metrics)

**For FastAPI Work**:
- `003-PROTOCOL-FastAPI_Pure_Code_Implementation` (FastAPI rules)
- `004-PROTOCOL-Validate_Remediate_Codebase` (validation)

**For Testing**:
- `009-PROTOCOL-Test_Implementation` (test standards)

**For Tool Usage**:
- `007-PROTOCOL-MCP_Tools_Workflow` (tool patterns)

**For Terminology**:
- `006-PROTOCOL-RFC2119_Requirements_Language` (MUST/SHALL/SHOULD/MAY)

**For Roles**:
- `005-PROTOCOL-Digital_Assistant_Roles` (role definitions)

---

**Last Updated**: 2025-12-20
**Quick Reference**: Copy template above, modify SPEC paths and options as needed
