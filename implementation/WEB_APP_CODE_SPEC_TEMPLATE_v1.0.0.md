# Session Initialization - Protocol Enforcement Code Implementation Specification

**Version**: v1.0.0
**Date**: [YYYY-MM-DD]
**Last Updated**: [YYYY-MM-DD HH:MM:SS] (Australia/Adelaide)
**Status**: ⚪ Pending - [Module] UI Parity Focus
**Priority**: P0 - CRITICAL
**Session Type**: Code Implementation and Remediation Session
**Instruction Files**:

- `000-DOCTRINE-Enterprise_Canonical_Execution.yaml`
- `001-PROTOCOL-The_GoldenRule_Execution-v2.0.1.yaml`
- `002-PROTOCOL-Zero_Tolerance_Remediation-v2.0.0.yaml`
- `003-PROTOCOL-FastAPI_Pure_Code_Implementation-v2.0.0.yaml`
- `004-PROTOCOL-Validate_Remediate_Codebase-v2.0.0.yaml`
- `006-PROTOCOL-RFC2119_Requirements_Language-v1.0.0.yaml`
- `104-INSTRUCTIONS-Execute_Implementation_Phase_Tasks-v2.0.0.yaml`
- `202-INSTRUCTIONS-Pure_Code_Implementation_Execution_Protocol-v2.0.0.yaml`
- `203-INSTRUCTIONS-FastAPI_Design_Implementation_Refactor-v2.0.0.yaml`

---

## 📊 SESSION SUMMARY

### Session Objective

This session is initialized for code implementation and remediation following the combined execution protocols. The session enforces multiple critical protocols:

- **002-PROTOCOL-Zero_Tolerance_Remediation** (v2.0.0) - ENFORCED
- **003-PROTOCOL-FastAPI_Pure_Code_Implementation** (v2.0.0) - ENFORCED
- **004-PROTOCOL-Validate_Remediate_Codebase** (v2.0.0) - ENFORCED

### Primary Objective

**Achieve 1-to-1 capability parity and architectural mirroring between the Frontend Web App (Root: `./src/ui/`) and the Backend REST API (Root: `./src/`).**

The core philosophy for this session is **Full-Stack Structural Correlation**. By anchoring the **Backend Root** at `./src/` and the **Frontend Root** at `./src/ui/`, the platform enables both **Fullstack** and **Standalone** deployment patterns. The Frontend MUST mirror the Backend directory structure to enable a direct, transparent correlation between the two layers, ensuring architectural consistency regardless of the deployment model.

**Implementation Standards**:
- **Mandatory**: Use components from `src/ui/templates/components/interactive/` for all dynamic features.
- **Mandatory**: Use DaisyUI macros for all standard UI elements (buttons, inputs, alerts, modals).
- **Mandatory**: Adhere to the 3-level panel/card hierarchy for all hub and list views.

---

### Instruction Protocol Loaded

- **Doctrine**: `000-DOCTRINE-Enterprise_Canonical_Execution.yaml` ✅ Loaded
- **Protocol 1**: `001-PROTOCOL-The_GoldenRule_Execution-v2.0.1.yaml` ✅ Loaded
- **Protocol 2**: `002-PROTOCOL-Zero_Tolerance_Remediation-v2.0.0.yaml` ✅ Loaded and **ENFORCED**
- **Protocol 3**: `003-PROTOCOL-FastAPI_Pure_Code_Implementation-v2.0.0.yaml` ✅ Loaded and **ENFORCED**
- **Protocol 4**: `004-PROTOCOL-Validate_Remediate_Codebase-v2.0.0.yaml` ✅ Loaded and **ENFORCED**
- **Protocol 6**: `006-PROTOCOL-RFC2119_Requirements_Language-v1.0.0.yaml` ✅ Loaded
- **Instruction 104**: `104-INSTRUCTIONS-Execute_Implementation_Phase_Tasks-v2.0.0.yaml` ✅ Loaded
- **Instruction 202**: `202-INSTRUCTIONS-Pure_Code_Implementation_Execution_Protocol-v2.0.0.yaml` ✅ Loaded
- **Instruction 203**: `203-INSTRUCTIONS-FastAPI_Design_Implementation_Refactor-v2.0.0.yaml` ✅ Loaded

