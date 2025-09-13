@echo off
chcp 65001 > nul
echo.
python3 FileComparer.py --case1 ips_only.txt --case2 fofa_ips.txt
echo.
pause