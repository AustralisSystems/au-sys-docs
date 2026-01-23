# Observability & Monitoring: Prometheus, Grafana, Distributed Tracing & structlog Best Practices

**Version**: v1.0.0
**Last Updated**: 2025-01-14

This document provides comprehensive best practices for implementing observability and monitoring in FastAPI applications, covering Prometheus metrics, Grafana dashboards, distributed tracing with OpenTelemetry, and structured logging with structlog.

---

## Table of Contents

1. [Architecture Principles](#architecture-principles)
2. [Prometheus Metrics Collection](#prometheus-metrics-collection)
3. [Grafana Dashboards & Visualization](#grafana-dashboards--visualization)
4. [Distributed Tracing with OpenTelemetry](#distributed-tracing-with-opentelemetry)
5. [Structured Logging with structlog](#structured-logging-with-structlog)
6. [FastAPI Integration](#fastapi-integration)
7. [Correlation: Metrics, Logs & Traces](#correlation-metrics-logs--traces)
8. [Performance Considerations](#performance-considerations)
9. [Production Deployment](#production-deployment)

---

## Architecture Principles

### Three Pillars of Observability

Observability consists of three complementary pillars:

1. **Metrics**: Quantitative measurements over time (Prometheus)
2. **Logs**: Discrete events with context (structlog → Loki)
3. **Traces**: Request flows across services (OpenTelemetry → Tempo)

### Unified Observability Stack

**RECOMMENDED**: Integrate all three pillars for comprehensive visibility:

```python
# Unified observability architecture
Observability Stack:
├── Metrics (Prometheus)
│   ├── Application metrics
│   ├── Infrastructure metrics
│   └── Business metrics
├── Logs (structlog → Loki)
│   ├── Structured JSON logs
│   ├── Correlation IDs
│   └── Context-aware logging
└── Traces (OpenTelemetry → Tempo)
    ├── Distributed tracing
    ├── Span correlation
    └── Performance analysis
```

### Defense in Depth

**MANDATORY**: Implement multiple layers of monitoring:

- **Application Layer**: Business logic metrics and traces
- **Framework Layer**: HTTP request/response metrics
- **Infrastructure Layer**: System resource metrics
- **Network Layer**: Service-to-service communication traces

### Zero Trust Observability

**REQUIRED**: Secure observability systems:

- Authenticate all data sources
- Encrypt data in transit
- Control access to dashboards
- Audit monitoring system access

---

## Prometheus Metrics Collection

### Core Principles

#### 1. Metric Types

**MANDATORY**: Use appropriate metric types:

```python
from prometheus_client import Counter, Gauge, Histogram, Summary, start_http_server

# Counter: Monotonically increasing value
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status_code']
)

# Gauge: Value that can go up or down
active_connections = Gauge(
    'active_connections',
    'Number of active connections',
    ['service']
)

# Histogram: Distribution of values (buckets)
http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint'],
    buckets=[0.1, 0.5, 1.0, 2.5, 5.0, 10.0]
)

# Summary: Similar to histogram but with quantiles
request_size_bytes = Summary(
    'request_size_bytes',
    'Request size in bytes',
    ['method', 'endpoint'],
    quantiles=[0.5, 0.9, 0.99]
)
```

#### 2. RED Metrics Pattern

**RECOMMENDED**: Track Rate, Errors, Duration for all services:

```python
from prometheus_client import Counter, Histogram
from typing import Dict

class REDMetrics:
    """RED metrics: Rate, Errors, Duration."""

    def __init__(self, service_name: str):
        self.service_name = service_name

        # Rate: Requests per second
        self.request_count = Counter(
            f'{service_name}_requests_total',
            'Total requests',
            ['method', 'endpoint', 'status_code']
        )

        # Errors: Error rate
        self.error_count = Counter(
            f'{service_name}_errors_total',
            'Total errors',
            ['method', 'endpoint', 'error_type']
        )

        # Duration: Request latency
        self.request_duration = Histogram(
            f'{service_name}_request_duration_seconds',
            'Request duration',
            ['method', 'endpoint'],
            buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.5, 5.0]
        )

    def record_request(
        self,
        method: str,
        endpoint: str,
        status_code: int,
        duration: float,
        error: Exception = None
    ):
        """Record request metrics."""
        # Rate
        self.request_count.labels(
            method=method,
            endpoint=endpoint,
            status_code=status_code
        ).inc()

        # Errors
        if error or status_code >= 400:
            error_type = type(error).__name__ if error else f"HTTP_{status_code}"
            self.error_count.labels(
                method=method,
                endpoint=endpoint,
                error_type=error_type
            ).inc()

        # Duration
        self.request_duration.labels(
            method=method,
            endpoint=endpoint
        ).observe(duration)
```

#### 3. USE Metrics Pattern

**RECOMMENDED**: Track Utilization, Saturation, Errors for resources:

```python
from prometheus_client import Gauge, Counter

class USEMetrics:
    """USE metrics: Utilization, Saturation, Errors."""

    def __init__(self, resource_name: str):
        self.resource_name = resource_name

        # Utilization: Percentage of resource in use
        self.utilization = Gauge(
            f'{resource_name}_utilization_percent',
            'Resource utilization percentage',
            ['resource_type']
        )

        # Saturation: Queue length or wait time
        self.saturation = Gauge(
            f'{resource_name}_saturation',
            'Resource saturation',
            ['resource_type']
        )

        # Errors: Error count
        self.errors = Counter(
            f'{resource_name}_errors_total',
            'Resource errors',
            ['resource_type', 'error_type']
        )

    def record_utilization(self, resource_type: str, percent: float):
        """Record resource utilization."""
        self.utilization.labels(resource_type=resource_type).set(percent)

    def record_saturation(self, resource_type: str, value: float):
        """Record resource saturation."""
        self.saturation.labels(resource_type=resource_type).set(value)

    def record_error(self, resource_type: str, error_type: str):
        """Record resource error."""
        self.errors.labels(
            resource_type=resource_type,
            error_type=error_type
        ).inc()
```

### Labeling Best Practices

#### 1. Consistent Label Names

**MANDATORY**: Use consistent label naming conventions:

```python
# GOOD: Consistent label names
http_requests_total.labels(
    method='GET',
    endpoint='/api/users',
    status_code='200'
).inc()

# BAD: Inconsistent label names
http_requests_total.labels(
    http_method='GET',  # Should be 'method'
    path='/api/users',  # Should be 'endpoint'
    code='200'  # Should be 'status_code'
).inc()
```

#### 2. Cardinality Management

**CRITICAL**: Control label cardinality to prevent metric explosion:

```python
# GOOD: Low cardinality labels
http_requests_total.labels(
    method='GET',  # 5-10 values
    endpoint='/api/users',  # 50-100 values
    status_code='200'  # 10-20 values
).inc()

# BAD: High cardinality labels
http_requests_total.labels(
    user_id='user_12345',  # Thousands of values
    request_id='req_abc123',  # Unique per request
    ip_address='192.168.1.1'  # Many unique values
).inc()
```

#### 3. Label Value Sanitization

**REQUIRED**: Sanitize label values to prevent issues:

```python
import re
from prometheus_client import Counter

def sanitize_label_value(value: str) -> str:
    """Sanitize label value for Prometheus."""
    # Remove invalid characters
    sanitized = re.sub(r'[^a-zA-Z0-9_:]', '_', str(value))
    # Limit length
    return sanitized[:100]

# Usage
http_requests_total.labels(
    method=sanitize_label_value(request.method),
    endpoint=sanitize_label_value(request.url.path),
    status_code=str(response.status_code)
).inc()
```

### FastAPI Integration

#### 1. Metrics Middleware

**RECOMMENDED**: Create reusable metrics middleware:

```python
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import Counter, Histogram, generate_latest
from prometheus_client.openmetrics.exposition import CONTENT_TYPE_LATEST
from starlette.responses import Response
import time

# Metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status_code']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.5, 5.0, 10.0]
)

class PrometheusMiddleware(BaseHTTPMiddleware):
    """Middleware for Prometheus metrics collection."""

    async def dispatch(self, request: Request, call_next):
        """Process request and collect metrics."""
        start_time = time.time()

        # Process request
        response = await call_next(request)

        # Calculate duration
        duration = time.time() - start_time

        # Extract endpoint (normalize to reduce cardinality)
        endpoint = self._normalize_endpoint(request.url.path)

        # Record metrics
        http_requests_total.labels(
            method=request.method,
            endpoint=endpoint,
            status_code=response.status_code
        ).inc()

        http_request_duration_seconds.labels(
            method=request.method,
            endpoint=endpoint
        ).observe(duration)

        return response

    def _normalize_endpoint(self, path: str) -> str:
        """Normalize endpoint to reduce cardinality."""
        # Replace UUIDs and IDs with placeholders
        import re
        normalized = re.sub(r'/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', '/{uuid}', path)
        normalized = re.sub(r'/\d+', '/{id}', normalized)
        return normalized

# FastAPI app setup
app = FastAPI()

# Add middleware
app.add_middleware(PrometheusMiddleware)

# Metrics endpoint
@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )
```

#### 2. Custom Metrics

**RECOMMENDED**: Add application-specific metrics:

```python
from prometheus_client import Counter, Gauge, Histogram

# Business metrics
orders_created_total = Counter(
    'orders_created_total',
    'Total orders created',
    ['status', 'payment_method']
)

order_value_dollars = Histogram(
    'order_value_dollars',
    'Order value distribution',
    ['status'],
    buckets=[10, 50, 100, 500, 1000, 5000]
)

# Application metrics
cache_hits_total = Counter(
    'cache_hits_total',
    'Total cache hits',
    ['cache_type']
)

cache_size_bytes = Gauge(
    'cache_size_bytes',
    'Cache size in bytes',
    ['cache_type']
)

# Database metrics
db_query_duration_seconds = Histogram(
    'db_query_duration_seconds',
    'Database query duration',
    ['query_type', 'table'],
    buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0]
)
```

#### 3. Process Metrics

**RECOMMENDED**: Collect process and platform metrics:

```python
from prometheus_client import (
    start_http_server,
    ProcessCollector,
    PlatformCollector,
    GCCollector,
    CollectorRegistry
)

def setup_process_metrics(namespace: str = "app"):
    """Setup process and platform metrics."""
    registry = CollectorRegistry()

    # Process metrics (CPU, memory, file descriptors)
    ProcessCollector(namespace=namespace, registry=registry)

    # Platform metrics (Python version, platform info)
    PlatformCollector(registry=registry)

    # Garbage collection metrics
    GCCollector(registry=registry)

    return registry
```

### Prometheus Configuration

#### 1. Scrape Configuration

**REQUIRED**: Configure Prometheus to scrape your application:

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'production'
    environment: 'prod'

scrape_configs:
  - job_name: 'fastapi-app'
    static_configs:
      - targets: ['app:8000']
        labels:
          service: 'api'
          version: '1.0.0'
    metrics_path: '/metrics'
    scrape_interval: 10s
    scrape_timeout: 5s

  - job_name: 'fastapi-app-process'
    static_configs:
      - targets: ['app:8000']
    metrics_path: '/metrics'
    params:
      format: ['prometheus']
```

#### 2. Recording Rules

**RECOMMENDED**: Create recording rules for common queries:

```yaml
# recording_rules.yml
groups:
  - name: http_rules
    interval: 30s
    rules:
      - record: http:requests:rate5m
        expr: rate(http_requests_total[5m])

      - record: http:errors:rate5m
        expr: rate(http_requests_total{status_code=~"5.."}[5m])

      - record: http:latency:p99
        expr: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))
```

#### 3. Alerting Rules

**REQUIRED**: Define alerting rules for critical issues:

```yaml
# alerting_rules.yml
groups:
  - name: http_alerts
    interval: 30s
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status_code=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} errors/second"

      - alert: HighLatency
        expr: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 1.0
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High latency detected"
          description: "P99 latency is {{ $value }} seconds"
```

---

## Grafana Dashboards & Visualization

### Dashboard Design Principles

#### 1. Dashboard Hierarchy

**RECOMMENDED**: Organize dashboards by level:

```
Dashboard Hierarchy:
├── Infrastructure (System-level)
│   ├── CPU, Memory, Disk
│   ├── Network I/O
│   └── Container metrics
├── Application (Service-level)
│   ├── Request rates
│   ├── Error rates
│   ├── Latency (p50, p95, p99)
│   └── Business metrics
└── Business (Domain-level)
    ├── User activity
    ├── Revenue metrics
    └── Feature adoption
```

#### 2. Panel Organization

**REQUIRED**: Follow consistent panel layout:

```json
{
  "dashboard": {
    "title": "FastAPI Application Metrics",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{endpoint}}"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0}
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total{status_code=~\"5..\"}[5m])",
            "legendFormat": "{{method}} {{endpoint}}"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0}
      },
      {
        "title": "Latency (P99)",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "{{method}} {{endpoint}}"
          }
        ],
        "gridPos": {"h": 8, "w": 24, "x": 0, "y": 8}
      }
    ]
  }
}
```

### Data Source Configuration

#### 1. Prometheus Data Source

**REQUIRED**: Configure Prometheus data source:

```yaml
# grafana/datasources/prometheus.yml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    jsonData:
      httpMethod: POST
      manageAlerts: true
      prometheusType: Prometheus
      prometheusVersion: 2.40.0
      timeInterval: 10s
      cacheLevel: 'High'
      exemplarTraceIdDestinations:
        - datasourceUid: tempo
          name: traceID
```

#### 2. Tempo Data Source (Tracing)

**RECOMMENDED**: Configure Tempo for distributed tracing:

```yaml
# grafana/datasources/tempo.yml
apiVersion: 1

datasources:
  - name: Tempo
    type: tempo
    access: proxy
    url: http://tempo:3200
    jsonData:
      httpMethod: GET
      tracesToLogs:
        datasourceUid: loki
        tags: ['job', 'instance', 'pod', 'namespace']
        mappedTags: [{ key: 'service.name', value: 'service' }]
        mapTagNamesEnabled: false
        spanStartTimeShift: '1h'
        spanEndTimeShift: '1h'
        filterByTraceID: false
        filterBySpanID: false
      tracesToMetrics:
        datasourceUid: prometheus
        tags: [{ key: 'service.name', value: 'service' }, { key: 'job' }]
        queries:
          - name: 'Sample query'
            query: 'sum(rate(tempo_spanmetrics_latency_bucket{$$__tags}[5m]))'
      serviceMap:
        datasourceUid: prometheus
      nodeGraph:
        enabled: true
      search:
        hide: false
      lokiSearch:
        datasourceUid: loki
```

#### 3. Loki Data Source (Logs)

**RECOMMENDED**: Configure Loki for log aggregation:

```yaml
# grafana/datasources/loki.yml
apiVersion: 1

datasources:
  - name: Loki
    type: loki
    access: proxy
    url: http://loki:3100
    jsonData:
      httpMethod: POST
      maxLines: 1000
      derivedFields:
        - datasourceUid: tempo
          matcherRegex: 'trace_id=(\w+)'
          name: TraceID
          url: '$${__value.raw}'
```

### Dashboard Provisioning

#### 1. Dashboard Configuration

**RECOMMENDED**: Provision dashboards as code:

```yaml
# grafana/dashboards/dashboard.yml
apiVersion: 1

providers:
  - name: 'default'
    orgId: 1
    folder: 'FastAPI'
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /etc/grafana/provisioning/dashboards
      foldersFromFilesStructure: true
```

#### 2. Dashboard JSON

**REQUIRED**: Create comprehensive dashboard JSON:

```json
{
  "dashboard": {
    "title": "FastAPI Application Overview",
    "tags": ["fastapi", "application"],
    "timezone": "browser",
    "schemaVersion": 38,
    "version": 1,
    "refresh": "10s",
    "panels": [
      {
        "id": 1,
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total[5m])) by (method, endpoint)",
            "legendFormat": "{{method}} {{endpoint}}",
            "refId": "A"
          }
        ],
        "yaxes": [
          {"format": "reqps", "label": "Requests/sec"},
          {"format": "short"}
        ],
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0}
      },
      {
        "id": 2,
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{status_code=~\"5..\"}[5m])) by (method, endpoint)",
            "legendFormat": "{{method}} {{endpoint}}",
            "refId": "A"
          }
        ],
        "yaxes": [
          {"format": "reqps", "label": "Errors/sec"},
          {"format": "short"}
        ],
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0}
      },
      {
        "id": 3,
        "title": "Latency Percentiles",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, method, endpoint))",
            "legendFormat": "P50 {{method}} {{endpoint}}",
            "refId": "A"
          },
          {
            "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, method, endpoint))",
            "legendFormat": "P95 {{method}} {{endpoint}}",
            "refId": "B"
          },
          {
            "expr": "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, method, endpoint))",
            "legendFormat": "P99 {{method}} {{endpoint}}",
            "refId": "C"
          }
        ],
        "yaxes": [
          {"format": "s", "label": "Latency"},
          {"format": "short"}
        ],
        "gridPos": {"h": 8, "w": 24, "x": 0, "y": 8}
      }
    ]
  }
}
```

### Alerting Configuration

#### 1. Alert Rules

**REQUIRED**: Configure Grafana alert rules:

```yaml
# grafana/alerts/rules.yml
apiVersion: 1

