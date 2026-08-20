"""
Network management, Cross-Platform Process Cleaning, and Proxy Handlers.
"""

import sys
import os
import time
import subprocess
import urllib.request
from colorama import Fore

def get_current_os() -> str:
    """Detect operating system name: 'windows', 'macos', or 'linux'."""
    if sys.platform.startswith("win"):
        return "windows"
    elif sys.platform.startswith("darwin"):
        return "macos"
    return "linux"

def clean_system_processes() -> None:
    """Kill lingering browser or driver instances cross-platform."""
    current_os = get_current_os()
    try:
        if current_os == "windows":
            # Suppress output on Windows
            os.system("taskkill /f /im msedge.exe >nul 2>&1")
            os.system("taskkill /f /im chrome.exe >nul 2>&1")
            os.system("taskkill /f /im psiphon3.exe >nul 2>&1")
            os.system("taskkill /f /im psiphon-tunnel-core.exe >nul 2>&1")
        else:
            # macOS / Linux
            subprocess.run(["pkill", "-f", "chromium"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["pkill", "-f", "playwright"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

def get_public_ip(timeout: int = 4) -> str | None:
    """Fetch current public IP address with multi-provider fallback."""
    endpoints = [
        "https://api.ipify.org",
        "https://icanhazip.com",
        "https://ifconfig.me/ip",
        "https://checkip.amazonaws.com"
    ]
    for url in endpoints:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "curl/7.68.0"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                ip = resp.read().decode("utf-8").strip()
                if ip and len(ip) <= 45:
                    return ip
        except Exception:
            continue
    return None

def parse_proxy_string(proxy_str: str | None) -> dict | None:
    """
    Parse proxy string (e.g., 'socks5://127.0.0.1:1080' or 'http://user:pass@host:port')
    into Playwright proxy dictionary.
    """
    if not proxy_str or not proxy_str.strip():
        return None
    p = proxy_str.strip()
    if not (p.startswith("http://") or p.startswith("https://") or p.startswith("socks5://") or p.startswith("socks4://")):
        p = "http://" + p
    return {"server": p}
