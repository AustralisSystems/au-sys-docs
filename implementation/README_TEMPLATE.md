# Implementation Documentation - Kanban Workflow

**Version**: v1.0.0
**Last Updated**: YYYY-MM-DD
**Project**: [Project Name]
**Purpose**: Kanban-style SPEC-based workflow following canonical 4-level hierarchy

---

## 📂 DIRECTORY STRUCTURE

```
docs/services/specifications/        docs/implementation/
├── README.md                        ├── README.md (this file)
├── SERVICE_SPEC_TEMPLATE_vX.Y.Z.md  │
└── SPEC_CREATION_GUIDE_vX.Y.Z.md    ├── 📋 ENDURING DOCUMENTS (Read & Maintain)
    (reference library)               │   ├── SERVICE_STATUS_INDEX_vX.Y.Z.md
                                     │   ├── IMPLEMENTATION_PLAN_vX.Y.Z.md
                                     │   ├── REFACTORING_METHODOLOGY_vX.Y.Z.md
          Kanban Pipeline →          │   ├── DOCUMENTATION_NAMING_CONVENTION_vX.Y.Z.md
                                     │   └── IMPLEMENTATION_WORKFLOW_GUIDE_vX.Y.Z.md
backlog/ → in_progress/ → done/      │
  (X)         (Y)          (Z)       ├── 📁 WORKFLOW DIRECTORIES (Kanban)
  [Status]   [Status]    [Status]    │   ├── backlog/ ([X] items)
                                     │   ├── in_progress/ ([Y] items)
                                     │   ├── done/ ([Z] items)
                                     │   └── temporal/ ([W] items - non-compliant temporal docs)
                                     │
                                     └── 📦 Session Reports (temporal docs)
```

---

## 🎯 CURRENT STATUS

### **Platform**: X% Complete (Y/Z Phases)

**✅ Completed Phases** (in done/):
- Phase 1: [Phase Name] (X%)
- Phase 2: [Phase Name] (X%)
- Phase N: [Phase Name] (X%)

**🚧 In Progress**: [Number] phases active

---

## 🎯 KANBAN WORKFLOW STATUS

### Visual Pipeline:

```
backlog/ (X)  →  in_progress/ (Y)  →  done/ (Z)          temporal/ (W)
[Status]          [Status]             [Status]            [Status]
```

**Goal**: Move all SPECs from backlog → done
**Note**: Temporal docs that don't follow naming convention go directly to temporal/

### Directory Counts:

| Directory | Count | Status |
|-----------|-------|--------|
| **backlog/** | X | [Description] |
| **in_progress/** | Y | [Description] |
| **done/** | Z | [Description] |
| **temporal/** | W | Non-compliant temporal documents |

---

## 📊 WHAT'S IN EACH DIRECTORY

### backlog/ ([X] items)

1. **[SPEC_NAME_SPEC_vX.Y.Z.md]**
   - Status: [Status]
   - Priority: [Priority]
   - Description: [Description]

### in_progress/ ([Y] items)

**Status**: [Description]

### done/ ([Z] items)

**SPECs** ([Number]):
1. [SPEC_NAME_SPEC_vX.Y.Z.md] ([Phase Name])
2. [SPEC_NAME_SPEC_vX.Y.Z.md] ([Phase Name])

**Reports** ([Number]):
1. [REPORT_NAME_YYYY-MM-DD.md] (if follows naming convention)

### temporal/ ([W] items)

**Non-Compliant Temporal Documents** ([Number]):
1. [Document with non-standard name]
2. [Document that doesn't follow DOCUMENT_NAME_YYYY-MM-DD.md format]
3. [Document that doesn't follow DOCUMENT_NAME_vX.Y.Z.md format]

**Note**: All temporal documents that don't conform to naming convention should be moved here

---

## 📋 REQUIRED ENDURING DOCUMENTS

### Core Documents:

1. **`IMPLEMENTATION_PLAN_vX.Y.Z.md`**
   - Master plan showing overall progress
   - All phases tracked
   - Current as of YYYY-MM-DD

2. **`SERVICE_STATUS_INDEX_vX.Y.Z.md`**
   - Service inventory
   - Shows [Number] total services
   - Last updated: YYYY-MM-DD

3. **`IMPLEMENTATION_WORKFLOW_GUIDE_vX.Y.Z.md`**
   - Kanban workflow process guide
   - Current and accurate

4. **`DOCUMENTATION_NAMING_CONVENTION_vX.Y.Z.md`**
   - Temporal vs Enduring naming standards
   - Current and accurate

5. **`SPEC_CREATION_GUIDE_vX.Y.Z.md`**
   - How to create specifications
   - Current and accurate

---

## ⚡ QUICK START

### To Continue Implementation:

```bash
# 1. Read master plan (5 min) ⭐ START HERE
cat IMPLEMENTATION_PLAN_vX.Y.Z.md

# 2. Check status (2 min)
# Current: X% complete (Y/Z phases)

# 3. Check in_progress/ (1 min)
ls -la in_progress/
# Result: [Description]

# 4. Review backlog (2 min)
ls -la backlog/
# Result: [Description]

# 5. Decision Point:
# [Decision guidance]
```

### To Verify Platform Status:

```bash
# Check all services
[Service verification command]

# Verify [Component]
[Verification command]

# Verify all phases operational
cat IMPLEMENTATION_PLAN_vX.Y.Z.md | grep "X%"
```

---

## 🎯 WORKFLOW RULES

### Rule 1: One Direction Flow

```
backlog → in_progress → done
  (never move backwards unless deprioritizing)
```

### Rule 2: Limit Work in Progress

- Maximum 1-3 items in `in_progress/` at any time
- Currently: **[X] items**

### Rule 3: Update on Every Move

When moving a work item:
- [ ] Update IMPLEMENTATION_PLAN (reflect new status)
- [ ] Update SPEC with progress
- [ ] Create completion report (if moving to done)
- [ ] Persist to memory (if applicable)

### Rule 4: Temporal Documents

- [ ] Check if temporal document follows naming convention:
  - ✅ Follows `DOCUMENT_NAME_YYYY-MM-DD.md` → Can stay in current location
  - ❌ Doesn't follow convention → Move to `temporal/`
- [ ] Move non-compliant temporal documents to `temporal/`
- [ ] Update references if needed

---

## 📞 QUICK REFERENCE TABLE

| Need | Document | Location |
|------|----------|----------|
| **Current status?** | `IMPLEMENTATION_PLAN_vX.Y.Z.md` | This directory |
| **What to work on?** | Check `backlog/` | [Description] |
| **How workflow works?** | `IMPLEMENTATION_WORKFLOW_GUIDE_vX.Y.Z.md` | This directory |
| **All phases complete?** | See `done/` directory | [X] items |
| **What's completed?** | [Description] | X% complete |

---

## 🚀 NEXT ACTIONS

### Current State: **[Status]**

**Status**:

1. **[Status Item 1]**
   - [Description]
   - [Description]

2. **[Status Item 2]** (Optional)
   - [Description]
   - Priority: [Priority]
   - Can be scheduled as needed

---

## 🎯 SUCCESS METRICS

**Workflow is working when**:
- ✅ backlog/ organized ([X] items)
- ✅ done/ growing ([Z] items)
- ✅ in_progress/ limited ([Y] items, max 3)
- ✅ temporal/ contains non-compliant temporal docs ([W] items)
- ✅ IMPLEMENTATION_PLAN current (vX.Y.Z)
- ✅ All references accurate

---

## 📚 DOCUMENTATION INVENTORY

### Enduring Documents ([Number]):
- IMPLEMENTATION_PLAN_vX.Y.Z.md
- SERVICE_STATUS_INDEX_vX.Y.Z.md
- IMPLEMENTATION_WORKFLOW_GUIDE_vX.Y.Z.md
- DOCUMENTATION_NAMING_CONVENTION_vX.Y.Z.md
- SPEC_CREATION_GUIDE_vX.Y.Z.md

### Session Reports ([Number] temporal):
- [REPORT_NAME_YYYY-MM-DD.md]
- [REPORT_NAME_YYYY-MM-DD.md]

### Specifications ([Number] in done/):
- [SPEC_NAME_SPEC_vX.Y.Z.md]
- [SPEC_NAME_SPEC_vX.Y.Z.md]

---

**Workflow Type**: Kanban pipeline (backlog → in_progress → done)
**Status Visibility**: File location = implementation status
**Traceability**: 100% tracked through directories
**Current**: [Current status description]