groups:
  - name: fastapi_alerts
    interval: 30s
    orgId: 1
    folder: 'FastAPI Alerts'
    rules:
      - uid: high_error_rate
        title: High Error Rate
        condition: A
        data:
          - refId: A
            relativeTimeRange:
              from: 300
              to: 0
            datasourceUid: prometheus
            model:
              expr: 'sum(rate(http_requests_total{status_code=~"5.."}[5m])) > 0.05'
              refId: A
        noDataState: NoData
        execErrState: Alerting
        for: 5m
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} errors/second"
        labels:
          severity: critical
          team: platform
```

#### 2. Notification Channels

**REQUIRED**: Configure notification channels:

```yaml
# grafana/notifiers/slack.yml
notifiers:
  - name: slack_alerts
    type: slack
    uid: slack_01
    org_id: 1
    is_default: false
    settings:
      url: 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'
      username: Grafana
      channel: '#alerts'
      title: '{{ .CommonAnnotations.summary }}'
      text: '{{ .CommonAnnotations.description }}'
      iconEmoji: ':warning:'
```

---

## Distributed Tracing with OpenTelemetry

### Core Concepts

#### 1. Trace, Span, Context

**REQUIRED**: Understand OpenTelemetry concepts:

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

# Initialize tracing
resource = Resource.create({
    "service.name": "fastapi-app",
    "service.version": "1.0.0",
    "deployment.environment": "production"
})

trace.set_tracer_provider(TracerProvider(resource=resource))

# Add span processor
span_processor = BatchSpanProcessor(
    OTLPSpanExporter(endpoint="http://tempo:4317")
)
trace.get_tracer_provider().add_span_processor(span_processor)

# Get tracer
tracer = trace.get_tracer(__name__)
```