### Current State

- **Status**: [Module] Parity Mapping Initialized - Reviewing backend vs UI gaps
- **Work Type**: UI-BACKEND PARITY MAPPING
- **Scope**: `src/ui/templates/pages/` (auth, chat, llm, ai_agent, core)
- **Files/Modules**: Templates and corresponding UI routers
- **Context**: 1:1 mapping of REST API capabilities to Web UI.

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

### Interactive Component & Macro Mandate

**ADHERENCE TO THE STANDARDIZED COMPONENT SYSTEM IS NON-NEGOTIABLE.**

- **FORBIDDEN**: Writing raw HTML for elements that have existing Interactive Components.
- **FORBIDDEN**: Hardcoding styles that are available via DaisyUI classes or macros.
- **FORBIDDEN**: Bypassing the `interactive_panel` → `interactive_card_group` hierarchy.
- **MANDATORY**: Use `src/ui/templates/components/interactive/` for tables, tabs, modas, and forms.
- **MANDATORY**: Use macros defined in `src/ui/templates/macros/` for consistency.
- **MANDATORY**: All new features MUST be built using the atomistic component methodology.

### HTMX CSP & CSS Security Gap Analysis (2025 Mandate)

A comprehensive audit was performed against `htmlx-csp-css-security-best-practices-2025.md`. The following gaps were identified that must be remediated to meet the 2025 security mandate.

#### 1. Audit HTMX Configuration
- **Finding**: `htmx.config.includeIndicatorStyles = false;` is correctly set in `src/ui/templates/components/interactive/base_pages/interactive_base.html` within a nonced script block.
- **Status**: **PASS (Base Template)** / **PENDING (Verify all layouts)**.
- **Remediation**: Ensure all top-level layouts (base_hub, base_dashboard) inherit from `interactive_base.html` or explicitly set this config.

#### 2. Analyze Content Security Policy (CSP) Implementation
- **Finding**: `SecurityHeadersMiddleware` (in `src/services/integration/middleware.py`) generates a `csp_nonce` for each request and sets the `Content-Security-Policy` header.
- **Gap**: The production CSP for `style-src` needs to be verified for strictness (no `'unsafe-inline'`).
- **Status**: **PASS (Middleware exists)** / **GAP (Context Injection)**.
- **Remediation**: The generated `csp_nonce` is NOT being injected into the Jinja2 context for templates to use.

#### 3. Assess Nonce Generation and Injection
- **Finding**: Nonce is generated in middleware (`request.state.csp_nonce`).
- **Gap**: `UITemplateService` (`src/ui/services/template_service.py`) does NOT extract `request.state.csp_nonce` and add it to the template context. This breaks nonced tags in templates.
- **Gap**: Systemic search identified multiple inline `<style>` tags in components (e.g., `interactive_tabs.html`, `interactive_tabs_group.html`) and pages that LACK the `nonce="{{ csp_nonce }}"` attribute.
- **Status**: **FAIL (Systemic)**.
- **Remediation**:
    1. Update `UITemplateService` to inject `csp_nonce` into context.
    2. Externalize inline styles to compiled CSS (v4) or add nonces to all `<style>` and `<script>` tags.

#### 4. Review CSS Build Process and HTMX Style Integration
- **Finding**: `package.json` contains `build:css` and `watch:css` scripts using PostCSS and Tailwind CLI.
- **Gap**: The production `Dockerfile` is MISSING the Node.js build stage. It copies source files directly, meaning CSS is NOT compiled during the Docker build.
- **Gap**: `src/ui/static/css/main.css` does NOT include the mandatory HTMX indicator styles (`.htmx-indicator`, etc.).
- **Status**: **FAIL (Process & Content)**.
- **Remediation**:
    1. Update `Dockerfile` to include a Node.js build stage for CSS compilation.
    2. Update `tailwind.css` to include standard HTMX indicator utility classes.
    3. Ensure Node.js is removed from the final production image.

