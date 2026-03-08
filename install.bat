@echo off
chcp 65001 >nul
echo Installation des dependances...
echo.
pip install -r requirements.txt
echo.
echo Installation terminée!
pause