---
title: "Logging Mandate - Enterprise Logging Standards"
version: "1.0.0"
type: "mandate"
status: "active"
created: "2025-12-08"
language: "en-AU"
---

# Logging Mandate - Enterprise Logging Standards

**Version**: v1.0.0  
**Last Updated**: 2025-12-08  
**Status**: Active  
**Classification**: Enterprise Canonical Standard

---

## Purpose

This mandate defines the **ABSOLUTE REQUIREMENTS** for all logging within the codebase. Compliance with this mandate is **MANDATORY** and **NON-NEGOTIABLE**. All code must adhere to these standards to ensure:

- Enterprise-grade logging consistency
- Cybersecurity audit compliance
- Effective troubleshooting and debugging
- Integration with log aggregation systems (ELK, Splunk, etc.)
- Compliance with syslog standards (RFC 3164/RFC 5424)

---

## Core Principle

**THE LOGGER FACTORY IS THE ONLY AUTHORIZED LOGGING MECHANISM**

All logging MUST use `src/services/logging/logger_factory.py`. No exceptions.

---

## Logger Factory Output Format Requirements

### 1. Console Output (stdout/stderr)

**Format**: Structured JSON (via `get_json_formatter`)  
**Purpose**: Machine-readable logs for log aggregation systems  
**Compliance**: Required for all console output

**Example Output**:
```json
{
  "@timestamp": "2025-12-08T00:30:58.532265+00:00",
  "level": "INFO",
  "logger": "module.name",
  "message": "Operation completed",
  "service": "rest_api_orchestrator",
  "environment": "production",
  "host": "hostname",
  "version": "1.0.0"
}
```

**Requirements**:
- ✅ All console output MUST be JSON formatted
- ✅ All console output MUST use logger factory
- ✅ NO plain text operational messages in console
- ✅ NO `print()` statements for operational logging

### 2. File Output (log files)

**Format**: Detailed text format (via `formatter_config.detailed`)  
**Purpose**: Human-readable logs for troubleshooting and analysis  
**Compliance**: Required for all file-based logging

**Example Output**:
```
2025-12-08 00:30:58 | module.name                    | INFO     | function_name          :1234 | Operation completed
```

**Requirements**:
- ✅ All file output MUST use detailed text format
- ✅ All file output MUST use logger factory
- ✅ Format: `%(asctime)s | %(name)-30s | %(levelname)-8s | %(funcName)-20s:%(lineno)-4d | %(message)s`

### 3. Syslog Output (if enabled)

**Format**: Structured JSON (via `formatter_config.json`)  
**Purpose**: RFC 3164/RFC 5424 compliant syslog messages for centralized logging  
**Compliance**: Required when syslog is enabled

**Requirements**:
- ✅ All syslog output MUST be JSON formatted
- ✅ All syslog output MUST comply with RFC 3164/RFC 5424
- ✅ All syslog output MUST use logger factory

---

## Mandatory Logger Factory Usage

### Standard Logger

**Use Case**: General purpose logging for modules  
**Function**: `get_logger(name, component=None)`

**Required Pattern**:
```python
from src.services.logging.logger_factory import get_logger

logger = get_logger(__name__)
logger.info("Operation completed")
logger.error("Operation failed", extra={"error_code": "ERR001"})
```

**When to Use**:
- Module-level logging
- General operational messages
- Error logging
- Information logging

### Component Logger

**Use Case**: Component-specific logging with hierarchical naming  
**Function**: `get_component_logger(component, subcomponent=None)`

**Required Pattern**:
```python
from src.services.logging.logger_factory import get_component_logger

logger = get_component_logger("component_name", "subcomponent_name")
logger.info("Component operation completed")
```

**When to Use**:
- Component-specific logging
- Hierarchical logger naming
- Component-level configuration
- Audit logging (see Audit Logging section)

### Debug Logger

**Use Case**: Detailed troubleshooting and development logging  
**Function**: `create_debug_logger(name)`

**Required Pattern**:
```python
from src.services.logging.logger_factory import create_debug_logger

debug_logger = create_debug_logger(__name__)
debug_logger.debug("Detailed execution flow", extra={"variable": value})
```

**When to Use**:
- Detailed execution flow logging
- Variable state logging
- Decision point logging
- Performance metrics logging
- Development troubleshooting

---

## Prohibited Patterns

### ABSOLUTELY FORBIDDEN

The following patterns are **STRICTLY PROHIBITED** and **MUST NOT** be used:

#### ❌ Direct `logging.getLogger()` Usage
```python
# FORBIDDEN
import logging
logger = logging.getLogger(__name__)

# REQUIRED
from src.services.logging.logger_factory import get_logger
logger = get_logger(__name__)
```

#### ❌ `logging.basicConfig()` Usage
```python
# FORBIDDEN
import logging
logging.basicConfig(level=logging.INFO)

# REQUIRED
# Use logger factory - configuration is handled centrally
```

