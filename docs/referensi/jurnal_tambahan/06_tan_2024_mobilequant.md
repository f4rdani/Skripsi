# Tan dkk. (2024) — MobileQuant: Mobile-friendly Quantization for On-device Language Models

## Metadata Bibliografi

| Field | Value |
|---|---|
| Penulis | Fuwen Tan, Royson Lee, \u0141ukasz Dudziak, Shell Xu Hu, Sourav Bhattacharya, Timothy Hospedales, Georgios Tzimiropoulos, Brais Martinez |
| Judul | MobileQuant: Mobile-friendly Quantization for On-device Language Models |
| Afiliasi | Samsung AI Center Cambridge |
| Venue | arXiv preprint |
| Tahun | 2024 (Agustus) |
| arXiv | 2408.13933 |
| URL | <https://arxiv.org/abs/2408.13933> |

## Format Sitasi APA-7

> Tan, F., Lee, R., Dudziak, \u0141., Hu, S. X., Bhattacharya, S., Hospedales, T., Tzimiropoulos, G., & Martinez, B. (2024). *MobileQuant: Mobile-friendly quantization for on-device language models* (arXiv:2408.13933). arXiv. https://arxiv.org/abs/2408.13933

## Ringkasan dan Relevansi

Metode PTQ baru dari Samsung AI yang khusus dirancang agar ramah eksekusi pada perangkat seluler. Kontribusi utama:

1. Mengidentifikasi bahwa kuantisasi *activation* di bawah 16-bit sering memicu *overhead* komputasi tinggi karena dukungan kuantisasi *on-device* yang lemah.
2. Mengusulkan PTQ yang mengoptimasi *weight transformation* dan *activation range parameter* secara *end-to-end*.
3. Mencapai *near-lossless quantization* pada serangkaian *benchmark* LLM dengan pengurangan *latency* dan energi 20\u201350% dibanding strategi *on-device* yang ada.

## Kontribusi terhadap Skripsi

- **BAB II 2.3 (PTQ):** Memperkaya pembahasan keluarga PTQ modern (selain GPTQ, AWQ, dan GGUF *k-quants*) dengan kontribusi yang berorientasi spesifik pada mobile.
- **BAB IV 4.4.5 (Rekomendasi Varian Operasional):** Memberi konteks tentang keberadaan metode kuantisasi mobile alternatif sebagai *future work*.
