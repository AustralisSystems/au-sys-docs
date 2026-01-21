# v3 MCP Artefact Migration Review (v2 -> v3)

Date: 2026-01-21
Scope: `docs/implementation/instructions/v2/` -> `docs/implementation/instructions/v3/`

This document captures a review of the v2-to-v3 MCP YAML artefact migration, with a focus on:

- intent preservation
- instruction/directive quality
- cohesiveness
- completeness (vs v2)
- understandability for a fresh LLM
- action-ability

No files were modified as part of this review (this is analysis-only).

## Validation Results

- Canonical v3 validator:
  - Command: `python tooling/au-sys-tools/tools/validate_v3_mcp_artifacts.py --root "docs/implementation/instructions/v3"`
  - Result: `Validated 61 file(s): 61 ok, 0 failed`

Notes:

- There are 81 YAML files under `docs/implementation/instructions/v3/`.
- 20 are under `docs/implementation/instructions/v3/_archive/` and are legacy snapshots; several are not single-document YAML and/or do not parse cleanly under PyYAML.
- The validator appears to validate the 61 non-archive artefacts only.

## Artefact Inventory

### Canonical (non-archive) v3 YAML files (61)

- `docs/implementation/instructions/v3/catalogue.yaml`
- `docs/implementation/instructions/v3/doctrines/doctrine-registry.yaml`
- `docs/implementation/instructions/v3/doctrines/enterprise_canonical_execution.yaml`
- `docs/implementation/instructions/v3/doctrines/prime_strategic_command.yaml`
- `docs/implementation/instructions/v3/examples/runbook_code_implementation_session.yaml`
- `docs/implementation/instructions/v3/examples/runbook_v3_implementation_session.yaml`
- `docs/implementation/instructions/v3/instructions/agent_task_coordination_session.yaml`
- `docs/implementation/instructions/v3/instructions/build_deploy_test_and_document_rest_api.yaml`
- `docs/implementation/instructions/v3/instructions/code_documentation_session.yaml`
- `docs/implementation/instructions/v3/instructions/debug_and_troubleshoot_codebase.yaml`
- `docs/implementation/instructions/v3/instructions/diataxis_documentation_framework_session.yaml`
- `docs/implementation/instructions/v3/instructions/draft_code_documentation.yaml`
- `docs/implementation/instructions/v3/instructions/draft_diataxis_explanation.yaml`
- `docs/implementation/instructions/v3/instructions/draft_diataxis_howto.yaml`
- `docs/implementation/instructions/v3/instructions/draft_diataxis_reference.yaml`
- `docs/implementation/instructions/v3/instructions/draft_diataxis_tutorial.yaml`
- `docs/implementation/instructions/v3/instructions/draft_high_level_architecture.yaml`
- `docs/implementation/instructions/v3/instructions/draft_technical_design.yaml`
- `docs/implementation/instructions/v3/instructions/enterprise_architecture_documentation_session.yaml`
- `docs/implementation/instructions/v3/instructions/execute_implementation_phase_tasks.yaml`
- `docs/implementation/instructions/v3/instructions/fastapi_design_implementation_refactor.yaml`
- `docs/implementation/instructions/v3/instructions/implementation_session.yaml`
- `docs/implementation/instructions/v3/instructions/instruction-registry.yaml`
- `docs/implementation/instructions/v3/instructions/live_debugging_and_remediation.yaml`
- `docs/implementation/instructions/v3/instructions/prime_strategic_orchestration_session.yaml`
- `docs/implementation/instructions/v3/instructions/pure_code_implementation_execution.yaml`
- `docs/implementation/instructions/v3/instructions/remediate_and_refactor_codebase.yaml`
- `docs/implementation/instructions/v3/instructions/review_documentation.yaml`
- `docs/implementation/instructions/v3/instructions/run_locally_and_test_api_webui.yaml`
- `docs/implementation/instructions/v3/instructions/scaffolding_prioritization_comparative_selection.yaml`
- `docs/implementation/instructions/v3/instructions/swarm_orchestrator_session.yaml`
- `docs/implementation/instructions/v3/instructions/validate_code_quality_and_compliance.yaml`
- `docs/implementation/instructions/v3/prompts/001-read-fastapi-platform-and-halt.yaml`
- `docs/implementation/instructions/v3/prompts/002-create-code-implementation-spec.yaml`
- `docs/implementation/instructions/v3/prompts/003-incomplete-code-eradication-scan.yaml`
- `docs/implementation/instructions/v3/prompts/004-discover-and-clone-reference-repos.yaml`
- `docs/implementation/instructions/v3/prompts/005-execute-treatment-plan-copy-and-adapt.yaml`
- `docs/implementation/instructions/v3/prompts/handover_doc_create.yaml`
- `docs/implementation/instructions/v3/prompts/handover_doc_update.yaml`
- `docs/implementation/instructions/v3/prompts/jsx_to_fastapi_jinja2_template_library.yaml`
- `docs/implementation/instructions/v3/prompts/prompt-registry.yaml`
- `docs/implementation/instructions/v3/protocols/agent_task_coordination.yaml`
- `docs/implementation/instructions/v3/protocols/api_real_http.yaml`
- `docs/implementation/instructions/v3/protocols/code_documentation.yaml`
- `docs/implementation/instructions/v3/protocols/diataxis_documentation_framework.yaml`
- `docs/implementation/instructions/v3/protocols/digital_assistant_roles.yaml`
- `docs/implementation/instructions/v3/protocols/enterprise_architecture_documentation.yaml`
- `docs/implementation/instructions/v3/protocols/fastapi_pure_code_implementation.yaml`
- `docs/implementation/instructions/v3/protocols/golden_rule_execution.yaml`
- `docs/implementation/instructions/v3/protocols/mcp_tools_workflow.yaml`
- `docs/implementation/instructions/v3/protocols/prime_strategic_orchestration.yaml`
- `docs/implementation/instructions/v3/protocols/production_code_quality.yaml`
- `docs/implementation/instructions/v3/protocols/protocol-registry.yaml`
- `docs/implementation/instructions/v3/protocols/real_resources_only.yaml`
- `docs/implementation/instructions/v3/protocols/rfc2119_requirements_language.yaml`
- `docs/implementation/instructions/v3/protocols/swarm_orchestrator.yaml`
- `docs/implementation/instructions/v3/protocols/test_implementation.yaml`
- `docs/implementation/instructions/v3/protocols/validate_remediate_codebase.yaml`
- `docs/implementation/instructions/v3/protocols/validation_suite_architecture.yaml`
- `docs/implementation/instructions/v3/protocols/zero_tolerance_remediation.yaml`
- `docs/implementation/instructions/v3/schemas/examples/prompt.code-review.yaml`

