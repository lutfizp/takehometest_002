# 🔐 Challenge 1: Custom Feistel & LFSR Decryptor

Repositori ini berisi implementasi *pure-Python* (tanpa *library* kriptografi pihak ketiga) untuk mendekripsi ciphertext yang dienkripsi menggunakan kombinasi **64-bit Feistel Network** dan **Linear-Feedback Shift Register (LFSR)**.

Solusi ini ditulis dengan fokus pada keterbacaan (*human-friendly*), modularitas, dan pemahaman konsep fundamental kriptografi.

## 🛠 Persyaratan Sistem

- **Python 3.10+** (Memanfaatkan fitur *Type Hints* modern).
- **Standard Library Saja**: Tidak memerlukan `pycryptodome` atau *library* eksternal lainnya. Semua operasi bitwise dan *byte manipulation* diimplementasikan secara mandiri.

## 🧠 Analisis & Struktur Algoritma

Algoritma ini menggunakan arsitektur *Feistel cipher* klasik dengan blok 64-bit yang dibagi menjadi dua bagian 32-bit (Kiri dan Kanan), dijalankan sebanyak 8 ronde per blok. Kunci setiap ronde di-generate secara dinamis oleh 32-bit LFSR.

Berikut adalah pemecahan komponen utama dalam implementasi (`decrypt.py`):

1. **Bitwise Operations**
   - `rotate_left_32`: Melakukan *circular left shift* 32-bit secara aman dengan memastikan *masking* 32-bit terjaga.
   - `advance_lfsr`: Menggeser *state* LFSR dan menghitung *feedback bit* berdasarkan tap khusus (bit 31, 30, 29, dan 9).
2. **Core Cipher Logic**
   - `feistel_round_function`: Fungsi `F` yang menggabungkan operasi Rotasi, XOR dengan *round key*, dan XOR dengan *round constant*.
   - `generate_block_round_keys`: Men-generate 8 kunci ronde (*round keys*) untuk satu blok. **Penting:** State LFSR diteruskan terus-menerus antar blok (*continuous state*), tidak di-reset per blok.
3. **Decryption Process**
   - `decrypt_block`: Mengembalikan blok 64-bit ke bentuk aslinya dengan mengeksekusi operasi Feistel secara terbalik (*reversed round keys*).
   - `decrypt_ciphertext`: Orkestrator utama yang membaca blok per blok, menjaga kelangsungan *state* LFSR, dan menggabungkan blok yang terdekripsi.
   - `remove_pkcs7_padding`: Memvalidasi integritas data dan membuang padding PKCS#7 yang ditambahkan saat enkripsi.

## 🚀 Cara Menjalankan (Penggunaan)

Script ini dapat dijalankan langsung dari *root directory* repositori.

### Penggunaan Default
Secara bawaan, script akan otomatis mencari file `cipher.enc` sesuai dengan struktur direktori tantangan.

```powershell
python .\submission\challenge-1\decrypt.py