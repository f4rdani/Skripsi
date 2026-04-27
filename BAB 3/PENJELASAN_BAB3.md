# Penjelasan BAB III — METODOLOGI PENELITIAN

Catatan ini menjelaskan struktur dan rasional tiap sub-bab BAB III sesuai panduan **Handout Skripsi Prodi Teknologi Informasi BSI** (halaman 13–14) dan adaptasinya untuk topik skripsi.

## Tujuan umum BAB III
BAB III adalah **resep eksperimen**. Pembaca yang ingin mereplikasi penelitian ini harus dapat melakukannya hanya dengan membaca BAB III. Tiga pertanyaan yang harus terjawab:
1. **Tahapan apa** yang dilewati peneliti dari awal hingga selesai?
2. **Alat apa** yang dipakai (hardware/software/dataset)?
3. **Bagaimana data dikumpulkan dan diolah** menjadi kesimpulan?

## 3.1 Tahapan Penelitian
**Fungsi:** Memberikan timeline / flow tahapan penelitian secara berurutan. Setiap tahap menghasilkan **artefak** (output) yang menjadi input tahap berikutnya. Disertai diagram alur (Gambar 3.1).

**Standar BSI:** "Menjelaskan tahapan-tahapan yang dilakukan dalam melakukan penelitian ini."

**Catatan untuk topik ini:** Delapan tahap yang dipakai mengikuti pola standar penelitian eksperimen ML systems—mulai dari studi pustaka, perencanaan GQM, persiapan model, pengukuran statik & dinamik, pengukuran kualitas, analisis, hingga pelaporan & validasi.

## 3.2 Instrumen Penelitian
**Fungsi:** Mendaftar alat bantu yang dipakai oleh peneliti agar pengumpulan data menjadi sistematis dan reproducible. Lazimnya dikelompokkan menjadi:
- **3.2.1 Hardware** — perangkat yang dipakai eksperimen.
- **3.2.2 Software** — toolchain, compiler, library, manajemen referensi.
- **3.2.3 Model dan Dataset** — bobot model dan dataset evaluasi.

**Standar BSI:** "Menjelaskan alat bantu yang dipilih dan digunakan oleh peneliti dalam kegiatannya mengumpulkan data agar kegiatan tersebut menjadi sistematis dan dipermudah."

**Pentingnya tabel:** Setiap kategori instrumen disajikan sebagai tabel (Tabel 3.1, 3.2, 3.3) supaya pembaca yang ingin mereplikasi tahu persis versi dan konfigurasi yang dipakai.

## 3.3 Metode Pengumpulan Data
**Fungsi:** Menjelaskan **bagaimana** data dikumpulkan dan **berapa** banyak. Pada skripsi rekayasa, populasi dan sampel sering diabstraksi sebagai kombinasi kondisi eksperimen (model × varian × benchmark × ulangan).

**Standar BSI:** "Menjelaskan tentang metode pengumpulan data yang real dilakukan antara lain berupa Pengamatan langsung, wawancara, studi Pustaka atau lainnya."

**Sub-bab yang dipakai:**
- **(a) Observasi** — terotomasi via System Benchmarking Logging (htop, /proc/meminfo, stdout llama.cpp, evaluator regex/exact-match).
- **(b) Wawancara** — terstruktur opsional terhadap dosen pembimbing teknis sebagai validator metodologi.
- **(c) Studi Pustaka** — review 12 jurnal lima tahun terakhir, manajemen referensi via Mendeley APA edisi ke-7.

Pada paragraf akhir 3.3, populasi dan sampel diabstraksi sebagai kombinasi kondisi eksperimen (model × varian × benchmark × ulangan) dengan justifikasi ukuran sampel statistik (Cohen's d). Sub-bab tidak diberi nomor 3.3.1/3.3.2 karena panduan BSI hanya menyebut 3.3 sebagai satu sub-bab tunggal.

**Catatan:** Wawancara pada penelitian rekayasa biasanya bukan sumber data primer — peneliti wajib jelas kapan wawancara digunakan dan kapan tidak.

## 3.4 Metode Analisis Data
**Fungsi:** Menjelaskan **bagaimana** data mentah diolah menjadi informasi/temuan. Untuk topik PTQ on-device, lima sub-poin standar internasional yang dipakai:

- **3.4.1 GQM Matrix** — pemetaan Goal → Question → Metric (Tabel 3.4 + Gambar 3.3).
- **3.4.2 Three-Dimensional Evaluation Framework** — pengelompokan metrik ke knowledge & capacity, alignment, efficiency (Gambar 3.4).
- **3.4.3 Statistik Inferensial** — Wilcoxon signed-rank (n = 5, α = 0,05).
- **3.4.4 Analisis Pareto** — pemetaan trade-off untuk menemukan varian Pareto-optimal.
- **3.4.5 Reproducibility & Threats to Validity** — dokumentasi mengikuti NeurIPS checklist + Wohlin et al. (2024).

**Standar BSI:** "Menjelaskan tentang proses mengolah data sehingga menjadi informasi baru."

## Daftar gambar BAB III
| Gambar | File | Konteks pemunculan |
|---|---|---|
| 3.1 Tahapan Penelitian | gambar/3.1_tahapan_penelitian.png | sub-bab 3.1 |
| 3.2 Pipeline Eksperimen | gambar/3.2_pipeline_eksperimen.png | sub-bab 3.2 |
| 3.3 Skema GQM | gambar/3.3_skema_GQM.png | sub-bab 3.4.1 |
| 3.4 3D Evaluation Framework | gambar/3.4_alur_evaluasi_3dimensi.png | sub-bab 3.4.2 |

## Daftar tabel BAB III
| Tabel | Judul | Letak |
|---|---|---|
| 3.1 | Spesifikasi Hardware Eksperimen | sub-bab 3.2.1 |
| 3.2 | Spesifikasi Software Eksperimen | sub-bab 3.2.2 |
| 3.3 | Spesifikasi Model dan Dataset Evaluasi | sub-bab 3.2.3 |
| 3.4 | GQM Matrix Penelitian | sub-bab 3.4.1 |

## Catatan kualitas akademik
- Setiap angka spesifik (n = 5, α = 0,05, 100 sampel, dst.) **wajib** dijelaskan justifikasinya.
- Hindari klaim "metode terbaik"; gunakan klaim "metode yang umum dipakai pada literatur 2023–2026".
- Setiap konfigurasi yang berpotensi memengaruhi hasil (governor CPU, suhu ambient, durasi cooldown) **wajib** dicantumkan agar reproducibility terjaga.
- Bila ada perubahan tahapan saat pelaksanaan, dokumentasikan deviasi tersebut beserta alasannya pada BAB IV.