#### 2. Span Creation

**MANDATORY**: Create spans for operations:

```python
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

tracer = trace.get_tracer(__name__)

# Basic span
with tracer.start_as_current_span("operation_name") as span:
    span.set_attribute("key", "value")
    # Your code here
    span.set_status(Status(StatusCode.OK))

# Span with error handling
with tracer.start_as_current_span("risky_operation") as span:
    try:
        result = risky_function()
        span.set_status(Status(StatusCode.OK))
        span.set_attribute("result", result)
    except Exception as e:
        span.set_status(Status(StatusCode.ERROR, str(e)))
        span.record_exception(e)
        raise
```

### FastAPI Instrumentation

#### 1. Automatic Instrumentation

**RECOMMENDED**: Use automatic instrumentation:

```python
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from fastapi import FastAPI

app = FastAPI()

# Instrument FastAPI
FastAPIInstrumentor.instrument_app(app)

# Instrument HTTP client
HTTPXClientInstrumentor.instrument()

# Instrument SQLAlchemy
SQLAlchemyInstrumentor.instrument()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

#### 2. Manual Instrumentation

**REQUIRED**: Add manual spans for business logic:

```python
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from fastapi import FastAPI, Depends

tracer = trace.get_tracer(__name__)
app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """Get user with tracing."""
    with tracer.start_as_current_span("get_user") as span:
        span.set_attribute("user.id", user_id)

        # Database query span
        with tracer.start_as_current_span("db.query") as db_span:
            db_span.set_attribute("db.statement", "SELECT * FROM users WHERE id = ?")
            db_span.set_attribute("db.operation", "SELECT")
            user = await db.get_user(user_id)
            db_span.set_status(Status(StatusCode.OK))

        # External API call span
        with tracer.start_as_current_span("external_api.call") as api_span:
            api_span.set_attribute("http.method", "GET")
            api_span.set_attribute("http.url", "https://api.example.com/data")
            response = await httpx.get("https://api.example.com/data")
            api_span.set_attribute("http.status_code", response.status_code)
            api_span.set_status(Status(StatusCode.OK))

        span.set_status(Status(StatusCode.OK))
        return {"user": user}
