# Penjelasan Gambar BAB II

Catatan ini menjelaskan tujuan, isi, dan konteks pemunculan tiap gambar pada BAB II.

---

## Gambar 2.1 — `2.1_arsitektur_transformer.png`
**Judul lengkap:** Arsitektur Transformer Decoder (basis SLM modern).

**Maksud / pesan utama.** Menampilkan blok-blok internal sebuah decoder-only transformer—yang menjadi cetak biru hampir seluruh SLM modern, termasuk LFM2 dan Qwen3.5—agar pembaca mengetahui **di mana** kuantisasi akan diaplikasikan (lapisan attention dan FFN).

**Komponen yang ditampilkan (dari atas ke bawah).**
1. Token + Positional Embedding — input ID token + informasi posisi.
2. RMSNorm — normalisasi sebelum attention.
3. Multi-Head Grouped-Query Attention (GQA) — mekanisme attention efisien-memori yang dipakai di LFM2/Qwen3.5.
4. Residual + (skip connection).
5. RMSNorm — normalisasi sebelum FFN.
6. SwiGLU FFN — feed-forward dengan aktivasi SwiGLU.
7. Residual +.
8. ×N decoder blocks — pengulangan blok 1–7 sebanyak N kali (LFM2.5-1.2B-Base ≈ 16 blok, Qwen3.5-2B ≈ 28 blok).
9. Final RMSNorm.
10. Linear → Softmax (vocab logits) — keluaran berupa distribusi probabilitas token berikutnya.

**Kapan dirujuk.** Sub-bab 2.1.2 Arsitektur Transformer Decoder.

**Sumber konsep.** Vaswani et al. (2017) untuk transformer asli; Touvron et al. (2023) untuk varian LLaMA-style; Lin et al. (2024) untuk GQA dan SwiGLU pada SLM modern.

---

## Gambar 2.2 — `2.2_skema_PTQ_GGUF_kquants.png`
**Judul lengkap:** Skema Post-Training Quantization GGUF k-quants (FP16 → Q5/Q4/Q3_K_M).

**Maksud / pesan utama.** Memvisualkan alur konversi bobot dari presisi FP16 ke tiga varian kuantisasi GGUF k-quants. Setelah membaca gambar ini pembaca paham bahwa skripsi ini menghasilkan **tiga artefak terkuantisasi per model** (Q5_K_M, Q4_K_M, Q3_K_M) dengan trade-off berbeda.

**Komponen yang ditampilkan.**
- Input kiri: Bobot FP16 (presisi tinggi) + Calibration set (WikiText-2).
- PTQ Engine (kotak oranye, llama.cpp quantize) — proses utama yang menerima bobot + kalibrasi.
- Tiga output:
  - Q5_K_M ≈ 5,5 bit/weight, kualitas mendekati FP16 (kotak hijau).
  - Q4_K_M ≈ 4,5 bit/weight, default sweet-spot (kotak oranye).
  - Q3_K_M ≈ 3,5 bit/weight, paling hemat tetapi risiko PPL ↑ (kotak merah).
- Caption: k-quants menggabungkan kuantisasi grouped (super-block) + scale FP16 untuk melindungi outliers.

**Kapan dirujuk.** Sub-bab 2.1.4 Format GGUF dan k-quants pada llama.cpp.

**Sumber konsep.** Frantar et al. (2023) GPTQ, Lin et al. (2024) AWQ, dokumentasi llama.cpp k-quants.

---

## Gambar 2.3 — `2.3_arsitektur_edge_intelligence.png`
**Judul lengkap:** Hierarki Edge Intelligence untuk Inferensi LLM/SLM.

**Maksud / pesan utama.** Menempatkan penelitian ini pada hierarki tiga-tier Edge Intelligence (Zhang et al., 2024) supaya pembaca paham bahwa skripsi ini berfokus pada **tier paling jauh dari cloud**, yaitu Edge Device.

**Komponen yang ditampilkan.**
- Tier 1: Cloud Tier (GPU clusters), latensi tinggi.
- Tier 2: Edge Server (MEC, Radio Access Network), latensi menengah.
- Tier 3: Edge Device (Smartphone Android Helio G99, 8 GB RAM), latensi rendah—**fokus penelitian**.
- Kotak biru di bawah: optimasi yang lazim dilakukan di Edge Intelligence (quantization, KV-cache compression, speculative decoding, batching dinamis).

**Kapan dirujuk.** Sub-bab 2.1.5 Edge Computing dan Edge Intelligence.

**Sumber konsep.** Zhang et al. (2024) "Edge Intelligence Optimization for LLM Inference".

---

## Gambar 2.4 — `2.4_taxonomy_quantization.png`
**Judul lengkap:** Taksonomi Teknik Kuantisasi LLM/SLM.

**Maksud / pesan utama.** Memetakan teknik-teknik kuantisasi yang ada saat ini dan menandai posisi **fokus penelitian** (GGUF k-quants Q3/Q4/Q5_K_M pada CPU ARM) di dalam taksonomi tersebut. Membantu pembaca melihat trade-off antara PTQ (cepat, tanpa training) vs QAT (lebih akurat tapi mahal).

**Komponen yang ditampilkan.**
- Akar: Kuantisasi LLM/SLM.
- Cabang utama: PTQ vs QAT.
- Sub-cabang PTQ: Weight-only GPTQ (Frantar 2023), Activation-aware AWQ (Lin 2024), Mixed-precision GGUF k-quants (llama.cpp), NormalFloat 4-bit QLoRA (Dettmers 2023).
- Kotak merah di bawah: Fokus penelitian — GGUF k-quants Q3_K_M / Q4_K_M / Q5_K_M pada CPU ARM (Helio G99).

**Kapan dirujuk.** Sub-bab 2.1.8 GQM dan Three-Dimensional Evaluation Framework (sebagai pemetaan taksonomi yang akan dievaluasi dengan kerangka 3D).

**Sumber konsep.** Frantar et al. (2023), Dettmers et al. (2023), Lin et al. (2024), dokumentasi llama.cpp.
