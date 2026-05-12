# Husom dkk. (2024) — Sustainable LLM Inference for Edge AI

## Metadata Bibliografi

| Field | Value |
|---|---|
| Penulis | Erik Johannes Husom, Arda Goknil, Merve Astekin, Lwin Khin Shar, Andre K\u00e5sen, Sagar Sen, Benedikt Andreas Mithassel, Ahmet Soylu |
| Judul | Sustainable LLM Inference for Edge AI: Evaluating Quantized LLMs for Energy Efficiency, Output Accuracy, and Inference Latency |
| Afiliasi | SINTEF (Norway), Singapore Management University, Oslo Metropolitan University, Kristiania University of Applied Sciences |
| Venue | arXiv preprint |
| Tahun | 2024 |
| arXiv | 2504.03360 |
| URL | <https://arxiv.org/abs/2504.03360> |

## Format Sitasi APA-7

> Husom, E. J., Goknil, A., Astekin, M., Shar, L. K., K\u00e5sen, A., Sen, S., Mithassel, B. A., & Soylu, A. (2024). *Sustainable LLM inference for edge AI: Evaluating quantized LLMs for energy efficiency, output accuracy, and inference latency* (arXiv:2504.03360). arXiv. https://arxiv.org/abs/2504.03360

## Ringkasan dan Relevansi

Analisis 28 LLM terkuantisasi dari pustaka Ollama yang di-*deploy* pada *Raspberry Pi 4* (RAM 4 GB). Metrik: efisiensi energi, performa inferensi, dan akurasi pada *benchmark* CommonsenseQA, BIG-Bench Hard, TruthfulQA, GSM8K, dan HumanEval. Penulis memakai *high-resolution energy measurement tool* (USB *current* sensor) untuk merekam konsumsi daya aktual.

Temuan kunci: terdapat *trade-off* eksplisit antara efisiensi energi, kecepatan, dan akurasi pada tingkat kuantisasi berbeda; konfigurasi optimal sangat tergantung pada *task*.

## Kontribusi terhadap Skripsi

- **BAB V 5.2 (Keterbatasan Penelitian):** Memberi rujukan terkini untuk metodologi pengukuran energi pada perangkat *edge* (yang belum termasuk dalam skripsi ini namun direkomendasikan untuk penelitian lanjutan).
- **BAB I 1.1 (Latar Belakang):** Menguatkan urgensi *sustainable AI* pada perangkat *edge*.
