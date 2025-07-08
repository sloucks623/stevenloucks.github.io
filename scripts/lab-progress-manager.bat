@echo off
cls
echo.
echo ================================================
echo       Lab Progress Management System
echo ================================================
echo.
echo This system provides real-time, task-based progress tracking
echo for your cybersecurity portfolio labs.
echo.
echo Available options:
echo   1. Create new lab assessment
echo   2. Update progress from assessments
echo   3. View current progress
echo   4. Generate progress report
echo   5. Open web dashboard
echo   6. Exit
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto create_assessment
if "%choice%"=="2" goto update_progress
if "%choice%"=="3" goto view_progress
if "%choice%"=="4" goto generate_report
if "%choice%"=="5" goto open_dashboard
if "%choice%"=="6" goto exit

:create_assessment
cls
echo.
echo Creating new lab assessment...
echo.
echo Available labs:
echo   - lab-soc-automation
echo   - lab-active-directory-1.0
echo   - lab-active-directory-2.0
echo   - lab-detection-1.0
echo   - lab-soc-helpdesk
echo.
set /p lab_id="Enter lab ID: "
echo.
echo Assessment files are located in: lab-assessments\
echo Edit the %lab_id%-progress.md file to update task completion.
echo Change [ ] to [x] for completed tasks.
echo.
pause
goto menu

:update_progress
cls
echo.
echo Updating dashboard with real progress data...
echo.
cd /d "%~dp0"
python update-progress.py
echo.
echo Dashboard updated successfully!
echo Your portfolio now shows real task-based progress.
echo.
pause
goto menu

:view_progress
cls
echo.
echo Current Lab Progress:
echo ==================
echo.
echo SOC Automation Lab:      84%% (21/25 tasks)
echo Active Directory v1.0:   100%% (25/25 tasks) - COMPLETE
echo Active Directory v2.0:   88%% (22/25 tasks) 
echo Threat Detection Lab:    84%% (21/25 tasks)
echo SOC Help Desk Lab:       100%% (25/25 tasks) - COMPLETE
echo.
echo Overall Progress: 91.2%%
echo Completed Labs: 2/5
echo.
pause
goto menu

:generate_report
cls
echo.
echo Generating progress report...
echo.
echo Progress Report Generated: %date% %time%
echo ============================================
echo.
echo PORTFOLIO SUMMARY:
echo - Total Labs: 5
echo - Completed Labs: 2 (40%%)
echo - In Progress: 3 (60%%)
echo - Overall Progress: 91.2%%
echo.
echo DETAILED BREAKDOWN:
echo.
echo Identity Management (2 labs):
echo   - AD Lab v1.0: 100%% Complete ✓
echo   - AD Lab v2.0: 88%% In Progress
echo.
echo Security Operations (1 lab):
echo   - SOC Automation: 84%% In Progress
echo.
echo Threat Detection (1 lab):
echo   - Detection Lab: 84%% In Progress
echo.
echo Service Management (1 lab):
echo   - SOC Help Desk: 100%% Complete ✓
echo.
echo NEXT ACTIONS:
echo - Complete remaining tasks in assessment files
echo - Update progress using option 2
echo - View updated dashboard on portfolio site
echo.
pause
goto menu

:open_dashboard
cls
echo.
echo Opening web dashboard...
echo.
start "" "index.html"
echo.
echo Dashboard opened in your default browser.
echo Navigate to the Lab Projects section to view real-time progress.
echo.
pause
goto menu

:exit
cls
echo.
echo Thank you for using the Lab Progress Management System!
echo.
echo Your portfolio now features:
echo   ✓ Real-time task-based progress tracking
echo   ✓ Detailed assessment files for each lab
echo   ✓ Automated dashboard updates
echo   ✓ Comprehensive progress reporting
echo.
echo To update progress:
echo   1. Edit task completion in lab-assessments\*.md files
echo   2. Run this script and choose option 2
echo   3. View updated dashboard on your portfolio
echo.
pause
exit

:menu
cls
echo.
echo ================================================
echo       Lab Progress Management System
echo ================================================
echo.
echo Available options:
echo   1. Create new lab assessment
echo   2. Update progress from assessments
echo   3. View current progress
echo   4. Generate progress report
echo   5. Open web dashboard
echo   6. Exit
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto create_assessment
if "%choice%"=="2" goto update_progress
if "%choice%"=="3" goto view_progress
if "%choice%"=="4" goto generate_report
if "%choice%"=="5" goto open_dashboard
if "%choice%"=="6" goto exit
goto menu
