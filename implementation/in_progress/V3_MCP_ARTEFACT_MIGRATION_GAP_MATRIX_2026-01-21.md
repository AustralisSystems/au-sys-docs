# v3 MCP Artefact Migration Gap Matrix (v2 -> v3)

Date: 2026-01-21
Scope: `docs/implementation/instructions/v2/` -> `docs/implementation/instructions/v3/`

This document is a gap-oriented companion to:

- `docs/implementation/in_progress/V3_MCP_ARTEFACT_MIGRATION_REVIEW_2026-01-21.md`

Goal: provide a quick “v2 mandate/concept -> v3 canonical location or missing” matrix.

No v3 artefacts were edited as part of this work; this is analysis-only.

## How To Read This Matrix

- **Category**: a governance mandate or operational concept that appears throughout v2.
- **v2 coverage**: rough indicator that the concept appears across many v2 artefacts.
- **v3 canonical coverage**: whether the concept appears in canonical v3 (non-archive) artefacts.
- **v3 archive-only**: whether the concept exists only in `docs/implementation/instructions/v3/_archive/` snapshots.
- **Status**: `covered`, `partial`, or `missing` from canonical v3.
- **Recommendation**: action to make the canonical v3 set self-contained and understandable to a new agent.

Notes:

- “Coverage” here is keyword-driven and then sanity-checked against the earlier qualitative review. It is meant to find likely gaps quickly, not replace human judgement.

## Mandate / Concept Matrix

### 1) Python minimum version requirement (Python 3.12+)

- v2 coverage: high (found in many v2 doctrine/protocol/instruction artefacts)
- v3 canonical coverage: none detected
- v3 archive-only: present in many archive snapshots
- Status: missing (canonical v3)

Canonical v3 locations:

- None identified.

Archive/reference locations:

- `docs/implementation/instructions/v3/_archive/000-DOCTRINE-Enterprise_Canonical_Execution-v2.0.1.yaml`
- `docs/implementation/instructions/v3/_archive/001-PROTOCOL-The_GoldenRule_Execution-v2.0.1.yaml`
- `docs/implementation/instructions/v3/_archive/002-PROTOCOL-Zero_Tolerance_Remediation-v2.0.0.yaml`
- `docs/implementation/instructions/v3/_archive/003-PROTOCOL-FastAPI_Pure_Code_Implementation-v2.0.0.yaml`
- `docs/implementation/instructions/v3/_archive/004-PROTOCOL-Validate_Remediate_Codebase-v2.0.0.yaml`
- `docs/implementation/instructions/v3/_archive/104-INSTRUCTIONS-Execute_Implementation_Phase_Tasks-v2.0.0.yaml`

Recommendation:

- If still enforceable governance, add a dedicated v3 protocol (or doctrine policy) defining minimum Python version and how it is validated.

### 2) Universal container deployability mandate (OCI compliant; Docker/Podman/Kubernetes parity)

- v2 coverage: high
- v3 canonical coverage: none detected
- v3 archive-only: present
- Status: missing (canonical v3)

Canonical v3 locations:

- None identified.

Archive/reference locations:

- Same cluster as above, commonly embedded inside the v2 narrative snapshots under `_archive/`.

Recommendation:

- If still enforceable, migrate to a v3 protocol (e.g. `deployment.universal_container_compatibility`) and reference it from `enterprise.canonical_execution`.

### 3) Security frameworks mandate (NIST/ISO/OWASP + AI security)

- v2 coverage: high
- v3 canonical coverage: partial
- v3 archive-only: present
- Status: partial (canonical v3)

Canonical v3 locations (observed keywords):

- `docs/implementation/instructions/v3/protocols/production_code_quality.yaml` (mentions security scanning expectations)
- `docs/implementation/instructions/v3/protocols/real_resources_only.yaml` (mentions security posture; details reduced)
- `docs/implementation/instructions/v3/protocols/prime_strategic_orchestration.yaml` (mentions security context)

What appears missing vs v2:

- Explicit “highest maturity” mandate language.
- Explicit named framework compliance statements (NIST CSF maturity, ISO 27001, OWASP Top 10/ASVS, AI security frameworks) as enforceable rules.

Recommendation:

- If these are still mandatory, encode them as explicit directives in a v3 security protocol (or doctrine policy) rather than scattered mentions.

### 4) Dependency management mandate (latest stable, vulnerability remediation)

- v2 coverage: high
- v3 canonical coverage: none detected
- v3 archive-only: present
- Status: missing (canonical v3)

Canonical v3 locations:

- None identified.

Recommendation:

- If still enforceable, define a v3 protocol (e.g. `deps.dependency_management`) with clear rules and evidence requirements.

### 5) Incomplete code eradication (TODO/stub/mock/placeholder/pass)

- v2 coverage: high
- v3 canonical coverage: partial
- v3 archive-only: present
- Status: partial (canonical v3)

Canonical v3 locations:

- `docs/implementation/instructions/v3/protocols/zero_tolerance_remediation.yaml` (core rule exists but is very condensed)
- `docs/implementation/instructions/v3/prompts/003-incomplete-code-eradication-scan.yaml` (pattern defaults exist but are incomplete)
- `docs/implementation/instructions/v3/instructions/validate_code_quality_and_compliance.yaml` (mentions scanning conceptually)

