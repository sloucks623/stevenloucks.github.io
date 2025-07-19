@echo off
echo ======================================
echo  Lab Assessment Generator
echo ======================================
echo.

echo This tool helps you create detailed lab assessments using ChatGPT
echo and track your real progress through cybersecurity labs.
echo.

echo USAGE OPTIONS:
echo.
echo 1. Create assessment from tutorial file
echo 2. Create assessment from tutorial URL  
echo 3. Create assessment with manual input
echo 4. Update dashboard with current progress
echo 5. Cancel
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto file_input
if "%choice%"=="2" goto url_input
if "%choice%"=="3" goto manual_input
if "%choice%"=="4" goto update_dashboard
if "%choice%"=="5" goto cancel

echo Invalid choice. Please run the script again.
pause
exit

:file_input
set /p lab_name="Enter lab name: "
set /p file_path="Enter path to tutorial file: "
echo.
echo Creating assessment for "%lab_name%" from file...
python lab-assessment-generator.py --lab-name "%lab_name%" --tutorial-file "%file_path%"
goto end

:url_input
set /p lab_name="Enter lab name: "
set /p url="Enter tutorial URL: "
echo.
echo Creating assessment for "%lab_name%" from URL...
python lab-assessment-generator.py --lab-name "%lab_name%" --tutorial-url "%url%"
goto end

:manual_input
set /p lab_name="Enter lab name: "
echo.
echo Creating template assessment for "%lab_name%"...
echo You can edit the generated files to add specific details.
python lab-assessment-generator.py --lab-name "%lab_name%"
goto end

:update_dashboard
echo.
echo Updating dashboard with current progress...
python lab-assessment-generator.py --update-dashboard
goto end

:cancel
echo Assessment cancelled.
pause
exit

:end
echo.
echo ======================================
echo  Assessment Complete!
echo ======================================
echo.
echo FILES CREATED:
echo - Assessment template (lab-name-template.json)
echo - Progress tracker (lab-name-progress.json)
echo.
echo HOW TO USE:
echo 1. Edit the progress tracker as you work through the lab
echo 2. Mark tasks as completed and add notes
echo 3. Run this script again with option 4 to update dashboard
echo.
echo NEXT STEPS:
echo - Check the lab-assessments folder for your files
echo - Start working through your lab and updating progress
echo - Your dashboard will show real completion percentages
echo.
pause
