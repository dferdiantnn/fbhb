#!/usr/bin/env bash
# ==============================================================================
# HACKBEN - 1-Line Automated Installer for macOS & Linux
# ==============================================================================

set -e

echo -e "\033[1;32m"
echo "  🍱 =============================================== 🥢"
echo "        HACKBEN - 1-LINE INSTALLER (macOS & Linux)     "
echo "  🍱 =============================================== 🥢"
echo -e "\033[0m"

# 1. Pastikan Git & Python3 terinstall
if ! command -v git &> /dev/null; then
    echo -e "\033[1;31m[!] Git belum terpasang. Harap pasang Git terlebih dahulu.\033[0m"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo -e "\033[1;31m[!] Python3 belum terpasang. Harap pasang Python3 terlebih dahulu.\033[0m"
    exit 1
fi

# 2. Clone atau Masuk ke Direktori Project
TARGET_DIR="hackben"
if [ ! -d "$TARGET_DIR" ]; then
    echo -e "\033[1;36m[1/4] Mengunduh source code HACKBEN dari GitHub...\033[0m"
    git clone https://github.com/dferdiantnn/fbhb.git "$TARGET_DIR"
    cd "$TARGET_DIR"
else
    cd "$TARGET_DIR"
    echo -e "\033[1;36m[1/4] Memperbarui repositori ke commit terbaru...\033[0m"
    git pull origin main || true
fi

# 3. Buat Virtual Environment
echo -e "\033[1;36m[2/4] Menyiapkan Virtual Environment Python...\033[0m"
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# 4. Install Dependencies
echo -e "\033[1;36m[3/4] Mengunduh seluruh paket dependensi (pip & library)...\033[0m"
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

# 5. Install Playwright Chromium Engine
echo -e "\033[1;36m[4/4] Memasang Playwright Chromium Engine...\033[0m"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    ./venv/bin/playwright install --with-deps chromium || ./venv/bin/playwright install chromium
else
    ./venv/bin/playwright install chromium
fi

echo -e "\033[1;32m"
echo "=============================================================="
echo "  ✅ SEMUA BAHAN BERHASIL DI-DOWNLOAD! MEMULAI PROGRAM...     "
echo "=============================================================="
echo -e "\033[0m"

# 6. Jalankan program
./venv/bin/python3 main.py
