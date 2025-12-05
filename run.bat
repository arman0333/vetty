@echo off
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Starting Cryptocurrency Market Updates API...
python run.py
pause

