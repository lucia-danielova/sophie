@echo off
setlocal

echo === Sophie Redstone Studio installer ===
where py >nul 2>nul
if errorlevel 1 (
    echo Python was not found on PATH.
    echo Please install Python 3.10+ from https://www.python.org/downloads/windows/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo Installing dependencies...
py -m pip install --upgrade pip
py -m pip install PyQt5 PyInstaller

echo Building desktop application...
py -m PyInstaller --onefile --windowed --name SophieRedstoneStudio redstone_desktop.py

echo.
echo Build complete.
echo Check the dist folder for SophieRedstoneStudio.exe
pause
