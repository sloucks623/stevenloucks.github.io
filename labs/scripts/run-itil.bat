@echo off
REM ITIL 4 Automation - Simple Launcher
REM Automatically handles Python version selection

echo.
echo ==========================================
echo   ITIL 4 Lab Documentation Automation
echo ==========================================
echo.

REM Check if we're in the right directory
if not exist "itil-automation.py" (
    echo ❌ itil-automation.py not found in current directory
    echo Please run this script from the scripts folder
    echo.
    pause
    exit /b 1
)

REM Try different Python commands in order of preference
echo 🔍 Looking for Python installation...

py -3 --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ Found Python via Windows launcher
    set PYTHON_CMD=py -3
    goto :run_script
)

python3 --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ Found python3 command
    set PYTHON_CMD=python3
    goto :run_script
)

python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ Found python command
    set PYTHON_CMD=python
    goto :run_script
)

REM No Python found
echo ❌ Python not found or not in PATH
echo.
echo 💡 SOLUTION OPTIONS:
echo.
echo 1. Install Python from Microsoft Store:
echo    - Open Microsoft Store
echo    - Search for "Python 3.11" or newer
echo    - Install and restart command prompt
echo.
echo 2. Install from python.org:
echo    - Go to https://python.org/downloads
echo    - Download latest Python 3.x
echo    - Check "Add Python to PATH" during install
echo.
echo 3. If Python is already installed:
echo    - Check if it's in your PATH environment variable
echo    - Try running: py --version
echo.
pause
exit /b 1

:run_script
echo.
echo 🚀 Starting ITIL 4 automation...
echo Command: %PYTHON_CMD% itil-automation.py %*
echo.

REM Run the Python script with all passed arguments
%PYTHON_CMD% itil-automation.py %*

echo.
if %ERRORLEVEL% EQU 0 (
    echo ✅ Script completed successfully!
) else (
    echo ⚠️  Script completed with issues.
    echo.
    echo 💡 For help, run: %PYTHON_CMD% itil-automation.py --help
)

echo.
echo Press any key to close...
pause >nul