### HTMX CSP & CSS Remediation Plan

| Phase | Task | File(s) | Owner | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Foundation** | Inject `csp_nonce` into Jinja2 Context | `src/ui/services/template_service.py` | Antigravity | [x] |
| **Foundation** | Add HTMX Indicator Styles to CSS | `src/ui/static/css/main.css` | Antigravity | [x] |
| **Security** | Nonce-protect all inline scripts/styles | `src/ui/templates/**/*.html` | Antigravity | [x] |
| **Build** | Implement Multi-Stage Docker CSS Build | `Dockerfile` | Antigravity | [x] |
| **Verification** | Verify production CSP headers | `src/services/integration/middleware.py` | Antigravity | [x] |
| **Standardization** | Replace custom JS with public packages | `src/ui/templates/**/*.html` | Antigravity | [x] |

## JS Standardization & Public Package Prioritization (NEW-2025-01-03)
**Mandate: Prioritize public JS packages over custom scripts.**

### Identified Custom Scripts & Proposed Replacements
| Custom Script | Functionality | Public Replacement |
| :--- | :--- | :--- |
| `keyboard-navigation.js` | Focus Trap, ARIA | `@alpinejs/focus` (Official) |
| `lazy-loading.js` | Intersection Observer | `@alpinejs/intersect` (Official) |
| `swipe-gestures.js` | Touch Events | `alpinejs_gestures.js` (or simplified touch events) |
| `reduced-motion.js` | Motion Control | CSS Media Queries + `@alpinejs/collapse` |
| `error-handling.js` | Error Boundaries | HTMX Std Events + Minimal App Config |
| `mobile-optimization.js`| Layout/Safe Area | CSS (Tailwind v4) + DaisyUI |

### JS Standardization Remediation Plan
1. **Infrastructure**:
   - [x] Update `package.json` with required Alpine.js plugins.
   - [x] Download/Sync public minified scripts to `src/ui/static/js/vendor/` (Standardized vendor pipeline created).
2. **Refactoring**:
   - [x] Replace `keyboard-navigation.js` logic with `x-trap` directive. (Completed in Tabs, Table, Sidebar)
   - [x] Replace `lazy-loading.js` logic with `x-intersect` directive. (Implied in new templates)
   - [x] Refactor `swipe-gestures.js` to use standard touch event listeners. (Removed custom dependencies)
   - [x] Migrate `reduced-motion.js` logic to CSS-first approach using `@media (prefers-reduced-motion: reduce)`.
   - [x] Simplify `error-handling.js` to focus on app-specific logging/UI, removing redundant Alpine wrappers. (Refactored usages)
3. **Template Integration**:
   - [x] Update `interactive_base.html` to load public plugins.
   - [x] Remove custom script tags once replacements are verified.

### Page Construction Mandate

**ALL `index.html` PAGES MUST FOLLOW CANONICAL TEMPLATES BASED ON FUNCTION.**

- **Navigation Hubs**: `index.html` pages serving as navigation hubs MUST be based on `src/ui/templates/components/interactive/base_pages/index_hub_template.html`.
- **Operational Dashboards**: `index.html` pages serving as action-oriented or operational interfaces MUST be based on `src/ui/templates/components/interactive/base_pages/index_dashboard_template.html`.
- **FORBIDDEN**: Creating custom `index.html` layouts that do not extend/copy these canonical templates.
- **MANDATORY**: Adhere to the 3-level panel/card hierarchy within these templates.

### Unified Hierarchy Mandate

**BOTH THE FRONTEND WEB APP (./src/ui/) AND THE BACKEND REST API (./src/) HIERARCHIES MUST MAP TO THE OPENAPI SPECIFICATION.**

