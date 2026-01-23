# Feature Flags Best Practices 2025
**Version**: v1.0.0
**Last Updated**: 2025-01-14
**OpenFeature Specification**: Latest
**Python Version**: 3.9+

This document compiles the latest best practices for implementing and managing feature flags based on official specifications (OpenFeature), production code examples, and industry recommendations.

---

## Table of Contents

1. [Architecture Principles](#architecture-principles)
2. [Feature Flag Types](#feature-flag-types)
3. [Evaluation Patterns](#evaluation-patterns)
4. [Targeting & Rollout Strategies](#targeting--rollout-strategies)
5. [A/B Testing](#ab-testing)
6. [Performance Optimization](#performance-optimization)
7. [Caching Strategies](#caching-strategies)
8. [Dependency Management](#dependency-management)
9. [Lifecycle Management](#lifecycle-management)
10. [Security & Compliance](#security--compliance)
11. [Monitoring & Observability](#monitoring--observability)
12. [FastAPI Integration](#fastapi-integration)

---

## Architecture Principles

### ✅ Core Design Principles

#### 1. Separation of Concerns

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from dataclasses import dataclass

@dataclass
class EvaluationContext:
    """Context for flag evaluation."""
    user_id: Optional[str] = None
    group_id: Optional[str] = None
    environment: Optional[str] = None
    attributes: Dict[str, Any] = None

class FeatureFlagProvider(ABC):
    """Abstract feature flag provider."""

    @abstractmethod
    async def evaluate(
        self,
        flag_key: str,
        context: EvaluationContext,
        default_value: Any
    ) -> Any:
        """Evaluate feature flag."""
        pass

class FeatureFlagManager:
    """Feature flag manager (orchestration layer)."""

    def __init__(self, provider: FeatureFlagProvider):
        self._provider = provider
        self._cache = {}

    async def is_enabled(
        self,
        flag_key: str,
        context: Optional[EvaluationContext] = None,
        default: bool = False
    ) -> bool:
        """Check if flag is enabled."""
        return await self._provider.evaluate(flag_key, context, default)
```

#### 2. Vendor-Agnostic API (OpenFeature)

```python
from openfeature import api
from openfeature.provider import Provider

# Vendor-agnostic API
client = api.get_client()

# Evaluate flag
is_enabled = client.get_boolean_value("new-feature", False)

# With context
context = api.EvaluationContext(
    targeting_key="user-123",
    attributes={"email": "user@example.com", "region": "us-east"}
)
is_enabled = client.get_boolean_value("new-feature", False, context)
```

---

## Feature Flag Types

### ✅ Best Practices

#### 1. Boolean Flags

```python
class FeatureFlag:
    """Boolean feature flag."""

    def __init__(
        self,
        name: str,
        enabled: bool = False,
        description: Optional[str] = None
    ):
        self.name = name
        self.enabled = enabled
        self.description = description

# Usage
flag = FeatureFlag("new-checkout-flow", enabled=True)
if flag_manager.is_enabled("new-checkout-flow"):
    # Use new checkout flow
    pass
```

#### 2. Percentage Rollout Flags

```python
class PercentageRolloutFlag(FeatureFlag):
    """Percentage-based rollout flag."""

    def __init__(
        self,
        name: str,
        rollout_percentage: int,
        **kwargs
    ):
        super().__init__(name, **kwargs)
        self.rollout_percentage = rollout_percentage

    def is_in_rollout(self, user_id: str) -> bool:
        """Check if user is in rollout percentage."""
        import hashlib

        # Consistent hashing for user
        hash_input = f"{self.name}:{user_id}"
        hash_value = int(hashlib.sha256(hash_input.encode()).hexdigest()[:8], 16) % 100
        return hash_value < self.rollout_percentage
```

#### 3. Variant Flags (A/B Testing)

```python
from enum import Enum

class Variant(str, Enum):
    """Feature flag variants."""
    CONTROL = "control"
    VARIANT_A = "variant_a"
    VARIANT_B = "variant_b"

class VariantFlag(FeatureFlag):
    """Variant-based flag for A/B testing."""

    def __init__(
        self,
        name: str,
        variants: Dict[str, Any],
        default_variant: str,
        **kwargs
    ):
        super().__init__(name, **kwargs)
        self.variants = variants
        self.default_variant = default_variant

    def get_variant(self, user_id: str) -> str:
        """Get variant for user."""
        # Consistent assignment based on user_id
        hash_value = hash(f"{self.name}:{user_id}") % 100

        # Example: 50% control, 25% variant_a, 25% variant_b
        if hash_value < 50:
            return Variant.CONTROL
        elif hash_value < 75:
            return Variant.VARIANT_A
        else:
            return Variant.VARIANT_B
```

#### 4. String/Numeric Flags

```python
class StringFlag(FeatureFlag):
    """String configuration flag."""

    def __init__(
        self,
        name: str,
        default_value: str,
        **kwargs
    ):
        super().__init__(name, **kwargs)
        self.default_value = default_value

class NumericFlag(FeatureFlag):
    """Numeric configuration flag."""

    def __init__(
        self,
        name: str,
        default_value: float,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        **kwargs
    ):
        super().__init__(name, **kwargs)
        self.default_value = default_value
        self.min_value = min_value
        self.max_value = max_value
```

#### 5. JSON/Complex Flags

```python
from typing import Dict, Any

class JSONFlag(FeatureFlag):
    """JSON configuration flag."""

    def __init__(
        self,
        name: str,
        default_config: Dict[str, Any],
        **kwargs
    ):
        super().__init__(name, **kwargs)
        self.default_config = default_config

    def get_config(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Get configuration for user."""
        # Can return different configs based on user
        return self.default_config
```

---

## Evaluation Patterns

### ✅ Best Practices

#### 1. Context-Based Evaluation

```python
from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class EvaluationContext:
    """Context for flag evaluation."""
    user_id: Optional[str] = None
    group_id: Optional[str] = None
    environment: Optional[str] = None
    session_id: Optional[str] = None
    geographic_region: Optional[str] = None
    device_type: Optional[str] = None
    user_segment: Optional[str] = None
    attributes: Dict[str, Any] = None

    def __post_init__(self):
        if self.attributes is None:
            self.attributes = {}

class FeatureFlagManager:
    """Feature flag manager with context evaluation."""

    async def evaluate(
        self,
        flag_key: str,
        context: EvaluationContext,
        default_value: Any
    ) -> Any:
        """Evaluate flag with context."""
        flag = self._get_flag(flag_key)
        if not flag:
            return default_value

        # Check environment
        if not self._is_environment_enabled(flag, context.environment):
            return default_value

        # Check user targeting
        if not self._is_user_targeted(flag, context):
            return default_value

        # Check group targeting
        if not self._is_group_targeted(flag, context):
            return default_value

        # Check percentage rollout
        if not self._is_in_rollout(flag, context.user_id):
            return default_value

        return flag.value
```

#### 2. Default Value Strategy

```python
class FeatureFlagManager:
    """Feature flag manager with safe defaults."""

    async def get_boolean_value(
        self,
        flag_key: str,
        default: bool = False,
        context: Optional[EvaluationContext] = None
    ) -> bool:
        """Get boolean value with safe default."""
        try:
            return await self.evaluate(flag_key, context or EvaluationContext(), default)
        except Exception as e:
            logger.error(f"Error evaluating flag {flag_key}: {e}")
            return default  # Always return default on error

    async def get_string_value(
        self,
        flag_key: str,
        default: str = "",
        context: Optional[EvaluationContext] = None
    ) -> str:
        """Get string value with safe default."""
        try:
            value = await self.evaluate(flag_key, context or EvaluationContext(), default)
            return str(value) if value is not None else default
        except Exception as e:
            logger.error(f"Error evaluating flag {flag_key}: {e}")
            return default
```

#### 3. Bulk Evaluation

```python
class FeatureFlagManager:
    """Feature flag manager with bulk evaluation."""

    async def evaluate_all(
        self,
        flag_keys: List[str],
        context: EvaluationContext,
        default_values: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Evaluate multiple flags at once."""
        default_values = default_values or {}
        results = {}

        # Evaluate all flags in parallel
        tasks = [
            self.evaluate(
                key,
                context,
                default_values.get(key, None)
            )
            for key in flag_keys
        ]

        values = await asyncio.gather(*tasks, return_exceptions=True)

        for key, value in zip(flag_keys, values):
            if isinstance(value, Exception):
                logger.error(f"Error evaluating {key}: {value}")
                results[key] = default_values.get(key, None)
            else:
                results[key] = value

        return results
```

---

## Targeting & Rollout Strategies

### ✅ Best Practices

#### 1. User Targeting

```python
class FeatureFlag:
    """Feature flag with user targeting."""

    def __init__(
        self,
        name: str,
        enabled_for_users: Optional[List[str]] = None,
        **kwargs
    ):
        super().__init__(name, **kwargs)
        self.enabled_for_users = enabled_for_users or []

    def is_user_targeted(self, user_id: Optional[str]) -> bool:
        """Check if user is targeted."""
        if not self.enabled_for_users:
            return True  # No targeting = all users
        return user_id in self.enabled_for_users
```

#### 2. Group Targeting

```python
class FeatureFlag:
    """Feature flag with group targeting."""

    def __init__(
        self,
        name: str,
        enabled_for_groups: Optional[List[str]] = None,
        **kwargs
    ):
        super().__init__(name, **kwargs)
        self.enabled_for_groups = enabled_for_groups or []

    def is_group_targeted(self, group_id: Optional[str]) -> bool:
        """Check if group is targeted."""
        if not self.enabled_for_groups:
            return True
        return group_id in self.enabled_for_groups
```

#### 3. Attribute-Based Targeting

```python
class FeatureFlag:
    """Feature flag with attribute-based targeting."""

    def __init__(
        self,
        name: str,
        targeting_rules: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ):
        super().__init__(name, **kwargs)
        self.targeting_rules = targeting_rules or []

    def matches_targeting(
        self,
        context: EvaluationContext
    ) -> bool:
        """Check if context matches targeting rules."""
        if not self.targeting_rules:
            return True

        for rule in self.targeting_rules:
            if self._evaluate_rule(rule, context):
                return True

        return False

    def _evaluate_rule(
        self,
        rule: Dict[str, Any],
        context: EvaluationContext
    ) -> bool:
        """Evaluate targeting rule."""
        attribute = rule.get("attribute")
        operator = rule.get("operator")
        value = rule.get("value")

        context_value = context.attributes.get(attribute)

        if operator == "equals":
            return context_value == value
        elif operator == "contains":
            return value in context_value if isinstance(context_value, list) else False
        elif operator == "greater_than":
            return context_value > value
        elif operator == "less_than":
            return context_value < value

        return False
```

#### 4. Gradual Rollout

```python
class GradualRolloutFlag(FeatureFlag):
    """Feature flag with gradual rollout."""

    def __init__(
        self,
        name: str,
        rollout_percentage: int = 0,
        rollout_schedule: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ):
        super().__init__(name, **kwargs)
        self.rollout_percentage = rollout_percentage
        self.rollout_schedule = rollout_schedule or []

    def get_current_rollout_percentage(self) -> int:
        """Get current rollout percentage based on schedule."""
        if not self.rollout_schedule:
            return self.rollout_percentage

        now = datetime.now(timezone.utc)

        for step in sorted(self.rollout_schedule, key=lambda x: x["date"]):
            if now >= step["date"]:
                return step["percentage"]

        return self.rollout_percentage

    def is_in_rollout(self, user_id: str) -> bool:
        """Check if user is in current rollout."""
        percentage = self.get_current_rollout_percentage()

        if percentage >= 100:
            return True

        # Consistent hashing
        hash_value = int(
            hashlib.sha256(f"{self.name}:{user_id}".encode()).hexdigest()[:8],
            16
        ) % 100

        return hash_value < percentage
```

#### 5. Scheduled Rollout

```python
from datetime import datetime, timezone
from typing import List, Dict, Any

class ScheduledRolloutFlag(FeatureFlag):
    """Feature flag with scheduled rollout."""

    def __init__(
        self,
        name: str,
        scheduled_steps: List[Dict[str, Any]],
        **kwargs
    ):
        super().__init__(name, **kwargs)
        self.scheduled_steps = sorted(
            scheduled_steps,
            key=lambda x: x["date"]
        )

    def get_active_step(self) -> Optional[Dict[str, Any]]:
        """Get currently active rollout step."""
        now = datetime.now(timezone.utc)

        active_step = None
        for step in self.scheduled_steps:
            if now >= step["date"]:
                active_step = step
            else:
                break

        return active_step
```

---

## A/B Testing

### ✅ Best Practices

#### 1. Variant Assignment

```python
import hashlib
from enum import Enum
from typing import Dict, Any

class Variant(str, Enum):
    """Feature flag variants."""
    CONTROL = "control"
    VARIANT_A = "variant_a"
    VARIANT_B = "variant_b"

class ABTestFlag(FeatureFlag):
    """A/B test feature flag."""

    def __init__(
        self,
        name: str,
        variants: Dict[str, Dict[str, Any]],
        distribution: Dict[str, float],
        **kwargs
    ):
        super().__init__(name, **kwargs)
        self.variants = variants
        self.distribution = distribution

    def get_variant(self, user_id: str) -> str:
        """Get variant for user (consistent assignment)."""
        # Consistent hashing ensures same user gets same variant
        hash_input = f"{self.name}:{user_id}"
        hash_value = int(
            hashlib.sha256(hash_input.encode()).hexdigest()[:8],
            16
        ) % 100

        cumulative = 0
        for variant, percentage in self.distribution.items():
            cumulative += percentage
            if hash_value < cumulative:
                return variant

        return Variant.CONTROL
```

#### 2. Experiment Tracking

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ExperimentEvent:
    """Experiment event for tracking."""
    flag_key: str
    variant: str
    user_id: str
    timestamp: datetime
    event_type: str  # "exposure", "conversion", etc.
    metadata: Dict[str, Any] = None

class ABTestManager:
    """A/B test manager with tracking."""

    def __init__(self, flag_manager: FeatureFlagManager):
        self._flag_manager = flag_manager
        self._events: List[ExperimentEvent] = []

    async def track_exposure(
        self,
        flag_key: str,
        user_id: str,
        context: EvaluationContext
    ) -> None:
        """Track experiment exposure."""
        variant = await self._flag_manager.get_variant(flag_key, context)

        event = ExperimentEvent(
            flag_key=flag_key,
            variant=variant,
            user_id=user_id,
            timestamp=datetime.now(timezone.utc),
            event_type="exposure"
        )

        self._events.append(event)
        # Send to analytics
        await self._send_to_analytics(event)

    async def track_conversion(
        self,
        flag_key: str,
        user_id: str,
        conversion_name: str
    ) -> None:
        """Track conversion event."""
        event = ExperimentEvent(
            flag_key=flag_key,
            variant="",  # Will be filled from exposure
            user_id=user_id,
            timestamp=datetime.now(timezone.utc),
            event_type="conversion",
            metadata={"conversion_name": conversion_name}
        )

        self._events.append(event)
        await self._send_to_analytics(event)
```

---

## Performance Optimization

### ✅ Best Practices

#### 1. Caching

```python
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta

class FeatureFlagCache:
    """Feature flag cache."""

    def __init__(self, ttl_seconds: int = 60):
        self._cache: Dict[str, Tuple[Any, datetime]] = {}
        self._ttl = timedelta(seconds=ttl_seconds)

    def get(self, key: str) -> Optional[Any]:
        """Get cached value."""
        if key not in self._cache:
            return None

        value, timestamp = self._cache[key]

        if datetime.now() - timestamp > self._ttl:
            del self._cache[key]
            return None

        return value

    def set(self, key: str, value: Any) -> None:
        """Set cached value."""
        self._cache[key] = (value, datetime.now())

    def invalidate(self, key: Optional[str] = None) -> None:
        """Invalidate cache."""
        if key:
            self._cache.pop(key, None)
        else:
            self._cache.clear()

class FeatureFlagManager:
    """Feature flag manager with caching."""

    def __init__(self, cache: Optional[FeatureFlagCache] = None):
        self._cache = cache or FeatureFlagCache()

    async def evaluate(
        self,
        flag_key: str,
        context: EvaluationContext,
        default_value: Any
    ) -> Any:
        """Evaluate flag with caching."""
        # Create cache key from flag and context
        cache_key = self._create_cache_key(flag_key, context)

        # Check cache
        cached_value = self._cache.get(cache_key)
        if cached_value is not None:
            return cached_value

        # Evaluate flag
        value = await self._evaluate_flag(flag_key, context, default_value)

        # Cache result
        self._cache.set(cache_key, value)

        return value

    def _create_cache_key(
        self,
        flag_key: str,
        context: EvaluationContext
    ) -> str:
        """Create cache key from flag and context."""
        key_parts = [flag_key]
        if context.user_id:
            key_parts.append(f"user:{context.user_id}")
        if context.group_id:
            key_parts.append(f"group:{context.group_id}")
        if context.environment:
            key_parts.append(f"env:{context.environment}")
        return ":".join(key_parts)
```

#### 2. Lazy Evaluation

```python
class FeatureFlagManager:
    """Feature flag manager with lazy evaluation."""

    def __init__(self):
        self._evaluated_flags: Dict[str, Any] = {}

    async def evaluate_lazy(
        self,
        flag_key: str,
        context: EvaluationContext,
        default_value: Any
    ) -> Any:
        """Lazy evaluate flag (only when accessed)."""
        cache_key = self._create_cache_key(flag_key, context)

        if cache_key not in self._evaluated_flags:
            self._evaluated_flags[cache_key] = await self._evaluate_flag(
                flag_key, context, default_value
            )

        return self._evaluated_flags[cache_key]
```

#### 3. Preloading

```python
class FeatureFlagManager:
    """Feature flag manager with preloading."""

    async def preload_flags(
        self,
        flag_keys: List[str],
        context: EvaluationContext
    ) -> None:
        """Preload flags for context."""
        tasks = [
            self.evaluate(key, context, None)
            for key in flag_keys
        ]
        await asyncio.gather(*tasks)
```

---

## Caching Strategies

### ✅ Best Practices

#### 1. Multi-Level Caching

```python
class MultiLevelCache:
    """Multi-level cache for feature flags."""

    def __init__(self):
        self._l1_cache: Dict[str, Any] = {}  # In-memory
        self._l2_cache = None  # Redis (optional)
        self._l1_ttl = 60  # seconds
        self._l2_ttl = 300  # seconds

    async def get(self, key: str) -> Optional[Any]:
        """Get from cache (L1 -> L2)."""
        # Check L1 cache
        if key in self._l1_cache:
            return self._l1_cache[key]

        # Check L2 cache (Redis)
        if self._l2_cache:
            value = await self._l2_cache.get(key)
            if value:
                self._l1_cache[key] = value
                return value

        return None

    async def set(self, key: str, value: Any) -> None:
        """Set in cache (L1 and L2)."""
        self._l1_cache[key] = value

        if self._l2_cache:
            await self._l2_cache.setex(key, self._l2_ttl, value)
```

#### 2. Cache Invalidation

```python
class FeatureFlagManager:
    """Feature flag manager with cache invalidation."""

    def __init__(self, cache: FeatureFlagCache):
        self._cache = cache
        self._invalidation_callbacks: List[Callable] = []

    def register_invalidation_callback(self, callback: Callable) -> None:
        """Register callback for cache invalidation."""
        self._invalidation_callbacks.append(callback)

    async def update_flag(self, flag_key: str, flag: FeatureFlag) -> None:
        """Update flag and invalidate cache."""
        # Update flag
        self._flags[flag_key] = flag

        # Invalidate cache
        self._cache.invalidate(flag_key)

        # Notify callbacks
        for callback in self._invalidation_callbacks:
            await callback(flag_key)
```

---

## Dependency Management

### ✅ Best Practices

#### 1. Flag Dependencies

```python
class FeatureFlag:
    """Feature flag with dependencies."""

    def __init__(
        self,
        name: str,
        depends_on: Optional[List[str]] = None,
        **kwargs
    ):
        super().__init__(name, **kwargs)
        self.depends_on = depends_on or []

    def check_dependencies(
        self,
        flag_manager: 'FeatureFlagManager',
        context: EvaluationContext
    ) -> Tuple[bool, List[str]]:
        """Check if dependencies are enabled."""
        failed_deps = []

        for dep_key in self.depends_on:
            dep_flag = flag_manager._get_flag(dep_key)
            if not dep_flag or not dep_flag.is_active(context):
                failed_deps.append(dep_key)

        return len(failed_deps) == 0, failed_deps

class FeatureFlagManager:
    """Feature flag manager with dependency checking."""

    async def evaluate_with_dependencies(
        self,
        flag_key: str,
        context: EvaluationContext,
        default_value: Any,
        check_dependencies: bool = True
    ) -> Any:
        """Evaluate flag with dependency checking."""
        flag = self._get_flag(flag_key)
        if not flag:
            return default_value

        # Check dependencies
        if check_dependencies:
            deps_ok, failed_deps = flag.check_dependencies(self, context)
            if not deps_ok:
                logger.warning(
                    f"Flag {flag_key} dependencies not met: {failed_deps}"
                )
                return default_value

        return await self.evaluate(flag_key, context, default_value)
```

#### 2. Circular Dependency Detection

```python
class FeatureFlagManager:
    """Feature flag manager with circular dependency detection."""

    def _check_circular_dependencies(
        self,
        flag_key: str,
        visited: Optional[Set[str]] = None
    ) -> bool:
        """Check for circular dependencies."""
        if visited is None:
            visited = set()

        if flag_key in visited:
            return True  # Circular dependency detected

        visited.add(flag_key)

        flag = self._get_flag(flag_key)
        if flag:
            for dep_key in flag.depends_on:
                if self._check_circular_dependencies(dep_key, visited.copy()):
                    return True

        return False
```

---

## Lifecycle Management

### ✅ Best Practices

#### 1. Flag Lifecycle States

```python
from enum import Enum
from datetime import datetime

class FlagStatus(str, Enum):
    """Feature flag lifecycle status."""
    DRAFT = "draft"
    ACTIVE = "active"
    SCHEDULED = "scheduled"
    PAUSED = "paused"
    ARCHIVED = "archived"
    EMERGENCY_OFF = "emergency_off"

class FeatureFlag:
    """Feature flag with lifecycle management."""

    def __init__(
        self,
        name: str,
        status: FlagStatus = FlagStatus.DRAFT,
        created_at: Optional[datetime] = None,
        archived_at: Optional[datetime] = None,
        **kwargs
    ):
        super().__init__(name, **kwargs)
        self.status = status
        self.created_at = created_at or datetime.now(timezone.utc)
        self.archived_at = archived_at

    def is_active(self) -> bool:
        """Check if flag is active."""
        return self.status == FlagStatus.ACTIVE

    def archive(self) -> None:
        """Archive flag."""
        self.status = FlagStatus.ARCHIVED
        self.archived_at = datetime.now(timezone.utc)
```

#### 2. Flag Cleanup

```python
class FeatureFlagManager:
    """Feature flag manager with cleanup."""

    async def cleanup_archived_flags(
        self,
        older_than_days: int = 90
    ) -> int:
        """Clean up archived flags older than specified days."""
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=older_than_days)

        archived_flags = [
            (key, flag)
            for key, flag in self._flags.items()
            if flag.status == FlagStatus.ARCHIVED
            and flag.archived_at
            and flag.archived_at < cutoff_date
        ]

        for key, flag in archived_flags:
            del self._flags[key]
            self._cache.invalidate(key)

        return len(archived_flags)
```

---

## Security & Compliance

### ✅ Best Practices

#### 1. Access Control

```python
from enum import Enum

class FlagPermission(str, Enum):
    """Feature flag permissions."""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"

class FeatureFlagManager:
    """Feature flag manager with access control."""

    def __init__(self, permission_checker: Optional[Callable] = None):
        self._permission_checker = permission_checker

    async def evaluate(
        self,
        flag_key: str,
        context: EvaluationContext,
        default_value: Any,
        require_permission: bool = False
    ) -> Any:
        """Evaluate flag with permission checking."""
        if require_permission:
            has_permission = await self._check_permission(
                context.user_id,
                flag_key,
                FlagPermission.READ
            )
            if not has_permission:
                return default_value

        return await self._evaluate_flag(flag_key, context, default_value)
```

#### 2. Audit Logging

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class FlagAuditLog:
    """Feature flag audit log entry."""
    flag_key: str
    action: str
    user_id: str
    timestamp: datetime
    old_value: Any
    new_value: Any
    reason: Optional[str] = None

class FeatureFlagManager:
    """Feature flag manager with audit logging."""

    def __init__(self, audit_logger: Optional[Callable] = None):
        self._audit_logger = audit_logger

    async def update_flag(
        self,
        flag_key: str,
        flag: FeatureFlag,
        user_id: str,
        reason: Optional[str] = None
    ) -> None:
        """Update flag with audit logging."""
        old_flag = self._get_flag(flag_key)
        old_value = old_flag.value if old_flag else None

        self._flags[flag_key] = flag

        # Log audit event
        if self._audit_logger:
            await self._audit_logger.log(
                FlagAuditLog(
                    flag_key=flag_key,
                    action="update",
                    user_id=user_id,
                    timestamp=datetime.now(timezone.utc),
                    old_value=old_value,
                    new_value=flag.value,
                    reason=reason
                )
            )
```

---

## Monitoring & Observability

### ✅ Best Practices

#### 1. Metrics Collection

```python
from dataclasses import dataclass
from typing import Dict

@dataclass
class FlagMetrics:
    """Feature flag metrics."""
    flag_key: str
    evaluation_count: int = 0
    enabled_count: int = 0
    disabled_count: int = 0
    error_count: int = 0
    avg_evaluation_time_ms: float = 0.0

class FeatureFlagManager:
    """Feature flag manager with metrics."""

    def __init__(self):
        self._metrics: Dict[str, FlagMetrics] = {}

    async def evaluate(
        self,
        flag_key: str,
        context: EvaluationContext,
        default_value: Any
    ) -> Any:
        """Evaluate flag with metrics."""
        start_time = time.time()

        try:
            value = await self._evaluate_flag(flag_key, context, default_value)

            # Update metrics
            metrics = self._metrics.setdefault(
                flag_key,
                FlagMetrics(flag_key=flag_key)
            )
            metrics.evaluation_count += 1

            if value:
                metrics.enabled_count += 1
            else:
                metrics.disabled_count += 1

            elapsed_ms = (time.time() - start_time) * 1000
            metrics.avg_evaluation_time_ms = (
                (metrics.avg_evaluation_time_ms * (metrics.evaluation_count - 1) + elapsed_ms)
                / metrics.evaluation_count
            )

            return value

        except Exception as e:
            metrics = self._metrics.setdefault(
                flag_key,
                FlagMetrics(flag_key=flag_key)
            )
            metrics.error_count += 1
            logger.error(f"Error evaluating flag {flag_key}: {e}")
            return default_value
```

---

## FastAPI Integration

### ✅ Best Practices

#### 1. Dependency Injection

```python
from fastapi import Depends, Request
from fastapi.routing import APIRoute

def get_feature_flag_manager() -> FeatureFlagManager:
    """Dependency for feature flag manager."""
    return app.state.feature_flag_manager

def get_evaluation_context(request: Request) -> EvaluationContext:
    """Create evaluation context from request."""
    return EvaluationContext(
        user_id=request.state.user_id if hasattr(request.state, 'user_id') else None,
        group_id=request.state.group_id if hasattr(request.state, 'group_id') else None,
        environment=request.app.state.environment,
        session_id=request.cookies.get('session_id'),
        attributes={
            'ip_address': request.client.host,
            'user_agent': request.headers.get('user-agent')
        }
    )

@app.get("/api/data")
async def get_data(
    flag_manager: FeatureFlagManager = Depends(get_feature_flag_manager),
    context: EvaluationContext = Depends(get_evaluation_context)
):
    """Endpoint with feature flag."""
    if await flag_manager.is_enabled("new-api", context):
        # Use new API
        return {"data": "new"}
    else:
        # Use old API
        return {"data": "old"}
```

#### 2. Middleware Integration

```python
from starlette.middleware.base import BaseHTTPMiddleware

class FeatureFlagMiddleware(BaseHTTPMiddleware):
    """Middleware for feature flag evaluation."""

    def __init__(self, app, flag_manager: FeatureFlagManager):
        super().__init__(app)
        self._flag_manager = flag_manager

    async def dispatch(self, request: Request, call_next):
        """Add feature flags to request state."""
        context = EvaluationContext(
            user_id=getattr(request.state, 'user_id', None),
            environment=request.app.state.environment
        )

        # Evaluate flags and add to request state
        request.state.feature_flags = await self._flag_manager.evaluate_all(
            ["feature_a", "feature_b"],
            context
        )

        response = await call_next(request)
        return response
```

---

## Summary Checklist

### Architecture
- [ ] Separation of concerns (provider, manager, cache)
- [ ] Vendor-agnostic API (OpenFeature)
- [ ] Context-based evaluation
- [ ] Safe defaults

### Flag Types
- [ ] Boolean flags
- [ ] Percentage rollout flags
- [ ] Variant flags (A/B testing)
- [ ] String/Numeric flags
- [ ] JSON/Complex flags

### Evaluation
- [ ] Context-based evaluation
- [ ] Default value strategy
- [ ] Bulk evaluation
- [ ] Error handling

### Targeting & Rollout
- [ ] User targeting
- [ ] Group targeting
- [ ] Attribute-based targeting
- [ ] Gradual rollout
- [ ] Scheduled rollout

### Performance
- [ ] Multi-level caching
- [ ] Cache invalidation
- [ ] Lazy evaluation
- [ ] Preloading

### Dependencies
- [ ] Flag dependencies
- [ ] Circular dependency detection
- [ ] Dependency resolution

### Lifecycle
- [ ] Flag lifecycle states
- [ ] Flag cleanup
- [ ] Archival process

### Security
- [ ] Access control
- [ ] Audit logging
- [ ] Permission checking

### Monitoring
- [ ] Metrics collection
- [ ] Evaluation tracking
- [ ] Performance monitoring

---

## References

- [OpenFeature Specification](https://openfeature.dev/)
- [GO Feature Flag Documentation](https://gofeatureflag.org/)
- [Feature Flags Best Practices](https://featureflags.io/)

---

**Note:** This document is based on OpenFeature specification latest, Python 3.9+, and industry best practices. Always refer to official documentation for the most up-to-date information.