#### ❌ `print()` Statements for Operational Logging
```python
# FORBIDDEN
print("Operation completed")

# REQUIRED
from src.services.logging.logger_factory import get_logger
logger = get_logger(__name__)
logger.info("Operation completed")
```

**Exception**: Test scripts may use `print()` for test output formatting, but operational logs MUST use logger factory.

#### ❌ Direct `logging.*` Method Calls
```python
# FORBIDDEN
import logging
logging.info("Message")
logging.error("Error")

# REQUIRED
from src.services.logging.logger_factory import get_logger
logger = get_logger(__name__)
logger.info("Message")
logger.error("Error")
```

#### ❌ Custom Logger Creation Outside Factory
```python
# FORBIDDEN
import logging
custom_logger = logging.getLogger("custom")
custom_handler = logging.StreamHandler()
custom_logger.addHandler(custom_handler)

# REQUIRED
# Use logger factory - all handlers are managed centrally
```

---

## Audit-Level Logging Requirements

### Purpose

Audit logging is **MANDATORY** for cybersecurity compliance and regulatory requirements. All security-related events MUST be logged with audit-level logging.

### When Audit Logging is Required

**MANDATORY** for:
- ✅ User authentication events (success/failure)
- ✅ User authorization events (access granted/denied)
- ✅ Data access events (read/write/delete)
- ✅ Security policy violations
- ✅ Compliance events
- ✅ Sensitive data operations
- ✅ Configuration changes
- ✅ System access events

### Implementation Pattern

**Required Pattern**:
```python
from src.services.logging.logger_factory import get_component_logger

# For security events
audit_logger = get_component_logger("audit", "security")
audit_logger.info(
    "User authentication successful",
    extra={
        "user_id": user_id,
        "ip_address": ip_address,
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": "authentication",
        "result": "success"
    }
)

# For compliance events
compliance_logger = get_component_logger("audit", "compliance")
compliance_logger.info(
    "Data access logged",
    extra={
        "user_id": user_id,
        "resource": resource_id,
        "action": "read",
        "timestamp": datetime.utcnow().isoformat()
    }
)
```

### Audit Logging Requirements

- ✅ **Level**: INFO or higher (never DEBUG)
- ✅ **Component**: Use `get_component_logger("audit", "security")` or `get_component_logger("audit", "compliance")`
- ✅ **Extra Fields**: MUST include contextual information (user_id, ip_address, timestamp, event_type, result)
- ✅ **Persistence**: Audit logs MUST be persisted to files (not just console)
- ✅ **Retention**: Audit logs MUST be retained per compliance requirements

### Modules Requiring Audit Logging

**MANDATORY** audit logging in:
- `src/services/auth/*` - All authentication/authorization modules
- `src/services/security/*` - All security modules
- `src/services/fastapi_services_platform/engine/security/*` - Platform security modules
- `src/routers/*` - API access logging
- `src/services/data/*` - Data access logging

---

## Debug-Level Logging Requirements

### Purpose

Debug logging is **MANDATORY** for effective troubleshooting and development. All service modules MUST have debug logging capability.

### When Debug Logging is Required

**MANDATORY** for:
- ✅ Detailed execution flow
- ✅ Variable states at critical points
- ✅ Decision point logging
- ✅ Performance metrics
- ✅ Error context and stack traces
- ✅ Request/response flows
- ✅ State transitions
- ✅ Integration points

### Implementation Pattern

**Required Pattern**:
```python
from src.services.logging.logger_factory import create_debug_logger

debug_logger = create_debug_logger(__name__)

# Detailed execution flow
debug_logger.debug(
    "Processing request",
    extra={
        "request_id": request_id,
        "method": method,
        "path": path,
        "params": params
    }
)

# Variable state logging
debug_logger.debug(
    "Variable state",
    extra={
        "variable_name": variable_name,
        "value": value,
        "type": type(value).__name__
    }
)

# Performance metrics
debug_logger.debug(
    "Operation performance",
    extra={
        "operation": operation_name,
        "duration_ms": duration_ms,
        "memory_usage": memory_usage
    }
)
```

### Debug Logging Requirements

- ✅ **Level**: DEBUG
- ✅ **Logger**: Use `create_debug_logger(__name__)` or standard logger with DEBUG level enabled
- ✅ **Extra Fields**: Include contextual information for troubleshooting
- ✅ **Performance**: Debug logging MUST NOT impact production performance (use appropriate log levels)

### Modules Requiring Debug Logging

**MANDATORY** debug logging in:
- All service modules (`src/services/*`)
- All API routers (`src/routers/*`)
- All core components (`src/services/core/*`)
- All integration modules (`src/services/integration/*`)

---

## Log Levels

### Standard Log Levels

The following log levels MUST be used appropriately:

#### CRITICAL
- **Use**: System-wide critical failures
- **Example**: Application cannot start, database connection lost permanently

