@echo off
setlocal
if exist dist\SophieRedstoneStudio.exe (
    start "" "%~dp0dist\SophieRedstoneStudio.exe"
) else (
    echo SophieRedstoneStudio.exe was not found.
    echo Run install_windows.bat first.
    pause
)
