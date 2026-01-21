# Instruction System v2 - Execution Guide

**Version**: v2.0.0
**Last Updated**: 2025-12-18
**Purpose**: Guide for AI agents executing structured instruction prompts

---

## 📋 OVERVIEW

This directory contains structured instruction files organized by type and priority. Instructions are executed through a standardized YAML prompt format that defines foundational rules (DOCTRINE/PROTOCOLS) and execution steps (INSTRUCTIONS).

---

## 📁 FILE NAMING CONVENTION

### Pattern
```
{number}-{TYPE}-{Name}-{version}.yaml
```

### Number Ranges (Hierarchy)
- **000**: Doctrine (only one - foundational execution rules)
- **001-099**: Protocols (validation, remediation, compliance rules)
- **100-199**: Formal multistep instructions (complete workflows)
- **200-299**: Focused instructions (targeted, single-purpose tasks)

### Type Prefixes
- **DOCTRINE**: Foundational execution rules (HOW to operate)
- **PROTOCOL**: Validation/compliance rules (HOW to validate)
- **INSTRUCTIONS**: Execution workflows (WHAT to do)

### Examples
- `000-DOCTRINE-Enterprise_Canonical_Execution-v2.0.1.yaml`
- `001-PROTOCOL-The_GoldenRule_Execution-v2.0.1.yaml`
- `104-INSTRUCTIONS-Execute_Implementation_Phase_Tasks-v2.0.0.yaml`
- `202-INSTRUCTIONS-Pure_Code_Implementation_Execution_Protocol-v2.0.0.yaml`

---

## 🎯 PROMPT STRUCTURE

### Standard Format (Simplified File References)

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
      SPEC: "docs/implementation/in_progress/STORAGE_FACTORY_DB_ARCHITECTURE_REDIS_REFACTOR_SPEC_v1.0.0.md"
      PHASES: ["ALL"]
      TASKS: ["ALL"]

    SPEC_2:
      SPEC: "{{ SPEC_2 file Path }}"
      DEPENDENCIES: ["SPEC_1"]
      WAIT_FOR:
        SPEC: "SPEC_1"
        CHECKPOINT: "PHASE_3"
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

### Simpler Formats

For quick execution, you can use simpler formats that reduce boilerplate:

#### Format 1: LOAD_AND_PARSE as List

When you only need protocols (no doctrine), you can use a simple list:

**Simplified Format**:
```yaml
LOAD_AND_PARSE:
  - "002-PROTOCOL-Zero_Tolerance_Remediation"

EXECUTE:
  - "202-INSTRUCTIONS-Pure_Code_Implementation_Execution_Protocol"

INPUT: |
  Your free text here
  Can be multiple lines
```

**Full Path Format** (also supported):
```yaml
LOAD_AND_PARSE:
  - docs/implementation/instructions/v2/002-PROTOCOL-Zero_Tolerance_Remediation-v2.0.0.yaml

EXECUTE:
  - docs/implementation/instructions/v2/202-INSTRUCTIONS-Pure_Code_Implementation_Execution_Protocol-v2.0.0.yaml
```

**Note**: Use standard dict format (`DOCTRINE:` + `PROTOCOLS:`) when you need both doctrine and protocols.

#### Format 2: Free Text After YAML

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
1. YAML structure (`LOAD_AND_PARSE`, `EXECUTE`) is parsed first
2. Any text after YAML (outside the YAML structure) is treated as `INPUT`
3. The instruction file's `input:` section receives this free text

**Why this works**: The instruction file already has `input:` defined as free text, so text after YAML is automatically treated as input.

#### Format 3: INPUT at the End

YAML key order doesn't matter. You can place `INPUT:` at the end:

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
- Easier to append/modify input without scrolling

#### Format 4: Minimal Single Instruction

For quick single-instruction execution without doctrine/protocols:

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