- **Architecture Anchoring**:
    - **Backend Root**: `./src/`
    - **Frontend Root**: `./src/ui/`
- **Deployment Pattern Support**: This structural anchoring is designed to natively support both **Fullstack** (integrated) and **Standalone** (container-isolated) deployment patterns.
- **Universal Structural Mapping**: Both the **Backend REST API** directory structure (`src/services/`) and the **Frontend Web App** directory structure (`src/ui/templates/pages/`) MUST explicitly map to the tags, path groups, and operations defined in the `openapi.json`.
- **Recursive Sub-Directory Mirroring**: The internal sub-directory structure within each module MUST be mirrored between layers. If a backend service implements deep nesting (e.g., sub-modules or category-based routers), the UI templates MUST follow an identical nested pathing.
- **API Version Mirroring (Filesystem)**: The REST API pathing (e.g., `/api/v1/`, `/api/v2/`) MUST be mirrored in the UI directory structure. Every UI page path must correspond to its API version (e.g., `src/ui/templates/pages/v1/...`).
- **UI URL Routing Policy**:
    - UI FastAPI decorators and URL paths MUST NOT include the `/api/v1/` or version prefix.
    - UI URL paths MUST start at `/`.
    - UI URL paths MUST map to the directory structure relative to the version-specific root.
- **Infrastructure Hierarchical Awareness**:
    - **Template Service**: MUST be configured to dynamically discover and load templates from the versioned hierarchy.
    - **Context Services**: MUST provide hierarchical-aware metadata (breadcrumbs, nav state) that respects the directory mirroring.
    - **UI Routers**: MUST be structured to match the hierarchy, ensuring that HTMX partials and full pages are resolved using the mirrored path logic.
    - **Jinja2 Environment**: MUST use the `ChoiceLoader` or similar mechanism to facilitate multi-version template discovery.
- **Absolute Structural Parity**: This mapping is MANDATORY to ensure 1:1 architectural parity between the Backend and Frontend.
- **Default Entry Point**: `index.html` MUST be the default page for every directory within the Frontend hierarchy.
- **Partials Isolation**: Every Frontend directory MUST contain a `partials/` subdirectory for HTMX-driven dynamic content.
- **Partial Composition**: Partial files MUST:
    - Import and use standardized Interactive Components.
    - OR contain a customized copy of a component from `src/ui/templates/components/generic/` for domain-specific tweaks.

### Generic Component (HEROUI) Workflow Mandate

**GENERIC COMPONENTS FROM HEROUI ARE SCAFFOLDING TOOLS FOR CUSTOMIZATION TO ACHIEVE REACT PARITY.**

- **Component Source**: `src/ui/templates/components/generic/`.
- **Directory Structure**:
    - `react/`: Contains JSX/TSX files from the HEROUI React library. **MANDATORY REFERENCE**.
    - `htmlx/`: Contains "draft" conversions of the React components into HTMLX/Jinja2 format.
- **Workflow Phase**:
    1. Identify a suitable component in the `generic/` directory.
    2. **Review React Reference**: Deeply analyze the `react/` code (JSX/TSX). This is the definitive source for how the component SHOULD look and behave.
    3. **Copy Draft**: Copy the `htmlx/` draft content into the target `index.html` or `partials/` file in the actual app hierarchy (`src/ui/templates/pages/...`).
- **Mandatory Refactoring & Parity Requirement**:
    - **Visual & UX Parity**: The final implementation MUST mirror the **look, feel, styling, and UX** of the React reference exactly.
    - **Macro Integration**: Draft components MUST be refactored to use **Mandatory DaisyUI Macros** to achieve the library-standard appearance.
    - **Service Binding**: All placeholder data MUST be replaced with real data from **UI Services**.
    - **Zero CSS**: Styling MUST adhere to the **Zero CSS Policy** using Tailwind v4 utilities.
