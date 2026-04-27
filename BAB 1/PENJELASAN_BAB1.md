# Penjelasan BAB I — PENDAHULUAN

Catatan ini merupakan rangkuman fungsi tiap sub-bab pada BAB I sesuai dengan **Handout Skripsi Prodi Teknologi Informasi** (Universitas Bina Sarana Informatika, Periode I 2024, halaman 11–12) dan adaptasinya untuk topik skripsi: **"Analisis Performa Post-Training Quantization (PTQ) pada Small Language Model untuk Implementasi Edge Computing Berbasis Android"**.

## Tujuan umum BAB I
BAB I berperan sebagai *prolog ilmiah*. Pembaca yang baru pertama kali melihat skripsi ini harus dapat menjawab tiga pertanyaan setelah selesai membaca BAB I:

1. **Apa** masalah yang diteliti?
2. **Mengapa** masalah itu penting & mendesak diteliti sekarang?
3. **Bagaimana** masalah itu akan dijawab (metode, batasan, hipotesis)?

## 1.1 Latar Belakang Masalah
**Fungsi:** Menarasikan konteks dunia nyata sehingga muncul "kebutuhan" akan penelitian ini. Susunan paragraf yang baik mengikuti pola **piramida terbalik**:
1. Konteks luas (LLM/SLM, NLP).
2. Tren / kebutuhan (asisten virtual, privacy, edge).
3. Hambatan teknis (RAM 8 GB, OOM, Force Close).
4. Pendekatan yang dipilih (PTQ GGUF k-quants).
5. Risiko / gap (perturbation, bukti empiris terbatas).
6. Kalimat penutup yang menegaskan apa yang akan diteliti & metodologi internasionalnya.

**Standar BSI:** Menjelaskan latar belakang munculnya ide, mengapa masalah penting, boleh menyertakan ringkasan penelitian terdahulu yang memperkuat alasan.

**Catatan untuk topik ini:** Latar belakang harus menyebut sitasi minimal 5 jurnal yang berasal dari folder `jurnal refrensi/` dan menyebut tahun rilis 2023–2026 untuk memenuhi syarat referensi 5 tahun terakhir.

## 1.2 Identifikasi Permasalahan
**Fungsi:** Menyaring kalimat-kalimat di latar belakang menjadi daftar permasalahan eksplisit (poin terpisah, biasanya 3–5 poin). Setiap poin menunjukkan **satu** masalah saja, ditulis dalam kalimat berita (bukan kalimat tanya).

**Standar BSI:** Berisi garis besar alasan pembuatan skripsi dan permasalahan yang ada.

**Catatan untuk topik ini:** Tiga poin utama yang dipakai—(1) ketergantungan cloud & risiko privasi, (2) keterbatasan RAM 8 GB & OOM, (3) risiko perturbation kuantisasi—mencerminkan tiga "sumbu" yang akan dievaluasi pada kerangka tiga dimensi Jin et al. (2024).

## 1.3 Perumusan Masalah
**Fungsi:** Mengubah daftar permasalahan menjadi **kalimat tanya** yang akan dijawab di BAB IV. Perumusan masalah idealnya bisa dipasangkan satu-per-satu dengan tujuan penelitian (1.4) dan dengan metrik di BAB III. Aturan praktis:
- Hindari pertanyaan yang berjawab ya/tidak; pakai "seberapa", "bagaimana", "varian mana".
- Pastikan setiap pertanyaan terukur (ada metrik kuantitatif).
- Jumlah pertanyaan = jumlah tujuan penelitian (kecuali tujuan teoretis tambahan).

**Standar BSI:** Perumusan masalah berbentuk kalimat tanya berdasarkan masalah yang akan dibahas.

**Catatan untuk topik ini:** Empat pertanyaan riset yang dipakai memetakan langsung ke empat dimensi metrik: (RQ1) storage, (RQ2) accuracy + perplexity, (RQ3) RAM + TPS, (RQ4) Pareto-optimal trade-off.

## 1.4 Tujuan dan Manfaat
### 1.4.1 Tujuan Penelitian
**Fungsi:** Menjelaskan apa yang ingin dicapai oleh peneliti. Ditulis dalam kalimat positif diawali kata kerja operasional (mengukur, membandingkan, menentukan, merekomendasikan). Setiap tujuan idealnya menjawab satu Perumusan Masalah.

