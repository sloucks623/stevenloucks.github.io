@echo off
cls
echo.
echo ========================================
echo    Complete Lab Integration System
echo ========================================
echo.
echo This script will:
echo   1. Create assessment files for all labs
echo   2. Update dashboard with real progress
echo   3. Integrate markdown progress tracking
echo.
echo Press any key to continue...
pause >nul

echo.
echo Running Complete Lab Integration...
echo.

cd /d "%~dp0"
python complete-lab-integration.py

echo.
echo ========================================
echo         Integration Complete!
echo ========================================
echo.
echo Your portfolio dashboard now reflects real progress data!
echo.
echo Next steps:
echo   1. Open lab-assessments folder
echo   2. Update task completion in .md files
echo   3. Run this script again to refresh dashboard
echo   4. View your updated portfolio website
echo.
pause
