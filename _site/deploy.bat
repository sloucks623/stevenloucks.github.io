@echo off
echo Setting up Git repository and pushing changes...
echo.

:: Initialize git if not already done
git init

:: Add the correct remote
git remote remove origin 2>nul
git remote add origin https://github.com/sloucks623/stevenloucks.github.io.git

:: Set the default branch to main
git branch -M main

:: Add all files
git add .

:: Commit the changes
git commit -m "Update portfolio with profile photo, theme toggle, and modern design"

:: Push to GitHub
git push -u origin main

echo.
echo Done! Your changes should now be live at https://stevenloucks.github.io
echo It may take a few minutes for GitHub Pages to update.
pause
