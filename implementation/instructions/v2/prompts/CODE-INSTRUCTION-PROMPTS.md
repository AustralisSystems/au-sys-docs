# CODE INSTRUCTIONS

######################################################################################################################

CONTEXT: You are starting a new session, and you have been provided with a handover document and some content from the previous session.

READ_AND_REVIEW:
  - the handover document
  - the CODE_IMPLEMENTATION_SPEC and/or DEBUG_TROUBLESHOOTING_SPEC
  - the provided content from the previous session

DOCUMENTS:


then HALT

######################################################################################################################


Base_Directory: docs/implementation/instructions/v2/
File_Extension: .yaml

SPEC_Directory: docs/implementation/in_progress
SPEC_File_Extention: .md

PROTOCOLS:
  - "001-PROTOCOL-The_GoldenRule_Execution"
  - "002-PROTOCOL-Zero_Tolerance_Remediation"
  - "003-PROTOCOL-FastAPI_Pure_Code_Implementation"
  - "004-PROTOCOL-Validate_Remediate_Codebase"
  - "006-PROTOCOL-RFC2119_Requirements_Language"

ENFORCE:
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

LOAD_AND_ENFORCE:
  DOCTRINE: "000-DOCTRINE-Enterprise_Canonical_Execution"

LOAD_AND_ENFORCE:
  - "001-PROTOCOL-The_GoldenRule_Execution"
  - "002-PROTOCOL-Zero_Tolerance_Remediation"
  - "003-PROTOCOL-FastAPI_Pure_Code_Implementation"
  - "004-PROTOCOL-Validate_Remediate_Codebase"
  - "006-PROTOCOL-RFC2119_Requirements_Language"

LOAD_AND_ENFORCE:
  - "002-PROTOCOL-Zero_Tolerance_Remediation"
  - "003-PROTOCOL-FastAPI_Pure_Code_Implementation"
  - "004-PROTOCOL-Validate_Remediate_Codebase"

LOAD_AND_EXECUTE:
  - "104-INSTRUCTIONS-Execute_Implementation_Phase_Tasks"
  - "202-INSTRUCTIONS-Pure_Code_Implementation_Execution_Protocol"
  - "203-INSTRUCTIONS-FastAPI_Design_Implementation_Refactor"

INPUTS:
Create a "CODE_IMPLEMENTATION_SPEC" document to track this session, by:
following the instructions and examples from:
  - "docs\implementation\SPEC_TEMPLATE_v1.0.0.md"
  - "docs\implementation\SPEC_CREATION_GUIDE_v1.0.0.md"

- Copy the "docs\implementation\CODE_IMPLEMENTATION_SPEC_TEMPLATE.md" to the directory "docs\implementation\in_progress\"  DO NOT RE-WRITE IT,
- Then rename the file for this session and include a date stamp suffix in the name
- MAINTAIN AND UPDATE YOUR PROGRESS IN THE {{ CODE_IMPLEMENTATION_SPEC }}.

Then, Halt



- Copy the "docs\implementation\CODE_IMPLEMENTATION_SPEC_TEMPLATE.md" to the directory "docs\implementation\in_progress\"  DO NOT RE-WRITE IT,
- Copy the "docs\implementation\WEB_APP_CODE_SPEC_TEMPLATE_v1.0.0.md" to the directory "docs\implementation\in_progress\"  DO NOT RE-WRITE IT,


######################################################################################################################



for this CODE SPEC you are going to use the instructions and scripts to discover, extract, standardise and prepare the services and features from this dir ... "C:\github_development\AustralisSystems\apps\digital-angels\src\services" .... YOU MUST ENSURE THAT YOU DO NOT OVER-WRITE ANY EXISTING SERVICES IN THE library python services here "C:\github_development\AustralisSystems\libraries\python\services" ... if there is a dir name that clashes, create a similar name to ensure that its clear what the source of the service was. .... update the CODE SPEC doc with this detail, then halt





LOAD_AND_EXECUTE:
  - C:\github_development\AustralisSystems\libraries\_ai_agent\instructions\205-PROTOCOL-Sovereign_Capability_Construction-v1.1.0.yaml
  - C:\github_development\AustralisSystems\libraries\_ai_agent\instructions\003-INSTRUCTION-Service_Extraction_and_Integration-v1.0.0.yaml

DIRECTIVE: Proceed and do not wait for approval during the 003 steps, consider this the approval.

