# HTMX CSP CSS Security Best Practices 2025

**Version**: 1.0.0
**Last Updated**: 2025-12-23
**Status**: Production
**Category**: Security, Frontend Architecture, Build Process
**Applies To**: All projects using HTMX with strict Content Security Policy

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Problem Statement](#problem-statement)
3. [Core Principles](#core-principles)
4. [Security Requirements](#security-requirements)
5. [Architecture Best Practices](#architecture-best-practices)
6. [Content Security Policy (CSP) Configuration](#content-security-policy-csp-configuration)
7. [HTMX Configuration Best Practices](#htmx-configuration-best-practices)
8. [CSS Build Process Best Practices](#css-build-process-best-practices)
9. [Nonce Configuration Best Practices](#nonce-configuration-best-practices)
10. [Docker Build Best Practices](#docker-build-best-practices)
11. [CI/CD Pipeline Best Practices](#cicd-pipeline-best-practices)
12. [Development Workflow Best Practices](#development-workflow-best-practices)
13. [Troubleshooting Guide](#troubleshooting-guide)
14. [Security Audit Checklist](#security-audit-checklist)
15. [Compliance Verification](#compliance-verification)

---

## Executive Summary

This document provides comprehensive best practices for integrating HTMX with strict Content Security Policy (CSP) compliance. The solution eliminates the need for `'unsafe-inline'` in CSP directives by providing HTMX indicator styles via external CSS compiled during build time.

### Key Outcomes

- ✅ **Strict CSP Compliance**: No `'unsafe-inline'` required
- ✅ **Full HTMX Functionality**: All indicators and animations work seamlessly
- ✅ **Maintainable**: Styles defined in CSS framework config, not hard-coded
- ✅ **Secure**: Prevents XSS attacks via style injection
- ✅ **Build-Time Compilation**: CSS built during Docker/CI-CD builds, not at runtime

### Target Audience

- Frontend developers working with HTMX
- Security engineers implementing CSP
- DevOps engineers configuring build pipelines
- Architects designing secure web applications

---

## Problem Statement

### The CSP Violation Challenge

HTMX, by default, injects inline `<style>` tags into the document `<head>` when `htmx.config.includeIndicatorStyles = true` (default). These inline styles violate strict Content Security Policy directives that prohibit `'unsafe-inline'` in `style-src`.

**Common Error**:
```
Applying inline style violates the following Content Security Policy directive
'style-src 'self' 'nonce-...' https://cdn.jsdelivr.net ...'.
Either the 'unsafe-inline' keyword, a hash ('sha256-...'), or a nonce ('nonce-...')
is required to enable inline execution.
```

### Why Common Solutions Fail

#### ❌ Using `'unsafe-inline'`

**Problems**:
- **Weakens Security**: Allows any inline styles, making XSS attacks easier
- **Violates Best Practices**: CSP guidelines recommend avoiding `'unsafe-inline'`
- **Reduces Protection**: Defeats the purpose of CSP for style injection attacks
- **Compliance Issues**: May violate security compliance requirements (OWASP, PCI-DSS)

#### ❌ Using SHA-256 Hashes

**Problems**:
- **Brittle**: Hash changes with every HTMX version update
- **Maintenance Burden**: Requires updating CSP config for each HTMX release
- **Error-Prone**: Hard-coded hashes break when HTMX changes its style content
- **Not Scalable**: Multiple hashes needed if HTMX injects different styles
- **Version Lock-In**: Prevents easy HTMX upgrades

#### ✅ Recommended Solution: External CSS with Build-Time Compilation

**Benefits**:
- **Secure**: No inline styles, strict CSP compliance
- **Maintainable**: Styles defined in CSS framework config
- **Upgrade-Friendly**: HTMX can be upgraded without CSP changes
- **Performance**: CSS cached by browser, single HTTP request
- **Flexible**: Easy to customize HTMX indicator styles

---

## Core Principles

### 1. Security First

**MANDATORY**: Security must never be compromised for convenience.

- **Never use `'unsafe-inline'`** in CSP `style-src` directive
- **Prefer external CSS** over inline styles
- **Use nonces** only when absolutely necessary for legitimate inline styles
- **Regular security audits** of CSP configuration

### 2. Build-Time Compilation

**MANDATORY**: CSS must be compiled during build time, not at runtime.

- **Docker builds**: CSS compiled in builder stage
- **CI/CD pipelines**: CSS built before deployment
- **Local development**: CSS built before testing
- **Never compile CSS** in production runtime

### 3. Framework Integration

**MANDATORY**: HTMX styles must be integrated into your CSS framework.

- **Use CSS framework plugins** (Tailwind, PostCSS, etc.)
- **Define HTMX utilities** in framework config
- **Compile into single CSS file** with other styles
- **Avoid hard-coding** styles in templates

### 4. Configuration Management

**MANDATORY**: Configuration must be centralized and version-controlled.

- **CSP config** in version-controlled files
- **HTMX config** in templates or global JS
- **CSS framework config** in version-controlled files
- **Build config** in CI/CD pipelines

---

## Security Requirements

### Content Security Policy Requirements

**MANDATORY**: The Content Security Policy MUST:

1. **Prohibit `'unsafe-inline'`** in `style-src` directive
2. **Use nonce-based CSP** for legitimate inline styles (when absolutely necessary)
3. **Allow external CSS** from `'self'` and trusted CDNs
4. **Support HTMX functionality** without CSP violations
5. **Include `'self'`** in `style-src` to allow local CSS files
6. **Specify trusted CDNs** explicitly (no wildcards)

### HTMX Configuration Requirements

**MANDATORY**: HTMX MUST be configured to:

1. **Disable inline style injection**: `htmx.config.includeIndicatorStyles = false`
2. **Use external CSS** for indicator styles
3. **Maintain full functionality** (loading indicators, swap animations, etc.)
4. **Be configured globally** in base templates or global JS files

### Build Process Requirements

**MANDATORY**: The build process MUST:

1. **Compile CSS during Docker/CI-CD builds** (not at runtime)
2. **Include HTMX styles** in compiled CSS
3. **Verify CSS build success** before deployment
4. **Fail build** if CSS compilation fails
5. **Remove build dependencies** from production images (multi-stage builds)

---

## Architecture Best Practices

### High-Level Architecture Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                    Build Time (Docker/CI-CD)                 │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  1. Install Node.js & npm                                    │
│  2. Copy CSS framework config & source files                  │
│  3. Install npm dependencies (CSS framework, PostCSS, etc.)   │
│  4. Run: npm run build:css                                   │
│     └─> CSS framework scans templates & JS files             │
│     └─> Includes HTMX styles from framework config           │
│     └─> Outputs: compiled.css (minified)                     │
│  5. Verify CSS file exists                                   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Runtime (Production)                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────┐  │
│  │   Browser    │─────▶│   Web App    │─────▶│  Static  │  │
│  │              │      │   Server     │      │  Files   │  │
│  └──────────────┘      └──────────────┘      └──────────┘  │
│         │                      │                    │        │
│         │  Request             │                    │        │
│         │──────────────────────┘                    │        │
│         │                                            │        │
│         │  Response (HTML + CSS)                    │        │
│         │◀──────────────────────────────────────────┘        │
│         │                                                    │
│         │  <link rel="stylesheet" href="/static/css.css">   │
│         │  <script src="/static/js/htmx.min.js">           │
│         │  <script>htmx.config.includeIndicatorStyles = false;</script>│
│         │                                                    │
│         │  HTMX adds classes (htmx-request, htmx-loading)   │
│         │  External CSS styles those classes                │
│         │  No inline styles = CSP compliant                 │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Component Interaction Pattern

1. **CSS Framework Config Plugin**: Defines HTMX utility classes
2. **Build Process**: Compiles HTMX styles into single CSS file
3. **HTMX Configuration**: Disables inline style injection globally
4. **CSP Middleware**: Enforces strict CSP without `'unsafe-inline'`
5. **Browser**: Loads external CSS, HTMX adds classes, CSS styles them

### Architecture Decision Records

**ADR-001: External CSS Over Inline Styles**
- **Decision**: Use external CSS compiled at build time
- **Rationale**: Maintains strict CSP compliance while preserving HTMX functionality
- **Consequences**: Requires build-time CSS compilation, adds Node.js to build process

**ADR-002: CSS Framework Integration**
- **Decision**: Integrate HTMX styles into CSS framework (Tailwind, PostCSS, etc.)
- **Rationale**: Centralized style management, consistent with project architecture
- **Consequences**: Requires CSS framework configuration, adds framework dependency

**ADR-003: Build-Time Compilation**
- **Decision**: Compile CSS during Docker/CI-CD builds, not at runtime
- **Rationale**: Performance, security, and maintainability
- **Consequences**: Requires Node.js in build environment, adds build step

---

## Content Security Policy (CSP) Configuration

### CSP Directive Best Practices

#### `style-src` Directive

**MANDATORY Configuration**:
```yaml
style_src:
  - "'self'"                    # Allow CSS from same origin
  - "{nonce}"                    # Nonce for legitimate inline styles (if needed)
  # Trusted CDNs (explicit, no wildcards)
  - "https://cdn.jsdelivr.net"
  - "https://fonts.googleapis.com"
  - "https://cdnjs.cloudflare.com"
  # Development only (remove in production)
  - "http://localhost:*"
  - "https://localhost:*"
```

**FORBIDDEN**:
- ❌ `'unsafe-inline'` - Never use this
- ❌ Hard-coded SHA-256 hashes for HTMX styles
- ❌ Wildcards (`*`) in CDN URLs
- ❌ `data:` URI scheme (unless absolutely necessary)

#### `script-src` Directive

**MANDATORY Configuration**:
```yaml
script_src:
  - "'self'"                    # Allow scripts from same origin
  - "{nonce}"                    # Nonce for legitimate inline scripts
  # HTMX CDN (if using CDN version)
  - "https://unpkg.com"
  - "https://cdn.jsdelivr.net"
```

**CRITICAL**: Inline scripts MUST use nonce attributes:
- ✅ **Use nonces** for inline scripts (HTMX configuration, Alpine.js initialization, etc.)
- ✅ **Generate nonce per request** using cryptographically secure random generator
- ✅ **Safely extract nonce** in template service using `getattr(request.state, "csp_nonce", "")` to prevent AttributeError
- ✅ **Add nonce to template context** as `csp_nonce` for safe access in templates
- ✅ **Add nonce to CSP header** in `script-src` directive
- ✅ **Add nonce attribute** to inline `<script>` tags in templates: `nonce="{{ csp_nonce }}"`
- ❌ **Never use `'unsafe-inline'`** in `script-src` directive
- ❌ **Avoid SHA-256 hashes** for inline scripts (nonces are more flexible)
- ❌ **Never access `request.state.csp_nonce` directly** in templates (use `{{ csp_nonce }}` from context)

### CSP Configuration Files

**Best Practice**: Store CSP configuration in version-controlled files:

1. **Primary Configuration**: YAML/JSON config files (migrated to database at runtime)
2. **Default Fallback**: Hard-coded defaults in middleware/security code
3. **Environment-Specific**: Separate configs for development, staging, production

**Example Structure**:
```
config/
  security/
    csp/
      development.yaml
      staging.yaml
      production.yaml
```

### CSP Nonce Generation

**MANDATORY**: If nonces are used, they MUST be:

1. **Cryptographically random**: Use secure random number generator
2. **Unique per request**: Generate new nonce for each HTTP request
3. **Included in CSP header**: Add nonce to `style-src` and `script-src` directives
4. **Added to HTML elements**: Include `nonce` attribute in `<style>` and `<script>` tags
5. **Safely extracted in template service**: Use `getattr(request.state, "csp_nonce", "")` to prevent AttributeError

**Example Implementation (Middleware)**:
```python
import secrets
from fastapi import Request

async def process_request(self, request: Request) -> None:
    """Generate CSP nonce for nonce-based CSP."""
    # Generate CSP nonce for nonce-based Content Security Policy
    # Nonce is a random value that changes per request, allowing inline scripts/styles
    # with matching nonce attribute while preventing XSS attacks
    nonce = secrets.token_urlsafe(16)
    if not hasattr(request.state, "csp_nonce"):
        request.state.csp_nonce = nonce
```

**Example Implementation (Template Service)**:
```python
# In UITemplateService._prepare_context() method
# CRITICAL: Safely extract CSP nonce to prevent AttributeError during template rendering
csp_nonce = ""
try:
    if hasattr(request, "state") and hasattr(request.state, "csp_nonce"):
        csp_nonce = getattr(request.state, "csp_nonce", "")
except (AttributeError, TypeError):
    # Nonce not available - use empty string (will be handled by CSP config)
    csp_nonce = ""

# Add nonce to template context
base_context = {
    "request": request,
    "csp_nonce": csp_nonce,  # Safe access in templates
    # ... other context variables ...
}
```

**Example Implementation (Template)**:
```html
<!-- In Jinja2 templates -->
<!-- CRITICAL CSP COMPLIANCE: Inline script requires nonce attribute -->
<!-- Nonce is generated per-request by SecurityHeadersMiddleware, safely extracted by UITemplateService, -->
<!-- and added to template context as 'csp_nonce' to prevent AttributeError -->
<script nonce="{{ csp_nonce }}">
  // HTMX Global Configuration
  if (typeof htmx !== 'undefined') {
    htmx.config.includeIndicatorStyles = false;
    // ... other HTMX config ...
  }
</script>

<!-- For inline styles (if absolutely necessary) -->
<style nonce="{{ csp_nonce }}">
  /* Legitimate inline styles */
</style>
```

**Example Implementation (CSP Header)**:
```python
# CSP header is built automatically by middleware
# The {nonce} placeholder in CSP config is replaced with actual nonce directive
csp_header = f"script-src 'self' 'nonce-{csp_nonce}' ...; style-src 'self' 'nonce-{csp_nonce}' ..."
```

---

## HTMX Configuration Best Practices

### Global HTMX Configuration

**MANDATORY**: Configure HTMX globally in base templates or global JS files:

```html
<!-- CRITICAL CSP COMPLIANCE: Inline script requires nonce attribute -->
<!-- Nonce is generated per-request by SecurityHeadersMiddleware, safely extracted by UITemplateService, -->
<!-- and added to template context as 'csp_nonce' to prevent AttributeError -->
<script nonce="{{ csp_nonce }}">
  // In base template or global JS file
  document.addEventListener('DOMContentLoaded', function() {
    if (typeof htmx !== 'undefined') {
      // CRITICAL CSP FIX: Disable inline styles to comply with strict CSP
      // HTMX indicator styles provided via external CSS
      htmx.config.includeIndicatorStyles = false;

      // Optional: Configure other HTMX settings
      htmx.config.globalViewTransition = true;
      htmx.config.useTemplateFragments = true;
    }
  });
</script>
```

**CRITICAL**: All inline scripts MUST include nonce attribute:
- ✅ **Add `nonce="{{ csp_nonce }}"`** to all inline `<script>` tags (nonce is safely extracted by template service)
- ✅ **Nonce is generated per-request** by security middleware (`SecurityHeadersMiddleware`)
- ✅ **Nonce is safely extracted** by `UITemplateService._prepare_context()` using `getattr(request.state, "csp_nonce", "")`
- ✅ **Nonce is added to template context** as `csp_nonce` for safe access in all templates
- ✅ **CSP header includes nonce** in `script-src` directive automatically
- ✅ **Defaults to empty string** if nonce is not available (prevents AttributeError during template rendering)
- ❌ **Never omit nonce** from inline scripts (will be blocked by CSP)
- ❌ **Never access `request.state.csp_nonce` directly** in templates (use `{{ csp_nonce }}` from context)

### Configuration Locations

**Best Practice**: Place HTMX configuration in:

1. **Base Templates**: Global configuration for all pages
2. **Layout Templates**: Page-specific configuration
3. **Global JS Files**: Centralized configuration file

**Avoid**:
- ❌ Inline configuration in individual templates
- ❌ Duplicate configuration across multiple files
- ❌ Configuration in page-specific scripts

### HTMX Indicator Classes

**MANDATORY**: Ensure HTMX indicator classes are defined in CSS:

```css
/* HTMX Loading States */
.htmx-indicator {
  display: none;
}

.htmx-request .htmx-indicator,
.htmx-request.htmx-indicator {
  display: inline-block;
}

.htmx-loading {
  opacity: 0.6;
  pointer-events: none;
}

.htmx-swapping {
  opacity: 1;
  transition: opacity 0.2s ease-out;
}

.htmx-settling {
  opacity: 1;
  transition: opacity 0.2s ease-in;
}
```

---

## CSS Build Process Best Practices

### CSS Framework Integration

**MANDATORY**: Integrate HTMX styles into your CSS framework:

#### Tailwind CSS Example

```javascript
// tailwind.config.js
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx}',
    './src/**/*.html',
    './templates/**/*.html',
  ],
  plugins: [
    function({ addUtilities }) {
      // HTMX Loading States
      addUtilities({
        '.htmx-indicator': {
          display: 'none',
        },
        '.htmx-request .htmx-indicator, .htmx-request.htmx-indicator': {
          display: 'inline-block',
        },
        '.htmx-loading': {
          opacity: '0.6',
          pointerEvents: 'none',
        },
        '.htmx-swapping': {
          opacity: '1',
          transition: 'opacity 0.2s ease-out',
        },
        '.htmx-settling': {
          opacity: '1',
          transition: 'opacity 0.2s ease-in',
        },
      });
    }
  ],
};
```

#### PostCSS Example

```javascript
// postcss.config.js
module.exports = {
  plugins: {
    tailwindcss: {
      config: './tailwind.config.js',
    },
    autoprefixer: {},
  },
};
```

### Build Command Best Practices

**MANDATORY**: Build commands MUST:

1. **Minify CSS** for production
2. **Include source maps** for development
3. **Verify output** exists and is not empty
4. **Fail on errors** (no silent failures)

**Example package.json**:
```json
{
  "scripts": {
    "build:css": "tailwindcss -i ./src/css/input.css -o ./src/css/output.css --minify",
    "build:css:dev": "tailwindcss -i ./src/css/input.css -o ./src/css/output.css",
    "build:css:watch": "tailwindcss -i ./src/css/input.css -o ./src/css/output.css --watch"
  }
}
```

---

## Nonce Configuration Best Practices

### When to Use Nonces

**Use nonces when**:
- ✅ Legitimate inline styles are absolutely necessary
- ✅ Third-party libraries require inline styles
- ✅ Dynamic styles must be generated server-side
- ✅ Security requirements mandate nonce-based CSP

**Avoid nonces when**:
- ❌ External CSS can be used instead
- ❌ Styles can be moved to external CSS files
- ❌ HTMX indicator styles (use external CSS)

### Nonce Implementation Pattern

**MANDATORY**: Nonce implementation MUST:

1. **Generate per request**: New nonce for each HTTP request
2. **Safely extract in template service**: Use `getattr(request.state, "csp_nonce", "")` to prevent AttributeError
3. **Add to template context**: Include nonce in template context as `csp_nonce` for safe access
4. **Include in CSP**: Add nonce to `style-src` and `script-src` directives
5. **Add to HTML**: Include `nonce` attribute in `<style>` and `<script>` tags using `{{ csp_nonce }}`
6. **Validate**: Verify nonce matches between CSP and HTML

**Example Implementation (Middleware)**:
```python
import secrets
from fastapi import Request

async def process_request(self, request: Request) -> None:
    """Generate CSP nonce for nonce-based CSP."""
    # Generate CSP nonce for nonce-based Content Security Policy
    # Nonce is a random value that changes per request, allowing inline scripts/styles
    # with matching nonce attribute while preventing XSS attacks
    nonce = secrets.token_urlsafe(16)
    if not hasattr(request.state, "csp_nonce"):
        request.state.csp_nonce = nonce
```

**Example Implementation (Template Service)**:
```python
# In UITemplateService._prepare_context() method
# CRITICAL: Safely extract CSP nonce to prevent AttributeError during template rendering
csp_nonce = ""
try:
    if hasattr(request, "state") and hasattr(request.state, "csp_nonce"):
        csp_nonce = getattr(request.state, "csp_nonce", "")
except (AttributeError, TypeError):
    # Nonce not available - use empty string (will be handled by CSP config)
    csp_nonce = ""

# Add nonce to template context
base_context = {
    "request": request,
    "csp_nonce": csp_nonce,  # Safe access in templates
    # ... other context variables ...
}
```

**Example Implementation (Template)**:
```html
<!-- In Jinja2 templates -->
<!-- CRITICAL CSP COMPLIANCE: Inline script requires nonce attribute -->
<!-- Nonce is generated per-request by SecurityHeadersMiddleware, safely extracted by UITemplateService, -->
<!-- and added to template context as 'csp_nonce' to prevent AttributeError -->
<script nonce="{{ csp_nonce }}">
  // HTMX Global Configuration
  if (typeof htmx !== 'undefined') {
    htmx.config.includeIndicatorStyles = false;
    // ... other HTMX config ...
  }
</script>

<!-- For inline styles (if absolutely necessary) -->
<style nonce="{{ csp_nonce }}">
  /* Legitimate inline styles */
</style>
```

**Example Implementation (CSP Header)**:
```python
# CSP header is built automatically by middleware
# The {nonce} placeholder in CSP config is replaced with actual nonce directive
csp_header = f"script-src 'self' 'nonce-{csp_nonce}' ...; style-src 'self' 'nonce-{csp_nonce}' ..."
```

### Nonce Security Considerations

**MANDATORY**: Nonce security MUST ensure:

1. **Cryptographic randomness**: Use `secrets` module (Python) or equivalent
2. **Sufficient length**: Minimum 16 bytes (128 bits)
3. **Single use**: Never reuse nonces across requests
4. **HTTPS only**: Nonces should only be used over HTTPS in production
5. **No exposure**: Never expose nonces in logs or error messages

---

## Docker Build Best Practices

### Multi-Stage Build Pattern

**MANDATORY**: Use multi-stage builds to:

1. **Separate build dependencies** from runtime
2. **Remove Node.js** from production image
3. **Minimize image size** and attack surface
4. **Improve security** by reducing dependencies

**Example Dockerfile Structure**:
```dockerfile
# Stage 1: Builder (includes Node.js for CSS build)
FROM python:3.12-slim AS builder

# Install Node.js for CSS build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Build CSS - copy package files, configs, and source files
WORKDIR /tmp/css-build
COPY package.json package-lock.json* ./
COPY tailwind.config.js postcss.config.js ./
COPY src/css/input.css ./src/css/

# Copy source files that CSS framework needs to scan
COPY src/ ./src/

# Install Node.js dependencies and build CSS
RUN --mount=type=cache,target=/root/.npm \
    npm ci --ignore-scripts && \
    npm run build:css

# Verify CSS was built
RUN test -f ./src/css/output.css || (echo "ERROR: CSS build failed!" && exit 1)

# Stage 2: Production (no Node.js)
FROM python:3.12-slim AS production

# ... Python dependencies, application code ...

# Copy built CSS from builder stage
COPY --from=builder /tmp/css-build/src/css/output.css ./src/css/output.css

# ... rest of production stage ...
```

### Docker Build Requirements Checklist

**MANDATORY**: Docker builds MUST:

- [ ] Install Node.js 18.x+ in builder stage
- [ ] Copy `package.json` and `package-lock.json`
- [ ] Copy CSS framework config files (`tailwind.config.js`, `postcss.config.js`)
- [ ] Copy CSS input file
- [ ] Copy source files for CSS framework scanning
- [ ] Install npm dependencies (including devDependencies)
- [ ] Run CSS build command (`npm run build:css`)
- [ ] Verify CSS file exists after build
- [ ] Copy built CSS to production stage
- [ ] Remove Node.js from production stage (multi-stage build)
- [ ] Use BuildKit cache mounts for npm packages
- [ ] Fail build if CSS compilation fails

### .dockerignore Best Practices

**MANDATORY**: Ensure `.dockerignore` does NOT exclude:

- ✅ `package.json`
- ✅ `package-lock.json`
- ✅ `tailwind.config.js` (or equivalent CSS framework config)
- ✅ `postcss.config.js` (or equivalent PostCSS config)
- ✅ CSS input files
- ✅ Source files needed for CSS framework scanning

**Example .dockerignore**:
```
# Node.js Artifacts
node_modules/
# CRITICAL: package.json, package-lock.json, and config files
# are REQUIRED for CSS build - DO NOT exclude them
# package.json
# package-lock.json
# tailwind.config.js
# postcss.config.js
.prettierrc.json
.eslintrc.json
```

---

## CI/CD Pipeline Best Practices

### Pipeline Stage Requirements

**MANDATORY**: CI/CD pipelines MUST include CSS build stage:

```yaml
# Example GitHub Actions
name: Build and Deploy

on:
  push:
    branches: [main, develop]

jobs:
  build-css:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build CSS
        run: npm run build:css

      - name: Verify CSS build
        run: |
          if [ ! -f "src/css/output.css" ]; then
            echo "ERROR: CSS build failed - output.css not found"
            exit 1
          fi
          if [ ! -s "src/css/output.css" ]; then
            echo "ERROR: CSS build failed - output.css is empty"
            exit 1
          fi

      - name: Upload CSS artifact
        uses: actions/upload-artifact@v3
        with:
          name: compiled-css
          path: src/css/output.css

  build-docker:
    needs: build-css
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/download-artifact@v3
        with:
          name: compiled-css

      - name: Build Docker image
        run: docker build -t app:latest .
```

### CI/CD Best Practices Checklist

**MANDATORY**: CI/CD pipelines MUST:

- [ ] Install Node.js 18.x+ in build environment
- [ ] Cache npm dependencies (BuildKit cache or CI cache)
- [ ] Install npm dependencies (`npm ci` preferred over `npm install`)
- [ ] Run CSS build command (`npm run build:css`)
- [ ] Verify CSS file exists and is not empty
- [ ] Fail pipeline if CSS build fails
- [ ] Store CSS artifact for Docker build (if separate stages)
- [ ] Include CSS in Docker build context
- [ ] Test CSP compliance in CI/CD (if possible)

---

## Development Workflow Best Practices

### Local Development Setup

**MANDATORY**: Developers MUST:

1. **Install Node.js**: Ensure Node.js 18.x+ is installed locally
2. **Install Dependencies**: Run `npm install` after cloning repository
3. **Build CSS**: Run `npm run build:css` before testing
4. **Use Watch Mode**: Use `npm run build:css:watch` during development

**Development Workflow**:
```bash
# Initial setup
npm install

# Build CSS for testing
npm run build:css

# Watch mode (auto-rebuild on changes)
npm run build:css:watch
```

### Pre-Commit Hooks

**RECOMMENDED**: Add pre-commit hook to build CSS:

```bash
#!/bin/sh
# .git/hooks/pre-commit

# Build CSS before commit
npm run build:css

# Verify CSS was built
if [ ! -f "src/css/output.css" ]; then
  echo "ERROR: CSS build failed - output.css not found"
  exit 1
fi

# Add CSS to commit if it changed
git add src/css/output.css
```

### Development Best Practices Checklist

**MANDATORY**: Developers MUST:

- [ ] Install Node.js 18.x+ locally
- [ ] Run `npm install` after cloning repository
- [ ] Build CSS before testing (`npm run build:css`)
- [ ] Use watch mode during development (`npm run build:css:watch`)
- [ ] Verify CSS changes are reflected in browser
- [ ] Test CSP compliance in development environment
- [ ] Document any changes to CSS framework config
- [ ] Commit CSS build artifacts (if not using Docker build)

---

## Troubleshooting Guide

### Issue: CSP Violations Still Occurring

**Symptoms**:
- Browser console shows CSP violation errors
- HTMX indicators not working

**Diagnosis Steps**:
1. Check if `htmx.config.includeIndicatorStyles = false` is set
2. Verify CSP config doesn't include `'unsafe-inline'`
3. Check browser DevTools → Network → Response Headers → `Content-Security-Policy`
4. Verify `tailwind.css` (or equivalent) is loaded
5. Check if HTMX classes are in compiled CSS

**Solution**:
- Ensure HTMX config disables inline styles in all templates
- Verify CSP config is correct (no `'unsafe-inline'`)
- Check that compiled CSS is loaded and contains HTMX styles
- Rebuild CSS if styles are missing

### Issue: HTMX Indicators Not Showing

**Symptoms**:
- HTMX requests work but no visual indicators
- Loading states not visible

**Diagnosis Steps**:
1. Check if compiled CSS is loaded (Network tab)
2. Verify HTMX classes are in compiled CSS (search for `.htmx-indicator`)
3. Check browser DevTools → Elements → Styles for HTMX classes
4. Verify HTMX is adding classes (`htmx-request`, `htmx-loading`, etc.)

**Solution**:
- Rebuild CSS: `npm run build:css`
- Verify CSS framework config includes HTMX utilities
- Check that HTMX is adding classes dynamically
- Verify CSS file path is correct in HTML

### Issue: CSS Build Fails in Docker

**Symptoms**:
- Docker build fails with npm/Tailwind errors
- CSS file not found after build

**Diagnosis Steps**:
1. Check Docker build logs for npm errors
2. Verify Node.js is installed in builder stage
3. Check if source files are copied correctly
4. Verify `package.json` and config files are not excluded in `.dockerignore`

**Solution**:
- Ensure Node.js installation step is present
- Verify `package.json` and CSS framework config files are copied
- Check that `src/` directory is copied for CSS framework scanning
- Verify npm cache mount is working (BuildKit required)
- Check `.dockerignore` doesn't exclude required files

### Issue: CSS Not Updated After Changes

**Symptoms**:
- Template changes don't reflect in CSS
- New CSS framework classes not working

**Diagnosis Steps**:
1. Check if CSS was rebuilt after template changes
2. Verify CSS framework content paths include changed files
3. Check if CSS file is cached in browser
4. Verify Docker build includes latest source files

**Solution**:
- Rebuild CSS: `npm run build:css`
- Clear browser cache or hard refresh (Ctrl+Shift+R)
- Verify CSS framework content paths in config file
- Check Docker build includes latest source files
- Use watch mode during development

---

## Security Audit Checklist

### CSP Configuration Audit

**MANDATORY**: Regularly audit CSP configuration:

- [ ] `style-src` does NOT include `'unsafe-inline'`
- [ ] `style-src` includes `'self'` for local CSS files
- [ ] `style-src` includes trusted CDNs explicitly (no wildcards)
- [ ] Nonces are used only when absolutely necessary
- [ ] Nonces are cryptographically random and unique per request
- [ ] CSP headers are set correctly in all environments
- [ ] CSP violations are logged and monitored

### HTMX Configuration Audit

**MANDATORY**: Regularly audit HTMX configuration:

- [ ] `htmx.config.includeIndicatorStyles = false` is set globally
- [ ] HTMX configuration is in base templates or global JS
- [ ] No duplicate HTMX configuration across files
- [ ] HTMX indicator classes are defined in CSS
- [ ] HTMX functionality works without CSP violations

### Build Process Audit

**MANDATORY**: Regularly audit build process:

- [ ] CSS is built during Docker/CI-CD builds (not at runtime)
- [ ] CSS build failures cause build to fail
- [ ] CSS file is verified to exist after build
- [ ] Node.js is removed from production images (multi-stage builds)
- [ ] Build dependencies are not included in production images

### Security Monitoring

**MANDATORY**: Monitor for security issues:

- [ ] CSP violation reports are collected and analyzed
- [ ] Browser console errors are monitored
- [ ] Security headers are verified in production
- [ ] Regular security scans are performed
- [ ] Dependencies are kept up to date

---

## Compliance Verification

### Verification Checklist

**MANDATORY**: Verify compliance before deployment:

- [ ] CSP configuration prohibits `'unsafe-inline'`
- [ ] HTMX is configured to disable inline styles
- [ ] CSS is built during Docker/CI-CD builds
- [ ] CSS file exists and is not empty
- [ ] HTMX indicators work without CSP violations
- [ ] Browser console shows no CSP violations
- [ ] Security headers are set correctly
- [ ] Build process includes CSS compilation
- [ ] Production image does not include Node.js
- [ ] Documentation is up to date

### Automated Verification

**RECOMMENDED**: Implement automated verification:

```bash
#!/bin/bash
# verify-csp-compliance.sh

# Check CSP config doesn't include 'unsafe-inline'
if grep -q "unsafe-inline" config/security/csp/*.yaml; then
  echo "ERROR: CSP config includes 'unsafe-inline'"
  exit 1
fi

# Check HTMX config disables inline styles
if ! grep -q "includeIndicatorStyles = false" src/templates/**/*.html; then
  echo "WARNING: HTMX config may not disable inline styles"
fi

# Check CSS file exists
if [ ! -f "src/css/output.css" ]; then
  echo "ERROR: CSS file not found"
  exit 1
fi

# Check CSS file is not empty
if [ ! -s "src/css/output.css" ]; then
  echo "ERROR: CSS file is empty"
  exit 1
fi

echo "✅ CSP compliance verification passed"
```

### Manual Verification Steps

**MANDATORY**: Perform manual verification:

1. **Browser DevTools**:
   - Open browser DevTools → Console
   - Check for CSP violation errors
   - Verify `Content-Security-Policy` header in Network tab

2. **HTMX Functionality**:
   - Test HTMX requests (forms, links, etc.)
   - Verify loading indicators appear
   - Check that animations work correctly

3. **CSS Loading**:
   - Verify CSS file is loaded (Network tab)
   - Check CSS file contains HTMX classes
   - Verify styles are applied correctly

---

## Related Documentation

- [OWASP Content Security Policy Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html)
- [HTMX Documentation](https://htmx.org/docs/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [PostCSS Documentation](https://postcss.org/docs/)

---

## Version History

- **v1.0.0** (2025-12-23): Initial best practices document
  - CSP configuration without `'unsafe-inline'`
  - HTMX inline styles disabled
  - CSS framework integration
  - Docker build process requirements
  - CI/CD pipeline requirements
  - Nonce configuration best practices
  - Security audit checklist
  - Compliance verification guide

---

## Conclusion

These best practices ensure HTMX works seamlessly with strict CSP while maintaining security best practices. By following these guidelines, you achieve:

- ✅ **Strict CSP Compliance**: No `'unsafe-inline'` required
- ✅ **Full HTMX Functionality**: All indicators and animations work
- ✅ **Maintainable**: Styles defined in CSS framework config
- ✅ **Secure**: Prevents XSS attacks via style injection
- ✅ **Build-Time Compilation**: CSS built during Docker/CI-CD builds
- ✅ **Production-Ready**: Follows security best practices

The solution is production-ready, maintainable, and follows security best practices recommended by OWASP and other security organizations.