### Archive (legacy/reference) v3 YAML files (20)

These are not canonical v3 single-doc MCP artefacts.

- `docs/implementation/instructions/v3/_archive/00-Enterprise_Canonical_Execution_DOCTRINE_v2.0.0.yaml`
- `docs/implementation/instructions/v3/_archive/000-DOCTRINE-Enterprise_Canonical_Execution-v2.0.1.yaml`
- `docs/implementation/instructions/v3/_archive/000-DOCTRINE-Enterprise_Canonical_Execution.yaml`
- `docs/implementation/instructions/v3/_archive/001-PROTOCOL-The_GoldenRule_Execution-v2.0.1.yaml`
- `docs/implementation/instructions/v3/_archive/002-PROTOCOL-Zero_Tolerance_Remediation-v2.0.0.yaml`
- `docs/implementation/instructions/v3/_archive/003-PROTOCOL-FastAPI_Pure_Code_Implementation-v2.0.0.yaml`
- `docs/implementation/instructions/v3/_archive/004-PROTOCOL-Validate_Remediate_Codebase-v2.0.0.yaml`
- `docs/implementation/instructions/v3/_archive/104-INSTRUCTIONS-Execute_Implementation_Phase_Tasks-v2.0.0.yaml`
- `docs/implementation/instructions/v3/_archive/105-INSTRUCTIONS-Run_Locally_and_Test_API_WebUI-v2.0.0.yaml`
- `docs/implementation/instructions/v3/_archive/106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance-v2.0.0.yaml`
- `docs/implementation/instructions/v3/_archive/107-INSTRUCTIONS-Remediate_And_Refactor_Codebase-v2.0.0.yaml`
- `docs/implementation/instructions/v3/_archive/108-INSTRUCTIONS-Debug_And_Troubleshoot_Codebase-v2.0.0.yaml`
- `docs/implementation/instructions/v3/_archive/110-INSTRUCTIONS-Build_Deploy_Test_and_Document_REST_API-v2.0.0.yaml`
- `docs/implementation/instructions/v3/_archive/202-INSTRUCTIONS-Pure_Code_Implementation_Execution_Protocol-v2.0.0.yaml`
- `docs/implementation/instructions/v3/_archive/203-INSTRUCTIONS-FastAPI_Design_Implementation_Refactor-v2.0.0.yaml`
- `docs/implementation/instructions/v3/_archive/204-INSTRUCTIONS-Live-Debugging-and-Remedation-v2.0.0.yaml`
- `docs/implementation/instructions/v3/_archive/handover-doc-creation.yaml`
- `docs/implementation/instructions/v3/_archive/handover-doc-update.yaml`
- `docs/implementation/instructions/v3/_archive/jsx_to_fastapi_jinja2_template_library_prompt.yaml`
- `docs/implementation/instructions/v3/_archive/prompts-index_legacy_20260121.yaml`

