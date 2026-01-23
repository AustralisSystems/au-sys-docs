# Implementation Workflow Guide - Kanban Process

**Version**: v1.0.0
**Last Updated**: YYYY-MM-DD
**Status**: Active Standard
**Applies To**: Any repository implementing systematic quality work

---

## 🎯 CORE CONCEPT

**Every capability, service, or feature** requires:
1. **ONE Specification** (design brief) - ONE per capability/service/feature
2. **Implementation Plan** (verbose breakdown) - Embedded in specification
3. **Checklist** (phases → actions → tasks → steps)
4. **Tracking** (auditing & traceability)

This workflow manages specifications through a **Kanban pipeline** where file location indicates implementation status.

---

## ⚠️ CRITICAL RULES

### Rule 1: ONE IMPLEMENTATION PLAN Per Repository
**THERE MUST ONLY EVER BE ONE `IMPLEMENTATION_PLAN_vX.Y.Z.md` FILE**

- ✅ Single source of truth for ALL outstanding work
- ✅ Consolidated view of all work packages
- ✅ One place to track overall progress
- ❌ NEVER create multiple implementation plans
- ❌ NEVER create per-service/per-feature implementation plans

**Location**: `docs/implementation/IMPLEMENTATION_PLAN_vX.Y.Z.md`

### Rule 2: ONE SPEC FILE Per Capability/Service/Feature
**Each capability/service/feature gets EXACTLY ONE specification file**

- ✅ One spec = one work item
- ✅ No duplicate specs for same item
- ✅ No multiple versions simultaneously (archive old versions)
- ❌ NEVER create multiple specs for same capability
- ❌ NEVER split one capability across multiple specs

**Naming**: `[NAME]_SPEC_vX.Y.Z.md`
**Location**: One of: backlog/, in_progress/, or done/

### Rule 3: CRITICAL DIRECTORY RULE - SPEC Directories Contain ONLY SPECs
**The directories backlog/, in_progress/, and done/ MUST ONLY contain SPEC documents**

- ✅ **ONLY** files matching pattern `*_SPEC_v*.md` belong in backlog/, in_progress/, or done/
- ❌ **NEVER** put temporal documents, status reports, completion reports, or session summaries in these directories
- ❌ **NEVER** put any non-SPEC files in backlog/, in_progress/, or done/
- ✅ **ALL** non-SPEC files MUST be moved to `temporal/` AFTER information extraction
- ✅ Workflow: Extract info → Update IMPLEMENTATION_PLAN/docs → Move to temporal/
- ❌ **NEVER** put SPECs in temporal/ (SPECs go in backlog/in_progress/done/ only)

**This rule is NON-NEGOTIABLE and must be enforced strictly.**

---

## 📋 SPECIFICATION REQUIREMENTS

### What is a "Specification"?

**A specification is a complete design brief** that includes:

1. **Design Brief**
   - Purpose and scope
   - Architecture and design
   - API/Interface definition
   - Dependencies

2. **Implementation Plan**
   - Verbose breakdown of ALL work
   - Organized into: Phases → Actions → Tasks → Steps

3. **Execution Checklists**
   - Every phase has checklist
   - Every action has checklist
   - Every task has checklist
   - Every step has checklist

4. **Success Criteria**
   - Quality gates
   - Validation requirements
   - Completion definition

### Who Needs a Specification?

**EVERYTHING requires a spec** (ONE spec per item):
- ✅ Services (backend services, APIs) - ONE spec per service
- ✅ Capabilities (features, functionality) - ONE spec per capability
- ✅ Features (user-facing features) - ONE spec per feature
- ✅ Components (reusable components) - ONE spec per component
- ✅ Modules (code modules) - ONE spec per module
- ✅ Systems (subsystems, integrations) - ONE spec per system

**Critical Rules**:
- ✅ ONE specification file per capability/service/feature
- ✅ ONE IMPLEMENTATION_PLAN for entire repository (not per-item)
- ❌ NEVER multiple specs for same item
- ❌ NEVER multiple implementation plans