Missing vs v2:

- The full marker list and classification rules.
- Scan timing rules (pre-flight, post-change re-scan) and explicit stop/plan mechanics.

Recommendation:

- Expand canonical v3 protocol to include patterns + scan timing + scope rules (or add a separate scan protocol referenced by the remediation protocol).

### 6) AST + SAST mandatory validation

- v2 coverage: medium-high
- v3 canonical coverage: partial
- v3 archive-only: present
- Status: partial (canonical v3)

Canonical v3 locations:

- `docs/implementation/instructions/v3/protocols/production_code_quality.yaml` includes an explicit AST/SAST directive.

Common missing vs v2:

- Explicit tooling expectations, severity thresholds, scope rules, and evidence format.

Recommendation:

- Keep the current directive, but add structured `validation_gates[]` (or a reference to canonical command sets per language/repo).

### 7) Real HTTP API validation (no in-process TestClient)

- v2 coverage: medium
- v3 canonical coverage: covered
- v3 archive-only: present
- Status: covered (canonical v3)

Canonical v3 locations:

- `docs/implementation/instructions/v3/protocols/api_real_http.yaml`
- Supporting instructions: `docs/implementation/instructions/v3/instructions/run_locally_and_test_api_webui.yaml`, `docs/implementation/instructions/v3/instructions/build_deploy_test_and_document_rest_api.yaml`

Remaining differences vs v2:

- v2 had more explicit “100% endpoints+methods” coverage requirements and reconciliation rules.

Recommendation:

- Tighten coverage requirements and define reconciliation failure behavior (inventory mismatch -> stop).

### 8) Real resources only (no fake infra)

- v2 coverage: low-medium
- v3 canonical coverage: covered
- v3 archive-only: present
- Status: covered (canonical v3)

Canonical v3 locations:

- `docs/implementation/instructions/v3/protocols/real_resources_only.yaml`

Remaining differences vs v2:

- v2 included strict artefact naming (inventories/reports), negative testing requirements, and restart semantics.

Recommendation:

- Add a small “required artefacts” list and negative testing directive if those behaviors are still mandatory.

### 9) Output discipline (no narration; evidence-first)

- v2 coverage: medium
- v3 canonical coverage: partial
- v3 archive-only: present
- Status: partial (canonical v3)

Canonical v3 locations:

- `docs/implementation/instructions/v3/doctrines/enterprise_canonical_execution.yaml` (concise output policy)
- `docs/implementation/instructions/v3/protocols/golden_rule_execution.yaml` and `docs/implementation/instructions/v3/protocols/validate_remediate_codebase.yaml` (evidence requirements)

Missing vs v2:

- v2 had strict output section templates for multiple instructions.

Recommendation:

- Add an instruction-level `output_contract` mechanism (similar to prompts).

### 10) Halt gating / operator-controlled continuation

- v2 coverage: medium
- v3 canonical coverage: high
- v3 archive-only: present
- Status: covered (canonical v3)

Canonical v3 locations:

- Many v3 instructions and prompts set `halt: true` explicitly.

Recommendation:

- Ensure the runtime/orchestrator semantics treat `halt: true` consistently (hard stop).

## File-Level Gap Hotspots (Most Condensed vs v2)

These are canonical v3 artefacts where completeness vs v2 was assessed as a gap or high-risk partial:

- `docs/implementation/instructions/v3/doctrines/enterprise_canonical_execution.yaml`
- `docs/implementation/instructions/v3/protocols/golden_rule_execution.yaml`
- `docs/implementation/instructions/v3/protocols/zero_tolerance_remediation.yaml`
- `docs/implementation/instructions/v3/protocols/fastapi_pure_code_implementation.yaml`
- `docs/implementation/instructions/v3/protocols/validate_remediate_codebase.yaml`
- `docs/implementation/instructions/v3/protocols/rfc2119_requirements_language.yaml`
- `docs/implementation/instructions/v3/protocols/digital_assistant_roles.yaml`
- `docs/implementation/instructions/v3/instructions/validate_code_quality_and_compliance.yaml`
- `docs/implementation/instructions/v3/instructions/remediate_and_refactor_codebase.yaml`
- `docs/implementation/instructions/v3/instructions/pure_code_implementation_execution.yaml`
- `docs/implementation/instructions/v3/instructions/fastapi_design_implementation_refactor.yaml`
- `docs/implementation/instructions/v3/prompts/jsx_to_fastapi_jinja2_template_library.yaml`

## Recommendations (Action Plan)

1) Decide whether the missing v2 mandates are still enforceable.
   - If yes: migrate into canonical v3 doctrine/protocol set (not `_archive/`).
   - If no: document the deprecation explicitly in a v3 doctrine/policy.

2) Add structured “evidence contracts” for instructions.

3) Evolve instruction schemas to structured inputs/outputs.

4) Add structured traceability mapping (migrated vs dropped vs relocated).

5) Clean up legacy examples that live under v3 but reference v2 IDs.
   - `docs/implementation/instructions/v3/examples/runbook_code_implementation_session.yaml`
   - `docs/implementation/instructions/v3/schemas/examples/prompt.code-review.yaml`
