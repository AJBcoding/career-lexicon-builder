# Logging Guide

## Overview

The wrapper application uses structured JSON logging for production-grade observability and monitoring. All log output is emitted as JSON with consistent fields for easy parsing and aggregation.

## Log Levels

- **DEBUG**: Detailed diagnostic information for troubleshooting
- **INFO**: General informational messages about application flow
- **WARNING**: Warning messages for potentially harmful situations
- **ERROR**: Error events that might still allow the app to continue
- **CRITICAL**: Very severe error events that may lead to application abort

## Structured Fields

Every log entry includes the following standard fields:

- `@timestamp`: ISO 8601 timestamp of the log event
- `severity`: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `name`: Logger name (typically the module path)
- `message`: Human-readable log message
- `service`: Service identifier (always "wrapper-backend")
- `request_id`: Unique identifier for the current request (if in request context)
- `user_id`: Authenticated user identifier (if available)

Additional context can be added via the `extra` parameter in logging calls.

## Log Format Example

```json
{
  "@timestamp": "2025-11-12T10:30:45.123456",
  "severity": "INFO",
  "name": "services.skill_service",
  "message": "Executing skill",
  "service": "wrapper-backend",
  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "user_id": "user_123",
  "skill_name": "job-description-analysis",
  "project_path": "/data/applications/acme-engineer-2025-01-15",
  "prompt_length": 1024
}
```

## Using Structured Logging

### Basic Usage

```python
import logging

logger = logging.getLogger(__name__)

# Simple message
logger.info("Operation completed")

# With structured context
logger.info("User action", extra={
    'action': 'create_project',
    'project_id': 'acme-corp-2025-01-15',
    'duration_ms': 123.45
})

# Error with exception info
try:
    risky_operation()
except Exception as e:
    logger.error("Operation failed", extra={
        'operation': 'risky_operation',
        'error': str(e),
        'error_type': type(e).__name__
    }, exc_info=True)
```

### Best Practices

1. **Always include relevant context**: Use the `extra` dict to add structured fields
2. **Use appropriate log levels**: Don't log everything as INFO or ERROR
3. **Don't log sensitive data**: Never log passwords, API keys, or tokens
4. **Keep messages concise**: The message should be human-readable summary
5. **Use consistent field names**: Maintain naming conventions across services
6. **Truncate large values**: Don't log full file contents or massive payloads

### Common Patterns

#### API Calls
```python
logger.info("Anthropic API call starting", extra={
    'skill_name': skill_name,
    'model': model_name,
    'max_tokens': max_tokens
})

# After completion
logger.info("Anthropic API call completed", extra={
    'skill_name': skill_name,
    'input_tokens': 1500,
    'output_tokens': 2048,
    'duration_ms': 3450.21
})
```

#### Service Operations
```python
logger.info("Creating project", extra={
    'project_id': project_id,
    'institution': institution,
    'position': position
})

logger.info("Project created successfully", extra={
    'project_id': project_id,
    'project_path': str(path)
})
```

#### Errors and Exceptions
```python
logger.error("Operation failed", extra={
    'operation': 'create_project',
    'project_id': project_id,
    'error': str(e),
    'error_type': type(e).__name__
}, exc_info=True)  # Include full traceback
```

## Querying Logs

### Using Docker Compose

```bash
# View all logs
docker-compose logs backend

# Follow logs in real-time
docker-compose logs -f backend

# All logs for a specific request
docker-compose logs backend | grep '"request_id":"abc-123"'

# All errors in last hour
docker-compose logs --since 1h backend | grep '"severity":"ERROR"'

# Skill execution logs
docker-compose logs backend | grep '"skill_name"'

# API token usage
docker-compose logs backend | grep '"input_tokens"'
```

### Using jq for JSON Parsing

```bash
# Pretty print logs
docker-compose logs backend | jq '.'

# Extract specific fields
docker-compose logs backend | jq '{time: .["@timestamp"], level: .severity, msg: .message}'

# Filter by severity
docker-compose logs backend | jq 'select(.severity == "ERROR")'

# Calculate average API response time
docker-compose logs backend | jq -s 'map(select(.duration_ms)) | map(.duration_ms) | add/length'
```

## Log Aggregation

For production deployments, consider using log aggregation tools:

### Recommended Tools
- **ELK Stack** (Elasticsearch, Logstash, Kibana)
- **Grafana Loki**
- **Datadog**
- **CloudWatch Logs** (AWS)
- **Google Cloud Logging** (GCP)

### Docker Logging Configuration

Configure in `docker-compose.prod.yml`:

```yaml
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
        labels: "service,environment"
```

### Shipping to External Services

For shipping to external log aggregation:

```yaml
services:
  backend:
    logging:
      driver: "syslog"
      options:
        syslog-address: "tcp://logs.example.com:514"
        tag: "wrapper-backend"
```

## Monitoring and Alerts

### Key Metrics to Monitor

1. **Error Rate**: Count of ERROR and CRITICAL logs
2. **API Latency**: `duration_ms` field in request logs
3. **Token Usage**: Sum of `input_tokens` and `output_tokens`
4. **WebSocket Connections**: Connection/disconnection events
5. **Skill Execution**: Success/failure rates by skill

### Sample Alert Queries

```
# High error rate
severity="ERROR" | count by 5m > 10

# Slow API responses
duration_ms > 5000

# Excessive token usage
output_tokens > 10000

# Failed skill executions
message="Skill execution failed" | count by 1h
```

## Request Tracing

Every HTTP request gets a unique `request_id` that propagates through all log entries for that request. Use this to trace the full lifecycle of a request:

```bash
# Get request_id from initial request log
docker-compose logs backend | grep "Request started" | jq .request_id

# Then trace all logs for that request
docker-compose logs backend | grep '"request_id":"<id>"'
```

## Configuration

### Environment Variables

```bash
# Set log level (default: INFO)
LOG_LEVEL=DEBUG

# Environment identifier for logs
ENVIRONMENT=production
```

### Code Configuration

Update in `utils/logging_config.py`:

```python
# Change default level
setup_logging(level=logging.DEBUG)

# Adjust library log levels
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
logging.getLogger("anthropic").setLevel(logging.INFO)
```

## Troubleshooting

### No Logs Appearing

1. Check that `setup_logging()` is called at startup
2. Verify logger is created: `logger = logging.getLogger(__name__)`
3. Ensure log level is appropriate for your messages

### Too Much Noise

1. Increase log level to WARNING or ERROR
2. Adjust specific library log levels
3. Add filtering in your log aggregation tool

### Missing Context Fields

1. Ensure middleware is added before CORS
2. Verify context vars are set in middleware
3. Check that `extra` dict is used in log calls

## Performance Considerations

- Structured logging has minimal overhead
- Avoid logging in tight loops
- Truncate large payloads before logging
- Use appropriate log levels (DEBUG should be rare)
- Consider async logging for high-throughput scenarios

## Security Notes

- Never log authentication credentials
- Redact sensitive user data (PII)
- Be cautious with file paths and system information
- Sanitize user input before logging
- Consider encrypting logs at rest in production
