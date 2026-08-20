# ⚡ HACKBEN - Universal Cross-Platform Automation Suite

Bot otomatisasi feedback kuesioner berbasis **Python** & **Playwright** dengan arsitektur modern yang mendukung penuh **macOS (Apple Silicon & Intel)**, **Windows**, dan **Linux / Chromebook**.

---

## 🌟 Fitur Utama

- **100% Cross-Platform:** Berjalan secara native tanpa dependensi biner platform tertentu.
- **Headless & Background Operation:** Berjalan sepenuhnya di latar belakang tanpa membuka jendela visual (bisa diatur ke mode visual jika diinginkan).
- **In-Place Progress & Spinner:** Tampilan terminal interaktif dan informatif (Step 1 s/d 7) dengan animasi spinner yang tidak memenuhi baris baru.
- **100+ Authentic Device Fingerprints:** Database profil perangkat seluler lengkap (iPhone, Samsung Galaxy, Xiaomi, Poco, Vivo, Oppo, Infinix, ROG, Google Pixel) dengan rotasi otomatis dan memori *cooldown* 48 jam.
- **Smart Dynamic Waits:** Interaksi cepat, tepat, dan akurat seketika elemen muncul di DOM tanpa *blind delay* yang rawan gagal.
- **Universal Proxy Routing:** Mendukung integrasi SOCKS5 / HTTP Proxy per sesi browser untuk manipulasi dan rotasi IP.
- **Application Builder Helper:** Menu pembuatan aplikasi desktop mandiri (`.exe`) untuk Windows dan panduan terminal untuk macOS/Linux.

---

## 📁 Struktur Proyek

```text
hackben/
├── main.py              # Entry point utama & Dashboard interaktif
├── core/
│   ├── engine.py        # Mesin otomasi Playwright (Smart Wait & Flow Kuesioner)
│   ├── network.py       # Pengelola Proxy, IP Checker & Pembersih Proses
│   ├── ui.py            # Animasi Spinner & Indikator Step Progress
│   └── builder.py       # Menu Build Desktop App (.exe / info OS)
├── data/
│   ├── devices.py       # Database 100+ Fingerprint Perangkat & Cooldown Memory
│   └── stores.py        # Database Kode & Nama Store
├── requirements.txt     # Daftar dependensi Python
└── README.md
```

---

## 🚀 Cara Instalasi & Menjalankan

### 1. Kloning Repositori
```bash
git clone https://github.com/dferdiantnn/fbhb.git
cd fbhb
```

### 2. Buat Virtual Environment & Install Dependensi

* **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  playwright install chromium
  ```

* **Windows:**
  ```cmd
  python -m venv venv
  venv\Scripts\activate
  pip install -r requirements.txt
  playwright install chromium
  ```

### 3. Jalankan Program
```bash
python main.py
```

---

## 📜 Lisensi & Penggunaan
Project ini dibuat untuk tujuan otomasi, benchmarking, dan pengujian keandalan antarmuka web. Gunakan secara bijak dan bertanggung jawab.
