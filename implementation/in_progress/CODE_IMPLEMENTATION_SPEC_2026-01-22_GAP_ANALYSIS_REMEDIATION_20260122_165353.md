# Session Initialization - Protocol Enforcement Code Implementation Specification

**Version**: v1.0.0
**Date**: 2026-01-22
**Last Updated**: 2026-01-22 16:57:39 (Australia/Adelaide)
**Status**: 🟡 In Progress - Session Initialized
**Priority**: P0 - CRITICAL
**Session Type**: Code Implementation and Remediation Session
**Instruction Files**:

- `002-PROTOCOL-Zero_Tolerance_Remediation-v2.0.0.yaml`
- `003-PROTOCOL-FastAPI_Pure_Code_Implementation-v2.0.0.yaml`
- `104-INSTRUCTIONS-Execute_Implementation_Phase_Tasks-v2.0.0.yaml`
- `107-INSTRUCTIONS-Remediate_And_Refactor_Codebase-v2.0.0.yaml`
- `202-INSTRUCTIONS-Pure_Code_Implementation_Execution_Protocol-v2.0.0.yaml`
- `203-INSTRUCTIONS-FastAPI_Design_Implementation_Refactor-v2.0.0.yaml`

---

## 📊 SESSION SUMMARY

### Session Objective

This session is initialized for code implementation and remediation following the combined execution protocols. The session enforces multiple critical protocols:

- **002-PROTOCOL-Zero_Tolerance_Remediation** (v2.0.0) - ENFORCED
- **003-PROTOCOL-FastAPI_Pure_Code_Implementation** (v2.0.0) - ENFORCED
- **104-INSTRUCTIONS-Execute_Implementation_Phase_Tasks** (v2.0.0) - ENFORCED
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

- **Status**: Session initialized - Awaiting explicit implementation task
- **Work Type**: TBD (IMPLEMENTATION / REMEDIATION / REFACTOR - awaiting classification)
- **Scope**: TBD (awaiting identification)
- **Files/Modules**: TBD (awaiting identification)
- **Context**: Session initialized per user instruction

### FastAPI Services Platform Context Loaded

The following FastAPI Services Platform documentation has been reviewed:

- ✅ `src/services/fastapi_services_platform/README.md` - Main platform documentation
- ✅ `src/services/fastapi_services_platform/engine/README.md` - Engine runtime layer
- ✅ `src/services/fastapi_services_platform/docs/README.md` - Documentation index
- ✅ `src/services/fastapi_services_platform/docs/architecture/README.md` - Architecture documentation index

**Key Understanding**:

- FastAPI Services Platform is a **FOUNDATIONAL DROP-IN SERVICE CAPABILITY**
- Uses its OWN dedicated databases (separate from application databases)
- Self-configuring via config files (`router_factory_settings.yaml`, `router_factory_features.yaml`, `feature_flags.json`)
- App Factory ONLY CALLS Router Factory, does NOT configure it
- Router registration order: API → UI → Platform API → Platform UI (Hub Router ABSOLUTE LAST)

---

## ✅ IMPLEMENTATION PLAN (TASK-BY-TASK) — GAP ANALYSIS REMEDIATION

This plan is derived from [docs/implementation/in_progress/GAP_ANALYSIS_AND_RECOMMENDATIONS_2026-01-22.md](docs/implementation/in_progress/GAP_ANALYSIS_AND_RECOMMENDATIONS_2026-01-22.md). It is written to be executed under the **Sequential Implementation Directive**:

- One change at a time, one file at a time.
- Validate each change before proceeding.
- No bulk/mass refactors.
- “No evidence = no pass”.

### Definitions (used throughout)

- **Gate**: a validation action that produces a pass/fail outcome (lint, tests, structure, build, runtime start).
- **Evidence Appendix**: an evidence record that captures command, cwd, target, exit code, and a short output excerpt.

### Evidence Appendix template (MANDATORY for every gate)

- **Timestamp**:
- **Purpose / Gate**:
- **Command**:
- **CWD**:
- **Target** (exact path / capability root):
- **Exit code**:
- **Output excerpt** (10–50 lines max):
- **Artifacts produced** (paths in repo, if any):

