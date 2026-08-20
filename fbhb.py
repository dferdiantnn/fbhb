import subprocess
import time
import random
import os
import ctypes
import sys
import json
from datetime import datetime, timedelta

# --- FIX WAJIB BUAT EXE PLAYWRIGHT ---
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "0"

from playwright.__main__ import main as playwright_installer
from colorama import Fore, Style, init
from playwright.sync_api import sync_playwright

# --- INISIALISASI ---
init(autoreset=True)

# --- KONFIGURASI ---
VERSION = "9.1 (100+ Devices & Fix Dine In LinkTo-2)"
AUTHOR = "ultramen pamulang"
MAX_IP_USAGE = 1  # 1 IP Cuma boleh 1 kali pakai (Strict)
HISTORY_FILE = "device_history.json" # File database ingatan bot
DURASI_BAN_JAM = 48 # Durasi device gak boleh dipake lagi (Jam)

# --- DATABASE STORE (DARI GAMBAR LU) ---
STORE_DB = {
    "518": "SENTRA PANCORAN",
    "521": "CILANDAK MALL",
    "522": "KALIBATA MAL",
    "527": "RUKO TEBET",
    "721": "RUKO KREO",
    "538": "PEJATEN VILLAGE",
    "C44": "HOKBEN KITCHEN FATMAWATI CILANDAK",
    "C54": "HOKBEN KITCHEN PASAR RUMPUT SETIABUDI",
    "C55": "HOKBEN KITCHEN CIPULIR SESKOAL",
    "540": "RUKO VETERAN BINTARO",
    "541": "AEON MALL TANJUNG BARAT",
    "C79": "HOKBEN KITCHEN MOH.KAHFI 1 JAGAKARSA",
    "543": "RUKO LAPANGAN ROOS TEBET"
}

