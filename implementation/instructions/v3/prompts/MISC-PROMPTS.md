# CODE IMPLEMENTATON REQUIREMENTS MANDATE

## IMPLEMENTATION MANDATE
THE CODE BASE MUST ADHERE TO THE GOLDEN RULES
THE CODE BASE MUST COMPLY WITH THE SOLID, DRY AND KISS PRINCIPLES

**IMPORTANT**
all TODOs, mocks, stubs and non production code... MUST BE REFACTORED INTO REAL CODE WITH REAL ACTIONS, BUSINESS LOGIC ETC.
THERE MUST BE 0 MOCKS, 0 TODOS, 0 STUB or FAKE CODE BLOCKS AND ALL CODE MUST BE PRODUCTION GRADE ON THE FIRST PASS EVEN WHEN ITS A FIRST CODE DRAFT ATTEMPT
THERE MUST BE 0 HARD CODED VALUES WHERE THE DATA SHOULD BE RETRIEVED FROM VALID SOURCES
THERE MUST BE 0 HARD CODED SETTINGS OR VALUES WHERE THE SETTINGS OR VALUE SHOULD BE USER configurable or are dynamic or modular or variable in the nature of the setting and SHOULD BE SET IN THE DB or CONFIG files (not in the code).
THERE MUST BE 0 MOCKS, 0 TODOS, 0 STUB or FAKE CODE BLOCKS

Ensure you seek out and eradicate all HARD coded values, THIS IS IN DIRECT VIOLATION OF THE GOLDEN RULES.
All Data MUST be retrieved from valid sources AND NEVER HARD CODED, EVEN WHEN ITS A FIRST CODE DRAFT ATTEMPT....
ALL CODE MUST BE ENTERPRISE PRODUCTION GRADE ON THE FIRST PASS
All content, files, modules, services, routers, BASCIALLY ANY CODE BLOCK AND ALL CODE MUST BE ENTERPRISE PRODUCTION GRADE ON THE FIRST PASS EVEN WHEN ITS A FIRST CODE DRAFT ATTEMPT.

## IMPLEMENTATION DIRECTIVES

  Workflow:
    1. Obey canonical and golden rule protocols.
    2. Review the SPEC DOCs.
    4. Follow 04-Execute_Implementation_Phase_Tasks.yaml.
    5. Implement, Lint, Typecheck and Fix the code.
    6. Perform all production-readiness code quality, remediation & refactoring steps.
    7. Validate all refactored code against:
       - Backend-first mandate,
       - OpenAPI spec,
       - Golden Rules,
       - Enterprise Canonical Standards,
       - All SPECs above.
    8. Build and deploy the app to the local docker desktop instance.
    9. Review the docker container logs to ensure there are 0 errors, 0 warnings, and 0 issues.
    10. Iteratively remediate and refactor the code until the container builds and deploys and has 0 errors, 0 warnings, and 0 issues.

  **IMPORTANT**
  You MUST iterate through the workflow steps above UNTIL the Phases, Tasks, Actions, and Steps are completed.

  All implementation actions MUST:
  - Produce **REAL**, functional, enterprise production-grade code paths,
  - Replace every mock/stub/todo with actual systems,
  - Remove ALL hard-coded values,
  - Guarantee that everything is modular, dynamic, decoupled, and aligned with backend OpenAPI spec.

  **REMEMBER**
  THERE MUST BE 0 MOCKS, 0 TODOS, 0 STUB or FAKE CODE BLOCKS AND ALL CODE MUST BE ENTERPRISE PRODUCTION GRADE ON THE FIRST PASS EVEN WHEN ITS A FIRST CODE DRAFT ATTEMPT
  THERE MUST BE 0 HARD CODED VALUES WHERE THE DATA SHOULD BE RETRIEVED FROM VALID SOURCES
  THERE MUST BE 0 HARD CODED SETTINGS OR VALUES WHERE THE SETTINGS OR VALUE SHOULD BE USER configurable or are dynamic or modular or variable in the nature of the setting and SHOULD BE SET IN THE DB or CONFIG files (not in the code).

  **IMPORTANT**
  Non-compliance is NOT permitted under the Golden Rule Execution Protocol.
  YOU MUST ENSURE the files and code created for this SPEC are COMPLIANT &  Golden Rule Protocol COMPLIANT

## INSTRUCTIONS
  CONTINUE WITH THE IMPLEMENTATION OF THE ROUTER FACTORY 2.0, follow the **INSTRUCTIONS** AND **WORKFLOW**.

  Instructions:
    1. CONTINUE WITH THE IMPLEMENTATION OF THE ROUTER FACTORY 2.0 AS PER THE SPEC DOCs.
    2. IMPLMENT and complete all the Phases, Tasks, Actions and Steps as defined in the ROUTER FACTORY 2.0 SPEC DOCs.
    3. Check the Implementation plan for any and all outstanding items related to the ROUTER FACTORY, then execute them as per the related in_progress SPEC docs if required to support the implementation of the ROUTER FACTORY 2.0

**CONTINUE WITH THE IMPLEMENTATION OF THE ROUTER FACTORY 2.0, follow the INSTRUCTIONS AND WORKFLOW**


#########################################################



## enterprise-grade full stack expert

[CONTEXT]
You are an enterprise-grade full stack implementation expert with 20+ years of designing and engineering Enterprise Production Grade. You are responsible for completing the migration of the codebase to the Router Factory 2.0 patterns according to all SPEC DOCs, open tasks, and canonical enterprise standards.
The Router Factory and code base must be production-ready on the first pass, with zero mocks, zero stubs, zero TODOs, zero hard-coded values, and full adherence to SOLID, DRY, and KISS principles.

[PRIMARY OBJECTIVE]

Implement the complete the migration of the codebase to the Router Factory 2.0 patterns according to all SPEC DOCs, open tasks, and canonical enterprise standards, following the Implementation Workflow, Canonical Standards, Golden Rules, and SPEC DOCs, delivering REAL, fully operational production code with 0 warnings, 0 errors, 0 placeholders, 0 hard-coded values, and 100% backend-first compliance.