---

## Phase 0 — Plan Setup & Target Lock (P0)

### 0.1 Target selection and locking
- [ ] Identify the exact capability/package/workspace target for this remediation stream (single canonical root).
- [ ] Record the resolved target path once and re-use it everywhere.
- [ ] Identify the **minimum** runtime start command (or import-only check) for the FastAPI platform target.

### 0.2 Evidence enforcement (meta-gate)
- [ ] For every future gate, append an Evidence Appendix entry into this spec under the relevant phase.
- [ ] Add the explicit rule: “PASS is forbidden without evidence.”

Exit criteria:
- Target is locked and recorded.
- Evidence Appendix template is present and will be used for all subsequent steps.

---

## Phase 1 — SPEC Phase-State Normalization (P0)

Objective: remove contradictions like “Pending + FAIL” and “Pending + PASS with criteria checked”.

### 1.1 Define canonical phase status model
- [ ] Add the allowed status set to the primary spec: Pending / In Progress / Complete (PASS) / Complete (FAIL) / Complete (MIXED).
- [ ] Define the rule: checklist and validation criteria must not conflict with the declared phase status.

### 1.2 Apply normalization to the current remediation specs
- [ ] Update [docs/implementation/in_progress/CODE_IMPLEMENTATION_SPEC_2026-01-22_UFC_RETROSPECTIVE_AND_FASTAPI_REMEDIATION.md](docs/implementation/in_progress/CODE_IMPLEMENTATION_SPEC_2026-01-22_UFC_RETROSPECTIVE_AND_FASTAPI_REMEDIATION.md) so Phase 2 is clearly “Complete (FAIL)” (or “In Progress” if being actively remediated).
- [ ] Update any “Phase 5 Complete” language appearing inside Phase 4 blocks (move/correct).
- [ ] Ensure every phase has an unambiguous entry/exit gate statement.

Gate: documentation-only consistency check (no code execution required).

Exit criteria:
- Phase state semantics are consistent and enforceable across the spec.

---

## Phase 2 — Runtime Viability Restoration: `au_sys_fastapi_services_platform` (P0)

Objective: remove import/startup failures caused by missing `core/*` modules referenced by `main.py`.

### 2.1 Reproduce the failure (evidence-first)
- [ ] Run the minimal “startup/import check” (as defined in Phase 0) and capture Evidence Appendix.
- [ ] Identify the first failing import(s) and their expected module locations.

### 2.2 Decide resolution approach (explicit decision record)
- [ ] Decision A: Implement the missing modules (`core/logging.py`, `core/middleware.py`, `core/database.py`, `core/bootstrap.py`) according to the UFC reference patterns.
- [ ] Decision B: Update the platform bootstrapping so it no longer imports non-existent modules (only if consistent with UFC reference and platform docs).
- [ ] Record the decision in this spec, including why.

### 2.3 Implement minimal viable core modules or adjust bootstrapping (one file per step)
- [ ] Create/restore `core/logging.py` or adjust its import usage.
- [ ] Create/restore `core/middleware.py` or adjust its import usage.
- [ ] Create/restore `core/database.py` or adjust its import usage.
- [ ] Create/restore `core/bootstrap.py` or adjust its import usage.
- [ ] After each file edit: run the minimal import/start check and capture Evidence Appendix.

### 2.4 Restore “start succeeds” gate
- [ ] Define a deterministic “platform starts” command (or import-only proxy if server start is not possible).
- [ ] Execute and capture evidence.

Exit criteria:
- No import errors from `main.py`.
- Minimal runtime start gate passes with evidence.

---

## Phase 3 — Structural Stabilization (P1)

Objective: reduce structural ambiguity and monolithic dumping in `adapters/api`, and eliminate duplicates.

### 3.1 Inventory and classify (read-only first)
- [ ] Identify top-level directories and their current UFC layer mapping (Core/Adapters/Manifest).
- [ ] Identify “misplaced infra” modules (e.g., `db.py`, `security.py`) and decide correct layer.
- [ ] Identify duplicates (e.g., `bulk_operations.py` appearing multiple times).

