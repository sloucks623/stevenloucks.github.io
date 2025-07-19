@echo off
echo ======================================
echo  Lab Dashboard Rollback Script
echo ======================================
echo.

echo This script will help you rollback the lab dashboard changes
echo if you need to revert to the original state.
echo.

echo ROLLBACK OPTIONS:
echo.
echo 1. Remove lab dashboard from index.html
echo 2. Remove lab dashboard from labs.html  
echo 3. Delete lab dashboard files
echo 4. Full rollback (all of the above)
echo 5. Cancel
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto remove_index
if "%choice%"=="2" goto remove_labs
if "%choice%"=="3" goto delete_files
if "%choice%"=="4" goto full_rollback
if "%choice%"=="5" goto cancel

echo Invalid choice. Please run the script again.
pause
exit

:remove_index
echo Removing dashboard from index.html...
git checkout HEAD -- index.html
echo Done! index.html has been restored to its previous state.
pause
exit

:remove_labs
echo Removing dashboard from labs.html...
git checkout HEAD -- labs.html
echo Done! labs.html has been restored to its previous state.
pause
exit

:delete_files
echo Deleting lab dashboard files...
if exist "test-dashboard.html" del "test-dashboard.html"
if exist "js\lab-dashboard.js" git checkout HEAD -- js\lab-dashboard.js
if exist "css\lab-status-widget.css" git checkout HEAD -- css\lab-status-widget.css
echo Done! Dashboard files have been cleaned up.
pause
exit

:full_rollback
echo Performing full rollback...
git checkout HEAD -- index.html
git checkout HEAD -- labs.html
git checkout HEAD -- js\lab-dashboard.js
git checkout HEAD -- css\lab-status-widget.css
if exist "test-dashboard.html" del "test-dashboard.html"
echo.
echo Full rollback complete! All changes have been reverted.
echo Your portfolio is back to its original state.
pause
exit

:cancel
echo Rollback cancelled.
pause
exit
