# Kurti\u0107 dkk. (2024) — "Give Me BF16 or Give Me Death"? Accuracy-Performance Trade-Offs in LLM Quantization

## Metadata Bibliografi

| Field | Value |
|---|---|
| Penulis | Eldar Kurti\u0107, Alexandre Marques, Shubhra Pandit, Mark Kurtz, Dan Alistarh |
| Judul | "Give Me BF16 or Give Me Death"? Accuracy-Performance Trade-Offs in LLM Quantization |
| Afiliasi | Red Hat AI, Institute of Science and Technology Austria |
| Venue | arXiv preprint |
| Tahun | 2024 (November) |
| arXiv | 2411.02355 |
| URL | <https://arxiv.org/abs/2411.02355> |

## Format Sitasi APA-7

> Kurti\u0107, E., Marques, A., Pandit, S., Kurtz, M., & Alistarh, D. (2024). *"Give me BF16 or give me death"? Accuracy-performance trade-offs in LLM quantization* (arXiv:2411.02355). arXiv. https://arxiv.org/abs/2411.02355

## Ringkasan dan Relevansi

Evaluasi *accuracy-performance trade-off* yang komprehensif di seluruh format kuantisasi (FP16, BF16, INT8, INT4, FP4, K-quants), mencakup *latency*, *throughput*, *memory*, dan akurasi pada *benchmark* akademik. Temuan utama:

1. Tidak ada satu format yang optimal untuk semua *use case*.
2. Penurunan akurasi akibat kuantisasi sangat tergantung pada *task*: *text generation* lebih toleran daripada *reasoning/math*.
3. Format K-quants yang dipakai di llama.cpp dapat mencapai keseimbangan *near-lossless* pada banyak *benchmark*.

## Kontribusi terhadap Skripsi

- **BAB IV 4.4.5 (Kuantifikasi Penurunan Kepintaran):** Memberikan kerangka pembandingan akurasi vs *resource* yang menjadi dasar penetapan *sweet spot* Q4\\_K\\_M.
- **BAB IV 4.3 (Hasil Uji Degradasi Kognitif):** Penelitian ini secara eksplisit mengonfirmasi bahwa *reasoning/math benchmark* paling sensitif terhadap kuantisasi.
