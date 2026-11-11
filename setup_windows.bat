@echo off
setlocal
cd /d "%~dp0"
echo ========================================
echo AttendX - first-time Windows setup
echo ========================================
where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found. Install Python 3.11 and enable Add Python to PATH.
  pause
  exit /b 1
)
where node >nul 2>nul
if errorlevel 1 (
  echo Node.js was not found. Install Node.js LTS and restart this script.
  pause
  exit /b 1
)
if not exist "backend\.venv\Scripts\python.exe" (
  echo Creating backend virtual environment...
  python -m venv backend\.venv
  if errorlevel 1 goto fail
)
echo Installing backend packages...
backend\.venv\Scripts\python.exe -m pip install --upgrade pip
if errorlevel 1 goto fail
backend\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
if errorlevel 1 goto fail
echo Installing frontend packages...
cd frontend
call npm install
if errorlevel 1 goto fail
cd ..
echo.
echo Setup complete. Run start_attendx.bat to launch AttendX.
pause
exit /b 0
:fail
echo Setup failed. Read the error above, fix it, and run setup_windows.bat again.
pause
exit /b 1