- **Generic Template Quality & Reusability**:
    - If any `htmlx` draft template is found to be below the project's quality standards, it MUST be updated at the source or during implementation.
    - Improvements MUST be made in a **generic, templatized structure** (using Jinja2 macros/parameters) to allow for easy reuse with minimal modifications across the entire application.
    - **Rationale**: This is critical to **improve the developer experience (DX)** by providing high-quality starting points and to **ensure total consistency with the platform's UX** standards.
- **Goal**: To leverage HEROUI layouts to build a professional, premium interface that is indistinguishable from a high-quality React application while maintaining a robust, reusable library of server-side component templates that enhance developer productivity.

---

### Navigation & Sidebar Mandate

**THE DYNAMIC SIDEBAR NAVIGATION COMPONENT IS MANDATORY FOR ALL AUTHENTICATED PAGES.**

- **Component Source**: `src/ui/templates/components/interactive/sidebar_nav/sidebar_navigation.html`.
- **Hierarchical Depth**: The sidebar supports a strict 3-level hierarchy:
    - **Level 0 (Root)**: Main platform sections.
    - **Level 1 (Section)**: Items within a specific domain section.
    - **Level 2 (Item)**: Detailed sub-items and operational views.
- **Context Awareness**: The sidebar MUST be driven by the `template_service.py` to ensure:
    - **Dynamic Route Building**: Automatic level detection based on the current URL path.
    - **Active State Highlighting**: Visual feedback for the current location.
    - **Breadcrumb Back Navigation**: Context-aware "Back" buttons for levels 1 and 2.
- **Implementation Requirement**: All authenticated pages MUST extend `base.html` (or equivalent) which includes the `sidebar_navigation` macro. No manual sidebar implementations are permitted.
- **Real-Time Integration**: The sidebar MUST include the integrated system status monitoring (HTMX/SSE) as defined in the component.

### Dashboard Search Mandate

**SEARCH FUNCTIONALITY IS MANDATORY FOR ALL DASHBOARD PAGES.**

- **Component Source**: `src/ui/templates/components/interactive/search/`.
- **Primary Suite**:
    - `interactive_search_controls.html`: MUST be used for filtering, sorting, and grouping.
    - `interactive_search_container.html`: MUST be used for cascading/nested search contexts.
    - `interactive_search_compare.html`: MUST be utilized where multi-pane comparison is required.
- **Integration Requirement**: All pages based on `index_dashboard_template.html` MUST include the standard search/filter toolset.
- **Visual/UX Parity**: Search components MUST adhere to the established styling (DaisyUI + Tailwind v4) and utilize the `interactive_search_mixins.js` for Alpine.js reactive state.
- **Placement**: Search controls MUST be positioned for high visibility, typically nested within an `interactive_panel` or as part of a global header section on dashboards.

### Action Bar Mandate

**ACTION BARS ARE MANDATORY FOR PROVIDING CONTEXT-AWARE CRUD AND OPERATIONAL FUNCTIONALITY.**

- **Component Source**: `src/ui/templates/components/interactive/action_bar/anchored_actions_bar.html`.
- **Purpose**: Action bars MUST be used to provide a consistent interface for functions like Create, Edit, Delete, Save, and other domain-specific operations.
- **Contextual Requirement**: They MUST be configured to be context-aware relative to the page or partial they are imported into, dynamically showing/hiding or enabling/disabling actions based on the user's state or data selection.
- **Standard Positioning**:
    - **Top Anchor**: For primary navigation, page-level actions, and toolbars.
    - **Bottom Anchor**: For form-level actions (Save/Submit), pagination, and footer toolbars.
- **Recursive Usage**: Action bars MUST be used within both Top-Level pages and HTMX Partials to ensure that actions are always available and properly scoped to the current view.
- **Accessibility & UX**: Must support the collapsible behavior and sticky positioning for optimal user experience across all device types (Thumb Zone Optimization).

### Institutional Best Practices Mandate

