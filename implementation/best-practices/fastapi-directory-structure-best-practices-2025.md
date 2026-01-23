# FastAPI Directory Structure Best Practices (December 2025)

**Date**: 2025-12-05
**Version**: 1.0.0
**Status**: Analysis & Comparison

---

## Executive Summary

This document compares:
1. **Current FastAPI Best Practices** (December 2025) for backend REST API + frontend web UI (HTMX + Jinja2)
2. **Router Factory 2.0 Scaffolder Output** - What it actually generates
3. **Gap Analysis** - Differences and recommendations

---

## 1. FastAPI Best Practices (2025)

### 1.1 Official FastAPI Structure (from Context7 Documentation)

Based on FastAPI official documentation and best practices:

```
project_name/
├── app/                          # Main application package
│   ├── __init__.py
│   ├── main.py                   # FastAPI app instance
│   ├── dependencies.py           # Shared dependencies
│   ├── api/                      # API endpoints
│   │   ├── __init__.py
│   │   └── v1/                   # API versioning
│   │       ├── __init__.py
│   │       └── endpoints/
│   │           ├── users.py
│   │           └── items.py
│   ├── core/                     # Core configuration
│   │   ├── config.py
│   │   └── security.py
│   ├── models/                   # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/                  # Pydantic schemas
│   │   ├── __init__.py
│   │   └── user.py
│   ├── services/                 # Business logic layer
│   │   ├── __init__.py
│   │   └── user_service.py
│   ├── templates/                # Jinja2 templates
│   │   ├── base.html
│   │   ├── index.html
│   │   └── components/
│   │       ├── navbar.html
│   │       └── footer.html
│   └── static/                   # Static files
│       ├── css/
│       │   └── style.css
│       ├── js/
│       │   └── script.js
│       └── images/
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── .env
├── requirements.txt
└── README.md
```

### 1.2 Key Principles (2025)

1. **Separation of Concerns**:
   - `api/` - API endpoints (REST)
   - `services/` - Business logic
   - `models/` - Database models
   - `schemas/` - Data validation
   - `templates/` - Frontend templates
   - `static/` - Static assets

2. **Template Organization**:
   ```
   templates/
   ├── base.html              # Base template with Jinja2 inheritance
   ├── pages/                 # Full page templates
   │   ├── dashboard.html
   │   └── login.html
   ├── partials/             # HTMX partial templates
   │   ├── dashboard_content.html
   │   └── data_content.html
   └── components/           # Reusable components (macros)
       ├── navbar.html
       └── cards.html
   ```

3. **Static Files**:
   ```
   static/
   ├── css/
   ├── js/
   │   └── htmx.min.js       # HTMX library
   └── images/
   ```

4. **FastAPI Configuration**:
   ```python
   from fastapi import FastAPI
   from fastapi.staticfiles import StaticFiles
   from fastapi.templating import Jinja2Templates

   app = FastAPI()

   # Mount static files
   app.mount("/static", StaticFiles(directory="app/static"), name="static")

   # Configure templates
   templates = Jinja2Templates(directory="app/templates")
   ```

---

## 2. Router Factory 2.0 Scaffolder Output

### 2.1 Generated Structure

The scaffolder generates:

```
tmp/router_factory_generated/
├── backend/
│   ├── database.py
│   └── src/
│       ├── models/              # ORM models by domain
│       │   ├── common/
│       │   ├── health/
│       │   └── {domain}/
│       ├── services/            # Service layer by domain
│       │   ├── common/
│       │   ├── health/
│       │   └── {domain}/
│       └── routers/            # Backend API routers
│           ├── base.py
│           └── {domain}_router.py
│
└── frontend/
    └── src/
        └── ui/
            ├── models/          # Frontend data models
            ├── middleware/      # UI middleware
            ├── routers/         # Frontend UI routers
            │   ├── base.py
            │   ├── core/
            │   │   ├── hub_router.py
            │   │   └── dashboard_router.py
            │   └── {domain}/    # Domain-specific routers
            │       └── static/  # Router-specific static files
            │           └── js/
            ├── services/        # UI services
            │   ├── template_service.py
            │   ├── renderer_service.py
            │   └── websocket/
            ├── templates/      # Jinja2 templates
            │   ├── base.html
            │   ├── pages/
            │   ├── partials/
            │   └── components/
            └── static/          # Global static assets
                ├── css/
                ├── js/
                └── images/
```

### 2.2 Key Differences from Best Practices

#### ✅ **What Matches Best Practices:**

1. **Separation of Backend/Frontend**: ✅
   - Clear separation: `backend/` and `frontend/`
   - Backend: `models/`, `services/`, `routers/`
   - Frontend: `templates/`, `static/`, `routers/`

2. **Template Organization**: ✅
   - `templates/pages/` - Full pages
   - `templates/partials/` - HTMX partials
   - `templates/components/` - Reusable components

3. **Static Files**: ✅
   - `static/css/`, `static/js/`, `static/images/`
   - Router-specific static files in `routers/{domain}/static/`

#### ⚠️ **What Differs from Best Practices:**

1. **Directory Depth**:
   - **Best Practice**: `app/templates/`, `app/static/`
   - **Scaffolder**: `frontend/src/ui/templates/`, `frontend/src/ui/static/`
   - **Impact**: Deeper nesting, but more organized

2. **API Structure**:
   - **Best Practice**: `app/api/v1/endpoints/`
   - **Scaffolder**: `backend/src/routers/{domain}_router.py`
   - **Impact**: Domain-based organization vs. versioned API structure

