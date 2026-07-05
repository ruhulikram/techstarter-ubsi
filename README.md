# Tech Starter UBSI

Tech Starter UBSI adalah fondasi awal untuk repository setup lingkungan pengembangan mahasiswa UBSI. Tujuan jangka panjangnya adalah membantu mahasiswa Sistem Informasi dan Teknologi Informasi menyiapkan software kuliah secara aman, konsisten, dan mudah diverifikasi.

Status saat ini: **Foundation MVP**. Repository ini belum memiliki installer Windows atau macOS. Fase pertama hanya menyediakan dokumentasi, manifest paket, schema, validator, dan CI dasar.

## Quick Start

Clone repository ini, lalu jalankan validasi manifest:

```bash
python tools/validate-manifest.py
```

Jika Python belum tersedia di perangkat, pasang Python terlebih dahulu dari sumber resmi atau gunakan environment yang sudah disediakan oleh kelas/lab.

## Isi MVP

- Manifest paket di `config/packages.json`
- Definisi profil di `config/profiles.json`
- Rekomendasi semester di `config/semesters.json`
- JSON schema di `config/schema/`
- Validator lokal di `tools/validate-manifest.py`
- GitHub Actions di `.github/workflows/validate.yml`

## Safe Common Core

MVP ini hanya mendefinisikan paket dasar bersama:

- Git
- Visual Studio Code
- Python
- Java JDK
- Node.js LTS
- Postman
- Browser modern
- Archive utility

Profil lanjutan seperti SI, TI, Web, Data, Mobile, Networking, Database, dan Full sudah disiapkan sebagai placeholder terencana. Paket berat dan paket yang membutuhkan keputusan akademik belum dimasukkan sebagai default.

## Peringatan Keamanan

- Jangan menjalankan script instalasi dari internet tanpa membaca sumbernya.
- Repository ini tidak menyediakan software bajakan, crack, keygen, atau mirror tidak resmi.
- Installer otomatis belum tersedia pada MVP ini.
- Package ID di manifest adalah metadata awal dan harus divalidasi lagi saat fase installer dibuat.

## Roadmap Singkat

1. Foundation repository, manifest, schema, validator, dan CI.
2. Windows dry run installer berbasis PowerShell.
3. macOS dry run installer berbasis Bash.
4. Instalasi Python virtual environment dan Composer.
5. Verification, logging, report, troubleshooting, dan release ZIP.

Detail produk lengkap tersedia di `PRD.md`.

## Kontribusi

Lihat `CONTRIBUTING.md` sebelum mengubah manifest atau menambahkan paket baru. Semua perubahan package/profile/semester harus lolos:

```bash
python tools/validate-manifest.py
```

