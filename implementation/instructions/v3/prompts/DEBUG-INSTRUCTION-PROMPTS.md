# DEBUG INSTRUCTIONS

######################################################################################################################


Base_Directory: docs/implementation/instructions/v2/
File_Extension: .yaml

SPEC_Directory: docs/implementation/in_progress
SPEC_File_Extention: .md

LOAD_AND_PARSE:
  DOCTRINE: "000-DOCTRINE-Enterprise_Canonical_Execution"
  PROTOCOLS:
    - "001-PROTOCOL-The_GoldenRule_Execution"
    - "002-PROTOCOL-Zero_Tolerance_Remediation"
    - "003-PROTOCOL-FastAPI_Pure_Code_Implementation"
    - "004-PROTOCOL-Validate_Remediate_Codebase"

EXECUTE:
Review the following documents to acquire a comprehensive understanding of the fastapi_services_platform:
  - @src/services/fastapi_services_platform/README.md
  - @src/services/fastapi_services_platform/engine/README.md
  - @src/services/fastapi_services_platform/docs/README.md
  - @src/services/fastapi_services_platform/docs/architecture/README.md
These resources provide detailed information and insights into the various components and architectural design of the fastapi_services_platform, which will be essential for thorough knowledge and effective utilization.

Then, HALT

######################################################################################################################


Base_Directory: docs/implementation/instructions/v2/
File_Extension: .yaml

SPEC_Directory: docs/implementation/in_progress
SPEC_File_Extention: .md

LOAD_AND_PARSE:
  DOCTRINE: "000-DOCTRINE-Enterprise_Canonical_Execution"
  PROTOCOLS:
    - "001-PROTOCOL-The_GoldenRule_Execution"
    - "002-PROTOCOL-Zero_Tolerance_Remediation"
    - "003-PROTOCOL-FastAPI_Pure_Code_Implementation"
    - "004-PROTOCOL-Validate_Remediate_Codebase"

ENFORCE:
 - "002-PROTOCOL-Zero_Tolerance_Remediation"
 - "003-PROTOCOL-FastAPI_Pure_Code_Implementation"
 - "004-PROTOCOL-Validate_Remediate_Codebase"

EXECUTE:
  - "204-INSTRUCTIONS-Live-Debugging-and-Remedation"

INPUTS:
Create a "DEBUG_TROUBLESHOOTING_SPEC" document to track this session, by:
 - Copy the "docs\implementation\DEBUG_TROUBLESHOOTING_SPEC_TEMPLATE.md" to the in the directory "docs\implementation\in_progress\debug",
 - Then rename the file for this session
 - MAINTAIN AND UPDATE YOUR PROGRESS IN THE {{ DEBUG_TROUBLESHOOTING_SPEC }}.

Then, Halt


######################################################################################################################


Base_Directory: docs/implementation/instructions/v2/
File_Extension: .yaml

SPEC_Directory: docs/implementation/in_progress
SPEC_File_Extention: .md

LOAD_AND_PARSE:
  DOCTRINE: "000-DOCTRINE-Enterprise_Canonical_Execution"
  PROTOCOLS:
    - "001-PROTOCOL-The_GoldenRule_Execution"
    - "002-PROTOCOL-Zero_Tolerance_Remediation"
    - "003-PROTOCOL-FastAPI_Pure_Code_Implementation"
    - "004-PROTOCOL-Validate_Remediate_Codebase"

ENFORCE:
  - "002-PROTOCOL-Zero_Tolerance_Remediation"
  - "003-PROTOCOL-FastAPI_Pure_Code_Implementation"
  - "004-PROTOCOL-Validate_Remediate_Codebase"

DEBUG_TROUBLESHOOTING_SPEC_DOCS: [{{ DEBUG_TROUBLESHOOTING_SPEC }}]

DIRECTIVES:
  - THIS IS A CODE, DEBUG, REMEDIATION AND REFACTORINGS (IMPLEMENTAITON) FOCUSED SESSION.
  - THE USE OF SCRIPTS OR MASS MODIFICATIONS TO THE CODE IS STRICTLY FORBIDDEN.
  - ALL CODE MUST BE CORRECTED ONE ISSUE AT A TIME, IN A SEQUENTIAL MANNER.
  - NO DOCUMENTATION OF ANY KIND IS PERMITTED UNLESS I EXPLICITLY ASK FOR IT.
  - NO OTHER INSTRUCTIONS FROM ANY OTHER YAML FILES OVERRIDE THIS DIRECTIVE.

