# Penjelasan Gambar BAB I

Catatan ini menjelaskan tujuan, isi, dan konteks pemunculan tiap gambar pada BAB I.

---

## Gambar 1.1 — `1.1_alur_inferensi_edge.png`
**Judul lengkap:** Perbandingan Alur Inferensi: Cloud-based vs On-Device (Edge) LLM/SLM.

**Maksud / pesan utama.** Menyandingkan dua paradigma deployment LLM/SLM secara visual, supaya pembaca langsung memahami **kenapa** edge inference diperlukan untuk topik skripsi ini.

**Komponen yang ditampilkan.**
- Baris atas (a) Cloud Inference: User → Internet (latensi & risiko privasi) → Cloud API LLM (GPU farm) → Response. Ini adalah baseline status quo.
- Baris bawah (b) On-Device / Edge Inference: User → Termux + llama.cpp (CPU ARM, RAM 8 GB) → SLM GGUF Q3/Q4/Q5_K_M → Response (offline). Inilah pendekatan yang dieksperimenkan pada skripsi.
- Caption hijau di bagian bawah merangkum tiga keuntungan edge: tanpa internet, privasi terjaga, biaya nol, latensi rendah.

**Kapan dirujuk.** Sub-bab 1.1 Latar Belakang Masalah, paragraf yang membahas perpindahan dari cloud ke edge serta privasi data.

**Sumber konsep.** Zhang et al. (2024) tentang Edge Intelligence; Zhan et al. (2025) tentang LLM lokal di domain biomedis privacy-preserving.

---

## Gambar 1.2 — `1.2_diagram_masalah_kompresi.png`
**Judul lengkap:** Identifikasi Permasalahan & Pendekatan Solusi.

**Maksud / pesan utama.** Memetakan tiga masalah utama (lihat 1.2 Identifikasi Permasalahan) ke dalam satu solusi tunggal (PTQ GGUF k-quants), kemudian menampilkan dua kategori outcome: teknis dan akademik.

**Komponen yang ditampilkan.**
- Tiga kotak merah di atas: Masalah 1 (cloud → privasi), Masalah 2 (RAM 8 GB → OOM), Masalah 3 (kompresi ekstrem → degradasi).
- Kotak oranye di tengah: Solusi PTQ GGUF k-quants Q3_K_M / Q4_K_M / Q5_K_M pada SLM LFM2-1.2B & Qwen3.5-2B.
- Kotak hijau (kiri bawah): outcome teknis—file size turun > 60%, peak RAM aman < 8 GB, TPS naik di CPU ARM.
- Kotak ungu (kanan bawah): outcome akademik—validasi 3D Evaluation Framework (Jin et al., 2024), pemetaan Pareto-optimal varian.

**Kapan dirujuk.** Sub-bab 1.2 Identifikasi Permasalahan, sebagai penutup yang merangkum tiga masalah dan menunjukkan jembatan ke solusi (sub-bab 1.5 Metode Penelitian).

**Sumber konsep.** Identifikasi masalah penelitian + 3D Evaluation Framework (Jin et al., 2024).
