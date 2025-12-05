# PowerShell script to test Docker setup

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
    Start-Sleep -Seconds 3
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -ErrorAction Stop
    Write-Host "✅ Health check passed: $($health.status)" -ForegroundColor Green
    $health | ConvertTo-Json
} catch {
    Write-Host "❌ Health check failed: $_" -ForegroundColor Red
    Write-Host "Container logs:" -ForegroundColor Yellow
    docker logs crypto-api-test
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
Write-Host "To view logs, run: docker logs -f crypto-api-test" -ForegroundColor Yellow

