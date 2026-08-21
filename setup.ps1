# ==============================================================================
# HACKBEN - 1-Line Automated Installer for Windows (PowerShell)
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
    Write-Host "[1/4] Mengunduh source code HACKBEN dari GitHub..." -ForegroundColor Cyan
    git clone https://github.com/dferdiantnn/fbhb.git $TargetDir
    Set-Location -Path $TargetDir
} else {
    Set-Location -Path $TargetDir
    Write-Host "[1/4] Memperbarui repositori ke versi terbaru..." -ForegroundColor Cyan
    git pull origin main
}

# 3. Buat Virtual Environment
Write-Host "[2/4] Menyiapkan Virtual Environment Python..." -ForegroundColor Cyan
if (-Not (Test-Path -Path "venv")) {
    python -m venv venv
}

# 4. Install Dependencies
Write-Host "[3/4] Mengunduh seluruh library & dependensi..." -ForegroundColor Cyan
& .\venv\Scripts\python.exe -m pip install --upgrade pip
& .\venv\Scripts\pip.exe install -r requirements.txt

# 5. Install Playwright Chromium Engine
Write-Host "[4/4] Memasang browser engine Chromium Playwright..." -ForegroundColor Cyan
& .\venv\Scripts\playwright.exe install chromium

Write-Host ""
Write-Host "==============================================================" -ForegroundColor Green
Write-Host "  ✅ SEMUA BAHAN SELESAI DI-DOWNLOAD! MEMULAI PROGRAM...       " -ForegroundColor Green
Write-Host "==============================================================" -ForegroundColor Green
Write-Host ""

# 6. Jalankan program
& .\venv\Scripts\python.exe main.py