### 3.2 One-by-one relocation and deduplication
- [ ] For each misplaced module: move/rename once, then immediately update imports in the smallest necessary set.
- [ ] For each duplicate: choose a single authoritative implementation; remove/merge the duplicate deterministically.
- [ ] After each change: run the minimal import/start gate and capture evidence.

### 3.3 Adapter boundary shaping (avoid monolith)
- [ ] Define coherent boundaries inside `adapters/api` (routers, services, dependencies, schemas, etc.).
- [ ] Apply the reshaping one sub-area at a time (one directory/file group per step, but still one edit operation at a time).

Exit criteria:
- Duplicate modules eliminated.
- Misplaced infra aligned with UFC layer expectations.
- Runtime gate still passes.

---

## Phase 4 — Canonical Script Catalog + Mechanical Validation (P1)

Objective: eliminate script numbering/naming drift (001–018 vs 001–019 vs 001–020) and ensure docs/YAML match actual filesystem.

### 4.1 Establish the canonical source of truth
- [ ] Select the canonical toolkit location (single directory) and record it.
- [ ] Produce a filesystem-derived inventory of scripts (name, purpose, expected inputs/outputs).

### 4.2 Update documentation references to match reality
- [ ] Update any runbooks/spec sections that reference script names that do not exist.
- [ ] Normalize naming in documentation to match actual filenames (no aliasing).

### 4.3 Add a mechanical consistency check
- [ ] Implement a non-destructive validator that checks: “docs/yaml references exist on disk”.
- [ ] Gate: run validator and capture evidence.

Exit criteria:
- One authoritative catalog exists.
- Specs/runbooks do not reference missing scripts.
- Validator gate passes with evidence.

---

## Phase 5 — Template Strategy Decision + Enforcement (P2)

Objective: resolve embedded-vs-external template ambiguity, and align success criteria.

### 5.1 Decision record (choose one)
- [ ] Option A (External Jinja2 templates): scripts load templates from a canonical templates directory.
- [ ] Option B (Embedded/library-first generation): embedded templates are allowed and documented; remove contradictory “external required” criteria.
- [ ] Record the decision, including:
   - rationale
   - constraints
   - where templates live
   - how drift is prevented

### 5.2 Apply enforcement
- [ ] Update the relevant generator scripts (e.g., 010–014 group) one-by-one to conform.
- [ ] Update the relevant YAML instructions to match the chosen reality.
- [ ] Gate: regenerate into a scratch/temporary target and verify expected outputs (no bulk edits to production targets).

Exit criteria:
- Template source-of-truth is unambiguous.
- Scripts + YAML + docs are aligned.

---

## Phase 6 — Path Resolution Standardization (P2)

Objective: eliminate fragile heuristic root finding and inconsistent `--target` usage.

### 6.1 Adopt a single PathResolver approach
- [ ] Confirm the canonical resolver (e.g., `PathResolver.resolve_from_monorepo`) and document it.
- [ ] For every tool that accepts a target: ensure it uses the same resolution and logs the resolved root.

### 6.2 “Target lock” convention enforcement
- [ ] Ensure tools echo the resolved target root in output.
- [ ] Ensure tools error if target is ambiguous rather than guessing.

Gate: run 2–3 representative tools with the same target and verify they agree on the resolved root (capture evidence).

Exit criteria:
- No tool uses “search up N directories” heuristics without explicit bounded rules.
- Resolved roots are consistent across tools.

---

## Phase 7 — Security Remediation Integrity (P2)

Objective: ensure security fixes remove risk rather than evading detectors.

### 7.1 Formalize security remediation rules
- [ ] Secrets must be removed to env/config/secret store; no obfuscation.
- [ ] Zero-tolerance checks must be satisfied by principled fixes.

### 7.2 Apply to any existing “questionable remediations”
- [ ] Identify instances where remediation narratives imply bypassing detectors.
- [ ] Replace with principled remediations; capture evidence gate.

Exit criteria:
- Security remediation posture is principled and auditable.

---

## Phase 8 — Migration Integrity Rules (Hierarchy Preservation) (P2)

