# Documentation Naming Convention

**Version**: v1.0.0
**Last Updated**: YYYY-MM-DD
**Status**: Active Standard
**Applies To**: Any software project

---

## 📋 OVERVIEW

This document defines the **mandatory naming convention** for all documentation. The convention distinguishes between temporal (point-in-time) and enduring (maintained) documentation through filename suffixes.

### Purpose

- Clearly identify document type from filename
- Enable version control for evolving documentation
- Provide temporal context for historical reports
- Facilitate automatic sorting and organization
- Support audit trails and compliance tracking

---

## 🎯 NAMING RULES

### Rule 1: TEMPORAL Documents (Point-in-Time)

**Format**: `DOCUMENT_NAME_YYYY-MM-DD.md`

**Definition**: Documents that capture information at a specific point in time and are NOT maintained or updated after creation.

**Use For**:

- ✅ Status reports and snapshots
- ✅ Session summaries and progress reports
- ✅ Assessment reports and audits
- ✅ Meeting notes and minutes
- ✅ Dated analysis and findings
- ✅ Historical records

**Examples**:

```
SERVICE_STATUS_YYYY-MM-DD.md
REMEDIATION_SESSION_PROGRESS_YYYY-MM-DD.md
QUALITY_ASSESSMENT_REPORT_YYYY-MM-DD.md
MEETING_NOTES_YYYY-MM-DD.md
COMPLETION_REPORT_YYYY-MM-DD.md
```

**Characteristics**:

- Created once, never updated
- Provides historical snapshot
- Date in filename indicates when created
- Useful for audit trails
- Can be archived when obsolete

---

### Rule 2: ENDURING Documents (Maintained, Evolving)

**Format**: `DOCUMENT_NAME_vX.Y.Z.md`

**Definition**: Documents that are actively maintained, updated, and versioned over time using semantic versioning.

**Use For**:

- ✅ Reference guides and manuals
- ✅ Standards and specifications
- ✅ Implementation plans and roadmaps
- ✅ Service/component specifications
- ✅ Architecture documentation
- ✅ Design documents
- ✅ Methodology guides

**Examples**:

```
IMPLEMENTATION_PLAN_v1.0.0.md
SERVICE_STATUS_INDEX_v2.1.0.md
REFACTORING_METHODOLOGY_v1.0.0.md
API_SPECIFICATION_v3.2.1.md
ARCHITECTURE_GUIDE_v2.0.0.md
```

**Characteristics**:

- Maintained and updated regularly
- Version number reflects evolution
- Single source of truth
- Supersedes previous versions
- Follows semantic versioning

---

### Rule 3: STANDARD Files (No Suffix)

**Format**: `STANDARD_NAME.md`

**Definition**: Conventional documentation files that follow established naming patterns and don't require suffixes.

**Use For**:

- ✅ README files (any directory)
- ✅ Template files
- ✅ Standard project files (CONTRIBUTING.md, LICENSE.md, CODE_OF_CONDUCT.md)
- ✅ Index files in specific contexts

**Examples**:

```
README.md
TEMPLATE.md
CONTRIBUTING.md
LICENSE.md
CHANGELOG.md
CODE_OF_CONDUCT.md
```

**Characteristics**:

- Universally recognized names
- Conventional in software projects
- Auto-displayed by tools (e.g., GitHub)
- No version/date needed
- Self-describing purpose

---

## 📊 SEMANTIC VERSIONING (Enduring Documents)

### Version Format: vMAJOR.MINOR.PATCH

**MAJOR** (v1.0.0 → v2.0.0)

- Breaking changes
- Complete restructure
- Incompatible with previous version
- Significant paradigm shift

**Example**: Reorganizing entire document structure, removing major sections, changing fundamental approach

**MINOR** (v1.0.0 → v1.1.0)

- New features or sections
- Significant additions
- Backward compatible
- Enhanced functionality

**Example**: Adding new sections, expanding content, adding new examples, new guidelines

**PATCH** (v1.0.0 → v1.0.1)

- Bug fixes and corrections
- Typo fixes
- Clarifications
- Minor improvements
- Link updates

