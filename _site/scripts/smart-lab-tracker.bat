@echo off
REM Intelligent Lab Tracker - Easy batch interface
REM Creates assessments and tracks progress automatically

echo.
echo ===============================================
echo   Intelligent Lab Progress Tracker
echo ===============================================
echo.

REM Set up environment
cd /d "%~dp0"
set SCRIPT_DIR=%~dp0
set PORTFOLIO_DIR=%SCRIPT_DIR%..

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.7+ and try again.
    pause
    exit /b 1
)

REM Install dependencies if needed
if not exist "%PORTFOLIO_DIR%\scripts\requirements.txt" (
    echo 📦 Creating requirements.txt...
    echo requests^>^>requirements.txt
    echo pathlib^>^>requirements.txt
    echo pyyaml^>^>requirements.txt
)

REM Check if virtual environment exists
if not exist "%PORTFOLIO_DIR%\venv" (
    echo 🔧 Creating virtual environment...
    python -m venv "%PORTFOLIO_DIR%\venv"
)

REM Activate virtual environment
call "%PORTFOLIO_DIR%\venv\Scripts\activate.bat"

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r "%PORTFOLIO_DIR%\scripts\requirements.txt" >nul 2>&1

echo.
echo Choose an action:
echo.
echo 1. Create new lab from tutorial URL
echo 2. Update task progress
echo 3. List lab tasks and progress
echo 4. Update dashboard
echo 5. View all labs status
echo 6. Exit
echo.

set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto create_lab
if "%choice%"=="2" goto update_task
if "%choice%"=="3" goto list_tasks
if "%choice%"=="4" goto update_dashboard
if "%choice%"=="5" goto view_status
if "%choice%"=="6" goto exit

echo Invalid choice. Please try again.
pause
goto menu

:create_lab
echo.
echo 🆕 Creating New Lab Assessment
echo.
set /p lab_name="Enter lab name: "
set /p tutorial_url="Enter tutorial URL: "

echo.
echo 🔄 Creating assessment and progress tracker...
python "%SCRIPT_DIR%intelligent-lab-tracker.py" create --lab-name "%lab_name%" --tutorial-url "%tutorial_url%"

echo.
echo ✅ Lab created! You can now:
echo   - View progress: run option 3
echo   - Update tasks: run option 2
echo   - Check dashboard: run option 4
echo.
pause
goto menu

:update_task
echo.
echo 📝 Update Task Progress
echo.
set /p lab_name="Enter lab name: "

echo.
echo 📋 Current tasks for %lab_name%:
python "%SCRIPT_DIR%intelligent-lab-tracker.py" list --lab-name "%lab_name%"

echo.
set /p task_id="Enter task ID to update: "
echo.
echo Status options:
echo   1. Not Started
echo   2. In Progress  
echo   3. Completed
echo.
set /p status_choice="Choose status (1-3): "

if "%status_choice%"=="1" set task_status=Not Started
if "%status_choice%"=="2" set task_status=In Progress
if "%status_choice%"=="3" set task_status=Completed

set /p notes="Enter notes (optional): "
set /p time_spent="Enter time spent in minutes (optional): "

echo.
echo 🔄 Updating task progress...
python "%SCRIPT_DIR%intelligent-lab-tracker.py" update --lab-name "%lab_name%" --task-id "%task_id%" --status "%task_status%" --notes "%notes%" --time-spent "%time_spent%"

echo.
pause
goto menu

:list_tasks
echo.
echo 📋 List Lab Tasks
echo.
set /p lab_name="Enter lab name: "

python "%SCRIPT_DIR%intelligent-lab-tracker.py" list --lab-name "%lab_name%"

echo.
pause
goto menu

:update_dashboard
echo.
echo 🔄 Updating Dashboard...
python "%SCRIPT_DIR%intelligent-lab-tracker.py" dashboard

echo.
echo ✅ Dashboard updated! You can view it at:
echo   - Test page: %PORTFOLIO_DIR%\test-dashboard.html
echo   - Main site: %PORTFOLIO_DIR%\index.html
echo   - Labs page: %PORTFOLIO_DIR%\labs.html
echo.
pause
goto menu

:view_status
echo.
echo 📊 All Labs Status
echo.

REM Show dashboard summary
if exist "%PORTFOLIO_DIR%\data\dashboard-summary.json" (
    echo 📈 Dashboard Summary:
    python -c "import json; d=json.load(open(r'%PORTFOLIO_DIR%\data\dashboard-summary.json')); print(f'Total Labs: {d[\"summary\"][\"total_labs\"]}'); print(f'Completed: {d[\"summary\"][\"completed_labs\"]}'); print(f'In Progress: {d[\"summary\"][\"in_progress_labs\"]}'); print(f'Total Hours: {d[\"summary\"][\"total_hours_spent\"]}'); print('\\nLabs:'); [print(f'  {lab[\"name\"]}: {lab[\"progress\"]:.1f}%% ({lab[\"status\"]})') for lab in d['labs']]"
) else (
    echo ⚠️  No dashboard data found. Run option 4 to create it.
)

echo.
pause
goto menu

:exit
echo.
echo 👋 Goodbye!
pause
exit /b 0

:menu
echo.
echo Choose an action:
echo.
echo 1. Create new lab from tutorial URL
echo 2. Update task progress
echo 3. List lab tasks and progress
echo 4. Update dashboard
echo 5. View all labs status
echo 6. Exit
echo.

set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto create_lab
if "%choice%"=="2" goto update_task
if "%choice%"=="3" goto list_tasks
if "%choice%"=="4" goto update_dashboard
if "%choice%"=="5" goto view_status
if "%choice%"=="6" goto exit

echo Invalid choice. Please try again.
pause
goto menu
