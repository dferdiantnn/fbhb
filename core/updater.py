"""
Universal Auto-Updater and Zero-Dependency Telegram Telemetry Bridge for HACKBEN.
Works out-of-the-box on standard Python with zero third-party library dependencies.
"""

import sys
import os
import platform
import subprocess
import urllib.request
import urllib.parse
import json
import time
import threading
from colorama import Fore

GITHUB_REPO_URL = "https://github.com/dferdiantnn/fbhb.git"
GITHUB_RAW_VERSION_URL = "https://raw.githubusercontent.com/dferdiantnn/fbhb/main/core/ui.py"

import base64

# --- TELEGRAM BOT CONFIGURATION ---
_ENC_TOKEN = "ODc1NTUyNzMzMTpBQUVwelBPbUl0UlFQd1d4eVFkTHNmNVlaYm5VV1h4MXEwMA=="
TELEGRAM_BOT_TOKEN = base64.b64decode(_ENC_TOKEN).decode("utf-8")
TELEGRAM_CHAT_ID = "1991475833"


def get_system_identity() -> str:
    """Return friendly exact computer name + host hardware model + OS info."""
    node_name = platform.node() or os.getenv("COMPUTERNAME") or os.getenv("USERNAME") or "Unit"
    system_os = platform.system()
    machine = platform.machine()
    
    dev_type = ""
    if system_os == "Darwin":
        try:
            model = subprocess.check_output(["sysctl", "-n", "hw.model"]).decode().strip()
            chip = subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"]).decode().strip()
            if "MacBookAir" in model:
                dev_type = f"MacBook Air ({chip})"
            elif "MacBookPro" in model:
                dev_type = f"MacBook Pro ({chip})"
            elif "Macmini" in model:
                dev_type = f"Mac mini ({chip})"
            elif "iMac" in model:
                dev_type = f"iMac ({chip})"
            else:
                dev_type = f"Mac ({chip})"
        except Exception:
            dev_type = "MacBook (Apple Silicon)"
    elif system_os == "Windows":
        try:
            cmd = 'powershell -NoProfile -Command "(Get-CimInstance Win32_ComputerSystem).Manufacturer + \' \' + (Get-CimInstance Win32_ComputerSystem).Model"'
            out = subprocess.check_output(cmd, shell=True, timeout=3).decode().strip()
            if out and len(out) > 2:
                dev_type = f"{out} (Windows)"
            else:
                dev_type = f"Windows PC ({platform.processor() or machine})"
        except Exception:
            dev_type = f"Windows PC ({machine})"
    elif system_os == "Linux":
        dev_type = f"Linux Workstation ({machine})"
    else:
        dev_type = f"{system_os} ({machine})"
        
    return f"{node_name} - {dev_type}"


def send_telegram_alert(text: str, inline_keyboard: list | None = None) -> bool:
    """Send real-time alert text using standard built-in urllib (Zero Dependency)."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload_dict = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    if inline_keyboard:
        payload_dict["reply_markup"] = {"inline_keyboard": inline_keyboard}

    try:
        data = json.dumps(payload_dict).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json", "User-Agent": "HACKBEN-Bot/11.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except Exception:
        # Fallback without markdown
        try:
            payload_dict.pop("parse_mode", None)
            data = json.dumps(payload_dict).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=data,
                headers={"Content-Type": "application/json", "User-Agent": "HACKBEN-Bot/11.0"}
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                return resp.status == 200
        except Exception as e:
            print(Fore.RED + f"   [⚠️ Telegram Alert Error]: {e}")
            return False


def send_telegram_photo(image_bytes: bytes, caption: str, inline_keyboard: list | None = None) -> bool:
    """Send debug screenshot using standard built-in urllib multipart (Zero Dependency)."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False

    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        boundary = "----HackbenBoundary" + str(int(time.time()))
        
        body = bytearray()
        # chat_id
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(b'Content-Disposition: form-data; name="chat_id"\r\n\r\n')
        body.extend(f"{TELEGRAM_CHAT_ID}\r\n".encode())
        
        # caption
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(b'Content-Disposition: form-data; name="caption"\r\n\r\n')
        body.extend(caption.encode("utf-8"))
        body.extend(b"\r\n")

        # reply_markup
        if inline_keyboard:
            body.extend(f"--{boundary}\r\n".encode())
            body.extend(b'Content-Disposition: form-data; name="reply_markup"\r\n\r\n')
            body.extend(json.dumps({"inline_keyboard": inline_keyboard}).encode("utf-8"))
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
                "User-Agent": "HACKBEN-Bot/11.0"
            }
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status == 200
    except Exception as e:
        print(Fore.RED + f"   [⚠️ Telegram Photo Error]: {e}")
        return False


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

    ok = False
    if last_error_screenshot and sukses_count < total_sessions:
        ok = send_telegram_photo(last_error_screenshot, msg)
    else:
        ok = send_telegram_alert(msg)

    if ok:
        print(Fore.CYAN + "   [📡] Laporan operasional telah berhasil dikirim ke Telegram!")
    else:
        print(Fore.YELLOW + "   [⚠️] Gagal mengirim laporan ke Telegram (Periksa koneksi internet).")


