#!/usr/bin/env bash
# ==============================================================================
# HACKBEN - 1-Line Automated Installer & Global Shortcut Setup (macOS & Linux)
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
    echo -e "\033[1;36m[1/5] Mengunduh source code HACKBEN dari GitHub...\033[0m"
    git clone https://github.com/dferdiantnn/fbhb.git "$TARGET_DIR"
    cd "$TARGET_DIR"
else
    cd "$TARGET_DIR"
    echo -e "\033[1;36m[1/5] Memperbarui repositori ke commit terbaru...\033[0m"
    git pull origin main || true
fi

ABS_PATH="$(pwd)"

# 3. Buat Virtual Environment
echo -e "\033[1;36m[2/5] Menyiapkan Virtual Environment Python...\033[0m"
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# 4. Install Dependencies
echo -e "\033[1;36m[3/5] Mengunduh seluruh paket dependensi (pip & library)...\033[0m"
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

# 5. Install Playwright Chromium Engine
echo -e "\033[1;36m[4/5] Memasang Playwright Chromium Engine...\033[0m"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    ./venv/bin/playwright install --with-deps chromium || ./venv/bin/playwright install chromium
else
    ./venv/bin/playwright install chromium
fi

# 6. Buat Perintah Global 'ferr' & Desktop Shortcut
echo -e "\033[1;36m[5/5] Membuat perintah pintasan instan 'ferr'...\033[0m"
mkdir -p "$HOME/.local/bin"
cat << EOF > "$HOME/.local/bin/ferr"
#!/usr/bin/env bash
clear
cd "$ABS_PATH" && source venv/bin/activate && python3 main.py
clear
EOF
chmod +x "$HOME/.local/bin/ferr"
cp "$HOME/.local/bin/ferr" "$HOME/.local/bin/hackben"

# Tambahkan alias ke shell config jika belum ada
for rc in "$HOME/.zshrc" "$HOME/.bashrc" "$HOME/.bash_profile"; do
    if [ -f "$rc" ]; then
        if ! grep -q "alias ferr=" "$rc"; then
            echo "alias ferr='cd $ABS_PATH && source venv/bin/activate && python3 main.py'" >> "$rc"
            echo "alias hackben='cd $ABS_PATH && source venv/bin/activate && python3 main.py'" >> "$rc"
        fi
    fi
done

# Buat shortcut di Desktop untuk macOS
if [ -d "$HOME/Desktop" ]; then
    cat << EOF > "$HOME/Desktop/FERR.command"
#!/usr/bin/env bash
cd "$ABS_PATH" && source venv/bin/activate && python3 main.py
EOF
    chmod +x "$HOME/Desktop/FERR.command"
    cp "$HOME/Desktop/FERR.command" "$HOME/Desktop/HACKBEN.command"
fi

echo -e "\033[1;32m"
echo "=============================================================="
echo "  ✅ INSTALASI SELESAI & SUDAH DIBUATKAN SHORTCUT OTOMATIS!   "
echo "  Mulai sekarang kamu cukup ketik: 'ferr' di Terminal,        "
echo "  atau dobel-klik shortcut 'FERR' di Desktop!                 "
echo "=============================================================="
echo -e "\033[0m"

# 7. Jalankan program
./venv/bin/python3 main.py