```

### Trace Context Propagation

#### 1. HTTP Propagation

**MANDATORY**: Propagate trace context across HTTP calls:

```python
from opentelemetry import trace
from opentelemetry.propagate import inject, extract
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
import httpx

tracer = trace.get_tracer(__name__)

async def call_external_api(url: str):
    """Call external API with trace context propagation."""
    with tracer.start_as_current_span("external_api.call") as span:
        span.set_attribute("http.method", "GET")
        span.set_attribute("http.url", url)

        # Inject trace context into headers
        headers = {}
        inject(headers)

        # Make HTTP request with trace context
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

            span.set_attribute("http.status_code", response.status_code)
            span.set_status(Status(StatusCode.OK))

            return response.json()
```

#### 2. Async Context Propagation

**REQUIRED**: Ensure context propagation in async code:

```python
import asyncio
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

tracer = trace.get_tracer(__name__)

async def process_items(items: list):
    """Process items with trace context propagation."""
    with tracer.start_as_current_span("process_items") as parent_span:
        parent_span.set_attribute("items.count", len(items))

        # Context is automatically propagated to child tasks
        tasks = [
            process_item(item) for item in items
        ]

        results = await asyncio.gather(*tasks)

        parent_span.set_status(Status(StatusCode.OK))
        return results

