# Python Code Quality & Auto-Remediation Cheat Sheet Template

**Version**: v1.0.0
**Date**: 2025-12-24

## 📌 Configuration Variables

Replace these placeholders with your project-specific values:

- `{{PROJECT_PATH}}` - Your project source code path (e.g., `src/`, `lib/`, `app/`)
- `{{TEST_PATH}}` - Your test directory path (e.g., `tests/`, `test/`, `tests/unit/`)
- `{{PYTHON_VERSION}}` - Your Python version (e.g., `3.12`, `3.11`, `3.10`)
- `{{LINE_LENGTH}}` - Maximum line length (e.g., `120`, `100`, `88`)
- `{{MAX_COMPLEXITY}}` - Maximum cyclomatic complexity (e.g., `15`, `10`)
- `{{COVERAGE_THRESHOLD}}` - Minimum test coverage percentage (e.g., `85`, `90`, `95`)

**Example**: If your project path is `src/`, tests are in `tests/`, Python 3.12, line length 120, complexity 15, coverage 85%, replace:

- `{{PROJECT_PATH}}` → `src/`
- `{{TEST_PATH}}` → `tests/`
- `{{PYTHON_VERSION}}` → `3.12`
- `{{LINE_LENGTH}}` → `120`
- `{{MAX_COMPLEXITY}}` → `15`
- `{{COVERAGE_THRESHOLD}}` → `85`

---

## ✅ SYNTAX VALIDATION

### Check Syntax (No Auto-Fix)

```bash
# Compile Python files to check syntax
python -m py_compile {{PROJECT_PATH}}**/*.py

# Compile all Python files recursively
python -m compileall {{PROJECT_PATH}}

# Compile with verbose output
python -m compileall -v {{PROJECT_PATH}}

# Compile specific file
python -m py_compile {{PROJECT_PATH}}/module/file.py
```

**Requirement**: 0 syntax errors
**Purpose**: Verify Python syntax is valid before other checks

---

## 🔍 TYPE CHECKING

### MyPy Type Checking

```bash
# Type check with strict mode
mypy {{PROJECT_PATH}} --strict

# Type check with ignore missing imports
mypy {{PROJECT_PATH}} --strict --ignore-missing-imports

# Type check specific module
mypy {{PROJECT_PATH}}/module/ --strict

# Type check with show error codes
mypy {{PROJECT_PATH}} --strict --show-error-codes

# Type check with error summary
mypy {{PROJECT_PATH}} --strict --show-error-summary

# Type check specific Python version
mypy {{PROJECT_PATH}} --python-version {{PYTHON_VERSION}} --strict

# Type check with config file
mypy {{PROJECT_PATH}} --config-file pyproject.toml
```

### Auto-Fix Type Issues

```bash
# Note: MyPy does not auto-fix, but you can use type stubs
# Install type stubs for missing types
pip install types-requests types-PyYAML

# Use mypy --strict to identify all type issues
# Then manually fix based on error messages
```

**Requirement**: 0 type errors, 0 warnings
**Coverage**: 100% type coverage recommended

---

## 🧹 LINTING

### Ruff (Fast, Modern Linter)

```bash
# Check for linting issues
ruff check {{PROJECT_PATH}}

# Check with specific rule sets
ruff check {{PROJECT_PATH}} --select E,F,W

# Check with line length limit
ruff check {{PROJECT_PATH}} --line-length {{LINE_LENGTH}}

# Check with complexity limit
ruff check {{PROJECT_PATH}} --max-complexity {{MAX_COMPLEXITY}}

# Auto-fix linting issues
ruff check {{PROJECT_PATH}} --fix

# Auto-fix with unsafe fixes
ruff check {{PROJECT_PATH}} --fix --unsafe-fixes

# Show all available rules
ruff rule --all

# Check specific file
ruff check {{PROJECT_PATH}}/module/file.py
```

### Flake8 (Traditional Linter)

```bash
# Full linting check
flake8 {{PROJECT_PATH}} --max-line-length={{LINE_LENGTH}} --max-complexity={{MAX_COMPLEXITY}}

# Critical errors only
flake8 {{PROJECT_PATH}} --select=E,F,W --max-line-length={{LINE_LENGTH}}

# Show statistics
flake8 {{PROJECT_PATH}} --statistics

# Count errors
flake8 {{PROJECT_PATH}} --count

# Check specific file
flake8 {{PROJECT_PATH}}/module/file.py
```