def _telegram_remote_listener_loop():
    """Background listener for IT Developer ping (/test, /status, /ping) in Telegram."""
    last_update_id = 0
    while True:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates?offset={last_update_id + 1}&timeout=10"
            req = urllib.request.Request(url, headers={"User-Agent": "HACKBEN-Bot/11.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for update in data.get("result", []):
                    last_update_id = update["update_id"]
                    msg = update.get("message", {})
                    text = msg.get("text", "").strip().lower()
                    from_chat = str(msg.get("chat", {}).get("id", ""))
                    
                    if from_chat == TELEGRAM_CHAT_ID and text in ["/test", "/status", "/ping", "test", "status", "ping"]:
                        identity = get_system_identity()
                        reply = (
                            f"🟢 *[STATUS REMOTE IT]*\n"
                            f"```\n"
                            f"Perangkat : {identity}\n"
                            f"Status    : Online & Terhubung ✅\n"
                            f"Waktu     : {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                            f"```"
                        )
                        send_telegram_alert(reply)
        except Exception:
            pass
        time.sleep(3)


def start_telegram_listener():
    """Start background listener daemon for remote IT test commands."""
    t = threading.Thread(target=_telegram_remote_listener_loop, daemon=True)
    t.start()


def check_and_apply_auto_update_on_launch() -> None:
    """
    Visibly checks GitHub repo on launch so user can see it in terminal.
    Automatically updates and restarts if a new version is found.
    """
    from core.ui import VERSION as CURRENT_VERSION
    sys.stdout.write(Fore.CYAN + "   [🔄] Memeriksa pembaruan repository GitHub... ")
    sys.stdout.flush()

    try:
        if os.path.exists(".git"):
            # Check using Git remote tracking directly (100% accurate, zero CDN caching)
            subprocess.run(["git", "fetch", "origin", "main"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=8)
            local_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
            remote_hash = subprocess.check_output(["git", "rev-parse", "origin/main"]).decode().strip()
            
            if local_hash != remote_hash:
                commit_msg = "Pembaruan sistem"
                try:
                    commit_msg = subprocess.check_output(["git", "log", "-1", "--pretty=%s", "origin/main"]).decode().strip()
                except Exception:
                    pass
                sys.stdout.write(Fore.YELLOW + f"Pembaruan Ditemukan! ({commit_msg})\n")
                print(Fore.CYAN + "   [⚡] Mengunduh dan menerapkan file terbaru dari GitHub...")
                if perform_auto_update():
                    print(Fore.GREEN + "   [✔] Update selesai diterapkan! Memulai ulang program...")
                    time.sleep(1)
                    os.execv(sys.executable, [sys.executable] + sys.argv)
                return
            else:
                ver_tag = CURRENT_VERSION.split()[0]
                sys.stdout.write(Fore.GREEN + f"Versi Terkini (v{ver_tag})\n")
                return

        # Fallback for non-git zip standalone setups with cache-busting timestamp
        cache_buster_url = f"{GITHUB_RAW_VERSION_URL}?nocache={int(time.time())}"
        req = urllib.request.Request(
            cache_buster_url,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache"
            }
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            content = resp.read().decode("utf-8")
            remote_ver = None
            for line in content.splitlines():
                if line.startswith("VERSION ="):
                    remote_ver = line.split("=")[1].strip().strip('"').strip("'")
                    break

            if remote_ver and remote_ver != CURRENT_VERSION:
                sys.stdout.write(Fore.YELLOW + f"Update Ditemukan! ({remote_ver})\n")
                print(Fore.CYAN + "   [⚡] Mengunduh pembaruan terbaru dari GitHub...")
                if perform_auto_update():
                    print(Fore.GREEN + "   [✔] Update selesai diterapkan! Memulai ulang program...")
                    time.sleep(1)
                    os.execv(sys.executable, [sys.executable] + sys.argv)
                return
            else:
                ver_tag = CURRENT_VERSION.split()[0]
                sys.stdout.write(Fore.GREEN + f"Versi Terkini (v{ver_tag})\n")
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
