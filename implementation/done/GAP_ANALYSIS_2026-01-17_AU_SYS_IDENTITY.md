# Gap Analysis: au_sys_identity Validation & Wiring Coverage

## Executive Summary
**Date:** 2026-01-17
**Status:** Core Identity Features are Production-Ready. Enterprise & Ops Features have significant Gaps.
**Scope:** Verification (Testing) Gaps and Implementation (Wiring) Gaps.

The `au_sys_identity` capability is verified generally stable (100% Core Pass Rate). However, a deep architectural scan reveals two categories of deficiencies preventing a "Enterprise V1.0" release:
1.  **Validation Gaps:** Dormant code that is not currently tested.
2.  **Wiring Gaps:** Core backend logic that is not exposed via API or Web UI.
3.  **Process Gaps:** Lack of automated enforcement for Code Quality, Security, and Coverage standards.

**MANDATE:** Protocol 321 "Real Resources" is strictly enforced. All identified gaps MUST be tested using **REAL** containerized resources.

---

## Part 1: Validation Coverage Gaps (Testing)

These components exist and are wired, but have **0% Test Coverage** in the current suite.

| Component | Status | Gap Description |
| :--- | :---: | :--- |
| **Enterprise Auth** | 🔴 **UNTESTED** | `oauth.py`, `ldap.py`, `magic_link.py`. Logic exists but inactive due to config/env. |
| **Recovery Ops** | ⚠️ **PARTIAL** | `recovery.py`. Backup (`POST /backup`) is tested. **Restore is NOT tested.** |
| **User Settings** | 🔴 **UNTESTED** | `settings.py`. Endpoints exist but are ignored by test suite. |
| **Audit Integrity** | ⚠️ **WRITE-ONLY**| Logs are written, but no test verifies they are readable or correct. |

---

## Part 2: Interface Wiring Gaps (Implementation)

These components exist in `core/services/` but are **NOT accessible** via the API or Web UI, rendering them "Dead Code" to external consumers (Agents/Users).

### 1. Missing API Endpoints
*   **MFA Orchestrator (`mfa.py`):**
    *   **Gap:** The router exposes `/approve` (Human Action) but **MISSES** `/request` (Agent Action).
    *   **Impact:** An external Agent cannot trigger a delegated approval flow.
    *   **Required Endpoint:** `POST /mfa/delegated/request`
*   **Custodian Service (`custodian.py`):**
    *   **Gap:** No endpoint to inspect the "Chain of Custody" or ownership tree.
    *   **Impact:** Operators cannot debug "Who owns this Agent?" at runtime.
    *   **Required Endpoint:** `GET /iam/custody/{identity_id}`

### 2. Missing Web UI Panels
*   **Audit Logger (`audit.py`):**
    *   **Gap:** The Admin UI (`/admin`) lists Users but **hides** the Audit Log.
    *   **Impact:** Security Blindspot. Admins cannot verify activity without SQL access.
    *   **Required View:** `/admin/audit` (Datatable of `iam_audit_logs`).
*   **RBAC Manager (`rbac.py`):**
    *   **Gap:** No UI for creating Roles or Assigning Permissions.
    *   **Impact:** Operational friction (API-only management).
    *   **Required View:** `/admin/rbac` (Role/Permission Editor).

---

## Part 3: Architecture & Process Gaps (Tooling)

A critical review of the `CODEBASE_ARCHITECTURE_v1.0.0.md` and `320-INSTRUCTIONS-Validation_Suite_Standard_Structure-v1.0.0.yaml` reveals significant gaps in **Automated Quality Enforcement**.

### 1. Missing Documentation Standards
*   **Architecture Doc:** Previously lacked "High-Assurance" sections defining automated tooling requirements. (Remediated: Jan 17).
*   **Validation Instructions (YAML):** The `320-INSTRUCTIONS` YAML currently defines the `framework.py` and `runner.py` structure but **completely omits**:
    *   **Coverage Reporting:** No instruction to run tests with `coverage.py`.
    *   **Static Analysis:** No integration of `bandit`, `vulture`, or `pylint` into the recommended validation flow.
    *   **Security Gates:** No mention of SAST checks as a prerequisite for validation success.

### 2. Runner Weakness
*   **Current State:** The provided `runner.py` template is a simple file iterator.
*   **Gap:** It does not enforce:
    *   **Coverage Thresholds** (e.g., Fail if < 90%).
    *   **Linting Checks** (e.g., Fail if Pylint errors exist).
    *   **Dead Code Detection** (e.g., Fail if Vulture finds zombies).
*   **Impact:** A developer can "pass" validation while introducing massive technical debt or security vulnerabilities.

---

## Mandatory Remediation Plan (Next Code Spec)

This plan constitutes the requirements for the next Implementation Cycle.

### Phase 1: Close Wiring Gaps (Implementation)
1.  **Expose MFA Request:** Add `POST /mfa/delegated/request` to `routers/mfa.py`.
2.  **Expose Custody:** Add `GET /iam/custody/{id}` to `routers/iam.py`.
3.  **Admin UI Upgrade:**
    *   Add **Audit Log View** to Admin Dashboard.
    *   Add **RBAC Policy Editor** (Basic) to Admin Dashboard.

### Phase 2: Close Validation Gaps (Testing)
1.  **Infrastructure Config:** Update `docker-compose.yml` with **OpenLDAP**, **Mailhog**, and **Redis**.
2.  **Prerequisites:** Update `validate_00_prereqs.py` to enforce container health.
3.  **New Test Scripts:**
    *   `validate_20_enterprise_auth.py`: LDAP/OAuth/MagicLink (Real Flows).
    *   `validate_21_settings.py`: User Settings CRUD.
    *   `validate_22_mfa.py`: Full Agent-Request -> Human-Approve loop.
4.  **Enhance Existing:** Update `validate_16` to perform **Restore verification**.

### Phase 3: Close Process Gaps (Tooling)
1.  **Update Instructions:** Rewrite `320-INSTRUCTIONS-Validation_Suite_Standard_Structure-v1.0.0.yaml` to mandate the "High-Assurance" runner pattern, including:
    *   Integrated `coverage` run.
    *   Pre-flight `vulture` and `bandit` checks.
2.  **Upgrade Runner:** Refactor the `au_sys_identity/validation/runner.py` to implementations of these new standards immediately.
3.  **Enforce Limits:** Configure `pylint`, `radon`, and `coverage` configs in `pyproject.toml` to fail builds that violate the new Architecture Doc standards.

**Conclusion:** The release is blocked until Phases 1, 2, and 3 are complete.
