# Specification Creation Guide

**Version**: v1.0.0
**Last Updated**: YYYY-MM-DD
**Purpose**: Guide for creating specifications for capabilities, services, and features
**Applies To**: Any repository using specification-driven development

---

## 📋 OVERVIEW

### ⚠️ CRITICAL RULES

**Rule 1: ONE IMPLEMENTATION PLAN Per Repository**
- **THERE MUST ONLY EVER BE ONE `IMPLEMENTATION_PLAN_vX.Y.Z.md` FILE**
- Single source of truth for ALL work across entire repository
- Consolidated view of all work packages
- Located at: `docs/implementation/IMPLEMENTATION_PLAN_vX.Y.Z.md`
- ❌ NEVER create multiple implementation plans

**Rule 2: ONE SPEC FILE Per Capability/Service/Feature**
- Each capability/service/feature gets EXACTLY ONE specification file
- No duplicate specs for same item
- One spec = one work item in Kanban workflow
- ❌ NEVER create multiple specs for same capability/service/feature

---

### What is a Specification?

A **specification** is a complete design and implementation document that includes:

1. **Design Brief**
   - Purpose and scope
   - Architecture and design patterns
   - API/Interface definition
   - Dependencies

2. **Implementation Plan** (Verbose Breakdown)
   - **Phases**: Major stages of work
   - **Actions**: Specific actions within phases
   - **Tasks**: Discrete tasks within actions
   - **Steps**: Individual steps within tasks (ALL with checkboxes)

3. **Success Criteria**
   - Quality gates
   - Validation requirements
   - Completion definition

4. **Progress Tracking**
   - Checkbox at every level
   - Auditable and traceable
   - Status always visible

---

## 🎯 WHO NEEDS A SPECIFICATION?

**EVERYTHING significant requires a specification**:

### Services
- Backend services
- API services
- Microservices
- Data services

### Capabilities
- Major functionality blocks
- System capabilities
- Processing capabilities

### Features
- User-facing features
- Developer features
- Integration features

### Components
- Reusable components
- UI components
- Library components

### Modules
- Code modules
- Plugin modules
- Extension modules

### Refactorings
- Major code quality work
- Architecture refactorings
- Performance optimizations

**Rule**: If it's significant work (>2 hours), it needs a full specification.

---

## 🏗️ SPECIFICATION BREAKDOWN HIERARCHY

### 4-Level Hierarchy (All Required)

```
SPECIFICATION
│
├── PHASE (Major stage)
│   └── Checkbox: [ ] PHASE 1: Validation
│       │
│       ├── ACTION (Specific action within phase)
│       │   └── Checkbox: [ ] ACTION 1.1: Run import tests
│       │       │
│       │       ├── TASK (Discrete task within action)
│       │       │   └── Checkbox: [ ] TASK 1.1.1: Test all modules
│       │       │       │
│       │       │       └── STEP (Individual step)
│       │       │           ├── Checkbox: [ ] STEP 1.1.1.1: cd to directory
│       │       │           ├── Checkbox: [ ] STEP 1.1.1.2: run command
│       │       │           └── Checkbox: [ ] STEP 1.1.1.3: verify output
│       │       │
│       │       └── TASK 1.1.2: [Next task]
│       │
│       └── ACTION 1.2: [Next action]
│
└── PHASE 2: [Next phase]
```

**Critical**: Every level has checkboxes for tracking progress.

---

## ✅ CHECKLIST REQUIREMENTS

### Level 1: PHASE Checklist
**Format**:
```markdown
- [ ] PHASE 1: [Phase Name]
- [ ] PHASE 2: [Phase Name]
- [ ] PHASE 3: [Phase Name]
```

**Example**:
```markdown
- [ ] PHASE 1: Validation
- [ ] PHASE 2: Automated Fixes
- [ ] PHASE 3: Complexity Analysis
- [ ] PHASE 4: Manual Remediation
- [ ] PHASE 5: Final Validation
```

---

