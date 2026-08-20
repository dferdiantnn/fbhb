"""
Auto-Updater and Telegram Telemetry Bridge for HACKBEN.
"""

import sys
import os
import subprocess
import urllib.request
import urllib.parse
import json
import time
from colorama import Fore

GITHUB_REPO_URL = "https://github.com/dferdiantnn/fbhb.git"
GITHUB_RAW_VERSION_URL = "https://raw.githubusercontent.com/dferdiantnn/fbhb/main/core/ui.py"

# --- TELEGRAM BOT CONFIGURATION ---
TELEGRAM_BOT_TOKEN = "8755527331:AAEpzPOmItRQPwWxyQdLsf5YZbnUWXx1q00"
TELEGRAM_CHAT_ID = "1991475833"

def send_telegram_alert(text: str) -> None:
    """Send real-time alert to Telegram bot non-blockingly."""
    if not TELEGRAM_BOT_TOKEN or "YOUR_TOKEN" in TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID or "YOUR_CHAT_ID" in TELEGRAM_CHAT_ID:
        return

    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = urllib.parse.urlencode({
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text,
            "parse_mode": "Markdown"
        }).encode("utf-8")
        
        req = urllib.request.Request(url, data=payload, headers={"User-Agent": "HACKBEN-Telemetry/10.0"})
        with urllib.request.urlopen(req, timeout=3) as _:
            pass
    except Exception:
        pass


def send_telemetry(event: str, store_name: str, session_num: int, total_sessions: int, status: str = "running", extra: str = "") -> None:
    """Send structured telemetry data to Telegram."""
    if event == "start_session":
        msg = (
            f"🚀 *[HACKBEN BOT STARTED]*\n"
            f"🏢 *Store Target:* `{store_name}`\n"
            f"📊 *Total Sesi:* `{total_sessions}`\n"
            f"⚙️ *Konfigurasi:* `{extra}`\n"
            f"⏰ *Waktu:* `{time.strftime('%Y-%m-%d %H:%M:%S')}`"
        )
    elif event == "session_progress":
        icon = "✅" if status == "success" else "❌"
        msg = (
            f"{icon} *[PROGRESS SESI {session_num}/{total_sessions}]*\n"
            f"🏢 *Store:* `{store_name}`\n"
            f"📡 *Status:* `{status.upper()}`\n"
            f"⏰ *Waktu:* `{time.strftime('%H:%M:%S')}`"
        )
    elif event == "finish_session":
        msg = (
            f"🏁 *[MISSION COMPLETED]*\n"
            f"🏢 *Store:* `{store_name}`\n"
            f"🎉 *Total Sukses:* `{session_num}/{total_sessions}`\n"
            f"⏰ *Waktu Selesai:* `{time.strftime('%Y-%m-%d %H:%M:%S')}`"
        )
    else:
        msg = f"ℹ️ *[EVENT]* `{event}` - Store: `{store_name}` ({status})"

    send_telegram_alert(msg)


def check_and_apply_auto_update_on_launch() -> None:
    """
    Silent & Fast Auto-Update Checker upon application startup.
    If a newer version exists on GitHub, automatically pulls and replaces files,
    then seamlessly restarts. If up to date, silently proceeds immediately.
    """
    from core.ui import VERSION as CURRENT_VERSION
    try:
        req = urllib.request.Request(
            GITHUB_RAW_VERSION_URL,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            content = resp.read().decode("utf-8")
            for line in content.splitlines():
                if line.startswith("VERSION ="):
                    remote_ver = line.split("=")[1].strip().strip('"').strip("'")
                    if remote_ver != CURRENT_VERSION:
                        print(Fore.CYAN + f"\n   [🔄] Pembaruan terdeteksi: {remote_ver} (Versi Lokal: {CURRENT_VERSION})")
                        print(Fore.YELLOW + "   [⚡] Mengunduh dan menerapkan update terbaru dari GitHub...")
                        if perform_auto_update():
                            print(Fore.GREEN + "   [✔] Update selesai diterapkan! Memulai ulang program...")
                            time.sleep(1)
                            # Restart script with original arguments
                            os.execv(sys.executable, [sys.executable] + sys.argv)
                    return
    except Exception:
        pass


def perform_auto_update() -> bool:
    """
    Pulls latest version from GitHub repository and replaces local files cleanly.
    """
    try:
        if os.path.exists(".git"):
            subprocess.run(["git", "fetch", "--all"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["git", "reset", "--hard", "origin/main"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["git", "clean", "-fd"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        else:
            zip_url = "https://github.com/dferdiantnn/fbhb/archive/refs/heads/main.zip"
            import zipfile
            import io
            req = urllib.request.Request(zip_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                zip_data = resp.read()
            with zipfile.ZipFile(io.BytesIO(zip_data)) as z:
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
            return True
    except Exception:
        return False