3. **Schemas Location**:
   - **Best Practice**: `app/schemas/` (separate Pydantic schemas)
   - **Scaffolder**: **NO separate schema files generated** - Only SQLAlchemy ORM models in `models/`
   - **Impact**: Schemas are not generated by default; routers use ORM models directly or schemas must be created manually

4. **Frontend Models**:
   - **Best Practice**: Not typically separate frontend models
   - **Scaffolder**: `frontend/src/ui/models/` for frontend-specific data structures
   - **Impact**: Additional organization layer for frontend-specific concerns

---

## 3. Comparison Matrix

| Aspect | FastAPI Best Practice | Router Factory 2.0 | Match? |
|--------|---------------------|-------------------|--------|
| **Backend/Frontend Separation** | Single `app/` package | Separate `backend/` and `frontend/` | ⚠️ Different approach |
| **Templates Location** | `app/templates/` | `frontend/src/ui/templates/` | ⚠️ Deeper nesting |
| **Static Files** | `app/static/` | `frontend/src/ui/static/` | ⚠️ Deeper nesting |
| **API Organization** | `app/api/v1/endpoints/` | `backend/src/routers/{domain}/` | ⚠️ Domain-based vs versioned |
| **Service Layer** | `app/services/` | `backend/src/services/{domain}/` | ✅ Matches (domain-organized) |
| **Models** | `app/models/` | `backend/src/models/{domain}/` | ✅ Matches (domain-organized) |
| **Schemas** | `app/schemas/` (separate) | **NOT GENERATED** (optional, disabled by default) | ❌ Missing |
| **Template Structure** | `pages/`, `partials/`, `components/` | `pages/`, `partials/`, `components/` | ✅ Matches |
| **HTMX Support** | Manual setup | Built-in HTMX infrastructure | ✅ Enhanced |

---

## 4. Analysis: Does Scaffolder Create Best Practice Structure?

### ✅ **YES - Core Principles Match:**

1. **Separation of Concerns**: ✅
   - Clear backend/frontend separation
   - Service layer separation
   - Template organization matches best practices

2. **Template Organization**: ✅
   - `pages/`, `partials/`, `components/` structure matches
   - Jinja2 inheritance pattern supported
   - HTMX integration built-in

3. **Static Files**: ✅
   - Proper static file organization
   - Router-specific static files supported

### ⚠️ **PARTIAL - Structural Differences:**

1. **Directory Depth**:
   - Scaffolder uses deeper nesting (`frontend/src/ui/` vs `app/`)
   - **Rationale**: Better organization for larger projects
   - **Trade-off**: More verbose paths, but clearer separation

2. **API Structure**:
   - Scaffolder uses domain-based organization vs. versioned API
   - **Rationale**: Domain-driven design approach
   - **Trade-off**: Less explicit versioning, but better domain organization

3. **Schemas**:
   - Scaffolder **does NOT generate Pydantic schemas** by default
   - Only SQLAlchemy ORM models are generated
   - Schema generation is optional (`generate_schemas=False` by default)
   - **Rationale**: Routers can use ORM models directly or schemas created manually
   - **Trade-off**: Schemas must be created separately if needed

### ❌ **NO - Missing Elements:**

1. **API Versioning**:
   - Best practice: `app/api/v1/endpoints/`
   - Scaffolder: `backend/src/routers/{domain}/`
   - **Recommendation**: Add versioning support

2. **Core Configuration**:
   - Best practice: `app/core/config.py`
   - Scaffolder: Configuration scattered
   - **Recommendation**: Centralize configuration

---

## 5. Recommendations

### 5.1 For Router Factory 2.0 Enhancement

1. **Add API Versioning Support**:
   ```
   backend/src/routers/
   ├── v1/
   │   └── {domain}_router.py
   └── v2/
       └── {domain}_router.py
   ```

2. **Centralize Configuration**:
   ```
   backend/src/core/
   ├── config.py
   └── security.py
   ```

3. **Enable Schema Generation** (Currently Optional):
   - Schema generation exists but is disabled by default (`generate_schemas=False`)
   - When enabled, creates stub Pydantic schema files in `schemas/` directory
   - **Recommendation**: Enable schema generation by default or provide option to generate schemas from ORM models

### 5.2 For Current Projects

The scaffolder output is **production-ready** and follows **modern best practices** with some enhancements:

- ✅ **Better**: Domain-driven organization
- ✅ **Better**: Built-in HTMX infrastructure
- ✅ **Better**: Frontend model separation
- ⚠️ **Different**: Deeper directory nesting (acceptable trade-off)
- ⚠️ **Different**: Domain-based vs. versioned API (both valid approaches)

---

## 6. Conclusion

### **Does the scaffolder create best practice structure?**

**YES** - The scaffolder creates a structure that:
- ✅ Follows FastAPI best practices for templates and static files
- ✅ Implements proper separation of concerns
- ✅ Supports HTMX + Jinja2 integration
- ⚠️ Uses domain-driven organization (alternative valid approach)
- ⚠️ Uses deeper nesting (acceptable for larger projects)

### **Recommendation:**

The scaffolder output is **production-ready** and aligns with FastAPI best practices, with some structural differences that are **acceptable trade-offs** for better organization in larger projects.

**Action Items:**
1. ✅ Current structure is valid and production-ready
2. ⚠️ Consider adding API versioning support as optional enhancement
3. ⚠️ Consider centralizing configuration in `core/` directory
4. ✅ Continue using domain-driven organization (matches modern best practices)

---

**Date**: 2025-12-05
**Status**: Analysis Complete
