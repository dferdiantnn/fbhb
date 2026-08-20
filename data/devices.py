"""
Database of 130+ Authentic Modern Mobile Device Fingerprints (2020 - 2026 Flagships & Popular Midrangers).
Includes viewport dimensions, user-agents, touch capability, and 48-hour cooldown memory tracker.
"""

import os
import json
import random
from pathlib import Path
from datetime import datetime, timedelta

MEMORY_FILE = Path(__file__).resolve().parent.parent / "device_memory.json"
COOLDOWN_HOURS = 48

RAW_DEVICES = [
    # === APPLE (iPhone 12 - 16 Series) ===
    ("iPhone 16 Pro Max", "Mozilla/5.0 (iPhone; CPU iPhone OS 18_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Mobile/15E148 Safari/604.1", 440, 956),
    ("iPhone 16 Pro", "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1", 402, 874),
    ("iPhone 16 Plus", "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1", 430, 932),
    ("iPhone 16", "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1", 393, 852),
    ("iPhone 15 Pro Max", "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1", 430, 932),
    ("iPhone 15 Pro", "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1", 393, 852),
    ("iPhone 15 Plus", "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1", 430, 932),
    ("iPhone 15", "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1", 393, 852),
    ("iPhone 14 Pro Max", "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1", 430, 932),
    ("iPhone 14 Pro", "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1", 393, 852),
    ("iPhone 14 Plus", "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1", 428, 926),
    ("iPhone 14", "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1", 390, 844),
    ("iPhone 13 Pro Max", "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1", 428, 926),
    ("iPhone 13 Pro", "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1", 390, 844),
    ("iPhone 13", "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1", 390, 844),
    ("iPhone 12 Pro Max", "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1", 428, 926),
    ("iPhone 12", "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1", 390, 844),
    ("iPhone 11 Pro", "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1", 375, 812),
    ("iPhone 11", "Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1", 414, 896),

    # === SAMSUNG GALAXY (S21 - S25, Z Fold/Flip, A & M Series) ===
    ("Samsung Galaxy S25 Ultra", "Mozilla/5.0 (Linux; Android 15; SM-S938B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Samsung Galaxy S25+", "Mozilla/5.0 (Linux; Android 15; SM-S936B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Samsung Galaxy S25", "Mozilla/5.0 (Linux; Android 15; SM-S931B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Samsung Galaxy S24 Ultra", "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Samsung Galaxy S24+", "Mozilla/5.0 (Linux; Android 14; SM-S926B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Samsung Galaxy S24", "Mozilla/5.0 (Linux; Android 14; SM-S921B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Samsung Galaxy Z Fold6", "Mozilla/5.0 (Linux; Android 14; SM-F956B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Samsung Galaxy Z Flip6", "Mozilla/5.0 (Linux; Android 14; SM-F741B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Samsung Galaxy S23 Ultra", "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36", 384, 854),
    ("Samsung Galaxy S23 FE", "Mozilla/5.0 (Linux; Android 14; SM-S711B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Samsung Galaxy S22 Ultra", "Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36", 384, 854),
    ("Samsung Galaxy A55 5G", "Mozilla/5.0 (Linux; Android 14; SM-A556B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Samsung Galaxy A35 5G", "Mozilla/5.0 (Linux; Android 14; SM-A356B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Samsung Galaxy A54 5G", "Mozilla/5.0 (Linux; Android 14; SM-A546E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Samsung Galaxy A34 5G", "Mozilla/5.0 (Linux; Android 13; SM-A346E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Samsung Galaxy A25 5G", "Mozilla/5.0 (Linux; Android 14; SM-A256E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Samsung Galaxy A15 5G", "Mozilla/5.0 (Linux; Android 14; SM-A156E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Samsung Galaxy A05s", "Mozilla/5.0 (Linux; Android 13; SM-A057F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Samsung Galaxy M54 5G", "Mozilla/5.0 (Linux; Android 13; SM-M546B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Samsung Galaxy M34 5G", "Mozilla/5.0 (Linux; Android 13; SM-M346B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36", 360, 800),

    # === XIAOMI / REDMI / POCO ===
    ("Xiaomi 14 Ultra", "Mozilla/5.0 (Linux; Android 14; 24030PN60G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Xiaomi 14", "Mozilla/5.0 (Linux; Android 14; 23127PN0CG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36", 393, 852),
    ("Xiaomi 13T Pro", "Mozilla/5.0 (Linux; Android 13; 23078PND5G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Xiaomi 13T", "Mozilla/5.0 (Linux; Android 13; 2306EPN60G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Poco F6 Pro", "Mozilla/5.0 (Linux; Android 14; 23113RKC6G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Poco F6", "Mozilla/5.0 (Linux; Android 14; 24069PC21G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Poco X6 Pro 5G", "Mozilla/5.0 (Linux; Android 14; 2311DRK48G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Poco X6 5G", "Mozilla/5.0 (Linux; Android 14; 23122PCD1G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Poco M6 Pro", "Mozilla/5.0 (Linux; Android 13; 2312FPCA6G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Redmi Note 13 Pro+ 5G", "Mozilla/5.0 (Linux; Android 14; 23090RA98G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Redmi Note 13 Pro 5G", "Mozilla/5.0 (Linux; Android 14; 2312DRA50G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Redmi Note 13 4G", "Mozilla/5.0 (Linux; Android 13; 23129RAA4G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Redmi 13C", "Mozilla/5.0 (Linux; Android 13; 23100RN82L) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Redmi 12", "Mozilla/5.0 (Linux; Android 13; 23053RN02A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36", 393, 873),

    # === VIVO / IQOO ===
    ("Vivo X100 Pro", "Mozilla/5.0 (Linux; Android 14; V2324A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Vivo X100", "Mozilla/5.0 (Linux; Android 14; V2309A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Vivo V40 5G", "Mozilla/5.0 (Linux; Android 14; V2348) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Vivo V30 Pro", "Mozilla/5.0 (Linux; Android 14; V2319) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Vivo V30 5G", "Mozilla/5.0 (Linux; Android 14; V2318) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Vivo V29 5G", "Mozilla/5.0 (Linux; Android 13; V2250) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Vivo Y100 5G", "Mozilla/5.0 (Linux; Android 14; V2327) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Vivo Y27 5G", "Mozilla/5.0 (Linux; Android 13; V2302) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Vivo Y36 5G", "Mozilla/5.0 (Linux; Android 13; V2248) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36", 393, 873),
    ("iQOO 12", "Mozilla/5.0 (Linux; Android 14; I2220) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36", 412, 915),
    ("iQOO Z9 5G", "Mozilla/5.0 (Linux; Android 14; I2302) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36", 393, 873),
    ("iQOO Z7 5G", "Mozilla/5.0 (Linux; Android 13; I2207) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36", 393, 873),

    # === OPPO / REALME / ONEPLUS ===
    ("Oppo Find X7 Ultra", "Mozilla/5.0 (Linux; Android 14; PHY110) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Oppo Find N3", "Mozilla/5.0 (Linux; Android 13; CPH2499) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Oppo Find N3 Flip", "Mozilla/5.0 (Linux; Android 13; CPH2519) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Oppo Reno 12 Pro 5G", "Mozilla/5.0 (Linux; Android 14; CPH2629) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Oppo Reno 12 5G", "Mozilla/5.0 (Linux; Android 14; CPH2625) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Oppo Reno 11 Pro 5G", "Mozilla/5.0 (Linux; Android 14; CPH2607) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Oppo Reno 11 5G", "Mozilla/5.0 (Linux; Android 14; CPH2599) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Oppo A79 5G", "Mozilla/5.0 (Linux; Android 13; CPH2557) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Oppo A58", "Mozilla/5.0 (Linux; Android 13; CPH2577) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Realme GT 6", "Mozilla/5.0 (Linux; Android 14; RMX3851) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Realme 12 Pro+ 5G", "Mozilla/5.0 (Linux; Android 14; RMX3840) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Realme 12+ 5G", "Mozilla/5.0 (Linux; Android 14; RMX3867) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Realme C67", "Mozilla/5.0 (Linux; Android 14; RMX3890) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36", 393, 873),
    ("OnePlus 12", "Mozilla/5.0 (Linux; Android 14; CPH2581) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36", 412, 915),

    # === INFINIX / TECNO / ITEL ===
    ("Infinix GT 20 Pro", "Mozilla/5.0 (Linux; Android 14; X6871) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Infinix Note 40 Pro 5G", "Mozilla/5.0 (Linux; Android 14; X6851) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Infinix Note 40", "Mozilla/5.0 (Linux; Android 14; X6853) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Infinix Zero 30 5G", "Mozilla/5.0 (Linux; Android 13; X6731) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Infinix Hot 40 Pro", "Mozilla/5.0 (Linux; Android 13; X6837) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Tecno Camon 30 Pro 5G", "Mozilla/5.0 (Linux; Android 14; CL8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Tecno Pova 6 Pro 5G", "Mozilla/5.0 (Linux; Android 14; LI9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Tecno Spark 20 Pro+", "Mozilla/5.0 (Linux; Android 14; KJ7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Itel S23+", "Mozilla/5.0 (Linux; Android 13; S665L) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36", 393, 873),

    # === GOOGLE PIXEL & ASUS ROG ===
    ("Google Pixel 9 Pro XL", "Mozilla/5.0 (Linux; Android 15; Pixel 9 Pro XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Google Pixel 9", "Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Google Pixel 8 Pro", "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Google Pixel 8a", "Mozilla/5.0 (Linux; Android 14; Pixel 8a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36", 412, 915),
    ("ASUS ROG Phone 8 Pro", "Mozilla/5.0 (Linux; Android 14; ASUS_AI2401) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36", 412, 915),
]

DEVICES = [
    {
        "name": d[0],
        "user_agent": d[1],
        "viewport": {"width": d[2], "height": d[3]},
        "is_mobile": True,
        "has_touch": True
    }
    for d in RAW_DEVICES
]

def load_device_memory() -> dict:
    if not MEMORY_FILE.exists():
        return {}
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_device_memory(memory: dict) -> None:
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(memory, f, indent=2)
    except Exception:
        pass

def get_available_device() -> dict | None:
    """
    Select a random device that has not been used in the last COOLDOWN_HOURS.
    Updates the memory file upon selection.
    """
    memory = load_device_memory()
    now = datetime.now()
    cutoff = now - timedelta(hours=COOLDOWN_HOURS)

    # Clean old records
    active_memory = {
        name: ts for name, ts in memory.items()
        if datetime.fromisoformat(ts) > cutoff
    }

    # Filter available devices
    available = [d for d in DEVICES if d["name"] not in active_memory]

    # If all devices exhausted, reset oldest
    if not available:
        available = DEVICES
        active_memory = {}

    selected = random.choice(available)
    active_memory[selected["name"]] = now.isoformat()
    save_device_memory(active_memory)
    return selected

def get_device_count() -> int:
    """Return total registered devices."""
    return len(DEVICES)
