# Contributing

Terima kasih sudah ingin membantu Tech Starter UBSI.

## Prinsip

- Gunakan sumber resmi atau package manager resmi.
- Jangan menambahkan software bajakan, crack, keygen, atau mirror tidak resmi.
- Jangan menjadikan software berat sebagai default tanpa persetujuan maintainer.
- Jangan menebak keputusan akademik seperti versi PHP, MySQL/MariaDB, Docker, atau Android Studio.
- Jaga bahasa dokumentasi tetap ramah untuk mahasiswa pemula.

## Mengubah Manifest

Semua package didefinisikan di `config/packages.json`. Profil berada di `config/profiles.json`, dan rekomendasi semester berada di `config/semesters.json`.

Sebelum membuat pull request, jalankan:

```bash
python tools/validate-manifest.py
```

Validator harus sukses sebelum perubahan dikirim.

## Menambahkan Package

Package baru harus memiliki:

- `key` unik dengan huruf kecil, angka, dan tanda hubung.
- Nama dan deskripsi yang jelas.
- Minimal satu profile.
- Status wajib atau opsional yang masuk akal.
- Rencana verification command yang aman dan read-only.
- Catatan manual jika package tidak boleh diunduh otomatis.

## Pull Request

Pull request sebaiknya kecil dan fokus. Jelaskan:

- Masalah yang diselesaikan.
- File manifest atau dokumentasi yang berubah.
- Hasil `python tools/validate-manifest.py`.

