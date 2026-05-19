# Lampiran — Skripsi PTQ SLM Android

Direktori `docs/lampiran/` ini berisi seluruh **lampiran** yang dirujuk oleh
naskah skripsi:

> *Analisis Performa Post-Training Quantization (PTQ) pada Small Language
> Model untuk Implementasi Edge Computing Berbasis Android.*

Lampiran dipisahkan ke berkas masing-masing untuk memudahkan *review* dan
reproduksi. Naskah utama (`docs/skripsi.md`) tetap menampilkan ringkasan
ke-5 lampiran ini di bagian **LAMPIRAN** sehingga pembaca PDF/DOCX dapat
melihat konten langsung tanpa membuka berkas terpisah.

| Lampiran | Berkas | Konten |
|---|---|---|
| **A** | `Lampiran_A_benchmark.sh` | Skrip Bash `benchmark.sh` v4 untuk Termux (Tecno Pova 5) — pengukuran TPS, RAM, CPU. |
| **B** | `Lampiran_B_quantize_pc.sh` | Skrip Bash untuk PC (WSL Ubuntu + RTX 3060) — *build* `llama.cpp` CUDA, unduh bobot HuggingFace, kuantisasi `.gguf`. |
| **C** | `Lampiran_C_data_dan_skrip_reproducibility.md` | Katalog seluruh berkas data dan skrip *reproducibility* di repositori. |
| **D** | `Lampiran_D_hasil_uji_statistik_lfm.txt` | Keluaran lengkap `statistical_tests.py` untuk LFM 2.5 — Welch's *t*-test + one-way ANOVA (sumber **Tabel IV.8**). |
| **E** | `Lampiran_E_hasil_uji_statistik_qwen.txt` | Keluaran lengkap `statistical_tests.py` untuk Qwen 3.5 — Welch's *t*-test + one-way ANOVA (sumber **Tabel IV.9**). |

## Catatan Versi Data

Per **Mei 2026**, agregat `docs/data/hasilv2_aggregated.csv` berisi **N = 3**
*replicate* untuk seluruh 8 varian (`LFM2.5-{F16,Q5,Q4,Q3}_K_M`,
`Qwen3.5-2B-{F16,Q5,Q4,Q3}_K_M`).

## Reproduksi Singkat

```bash
# 1) Generate ulang agregat + uji statistik
python3 docs/scripts/statistical_tests.py

# 2) Generate ulang seluruh grafik (Gambar IV.1 - Gambar IV.8)
python3 docs/scripts/generate_charts.py

# 3) Render ulang PDF + DOCX
(cd docs && pandoc skripsi.md -o Skripsi_PTQ_SLM_Android.pdf --pdf-engine=xelatex)
(cd docs && pandoc skripsi.md -o Skripsi_PTQ_SLM_Android.docx)
```