TARGETS:
 - C:\github_development\AustralisSystems\apps\digital-angels\src\services\api_client
 - C:\github_development\AustralisSystems\apps\digital-angels\src\services\auth
 - C:\github_development\AustralisSystems\apps\digital-angels\src\services\aws
 - C:\github_development\AustralisSystems\apps\digital-angels\src\services\celery
 - C:\github_development\AustralisSystems\apps\digital-angels\src\services\config
 - C:\github_development\AustralisSystems\apps\digital-angels\src\services\conversion
 - C:\github_development\AustralisSystems\apps\digital-angels\src\services\discovery
 - C:\github_development\AustralisSystems\apps\digital-angels\src\services\feature_flags

 - C:\github_development\AustralisSystems\apps\digital-angels\src\services\google
 - C:\github_development\AustralisSystems\apps\digital-angels\src\services\graphql
 - C:\github_development\AustralisSystems\apps\digital-angels\src\services\integration
 - C:\github_development\AustralisSystems\apps\digital-angels\src\services\logging

 - C:\github_development\AustralisSystems\apps\digital-angels\src\services\microsoft
 - C:\github_development\AustralisSystems\apps\digital-angels\src\services\monitoring
 - C:\github_development\AustralisSystems\apps\digital-angels\src\services\notifications
 - C:\github_development\AustralisSystems\apps\digital-angels\src\services\optimization

 - C:\github_development\AustralisSystems\apps\digital-angels\src\services\providers
 - C:\github_development\AustralisSystems\apps\digital-angels\src\services\redis_cache
 - C:\github_development\AustralisSystems\apps\digital-angels\src\services\runtime
 - C:\github_development\AustralisSystems\apps\digital-angels\src\services\secrets

 - C:\github_development\AustralisSystems\apps\digital-angels\src\services\security
 - C:\github_development\AustralisSystems\apps\digital-angels\src\services\sessions
 - C:\github_development\AustralisSystems\apps\digital-angels\src\services\shared
 - C:\github_development\AustralisSystems\apps\digital-angels\src\services\storage
 - C:\github_development\AustralisSystems\apps\digital-angels\src\services\sync
 - C:\github_development\AustralisSystems\apps\digital-angels\src\services\system
 - C:\github_development\AustralisSystems\apps\digital-angels\src\services\websocket


LOAD_AND_EXECUTE:
  - C:\github_development\AustralisSystems\libraries\_ai_agent\instructions\205-PROTOCOL-Sovereign_Capability_Construction-v1.1.0.yaml
  - C:\github_development\AustralisSystems\libraries\_ai_agent\instructions\003-INSTRUCTION-Service_Extraction_and_Integration-v1.0.0.yaml

DIRECTIVE: Proceed and do not wait for approval during the 003 steps, consider this the approval.

TARGETS:
 - C:\github_development\AustralisSystems\apps\digital-angels\src\services\security
 - C:\github_development\AustralisSystems\apps\digital-angels\src\services\sessions
 - C:\github_development\AustralisSystems\apps\digital-angels\src\services\shared



REMEMBER:
  - "Use the scripts in this directory "C:\github_development\AustralisSystems\libraries\_ai_agent\tools" to fast track the process"





CONTINUE WITH THE CURRENT {{ CODE_IMPLEMENTATION_SPEC }}
REMEMBER:
  - "Use the scripts in this directory "C:\github_development\AustralisSystems\libraries\_ai_agent\tools" to fast track the process"
  - MAINTAIN AND UPDATE YOUR PROGRESS IN THE {{ CODE_IMPLEMENTATION_SPEC }}.

CODE_IMPLEMENTATION_SPEC:C:\github_development\AustralisSystems\docs\implementation\in_progress\CODE_IMPLEMENTATION_SPEC_20260113.md

CODE_IMPLEMENTATION_SPEC: C:\github_development\AustralisSystems\docs\implementation\in_progress\CODE_IMPLEMENTATION_SPEC_20260113_005422.md


CODE_IMPLEMENTATION_SPEC:C:\github_development\AustralisSystems\docs\implementation\in_progress\CODE_IMPLEMENTATION_SPEC_20260113.md