---

## 🏗️ SPECIFICATION STRUCTURE

### Complete Breakdown Hierarchy

```
SPECIFICATION
└── DESIGN BRIEF
    ├── Purpose & Scope
    ├── Architecture
    ├── API/Interface
    └── Dependencies

└── IMPLEMENTATION PLAN
    ├── PHASE 1: [Phase Name]
    │   ├── ACTION 1.1: [Action Name]
    │   │   ├── TASK 1.1.1: [Task Name]
    │   │   │   ├── STEP 1.1.1.1: [Step description] ☐
    │   │   │   ├── STEP 1.1.1.2: [Step description] ☐
    │   │   │   └── STEP 1.1.1.3: [Step description] ☐
    │   │   ├── TASK 1.1.2: [Task Name]
    │   │   │   ├── STEP 1.1.2.1: [Step description] ☐
    │   │   │   └── STEP 1.1.2.2: [Step description] ☐
    │   │   └── TASK 1.1.3: [Task Name]
    │   │       └── STEP 1.1.3.1: [Step description] ☐
    │   └── ACTION 1.2: [Action Name]
    │       └── [Tasks and Steps...]
    ├── PHASE 2: [Phase Name]
    │   └── [Actions, Tasks, Steps...]
    └── PHASE N: [Phase Name]
        └── [Actions, Tasks, Steps...]

└── SUCCESS CRITERIA
    ├── Quality Gates ☐
    ├── Validation Requirements ☐
    └── Completion Definition ☐
```

---

## ✅ CHECKLIST TRACKING SYSTEM

### Checklist Levels (All Required)

**Level 1: PHASE Checklist**
```
- [ ] PHASE 1: Validation
- [ ] PHASE 2: Automated Fixes
- [ ] PHASE 3: Complexity Analysis
- [ ] PHASE 4: Manual Remediation
- [ ] PHASE 5: Final Validation
- [ ] PHASE 6: Documentation
- [ ] PHASE 7: Memory Update
```

**Level 2: ACTION Checklist** (within each phase)
```
PHASE 1: Validation
- [ ] ACTION 1.1: Import test
- [ ] ACTION 1.2: AST compilation
- [ ] ACTION 1.3: Linting analysis
- [ ] ACTION 1.4: Document baseline
```

**Level 3: TASK Checklist** (within each action)
```
ACTION 1.3: Linting analysis
- [ ] TASK 1.3.1: Run flake8 with E,F selectors
- [ ] TASK 1.3.2: Run flake8 with complexity check
- [ ] TASK 1.3.3: Document violation counts
```

**Level 4: STEP Checklist** (within each task)
```
TASK 1.3.1: Run flake8 with E,F selectors
- [ ] STEP 1.3.1.1: Execute command `python -m flake8 [path] --select=E,F`
- [ ] STEP 1.3.1.2: Capture output to file
- [ ] STEP 1.3.1.3: Parse error counts
- [ ] STEP 1.3.1.4: Record in tracking document
```

---

## 📊 AUDITING & TRACEABILITY

### Traceability Requirements

**Every work item MUST have**:

1. **Specification File**
   - Complete design brief
   - Full implementation plan
   - All checklists (4 levels deep)
   - Current status clearly marked

2. **Progress Tracking**
   - Checked-off items show what's done
   - Unchecked items show what remains
   - Partial completion visible at all levels

3. **Completion Report** (when done)
   - What was accomplished
   - How it was validated
   - Metrics achieved
   - Lessons learned

4. **Status Index Entry**
   - Current state reflected
   - Quality metrics documented
   - Cross-references maintained

### Audit Trail

**Can answer at any time**:
- ✅ What's complete? → Check done/
- ✅ What's in progress? → Check in_progress/
- ✅ What's planned? → Check backlog/
- ✅ How was it done? → Check completion reports
- ✅ What's the quality? → Check SERVICE_STATUS_INDEX metrics
- ✅ Where are we? → Count files in each directory

