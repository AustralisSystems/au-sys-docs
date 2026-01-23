# Code Quality & Linting Best Practices

**Version**: v1.0.0  
**Last Updated**: 2025-01-14

This document provides comprehensive best practices for implementing code quality and linting in FastAPI applications, covering black formatting, isort import sorting, mypy type checking, flake8 linting, bandit security analysis, pre-commit hooks, CI/CD integration, and production deployment.

---

## Table of Contents

1. [Architecture Principles](#architecture-principles)
2. [Code Formatting (Black)](#code-formatting-black)
3. [Import Sorting (isort)](#import-sorting-isort)
4. [Type Checking (mypy)](#type-checking-mypy)
5. [Linting (flake8)](#linting-flake8)
6. [Security Analysis (Bandit)](#security-analysis-bandit)
7. [Pre-commit Hooks](#pre-commit-hooks)
8. [CI/CD Integration](#cicd-integration)
9. [Production Deployment](#production-deployment)

---

## Architecture Principles

### Code Quality Philosophy

**REQUIRED**: Understand code quality principles:

1. **Consistency**: Consistent code style across codebase
2. **Type Safety**: Type hints for all functions
3. **Security**: Security analysis for vulnerabilities
4. **Automation**: Automated quality checks
5. **Early Detection**: Catch issues before commit
6. **Documentation**: Self-documenting code

---

## Code Formatting (Black)

### Black Configuration

**REQUIRED**: Black setup:

```toml
# pyproject.toml
[tool.black]
line-length = 88
target-version = ['py311']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | venv
  | _build
  | buck-out
  | build
  | dist
)/
'''
```

### Black Usage

**REQUIRED**: Black commands:

```bash
# Format all files
black .

# Check formatting (CI)
black --check .

# Format specific file
black app/main.py
```

---

## Import Sorting (isort)

### isort Configuration

**REQUIRED**: isort setup:

```toml
# pyproject.toml
[tool.isort]
profile = "black"
line_length = 88
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true
skip_glob = ["*/migrations/*"]
known_first_party = ["app", "core", "shared_components"]
```

### isort Usage

**REQUIRED**: isort commands:

```bash
# Sort imports
isort .

# Check sorting (CI)
isort --check-only .

# Sort specific file
isort app/main.py
```

---

## Type Checking (mypy)

### mypy Configuration

**REQUIRED**: mypy setup:

```ini
# mypy.ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_incomplete_defs = True
check_untyped_defs = True
disallow_untyped_decorators = True
no_implicit_optional = True
warn_redundant_casts = True
warn_unused_ignores = True
warn_no_return = True
strict_equality = True

[mypy-fastapi.*]
ignore_missing_imports = True

[mypy-pydantic.*]
ignore_missing_imports = True
```

### mypy Usage

**REQUIRED**: mypy commands:

```bash
# Type check
mypy .

# Type check specific module
mypy app/

# Strict mode
mypy --strict .
```

---

## Linting (flake8)

### flake8 Configuration

**REQUIRED**: flake8 setup:

```ini
# .flake8
[flake8]
max-line-length = 88
extend-ignore = E203, E266, E501, W503
exclude =
    .git,
    __pycache__,
    .venv,
    venv,
    .mypy_cache,
    .pytest_cache,
    migrations,
    alembic
max-complexity = 10
```

### flake8 Usage

**REQUIRED**: flake8 commands:

```bash
# Lint code
flake8 .

# Lint specific file
flake8 app/main.py
```

---

## Security Analysis (Bandit)

### Bandit Configuration

**REQUIRED**: Bandit setup:

```ini
# .bandit
[bandit]
exclude_dirs = tests,test,venv,.venv
skips = B101,B601
```

### Bandit Usage

**REQUIRED**: Bandit commands:

```bash
# Security scan
bandit -r .

# Generate report
bandit -r . -f json -o bandit-report.json
```

---

## Pre-commit Hooks

### Pre-commit Configuration

**REQUIRED**: Pre-commit setup:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]

  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.6
    hooks:
      - id: bandit
        args: ["-r", ".", "-f", "json"]
```

### Pre-commit Usage

**REQUIRED**: Pre-commit commands:

```bash
# Install hooks
pre-commit install

# Run on all files
pre-commit run --all-files

# Run on staged files (automatic)
git commit -m "message"
```

---

## CI/CD Integration

### GitHub Actions Workflow

**REQUIRED**: CI/CD integration:

```yaml
# .github/workflows/quality.yml
name: Code Quality

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install black isort mypy flake8 bandit
      
      - name: Run Black
        run: black --check .
      
      - name: Run isort
        run: isort --check-only .
      
      - name: Run mypy
        run: mypy .
      
      - name: Run flake8
        run: flake8 .
      
      - name: Run Bandit
        run: bandit -r .
```

---

## Production Deployment

### Quality Gates

**REQUIRED**: Production quality gates:

```python
# scripts/quality_check.py
import subprocess
import sys

def run_quality_checks():
    """Run all quality checks."""
    checks = [
        ("black", ["black", "--check", "."]),
        ("isort", ["isort", "--check-only", "."]),
        ("mypy", ["mypy", "."]),
        ("flake8", ["flake8", "."]),
        ("bandit", ["bandit", "-r", "."]),
    ]
    
    failed = []
    
    for name, cmd in checks:
        print(f"Running {name}...")
        result = subprocess.run(cmd, capture_output=True)
        
        if result.returncode != 0:
            print(f"❌ {name} failed")
            failed.append(name)
        else:
            print(f"✅ {name} passed")
    
    if failed:
        print(f"\nFailed checks: {', '.join(failed)}")
        sys.exit(1)
    
    print("\n✅ All quality checks passed!")

if __name__ == "__main__":
    run_quality_checks()
```

---

## Summary

### Key Takeaways

1. **Black**: Consistent code formatting
2. **isort**: Organized imports
3. **mypy**: Type safety
4. **flake8**: Code quality
5. **Bandit**: Security analysis
6. **Pre-commit**: Catch issues early
7. **CI/CD**: Automated quality gates
8. **Production Ready**: 0 errors required

---

**Version**: v1.0.0  
**Last Updated**: 2025-01-14