DIRECTIVE:
  - THIS IS A CODE IMPLEMENTAITON, REFACTORING AND VALIDATION FOCUSED SESSION.
  - THE USE OF SCRIPTS OR MASS MODIFICATIONS TO THE CODE IS STRICTLY FORBIDDEN.
  - ALL CODE MUST BE IMPLEMENTED ONE STEP AT A TIME, IN A SEQUENTIAL MANNER.
  - NO DOCUMENTATION OF ANY KIND IS PERMITTED UNLESS I EXPLICITLY ASK FOR IT.

LOAD_AND_EXECUTE:
  - "C:\github_development\AustralisSystems\libraries\_ai_agent\instructions\003-INSTRUCTION-Service_Extraction_and_Integration-v1.0.0.yaml"
  - CONTINUE WITH THE CURRENT {{ CODE_IMPLEMENTATION_SPEC }} ...
  - Continue to iterate through the plans in the {{ CODE_IMPLEMENTATION_SPEC }} until all plans are completed, pass code quality checks and have been validated

REMEMBER:
  - "Use the scripts in this directory "C:\github_development\AustralisSystems\libraries\_ai_agent\tools" to fast track the process"
  - MAINTAIN AND UPDATE YOUR PROGRESS IN THE {{ CODE_IMPLEMENTATION_SPEC }}.


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
    - "006-PROTOCOL-RFC2119_Requirements_Language"

ENFORCE:
  - "002-PROTOCOL-Zero_Tolerance_Remediation"
  - "003-PROTOCOL-FastAPI_Pure_Code_Implementation"
  - "004-PROTOCOL-Validate_Remediate_Codebase"


REMEMBER:
  - USE MCP TOOLS CONTEXT7 AND MCP TOOLS GREP.
  - SCAFFOLD THE CURRENT CODE FROM THE REF CODEBASES FIRST.
  - THEN, COPY THE FILES FORM THE REF REPOS.
  - THEN, ADAPT TO THE DESTINATION CODEBASE.

EXECUTE: "205-INSTRUCTIONS-Scaffolding_Prioritization_Comparative_Selection-v2.0.0"

INPUTS:




######################################################################################################################


