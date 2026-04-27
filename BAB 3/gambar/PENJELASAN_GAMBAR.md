# Penjelasan Gambar BAB III

Catatan ini menjelaskan tujuan, isi, dan konteks pemunculan tiap gambar pada BAB III.

---

## Gambar 3.1 — `3.1_tahapan_penelitian.png`
**Judul lengkap:** Tahapan Penelitian (waterfall eksperimental).

**Maksud / pesan utama.** Memberi gambaran keseluruhan delapan tahap yang dilewati peneliti dari awal sampai laporan final. Setiap tahap menghasilkan artefak yang menjadi input tahap berikutnya, sehingga pembaca tahu **urutan kerja** yang harus dilakukan untuk mereplikasi penelitian.

**Komponen yang ditampilkan (kiri ke kanan).**
1. Studi Pustaka — review literatur 12 jurnal.
2. Perencanaan GQM — turunkan goal ke pertanyaan ke metrik.
3. Persiapan Model & Env — unduh bobot, konversi ke GGUF, kuantisasi.
4. Pengukuran Statik — file size, peak RAM idle.
5. Pengukuran Dinamik — prompt t/s, gen t/s.
6. Pengukuran Kualitas — PPL, MMLU, GSM8k, HumanEval.
7. Analisis Pareto + Stats — Wilcoxon, diagram radar, Pareto.
8. Pelaporan & Validasi — penulisan + re-run subset.

**Kapan dirujuk.** Sub-bab 3.1 Tahapan Penelitian, sebagai ilustrasi flow.

**Sumber konsep.** Adaptasi waterfall standar penelitian eksperimen ML systems + GQM (Basili et al., 1994) + MLPerf-style benchmarking.

---

## Gambar 3.2 — `3.2_pipeline_eksperimen.png`
**Judul lengkap:** Pipeline Eksperimen On-Device pada Tecno Pova 5.

**Maksud / pesan utama.** Memetakan pipeline teknis dari **sumber bobot** hingga **aggregator hasil**. Pembaca yang ingin mereplikasi tahu persis tool apa yang dipakai pada setiap step, dan log apa yang harus direkam.

**Komponen yang ditampilkan.**
- Baris 1 (atas): Sumber Bobot Hugging Face → Konversi & Kuantisasi llama.cpp convert.py + quantize → Artefak GGUF (8 file: 2 model × 4 varian).
- Baris 2 (tengah): Transfer ke Device adb push/scp → Termux llama.cpp build (NDK ARMv8 + NEON) → Eksekusi Benchmark llama-bench, perplexity, mmlu/gsm8k/humaneval scripts.
- Baris 3 (bawah): tiga sumber telemetri (sistem htop/meminfo, engine llama.cpp, skor benchmark) yang semuanya bermuara ke Aggregator Python pandas.
- Aggregator akhir: tabel hasil + diagram radar/Pareto + uji Wilcoxon.

**Kapan dirujuk.** Sub-bab 3.2 Instrumen Penelitian (akhir bagian instrumen sebelum 3.3).

**Sumber konsep.** Praktik benchmarking on-device pada llama.cpp + NeurIPS Reproducibility Checklist (NeurIPS, 2024).

---

## Gambar 3.3 — `3.3_skema_GQM.png`
**Judul lengkap:** Goal–Question–Metric (Basili et al., 1994).

**Maksud / pesan utama.** Menampilkan kerangka pengukuran empiris yang menurunkan **satu goal penelitian** ke empat **pertanyaan riset (Q1–Q4)** dan kemudian ke **metrik konkret yang dapat diukur (M1.x, M2.x, M3.x, M4.x)**. Pembaca akademik (terutama dosen pembimbing) langsung tahu bahwa skripsi ini memakai kerangka pengukuran yang sudah teruji 30+ tahun di Empirical Software Engineering.

**Komponen yang ditampilkan.**
- Goal di puncak: kuantifikasi trade-off PTQ k-quants pada SLM untuk Android RAM 8 GB.
- Empat Question (oranye): Q1 Storage hemat? · Q2 Kualitas terjaga? · Q3 RAM aman? · Q4 TPS naik?
- Empat blok Metric (hijau) di bawah masing-masing question:
  - Q1 → file size MB; ratio FP16/Qx.
  - Q2 → PPL WikiText-2; MMLU/GSM8k/HumanEval.
  - Q3 → peak RSS RAM; OOM count.
  - Q4 → prompt t/s; generation t/s.

**Kapan dirujuk.** Sub-bab 3.4.1 Goal–Question–Metric Matrix.

**Sumber konsep.** Basili et al. (1994) "The Goal Question Metric Approach"; Wohlin et al. (2024) "Experimentation in Software Engineering" 2nd ed.

---

## Gambar 3.4 — `3.4_alur_evaluasi_3dimensi.png`
**Judul lengkap:** Three-Dimensional Evaluation Framework (Jin et al., 2024).

**Maksud / pesan utama.** Mengelompokkan metrik dari Gambar 3.3 ke dalam **tiga dimensi evaluasi** sesuai standar internasional terbaru untuk LLM terkuantisasi (Jin et al., 2024). Pembaca tahu mengapa pemilihan metrik (MMLU, GSM8k, HumanEval, PPL, file size, RAM, TPS) bukan acak—melainkan refleksi dari knowledge & capacity (apa yang model "tahu"), alignment (seberapa "lancar" output), dan efficiency (seberapa hemat resource).

**Komponen yang ditampilkan.**
- Atas: model terkuantisasi (LFM2 / Qwen2.5 × Q3/Q4/Q5/FP16).
- Tiga dimensi sejajar:
  - Knowledge & Capacity (hijau) → MMLU, GSM8k, HumanEval.
  - Alignment (oranye) → Perplexity WikiText-2.
  - Efficiency (ungu) → File size, peak RAM, prompt t/s, gen t/s.
- Bawah: Aggregator yang menghasilkan diagram radar per model, diagram Pareto efficiency vs accuracy, uji Wilcoxon vs FP16, dan reproducibility checklist.

**Kapan dirujuk.** Sub-bab 3.4.2 Three-Dimensional Evaluation Framework, dan menjadi rujukan utama saat menyusun BAB IV.

**Sumber konsep.** Jin et al. (2024) "A Comprehensive Evaluation of Quantization Strategies for Large Language Models" (Findings of ACL 2024).