### 1.4.2 Manfaat Penelitian
**Fungsi:** Menjelaskan dampak penelitian. Lazim dibagi menjadi:
- **Manfaat Praktis** — siapa yang diuntungkan secara langsung di lapangan (developer aplikasi, RS, korporat).
- **Manfaat Teoretis** — kontribusi ke literatur ilmiah / scaling laws / kerangka evaluasi.

**Standar BSI:** Menjelaskan tujuan dan manfaat dari penulisan skripsi.

## 1.5 Metode Penelitian
**Fungsi:** Memberi gambaran umum (executive summary) metode penelitian. Detail teknis dijabarkan di BAB III. Yang **harus** disebut di sini:
1. Jenis pendekatan (kuantitatif eksperimental).
2. Kerangka kerja standar internasional yang dipakai (GQM + Three-Dimensional Evaluation Framework Jin et al., 2024).
3. Disiplin pengukuran (n = 5 ulangan, warm-up dipisah, MLPerf-style).
4. Statistik komparasi (Wilcoxon signed-rank, α = 0,05).
5. Analisis akhir (Pareto, diagram radar).
6. Reproducibility (NeurIPS Reproducibility Checklist).

**Standar BSI:** Menjelaskan mengenai metode penelitian yang digunakan untuk mengumpulkan data.

## 1.6 Teknik Pengumpulan Data
**Fungsi:** Mendetailkan instrumen pengumpulan data, dibagi tiga sub-poin sesuai panduan BSI:
- **a. Observasi** — apa yang diamati, dengan instrumen apa, format log apa.
- **b. Wawancara** — bila ada (untuk skripsi rekayasa, sering opsional sebagai validator metodologi).
- **c. Studi Pustaka** — daftar jurnal, rentang tahun, manajemen referensi (Mendeley + APA).

**Standar BSI:** Menjelaskan teknik pengumpulan data: observasi, wawancara, studi pustaka.

## 1.7 Ruang Lingkup
**Fungsi:** Membatasi cakupan penelitian agar tidak meluas. Ruang lingkup berbeda dengan keterbatasan—ruang lingkup adalah **batas yang sengaja ditetapkan peneliti**, sedangkan keterbatasan adalah **kondisi luar yang tidak dapat dikontrol**.

Aspek yang lazim dibatasi pada skripsi rekayasa: hardware, lingkungan eksekusi, model uji, varian eksperimen, metrik kualitas, metrik sistem, metode yang **tidak** dievaluasi.

**Standar BSI:** Menjelaskan proses-proses yang dibahas pada penelitian berdasarkan latar belakang.

## 1.8 Hipotesis
**Fungsi:** Menyatakan dugaan ilmiah peneliti tentang hasil yang akan diperoleh. Hipotesis penelitian harus:
1. Spesifik dan terukur.
2. Dapat diuji secara empiris (falsifiable).
3. Sebaiknya menyebut arah perubahan (naik/turun) dan besaran kasar (≤ 5%, ≥ 2× lipat, dst).
4. Konsisten dengan teori di latar belakang.

**Standar BSI:** Mendeskripsikan secara konkret apa yang ingin dicapai/diharapkan dalam penelitian.

## Catatan tambahan
- Semua sitasi yang dipakai pada BAB I **harus** muncul di Daftar Pustaka dan ada di folder `jurnal refrensi/`.
- Format sitasi pada teks: gaya APA edisi ke-7 (Penulis et al., Tahun).
- Hindari gaya bahasa metaforis berlebihan ("rahim sistem", "sangkar isolasi", "dijebloskan"). Pakai diksi formal akademik.
- Setiap sub-bab dimulai dengan paragraf pembuka yang menyambungkan dengan sub-bab sebelumnya.
- Tidak boleh ada kalimat opini personal tanpa rujukan.

## Pemetaan singkat antara dokumen
| Sub-bab | Output dokumen | Cek konsistensi dengan |
|---|---|---|
| 1.2 Identifikasi | Tiga masalah | 2.2 Penelitian Terkait |
| 1.3 Perumusan | 4 RQ | 4 sub-bab di BAB IV |
| 1.4.1 Tujuan | 4 poin | 4 sub-bab di BAB IV |
| 1.5 Metode | GQM + 3D Eval | 3.1–3.4 BAB III |
| 1.6 Teknik | Observasi/Wawancara/Pustaka | 3.3 BAB III |
| 1.7 Ruang Lingkup | 7 batas | 3.2 Instrumen |
| 1.8 Hipotesis | H1 | 5.1 Kesimpulan |
