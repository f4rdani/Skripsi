# Warden & Situnayake (2019) — TinyML

## Metadata Bibliografi

| Field | Value |
|---|---|
| Penulis | Pete Warden, Daniel Situnayake |
| Judul | *TinyML: Machine Learning with TensorFlow Lite on Arduino and Ultra-Low-Power Microcontrollers* |
| Penerbit | O'Reilly Media, Inc. |
| Tahun terbit | 2019 (Desember) |
| ISBN cetak | 978-1-4920-5204-3 |
| ISBN ebook | 978-1-4920-5203-6 |
| Jumlah halaman | 504 |
| URL O'Reilly | <https://www.oreilly.com/library/view/tinyml/9781492052036/> |
| URL landing | <https://tinymlbook.com/> |
| Google Books | <https://books.google.com/books?id=tn3EDwAAQBAJ> |

## Format Sitasi APA-7

> Warden, P., & Situnayake, D. (2019). *TinyML: Machine learning with TensorFlow Lite on Arduino and ultra-low-power microcontrollers*. O'Reilly Media.

## Ringkasan dan Relevansi

Pete Warden (lead Google TensorFlow Lite Micro) dan Daniel Situnayake (lead developer experience di Edge Impulse) menulis buku rujukan utama dalam bidang *TinyML* yang mengkaji pemampatan model *deep learning* hingga ukuran kilobyte agar dapat dijalankan pada mikrokontroler dan perangkat ultra-low-power. Buku membahas:

- Latar belakang *embedded machine learning* dan motivasi pemrosesan AI di tepi (edge);
- Teknik kuantisasi 8-bit dan pemampatan model untuk TensorFlow Lite Micro;
- Optimasi *latency*, konsumsi energi, dan *binary size*;
- Studi kasus *speech-wake-word*, *person detection*, dan *gesture recognition* pada mikrokontroler dengan RAM 256 KB ke bawah.

## Kontribusi terhadap Skripsi

Skripsi ini mengangkat domain *Mobile Edge AI* yang merupakan ekstensi natural dari konsep *TinyML* — sehingga referensi Warden & Situnayake (2019) memberikan dasar teoretis untuk dua hal:

1. **BAB II — Konsep PTQ dan Edge Inference.** Buku ini menjabarkan secara komprehensif rasionalisasi kuantisasi (mengapa, kapan, dan dengan trade-off apa) yang menjadi dasar pemilihan GGUF *k-quants* di skripsi.
2. **BAB II — Strategi Optimasi *Latency-Energy-Binary* yang menjadi tiga pilar evaluasi dalam Tabel 4.2 (kecepatan inferensi, peak RAM proses, dan total waktu eksekusi).**

## Sub-bab Sitasi dalam Skripsi

- BAB II Sub-bab 2.1 (Konsep *Small Language Model*)
- BAB II Sub-bab 2.3 (*Post-Training Quantization*)