**Note**: Flake8 does not auto-fix. Use `ruff --fix` or `autopep8` for auto-fixing.

### Auto-Fix Linting Issues

```bash
# Using Ruff (recommended - fastest)
ruff check {{PROJECT_PATH}} --fix

# Using autopep8 (for flake8 compatibility)
autopep8 --in-place --aggressive --aggressive {{PROJECT_PATH}}/**/*.py

# Using autopep8 with max line length
autopep8 --in-place --max-line-length {{LINE_LENGTH}} {{PROJECT_PATH}}/**/*.py
```

**Requirement**: 0 errors, 0 warnings (per policy)

---

## 🎨 CODE FORMATTING

### Black (Code Formatter)

```bash
# Check formatting (no changes)
black {{PROJECT_PATH}} --check --line-length={{LINE_LENGTH}}

# Check formatting with diff
black {{PROJECT_PATH}} --check --diff --line-length={{LINE_LENGTH}}

# Auto-fix formatting
black {{PROJECT_PATH}} --line-length={{LINE_LENGTH}}

# Format specific file
black {{PROJECT_PATH}}/module/file.py --line-length={{LINE_LENGTH}}

# Format with string normalization
black {{PROJECT_PATH}} --line-length={{LINE_LENGTH}} --skip-string-normalization

# Format with target Python version
black {{PROJECT_PATH}} --line-length={{LINE_LENGTH}} --target-version py{{PYTHON_VERSION}}
```

**Requirement**: All files correctly formatted
**Auto-fix**: Yes (removes `--check` flag)

---

## 📦 IMPORT SORTING

### isort (Import Organizer)

```bash
# Check import sorting (no changes)
isort {{PROJECT_PATH}} --check-only

# Check with Black profile
isort {{PROJECT_PATH}} --profile black --check-only

# Check with diff output
isort {{PROJECT_PATH}} --check-only --diff

# Auto-fix import sorting
isort {{PROJECT_PATH}}

# Auto-fix with Black profile
isort {{PROJECT_PATH}} --profile black

# Auto-fix with line length
isort {{PROJECT_PATH}} --profile black --line-length={{LINE_LENGTH}}

# Auto-fix specific file
isort {{PROJECT_PATH}}/module/file.py --profile black
```

**Requirement**: All imports correctly sorted
**Auto-fix**: Yes (removes `--check-only` flag)

---

## 🔒 SECURITY ANALYSIS

### Bandit (Security Linter)

```bash
# Security scan (low confidence)
bandit -r {{PROJECT_PATH}} -ll

# Security scan (medium confidence)
bandit -r {{PROJECT_PATH}} -l

# Security scan (high confidence)
bandit -r {{PROJECT_PATH}}

# Security scan with JSON output
bandit -r {{PROJECT_PATH}} -f json -o bandit-report.json

# Security scan excluding tests
bandit -r {{PROJECT_PATH}} --exclude {{TEST_PATH}}

# Security scan specific severity
bandit -r {{PROJECT_PATH}} -ll --severity-level high

# Security scan with config file
bandit -r {{PROJECT_PATH}} -c bandit.yaml
```

**Requirement**: 0 HIGH/MEDIUM security issues

### Safety (Dependency Vulnerability Check)

```bash
# Check dependencies for vulnerabilities
safety check

# Check specific requirements file
safety check --file requirements.txt

# Check with full report
safety check --full-report

# Check with JSON output
safety check --json

# Check and update database
safety check --update
```

**Requirement**: 0 HIGH/CRITICAL vulnerabilities

---

## 📊 COMPLEXITY ANALYSIS

### Radon (Complexity Metrics)

```bash
# Cyclomatic complexity analysis
radon cc {{PROJECT_PATH}} -a -nb

# Cyclomatic complexity with grades
radon cc {{PROJECT_PATH}} -a

# Maintainability index
radon mi {{PROJECT_PATH}} -nb

# Maintainability index with grades
radon mi {{PROJECT_PATH}}

# Raw metrics
radon raw {{PROJECT_PATH}}

# Halstead metrics
radon hal {{PROJECT_PATH}}
```

**Requirement**: Average complexity ≤ {{MAX_COMPLEXITY}}, Grade A or B maintainability

### Xenon (Complexity Monitor)