async def process_item(item: dict):
    """Process single item (child span)."""
    with tracer.start_as_current_span("process_item") as span:
        span.set_attribute("item.id", item.get("id"))
        # Process item
        result = await do_work(item)
        span.set_status(Status(StatusCode.OK))
        return result
```

### Sampling Strategies

#### 1. Head-Based Sampling

**RECOMMENDED**: Use head-based sampling:

```python
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased

# Sample 10% of traces
sampler = TraceIdRatioBased(0.1)

tracer_provider = TracerProvider(
    resource=resource,
    sampler=sampler
)
```

#### 2. Tail-Based Sampling

**ADVANCED**: Implement tail-based sampling:

```python
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.sampling import Decision

class TailSampler:
    """Tail-based sampler that samples based on span attributes."""

    def should_sample(self, context, trace_id, name, attributes, links):
        """Sample traces with errors or high latency."""
        # Sample all errors
        if attributes.get("error", False):
            return Decision.RECORD_AND_SAMPLE

        # Sample slow operations
        if attributes.get("duration_ms", 0) > 1000:
            return Decision.RECORD_AND_SAMPLE

        # Sample 1% of others
        if trace_id % 100 == 0:
            return Decision.RECORD_AND_SAMPLE

        return Decision.DROP

tracer_provider = TracerProvider(
    resource=resource,
    sampler=TailSampler()
)
```

---

## Structured Logging with structlog

### Core Principles

#### 1. Structured Output

**MANDATORY**: Use structured logging for machine readability:

```python
import structlog
import sys

# Configure structlog for JSON output
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.dict_tracebacks,
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    context_class=dict,
    logger_factory=structlog.WriteLoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()