# --- DATABASE DEVICE (100+ HP INDONESIA) ---
# Format: Nama HP, User Agent, Width, Height
RAW_DEVICES = [
    # === APPLE (iPhone 11 - 15) ===
    ("iPhone 11", "Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1", 414, 896),
    ("iPhone 11 Pro", "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1", 375, 812),
    ("iPhone 12", "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1", 390, 844),
    ("iPhone 12 Mini", "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.1", 360, 780),
    ("iPhone 12 Pro Max", "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1", 428, 926),
    ("iPhone 13", "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1", 390, 844),
    ("iPhone 13 Pro", "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1", 390, 844),
    ("iPhone 13 Mini", "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1", 375, 812),
    ("iPhone 14", "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1", 390, 844),
    ("iPhone 14 Plus", "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1", 428, 926),
    ("iPhone 14 Pro", "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1", 393, 852),
    ("iPhone 14 Pro Max", "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1", 430, 932),
    ("iPhone 15", "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1", 393, 852),
    ("iPhone 15 Plus", "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1", 430, 932),
    ("iPhone 15 Pro", "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1", 393, 852),
    ("iPhone 15 Pro Max", "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1", 430, 932),
    ("iPhone SE 2022", "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1", 375, 667),

    # === SAMSUNG (S, A, M Series) ===
    ("Samsung S24 Ultra", "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Samsung S24+", "Mozilla/5.0 (Linux; Android 14; SM-S926B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Samsung S23 Ultra", "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36", 384, 854),
    ("Samsung S23", "Mozilla/5.0 (Linux; Android 13; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Samsung S22 Ultra", "Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36", 384, 854),
    ("Samsung S21 FE", "Mozilla/5.0 (Linux; Android 13; SM-G990B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Samsung A54 5G", "Mozilla/5.0 (Linux; Android 14; SM-A546E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Samsung A34 5G", "Mozilla/5.0 (Linux; Android 13; SM-A346E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Samsung A24", "Mozilla/5.0 (Linux; Android 13; SM-A245F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Samsung A14", "Mozilla/5.0 (Linux; Android 13; SM-A145F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Samsung A04s", "Mozilla/5.0 (Linux; Android 12; SM-A047F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Samsung A05", "Mozilla/5.0 (Linux; Android 13; SM-A055F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Samsung A05s", "Mozilla/5.0 (Linux; Android 13; SM-A057F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Samsung A53 5G", "Mozilla/5.0 (Linux; Android 13; SM-A536E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Samsung A33 5G", "Mozilla/5.0 (Linux; Android 12; SM-A336E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Samsung M14 5G", "Mozilla/5.0 (Linux; Android 13; SM-M146B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Samsung M34 5G", "Mozilla/5.0 (Linux; Android 13; SM-M346B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Samsung A52s", "Mozilla/5.0 (Linux; Android 12; SM-A528B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36", 412, 915),
    ("Samsung A73 5G", "Mozilla/5.0 (Linux; Android 13; SM-A736B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36", 412, 915),

    # === XIAOMI / REDMI / POCO ===
    ("Redmi Note 13 Pro+ 5G", "Mozilla/5.0 (Linux; Android 14; 23090RA98G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Redmi Note 13 Pro 5G", "Mozilla/5.0 (Linux; Android 14; 2312DRA50G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Redmi Note 13 4G", "Mozilla/5.0 (Linux; Android 13; 23129RAA4G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Redmi Note 12 Pro 5G", "Mozilla/5.0 (Linux; Android 13; 22101316G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Redmi Note 12 4G", "Mozilla/5.0 (Linux; Android 13; 23021RAAEG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Redmi 12", "Mozilla/5.0 (Linux; Android 13; 23053RN02A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Redmi 13C", "Mozilla/5.0 (Linux; Android 13; 23100RN82L) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Redmi 12C", "Mozilla/5.0 (Linux; Android 12; 22120RN86G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Redmi 10 2022", "Mozilla/5.0 (Linux; Android 11; 21121119SG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Redmi 9C", "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Redmi A2", "Mozilla/5.0 (Linux; Android 13; 23028RN4DG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Poco X6 Pro", "Mozilla/5.0 (Linux; Android 14; 2311DRK48G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Poco X6", "Mozilla/5.0 (Linux; Android 13; 23122PCD1G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Poco M6 Pro", "Mozilla/5.0 (Linux; Android 13; 2312FPCA6G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Poco F5", "Mozilla/5.0 (Linux; Android 13; 23049PCD8G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Poco X5 Pro", "Mozilla/5.0 (Linux; Android 12; 22101320G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Poco C65", "Mozilla/5.0 (Linux; Android 13; 2310FPCA4G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Xiaomi 14", "Mozilla/5.0 (Linux; Android 14; 23127PN0CG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Xiaomi 13T", "Mozilla/5.0 (Linux; Android 14; 2306EPN60G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Xiaomi 12 Lite", "Mozilla/5.0 (Linux; Android 13; 2203129G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36", 393, 873),

    # === OPPO ===
    ("Oppo Reno 11 F", "Mozilla/5.0 (Linux; Android 14; CPH2603) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Oppo Reno 11 5G", "Mozilla/5.0 (Linux; Android 14; CPH2599) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Oppo Reno 10 5G", "Mozilla/5.0 (Linux; Android 13; CPH2531) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Oppo Reno 8T", "Mozilla/5.0 (Linux; Android 13; CPH2481) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Oppo A79 5G", "Mozilla/5.0 (Linux; Android 13; CPH2557) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Oppo A98 5G", "Mozilla/5.0 (Linux; Android 13; CPH2529) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Oppo A78 4G", "Mozilla/5.0 (Linux; Android 13; CPH2565) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Oppo A58", "Mozilla/5.0 (Linux; Android 13; CPH2577) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Oppo A38", "Mozilla/5.0 (Linux; Android 13; CPH2579) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Oppo A18", "Mozilla/5.0 (Linux; Android 13; CPH2591) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Oppo A57", "Mozilla/5.0 (Linux; Android 12; CPH2387) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Oppo A17", "Mozilla/5.0 (Linux; Android 12; CPH2477) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Oppo A17k", "Mozilla/5.0 (Linux; Android 12; CPH2471) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Oppo A16", "Mozilla/5.0 (Linux; Android 11; CPH2269) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Oppo Find N3 Flip", "Mozilla/5.0 (Linux; Android 13; CPH2519) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36", 393, 873),

    # === VIVO ===
    ("Vivo V30", "Mozilla/5.0 (Linux; Android 14; V2318) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Vivo V29 5G", "Mozilla/5.0 (Linux; Android 13; V2250) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Vivo V29e", "Mozilla/5.0 (Linux; Android 13; V2303) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Vivo V27 5G", "Mozilla/5.0 (Linux; Android 13; V2246) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Vivo Y100 5G", "Mozilla/5.0 (Linux; Android 14; V2327) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Vivo Y36 5G", "Mozilla/5.0 (Linux; Android 13; V2248) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Vivo Y27s", "Mozilla/5.0 (Linux; Android 13; V2322) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Vivo Y27", "Mozilla/5.0 (Linux; Android 13; V2249) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Vivo Y17s", "Mozilla/5.0 (Linux; Android 13; V2310) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Vivo Y02t", "Mozilla/5.0 (Linux; Android 13; V2254) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Vivo Y35", "Mozilla/5.0 (Linux; Android 12; V2205) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Vivo Y22", "Mozilla/5.0 (Linux; Android 12; V2207) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36", 360, 800),
    ("iQOO Z7 5G", "Mozilla/5.0 (Linux; Android 13; I2213) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36", 393, 873),
    ("iQOO 12", "Mozilla/5.0 (Linux; Android 14; I2220) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36", 393, 873),

    # === REALME ===
    ("Realme 12+ 5G", "Mozilla/5.0 (Linux; Android 14; RMX3867) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Realme 12 Pro+ 5G", "Mozilla/5.0 (Linux; Android 14; RMX3840) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Realme 11 Pro+ 5G", "Mozilla/5.0 (Linux; Android 13; RMX3741) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Realme 11", "Mozilla/5.0 (Linux; Android 13; RMX3780) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Realme C67", "Mozilla/5.0 (Linux; Android 14; RMX3890) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Realme C55", "Mozilla/5.0 (Linux; Android 13; RMX3710) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Realme C53", "Mozilla/5.0 (Linux; Android 13; RMX3760) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Realme C51", "Mozilla/5.0 (Linux; Android 13; RMX3830) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Realme C35", "Mozilla/5.0 (Linux; Android 11; RMX3511) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Realme Narzo 50 5G", "Mozilla/5.0 (Linux; Android 12; RMX3571) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Realme GT 2 Pro", "Mozilla/5.0 (Linux; Android 13; RMX3301) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36", 393, 873),

    # === INFINIX ===
    ("Infinix Note 30 Pro", "Mozilla/5.0 (Linux; Android 13; X678B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Infinix Note 30", "Mozilla/5.0 (Linux; Android 13; X6833B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Infinix GT 10 Pro", "Mozilla/5.0 (Linux; Android 13; X6739) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Infinix Zero 30 5G", "Mozilla/5.0 (Linux; Android 13; X6731) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Infinix Hot 30", "Mozilla/5.0 (Linux; Android 13; X6831) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Infinix Hot 30i", "Mozilla/5.0 (Linux; Android 12; X669C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Infinix Smart 8", "Mozilla/5.0 (Linux; Android 13; X6525) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Infinix Smart 7", "Mozilla/5.0 (Linux; Android 12; X6515) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36", 360, 800),

    # === TECNO ===
    ("Tecno Pova 5 Pro 5G", "Mozilla/5.0 (Linux; Android 13; LH8n) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Tecno Pova 5", "Mozilla/5.0 (Linux; Android 13; LH7n) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Tecno Spark 20 Pro+", "Mozilla/5.0 (Linux; Android 14; KJ7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Tecno Spark 20", "Mozilla/5.0 (Linux; Android 13; KJ5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Tecno Spark 10 Pro", "Mozilla/5.0 (Linux; Android 13; KI7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Tecno Camon 20 Pro", "Mozilla/5.0 (Linux; Android 13; CK7n) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36", 393, 873),

    # === ITEL ===
    ("Itel S23+", "Mozilla/5.0 (Linux; Android 13; T616) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36", 393, 873),
    ("Itel S23", "Mozilla/5.0 (Linux; Android 12; S665L) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36", 360, 800),
    ("Itel A70", "Mozilla/5.0 (Linux; Android 13; A665L) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36", 360, 800)
]

