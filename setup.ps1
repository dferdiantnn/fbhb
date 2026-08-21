# ==============================================================================
# HACKBEN - 1-Line Automated Installer & Global Shortcut Setup (Windows)
# ==============================================================================

Write-Host ""
Write-Host "  🍱 =============================================== 🥢" -ForegroundColor Green
Write-Host "         HACKBEN - 1-LINE INSTALLER (WINDOWS)          " -ForegroundColor Green
Write-Host "  🍱 =============================================== 🥢" -ForegroundColor Green
Write-Host ""

# 1. Pastikan Execution Policy mengizinkan script
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force -ErrorAction SilentlyContinue

# 2. Clone atau Masuk ke Direktori Project
$TargetDir = "hackben"
if (-Not (Test-Path -Path $TargetDir)) {
    Write-Host "[1/5] Mengunduh source code HACKBEN dari GitHub..." -ForegroundColor Cyan
    git clone https://github.com/dferdiantnn/fbhb.git $TargetDir
    Set-Location -Path $TargetDir
} else {
    Set-Location -Path $TargetDir
    Write-Host "[1/5] Memperbarui repositori ke versi terbaru..." -ForegroundColor Cyan
    git pull origin main
}

$AbsPath = (Get-Location).Path

# 3. Buat Virtual Environment
Write-Host "[2/5] Menyiapkan Virtual Environment Python..." -ForegroundColor Cyan
if (-Not (Test-Path -Path "venv")) {
    python -m venv venv
}

# 4. Install Dependencies
Write-Host "[3/5] Mengunduh seluruh library & dependensi..." -ForegroundColor Cyan
& .\venv\Scripts\python.exe -m pip install --upgrade pip
& .\venv\Scripts\pip.exe install -r requirements.txt

# 5. Install Playwright Chromium Engine
Write-Host "[4/5] Memasang browser engine Chromium Playwright..." -ForegroundColor Cyan
& .\venv\Scripts\playwright.exe install chromium

# 6. Buat Global Shortcut 'hackben' & Desktop Shortcut Icon
Write-Host "[5/5] Membuat shortcut otomatis 'hackben'..." -ForegroundColor Cyan

# Simpan hackben.cmd di WindowsApps (otomatis masuk PATH bawaan Windows)
$WinAppsPath = "$env:LOCALAPPDATA\Microsoft\WindowsApps\hackben.cmd"
$CmdContent = "@echo off`r`ncd /d `"$AbsPath`"`r`ncall venv\Scripts\activate`r`npython main.py"
Set-Content -Path $WinAppsPath -Value $CmdContent -Force -ErrorAction SilentlyContinue

# Buat Desktop Shortcut Icon
$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::Desktop)
$Shortcut = $WshShell.CreateShortcut("$DesktopPath\HACKBEN.lnk")
$Shortcut.TargetPath = "$AbsPath\install.bat"
$Shortcut.WorkingDirectory = "$AbsPath"
$Shortcut.WindowStyle = 1
$Shortcut.Description = "HACKBEN Automation Suite"
$Shortcut.Save()

Write-Host ""
Write-Host "==============================================================" -ForegroundColor Green
Write-Host "  ✅ INSTALASI SELESAI & SUDAH DIBUATKAN SHORTCUT OTOMATIS!   " -ForegroundColor Green
Write-Host "  Mulai sekarang kamu cukup ketik: 'hackben' di CMD/PowerShell," -ForegroundColor Green
Write-Host "  atau dobel-klik icon 'HACKBEN' di Desktop!                  " -ForegroundColor Green
Write-Host "==============================================================" -ForegroundColor Green
Write-Host ""

# 7. Jalankan program
& .\venv\Scripts\python.exe main.py
