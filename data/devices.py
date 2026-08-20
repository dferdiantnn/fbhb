"""
Database of 100+ Authentic Mobile Device Fingerprints for HACKBEN.
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
