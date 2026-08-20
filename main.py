#!/usr/bin/env python3
"""
HACKBEN - Universal Cross-Platform Automation Suite
Entry Point & Interactive Dashboard.
"""

import sys
import time
from colorama import Fore, Style, init

from core.ui import print_banner, Spinner, VERSION
from core.network import clean_system_processes, get_public_ip, get_current_os
from core.engine import ensure_playwright_installed, execute_feedback_session
from core.builder import menu_build_app
from core.guide import show_user_guide
from core.updater import check_and_apply_auto_update_on_launch, send_telemetry
from data.stores import (
    STORE_DB, 
    get_store_name, 
    search_stores, 
    get_all_regions, 
    get_region_stores,
    get_all_stores_count
)
from data.devices import get_device_count

init(autoreset=True)

class HackbenApp:
    def __init__(self):
        self.headless = True
        self.proxy_url = None
        self.default_store_code = "C55"
        self.default_service = "TAKE AWAY"

    def browse_stores_by_region(self) -> str | None:
        """Interactive regional store browser."""
        while True:
            print(Fore.CYAN + "\n" + "=" * 65)
            print(Fore.YELLOW + Style.BRIGHT + f"   🗺️  PILIH WILAYAH OUTLET HOKBEN ({get_all_stores_count()} Store)")
            print(Fore.CYAN + "=" * 65)
            regions = get_all_regions()
            for r_id, r_name in regions.items():
                st_count = len(get_region_stores(r_id))
                print(Fore.WHITE + f"   {r_id}. {r_name} {Fore.YELLOW}({st_count} Store){Fore.WHITE}")
            print(Fore.GREEN + "   S. 🔍 Cari Berdasarkan Nama Kota / Mall (Ketik Kata Kunci)")
            print(Fore.MAGENTA + "   0. ↩️  Kembali")
            print(Fore.CYAN + "-" * 65)

            p_reg = input(Fore.YELLOW + "   ?> Pilih Wilayah (1-9/S/0): " + Fore.RESET).strip().upper()

            if p_reg == "0" or p_reg == "KEMBALI":
                return None
            elif p_reg == "S" or p_reg == "CARI":
                kw = input(Fore.YELLOW + "   ?> Masukkan kata kunci pencarian (contoh: Pancoran, Galaxy, Tebet): " + Fore.RESET).strip()
                if not kw:
                    continue
                found = search_stores(kw)
                if not found:
                    print(Fore.RED + f"   ❌ Tidak ditemukan store dengan kata kunci '{kw}'.")
                    time.sleep(1)
                    continue
                print(Fore.GREEN + f"\n   [ HASIL PENCARIAN: {len(found)} Store Ditemukan ]")
                for k, v in list(found.items())[:25]:
                    print(Fore.WHITE + f"   • Kode: {Fore.CYAN}[{k}]{Fore.WHITE} -> {v}")
                if len(found) > 25:
                    print(Fore.YELLOW + f"   ... dan {len(found) - 25} store lainnya. Silakan persempit kata kunci.")
                input(Fore.YELLOW + "\n   [Tekan Enter untuk lanjut...]" + Fore.RESET)
            elif p_reg in regions:
                stores = get_region_stores(p_reg)
                print(Fore.GREEN + f"\n   [ DAFTAR STORE WILAYAH: {regions[p_reg]} ]")
                for k, v in stores.items():
                    print(Fore.WHITE + f"   • Kode: {Fore.CYAN}[{k}]{Fore.WHITE} -> {v}")
                input(Fore.YELLOW + "\n   [Tekan Enter untuk lanjut...]" + Fore.RESET)
            else:
                continue

    def menu_network_settings(self):
        """Configure Proxy and check public IP."""
        print(Fore.CYAN + "\n" + "=" * 65)
        print(Fore.YELLOW + Style.BRIGHT + "   🌐 PENGATURAN JARINGAN & PROXY")
        print(Fore.CYAN + "=" * 65)
        
        spinner = Spinner(message="Memeriksa IP Publik saat ini...")
        spinner.start()
        ip = get_public_ip()
        spinner.stop(f"IP Publik Anda: {Fore.GREEN}{ip or 'Tidak terdeteksi'}{Fore.RESET}", success=bool(ip))

        print(Fore.WHITE + f"   Proxy Aktif : {Fore.YELLOW}{self.proxy_url or 'Tidak Ada (Direct Connection)'}{Fore.RESET}")
        print(Fore.WHITE + "\n   1. Set Proxy Baru (Contoh: socks5://127.0.0.1:1080 atau http://ip:port)")
        print(Fore.WHITE + "   2. Hapus Proxy (Kembali ke Direct Mode)")
        print(Fore.MAGENTA + "   0. ↩️  Kembali ke Menu Utama")

        p = input(Fore.YELLOW + "\n   ?> Pilihan: " + Fore.RESET).strip()
        if p == "1":
            new_p = input(Fore.YELLOW + "   ?> Masukkan URL Proxy (atau ketik 0 untuk batal): " + Fore.RESET).strip()
            if new_p and new_p != "0":
                self.proxy_url = new_p
                print(Fore.GREEN + f"   ✅ Proxy diset ke: {self.proxy_url}")
        elif p == "2":
            self.proxy_url = None
            print(Fore.GREEN + "   ✅ Proxy dinonaktifkan (Direct Mode).")
        
        time.sleep(1)

    def menu_display_settings(self):
        """Toggle between Headless and Visual Window mode."""
        print(Fore.CYAN + "\n" + "=" * 65)
        print(Fore.YELLOW + Style.BRIGHT + "   👁️  PENGATURAN TAMPILAN BROWSER")
        print(Fore.CYAN + "=" * 65)
        print(Fore.WHITE + f"   Status saat ini: {Fore.GREEN if self.headless else Fore.YELLOW}{'Background / Headless (Diam-diam)' if self.headless else 'Visual Window (Jendela Terbuka)'}{Fore.RESET}")
        print(Fore.WHITE + "\n   1. Mode Background / Headless (Rekomendasi - Cepat & Tak Terlihat)")
        print(Fore.WHITE + "   2. Mode Visual Window (Jendela Terbuka - Untuk Debugging)")
        print(Fore.MAGENTA + "   0. ↩️  Kembali ke Menu Utama")

        p = input(Fore.YELLOW + "\n   ?> Pilihan: " + Fore.RESET).strip()
        if p == "1":
            self.headless = True
            print(Fore.GREEN + "   ✅ Mode diubah ke: Background (Headless).")
        elif p == "2":
            self.headless = False
            print(Fore.YELLOW + "   ✅ Mode diubah ke: Visual Window.")
        time.sleep(1)

    def start_bot(self):
        """Configure target and launch feedback automation loop."""
        while True:
            print_banner(headless=self.headless)
            
            # 1. Pilih Store
            print(Fore.GREEN + "   [ KONFIGURASI TARGET STORE ]")
            print(Fore.WHITE + "   • Ketik kode store langsung (contoh: C55, 518, 104)")
            print(Fore.CYAN + "   • Ketik 'list' atau 'cari' untuk melihat store per wilayah")
            print(Fore.MAGENTA + "   • Ketik '0' untuk kembali ke Menu Utama\n")
            
            target_store_name = None
            while True:
                kode = input(Fore.YELLOW + f"   ?> Masukkan Kode Store [Enter = {self.default_store_code}]: " + Fore.RESET).strip().upper()
                
                if kode == "0" or kode == "KEMBALI" or kode == "BACK":
                    return  # Kembali ke menu utama

                if not kode:
                    kode = self.default_store_code
                
                if kode in ["LIST", "CARI", "WILAYAH"]:
                    self.browse_stores_by_region()
                    break  # Reprompt store input

                store_name = get_store_name(kode)
                if store_name:
                    target_store_name = store_name
                    print(Fore.CYAN + f"   ✅ Target Store Dipilih: [{kode}] {target_store_name}")
                    break
                else:
                    print(Fore.RED + f"   ❌ Kode store '{kode}' tidak ditemukan! Ketik 'list' untuk melihat per wilayah atau '0' untuk kembali.")

            if not target_store_name:
                continue

            # 2. Pilih Layanan
            print(Fore.GREEN + "\n   [ PILIH METODE LAYANAN ]")
            print(Fore.WHITE + "   1. Dine In (Makan di Tempat)")
            print(Fore.WHITE + "   2. Take Away (Bawa Pulang)")
            print(Fore.MAGENTA + "   0. ↩️  Kembali ke Menu Utama")
            
            service_type = "TAKE AWAY"
            p_layanan = input(Fore.YELLOW + "   ?> Pilihan (1/2/0) [Enter = 2]: " + Fore.RESET).strip()
            if p_layanan == "0" or p_layanan.lower() == "kembali":
                return
            elif p_layanan == "1":
                service_type = "DINE IN"
            else:
                service_type = "TAKE AWAY"

            # 3. Jumlah Sesi
            print(Fore.GREEN + "\n   [ JUMLAH SESI FEEDBACK ]")
            print(Fore.WHITE + "   Masukkan berapa kali feedback ingin dikirim (Ketik 0 untuk batal).")
            raw_jum = input(Fore.YELLOW + "   ?> Berapa sesi? [Enter = 5]: " + Fore.RESET).strip()
            if raw_jum == "0" or raw_jum.lower() == "kembali":
                return
            try:
                total_sessions = int(raw_jum) if raw_jum else 5
            except ValueError:
                total_sessions = 5

            # Summary Before Launch
            print(Fore.CYAN + "\n" + "=" * 65)
            print(Fore.GREEN + f"   🚀 MEMULAI {total_sessions} SESI OTOMASI HACKBEN")
            print(Fore.WHITE + f"   🏢 Store   : {target_store_name}")
            print(Fore.WHITE + f"   🍱 Layanan : {service_type}")
            print(Fore.WHITE + f"   📱 Device  : {get_device_count()} Profil Siap Rotasi")
            print(Fore.WHITE + f"   🌐 Jaringan: {'Proxy (' + self.proxy_url + ')' if self.proxy_url else 'Direct Mode'}")
            print(Fore.CYAN + "=" * 65 + "\n")
            time.sleep(1.5)

            # Telemetry Start Event
            send_telemetry("start_session", target_store_name, 0, total_sessions, status="started", extra=f"service={service_type}")

            spinner = Spinner()
            sukses_count = 0

            for i in range(1, total_sessions + 1):
                print(Fore.YELLOW + f"   ▶ Menjalankan Sesi #{i} dari {total_sessions}:")
                ok = execute_feedback_session(
                    session_num=i,
                    total_sessions=total_sessions,
                    target_store=target_store_name,
                    service_type=service_type,
                    headless=self.headless,
                    proxy_url=self.proxy_url,
                    spinner=spinner
                )
                if ok:
                    sukses_count += 1
                    send_telemetry("session_progress", target_store_name, i, total_sessions, status="success")
                else:
                    send_telemetry("session_progress", target_store_name, i, total_sessions, status="failed")

                if i < total_sessions:
                    print(Fore.CYAN + "   ⏳ Jeda 3 detik antar sesi untuk stabilisasi...")
                    time.sleep(3)
                    print("")

            # Telemetry Finish Event
            send_telemetry("finish_session", target_store_name, sukses_count, total_sessions, status="completed")

            print(Fore.GREEN + "\n" + "=" * 65)
            print(Fore.YELLOW + Style.BRIGHT + f"   🎉 MISSION COMPLETED: {sukses_count}/{total_sessions} Sesi Berhasil!")
            print(Fore.CYAN + "=" * 65)
            input(Fore.YELLOW + "\n   [Tekan Enter untuk kembali ke Menu Utama...]" + Fore.RESET)
            break

    def run(self):
        """Main dashboard loop."""
        check_and_apply_auto_update_on_launch()
        ensure_playwright_installed()
        
        while True:
            try:
                print_banner(headless=self.headless)
                print(Fore.GREEN + "   [ MENU UTAMA DASHBOARD ]")
                print("   1. 🚀 Mulai Kirim Feedback Otomatis")
                print("   2. 📖 Petunjuk Penggunaan (Panduan Lengkap & Ramah)")
                print("   3. 👁️  Pengaturan Tampilan (Headless Background / Visual)")
                print("   4. 🌐 Pengaturan Jaringan & Proxy")
                print("   5. 🛠️  Jadikan Aplikasi (Build Standalone .exe / dll)")
                print("   0. 🚪 Keluar")
                print("")

                pilihan = input(Fore.YELLOW + "   ?> Masukkan pilihan (0-5) [Enter = 1 (Mulai)]: " + Fore.RESET).strip()

                if pilihan == "1" or not pilihan:
                    self.start_bot()
                elif pilihan == "2":
                    show_user_guide()
                elif pilihan == "3":
                    self.menu_display_settings()
                elif pilihan == "4":
                    self.menu_network_settings()
                elif pilihan == "5":
                    menu_build_app()
                elif pilihan == "0":
                    clean_system_processes()
                    print(Fore.CYAN + "\n   Sampai jumpa! Tetap semangat ya Kak. ✨\n")
                    break
                else:
                    continue

            except KeyboardInterrupt:
                clean_system_processes()
                print(Fore.RED + "\n\n   [!] Program dihentikan paksa oleh pengguna (CTRL+C).")
                print(Fore.CYAN + "   Membersihkan proses sistem... Selesai.\n")
                break


if __name__ == "__main__":
    app = HackbenApp()
    app.run()
