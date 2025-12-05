# 🚀 How to Run the Application

## Quick Start (3 Steps)

### Step 1: Activate Virtual Environment

Open PowerShell in the project directory and run:

```powershell
.\venv\Scripts\Activate.ps1
```

**If you get an execution policy error**, run this first:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

You should see `(venv)` appear in your prompt.

### Step 2: Run the Application

Choose one of these methods:

**Option A: Using the run script (Easiest)**
```powershell
python run.py
```

**Option B: Using uvicorn directly**
```powershell
uvicorn app.main:app --reload
```

**Option C: Using Python module**
```powershell
python -m uvicorn app.main:app --reload
```

### Step 3: Access the API

Once you see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

**Important:** Use `localhost` or `127.0.0.1` in your browser, NOT `0.0.0.0`

Open your browser and go to:
- **📚 Swagger UI (Interactive API Docs)**: http://localhost:8000/docs
- **📖 ReDoc**: http://localhost:8000/redoc
- **🏠 API Base**: http://localhost:8000
- **❤️ Health Check**: http://localhost:8000/health

## 🔑 Test Authentication

### Get a JWT Token

**Using PowerShell:**
```powershell
$body = @{
    username = "testuser"
    password = "testpass"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/auth/login" -Method Post -Body $body -ContentType "application/json"
$token = $response.access_token
Write-Host "Your token: $token"
```

**Or use the Swagger UI at http://localhost:8000/docs:**
1. Click on `POST /auth/login`
2. Click "Try it out"
3. Enter username: `testuser` and password: `testpass`
4. Click "Execute"
5. Copy the `access_token` from the response

### Use the Token

**In Swagger UI:**
1. Click the "Authorize" button at the top
2. Enter: `Bearer YOUR_TOKEN_HERE` (replace YOUR_TOKEN_HERE with the actual token)
3. Click "Authorize"
4. Now you can test all protected endpoints

**Using PowerShell:**
```powershell
$headers = @{
    Authorization = "Bearer $token"
}
Invoke-RestMethod -Uri "http://localhost:8000/coins?page_num=1&per_page=10" -Headers $headers
```

## 🛑 To Stop the Server

Press `Ctrl+C` in the terminal where the server is running.

## 📝 Complete Command Sequence

```powershell
# 1. Navigate to project directory (if not already there)
cd C:\Users\arman\Desktop\vetty

# 2. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 3. Run the application
python run.py

# 4. Open browser to http://localhost:8000/docs
```

## 🧪 Run Tests

```powershell
# Make sure venv is activated first
pytest

# With coverage report
pytest --cov=app --cov-report=html
```

## ⚠️ Troubleshooting

**Port 8000 already in use?**
```powershell
uvicorn app.main:app --reload --port 8001
```

**Module not found?**
- Make sure venv is activated (you see `(venv)` in prompt)
- Reinstall: `pip install -r requirements.txt`

**Can't activate venv?**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