#### Format 5: Protocol List + Free Text (Simplest)

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
- ✅ Instruction accepts free text input (check instruction file's `input:` section)
- ✅ No need for doctrine/protocols
- ✅ Minimal structure needed

**Use standard format when**:
- ✅ Multiple instructions with chaining
- ✅ Need doctrine + protocols
- ✅ Complex SPEC dependencies
- ✅ OUTPUT_FROM mappings required
- ✅ Instruction expects structured input fields

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

## 🔍 SECTION BREAKDOWN

### LOAD_AND_PARSE

**Purpose**: Load foundational rules that govern HOW execution occurs.

**Structure**:
- `DOCTRINE`: Single file (the 000-DOCTRINE file)
- `PROTOCOLS`: List of protocol files (001-099 range)

**What to do**:
1. Load and parse the DOCTRINE file
2. Load and parse all PROTOCOL files
3. Understand the behavioral constraints and validation rules
4. These rules govern ALL downstream execution

**Key Rules**:
- DOCTRINE defines HOW to operate (log-first, evidence-based, minimal changes)
- PROTOCOLS define HOW to validate (stop on failure, require evidence, binary verdicts)
- These rules take precedence over any conflicting instructions

---

### EXECUTE

**Purpose**: List of instruction files to execute in order.

**Structure**:
- List of instruction file paths (100-199 or 200-299 range)

**What to do**:
1. Execute instruction files sequentially in the order listed
2. Each instruction file defines a workflow or task
3. Follow the workflow defined in each instruction file
4. Complete each instruction before moving to the next
5. Capture output from each instruction for potential chaining

**Execution Order**:
- Files are executed in the order they appear in the list
- Do NOT skip files or execute in parallel unless explicitly allowed
- Each instruction may reference INPUT.SPECS for context
- Output from one instruction can be passed to the next via INPUT.OUTPUT_FROM

**Output Chaining**:
- Each instruction produces output (validation results, errors, file changes, etc.)
- Output can be captured and passed to subsequent instructions
- Use `INPUT.OUTPUT_FROM` to map output from one instruction to input of another
- See "Chaining Outputs Between Instructions" section below for details

---

### INPUT.SPECS

**Purpose**: Define which SPEC files to process and their dependencies.

**Structure**:
```yaml
SPECS:
  SPEC_1:
    SPEC: "path/to/spec.md"
    PHASES: ["ALL"]  # or ["PHASE_1", "PHASE_2"]
    TASKS: ["ALL"]   # or ["TASK_1.1.1", "TASK_1.1.2"]

  SPEC_2:
    SPEC: "path/to/spec2.md"
    DEPENDENCIES: ["SPEC_1"]
    WAIT_FOR:
      SPEC: "SPEC_1"
      CHECKPOINT: "PHASE_3"  # Wait for PHASE 3 to complete
    PHASES: ["ALL"]
    TASKS: ["ALL"]
```

**What to do**:

1. **Load SPEC Files**:
   - Load each SPEC file listed
   - Parse the SPEC structure (Phases → Actions → Tasks → Steps)
   - Understand the work scope

2. **Process Dependencies**:
   - If `DEPENDENCIES` is specified, check dependency completion
   - Use `WAIT_FOR` to determine completion criteria:
     - `CHECKPOINT: "PHASE_X"` → Wait for all checkboxes in PHASE X to be `[x]`
     - `CHECKPOINT: "ACTION_X.Y"` → Wait for all checkboxes in ACTION X.Y to be `[x]`
     - `CHECKPOINT: "TASK_X.Y.Z"` → Wait for all checkboxes in TASK X.Y.Z to be `[x]`
     - `CHECKPOINT: "STEP_X.Y.Z.W"` → Wait for STEP X.Y.Z.W checkbox to be `[x]`

3. **Checkbox Verification**:
   - Parse SPEC file markdown
   - Find the specified checkpoint (PHASE/ACTION/TASK/STEP)
   - Verify all checkboxes under that checkpoint are `[x]` (checked)
   - If all checked → Dependency satisfied → Proceed
   - If any unchecked → Dependency not satisfied → Wait or handle per policy

4. **Execute SPEC Work**:
   - Process phases/tasks as specified in `PHASES` and `TASKS`
   - `["ALL"]` means process all phases/tasks
   - `["PHASE_1", "PHASE_2"]` means process only those phases
   - Follow the SPEC file's implementation plan

**Dependency Resolution Logic**:
```
For each dependency:
  1. Load dependency SPEC file
  2. Find checkpoint section (PHASE/ACTION/TASK/STEP)
  3. Check all checkboxes under checkpoint
  4. If all [x] → Dependency satisfied
  5. If any [ ] → Dependency not satisfied
  6. If WAIT_FOR specified → Wait until satisfied
  7. If ON_BLOCKED policy → Handle per policy (SKIP/CONTINUE/ERROR)
```

---

### REMEMBER

**Purpose**: Session-level directives that override other instructions.

**Structure**:
- List of directive strings

**What to do**:
1. Apply these directives to ALL execution
2. These override conflicting instructions from other YAML files
3. Common directives:
   - `CODE ONLY SESSION` → No documentation unless explicitly requested
   - `NO DOCUMENTATION` → Prohibit documentation creation
   - `OVERRIDE DIRECTIVE` → This section takes precedence

**Enforcement**:
- These directives are ABSOLUTE
- They override instructions from DOCTRINE/PROTOCOLS/INSTRUCTIONS
- Exception: SPEC file creation/updates are mandatory (protocol requirement)

---

## 📥 INSTRUCTION-SPECIFIC INPUT FIELDS

### Overview

Each instruction file defines its own `input:` template that specifies what input fields it expects. You can provide instruction-specific input fields in the `INPUT:` section to guide execution. These fields work alongside `SPECS` and `OUTPUT_FROM` mappings.

### How Instruction Input Works

1. **Instruction File Defines Template**: Each instruction file has an `input:` section showing expected fields
2. **You Provide Matching Fields**: Add fields to `INPUT:` section that match the instruction's template
3. **Fields Guide Execution**: Instruction uses these fields to understand scope, constraints, and context

### Finding Input Templates

To see what fields an instruction expects:
1. Open the instruction file (e.g., `106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance-v2.0.0.yaml`)
2. Find the `input:` section
3. Review the commented template showing expected fields

### Common Instruction Input Fields

#### Validation Instruction (106)

**Template** (from instruction file):
```yaml
input: |
  # Active SPEC / compliance references:
  # [PATHS]
  #
  # Validation tools / commands (if known):
  # [COMMANDS]
  #
  # Policy notes (if relevant):
  # [ZERO-WARNING / STRICT MODE FLAGS]
```

**Usage Example**:
```yaml
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

#### Remediation Instruction (107)

**Template** (from instruction file):
```yaml
input: |
  # Triggering failure(s):
  # [ERRORS / FAILED CHECKS / SPEC REFERENCES]
  #
  # Allowed remediation scope (if constrained):
  # [FILES / MODULES]
  #
  # Validation(s) to re-run:
  # [COMMANDS]
```

**Usage Example**:
```yaml
INPUT:
  TRIGGERING_FAILURES: |
    flake8: FAILED (15 errors, 3 warnings)
    - src/services/api/routers/auth.py:15: F401 'unused_import' imported but unused

    mypy: FAILED (8 type errors)
    - src/services/api/routers/auth.py:45: Argument 1 has incompatible type

  ALLOWED_REMEDIATION_SCOPE: |
    Focus areas:
    - Files, modules, codeblocks implemented in this session
    - AST-defined upstream and downstream dependencies

  VALIDATION_TO_RE_RUN: |
    python -m flake8 src/services/api/routers/auth.py --select=E,F
    python -m mypy src/services/api/routers/auth.py --config-file mypy.ini
```

#### Debug Instruction (108)

**Template** (from instruction file):
```yaml
input: |
  # Observed failure / error:
  # [DESCRIPTION]
  #
  # Runtime/platform (if known):
  # [docker | k8s | systemd | local | ci | cloud | unknown]
  #
  # Logs (if available):
  # [PASTE LOGS]
  #
  # Code under investigation:
  # [FILES / SNIPPETS]
  #
  # Reproduction notes (if any):
  # [STEPS / CONDITIONS]
```

**Usage Example**:
```yaml
INPUT:
  OBSERVED_FAILURE: |
    RedisConnectionError: Connection refused
    Application fails to initialize during StorageFactory startup

  RUNTIME_PLATFORM: docker

  LOGS: |
    [2025-12-18 10:15:23] ERROR: Redis connection failed
    [2025-12-18 10:15:23] ERROR: StorageFactory initialization failed

  CODE_UNDER_INVESTIGATION: |
    src/services/fastapi_services_platform/engine/services/storage/factory.py:731

  REPRODUCTION_NOTES: |
    - Occurs on application startup
    - Redis container not running or not accessible
```

#### Implementation Instruction (104)

**Template** (from instruction file):
```yaml
input: |
  # Active SPEC file path:
  # [PATH]
  #
  # Execution scope:
  # - full execution
  # - continuation
  # - specific YAML key (e.g. instructions.steps[2])
  #
  # Current status (if resuming):
  # [PHASE / ACTION / TASK / STEP]
```

**Usage Example**:
```yaml
INPUT:
  ACTIVE_SPEC_PATH: |
    docs/implementation/in_progress/YOUR_SPEC_v1.0.0.md

  EXECUTION_SCOPE: full execution

  CURRENT_STATUS: |
    PHASE_3 / ACTION_3.1 / TASK_3.1.1
```

### Combining Instruction Input with SPECS

You can provide both instruction-specific fields AND `SPECS`:

```yaml
INPUT:
  # Instruction-specific fields
  ACTIVE_SPEC: |
    docs/implementation/in_progress/YOUR_SPEC_v1.0.0.md

  VALIDATION_TOOLS: |
    python -m flake8 src/

  # SPEC definitions
  SPECS:
    SPEC_1:
      SPEC: "docs/implementation/in_progress/YOUR_SPEC_v1.0.0.md"
      PHASES: ["ALL"]
      TASKS: ["ALL"]
```

### Combining Instruction Input with OUTPUT_FROM

You can combine instruction-specific fields with output chaining:

```yaml
INPUT:
  # Input for instruction 1
  ACTIVE_SPEC: |
    docs/implementation/in_progress/YOUR_SPEC_v1.0.0.md

  VALIDATION_TOOLS: |
    python -m flake8 src/

  # Output chaining
  OUTPUT_FROM:
    FROM_INSTRUCTION: "106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance-v2.0.0.yaml"
    TO_INSTRUCTION: "107-INSTRUCTIONS-Remediate_And_Refactor_Codebase-v2.0.0.yaml"
    MAP:
      FAILURES: "TRIGGERING_FAILURES"

  # Input for instruction 2 (will receive output from instruction 1)
  TRIGGERING_FAILURES: |
    # Will be populated from instruction 1 output
    Focus areas:
    - Files implemented in this session

  ALLOWED_REMEDIATION_SCOPE: |
    Focus areas:
    - Files implemented in this session
```

### Field Name Matching

**Important**: Field names in your `INPUT:` section should match the instruction file's `input:` template. The instruction file uses these field names to extract values.

**Best Practice**:
- Review the instruction file's `input:` section
- Use exact field names shown in comments
- Add your own comments to clarify which instruction each field applies to

### Complete Example

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

---

## 🔗 CHAINING OUTPUTS BETWEEN INSTRUCTIONS

### Overview

When executing multiple instructions sequentially, output from one instruction can be passed as input to the next instruction. This enables workflows like:
- Validate → Remediate (pass failures to remediation)
- Execute → Debug (pass errors to debugging)
- Remediate → Validate (pass modified files to validation)

### How It Works

1. **First Instruction Executes**:
   - Produces output according to its `output:` section format
   - Output includes: failures, errors, file changes, validation results, etc.

2. **Output Captured**:
   - System captures output from first instruction
   - Output formatted according to instruction's output specification

3. **Output Mapped to Next Instruction**:
   - Output fields mapped to next instruction's `input:` template
   - Mapping defined in `INPUT.OUTPUT_FROM` section

4. **Second Instruction Executes**:
   - Receives mapped output as input context
   - Uses input to guide execution

### Basic Pattern

```yaml
EXECUTE:
  - docs/implementation/instructions/v2/106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance-v2.0.0.yaml
  - docs/implementation/instructions/v2/107-INSTRUCTIONS-Remediate_And_Refactor_Codebase-v2.0.0.yaml

INPUT:
  OUTPUT_FROM:
    FROM_INSTRUCTION: "106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance-v2.0.0.yaml"
    TO_INSTRUCTION: "107-INSTRUCTIONS-Remediate_And_Refactor_Codebase-v2.0.0.yaml"
    MAPPING:
      FAILURES: "TRIGGERING_FAILURES"
      BLOCKERS: "BLOCKERS"
      VALIDATION_COMMANDS: "VALIDATION_TO_RE_RUN"
  SPECS:
    SPEC_1:
      SPEC: "docs/implementation/in_progress/YOUR_SPEC_v1.0.0.md"
      PHASES: ["ALL"]
      TASKS: ["ALL"]
```

### Simplified Format (Recommended)

Instead of complex mappings, directly paste output into next instruction's input format:

```yaml
EXECUTE:
  - docs/implementation/instructions/v2/106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance-v2.0.0.yaml
  - docs/implementation/instructions/v2/107-INSTRUCTIONS-Remediate_And_Refactor_Codebase-v2.0.0.yaml

INPUT:
  # Output from instruction 1 (paste here):
  TRIGGERING_FAILURES: |
    # Paste validation failures here
    # Format matches instruction's output section

  VALIDATION_TO_RE_RUN: |
    # Paste validation commands to re-run

  SPECS:
    SPEC_1:
      SPEC: "docs/implementation/in_progress/YOUR_SPEC_v1.0.0.md"
      PHASES: ["ALL"]
      TASKS: ["ALL"]
```

### Common Output Mappings

**Validate → Remediate**:
- `FAILURES` → `TRIGGERING_FAILURES`
- `BLOCKERS` → `BLOCKERS`
- `VALIDATION_COMMANDS` → `VALIDATION_TO_RE_RUN`
- `FILES_WITH_ISSUES` → `ALLOWED_REMEDIATION_SCOPE`

**Remediation → Validate**:
- `FILES_MODIFIED` → `VALIDATION_SCOPE`
- `RE_VALIDATION_COMMANDS` → `VALIDATION_TOOLS`

**Implementation → Debug**:
- `RUNTIME_ERROR` → `OBSERVED_FAILURE`
- `TRACEBACK` → `TRACEBACK`
- `FAILING_CODE` → `CODE_UNDER_INVESTIGATION`

**Debug → Remediation**:
- `ROOT_CAUSE` → `TRIGGERING_FAILURE`
- `EVIDENCE` → `EVIDENCE`

### Manual Chaining Process

1. **Execute First Instruction**:
   ```yaml
   EXECUTE:
     - docs/implementation/instructions/v2/106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance-v2.0.0.yaml
   ```

2. **Capture Output**:
   - Copy output from first instruction execution
   - Output format defined in instruction's `output:` section

3. **Format for Next Instruction**:
   - Review next instruction's `input:` section template
   - Format captured output to match input template

4. **Execute Second Instruction with Output**:
   ```yaml
   EXECUTE:
     - docs/implementation/instructions/v2/107-INSTRUCTIONS-Remediate_And_Refactor_Codebase-v2.0.0.yaml

   INPUT:
     TRIGGERING_FAILURES: |
       # Paste formatted output here
   ```

### Example: Validate → Remediate → Validate

```yaml
EXECUTE:
  - docs/implementation/instructions/v2/106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance-v2.0.0.yaml
  - docs/implementation/instructions/v2/107-INSTRUCTIONS-Remediate_And_Refactor_Codebase-v2.0.0.yaml
  - docs/implementation/instructions/v2/106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance-v2.0.0.yaml

INPUT:
  OUTPUT_FROM:
    STEP_1_TO_2:
      FROM: "106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance-v2.0.0.yaml"
      TO: "107-INSTRUCTIONS-Remediate_And_Refactor_Codebase-v2.0.0.yaml"
      MAP:
        FAILURES: "TRIGGERING_FAILURES"
        BLOCKERS: "BLOCKERS"
    STEP_2_TO_3:
      FROM: "107-INSTRUCTIONS-Remediate_And_Refactor_Codebase-v2.0.0.yaml"
      TO: "106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance-v2.0.0.yaml"
      MAP:
        FILES_MODIFIED: "VALIDATION_SCOPE"
        RE_VALIDATION_COMMANDS: "VALIDATION_TOOLS"
  SPECS:
    SPEC_1:
      SPEC: "docs/implementation/in_progress/YOUR_SPEC_v1.0.0.md"
      PHASES: ["ALL"]
      TASKS: ["ALL"]
```

**Execution Flow**:
1. Instruction 1 executes → Produces validation results
2. Output captured → Mapped to Instruction 2 input
3. Instruction 2 executes → Uses validation failures to remediate
4. Output captured → Mapped to Instruction 3 input
5. Instruction 3 executes → Validates remediation results

---

## 🔄 EXECUTION FLOW

### Step-by-Step Process

1. **Parse YAML Prompt**:
   - Load the YAML structure
   - Validate structure (LOAD_AND_PARSE, EXECUTE, INPUT, REMEMBER)

2. **Load Foundational Rules**:
   - Load DOCTRINE file → Understand HOW to operate
   - Load all PROTOCOL files → Understand HOW to validate
   - Apply these rules to all downstream execution

3. **Resolve SPEC Dependencies**:
   - For each SPEC in INPUT.SPECS:
     - Check if DEPENDENCIES specified
     - If yes, load dependency SPEC files
     - Check WAIT_FOR checkpoint completion
     - Verify checkboxes are `[x]`
     - If satisfied → Mark SPEC ready
     - If not satisfied → Wait or handle per policy

4. **Execute Instructions**:
   - For each instruction file in EXECUTE list:
     - Load instruction file
     - Understand workflow/task
     - If `INPUT.OUTPUT_FROM` specified, load output from previous instruction
     - Map previous output to current instruction's input format
     - Execute workflow using INPUT.SPECS context and mapped output
     - Capture output according to instruction's output format
     - Complete instruction before moving to next

5. **Process SPEC Work**:
   - For each ready SPEC:
     - Process phases/tasks as specified
     - Follow SPEC file implementation plan
     - Update SPEC file checkboxes as work completes
     - Respect REMEMBER directives

6. **Apply REMEMBER Directives**:
   - Enforce session-level directives throughout
   - Override conflicting instructions
   - Exception: SPEC lifecycle management (mandatory)

---

## 📊 DEPENDENCY RESOLUTION DETAILS

### Checkpoint Levels

**PHASE Level**:
- Identifier: `"PHASE_3"`
- Checks: All checkboxes under `### PHASE 3:` section
- Complete when: All actions/tasks/steps in PHASE 3 are `[x]`

**ACTION Level**:
- Identifier: `"ACTION_3.1"`
- Checks: All checkboxes under `#### ACTION 3.1:` section
- Complete when: All tasks/steps in ACTION 3.1 are `[x]`

**TASK Level**:
- Identifier: `"TASK_3.1.1"`
- Checks: All checkboxes under `- [ ] **TASK 3.1.1**:` section
- Complete when: All steps in TASK 3.1.1 are `[x]`

**STEP Level**:
- Identifier: `"STEP_3.1.1.1"`
- Checks: Single checkbox `- [ ] STEP 3.1.1.1:`
- Complete when: STEP 3.1.1.1 is `[x]`

### Multiple Dependencies

```yaml
WAIT_FOR:
  - SPEC: "SPEC_1"
    CHECKPOINT: "PHASE_3"
  - SPEC: "SPEC_1"
    CHECKPOINT: "ACTION_4.1"
```
- Wait for BOTH checkpoints to be complete
- All specified checkpoints must be satisfied

### Dependency Policies

```yaml
DEPENDENCIES: ["SPEC_1"]
WAIT_FOR:
  SPEC: "SPEC_1"
  CHECKPOINT: "PHASE_3"
ON_BLOCKED: "CONTINUE"  # Options: SKIP, CONTINUE, ERROR, WAIT
```
- `SKIP`: Skip this SPEC if dependency is blocked
- `CONTINUE`: Continue anyway (ignore dependency)
- `ERROR`: Stop execution with error
- `WAIT`: Wait indefinitely (default)

---

## 🎯 EXAMPLES

### Example 1: Simple Execution

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
      SPEC: "docs/implementation/in_progress/MY_SPEC_v1.0.0.md"
      PHASES: ["ALL"]
      TASKS: ["ALL"]
```

**What to do**:
1. Load DOCTRINE and PROTOCOL
2. Execute instruction 104
3. Process SPEC_1 (all phases/tasks)

---

### Example 2: With Dependencies

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
```

**What to do**:
1. Load DOCTRINE and PROTOCOL
2. Load SPEC_1 and SPEC_2
3. Check SPEC_1 PHASE_3 completion (all checkboxes `[x]`)
4. If SPEC_1 PHASE_3 complete → Start SPEC_2
5. If SPEC_1 PHASE_3 incomplete → Wait (or handle per policy)
6. Execute instruction 104 with both SPECs

---

### Example 3: Multiple Checkpoints

```yaml
INPUT:
  SPECS:
    SPEC_2:
      SPEC: "docs/implementation/in_progress/SPEC_2.md"
      DEPENDENCIES: ["SPEC_1"]
      WAIT_FOR:
        - SPEC: "SPEC_1"
          CHECKPOINT: "PHASE_3"
        - SPEC: "SPEC_1"
          CHECKPOINT: "ACTION_4.1"
      PHASES: ["ALL"]
      TASKS: ["ALL"]
```

**What to do**:
1. Check SPEC_1 PHASE_3 → All checkboxes `[x]`?
2. Check SPEC_1 ACTION_4.1 → All checkboxes `[x]`?
3. If BOTH satisfied → Start SPEC_2
4. If either incomplete → Wait

---

## ⚠️ CRITICAL RULES

### Rule 1: Sequential Execution
- Execute instruction files in order
- Complete each before moving to next
- Do NOT parallelize unless explicitly allowed

### Rule 2: Dependency Resolution
- Always check dependency completion before starting dependent SPEC
- Use checkbox state, not status text
- Respect WAIT_FOR checkpoints

### Rule 3: REMEMBER Directives
- REMEMBER directives are ABSOLUTE
- They override other instructions
- Exception: SPEC lifecycle management (mandatory)

### Rule 4: SPEC File Updates
- Update SPEC file checkboxes as work completes
- Mark `[ ]` → `[x]` when step/task/action/phase complete
- This enables dependency resolution for other SPECs

### Rule 5: File Discovery
- Use glob patterns to find files:
  - `*-DOCTRINE-*.yaml` → Find doctrine
  - `*-PROTOCOL-*.yaml` → Find all protocols
  - `*-INSTRUCTIONS-*.yaml` → Find all instructions
- Number ranges indicate category (000, 001-099, 100-199, 200-299)

---

## 🔧 IMPLEMENTATION NOTES

### Parsing SPEC Files

When checking checkboxes:
1. Load SPEC file markdown
2. Find section header (e.g., `### PHASE 3:`)
3. Parse all checkboxes under that section
4. Check format: `- [ ]` (unchecked) or `- [x]` (checked)
5. Verify ALL are `[x]` for completion

### Handling Blocked SPECs

If SPEC is blocked (waiting for testing, etc.):
- Check `ON_BLOCKED` policy if specified
- Default: Wait indefinitely
- Options: SKIP, CONTINUE, ERROR, WAIT

### SPEC File Status

SPEC files track status via:
- Checkbox state (`[x]` = complete, `[ ]` = incomplete)
- Status line (e.g., `Status: ✅ Production Code Complete`)
- Both can be used, but checkboxes are more reliable

---

## 📚 RELATED DOCUMENTATION

- **Workflow Guide**: `docs/implementation/IMPLEMENTATION_WORKFLOW_GUIDE_v1.0.0.md`
- **Implementation Plan**: `docs/implementation/IMPLEMENTATION_PLAN_v1.0.0.md`
- **SPEC Template**: See workflow guide for SPEC structure

---

## ✅ VALIDATION CHECKLIST

Before executing a prompt, verify:
- [ ] YAML structure is valid
- [ ] All file paths exist
- [ ] DOCTRINE file loaded and understood
- [ ] PROTOCOL files loaded and understood
- [ ] SPEC files exist and are parseable
- [ ] Dependencies can be resolved
- [ ] REMEMBER directives are clear
- [ ] Execution order is logical

---

**Last Updated**: 2025-12-18
**Maintainer**: Implementation Team
