# Penjelasan BAB IV — HASIL PENELITIAN DAN PEMBAHASAN

Catatan ini menjelaskan kerangka BAB IV. File `bab 4.txt` di folder ini sudah
diisi dengan **data riil pengukuran** (storage, perplexity, akurasi tiga
benchmark). Subbab 4.4 (RAM dan TPS on-device) sengaja dipertahankan sebagai
template kosong karena pengujian on-device pada smartphone Tecno Pova 5 belum
dilakukan (setup Termux + llama.cpp masih dalam tahap penyesuaian).

## Tujuan umum BAB IV
**Standar BSI:** "Berisi hasil dan pembahasan dari penelitian yang dilakukan, Bagian ini dapat menjelaskan tentang data dataset yang digunakan, perhitungan metode yang digunakan, instrument Penelitian yang digunakan, hasil dari penelitian. Data dapat dijelaskan dalam bentuk tabel dan atau gambar. Interpretasi dan ketajaman analisis dari penulis terhadap hasil yang diperoleh, termasuk pembahasan tentang pertanyaan yang timbul dari hasil observasi serta dugaan ilmiah yang dapat bermanfaat untuk kelanjutan bagi penelitian mendatang."

## Mapping RQ → Subbab BAB IV
| RQ (BAB I) | Subbab BAB IV | Tabel | Gambar |
|---|---|---|---|
| RQ-1 — Storage             | 4.1 | 4.1 | 4.1 |
| RQ-2 — Quality (PPL)       | 4.2 | 4.2 | 4.2 |
| RQ-2 — Quality (Akurasi)   | 4.3 | 4.3 | 4.3 |
| RQ-3 — RAM & TPS           | 4.4 | 4.4 (kosong, menunggu data) | 4.6 (placeholder) |
| RQ-4 — Pareto-optimal      | 4.5 | 4.5 | 4.4 + 4.5 |
| Ringkasan                  | 4.6 | —   | —   |

## Status data per November 2026
| Kategori data           | Status      | Sumber                                      |
|-------------------------|-------------|---------------------------------------------|
| Ukuran berkas GGUF      | Tersedia    | `ls -lh` direktori model                    |
| Perplexity WikiText-2   | Tersedia    | `llama-perplexity`                          |
| MMLU / GSM8k / HumanEval| Tersedia    | lm-evaluation-harness (100 sampel/benchmark)|
| Peak RAM smartphone     | **Belum**   | Menunggu Termux Pova 5                      |
| Tokens per Second       | **Belum**   | Menunggu Termux Pova 5                      |

## Cara mengisi subbab 4.4 ketika data RAM/TPS sudah ada
1. Tambahkan data ke `scripts/make_figures.py` pada dictionary baru `RAM_MB`
   dan `TPS` (mengikuti format `FILE_SIZE_MB`).
2. Implementasikan fungsi `fig_4_6_ram_tps()` (replace placeholder) yang
   menggambar dua bar chart (peak RAM dengan garis ambang 8 192 MB, dan
   prompt-t/s + generation-t/s side-by-side).
3. Jalankan `python3 scripts/make_figures.py` agar `4.6_ram_tps_placeholder.png`
   tertimpa berkas baru `4.6_ram_tps.png`. Update juga `DAFTAR_GAMBAR.txt` dan
   sub-bab 4.5 agar memasukkan dimensi RAM dan TPS ke analisis Pareto.
4. Lakukan uji Wilcoxon signed-rank (paired) FP16 vs setiap Qx_K_M untuk
   metrik dinamik (gen t/s, peak RAM). Gunakan `scipy.stats.wilcoxon` dengan
   `alternative="two-sided"` dan effect size r = Z/√N.
5. Tentukan Pareto frontier final menggunakan strict-domination check pada
   empat sumbu (storage hemat, akurasi tinggi, RAM rendah, TPS tinggi).

## Pola paragraf pembahasan yang dipakai (CLAIM → EVIDENCE → CONTEXT → IMPLICATION)
> Q4_K_M LFM2.5-1.2B-Base mereduksi storage 69,0 % dibanding FP16 (Tabel 4.1),
> sementara rerata akurasi tiga benchmark hanya turun 1,6 poin persentase
> (Tabel 4.3). Hasil ini konsisten dengan klaim Frantar et al. (2023) dan
> Lin et al. (2024) bahwa kuantisasi 4-bit dapat menjaga kualitas mendekati
> FP16. Implikasinya, Q4_K_M layak dipakai sebagai default deployment SLM 1–2 B
> pada smartphone Android RAM 8 GB.

## Catatan kualitas akademik
- Setiap angka **wajib** punya sumber tabel. Hindari angka melayang di paragraf tanpa rujukan tabel.
- Pembahasan harus melampaui deskripsi angka; ada interpretasi dan koneksi ke literatur.
- Catat eksplisit setiap *threats to validity* (mis. ukuran sampel benchmark 100 soal, varian MMLU pada SLM kelas 2 B) sebagaimana di subbab 4.3.
