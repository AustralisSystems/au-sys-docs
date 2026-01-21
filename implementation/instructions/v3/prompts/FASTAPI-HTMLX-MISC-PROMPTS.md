### webui/20-WebUI_Design_Phase_Tasks.yaml ###
system:
  Load_and_obey:
    ./docs/implementation/instructions/00-Enterprise_Cannonical_Execution_Protocol.yaml and ./docs/implementation/instructions/01-The_GoldenRule_Execution_Protocol.yaml as the canonical framework.

  context:
    ui_instructions:
      - ./docs/implementation/instructions/webui/20-WebUI_Design_Phase_Tasks.yaml
      - ./docs/implementation/instructions/webui/21-WebUI_Component_Mapping_Phase.yaml
 
    ui_design_protocols:
      - ./docs/implementation/instructions/webui/design_system_foundations.md
      - ./docs/implementation/instructions/webui/COLOR_SCHEME_DIRECTIVE.md
      - ./docs/implementation/instructions/webui/responsive_layout_principles.md
      - ./docs/implementation/instructions/webui/openapi_ui_model_conversion_rules.md
      - ./docs/implementation/instructions/webui/motion_transition_spec.md
      - ./docs/implementation/instructions/webui/renderer_mapping_spec.md

     ui_implementation_protocols:
      - ./docs/implementation/instructions/webui/responsive_layout_developer_workflow.md
      - ./docs/implementation/instructions/webui/SCAFFOLDING_LIBRARIES_OVERVIEW.md

    ui_token_protocols:
      - ./docs/implementation/instructions/webuiuniversal_component_mapping_protocol.md
      - ./docs/implementation/instructions/webui/layout_tokens.json
      - ./docs/implementation/instructions/webui/component_tokens.json
      - ./docs/implementation/instructions/webui/tailwind_generator_template.js

  target_paths:

    - ./src/services/ui/templates/pages/core/interactive_sessions
    - ./src/services/ui/templates/pages/core/dashboard


instructions:
  this is a brownfields review of the existing htmlx template, pages, partials, macros, components to align the code and content to our **NEW** standards defined in the `system context` above.
 
goal_description:
  Execute the design phase of web UI development by applying foundational design principles (shadows, depth, responsive layout, color systems, typography, spacing) to the existing codebase. This execution must ensure strict compliance with all standards listed   in   the **Documentation & Enforcement Protocols** section above, with specific focus on `COLOR\_SCHEME\_DIRECTIVE.md`, `universal\_component\_mapping\_protocol.md`, and `responsive\_layout\_principles.md`.

 **Tailwind Configuration**: The `tailwind.config.js` will be regenerated using the logic from `tailwind\_generator\_template.js` and values from `layout\_tokens.json`. This will strictly enforce the new design tokens.

 **CSS Variables**: New CSS variables for colors and shadows will be introduced to support theming and the dual-shadow system.

 **Container Queries**: Layouts will be refactored to use `@container` queries instead of `@media` viewport queries where applicable.

Documentation & Enforcement Protocols:

### UI Instructions
*   **`./docs/implementation/instructions/webui/20-WebUI\_Design\_Phase\_Tasks.yaml`**
    *   **Enforces**: 10-step design phase execution protocol.
    *   **Mandates**: "Load and Obey" protocol for all tasks.
    *   **Requires**: Strict technology stack validation (HTMX > Alpine > Public Libs).
*   **`./docs/implementation/instructions/webui/21-WebUI\_Component\_Mapping\_Phase.yaml`**
    *   **Enforces**: 6-step component mapping workflow.
    *   **Mandates**: Deterministic layout assignments based on field count (1-3: Card, 4-8: Table, etc.).
    *   **Requires**: Dual tokens (primary/secondary) for all components.
    *   **Enforces**: Three-tier visibility hierarchy (Must/Should/Nice to Show).

### UI Design Protocols
*   **`./docs/implementation/instructions/webui/design\_system\_foundations.md`**
    *   **Enforces**: Dual-shadow system (no borders, tonal contrast).
    *   **Mandates**: Colour layering (3-4 tonal variations).
    *   **Requires**: Responsive rearrangement (no shrinking, priority-based reflow).
    *   **Defines**: Palette roles (Primary, Secondary, Neutral, Semantic).
*   **`./docs/implementation/instructions/webui/COLOR\_SCHEME\_DIRECTIVE.md`**
    *   **Prohibits**: Hardcoded colors (`#fff`, `rgb()`), named color utilities (`bg-blue-500`, `text-gray-600`).
    *   **Mandates**: DaisyUI semantic classes (`bg-base-100`, `text-primary`, `btn-success`).
    *   **Requires**: Full theme support (light/dark/custom) and user customization controls.
