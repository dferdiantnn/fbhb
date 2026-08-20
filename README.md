# ⚡ HACKBEN - Universal Next-Gen Automation Suite
`Versi: v10.9.4 (Latest Release)`

> *High-Performance, Zero-Latency, Cross-Platform Feedback Automation Engine powered by Playwright Async & Dynamic Context Emulation.*

---

## 🚀 Apa yang Baru di Versi Terbaru? (Legacy vs Next-Gen)

Arsitektur **HACKBEN** telah di-refactor secara menyeluruh dari arsitektur monolitik konvensional menjadi modul terdistribusi yang modern, stabil, dan berkinerja tinggi.

| Fitur & Spesifikasi | 🛑 Versi Lama (Legacy v8.x / v9.x) | ⚡ Versi Terbaru (Next-Gen v10+) |
| :--- | :--- | :--- |
| **Sistem Eksekusi** | Terikat Windows murni (`.exe`, `ctypes.windll`, `taskkill`) | **100% Universal Cross-Platform** (macOS M-Series/Intel, Windows, Linux) |
| **Sistem Pembaruan** | Manual download & timpa file sendiri | **⚡ Seamless Auto-Update:** Otomatis memeriksa & menimpa ke rilis GitHub terbaru saat startup |
| **Browser Lifecycle** | Spawn jendela visual GUI berat & rentan crash | **Headless Background Engine:** Berjalan senyap, ringan, hemat memori RAM/CPU |
| **Elemen & Waiting** | *Blind Sleep (`time.sleep`)* yang rawan timeout | **Smart Dynamic DOM Waiting:** Deteksi elemen presisi tinggi (*zero miss aim*) |
| **Fingerprint Isolation**| Restart seluruh proses browser berulang kali | **Isolated Browser Context Sandbox:** Profil perangkat & storage bersih per sesi |
| **Device Library** | ~25 perangkat lawas | **100+ Flagship Mobile Fingerprints** dengan memori *cooldown* 48 jam |
| **Network & Routing** | Ketergantungan aplikasi pihak ketiga desktop | **Native SOCKS5 / HTTP Proxy Tunneling** di level konteks sesi |

> 💡 **Poin Penting:** Repository ini akan terus mendapatkan *continuous deployment (CD)* & *rolling release* langsung dari GitHub untuk memastikan bypass DOM selector dan akurasi bot selalu sinkron dengan sistem target terbaru.

---

## 📁 Struktur Modular

```text
hackben/
├── main.py              # Entry point utama & CLI Interactive Dashboard
├── core/
│   ├── engine.py        # Playwright Core Engine (Dynamic Waiting & Automated DOM Flow)
│   ├── updater.py       # Seamless Startup Auto-Update Manager
│   ├── network.py       # Universal Proxy Handler & Process Terminator
│   ├── ui.py            # Real-Time In-Place Step Progress & Animated Spinner
│   └── builder.py       # Standalone Desktop Compilation Helper (.exe / OS info)
├── data/
│   ├── devices.py       # 100+ Authentic Mobile Fingerprints & Cooldown Tracker
│   └── stores.py        # Store Codes & Outlet Mapping Database
├── requirements.txt     # Dependensi Python
└── README.md
```

---

## 💻 Cara Instalasi & Menjalankan

### 1. Clone Repositori
```bash
git clone https://github.com/dferdiantnn/fbhb.git
cd fbhb
```

### 2. Setup Environment & Dependensi
* **macOS / Linux / Chromebook:**
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

### 3. Eksekusi Program
```bash
python main.py
```
*(Program akan otomatis memeriksa pembaruan ke GitHub sebelum memulai menu).*

---

## 📄 Catatan Penggunaan

Software ini dirancang untuk otomasi pengujian sistem dan efisiensi operasional. Gunakan secara bijak sesuai kebutuhan masing-masing.

Copyright © 2026 **dferdiantnn**. All rights reserved.
