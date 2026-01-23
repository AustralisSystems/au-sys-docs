# Security Best Practices: Input Validation, Encryption & OWASP Compliance

**Version**: v1.0.0
**Last Updated**: 2025-01-14

This document provides comprehensive best practices for implementing security measures in FastAPI applications, covering input validation, encryption, and OWASP compliance.

---

## Table of Contents

1. [Architecture Principles](#architecture-principles)
2. [Input Validation](#input-validation)
3. [Encryption & Cryptographic Security](#encryption--cryptographic-security)
4. [OWASP Compliance](#owasp-compliance)
5. [FastAPI Integration](#fastapi-integration)
6. [Security Testing](#security-testing)
7. [Performance Considerations](#performance-considerations)
8. [Production Deployment](#production-deployment)

---

## Architecture Principles

### Defense in Depth

Security must be implemented at multiple layers:

- **Input Layer**: Validate all data entering the system
- **Application Layer**: Secure code practices and business logic
- **Data Layer**: Encrypt and protect sensitive information
- **Infrastructure Layer**: Secure deployment and operations
- **Monitoring Layer**: Detect and respond to security events

### Zero Trust Approach

Never trust, always verify:

- **Verify Every Request**: Authentication and authorization required
- **Least Privilege**: Grant minimum necessary access
- **Assume Breach**: Plan for compromise scenarios
- **Continuous Validation**: Ongoing security monitoring

### Security by Design

- **Secure Defaults**: Fail securely, deny by default
- **Principle of Least Privilege**: Minimum necessary permissions
- **Fail-Safe Defaults**: Secure configuration out of the box
- **Complete Mediation**: Check authorization on every access

---

## Input Validation

### Core Principles

#### 1. Validate All Inputs

**MANDATORY**: Assume all input is potentially malicious. Validate data from all sources:

```python
from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Annotated
import re

class UserInput(BaseModel):
    """User input with comprehensive validation."""

    username: Annotated[
        str,
        Field(
            min_length=3,
            max_length=20,
            pattern=r'^[a-zA-Z0-9_]+$',
            description="Username: 3-20 alphanumeric characters"
        )
    ]

    email: Annotated[
        str,
        Field(
            pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            description="Valid email address"
        )
    ]

    age: Annotated[
        int,
        Field(ge=0, le=150, description="Age between 0 and 150")
    ]

    @field_validator('username', mode='before')
    @classmethod
    def sanitize_username(cls, v: str) -> str:
        """Sanitize username input."""
        if not isinstance(v, str):
            raise ValueError("Username must be a string")

        # Remove whitespace
        v = v.strip()

        # Remove null bytes
        v = v.replace('\x00', '')

        return v

    @field_validator('email', mode='after')
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        """Validate email format."""
        # Pydantic's EmailStr handles basic validation
        # Additional checks can be added here
        if len(v) > 254:  # RFC 5321 limit
            raise ValueError("Email address too long")
        return v.lower()  # Normalize to lowercase
```

#### 2. Use Allow-Lists (Whitelisting)

**PREFERRED**: Accept only known good inputs, reject all others:

```python
from enum import Enum
from pydantic import BaseModel, field_validator

class AllowedFileType(str, Enum):
    """Allowed file types."""
    PDF = "application/pdf"
    PNG = "image/png"
    JPEG = "image/jpeg"
    JSON = "application/json"

class FileUpload(BaseModel):
    """File upload with allow-list validation."""

    filename: str
    content_type: AllowedFileType
    size: int = Field(ge=1, le=10_000_000)  # Max 10MB

    @field_validator('filename')
    @classmethod
    def validate_filename(cls, v: str) -> str:
        """Validate filename against allow-list."""
        # Allow only alphanumeric, dots, hyphens, underscores
        if not re.match(r'^[a-zA-Z0-9._-]+$', v):
            raise ValueError("Invalid filename characters")

        # Block dangerous extensions
        dangerous_extensions = ['.exe', '.bat', '.sh', '.php', '.jsp']
        if any(v.lower().endswith(ext) for ext in dangerous_extensions):
            raise ValueError("File type not allowed")

        return v
```

#### 3. Syntactic and Semantic Validation

**REQUIRED**: Validate both format (syntactic) and meaning (semantic):

```python
from pydantic import BaseModel, field_validator, model_validator
from datetime import datetime

class DateRange(BaseModel):
    """Date range with semantic validation."""

    start_date: datetime
    end_date: datetime

    @model_validator(mode='after')
    def validate_date_range(self):
        """Semantic validation: end must be after start."""
        if self.end_date <= self.start_date:
            raise ValueError("End date must be after start date")

        # Check range is not too large
        delta = self.end_date - self.start_date
        if delta.days > 365:
            raise ValueError("Date range cannot exceed 365 days")

        return self
```

#### 4. Centralized Validation

**RECOMMENDED**: Use centralized validation routines:

```python
from pydantic import BaseModel, TypeAdapter
from typing import Any, Dict

class InputValidator:
    """Centralized input validation service."""

    def __init__(self):
        self.validators: Dict[str, TypeAdapter] = {}

    def register_validator(self, name: str, model: type[BaseModel]):
        """Register a validator for a specific input type."""
        self.validators[name] = TypeAdapter(model)

    def validate(self, name: str, data: Any) -> BaseModel:
        """Validate input using registered validator."""
        if name not in self.validators:
            raise ValueError(f"Validator '{name}' not found")

        return self.validators[name].validate_python(data)

# Usage
validator = InputValidator()
validator.register_validator("user", UserInput)
validator.register_validator("file", FileUpload)

# Validate anywhere in application
try:
    user = validator.validate("user", request_data)
except ValidationError as e:
    # Handle validation error
    pass
```

### SQL Injection Prevention

#### 1. Use Parameterized Queries

**MANDATORY**: Always use parameterized queries or ORM:

```python
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

# SECURE: Parameterized query
async def get_user_by_email(session: AsyncSession, email: str):
    """Get user by email using parameterized query."""
    query = text("SELECT * FROM users WHERE email = :email")
    result = await session.execute(query, {"email": email})
    return result.fetchone()

# SECURE: Using SQLAlchemy ORM
from sqlalchemy.orm import Session

async def get_user_by_email_orm(session: AsyncSession, email: str):
    """Get user using ORM (automatically parameterized)."""
    from app.models import User
    result = await session.query(User).filter(User.email == email).first()
    return result

# INSECURE: String concatenation (NEVER DO THIS)
async def get_user_by_email_unsafe(session: AsyncSession, email: str):
    """INSECURE - Vulnerable to SQL injection."""
    query = text(f"SELECT * FROM users WHERE email = '{email}'")  # DON'T DO THIS
    result = await session.execute(query)
    return result.fetchone()
```

#### 2. Input Sanitization for Database Operations

```python
import re
from pydantic import BaseModel, field_validator

class DatabaseQuery(BaseModel):
    """Database query parameters with sanitization."""

    table_name: str
    column_name: str
    value: str

    @field_validator('table_name', 'column_name')
    @classmethod
    def validate_identifier(cls, v: str) -> str:
        """Validate SQL identifier (table/column name)."""
        # Allow only alphanumeric and underscores
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', v):
            raise ValueError("Invalid identifier format")
        return v

    @field_validator('value')
    @classmethod
    def sanitize_value(cls, v: str) -> str:
        """Sanitize query value."""
        # Remove SQL injection patterns
        dangerous_patterns = [
            r"(\bOR\b|\bAND\b)",
            r"(--|#|\/\*|\*\/)",
            r"(\bUNION\b|\bSELECT\b)",
            r"(\bDROP\b|\bDELETE\b|\bINSERT\b|\bUPDATE\b)",
        ]

        for pattern in dangerous_patterns:
            if re.search(pattern, v, re.IGNORECASE):
                raise ValueError("Potentially dangerous SQL pattern detected")

        return v
```

### XSS (Cross-Site Scripting) Prevention

#### 1. Output Encoding

**MANDATORY**: Encode all output data:

```python
import html
from jinja2 import Environment, select_autoescape

# Configure Jinja2 with auto-escaping
env = Environment(
    autoescape=select_autoescape(['html', 'xml']),
    enable_async=True
)

# In templates, user input is automatically escaped
# {{ user_input }}  <!-- Automatically escaped -->

# Manual encoding in Python
def escape_html(text: str) -> str:
    """Escape HTML special characters."""
    return html.escape(text, quote=True)

# Example usage
user_input = "<script>alert('XSS')</script>"
safe_output = escape_html(user_input)
# Result: &lt;script&gt;alert(&#x27;XSS&#x27;)&lt;/script&gt;
```

#### 2. Content Security Policy (CSP)

```python
from fastapi import FastAPI, Response

app = FastAPI()

@app.middleware("http")
async def add_security_headers(request, call_next):
    """Add security headers including CSP."""
    response = await call_next(request)

    # Content Security Policy
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self' data:; "
        "connect-src 'self'; "
        "frame-ancestors 'none';"
    )

    # XSS Protection
    response.headers["X-XSS-Protection"] = "1; mode=block"

    # X-Content-Type-Options
    response.headers["X-Content-Type-Options"] = "nosniff"

    return response
```

#### 3. Input Sanitization for XSS

```python
import html
import re
from pydantic import BaseModel, field_validator

class SafeHTMLInput(BaseModel):
    """HTML input with XSS protection."""

    content: str

    @field_validator('content', mode='before')
    @classmethod
    def sanitize_html(cls, v: str) -> str:
        """Sanitize HTML input to prevent XSS."""
        if not isinstance(v, str):
            raise ValueError("Content must be a string")

        # Remove script tags and event handlers
        dangerous_patterns = [
            r'<script[^>]*>.*?</script>',
            r'on\w+\s*=',  # Event handlers like onclick=
            r'javascript:',
            r'vbscript:',
            r'data:text/html',
        ]

        sanitized = v
        for pattern in dangerous_patterns:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE | re.DOTALL)

        # HTML encode remaining content
        sanitized = html.escape(sanitized)

        return sanitized
```

### Command Injection Prevention

#### 1. Avoid Shell Execution

**MANDATORY**: Never use `shell=True` with user input:

```python
import subprocess
from typing import List

# SECURE: Direct command execution without shell
async def execute_command_secure(command: List[str]):
    """Execute command securely without shell."""
    try:
        result = subprocess.run(
            command,
            shell=False,  # Never use shell=True
            capture_output=True,
            text=True,
            timeout=30,
            check=True
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        raise ValueError("Command execution timeout")
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Command failed: {e.stderr}")

# SECURE: Validate command before execution
ALLOWED_COMMANDS = ['ls', 'cat', 'grep', 'find']

async def execute_allowed_command(command: str, args: List[str]):
    """Execute only allowed commands."""
    if command not in ALLOWED_COMMANDS:
        raise ValueError(f"Command '{command}' not allowed")

    # Validate arguments
    for arg in args:
        if not re.match(r'^[a-zA-Z0-9._/-]+$', arg):
            raise ValueError(f"Invalid argument: {arg}")

    return await execute_command_secure([command] + args)

# INSECURE: Shell execution with user input (NEVER DO THIS)
async def execute_command_unsafe(user_input: str):
    """INSECURE - Vulnerable to command injection."""
    subprocess.run(f"ls {user_input}", shell=True)  # DON'T DO THIS
```

#### 2. Path Traversal Prevention

```python
from pathlib import Path
from pydantic import BaseModel, field_validator

class FilePathInput(BaseModel):
    """File path input with traversal prevention."""

    file_path: str

    @field_validator('file_path')
    @classmethod
    def validate_path(cls, v: str) -> Path:
        """Validate and normalize file path."""
        # Remove any path traversal attempts
        normalized = Path(v).resolve()

        # Define allowed base directory
        BASE_DIR = Path("/allowed/directory")

        # Ensure path is within base directory
        try:
            normalized.relative_to(BASE_DIR)
        except ValueError:
            raise ValueError("Path traversal detected")

        # Check for dangerous patterns
        if '..' in str(normalized):
            raise ValueError("Path traversal detected")

        return normalized
```

---

## Encryption & Cryptographic Security

### Core Principles

#### 1. Use Strong Algorithms

**MANDATORY**: Use industry-standard encryption algorithms:

```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import secrets
import os

class EncryptionService:
    """Enterprise encryption service."""

    def __init__(self):
        self.backend = default_backend()

    def generate_key(self, algorithm: str = "AES-256") -> bytes:
        """Generate encryption key."""
        if algorithm == "AES-256":
            return secrets.token_bytes(32)  # 256 bits
        elif algorithm == "AES-128":
            return secrets.token_bytes(16)  # 128 bits
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")

    def encrypt_aes_gcm(self, data: bytes, key: bytes) -> tuple[bytes, bytes, bytes]:
        """Encrypt data using AES-256-GCM."""
        # Generate nonce
        nonce = secrets.token_bytes(12)  # 96 bits for GCM

        # Create cipher
        aesgcm = AESGCM(key)

        # Encrypt
        ciphertext = aesgcm.encrypt(nonce, data, None)

        return ciphertext, nonce, key

    def decrypt_aes_gcm(self, ciphertext: bytes, nonce: bytes, key: bytes) -> bytes:
        """Decrypt data using AES-256-GCM."""
        aesgcm = AESGCM(key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext
```

#### 2. Key Derivation

**REQUIRED**: Use proper key derivation functions:

```python
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import secrets

class KeyDerivationService:
    """Key derivation service."""

    def derive_key_from_password(
        self,
        password: str,
        salt: bytes = None,
        iterations: int = 100000
    ) -> tuple[bytes, bytes]:
        """Derive encryption key from password using PBKDF2."""
        # Generate salt if not provided
        if salt is None:
            salt = secrets.token_bytes(16)

        # Create KDF
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # 256 bits
            salt=salt,
            iterations=iterations,
            backend=default_backend()
        )

        # Derive key
        key = kdf.derive(password.encode('utf-8'))

        return key, salt
```

#### 3. Password Hashing

**MANDATORY**: Use bcrypt or Argon2 for password hashing:

```python
from passlib.context import CryptContext
import bcrypt

# Use Argon2 (preferred) or bcrypt
pwd_context = CryptContext(
    schemes=["argon2"],  # or ["bcrypt"]
    deprecated="auto",
    argon2__memory_cost=65536,  # 64 MB
    argon2__time_cost=3,  # 3 iterations
    argon2__parallelism=4,  # 4 threads
)

def hash_password(password: str) -> str:
    """Hash password securely."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(plain_password, hashed_password)

# Alternative: Direct bcrypt usage
def hash_password_bcrypt(password: str) -> str:
    """Hash password using bcrypt."""
    salt = bcrypt.gensalt(rounds=12)  # 2^12 rounds
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password_bcrypt(plain_password: str, hashed_password: str) -> bool:
    """Verify password using bcrypt."""
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )
```

### Key Management

#### 1. Secure Key Storage

**CRITICAL**: Never store keys in code or configuration files:

```python
import os
from cryptography.fernet import Fernet
from typing import Optional

class KeyManager:
    """Secure key management service."""

    def __init__(self):
        # Load master key from environment variable
        master_key = os.getenv("MASTER_ENCRYPTION_KEY")
        if not master_key:
            raise ValueError("MASTER_ENCRYPTION_KEY environment variable not set")

        # Convert to bytes if needed
        if isinstance(master_key, str):
            master_key = master_key.encode('utf-8')

        self.master_key = master_key
        self.fernet = Fernet(self.master_key)

    def encrypt_key(self, key: bytes) -> bytes:
        """Encrypt a key for storage."""
        return self.fernet.encrypt(key)

    def decrypt_key(self, encrypted_key: bytes) -> bytes:
        """Decrypt a stored key."""
        return self.fernet.decrypt(encrypted_key)

    def generate_application_key(self) -> tuple[bytes, bytes]:
        """Generate and encrypt application key."""
        # Generate new key
        app_key = secrets.token_bytes(32)

        # Encrypt for storage
        encrypted_key = self.encrypt_key(app_key)

        return app_key, encrypted_key
```

#### 2. Key Rotation

```python
from datetime import datetime, timedelta
from typing import Dict, Optional

class RotatingKeyManager:
    """Key manager with automatic rotation."""

    def __init__(self, rotation_interval_days: int = 90):
        self.keys: Dict[str, Dict] = {}
        self.rotation_interval = timedelta(days=rotation_interval_days)

    def get_current_key(self, key_id: str) -> Optional[bytes]:
        """Get current active key."""
        key_info = self.keys.get(key_id)
        if not key_info:
            return None

        # Check if key needs rotation
        if datetime.now() - key_info['created_at'] > self.rotation_interval:
            self.rotate_key(key_id)
            key_info = self.keys[key_id]

        return key_info['key']

    def rotate_key(self, key_id: str) -> bytes:
        """Rotate key and keep old key for decryption."""
        old_key_info = self.keys.get(key_id)

        # Generate new key
        new_key = secrets.token_bytes(32)

        # Store new key
        self.keys[key_id] = {
            'key': new_key,
            'created_at': datetime.now(),
            'previous_key': old_key_info['key'] if old_key_info else None,
        }

        return new_key
```

### Data Encryption at Rest

```python
from cryptography.fernet import Fernet
import json
from typing import Any, Dict

class DataEncryptionService:
    """Service for encrypting data at rest."""

    def __init__(self, key: bytes):
        self.fernet = Fernet(key)

    def encrypt_data(self, data: Dict[str, Any]) -> bytes:
        """Encrypt data dictionary."""
        # Serialize to JSON
        json_data = json.dumps(data).encode('utf-8')

        # Encrypt
        encrypted = self.fernet.encrypt(json_data)

        return encrypted

    def decrypt_data(self, encrypted_data: bytes) -> Dict[str, Any]:
        """Decrypt data dictionary."""
        # Decrypt
        json_data = self.fernet.decrypt(encrypted_data)

        # Deserialize from JSON
        data = json.loads(json_data.decode('utf-8'))

        return data
```

### Data Encryption in Transit

```python
from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app = FastAPI()

# Force HTTPS in production
if os.getenv("ENVIRONMENT") == "production":
    app.add_middleware(HTTPSRedirectMiddleware)

@app.middleware("http")
async def add_security_headers(request, call_next):
    """Add security headers for encrypted transit."""
    response = await call_next(request)

    # HSTS (HTTP Strict Transport Security)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

    # Prevent protocol downgrade
    response.headers["Upgrade-Insecure-Requests"] = "1"

    return response
```

---

## OWASP Compliance

### OWASP Top 10 (2021)

#### 1. Broken Access Control

**Prevention**:

```python
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer
from typing import List

security = HTTPBearer()

async def verify_permission(
    required_permission: str,
    token: str = Security(security)
):
    """Verify user has required permission."""
    # Decode and verify token
    user = await decode_jwt_token(token.credentials)

    # Check permissions
    if required_permission not in user.permissions:
        raise HTTPException(
            status_code=403,
            detail=f"Permission '{required_permission}' required"
        )

    return user

# Usage
@app.get("/admin/users")
async def get_users(
    user: dict = Depends(lambda: verify_permission("admin:read"))
):
    """Get users (admin only)."""
    return {"users": []}
```

#### 2. Cryptographic Failures

**Prevention**: See [Encryption & Cryptographic Security](#encryption--cryptographic-security) section.

#### 3. Injection

**Prevention**: See [SQL Injection Prevention](#sql-injection-prevention) and [Command Injection Prevention](#command-injection-prevention) sections.

#### 4. Insecure Design

**Prevention**:

```python
from pydantic import BaseModel, Field
from typing import Optional

class SecureUserModel(BaseModel):
    """Secure user model with proper design."""

    id: int = Field(gt=0, description="User ID")
    username: str = Field(
        min_length=3,
        max_length=20,
        pattern=r'^[a-zA-Z0-9_]+$',
        description="Username"
    )
    email: str = Field(
        pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        description="Email address"
    )
    # Never expose password in response
    password: Optional[str] = Field(exclude=True)

    class Config:
        # Prevent mass assignment
        extra = "forbid"
        # Validate on assignment
        validate_assignment = True
```

#### 5. Security Misconfiguration

**Prevention**:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(
    title="Secure API",
    version="1.0.0",
    # Disable docs in production
    docs_url="/docs" if os.getenv("ENVIRONMENT") == "development" else None,
    redoc_url="/redoc" if os.getenv("ENVIRONMENT") == "development" else None,
)

# Secure CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "").split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    max_age=3600,
)
```

#### 6. Vulnerable and Outdated Components

**Prevention**:

```bash
# Regularly update dependencies
pip list --outdated
pip install --upgrade package-name

# Use security scanning tools
bandit -r . --severity-level=high
safety check
```

#### 7. Identification and Authentication Failures

**Prevention**: See [Authentication & Authorization Best Practices](./authentication-authorization-multi-strategy-best-practices-2025.md).

#### 8. Software and Data Integrity Failures

**Prevention**:

```python
import hashlib
from typing import Optional

class IntegrityChecker:
    """Check data integrity using checksums."""

    def calculate_checksum(self, data: bytes) -> str:
        """Calculate SHA-256 checksum."""
        return hashlib.sha256(data).hexdigest()

    def verify_integrity(self, data: bytes, expected_checksum: str) -> bool:
        """Verify data integrity."""
        actual_checksum = self.calculate_checksum(data)
        return actual_checksum == expected_checksum
```

#### 9. Security Logging and Monitoring Failures

**Prevention**:

```python
import logging
from datetime import datetime
from typing import Dict, Any

class SecurityLogger:
    """Security event logger."""

    def __init__(self):
        self.logger = logging.getLogger("security")
        self.logger.setLevel(logging.INFO)

    def log_security_event(
        self,
        event_type: str,
        details: Dict[str, Any],
        severity: str = "INFO"
    ):
        """Log security event."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "severity": severity,
            "details": details,
        }

        if severity == "CRITICAL":
            self.logger.critical(log_entry)
        elif severity == "WARNING":
            self.logger.warning(log_entry)
        else:
            self.logger.info(log_entry)
```

#### 10. Server-Side Request Forgery (SSRF)

**Prevention**:

```python
from pydantic import BaseModel, field_validator, HttpUrl
from ipaddress import ip_address
import socket

class URLValidator:
    """Validate URLs to prevent SSRF."""

    BLOCKED_IPS = [
        "127.0.0.1",
        "localhost",
        "0.0.0.0",
        "::1",
    ]

    def validate_url(self, url: str) -> bool:
        """Validate URL is safe from SSRF."""
        try:
            parsed = HttpUrl(url)
            hostname = parsed.host

            # Resolve hostname to IP
            ip = socket.gethostbyname(hostname)

            # Check if IP is blocked
            if ip in self.BLOCKED_IPS:
                return False

            # Check if IP is private
            ip_obj = ip_address(ip)
            if ip_obj.is_private or ip_obj.is_loopback:
                return False

            return True

        except Exception:
            return False
```

---

## FastAPI Integration

### Security Middleware Stack

```python
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
import time

app = FastAPI()

# 1. HTTPS Redirect (production)
if os.getenv("ENVIRONMENT") == "production":
    app.add_middleware(HTTPSRedirectMiddleware)

# 2. CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "").split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# 3. Security Headers
@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    """Add security headers."""
    response = await call_next(request)

    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

    # CSP
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:;"
    )

    return response

# 4. Input Validation Middleware
@app.middleware("http")
async def input_validation_middleware(request: Request, call_next):
    """Validate input before processing."""
    # Validate request size
    if request.headers.get("content-length"):
        content_length = int(request.headers["content-length"])
        if content_length > 10_000_000:  # 10MB limit
            return Response(
                status_code=413,
                content="Request too large"
            )

    response = await call_next(request)
    return response
```

### Pydantic Validation Integration

```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, ValidationError
from typing import Any

app = FastAPI()

# Custom validation error handler
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc: ValidationError):
    """Handle Pydantic validation errors."""
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "message": "Validation error"
        }
    )

# Use Pydantic models for automatic validation
class CreateUserRequest(BaseModel):
    """User creation request with validation."""
    username: str = Field(min_length=3, max_length=20)
    email: str = Field(pattern=r'^[^\s@]+@[^\s@]+\.[^\s@]+$')
    password: str = Field(min_length=8)

@app.post("/users")
async def create_user(user: CreateUserRequest):
    """Create user (automatically validated)."""
    # User data is already validated by Pydantic
    return {"message": "User created", "username": user.username}
```

---

## Security Testing

### Static Analysis with Bandit

```bash
# Install Bandit
pip install bandit

# Run security scan
bandit -r . -f json -o bandit-report.json

# Scan with specific severity level
bandit -r . --severity-level=high

# Scan specific file types
bandit -r . -lll  # Low, Low, Low (severity levels)
```

### Security Test Examples

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_sql_injection_prevention():
    """Test SQL injection prevention."""
    # Attempt SQL injection
    response = client.get("/users?email=' OR '1'='1")
    assert response.status_code != 200  # Should fail validation

def test_xss_prevention():
    """Test XSS prevention."""
    # Attempt XSS
    xss_payload = "<script>alert('XSS')</script>"
    response = client.post("/users", json={"username": xss_payload})
    assert response.status_code == 422  # Should fail validation

def test_command_injection_prevention():
    """Test command injection prevention."""
    # Attempt command injection
    payload = "; rm -rf /"
    response = client.post("/execute", json={"command": payload})
    assert response.status_code != 200  # Should fail validation
```

---

## Performance Considerations

### Efficient Validation

```python
from pydantic import BaseModel, field_validator
from typing import Optional
import re

# Cache compiled regex patterns
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

class OptimizedUserModel(BaseModel):
    """Optimized user model with cached patterns."""

    email: str

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate email using cached pattern."""
        if not EMAIL_PATTERN.match(v):
            raise ValueError("Invalid email format")
        return v.lower()
```

### Async Validation

```python
from pydantic import BaseModel
from typing import Optional
import httpx

class AsyncValidationModel(BaseModel):
    """Model with async validation."""

    email: str

    @field_validator('email', mode='after')
    @classmethod
    async def validate_email_exists(cls, v: str) -> str:
        """Async validation: check if email exists."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://api.example.com/check-email/{v}")
            if response.status_code == 404:
                raise ValueError("Email not found")
        return v
```

---

## Production Deployment

### Security Checklist

- [ ] All inputs validated with Pydantic
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (output encoding)
- [ ] CSRF protection implemented
- [ ] Strong encryption algorithms (AES-256, RSA-2048+)
- [ ] Secure key management (environment variables, key vaults)
- [ ] HTTPS enforced in production
- [ ] Security headers configured
- [ ] Content Security Policy (CSP) implemented
- [ ] Security logging enabled
- [ ] Regular dependency updates
- [ ] Security scanning (Bandit, Safety)
- [ ] Rate limiting implemented
- [ ] Error messages don't expose sensitive information

### Environment Configuration

```python
from pydantic_settings import BaseSettings

class SecuritySettings(BaseSettings):
    """Security configuration."""

    # Encryption
    encryption_key: str
    encryption_algorithm: str = "AES-256-GCM"

    # Key Management
    key_rotation_interval_days: int = 90

    # Validation
    max_input_length: int = 10000
    max_file_size_mb: int = 10

    # Security Headers
    enable_csp: bool = True
    enable_hsts: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = SecuritySettings()
```

---

## Summary

### Key Takeaways

1. **Input Validation**: Always validate and sanitize all inputs using Pydantic
2. **Encryption**: Use strong algorithms (AES-256, RSA-2048+) and secure key management
3. **OWASP Compliance**: Follow OWASP Top 10 guidelines and secure coding practices
4. **Defense in Depth**: Implement security at multiple layers
5. **Security Testing**: Regular security scans and penetration testing
6. **Secure Defaults**: Fail securely, deny by default

### Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Cryptography Library](https://cryptography.io/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)

---

**Version**: v1.0.0
**Last Updated**: 2025-01-14
