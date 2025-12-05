# 🐳 Testing Docker Setup

## Quick Test Commands

### 1. Build the Docker Image

```bash
docker build -t cryptocurrency-api .
```

**Expected Output:**
```
[+] Building ... 
 => [internal] load build definition from Dockerfile
 => => transferring dockerfile: ...
 => [1/7] FROM docker.io/library/python:3.13-slim
 => ...
 => => exporting to image
 => => => writing image sha256:...
Successfully built abc123def456
Successfully tagged cryptocurrency-api:latest
```

---

### 2. Test the Container Locally

#### Run the container:
```bash
docker run -d \
  --name crypto-api-test \
  -p 8000:8000 \
  -e SECRET_KEY=test-secret-key-min-32-chars-long-for-testing \
  cryptocurrency-api
```

#### Check if container is running:
```bash
docker ps
```

**Expected Output:**
```
CONTAINER ID   IMAGE                STATUS          PORTS                    NAMES
abc123def456   cryptocurrency-api   Up 2 seconds   (healthy) 0.0.0.0:8000->8000/tcp   crypto-api-test
```

---

### 3. Test Health Check Endpoints

#### Basic Health Check:
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.123456Z",
  "service": "cryptocurrency-api"
}
```

#### Detailed Health Check:
```bash
curl http://localhost:8000/health/detailed
```

**Expected Response:**
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

#### Version Information:
```bash
curl http://localhost:8000/version
```

**Expected Response:**
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
    ...
  },
  "external_services": {
    "coingecko": {
      "api_url": "https://api.coingecko.com/api/v3",
      "status": "available"
    }
  }
}
```

---

### 4. Test Docker Health Check

#### Check container health status:
```bash
docker inspect --format='{{.State.Health.Status}}' crypto-api-test
```

**Expected Output:** `healthy`

#### View health check logs:
```bash
docker inspect --format='{{json .State.Health}}' crypto-api-test | python -m json.tool
```

---

### 5. Test API Endpoints

#### Get authentication token:
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass"}'
```

#### Test protected endpoint:
```bash
TOKEN="your-token-here"
curl -X GET "http://localhost:8000/coins?page_num=1&per_page=5" \
  -H "Authorization: Bearer $TOKEN"
```

---

### 6. Test with Docker Compose

#### Start services:
```bash
docker-compose up --build
```

#### Start in background:
```bash
docker-compose up -d --build
```

#### View logs:
```bash
docker-compose logs -f api
```

#### Check health:
```bash
docker-compose ps
```

#### Stop services:
```bash
docker-compose down
```

---

## Complete Test Script

### PowerShell Script (`test-docker.ps1`):

```powershell
Write-Host "🐳 Testing Docker Setup" -ForegroundColor Cyan

# 1. Build image
Write-Host "`n1. Building Docker image..." -ForegroundColor Yellow
docker build -t cryptocurrency-api .

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Build failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Build successful!" -ForegroundColor Green

# 2. Stop and remove existing container if exists
Write-Host "`n2. Cleaning up existing containers..." -ForegroundColor Yellow
docker stop crypto-api-test 2>$null
docker rm crypto-api-test 2>$null

# 3. Run container
Write-Host "`n3. Starting container..." -ForegroundColor Yellow
docker run -d `
  --name crypto-api-test `
  -p 8000:8000 `
  -e SECRET_KEY=test-secret-key-min-32-chars-long-for-testing `
  cryptocurrency-api

Start-Sleep -Seconds 5

# 4. Check container status
Write-Host "`n4. Checking container status..." -ForegroundColor Yellow
docker ps --filter "name=crypto-api-test"

# 5. Test health endpoint
Write-Host "`n5. Testing /health endpoint..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -ErrorAction Stop
    Write-Host "✅ Health check passed: $($health.status)" -ForegroundColor Green
    $health | ConvertTo-Json
} catch {
    Write-Host "❌ Health check failed: $_" -ForegroundColor Red
}

# 6. Test detailed health
Write-Host "`n6. Testing /health/detailed endpoint..." -ForegroundColor Yellow
try {
    $detailed = Invoke-RestMethod -Uri "http://localhost:8000/health/detailed" -ErrorAction Stop
    Write-Host "✅ Detailed health check passed: $($detailed.status)" -ForegroundColor Green
    Write-Host "CoinGecko API: $($detailed.checks.coingecko_api.status)" -ForegroundColor Cyan
    $detailed | ConvertTo-Json -Depth 5
} catch {
    Write-Host "❌ Detailed health check failed: $_" -ForegroundColor Red
}

# 7. Test version endpoint
Write-Host "`n7. Testing /version endpoint..." -ForegroundColor Yellow
try {
    $version = Invoke-RestMethod -Uri "http://localhost:8000/version" -ErrorAction Stop
    Write-Host "✅ Version endpoint passed" -ForegroundColor Green
    Write-Host "App Version: $($version.application.version)" -ForegroundColor Cyan
    Write-Host "Python Version: $($version.application.python_version)" -ForegroundColor Cyan
    $version | ConvertTo-Json -Depth 3
} catch {
    Write-Host "❌ Version check failed: $_" -ForegroundColor Red
}

