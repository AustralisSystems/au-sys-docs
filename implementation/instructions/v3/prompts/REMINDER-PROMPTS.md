
C:\github_development\projects\

C:\github_development\projects\rest-api-orchestrator

####################################################################################################

**IMPORTANT**
- Maintain and update your progress through the plan in the {{ CODE_IMPLEMENTATION_SPEC_DOCS }}

####################################################################################################

**IMPORTANT**
Ensure the design of the capabilities and features follows the Design and implementation pattern of PRIORITY OF IMPLEMENTATION: SDK, REST API calls, Bicep, Shell Scripts with az cli, powershell scripts

UPDATE THE SPEC DOC with the details of the design and implementation, then halt



Maintain and update your progress through the plan in the {{ CODE_IMPLEMENTATION_SPEC_DOCS }}


####################################################################################################


NEW_SPEC_FOCUS: "storage factory"

Create a "CODE_IMPLEMENTATION_SPEC" document to track this session, by:

- Copy the file  "docs\implementation\.CODE_IMPLEMENTATION_SPEC_TEMPLATE.md" into the directory "docs\implementation\in_progress\" DO NOT RE-WRITE IT YET.
- Within the newly created code specification document, provide a thorough and complete definition of the entire {{ NEW_SPEC_FOCUS }} capability, covering it comprehensively from beginning to end.
- Ensure that both the implementation and the code specification represent a FULL REWRITE, explicitly avoiding any form of migration, shims, or shortcuts.
- Address every aspect of the full rewrite in detail, breaking down the process into clear phases, tasks, actions, and steps, all organized as a detailed checklist.
- Incorporate any code examples or draft versions produced during this session to support the specification.
- Upon completion of these updates, finalize the creation of this new code specification document and then cease further modifications.



####################################################################################################


NEW_SPEC_FOCUS: "Web Application implementation"

NEW_SPEC_FOCUS: {{ Provided_Documents }}

Create a "CODE_IMPLEMENTATION_SPEC" document to track this session, by:

- Copy the file  "docs\implementation\WEB_APP_CODE_SPEC_TEMPLATE_v1.0.0.md" into the directory "docs\implementation\in_progress\" DO NOT RE-WRITE IT YET.
- Within the newly created code specification document, provide a thorough and complete definition of the entire {{ NEW_SPEC_FOCUS }} capability, covering it comprehensively from beginning to end.
- Ensure that both the implementation and the code specification represent a FULL REWRITE, explicitly avoiding any form of migration, shims, or shortcuts.
- Address every aspect of the full rewrite in detail, breaking down the process into clear phases, tasks, actions, and steps, all organized as a detailed checklist.
- Incorporate any code examples or draft versions produced during this session to support the specification.
- Upon completion of these updates, finalize the creation of this new code specification document and then cease further modifications.




####################################################################################################

**IMPORTANT**
The provided SPEC document(s) and handover document(s) provided are now your current focus for this session and for the SPEC document you created.
You MUST CONTINUE TO implement and action all the capabilities, items etc. defined in the handover and previous SPEC(s).
THIS IS A FULL RE-WRITE.


####################################################################################################

**IMPORTANT**
The handover and SEPC documents provided are now your current focus for this session and for the SPEC document you created.
You MUST CONTINUE TO implement and action all the capabilities, items etc. defined in the handover and previous SPEC(s).
THIS IS A FULL RE-WRITE.

**IMPORTANT**
THERE MUST BE NO PLANS OR IMPLEMENTATIONS FOR:
  - migrations
  - shims,
  - hacks
  - workarounds


####################################################################################################

**MANDATE**
MANDATE: THE USER IS RUNNING THE TEST SCRIPTS, AND YOUR RESPONSIBILITY IS TO REVIEW THE LOGS AND FIX ALL ISSUES IDENTIFIED
Update your SPEC doc with this mandate

####################################################################################################


FILE_NAME: "docs\implementation\in_progress\CODE_IMPLEMENTATION_SPEC_2025-12-27.md"

review the following file:

{{ FILE_NAME }}

**IMPORTANT**
this is your current focus for this session and for the SPEC document you created.
You MUST implement and action all the capabilities, items etc. defined in the {{ FILE_NAME }}.
THIS IS A FULL RE-WRITE..
THERE MUST BE NO PLANS OR IMPLEMENTATIONS FOR:
  - migrations
  - shims,
  - hacks
  - workarounds

Update your SPEC doc with this {{ FILE_NAME }} as a reference.
Prepare your SPEC doc to continue the implementation of the {{ FILE_NAME }}, then halt.


#####################################################################################################

**MANDATE**
review the in-scope files, modules, functions and content by:

first, perform an analysis of the in scope code content etc, to determine what additional re-writes are required to make all the code, modules functions and content:
then, perform a SOLID, DRY and KISS principles compliance analysis

The analysis of coding best practices must include:
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



########################################################################################################


update the in-scope files, modules, functions and content to use the logger factory for all standard logging.
then implement the diagnostics logger to do the debug and troubleshooting level logging for"
  - operations
  - transactions
  - data in and data out

you MUST ENSURE the logger factory and diagnostics logger implementation for the in scope files to greatly simplify the production validation of this feature and capability.



########################################################################################################


**IMPORTANT**
All db access and operations MUST be performed by the storage factory, and are the responsibility of the storage factory.
SQLAlchemy ORM MUST be fully integrated and are the responsibility of the storage factory.
Beanie ODM MUST be fully integrated and are the responsibility of the storage factory.



#######################################################################################################
