# Penjelasan Gambar BAB IV

Catatan ini menjelaskan tujuan dan isi tiap gambar pada BAB IV. Seluruh gambar
diregenerasi via `scripts/make_figures.py` dari data riil pengukuran (kecuali
Gambar 4.6 yang masih menunggu pengujian Termux di Pova 5).

Konvensi visual (sama untuk seluruh bab):
- Bentuk node tunggal: rounded rectangle.
- Tiga warna utama: biru (default/proses), merah (alert/risiko), hijau
  (success/target). Untuk grafik perbandingan dua model: biru = LFM2.5-1.2B-Base,
  hijau = Qwen3.5-2B; konsisten di Gambar 4.1–4.5.
- Satu jenis panah (-|>) di seluruh diagram.
- Tidak ada ikon eksternal; semua keterangan adalah teks.

---

## Gambar 4.1 — `4.1_ukuran_berkas.png`
**Judul.** Ukuran Berkas Model GGUF (FP16 vs k-quants).

**Maksud.** Membuktikan secara visual reduksi storage progresif sesuai gradasi
presisi, menjawab RQ-1.

**Komponen.** Bar chart ganda (LFM biru, Qwen hijau) × empat varian (FP16, Q5,
Q4, Q3) dalam satuan MB. Label numerik ditempatkan di atas tiap bar.

**Dirujuk pada.** Subbab 4.1 (Hasil Pengujian Ukuran Berkas).

---

## Gambar 4.2 — `4.2_perplexity.png`
**Judul.** Perplexity WikiText-2 per Varian Kuantisasi.

**Maksud.** Memvisualkan tren PPL monoton (FP16 < Q5 < Q4 < Q3) yang
mengonfirmasi degradasi kualitas linguistik akibat kuantisasi.

**Komponen.** Bar chart ganda dengan tiga desimal di label.

**Dirujuk pada.** Subbab 4.2 (Hasil Pengujian Kualitas Linguistik).

---

## Gambar 4.3 — `4.3_akurasi_mmlu_gsm8k_humaneval.png`
**Judul.** Akurasi MMLU, GSM8k, HumanEval per Varian Kuantisasi.

**Maksud.** Memperlihatkan perbandingan akurasi 8 kondisi (2 model × 4 varian)
pada tiga benchmark berbeda dalam satu kanvas dengan sumbu Y bersama (0–70 %).

**Komponen.** Tiga panel sub-plot horizontal (MMLU, GSM8k, HumanEval), masing-
masing menampilkan dua model dengan empat varian.

**Dirujuk pada.** Subbab 4.3 (Hasil Pengujian Akurasi Kognitif).

---

## Gambar 4.4 — `4.4_pareto_storage_vs_accuracy.png`
**Judul.** Pareto Storage vs Composite Accuracy.

**Maksud.** Menjawab RQ-4 secara parsial (sumbu storage dan akurasi). Dimensi
RAM dan TPS akan ditambahkan setelah subbab 4.4 terisi.

**Komponen.** Scatter dua sumbu (relative storage di X, composite accuracy di
Y), empat marker berbeda (FP16=lingkaran, Q5=kotak, Q4=segitiga, Q3=diamond),
dua warna model. Titik-titik untuk setiap model dihubungkan garis tipis untuk
menggambarkan trayektori reduksi.

**Dirujuk pada.** Subbab 4.5 (Analisis Trade-off Pareto).

---

## Gambar 4.5 — `4.5_radar_kualitas.png`
**Judul.** Radar Kualitas × Efisiensi (Storage · PPL⁻¹ · MMLU · GSM8k ·
HumanEval) — Per Model.

**Maksud.** Menyajikan rangkuman holistik per model. Lima sumbu dipilih agar
semuanya berorientasi "lebih luas = lebih baik" (storage di-invert, PPL
di-invert, akurasi langsung).

**Komponen.** Dua panel polar bersisihan (LFM dan Qwen), masing-masing memuat
empat polygon area untuk FP16, Q5, Q4, Q3 dengan style garis berbeda
(continuous untuk FP16/Q5; dashed untuk Q4; dotted untuk Q3) supaya tetap
terbaca jika dicetak hitam-putih.

**Dirujuk pada.** Subbab 4.5 (Analisis Trade-off).

---

## Gambar 4.6 — `4.6_ram_tps_placeholder.png` (PLACEHOLDER)
**Judul.** Profil RAM dan Tokens per Second (placeholder — menunggu pengujian
Termux di Pova 5).

**Status.** Belum tersedia. Akan diregenerasi menjadi:
- Bar chart peak RAM (MB) dengan garis ambang 8 GB.
- Bar chart prompt-t/s dan generation-t/s side-by-side.

**Dirujuk pada.** Subbab 4.4 (Profil RAM dan TPS).

---

## Tabel ringkas peta gambar BAB IV
| Gambar | Tujuan singkat                                          | Sumber data         |
|--------|---------------------------------------------------------|---------------------|
| 4.1    | Reduksi storage (RQ-1)                                  | `ls -lh` GGUF       |
| 4.2    | Degradasi PPL (RQ-2 bagian linguistik)                  | llama-perplexity    |
| 4.3    | Akurasi tiga benchmark (RQ-2 bagian kognitif)           | lm-evaluation-harness |
| 4.4    | Trade-off storage × akurasi (RQ-4 parsial)              | gabungan 4.1 & 4.3  |
| 4.5    | Rangkuman holistik per model                            | gabungan 4.1–4.3    |
| 4.6    | Profil RAM & TPS (RQ-3) — placeholder                   | menunggu Termux Pova 5 |