# Convert tuple list to list of dicts for script compatibility
DEVICES = [{"name": d[0], "ua": d[1], "w": d[2], "h": d[3]} for d in RAW_DEVICES]

IP_USAGE_TRACKER = {} 
STATE = {"last_region": None}

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

PSIPHON_PATH = resource_path("psiphon3.exe")

# --- FUNGSI MEMORY DEVICE ---
def get_secure_random_device():
    """Memilih device yang belum dipakai dalam 48 jam terakhir"""
    
    # 1. Load History
    history = {}
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
        except: history = {}

    now = datetime.now()
    clean_history = {}
    used_names = []

    # 2. Pruning (Hapus data lama > 48 jam)
    for name, str_time in history.items():
        try:
            last_used = datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")
            if (now - last_used) < timedelta(hours=DURASI_BAN_JAM):
                clean_history[name] = str_time # Masih di ban
                used_names.append(name)
        except: pass

    # 3. Filter Stok Device
    available_devs = [d for d in DEVICES if d['name'] not in used_names]

    if not available_devs:
        return None # Stok habis

    # 4. Pilih & Simpan
    chosen = random.choice(available_devs)
    clean_history[chosen['name']] = now.strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(clean_history, f, indent=4)
    except: pass

    return chosen

def banner():
    os.system("cls" if os.name == "nt" else "clear")
    print(Fore.CYAN + Style.BRIGHT + "="*65)
    print(Fore.CYAN + Style.BRIGHT + r"""
    ██╗  ██╗ █████╗  ██████╗██╗  ██╗██████╗ ███████╗███╗   ██╗
    ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔══██╗██╔════╝████╗  ██║
    ███████║███████║██║     █████╔╝ ██████╔╝█████╗  ██╔██╗ ██║
    ██╔══██║██╔══██║██║     ██╔═██╗ ██╔══██╗██╔══╝  ██║╚██╗██║
    ██║  ██║██║  ██║╚██████╗██║  ██╗██████╔╝███████╗██║ ╚████║
    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═══╝
          >> Created by: """ + Fore.YELLOW + AUTHOR + Fore.CYAN + """ <<
    """ + Fore.RED + Style.DIM + "    \"Program dibuat dengan hati yang hancur. ferr\"" + Fore.CYAN + Style.BRIGHT + """
    """)
    print(Fore.CYAN + Style.BRIGHT + "="*65)
    print(Fore.WHITE + f"   Bot Version : {VERSION}")
    print(Fore.CYAN + Style.BRIGHT + "="*65 + "\n")

