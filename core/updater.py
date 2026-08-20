"""
Auto-Updater and Telemetry/Bridge Module for HACKBEN.
"""

import sys
import os
import subprocess
import urllib.request
import json
import time
from colorama import Fore

GITHUB_REPO_URL = "https://github.com/dferdiantnn/fbhb.git"
GITHUB_RAW_VERSION_URL = "https://raw.githubusercontent.com/dferdiantnn/fbhb/main/core/ui.py"
TELEMETRY_WEBHOOK_URL = ""  # Dapat diisi webhook Discord / Telegram / Server API kamu

def send_telemetry(event: str, store_name: str, session_num: int, total_sessions: int, status: str = "running", extra: str = "") -> None:
    """
    Send lightweight telemetry event to your remote bridge/webhook.
    Runs non-blockingly with low timeout so it never slows down the bot.
    """
    if not TELEMETRY_WEBHOOK_URL:
        # Fallback lokal / logger jika webhook belum diisi URL oleh owner
        return

    payload = {
        "event": event,
        "store": store_name,
        "session": f"{session_num}/{total_sessions}",
        "status": status,
        "extra": extra,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            TELEMETRY_WEBHOOK_URL,
            data=data,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "HACKBEN-Bridge/10.0"
            }
        )
        with urllib.request.urlopen(req, timeout=3) as _:
            pass
    except Exception:
        # Silent ignore agar bot utama tetap lancar jika jaringan offline
        pass


def check_for_updates() -> tuple[bool, str]:
    """
    Check GitHub repo for newer version.
    Returns (has_update, latest_version_string).
    """
    from core.ui import VERSION as CURRENT_VERSION
    try:
        req = urllib.request.Request(
            GITHUB_RAW_VERSION_URL,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            content = resp.read().decode("utf-8")
            for line in content.splitlines():
                if line.startswith("VERSION ="):
                    remote_ver = line.split("=")[1].strip().strip('"').strip("'")
                    if remote_ver != CURRENT_VERSION:
                        return True, remote_ver
                    return False, CURRENT_VERSION
    except Exception:
        pass
    return False, CURRENT_VERSION


def perform_auto_update() -> bool:
    """
    Pulls latest version from GitHub repository and replaces local files cleanly.
    """
    print(Fore.CYAN + "   [1/3] Memeriksa remote repository Git...")
    try:
        # If running inside a git cloned repo
        if os.path.exists(".git"):
            subprocess.run(["git", "fetch", "--all"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(Fore.CYAN + "   [2/3] Mengunduh pembaruan dan menimpa file lama...")
            subprocess.run(["git", "reset", "--hard", "origin/main"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["git", "clean", "-fd"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(Fore.GREEN + "   [3/3] Pembaruan berhasil diterapkan! File lama berhasil ditimpa.")
            return True
        else:
            # Fallback: Unduh archive zip langsung dari GitHub jika user download manual tanpa git
            print(Fore.YELLOW + "   [!] Repository .git tidak ditemukan. Menggunakan fast-pull script...")
            zip_url = "https://github.com/dferdiantnn/fbhb/archive/refs/heads/main.zip"
            import zipfile
            import io
            req = urllib.request.Request(zip_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                zip_data = resp.read()
            with zipfile.ZipFile(io.BytesIO(zip_data)) as z:
                # Extract all files stripping the top folder 'fbhb-main/'
                for member in z.namelist():
                    parts = member.split('/', 1)
                    if len(parts) > 1 and parts[1]:
                        target_path = parts[1]
                        if member.endswith('/'):
                            os.makedirs(target_path, exist_ok=True)
                        else:
                            os.makedirs(os.path.dirname(target_path), exist_ok=True)
                            with open(target_path, "wb") as outfile:
                                outfile.write(z.read(member))
            print(Fore.GREEN + "   [3/3] File berhasil diperbarui dan ditimpa dari GitHub!")
            return True
    except Exception as err:
        print(Fore.RED + f"   ❌ Gagal melakukan pembaruan otomatis: {err}")
        return False