**Example**: Fixing typos, correcting errors, updating broken links, clarifying existing content

---

## 🔍 DECISION TREE

### When Creating New Documentation

```
START
  ↓
Is this a README, TEMPLATE, or standard file?
  ├─ YES → Use STANDARD format (no suffix)
  │         Example: README.md
  └─ NO
      ↓
Will this document be maintained and updated over time?
  ├─ YES → Use ENDURING format (_vX.Y.Z.md)
  │         Example: IMPLEMENTATION_PLAN_v1.0.0.md
  └─ NO
      ↓
Is this a point-in-time report or snapshot?
      └─ YES → Use TEMPORAL format (_YYYY-MM-DD.md)
                Example: STATUS_REPORT_YYYY-MM-DD.md
```

---

## ✅ COMPLIANCE REQUIREMENTS

### Mandatory Requirements

**All New Documentation MUST**:

- [ ] Follow one of the three naming conventions
- [ ] Use correct suffix format (no variations)
- [ ] Use consistent date format (YYYY-MM-DD)
- [ ] Use semantic versioning for enduring docs (vX.Y.Z)
- [ ] Have clear, descriptive base names
- [ ] Use underscores to separate words in base name
- [ ] Use `.md` extension for Markdown files

**Prohibited**:

- ❌ Mixed formats (e.g., `DOCUMENT_v1.0.0_YYYY-MM-DD.md`)
- ❌ Non-standard date formats (e.g., `MM-DD-YYYY`, `DDMONYYYY`)
- ❌ Non-semantic versions (e.g., `v1`, `v2.1`)
- ❌ Spaces in filenames (use underscores)
- ❌ Special characters except underscore and hyphen

**Non-Compliant Documents**:

- Documents that don't follow naming convention should be moved to `temporal/` directory
- This includes temporal documents with non-standard names
- SPECs should NEVER go in `temporal/` (SPECs go in backlog/in_progress/done/)

**CRITICAL DIRECTORY RULE**:

- **backlog/, in_progress/, and done/ directories MUST ONLY contain SPEC documents** (files matching pattern `*_SPEC_v*.md`)
- **ALL other documents** (temporal documents, status reports, completion reports, session summaries, etc.) **MUST be moved to temporal/** AFTER important information has been extracted and used to update the implementation plan and other documentation
- **Workflow**: Extract info → Update IMPLEMENTATION_PLAN/docs → Move to temporal/
- **This rule is NON-NEGOTIABLE**

---

## 📂 TYPICAL DIRECTORY STRUCTURE

### Common Documentation Organization

```
docs/
├── implementation/
│   ├── STATUS_INDEX_vX.Y.Z.md (enduring)
│   ├── IMPLEMENTATION_PLAN_vX.Y.Z.md (enduring)
│   ├── METHODOLOGY_vX.Y.Z.md (enduring)
│   ├── WORKFLOW_GUIDE_vX.Y.Z.md (enduring)
│   ├── NAMING_CONVENTION_vX.Y.Z.md (enduring)
│   ├── backlog/ (SPECs ONLY - queued)
│   ├── in_progress/ (SPECs ONLY - active)
│   ├── done/ (SPECs ONLY - complete)
│   ├── temporal/ (ALL temporal docs, status reports, completion reports, session summaries)
│   │   ├── SESSION_REPORT_YYYY-MM-DD.md (temporal - compliant)
│   │   ├── COMPLETION_REPORT_YYYY-MM-DD.md (temporal - compliant)
│   │   └── ... (all other temporal documents)
│   └── _archive/ (archived temporal docs)
│
├── services/specifications/
│   ├── README.md (standard)
│   ├── SPEC_TEMPLATE_vX.Y.Z.md (enduring)
│   └── [SERVICE]_SPEC_vX.Y.Z.md (enduring)
│
├── architecture/
│   ├── README.md (standard)
│   └── ARCHITECTURE_vX.Y.Z.md (enduring)
│
└── api/
    ├── README.md (standard)
    └── API_SPEC_vX.Y.Z.md (enduring)
```

---

## 🔄 UPDATING ENDURING DOCUMENTS

### Process for Version Updates

**Step 1: Determine Version Change**

- Review changes against semantic versioning rules
- Identify MAJOR, MINOR, or PATCH level

**Step 2: Update Document**

- Modify content as needed
- Update "Last Updated" date in header
- Update "Version" in header

**Step 3: Update Filename** (MAJOR/MINOR only)

```bash
# For MAJOR or MINOR updates, create new version file
cp DOCUMENT_v1.0.0.md DOCUMENT_v1.1.0.md

# For PATCH updates, keep same filename (just update content)
# DOCUMENT_v1.0.0.md (content updated, filename unchanged)
```

**Step 4: Update References**

- Update links in other documents
- Update indexes and catalogs
- Archive old version if needed (MAJOR changes)

---

## 📋 EXAMPLES

### Correct Naming

✅ **TEMPORAL**:

```
QUALITY_REPORT_YYYY-MM-DD.md
SESSION_SUMMARY_YYYY-MM-DD.md
AUDIT_RESULTS_YYYY-MM-DD.md
MEETING_NOTES_YYYY-MM-DD.md
```

✅ **ENDURING**:

```
IMPLEMENTATION_PLAN_v1.0.0.md
STATUS_INDEX_v2.1.0.md
API_SPECIFICATION_v3.0.0.md
DEVELOPER_GUIDE_v1.2.3.md
```

✅ **STANDARD**:

```
README.md
TEMPLATE.md
CONTRIBUTING.md
LICENSE.md
```

### Incorrect Naming

❌ **Wrong Date Format**:

```
REPORT_MM-DD-YYYY.md        # Use YYYY-MM-DD
STATUS_DDMONYYYY.md         # Use YYYY-MM-DD
```

❌ **Wrong Version Format**:

```
PLAN_v1.md                  # Use vX.Y.Z
GUIDE_version_2.1.md        # Use v2.1.0
SPEC_ver_3.0.0.md          # Use v3.0.0
```

❌ **Mixed Formats**:

```
DOCUMENT_v1.0.0_YYYY-MM-DD.md  # Choose one format
STATUS_YYYY-MM-DD_v2.md        # Choose one format
```

---

## 🎯 VALIDATION CHECKLIST

Before finalizing any document:

- [ ] Filename follows one of three conventions (TEMPORAL, ENDURING, STANDARD)
- [ ] Date format is YYYY-MM-DD (if temporal)
- [ ] Version format is vX.Y.Z (if enduring)
- [ ] Base name is descriptive and uses underscores
- [ ] Extension is `.md` for Markdown
- [ ] Document header includes Version/Date and Status
- [ ] Document type matches content purpose
- [ ] No spaces or special characters in filename
- [ ] Consistent with similar documents in directory

---

## 🎯 ENFORCEMENT

### Responsibility

- **Authors**: Follow convention for new documents
- **Reviewers**: Verify compliance in code reviews
- **Maintainers**: Enforce standard in pull requests
- **Automation**: Validate in CI/CD (recommended)

### Non-Compliance

- Pull requests with non-compliant docs may be rejected
- Existing non-compliant docs should be renamed progressively
- New docs MUST comply from day one

---

## 📊 BENEFITS

### For Developers

- ✅ Instantly identify document type
- ✅ Know if document is current or historical
- ✅ Understand versioning and updates
- ✅ Easy to find latest version

### For Maintainers

- ✅ Clear versioning for evolving docs
- ✅ Easy archival of temporal docs
- ✅ Consistent organization across projects
- ✅ Simplified documentation management

### For Teams

- ✅ Professional documentation structure
- ✅ Clear audit trails
- ✅ Reduced confusion
- ✅ Improved discoverability
- ✅ Portable across repositories

---

## 🔄 REVISION HISTORY

| Version | Date       | Changes                      |
| ------- | ---------- | ---------------------------- |
| v1.0.0  | YYYY-MM-DD | Initial standard established |

---

**Standard Type**: Universal documentation naming convention
**Review Cycle**: Quarterly recommended
**Compliance**: Mandatory for all new documentation
**Portability**: Copy to any repository for consistent documentation