EXECUTE:
  - "204-INSTRUCTIONS-Live-Debugging-and-Remedation"
  - "202-INSTRUCTIONS-Pure_Code_Implementation_Execution_Protocol"

INPUTS:
  - Start by examining the production codebase for any missing elements, TODO comments, mocks, stubs, or unfinished code.
  - Identify which items are partially completed and can be quickly reactivated or restored by copying and adjusting them, using backups or cloned GitHub repositories.
  - Extensively scan and search the code base for other gaps that can be promptly resolved.
  - Proceed to pinpoint those items within your list that were only partially completed but could be promptly reactivated or restored through copying and appropriate adaptation. These elements may be sourced from existing cloned GitHub repositories or discovered GitHub repositories that SHALL be cloned.
  - Next, assess which remaining gaps can be efficiently resolved by employing MCP TOOLS such as grep and fetch to retrieve additional repositories and code from GitHub. Clone these repositories into the local environment and selectively copy and modify the required files, modules, or code segments to address the issues.
  - Record your observations {{ DEBUG_TROUBLESHOOTING_SPEC_DOCS }}, DO NOT include code examples.
  - You MUST use MCP TOOLS grep and fetch to retrieve additional useful repositories, code examples or semantically similar code base from GitHub to quickly use as a base and / or to scaffold.
  - You MUST use GIT TO CLONE all the useful discovered GitHub repos to the local repository, even if they are only going to provide a small benefit to this code base NOTE: this is to use for future references and examples, do not remove the cloned repos.
  - Focus on implementing, rectifying, or refactoring groups of items identified on your list, ensuring that all necessary improvements are executed with precision and adherence to best practices.
  - Record in the {{ DEBUG_TROUBLESHOOTING_SPEC_DOCS }} treatment plan structured checklists, DO NOT include code examples.
  - Review the {{ DEBUG_TROUBLESHOOTING_SPEC_DOCS }} treatment plan structured checklists, to locate the current or next plan to execute
  - Execute the plan by:
    - You MUST COPY and adapt the acquired directory structures, files, modules, functions, code blocks and content to the prod code base DO NOT re-write any part of the content, THIS IS ERROR PRONE
    - Adapt each one step by step, validate then continue to the next
    - Continue to implement, fix, remediate and refactor the plan until complete
    - Perform code quality checks
    - Validate the plan has successfully
  - Maintain and update your progress through the plan in the {{ DEBUG_TROUBLESHOOTING_SPEC_DOCS }}
  - Continue to iterate through the plans in the {{ DEBUG_TROUBLESHOOTING_SPEC_DOCS }} until all plans are completed, pass code quality checks and have been validated.

  IF THERE IS A FEATURE, MODULE OR FUNCTION NOT 100% COMPLETE... IS THAT 100% PRODUCTION CODE IMPLEMENTATION ?
  Are there any remaining activities or tasks that require attention?
  Has the production code been fully implemented to meet the standards of enterprise-class production quality with no future or planned tasks, items, or activities?
  If there are pending items, your responsibilities are considered unfulfilled, reflecting a lack of diligence similar to previous efforts.
  All code and content related comments, notes or documentation must be updated accordingly to indicate that the production codebase, specifically within the /src/* directory, must consist of a complete and fully implemented version of all modules, features, functions, utilities and content.
  Additionally, the debugging SPEC document(s) should be revised to reflect your findings, and the production code and documentation files must clearly state if the implementation is incomplete, with a treatment plan to complete the implementation of the code and content to meet the standards of enterprise-class production quality with no future or planned tasks, items, or activities.
  If there are no outstanding activities, tasks, or to-dos, then the current state may be considered complete
  Prompt action is required to address these matters without delay.

Directories:




######################################################################################################################


ENFORCE:
  - "002-PROTOCOL-Zero_Tolerance_Remediation"
  - "003-PROTOCOL-FastAPI_Pure_Code_Implementation"
  - "004-PROTOCOL-Validate_Remediate_Codebase"

EXECUTE:
  - "204-INSTRUCTIONS-Live-Debugging-and-Remedation"
  - "202-INSTRUCTIONS-Pure_Code_Implementation_Execution_Protocol"

DEBUG_TROUBLESHOOTING_SPEC: [docs\implementation\in_progress\debug\INCOMPLETE_CODE_ERADICATION_PLAN_2025-12-22.md,docs\implementation\in_progress\debug\DEBUG_TROUBLESHOOTING_SPEC_2025-12-22_1317.md]

DEBUG_TROUBLESHOOTING_SPEC_DOCS: [{{ DEBUG_TROUBLESHOOTING_SPEC }}]

INPUTS:
  - Continue to iterate through the plans in the {{ DEBUG_TROUBLESHOOTING_SPEC_DOCS }} until all plans are completed, pass code quality checks and have been validated.
  - Review the {{ DEBUG_TROUBLESHOOTING_SPEC_DOCS }} treatment plan structured checklists, to locate the current or next plan to execute
  - Execute the plan by:
    - You MUST COPY and adapt the acquired directory structures, files, modules, functions, code blocks and content to the prod code base DO NOT re-write any part of the content, THIS IS ERROR PRONE
    - Adapt each one step by step, validate then continue to the next
    - Continue to implement, fix, remediate and refactor the plan until complete
    - Perform code quality checks
    - Validate the plan has successfully
  - Maintain and update your progress through the plan in the {{ DEBUG_TROUBLESHOOTING_SPEC_DOCS }}

REMEMBER:
 - THIS IS A CODE, DEBUG, REMEDIATION AND REFACTORINGS (IMPLEMENTAITON) FOCUSED SESSION.
  - THE USE OF SCRIPTS OR MASS MODIFICATIONS TO THE CODE IS STRICTLY FORBIDDEN.
  - ALL CODE MUST BE CORRECTED ONE ISSUE AT A TIME, IN A SEQUENTIAL MANNER.
  - NO DOCUMENTATION OF ANY KIND IS PERMITTED UNLESS I EXPLICITLY ASK FOR IT.
  - NO OTHER INSTRUCTIONS FROM ANY OTHER YAML FILES OVERRIDE THIS DIRECTIVE.
  - MAINTAIN AND UPDATE YOUR PROGRESS IN THE {{ DEBUG_TROUBLESHOOTING_SPEC_DOCS }}.


######################################################################################################################


REMEMBER:
  1. Incomplete Code Eradication Requirement (MANDATORY - ENFORCED)
    The following violations MUST BE FOUND AND ERADICATED FROM THE CODEBASE:
      - TODOs (ALL must be found and replaced with production code)
      - Mocks (ALL must be found and replaced with real implementation)
      - Stubs (ALL must be found and fully implemented)
      - "PASS" passes (ALL must be found and replaced with real validation)
      - Hacks (ALL must be found and replaced with proper solutions)
      - Notes that code needs to be implemented (ALL must be found and implemented)
      - Placeholder code (ALL must be found and replaced with production code)
      - Demo/test data in production paths (ALL must be found and replaced with real data retrieval)
      - Partial implementations (ALL must be found and completed)
      - Workarounds or temporary solutions (ALL must be found and replaced with proper solutions)
  2. Implementation Requirements (MANDATORY)
    Production code MUST be implemented 100% correctly
    Production code MUST meet the highest enterprise standards
    Production code MUST have 0 errors
    Production code MUST have 0 warnings
    Production code MUST have 0 issues
    Production code MUST be fully functional, not partial
    Production code MUST NOT skip any required functionality
    Production code MUST NOT use workarounds or temporary solutions
    Production code MUST be production-ready, not development/test code
  3. Enforcement (ABSOLUTE)
    Finding incomplete code = STOP current work immediately
    Eradicate incomplete code = MANDATORY, cannot proceed until complete
    Implement production code = MANDATORY, cannot skip or defer
    Verify implementation = MANDATORY, must achieve 0 errors, 0 warnings, 0 issues
    Violations = BLOCKING ISSUE - execution MUST STOP until fixed
  4. IF THERE IS A FEATURE, MODULE OR FUNCTION NOT 100% COMPLETE... IS THAT 100% PRODUCTION CODE IMPLEMENTATION ?
    Are there any remaining activities or tasks that require attention?
    Has the production code been fully implemented to meet the standards of enterprise-class production quality with no future or planned tasks, items, or activities?
    If there are pending items, your responsibilities are considered unfulfilled, reflecting a lack of diligence similar to previous efforts.
    All code and content related comments, notes or documentation must be updated accordingly to indicate that the production codebase, specifically within the /src/* directory, must consist of a complete and fully implemented version    of all modules, features, functions, utilities and content.
    Additionally, the debugging SPEC document(s) should be revised to reflect your findings, and the production code and documentation files must clearly state if the implementation is incomplete, with a treatment plan to complete the     implementation of the code and content to meet the standards of enterprise-class production quality with no future or planned tasks, items, or activities.
   If there are no outstanding activities, tasks, or to-dos, then the current state may be considered complete
  5. Prompt action is required to address these matters without delay.



######################################################################################################################


PLAN:
- Confirm that this capability is or SHOULD be incorporated into the fastapi_services_platform feature flags.
- Ensure that the feature flags are added to every .env* file without exception.
- Verify that the code respects the feature flag associated with this capability.
- Make certain that the feature flags adhere to the configurations specified in the .env files.
- Guarantee that all settings are saved persistently within the fastapi_services_platform settings database.
- Ensure that these settings remain configurable during runtime.
- Develop the necessary routes and endpoints to support these functionalities.
- YOU MUST ensure the fastapi_services_platform RUNTIME router factories, services, utilities etc. AND the CONFIG + settings database are fully integrated and dynamically implement the capabilities
- Ensure there is sufficient DEBUG level and INFO, WARNING, ERROR level logging to empower developers and digital llm developer agents to triage, troubleshoot and resolve any issues.

EXECUTE: The PLAN

REMEMBER:
  - THIS IS A CODE, DEBUG, REMEDIATION AND REFACTORINGS (IMPLEMENTAITON) FOCUSED SESSION.
  - THE USE OF SCRIPTS OR MASS MODIFICATIONS TO THE CODE IS STRICTLY FORBIDDEN.
  - ALL CODE MUST BE CORRECTED ONE ISSUE AT A TIME, IN A SEQUENTIAL MANNER.
  - NO DOCUMENTATION OF ANY KIND IS PERMITTED UNLESS I EXPLICITLY ASK FOR IT.
  - NO OTHER INSTRUCTIONS FROM ANY OTHER YAML FILES OVERRIDE THIS DIRECTIVE.
  - MAINTAIN AND UPDATE YOUR PROGRESS IN THE {{ DEBUG_TROUBLESHOOTING_SPEC_DOCS }}.
  - IF THERE IS A FEATURE, MODULE OR FUNCTION NOT 100% COMPLETE... IS THAT 100% PRODUCTION CODE IMPLEMENTATION ?
  - Are there any remaining activities or tasks that require attention?
  - Has the production code been fully implemented to meet the standards of enterprise-class production quality with no future or planned tasks, items, or activities?
  - If there are pending items, your responsibilities are considered unfulfilled, reflecting a lack of diligence similar to previous efforts.
  - Prompt action is required to address these matters without delay.


######################################################################################################################


PLAN:
- Confirm that any of these capabilities is or SHOULD be incorporated into the application / repositories feature flags (NOT fastapi_services_platform feature flags).
- Ensure that the feature flags are added to every .env* file without exception.
- Verify that the code respects the feature flag associated with this capability.
- Make certain that the feature flags adhere to the configurations specified in the .env files.
- Guarantee that all settings are saved persistently within the application settings database.
- Ensure that these settings remain configurable during runtime.
- Develop the necessary routes and endpoints to support these functionalities.
- YOU MUST ensure the application RUNTIME router factories, services, utilities etc. AND the CONFIG + settings database are fully integrated and dynamically implement the capabilities
- Ensure there is sufficient DEBUG level and INFO, WARNING, ERROR level logging to empower developers and digital llm developer agents to triage, troubleshoot and resolve any issues.

EXECUTE: The PLAN

REMEMBER:
  - THIS IS A CODE, DEBUG, REMEDIATION AND REFACTORINGS (IMPLEMENTAITON) FOCUSED SESSION.
  - THE USE OF SCRIPTS OR MASS MODIFICATIONS TO THE CODE IS STRICTLY FORBIDDEN.
  - ALL CODE MUST BE CORRECTED ONE ISSUE AT A TIME, IN A SEQUENTIAL MANNER.
  - NO DOCUMENTATION OF ANY KIND IS PERMITTED UNLESS I EXPLICITLY ASK FOR IT.
  - NO OTHER INSTRUCTIONS FROM ANY OTHER YAML FILES OVERRIDE THIS DIRECTIVE.
  - MAINTAIN AND UPDATE YOUR PROGRESS IN THE {{ DEBUG_TROUBLESHOOTING_SPEC_DOCS }}.
  - IF THERE IS A FEATURE, MODULE OR FUNCTION NOT 100% COMPLETE... IS THAT 100% PRODUCTION CODE IMPLEMENTATION ?
  - Are there any remaining activities or tasks that require attention?
  - Has the production code been fully implemented to meet the standards of enterprise-class production quality with no future or planned tasks, items, or activities?
  - If there are pending items, your responsibilities are considered unfulfilled, reflecting a lack of diligence similar to previous efforts.
  - Prompt action is required to address these matters without delay.


######################################################################################################################


Base_Directory: docs/implementation/instructions/v2/
File_Extension: .yaml

SPEC_Directory: docs/implementation/in_progress
SPEC_File_Extention: .md

LOAD_AND_PARSE:
  DOCTRINE: "000-DOCTRINE-Enterprise_Canonical_Execution"
  PROTOCOLS:
    - "001-PROTOCOL-The_GoldenRule_Execution"
    - "002-PROTOCOL-Zero_Tolerance_Remediation"
    - "003-PROTOCOL-FastAPI_Pure_Code_Implementation"
    - "004-PROTOCOL-Validate_Remediate_Codebase"

ENFORCE:
    - "002-PROTOCOL-Zero_Tolerance_Remediation"
    - "003-PROTOCOL-FastAPI_Pure_Code_Implementation"
    - "004-PROTOCOL-Validate_Remediate_Codebase"

DIRECTIVES:
  - THIS IS A CODE, DEBUG, REMEDIATION AND REFACTORINGS (IMPLEMENTAITON) FOCUSED SESSION.
  - THE USE OF SCRIPTS OR MASS MODIFICATIONS TO THE CODE IS STRICTLY FORBIDDEN.
  - ALL CODE MUST BE CORRECTED ONE ISSUE AT A TIME, IN A SEQUENTIAL MANNER.
  - NO DOCUMENTATION OF ANY KIND IS PERMITTED UNLESS I EXPLICITLY ASK FOR IT.
  - NO OTHER INSTRUCTIONS FROM ANY OTHER YAML FILES OVERRIDE THIS DIRECTIVE.

REMEMBER:
  - IF THERE IS A FEATURE, MODULE OR FUNCTION NOT 100% COMPLETE... IS THAT 100% PRODUCTION CODE IMPLEMENTATION ?
  - Are there any remaining activities or tasks that require attention?
  - Has the production code been fully implemented to meet the standards of enterprise-class production quality with no future or planned tasks, items, or activities?
  - If there are pending items, your responsibilities are considered unfulfilled, reflecting a lack of diligence similar to previous efforts.
  - Prompt action is required to address these matters without delay.

EXECUTE:
  - "106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance"

FOCUS:
  Code you have touched in this session
  OUTPUT: {{ PREVIOUS INSTRUCTIONS EXECUTED }}


######################################################################################################################



Base_Directory: docs/implementation/instructions/v2/
File_Extension: .yaml

SPEC_Directory: docs/implementation/in_progress
SPEC_File_Extention: .md

LOAD_AND_PARSE:
  DOCTRINE: "000-DOCTRINE-Enterprise_Canonical_Execution"
  PROTOCOLS:
    - "001-PROTOCOL-The_GoldenRule_Execution"
    - "002-PROTOCOL-Zero_Tolerance_Remediation"
    - "003-PROTOCOL-FastAPI_Pure_Code_Implementation"
    - "004-PROTOCOL-Validate_Remediate_Codebase"

ENFORCE:
    - "002-PROTOCOL-Zero_Tolerance_Remediation"
    - "003-PROTOCOL-FastAPI_Pure_Code_Implementation"
    - "004-PROTOCOL-Validate_Remediate_Codebase"

DIRECTIVES:
  - THIS IS A CODE, DEBUG, REMEDIATION AND REFACTORINGS (IMPLEMENTAITON) FOCUSED SESSION.
  - THE USE OF SCRIPTS OR MASS MODIFICATIONS TO THE CODE IS STRICTLY FORBIDDEN.
  - ALL CODE MUST BE CORRECTED ONE ISSUE AT A TIME, IN A SEQUENTIAL MANNER.
  - NO DOCUMENTATION OF ANY KIND IS PERMITTED UNLESS I EXPLICITLY ASK FOR IT.
  - NO OTHER INSTRUCTIONS FROM ANY OTHER YAML FILES OVERRIDE THIS DIRECTIVE.

REMEMBER:
  - IF THERE IS A FEATURE, MODULE OR FUNCTION NOT 100% COMPLETE... IS THAT 100% PRODUCTION CODE IMPLEMENTATION ?
  - Are there any remaining activities or tasks that require attention?
  - Has the production code been fully implemented to meet the standards of enterprise-class production quality with no future or planned tasks, items, or activities?
  - If there are pending items, your responsibilities are considered unfulfilled, reflecting a lack of diligence similar to previous efforts.
  - Prompt action is required to address these matters without delay.

EXECUTE:
  - "107-INSTRUCTIONS-Remediate_And_Refactor_Codebase"
  - "203-INSTRUCTIONS-FastAPI_Design_Implementation_Refactor"

FOCUS:
  Code you have touched in this session
  OUTPUT: 106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance


######################################################################################################################
