#!/usr/bin/env python3
"""
HACKBEN - Universal Cross-Platform Automation Suite
Entry Point & Interactive Dashboard with Auto-Update & Telemetry Bridge.
"""

import sys
import time
from colorama import Fore, Style, init

from core.ui import print_banner, Spinner, VERSION
from core.network import clean_system_processes, get_public_ip, get_current_os
from core.engine import ensure_playwright_installed, execute_feedback_session
from core.builder import menu_build_app
from core.updater import check_for_updates, perform_auto_update, send_telemetry
from data.stores import STORE_DB, get_store_name, search_stores
from data.devices import get_device_count

init(autoreset=True)

class HackbenApp:
    def __init__(self):
        self.headless = True
        self.proxy_url = None
        self.default_store_code = "C55"
        self.default_service = "TAKE AWAY"

    def menu_update_checker(self):
        """Interactive update menu from GitHub repo."""
        print(Fore.CYAN + "\n" + "=" * 65)
        print(Fore.YELLOW + Style.BRIGHT + "   🔄 SISTEM PEMBARUAN OTOMATIS (GITHUB)")
        print(Fore.CYAN + "=" * 65)
        
        spinner = Spinner(message="Memeriksa rilis terbaru di GitHub...")
        spinner.start()
        has_update, latest_ver = check_for_updates()
        
        if has_update:
            spinner.stop(f"Pembaruan Ditemukan! Versi terbaru: {Fore.GREEN}{latest_ver}{Fore.RESET}", success=True)
            print(Fore.WHITE + f"   Versi Anda saat ini: {Fore.YELLOW}{VERSION}{Fore.RESET}")
            print(Fore.CYAN + "\n   Apakah kamu ingin memperbarui dan menimpa file lama sekarang?")
            confirm = input(Fore.YELLOW + "   ?> Update sekarang? (y/n) [Enter = y]: " + Fore.RESET).strip().lower()
            if confirm in ["y", "yes", ""]:
                print("")
                if perform_auto_update():
                    print(Fore.GREEN + "\n   🎉 Program berhasil diperbarui! Silakan restart aplikasi.")
                    sys.exit(0)
        else:
            spinner.stop(f"Anda sudah menggunakan versi paling mutakhir ({VERSION}).", success=True)

        input(Fore.YELLOW + "\n   [Tekan Enter untuk kembali...]" + Fore.RESET)

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
        print(Fore.WHITE + "   0. Kembali")

        p = input(Fore.YELLOW + "\n   ?> Pilihan: " + Fore.RESET).strip()
        if p == "1":
            new_p = input(Fore.YELLOW + "   ?> Masukkan URL Proxy: " + Fore.RESET).strip()
            if new_p:
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
        print(Fore.WHITE + "   0. Kembali")

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
        print_banner(headless=self.headless)
        
        # 1. Pilih Store
        print(Fore.GREEN + "   [ KONFIGURASI TARGET STORE ]")
        target_store_name = None
        while True:
            kode = input(Fore.YELLOW + f"   ?> Masukkan Kode Store (Contoh C55, 518, 521) [Enter = {self.default_store_code}]: " + Fore.RESET).strip().upper()
            if not kode:
                kode = self.default_store_code
            
            store_name = get_store_name(kode)
            if store_name:
                target_store_name = store_name
                print(Fore.CYAN + f"   ✅ Target Store: {target_store_name}")
                break
            else:
                print(Fore.RED + "   ❌ Kode store tidak ditemukan! Coba lagi (ketik 'list' untuk melihat daftar).")
                if kode == "LIST":
                    for k, v in STORE_DB.items():
                        print(f"      [{k}] {v}")

        # 2. Pilih Layanan
        print(Fore.GREEN + "\n   [ PILIH METODE LAYANAN ]")
        print("   1. Dine In (Makan di Tempat)")
        print("   2. Take Away (Bawa Pulang)")
        
        service_type = "TAKE AWAY"
        while True:
            p_layanan = input(Fore.YELLOW + "   ?> Pilihan (1/2) [Enter = 2]: " + Fore.RESET).strip()
            if p_layanan == "1":
                service_type = "DINE IN"
                break
            elif p_layanan == "2" or not p_layanan:
                service_type = "TAKE AWAY"
                break
            else:
                print(Fore.RED + "   ❌ Pilihan tidak valid.")

        # 3. Jumlah Sesi
        print(Fore.GREEN + "\n   [ JUMLAH SESI FEEDBACK ]")
        raw_jum = input(Fore.YELLOW + "   ?> Berapa kali feedback ingin dikirim? [Enter = 5]: " + Fore.RESET).strip()
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

        # Telemetry Start
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

        # Telemetry Finish
        send_telemetry("finish_session", target_store_name, sukses_count, total_sessions, status="completed")

        print(Fore.GREEN + "\n" + "=" * 65)
        print(Fore.YELLOW + Style.BRIGHT + f"   🎉 MISSION COMPLETED: {sukses_count}/{total_sessions} Sesi Berhasil!")
        print(Fore.CYAN + "=" * 65)
        input(Fore.YELLOW + "\n   [Tekan Enter untuk kembali ke Menu Utama...]" + Fore.RESET)

    def run(self):
        """Main dashboard loop."""
        ensure_playwright_installed()
        
        while True:
            try:
                print_banner(headless=self.headless)
                print(Fore.GREEN + "   [ MENU UTAMA DASHBOARD ]")
                print("   1. 🚀 Mulai Kirim Feedback Otomatis")
                print("   2. 👁️  Pengaturan Tampilan (Headless Background / Visual)")
                print("   3. 🌐 Pengaturan Jaringan & Proxy")
                print("   4. 🛠️  Jadikan Aplikasi (Build Standalone .exe / dll)")
                print("   5. 🔄 Cek & Perbarui Versi (Auto-Update GitHub)")
                print("   0. 🚪 Keluar")
                print("")

                pilihan = input(Fore.YELLOW + "   ?> Masukkan pilihan (0-5): " + Fore.RESET).strip()

                if pilihan == "1":
                    self.start_bot()
                elif pilihan == "2":
                    self.menu_display_settings()
                elif pilihan == "3":
                    self.menu_network_settings()
                elif pilihan == "4":
                    menu_build_app()
                elif pilihan == "5":
                    self.menu_update_checker()
                elif pilihan == "0":
                    clean_system_processes()
                    print(Fore.CYAN + "\n   Sampai jumpa! Stay safe & keep coding. 🚀\n")
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
