@echo off
chcp 65001 > nul
echo.
:new
python3 CodeFinder.py 
echo.
echo 点击回车，继续搜索！！!
pause > nul
echo.
goto new
echo.
pause