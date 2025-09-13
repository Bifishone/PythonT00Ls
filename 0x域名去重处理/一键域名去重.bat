@echo off
chcp 65001 > nul
echo.
python3 domain_duplicate_remover.py domains.txt
echo.
pause