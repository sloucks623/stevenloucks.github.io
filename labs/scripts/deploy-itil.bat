@echo off
REM ITIL 4 Lab Documentation Deployment
REM Quick deployment script for ITIL 4 automation

echo.
echo ========================================
echo   ITIL 4 Lab Documentation Deployment
echo ========================================
echo.

if "%1"=="help" (
    echo USAGE: deploy-itil.bat [lab-directory]
    echo.
    echo Examples:
    echo   deploy-itil.bat                     Deploy to current directory
    echo   deploy-itil.bat C:\Labs\MyLab       Deploy to specific lab
    echo.
    echo This script will:
    echo   - Create ITIL 4 reference documentation
    echo   - Add professional service management templates
    echo   - Update README with ITIL 4 integration
    echo   - Create automation widgets for documentation
    echo.
    pause
    exit /b 0
)

set "SCRIPT_DIR=%~dp0"
set "LAB_PATH=%1"

if "%LAB_PATH%"=="" (
    set "LAB_PATH=%cd%"
)

echo Deploying ITIL 4 documentation to: %LAB_PATH%
echo.

PowerShell -ExecutionPolicy Bypass -File "%SCRIPT_DIR%Deploy-ITIL.ps1" -LabPath "%LAB_PATH%"

echo.
if %ERRORLEVEL% EQU 0 (
    echo ✅ Deployment completed successfully!
    echo.
    echo Check the docs/ folder for your new ITIL 4 reference materials.
) else (
    echo ❌ Deployment failed. Check the output above for details.
)

echo.
pause
