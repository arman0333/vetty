# PowerShell script to run the application
Write-Host "Activating virtual environment..." -ForegroundColor Green
& .\venv\Scripts\Activate.ps1

Write-Host "Starting Cryptocurrency Market Updates API..." -ForegroundColor Green
python run.py