## Review Method

- For artefacts with `artifact.traceability.raw_ref`, compare the v3 content to the referenced v2 YAML.
- Rate each file on:
  - intent
  - instructions/directives quality
  - cohesiveness
  - completeness (vs v2)
  - understandability
  - action-ability

Ratings use `pass`, `partial`, `gap` (or `n/a` when no v2 mapping exists).

## Critical Cross-Cutting Gaps

### 1) Large v2 mandates appear to be missing from canonical v3 governance

Several mandates that were explicit and enforceable in v2 are only found in legacy content (v2 sources and/or v3 `_archive/`), but are not clearly represented in canonical v3 doctrine/protocols:

- Python minimum version (v2: Python 3.12+ requirement)
- Universal container deployability mandate (OCI compliance, Docker/Podman/Kubernetes parity)
- Cybersecurity/AI security frameworks mandate (NIST CSF, ISO 27001, OWASP, etc.)
- Dependency management mandate (“latest stable versions immediately”, vulnerability remediation)

Risk:

- A new LLM reading canonical v3 doctrine/protocols may not infer these as required, leading to inconsistent behavior vs v2 governance.

Recommendation:

- If these mandates are still intended to be active governance, migrate them into canonical v3 doctrine/protocol(s) explicitly (or create dedicated v3 protocols referenced by `enterprise.canonical_execution`).

### 2) Evidence and output formats are not standardized for v3 instructions

Many v3 instructions mention evidence (e.g., `validation_evidence`, `verification_evidence`) but do not define:

- minimum structure (command, exit code, output excerpt)
- what constitutes pass/fail
- where evidence is recorded (spec vs console output)

Risk:

- Two agents can claim compliance with different interpretations.

Recommendation:

- Add a standardized “evidence contract” concept to v3 instruction schema/content (similar to prompt `output_contract`).

### 3) `inputs`/`outputs` are bare strings

Most v3 instructions define `inputs` and `outputs` as arrays of strings.

Risk:

- Not self-describing; low actionability for a fresh agent.

Recommendation:

- Evolve schemas to support structured inputs/outputs:
  - name
  - type
  - required
  - description
  - example

### 4) Overlapping/ambiguous instruction boundaries

There is overlap between:

- `debug.troubleshoot_codebase`
- `debug.live_debugging_and_remediation`

Risk:

- Different teams may choose different instruction, producing inconsistent workflows.

Recommendation:

- Add explicit “use when / do not use when” framing or add a `session_type` field.

### 5) Traceability is present, but “mandate mapping” is missing

Even when `raw_ref` is provided, it does not identify:

- what was migrated
- what was intentionally dropped
- where dropped content moved to (if anywhere)

Recommendation:

- Extend `traceability` with structured fields like:
  - `migrated_sections[]`
  - `dropped_sections[]`
  - `relocated_to[]`

## Per-File Checklist (Canonical v3)

Format:

- File path
  - v2 source (if any)
  - Ratings: intent / instructions / cohesiveness / completeness / understandability / actionability
  - Improvements

### Doctrines

- `docs/implementation/instructions/v3/doctrines/enterprise_canonical_execution.yaml`
  - v2: `repo://docs/implementation/instructions/v2/000-DOCTRINE-Enterprise_Canonical_Execution-v2.0.1.yaml`
  - Ratings: pass / partial / pass / gap / pass / partial
  - Improvements:
    - Content: explicitly include/relocate v2 hard mandates (Python/container/security/deps) if still intended.
    - Schema/content: add a mandate mapping (what moved where).

- `docs/implementation/instructions/v3/doctrines/prime_strategic_command.yaml`
  - v2: `repo://docs/implementation/instructions/v2/000-DOCTRINE-PRIME_Strategic_Command-v1.0.0.yaml`
  - Ratings: pass / pass / pass / partial / pass / partial
  - Improvements:
    - Content: add pointers to canonical orchestrator catalogue/tool docs.

### Protocols

- `docs/implementation/instructions/v3/protocols/golden_rule_execution.yaml`
  - v2: `repo://docs/implementation/instructions/v2/001-PROTOCOL-The_GoldenRule_Execution-v2.0.1.yaml`
  - Ratings: pass / partial / pass / gap / pass / partial
  - Improvements: restore minimal workflow + evidence contract; consider a protocol-level output contract.

- `docs/implementation/instructions/v3/protocols/zero_tolerance_remediation.yaml`
  - v2: `repo://docs/implementation/instructions/v2/002-PROTOCOL-Zero_Tolerance_Remediation-v2.0.0.yaml`
  - Ratings: pass / partial / partial / gap / pass / partial
  - Improvements: add scan schedule + pattern lists + scope rules.

- `docs/implementation/instructions/v3/protocols/fastapi_pure_code_implementation.yaml`
  - v2: `repo://docs/implementation/instructions/v2/003-PROTOCOL-FastAPI_Pure_Code_Implementation-v2.0.0.yaml`
  - Ratings: pass / pass / pass / gap / pass / partial
  - Improvements: if still required, add FastAPI operational gates or point to where they moved.

- `docs/implementation/instructions/v3/protocols/validate_remediate_codebase.yaml`
  - v2: `repo://docs/implementation/instructions/v2/004-PROTOCOL-Validate_Remediate_Codebase-v2.0.0.yaml`
  - Ratings: pass / partial / pass / gap / pass / partial
  - Improvements: incorporate explicit AST/SAST requirements or require `quality.production_code_quality`.

- `docs/implementation/instructions/v3/protocols/production_code_quality.yaml`
  - v2: `repo://docs/implementation/instructions/v2/008-PROTOCOL-Production_Code_Quality-v1.0.0.yaml`
  - Ratings: pass / pass / pass / partial / pass / partial
  - Improvements: add minimum tool categories + suppression policy.

- `docs/implementation/instructions/v3/protocols/mcp_tools_workflow.yaml`
  - v2: `repo://docs/implementation/instructions/v2/007-PROTOCOL-MCP_Tools_Workflow-v1.0.0.yaml`
  - Ratings: pass / pass / pass / partial / pass / partial
  - Improvements: encode deterministic `workflow_steps[]`.

- `docs/implementation/instructions/v3/protocols/rfc2119_requirements_language.yaml`
  - v2: `repo://docs/implementation/instructions/v2/006-PROTOCOL-RFC2119_Requirements_Language-v1.0.0.yaml`
  - Ratings: pass / partial / pass / gap / pass / partial
  - Improvements: define FORBIDDEN/PROHIBITED semantics or ban them in v3.

