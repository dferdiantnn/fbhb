"""
Auto-Updater and Telegram Telemetry Bridge for HACKBEN.
"""

import sys
import os
import platform
import subprocess
import urllib.request
import urllib.parse
import json
import time
from colorama import Fore

GITHUB_REPO_URL = "https://github.com/dferdiantnn/fbhb.git"
GITHUB_RAW_VERSION_URL = "https://raw.githubusercontent.com/dferdiantnn/fbhb/main/core/ui.py"

import base64

# --- TELEGRAM BOT CONFIGURATION ---
_ENC_TOKEN = "ODc1NTUyNzMzMTpBQUVwelBPbUl0UlFQd1d4eVFkTHNmNVlaYm5VV1h4MXEwMA=="
TELEGRAM_BOT_TOKEN = base64.b64decode(_ENC_TOKEN).decode("utf-8")
TELEGRAM_CHAT_ID = "1991475833"

def get_system_identity() -> str:
    """Return friendly host device name and OS info."""
    node_name = platform.node() or "Laptop-Operator"
    system_os = platform.system()
    machine = platform.machine()
    return f"{node_name} ({system_os} - {machine})"

def send_telegram_alert(text: str, inline_keyboard: list | None = None) -> None:
    """Send real-time alert text to Telegram bot reliably with plain text fallback."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return

    try:
        import requests
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload_dict = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text,
            "parse_mode": "Markdown"
        }
        if inline_keyboard:
            payload_dict["reply_markup"] = json.dumps({"inline_keyboard": inline_keyboard})

        resp = requests.post(url, data=payload_dict, timeout=8)
        if resp.status_code != 200:
            # Fallback without markdown formatting
            payload_dict.pop("parse_mode", None)
            requests.post(url, data=payload_dict, timeout=8)
    except Exception:
        pass


def send_telegram_photo(image_bytes: bytes, caption: str, inline_keyboard: list | None = None) -> None:
    """Send debug failure screenshot to Telegram bot with plain text fallback."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return

    try:
        import requests
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "caption": caption,
            "parse_mode": "Markdown"
        }
        if inline_keyboard:
            data["reply_markup"] = json.dumps({"inline_keyboard": inline_keyboard})

        files = {
            "photo": ("error_debug.png", image_bytes, "image/png")
        }

        resp = requests.post(url, data=data, files=files, timeout=12)
        if resp.status_code != 200:
            # Fallback without markdown parsing in caption
            data.pop("parse_mode", None)
            requests.post(url, data=data, files=files, timeout=12)
    except Exception:
        pass


def send_operational_report(store_name: str, service_type: str, sukses_count: int, total_sessions: int, errors_summary: list | None = None, last_error_screenshot: bytes | None = None) -> None:
    """
    Send clean single operational report to Telegram without spamming single sessions.
    """
    device_info = get_system_identity()
    status_text = f"Selesai ({sukses_count}/{total_sessions} Berhasil)"
    if sukses_count < total_sessions:
        gagal_count = total_sessions - sukses_count
        status_text = f"Selesai ({sukses_count}/{total_sessions} Berhasil, {gagal_count} Gagal)"

    msg = (
        f"📊 *LOG OPERASIONAL HACKBEN*\n"
        f"```\n"
        f"Perangkat : {device_info}\n"
        f"Store     : {store_name}\n"
        f"Layanan   : {service_type}\n"
        f"Status    : {status_text}\n"
        f"Waktu     : {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"```"
    )

    if errors_summary:
        clean_err = errors_summary[-1].replace("*", "").replace("`", "")[:120]
        msg += f"\n⚠️ *Kendala:* `{clean_err}`"

    if last_error_screenshot and sukses_count < total_sessions:
        send_telegram_photo(last_error_screenshot, msg)
    else:
        send_telegram_alert(msg)


def check_and_apply_auto_update_on_launch() -> None:
    """
    Visibly checks GitHub repo on launch so user can see it in terminal.
    Automatically updates and restarts if a new version is found.
    """
    from core.ui import VERSION as CURRENT_VERSION
    sys.stdout.write(Fore.CYAN + "   [🔄] Memeriksa pembaruan repository GitHub... ")
    sys.stdout.flush()

    try:
        req = urllib.request.Request(
            GITHUB_RAW_VERSION_URL,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=4) as resp:
            content = resp.read().decode("utf-8")
            remote_ver = None
            for line in content.splitlines():
                if line.startswith("VERSION ="):
                    remote_ver = line.split("=")[1].strip().strip('"').strip("'")
                    break

            if remote_ver and remote_ver != CURRENT_VERSION:
                sys.stdout.write(Fore.YELLOW + f"Update Ditemukan! ({remote_ver})\n")
                print(Fore.CYAN + f"   [⚡] Mengunduh pembaruan terbaru dari GitHub...")
                if perform_auto_update():
                    print(Fore.GREEN + "   [✔] Update selesai diterapkan! Memulai ulang program...")
                    time.sleep(1)
                    os.execv(sys.executable, [sys.executable] + sys.argv)
                return
            else:
                sys.stdout.write(Fore.GREEN + f"Versi Terkini ({CURRENT_VERSION})\n")
    except Exception:
        sys.stdout.write(Fore.YELLOW + "Offline / Melewati cek update.\n")


def perform_auto_update() -> bool:
    """Pulls latest version from GitHub repository and replaces local files."""
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
