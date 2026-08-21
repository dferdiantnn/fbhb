<p align="center">
  <img src="assets/banner.png" alt="HACKBEN Logo" width="240">
</p>

# ⚡ HACKBEN - Universal Next-Gen Automation Suite
`Versi: v12.0.8 (Latest Release)`

[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue?logo=python&logoColor=white)](https://python.org)
[![Engine](https://img.shields.io/badge/Engine-Playwright%20Chromium%20Async-green?logo=playwright&logoColor=white)](https://playwright.dev)
[![Architecture](https://img.shields.io/badge/Architecture-Universal%20Cross--Platform-orange)](#-arsitektur-sistem--alur-kerja)
[![Auto--Update](https://img.shields.io/badge/Auto--Update-Zero--Cache%20Git%20Rollout-purple)](#-sistem-auto-updater--continuous-deployment)

> **Enterprise-Grade, Zero-Latency, Cross-Platform Automation Suite** dirancang khusus untuk otomatisasi pengisian kuesioner & feedback operasional dengan kecepatan tinggi (~1 detik/sesi), emulasi profil perangkat modern (2020–2026), integrasi jaringan fleksibel, serta proteksi kode mandiri.

---

## 🏗️ Arsitektur Sistem & Alur Kerja

HACKBEN dibangun dengan arsitektur modular berlapis (*Layered Enterprise Architecture*) yang memisahkan antarmuka pengguna CLI, mesin eksekusi browser asinkron, lapisan emulasi perangkat, dan sistem manajemen update.

### 📊 Diagram Alur Kerja End-to-End

```mermaid
flowchart TD
    subgraph LaunchPhase ["🚀 1. INITIATION & UPDATE PHASE"]
        A[Terminal / Operator: python main.py] --> B[core/updater.py: check_and_apply_auto_update]
        B -->|Check GitHub Commit Hash| C{Ada Commit Baru?}
        C -->|Ya| D[Git Pull / Reset Hard origin/main]
        D --> E[Auto-Restart Program]
        C -->|Tidak| F[Render Interactive CLI Dashboard]
    end

    subgraph ConfigPhase ["⚙️ 2. CONFIGURATION PHASE"]
        F --> G[Pilih Target Store & Wilayah]
        G --> H[Pilih Metode Layanan: Dine In / Take Away / Survey]
        H --> I[Tentukan Jumlah Sesi Feedback]
    end

    subgraph ExecutionPhase ["⚡ 3. HIGH-SPEED EXECUTION ENGINE"]
        I --> J[core/engine.py: execute_feedback_session]
        J --> K[data/devices.py: Rotasi Profil Smartphone 2020-2026]
        K --> L[Playwright Context Isolation + Media Asset Blocking]
        L --> M[Membuka Target Portal & Cari Store]
        M --> N[Auto-Route Layanan: Dine In / Take Away / Survey]
        N --> O[Instant Batch DOM Evaluation: Smart Randomizer]
        O --> P[Auto-Submit & Verifikasi Halaman Konfirmasi]
    end

    subgraph CompletionPhase ["📊 4. OPERATIONAL COMPLETION PHASE"]
        P --> Q{Semua Sesi Selesai?}
        Q -->|Belum| R[Jeda 3 Detik Stabilisasi] --> J
        Q -->|Ya| S[Tampilkan Rekapitulasi Hasil di Terminal]
    end
```

---

## 🏛️ Rincian Sub-Sistem Utama (Core Modules)

### 1. ⚡ High-Speed DOM Engine (`core/engine.py`)
* **Asset Interception Strategy:** Menggunakan `context.route()` untuk memblokir unduhan file statis berat seperti gambar (`.png`, `.jpg`, `.webp`, `.svg`) dan web fonts (`.woff`, `.woff2`, `.ttf`). Waktu buka halaman portal turun drastis dari **~4.5 detik** menjadi **~0.3 detik**.
* **Instant Batch DOM Evaluation:** Menjawab seluruh kuesioner multi-step form langsung di level Document Object Model (DOM) dalam satu putaran tanpa jeda animasi tombol manual, menyelesaikan kuesioner dalam **~0.25 detik**.
* **Smart Answer Rules:**
  * Pertanyaan kepuasan otomatis memilih **Sangat Puas / Sangat Baik**.
  * Pertanyaan kesesuaian menu & standar otomatis memilih **Sudah Sesuai / Sesuai**.
  * Pertanyaan biner otomatis memilih **Ya** (kecuali kondisi khusus roti/kempes).
  * Pertanyaan demografi usia otomatis memfilter opsi di atas 13 tahun.
  * Pertanyaan budget pengeluaran otomatis memilih rentang realistis (> Rp 25.000).

### 2. 📱 Device Fingerprinting Matrix (`data/devices.py`)
* **130+ Profil Smartphone Modern (2020–2026):** Mencakup lini flagship dan midrange dari Apple (iPhone 12–16 Pro Max), Samsung (Galaxy S20–S25 Ultra, Z Fold/Flip), Xiaomi, Vivo, Oppo, Infinix, Tecno, ROG Phone, dan Google Pixel.
* **48-Hour Cooldown Tracker:** Mencegah penggunaan profil perangkat yang sama berulang kali dalam kurun waktu 48 jam untuk menjaga keunikan data sesi.
* **Context Emulation:** Mensimulasikan User-Agent, resolusi viewport, pixel ratio, platform OS, touch screen event, dan locale `id-ID` (Asia/Jakarta).

### 3. 🔄 Zero-Cache Auto-Updater (`core/updater.py`)
* Memanfaatkan Git Remote Tracking Commit Hash (`git rev-parse HEAD` vs `git rev-parse origin/main`) untuk memotong cache CDN GitHub hingga 0 detik.
* Menampilkan ringkasan catatan perbaikan (*commit log note*) langsung di terminal saat pembaruan terdeteksi.

---

## 🔒 Panduan Proteksi & Obfuscation Source Code

Untuk menjaga kerahasiaan logika bisnis dan arsitektur script dari inspeksi pihak ketiga maupun operator lapangan, gunakan salah satu metode proteksi berikut:

### Metode 1: AST Code Obfuscation (PyArmor)
Mengenkripsi struktur Abstract Syntax Tree (AST), mengacak nama variabel/fungsi, dan menambahkan runtime key decryption:

```bash
# 1. Install PyArmor
pip install pyarmor

# 2. Obfuscate seluruh project ke folder dist/
pyarmor gen -O dist_protected -r main.py core/ data/

# 3. Jalankan versi terproteksi
cd dist_protected && python main.py
```
*Hasil:* Seluruh file `.py` berubah menjadi deretan binary terenkripsi yang tidak dapat dibaca oleh decompiler atau text editor.

### Metode 2: Kompilasi ke Native Standalone Binary (.EXE / Mach-O)
Mengompilasi seluruh source code Python menjadi file binary mesin mandiri (Standalone Executable):

* **Di Windows (Menghasilkan HACKBEN.exe):**
  ```cmd
  pip install pyinstaller
  pyinstaller --onefile --noconsole --name "HACKBEN" main.py
  ```
* **Kompilasi C via Cython / Nuitka (Performa Ekstrem C-Speed):**
  ```bash
  pip install nuitka
  python -m nuitka --standalone --onefile --plugin-enable=playwright main.py
  ```

---

## 💻 Panduan Instalasi & Penggunaan Cepat

### 1. Clone Repository
```bash
git clone https://github.com/dferdiantnn/fbhb.git
cd fbhb
```

### 2. Konfigurasi Virtual Environment & Dependensi
* **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  playwright install chromium
  ```
* **Windows (Command Prompt / PowerShell):**
  ```cmd
  python -m venv venv
  venv\Scripts\activate
  pip install -r requirements.txt
  playwright install chromium
  ```

### 3. Menjalankan Dashboard
```bash
python main.py
```

---

## 📋 Tabel Rangkuman Perizinan & Setup Cepat (Cheat Sheet)

| Sistem Operasi (OS) | Perizinan Kunci | Perintah / Langkah Sekali Jalan |
| :--- | :--- | :--- |
| **🪟 Windows** (Acer, Asus, Lenovo, dll) | `Set-ExecutionPolicy RemoteSigned` (Izin venv) | `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| **🍎 macOS** (MacBook Air/Pro) | Izin *Screen Recording* (Perekaman Layar) | Buka *System Settings* ➔ *Privacy & Security* ➔ *Screen Recording* ➔ Centang **Terminal** |
| **🐧 Linux** (Ubuntu / Debian / Server) | Playwright System Deps & Scrot | `sudo apt install scrot && playwright install --with-deps chromium` |
| **📱 Android** (via Termux + PRoot Ubuntu) | ARM64 Linux Sandbox & Chromium | `pkg install proot-distro && proot-distro login ubuntu` lalu ikuti langkah Linux |

---

## ⚖️ Lisensi & Tanggung Jawab

Software ini dikembangkan untuk tujuan otomatisasi uji beban, audit alur sistem, dan efisiensi operasional terdistribusi. Pengguna bertanggung jawab penuh atas penggunaan script pada lingkungan masing-masing.

Copyright © 2026 **dferdiantnn**. All rights reserved.
