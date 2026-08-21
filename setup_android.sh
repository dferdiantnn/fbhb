#!/usr/bin/env bash
# ==============================================================================
# HACKBEN - 1-Line Automated Installer for Android (Termux Environment)
# ==============================================================================

set -e

echo -e "\033[1;32m"
echo "  🍱 =============================================== 🥢"
echo "       HACKBEN - 1-LINE INSTALLER FOR ANDROID TERMUX"
echo "  🍱 =============================================== 🥢"
echo -e "\033[0m"

echo -e "\033[1;36m[1/4] Mempersiapkan repositori & paket dasar Termux...\033[0m"
pkg update -y
pkg install -y git proot-distro curl

echo -e "\033[1;36m[2/4] Menyiapkan sub-sistem Ubuntu Linux ARM64...\033[0m"
if ! proot-distro list | grep -q "ubuntu (installed)"; then
    proot-distro install ubuntu
fi

echo -e "\033[1;36m[3/4] Memasang Python, Playwright, dan Chromium di dalam Ubuntu...\033[0m"
proot-distro login ubuntu -- bash -c "
    apt update -y &&
    apt install -y python3 python3-pip python3-venv git chromium-browser libnss3 libatk-bridge2.0-0 libgtk-3-0 libasound2 libxss1 libx11-xcb1 &&
    if [ ! -d '/root/hackben' ]; then
        git clone https://github.com/dferdiantnn/fbhb.git /root/hackben
    else
        cd /root/hackben && git pull origin main
    fi &&
    cd /root/hackben &&
    python3 -m venv venv &&
    ./venv/bin/pip install --upgrade pip &&
    ./venv/bin/pip install -r requirements.txt &&
    ./venv/bin/playwright install chromium
"

echo -e "\033[1;36m[4/4] Membuat perintah pintasan 'ferr' di Termux...\033[0m"
cat << 'EOF' > "$PREFIX/bin/ferr"
#!/usr/bin/env bash
proot-distro login ubuntu -- bash -c "cd /root/hackben && source venv/bin/activate && python3 main.py"
EOF
chmod +x "$PREFIX/bin/ferr"
cp "$PREFIX/bin/ferr" "$PREFIX/bin/hackben"

echo -e "\033[1;32m"
echo "=============================================================="
echo "  ✅ INSTALASI SELESAI! "
echo "  Mulai sekarang kamu cukup ketik: 'ferr' di Termux."
echo "=============================================================="
echo -e "\033[0m"

# Langsung jalankan aplikasi
hackben
