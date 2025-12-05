# 🐳 Docker Setup Guide

## Quick Start

### Option 1: Using Docker Compose (Recommended)

1. **Build and run:**
   ```bash
   docker-compose up --build
   ```

2. **Run in background:**
   ```bash
   docker-compose up -d
   ```

3. **View logs:**
   ```bash
   docker-compose logs -f
   ```

4. **Stop:**
   ```bash
   docker-compose down
   ```

### Option 2: Using Docker Directly

1. **Build the image:**
   ```bash
   docker build -t cryptocurrency-api .
   ```

2. **Run the container:**
   ```bash
   docker run -d \
     --name crypto-api \
     -p 8000:8000 \
     -e SECRET_KEY=your-secret-key-here \
     cryptocurrency-api
   ```

3. **View logs:**
   ```bash
   docker logs -f crypto-api
   ```

4. **Stop:**
   ```bash
   docker stop crypto-api
   docker rm crypto-api
   ```

## Environment Variables

Create a `.env` file or set environment variables:

```env
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
COINGECKO_API_URL=https://api.coingecko.com/api/v3
DEFAULT_PER_PAGE=10
```

## Health Checks

The container includes built-in health checks:

- **Basic Health:** `GET http://localhost:8000/health`
- **Detailed Health:** `GET http://localhost:8000/health/detailed`
- **Version Info:** `GET http://localhost:8000/version`

## Docker Compose Commands

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Rebuild and start
docker-compose up --build

# Stop services
docker-compose down

# View logs
docker-compose logs -f api

# Execute command in container
docker-compose exec api python -c "print('Hello')"

# Restart service
docker-compose restart api
```

## Production Considerations

1. **Use environment variables** for secrets (never hardcode)
2. **Use Docker secrets** or external secret management
3. **Set up proper logging** (consider volume mounts for logs)
4. **Configure resource limits** in docker-compose.yml
5. **Use reverse proxy** (nginx/traefik) in front of the API
6. **Enable HTTPS** at the reverse proxy level

## Testing Docker Setup

### Quick Test
```bash
# Build and test
docker build -t cryptocurrency-api .
docker run -d --name test -p 8000:8000 cryptocurrency-api

# Test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/version

# Cleanup
docker stop test && docker rm test
```

### Automated Test Script
```powershell
# Windows PowerShell
.\test-docker.ps1
```

See [TEST_DOCKER.md](TEST_DOCKER.md) for comprehensive testing guide.

## Troubleshooting

### Container won't start
```bash
docker-compose logs api
# Or for direct Docker
docker logs crypto-api-test
```

### Port already in use
Change the port mapping in docker-compose.yml:
```yaml
ports:
  - "8001:8000"  # Use port 8001 instead
```

### Permission issues
The Dockerfile creates a non-root user. If you need to debug:
```bash
docker-compose exec api sh
```

### Health check failing
```bash
# Check logs
docker logs crypto-api-test

# Test health manually
docker exec crypto-api-test python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
```

