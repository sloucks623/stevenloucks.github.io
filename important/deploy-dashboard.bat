@echo off
echo Deploying dashboard button changes...
echo.

cd /d "c:\Users\New User\stevenloucks.github.io"

echo Adding all files...
git add .

echo Committing changes...
git commit -m "Deploy dashboard button - urgent fix"

echo Pushing to GitHub...
git push origin main --force

echo.
echo Dashboard button should now be live!
echo Check: https://stevenloucks.tech
pause
