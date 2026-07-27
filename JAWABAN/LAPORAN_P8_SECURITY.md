# LAPORAN TUGAS: Project 8. Enhancing IoT Security of IoT Web Applications

* **Nama Mahasiswa**: Muhammad Ketsar Ali Abi Wahid
* **NIM**: 230401070204
* **Mata Kuliah**: Internet of Things (IoT)
* **Dosen**: Prof. Jong-Dae Park
* **Institusi**: Universitas Siber Asia (UNSIA)

---

## A. Analisis Folder & Solusi Masalah

Folder **`JAWABAN`** telah dikonfigurasi agar fleksibel dan dapat berjalan di dua *environment* berbeda:

1. **Localhost (Development)**: Aplikasi berjalan di root URL (`/`).
2. **Server Remote (Production)**: Aplikasi berjalan di balik sub-path (`/django/`) yang dikonfigurasi melalui `FORCE_SCRIPT_NAME` pada `settings.py` untuk menyesuaikan dengan *reverse proxy* server.

### Fitur Keamanan & UX:
* **Autentikasi & Redirect Dinamis**: Menggunakan `django.contrib.auth`. Jika pengguna mengakses halaman terproteksi tanpa login, Django akan mengarahkan ke halaman login dengan menyertakan parameter `?next=...`. Setelah login berhasil, Django secara otomatis mengembalikan pengguna ke halaman yang dituju sebelumnya.
* **Solusi Bug & Fallback**: Implementasi `logout_view` untuk mendukung navigasi GET dan pengaman JavaScript (`{% if latest %}`) pada visualisasi gauge.

---

## B. Jawaban Tugas (Task 1)

### Task 1: Mengaktifkan Fitur Login dan Membatasi Akses View

Untuk mengamankan aplikasi, kami menerapkan:
1. **Decorator `@login_required`**: Membatasi akses view (`device_data_view` dan `sensor_gauge_view`).
2. **Mekanisme Redirect**: Saat akses ditolak karena belum login, Django menambahkan parameter `?next=/...` pada URL login. Fitur ini memastikan user diarahkan kembali ke URL asal setelah login berhasil, baik di localhost maupun di server remote (`/django/...`).
3. **Pengecualian API**: Endpoint POST API sensor tidak diproteksi session login agar ESP8266 tetap bisa mengirim data melalui *API Key Validation*.

---

## C. Detail Modifikasi File

### 1. File `settings.py` (Konfigurasi Fleksibel)
Kami mendeteksi `DEBUG` untuk menentukan apakah aplikasi berjalan di localhost atau server remote.

```python
# settings.py
if not DEBUG:
    # Konfigurasi untuk Server Remote
    FORCE_SCRIPT_NAME = '/django'
    LOGIN_URL = '/django/login/'
    LOGIN_REDIRECT_URL = '/django/device/device01/gauge/'
    LOGOUT_REDIRECT_URL = '/django/login/'
else:
    # Konfigurasi untuk Localhost
    LOGIN_URL = '/login/'
    LOGIN_REDIRECT_URL = '/device/device01/'
    LOGOUT_REDIRECT_URL = '/login/'
```

---

## D. Cara Menjalankan Project

### 1. Di Localhost (Komputer Sendiri)
1. Aktifkan venv dan jalankan: `python manage.py runserver`.
2. Akses: `http://127.0.0.1:8000/`.
3. Anda akan diarahkan ke login `/login/`.

### 2. Di Server Remote
1. Aplikasi diakses melalui: `https://m70204.belajarhub.id/django/...`.
2. Jika belum login, URL akan menjadi `.../django/login/?next=/django/device/device01/gauge/...`.
3. **Login**: Masukkan kredensial:
   * **Username**: `m70204`
   * **Password**: `m70204*01`
4. Setelah sukses, Django akan menggunakan parameter `next` untuk mengarahkan kembali ke halaman target (misal: Gauge).


