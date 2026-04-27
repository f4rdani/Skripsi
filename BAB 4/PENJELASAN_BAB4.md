# Penjelasan BAB IV — HASIL PENELITIAN DAN PEMBAHASAN

Catatan ini menjelaskan kerangka BAB IV. Bab ini ditulis **setelah** seluruh data eksperimen tersedia. File `bab 4 TEMPLATE.txt` di folder ini sudah berisi kerangka tabel + paragraf siap-isi.

## Tujuan umum BAB IV
**Standar BSI:** "Berisi hasil dan pembahasan dari penelitian yang dilakukan, Bagian ini dapat menjelaskan tentang data dataset yang digunakan, perhitungan metode yang digunakan, instrument Penelitian yang digunakan, hasil dari penellitian. Data dapat dijelaskan dalam bentuk tabel dan atau gambar. Interpretasi dan ketajaman analisis dari penulis terhadap hasil yang diperoleh, termasuk pembahasan tentang pertanyaan yang timbul dari hasil observasi serta dugaan ilmiah yang dapat bermanfaat untuk kelanjutan bagi penelitian mendatang."

## Mapping RQ → Sub-bab BAB IV
| RQ (BAB I) | Sub-bab BAB IV | Tabel pendukung | Gambar pendukung |
|---|---|---|---|
| RQ1 — Storage | 4.1 | 4.1 | 4.1 |
| RQ2 — Quality (PPL + Akurasi) | 4.3 | 4.3 | 4.3 (radar) |
| RQ3 — RAM & TPS | 4.2 + 4.4 | 4.2, 4.4, 4.5 | 4.2, 4.4 |
| RQ4 — Pareto-optimal | 4.5 | 4.6 | 4.5 (Pareto) |

## Cara mengisi template
1. Copy file `bab 4 TEMPLATE.txt` menjadi `bab 4.txt`.
2. Ganti seluruh placeholder bertanda `<…>` dengan angka aktual.
3. Hitung selisih persentase `Δ vs FP16` di kolom yang sesuai.
4. Generate diagram (gambar/4.1_storage.png, 4.2_ram.png, 4.3_radar.png, 4.4_tps.png, 4.5_pareto.png) menggunakan skrip `scripts/make_figures.py` setelah menambahkan fungsi yang membaca CSV hasil.
5. Lakukan uji Wilcoxon signed-rank (paired) FP16 vs setiap Qx_K_M untuk metrik dinamik (gen t/s, peak RAM). Saya rekomendasikan `scipy.stats.wilcoxon` dengan `alternative="two-sided"` dan effect size r = Z/√N.
6. Tentukan Pareto frontier menggunakan strict-domination check pada empat sumbu (storage hemat, akurasi tinggi, RAM rendah, TPS tinggi).
7. Tulis paragraf pembahasan setiap sub-bab dengan pola: **Apa angkanya → Bagaimana dibanding baseline → Apakah konsisten dengan literatur → Implikasi praktis**.

## Format gambar BAB IV (saat data masuk)
- Diagram batang ukuran file (4.1).
- Diagram batang peak RAM dengan garis ambang 8 GB (4.2).
- Diagram radar PPL inv. + 3 akurasi (4.3).
- Diagram batang prompt t/s & gen t/s (4.4).
- Pareto plot storage × composite accuracy × peak RAM (4.5).

Placeholder radar dan Pareto sudah saya generate di `gambar/4.X_radar_placeholder.png` dan `gambar/4.Y_pareto_placeholder.png` dengan **data ilustrasi**—bukan data aktual—agar Anda bisa melihat layout target.

## Pola paragraf pembahasan yang baik
Pola **CLAIM → EVIDENCE → CONTEXT → IMPLICATION**:
> Q4_K_M LFM2-1.2B mereduksi storage 65,8% dibanding FP16 (Tabel 4.1), sementara akurasi MMLU hanya turun 1,2 poin (Tabel 4.3). Reduksi serupa juga teramati pada Qwen3.5-2B (66,1%, MMLU −1,4). Hasil ini konsisten dengan klaim Frantar et al. (2023) dan Jin et al. (2024) bahwa kuantisasi 4-bit dapat menjaga kualitas mendekati FP16 (≤ 5%). Implikasinya, Q4_K_M cocok dipakai sebagai default deploy SLM 1B–2B pada smartphone Android RAM 8 GB.

## Catatan kualitas akademik
- Setiap angka **wajib** punya sumber tabel. Hindari angka melayang di paragraf tanpa rujukan tabel.
- Pembahasan harus melampaui sekedar deskripsi angka; ada interpretasi & koneksi ke literatur.
- Bila ada anomali atau hasil yang berbeda dari hipotesis, **tetap dilaporkan** dan dijelaskan kemungkinan penyebabnya.
- Threats to validity yang sudah disebut di BAB III harus dikonfirmasi/diperbarui di Bagian 4.6 berdasarkan pengalaman pelaksanaan.
