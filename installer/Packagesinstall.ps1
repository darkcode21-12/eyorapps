# install_eyor_env.ps1
Write-Host "`n🛠️ Setting up Eyor Python environment..." -ForegroundColor Cyan

# STEP 1: Check if Python is installed
$pythonInstalled = Get-Command python -ErrorAction SilentlyContinue

if (-not $pythonInstalled) {
    Write-Host "🐍 Python not found. Downloading Python 3.11.6..." -ForegroundColor Yellow
    $pythonInstaller = "$env:TEMP\python-installer.exe"
    Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.11.6/python-3.11.6-amd64.exe" -OutFile $pythonInstaller

    Write-Host "📥 Installing Python silently..." -ForegroundColor Yellow
    Start-Process -Wait -FilePath $pythonInstaller -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1 Include_pip=1"
    Remove-Item $pythonInstaller -Force
    Write-Host "✅ Python installed and added to PATH." -ForegroundColor Green
} else {
    Write-Host "✅ Python is already installed." -ForegroundColor Green
}

# STEP 2: Upgrade pip and install modules
$modules = @(
    "pyinstaller",
    "playsound",
    "Pillow",
    "customtkinter",
    "requests",
    "urllib3",
    "winshell",
    "pywin32"
)

Write-Host "`n⬆️ Upgrading pip..." -ForegroundColor Cyan
python -m ensurepip --upgrade
python -m pip install --upgrade pip

# STEP 3: Install required modules
foreach ($module in $modules) {
    Write-Host "📦 Installing $module..." -ForegroundColor Magenta
    python -m pip install $module
}

Write-Host "`n✅ All modules installed successfully!" -ForegroundColor Green