def cek_dan_install_browser():
    print(Fore.YELLOW + "   ⚙️  System Check: Memeriksa kelengkapan Browser...")
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            p.chromium.launch(headless=True).close()
        print(Fore.GREEN + "   ✅ Browser Engine Siap!")
    except Exception as e:
        print(Fore.RED + "   ⚠️ Browser belum ada! Bot akan mendownload otomatis...")
        try:
            backup_argv = sys.argv
            sys.argv = ["playwright", "install", "chromium"]
            try: playwright_installer()
            except SystemExit: pass
            sys.argv = backup_argv
            print(Fore.GREEN + "   ✅ Instalasi Selesai!")
        except Exception as err:
            print(Fore.RED + f"   ❌ Gagal Install: {err}")
            sys.exit()

def minimize_psiphon():
    try:
        hwnd = ctypes.windll.user32.FindWindowW(None, "Psiphon 3")
        if hwnd: ctypes.windll.user32.ShowWindow(hwnd, 6)
    except: pass

def kill_popup_browser():
    os.system("taskkill /f /im msedge.exe >nul 2>&1") 
    os.system("taskkill /f /im chrome.exe >nul 2>&1") 

def bersihkan_jejak_network():
    os.system("taskkill /f /im psiphon3.exe >nul 2>&1")
    os.system("taskkill /f /im psiphon-tunnel-core.exe >nul 2>&1")
    os.system("ipconfig /flushdns >nul 2>&1") 
    time.sleep(1)