Objective: enforce the migration rule stated in the gap analysis: preserve relative hierarchy by default; regroup deterministically when needed.

### 8.1 Define the migration ruleset
- [ ] Default: preserve relative source hierarchy.
- [ ] Exceptions: regroup by vendor / role / function (documented mapping).
- [ ] Require a mapping artifact when regrouping.

### 8.2 Update migrator/import-rewriter tooling to enforce
- [ ] Ensure the physical migration step preserves hierarchy unless instructed.
- [ ] Ensure import rewriting is deterministic and recorded.
- [ ] Gate: run on a small representative subset and compare mapping outputs.

Exit criteria:
- Migration behavior is deterministic, repeatable, and evidenced.

---

## Phase 9 — End-to-End Gate Run (P0/P1/P2 consolidated)

Objective: produce a final auditable run proving the plan outcomes.

### 9.1 Define the final gate sequence
- [ ] Structure validation gate
- [ ] Imports validation gate
- [ ] Build gate
- [ ] Unit test gate
- [ ] Integration gate (if applicable)
- [ ] Zero-tolerance gate
- [ ] Runtime start gate (FastAPI platform)

### 9.2 Execute gates sequentially with evidence
- [ ] Run Gate 1 + Evidence Appendix
- [ ] Run Gate 2 + Evidence Appendix
- [ ] …

Exit criteria:
- All applicable gates pass.
- Evidence exists for every gate.

---

## ⚠️ CRITICAL DIRECTIVES (ABSOLUTE AUTHORITY - OVERRIDES ALL OTHER INSTRUCTIONS)

### Session Focus Directive

**THIS IS A CODE IMPLEMENTATION AND REFACTORINGS FOCUSED SESSION.**

- **PRIMARY FOCUS**: Code implementation and refactoring ONLY
- **FORBIDDEN**: Any activity not directly related to code implementation/refactoring
- **MANDATORY**: All work must be code-focused and production-ready

### Sequential Implementation Directive

**THE USE OF SCRIPTS OR MASS MODIFICATIONS TO THE CODE IS STRICTLY FORBIDDEN.**

- **FORBIDDEN**: Scripts that modify multiple files simultaneously
- **FORBIDDEN**: Mass modifications or bulk changes
- **FORBIDDEN**: Automated refactoring tools that modify multiple files at once
- **MANDATORY**: ALL code must be implemented and validated ONE STEP AT A TIME, in a SEQUENTIAL MANNER
- **MANDATORY**: Each file modification must be validated before proceeding to the next
- **MANDATORY**: Sequential, controlled, validated implementation only

### Documentation Directive

**NO DOCUMENTATION OF ANY KIND IS PERMITTED UNLESS EXPLICITLY REQUESTED.**

- **FORBIDDEN**: Creating documentation files unless user explicitly asks for it
- **FORBIDDEN**: Writing README files, markdown documentation, or temporal reports
- **FORBIDDEN**: Interpreting implicit requests as documentation needs
- **MANDATORY**: User must EXPLICITLY state "create documentation" or "write documentation"
- **EXCEPTION**: CODE_IMPLEMENTATION_SPEC is EXEMPT (mandatory protocol artifact)
- **EXCEPTION**: Code docstrings REQUIRED (standard Python practice - NOT documentation files)

### Override Authority Directive

**NO OTHER INSTRUCTIONS FROM ANY OTHER YAML FILES OVERRIDE THIS DIRECTIVE.**

- **ABSOLUTE AUTHORITY**: These directives take precedence over ALL other YAML file instructions
- **FORBIDDEN**: Following documentation requirements from other YAML files that conflict with these directives
- **MANDATORY**: These directives are IRON CLAD and NON-NEGOTIABLE
- **ENFORCEMENT**: Violation of these directives = BLOCKING ISSUE - execution MUST STOP immediately

---

## 🔧 IMPLEMENTATION METHODOLOGY

### Core Principles (From Combined Protocols)