---

## 🔄 KANBAN WORKFLOW

### Pipeline Visualization

```
BACKLOG/          IN_PROGRESS/       DONE/          TEMPORAL/
┌─────────┐      ┌──────────┐      ┌──────────┐   ┌──────────┐
│ Item A  │ -->  │          │      │ Item X   │   │ Report 1 │
│ Item B  │      │ Item Y   │ -->  │ + Report │   │ Report 2 │
│ Item C  │      │          │      │          │   │ Report 3 │
│ Item D  │      │ (1-3 max)│      │ Item Z   │   │   ...    │
│ ...     │      │          │      │ + Report │   └──────────┘
└─────────┘      └──────────┘      └──────────┘   (non-compliant
 (queued)         (active)          (complete)      temporal docs)

Rule: SPECs move one direction only (left to right)
Rule: Temporal docs go directly to temporal/ (not part of SPEC workflow)
```

### Movement Process

**PULL from Backlog**:
1. Select highest priority item
2. Check in_progress/ has capacity (< 3 items)
3. Move spec file to in_progress/
4. Update SERVICE_STATUS_INDEX

**WORK in Progress**:
1. Open spec file
2. Execute phases sequentially
3. Check off items as completed (☐ → ☑)
4. Update spec file with progress

**PUSH to Done**:
1. Verify all checklists complete
2. Verify all success criteria pass
3. Move spec file to done/
4. **CRITICAL**: Verify done/ contains ONLY SPEC documents
5. If any non-SPEC files found in done/:
   - Extract important information
   - Update IMPLEMENTATION_PLAN and other documentation
   - Move ALL non-SPEC files to temporal/
6. Create completion report (temporal) → Save directly to temporal/
7. Update SERVICE_STATUS_INDEX (bump version)

**TEMPORAL Documents**:
1. **CRITICAL**: Check backlog/, in_progress/, and done/ for ANY non-SPEC files
2. For each non-SPEC file found:
   - Extract important information
   - Update IMPLEMENTATION_PLAN and other documentation with extracted information
   - Move file to temporal/
3. For temporal documents elsewhere:
   - Check if document follows naming convention:
     - ✅ Follows `DOCUMENT_NAME_YYYY-MM-DD.md` → Can stay in current location (if not in SPEC directories)
     - ❌ Doesn't follow convention → Move to `temporal/`
4. **CRITICAL**: Verify backlog/, in_progress/, and done/ contain ONLY SPEC documents
5. Update references if needed

**AUTOMATION TOOLS**:
- Use `scripts/Audit-WorkflowCompliance.ps1` to audit compliance
- Use `scripts/Move-NonSpecFilesFromSpecDirectories.ps1` to move non-SPEC files after information extraction

---

## 🔧 AUTOMATION SCRIPTS FOR COMPLIANCE

### Audit-WorkflowCompliance.ps1

**Purpose**: Audits all documentation for compliance with workflow guide and naming convention.

**What it checks**:
- ✅ Directory structure (backlog/, in_progress/, done/, temporal/)
- ✅ SPEC file locations (must be in backlog/in_progress/done/ only)
- ✅ SPEC file naming (must match `[NAME]_SPEC_vX.Y.Z.md` pattern)
- ✅ **CRITICAL**: Non-SPEC files in SPEC directories (backlog/in_progress/done/)
- ✅ Temporal document naming compliance
- ✅ Enduring document naming compliance
- ✅ Standard file naming compliance

**Usage**:
```powershell
cd docs/implementation
.\scripts\Audit-WorkflowCompliance.ps1
```

**Output**: Provides detailed audit results with color-coded violations and recommendations.

### Move-NonSpecFilesFromSpecDirectories.ps1

**Purpose**: Moves all non-SPEC files from backlog/, in_progress/, and done/ to temporal/.

