# Tech Starter UBSI

Tech Starter UBSI adalah one-command starter untuk membantu mahasiswa UBSI menyiapkan software dasar perkuliahan secara aman, konsisten, dan mudah diverifikasi.

Status saat ini: **Windows Core MVP**. Installer awal sudah tersedia untuk Windows melalui WinGet. macOS, Composer, Python virtual environment, dan profil lanjutan masih dalam roadmap.

## Install (one command)

### Windows (PowerShell)

Buka **PowerShell**, lalu jalankan:

```powershell
irm https://raw.githubusercontent.com/ruhulikram/techstarter-ubsi/main/install.ps1 | iex
```

Command ini akan:

- Mengambil manifest paket Core dari repository ini.
- Mengecek paket yang sudah terpasang.
- Menginstal paket Core yang belum tersedia melalui `winget`.
- Menampilkan summary sukses, gagal, dan dilewati.

Paket Core saat ini:

- Git
- Visual Studio Code
- Python
- Java JDK
- Node.js LTS
- Postman
- Google Chrome
- 7-Zip

Setelah instalasi selesai, tutup terminal lalu buka terminal baru agar `PATH` terbaru terbaca.

### Dry Run

Untuk melihat paket yang akan diproses tanpa menginstal:

```powershell
iwr https://raw.githubusercontent.com/ruhulikram/techstarter-ubsi/main/install.ps1 -OutFile install.ps1
.\install.ps1 -DryRun
```

### Validasi Manifest

Clone repository ini, lalu jalankan validasi manifest:

```bash
python tools/validate-manifest.py
```

Jika Python belum tersedia di perangkat, pasang Python terlebih dahulu dari sumber resmi atau gunakan environment yang sudah disediakan oleh kelas/lab.

## Install Python di Windows

Untuk Windows 10/11, cara paling mudah adalah menggunakan `winget` dari Command Prompt atau PowerShell.

1. Buka **Command Prompt** atau **PowerShell**.
2. Jalankan salah satu command berikut:

```powershell
winget install Python.Python.3.13
```

Jika versi tersebut belum tersedia di perangkat, gunakan:

```powershell
winget install Python.Python.3.12
```

3. Tutup terminal, lalu buka lagi.
4. Cek instalasi Python:

```powershell
python --version
pip --version
```

Jika `python` belum dikenali, coba:

```powershell
py -3 --version
```

Setelah Python berhasil terpasang, jalankan kembali:

```bash
python tools/validate-manifest.py
```

Catatan: command ini hanya memasang Python. Untuk memasang semua paket Core, gunakan one-command installer di atas.

## Isi Repository

- Manifest paket di `config/packages.json`
- Definisi profil di `config/profiles.json`
- Rekomendasi semester di `config/semesters.json`
- JSON schema di `config/schema/`
- Validator lokal di `tools/validate-manifest.py`
- GitHub Actions di `.github/workflows/validate.yml`
- One-command installer Windows di `install.ps1`

## Safe Common Core

Installer awal hanya memproses paket dasar bersama:

- Git
- Visual Studio Code
- Python
- Java JDK
- Node.js LTS
- Postman
- Google Chrome
- 7-Zip

Profil lanjutan seperti SI, TI, Web, Data, Mobile, Networking, Database, dan Full sudah disiapkan sebagai placeholder terencana. Paket berat dan paket yang membutuhkan keputusan akademik belum dimasukkan sebagai default.

## Peringatan Keamanan

- Jika ingin mengecek script sebelum menjalankan one-command installer, buka `install.ps1` terlebih dahulu.
- Repository ini tidak menyediakan software bajakan, crack, keygen, atau mirror tidak resmi.
- Installer menggunakan `winget` dan package ID dari manifest.
- Jangan jalankan installer dari fork yang tidak kamu percaya.

## Roadmap Singkat

1. Windows Core one-command installer berbasis PowerShell dan WinGet.
2. macOS one-command installer berbasis Bash dan Homebrew.
3. Instalasi Python virtual environment dan Composer.
4. Verification, logging, report, troubleshooting, dan release ZIP.
5. Profil lanjutan SI, TI, Web, Data, Mobile, Networking, dan Database.

Detail produk lengkap tersedia di `PRD.md`.

## Kontribusi

Lihat `CONTRIBUTING.md` sebelum mengubah manifest atau menambahkan paket baru. Semua perubahan package/profile/semester harus lolos:

```bash
python tools/validate-manifest.py
```