MANDATE:
  ALL INSCOPE CODE IN THIS CODEBASE MUST COMPLY WITH THE FOLLOWING:
    - SOLID Principles
    - DRY (Don't Repeat Yourself)
    - KISS (Keep It Simple, Stupid)
    - YAGNI (You Ain't Gonna Need It)

  ALL INSCOPE CODE IN THIS CODEBASE MUST COMPLY WITH THE FOLLOWING CODING PRACTICES:
    - extensible
    - modular
    - idempotent
    - responsive
    - resilient
    - adaptable
    - loose coupling
    - singleton patterns
    - factory patterns
    - decorator patterns
    - observer patterns
    - pooling patterns
    - fastapi best practice code and dir structures
    - python code best practices
    - ansync io non blocking patterns



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
   - Shims (ALL must be found, removed and the code replaced or updated to use the proper solutions)
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
   All code and content related comments, notes or documentation must be updated accordingly to indicate that the production codebase, specifically within the /src/* directory, must consist of a complete and fully implemented version of all modules, features, functions, utilities and content.
   Additionally, the debugging SPEC document(s) should be revised to reflect your findings, and the production code and documentation files must clearly state if the implementation is incomplete, with a treatment plan to complete the implementation of the code and content to meet the standards of enterprise-class production quality with no future or planned tasks, items, or activities.
   If there are no outstanding activities, tasks, or to-dos, then the current state may be considered complete
5. Prompt action is required to address these matters without delay.



######################################################################################################################


Base_Directory: docs/implementation/instructions/v2/
File_Extension: .yaml

SPEC_Directory: docs/implementation/in_progress
SPEC_File_Extention: .md

CODE_IMPLEMENTATION_SPEC_DOCS: "The provided CODE SPEC document(s) and OTHER document(s) provided in this instruction SHALL BE YOUR ONLY FOCUS."

LOAD_AND_EXECUTE:
  DOCTRINE: "000-DOCTRINE-Enterprise_Canonical_Execution"

LOAD_AND_EXECUTE::
  PROTOCOLS:
    - "001-PROTOCOL-The_GoldenRule_Execution"
    - "002-PROTOCOL-Zero_Tolerance_Remediation"
    - "003-PROTOCOL-FastAPI_Pure_Code_Implementation"
    - "004-PROTOCOL-Validate_Remediate_Codebase"
    - "006-PROTOCOL-RFC2119_Requirements_Language"

DIRECTIVES:
  - THIS IS A CODE IMPLEMENTAITON, REFACTORING AND VALIDATION FOCUSED SESSION.
  - THE USE OF SCRIPTS OR MASS MODIFICATIONS TO THE CODE IS STRICTLY FORBIDDEN.
  - ALL CODE MUST BE CORRECTED ONE ISSUE AT A TIME, IN A SEQUENTIAL MANNER.
  - NO DOCUMENTATION OF ANY KIND IS PERMITTED UNLESS I EXPLICITLY ASK FOR IT.
  - NO OTHER INSTRUCTIONS FROM ANY OTHER YAML FILES OVERRIDE THIS DIRECTIVE.
  - MAINTAIN AND UPDATE YOUR PROGRESS IN THE {{ CODE_IMPLEMENTATION_SPEC_DOCS }}.
  - THIS IS A FULL RE-WRITE.

LOAD_AND_EXECUTE:
  - "104-INSTRUCTIONS-Execute_Implementation_Phase_Tasks"
    INPUTS: {{ CODE_IMPLEMENTATION_SPEC_DOCS }}


---

EXECUTE:
  - "104-INSTRUCTIONS-Execute_Implementation_Phase_Tasks"
    INPUTS: {{ CODE_IMPLEMENTATION_SPEC_DOCS }}

EXECUTE:
  - "203-INSTRUCTIONS-FastAPI_Design_Implementation_Refactor"
    INPUTS: {{ CODE_IMPLEMENTATION_SPEC_DOCS }}

EXECUTE:
  - "204-INSTRUCTIONS-Live-Debugging-and-Remedation"
    INPUTS: {{ CODE_IMPLEMENTATION_SPEC_DOCS }}



######################################################################################################################


Base_Directory: docs/implementation/instructions/v2/
File_Extension: .yaml

SPEC_Directory: docs/implementation/in_progress
SPEC_File_Extention: .md

# DEFINE THE CODE SPEC FILES HERE
CODE_IMPLEMENTATION_SPEC_DOCS: [{{ CODE_IMPLEMENTATION_SPEC }}]

LOAD_AND_PARSE:
  DOCTRINE: "000-DOCTRINE-Enterprise_Canonical_Execution"

  PROTOCOLS:
    - "001-PROTOCOL-The_GoldenRule_Execution"
    - "002-PROTOCOL-Zero_Tolerance_Remediation"
    - "003-PROTOCOL-FastAPI_Pure_Code_Implementation"
    - "004-PROTOCOL-Validate_Remediate_Codebase"
    - "006-PROTOCOL-RFC2119_Requirements_Language"

ENFORCE:
  - "002-PROTOCOL-Zero_Tolerance_Remediation"
  - "003-PROTOCOL-FastAPI_Pure_Code_Implementation"
  - "004-PROTOCOL-Validate_Remediate_Codebase"

DIRECTIVES:
- THIS IS A CODE IMPLEMENTAITON, REFACTORING AND VALIDATION FOCUSED SESSION.
- THE USE OF SCRIPTS OR MASS MODIFICATIONS TO THE CODE IS STRICTLY FORBIDDEN.
- ALL CODE MUST BE CORRECTED ONE ISSUE AT A TIME, IN A SEQUENTIAL MANNER.
- NO DOCUMENTATION OF ANY KIND IS PERMITTED UNLESS I EXPLICITLY ASK FOR IT.
- NO OTHER INSTRUCTIONS FROM ANY OTHER YAML FILES OVERRIDE THIS DIRECTIVE.

EXECUTE:
  - "104-INSTRUCTIONS-Execute_Implementation_Phase_Tasks"
  - "202-INSTRUCTIONS-Pure_Code_Implementation_Execution_Protocol"
  - "203-INSTRUCTIONS-FastAPI_Design_Implementation_Refactor"




INPUTS:
- Start by examining the production codebase for any missing elements, TODO comments, mocks, stubs, or unfinished code.
- Identify which items are partially completed and can be quickly reactivated or restored by copying and adjusting them, using backups or cloned GitHub repositories.
- Extensively scan and search the code base for other gaps that can be promptly resolved.
- Proceed to pinpoint those items within your list that were only partially completed but could be promptly reactivated or restored through copying and appropriate adaptation. These elements may be sourced from existing cloned GitHub repositories or discovered GitHub repositories that SHALL be cloned.
- Next, assess which remaining gaps can be efficiently resolved by employing MCP TOOLS such as grep and fetch to retrieve additional repositories and code from GitHub. Clone these repositories into the local environment and selectively copy and modify the required files, modules, or code segments to address the issues.
- Record your observations {{ CODE_IMPLEMENTATION_SPEC_DOCS }}, DO NOT include code examples.
- You MUST use MCP TOOLS grep and fetch to retrieve additional useful repositories, code examples or semantically similar code base from GitHub to quickly use as a base and / or to scaffold.
- You MUST use GIT TO CLONE all the useful discovered GitHub repos to the local repository, even if they are only going to provide a small benefit to this code base NOTE: this is to use for future references and examples, do not remove the cloned repos.
- Focus on implementing, rectifying, or refactoring groups of items identified on your list, ensuring that all necessary improvements are executed with precision and adherence to best practices.
- Record in the {{ CODE_IMPLEMENTATION_SPEC_DOCS }} treatment plan structured checklists, DO NOT include code examples.
- Review the {{ CODE_IMPLEMENTATION_SPEC_DOCS }} treatment plan structured checklists, to locate the current or next plan to execute
- Execute the plan by:
  - You MUST COPY and adapt the acquired directory structures, files, modules, functions, code blocks and content to the prod code base DO NOT re-write any part of the content, THIS IS ERROR PRONE
  - Adapt each one step by step, validate then continue to the next
  - Continue to implement, fix, remediate and refactor the plan until complete
  - Perform code quality checks
  - Validate the plan has successfully
- Maintain and update your progress through the plan in the {{ CODE_IMPLEMENTATION_SPEC_DOCS }}
- Continue to iterate through the plans in the {{ CODE_IMPLEMENTATION_SPEC_DOCS }} until all plans are completed, pass code quality checks and have been validated.

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

**CODE_SPEC_DOC**

CODE_IMPLEMENTATION_SPEC_DOCS: `docs\implementation\in_progress\AI_AGENT_PIPELINE_SPEC_v1.0.1.md and docs\implementation\in_progress\2026-01-03-CODE_IMPLEMENTATION_SPEC.md`

CODE_IMPLEMENTATION_SPEC_DOCS:

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
    - "006-PROTOCOL-RFC2119_Requirements_Language"

ENFORCE:
  - "002-PROTOCOL-Zero_Tolerance_Remediation"
  - "003-PROTOCOL-FastAPI_Pure_Code_Implementation"
  - "004-PROTOCOL-Validate_Remediate_Codebase"

EXECUTE:
  - "104-INSTRUCTIONS-Execute_Implementation_Phase_Tasks"
  - "202-INSTRUCTIONS-Pure_Code_Implementation_Execution_Protocol"
  - "203-INSTRUCTIONS-FastAPI_Design_Implementation_Refactor"

**IMPORTANT**
  - All db access and operations MUST be performed by the storage factory, and are the responsibility of the storage factory.
  - SQLAlchemy ORM MUST be fully integrated and are the responsibility of the storage factory.
  - Beanie ODM MUST be fully integrated and are the responsibility of the storage factory.

**IMPORTANT**
  The Logger Factory MUST be used for all standard logging for the codebase.
  Implement for all: modules, functions and content to use the Logger Factory for all standard logging.
  Implement the diagnostics logger to do the debug and troubleshooting level logging for:
    - operations
    - transactions
    - data in and data out

  YOU MUST ENSURE the logger factory and diagnostics logger implementation for the in scope SPEC greatly simplify the production validation of this feature and capability.

REMEMBER:
  - THIS IS A CODE IMPLEMENTAITON, REFACTORING AND VALIDATION FOCUSED SESSION.
  - THE USE OF SCRIPTS OR MASS MODIFICATIONS TO THE CODE IS STRICTLY FORBIDDEN.
  - ALL CODE MUST BE IMPLEMENTED ONE STEP AT A TIME, IN A SEQUENTIAL MANNER.
  - NO DOCUMENTATION OF ANY KIND IS PERMITTED UNLESS I EXPLICITLY ASK FOR IT.
  - NO OTHER INSTRUCTIONS FROM ANY OTHER YAML FILES OVERRIDE THIS DIRECTIVE.
  - MAINTAIN AND UPDATE YOUR PROGRESS IN THE {{ CODE_IMPLEMENTATION_SPEC_DOCS }}.

INPUTS:
  - Review the {{ CODE_IMPLEMENTATION_SPEC_DOCS }} implmentation plans and structured checklists, to locate the current or next plan to execute
  - Execute the plan by:
    - You MUST COPY and adapt the acquired directory structures, files, modules, functions, code blocks and content to the prod code base DO NOT re-write any part of the content, THIS IS ERROR PRONE
    - Adapt each one step by step, validate then continue to the next
    - Continue to implement, fix, remediate and refactor the plan until complete
    - Perform code quality checks
    - Validate the plan has successfully
    - Maintain and update your progress through the plan in the {{ CODE_IMPLEMENTATION_SPEC_DOCS }}
  - Continue to iterate through the plans in the {{ CODE_IMPLEMENTATION_SPEC_DOCS }} until all plans are completed, pass code quality checks and have been validated.


######################################################################################################################


DIRECTIVE:
  - THIS IS A CODE IMPLEMENTAITON, REFACTORING AND VALIDATION FOCUSED SESSION.
  - THE USE OF SCRIPTS OR MASS MODIFICATIONS TO THE CODE IS STRICTLY FORBIDDEN.
  - ALL CODE MUST BE IMPLEMENTED ONE STEP AT A TIME, IN A SEQUENTIAL MANNER.
  - NO DOCUMENTATION OF ANY KIND IS PERMITTED UNLESS I EXPLICITLY ASK FOR IT.
  - NO OTHER INSTRUCTIONS FROM ANY OTHER YAML FILES OVERRIDE THIS DIRECTIVE.
  - MAINTAIN AND UPDATE YOUR PROGRESS IN THE {{ CODE_IMPLEMENTATION_SPEC_DOCS }}.

EXECUTE:
  Continue to iterate through the plans in the {{ CODE_IMPLEMENTATION_SPEC_DOCS }} until all plans are completed, pass code quality checks and have been validated


######################################################################################################################

PLAN:
  - Confirm that this capability is or SHOULD be incorporated into the fastapi_services_platform feature flags.
  - Verify that the code respects the feature flag associated with this capability.
  - Make certain that the feature flags adhere to the configurations specified in the .env files.
  - Guarantee that all settings are saved persistently within the fastapi_services_platform settings database.
  - Ensure that these settings remain configurable during runtime.
  - Develop the necessary routes and endpoints to support these functionalities.
  - YOU MUST ensure the fastapi_services_platform RUNTIME router factories, services, utilities etc. AND the CONFIG + settings database are fully integrated and dynamically implement the capabilities
  - Ensure there is sufficient DEBUG level and INFO, WARNING, ERROR level logging to empower developers and digital llm developer agents to triage, troubleshoot and resolve any issues.

EXECUTE: The PLAN

REMEMBER:
  - THIS IS A CODE IMPLEMENTAITON, REFACTORING AND VALIDATION FOCUSED SESSION.
  - THE USE OF SCRIPTS OR MASS MODIFICATIONS TO THE CODE IS STRICTLY FORBIDDEN.
  - ALL CODE MUST BE IMPLEMENTED ONE STEP AT A TIME, IN A SEQUENTIAL MANNER.
  - NO DOCUMENTATION OF ANY KIND IS PERMITTED UNLESS I EXPLICITLY ASK FOR IT.
  - NO OTHER INSTRUCTIONS FROM ANY OTHER YAML FILES OVERRIDE THIS DIRECTIVE.
  - MAINTAIN AND UPDATE YOUR PROGRESS IN THE {{ CODE_IMPLEMENTATION_SPEC_DOCS }}.
  - IF THERE IS A FEATURE, MODULE OR FUNCTION NOT 100% COMPLETE... IS THAT 100% PRODUCTION CODE IMPLEMENTATION ?
  - Are there any remaining activities or tasks that require attention?
  - Has the production code been fully implemented to meet the standards of enterprise-class production quality with no future or planned tasks, items, or activities?
  - If there are pending items, your responsibilities are considered unfulfilled, reflecting a lack of diligence similar to previous efforts.
  - Prompt action is required to address these matters without delay.

######################################################################################################################

PLAN:

- Confirm that any of these capabilities is or SHOULD be incorporated into the application / repositories feature flags (NOT fastapi_services_platform feature flags).
- Verify that the code respects the feature flag associated with this capability.
- Make certain that the feature flags adhere to the configurations specified in the .env files.
- Guarantee that all settings are saved persistently within the application settings database.
- Ensure that these settings remain configurable during runtime.
- Develop the necessary routes and endpoints to support these functionalities.
- YOU MUST ensure the application RUNTIME router factories, services, utilities etc. AND the CONFIG + settings database are fully integrated and dynamically implement the capabilities
- Ensure there is sufficient DEBUG level and INFO, WARNING, ERROR level logging to empower developers and digital llm developer agents to triage, troubleshoot and resolve any issues.

EXECUTE: The PLAN

REMEMBER:

- THIS IS A CODE IMPLEMENTAITON, REFACTORING AND VALIDATION FOCUSED SESSION.
- THE USE OF SCRIPTS OR MASS MODIFICATIONS TO THE CODE IS STRICTLY FORBIDDEN.
- ALL CODE MUST BE IMPLEMENTED ONE STEP AT A TIME, IN A SEQUENTIAL MANNER.
- NO DOCUMENTATION OF ANY KIND IS PERMITTED UNLESS I EXPLICITLY ASK FOR IT.
- NO OTHER INSTRUCTIONS FROM ANY OTHER YAML FILES OVERRIDE THIS DIRECTIVE.
- MAINTAIN AND UPDATE YOUR PROGRESS IN THE {{ CODE_IMPLEMENTATION_SPEC_DOCS }}.
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
    - "006-PROTOCOL-RFC2119_Requirements_Language"

ENFORCE:
  - "002-PROTOCOL-Zero_Tolerance_Remediation"
  - "003-PROTOCOL-FastAPI_Pure_Code_Implementation"
  - "004-PROTOCOL-Validate_Remediate_Codebase"

DIRECTIVE:
- THIS IS A CODE IMPLEMENTATION AND REFACTORINGS FOCUSED SESSION.
- THE USE OF SCRIPTS OR MASS MODIFICATIONS TO THE CODE IS STRICTLY FORBIDDEN.
- ALL CODE MUST BE IMPLEMENTATION AND VALIDATED ONE STEP AT A TIME, IN A SEQUENTIAL MANNER.
- NO DOCUMENTATION OF ANY KIND IS PERMITTED UNLESS I EXPLICITLY ASK FOR IT.
- NO OTHER INSTRUCTIONS FROM ANY OTHER YAML FILES OVERRIDE THIS DIRECTIVE.

INPUTS:
  - Start by examining the production codebase for any missing elements, TODO comments, mocks, stubs, or unfinished code.
  - Identify which items are partially completed and can be quickly implemented by copying and adjusting them, using local repositories or cloned GitHub repositories.
  - Extensively scan and search the code base for other gaps that can be promptly resolved.
  - Proceed to pinpoint those items within your list that were only partially completed but could be promptly reactivated or restored through copying and appropriate adaptation. These elements should be sourced from existing cloned GitHub repositories or discovered GitHub repositories that SHALL be cloned.
  - Next, assess which remaining gaps can be efficiently resolved by employing MCP TOOLS such as grep and fetch to retrieve additional repositories and code from GitHub.
  - Clone these repositories into the local environment and selectively copy and modify the required files, modules, or code segments to address the issues.
  - Record your planning in {{ CODE_IMPLEMENTATION_SPEC_DOCS }}, DO NOT include code examples.
  - You MUST use MCP TOOLS grep and fetch to retrieve additional useful repositories, code examples or semantically similar code base from GitHub to quickly use as a base and / or to scaffold.
  - You MUST use GIT TO CLONE all the useful discovered GitHub repos to the local repository, even if they are only going to provide a small benefit to this code base NOTE: this is to use for future references and examples, do not remove the cloned repos.
  - Focus on implementing, refactoring and validating groups of items identified on your list, ensuring that all necessary improvements are executed with precision and adherence to best practices.
  - Record in the {{ CODE_IMPLEMENTATION_SPEC_DOCS }} implementation plan structured checklists, DO NOT include code examples.
  - Review the {{ CODE_IMPLEMENTATION_SPEC_DOCS }} implementation plan structured checklists, to locate the current or next plan to execute
  - Execute the plan by:
    - You MUST COPY and adapt the acquired directory structures, files, modules, functions, code blocks and content to the prod code base DO NOT re-write any part of the content, THIS IS ERROR PRONE
    - Adapt each one step by step, validate then continue to the next
    - Continue to implement, fix, remediate and refactor the plan until complete
    - Perform code quality checks
    - Validate the plan has successfully
  - Maintain and update your progress through the plan in the {{ CODE_IMPLEMENTATION_SPEC_DOCS }}

EXECUTE:
  Continue to iterate through the plans in the {{ CODE_IMPLEMENTATION_SPEC_DOCS }} until all plans are completed, pass code quality checks and have been validated.



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
    - "006-PROTOCOL-RFC2119_Requirements_Language"

ENFORCE:
  - "002-PROTOCOL-Zero_Tolerance_Remediation"
  - "003-PROTOCOL-FastAPI_Pure_Code_Implementation"
  - "004-PROTOCOL-Validate_Remediate_Codebase"

DIRECTIVES:
  - THIS IS A CODE IMPLEMENTAITON, REFACTORING AND VALIDATION FOCUSED SESSION.
  - THE USE OF SCRIPTS OR MASS MODIFICATIONS TO THE CODE IS STRICTLY FORBIDDEN.
  - ALL CODE MUST BE IMPLEMENTED ONE STEP AT A TIME, IN A SEQUENTIAL MANNER.
  - NO DOCUMENTATION OF ANY KIND IS PERMITTED UNLESS I EXPLICITLY ASK FOR IT.
  - NO OTHER INSTRUCTIONS FROM ANY OTHER YAML FILES OVERRIDE THIS DIRECTIVE.

REMEMBER:
  - PERFORM ALL CODE QUALITY CHECKS INCLUDING AST AND COMPILE
  - IF THERE IS A FEATURE, MODULE OR FUNCTION NOT 100% COMPLETE... IS THAT 100% PRODUCTION CODE IMPLEMENTATION ?
  - Are there any remaining activities or tasks that require attention?
  - Has the production code been fully implemented to meet the standards of enterprise-class production quality with no future or planned tasks, items, or activities?
  - If there are pending items, your responsibilities are considered unfulfilled, reflecting a lack of diligence similar to previous efforts.
  - Prompt action is required to address these matters without delay.

EXECUTE:
  "106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance"

FOCUS:
  - Code you have touched in this session
  - OUTPUT: {{ PREVIOUS INSTRUCTIONS EXECUTED }}


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
    - "006-PROTOCOL-RFC2119_Requirements_Language"

ENFORCE:
  - "002-PROTOCOL-Zero_Tolerance_Remediation"
  - "003-PROTOCOL-FastAPI_Pure_Code_Implementation"
  - "004-PROTOCOL-Validate_Remediate_Codebase"

DIRECTIVES:
  - THIS IS A CODE IMPLEMENTAITON, REFACTORING AND VALIDATION FOCUSED SESSION.
  - THE USE OF SCRIPTS OR MASS MODIFICATIONS TO THE CODE IS STRICTLY FORBIDDEN.
  - ALL CODE MUST BE IMPLEMENTED ONE STEP AT A TIME, IN A SEQUENTIAL MANNER.
  - NO DOCUMENTATION OF ANY KIND IS PERMITTED UNLESS I EXPLICITLY ASK FOR IT.
  - NO OTHER INSTRUCTIONS FROM ANY OTHER YAML FILES OVERRIDE THIS DIRECTIVE.

REMEMBER:
  - PERFORM ALL CODE QUALITY CHECKS INCLUDING AST AND COMPILE
  - IF THERE IS A FEATURE, MODULE OR FUNCTION NOT 100% COMPLETE... IS THAT 100% PRODUCTION CODE IMPLEMENTATION ?
  - Are there any remaining activities or tasks that require attention?
  - Has the production code been fully implemented to meet the standards of enterprise-class production quality with no future or planned tasks, items, or activities?
  - If there are pending items, your responsibilities are considered unfulfilled, reflecting a lack of diligence similar to previous efforts.
  - Prompt action is required to address these matters without delay.

EXECUTE:
  "107-INSTRUCTIONS-Remediate_And_Refactor_Codebase"

INPUT:
  - Code you have touched in this session
  - OUTPUT: 106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance

EXECUTE:
  "203-INSTRUCTIONS-FastAPI_Design_Implementation_Refactor"

INPUT:
  - Code you have touched in this session
  - OUTPUT: 106-INSTRUCTIONS-Validate_Code_Quality_and_Compliance



######################################################################################################################
