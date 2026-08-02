# Laporan Audit & Refactoring - Challenge 2

## 📝 Ringkasan (Executive Summary)
Halo! Ini adalah laporan audit dan refactoring saya untuk Challenge 2. 

Kode prosesor telemetri bawaan (legacy) sebenarnya sudah menghasilkan output yang benar, tetapi performanya sangat lambat karena melakukan *scanning* seluruh data secara berulang kali, menyalin *list* secara terus-menerus, dan sangat bergantung pada *mutable global state*. 

Pendekatan *refactoring* saya mempertahankan *output* akhir agar tetap sama persis, sambil mengganti beban kerja yang tadinya kuadratik `O(N²)` menjadi lintasan linear `O(N)` dengan objek hasil yang eksplisit. Berdasarkan *benchmark* akhir, kode baru ini menghasilkan **521.26x speedup** (berkurang dari `9.486s` menjadi `0.018s`), yang mana sukses melampaui target `>100x`.

---

## ✅ Verifikasi Kesamaan Output (Preserved Behavior)
Pengecekan ekuivalensi (kesamaan) memvalidasi seluruh hasil *pipeline*, bukan hanya yang tampil di *console*:
- Seluruh 10.000 *record* telemetri deterministik berhasil di-*generate*.
- Format laporan teks identik sama persis, termasuk urutan dan baris baru (*newline*).
- Laporan teks memiliki panjang tepat 152.172 karakter.
- Total *record* yang diproses tetap 10.000.
- Nilai rata-rata tetap 7.499,25.
- Transformasi nilai dan jumlah status aktif per perangkat yang digunakan tetap sama.

---

## 🔍 Temuan Audit Legacy & Solusi Refactoring

### 1. Perulangan Kuadratik (Quadratic per-record scanning)
* **Dampak:** Untuk setiap *record*, `do_processing` memindai ulang seluruh data untuk menghitung status aktif (menghasilkan ~100.000.000 komparasi). Kompleksitas waktu menjadi `O(N²)` alih-alih `O(N)`. Proses *lookup dictionary* yang berulang juga menambah beban *interpreter*.
* **Refactoring:** Saya menghitung status aktif cukup *satu kali saja* menggunakan `collections.Counter`, lalu menggunakan ulang nilai tersebut saat pembuatan laporan.

### 2. Realokasi List Berulang (Repeated list reallocation)
* **Dampak:** Perintah `g_cache = g_cache + [current_record["value"]]` menyalin seluruh elemen *list* di setiap iterasi. Ini menciptakan kerja *copying* `O(N²)` dan membebani *garbage-collector* memori, padahal datanya hanya dipakai untuk mencari total rata-rata.
* **Refactoring:** Saya menghapus *cache* tersebut sepenuhnya dan mengakumulasi nilai `total_value` serta `total_count` secara langsung (*scalar accumulation*).

### 3. Penggabungan String Berulang (Repeated immutable string concatenation)
* **Dampak:** Laporan diperpanjang dengan `g_results_str += ...`. Karena tipe *string* bersifat *immutable*, ini memaksa Python mengalokasikan memori baru secara berulang seiring bertambah besarnya teks laporan.
* **Refactoring:** Saya menyimpan setiap baris ke dalam `list`, lalu menggabungkannya tepat satu kali menggunakan `"".join()` di akhir proses.

### 4. Mutable Global State
* **Dampak:** Data bergantung pada variabel global (`g_records`, `g_results_str`, `g_cache`). Akibatnya, fungsi tidak bisa diuji secara mandiri (*testable*), rawan menyisakan data lama jika dieksekusi berulang, dan berbahaya jika dijalankan secara bersamaan (*concurrent*).
* **Refactoring:** Fungsi kini saling mengoper parameter secara eksplisit dan mengembalikan data dalam bentuk *dataclass* `stats` yang *immutable*.

### 5. Kontrak Data yang Lemah (Weak data contracts)
* **Dampak:** Penggunaan tipe *dictionary* bergantung pada kunci teks (*string keys*) yang rawan salah ketik (*typo*) dan tipe datanya tidak bisa divalidasi hingga *runtime* terjadi.
* **Refactoring:** Saya merepresentasikan data menggunakan `@dataclass(frozen=True, slots=True)` tipe eksplisit (`TelemetryRecord`). Status dan angka pengali juga dijadikan variabel konstanta.