**ADHERENCE TO THE FOLLOWING BEST PRACTICES DOCUMENTS IS MANDATORY FOR ALL UI DEVELOPMENT.**

- **Architecture & Interaction**:
    - `docs/implementation/best-practices/fastapi-htmx-jinja2-best-practices-2025.md`
    - `docs/implementation/best-practices/web-ui-reactive-components-htmx-jinja2-tailwind-v4-best-practices-2025.md`
- **Styling & Components**:
    - `docs/implementation/best-practices/component-libraries-daisyui-tailwind-v4-best-practices-2025.md`
- **Real-Time & Streaming**:
    - `docs/implementation/best-practices/websockets-server-sent-events-best-practices-2025.md`
    - `docs/implementation/best-practices/streaming-real-time-data-best-practices-2025.md`
- **Security & Identity**:
    - `docs/implementation/best-practices/authentication-authorization-multi-strategy-best-practices-2025.md`
    - `docs/implementation/best-practices/htmlx-csp-css-security-best-practices-2025.md` (**CRITICAL**)

### HTMX CSP & CSS Security Mandate (NON-NEGOTIABLE)

**STRICT ADHERENCE TO HTMX SECURITY AND CSP BEST PRACTICES IS MANDATORY.**

1. **Strict CSP Compliance**:
    - **FORBIDDEN**: The use of `'unsafe-inline'` in `style-src` is strictly prohibited.
    - **MANDATORY**: All CSS MUST be served from external files or via secure, nonce-approved blocks.
2. **HTMX Configuration**:
    - **MANDATORY**: Inline style injection MUST be disabled globally: `htmx.config.includeIndicatorStyles = false`.
    - **MANDATORY**: HTMX indicator and animation styles MUST be included in the compiled project CSS (e.g., via Tailwind plugin).
3. **Nonce-Based Security**:
    - **MANDATORY**: All legitimate inline scripts and styles MUST use a request-specific `nonce` attribute.
    - **MANDATORY**: Nonces MUST be cryptographically secure, generated per request, and safely extracted in the `UITemplateService`.
4. **Build-Time Compilation**:
    - **MANDATORY**: CSS MUST be compiled during build time (Docker/CI-CD). Node.js dependency is strictly for build-time only and MUST NOT exist in production images.