```bash
# Check complexity thresholds
xenon {{PROJECT_PATH}} --max-absolute B --max-modules A --max-average A

# Check with specific thresholds
xenon {{PROJECT_PATH}} --max-absolute {{MAX_COMPLEXITY}} --max-modules A --max-average A

# Show complexity report
xenon {{PROJECT_PATH}} --max-absolute B --max-modules A --max-average A --show
```

**Requirement**: 0 complexity violations

---

## 🧪 TESTING

### Pytest

```bash
# Run all tests
pytest {{TEST_PATH}}

# Run tests with verbose output
pytest {{TEST_PATH}} -v

# Run specific test file
pytest {{TEST_PATH}}/test_module.py

# Run specific test function
pytest {{TEST_PATH}}/test_module.py::test_function

# Run tests with coverage
pytest {{TEST_PATH}} --cov={{PROJECT_PATH}} --cov-report=term-missing

# Run tests with HTML coverage report
pytest {{TEST_PATH}} --cov={{PROJECT_PATH}} --cov-report=html

# Run tests with coverage threshold
pytest {{TEST_PATH}} --cov={{PROJECT_PATH}} --cov-report=term-missing --cov-fail-under={{COVERAGE_THRESHOLD}}

# Run tests in parallel
pytest {{TEST_PATH}} -n auto

# Run tests with markers
pytest {{TEST_PATH}} -m "not slow"

# Run tests with output capture
pytest {{TEST_PATH}} -s

# Run tests and stop on first failure
pytest {{TEST_PATH}} -x
```

**Requirement**: All tests pass, coverage ≥ {{COVERAGE_THRESHOLD}}%

---

## 🔄 AUTO-REMEDIATION WORKFLOW

### Complete Auto-Fix Sequence

```bash
# Step 1: Format code with Black
black {{PROJECT_PATH}} --line-length={{LINE_LENGTH}}

# Step 2: Sort imports with isort
isort {{PROJECT_PATH}} --profile black --line-length={{LINE_LENGTH}}

# Step 3: Fix linting issues with Ruff
ruff check {{PROJECT_PATH}} --fix

# Step 4: Verify syntax
python -m compileall {{PROJECT_PATH}}

# Step 5: Run type checking
mypy {{PROJECT_PATH}} --strict --ignore-missing-imports

# Step 6: Run security scan
bandit -r {{PROJECT_PATH}} -ll

# Step 7: Run tests
pytest {{TEST_PATH}} --cov={{PROJECT_PATH}} --cov-report=term-missing
```

### Quick Auto-Fix (Formatting + Linting)

```bash
# Format and fix in one go
black {{PROJECT_PATH}} --line-length={{LINE_LENGTH}} && \
isort {{PROJECT_PATH}} --profile black --line-length={{LINE_LENGTH}} && \
ruff check {{PROJECT_PATH}} --fix
```

---

## 📋 VALIDATION PIPELINE

### Complete Validation Sequence

```bash
# 1. Syntax Validation
python -m py_compile {{PROJECT_PATH}}**/*.py

# 2. Type Checking
mypy {{PROJECT_PATH}} --strict --ignore-missing-imports

# 3. Formatting Check
black {{PROJECT_PATH}} --check --line-length={{LINE_LENGTH}}

# 4. Import Sorting Check
isort {{PROJECT_PATH}} --profile black --check-only --line-length={{LINE_LENGTH}}

# 5. Linting Check
ruff check {{PROJECT_PATH}} --line-length={{LINE_LENGTH}}

# 6. Security Scan
bandit -r {{PROJECT_PATH}} -ll

# 7. Dependency Security
safety check

# 8. Complexity Check
xenon {{PROJECT_PATH}} --max-absolute B --max-modules A --max-average A

# 9. Test Execution
pytest {{TEST_PATH}} --cov={{PROJECT_PATH}} --cov-report=term-missing --cov-fail-under={{COVERAGE_THRESHOLD}}
```

**Requirement**: All checks must pass with 0 errors, 0 warnings

---

## 🎯 QUICK REFERENCE

### Most Common Commands

