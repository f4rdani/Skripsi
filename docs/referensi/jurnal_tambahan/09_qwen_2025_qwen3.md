# Qwen Team (2025) — Qwen3 Technical Report

## Metadata Bibliografi

| Field | Value |
|---|---|
| Penulis korporat | Qwen Team (Alibaba Group) |
| Judul | Qwen3 Technical Report |
| Venue | arXiv preprint |
| Tahun | 2025 (Mei) |
| arXiv | 2505.09388 |
| URL | <https://arxiv.org/abs/2505.09388> |

## Format Sitasi APA-7

> Qwen Team. (2025). *Qwen3 technical report* (arXiv:2505.09388). arXiv. https://arxiv.org/abs/2505.09388

## Ringkasan dan Relevansi

Laporan teknis resmi keluarga model Qwen3 (Alibaba). Inovasi utama:

1. Integrasi **dua mode di satu model**: ***thinking mode*** (untuk *multi-step reasoning* kompleks) dan ***non-thinking mode*** (untuk respons cepat berbasis konteks).
2. *Parameter scale* 0,6 B hingga 235 B (termasuk varian *Mixture-of-Experts*).
3. Mekanisme *adaptive routing* yang memutuskan kapan masuk ke *thinking mode* berdasarkan kerumitan *prompt*.

## Kontribusi terhadap Skripsi

- **BAB II 2.4 (Arsitektur Model Uji):** Memberikan rujukan resmi untuk arsitektur Qwen 3.5 yang dipakai sebagai *baseline* di skripsi.
- **BAB IV 4.3.3 (Keterbatasan Reasoning Model):** Menguatkan klaim bahwa Qwen 3.5 adalah model *reasoning* dengan blok `<think>`, yang menjadi sumber kompleksitas evaluasi GSM8K.