```

#### 2. Context Variables

**REQUIRED**: Use context variables for request-scoped logging:

```python
from structlog.contextvars import (
    bind_contextvars,
    clear_contextvars,
    merge_contextvars,
)

# At request start
def setup_request_context(request_id: str, user_id: str):
    """Setup request context for logging."""
    clear_contextvars()
    bind_contextvars(
        request_id=request_id,
        user_id=user_id,
        service="fastapi-app"
    )

# In request handler
logger.info("Processing request", endpoint="/api/users", method="GET")

# Output includes request_id and user_id automatically
# {"event": "Processing request", "request_id": "req_123", "user_id": "user_456", ...}
```

#### 3. Conditional Formatting

**RECOMMENDED**: Use different formats for dev vs production:

```python
import sys
import structlog

# Shared processors
shared_processors = [
    structlog.contextvars.merge_contextvars,
    structlog.processors.add_log_level,
    structlog.processors.TimeStamper(fmt="iso"),
]

# Conditional processors based on environment
if sys.stderr.isatty():
    # Development: Pretty console output
    processors = shared_processors + [
        structlog.dev.ConsoleRenderer(colors=True),
    ]
else:
    # Production: JSON output
    processors = shared_processors + [
        structlog.processors.dict_tracebacks,
        structlog.processors.JSONRenderer(),
    ]

structlog.configure(
    processors=processors,
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    context_class=dict,
    logger_factory=structlog.WriteLoggerFactory(),
    cache_logger_on_first_use=True,
)
```

### FastAPI Integration

#### 1. Request Logging Middleware

**REQUIRED**: Log all requests with context:

```python
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from structlog.contextvars import bind_contextvars, clear_contextvars
from structlog import get_logger
import time
import uuid

logger = get_logger()

class StructlogMiddleware(BaseHTTPMiddleware):
    """Middleware for structured request logging."""

    async def dispatch(self, request: Request, call_next):
        """Process request with structured logging."""
        # Generate request ID
        request_id = str(uuid.uuid4())

        # Clear and bind context
        clear_contextvars()
        bind_contextvars(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            client_ip=request.client.host if request.client else None,
        )

        start_time = time.time()

        try:
            response = await call_next(request)
            duration_ms = (time.time() - start_time) * 1000

            # Log request completion
            logger.info(
                "request_completed",
                status_code=response.status_code,
                duration_ms=duration_ms,
            )

            return response

        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000

            # Log error
            logger.error(
                "request_failed",
                error_type=type(e).__name__,
                error_message=str(e),
                duration_ms=duration_ms,
                exc_info=True,
            )
            raise

app = FastAPI()
app.add_middleware(StructlogMiddleware)
```

#### 2. Correlation IDs

**MANDATORY**: Use correlation IDs for request tracing:

```python
import contextvars
from structlog.contextvars import bind_contextvars, clear_contextvars
from structlog import get_logger
from uuid import uuid4

# Context variable for correlation ID
correlation_id_var: contextvars.ContextVar[str] = contextvars.ContextVar(
    "correlation_id", default=""
)

def get_correlation_id() -> str:
    """Get current correlation ID."""
    return correlation_id_var.get("")

def set_correlation_id(cid: str) -> None:
    """Set correlation ID."""
    correlation_id_var.set(cid)

class CorrelationProcessor:
    """Processor to add correlation ID to logs."""

    def __call__(self, logger, method_name, event_dict):
        """Add correlation ID to event dict."""
        cid = get_correlation_id()
        if cid:
            event_dict["correlation_id"] = cid
        return event_dict