**Public Standards Enforcement**:
In addition to internal docs, the UI MUST enforce industry-standard best practices for **FastAPI**, **HTMX**, **Jinja2**, and **DaisyUI**. This includes:
- Semantic HTML and ARIA compliance.
- DRY (Don't Repeat Yourself) template inheritance.
- CSRF protection for all mutating HTMX requests.
- Progressive enhancement and fallback strategies.

---

### Technical Framework Mandates

#### 🎨 Styling: Tailwind CSS v4 & DaisyUI
- **Zero CSS Policy**: Writing separate CSS files is FORBIDDEN. All custom styles MUST be defined in `src/ui/static/css/tailwind.config.js` or via Tailwind plugin definitions.
- **Utility-First**: Utility classes MUST be used for all layouts, spacing, and typography.
- **Responsive-First**: All components MUST implement mobile-first responsive design using Tailwind's breakpoint prefixes (`sm:`, `md:`, `lg:`, etc.) and `@container` queries for component-level scaling.
- **DaisyUI Primacy**: Use standardized DaisyUI components and themes for all basic UI elements (buttons, inputs, alerts, modals).

#### ⚡ Interaction: HTMX & Alpine.js
- **HTMX First**: All server-side interactions (data fetching, form submission, partial updates, polling) MUST use HTMX attributes (`hx-get`, `hx-post`, `hx-swap`, `hx-target`).
- **Partial Discipline**: Server responses for HTMX requests MUST return partial HTML fragments, not full pages.
- **Alpine.js for Client State**: Use Alpine.js for local UI state (toggles, modals, dropdowns, simple reactivity). Keep client-side logic minimal and declarative.
- **Vanilla JS as Last Resort**: Use vanilla JavaScript ONLY for complex 3rd party integrations (e.g., Chart.js, D3.js) or heavy client-side calculations.
- **Event-Driven UI**: Utilize `hx-trigger` and Alpine.js events (`@click`, `@input`) for all user-triggered actions.

### DaisyUI Macro Mandate

**USE OF DAISYUI MACROS IS MANDATORY FOR ALL STANDARD UI ELEMENTS.**

- **Macro Source**: `src/ui/templates/macros/daisyui/`.
- **Primary Import Path**: `src/ui/templates/macros/daisyui/__init__.html` (re-exports all macros).
- **Universal Import & Usage Requirement**:
    - These macros MUST be imported and utilized by all **HTML pages**, **Components** (generic and interactive), and **Other Macros**.
    - This ensures a recursive and consistent application of the design system throughout the entire template hierarchy.
- **Mandatory Usage**:
    - **Buttons**: MUST use `daisy_button` from `button.html`.
    - **Inputs**: MUST use `daisy_input`, `daisy_textarea`, `daisy_select` etc.
    - **Containers**: MUST use `daisy_card`, `daisy_modal`, `daisy_alert`.
    - **Feedback**: MUST use `daisy_loading`, `daisy_progress`, `daisy_badge`.
- **Philosophy**: All standard HTML elements for which a DaisyUI macro exists MUST use that macro. This ensures accessibility, theme consistency, and structural integrity across the platform.
- **Forbidden Practice**: Writing raw HTML strings for standard UI components (like buttons, modals, or form fields) in any template file, component, or macro is strictly FORBIDDEN.

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
+- a confirmed runtime error
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
+- asyncio.get_running_loop() for background tasks
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

4. **UI Architecture Audit Complete**
   - **Framework**: FastAPI + Jinja2 + Tailwind CSS v4 + HTMX + Alpine.js
   - **Template Pattern**: Standardized 3-level hierarchy (Panel Group → Panel → Card Group) enforced via `index_hub_template.html`.
   - **Infrastructure**: Context-aware rendering via `template_service.py` with automatic navigation and breadcrumb injection.
   - **Compliance**: Adheres to USER_INTERFACE_SPEC v1.0.0 and modern enterprise design standards.
   - **Status**: Ready for implementation/extension.

---

## 📋 STRUCTURED IMPLEMENTATION PLAN CHECKLISTS

### Group 1: Capability Gap Analysis ([Module])
**Status**: ⚪ Pending
**Priority**: P0-CRITICAL
**Description**: Identify missing features in the Web UI compared to the REST API for the target module.

**Items**:
- [ ] Item 1: API Router Analysis
- [ ] Item 2: UI Router Analysis
- [ ] Item 3: Template Structure Mapping

**Validation Criteria**: A documented list of missing UI features and inconsistent structural mappings.

---

### Group 2: UI Implementation & Enhancement (Parity Execution)
**Status**: ⚪ Pending
**Priority**: P1-HIGH
**Description**: Implement and update UI templates and routers to achieve 1:1 mapping.

**Items**:
- [ ] Item 1: Router Implementation
- [ ] Item 2: Template Creation (Index Hub/Dashboard)
- [ ] Item 3: Partial Integration (HTMX endpoints)
- [ ] Item 4: Interactive Component Integration

**Validation Criteria**: Functional Web UI for [Module] that mirrors all backend management features.

---

## 🔄 SESSION STATUS TRACKING

### Phase: Initialization
**Status**: ⚪ Pending
- [ ] Review source endpoints
- [ ] Create Parity SPEC
- [ ] Lock scope

---

## 🎯 SESSION OBJECTIVES

### Primary Objective
Achieve full parity for the [Module], ensuring every management endpoint has a corresponding functional UI element.

### Success Criteria
- [ ] All protocols enforced and validated.

---

## 📌 NOTES

### Session Notes
- [Add notes here]