- `docs/implementation/instructions/v3/protocols/digital_assistant_roles.yaml`
  - v2: `repo://docs/implementation/instructions/v2/005-PROTOCOL-Digital_Assistant_Roles-v1.0.0.yaml`
  - Ratings: pass / partial / partial / gap / pass / gap
  - Improvements: create a v3 role registry or add explicit pointer to the authoritative role list.

- `docs/implementation/instructions/v3/protocols/test_implementation.yaml`
  - v2: `repo://docs/implementation/instructions/v2/009-PROTOCOL-Test_Implementation-v1.0.0.yaml`
  - Ratings: pass / pass / pass / partial / pass / pass
  - Improvements: optionally restore v2 taxonomy/templates via references.

- `docs/implementation/instructions/v3/protocols/validation_suite_architecture.yaml`
  - v2: `repo://docs/implementation/instructions/v2/320-INSTRUCTIONS-Validation_Suite_Standard_Structure-v1.0.0.yaml`
  - Ratings: pass / pass / pass / partial / pass / partial
  - Improvements: link to v2 template code or embed minimal skeleton.

- `docs/implementation/instructions/v3/protocols/real_resources_only.yaml`
  - v2: `repo://docs/implementation/instructions/v2/321-INSTRUCTIONS-Validation_CORE_Services-v1.0.0.yaml`
  - Ratings: pass / pass / pass / partial / pass / partial
  - Improvements: restore explicit inventory/restart semantics if required.

- `docs/implementation/instructions/v3/protocols/api_real_http.yaml`
  - v2: `repo://docs/implementation/instructions/v2/322-INSTRUCTIONS-Validation_ADAPTER_API_REST_Web-v1.0.0.yaml`
  - Ratings: pass / pass / pass / partial / pass / partial
  - Improvements: add explicit 100% endpoints+methods requirement + reconciliation abort behavior.

- `docs/implementation/instructions/v3/protocols/prime_strategic_orchestration.yaml`
  - v2: `repo://docs/implementation/instructions/v2/010-PROTOCOL-PRIME_Strategic_Orchestration-v1.0.0.yaml`
  - Ratings: pass / pass / pass / partial / pass / pass
  - Improvements: add pointer to canonical orchestrator catalogue/model selection rules.

- `docs/implementation/instructions/v3/protocols/swarm_orchestrator.yaml`
  - v2: `repo://docs/implementation/instructions/v2/011-PROTOCOL-Swarm_Orchestrator-v1.0.0.yaml`
  - Ratings: pass / pass / pass / partial / pass / pass
  - Improvements: add pointer to spawn templates/tooling.

- `docs/implementation/instructions/v3/protocols/agent_task_coordination.yaml`
  - v2: `repo://docs/implementation/instructions/v2/012-PROTOCOL-Agent_Task_Coordination-v1.0.0.yaml`
  - Ratings: pass / pass / pass / partial / pass / pass
  - Improvements: define report/status fields more rigidly.

- `docs/implementation/instructions/v3/protocols/code_documentation.yaml`
  - v2: `repo://docs/implementation/instructions/v2/912-PROTOCOL-Code_Documentation-v1.0.0.yaml`
  - Ratings: pass / pass / pass / partial / pass / pass
  - Improvements: add explicit template/path pointers.

- `docs/implementation/instructions/v3/protocols/diataxis_documentation_framework.yaml`
  - v2: `repo://docs/implementation/instructions/v2/911-PROTOCOL-Diataxis_Documentation_Framework-v1.0.0.yaml`
  - Ratings: pass / pass / pass / partial / pass / pass
  - Improvements: link to canonical templates and anti-patterns.

- `docs/implementation/instructions/v3/protocols/enterprise_architecture_documentation.yaml`
  - v2: `repo://docs/implementation/instructions/v2/913-PROTOCOL-Enterprise_Architecture_Documentation-v1.0.0.yaml`
  - Ratings: pass / pass / pass / partial / pass / pass
  - Improvements: list minimum required views + diagram format guidance.

### Instructions (execution/implementation)