```bash
# Format code
black {{PROJECT_PATH}} --line-length={{LINE_LENGTH}}

# Sort imports
isort {{PROJECT_PATH}} --profile black --line-length={{LINE_LENGTH}}

# Fix linting
ruff check {{PROJECT_PATH}} --fix

# Type check
mypy {{PROJECT_PATH}} --strict --ignore-missing-imports

# Security scan
bandit -r {{PROJECT_PATH}} -ll

# Run tests
pytest {{TEST_PATH}} --cov={{PROJECT_PATH}} --cov-report=term-missing

# Complete validation
python -m py_compile {{PROJECT_PATH}}**/*.py && \
mypy {{PROJECT_PATH}} --strict --ignore-missing-imports && \
black {{PROJECT_PATH}} --check --line-length={{LINE_LENGTH}} && \
isort {{PROJECT_PATH}} --profile black --check-only --line-length={{LINE_LENGTH}} && \
ruff check {{PROJECT_PATH}} --line-length={{LINE_LENGTH}} && \
bandit -r {{PROJECT_PATH}} -ll && \
pytest {{TEST_PATH}} --cov={{PROJECT_PATH}} --cov-report=term-missing
```

### Recommended Auto-Remediation Command

```bash
# Auto-fix formatting, imports, and linting (best for quick fixes)
black {{PROJECT_PATH}} --line-length={{LINE_LENGTH}} && \
isort {{PROJECT_PATH}} --profile black --line-length={{LINE_LENGTH}} && \
ruff check {{PROJECT_PATH}} --fix
```

---

## 🔧 INSTALLATION

### Install Required Tools

```bash
# Install all quality tools
pip install black isort ruff mypy bandit safety pytest pytest-cov radon xenon

# Or install from requirements file
pip install -r requirements-dev.txt

# Install with specific versions
pip install black==23.12.0 isort==5.13.0 ruff==0.1.0 mypy==1.7.0 bandit==1.7.5
```

---

## 📝 USAGE INSTRUCTIONS

1. **Copy this template** to your project directory
2. **Replace all placeholders** with your project-specific values:
   - `{{PROJECT_PATH}}` → Your source code path (e.g., `src/`, `lib/`)
   - `{{TEST_PATH}}` → Your test directory (e.g., `tests/`, `test/`)
   - `{{PYTHON_VERSION}}` → Your Python version (e.g., `3.12`, `3.11`)
   - `{{LINE_LENGTH}}` → Maximum line length (e.g., `120`, `100`)
   - `{{MAX_COMPLEXITY}}` → Maximum complexity (e.g., `15`, `10`)
   - `{{COVERAGE_THRESHOLD}}` → Minimum coverage (e.g., `85`, `90`)

3. **Use find-and-replace** in your editor:
   - Find: `{{PROJECT_PATH}}` → Replace: `src/`
   - Find: `{{TEST_PATH}}` → Replace: `tests/`
   - Find: `{{PYTHON_VERSION}}` → Replace: `3.12`
   - Find: `{{LINE_LENGTH}}` → Replace: `120`
   - Find: `{{MAX_COMPLEXITY}}` → Replace: `15`
   - Find: `{{COVERAGE_THRESHOLD}}` → Replace: `85`

### Example Project Values

**For a FastAPI project:**
- `{{PROJECT_PATH}}` → `src/`
- `{{TEST_PATH}}` → `tests/`
- `{{PYTHON_VERSION}}` → `3.12`
- `{{LINE_LENGTH}}` → `120`
- `{{MAX_COMPLEXITY}}` → `15`
- `{{COVERAGE_THRESHOLD}}` → `85`

**For a Django project:**
- `{{PROJECT_PATH}}` → `app/`
- `{{TEST_PATH}}` → `tests/`
- `{{PYTHON_VERSION}}` → `3.11`
- `{{LINE_LENGTH}}` → `100`
- `{{MAX_COMPLEXITY}}` → `10`
- `{{COVERAGE_THRESHOLD}}` → `90`

---

## 🚨 COMMON ISSUES & SOLUTIONS

### Issue: Import sorting conflicts with Black

**Solution**: Use `isort --profile black` to ensure compatibility

```bash
isort {{PROJECT_PATH}} --profile black --line-length={{LINE_LENGTH}}
```

### Issue: Type checking fails on third-party imports

**Solution**: Use `--ignore-missing-imports` flag

```bash
mypy {{PROJECT_PATH}} --strict --ignore-missing-imports
```

### Issue: Ruff and Flake8 give different results

**Solution**: Use Ruff as primary linter (faster, more modern). Flake8 for compatibility checks only.

### Issue: Coverage threshold not met

**Solution**: Run coverage report to identify uncovered lines

```bash
pytest {{TEST_PATH}} --cov={{PROJECT_PATH}} --cov-report=term-missing --cov-fail-under={{COVERAGE_THRESHOLD}}
```

---

**Last Updated**: 2025-12-24