# Configure structlog with correlation processor
structlog.configure(
    processors=[
        CorrelationProcessor(),
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    # ... other config
)
```

#### 3. Exception Logging

**REQUIRED**: Log exceptions with full context:

```python
from structlog import get_logger
from structlog.processors import dict_tracebacks

logger = get_logger()

try:
    risky_operation()
except Exception as e:
    logger.error(
        "operation_failed",
        operation="risky_operation",
        error_type=type(e).__name__,
        error_message=str(e),
        exc_info=True,  # Include full traceback
    )
```

### Integration with Observability Stack

#### 1. Log → Trace Correlation

**RECOMMENDED**: Correlate logs with traces:

```python
from opentelemetry import trace
from structlog import get_logger

tracer = trace.get_tracer(__name__)
logger = get_logger()

def operation_with_trace():
    """Operation with trace and log correlation."""
    span = trace.get_current_span()
    trace_id = format(span.get_span_context().trace_id, '032x')
    span_id = format(span.get_span_context().span_id, '016x')

    # Include trace context in logs
    logger.info(
        "operation_started",
        trace_id=trace_id,
        span_id=span_id,
        operation="process_data",
    )

    # Your code here

    logger.info(
        "operation_completed",
        trace_id=trace_id,
        span_id=span_id,
        operation="process_data",
    )
```

#### 2. Log → Metrics Correlation

**RECOMMENDED**: Extract metrics from logs:

```python
from prometheus_client import Counter
from structlog import get_logger

error_counter = Counter('log_errors_total', 'Errors from logs', ['error_type'])
logger = get_logger()

def log_and_metric_error(error: Exception):
    """Log error and increment metric."""
    error_type = type(error).__name__

    # Log error
    logger.error(
        "error_occurred",
        error_type=error_type,
        error_message=str(error),
        exc_info=True,
    )

    # Increment metric
    error_counter.labels(error_type=error_type).inc()
```

---

## FastAPI Integration

### Complete Observability Setup

#### 1. Unified Observability Middleware

**RECOMMENDED**: Combine metrics, tracing, and logging:

```python
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import Counter, Histogram
from opentelemetry import trace
from structlog import get_logger
from structlog.contextvars import bind_contextvars, clear_contextvars
import time
import uuid

# Metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status_code']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

# Tracer
tracer = trace.get_tracer(__name__)

# Logger
logger = get_logger()

class ObservabilityMiddleware(BaseHTTPMiddleware):
    """Unified observability middleware."""

    async def dispatch(self, request: Request, call_next):
        """Process request with full observability."""
        # Generate request ID
        request_id = str(uuid.uuid4())

        # Start trace
        span = tracer.start_span(
            name=f"{request.method} {request.url.path}",
            kind=trace.SpanKind.SERVER,
        )

        # Set trace attributes
        span.set_attribute("http.method", request.method)
        span.set_attribute("http.url", str(request.url))
        span.set_attribute("http.route", request.url.path)

        # Setup logging context
        clear_contextvars()
        bind_contextvars(
            request_id=request_id,
            trace_id=format(span.get_span_context().trace_id, '032x'),
            span_id=format(span.get_span_context().span_id, '016x'),
            method=request.method,
            path=request.url.path,
        )

        start_time = time.time()

        try:
            # Process request
            response = await call_next(request)
            duration = time.time() - start_time

            # Record metrics
            http_requests_total.labels(
                method=request.method,
                endpoint=request.url.path,
                status_code=response.status_code
            ).inc()

            http_request_duration_seconds.labels(
                method=request.method,
                endpoint=request.url.path
            ).observe(duration)

            # Update trace
            span.set_attribute("http.status_code", response.status_code)
            span.set_attribute("http.duration_ms", duration * 1000)
            span.set_status(trace.Status(trace.StatusCode.OK))

            # Log success
            logger.info(
                "request_completed",
                status_code=response.status_code,
                duration_ms=duration * 1000,
            )

            return response

        except Exception as e:
            duration = time.time() - start_time

            # Record error metrics
            http_requests_total.labels(
                method=request.method,
                endpoint=request.url.path,
                status_code=500
            ).inc()

            # Update trace
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
            span.record_exception(e)

            # Log error
            logger.error(
                "request_failed",
                error_type=type(e).__name__,
                error_message=str(e),
                duration_ms=duration * 1000,
                exc_info=True,
            )

            raise

        finally:
            span.end()

app = FastAPI()
app.add_middleware(ObservabilityMiddleware)
```

#### 2. Metrics Endpoint

**REQUIRED**: Expose Prometheus metrics:

```python
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )
```

#### 3. Health Check with Metrics

**RECOMMENDED**: Include metrics in health check:

```python
from prometheus_client import Gauge
from fastapi import FastAPI

health_status = Gauge('app_health', 'Application health status', ['component'])

@app.get("/health")
async def health():
    """Health check endpoint."""
    # Check components
    db_healthy = await check_database()
    redis_healthy = await check_redis()

    # Update metrics
    health_status.labels(component='database').set(1 if db_healthy else 0)
    health_status.labels(component='redis').set(1 if redis_healthy else 0)

    if db_healthy and redis_healthy:
        return {"status": "healthy"}
    else:
        return {"status": "unhealthy"}, 503
```

---

## Correlation: Metrics, Logs & Traces

### Trace Context in Logs

**REQUIRED**: Include trace context in logs:

```python
from opentelemetry import trace
from structlog import get_logger

tracer = trace.get_tracer(__name__)
logger = get_logger()

def operation_with_correlation():
    """Operation with trace-log correlation."""
    span = trace.get_current_span()

    if span:
        trace_id = format(span.get_span_context().trace_id, '032x')
        span_id = format(span.get_span_context().span_id, '016x')

        logger.info(
            "operation_started",
            trace_id=trace_id,
            span_id=span_id,
        )
```

### Exemplars in Metrics

**RECOMMENDED**: Add trace IDs as exemplars:

```python
from prometheus_client import Histogram
from opentelemetry import trace

http_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

def record_request_duration(method: str, endpoint: str, duration: float):
    """Record request duration with exemplar."""
    span = trace.get_current_span()

    exemplar = {}
    if span:
        trace_id = format(span.get_span_context().trace_id, '032x')
        exemplar['trace_id'] = trace_id

    http_duration.labels(
        method=method,
        endpoint=endpoint
    ).observe(duration, exemplar=exemplar)
