# Security Policy

## Supported Versions

Saat ini hanya Foundation MVP yang didukung. Installer otomatis belum tersedia.

| Version | Supported |
| --- | --- |
| 0.1.x | Yes |

## Reporting a Vulnerability

Jika menemukan risiko keamanan, buat issue dengan informasi minimum berikut:

- File atau bagian yang bermasalah.
- Dampak yang mungkin terjadi.
- Langkah reproduksi jika ada.
- Saran perbaikan jika tersedia.

Jangan memasukkan token, password, API key, atau credential lain ke issue publik.

## Security Rules

- Tidak menjalankan remote script langsung melalui `Invoke-Expression` atau `curl | bash`.
- Tidak menggunakan installer dari mirror tidak resmi.
- Tidak menyimpan credential.
- Tidak mengubah antivirus, firewall, service, BIOS, atau system policy.
- Tidak mengubah execution policy secara permanen.

