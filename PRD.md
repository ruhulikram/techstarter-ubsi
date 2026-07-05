# Product Requirements Document (PRD)

## UBSI Student Development Environment Installer

**Document Status:** Draft for Agent Implementation  
**Version:** 1.0.0  
**Target Repository:** `ubsi-student-dev-setup`  
**Primary Platforms:** Windows 10/11 and macOS  
**Primary Users:** Mahasiswa UBSI Program Studi Sistem Informasi (SI) dan Teknologi Informasi (TI)  
**Document Language:** Indonesian  
**Implementation Language:** PowerShell, Bash, JSON, YAML, Markdown  

---

## 1. Ringkasan Produk

UBSI Student Development Environment Installer adalah repository GitHub yang menyediakan sistem instalasi berbasis terminal untuk membantu mahasiswa menyiapkan software, bahasa pemrograman, package manager, library, extension, dan konfigurasi dasar yang digunakan selama perkuliahan.

Produk harus mendukung Windows dan macOS dengan alur penggunaan yang sederhana, aman, modular, dapat diverifikasi, dapat diulang, dan mudah dipelihara. Mahasiswa tidak diwajibkan memahami detail package manager, environment variable, virtual environment, atau dependency management untuk dapat menyiapkan lingkungan pengembangan awal.

Produk bukan sekadar kumpulan command instalasi. Produk harus berfungsi sebagai sistem onboarding teknis yang:

1. Mendeteksi sistem operasi dan arsitektur perangkat.
2. Memeriksa prasyarat dan spesifikasi minimum.
3. Menawarkan profil instalasi sesuai jurusan, semester, dan kebutuhan mata kuliah.
4. Menginstal software melalui sumber resmi atau package manager yang sesuai.
5. Memisahkan software wajib, opsional, berat, dan manual.
6. Mengatur environment variable yang diperlukan.
7. Membuat Python virtual environment terisolasi.
8. Menginstal library Python seperti `pandas`.
9. Menginstal dan memverifikasi Composer.
10. Menyediakan log, laporan hasil, dan panduan troubleshooting.
11. Dapat dijalankan ulang tanpa merusak instalasi yang sudah ada.
12. Dapat dikembangkan oleh contributor atau agent tanpa mengubah arsitektur inti secara sembarangan.

---

## 2. Latar Belakang dan Masalah

Banyak mahasiswa mengalami kesulitan saat menginstal lingkungan pengembangan untuk praktikum, antara lain:

- Tidak mengetahui software yang perlu dipasang.
- Mengunduh installer dari sumber tidak resmi.
- Menggunakan versi software yang tidak kompatibel dengan materi kuliah.
- Gagal mengatur `PATH`.
- Mengalami konflik antara PHP dari XAMPP, PHP standalone, dan Composer.
- Menginstal library Python secara global sehingga terjadi konflik dependency.
- Tidak mengetahui perbedaan `python`, `python3`, dan `py`.
- Tidak dapat memverifikasi apakah instalasi sudah benar.
- Kesulitan memasang software berat seperti Android Studio, Docker Desktop, VirtualBox, dan Packet Tracer.
- Mengalami perbedaan langkah instalasi antara Windows dan macOS.
- Tidak memiliki dokumentasi troubleshooting yang seragam.

Akibatnya, waktu praktikum banyak terbuang untuk menyelesaikan masalah instalasi yang sebenarnya dapat distandardisasi.

---

## 3. Visi Produk

Menyediakan satu repository GitHub yang menjadi standar onboarding lingkungan pengembangan mahasiswa UBSI SI dan TI, sehingga mahasiswa dapat menyiapkan perangkat dengan aman melalui panduan dan command yang konsisten di Windows maupun macOS.

---

## 4. Tujuan Produk

### 4.1 Tujuan Utama

- Menurunkan tingkat kegagalan instalasi software perkuliahan.
- Mengurangi ketergantungan mahasiswa pada instalasi manual.
- Memastikan software berasal dari sumber resmi.
- Menyediakan konfigurasi yang konsisten antarmahasiswa.
- Memudahkan dosen, asisten, dan komunitas kampus memberikan dukungan teknis.
- Membuat lingkungan pengembangan dapat diverifikasi melalui satu command.

### 4.2 Tujuan Teknis

- Mendukung instalasi berbasis `winget` pada Windows.
- Mendukung instalasi berbasis Homebrew pada macOS.
- Mendukung instalasi Composer setelah PHP tersedia.
- Mendukung instalasi library Python melalui `venv` dan file requirements.
- Menyediakan profil SI, TI, Web, Data Science, Mobile, Networking, Database, dan Core.
- Menyediakan mekanisme dry run, logging, retry, skip, dan verification.
- Menyediakan manifest paket terpusat agar script tidak berisi hardcode berulang.

---

## 5. Non-Goals

Produk tidak bertujuan untuk:

- Menginstal software bajakan, crack, keygen, atau lisensi ilegal.
- Membypass login, lisensi, persetujuan pengguna, atau kebijakan vendor.
- Mengubah konfigurasi BIOS secara otomatis.
- Memaksa instalasi semua software pada semua perangkat.
- Menjamin kompatibilitas untuk seluruh versi Windows dan macOS.
- Menggantikan dokumentasi resmi software.
- Menyimpan password, token, API key, atau credential pengguna.
- Mengelola project source code mahasiswa.
- Menjadi package manager baru.
- Menghapus software pengguna tanpa persetujuan eksplisit.

---

## 6. Persona Pengguna

### 6.1 Mahasiswa Semester Awal

Karakteristik:

- Minim pengalaman terminal.
- Belum memahami environment variable.
- Membutuhkan Git, VS Code, Python, Java, Node.js, dan browser.
- Membutuhkan instruksi yang sangat jelas.

Kebutuhan:

- Mode interaktif.
- Pesan kesalahan sederhana.
- Rekomendasi paket sesuai semester.
- Verifikasi otomatis.

### 6.2 Mahasiswa Sistem Informasi

Karakteristik:

- Membutuhkan pengembangan web, database, API, dan data analysis dasar.

Kebutuhan:

- PHP atau XAMPP.
- Composer.
- Laravel tooling.
- MySQL/MariaDB dan MySQL Workbench.
- Postman.
- Node.js.
- Python dan `pandas`.

### 6.3 Mahasiswa Teknologi Informasi

Karakteristik:

- Membutuhkan networking, virtualisasi, keamanan, mobile, dan cloud.

Kebutuhan:

- Wireshark.
- VirtualBox.
- Docker Desktop.
- Android Studio.
- JDK.
- Python.
- Packet Tracer dengan panduan instalasi manual.

### 6.4 Dosen atau Asisten Praktikum

Kebutuhan:

- Daftar software dan versi yang konsisten.
- Command verifikasi cepat.
- Log untuk membantu diagnosis.
- File konfigurasi yang mudah diperbarui.

### 6.5 Maintainer Repository

Kebutuhan:

- Struktur code modular.
- Manifest terpusat.
- Test otomatis.
- Dokumentasi kontribusi.
- Release versioning.
- Kemampuan mengganti package ID tanpa mengedit seluruh script.

---

## 7. Prinsip Produk

1. **Safe by default**  
   Tidak menjalankan penghapusan, overwrite, atau perubahan sistem berisiko tanpa persetujuan.

2. **Official source only**  
   Software hanya diunduh melalui package manager resmi atau situs vendor resmi.

3. **Idempotent**  
   Script dapat dijalankan ulang tanpa menghasilkan instalasi ganda atau kerusakan konfigurasi.

4. **Modular**  
   Profil dan paket dapat ditambah tanpa menulis ulang core installer.

5. **Transparent**  
   Sebelum instalasi, tampilkan paket yang akan dipasang dan konsekuensinya.

6. **Cross-platform parity**  
   Perilaku Windows dan macOS harus konsisten sejauh memungkinkan.

7. **Beginner-friendly**  
   Pesan terminal harus mudah dipahami mahasiswa pemula.

8. **Verifiable**  
   Setiap instalasi wajib memiliki command verifikasi.

9. **No global Python pollution**  
   Library Python dipasang dalam virtual environment.

10. **Minimal privilege**  
    Hak administrator hanya digunakan saat benar-benar dibutuhkan.

---

## 8. Scope Produk

### 8.1 In Scope untuk Versi 1.0

- Installer Windows berbasis PowerShell.
- Installer macOS berbasis Bash.
- Package manager detection.
- Profile selection.
- Semester-based recommendation.
- Manifest paket berbasis JSON.
- Core package installation.
- Composer installation dan verification.
- Python virtual environment.
- Instalasi `pandas`.
- Logging.
- Verification scripts.
- Dry run.
- Manual installation guidance.
- GitHub Actions untuk lint dan validasi dasar.
- Release ZIP untuk Windows dan macOS.
- README utama dan dokumentasi terpisah.

### 8.2 Out of Scope untuk Versi 1.0

- GUI desktop installer.
- Auto-update background service.
- Central telemetry.
- Login akun UBSI.
- Integrasi LMS.
- Remote device management.
- Instalasi Linux penuh.
- Auto-configure BIOS virtualization.
- Auto-login Cisco, Google, Oracle, Docker, atau vendor lain.

---

## 9. Daftar Profil Instalasi

### 9.1 Core

Paket minimum untuk seluruh mahasiswa:

- Git
- Visual Studio Code
- Python
- Java JDK
- Node.js LTS
- npm
- Postman
- Browser modern
- 7-Zip atau alternatif macOS
- Windows Terminal pada Windows

### 9.2 Sistem Informasi

Mencakup Core ditambah:

- XAMPP atau PHP stack yang dipilih
- PHP CLI
- Composer
- MySQL atau MariaDB
- MySQL Workbench
- Laravel installer opsional
- Node.js tooling
- Postman
- Python basic environment
- `pandas`
- JupyterLab opsional

### 9.3 Teknologi Informasi

Mencakup Core ditambah:

- Wireshark
- VirtualBox
- Docker Desktop opsional
- Android Studio opsional
- JDK
- Python
- Packet Tracer manual
- Git
- VS Code

### 9.4 Web Programming

- Git
- VS Code
- PHP
- Composer
- Node.js LTS
- npm
- MySQL/MariaDB
- Postman
- Browser
- Laravel installer opsional

### 9.5 Data Science

- Python
- Python virtual environment
- pandas
- numpy
- matplotlib
- scikit-learn
- jupyterlab
- openpyxl
- requests

### 9.6 Mobile Programming

- JDK
- Android Studio
- Android SDK tools
- Git
- VS Code opsional
- Node.js untuk React Native opsional

### 9.7 Networking

- Wireshark
- VirtualBox
- Packet Tracer manual
- PuTTY atau OpenSSH client pada Windows jika diperlukan
- Docker Desktop opsional

### 9.8 Database

- MySQL atau MariaDB
- MySQL Workbench
- PostgreSQL opsional
- DBeaver opsional

### 9.9 Full

Menggabungkan seluruh profil, tetapi harus menampilkan peringatan bahwa:

- Membutuhkan ruang penyimpanan besar.
- Membutuhkan RAM memadai.
- Proses instalasi lebih berat.
- Tidak direkomendasikan untuk semester awal.

---

## 10. Rekomendasi Berdasarkan Semester

Konfigurasi semester harus dapat diubah melalui manifest. Default awal:

### Semester 1

- Core
- Python basic
- Java JDK
- Git
- VS Code

### Semester 2

- Core
- Database
- Web Programming dasar
- Composer
- pandas

### Semester 3

- Sistem Informasi atau Teknologi Informasi sesuai jurusan
- Postman
- MySQL Workbench
- Wireshark untuk TI

### Semester 4

- Laravel tooling untuk SI
- Android Studio untuk mata kuliah mobile
- VirtualBox untuk TI

### Semester 5 ke atas

- Docker Desktop opsional
- JupyterLab atau Data Science stack
- Cloud dan tooling lanjutan