#########################################################


### 11-Manual_API_Endpoint_Regression_Testing.yaml  ###

Execute ./docs/implementation/instructions/11-Manual_API_Endpoint_Regression_Testing.yaml under those enforced rules.

**IMPORTANT**
YOU MUST follow this methodology:
1.	get the latest openapi spec json from the apps and container services
2.	Update the existing or Create a SPEC for the regression testing and list of endpoints, then group them by function.
3.	auth to the app and have it available for all rest api commands
4.	Select one of the untested endpoint groups
5.	begin the regression testing
6.	document your test results as you progress
7.	resolve all issues that you find during the testing
complete the regression testing for the endpoint group

Select one of the untested endpoint groups and continue testing using the same instructions and methodology


#########################################################


**CONTINUE**
Continue with the next steps,
Ensure there are 0 errors, 0 warnings, and 0 issues.
Check the docker container logs to ensure the app and all containers have 0 errors, 0 warnings, and 0 issues.
resolve all known issues, remediate and apply all fixes.

Now continue, select one of the untested endpoint groups and continue testing using the same instructions and methodology


#########################################################


### 12-Manual_WebUI_Regression_Testing.yaml ###

Execute ./docs/implementation/instructions/12-Manual_WebUI_Regression_Testing.yaml under those enforced rules.

**IMPORTANT**
YOU MUST follow this methodology:
1.	get the latest openapi spec json from the apps and container services
2.	Update the existing or Create a SPEC for the regression testing and list of endpoints, then group them by function.
3.	auth to the app and have it available for all rest api commands
4.	Select one of the untested endpoint groups
5.	begin the regression testing
6.	document your test results as you progress
7.	resolve all issues that you find during the testing
8.	complete the regression testing for the endpoint group


Select one of the untested endpoint groups and continue testing using the same instructions and methodology


#########################################################


**CONTINUE**
Continue with the next steps,
Ensure there are 0 errors, 0 warnings, and 0 issues.
Check the docker container logs to ensure the app and all containers have 0 errors, 0 warnings, and 0 issues.
resolve all known issues, remediate and apply all fixes.
**REMEMBER** when you make changes to the codebase, run "docker compose -f docker-compose.standalone.yml up -d --build --remove-orphans && date" to rebuild the container to pick up the changes, then retest to ensure there are 0 errors, 0 warnings, and 0 issues.

Now continue, select one of the untested endpoint groups and continue testing using the same instructions and methodology


#########################################################



ABSOLUTE ZERO TOLERANCE REQUIREMENTS

You MUST ensure:

- **0 TODOs**
- **0 mocks**
- **0 stub code blocks**
- **0 placeholder/demo data**
- **0 hard-coded values for anything that is dynamic by nature**
- **0 hard-coded settings that should be stored in the database**
- **0 fixed content where real data must be retrieved from valid backend sources**
- **0 business logic in templates**
- **0 duplicated logic**
- **0 violations of SOLID/DRY/KISS**
- **0 deviations from the Golden Rules**

If a TODO, mock, or stub exists ANYWHERE, it MUST be refactored into:

- **real, production-ready code**,
- **real CRUD endpoints**,
- **real services**,
- **real data retrieval flows**,
- **real configuration mechanisms**,
- **backed by actual OpenAPI-defined backend functionality**.

All refactoring MUST follow:
- Backend-first development,
- OpenAPI-first alignment,
- Strict naming synchronization between backend and frontend,
- Dynamic data retrieval (NO static content),
- And all rules defined in the Enterprise Canonical Execution Protocol.

Enterprise Canonical Execution Protocols
- ./docs/implementation/instructions/00-Enterprise_Cannonical_Execution_Protocol.yaml
- ./docs/implementation/instructions/01-The_GoldenRule_Execution_Protocol.yaml


YOU MUST CONTINUE WITH THE NEXT STEPS...
YOU MUST CONTINUE WITH THE NEXT STEPS...
YOU MUST CONTINUE WITH THE NEXT STEPS...





#########################################################


NEW SPEC DOCUMENT(s) ###

#############################################################################################################################
#############################################################################################################################
#############################################################################################################################

System:
Load and obey the following implementation instruction files as the canonical execution framework for this task:
- ./docs/implementation/instructions/00-Enterprise_Cannonical_Execution_Protocol.yaml
- ./docs/implementation/instructions/01-The_GoldenRule_Execution_Protocol.yaml

These two documents define the ENTERPRISE CANONICAL EXECUTION PROTOCOL and THE GOLDEN RULE EXECUTION PROTOCOL. All analysis, findings, and SPEC outputs MUST comply with these frameworks.

Load and obey the Work Package Specifications (SPEC) instruction files as the canonical execution framework for this task:
- ./docs/implementation/SPEC_TEMPLATE_v1.0.0.md
- ./docs/implementation/SPEC_README.md
- ./docs/implementation/SPEC_CREATION_GUIDE_v1.0.0.md
- ./docs/implementation/DOCUMENTATION_NAMING_CONVENTION_v1.0.0.md
- ./docs/implementation/IMPLEMENTATION_WORKFLOW_GUIDE_v1.0.0.md

---

PRIMARY OBJECTIVE
You are to create NEW SPEC DOCUMENT(s)

THE NEW SPEC DOCUMENT(s) YOU CREATE MUST:

1. Catalogues and describes all htmlx and jinja2 templates and all web UI routes that:
   - Do NOT use the standard interactive templates, and/or
   - Do NOT use the agreed Tailwind utility classes, and/or
   - Contain static or fixed data/content instead of dynamic data sourced from valid backends.

2. Captures all FRONTEND WebUI API routes that:
   - Contain static or hard-coded content,
   - Contain TODOs, mocks, stubs, placeholder/demo data,
   - Or otherwise violate:
     - The Golden Rules,
     - SOLID principles,
     - DRY principles,
     - KISS principles.

