# Penjelasan BAB II — LANDASAN TEORI

Catatan ini menjelaskan fungsi dan struktur tiap sub-bab BAB II sesuai panduan **Handout Skripsi Prodi Teknologi Informasi BSI** (halaman 12–13).

## Tujuan umum BAB II
BAB II adalah **fondasi konseptual** penelitian. Pembaca harus mendapatkan tiga hal:
1. Penguasaan teori dasar yang dipakai (transformer, PTQ, GGUF, edge intelligence, GQM).
2. Konteks penelitian-penelitian sebelumnya yang sudah membahas tema serupa.
3. Profil objek/subjek yang diteliti (perangkat, model, software).

## 2.1 Tinjauan Pustaka
**Fungsi:** Menjelaskan teori-teori dan konsep yang berhubungan langsung dengan judul. Bukan sekadar definisi, tetapi konsep dasar yang memberi pembaca kerangka berpikir untuk memahami BAB III dan BAB IV.

**Standar BSI:** "Berisi semua teori-teori yang berhubungan dengan skripsi yang akan dibahas. Pada bab ini juga ditulis tentang tools/software/komponen yang digunakan untuk keperluan penelitian."

**Sub-bab yang dipakai (urutan dari umum → spesifik):**
1. **2.1.1 LLM dan SLM** — definisi dan posisi dalam taksonomi model bahasa.
2. **2.1.2 Arsitektur Transformer Decoder** — komponen blok decoder (RMSNorm, GQA, SwiGLU). Disertai Gambar 2.1.
3. **2.1.3 Post-Training Quantization (PTQ)** — definisi, GPTQ, AWQ, QLoRA.
4. **2.1.4 Format GGUF dan k-quants** — fokus utama metode kompresi yang dipakai. Disertai Gambar 2.2.
5. **2.1.5 Edge Computing dan Edge Intelligence** — paradigma deployment. Disertai Gambar 2.3.
6. **2.1.6 Spesifikasi MediaTek Helio G99** — hardware target.
7. **2.1.7 Benchmark MMLU/GSM8k/HumanEval/Perplexity** — metrik kualitas yang dipakai.
8. **2.1.8 GQM dan Three-Dimensional Evaluation Framework** — kerangka metodologi internasional. Disertai Gambar 2.4.
9. **2.1.9 Reproducibility dan Threats to Validity** — standar pelaporan modern.

**Catatan:** Susunan ini mengikuti pola **funnel** (corong)—dari konsep paling umum hingga ke metrik dan kerangka evaluasi paling spesifik—agar pembaca terbawa secara natural menuju BAB III.

## 2.2 Penelitian Terkait
**Fungsi:** Menunjukkan posisi penelitian ini terhadap state-of-the-art. Setiap penelitian terkait wajib:
- berasal dari jurnal/prosiding ilmiah.
- diterbitkan dalam **maksimal 5 tahun terakhir** (panduan BSI).
- minimal **5 kutipan** (panduan BSI).
- format sitasi **APA** dengan manajemen Mendeley.

Skripsi ini memakai **12 referensi** yang memenuhi syarat (terdapat di folder `jurnal refrensi/`).

**Format sub-bab yang dipakai:**
- Tabel ringkasan (No, Penulis, Tahun, Kontribusi).
- Penjelasan ringkas paragraf untuk setiap penelitian.
- Penjelasan dikaitkan secara eksplisit ke topik skripsi (mengapa relevan, bukan sekadar daftar abstrak).

## 2.3 Tinjauan Organisasi
**Standar BSI (panduan):** "Berisi tentang tinjauan organisasi ditempat riset dilakukan."

**Adaptasi untuk skripsi ini.** Penelitian ini bersifat rekayasa sistem (engineering thesis) dan tidak mengambil studi kasus pada satu organisasi tertentu. Karena itu sub-bab 2.3 diadaptasi—tetap memakai judul resmi panduan **"Tinjauan Organisasi"**—dengan isi yang dibagi menjadi:
- **2.3.1 Universitas Bina Sarana Informatika (BSI)** — institusi tempat skripsi disusun.
- **2.3.2 Smartphone Tecno Pova 5** — perangkat eksperimen.
- **2.3.3 LFM2-1.2B** — model uji 1.
- **2.3.4 Qwen3.5-2B** — model uji 2.
- **2.3.5 Termux dan llama.cpp** — runtime utama.

Adaptasi ini lazim dilakukan pada skripsi rekayasa di prodi yang sama, supaya struktur sub-bab tetap mengikuti panduan tetapi konten relevan dengan tema teknis.

## Aturan kutipan & gaya
- Setiap teori atau angka spesifik **wajib** memiliki sitasi.
- Hindari "tinjauan pustaka" yang hanya copy-paste abstrak; rangkum dengan kalimat sendiri.
- Setiap gambar disebut secara eksplisit di paragraf sebelumnya: "...ditampilkan pada Gambar 2.x."
- Setiap tabel diberi nomor + judul deskriptif di atas tabel (Tabel 2.x).
- Daftar referensi BAB II harus identik (subset) dengan Daftar Pustaka utama.

## Daftar gambar BAB II
| Gambar | File | Konteks pemunculan |
|---|---|---|
| 2.1 Arsitektur Transformer Decoder | gambar/2.1_arsitektur_transformer.png | sub-bab 2.1.2 |
| 2.2 Skema PTQ GGUF k-quants | gambar/2.2_skema_PTQ_GGUF_kquants.png | sub-bab 2.1.4 |
| 2.3 Hierarki Edge Intelligence | gambar/2.3_arsitektur_edge_intelligence.png | sub-bab 2.1.5 |
| 2.4 Taksonomi Teknik Kuantisasi | gambar/2.4_taxonomy_quantization.png | sub-bab 2.1.8 |

## Daftar tabel BAB II
| Tabel | Judul | Letak |
|---|---|---|
| 2.1 | Ringkasan Penelitian Terkait | sub-bab 2.2 |