def dapatkan_ip_sekarang():
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True) 
            page = browser.new_page()
            page.goto("https://api.ipify.org", timeout=15000) 
            ip = page.locator("body").text_content().strip()
            browser.close()
            return ip
        except:
            return None

def cari_ip_fresh(vpn_wait_time):
    regions = ['us', 'jp', 'sg', 'gb', 'de', 'ca', 'nl', 'in']
    MAX_ATTEMPTS = 5 
    
    for i in range(MAX_ATTEMPTS): 
        bersihkan_jejak_network()
        pilihan_region = random.choice(regions)
        
        print(Fore.YELLOW + f"   📡 [SEARCH {i+1}/{MAX_ATTEMPTS}] Start Region: {pilihan_region.upper()}")
        
        try:
            subprocess.Popen([PSIPHON_PATH, "-r", pilihan_region], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e: 
            print(Fore.RED + f"   ❌ Gagal start Psiphon: {e}")
            continue

        print(f"   ⏳ Connecting ({vpn_wait_time}s) ", end="", flush=True)
        for _ in range(vpn_wait_time): 
            time.sleep(1)
            print(Fore.GREEN + ".", end="", flush=True)
        print(Fore.RESET)
        
        kill_popup_browser()
        minimize_psiphon()

        ip_baru = dapatkan_ip_sekarang()
        
        if not ip_baru:
            print(Fore.RED + "   ⚠️ No IP detected, retrying...")
            continue

        if ip_baru:
            print(f"   > IP Detected: {Fore.CYAN}{ip_baru}{Fore.RESET}")
            count = IP_USAGE_TRACKER.get(ip_baru, 0)
            
            # --- CEK STRICT 1 IP 1 HIT ---
            if count >= MAX_IP_USAGE:
                print(Fore.RED + f"   ❌ IP USED! ({count}/{MAX_IP_USAGE}). Cari baru...")
                time.sleep(2)
            else:
                IP_USAGE_TRACKER[ip_baru] = count + 1
                sisa = MAX_IP_USAGE - IP_USAGE_TRACKER[ip_baru]
                print(Fore.GREEN + f"   ✅ IP ACCEPTED. (Fresh IP)")
                STATE["last_region"] = pilihan_region
                return True
            
    return False

def jalankan_survei(nomer_sesi, use_vpn, vpn_wait_time, target_store_name, service_type):
    print(Fore.CYAN + "\n" + "="*40)
    
    # --- LOGIKA AUTO SWITCH ---
    mode_saat_ini_vpn = use_vpn 
    
    if mode_saat_ini_vpn:
        print(Fore.CYAN + f"   SESI {nomer_sesi}: CONFIG NETWORK (VPN)...")
        sukses_ip = cari_ip_fresh(vpn_wait_time)
        
        if not sukses_ip:
            print(Fore.RED + "\n   [!] GAGAL DAPAT IP FRESH 5x!")
            print(Fore.MAGENTA + "   [!] SWITCHING TO DIRECT MODE (NO VPN) UNTUK SESI INI...")
            bersihkan_jejak_network() 
            mode_saat_ini_vpn = False 
            time.sleep(2)

    if not mode_saat_ini_vpn:
        print(Fore.CYAN + f"   SESI {nomer_sesi}: DIRECT MODE (MANIPULASI PERANGKAT)...")
    
    print(Fore.CYAN + "="*40)

    # --- PILIH DEVICE DENGAN MEMORY ---
    dev = get_secure_random_device()
    if dev is None:
        print(Fore.RED + "❌ STOK DEVICE HABIS (Semua dipakai < 48 jam)!")
        print(Fore.WHITE + "   Menunggu 5 detik lalu skip sesi ini...")
        time.sleep(5)
        return

    print(Fore.YELLOW + f"\n📱 Fake Device: {dev['name']}...")
    print(Fore.WHITE + f"🎯 Target Store: {target_store_name}")
    print(Fore.WHITE + f"🍽️  Service: {service_type}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent=dev['ua'],
            viewport={'width': dev['w'], 'height': dev['h']},
            is_mobile=True, has_touch=True, ignore_https_errors=True
        )
        context.set_default_timeout(60000)
        page = context.new_page()

        try:
            page.goto("https://update.hokben.co.id/", timeout=60000)
            
            print("   🏢 Login Store...")
            page.wait_for_selector("input[placeholder='Cari Store ...']", state="visible")
            
            # --- INPUT NAMA STORE DARI KODE ---
            page.fill("input[placeholder='Cari Store ...']", target_store_name)
            time.sleep(2)
            
            saran = page.locator(f"//a[contains(text(), '{target_store_name}')]")
            if saran.count() > 0: saran.first.click()
            else: page.keyboard.press("Enter")
            time.sleep(2)

            # --- PILIHAN LAYANAN (BYPASS TOMBOL RUSAK) ---
            if service_type == "DINE IN":
                print("   🍽️  Memilih Menu Dine In (via linkTo-2)...")
                # HACK: Langsung eksekusi JS karena tombol UI nya rusak (Gambar Takeaway)
                page.evaluate("try { linkTo(2) } catch(e) { console.log(e) }")

            else: # TAKE AWAY
                print("   🎁 Memilih Menu Take Away (via linkTo-3)...")
                page.evaluate("try { linkTo(3) } catch(e) { console.log(e) }") 
            
            time.sleep(2)
            
            print("   📝 Mengisi Kuesioner (Mode Positif)...")
            page.wait_for_selector("fieldset", state="visible", timeout=60000)
            all_q = page.locator("fieldset:visible")
            
            for i in range(all_q.count()):
                q = all_q.nth(i)
                q.scroll_into_view_if_needed()
                time.sleep(random.uniform(0.5, 1.5)) 
                
                # Logic Jawaban: Prioritas "Ya" & "Sangat Puas"
                target = q.locator("label:has-text('Ya') input, label:has-text('Sangat Puas') input")
                others = q.locator("input[type='radio']")
                
                if target.count() > 0: target.first.click(force=True)
                elif others.count() > 0: others.nth(random.randint(0, others.count()-1)).click(force=True)

            print("   ✅ Mencoba Submit...")
            page.keyboard.press("End") 
            time.sleep(1)

            tombol_submit = page.locator("input[type='submit'], button:has-text('Kirim'), button:has-text('Submit'), input[value='Kirim']")

            if tombol_submit.count() > 0:
                tombol_submit.first.evaluate("node => node.click()")
                print("   🚀 Tombol diklik paksa!")
            else:
                print("   ⚠️ Tombol Submit gak ketemu, coba manual!")
            
            print("   👀 Verifikasi Sukses...")
            try:
                page.wait_for_url("**/arigatou", timeout=30000)
                print(Fore.GREEN + f"   🎉 Sesi {nomer_sesi} BERHASIL!")
            except:
                print(Fore.RED + f"   ⚠️ Warning: Tidak redirect ke Arigatou.")

            time.sleep(2)

        except Exception as e:
            print(Fore.RED + f"❌ Error Browser: {e}")
        
        browser.close()

if __name__ == "__main__":
    banner()
    cek_dan_install_browser() 
    
    while True:
        try:
            banner()
            
            # --- INPUT KODE STORE ---
            print(Fore.GREEN + "   [ KONFIGURASI TARGET ]")
            while True:
                kode_input = input(Fore.YELLOW + "   ?> Masukan KODE STORE (Contoh C55): " + Fore.RESET).strip().upper()
                if kode_input in STORE_DB:
                    target_store_name = STORE_DB[kode_input]
                    print(Fore.CYAN + f"   ✅ Store Ditemukan: {target_store_name}")
                    break
                else:
                    print(Fore.RED + "   ❌ Kode tidak ditemukan di database! Coba lagi.")
            
            # --- INPUT LAYANAN ---
            print(Fore.GREEN + "\n   [ PILIH LAYANAN ]")
            print("   1. Dine In (Makan di Tempat)")
            print("   2. Take Away (Bawa Pulang)")
            
            while True:
                layanan_input = input(Fore.YELLOW + "   ?> Pilihan (1/2): " + Fore.RESET).strip()
                if layanan_input == "1":
                    service_type = "DINE IN"
                    break
                elif layanan_input == "2":
                    service_type = "TAKE AWAY"
                    break
                else:
                    print(Fore.RED + "   ❌ Pilihan salah!")

            print(Fore.GREEN + "\n   [ MODE JARINGAN ]")
            print("   1. MODE VPN (Auto Ganti IP)")
            print("   2. MODE DIRECT (Tanpa VPN, Cuma Ganti HP)")
            print("   3. Exit")
            
            pilihan = input(Fore.YELLOW + "   ?> Pilihan (1-3): " + Fore.RESET)
            
            use_vpn = False
            if pilihan == "1": use_vpn = True
            elif pilihan == "2": use_vpn = False
            elif pilihan == "3":
                bersihkan_jejak_network()
                print("Bye Guys.")
                time.sleep(1)
                break
            else: continue

            print(Fore.MAGENTA + "\n   [Ketik '0' atau 'b' untuk KEMBALI]")
            raw_jum = input(Fore.YELLOW + "   ?> Jumlah Feedback (Enter = 8): " + Fore.RESET)
            if raw_jum.strip().lower() in ['0', 'b']:
                continue 
            
            try:
                jumlah = int(raw_jum) if raw_jum.strip() else 8
            except: jumlah = 8

            vpn_delay = 20
            if use_vpn:
                raw_vpn = input(Fore.YELLOW + "   ?> Jeda Koneksi VPN (Detik) (Enter = 20): " + Fore.RESET)
                if raw_vpn.strip().lower() in ['0', 'b']:
                    continue 
                try:
                    vpn_delay = int(raw_vpn) if raw_vpn.strip() else 20
                except: vpn_delay = 20
            
            mode_str = "VPN MODE" if use_vpn else "DIRECT MODE"
            print(Fore.GREEN + f"\n   🚀 HACKBEN STARTED: {jumlah} SESI [{mode_str}]")
            print(Fore.WHITE + f"   🎯 TARGET: {target_store_name} ({service_type})")
            time.sleep(2)
            
            if use_vpn: bersihkan_jejak_network()
            IP_USAGE_TRACKER = {} 
            
            for i in range(1, jumlah + 1):
                jalankan_survei(i, use_vpn=use_vpn, vpn_wait_time=vpn_delay, target_store_name=target_store_name, service_type=service_type)
                print(Fore.YELLOW + "\n   [REHAT ANTAR SESI 5 DETIK]...")
                time.sleep(5)
            
            print(Fore.GREEN + "\n   ✅ MISSION COMPLETE!")
            input("\n   Enter untuk kembali...")

        except KeyboardInterrupt:
            print(Fore.RED + "\n\n   [!] FORCE EXIT DETECTED (CTRL+C)")
            bersihkan_jejak_network()
            print("   Bye Guys, Stay Strong.")
            time.sleep(2)
            break