Catatan: daftar semester bukan sumber akademik resmi dan harus dapat disesuaikan berdasarkan RPS atau arahan dosen.

---

## 11. User Flow

### 11.1 Flow Interaktif

1. Pengguna mengunduh release ZIP atau clone repository.
2. Pengguna membuka README.
3. Pengguna memilih panduan Windows atau macOS.
4. Pengguna menjalankan installer.
5. Installer mendeteksi OS, arsitektur, dan package manager.
6. Installer memeriksa spesifikasi dasar.
7. Pengguna memilih jurusan.
8. Pengguna memilih semester.
9. Installer merekomendasikan profil.
10. Pengguna dapat memilih atau menghapus paket opsional.
11. Installer menampilkan ringkasan paket.
12. Pengguna menyetujui instalasi.
13. Installer memasang paket satu per satu.
14. Installer menyiapkan Python virtual environment.
15. Installer menginstal `pandas` dan requirements lainnya.
16. Installer memasang Composer setelah PHP terdeteksi.
17. Installer menjalankan verifikasi.
18. Installer menampilkan summary berhasil, gagal, dilewati, dan manual.
19. Installer menyimpan log dan report.

### 11.2 Flow Non-Interaktif

Contoh Windows:

```powershell
.\scripts\windows\setup.ps1 `
  -Jurusan SI `
  -Semester 3 `
  -Profiles Core,Web,Data `
  -NonInteractive
```

Contoh macOS:

```bash
./scripts/macos/setup.sh \
  --jurusan SI \
  --semester 3 \
  --profiles core,web,data \
  --non-interactive
```

### 11.3 Dry Run

Windows:

```powershell
.\scripts\windows\setup.ps1 -Jurusan SI -Semester 3 -DryRun
```

macOS:

```bash
./scripts/macos/setup.sh --jurusan SI --semester 3 --dry-run
```

Dry run tidak boleh mengubah sistem. Output harus menampilkan:

- Paket yang akan dipasang.
- Paket yang sudah ada.
- Paket manual.
- Perubahan PATH yang direncanakan.
- Virtual environment yang akan dibuat.
- Estimasi kebutuhan storage dari metadata jika tersedia.

---

## 12. Struktur Repository

```text
ubsi-student-dev-setup/
├── README.md
├── PRD.md
├── LICENSE
├── CONTRIBUTING.md
├── SECURITY.md
├── CODE_OF_CONDUCT.md
├── CHANGELOG.md
│
├── config/
│   ├── packages.json
│   ├── profiles.json
│   ├── semesters.json
│   ├── versions.json
│   ├── manual-packages.json
│   └── schema/
│       ├── packages.schema.json
│       ├── profiles.schema.json
│       └── semesters.schema.json
│
├── scripts/
│   ├── windows/
│   │   ├── setup.ps1
│   │   ├── verify.ps1
│   │   ├── diagnostics.ps1
│   │   ├── repair.ps1
│   │   ├── common.psm1
│   │   └── modules/
│   │       ├── PackageManager.psm1
│   │       ├── Environment.psm1
│   │       ├── Python.psm1
│   │       ├── Composer.psm1
│   │       ├── Verification.psm1
│   │       └── Logging.psm1
│   │
│   └── macos/
│       ├── setup.sh
│       ├── verify.sh
│       ├── diagnostics.sh
│       ├── repair.sh
│       └── lib/
│           ├── package_manager.sh
│           ├── environment.sh
│           ├── python.sh
│           ├── composer.sh
│           ├── verification.sh
│           └── logging.sh
│
├── requirements/
│   ├── python-basic.txt
│   ├── python-data-science.txt
│   ├── python-web.txt
│   └── constraints.txt
│
├── vscode/
│   ├── extensions-core.txt
│   ├── extensions-web.txt
│   ├── extensions-data.txt
│   ├── extensions-mobile.txt
│   └── extensions-networking.txt
│
├── docs/
│   ├── windows.md
│   ├── macos.md
│   ├── troubleshooting.md
│   ├── software-list.md
│   ├── manual-installation.md
│   ├── architecture.md
│   ├── security.md
│   ├── faq.md
│   └── screenshots/
│
├── tests/
│   ├── powershell/
│   │   ├── manifest.Tests.ps1
│   │   ├── profiles.Tests.ps1
│   │   ├── commands.Tests.ps1
│   │   └── idempotency.Tests.ps1
│   ├── bash/
│   │   ├── test_manifest.sh
│   │   ├── test_profiles.sh
│   │   └── test_commands.sh
│   └── fixtures/
│
├── tools/
│   ├── validate-manifest.py
│   ├── generate-checksums.py
│   ├── build-release.py
│   └── check-package-availability.py
│
├── logs/
│   └── .gitkeep
│
└── .github/
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.yml
    │   ├── software_request.yml
    │   └── documentation.yml
    ├── pull_request_template.md
    └── workflows/
        ├── validate.yml
        ├── powershell-tests.yml
        ├── bash-tests.yml
        ├── security.yml
        └── release.yml
```

---

## 13. Manifest Paket

### 13.1 Tujuan

Semua definisi paket harus disimpan di `config/packages.json`. Script tidak boleh memiliki package ID yang tersebar di banyak file.

### 13.2 Contoh Struktur Paket