- `docs/implementation/instructions/v3/instructions/execute_implementation_phase_tasks.yaml`
  - v2: `repo://docs/implementation/instructions/v2/104-INSTRUCTIONS-Execute_Implementation_Phase_Tasks-v2.0.0.yaml`
  - Ratings: pass / partial / pass / partial / pass / partial
  - Improvements: add minimum evidence contract; ensure dropped mandates are represented elsewhere.

- `docs/implementation/instructions/v3/instructions/run_locally_and_test_api_webui.yaml`
  - v2: `repo://docs/implementation/instructions/v2/105-INSTRUCTIONS-Run_Locally_and_Test_API_WebUI-v2.0.0.yaml`
  - Ratings: pass / partial / pass / partial / pass / partial
  - Improvements: define default scope + evidence expectations.

- `docs/implementation/instructions/v3/instructions/validate_code_quality_and_compliance.yaml`
  - v2: `repo://docs/implementation/instructions/v2/106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance-v2.0.0.yaml`
  - Ratings: pass / partial / pass / gap / pass / gap
  - Improvements: restore operational gates or encode them as structured `validation_gates[]`.

- `docs/implementation/instructions/v3/instructions/remediate_and_refactor_codebase.yaml`
  - v2: `repo://docs/implementation/instructions/v2/107-INSTRUCTIONS-Remediate_And_Refactor_Codebase-v2.0.0.yaml`
  - Ratings: pass / partial / pass / gap / pass / partial
  - Improvements: restore v2 consistency/reuse rules + entry/exit conditions.

- `docs/implementation/instructions/v3/instructions/debug_and_troubleshoot_codebase.yaml`
  - v2: `repo://docs/implementation/instructions/v2/108-INSTRUCTIONS-Debug_And_Troubleshoot_Codebase-v2.0.0.yaml`
  - Ratings: pass / partial / pass / partial / pass / partial
  - Improvements: add log discovery order + root-cause evidence format.

- `docs/implementation/instructions/v3/instructions/build_deploy_test_and_document_rest_api.yaml`
  - v2: `repo://docs/implementation/instructions/v2/110-INSTRUCTIONS-Build_Deploy_Test_and_Document_REST_API-v2.0.0.yaml`
  - Ratings: pass / partial / pass / partial / pass / partial
  - Improvements: standardized endpoint matrix + allowed/forbidden testing methods.

- `docs/implementation/instructions/v3/instructions/pure_code_implementation_execution.yaml`
  - v2: `repo://docs/implementation/instructions/v2/202-INSTRUCTIONS-Pure_Code_Implementation_Execution_Protocol-v2.0.0.yaml`
  - Ratings: pass / partial / pass / gap / pass / partial
  - Improvements: add conditional tool mandates (grep/context7) + output contract.

- `docs/implementation/instructions/v3/instructions/fastapi_design_implementation_refactor.yaml`
  - v2: `repo://docs/implementation/instructions/v2/203-INSTRUCTIONS-FastAPI_Design_Implementation_Refactor-v2.0.0.yaml`
  - Ratings: pass / partial / pass / gap / pass / gap
  - Improvements: restore concrete async/perf/reliability checklists.

- `docs/implementation/instructions/v3/instructions/live_debugging_and_remediation.yaml`
  - v2: `repo://docs/implementation/instructions/v2/204-INSTRUCTIONS-Live-Debugging-and-Remedation-v2.0.0.yaml`
  - Ratings: pass / pass / pass / partial / pass / partial
  - Improvements: disambiguate from other debug instruction; add minimal output contract.

- `docs/implementation/instructions/v3/instructions/scaffolding_prioritization_comparative_selection.yaml`
  - v2: `repo://docs/implementation/instructions/v2/205-INSTRUCTIONS-Scaffolding_Prioritization_Comparative_Selection-v2.0.0.yaml`
  - Ratings: pass / partial / pass / partial / pass / partial
  - Improvements: selection rubric + evidence requirements.

### Instructions (swarm/docs sessions)

- `docs/implementation/instructions/v3/instructions/agent_task_coordination_session.yaml`
  - v2: `repo://docs/implementation/instructions/v2/113-INSTRUCTIONS-Agent_Task_Coordination-v1.0.0.yaml`
  - Ratings: pass / partial / pass / gap / pass / partial