# 8. Test authentication
Write-Host "`n8. Testing authentication..." -ForegroundColor Yellow
try {
    $body = @{
        username = "testuser"
        password = "testpass"
    } | ConvertTo-Json
    
    $auth = Invoke-RestMethod -Uri "http://localhost:8000/auth/login" `
        -Method Post -Body $body -ContentType "application/json" -ErrorAction Stop
    Write-Host "✅ Authentication successful" -ForegroundColor Green
    $token = $auth.access_token
    Write-Host "Token received: $($token.Substring(0, 20))..." -ForegroundColor Cyan
} catch {
    Write-Host "❌ Authentication failed: $_" -ForegroundColor Red
}

# 9. Test protected endpoint
if ($token) {
    Write-Host "`n9. Testing protected endpoint..." -ForegroundColor Yellow
    try {
        $headers = @{
            Authorization = "Bearer $token"
        }
        $coins = Invoke-RestMethod -Uri "http://localhost:8000/coins?page_num=1&per_page=3" `
            -Headers $headers -ErrorAction Stop
        Write-Host "✅ Protected endpoint works!" -ForegroundColor Green
        Write-Host "Retrieved $($coins.data.Count) coins" -ForegroundColor Cyan
    } catch {
        Write-Host "❌ Protected endpoint failed: $_" -ForegroundColor Red
    }
}

# 10. Check Docker health
Write-Host "`n10. Checking Docker health status..." -ForegroundColor Yellow
$healthStatus = docker inspect --format='{{.State.Health.Status}}' crypto-api-test 2>$null
if ($healthStatus -eq "healthy") {
    Write-Host "✅ Docker health check: $healthStatus" -ForegroundColor Green
} else {
    Write-Host "⚠️ Docker health check: $healthStatus" -ForegroundColor Yellow
}

Write-Host "`n✨ Testing complete!" -ForegroundColor Cyan
Write-Host "`nTo stop the container, run: docker stop crypto-api-test" -ForegroundColor Yellow
Write-Host "To remove the container, run: docker rm crypto-api-test" -ForegroundColor Yellow
```

### Bash Script (`test-docker.sh`):

```bash
#!/bin/bash

echo "🐳 Testing Docker Setup"

# 1. Build image
echo -e "\n1. Building Docker image..."
docker build -t cryptocurrency-api .

if [ $? -ne 0 ]; then
    echo "❌ Build failed!"
    exit 1
fi
echo "✅ Build successful!"

# 2. Clean up
echo -e "\n2. Cleaning up existing containers..."
docker stop crypto-api-test 2>/dev/null
docker rm crypto-api-test 2>/dev/null

# 3. Run container
echo -e "\n3. Starting container..."
docker run -d \
  --name crypto-api-test \
  -p 8000:8000 \
  -e SECRET_KEY=test-secret-key-min-32-chars-long-for-testing \
  cryptocurrency-api

sleep 5

# 4. Check status
echo -e "\n4. Checking container status..."
docker ps --filter "name=crypto-api-test"

# 5. Test health
echo -e "\n5. Testing /health endpoint..."
curl -s http://localhost:8000/health | jq .

# 6. Test detailed health
echo -e "\n6. Testing /health/detailed endpoint..."
curl -s http://localhost:8000/health/detailed | jq .

# 7. Test version
echo -e "\n7. Testing /version endpoint..."
curl -s http://localhost:8000/version | jq .

# 8. Test auth
echo -e "\n8. Testing authentication..."
TOKEN=$(curl -s -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass"}' | jq -r '.access_token')

if [ -n "$TOKEN" ]; then
    echo "✅ Authentication successful"
    echo "Token: ${TOKEN:0:20}..."
    
    # 9. Test protected endpoint
    echo -e "\n9. Testing protected endpoint..."
    curl -s -H "Authorization: Bearer $TOKEN" \
      "http://localhost:8000/coins?page_num=1&per_page=3" | jq .
fi

# 10. Docker health
echo -e "\n10. Checking Docker health status..."
docker inspect --format='{{.State.Health.Status}}' crypto-api-test

echo -e "\n✨ Testing complete!"
echo -e "\nTo stop: docker stop crypto-api-test"
echo "To remove: docker rm crypto-api-test"
```

---

## Step-by-Step Manual Testing

### Step 1: Build Image
```bash
docker build -t cryptocurrency-api .
```

### Step 2: Run Container
```bash
docker run -d --name crypto-api-test -p 8000:8000 \
  -e SECRET_KEY=test-secret-key-min-32-chars-long-for-testing \
  cryptocurrency-api
```

### Step 3: Wait for Startup
```bash
# Wait 5-10 seconds for app to start
sleep 10

# Check logs
docker logs crypto-api-test
```

### Step 4: Test Endpoints
```bash
# Health check
curl http://localhost:8000/health

# Detailed health
curl http://localhost:8000/health/detailed

# Version
curl http://localhost:8000/version

# Swagger UI (open in browser)
# http://localhost:8000/docs
```

### Step 5: Check Docker Health
```bash
docker inspect crypto-api-test | grep -A 10 Health
```

### Step 6: Clean Up
```bash
docker stop crypto-api-test
docker rm crypto-api-test
```

---

## Troubleshooting

### Container won't start
```bash
# Check logs
docker logs crypto-api-test

# Run interactively to see errors
docker run -it --rm -p 8000:8000 cryptocurrency-api
```

### Port already in use
```bash
# Change port mapping
docker run -d --name crypto-api-test -p 8001:8000 cryptocurrency-api
# Then access at http://localhost:8001
```

### Health check failing
```bash
# Check container logs
docker logs crypto-api-test

# Test health manually
docker exec crypto-api-test python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
```

### Permission issues
```bash
# Check if running as non-root user
docker exec crypto-api-test whoami
# Should output: appuser
```

---

## Quick Test Commands Summary

```bash
# Build
docker build -t cryptocurrency-api .

# Run
docker run -d --name test -p 8000:8000 cryptocurrency-api

# Test
curl http://localhost:8000/health
curl http://localhost:8000/version

# Cleanup
docker stop test && docker rm test
```

