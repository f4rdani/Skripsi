# Gope dkk. (2025) — Highly Optimized Kernels and Fine-Grained Codebooks for LLM Inference on Arm CPUs

## Metadata Bibliografi

| Field | Value |
|---|---|
| Penulis | Dibakar Gope, David Mansell, Danny Loh, Ian Bratt |
| Judul | Highly Optimized Kernels and Fine-Grained Codebooks for LLM Inference on Arm CPUs |
| Afiliasi | Arm Inc. |
| Venue | arXiv preprint |
| Tahun | 2025 (Januari) |
| arXiv | 2501.00032 |
| URL | <https://arxiv.org/abs/2501.00032> |

## Format Sitasi APA-7

> Gope, D., Mansell, D., Loh, D., & Bratt, I. (2025). *Highly optimized kernels and fine-grained codebooks for LLM inference on Arm CPUs* (arXiv:2501.00032). arXiv. https://arxiv.org/abs/2501.00032

## Ringkasan dan Relevansi

Studi resmi Arm Inc. mengenai *bottleneck* eksekusi LLM terkuantisasi pada CPU Arm. Temuan utama:

1. *Group quantization format* yang lazim untuk LLM memiliki *compute overhead* dan proses *dequantization* yang memberatkan.
2. Proporsi instruksi yang melakukan *multiplication* (kerja nyata) sangat rendah karena *unpacking* bobot mengonsumsi *cycle* CPU.
3. *Codebook quantization* dengan layout *interleaved group data* dapat menekan *overhead* *dequantization* dan memanfaatkan *vector/matrix multiply operations*.

## Kontribusi terhadap Skripsi

- **BAB IV 4.4.2 (Anomali *Prompt Speed* Q3\\_K\\_M):** Memberikan landasan teoretis kuat untuk anomali yang ditemukan: *overhead* *unpacking* susunan bit ganjil pada CPU Arm. Penelitian ini adalah rujukan langsung dari pembuat arsitektur Arm sendiri, sehingga kredibilitasnya sangat tinggi untuk klaim yang dibuat di skripsi.