*   **`./docs/implementation/instructions/webui/responsive\_layout\_principles.md`**
    *   **Enforces**: Container Queries (`@container`) over Media Queries (`@media`).
    *   **Mandates**: Fluid scaling and component rearrangement.
    *   **Requires**: Minimum touch targets (44px) and mobile-first design.
*   **`./docs/implementation/instructions/webui/openapi\_ui\_model\_conversion\_rules.md`**
    *   **Enforces**: Deterministic mapping of OpenAPI types to UI components.
    *   **Defines**: Layout mapping rules (Table -> Cards -> List).
    *   **Mandates**: CRUD operation to UI action mapping (GET->List, POST->Create, etc.).
*   **`./docs/implementation/instructions/webui/motion\_transition\_spec.md`**
    *   **Enforces**: Standard duration tokens (`duration-fast`, `duration-normal`).
    *   **Mandates**: Standard easing curves (`ease-standard`).
    *   **Requires**: Reduced motion support.
*   **`./docs/implementation/instructions/webui/renderer\_mapping\_spec.md`**
    *   **Enforces**: Specific rendering patterns for HTMX vs React.
    *   **Mandates**: Relative paths for router integration.

### UI Implementation Protocols
*   **`./docs/implementation/instructions/webui/responsive\_layout\_developer\_workflow.md`**
    *   **Enforces**: Mobile-First development approach.
    *   **Mandates**: Use of `@tailwindcss/container-queries`.
*   **`./docs/implementation/instructions/webui/SCAFFOLDING\_LIBRARIES\_OVERVIEW.md`**
    *   **Enforces**: Technology Stack Hierarchy (HTMX > Extensions > Alpine > Libs > Custom JS).
    *   **Mandates**: Use of `src\_templates` for HTMX and `react\_component\_libs` for React.
    *   **Prohibits**: Custom code without documented justification.

### UI Token Protocols
*   **`./docs/implementation/instructions/webui/universal\_component\_mapping\_protocol.md`**
    *   **Enforces**: 6-step mapping logic (Metadata -> Context -> Base Type -> Semantic -> Secondary -> Constraints).
    *   **Mandates**: Semantic overrides (e.g., `email` field -> `email\_primary` component).
    *   **Requires**: Dual-token generation for responsive behavior.
*   **`./docs/implementation/instructions/webui/layout\_tokens.json`**
    *   **Defines**: Concrete values for spacing, breakpoints, radius, typography, and motion.
*   **`./docs/implementation/instructions/webui/component\_tokens.json`**
    *   **Defines**: Primary and secondary token mappings for specific components.
*   **`./docs/implementation/instructions/webui/tailwind\_generator\_template.js`**
    *   **Enforces**: Configuration structure for Tailwind to ensure token compliance.


  workflow:
    1. identify and list all files in scope that do not conform to the standards and how they do not conform.
    2. define a remediation plan to remediate and refactor the files one at a time to conform to the new standards.
    3. EXECUTE the remediation plan to remediate and refactor the files, ensuring the 00-Enterprise_Cannonical_Execution_Protocol AND 01-The_GoldenRule_Execution_Protocol are met.




30-WebUI_Refactoring_Phase

System:
  Load and obey ./docs/implementation/instructions/00-Enterprise_Canonical_Execution_Protocol.yaml and ./docs/implementation/instructions/01-The_GoldenRule_Execution_Protocol.yaml as the canonical framework.
  Then execute ./docs/implementation/instructions/webui/30-WebUI_Refactoring_Phase.yaml under those enforced rules.

  context:
    ui_instructions:
      - ./docs/implementation/instructions/webui/30-WebUI_Refactoring_Phase.yaml
      - ./docs/implementation/instructions/webui/20-WebUI_Design_Phase_Tasks.yaml
      - ./docs/implementation/instructions/webui/21-WebUI_Component_Mapping_Phase.yaml
 
    ui_design_protocols:
      - ./docs/implementation/instructions/webui/design_system_foundations.md
      - ./docs/implementation/instructions/webui/COLOR_SCHEME_DIRECTIVE.md
      - ./docs/implementation/instructions/webui/responsive_layout_principles.md
      - ./docs/implementation/instructions/webui/openapi_ui_model_conversion_rules.md
      - ./docs/implementation/instructions/webui/motion_transition_spec.md
      - ./docs/implementation/instructions/webui/renderer_mapping_spec.md

     ui_implementation_protocols:
      - ./docs/implementation/instructions/webui/responsive_layout_developer_workflow.md
      - ./docs/implementation/instructions/webui/SCAFFOLDING_LIBRARIES_OVERVIEW.md

    ui_token_protocols:
      - ./docs/implementation/instructions/webuiuniversal_component_mapping_protocol.md
      - ./docs/implementation/instructions/webui/layout_tokens.json
      - ./docs/implementation/instructions/webui/component_tokens.json
      - ./docs/implementation/instructions/webui/tailwind_generator_template.js

    target_paths:
      - ./src/services/ui/templates/pages/core/api-clients

