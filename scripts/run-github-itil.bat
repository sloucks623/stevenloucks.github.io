@echo off
REM GitHub Lab Repository ITIL 4 Automation Launcher
REM Easy launcher for updating all your GitHub lab repositories

echo.
echo ==========================================
echo   GitHub Lab ITIL 4 Automation
echo ==========================================
echo.
echo This will add ITIL 4 professional documentation
echo to your GitHub lab repositories:
echo.
echo   - lab-soc-automation
echo   - lab-active-directory-1.0  
echo   - lab-active-directory-2.0
echo   - lab-detection-1.0
echo.

REM Check if we're in the right directory
if not exist "github-itil-automation.py" (
    echo ❌ github-itil-automation.py not found
    echo Please run this from the scripts folder
    pause
    exit /b 1
)

REM Check for dry-run argument
if "%1"=="--dry-run" (
    echo 🧪 DRY RUN MODE: Will show what would be done
    echo.
    goto :find_python
)

if "%1"=="--help" (
    echo.
    echo USAGE:
    echo   run-github-itil.bat                # Process all repositories
    echo   run-github-itil.bat --dry-run      # Preview changes only
    echo   run-github-itil.bat [repo-name]    # Process specific repository
    echo.
    echo EXAMPLES:
    echo   run-github-itil.bat lab-soc-automation
    echo   run-github-itil.bat --dry-run
    echo.
    pause
    exit /b 0
)

echo ⚠️  WARNING: This will modify your GitHub repositories!
echo.
echo Do you want to continue? (y/N)
set /p confirm=
if /i not "%confirm%"=="y" (
    echo Operation cancelled.
    pause
    exit /b 0
)

:find_python
echo.
echo 🔍 Looking for Python installation...

REM Try different Python commands
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

echo ❌ Python not found
echo.
echo Please install Python 3.x and try again:
echo - Microsoft Store: Search "Python 3.11"
echo - Or: https://python.org/downloads
pause
exit /b 1

:run_script
echo.
echo 🚀 Starting GitHub lab repository automation...
echo.

REM Run the Python script with arguments
if "%1"=="" (
    %PYTHON_CMD% github-itil-automation.py
) else (
    %PYTHON_CMD% github-itil-automation.py %*
)

echo.
if %ERRORLEVEL% EQU 0 (
    echo ✅ Automation completed successfully!
    echo.
    echo 💡 Next steps:
    echo - Check your GitHub repositories for the changes
    echo - Review the ITIL 4 content in each lab README
    echo - Customize the content for each specific lab
) else (
    echo ⚠️  Automation completed with issues.
    echo.
    echo 💡 For help: %PYTHON_CMD% github-itil-automation.py --help
)

echo.
echo Press any key to close...
pause >nul