### Level 2: ACTION Checklist
**Format** (within each phase):
```markdown
PHASE 1: Validation
- [ ] ACTION 1.1: [Action description]
- [ ] ACTION 1.2: [Action description]
- [ ] ACTION 1.3: [Action description]
```

**Example**:
```markdown
PHASE 1: Validation
- [ ] ACTION 1.1: Import test
- [ ] ACTION 1.2: AST compilation check
- [ ] ACTION 1.3: Linting analysis
- [ ] ACTION 1.4: Document baseline metrics
```

---

### Level 3: TASK Checklist
**Format** (within each action):
```markdown
ACTION 1.3: Linting analysis
- [ ] TASK 1.3.1: Run flake8 critical errors
- [ ] TASK 1.3.2: Run flake8 complexity check
- [ ] TASK 1.3.3: Document violations
```

---

### Level 4: STEP Checklist
**Format** (within each task):
```markdown
TASK 1.3.1: Run flake8 critical errors
- [ ] STEP 1.3.1.1: Execute `python -m flake8 [path] --select=E,F`
- [ ] STEP 1.3.1.2: Capture output to file
- [ ] STEP 1.3.1.3: Count errors
- [ ] STEP 1.3.1.4: Record in tracking document
```

**Critical**: Steps must be SPECIFIC and ACTIONABLE (include commands where applicable).

---

## 📊 AUDITING & TRACEABILITY

### Why 4-Level Checklists?

**Granular Progress Tracking**:
- See exactly what's done at any level
- Identify blockers quickly
- Audit trail of execution

**Accountability**:
- Each checkbox = discrete action
- Can verify what was done
- Can replay execution path

**Traceability**:
- From high-level phase → specific step
- From completion → exact actions taken
- Complete audit trail

**Quality Assurance**:
- Nothing gets skipped
- All steps documented
- Validation at every level

---

## 🛠️ CREATION PROCESS

### Step 1: Copy Template (2 min)
```bash
cp SERVICE_SPEC_TEMPLATE_v1.0.0.md [NAME]_SPEC_v1.0.0.md
```

### Step 2: Fill Design Brief (15-30 min)
- Define purpose and scope
- Document architecture
- Specify API/interface
- List dependencies

### Step 3: Create Implementation Plan (30-60 min)

**3a. Identify Phases** (10 min)
- What are the major stages?
- Typical: 5-7 phases
- Examples: Validation, Implementation, Testing, Documentation

**3b. Break Phases into Actions** (15 min)
- What specific actions in each phase?
- Typical: 3-5 actions per phase

**3c. Break Actions into Tasks** (15 min)
- What discrete tasks for each action?
- Typical: 2-4 tasks per action

**3d. Break Tasks into Steps** (20 min)
- What individual steps for each task?
- Typical: 2-5 steps per task
- **MUST be specific** (include commands, files, etc.)

### Step 4: Define Success Criteria (10 min)
- Quality gates
- Validation requirements
- Completion definition

### Step 5: Validate Completeness (10 min)
- [ ] All 4 levels present
- [ ] All levels have checkboxes
- [ ] Steps are specific and actionable
- [ ] Success criteria are clear