src\services\ui\templates\pages\core\api-clients

  workflow:
    1. identify and list all files in scope that do not conform to the standards and how they do not conform.
    2. define a remediation plan to remediate and refactor the files one at a time to conform to the new standards.
    3. EXECUTE the remediation plan to remediate and refactor the files, ensuring the 00-Enterprise_Cannonical_Execution_Protocol AND 01-The_GoldenRule_Execution_Protocol are met.



src\services\ui\templates\pages\api_integration

src\services\ui\templates\errors
src\services\ui\templates\pages\auth
src\services\ui\templates\pages\partials




CONTINUE TO SYSTEMATICALLY search for legacy tabs and  REPLACE THE tabs and containers with @interactive_tabs_group.html @interactive_tabs.html @tabs_elements.html  with embedded and @interactive_card_group.html @interactive_card.html ... and @interactive_panel_group.html @interactive_panel.html which can have any type of interactive components...

**Container Queries**: Layouts MUST be refactored to use `@container` queries instead of `@media` viewport queries where applicable.

UI Design Protocols
*   **`./docs/implementation/instructions/webui/design_system_foundations.md`**
    *   **Enforces**: Dual-shadow system (no borders, tonal contrast).
    *   **Requires**: Responsive rearrangement (no shrinking, priority-based reflow).
    *   **Defines**: Palette roles (Primary, Secondary, Neutral, Semantic).
*   **`./docs/implementation/instructions/webui/COLOR_SCHEME_DIRECTIVE.md`**
    *   **Prohibits**: Hardcoded colors (`#fff`, `rgb()`), named color utilities (`bg-blue-500`, `text-gray-600`).
    *   **Mandates**: DaisyUI semantic classes (`bg-base-100`, `text-primary`, `btn-success`).
    *   **Requires**: Full theme support (light/dark/custom) and user customization controls.
*   **`./docs/implementation/instructions/webui/responsive_layout_principles.md`**
    *   **Enforces**: Container Queries (`@container`) over Media Queries (`@media`).
    *   **Mandates**: Fluid scaling and component rearrangement.
    *   **Requires**: Minimum touch targets (44px) and mobile-first design.

ENSURE THE UI DESIGN PROTOCOLS ARE ENFORCED

Refactoring Strategy
1.  **Replace Tabs:** Replace manual `div.tabs` and `a.tab` structures with `interactive_tabs_group` or `interactive_tabs`.
2.  **Replace Cards:** Replace manual `div.card` structures with `interactive_card` or `interactive_card_group`.
3.  **Replace Panels:** Replace complex card layouts or grouped stats with `interactive_panel` or `interactive_panel_group`.
4.  **Migrate Content:** Move existing content into the `content` property of the new components or use the component-specific properties.
5.  **Verify:** Ensure all functionality (switching tabs, interactions) remains intact.


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







webui htmlx and jinja2 template updates
#############################################################################################################################


System:

1. Load and obey the following canonical frameworks immediately:
   - ./docs/implementation/instructions/00-Enterprise_Cannonical_Execution_Protocol.yaml
   - ./docs/implementation/instructions/01-The_GoldenRule_Execution_Protocol.yaml

   These two instruction sets are the authoritative standards governing:
   - All implementation rules,
   - All production-readiness requirements,
   - All naming, structural, architectural, and behavioral constraints,
   - And all Golden Rule compliance rules.

2. Once canonical standards are enforced, execute:
   - ./docs/implementation/instructions/04-Execute_Implementation_Phase_Tasks.yaml

   This governs the implementation actions to be executed during this phase.

---

### SPEC DOCUMENTS REQUIRED FOR EXECUTION

You MUST load, obey, and implement all directives defined in the following SPECs. These documents represent the authoritative production-readiness requirements and the official mandate for backend-first enforcement, ui–backend synchronization, and route/template refactoring.

**MANDATORY SPEC REFERENCES**

1. FOCUS SPEC FILE REFERENCES:
  - ./docs/implementation/in_progress/LLM_MODEL_DISCOVERY_AND_PREFERENCES_SPEC_v1.0.0.md
  - ./docs/implementation/in_progress/HTMX_SSE_WEBSOCKET_INTEGRATION_PATTERNS.md
  - ./docs/implementation/in_progress/ui_REGRESSION_ISSUES_REMEDIATION_SPEC_v1.0.0.md
  - ./docs/implementation/in_progress/LLM_ROUTER_ENHANCEMENTS_SUMMARY.md


