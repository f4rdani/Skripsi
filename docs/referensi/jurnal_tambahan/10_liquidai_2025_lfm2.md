# Liquid AI (2025) — LFM2 Technical Report

## Metadata Bibliografi

| Field | Value |
|---|---|
| Penulis korporat | Liquid AI Team |
| Judul | LFM2 Technical Report |
| Venue | arXiv preprint |
| Tahun | 2025 (November) |
| arXiv | 2511.23404 |
| URL | <https://arxiv.org/abs/2511.23404> |

## Format Sitasi APA-7

> Liquid AI. (2025). *LFM2 technical report* (arXiv:2511.23404). arXiv. https://arxiv.org/abs/2511.23404

## Ringkasan dan Relevansi

Laporan teknis resmi keluarga *Liquid Foundation Models* (LFM2), termasuk varian **LFM2-1.2B** yang dipakai di skripsi. Inovasi utama:

1. Arsitektur *hybrid backbone* yang menggabungkan *gated short convolutions* dengan *grouped query attention* — dirancang spesifik untuk *edge inference* dengan *prefill/decode* hingga 2\u00d7 lebih cepat di CPU dibanding model setara.
2. Tersedia paket *deployment* untuk **ExecuTorch, llama.cpp, dan vLLM**, sehingga sangat sesuai dengan tumpukan teknologi skripsi (Termux + llama.cpp).
3. *Training* dengan *Top-K knowledge distillation*, *curriculum learning*, dan *length-normalized preference optimization*.

## Kontribusi terhadap Skripsi

- **BAB II 2.4 (Arsitektur Model Uji):** Rujukan resmi untuk LFM 2.5 (1,2 B). Mengonfirmasi bahwa LFM 2 dirancang spesifik untuk *edge*, sehingga memperkuat *rasional* pemilihan model di skripsi.
- **BAB IV 4.4.1 (Efisiensi RAM dan Generation Speed):** Membantu menjelaskan kenapa LFM 2.5 secara konsisten lebih cepat daripada Qwen 3.5 yang setara secara parameter \u2014 perbedaan ini diakibatkan oleh arsitektur *hybrid* LFM 2 yang dirancang untuk *fast prefill/decode* di CPU.