```json
{
  "schemaVersion": "1.0.0",
  "packages": [
    {
      "key": "python",
      "name": "Python",
      "description": "Bahasa pemrograman Python untuk praktikum dan data analysis.",
      "category": "language",
      "profiles": ["core", "si", "ti", "data"],
      "minimumSemester": 1,
      "required": true,
      "heavy": false,
      "manual": false,
      "dependencies": [],
      "verification": [
        "python --version",
        "python3 --version",
        "py -3 --version"
      ],
      "windows": {
        "manager": "winget",
        "id": "Python.Python.3.13",
        "scope": "user",
        "fallbackIds": [
          "Python.Python.3.12"
        ]
      },
      "macos": {
        "manager": "brew",
        "id": "python"
      }
    },
    {
      "key": "composer",
      "name": "Composer",
      "description": "Dependency manager untuk PHP.",
      "category": "package-manager",
      "profiles": ["si", "web"],
      "minimumSemester": 2,
      "required": true,
      "heavy": false,
      "manual": false,
      "dependencies": ["php"],
      "verification": [
        "composer --version",
        "composer diagnose"
      ],
      "windows": {
        "manager": "custom",
        "installer": "Install-Composer"
      },
      "macos": {
        "manager": "brew",
        "id": "composer"
      }
    },
    {
      "key": "packet-tracer",
      "name": "Cisco Packet Tracer",
      "category": "networking",
      "profiles": ["ti", "networking"],
      "minimumSemester": 2,
      "required": false,
      "heavy": true,
      "manual": true,
      "dependencies": [],
      "manualGuide": "docs/manual-installation.md#cisco-packet-tracer"
    }
  ]
}
```

### 13.3 Aturan Manifest

- `key` harus unik.
- `key` hanya menggunakan huruf kecil, angka, dan tanda hubung.
- Paket harus memiliki minimal satu profile.
- Paket manual tidak boleh memiliki command download otomatis.
- Paket dengan dependency wajib diproses setelah dependency berhasil.
- Package ID harus dapat memiliki fallback.
- Verification command harus aman dan read-only.
- Versi paket tidak boleh dipatok tanpa alasan kompatibilitas.

---

## 14. Python Environment Requirements

### 14.1 Prinsip

Library Python tidak boleh dipasang secara global sebagai default.

### 14.2 Lokasi Virtual Environment

Windows:

```text
%USERPROFILE%\.ubsi\venvs\python-basic
```

macOS:

```text
$HOME/.ubsi/venvs/python-basic
```

### 14.3 Requirements Minimum

`requirements/python-basic.txt`:

```text
pandas
```

`requirements/python-data-science.txt`:

```text
numpy
pandas
matplotlib
scikit-learn
jupyterlab
openpyxl
requests
```

### 14.4 Constraints

File `requirements/constraints.txt` dapat digunakan bila diperlukan untuk mengunci versi yang sudah diuji.

Contoh:

```text
pandas>=2.2,<3.0
numpy>=1.26,<3.0
```

### 14.5 Proses Instalasi Python

1. Deteksi executable Python.
2. Prioritas Windows: `py -3`, lalu `python`.
3. Prioritas macOS: `python3`.
4. Buat virtual environment jika belum ada.
5. Upgrade `pip`, `setuptools`, dan `wheel`.
6. Instal requirements.
7. Verifikasi import `pandas`.
8. Simpan lokasi environment pada summary.
9. Tampilkan command aktivasi.

### 14.6 Verifikasi pandas

```python
import pandas as pd
print(pd.__version__)
```

Status dianggap berhasil jika:

- Python environment ditemukan.
- Import tidak menghasilkan exception.
- Versi dapat dicetak.

---

## 15. Composer Requirements

### 15.1 Prasyarat

- PHP CLI harus tersedia.
- Pada Windows, PHP dapat berasal dari PATH atau XAMPP.
- Pada macOS, Composer dapat dipasang melalui Homebrew.

### 15.2 Deteksi PHP Windows

Urutan deteksi:

1. `Get-Command php`
2. `C:\xampp\php\php.exe`
3. Path yang didefinisikan dalam manifest.
4. Lokasi alternatif yang dikonfigurasi pengguna.

### 15.3 Instalasi Composer Windows

- Unduh installer hanya dari domain resmi Composer.
- Ambil signature installer terbaru.
- Verifikasi hash SHA-384.
- Batalkan instalasi jika hash tidak cocok.
- Instal Composer pada lokasi user-space.
- Buat wrapper `composer.bat` bila diperlukan.
- Tambahkan direktori Composer ke user PATH secara idempotent.

### 15.4 Instalasi Composer macOS

Default:

```bash
brew install composer
```

### 15.5 Verifikasi Composer

```text
composer --version
composer diagnose
```

`composer diagnose` boleh menghasilkan warning tertentu, tetapi command harus dapat berjalan. Error koneksi internet tidak boleh dianggap sebagai kerusakan instalasi jika executable Composer dapat dijalankan.

---

## 16. Functional Requirements

### FR-001 — Deteksi Sistem Operasi

Installer harus mendeteksi sistem operasi dan menolak berjalan jika platform tidak didukung.

**Acceptance Criteria:**

- Windows menjalankan PowerShell installer.
- macOS menjalankan Bash installer.
- Linux menampilkan pesan belum didukung.

### FR-002 — Deteksi Arsitektur

Installer harus mendeteksi x64 atau ARM64.

**Acceptance Criteria:**

- Arsitektur dicatat dalam log.
- Paket yang tidak kompatibel ditandai manual atau skipped.

### FR-003 — Deteksi Package Manager

- Windows: WinGet.
- macOS: Homebrew.

**Acceptance Criteria:**

- Jika package manager tersedia, versi ditampilkan.
- Jika tidak tersedia, installer memberikan panduan pemasangan.
- Installer tidak mengunduh package manager dari sumber tidak resmi.

### FR-004 — Mode Interaktif

Installer harus menyediakan pilihan jurusan, semester, dan profil.

**Acceptance Criteria:**

- Input tidak valid diminta ulang.
- Default aman tersedia.
- Ringkasan ditampilkan sebelum instalasi.

### FR-005 — Mode Non-Interaktif

Installer harus mendukung parameter command-line.

**Acceptance Criteria:**

- Tidak meminta input selama proses.
- Menghasilkan exit code yang benar.
- Semua opsi terdokumentasi.

### FR-006 — Dry Run

Installer harus mendukung simulasi tanpa perubahan sistem.

**Acceptance Criteria:**

- Tidak menginstal paket.
- Tidak mengubah PATH.
- Tidak membuat virtual environment.
- Menampilkan rencana lengkap.

### FR-007 — Instalasi Paket

Installer harus memasang paket sesuai manifest.