### 6. Tahapan Pipeline yang Saling Terikat (Coupled pipeline stages)
* **Dampak:** Proses pembuatan data, pemrosesan, dan kalkulasi waktu digabung secara kaku melalui *global variable*.
* **Refactoring:** Saya memisahkan fungsi `load_raw_data`, `count_active_records`, `process_records`, dan `run_pipeline`. Fungsi `main` kini dikhususkan untuk pencatatan waktu dan presentasi di layar.

### 7. Penggunaan Timer yang Kurang Tepat
* **Dampak:** Skrip bawaan menggunakan `time.time`, yang merupakan *wall-clock* dan bisa terpengaruh oleh penyesuaian jam sistem komputer.
* **Refactoring:** Saya menggunakan `time.perf_counter` untuk perhitungan durasi (*elapsed time*) yang jauh lebih presisi dan stabil.

### 8. Kurangnya Validasi Batas Error
* **Dampak:** Fungsi bawaan berasumsi bahwa input angka dimensi data selalu valid (positif).
* **Refactoring:** Saya menambahkan validasi nilai untuk memastikan `record_count` dan `device_count` tidak bernilai negatif sebelum data di-*generate*.

---

## 📊 Perbandingan Kompleksitas (Complexity Comparison)

| Operasi | Legacy (Bawaan) | Refactored (Baru) |
| :--- | ---: | ---: |
| **Kalkulasi status aktif** | `O(N²)` | `O(N)` |
| **Akumulasi nilai** | `O(N²)` *(list copying)* | `O(N)` *(scalar accumulation)* |
| **Pembuatan laporan** | Pertumbuhan string berulang | `O(N)` *(list dan 1 kali join)* |
| **Total Pemrosesan** | **`O(N²)`** | **`O(N)`** |
| **Mutable global variables** | 3 Variabel | 0 Variabel |

---

## ⚙️ Metodologi Benchmark

Benchmark diimplementasikan pada `benchmark.py` menggunakan `time.perf_counter`. Kedua pengujian mengeksekusi siklus *load-process-summary* secara penuh pada mesin dan *interpreter* Python yang sama.

Sebelum setiap iterasi *legacy* berjalan, *global variable*-nya di-reset agar proses dimulai dalam keadaan bersih. Skrip *benchmark* ini akan memvalidasi kesamaan laporan teks, total data, dan rata-rata. Jika ada ketidakcocokan sedikit saja, program akan gagal secara paksa (*assertion failure*).

**Konfigurasi Final:**
- Eksekusi Legacy: 3 kali
- Eksekusi Refactored: 20 kali
- Statistik yang dilaporkan: Median
- Python: 3.13.0
- Platform: Windows 11
- Input records: 10.000

---

## ⏱️ Hasil Benchmark Akhir

| Metrik | Hasil |
| :--- | ---: |
| Legacy median | 9,486019 detik |
| Legacy minimum | 8,383305 detik |
| Refactored median | 0,018198 detik |
| Refactored minimum | 0,016818 detik |
| **Median Speedup** | **521,26x** |
| Target yang diminta | >100x |
| **Status Target** | **LULUS (PASS)** |
| **Kesamaan Output** | **LULUS (PASS)** |

*Waktu mentah tersimpan di `benchmark_results.txt`. Bukti tangkapan layar yang di-*generate* dari output benchmark yang sama tersimpan di `benchmark_proof.png`.*

---

## 🚀 Instruksi Eksekusi

Jalankan *pipeline* yang telah di-refactor langsung dari *root directory* repositori:
```powershell
python submission/challenge-2/refactored_processor.py
```

Untuk menjalankan verifikasi ekuivalensi (kesamaan) dan benchmark secara utuh:

```powershell
python submission/challenge-2/benchmark.py
```

Catatan: Perintah benchmark di atas akan otomatis menimpa (overwrite) file `benchmark_results.txt` dengan hasil pengukuran dari mesin yang sedang menjalankannya. Karena rasio runtime sangat bergantung pada spesifikasi perangkat keras (machine-dependent), file bukti benchmark_proof.png sengaja disertakan untuk merekam environment dan timestamp asli pada saat submisi ini dibuat.