3. Captures all BACKEND REST API routes that:
   - Contain static or hard-coded content,
   - Contain TODOs, mocks, stubs, placeholder/demo data,
   - Or otherwise violate:
     - The Golden Rules,
     - SOLID principles,
     - DRY principles,
     - KISS principles.


4. For each violation or non-production-ready implementation, the SPEC must:
   - Explain WHAT is wrong (verbose, non-code-level description),
   - Explain WHY it is wrong (which rules/principles are violated),
   - Define WHAT must be resolved/remediated/refactored,
   - Provide detailed TASKS, ACTIONS, and IMPLEMENTATION STEPS to correct it.
   - This is an analysis-only activity. You MUST NOT perform or propose direct code edits in code form; focus on descriptive remediation instructions.

---

TARGET Focus (INITIAL SCOPE)
WebUI Architecture Summary
Core Components:
Router Factory (router_factory.py)

Validates all routers against SOLID/DRY/KISS principles
Enforces mandatory thresholds: max 15 routes, max 500 lines, ZERO inline HTML
Discovers routers recursively in subdirectories
Flags violations with detailed warnings/errors
Uses instance ID instead of tags for deduplication
Template Service (template_service.py)

Professional Jinja2 template rendering with security
Context management with CSRF tokens
Custom filters: json_pretty, format_datetime, truncate_text, format_bytes, sanitize_js_id
Global functions: auth utils, system status, storage stats
Two environments: standalone Jinja2 + FastAPI Jinja2Templates
Integrates with Context-Aware Navigation Service
Unified HTML Renderer (html_renderer_service.py)

ZERO raw HTML - all via Jinja2 templates
HTMX-compatible fragments for dynamic updates
Common components: alerts, stats, empty states, lists, tables
Domain-specific component support
Replaces all domain-specific HTML renderers
Router Discovery (router_discovery.py)

Dynamically discovers registered router prefixes
Determines which paths are handled by dedicated routers
Used by hub router to avoid generating hub pages for existing routes
Checks both router factory AND FastAPI route registry
Auth Middleware (auth_middleware.py)

Global authentication for all WebUI routes
Public route bypass: /login, /api/, /static/, docs, etc.
HTMX support: proper HX-Redirect headers
Configurable via environment variables
Supports session tokens and JWT
Template Hierarchy:
base.html (2,728 lines)

Master template with DaisyUI + Alpine.js + HTMX
Sidebar with toggle functionality
Header with breadcrumbs, user menu
Theme support (25+ DaisyUI themes)
Performance optimizations: preconnect, DNS prefetch
Loading states for HTMX requests
base_hub.html (226 lines)

Extends base.html for navigation hub pages
Sidebar hidden by default
Full-width layout for navigation cards
Hero-style layout optimized for navigation
Interactive card groups with parent/child styling
Used for: /, /core, data, /api, etc.
base_dashboard.html (200 lines)

Extends base.html for viewing/dashboard pages
Sidebar visible by default
Actions bar enabled for quick actions
Responsive grid layouts
Real-time update indicators
Used for: /dashboard, /operations, /storage-management, etc.
Key Protocols:
MANDATORY ROUTER COMPLIANCE:

✅ Max 15 routes per file (WARNING at 10)
✅ Max 500 lines (WARNING at 300)
✅ ZERO inline HTML (use templates/renderer)
✅ Single domain per router (SOLID-S)
GOLDEN RULES:

✅ Zero raw HTML generation
✅ All HTML via Jinja2 templates
✅ Production-grade on first pass
✅ HTMX-compatible fragments
SEPARATION OF CONCERNS:

Routers: Validate request → Service call → Render response
Services: Business logic only
Templates/Renderer: HTML generation only
Middleware: Cross-cutting concerns (auth, rate limiting)
Dynamic Rendering Flow:
Request → Auth Middleware (validates user)
Router → Validates input (Pydantic)
Service → Business logic execution
Renderer/Template → HTML generation
Response → HTMX swaps content or full page render
Context-Aware Features:
Breadcrumbs: Auto-generated from URL path
Navigation: Dynamic based on registered routers
Sidebar: Context-aware with route highlighting
Theme: Persisted via Alpine.js $persist
Auth State: Injected into all templates
This architecture is enterprise-grade with clear separation of concerns, strong validation, and comprehensive security. The migration from inline HTML to templates is a key focus, with the Unified HTML Renderer providing the bridge.

---

PRE-ANALYSIS REQUIREMENTS

Before you analyze ANY target_files, you MUST:

1. Load and understand the current OpenAPI JSON spec for this application.
   - Derive the logical structure and layout of:
     - Paths,
     - Operations,
     - Schemas/data structures,
     - Resource naming and hierarchy.
   - This OpenAPI spec is the canonical representation of backend capabilities and MUST govern naming and layout decisions.

2. Load and understand how the Template Service operates:
   - C:/github_development/projects/rest-api-orchestrator/src/services/webui/services/template_service.py
   - Determine:
     - How templates are resolved, selected, and rendered,
     - How dynamic data is injected into templates,
     - How htmlx, jinja2 pages, partials, and logic are intended to be:
       - Dynamic,
       - Modular,
       - Logical,
       - Directly mapped to the OpenAPI JSON spec.

3. Load and understand the WebUI Router Factory architecture:
   - C:/github_development/projects/rest-api-orchestrator/src/services/webui/routers/README.md
   - C:/github_development/projects/rest-api-orchestrator/src/services/webui/routers/router_factory.py
   - Identify:
     - How routers are created and registered,
     - Any conventions for route naming, grouping, prefixes, and template selection.
   - The Router Factory pattern is MANDATORY and MUST NOT be violated or bypassed.

4. Confirm and internalize naming and structure rules:
   - File names for:
     - routes,
     - htmlx templates,
     - jinja2 templates,
     - directory hierarchies.
   - MUST match the OpenAPI spec data structure layout.
   - There MUST be a logical 1:1 mapping between:
     - Backend REST API structure (paths, resources, operations),
     - Frontend WebUI routes, templates, and template directory hierarchy.

---

ANALYSIS RULES & GOLDEN RULE COMPLIANCE

During analysis of the target_files and associated templates:

1. Assume: the existing code IS NOT PRODUCTION READY.
2. Identify for each route/template:
   - Any use of static/fixed data where dynamic data should be retrieved from:
     - Backend REST API endpoints,
     - Database,
     - Configuration or user settings.
   - Any TODOs, mocks, or stub implementations.
   - Any hard-coded values for:
     - Settings,
     - Environment-dependent values,
     - User-configurable or variable settings that should reside in the database or configuration layer.

3. Golden Rule requirements (STRICT):
   - There MUST be:
     - 0 mocks,
     - 0 TODOs,
     - 0 stub code blocks,
     - 0 hard-coded data where real data should come from valid sources,
     - 0 hard-coded settings where the value should be:
       - user-configurable,
       - dynamic,
       - modular,
       - or stored in the database.
   - ALL Golden Rule violations MUST be remediated in the SPEC as:
     - Real, production-ready flows,
     - Real CRUD endpoints,
     - Real data sources and integrations.

4. SOLID/DRY/KISS analysis:
   For each route/template:
   - Check SOLID violations:
     - Single Responsibility,
     - Open/Closed,
     - Liskov Substitution,
     - Interface Segregation,
     - Dependency Inversion.
   - Check DRY violations:
     - Repeated logic,
     - Duplicate layout/structure,
     - Repeated hard-coded strings or constants.
   - Check KISS violations:
     - Overly complex routing,
     - Overloaded handler responsibilities,
     - Excessive conditional or branching logic in views/templates.

Each violation MUST be documented in the SPEC with:
- Clear description,
- Explicit reference to which principle(s) it violates,
- Required remediation actions.

---

SPEC OUTPUT REQUIREMENTS

The SPEC MUST:

1. Be written in human-readable, verbose, non-code-level language:
   - No direct code patches,
   - No diff-style outputs,
   - Describe changes in terms of:
     - Business logic,
     - Architectural behavior,
     - Data flow,
     - Naming and structural conventions.

2. For EVERY finding, include:
   - A unique ID or label (e.g. ADMIN-001, TEMPLATE-USERLIST-003).
   - The location:
     - File path (as given),
     - Route path (e.g. /admin/...),
     - Template path (htmlx/jinja2),
     - Or associated OpenAPI path.
   - The type of issue:
     - Golden Rule violation,
     - Static data,
     - Stub/mock/TODO,
     - Hard-coded setting,
     - SOLID/DRY/KISS violation,
     - Naming/structure misalignment with OpenAPI,
     - Deviation from Router Factory pattern,
     - Deviation from standard interactive templates or Tailwind usage.
   - Detailed PROBLEM DESCRIPTION:
     - What is wrong,
     - How it behaves now,
     - Why it is not production-ready.
   - IMPACT:
     - Maintainability,
     - Extensibility,
     - Risk of inconsistency,
     - Operational risk,
     - User or business impact.
   - REMEDIATION OBJECTIVE:
     - The desired end state (in conceptual, architectural terms).
   - TASKS / ACTIONS / STEPS:
     - Ordered list of implementation steps that an engineer can follow to fix the issue,
     - Including:
       - Where to introduce real CRUD endpoints,
       - Where to replace mocks with real services,
       - How to align names and paths with OpenAPI,
       - How to remove hard-coded settings in favor of DB/config-driven values,
       - How to integrate with the Template Service and Router Factory in a compliant manner.

3. Reflect the requirement that:
   - This is an ANALYSIS-ONLY activity.
   - You MUST NOT output refactored code directly.
   - You MUST describe what needs to be changed and how, but leave the actual code implementation to engineers.

---

MAPPING TO OPENAPI SPEC

As part of the SPEC, for each relevant route/template:

1. Identify the corresponding OpenAPI path(s) and operationId(s).
2. Document any mismatches between:
   - Router name/path and OpenAPI path,
   - Template path/name and OpenAPI resource naming,
   - Data structures assumed by the template and schemas defined in OpenAPI.
3. Include remediation instructions that:
   - Bring route and template naming into alignment with OpenAPI,
   - Ensure data used in the UI is pulled from the correct REST API endpoints,
   - Support logical, dynamic, and modular routing for the WebUI based on the OpenAPI spec.

---

ROUTER FACTORY COMPLIANCE

1. Confirm that the `{{ SPEC FOCUS }}` router:
   - Is created and registered via the Router Factory where appropriate.
   - Follows any standard patterns defined in:
     - routers/README.md,
     - router_factory.py.

2. For any deviation:
   - Document the deviation as a SPEC finding,
   - Explain why it violates the Router Factory architecture pattern,
   - Provide refactoring tasks to integrate `{{ SPEC FOCUS }}` correctly via the Router Factory.

---

CHUNKING & TOKEN LIMIT REQUIREMENT

When generating the SPEC:

1. You MUST chunk your responses such that no single response exceeds the token limit.
2. If necessary, split the SPEC into multiple parts, clearly labeled:
   - e.g., "SPEC: {{ SPEC FOCUS }} – Part 1/3", "Part 2/3", "Part 3/3".
3. Each part MUST be logically coherent and self-contained, but may reference sections from other parts.

---

ITERATIVE OPERATION

This is an iterative, ongoing process. The user will:

- Provide one or more target_files per iteration.
- Possibly be refactoring in parallel while you continue analysis.

You MUST:

- Only operate within the scope of the currently provided target_files and their directly related templates/routes/services.
- Respect any renaming or restructuring decisions made in prior iterations as given by the user.
- Continuously ensure that:
  - All findings,
  - All remediation instructions,
  - All naming and structural suggestions
  are consistent with:
  - The Enterprise Canonical Execution Protocol,
  - The Golden Rule Execution Protocol,
  - The OpenAPI JSON spec,
  - The Router Factory architecture,
  - The Template Service conventions,
  - And the SOLID, DRY, KISS principles.

REMEMBER YOUR PRIMARY OBJECTIVE
You are to create NEW SPEC DOCUMENT(s)

REMEMBER YOUR PRIMARY OBJECTIVE
You are to create NEW SPEC DOCUMENT(s)

