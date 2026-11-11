@echo off
setlocal
cd /d "%~dp0"
if not exist "backend\.venv\Scripts\python.exe" (
  echo Run setup_windows.bat first.
  pause
  exit /b 1
)
if not exist "frontend\node_modules" (
  echo Frontend dependencies are missing. Run setup_windows.bat first.
  pause
  exit /b 1
)
start "AttendX Backend" cmd /k "cd /d ""%~dp0backend"" && ""%~dp0backend\.venv\Scripts\python.exe"" -m uvicorn main:app --reload --host 127.0.0.1 --port 8000"
start "AttendX Frontend" cmd /k "cd /d ""%~dp0frontend"" && npm run dev"
echo AttendX services launched in separate windows.
echo Frontend: http://localhost:5173
echo API docs: http://127.0.0.1:8000/docs