#### ERROR
- **Use**: Errors that require attention but don't stop execution
- **Example**: API request failed, file operation failed

#### WARNING
- **Use**: Potential issues that don't prevent operation
- **Example**: Deprecated API usage, performance degradation

#### INFO
- **Use**: General operational information
- **Example**: Service started, operation completed, configuration loaded

#### DEBUG
- **Use**: Detailed troubleshooting information
- **Example**: Variable states, execution flow, performance metrics

### Audit Log Levels

Audit logging MUST use:
- **INFO**: Normal audit events (authentication, authorization, data access)
- **WARNING**: Security policy violations, suspicious activity
- **ERROR**: Security failures, compliance violations

**NEVER** use DEBUG level for audit logging.

---

## Structured Logging with Extra Fields

### Purpose

Structured logging with extra fields enables:
- Machine-readable log analysis
- Log aggregation and filtering
- Contextual information preservation
- Correlation across services

### Required Pattern

```python
from src.services.logging.logger_factory import get_logger

logger = get_logger(__name__)

# With extra fields
logger.info(
    "Operation completed",
    extra={
        "operation_id": operation_id,
        "user_id": user_id,
        "duration_ms": duration_ms,
        "status": "success"
    }
)
```

### Extra Fields Best Practices

- ✅ Use consistent field names across modules
- ✅ Include contextual information (IDs, timestamps, status)
- ✅ Use appropriate data types (strings, numbers, booleans)
- ✅ Avoid sensitive data (passwords, tokens) - use masking
- ✅ Keep extra fields concise and relevant

---

## Compliance Requirements

### Zero Tolerance Requirements

**MANDATORY** compliance metrics:

- ✅ **0** direct `logging.getLogger()` calls (except in logger_factory itself)
- ✅ **0** `logging.basicConfig()` calls (except in logger_factory itself)
- ✅ **0** `print()` statements for operational logging (test scripts exempt)
- ✅ **100%** of security modules use audit logging
- ✅ **100%** of service modules have debug logging capability
- ✅ **100%** console output is JSON formatted
- ✅ **100%** file output is detailed text formatted

### Quality Gates

All code MUST pass:

- ✅ **0** linting errors
- ✅ **0** type checking errors
- ✅ **0** security issues
- ✅ **0** TODO comments related to logging

### Functional Requirements

- ✅ Docker logs show consistent JSON format (console)
- ✅ Log files show consistent detailed text format
- ✅ Audit logs capture all security events
- ✅ Debug logs enable effective troubleshooting
- ✅ Syslog integration works correctly (if enabled)

---

## Enforcement

### Automated Enforcement

**MANDATORY** enforcement mechanisms:

1. **Pre-commit Hooks**: Detect logging violations before commit
2. **CI/CD Pipeline**: Validate logging compliance in build pipeline
3. **Linting Rules**: Automated detection of prohibited patterns
4. **Code Review**: Manual review for logging compliance

### Validation Scripts

Validation scripts MUST check for:
- Direct `logging.getLogger()` usage
- `logging.basicConfig()` usage
- `print()` statements in production code
- Missing audit logging in security modules
- Missing debug logging in service modules

---

## Migration Guide

### From Direct Logging to Logger Factory

#### Step 1: Replace Import
```python
# BEFORE (FORBIDDEN)
import logging
logger = logging.getLogger(__name__)

# AFTER (REQUIRED)
from src.services.logging.logger_factory import get_logger
logger = get_logger(__name__)
```

#### Step 2: Replace Logger Creation
```python
# BEFORE (FORBIDDEN)
logger = logging.getLogger(__name__)
component_logger = logging.getLogger(f"{__name__}.component")

# AFTER (REQUIRED)
logger = get_logger(__name__)
component_logger = get_component_logger("component_name", "subcomponent_name")
```

#### Step 3: Remove basicConfig Calls
```python
# BEFORE (FORBIDDEN)
logging.basicConfig(level=logging.INFO)

# AFTER (REQUIRED)
# Remove - configuration is handled centrally by logger factory
```

#### Step 4: Replace Print Statements
```python
# BEFORE (FORBIDDEN)
print("Operation completed")

# AFTER (REQUIRED)
logger.info("Operation completed")
```

---

## Related Documentation

- `src/services/logging/logger_factory.py` - Logger factory implementation
- `src/services/logging/structured/json_formatter.py` - JSON formatter
- `src/services/logging/config_manager.py` - Configuration manager
- `docs/implementation/in_progress/DEBUG_TROUBLESHOOTING_LOGGING_COMPLIANCE_SPEC_v1.0.0.md` - Troubleshooting and remediation guide
- Enterprise Canonical Execution Protocol
- Golden Rule Execution Protocol

---

## Version History

- **v1.0.0** (2025-12-08): Initial mandate document created

---

## Approval

This mandate is **ACTIVE** and **ENFORCEABLE** as of 2025-12-08.

**Compliance is MANDATORY. Non-compliance is a blocking issue.**