**CRITICAL**: Run this script **AFTER** you have:
1. ✅ Extracted important information from temporal documents
2. ✅ Updated IMPLEMENTATION_PLAN with extracted information
3. ✅ Updated other documentation as needed

**Usage**:
```powershell
cd docs/implementation
# First, audit to see what needs to be moved
.\scripts\Audit-WorkflowCompliance.ps1

# Extract information and update plans/docs manually

# Then move files
.\scripts\Move-NonSpecFilesFromSpecDirectories.ps1

# Or use -WhatIf to preview
.\scripts\Move-NonSpecFilesFromSpecDirectories.ps1 -WhatIf
```

**What it does**:
- Scans backlog/, in_progress/, and done/ for non-SPEC files
- Moves all non-SPEC files to temporal/
- Handles duplicate filenames by appending directory name and timestamp
- Provides summary of moved files

**Workflow**:
1. Run `Audit-WorkflowCompliance.ps1` to identify violations
2. Extract important information from non-SPEC files found
3. Update IMPLEMENTATION_PLAN and other documentation
4. Run `Move-NonSpecFilesFromSpecDirectories.ps1` to move files
5. Verify compliance by running `Audit-WorkflowCompliance.ps1` again

---

## 📚 SPECIFICATION TEMPLATE EXAMPLE

```markdown
# [Capability/Service/Feature] - Specification

**Version**: v1.0.0
**Status**: ⚠️ Needs Implementation
**Priority**: [P0/P1/P2/P3]

## DESIGN BRIEF
[Architecture, purpose, scope]

## IMPLEMENTATION PLAN

### PHASE 1: [Phase Name]
**Estimated**: [time]

#### ACTION 1.1: [Action Name]
- [ ] TASK 1.1.1: [Task description]
  - [ ] STEP 1.1.1.1: [Specific step]
  - [ ] STEP 1.1.1.2: [Specific step]
- [ ] TASK 1.1.2: [Task description]
  - [ ] STEP 1.1.2.1: [Specific step]

#### ACTION 1.2: [Action Name]
- [ ] TASK 1.2.1: [Task description]

### PHASE 2: [Phase Name]
[Actions, Tasks, Steps...]

## SUCCESS CRITERIA
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## VALIDATION
- [ ] Quality gate 1
- [ ] Quality gate 2
```

---

## 🎯 BENEFITS

### For Developers
- ✅ Know exactly what to do next
- ✅ Track progress granularly
- ✅ See what's completed
- ✅ Visual status (file location)

### For Managers
- ✅ See progress at a glance (directory counts)
- ✅ Know what's in progress
- ✅ Audit trail of all work
- ✅ Completion reports for metrics

### For Teams
- ✅ Shared understanding of workflow
- ✅ Consistent process across projects
- ✅ Reusable methodology
- ✅ Clear handoffs

---

## 🔧 CUSTOMIZATION FOR YOUR REPO

### 1. Copy These Files
- This WORKFLOW_GUIDE
- NAMING_CONVENTION
- SERVICE_STATUS_INDEX template
- IMPLEMENTATION_PLAN template
- METHODOLOGY_REFERENCE template
- SPEC_TEMPLATE

### 2. Create Workflow Directories
```bash
mkdir -p docs/implementation/{backlog,in_progress,done,temporal}
```

### 3. Customize for Your Project
- Update SERVICE_STATUS_INDEX with your items
- Update IMPLEMENTATION_PLAN with your phases
- Keep workflow and naming docs generic

### 4. Create Specifications
- One spec per capability/service/feature
- Use SPEC_TEMPLATE as starting point
- Add to backlog/

### 5. Start Workflow
- Select from backlog/
- Move through pipeline
- Track and document
- Move non-compliant temporal docs to temporal/

---

**Workflow Standard**: Kanban-based systematic implementation
**Granularity**: Phase → Action → Task → Step (all checkboxes)
**Traceability**: 100% through specs and completion reports
**Portability**: Copy to any repository for consistent quality work