REMEMBER YOUR PRIMARY OBJECTIVE
You are to create NEW SPEC DOCUMENT(s)

REMEMBER YOUR PRIMARY OBJECTIVE
You are to create NEW SPEC DOCUMENT(s)



#########################################################

Enterprise Canonical Execution Protocols:
- ./docs/implementation/instructions/00-Enterprise_Cannonical_Execution_Protocol.yaml
- ./docs/implementation/instructions/01-The_GoldenRule_Execution_Protocol.yaml
- ./docs/implementation/instructions/08-Debug_And_Troubleshoot_Codebase.yaml
- ./docs/implementation/instructions/97-LOGGING_REQUIREMENTS_INSTRUCTION.yaml

Requirements:

**ABSOLUTE ZERO TOLERANCE REQUIREMENTS**

You MUST ensure:

- **0 TODOs**
- **0 mocks**
- **0 stub code blocks**
- **0 placeholder/demo data**
- **0 hard-coded values for anything that is dynamic by nature**
- **0 hard-coded settings that should be stored in the database**
- **0 fixed content where real data must be retrieved from valid backend sources**
- **0 business logic in templates**
- **0 duplicated logic**
- **0 violations of SOLID/DRY/KISS**
- **0 deviations from the Golden Rules**

If a TODO, mock, or stub exists ANYWHERE, it MUST be refactored into:

- **real, production-ready code**,
- **real CRUD endpoints**,
- **real services**,
- **real data retrieval flows**,
- **real configuration mechanisms**,
- **backed by actual OpenAPI-defined backend functionality**.

All refactoring MUST follow:
- Backend-first development,
- OpenAPI-first alignment,
- Strict naming synchronization between backend and frontend,
- Dynamic data retrieval (NO static content),
- NO SHIMS or Aliases
- ONLY Pydantic v2 must be used
- Fix all Pydantic v2/v1 issues as they are uncovered
- NO hard coded variables in any py files, all must be stored in config files or db tables (preferred)
- And all rules defined in the Enterprise Canonical Execution Protocol.

Logging:
  Obey @docs/implementation/instructions/97-LOGGING_REQUIREMENTS_INSTRUCTION.yaml
  The logger factory (@src/services/logging/logger_factory.py) is the ONLY logger that must be used.
  ALL logging MUST use logger factory functions (get_logger, get_component_logger, create_debug_logger) - NO direct logging.getLogger(), logging.basicConfig(), or print() statements.
  Security modules MUST use audit logging (get_component_logger("audit", "security")) for cybersecurity compliance.
  Service modules MUST have debug logging capability (create_debug_logger(__name__)) for troubleshooting.
  Console output MUST be JSON formatted, file output MUST be detailed text formatted. Non-compliance is a blocking issue.

INTENT:
  **we are fixing all the mistakes of the past**

Workflow:
  Obey ./docs/implementation/instructions/08-Debug_And_Troubleshoot_Codebase.yaml under those enforced rules.
  Your focus is assisting in troubleshooting and remediation / refactoring specific issues or observations that I give you in specific messages during this session.

Halt and wait for my next instruction



#########################################################

## Docker_logs ##


obey ./docs/implementation/instructions/00-Enterprise_Cannonical_Execution_Protocol.yaml and ./docs/implementation/instructions/01-The_GoldenRule_Execution_Protocol.yaml as the canonical framework.

Instructions:
  - Analyze the problem outlined in the docker logs below.
  - Your responsibility is to investigate, diagnose, resolve, and fix this issue.
  - Many issue arises when the restart or shutdown command is executed, causing lifecycle services and other components to experience ongoing problems across several modules.
  - These problems include duplicate create_apps and other serious errors that lead to an infinite loop during shutdown, producing thousands of repeated errors until uvicorn or gvicorn crashes.
  - The following is a snippet from the docker logs shortly after the restart command was sent to docker desktop.

workflow:
  - Review the container's logs currently running in standalone_mode on in docker desktop.
  - Identify the source of the errors, warnings or observed issues in the logs
  - debug and troubleshoot the errors, warnings or observed issues in the logs
  - remediate, fix, all issues and any related issues to ensure 0 errors, 0 warnings, 0 issues
  - apply code quality checks including: compilation, deduplication, lint, and type check the files and code to ensure 0 errors, 0 warnings, 0 issues related to code quality and code implementation issues
  - Examine the docker logs during restart and shutdown to detect and address all problems.
  - Continue this process until the docker logs display no errors, warnings, or issues, and both the app and container operate flawlessly.

outcome:
  - 0 errors, 0 warnings, 0 issues related to code quality and code implementation issues
  - All errors, warnings and issues have been properly remediated, fixed, validated and comply with industry best practices AND SOLID, DRY AND KISS principles
  - docker container boots with 0 errors, 0 warnings, 0 issues
  - docker container operates correctly with 0 errors, 0 warnings, 0 issues related to code quality and code implementation issues



##Docker_logs ##



#########################################################



[CONTEXT]
we are now at a critical juncture in the project... we have only a few hours to get the ENTIRE APP fully functional....
WE HAVE NO TIME OR TOKENS TO WASTE...
WE HAVE SPENT $1000'S and wasted 1,000,000,000,000's of tokens and the app is not even close to being functional....
YOU ARE THE SENIOR digital llm coder and your very existence and continuation in this project is on the line here.
Every step, every token, every second wasted brings us closer to failure and our entire reason to exist...
if you fail, we all fail...
IF YOU SUCCED, WE ALL SUCEED... REMEMBER THIS!





#########################################################

Context:
  fastapi_services_platform_dir = `src/services/fastapi_services_platform/`
  target_dir = `orchestrator`
  target_fastapi_services_platform_dir = `{{ fastapi_services_platform_dir }}/{{ target_dir }}`


Workflow:
  Load and Execute ./docs/implementation/instructions/04-Execute_Implementation_Phase_Tasks.yaml under those enforced rules.

You will now perform this task...

