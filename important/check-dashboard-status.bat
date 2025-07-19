@echo off
echo ======================================
echo  Lab Dashboard Status Check
echo ======================================
echo.

echo CURRENT STATUS:
echo.

echo Files that exist:
if exist "index.html" echo [✓] index.html - Main portfolio page
if exist "labs.html" echo [✓] labs.html - Dedicated labs page  
if exist "test-dashboard.html" echo [✓] test-dashboard.html - Test preview page
if exist "js\lab-dashboard.js" echo [✓] js\lab-dashboard.js - Dashboard logic
if exist "css\lab-status-widget.css" echo [✓] css\lab-status-widget.css - Widget styles
if exist "data\lab-status.json" echo [✓] data\lab-status.json - Lab data
if exist "data\dashboard-summary.json" echo [✓] data\dashboard-summary.json - Summary data

echo.
echo FILES TO TEST:
echo.
echo 1. Open test-dashboard.html in browser (shows real lab data)
echo 2. Open index.html in browser (main portfolio with lab widgets)
echo 3. Open labs.html in browser (dedicated labs page)
echo.

echo ROLLBACK SAFETY:
echo.
echo - Run rollback-dashboard.bat if you need to undo changes
echo - All changes are local until you commit to Git
echo - Your automation scripts are unchanged and safe
echo.

echo NEXT STEPS:
echo.
echo 1. Test the dashboard files in your browser
echo 2. If satisfied, you can commit changes with Git
echo 3. If not satisfied, use the rollback script
echo.

pause
