# Laskaridis dkk. (2024) — MELTing point: Mobile Evaluation of Language Transformers

## Metadata Bibliografi

| Field | Value |
|---|---|
| Penulis | Stefanos Laskaridis, Kleomenis Katevas, Lorenzo Minto, Hamed Haddadi |
| Judul | MELTing point: Mobile Evaluation of Language Transformers |
| Venue | *Proceedings of the 30th Annual International Conference On Mobile Computing And Networking (MobiCom '24)* |
| Tahun | 2024 |
| DOI | 10.1145/3636534.3690668 |
| arXiv | 2403.12844 |
| URL | <https://arxiv.org/abs/2403.12844> |

## Format Sitasi APA-7

> Laskaridis, S., Katevas, K., Minto, L., & Haddadi, H. (2024). MELTing point: Mobile evaluation of language transformers. *Proceedings of the 30th Annual International Conference on Mobile Computing and Networking (MobiCom '24)*, 1–15. https://doi.org/10.1145/3636534.3690668

## Ringkasan dan Relevansi

Studi sistematis pertama tentang eksekusi LLM *on-device* pada perangkat seluler (Android, iOS, dan Nvidia Jetson). Penulis mengembangkan infrastruktur otomatisasi MELT yang mendukung *headless execution* dan *benchmarking* LLM. Temuan utama:

1. Inferensi LLM bersifat *memory-bound* — sejalan dengan motivasi PTQ pada skripsi ini.
2. Kuantisasi mereduksi kebutuhan memori secara drastis dan membuat eksekusi *viable*, **dengan biaya akurasi yang tidak dapat diabaikan**.
3. *Continuous execution* LLM pada perangkat seluler masih sulit karena *thermal behavior* dan konsumsi energi.

## Kontribusi terhadap Skripsi

- **BAB I 1.1 (Latar Belakang):** Menguatkan klaim bahwa *on-device LLM* adalah topik aktual dan masih open problem.
- **BAB IV 4.4.1 (Efisiensi RAM dan Generation Speed):** Mendukung dalil *Memory-Bound* yang dikutip dari Zhang dkk. (2024).