**Acceptance Criteria:**

- Paket yang sudah ada dilewati.
- Paket gagal tidak menghentikan paket independen berikutnya.
- Dependency failure menandai dependent package sebagai blocked.

### FR-008 — Composer

Installer harus memasang dan memverifikasi Composer.

**Acceptance Criteria:**

- Composer hanya diproses setelah PHP tersedia.
- Signature diverifikasi pada Windows.
- `composer --version` berhasil.

### FR-009 — Python Virtual Environment

Installer harus membuat environment Python terisolasi.

**Acceptance Criteria:**

- Environment dibuat di folder `.ubsi/venvs`.
- `pip` diperbarui.
- `pandas` terpasang.
- Import berhasil.

### FR-010 — Verifikasi

Installer harus memiliki script verifikasi terpisah.

**Acceptance Criteria:**

- Verifikasi dapat dijalankan tanpa instalasi ulang.
- Hasil ditampilkan per software.
- Hasil dapat diekspor ke file report.

### FR-011 — Logging

Semua langkah penting harus dicatat.

**Acceptance Criteria:**

- Log memiliki timestamp.
- Log mencatat OS, arsitektur, profile, command, status, dan error.
- Credential tidak pernah ditulis.

### FR-012 — Manual Package Guidance

Software manual harus ditampilkan bersama panduan.

**Acceptance Criteria:**

- Packet Tracer tidak diunduh dari mirror tidak resmi.
- Link panduan mengarah ke dokumentasi repository.
- Status akhir adalah `MANUAL_REQUIRED`.

### FR-013 — Resume

Installer harus dapat dijalankan ulang setelah kegagalan.

**Acceptance Criteria:**

- Paket berhasil tidak dipasang ulang.
- Paket gagal dapat dicoba ulang.
- Tidak ada duplikasi PATH.

### FR-014 — Repair Mode

Installer harus menyediakan mode repair dasar.

**Acceptance Criteria:**

- Memeriksa PATH.
- Memeriksa Python environment.
- Memeriksa Composer wrapper.
- Tidak menghapus data project pengguna.

### FR-015 — Uninstall Guidance

Versi 1.0 tidak wajib melakukan uninstall otomatis penuh, tetapi harus menyediakan panduan.

**Acceptance Criteria:**

- Tidak ada bulk uninstall tanpa konfirmasi.
- Folder `.ubsi/venvs` dapat dihapus dengan command yang dijelaskan.

---

## 17. Non-Functional Requirements

### NFR-001 — Security

- Hanya menggunakan HTTPS.
- Memverifikasi installer Composer.
- Tidak menggunakan `Invoke-Expression` terhadap konten remote.
- Tidak menjalankan script remote langsung melalui pipe sebagai alur default.
- Tidak menyimpan credential.

### NFR-002 — Reliability

- Kegagalan satu paket tidak boleh menghentikan seluruh proses kecuali paket core kritis.
- Script harus memiliki retry terbatas untuk network error.
- Tidak boleh terjadi infinite loop.

### NFR-003 — Maintainability

- Package metadata berada di manifest.
- Function maksimal memiliki satu tanggung jawab utama.
- Script lint harus lolos sebelum merge.

### NFR-004 — Usability

- Bahasa utama Indonesia.
- Pesan error harus menjelaskan tindakan berikutnya.
- Warna terminal hanya sebagai tambahan, bukan satu-satunya indikator.

### NFR-005 — Performance

- Deteksi paket harus menggunakan command paling efisien.
- Tidak melakukan update package manager berkali-kali dalam satu sesi.
- Verification read-only harus selesai secepat mungkin.

### NFR-006 — Compatibility

Windows minimum:

- Windows 10 versi yang mendukung WinGet.
- PowerShell 5.1 minimum, PowerShell 7 direkomendasikan.

macOS minimum:

- Versi yang masih dapat menjalankan Homebrew yang digunakan.
- Bash atau Zsh shell environment.

### NFR-007 — Accessibility

- Jangan mengandalkan emoji untuk status utama.
- Status harus ditulis jelas: SUCCESS, FAILED, SKIPPED, MANUAL, BLOCKED.

---

## 18. Status dan Exit Code

### Status Paket

- `PENDING`
- `INSTALLED`
- `ALREADY_INSTALLED`
- `UPDATED`
- `FAILED`
- `SKIPPED`
- `BLOCKED`
- `MANUAL_REQUIRED`
- `NOT_COMPATIBLE`

### Exit Code

- `0`: seluruh paket wajib berhasil; paket opsional boleh gagal.
- `1`: satu atau lebih paket wajib gagal.
- `2`: konfigurasi atau argument invalid.
- `3`: platform tidak didukung.
- `4`: package manager tidak tersedia.
- `5`: verifikasi keamanan gagal.

---

## 19. Logging Specification

### 19.1 Lokasi Log

Windows:

```text
%USERPROFILE%\.ubsi\logs\install-YYYYMMDD-HHMMSS.log
```

macOS:

```text
$HOME/.ubsi/logs/install-YYYYMMDD-HHMMSS.log
```

### 19.2 Format Minimum

```text
2026-07-05T17:30:12+08:00 | INFO | SYSTEM | OS=Windows 11 | ARCH=x64
2026-07-05T17:30:15+08:00 | INFO | PACKAGE | key=python | status=ALREADY_INSTALLED
2026-07-05T17:30:20+08:00 | ERROR | PACKAGE | key=composer | reason=PHP_NOT_FOUND
```

### 19.3 Redaction

Log harus menyamarkan:

- Username bila diminta melalui privacy mode.
- Token.
- Password.
- API key.
- Credential URL.

---

## 20. Verification Report

Report dapat dibuat dalam format Markdown atau JSON.

Contoh `verification-report.md`:

```markdown
# UBSI Environment Verification

- OS: Windows 11
- Architecture: x64
- Profile: SI, Web, Data

| Component | Status | Version | Notes |
|---|---|---:|---|
| Git | PASS | 2.x | - |
| Python | PASS | 3.13.x | - |
| pandas | PASS | 2.x | venv: python-basic |
| PHP | PASS | 8.2.x | XAMPP |
| Composer | PASS | 2.x | diagnose completed |
| Packet Tracer | MANUAL | - | Requires Cisco account |
```

