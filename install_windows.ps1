Write-Host "=== Sophie Redstone Studio installer ==="

$python = Get-Command py -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "Python was not found on PATH."
    Write-Host "Install Python 3.10+ from https://www.python.org/downloads/windows/ and enable 'Add Python to PATH'."
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Installing dependencies..."
py -m pip install --upgrade pip
py -m pip install PyQt5 PyInstaller

Write-Host "Building desktop application..."
py -m PyInstaller --onefile --windowed --name SophieRedstoneStudio redstone_desktop.py

Write-Host "Build complete. Check the dist folder for SophieRedstoneStudio.exe"
Read-Host "Press Enter to close"