- `docs/implementation/instructions/v3/instructions/swarm_orchestrator_session.yaml`
  - v2: `repo://docs/implementation/instructions/v2/112-INSTRUCTIONS-Swarm_Orchestrator-v1.0.0.yaml`
  - Ratings: pass / pass / partial / partial / pass / pass

- `docs/implementation/instructions/v3/instructions/prime_strategic_orchestration_session.yaml`
  - v2: `repo://docs/implementation/instructions/v2/111-INSTRUCTIONS-PRIME_Strategic_Orchestration-v1.0.0.yaml`
  - Ratings: pass / pass / pass / gap / pass / pass

- `docs/implementation/instructions/v3/instructions/code_documentation_session.yaml`
  - v2: `repo://docs/implementation/instructions/v2/921-INSTRUCTIONS-Code_Documentation-v1.0.0.yaml`
  - Ratings: pass / partial / pass / gap / pass / partial

- `docs/implementation/instructions/v3/instructions/diataxis_documentation_framework_session.yaml`
  - v2: `repo://docs/implementation/instructions/v2/920-INSTRUCTIONS-Diataxis_Documentation_Framework-v1.0.0.yaml`
  - Ratings: pass / pass / pass / partial / pass / pass

- `docs/implementation/instructions/v3/instructions/enterprise_architecture_documentation_session.yaml`
  - v2: `repo://docs/implementation/instructions/v2/922-INSTRUCTIONS-Enterprise_Architecture_Documentation-v1.0.0.yaml`
  - Ratings: pass / partial / pass / gap / pass / partial

### Instructions (documentation drafting)

- `docs/implementation/instructions/v3/instructions/draft_diataxis_tutorial.yaml` (v2: `repo://docs/implementation/instructions/v2/924-INSTRUCTIONS-Draft_Diataxis_Tutorial-v1.0.0.yaml`)
  - Ratings: pass / pass / pass / partial / pass / pass

- `docs/implementation/instructions/v3/instructions/draft_diataxis_howto.yaml` (v2: `repo://docs/implementation/instructions/v2/925-INSTRUCTIONS-Draft_Diataxis_HowTo-v1.0.0.yaml`)
  - Ratings: pass / pass / pass / partial / pass / pass

- `docs/implementation/instructions/v3/instructions/draft_diataxis_reference.yaml` (v2: `repo://docs/implementation/instructions/v2/926-INSTRUCTIONS-Draft_Diataxis_Reference-v1.0.0.yaml`)
  - Ratings: pass / pass / pass / partial / pass / pass

- `docs/implementation/instructions/v3/instructions/draft_diataxis_explanation.yaml` (v2: `repo://docs/implementation/instructions/v2/927-INSTRUCTIONS-Draft_Diataxis_Explanation-v1.0.0.yaml`)
  - Ratings: pass / pass / pass / partial / pass / pass

- `docs/implementation/instructions/v3/instructions/draft_high_level_architecture.yaml` (v2: `repo://docs/implementation/instructions/v2/923-INSTRUCTIONS-Draft_High_Level_Architecture-v1.0.0.yaml`)
  - Ratings: pass / pass / pass / partial / pass / pass

- `docs/implementation/instructions/v3/instructions/draft_technical_design.yaml` (v2: `repo://docs/implementation/instructions/v2/928-INSTRUCTIONS-Draft_Technical_Design-v1.0.0.yaml`)
  - Ratings: pass / pass / pass / partial / pass / pass

- `docs/implementation/instructions/v3/instructions/draft_code_documentation.yaml` (v2: `repo://docs/implementation/instructions/v2/929-INSTRUCTIONS-Draft_Code_Documentation-v1.0.0.yaml`)
  - Ratings: pass / partial / pass / partial / pass / partial

- `docs/implementation/instructions/v3/instructions/review_documentation.yaml` (v2: `repo://docs/implementation/instructions/v2/930-INSTRUCTIONS-Review_Documentation-v1.0.0.yaml`)
  - Ratings: pass / pass / pass / partial / pass / pass