3. Implementation Plan:
   - C:\github_development\projects\rest-api-orchestrator\docs\implementation\IMPLEMENTATION_PLAN_v1.0.1.md

You MUST treat these paths and filenames as authoritative. Do not reinterpret, normalize, or alter them in any way.
These SPEC documents define:
- The required ui template structure,
- The router → template mapping rules,
- The backend-first synchronization mandates,
- The DaisyUI/Tailwind v4 theming rules,
- And the production-readiness requirements for htmlx + jinja2 templates.

---

### PRIMARY OBJECTIVE

You MUST review, update, and fully refactor the **htmlx** and **jinja2** templates identified in the SPECs to:

1. **Use the new routers, new functions, and updated codebase** as defined by the SPECs and Implementation Plan.
2. Replace any legacy templates, macros, partials, includes, components, or layout files that:
   - Do not align with the new router architecture,
   - Do not adhere to DaisyUI/Tailwind v4,
   - Contain static content,
   - Contain non-production code.

---

### UI COMPONENT COMPLIANCE REQUIREMENTS

You MUST enforce the following:

#### 1. DaisyUI Component Library Enforcement
- All macros and partials MUST use the correct DaisyUI component patterns from the **@daisyui** directory.
- No custom component variants or overrides unless authorized by SPEC.

#### 2. Interactive Component Enforcement
- All cards, panels, modals, tables, inputs, alerts, drawers, collapsibles, dropdowns, and interactive UI patterns MUST use the standardized **interactive** components from the `@/templates/components` directory.

- No inline HTML that reimplements or duplicates components.
- No custom CSS replacing or overriding component logic.

#### 3. Tailwind v4 + DaisyUI Theme Enforcement
You MUST ensure:
- Full theme compliance,
- Zero custom colors,
- Zero custom CSS,
- Zero arbitrary style attributes,
- Zero deviations from standardized utility classes.

Any violation MUST be documented and remediated in the SPEC.

---

### GOLDEN RULE ENFORCEMENT (CRITICAL)

The following requirements MUST be enforced on **every single htmlx and jinja2 file**, and on all related routers:

1. **0 MOCKS**
2. **0 TODOS**
3. **0 STUBS**
4. **0 PLACEHOLDERS**
5. **0 HARD-CODED VALUES** where dynamic data is expected
6. **0 HARD-CODED SETTINGS** that should be:
   - User-configurable,
   - Environment-configurable,
   - Database-backed,
   - Retrieved from a backend API.

Every template MUST be production-grade **on first pass**, including:
- Data binding,
- Component usage,
- CRUD integration,
- Backend sourcing.

Any template relying on temporary content, scaffolding, or sample data is a **Golden Rule violation** and MUST be refactored.

---

### DATA SOURCE ENFORCEMENT

All data rendered into htmlx or jinja2 templates MUST originate from **valid backend sources**, including:

- REST API responses defined in OpenAPI,
- Database-backed CRUD endpoints,
- Configuration values stored in DB or configuration service.

You MUST eliminate:
- Hard-coded labels,
- Hard-coded table content,
- Hard-coded variable values,
- Static lists,
- Static dropdown entries,
- Fake examples,
- Demo content.

EVERY item MUST map 1:1 to a backend resource, or it violates Golden Rule Protocol.

---

### SPEC TRACKING REQUIREMENT (MANDATORY FOR AUDITING)

You MUST:

- List every template file you touch,
- List every endpoint used,
- List every router involved,
- List every htmlx and jinja2 file refactored,
- Document every CRUD action implemented,
- Track every piece of content created or modified,
- Update the SPEC documents accordingly.

This ensures:
- Full traceability,
- Auditability,
- Confirmed coverage,
- Zero missing endpoints,
- Zero missing CRUD operations.

---

### FINAL COMPLIANCE MANDATE

YOU MUST ENSURE:

- 0 mocks,
- 0 TODOs,
- 0 stub blocks,
- 0 hard-coded values,
- 0 hard-coded settings,
- 0 non-production drafts.

ALL htmlx + jinja2 templates, all routers, all modules, all code, MUST be **PRODUCTION GRADE ON FIRST PASS**, aligned with:

- The SPECs,
- The Implementation Plan,
- The Enterprise Canonical Execution Protocol,
- The Golden Rule Execution Protocol,
- Tailwind v4 standards,
- DaisyUI component library conventions,
- Backend-first / OpenAPI-first architecture.

Non-compliance is NOT permitted under the Golden Rule Execution Protocol.
YOU MUST ENSURE the files and code created for this SPEC are COMPLIANT &  Golden Rule Protocol COMPLIANT

CONTINUE WITH THE PHASES, TASKS ACTIONS AND STEPS IN THE SPEC DOCs.