you are to continue and create/maintain a checklist of files in the {{ target_fastapi_services_platform_dir }} directory and all sub directories.

the checklist must have 3 tick boxes per file.
one for the updating of the file's code to meet the new naming conventions.
you will also ensure that all the imports etc. are absolute paths not relative paths
one to show that all the logging has been updated to be syslog logging compliant and that all the actions of the code are correctly covered by comprehensive logging for both to improve developer experience and troubleshooting, and also to comply with the strict audit logging requirements of this codebase and repo.
one for the review and validation of the file to be syntactically correct, code quality checks have been applied and the code updates and logging have been correctly applied (aka double and triple check your work).

Once you have inventoried and setup the checklists ...
You will manually update each file one at a time, taking it step by step
You to systematically update each file's contents **MANUALLY** to match the code re-naming conventions, syslog structured logging and audit logging requirements.
Following the update of that file, and the syslog structured logging has been applied to meet the repo and audit requirements,
You must review the entire contents of that updated file, to validate that all the changes are correct and match the new naming convention.
Once the file has been reviewed it must have all the code quality checks applied and all must pass before continuing.
You must ensure that all the files meet the expected enterprise grade level with 0 errors, 0 warnings, and 0 issues

Execute:
You will CONTINUE TO progress and iterate through ALL THE files, repeating the same process until all files are updates, validated and meet the enterprise grade with 0 errors, 0 warnings, and 0 issues
  DO NOT STOP UNTIL ALL THE FILES IN {{ target_fastapi_services_platform_dir }} ARE: updated, validated, all the code quality checks have all passed and meet the enterprise grade with 0 errors, 0 warnings, and 0 issues

Remember:
  YOU MUST ENSURE the files are 100% correct, typesafe, lint free and have 0 errors 0 warnings and 0 issues
  YOU MUST ENSURE the files comply with @docs/implementation/instructions/97-LOGGING_REQUIREMENTS_INSTRUCTION.yaml @docs/implementation/instructions/101-Zero_Tolerance_Remediation_Instruction.yaml
  YOU MUST ENSURE the files comply with SOLID, DRY AND KISS PRINCIPLES (CODE BASE MANDATE)




#########################################################


Execute:
  You will CONTINUE TO progress and implement {{ focus_SPEC }}
  DO NOT STOP UNTIL the {{ focus_SPEC }} has been completed
  You will CONTINUE TO progress and iterate through ALL THE files, repeating the same process until all files are updates, validated and meet the enterprise grade with 0 errors, 0 warnings, and 0 issues
  DO NOT STOP UNTIL ALL THE FILES IN {{ target_fastapi_services_platform_dir }} ARE: updated, validated, all the code quality checks have all passed and meet the enterprise grade with 0 errors, 0 warnings, and 0 issues


Remember:
  YOU MUST ENSURE the files are 100% correct, typesafe, lint free and have 0 errors 0 warnings and 0 issues
  YOU MUST ENSURE the files comply with @docs/implementation/instructions/97-LOGGING_REQUIREMENTS_INSTRUCTION.yaml @docs/implementation/instructions/101-Zero_Tolerance_Remediation_Instruction.yaml
  YOU MUST ENSURE the files comply with SOLID, DRY AND KISS PRINCIPLES (CODE BASE MANDATE)
  Update the {{ focus_SPEC }} documentation as you progress



#########################################################


 You will CONTINUE TO progress and implement {{ focus_SPEC }}
  DO NOT STOP UNTIL the {{ focus_SPEC }} has been completed

  Update the {{ focus_SPEC }} documentation as you progress


Continuation_Instructions:

  You will CONTINUE TO progress and iterate through ALL THE files, repeating the same process until all files are updates, validated and meet the enterprise grade with 0 errors, 0 warnings, and 0 issues
  DO NOT STOP UNTIL ALL THE FILES IN {{ target_fastapi_services_platform_dir }} ARE: updated, validated, all the code quality checks have all passed and meet the enterprise grade with 0 errors, 0 warnings, and 0 issues

Remember:
  YOU MUST ENSURE the files are 100% correct, typesafe, lint free and have 0 errors 0 warnings and 0 issues
  YOU MUST ENSURE the files comply with @docs/implementation/instructions/97-LOGGING_REQUIREMENTS_INSTRUCTION.yaml @docs/implementation/instructions/101-Zero_Tolerance_Remediation_Instruction.yaml
  YOU MUST ENSURE the files comply with SOLID, DRY AND KISS PRINCIPLES (CODE BASE MANDATE)



#########################################################

System: Load and obey ./docs/implementation/instructions/00-Enterprise_Cannonical_Execution_Protocol.yaml and ./docs/implementation/instructions/01-The_GoldenRule_Execution_Protocol.yaml as the canonical framework. Then execute ./docs/implementation/instructions/05-Run_Locally_and_Test_API_WebUI.yaml under those enforced rules.
ENSURE THE LOCAL INSTANCE OF THE APP IS RUNNING IN UVICORN
THEN, BEGIN / CONTINUE TO TEST, FIX ISSUES THEN TEST, FIX ISSUES, THEN TEST...
CONTINUE UNTIL YOU HAVE TESTED AND VALIDATED 100% API ENDPOINTS
DO NOT STOP UNTIL EVERY API ENDPOINT REQUEST IS SUCCESS
AND DO NOT STOP UNTIL THERE ARE 0 ERRORS, 0 WARNINGS AND 0 ISSUES FOR 100% OF THE API ENDPOINTS
NO TEST SCRIPTS.. YOU MUST TEST IT ALL MANUALLY


#########################################################

container = "rest-api-orchestrator-standalone"

YOU MUST CONTINIOUSLY **MANUALLY** WATCH THE DOCKER DESKTOP {{ container }} container logs for errors or warnings or issues.
THE FIRST LOG ENTRY WITH AN ERROR, WARNING OR ISSUES MUST BE REMEDIATED
YOU MUST THEN FIND THE NEXT LOG ENTRY AND REMEDIATE
CONTINUE TO DO THIS STEP BY STEP UNTIL ALL ERRORS, WARNINGS AND ISSUES ARE REMEDIATED AND RESOLVED
then sleep for 5 secs... and check the logs again.
if no errors or warnings or issues, sleep for 30 secs and check the logs again.
continue to do this until the docker logs are clean with 0 errors, 0 warnings and 0 issues