### Prompts

- `docs/implementation/instructions/v3/prompts/001-read-fastapi-platform-and-halt.yaml`
  - v2: `repo://docs/implementation/instructions/v2/prompts/001-read-fastapi-platform-and-halt.yaml`
  - Ratings: pass / pass / pass / pass / pass / pass
  - Improvements: reduce duplicated `traceability.raw`.

- `docs/implementation/instructions/v3/prompts/002-create-code-implementation-spec.yaml`
  - v2: `repo://docs/implementation/instructions/v2/prompts/002-create-code-implementation-spec.yaml`
  - Ratings: pass / pass / pass / partial / pass / pass

- `docs/implementation/instructions/v3/prompts/003-incomplete-code-eradication-scan.yaml`
  - v2: `repo://docs/implementation/instructions/v2/prompts/003-incomplete-code-eradication-scan.yaml`
  - Ratings: pass / pass / pass / partial / pass / partial

- `docs/implementation/instructions/v3/prompts/004-discover-and-clone-reference-repos.yaml`
  - v2: `repo://docs/implementation/instructions/v2/prompts/004-discover-and-clone-reference-repos.yaml`
  - Ratings: pass / partial / pass / partial / pass / partial

- `docs/implementation/instructions/v3/prompts/005-execute-treatment-plan-copy-and-adapt.yaml`
  - v2: `repo://docs/implementation/instructions/v2/prompts/005-execute-treatment-plan-copy-and-adapt.yaml`
  - Ratings: pass / partial / pass / partial / pass / partial

- `docs/implementation/instructions/v3/prompts/handover_doc_create.yaml`
  - v2: `repo://docs/implementation/instructions/v2/handover-doc-creation.yaml`
  - Ratings: pass / pass / pass / pass / pass / pass

- `docs/implementation/instructions/v3/prompts/handover_doc_update.yaml`
  - v2: `repo://docs/implementation/instructions/v2/handover-doc-update.yaml`
  - Ratings: pass / pass / pass / pass / pass / partial
  - Improvements: add required output sections.

- `docs/implementation/instructions/v3/prompts/jsx_to_fastapi_jinja2_template_library.yaml`
  - v2: `repo://docs/implementation/instructions/v2/jsx_to_fastapi_jinja2_template_library_prompt.yaml`
  - Ratings: pass / partial / pass / gap / pass / partial
  - Improvements: restore missing conversion rules + validation checklist + deliverables.

## Recommendations (Prioritized)

1) If still required, reintroduce the major v2 governance mandates into canonical v3 doctrine/protocol(s):
   - Python minimum version
   - universal container deployability
   - explicit security frameworks
   - dependency policy

2) Introduce standardized evidence and output contracts for instructions (and optionally protocols).

3) Evolve schemas to support structured `inputs`/`outputs` and structured evidence requirements.

4) Add structured traceability mapping (migrated vs dropped vs relocated), not just `raw_ref`.

5) Clean up legacy example ambiguity:
   - mark `docs/implementation/instructions/v3/examples/runbook_code_implementation_session.yaml` as legacy or relocate
   - update or label `docs/implementation/instructions/v3/schemas/examples/prompt.code-review.yaml` to use v3 doctrine IDs

## Appendix: Known Legacy/Archive Parsing Issues

The following archive YAMLs were observed (by inspection) to be non-canonical and/or not parseable as single-doc YAML:

- `docs/implementation/instructions/v3/_archive/002-PROTOCOL-Zero_Tolerance_Remediation-v2.0.0.yaml` (multiple YAML documents)
- `docs/implementation/instructions/v3/_archive/003-PROTOCOL-FastAPI_Pure_Code_Implementation-v2.0.0.yaml` (parse error)
- `docs/implementation/instructions/v3/_archive/004-PROTOCOL-Validate_Remediate_Codebase-v2.0.0.yaml` (parse error)
- `docs/implementation/instructions/v3/_archive/handover-doc-creation.yaml` (parse error)
- `docs/implementation/instructions/v3/_archive/handover-doc-update.yaml` (parse error)
