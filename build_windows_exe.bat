@echo off
py -m pip install PyQt5 PyInstaller
py -m PyInstaller --onefile --windowed --name SophieRedstoneStudio redstone_desktop.py
pause
