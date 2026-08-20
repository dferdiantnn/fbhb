"""
Interactive User Guide Module for HACKBEN.
Designed to be friendly, clear, detailed, and easy to understand.
"""

from colorama import Fore, Style

def show_user_guide():
    """Display interactive and friendly step-by-step user guide."""
    while True:
        print(Fore.CYAN + "\n" + "=" * 65)
        print(Fore.YELLOW + Style.BRIGHT + "   📖 BUKU PANDUAN PENGGUNAAN HACKBEN (SUPER SIMPLE & DETAIL)")
        print(Fore.CYAN + "=" * 65)
        print(Fore.WHITE + "   Hai Kak! Selamat datang di HACKBEN Automation ✨")
        print(Fore.WHITE + "   Aplikasi ini dibuat praktis banget biar tugas pengisian feedback")
        print(Fore.WHITE + "   bisa selesai otomatis, cepat, rapi, dan tanpa bikin pusing!")
        print(Fore.CYAN + "-" * 65)
        print(Fore.GREEN + "   Pilih bagian yang ingin kamu baca:")
        print(Fore.WHITE + "   1. 🌸 Cara Cepat Pakai Bot (Panduan 3 Langkah)")
        print(Fore.WHITE + "   2. 🏢 Penjelasan Menu 1 (Mulai Kirim Feedback)")
        print(Fore.WHITE + "   3. 👁️  Penjelasan Menu 3 (Pengaturan Tampilan Background/Visual)")
        print(Fore.WHITE + "   4. 🌐 Penjelasan Menu 4 (Pengaturan Jaringan & Proxy)")
        print(Fore.WHITE + "   5. 🛠️  Penjelasan Menu 5 (Jadikan Aplikasi Desktop)")
        print(Fore.WHITE + "   6. 💡 Tips Penting & Pertanyaan Sering Ditanyakan (FAQ)")
        print(Fore.MAGENTA + "   0. ↩️  Kembali ke Menu Utama")
        print(Fore.CYAN + "-" * 65)

        p = input(Fore.YELLOW + "   ?> Mau baca yang mana? (Ketik 0-6): " + Fore.RESET).strip()

        if p == "1":
            print(Fore.CYAN + "\n" + "=" * 60)
            print(Fore.YELLOW + Style.BRIGHT + "   🌸 CARA CEPAT PAKAI BOT (LANGSUNG JALAN)")
            print(Fore.CYAN + "=" * 60)
            print(Fore.WHITE + "   Kalau Kakak lagi buru-buru dan mau langsung jalan, cukup:")
            print(Fore.GREEN + "   Langkah 1:" + Fore.WHITE + " Pilih menu nomor " + Fore.YELLOW + "1" + Fore.WHITE + " di menu utama.")
            print(Fore.GREEN + "   Langkah 2:" + Fore.WHITE + " Masukkan kode store (misal: " + Fore.CYAN + "C55" + Fore.WHITE + ") lalu tekan Enter.")
            print(Fore.GREEN + "   Langkah 3:" + Fore.WHITE + " Pilih Dine In (1) atau Take Away (2), lalu ketik jumlah feedback yang mau dikirim.")
            print(Fore.CYAN + "\n   ✨ Selesai! Bot akan jalan sendiri di background sampai tuntas.")
            input(Fore.YELLOW + "\n   [Tekan Enter untuk kembali...]" + Fore.RESET)

        elif p == "2":
            print(Fore.CYAN + "\n" + "=" * 60)
            print(Fore.YELLOW + Style.BRIGHT + "   🏢 DETAIL MENU 1: MULAI KIRIM FEEDBACK")
            print(Fore.CYAN + "=" * 60)
            print(Fore.WHITE + "   Menu ini adalah fitur utama untuk kirim feedback otomatis.")
            print(Fore.CYAN + "\n   Pilihan & Isian yang Akan Ditanyakan:")
            print(Fore.YELLOW + "   • Kode Store:" + Fore.WHITE + " Masukkan kode outlet kamu (contoh: C55, 518, 521).")
            print(Fore.WHITE + "     Tips: Kalau lupa kodenya, ketik 'list' lalu Enter untuk lihat daftar nama store.")
            print(Fore.YELLOW + "   • Metode Layanan:" + Fore.WHITE + " Pilih 1 untuk Makan di Tempat (Dine In) atau 2 untuk Bawa Pulang (Take Away).")
            print(Fore.YELLOW + "   • Jumlah Feedback:" + Fore.WHITE + " Masukkan berapa kali kuesioner mau diisi (misal: 5 atau 10).")
            print(Fore.GREEN + "\n   🤖 Apa yang Dilakukan Bot?")
            print(Fore.WHITE + "   Setiap kali mengisi, bot otomatis ganti identitas HP (iPhone/Samsung/Oppo/dll),")
            print(Fore.WHITE + "   memilih jawaban bintang 5 / 'Sangat Puas', lalu submit sampai sukses!")
            input(Fore.YELLOW + "\n   [Tekan Enter untuk kembali...]" + Fore.RESET)

        elif p == "3":
            print(Fore.CYAN + "\n" + "=" * 60)
            print(Fore.YELLOW + Style.BRIGHT + "   👁️  DETAIL MENU 3: PENGATURAN TAMPILAN")
            print(Fore.CYAN + "=" * 60)
            print(Fore.WHITE + "   Di sini Kakak bisa atur apakah proses bot mau diperlihatkan atau tidak:")
            print(Fore.GREEN + "\n   1. Mode Background / Headless (Default & Sangat Direkomendasikan):")
            print(Fore.WHITE + "      Bot bekerja diam-diam di latar belakang. Tidak ada jendela browser")
            print(Fore.WHITE + "      yang tiba-tiba muncul di layar, jadi Kakak bisa tetap lanjut kerja/nonton.")
            print(Fore.YELLOW + "\n   2. Mode Visual Window:")
            print(Fore.WHITE + "      Jendela browser akan terbuka dan kelihatan tombol-tombolnya terklik sendiri.")
            print(Fore.WHITE + "      Cocok kalau Kakak penasaran ingin lihat cara bot bekerja.")
            input(Fore.YELLOW + "\n   [Tekan Enter untuk kembali...]" + Fore.RESET)

        elif p == "4":
            print(Fore.CYAN + "\n" + "=" * 60)
            print(Fore.YELLOW + Style.BRIGHT + "   🌐 DETAIL MENU 4: PENGATURAN JARINGAN & PROXY")
            print(Fore.CYAN + "=" * 60)
            print(Fore.WHITE + "   Fitur ini untuk mengatur jalur koneksi internet bot:")
            print(Fore.GREEN + "\n   • Direct Mode (Bawaan):" + Fore.WHITE + " Memakai internet normal laptop kamu. Praktis dan cepat.")
            print(Fore.YELLOW + "\n   • Proxy Mode:" + Fore.WHITE + " Kalau kamu punya proxy SOCKS5/HTTP untuk ganti-ganti IP,")
            print(Fore.WHITE + "     cukup masukkan alamat proxynya di submenu ini.")
            print(Fore.CYAN + "\n   Di menu ini Kakak juga bisa cek alamat IP publik laptop secara instan!")
            input(Fore.YELLOW + "\n   [Tekan Enter untuk kembali...]" + Fore.RESET)

        elif p == "5":
            print(Fore.CYAN + "\n" + "=" * 60)
            print(Fore.YELLOW + Style.BRIGHT + "   🛠️  DETAIL MENU 5: JADIKAN APLIKASI DESKTOP")
            print(Fore.CYAN + "=" * 60)
            print(Fore.WHITE + "   Mau bikin aplikasi file klik (.exe) untuk komputer Windows?")
            print(Fore.WHITE + "   Tinggal pilih menu nomor 5, pilih Windows, dan sistem akan otomatis")
            print(Fore.WHITE + "   membungkus seluruh program menjadi satu file aplikasi yang siap dipakai.")
            print(Fore.WHITE + "   (Untuk pengguna Mac/Linux, menjalankan lewat terminal adalah cara paling cepat & aman).")
            input(Fore.YELLOW + "\n   [Tekan Enter untuk kembali...]" + Fore.RESET)

        elif p == "6":
            print(Fore.CYAN + "\n" + "=" * 60)
            print(Fore.YELLOW + Style.BRIGHT + "   💡 TIPS PENTING & TANYA JAWAB (FAQ)")
            print(Fore.CYAN + "=" * 60)
            print(Fore.GREEN + "   Q: Apakah jawaban kuesionernya dijamin bagus?")
            print(Fore.WHITE + "   A: Pasti! Bot sudah diprogram untuk selalu memilih opsi 'Ya' dan 'Sangat Puas'.")
            print(Fore.GREEN + "\n   Q: Kalau di tengah jalan mau membatalkan/berhenti gimana?")
            print(Fore.WHITE + "   A: Tinggal tekan tombol " + Fore.RED + "CTRL + C" + Fore.WHITE + " di keyboard laptop kamu kapan saja.")
            print(Fore.GREEN + "\n   Q: Apakah bot ini otomatis update kalau ada pembaruan?")
            print(Fore.WHITE + "   A: Ya! Setiap kali program baru dibuka, ia otomatis memeriksa update ke GitHub.")
            input(Fore.YELLOW + "\n   [Tekan Enter untuk kembali...]" + Fore.RESET)

        elif p == "0":
            break
        else:
            continue