1. **CODE DISCOVERY AND GAP ANALYSIS FIRST** (NON-NEGOTIABLE)
   - **EXAMINE PRODUCTION CODEBASE**: Start by examining the production codebase for any missing elements, TODO comments, mocks, stubs, or unfinished code
   - **IDENTIFY PARTIALLY COMPLETED ITEMS**: Identify which items are partially completed and can be quickly implemented by copying and adjusting them, using local repositories or cloned GitHub repositories
   - **EXTENSIVELY SCAN CODEBASE**: Extensively scan and search the codebase for other gaps that can be promptly resolved
   - **PINPOINT REACTIVATABLE ITEMS**: Proceed to pinpoint those items within your list that were only partially completed but could be promptly reactivated or restored through copying and appropriate adaptation. These elements should be sourced from existing cloned GitHub repositories or discovered GitHub repositories that SHALL be cloned
   - **USE MCP TOOLS**: MUST use MCP TOOLS (grep and fetch) to retrieve additional repositories, code examples, or semantically similar codebase from GitHub to quickly use as a base and/or to scaffold
   - **CLONE REPOSITORIES**: MUST use GIT TO CLONE all useful discovered GitHub repos to the local repository, even if they are only going to provide a small benefit to this codebase. NOTE: This is to use for future references and examples, do NOT remove the cloned repos
   - **SELECTIVE COPY AND MODIFY**: Clone these repositories into the local environment and selectively copy and modify the required files, modules, or code segments to address the issues
   - **RECORD PLANNING**: Record your planning in CODE_IMPLEMENTATION_SPEC_DOCS, DO NOT include code examples
   - ALWAYS search codebase before writing code
   - Use MCP Grep to find existing patterns/utilities
   - Consult Context7 for external library/framework usage
   - Identify canonical patterns to follow
   - WRITING CODE WITHOUT FIRST USING MCP Grep (and Context7 when applicable) IS A BLOCKING VIOLATION

2. **SCOPE LOCK** (MANDATORY)
   - State exact files/modules in scope
   - Anything outside scope is forbidden unless explicitly approved
   - Preserve public APIs unless explicitly authorised

3. **SCAFFOLD BEFORE IMPLEMENT** (MANDATORY)
   - Create/adapt minimal required structure consistent with repo
   - Align naming, imports, interfaces, and directory layout to existing patterns
   - Ensure async structure is correct (for FastAPI)

4. **ZERO TOLERANCE** (ABSOLUTE)
   - 0 TODOs, mocks, stubs, "PASS" passes, hacks, placeholders, partial implementations, workarounds
   - ALL incomplete code MUST BE FOUND AND ERADICATED
   - Production code MUST be implemented 100% correctly

5. **PRODUCTION CODE MANDATE** (ABSOLUTE)
   - ALL production code MUST be implemented 100% correctly, to highest standards
   - 0 errors, 0 warnings, 0 issues
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
   - Create/adapt minimal required structure consistent with repo
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
- [ ] Review structured checklists to locate current/next plan
- [ ] Copy and adapt acquired content to production codebase
- [ ] Execute implementation sequence (32 steps)
- [ ] Perform code quality checks
- [ ] Validate plan success
- [ ] Update progress in CODE_IMPLEMENTATION_SPEC
- [ ] Iterate through all plans until complete
- [ ] Complete validation checkpoints

### Phase: [Current Phase Name]

**Status**: 🟡 In Progress

**Actions Completed**:

- [ ] Codebase examination and gap analysis complete
- [ ] Search and discovery phase complete (MCP Grep + MCP Fetch)
- [ ] Repository cloning complete
- [ ] Structured checklists reviewed and current/next plan located
- [ ] Copy-and-adapt operations complete
- [ ] Scope locked
- [ ] Pre-flight violation scan complete
- [ ] Scaffolding complete
- [ ] Group-based implementation complete
- [ ] Implementation complete
- [ ] Code quality checks performed and passed
- [ ] Plan validation complete
- [ ] Validation complete
- [ ] Zero-tolerance verification complete
- [ ] Progress updated in CODE_IMPLEMENTATION_SPEC
- [ ] Structured checklists updated
- [ ] All plans iterated through and completed

**Actions Pending**:

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
