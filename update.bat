echo Don't use this file unless you're making GUI changes.
pause

echo Please use sync.bat if you are just adding saves.
pause

git add .
git commit -m "Update GUI"
git push -u origin master