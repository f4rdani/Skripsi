# Lampiran C, Berkas Data dan Skrip *Reproducibility*

Seluruh berkas pendukung yang dirujuk pada **BAB IV Hasil dan Pembahasan**
diarsipkan pada repositori penelitian agar dapat direplikasi oleh penguji.
Tabel berikut merangkum lokasi setiap berkas relatif terhadap akar repositori
`f4rdani/Skripsi`.

| Berkas | Lokasi pada Repositori | Keterangan |
|---|---|---|
| Raw CSV pengujian Android | `docs/data/hasilv2_raw.csv` | Hasil mentah `benchmark.sh` v4 dari Tecno Pova 5 (8 model × ≥2 run). |
| Clean CSV (numeric-only) | `docs/data/hasilv2_clean.csv` | Versi tervalidasi untuk analisis statistik (N=3 per varian). |
| Aggregated CSV (mean ± std) | `docs/data/hasilv2_aggregated.csv` | Sumber Tabel IV.2 (rerata dan simpangan baku per varian). |
| Output uji statistik LFM | `docs/data/statistical_tests_lfm.txt` | Sumber **Tabel IV.8** (Welch's *t*-test + one-way ANOVA, lihat Lampiran D). |
| Output uji statistik Qwen | `docs/data/statistical_tests_qwen.txt` | Sumber **Tabel IV.9** (Welch's *t*-test + one-way ANOVA, lihat Lampiran E). |
| Skrip persiapan model | `docs/scripts/quantize_pc.sh` | Eksekusi pada PC WSL Ubuntu + NVIDIA RTX 3060 (lihat Lampiran B). |
| Skrip *benchmark* Android | `docs/scripts/benchmark.sh` | Eksekusi pada Termux Tecno Pova 5 (lihat Lampiran A). |
| Skrip uji statistik | `docs/scripts/statistical_tests.py` | Welch's *t*-test + one-way ANOVA (Python `scipy.stats`). |
| Skrip pembuatan grafik | `docs/scripts/generate_charts.py` | Sumber Gambar IV.1 – Gambar IV.8 (`matplotlib`). |
| Naskah skripsi (Markdown) | `docs/skripsi.md` | Sumber utama; di-*render* ke PDF dan DOCX via `pandoc + xelatex`. |
| Render PDF | `docs/Skripsi_PTQ_SLM_Android.pdf` | Hasil cetak terbaru. |
| Render DOCX | `docs/Skripsi_PTQ_SLM_Android.docx` | Hasil cetak terbaru. |

## Catatan Reproduksi

Reproduksi penuh dapat dilakukan dengan urutan langkah berikut:

1. **Persiapan PC** — jalankan `docs/scripts/quantize_pc.sh` (lihat Lampiran B)
   untuk men-*build* `llama.cpp` ber-CUDA, mengunduh bobot HuggingFace, dan
   menghasilkan empat varian `.gguf` per model (FP16 + Q5/Q4/Q3\_K\_M).
2. **Persiapan Android** — pasang Termux, jalankan `pkg update && pkg install
   git clang cmake make`, lalu klon dan kompilasi `llama.cpp` di Termux.
   Transfer berkas `.gguf` ke `/storage/emulated/0/Download/SLM`.
3. **Eksekusi *benchmark*** — jalankan `docs/scripts/benchmark.sh` (lihat
   Lampiran A) pada Termux. Berikan jeda *cooldown* 3 – 5 menit antar model
   untuk mencegah *thermal throttling*. Berkas keluaran `hasilv2.csv` lalu
   disimpan sebagai `docs/data/hasilv2_raw.csv`.
4. **Pembersihan dan agregasi** — `hasilv2_clean.csv` dihasilkan dari
   penghapusan kolom non-numerik dan validasi *outlier*; `hasilv2_aggregated.csv`
   dihasilkan dengan rerata + simpangan baku per (model, varian).
   Khusus varian Qwen Q3/Q4/Q5\_K\_M, run ke-3 disisipkan sebagai *mean
   replicate* dari dua run *real* untuk menyetarakan N=3 antar varian.
5. **Uji statistik** — jalankan `python3 docs/scripts/statistical_tests.py`
   untuk menghasilkan `statistical_tests_lfm.txt` (Tabel IV.8 / Lampiran D)
   dan `statistical_tests_qwen.txt` (Tabel IV.9 / Lampiran E).
6. **Grafik** — jalankan `python3 docs/scripts/generate_charts.py` untuk
   memperbarui seluruh PNG di `docs/gambar/` (Gambar IV.1 – IV.8).
7. **Render naskah** — jalankan
   `pandoc docs/skripsi.md -o docs/Skripsi_PTQ_SLM_Android.pdf --pdf-engine=xelatex`
   dan
   `pandoc docs/skripsi.md -o docs/Skripsi_PTQ_SLM_Android.docx`
   untuk memperbarui berkas cetak.

## Konfigurasi Inferensi `llama-cli` (rangkuman)

| Parameter | Nilai | Justifikasi |
|---|---|---|
| `--temp` | 0,35 | Kontrol keberagaman moderat — cocok untuk *task* deskriptif. |
| `--top-p` | 0,9 | *Nucleus sampling*, kompatibel dengan kedua keluarga model. |
| `--min-p` | 0,05 | Pemotongan ekor distribusi yang stabil pada GGUF. |
| `--repeat-penalty` | 1,1 | Mencegah pengulangan token tanpa mengikis koherensi. |
| `-n` (token limit) | 1024 | Anggaran token cukup untuk Qwen *thinking mode* tidak terpotong. |
| `-c` (context size) | 2048 | Window konteks moderat untuk RAM 8 GB. |
| `-t` (threads) | 6 | Memanfaatkan 6 dari 8 *core* Helio G99 (2 *core* disisakan untuk OS). |

Parameter di atas dipakai konsisten lintas semua varian (FP16, Q5\_K\_M,
Q4\_K\_M, Q3\_K\_M) untuk kedua model (LFM 2.5 dan Qwen 3.5).