---

## 21. Security Requirements

1. Jangan menjalankan script remote langsung dari URL sebagai metode utama README.
2. Release harus menyediakan checksum SHA-256.
3. GitHub Actions release harus menghasilkan `checksums.txt`.
4. Installer Composer wajib memverifikasi signature.
5. Package manager harus menerima agreement hanya saat pengguna telah diberi informasi.
6. Script tidak boleh mematikan antivirus atau firewall.
7. Script tidak boleh menonaktifkan execution policy secara permanen.
8. Pada Windows, gunakan `Set-ExecutionPolicy -Scope Process` bila diperlukan.
9. Tidak boleh mengubah system PATH jika user PATH sudah memadai.
10. Tidak boleh menulis ke folder system tanpa alasan teknis.

---

## 22. UX Terminal

### 22.1 Header

```text
============================================================
UBSI Student Development Environment Installer
Windows/macOS Setup for SI and TI Students
============================================================
```

### 22.2 Summary Sebelum Instalasi

```text
Jurusan        : Sistem Informasi
Semester       : 3
Profiles       : Core, Web, Data
Paket wajib    : 12
Paket opsional : 3
Paket manual   : 1

Perubahan yang akan dilakukan:
- Menginstal software yang belum tersedia.
- Menambahkan PATH pada scope pengguna bila diperlukan.
- Membuat Python environment di ~/.ubsi/venvs/python-basic.
- Menginstal pandas pada environment tersebut.

Lanjutkan? [Y/n]
```

### 22.3 Final Summary

```text
============================================================
INSTALLATION SUMMARY
============================================================
Installed         : 8
Already installed : 5
Failed            : 1
Manual required   : 1
Skipped           : 2

Log:
C:\Users\Student\.ubsi\logs\install-20260705-173012.log

Verification:
.\scripts\windows\verify.ps1
```

---

## 23. Documentation Requirements

### README.md

Harus mencakup:

- Deskripsi singkat.
- Warning keamanan.
- Quick start Windows.
- Quick start macOS.
- Daftar profil.
- Link troubleshooting.
- Link release.
- Disclaimer bahwa software mengikuti RPS/dosen.

### docs/windows.md

Harus mencakup:

- Cara membuka PowerShell.
- Cara menjalankan script.
- Execution policy scope process.
- Masalah WinGet.
- Masalah PATH.
- Masalah XAMPP dan PHP.

### docs/macos.md

Harus mencakup:

- Cara membuka Terminal.
- Homebrew.
- Apple Silicon dan Intel.
- Permission shell script.
- PATH Homebrew.

### docs/troubleshooting.md

Minimal mencakup:

- `winget` tidak ditemukan.
- `brew` tidak ditemukan.
- Python command tidak dikenali.
- `pip` error.
- `pandas` gagal di-import.
- PHP tidak ditemukan.
- Composer gagal.
- XAMPP conflict.
- Android Studio tidak cocok.
- Virtualization disabled.
- Docker WSL error.
- Permission denied macOS.

---

## 24. Testing Strategy

### 24.1 Static Validation

- JSON schema validation.
- PowerShell lint.
- ShellCheck.
- Markdown lint.
- Secret scanning.

### 24.2 Unit Tests

Windows menggunakan Pester untuk:

- Manifest loading.
- Dependency resolution.
- PATH deduplication.
- Profile filtering.
- Semester recommendation.
- Dry run behavior.

Bash tests untuk:

- Argument parsing.
- Profile filtering.
- Manifest parsing.
- Dry run behavior.

### 24.3 Integration Tests

- Windows runner GitHub Actions untuk command parsing dan mock package install.
- macOS runner GitHub Actions untuk Homebrew detection dan mock install.
- Tidak menginstal seluruh software berat pada CI.

### 24.4 Manual QA Matrix

Minimal diuji pada:

- Windows 10 x64.
- Windows 11 x64.
- Windows 11 ARM64 bila tersedia.
- macOS Intel.
- macOS Apple Silicon.

### 24.5 Idempotency Test

Jalankan installer dua kali.

Expected result:

- Run pertama: paket dipasang.
- Run kedua: sebagian besar status `ALREADY_INSTALLED`.
- PATH tidak memiliki duplikasi.
- Python environment tetap valid.

---

## 25. GitHub Actions

### validate.yml

- Validate JSON schema.
- Run Markdown lint.
- Validate no duplicate package keys.

### powershell-tests.yml

- Run Pester.
- Run PSScriptAnalyzer.

### bash-tests.yml

- Run ShellCheck.
- Run Bash tests.

### security.yml

- Dependency review.
- Secret scanning.
- Optional CodeQL untuk helper tools.

### release.yml

Saat tag `v*` dibuat:

1. Validate repository.
2. Build Windows ZIP.
3. Build macOS ZIP.
4. Generate SHA-256 checksums.
5. Generate release notes.
6. Upload assets ke GitHub Release.

---

## 26. Release Artifacts

```text
ubsi-setup-windows-v1.0.0.zip
ubsi-setup-macos-v1.0.0.zip
checksums.txt
release-notes.md
```

Windows ZIP hanya berisi file relevan Windows dan config bersama. macOS ZIP hanya berisi file relevan macOS dan config bersama.

---

## 27. Versioning

Gunakan Semantic Versioning:

- PATCH: perbaikan bug, package ID, dokumentasi.
- MINOR: profil baru, software baru, fitur opsional.
- MAJOR: perubahan arsitektur, format manifest, atau breaking CLI.

Contoh roadmap versi:

- `v0.1.0`: Windows prototype.
- `v0.2.0`: macOS prototype.
- `v0.3.0`: manifest dan profiles.
- `v0.4.0`: Composer dan Python environment.
- `v0.5.0`: verification dan logging.
- `v0.8.0`: testing dan release pipeline.
- `v1.0.0`: stable release.

