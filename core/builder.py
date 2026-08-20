"""
Application Builder Module for HACKBEN.
Handles OS-specific standalone compilation and platform guidance.
"""

import sys
import os
import subprocess
import time
from colorama import Fore, Style
from core.network import get_current_os

def menu_build_app():
    """Interactive menu for building standalone desktop applications."""
    current_os = get_current_os()
    
    print(Fore.CYAN + "\n" + "=" * 65)
    print(Fore.YELLOW + Style.BRIGHT + "   🛠️  HACKBEN STANDALONE APPLICATION BUILDER")
    print(Fore.CYAN + "=" * 65)
    print(Fore.WHITE + "   Pilih sistem operasi target aplikasi yang ingin kamu buat:")
    print(Fore.GREEN + "   1. Windows  (.exe)")
    print(Fore.BLUE  + "   2. macOS    (.app / .dmg)")
    print(Fore.CYAN  + "   3. Linux    (.AppImage / .deb)")
    print(Fore.MAGENTA + "   0. Kembali ke Menu Utama")
    print(Fore.CYAN + "-" * 65)

    pilihan = input(Fore.YELLOW + "   ?> Masukkan pilihan (0-3): " + Fore.RESET).strip()

    if pilihan == "1":
        # Windows Build
        print(Fore.YELLOW + "\n   [⚙️ Mempersiapkan Build Windows .exe]")
        if current_os == "windows":
            print(Fore.CYAN + "   Sedang mengompilasi menggunakan PyInstaller...")
            try:
                subprocess.run([
                    sys.executable, "-m", "PyInstaller",
                    "--onefile",
                    "--name", "HACKBEN",
                    "--clean",
                    "main.py"
                ], check=True)
                print(Fore.GREEN + "\n   🎉 Build Berhasil! File EXE tersimpan di folder: dist/HACKBEN.exe")
            except Exception as err:
                print(Fore.RED + f"   ❌ Gagal melakukan build: {err}")
        else:
            print(Fore.YELLOW + f"   [Informasi]: Sistem operasi saat ini adalah {current_os.upper()}.")
            print(Fore.WHITE + "   Binary .EXE Windows membutuhkan environment Windows untuk dikompilasi.")
            print(Fore.CYAN + "\n   💡 Cara Build di PC/Laptop Windows kamu:")
            print(Fore.WHITE + "   1. Clone repo ini di Windows.")
            print(Fore.WHITE + "   2. Jalankan perintah: " + Fore.GREEN + "pip install pyinstaller")
            print(Fore.WHITE + "   3. Jalankan: " + Fore.GREEN + "pyinstaller --onefile --name HACKBEN main.py")
        
        input(Fore.YELLOW + "\n   [Tekan Enter untuk kembali...]" + Fore.RESET)

    elif pilihan == "2":
        # macOS notice
        print(Fore.YELLOW + "\n   " + "=" * 60)
        print(Fore.YELLOW + "   🍏 STATUS PENGEMBANGAN MACOS (.APP / .DMG)")
        print(Fore.YELLOW + "   " + "=" * 60)
        print(Fore.WHITE + "   Status: " + Fore.RED + "[SEDANG DALAM TAHAP PENGEMBANGAN]")
        print(Fore.WHITE + "\n   Keterangan Teknis:")
        print(Fore.CYAN + "   • Sistem keamanan Gatekeeper macOS dan arsitektur Apple Silicon")
        print(Fore.CYAN + "     mewajibkan proses Notarization serta sertifikat Apple Developer")
        print(Fore.CYAN + "     ID resmi agar aplikasi desktop GUI dapat berjalan tanpa terblokir.")
        print(Fore.GREEN + "\n   💡 Solusi Terbaik:")
        print(Fore.WHITE + "   Untuk stabilitas dan performa penuh di Mac, program HACKBEN")
        print(Fore.WHITE + "   didesain berjalan 100% optimal dan aman langsung via Terminal.")
        print(Fore.YELLOW + "   " + "=" * 60)
        input(Fore.YELLOW + "\n   [Tekan Enter untuk kembali...]" + Fore.RESET)

    elif pilihan == "3":
        # Linux notice
        print(Fore.CYAN + "\n   " + "=" * 60)
        print(Fore.CYAN + "   🐧 STATUS PENGEMBANGAN LINUX / CHROMEBOOK")
        print(Fore.CYAN + "   " + "=" * 60)
        print(Fore.WHITE + "   Status: " + Fore.RED + "[SEDANG DALAM TAHAP PENGEMBANGAN]")
        print(Fore.WHITE + "\n   Keterangan Keamanan:")
        print(Fore.CYAN + "   • Distribusi paket binary Linux (.AppImage / .deb) sedang")
        print(Fore.CYAN + "     dalam tahap audit keamanan ketat untuk memastikan tidak ada")
        print(Fore.CYAN + "     vektor kerentanan malware ataupun penyalahgunaan hak akses root.")
        print(Fore.GREEN + "\n   💡 Solusi Terbaik:")
        print(Fore.WHITE + "   Jalankan script Python secara native melalui Terminal (CLI)")
        print(Fore.WHITE + "   untuk transparansi kode dan keamanan sistem maksimal.")
        print(Fore.CYAN + "   " + "=" * 60)
        input(Fore.YELLOW + "\n   [Tekan Enter untuk kembali...]" + Fore.RESET)
