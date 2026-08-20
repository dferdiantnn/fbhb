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
    node_name = platform.node() or "Unknown-Host"
    system_os = platform.system()
    release = platform.release()
    return f"{node_name} ({system_os} {release})"

def send_telegram_alert(text: str) -> None:
    """Send real-time alert text to Telegram bot non-blockingly."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return

    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = urllib.parse.urlencode({
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text,
            "parse_mode": "Markdown"
        }).encode("utf-8")
        
        req = urllib.request.Request(url, data=payload, headers={"User-Agent": "HACKBEN-Telemetry/10.0"})
        with urllib.request.urlopen(req, timeout=4) as _:
            pass
    except Exception:
        pass


def send_telegram_photo(image_bytes: bytes, caption: str) -> None:
    """Send debug failure screenshot to Telegram bot."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return

    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        boundary = "----HackbenBoundary" + str(int(time.time()))
        
        body = bytearray()
        # chat_id field
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(b'Content-Disposition: form-data; name="chat_id"\r\n\r\n')
        body.extend(f"{TELEGRAM_CHAT_ID}\r\n".encode())
        
        # caption field
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(b'Content-Disposition: form-data; name="caption"\r\n\r\n')
        body.extend(caption.encode())
        body.extend(b"\r\n")

        # photo file
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(b'Content-Disposition: form-data; name="photo"; filename="error_debug.png"\r\n')
        body.extend(b"Content-Type: image/png\r\n\r\n")
        body.extend(image_bytes)
        body.extend(b"\r\n")
        body.extend(f"--{boundary}--\r\n".encode())

        req = urllib.request.Request(
            url,
            data=body,
            headers={
                "Content-Type": f"multipart/form-data; boundary={boundary}",
                "User-Agent": "HACKBEN-Telemetry/10.0"
            }
        )
        with urllib.request.urlopen(req, timeout=10) as _:
            pass
    except Exception:
        pass


def send_telemetry(event: str, store_name: str, session_num: int, total_sessions: int, status: str = "running", extra: str = "", screenshot_bytes: bytes | None = None) -> None:
    """Send structured telemetry data to Telegram."""
    device_info = get_system_identity()

    if event == "start_session":
        msg = (
            f"🚀 *[HACKBEN BOT STARTED]*\n"
            f"💻 *Perangkat:* `{device_info}`\n"
            f"🏢 *Store Target:* `{store_name}`\n"
            f"📊 *Total Antrean:* `{total_sessions} Sesi`\n"
            f"⚙️ *Layanan:* `{extra}`\n"
            f"⏰ *Waktu Mulai:* `{time.strftime('%Y-%m-%d %H:%M:%S')}`"
        )
        send_telegram_alert(msg)

    elif event == "session_progress":
        if status == "success":
            msg = (
                f"✅ *[SESI {session_num}/{total_sessions} BERHASIL]*\n"
                f"💻 *Perangkat:* `{device_info}`\n"
                f"🏢 *Store:* `{store_name}`\n"
                f"⏰ *Waktu:* `{time.strftime('%H:%M:%S')}`"
            )
            send_telegram_alert(msg)
        else:
            caption = (
                f"❌ *[DEBUG ERROR: SESI {session_num}/{total_sessions}]*\n"
                f"💻 *Perangkat:* `{device_info}`\n"
                f"🏢 *Store:* `{store_name}`\n"
                f"⚠️ *Error:* `{extra[:120]}`\n"
                f"⏰ *Waktu:* `{time.strftime('%H:%M:%S')}`"
            )
            if screenshot_bytes:
                send_telegram_photo(screenshot_bytes, caption)
            else:
                send_telegram_alert(caption)

    elif event == "finish_session":
        msg = (
            f"🏁 *[PENUGASAN SELESAI]*\n"
            f"💻 *Perangkat:* `{device_info}`\n"
            f"🏢 *Store:* `{store_name}`\n"
            f"📊 *Hasil Akhir:* `{session_num}/{total_sessions} Sukses`\n"
            f"⏰ *Waktu Selesai:* `{time.strftime('%Y-%m-%d %H:%M:%S')}`"
        )
        send_telegram_alert(msg)


def check_and_apply_auto_update_on_launch() -> None:
    """Silent auto-update checker on startup."""
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
                            os.execv(sys.executable, [sys.executable] + sys.argv)
                    return
    except Exception:
        pass


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