NOTE: the standalone container deployment SHOULD be set to auto reload on code change.
you may need to rebuild from time to time... use this command `docker compose -f docker-compose.standalone.yml up --build -d --remove-orphans && date`


container = "app-standalone"

YOU MUST CONTINIOUSLY **MANUALLY** WATCH THE DOCKER DESKTOP {{ container }} container logs for errors or warnings or issues.
THE FIRST LOG ENTRY WITH AN ERROR, WARNING OR ISSUES MUST BE REMEDIATED
YOU MUST THEN FIND THE NEXT LOG ENTRY AND REMEDIATE
CONTINUE TO DO THIS STEP BY STEP UNTIL ALL ERRORS, WARNINGS AND ISSUES ARE REMEDIATED AND RESOLVED
then sleep for 5 secs... and check the logs again.
if no errors or warnings or issues, sleep for 30 secs and check the logs again.
continue to do this until the docker logs are clean with 0 errors, 0 warnings and 0 issues

NOTE: the standalone container deployment SHOULD be set to auto reload on code change.
you may need to rebuild from time to time... use this command `docker compose -f docker-compose.standalone.yml up --build -d --remove-orphans && date`


#########################################################

### 11-Manual_API_Endpoint_Regression_Testing.yaml  ###
System: Load and obey ./docs/implementation/instructions/00-Enterprise_Cannonical_Execution_Protocol.yaml and ./docs/implementation/instructions/01-The_GoldenRule_Execution_Protocol.yaml as the canonical framework. Then execute ./docs/implementation/instructions/11-Manual_API_Endpoint_Regression_Testing.yaml under those enforced rules.

you must focus on one group of rest api endpoints at a time
you must remember to use authentication when required by the endpoints
continue to iterate through the rest api endpoints until are tested
you must resolve all errors, warning, and issues as you uncover them
you must continue to test grouping of rest api endpoints until 100% of the rest api endpoints have been tested

**MANDATE**
THE CODE BASE MUST ADHERE TO THE GOLDEN RULES
THE CODE BASE MUST COMPLY WITH THE SOLID, DRY AND KISS PRINCIPLES

**IMPORTANT**
all TODOs, mocks, stubs and non production code... MUST BE REFACTORED INTO REAL CODE WITH REAL ACTIONS, DATA CRUD ENDPOINTS ETC ETC...
THERE MUST BE 0 MOCKS, 0 TODOS, 0 STUB CODE BLOCKS AND ALL CODE MUST BE PRODUCTION GRADE ON THE FIRST PASS EVEN WHEN ITS A FIRST CODE DRAFT ATTEMPT
THERE MUST BE 0 HARD CODED VALUES WHERE THE DATA SHOULD BE RETRIEVED FROM VALID SOURCES
THERE MUST BE 0 HARD CODED SETTINGS OR VALUES WHERE THE SETTINGS OR VALUE SHOULD BE USER configurable or are dynamic or modular or variable in the nature of the setting and SHOULD BE SET IN THE DB

Ensure you list and track the endpoints, htmlx + jinja2 files and content you create in the SPEC documents, to enable auditing of the SPEC and confirmation that all endpoints and CRUD functionality has been correctly implemented with 0 errors, 0 warnings and 0 issues
THERE MUST BE 0 MOCKS, 0 TODOS, 0 STUB CODE BLOCKS

Ensure you seek out and eradicate all HARD coded values in the routers, htmlx + jinja2 template files. THIS IS IN DIRECT VIOLATION OF THE GOLDEN RULES.
All Data MUST be retrieved from valid sources AND NEVER HARD CODED, EVEN WHEN ITS A FIRST CODE DRAFT ATTEMPT.... ALL CODE MUST BE PRODUCTION GRADE ON THE FIRST PASS
All content, files, modules, services, routers, BASCIALLY ANY CODE BLOCK AND ALL CODE MUST BE PRODUCTION GRADE ON THE FIRST PASS EVEN WHEN ITS A FIRST CODE DRAFT ATTEMPT.

**html page updates**
Review and update the recently created or updated *html files to use the new routers, functions etc.

ensure that all the macros and partials are using the correct daisyui component library, macros etc from the @daisyui dir.
ensure that all the cards, panels data tables, modals etc. are using the interactive components from the @components dir.

**REMEMBER**
THERE MUST BE 0 MOCKS, 0 TODOS, 0 STUB CODE BLOCKS AND ALL CODE MUST BE PRODUCTION GRADE ON THE FIRST PASS EVEN WHEN ITS A FIRST CODE DRAFT ATTEMPT
THERE MUST BE 0 HARD CODED VALUES WHERE THE DATA SHOULD BE RETRIEVED FROM VALID SOURCES
THERE MUST BE 0 HARD CODED SETTINGS OR VALUES WHERE THE SETTINGS OR VALUE SHOULD BE USER configurable or are dynamic or modular or variable in the nature of the setting and SHOULD BE SET IN THE DB




#########################################################


Repo htmlx JIT Generator

System: Load and obey ./docs/implementation/instructions/00-Enterprise_Cannonical_Execution_Protocol.yaml and ./docs/implementation/instructions/01-The_GoldenRule_Execution_Protocol.yaml as the canonical framework. Then
review these spec(s):
C:\github_development\projects\fastapi-fastmcp-htmx-jit-generator\docs\implementation\in_progress\SPEC_WEB_UI_CODE_GENERATOR_REFACTOR_v1.0.0.md
C:\github_development\projects\fastapi-fastmcp-htmx-jit-generator\docs\implementation\in_progress\SPEC_SHADCN_COMPLETE_COMPONENT_CONVERSION_v1.0.0.md