```

### Grafana Correlation

**RECOMMENDED**: Configure Grafana for correlation:

```yaml
# grafana/datasources/prometheus.yml
datasources:
  - name: Prometheus
    jsonData:
      exemplarTraceIdDestinations:
        - datasourceUid: tempo
          name: traceID
```

---

## Performance Considerations

### Efficient Metric Collection

#### 1. Metric Cardinality

**CRITICAL**: Control metric cardinality:

```python
# GOOD: Low cardinality
http_requests_total.labels(
    method='GET',  # 5-10 values
    endpoint='/api/users',  # Normalized paths
    status_code='200'  # 10-20 values
).inc()

# BAD: High cardinality
http_requests_total.labels(
    user_id='user_12345',  # Thousands of values
    request_id='req_abc123',  # Unique per request
).inc()
```

#### 2. Sampling for Traces

**REQUIRED**: Implement sampling to reduce overhead:

```python
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased

# Sample 10% of traces
sampler = TraceIdRatioBased(0.1)

tracer_provider = TracerProvider(
    resource=resource,
    sampler=sampler
)
```

### Async Logging

**RECOMMENDED**: Use async logging for high-throughput:

```python
import asyncio
from structlog import get_logger
from structlog.processors import JSONRenderer

logger = get_logger()

async def async_log_operation():
    """Async operation with logging."""
    # Logging is non-blocking
    logger.info("async_operation_started")

    # Do async work
    result = await do_async_work()

    logger.info("async_operation_completed", result=result)
```

---

## Production Deployment

### Docker Compose Setup

**REQUIRED**: Configure observability stack:

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Application
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OTEL_EXPORTER_OTLP_ENDPOINT=http://tempo:4317
      - OTEL_SERVICE_NAME=fastapi-app
    depends_on:
      - prometheus
      - tempo
      - loki

  # Prometheus
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'

  # Grafana
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana:/etc/grafana/provisioning
    depends_on:
      - prometheus
      - tempo
      - loki

  # Tempo (Tracing)
  tempo:
    image: grafana/tempo:latest
    ports:
      - "4317:4317"  # OTLP gRPC
      - "3200:3200"  # Tempo API
    volumes:
      - tempo_data:/var/tempo
    command: ["-config.file=/etc/tempo.yaml"]

  # Loki (Logs)
  loki:
    image: grafana/loki:latest
    ports:
      - "3100:3100"
    volumes:
      - ./monitoring/loki.yml:/etc/loki/local-config.yaml
      - loki_data:/loki

volumes:
  prometheus_data:
  grafana_data:
  tempo_data:
  loki_data:
```

### Environment Configuration

**REQUIRED**: Configure via environment variables:

```python
from pydantic_settings import BaseSettings

class ObservabilitySettings(BaseSettings):
    """Observability configuration."""

    # Prometheus
    prometheus_enabled: bool = True
    metrics_path: str = "/metrics"

    # OpenTelemetry
    otel_enabled: bool = True
    otel_exporter_endpoint: str = "http://tempo:4317"
    otel_service_name: str = "fastapi-app"
    otel_sampling_ratio: float = 0.1

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"  # json or console

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = ObservabilitySettings()
```

### Production Checklist

- [ ] Prometheus metrics endpoint exposed
- [ ] Grafana dashboards configured
- [ ] Distributed tracing enabled
- [ ] Structured logging with structlog
- [ ] Correlation IDs in all logs
- [ ] Trace context propagation configured
- [ ] Alerting rules defined
- [ ] Sampling strategy implemented
- [ ] Metric cardinality controlled
- [ ] Log aggregation configured (Loki)
- [ ] Trace storage configured (Tempo)
- [ ] Dashboard provisioning automated
- [ ] Alert notification channels configured

---

## Summary

### Key Takeaways

1. **Three Pillars**: Metrics (Prometheus), Logs (structlog → Loki), Traces (OpenTelemetry → Tempo)
2. **RED Metrics**: Track Rate, Errors, Duration for all services
3. **USE Metrics**: Track Utilization, Saturation, Errors for resources
4. **Structured Logging**: Use structlog with JSON output and correlation IDs
5. **Distributed Tracing**: Use OpenTelemetry with proper context propagation
6. **Correlation**: Link metrics, logs, and traces for complete visibility
7. **Sampling**: Implement sampling strategies to balance observability and performance
8. **Cardinality**: Control metric label cardinality to prevent explosion

### Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [OpenTelemetry Python](https://opentelemetry.io/docs/instrumentation/python/)
- [structlog Documentation](https://www.structlog.org/)
- [Grafana Tempo](https://grafana.com/docs/tempo/)
- [Grafana Loki](https://grafana.com/docs/loki/)

---

**Version**: v1.0.0
**Last Updated**: 2025-01-14