### Step 6: Verify Uniqueness (2 min)
- [ ] Confirm NO existing spec for this capability/service/feature
- [ ] Search backlog/, in_progress/, done/ for duplicates
- [ ] If duplicate exists, update existing (don't create new)

### Step 7: Add to Workflow (5 min)
- Save to `../implementation/backlog/` (if new work)
- Add entry to SERVICE_STATUS_INDEX
- Ready for Kanban process

**Total Time**: ~2-3 hours per specification

**Critical**: NEVER create duplicate specs - update existing instead!

---

## 📝 SPECIFICATION QUALITY CHECKLIST

### Completeness
- [ ] Design brief filled completely
- [ ] All 4 hierarchy levels present (Phase → Action → Task → Step)
- [ ] Every level has checkboxes
- [ ] Success criteria defined
- [ ] No "[placeholder]" or "TODO" text

### Specificity
- [ ] Phases are clear major stages
- [ ] Actions are specific activities
- [ ] Tasks are discrete work units
- [ ] Steps include commands/file names/specific details

### Traceability
- [ ] Can track progress at all levels
- [ ] Can audit what was done
- [ ] Can verify completion
- [ ] Can estimate effort from breakdown

### Integration
- [ ] Added to backlog/ directory
- [ ] Referenced in STATUS_INDEX
- [ ] Follows naming convention ([NAME]_SPEC_v1.0.0.md)
- [ ] NO duplicate spec exists for this item
- [ ] Only ONE IMPLEMENTATION_PLAN exists in repository

---

## 🎯 EXAMPLES

### Good PHASE Definition
```markdown
- [ ] PHASE 1: Validation (5-10 min)
- [ ] PHASE 2: Automated Fixes (5-10 min)
- [ ] PHASE 3: Complexity Analysis (10-15 min)
- [ ] PHASE 4: Manual Remediation (30-60 min)
- [ ] PHASE 5: Final Validation (10-15 min)
```

### Good ACTION Definition
```markdown
PHASE 1: Validation
- [ ] ACTION 1.1: Import test all modules
- [ ] ACTION 1.2: AST compilation check
- [ ] ACTION 1.3: Run linting analysis
- [ ] ACTION 1.4: Document baseline metrics
```

### Good TASK Definition
```markdown
ACTION 1.3: Run linting analysis
- [ ] TASK 1.3.1: Run flake8 with E,F selectors
- [ ] TASK 1.3.2: Run flake8 with complexity check
- [ ] TASK 1.3.3: Document violation counts by type
```

### Good STEP Definition (SPECIFIC!)
```markdown
TASK 1.3.1: Run flake8 with E,F selectors
- [ ] STEP 1.3.1.1: Execute `python -m flake8 app/services/[name]/ --select=E,F`
- [ ] STEP 1.3.1.2: Save output to `validation_errors_EF.txt`
- [ ] STEP 1.3.1.3: Count errors: `wc -l validation_errors_EF.txt`
- [ ] STEP 1.3.1.4: Record count in tracking document
```

---

## 🚀 RECOMMENDED APPROACH

### For Simple Work (<4 hours)
- **Phases**: 3-5
- **Actions/Phase**: 2-4
- **Tasks/Action**: 2-3
- **Steps/Task**: 2-4
- **Total Checkboxes**: 30-60

### For Complex Work (4-8 hours)
- **Phases**: 5-7
- **Actions/Phase**: 3-5
- **Tasks/Action**: 2-4
- **Steps/Task**: 3-5
- **Total Checkboxes**: 60-120

### For Major Work (>8 hours)
- **Phases**: 7-10
- **Actions/Phase**: 4-6
- **Tasks/Action**: 3-5
- **Steps/Task**: 3-6
- **Total Checkboxes**: 100-200+

**Rule**: More complex work = more granular breakdown.

---

## 📚 RELATED DOCUMENTATION

### Templates & References
- `SERVICE_SPEC_TEMPLATE_v1.0.0.md` - Use this template
- `../implementation/IMPLEMENTATION_WORKFLOW_GUIDE_v1.0.0.md` - Workflow process
- `../implementation/DOCUMENTATION_NAMING_CONVENTION_v1.0.0.md` - Naming rules

### Status & Planning
- `../implementation/SERVICE_STATUS_INDEX_vX.Y.Z.md` - Overall status
- `../implementation/IMPLEMENTATION_PLAN_vX.Y.Z.md` - Work breakdown

---

## 🎯 SUCCESS CRITERIA

**Specification is complete when**:
- [ ] Design brief fully documented
- [ ] Implementation plan has all 4 levels (Phase/Action/Task/Step)
- [ ] Every level has checkboxes
- [ ] Steps are specific and actionable
- [ ] Success criteria defined
- [ ] Quality gates specified
- [ ] Added to backlog/
- [ ] Referenced in SERVICE_STATUS_INDEX

---

**Guide Type**: Universal specification creation process
**Granularity**: Phase → Action → Task → Step (4 levels, all checkboxes)
**Traceability**: 100% through checkbox hierarchy
**Portability**: Use in any repository for systematic work
