# Health Check and Version Information Endpoints

## Health Check Endpoints

### 1. Basic Health Check
**Endpoint:** `GET /health`

**Description:** Simple health check endpoint for the application.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.123456Z",
  "service": "cryptocurrency-api"
}
```

**Use Cases:**
- Docker health checks
- Load balancer health checks
- Simple monitoring

---

### 2. Detailed Health Check
**Endpoint:** `GET /health/detailed`

**Description:** Comprehensive health check including 3rd party service status (CoinGecko API).

**Response (All Healthy):**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.123456Z",
  "service": "cryptocurrency-api",
  "version": "1.0.0",
  "checks": {
    "application": {
      "status": "healthy",
      "message": "Application is running"
    },
    "coingecko_api": {
      "status": "healthy",
      "message": "CoinGecko API is accessible",
      "response_time_ms": 245.5
    }
  }
}
```

**Response (Degraded):**
```json
{
  "status": "degraded",
  "timestamp": "2024-01-15T10:30:00.123456Z",
  "service": "cryptocurrency-api",
  "version": "1.0.0",
  "checks": {
    "application": {
      "status": "healthy",
      "message": "Application is running"
    },
    "coingecko_api": {
      "status": "unhealthy",
      "message": "CoinGecko API request timed out"
    }
  }
}
```

**Status Values:**
- `healthy`: All systems operational
- `degraded`: Application running but external service issues
- `unhealthy`: Critical failures

**Use Cases:**
- Detailed monitoring
- Troubleshooting
- Service dependency checks

---

## Version Information Endpoint

### Version Info
**Endpoint:** `GET /version`

**Description:** Get version information for the application and 3rd party services.

**Response:**
```json
{
  "application": {
    "name": "Cryptocurrency Market Updates API",
    "version": "1.0.0",
    "python_version": "3.13.5"
  },
  "dependencies": {
    "fastapi": "0.123.9",
    "uvicorn": "0.38.0",
    "httpx": "0.28.1",
    "pydantic": "2.12.5",
    "python-jose": "3.5.0"
  },
  "external_services": {
    "coingecko": {
      "api_url": "https://api.coingecko.com/api/v3",
      "status": "available"
    }
  },
  "configuration": {
    "default_per_page": 10,
    "coingecko_api_url": "https://api.coingecko.com/api/v3"
  }
}
```

**Use Cases:**
- Version tracking
- Dependency management
- Debugging
- Deployment verification

---

## Docker Health Checks

The Dockerfile includes a built-in health check:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
```

**Check Docker Health:**
```bash
docker ps
# Look for "healthy" status

docker inspect --format='{{.State.Health.Status}}' <container_id>
```

---

## Monitoring Integration

### Prometheus-style Metrics (Future Enhancement)
These endpoints can be easily integrated with monitoring tools:
- Prometheus
- Grafana
- Datadog
- New Relic

### Example Monitoring Queries

**Check if service is healthy:**
```bash
curl http://localhost:8000/health | jq '.status'
```

**Get CoinGecko API status:**
```bash
curl http://localhost:8000/health/detailed | jq '.checks.coingecko_api.status'
```

**Get application version:**
```bash
curl http://localhost:8000/version | jq '.application.version'
```

---

## Testing Endpoints

### Using curl:
```bash
# Basic health
curl http://localhost:8000/health

# Detailed health
curl http://localhost:8000/health/detailed

# Version info
curl http://localhost:8000/version
```

### Using PowerShell:
```powershell
# Basic health
Invoke-RestMethod -Uri "http://localhost:8000/health"

# Detailed health
Invoke-RestMethod -Uri "http://localhost:8000/health/detailed"

# Version info
Invoke-RestMethod -Uri "http://localhost:8000/version"
```

### Using Swagger UI:
1. Open http://localhost:8000/docs
2. Find the endpoints under "default" section
3. Click "Try it out" and "Execute"

---

## Status Codes

- `200 OK`: Service is healthy
- `503 Service Unavailable`: Service is degraded (if implemented)
- `500 Internal Server Error`: Critical failure

---

## Best Practices

1. **Use `/health` for simple checks** (faster, no external calls)
2. **Use `/health/detailed` for comprehensive monitoring** (includes external service checks)
3. **Use `/version` for deployment verification** (check versions match)
4. **Monitor response times** for `/health/detailed` to detect performance issues
5. **Set up alerts** based on health check responses

