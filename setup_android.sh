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

echo -e "\033[1;36m[3/4] Memasang Python, Playwright, dan Chromium di dalam Ubuntu (Cepat & Ringan)...\033[0m"
proot-distro login ubuntu -- bash -c "
    export DEBIAN_FRONTEND=noninteractive
    export TZ=Asia/Jakarta
    apt update -y &&
    apt install -y --no-install-recommends python3 python3-pip python3-venv git curl chromium-browser tzdata &&
    if [ ! -d '/root/hackben' ]; then
        git clone https://github.com/dferdiantnn/fbhb.git /root/hackben
    else
        cd /root/hackben && git pull origin main
    fi &&
    cd /root/hackben &&
    python3 -m venv venv &&
    ./venv/bin/pip install --upgrade pip &&
    ./venv/bin/pip install -r requirements.txt &&
    (./venv/bin/playwright install --with-deps chromium || ./venv/bin/playwright install chromium) &&
    apt-get clean && rm -rf /var/lib/apt/lists/* /root/.cache ~/.cache /tmp/*
"

# Bersihkan cache installer rootfs di Termux host agar hemat storage
proot-distro clear-cache 2>/dev/null
pkg clean 2>/dev/null

echo -e "\033[1;36m[4/4] Membuat perintah pintasan 'ferr' di Termux...\033[0m"
cat << 'EOF' > "$PREFIX/bin/ferr"
#!/usr/bin/env bash
clear
proot-distro login ubuntu -- bash -c "cd /root/hackben && source venv/bin/activate && python3 main.py"
EXIT_CODE=$?

if [ $EXIT_CODE -eq 99 ] || [ -f "$PREFIX/var/lib/proot-distro/installed-rootfs/ubuntu/tmp/.hackben_destruct" ]; then
    echo -e "\033[1;31m\n[💥] Melenyapkan sub-sistem Ubuntu dan membersihkan Termux (Auto-Wipe 100%)...\033[0m"
    yes y | proot-distro remove ubuntu 2>/dev/null || proot-distro remove ubuntu 2>/dev/null
    proot-distro clear-cache 2>/dev/null
    pkg clean 2>/dev/null
    rm -rf "$PREFIX/bin/ferr" "$PREFIX/bin/hackben" "$PREFIX/tmp/*" "$HOME/.cache"
    echo -e "\033[1;32m[✔] Penghancuran total tuntas 100%! Memori penyimpanan HP telah bersih sempurna.\033[0m\n"
    exit 0
fi
clear
EOF
chmod +x "$PREFIX/bin/ferr"
cp "$PREFIX/bin/ferr" "$PREFIX/bin/hackben"

echo -e "\033[1;32m"
echo "=============================================================="
echo "  ✅ INSTALASI SELESAI & SUDAH 100% SIAP PAKAI!               "
echo "  Mulai sekarang kamu cukup ketik: ferr lalu tekan Enter!     "
echo "=============================================================="
echo -e "\033[0m"