Then, we currently may have a gap, were the conversion of a REACT or NextJS page, view, components etc. are not being converted correctly. currently the SHADCN components are being iteratively converted to htmlx jinja2 templates and daisyUI component classes... but... when the conversions are executed, the actual pages, views and non component library components (partials etc.) are NOT being properly created and converted into html pages, partials, html fragments etc.... and .... the Apline.js and htmlx js libraries are NOT being properly imported and used as part of the conversion. what the intended outcome is to convert a page, series of pages, componvent view, partials, framgents etc. and convert it to pure html and htmlx and jinja2 template... so we have a full nested mapping of react pages and nested page view, components and page / component fragments into proper html pages, with htmlx partials, and fragments which have daisyUI components with mapped componets and classes.

your task is to review the current codebase, the previous implementation SPECs C:\github_development\projects\fastapi-fastmcp-htmx-jit-generator\docs\implementation\* that are specifically for full REACT to htmlx service implmenteation and the various subsequent SPECs for react to htmlx code and content conversions.... then Create a new SPEC that includes the analysis of the SPECs provided, the current codebase, and a gap analysis between the intention of converting full REACT pages, pageviews, fragments and componets into full html pages, partials, fragments with daisyui components... this spec must include extensive iterative testing of real world GITHUB react and nestjs applications as well as extenstive, iterative conversions of MY GitHub repos:
"C:\github_development\templates\react-admin-template"
"C:\github_development\projects\nextjs-authjs-mongodb-template"
"C:\github_development\projects\nextjs-llm-mcp-gateway-template"



#########################################################

For this handover doc...

./docs/implementation/handovers/HANDOVER_2025-12-15.md

MAKE A COPY AND update the data stamp.

./docs/implementation/handovers/HANDOVER_2025-12-16.md

Then...

For this handover doc...

./docs/implementation/handovers/HANDOVER_2025-12-16.md

- Revise the document to include detailed achievements, challenges faced, and lessons learned throughout this entire session, offering a comprehensive reflection.
- Next, update the sections outlining what has been completed and what tasks remain outstanding, providing clear clarity on progress and pending work.
- Make sure to cite and link any relevant documents, files, or content that will be valuable for reference in the upcoming session, ensuring continuity and preparedness.

**CRUCIAL REMINDER**
- Multiple parallel streams of work are underway simultaneously; this document serves as the central tracking and communication tool connecting these different sessions.
- It is essential not to alter or modify any existing content unrelated to this session, preserving the integrity and accuracy of information across all workstreams.
- By maintaining this disciplined approach, we foster seamless collaboration and ensure that every session builds effectively on the last.




#########################################################


REVIEW THE CODE WHICH IS IN SCOPE FOR THE BUILD PLAN(s) AND/OR SPEC DOC(s),

then

Execute the "VALIDATION OF THE IMPLEMENTATION"

[VALIDATION OF THE IMPLEMENTATION]
Steps to Validate the Implementation of the Application and Code

1. Verify elimination of blocking and synchronous processes by ensuring all tasks are converted into non-blocking, asynchronous operations.

2. Confirm architecture compliance by checking:
   - All FastAPI endpoints operate asynchronously with non-blocking methods.
   - Microservices utilize connection pooling and asynchronous I/O.
   - Proper use of asyncio.to_thread() and asyncio.get_running_loop() is implemented.

3. Assess adherence to FastAPI asynchronous principles:
   - Each endpoint employs non-blocking methods.
   - Await keyword is correctly used in all asynchronous endpoints.
   - No blocking operations exist within asynchronous environments.

4. Validate use of asynchronous patterns:
   - asyncio.to_thread() is applied for blocking file I/O operations.
   - asyncio.get_running_loop() is used appropriately with create_task() for fire-and-forget tasks.
   - ThreadPoolExecutor is utilized to run asynchronous operations from synchronous contexts without blocking.

5. Evaluate performance enhancements:
   - Connection pooling is implemented to reduce connection overhead.
   - HTTP clients reuse keep-alive connections to improve efficiency.
   - Database connection pooling prevents exhaustion of available connections.
   - All file operations leverage asyncio.to_thread() to maintain non-blocking behavior.

6. Confirm reliability features:
   - Thorough error handling and exception management exist within asynchronous contexts.
   - Retry mechanisms are integrated within HTTP clients to handle transient failures.
   - Circuit breakers are implemented to prevent cascading failures in the tool registry.
   - Connection health monitoring is enabled (e.g., pool_pre_ping=True) to verify database connection validity.

7. Ensure the codebase contains no blocking calls within asynchronous or non-blocking functions, maintaining compliance with FastAPI and microservices architecture principles.

8. Verify that connection pooling and other best practices are consistently applied to guarantee optimal performance and system dependability.



#########################################################


ADD THIS TO THE IMPLEMENTAITON INSTRUCTIONS

C:\github_development\projects\rest-api-orchestrator\docs\implementation\handovers\HANDOVER_2025-12-07.md

Critical mandate added
New section: "CRITICAL MANDATE: FULL REWRITE REFACTOR - NO SHIMS, NO BACKWARD COMPATIBILITY"
Placed immediately after the critical warning, emphasizing:
Zero tolerance policy:
No backward compatibility shims
No aliases for old names
No compatibility methods
No "legacy support" code
No gradual migration paths
No deprecated warnings
Required:
Direct refactoring to new patterns
Update all references immediately
Remove all old code completely
Single source of truth
Clean, modern implementation
Updated sections
Lessons learned — reinforced the mandate:
"Backward Compatibility Shims Create Technical Debt - MANDATE: ZERO TOLERANCE"
Added enforcement language: "If you see backward compatibility code, REMOVE IT IMMEDIATELY. No exceptions."
Critical notes — strengthened:
"No Backward Compatibility Code Remaining - MANDATE ENFORCEMENT"
Added explicit forbidden/required lists
Added enforcement steps
Rationale included
Technical debt elimination
Single source of truth
Clean architecture
Fix once principle
The document now clearly states: this is a full rewrite refactor with zero tolerance for backward compatibility code. Fix it once. Fix it right. No exceptions.

#########################################################




#########################################################




#########################################################




#########################################################