---

## 28. Roadmap Implementasi Agent

### Phase 1 — Repository Foundation

Agent harus:

1. Membuat struktur folder.
2. Membuat README, LICENSE, CONTRIBUTING, SECURITY, dan CHANGELOG.
3. Membuat JSON schema.
4. Membuat initial package manifest.
5. Membuat profile dan semester manifest.

**Definition of Done:**

- Repository dapat divalidasi.
- Tidak ada duplicate package key.
- Semua file JSON lolos schema.

### Phase 2 — Windows Core Installer

Agent harus:

1. Membuat argument parser PowerShell.
2. Membuat OS dan architecture detection.
3. Membuat WinGet detection.
4. Membuat manifest loader.
5. Membuat package installation abstraction.
6. Membuat dry run.
7. Membuat logging.

**Definition of Done:**

- Core profile dapat diproses.
- Script dapat dijalankan ulang.
- Dry run tidak mengubah sistem.

### Phase 3 — macOS Core Installer

Agent harus:

1. Membuat Bash argument parser.
2. Mendeteksi Intel/Apple Silicon.
3. Mendeteksi Homebrew.
4. Membuat manifest loader.
5. Membuat package installation abstraction.
6. Membuat dry run.
7. Membuat logging.

### Phase 4 — Composer and Python

Agent harus:

1. Membuat Composer module Windows.
2. Memverifikasi Composer signature.
3. Membuat Composer module macOS.
4. Membuat Python virtual environment module.
5. Menginstal `pandas`.
6. Membuat verification command.

### Phase 5 — Profiles and Heavy Software

Agent harus:

1. Menambahkan SI, TI, Web, Data, Mobile, Networking.
2. Menandai heavy package.
3. Menambahkan system requirement checks.
4. Menambahkan manual package guidance.

### Phase 6 — Diagnostics and Repair

Agent harus:

1. Membuat diagnostics script.
2. Membuat repair PATH.
3. Membuat repair Python environment.
4. Membuat Composer repair.
5. Membuat report.

### Phase 7 — Tests and CI

Agent harus:

1. Menambahkan unit test.
2. Menambahkan static analysis.
3. Menambahkan schema validation.
4. Menambahkan release workflow.

### Phase 8 — Documentation and Stable Release

Agent harus:

1. Melengkapi dokumentasi.
2. Menambahkan troubleshooting.
3. Menambahkan manual QA checklist.
4. Menghasilkan v1.0.0 release candidate.

---

## 29. Agent Implementation Rules

Agent coding harus mengikuti aturan berikut:

1. Jangan menulis seluruh logic dalam satu file.
2. Jangan meng-hardcode package ID di lebih dari satu tempat.
3. Jangan menggunakan installer dari mirror tidak resmi.
4. Jangan menjalankan remote script menggunakan `iex` atau `curl | bash` sebagai flow utama.
5. Jangan mengubah execution policy secara permanen.
6. Jangan memasang library Python ke global environment secara default.
7. Jangan menambahkan package tanpa verification strategy.
8. Jangan menganggap software tersedia hanya karena foldernya ada.
9. Jangan menghapus software existing.
10. Jangan mengubah service, firewall, antivirus, atau BIOS.
11. Semua function publik harus memiliki komentar atau documentation block.
12. Semua perubahan manifest harus disertai test.
13. Semua error harus menghasilkan message yang dapat ditindaklanjuti.
14. Semua command harus mendukung path yang mengandung spasi.
15. Semua output status harus konsisten.
16. Script harus tetap berjalan bila package opsional gagal.
17. Script harus berhenti bila verifikasi keamanan gagal.
18. Jangan menganggap akses administrator selalu tersedia.
19. Prioritaskan user-scope installation.
20. Semua file text menggunakan UTF-8.

---

## 30. Acceptance Criteria Produk v1.0

Produk dinyatakan siap rilis jika:

1. Windows installer dapat dijalankan pada Windows 10/11 yang didukung.
2. macOS installer dapat dijalankan pada Intel dan Apple Silicon yang didukung.
3. Core profile dapat dipasang atau dideteksi.
4. Composer dapat dipasang dan diverifikasi.
5. Python virtual environment dapat dibuat.
6. `pandas` dapat di-import.
7. Installer dapat dijalankan ulang tanpa duplikasi PATH.
8. Dry run tidak mengubah perangkat.
9. Log dan summary dihasilkan.
10. Manual package ditangani dengan status yang benar.
11. Semua JSON lolos schema validation.
12. PowerShell dan Bash lint lolos.
13. Unit test utama lolos.
14. Release ZIP dan checksum berhasil dibuat.
15. README dan troubleshooting tersedia.
16. Tidak ada credential atau binary ilegal dalam repository.
17. Tidak ada critical security issue yang diketahui.

---

## 31. Success Metrics

Setelah digunakan pada kelompok uji mahasiswa:

- Minimal 80% pengguna berhasil memasang Core profile tanpa bantuan langsung.
- Minimal 90% pengguna dapat menjalankan verification script.
- Minimal 90% instalasi `pandas` berhasil pada perangkat yang memenuhi syarat.
- Minimal 90% instalasi Composer berhasil bila PHP tersedia.
- Waktu bantuan instalasi dari asisten berkurang dibanding proses manual.
- Mayoritas issue GitHub menyertakan log yang valid.

---

## 32. Risk Register

### Risiko: Package ID berubah

Mitigasi:

- Package ID berada di manifest.
- Tambahkan scheduled validation workflow.
- Sediakan fallback ID.

### Risiko: Versi software tidak sesuai materi dosen

Mitigasi:

- `versions.json` dapat mengunci versi.
- Dokumentasikan sumber keputusan versi.

### Risiko: Laptop tidak memenuhi spesifikasi

Mitigasi:

- Preflight checks.
- Heavy package warning.
- Opsi skip.

### Risiko: Konflik PHP/XAMPP

Mitigasi:

- Deteksi lebih dari satu PHP.
- Tampilkan path yang aktif.
- Composer menggunakan PHP yang dipilih secara eksplisit.

### Risiko: Python environment rusak

Mitigasi:

- Repair mode.
- Recreate venv dengan konfirmasi.
- Simpan requirements terpisah.

### Risiko: Antivirus memblokir script

Mitigasi:

- Release checksum.
- Tidak menggunakan obfuscation.
- Dokumentasi keamanan.

### Risiko: Pengguna menjalankan command sebagai administrator tanpa perlu

Mitigasi:

- Default user scope.
- Escalation hanya per langkah yang membutuhkan.

---

## 33. Open Questions

Pertanyaan yang harus diputuskan sebelum stable release:

1. Apakah stack PHP default menggunakan XAMPP atau PHP standalone?
2. Apakah MySQL Server wajib atau cukup melalui XAMPP/MariaDB?
3. Versi JDK default yang digunakan dosen.
4. Apakah Android Studio masuk profile semester tertentu atau hanya opsional.
5. Apakah Docker Desktop diperlukan oleh seluruh mahasiswa TI.
6. Apakah Laravel installer global perlu dipasang atau cukup Composer.
7. Apakah JupyterLab masuk Python basic atau Data Science saja.
8. Apakah repository bersifat resmi kampus atau komunitas mahasiswa.
9. Siapa maintainer yang menyetujui perubahan versi software.
10. Apakah perlu dukungan Ubuntu pada versi berikutnya.

Agent tidak boleh menebak keputusan akademik. Jika belum ada keputusan, gunakan konfigurasi opsional dan dokumentasikan asumsi.

---

## 34. Initial Package List

### Core

- Git
- Visual Studio Code
- Python
- Java JDK
- Node.js LTS
- Postman
- Browser
- Archive utility

### SI/Web

- XAMPP atau PHP
- Composer
- MySQL Workbench
- Laravel installer opsional

### Python Basic

- pandas

### Data Science

- numpy
- pandas
- matplotlib
- scikit-learn
- jupyterlab
- openpyxl
- requests

### TI/Networking

- Wireshark
- VirtualBox
- Packet Tracer manual
- Docker Desktop opsional

### Mobile

- Android Studio
- JDK

---

## 35. Command Interface Specification

### Windows

```powershell
.\scripts\windows\setup.ps1 [options]
```

Options:

```text
-Jurusan SI|TI
-Semester 1..8
-Profiles Core,Web,Data
-IncludeOptional
-SkipHeavy
-DryRun
-NonInteractive
-ForceRetry
-LogPath <path>
-ConfigPath <path>
```

### macOS

```bash
./scripts/macos/setup.sh [options]
```

Options:

```text
--jurusan SI|TI
--semester 1..8
--profiles core,web,data
--include-optional
--skip-heavy
--dry-run
--non-interactive
--force-retry
--log-path <path>
--config-path <path>
```

Argument yang tidak dikenal harus menghasilkan exit code `2` dan menampilkan help.

---

## 36. Example Definition of Done per Feature

### Feature: pandas Installation

Selesai apabila:

- Python ditemukan.
- Venv dibuat.
- pip diperbarui.
- pandas dipasang dari requirements.
- `import pandas` berhasil.
- Versi ditampilkan.
- Log tersedia.
- Dapat dijalankan ulang tanpa reinstall yang merusak.
- Unit test argument dan path lolos.

### Feature: Composer Installation

Selesai apabila:

- PHP ditemukan.
- Installer berasal dari domain resmi.
- Signature diverifikasi pada Windows.
- Composer tersedia pada PATH user.
- `composer --version` berhasil.
- `composer diagnose` dapat dijalankan.
- Dapat dijalankan ulang.
- Tidak ada perubahan PATH duplikat.

---

## 37. Future Enhancements

Setelah v1.0:

- Dukungan Ubuntu.
- GUI sederhana.
- Web-based package profile generator.
- Self-update checker.
- Offline installation bundle untuk lab kampus.
- Proxy support untuk jaringan kampus.
- Per-course manifest.
- Dosen dapat membagikan profile code.
- Export machine report.
- Signed releases.
- Optional anonymous failure telemetry dengan opt-in eksplisit.

---

## 38. Final Instruction for Coding Agent

Mulai implementasi dari fondasi repository dan manifest, bukan langsung dari script instalasi besar. Setiap fase harus menghasilkan code yang dapat dijalankan, diuji, dan direview. Jangan mengimplementasikan seluruh fitur dalam satu commit. Gunakan perubahan kecil dan terukur.

Urutan kerja wajib:

1. Buat struktur repository.
2. Buat schema dan manifest.
3. Buat loader dan dependency resolver.
4. Buat dry run.
5. Buat installer Core Windows.
6. Buat installer Core macOS.
7. Tambahkan Composer.
8. Tambahkan Python venv dan pandas.
9. Tambahkan verification.
10. Tambahkan logging dan report.
11. Tambahkan profiles lanjutan.
12. Tambahkan tests dan CI.
13. Lengkapi dokumentasi.
14. Build release candidate.

Setelah setiap fase, agent harus:

- Menjelaskan file yang dibuat atau diubah.
- Menjalankan test yang relevan.
- Menyebutkan keterbatasan yang masih ada.
- Tidak mengklaim berhasil jika test belum dijalankan.
- Tidak menghapus keputusan arsitektur dari PRD tanpa alasan yang didokumentasikan.

---

## 39. Product Owner Approval Checklist

Sebelum agent melanjutkan ke implementasi penuh, product owner perlu menyetujui:

- [ ] Nama repository.
- [ ] Status resmi atau komunitas.
- [ ] Daftar software SI.
- [ ] Daftar software TI.
- [ ] Versi PHP default.
- [ ] Versi Python default.
- [ ] Versi JDK default.
- [ ] XAMPP atau PHP standalone.
- [ ] MySQL atau MariaDB default.
- [ ] Software heavy yang masuk default.
- [ ] Lisensi repository.
- [ ] Maintainer dan reviewer.

---

**End of PRD**
