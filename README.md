# Sophie Redstone Studio

A cross-platform Minecraft redstone engineering toolkit with both a desktop GUI and a lightweight FastAPI backend.

## Features
- Redstone gate truth tables
- Comparator signal math
- Repeater pulse timing estimates
- Farm planning suggestions for mob, iron, gold, villager, and crop farms
- JSON export for calculations and plans
- Browser-based API/web version plus a desktop GUI

## Run the desktop app

1. Open a terminal in this folder.
2. Install dependencies:
   `python3 -m pip install -r requirements.txt`
3. Launch the desktop app:
   `python3 redstone_desktop.py`

## Build a Windows EXE

This repository includes a Windows build helper:
- `build_windows_exe.bat` for Command Prompt
- `build_windows_exe.ps1` for PowerShell

Run one of them on a Windows machine. The command used is:
`py -m PyInstaller --onefile --windowed --name SophieRedstoneStudio redstone_desktop.py`

## Run the web API version

1. Install dependencies:
   `python3 -m pip install -r requirements.txt`
2. Start the API:
   `python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000`
3. Open:
   `http://localhost:8000`

## Notes
The default configuration chosen here is a cross-platform PyQt desktop app with redstone planning tools, timing calculators, and farm optimization suggestions.
