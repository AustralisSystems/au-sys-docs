# FastAPI + HTMX + Jinja2 Best Practices 2025
**Version**: v1.0.0
**Last Updated**: 2025-01-14
**HTMX Version**: 2.0.0+
**Jinja2 Version**: Latest
**FastAPI Version**: Latest

This document compiles the latest best practices for building modern web applications with FastAPI, HTMX, and Jinja2 templating based on official documentation, production code examples, and community recommendations.

---

## Table of Contents

1. [Architecture Patterns](#architecture-patterns)
2. [HTMX Best Practices](#htmx-best-practices)
3. [Jinja2 Templating](#jinja2-templating)
4. [FastAPI Integration](#fastapi-integration)
5. [Dual-Response Pattern](#dual-response-pattern)
6. [Component Architecture](#component-architecture)
7. [Error Handling](#error-handling)
8. [Performance Optimization](#performance-optimization)
9. [Security Considerations](#security-considerations)
10. [Testing](#testing)

---

## Architecture Patterns

### ✅ Best Practices

#### 1. Dual-Response Pattern (HTMX Detection)

The most important pattern: detect HTMX requests and return partial HTML for HTMX, full pages for regular requests.

```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/users/", response_class=HTMLResponse)
async def get_users(request: Request):
    """Handle both HTMX and regular requests."""
    users = await get_users_from_db()

    # Check if this is an HTMX request
    is_htmx = request.headers.get("HX-Request") == "true"

    if is_htmx:
        # Return partial template for HTMX
        return templates.TemplateResponse(
            "partials/user_table.html",
            {"request": request, "users": users}
        )
    else:
        # Return full page for regular requests
        return templates.TemplateResponse(
            "users.html",
            {"request": request, "users": users}
        )
```

#### 2. Helper Function for HTMX Detection

```python
from fastapi import Request

def is_htmx_request(request: Request) -> bool:
    """Check if request is from HTMX."""
    return request.headers.get("HX-Request") == "true"

@app.get("/items/")
async def get_items(request: Request):
    if is_htmx_request(request):
        return templates.TemplateResponse("partials/items.html", {"request": request})
    return templates.TemplateResponse("items.html", {"request": request})
```

#### 3. Using FastHX Library (Recommended)

```python
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fasthx import Jinja
from pydantic import BaseModel

app = FastAPI()
jinja = Jinja(Jinja2Templates("templates"))

class User(BaseModel):
    name: str
    email: str

@app.get("/users/")
@jinja.hx("partials/user_list.html")  # HTMX partial
async def get_users() -> list[User]:
    return await get_users_from_db()

@app.get("/")
@jinja.page("index.html")  # Full page
def index() -> None:
    ...
```

---

## HTMX Best Practices

### ✅ Core Attributes

#### 1. Basic HTMX Attributes

```html
<!-- GET request -->
<button hx-get="/api/data"
        hx-target="#result"
        hx-swap="innerHTML">
    Load Data
</button>

<!-- POST request -->
<form hx-post="/api/submit"
      hx-target="#response"
      hx-swap="outerHTML">
    <input name="data" type="text">
    <button type="submit">Submit</button>
</form>

<!-- PUT/DELETE -->
<button hx-delete="/api/item/1"
        hx-target="#item-1"
        hx-swap="outerHTML">
    Delete
</button>
```

#### 2. Swap Strategies

```html
<!-- innerHTML (default) - Replace content inside -->
<div hx-get="/content" hx-swap="innerHTML">Loading...</div>

<!-- outerHTML - Replace entire element -->
<div hx-get="/content" hx-swap="outerHTML">Loading...</div>

<!-- beforebegin - Insert before element -->
<div id="target"></div>
<button hx-get="/content" hx-target="#target" hx-swap="beforebegin">Add Before</button>

<!-- afterbegin - Insert at start -->
<div id="target">Existing</div>
<button hx-get="/content" hx-target="#target" hx-swap="afterbegin">Add Start</button>

<!-- beforeend - Insert at end -->
<div id="target">Existing</div>
<button hx-get="/content" hx-target="#target" hx-swap="beforeend">Add End</button>

<!-- afterend - Insert after element -->
<div id="target"></div>
<button hx-get="/content" hx-target="#target" hx-swap="afterend">Add After</button>

<!-- none - No swap (for side effects) -->
<button hx-post="/api/log" hx-swap="none">Log Action</button>
```

#### 3. Trigger Options

```html
<!-- Click (default) -->
<button hx-get="/data">Click Me</button>

<!-- Multiple triggers -->
<button hx-get="/data" hx-trigger="click, keyup[key=='Enter']">Click or Enter</button>

<!-- Event filters -->
<button hx-get="/data" hx-trigger="click[ctrlKey]">Ctrl+Click</button>

<!-- Delayed trigger -->
<input hx-get="/search"
       hx-trigger="keyup changed delay:500ms"
       hx-target="#results">

<!-- Polling -->
<div hx-get="/status" hx-trigger="every 2s">Status</div>

<!-- Load trigger -->
<div hx-get="/content" hx-trigger="load">Auto-load</div>

<!-- Intersection observer -->
<div hx-get="/more" hx-trigger="intersect">Load More</div>
```

#### 4. Target Selection

```html
<!-- ID selector -->
<button hx-get="/data" hx-target="#result">Load</button>

<!-- Class selector -->
<button hx-get="/data" hx-target=".results">Load</button>

<!-- CSS selector -->
<button hx-get="/data" hx-target="main > .content">Load</button>

<!-- Closest parent -->
<button hx-get="/data" hx-target="closest div">Load</button>

<!-- Next sibling -->
<button hx-get="/data" hx-target="next .content">Load</button>

<!-- Previous sibling -->
<button hx-get="/data" hx-target="previous .content">Load</button>

<!-- Find -->
<button hx-get="/data" hx-target="find .result">Load</button>
```

#### 5. Request Headers

```html
<!-- Send custom headers -->
<button hx-get="/api/data"
        hx-headers='{"X-Custom-Header": "value"}'>
    Load
</button>

<!-- Include CSRF token -->
<form hx-post="/api/submit"
      hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'>
    ...
</form>
```

#### 6. Request Values

```html
<!-- Static values -->
<button hx-get="/api/data"
        hx-vals='{"filter": "active", "sort": "name"}'>
    Filter
</button>

<!-- Dynamic values from form -->
<form hx-post="/api/search">
    <input name="query" id="search-query">
    <button hx-vals='js:{query: document.getElementById("search-query").value}'>
        Search
    </button>
</form>
```

#### 7. Response Headers

```python
from fastapi import Response

@app.get("/redirect")
async def redirect_handler(request: Request):
    if is_htmx_request(request):
        return Response(
            content="<div>Redirected content</div>",
            headers={"HX-Redirect": "/new-location"}
        )
    return RedirectResponse("/new-location")
```

```python
# Trigger client-side event
@app.post("/update")
async def update_handler(request: Request):
    return Response(
        content="<div>Updated</div>",
        headers={"HX-Trigger": "updateComplete"}
    )
```

```html
<!-- Listen for event -->
<div hx-on:update-complete="showNotification()">
    Content
</div>
```

#### 8. Loading Indicators

```html
<!-- Inline indicator -->
<button hx-get="/data" hx-indicator="#spinner">
    Load Data
    <span id="spinner" class="htmx-indicator">Loading...</span>
</button>

<!-- External indicator -->
<div id="spinner" class="htmx-indicator">
    <div class="spinner"></div>
</div>
<button hx-get="/data" hx-indicator="#spinner">Load</button>

<!-- CSS for indicators -->
<style>
.htmx-indicator {
    opacity: 0;
    transition: opacity 200ms ease-in;
}
.htmx-request .htmx-indicator,
.htmx-request.htmx-indicator {
    opacity: 1;
}
</style>
```

#### 9. Disable Elements During Request

```html
<!-- Disable button -->
<button hx-post="/submit"
        hx-disabled-elt="this">
    Submit
</button>

<!-- Disable form elements -->
<form hx-post="/submit"
      hx-disabled-elt="find button, find input">
    <input name="data">
    <button type="submit">Submit</button>
</form>
```

#### 10. Confirmation and Prompts

```html
<!-- Confirmation dialog -->
<button hx-delete="/item/1"
        hx-confirm="Are you sure?">
    Delete
</button>

<!-- Prompt for input -->
<button hx-post="/rename"
        hx-prompt="Enter new name:">
    Rename
</button>
```

#### 11. CSS Transitions

```html
<style>
.fade-me-out.htmx-swapping {
    opacity: 0;
    transition: opacity 1s ease-out;
}

.fade-me-in.htmx-added {
    opacity: 0;
}
.fade-me-in {
    opacity: 1;
    transition: opacity 1s ease-in;
}
</style>

<button class="fade-me-out"
        hx-delete="/item"
        hx-swap="outerHTML swap:1s">
    Fade Out
</button>

<div class="fade-me-in"
     hx-get="/content"
     hx-swap="innerHTML settle:1s">
    Content
</div>
```

#### 12. View Transitions API

```html
<style>
@keyframes fade-in { from { opacity: 0; } }
@keyframes fade-out { to { opacity: 0; } }

::view-transition-old(slide-it) {
    animation: fade-out 180ms;
}
::view-transition-new(slide-it) {
    animation: fade-in 420ms;
}

.slide-it {
    view-transition-name: slide-it;
}
</style>

<div class="slide-it">
    <button hx-get="/new-content"
            hx-swap="innerHTML transition:true">
        Swap Content
    </button>
</div>
```

---

## Jinja2 Templating

### ✅ Best Practices

#### 1. Template Inheritance

```jinja
<!-- base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Default Title{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', path='/css/app.css') }}">
    <script src="https://unpkg.com/htmx.org@2.0.0"></script>
    {% block extra_head %}{% endblock %}
</head>
<body>
    <nav>{% block nav %}{% endblock %}</nav>
    <main>{% block content %}{% endblock %}</main>
    {% block extra_scripts %}{% endblock %}
</body>
</html>

<!-- page.html -->
{% extends "base.html" %}

{% block title %}My Page{% endblock %}

{% block content %}
<h1>Welcome</h1>
<p>Content here</p>
{% endblock %}
```

#### 2. Using Super() in Blocks

```jinja
<!-- base.html -->
{% block sidebar %}
    <h3>Default Sidebar</h3>
{% endblock %}

<!-- page.html -->
{% extends "base.html" %}

{% block sidebar %}
    <h3>Custom Sidebar</h3>
    {{ super() }}  <!-- Include parent content -->
    <p>Additional content</p>
{% endblock %}
```

#### 3. Required Blocks

```jinja
<!-- base.html -->
{% block content required %}{% endblock %}

<!-- page.html -->
{% extends "base.html" %}
{% block content %}
    <!-- Must override, otherwise TemplateRuntimeError -->
    <h1>Content</h1>
{% endblock %}
```

#### 4. Macros for Reusable Components

```jinja
<!-- macros.html -->
{% macro input_field(name, type="text", placeholder="", value="", required=false) %}
<div class="form-group">
    <label for="{{ name }}">{{ name|title }}</label>
    <input type="{{ type }}"
           id="{{ name }}"
           name="{{ name }}"
           placeholder="{{ placeholder }}"
           value="{{ value }}"
           {% if required %}required{% endif %}
           class="form-control">
</div>
{% endmacro %}

{% macro button(text, type="button", variant="primary") %}
<button type="{{ type }}" class="btn btn-{{ variant }}">
    {{ text }}
</button>
{% endmacro %}

<!-- form.html -->
{% import "macros.html" as forms %}

<form hx-post="/submit" hx-target="#result">
    {{ forms.input_field("username", placeholder="Enter username", required=true) }}
    {{ forms.input_field("email", type="email", placeholder="Enter email") }}
    {{ forms.button("Submit", type="submit") }}
</form>
```

#### 5. Macros with Call Blocks

```jinja
<!-- macros.html -->
{% macro card(title, class="") %}
<div class="card {{ class }}">
    <div class="card-header">
        <h3>{{ title }}</h3>
    </div>
    <div class="card-body">
        {{ caller() }}
    </div>
</div>
{% endmacro %}

<!-- page.html -->
{% import "macros.html" as components %}

{% call components.card("User Profile") %}
    <p>User information goes here</p>
    <button>Edit</button>
{% endcall %}
```

#### 6. Includes for Partial Templates

```jinja
<!-- partials/user_row.html -->
<tr>
    <td>{{ user.name }}</td>
    <td>{{ user.email }}</td>
    <td>
        <button hx-delete="/users/{{ user.id }}"
                hx-target="closest tr"
                hx-swap="outerHTML">
            Delete
        </button>
    </td>
</tr>

<!-- users.html -->
<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        {% for user in users %}
            {% include "partials/user_row.html" %}
        {% endfor %}
    </tbody>
</table>
```

#### 7. Filters

```jinja
<!-- Built-in filters -->
{{ user.name|upper }}
{{ user.email|lower }}
{{ description|truncate(50) }}
{{ price|currency }}
{{ date|dateformat("%Y-%m-%d") }}
{{ html_content|safe }}
{{ text|default("No content") }}

<!-- Custom filters -->
{{ user.created_at|timeago }}
{{ content|markdown }}
{{ url|urlencode }}
```

#### 8. Custom Filters

```python
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def timeago_filter(dt):
    """Convert datetime to timeago string."""
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc)
    diff = now - dt
    if diff.days > 365:
        return f"{diff.days // 365} years ago"
    elif diff.days > 30:
        return f"{diff.days // 30} months ago"
    elif diff.days > 0:
        return f"{diff.days} days ago"
    elif diff.seconds > 3600:
        return f"{diff.seconds // 3600} hours ago"
    else:
        return f"{diff.seconds // 60} minutes ago"

templates.env.filters["timeago"] = timeago_filter
```

#### 9. Global Variables

```python
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Add global variables
templates.env.globals["settings"] = settings
templates.env.globals["url_for"] = url_for
templates.env.globals["get_feature_context"] = get_feature_context
```

#### 10. Scoped Blocks

```jinja
<!-- Access outer scope variables -->
{% for user in users %}
    <div>
        {% block user_card scoped %}
            <h3>{{ user.name }}</h3>
            <p>{{ user.email }}</p>
        {% endblock %}
    </div>
{% endfor %}
```

#### 11. Template Fragments (for HTMX)

```python
from jinja2_fragments import render_block

@app.get("/users/")
async def get_users(request: Request):
    users = await get_users_from_db()

    if is_htmx_request(request):
        # Render only the table block
        return render_block(
            "users.html",
            "user_table",
            users=users,
            request=request
        )
    return templates.TemplateResponse("users.html", {"request": request, "users": users})
```

```jinja
<!-- users.html -->
{% extends "base.html" %}

{% block content %}
<div id="user-table">
    {% block user_table %}
    <table>
        {% for user in users %}
        <tr>
            <td>{{ user.name }}</td>
            <td>{{ user.email }}</td>
        </tr>
        {% endfor %}
    </table>
    {% endblock %}
</div>
{% endblock %}
```

---

## FastAPI Integration

### ✅ Best Practices

#### 1. Jinja2Templates Setup

```python
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Add globals
templates.env.globals["settings"] = settings
templates.env.globals["url_for"] = url_for

# Add filters
templates.env.filters["timeago"] = timeago_filter
```

#### 2. Template Response Pattern

```python
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "Home"}
    )
```

#### 3. HTMX Request Detection

```python
from fastapi import Request

def is_htmx_request(request: Request) -> bool:
    """Check if request is from HTMX."""
    return request.headers.get("HX-Request") == "true"

def get_htmx_target(request: Request) -> str | None:
    """Get HTMX target from request."""
    return request.headers.get("HX-Target")

def get_htmx_trigger(request: Request) -> str | None:
    """Get HTMX trigger from request."""
    return request.headers.get("HX-Trigger")
```

#### 4. Dual-Response Helper

```python
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

templates = Jinja2Templates(directory="templates")

async def render_response(
    request: Request,
    full_template: str,
    partial_template: str,
    context: dict
):
    """Render full page or partial based on HTMX request."""
    template = partial_template if is_htmx_request(request) else full_template
    return templates.TemplateResponse(
        template,
        {"request": request, **context}
    )

@app.get("/users/", response_class=HTMLResponse)
async def get_users(request: Request):
    users = await get_users_from_db()
    return await render_response(
        request,
        "users.html",
        "partials/user_table.html",
        {"users": users}
    )
```

#### 5. HTMX Response Headers

```python
from fastapi import Response

@app.post("/update")
async def update_item(request: Request):
    # Process update
    await update_item_in_db()

    if is_htmx_request(request):
        return Response(
            content="<div>Updated successfully</div>",
            headers={
                "HX-Trigger": "updateComplete",
                "HX-Refresh": "true"  # Refresh page
            }
        )
    return RedirectResponse("/items")
```

#### 6. Error Handling for HTMX

```python
from fastapi import Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

templates = Jinja2Templates(directory="templates")

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if is_htmx_request(request):
        return templates.TemplateResponse(
            "partials/error.html",
            {"request": request, "error": exc.detail},
            status_code=exc.status_code
        )
    return templates.TemplateResponse(
        "error.html",
        {"request": request, "error": exc.detail},
        status_code=exc.status_code
    )
```

---

## Component Architecture

### ✅ Best Practices

#### 1. Template Organization

```
templates/
├── base.html              # Base layout
├── index.html             # Home page
├── users/
│   ├── list.html          # Full user list page
│   └── detail.html        # User detail page
├── partials/               # HTMX partials
│   ├── user_table.html    # User table component
│   ├── user_row.html      # Single user row
│   ├── user_form.html     # User form component
│   └── error_message.html # Error component
├── components/             # Reusable components
│   ├── card.html          # Card component
│   ├── modal.html         # Modal component
│   └── form_field.html    # Form field component
└── macros.html            # Jinja2 macros
```

#### 2. Component Pattern

```jinja
<!-- components/card.html -->
<div class="card {{ class }}">
    <div class="card-header">
        <h3>{{ title }}</h3>
    </div>
    <div class="card-body">
        {% block card_content %}{% endblock %}
    </div>
</div>

<!-- Usage -->
{% include "components/card.html" %}
{% block card_content %}
    <p>Card content</p>
{% endblock %}
```

#### 3. Partial Templates for HTMX

```jinja
<!-- partials/user_row.html -->
<tr id="user-{{ user.id }}">
    <td>{{ user.name }}</td>
    <td>{{ user.email }}</td>
    <td>
        <button hx-get="/users/{{ user.id }}/edit"
                hx-target="#user-{{ user.id }}"
                hx-swap="outerHTML">
            Edit
        </button>
        <button hx-delete="/users/{{ user.id }}"
                hx-target="#user-{{ user.id }}"
                hx-swap="outerHTML"
                hx-confirm="Delete user?">
            Delete
        </button>
    </td>
</tr>
```

---

## Error Handling

### ✅ Best Practices

#### 1. HTMX Error Responses

```python
from fastapi import Request, HTTPException
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

@app.post("/users/")
async def create_user(request: Request, user_data: UserCreate):
    try:
        user = await create_user_in_db(user_data)
        if is_htmx_request(request):
            return templates.TemplateResponse(
                "partials/user_row.html",
                {"request": request, "user": user}
            )
        return RedirectResponse("/users/", status_code=303)
    except ValidationError as e:
        if is_htmx_request(request):
            return templates.TemplateResponse(
                "partials/error_message.html",
                {"request": request, "errors": e.errors()},
                status_code=422
            )
        raise HTTPException(status_code=422, detail=e.errors())
```

#### 2. Global Error Handler

```python
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    if is_htmx_request(request):
        return templates.TemplateResponse(
            "partials/validation_errors.html",
            {"request": request, "errors": exc.errors()},
            status_code=422
        )
    # Return JSON for API requests
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )
```

---

## Performance Optimization

### ✅ Best Practices

#### 1. Template Caching

```python
from fastapi.templating import Jinja2Templates

# Enable auto-reload only in development
templates = Jinja2Templates(
    directory="templates",
    auto_reload=False  # Disable in production
)
```

#### 2. Lazy Loading with HTMX

```html
<!-- Load content on scroll -->
<div hx-get="/more-items"
     hx-trigger="intersect"
     hx-swap="afterend">
    Load More
</div>

<!-- Load on page load -->
<div hx-get="/dashboard/stats"
     hx-trigger="load"
     hx-target="this">
    Loading stats...
</div>
```

#### 3. Debouncing Search

```html
<input type="search"
       name="query"
       hx-get="/search"
       hx-trigger="keyup changed delay:500ms"
       hx-target="#results"
       hx-indicator="#spinner">
```

#### 4. Preloading

```html
<!-- Preload on hover -->
<a href="/page"
   hx-get="/page"
   hx-trigger="mouseenter"
   hx-swap="none"
   hx-preload="true">
    Hover to preload
</a>
```

---

## Security Considerations

### ✅ Best Practices

#### 1. CSRF Protection

```python
from fastapi import Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

def get_csrf_token() -> str:
    """Generate CSRF token."""
    import secrets
    return secrets.token_urlsafe(32)

@app.get("/form")
async def show_form(request: Request):
    csrf_token = get_csrf_token()
    request.session["csrf_token"] = csrf_token
    return templates.TemplateResponse(
        "form.html",
        {"request": request, "csrf_token": csrf_token}
    )
```

```html
<!-- Include CSRF token in HTMX requests -->
<form hx-post="/submit"
      hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'>
    <input name="data">
    <button type="submit">Submit</button>
</form>
```

#### 2. Content Security Policy

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["example.com", "*.example.com"]
)
```

#### 3. XSS Prevention

```jinja
<!-- Auto-escaping (default) -->
{{ user_input }}  <!-- Escaped -->

<!-- Safe HTML (use carefully) -->
{{ trusted_html|safe }}

<!-- Markdown -->
{{ markdown_content|markdown }}
```

---

## Testing

### ✅ Best Practices

#### 1. Testing HTMX Requests

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_htmx_request():
    """Test HTMX partial response."""
    response = client.get(
        "/users/",
        headers={"HX-Request": "true"}
    )
    assert response.status_code == 200
    assert "user_table" in response.text
    assert "<!DOCTYPE html>" not in response.text  # Should be partial

def test_regular_request():
    """Test full page response."""
    response = client.get("/users/")
    assert response.status_code == 200
    assert "<!DOCTYPE html>" in response.text  # Should be full page
```

#### 2. Testing Template Rendering

```python
def test_template_rendering():
    """Test template renders correctly."""
    response = client.get("/users/")
    assert "User List" in response.text
    assert "users" in response.text
```

---

## Summary Checklist

### HTMX
- [ ] Proper use of hx-get, hx-post, hx-put, hx-delete
- [ ] Appropriate swap strategies selected
- [ ] Loading indicators implemented
- [ ] Error handling for HTMX requests
- [ ] Response headers used (HX-Trigger, HX-Redirect)
- [ ] Debouncing for search/input
- [ ] CSS transitions configured

### Jinja2
- [ ] Template inheritance properly used
- [ ] Macros for reusable components
- [ ] Includes for partial templates
- [ ] Custom filters defined
- [ ] Global variables configured
- [ ] Required blocks used where needed
- [ ] Scoped blocks for loops

### FastAPI Integration
- [ ] Dual-response pattern implemented
- [ ] HTMX request detection helper
- [ ] Template fragments for HTMX
- [ ] Error handling for HTMX vs regular requests
- [ ] CSRF protection implemented
- [ ] Template caching configured

### Architecture
- [ ] Clear separation of partials and full pages
- [ ] Component-based template organization
- [ ] Consistent naming conventions
- [ ] Proper template directory structure

---

## References

- [HTMX Documentation](https://htmx.org/docs/)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FastHX Library](https://github.com/volfpeter/fasthx)
- [Jinja2 Fragments](https://github.com/sponsfreixes/jinja2-fragments)

---

**Note:** This document is based on HTMX 2.0.0+, Jinja2 latest, and FastAPI latest. Always refer to official documentation for the most up-to-date information.
