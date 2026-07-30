@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel% equ 0 (
    py -3.12 KAYNAGI_CIKAR.py
) else (
    python KAYNAGI_CIKAR.py
)

if errorlevel 1 (
    echo.
    echo Kaynak kodu cikarilamadi. Yukaridaki hatayi kontrol et.
    pause
    exit /b 1
)

echo.
echo Kaynak kodu hazir. Degisiklikleri GitHub'a yazmak icin:
echo git add -A
echo git commit -m "feat: add v1.4.1 source"
echo git push
pause
