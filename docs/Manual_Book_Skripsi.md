---
title: "Manual Book Skripsi --- Panduan Membaca BAB III & BAB IV"
subtitle: "Pendamping naskah *Analisis Performa Post-Training Quantization (PTQ) pada Small Language Model untuk Implementasi Edge Computing Berbasis Android*"
author: "Ai Sha"
date: "Mei 2026"
geometry: "left=2.5cm,right=2.5cm,top=2.5cm,bottom=2.5cm"
fontsize: 11pt
mainfont: "Liberation Serif"
linestretch: 1.3
---

\newpage

# Pengantar

Manual book ini dibuat sebagai pendamping naskah skripsi untuk memudahkan
pembaca memahami **istilah teknis**, **rumus**, dan **tabel** yang muncul
pada BAB III (Metodologi Penelitian) dan BAB IV (Hasil Penelitian dan
Pembahasan). Setiap bagian disusun dengan format:

1.  **Definisi singkat** dalam Bahasa Indonesia.
2.  **Analogi atau penjelasan sehari-hari** agar konsep mudah dibayangkan.
3.  **Contoh angka** yang diambil langsung dari tabel di skripsi.
4.  **Cara membaca** tabel atau formula, langkah per langkah.

Manual ini tidak menambah atau mengubah data eksperimen. Tujuannya semata
menyediakan glosarium dan panduan bagi pembaca awam (termasuk penulis
sendiri) ketika perlu kembali ke naskah utama untuk meninjau hasil
penelitian.

\newpage

# Bagian 1: Glosarium Istilah Teknis

## 1.1 Istilah Tingkat Sistem

### 1.1.1 SLM (*Small Language Model*)
Model bahasa berukuran 1--3 miliar parameter. Dibanding LLM (*Large
Language Model*) yang punya ratusan miliar parameter, SLM cukup ringan
untuk dijalankan di perangkat seluler. Pada skripsi ini diuji dua SLM,
yaitu **LFM 2.5** (1,2 miliar parameter) dan **Qwen 3.5** (2 miliar
parameter).

### 1.1.2 PTQ (*Post-Training Quantization*)
Teknik kompresi model setelah model selesai dilatih. PTQ menurunkan
presisi angka di bobot model (misalnya dari 16-bit menjadi 4-bit) supaya
ukuran berkas mengecil dan inferensi lebih cepat, dengan trade-off
penurunan akurasi yang relatif kecil.

### 1.1.3 GGUF
Format berkas biner yang dipakai `llama.cpp` untuk menyimpan model
terkuantisasi. Bobot disimpan sudah dalam bentuk presisi rendah
(F16/Q5/Q4/Q3) sehingga bisa langsung dimuat ke RAM tanpa perlu
konversi tambahan saat *runtime*.

### 1.1.4 *k-quants*
Strategi kuantisasi presisi campuran yang dipakai pada GGUF. Bobot
"penting" (misalnya pada lapisan atensi atau lapisan akhir) diberi
presisi lebih tinggi, sedangkan bobot "biasa" dikompresi lebih agresif.
Pada skripsi ini diuji tiga varian:

> **Q5\_K\_M** -- presisi 5-bit, kualitas paling dekat dengan F16.
>
> **Q4\_K\_M** -- presisi 4-bit, *sweet spot* antara ukuran dan akurasi.
>
> **Q3\_K\_M** -- presisi 3-bit, paling kecil tetapi paling banyak
> kehilangan akurasi.

### 1.1.5 F16 (FP16)
Format *floating-point* 16-bit. Pada skripsi ini F16 dipakai sebagai
**baseline** (variabel kontrol) karena dianggap mendekati presisi
penuh tanpa kompresi.

### 1.1.6 *Edge Computing* / *Edge AI* / *Mobile Edge AI*
Paradigma komputasi yang menjalankan inferensi AI **di perangkat
pengguna** (misalnya *smartphone*) alih-alih di server *cloud*. Tujuan
utamanya adalah privasi data, latensi rendah, dan kemampuan operasi
*offline*.

### 1.1.7 *Host-to-Target Deployment*
Pola kerja dua mesin: bobot model disiapkan di **host** ber-GPU (PC
NVIDIA RTX 3060), lalu berkas `.gguf` hasilnya dipindahkan ke **target**
(Tecno Pova 5) untuk dieksekusi pada lingkungan akhir.

### 1.1.8 OOM (*Out-of-Memory*) dan *Force Close*
*OOM Killer* adalah mekanisme Android yang menghentikan paksa aplikasi
saat RAM hampir habis, biasanya tampak sebagai *Force Close* di layar
pengguna. Salah satu alasan utama mengapa SLM perlu dikuantisasi adalah
mencegah pemicuan *OOM Killer* ini.

### 1.1.9 *Thermal Throttling*
Penurunan otomatis frekuensi CPU/GPU ketika suhu chip melewati ambang
aman. Pada *smartphone* yang inferensi LLM-nya berlangsung beberapa
menit, *thermal throttling* dapat membuat *throughput* turun pelan-pelan
walau model tidak berubah.

## 1.2 Istilah Performa Perangkat Keras (*Hardware*)

### 1.2.1 *Peak* RAM (MB)
Jumlah memori RAM **maksimum** yang dipakai proses inferensi selama satu
sesi. Diukur dari `VmRSS` di `/proc/<pid>/status` setiap 0,5 detik.
Semakin kecil semakin baik karena memberi ruang lebih besar bagi OS dan
aplikasi lain.

**Contoh dari Tabel IV.2:** LFM 2.5 F16 menyerap 2.303,47 MB, sedangkan
LFM 2.5 Q3\_K\_M hanya 911,97 MB -- artinya kuantisasi menghemat hampir
1,4 GB RAM.

### 1.2.2 CPU *Peak* (%)
Beban CPU **maksimum** yang dicapai selama inferensi, diukur via metrik
`%CPU` di `ps`. Karena penelitian ini mengalokasikan **enam thread**,
skala teoritisnya **0--600%**. Nilai 300% berarti tiga *thread* penuh
terpakai; 600% berarti semua *thread* tersaturasi penuh.

**Contoh dari Tabel IV.2:** LFM 2.5 Q4\_K\_M mencatat 299,33% (sehat,
sekitar tiga *thread* aktif), sedangkan LFM 2.5 Q3\_K\_M mencapai
464,00% yang mendekati saturasi penuh dan berisiko *thermal
throttling*.

### 1.2.3 *Prompt Speed* (*Prompt TPS*, t/s)
Kecepatan model **membaca** dan **memproses prompt** masukan dari
pengguna, dalam satuan *token per second*. Semakin tinggi, semakin
cepat model "membaca soal".

### 1.2.4 *Generation Speed* (*Gen TPS*, t/s)
Kecepatan model **menulis** jawaban, juga dalam *token per second*.
Ini metrik paling penting bagi pengalaman pengguna karena menentukan
seberapa cepat jawaban muncul.

**Analogi:** Kalau *Prompt Speed* itu seperti kecepatan **membaca soal**,
maka *Generation Speed* itu kecepatan **menulis jawaban**.

### 1.2.5 Total Waktu Eksekusi (s)
Durasi total dari awal pemuatan model hingga jawaban selesai
diproduksi. Mencakup waktu membaca *prompt* + waktu menulis jawaban.

### 1.2.6 *Token*
Unit teks terkecil yang diproses model. Bahasa Indonesia rata-rata
satu kata terdiri dari 1--3 *token*; satu kalimat pendek biasanya
10--20 *token*; satu paragraf biasanya 80--150 *token*.

## 1.3 Istilah Performa Kognitif (*Software* / AI)

### 1.3.1 *Perplexity* (PPL)
Ukuran "kebingungan" model terhadap kalimat baru. Semakin **rendah**
PPL, semakin baik model dalam memprediksi kata berikutnya pada teks.
Berbeda dengan metrik lain, **PPL bersifat *inverse*: kecil lebih
baik**.

**Contoh dari Tabel IV.3:** LFM 2.5 F16 punya PPL 12,6829 (terbaik);
LFM 2.5 Q3\_K\_M punya PPL 14,5135 (sudah lebih bingung). Selisih 1,83
poin ini menandakan degradasi linguistik kecil tetapi terdeteksi.

### 1.3.2 MMLU (*Massive Multitask Language Understanding*)
Benchmark pilihan ganda A/B/C/D pada berbagai topik akademik
(matematika, sejarah, hukum, biologi, dst.). Skor dalam persentase
jawaban benar dari 100 sampel.

### 1.3.3 GSM8K (*Grade School Math 8K*)
Benchmark soal matematika tingkat SD/SMP dengan jawaban numerik. Skor
dalam persentase jawaban benar. **Untuk Qwen 3.5 yang *reasoning
model*, skor GSM8K dilaporkan sebagai *lower bound*** akibat
keterbatasan *parser* (lihat Sub-bab 4.3.3 di skripsi utama).

### 1.3.4 HumanEval (*Code Generation Benchmark*)
Benchmark menulis fungsi Python sederhana yang lalu diuji melalui
*unit-test*. Skor dalam persentase fungsi yang lolos *unit-test*.

### 1.3.5 MT-Bench TTR (*Type-Token Ratio*)
Skor keragaman leksikal jawaban generatif. TTR = jumlah kata unik /
jumlah total kata. **Skala 0--1, semakin tinggi semakin beragam
kosakatanya.** Pada tabel kadang ditampilkan dikalikan 100 (jadi skala
0--100) supaya satuannya sebanding dengan persentase akurasi.

**Contoh:** TTR 0,526 (= 52,6) artinya 52,6% kata pada jawaban model
adalah kata unik (tidak terulang). Nilai 0,403 menandakan banyak
pengulangan kata.

### 1.3.6 Retensi Kepintaran / Retensi Akurasi (%)
Persentase **akurasi rata-rata** sebuah varian terkuantisasi terhadap
**baseline F16**. Rumusnya:

$$
\text{Retensi (\%)} = \frac{\text{Rerata akurasi varian kuantisasi}}{\text{Rerata akurasi F16}} \times 100\%
$$

**Contoh dari Tabel IV.6:** Rerata akurasi LFM 2.5 Q4\_K\_M adalah
37,3%, sedangkan rerata F16 42,0%. Retensi = 37,3 / 42,0 × 100% = 88,9%.
Artinya Q4\_K\_M masih mempertahankan 88,9% kepintaran F16 (kehilangan
11,1%).

### 1.3.7 Delta (Δ) Akurasi
Selisih akurasi (dalam **poin persentase**) antara varian
terkuantisasi dengan F16. Tanda + berarti naik, tanda − berarti turun.

**Contoh dari Tabel IV.6:** GSM8K LFM 2.5 di F16 = 58% dan di Q3\_K\_M =
40%, sehingga ΔQ3 = −18. Artinya akurasi GSM8K **turun 18 poin** akibat
kuantisasi ke Q3\_K\_M.

### 1.3.8 *Compound Score*
Skor gabungan untuk menilai *trade-off* antara kecepatan, retensi
akurasi, dan konsumsi RAM. Rumusnya:

$$
\text{Compound Score} = \frac{\text{Gen TPS} \times \text{Retensi Akurasi}}{\text{RAM}_{\text{GB}}} \times 1000
$$

**Interpretasi:** Semakin tinggi, semakin baik. Skor ini mengukur
"berapa banyak *token per second* yang berguna (sudah dikalikan
retensi akurasi) yang bisa didapat per 1 GB RAM yang dikonsumsi".

**Contoh dari Tabel IV.7 (LFM 2.5 Q4\_K\_M):**

> Gen TPS = 13,67 t/s
>
> Retensi akurasi = 88,9% = 0,889
>
> RAM = 1.453 MB = 1,453 GB
>
> Compound Score = (13,67 × 0,889) / 1,453 × 1000 = 12,15 / 1,453 × 1000 = 8.363 / 1000 = **8,36**

Skor 8,36 artinya Q4\_K\_M memberikan 8,36 unit "produktivitas
inferensi" per GB RAM, jauh lebih baik daripada F16 (2,42) dan masih
kompetitif terhadap Q3\_K\_M (9,44). Q3 unggul aritmetik karena RAM-nya
kecil, tetapi penurunan akurasinya membuat Compound Score saja tidak
cukup sebagai dasar rekomendasi.

## 1.4 Istilah Statistik (BAB 4.4.6)

### 1.4.1 N (Jumlah Replikasi)
Berapa kali eksperimen diulang untuk satu varian. Pada skripsi ini N=3
untuk seluruh varian, artinya setiap varian (F16, Q5, Q4, Q3) di kedua
keluarga model (LFM dan Qwen) diuji tiga kali, lalu dihitung rerata
untuk dilaporkan pada Tabel IV.2.

### 1.4.2 Rerata (*Mean*)
Rerata = nilai rata-rata dari tiga pengulangan untuk tiap metrik.
Rerata dipilih sebagai bentuk pelaporan utama pada Tabel IV.2 agar
tabel mudah dibaca tanpa dipenuhi notasi sebaran data.

**Contoh:** Gen TPS LFM 2.5 Q4\_K\_M = 13,67 t/s adalah rerata dari
tiga ulangan pengujian pada Tecno Pova 5.

### 1.4.3 *Welch's t-test*
Uji statistik untuk menentukan apakah **dua rerata** berbeda secara
nyata (signifikan) atau hanya kebetulan. *Welch's t-test* adalah
varian yang lebih **konservatif** (lebih sulit menyatakan "berbeda
nyata") dibanding *t-test* klasik. Penelitian ini memakai uji ini
dengan taraf signifikansi **α = 0,05** (toleransi kesalahan 5%).

### 1.4.4 ANOVA (*Analysis of Variance*)
Uji statistik untuk menentukan apakah **tiga atau lebih kelompok**
secara keseluruhan punya rerata yang berbeda. Pada penelitian ini,
ANOVA dipakai untuk menilai apakah keempat varian (F16, Q5, Q4, Q3)
secara keseluruhan benar-benar berbeda. Detail nilai uji ANOVA
tersedia pada Lampiran D (LFM 2.5) dan Lampiran E (Qwen 3.5).

### 1.4.5 Notasi pada Tabel IV.8 dan IV.9
Tabel IV.8 dan IV.9 sengaja disederhanakan supaya mudah dibaca. Tiap
sel hanya berisi dua kemungkinan:

> **Beda** -- dua varian *berbeda nyata* pada metrik tersebut.
> Artinya perbedaan yang terlihat kemungkinan besar bukan kebetulan;
> selisih rerata cukup besar dibanding variasi alami antar ulangan.
>
> **Tidak** -- dua varian *belum cukup berbeda* untuk disebut nyata.
> Perbedaannya mungkin hanya selisih kecil yang masih bisa muncul
> akibat fluktuasi pengukuran.

Kolom **Ringkasan** di ujung kanan menerjemahkan hasil tiap baris
menjadi satu kalimat agar tabel langsung dipahami tanpa harus membaca
kata kunci di tiap sel.

**Analogi sederhana:** Bayangkan kamu menimbang dua kantong gula yang
seharusnya isinya sama. Kalau selisihnya jauh lebih besar daripada
fluktuasi timbangan, kamu yakin isinya memang beda (**Beda**). Kalau
selisihnya kecil dan masih dalam rentang ketidaktelitian timbangan,
kamu tidak bisa memastikan (**Tidak**).

Bagi pembaca yang ingin menelusuri angka uji lebih dalam (statistik
*t*, nilai *p*, F-ratio ANOVA), seluruh detail teknis sudah
dilampirkan pada **Lampiran D** dan **Lampiran E** skripsi utama.

\newpage

# Bagian 2: Panduan Membaca Tabel BAB III

## 2.1 Tabel III.0 -- Pemetaan Langkah MobileAIBench ke Tahap Penelitian

**Fungsi:** Menjelaskan bagaimana lima tahap penelitian ini (Sub-bab
3.1) sejalan dengan kerangka *workflow* enam langkah MobileAIBench
(Murthy dkk., 2024).

**Cara baca:**

> **Kolom kiri** = nama langkah pada *workflow* MobileAIBench.
>
> **Kolom kanan** = tahap penelitian yang mengisinya pada skripsi ini.

**Contoh interpretasi:** "Step 1--2 (*Task/Dataset Identification* +
*Data Preprocess/Loading*) -> Tahap 1 (Studi Pendahuluan)" berarti dua
langkah pertama MobileAIBench dikerjakan secara terpadu dalam Tahap 1.

## 2.2 Tabel III.1 -- Spesifikasi Perangkat Keras

**Fungsi:** Mendokumentasikan dua *host* yang dipakai pada eksperimen.

**Cara baca:**

> **Peran** -- jenis tugas yang ditangani *host* tersebut (persiapan
> model & evaluasi akurasi, vs. *target deployment*).
>
> **Komponen** -- nama komponen perangkat keras.
>
> **Spesifikasi** -- detail teknis komponen.
>
> **Keterangan** -- catatan tambahan, misalnya mengapa RAM 8 GB jadi
> *bottleneck*.

**Catatan penting:** RAM 8 GB pada Tecno Pova 5 menjadi *limit* paling
ketat karena memori dipakai bersama OS Android, sehingga eksekusi
model FP16 berisiko memicu *OOM Killer*.

## 2.3 Tabel III.2 -- Spesifikasi Perangkat Lunak

**Fungsi:** Mencantumkan *toolchain* lengkap di kedua *host*.

**Cara baca:** Sama dengan Tabel III.1, tetapi kolom "Komponen" diisi
oleh perangkat lunak (sistem operasi, *library*, skrip).

**Contoh interpretasi:** Baris "PC persiapan / Konversi & kuantisasi /
`convert_hf_to_gguf.py`, `./llama-quantize`" menunjukkan bahwa proses
konversi `.safetensors` -> `.gguf` dan kuantisasi ke Q5/Q4/Q3\_K\_M
semua dilakukan di PC, bukan di *smartphone*.

\newpage

# Bagian 3: Panduan Membaca Tabel BAB IV

## 3.1 Tabel IV.1 -- Reduksi Ukuran Berkas Model

**Fungsi:** Menunjukkan seberapa kecil berkas `.gguf` setelah
dikuantisasi.

**Cara baca:**

> **Model Arsitektur** -- LFM 2.5 atau Qwen 3.5.
>
> **Presisi / Format** -- F16, Q5\_K\_M, Q4\_K\_M, atau Q3\_K\_M.
>
> **Ukuran Berkas** -- ukuran fisik pada penyimpanan internal.
>
> **Persentase Reduksi** -- penurunan ukuran berkas terhadap F16
> *baseline* keluarga model yang sama.

**Contoh interpretasi:** LFM 2.5 Q4\_K\_M berukuran 698 MB, turun 68,27%
dari F16 yang 2,2 GB. Artinya kuantisasi 4-bit pada LFM menghemat dua
pertiga ukuran penyimpanan.

**Implikasi praktis:** Penghematan ini langsung berarti pengguna
*smartphone* dengan ROM 64--128 GB bisa menyimpan lebih banyak model
sekaligus.

## 3.2 Tabel IV.2 -- Performa Inferensi (Tabel Terpadat)

**Fungsi:** Tabel utama BAB IV. Mencatat lima metrik *hardware* untuk
delapan varian (4 varian × 2 keluarga model).

**Kolom-kolomnya:**

> **N** -- jumlah replikasi (selalu 3 pada penelitian ini).
>
> **Total Waktu (s)** -- durasi sebuah sesi inferensi dari awal hingga
> akhir.
>
> **Prompt Speed (t/s)** -- kecepatan baca *prompt* (lihat 1.2.3).
>
> **Gen Speed (t/s)** -- kecepatan tulis jawaban (lihat 1.2.4).
>
> **Peak RAM Proses (MB)** -- konsumsi RAM puncak (lihat 1.2.1).
>
> **CPU Peak (%)** -- beban CPU puncak (lihat 1.2.2; skala 0--600%).

**Cara membaca satu baris (contoh: LFM 2.5 Q4\_K\_M):**

> "3 \| 7,33 \| 43,67 \| 13,67 \| 1.452,97 \| 299,33"

Artinya: dari tiga ulangan pengujian, sesi inferensi rata-rata selesai
dalam 7,33 detik, model membaca *prompt* di 43,67 t/s, menulis jawaban
di 13,67 t/s, memakai RAM puncak 1.452,97 MB, dan CPU puncaknya 299,33%
(tiga *thread* aktif penuh). Seluruh nilai pada Tabel IV.2 adalah
rerata dari tiga ulangan.

**Cara membandingkan antar varian:**

1.  Tetapkan satu kolom metrik (mis. *Peak* RAM).
2.  Bandingkan F16 vs Q5 vs Q4 vs Q3 dalam keluarga model yang sama.
3.  Hitung persentase penurunan/peningkatan dengan rumus *delta*
    standar:
    $\frac{\text{nilai varian} - \text{nilai F16}}{\text{nilai F16}} \times 100\%$.

## 3.3 Tabel IV.3 -- *Perplexity* (PPL)

**Fungsi:** Mengukur degradasi linguistik akibat kuantisasi pada
dataset WikiText-2.

**Cara baca:** Kolom-kolomnya adalah varian (F16 sampai Q3\_K\_M), dan
baris-barisnya adalah dua keluarga model. **Nilai kecil = model lebih
"pintar" memahami bahasa**.

**Contoh interpretasi:** LFM 2.5 PPL naik dari 12,6829 (F16) menjadi
14,5135 (Q3\_K\_M). Pelebaran 1,83 poin ini relatif kecil di atas
*baseline* yang sudah 12 poin, sehingga degradasi linguistik LFM
secara umum masih dapat diterima.

## 3.4 Tabel IV.4 -- Akurasi LFM 2.5

**Fungsi:** Mencatat akurasi LFM 2.5 pada empat *benchmark* kognitif.

**Cara baca:**

> **Baris** -- jenis *benchmark* (MMLU, GSM8K, HumanEval, MT-Bench TTR).
>
> **Kolom** -- varian kuantisasi (F16, Q5, Q4, Q3).
>
> **Nilai** -- skor akurasi (% untuk tiga *benchmark* pertama; rasio
> 0--1 untuk MT-Bench TTR).

**Catatan margin error:** Karena setiap *benchmark* dijalankan dengan
n=100 sampel, **selisih ≤ 10 poin antar varian belum tentu bermakna**
secara statistik (margin error 95% CI ≈ ±10 poin pada distribusi biner
pass/fail).

## 3.5 Tabel IV.5 -- Akurasi Qwen 3.5

**Fungsi:** Sama dengan Tabel IV.4, tetapi untuk Qwen 3.5.

**Perhatian khusus pada GSM8K:** Qwen 3.5 adalah *reasoning model*
(menghasilkan blok `<think>...</think>` sebelum jawaban). Skor GSM8K
yang rendah (12--19%) **bukan menandakan model bodoh**, tetapi
keterbatasan *parser* yang sering tidak menangkap jawaban akhir
sebelum anggaran *token* habis. Penjelasan lengkap di Sub-bab 4.3.3.

## 3.6 Tabel IV.6 -- *Delta* Akurasi LFM 2.5

**Fungsi:** Menghitung **selisih akurasi** tiap varian terhadap F16,
beserta **rata-rata** dan **retensi**.

**Cara baca kolom:**

> **F16 (kontrol)** -- skor *baseline*.
>
> **Q5\_K\_M** dan **ΔQ5** -- skor varian Q5 dan selisihnya terhadap
> F16. Contoh: MMLU F16 = 32%, Q5 = 34%, ΔQ5 = +2 poin (naik 2 poin).
>
> **Q4\_K\_M** dan **ΔQ4** -- demikian pula untuk Q4.
>
> **Q3\_K\_M** dan **ΔQ3** -- demikian pula untuk Q3.

**Baris terakhir:**

> **Rata-rata akurasi tiga *benchmark*** -- rerata aritmetik dari
> MMLU, HumanEval, dan MT-Bench TTR (skala disetarakan ×100). GSM8K
> tidak dimasukkan ke rerata pada Tabel IV.6-B (Qwen) karena
> keterbatasan *parser*; untuk LFM 2.5 di Tabel IV.6, GSM8K **ikut**
> dihitung.
>
> **Retensi kepintaran** -- persentase rerata varian terhadap rerata
> F16. Contoh: Q4 LFM = 37,3% / 42,0% = 88,9%.

**Tabel IV.6 untuk LFM** termasuk GSM8K karena LFM bukan *reasoning
model* dan skor GSM8K-nya valid.

**Tabel IV.6-B untuk Qwen** tidak menyertakan GSM8K dalam rerata karena
skor tersebut berada di bawah margin instrumen.

## 3.7 Tabel IV.7 -- Matriks Rekomendasi LFM 2.5

**Fungsi:** Tabel pengambilan keputusan. Menggabungkan empat metrik
(RAM, Gen TPS, Total Waktu, Retensi Akurasi, CPU *Peak*) menjadi satu
skor: ***Compound Score***.

**Cara baca:**

> **Varian** -- pilihan F16 hingga Q3\_K\_M.
>
> **Peak RAM (MB)** -- ambil dari Tabel IV.2.
>
> **Gen TPS (t/s)** -- ambil dari Tabel IV.2.
>
> **Total Waktu (s)** -- ambil dari Tabel IV.2.
>
> **Retensi Akurasi** -- ambil dari Tabel IV.6 (baris paling bawah).
>
> **CPU Peak (%)** -- ambil dari Tabel IV.2.
>
> **Compound Score** -- dihitung dengan rumus di Sub-bab 1.3.8 manual
> ini.

**Cara memutuskan varian terbaik:**

1.  Lihat dua varian dengan *Compound Score* tertinggi (Q4 = 8,36 dan
    Q3 = 9,44).
2.  Periksa apakah skor tertinggi (Q3) punya **risiko** lain: CPU
    *peak* (464% mendekati saturasi), GSM8K (turun 18 poin), dan
    anomali *Prompt Speed* (18,27 t/s < 43,67 t/s pada Q4).
3.  Pilih varian dengan *trade-off* paling sehat. Dalam penelitian ini:
    **Q4\_K\_M** terpilih karena *Compound Score*-nya tinggi (8,36)
    tanpa risiko *thermal* atau *code-collapse*.

## 3.8 Tabel IV.6-B -- *Delta* Akurasi Qwen 3.5

**Fungsi:** Identik dengan Tabel IV.6, tetapi untuk Qwen 3.5.

**Yang harus diperhatikan:** Rerata Qwen **hanya dari tiga *benchmark***
(MMLU, HumanEval, MT-Bench TTR×100). GSM8K dilaporkan apa adanya pada
baris GSM8K, tetapi **tidak ikut** dihitung pada baris "Rata-rata".

**Contoh interpretasi:** Qwen Q3\_K\_M punya MMLU 40% (sama persis
dengan F16, ΔQ3 = ±0) tetapi HumanEval anjlok 27 poin (52% -> 25%).
Artinya kuantisasi 3-bit menggerus kemampuan *coding* Qwen jauh lebih
parah daripada kemampuan pemahaman umum.

## 3.9 Tabel IV.7-B -- Matriks Rekomendasi Qwen 3.5

**Fungsi:** Identik dengan Tabel IV.7, tetapi untuk Qwen.

**Cara baca dan analisis sama persis** dengan Tabel IV.7. Hasilnya:
Q4\_K\_M kembali jadi rekomendasi (Compound Score 1,76) meskipun
Q3\_K\_M aritmetik unggul (1,79), karena Q3 menyebabkan *code-collapse*
(HumanEval −27 poin) dan CPU *peak* tertinggi (525%).

**Mengapa skor Qwen jauh lebih kecil daripada LFM?** Karena Qwen
3.5 jenuh di 4--5 t/s pada CPU Helio G99, sedangkan LFM 2.5 mencapai
13--14 t/s. Rumus *Compound Score* sangat sensitif terhadap Gen TPS,
sehingga model 2B parameter pada CPU kelas menengah otomatis menerima
skor lebih kecil. Ini bukan berarti Qwen "kalah", melainkan ada
*hardware ceiling* yang sama-sama dialami semua varian Qwen.

## 3.10 Tabel IV.8 -- Ringkasan Uji Beda LFM 2.5

**Fungsi:** Mengonfirmasi apakah selisih rerata yang terlihat di Tabel
IV.2 benar-benar nyata atau cuma kebetulan. Tabel IV.8 sengaja
disederhanakan: nilai uji teknis (statistik *t* dan *p*) tidak
ditampilkan; sebagai gantinya tiap sel hanya berisi kata **Beda** atau
**Tidak**. Detail nilai uji bisa dicek pada **Lampiran D**.

**Cara baca per baris (contoh: F16 vs Q5\_K\_M):**

> **Pasangan Varian** -- dua varian yang dibandingkan.
>
> **Gen TPS \| Beda** -> *Generation Speed* F16 dan Q5\_K\_M berbeda
> nyata.
>
> **Prompt TPS \| Tidak** -> *Prompt Speed* F16 dan Q5\_K\_M tidak
> berbeda nyata (selisihnya masih dalam rentang fluktuasi pengukuran).
>
> **Peak RAM \| Beda** -> konsumsi RAM jelas berbeda.
>
> **Ringkasan** -- terjemahan satu kalimat: "Gen & RAM berbeda; Prompt
> tidak".

**Pesan utama dari Tabel IV.8:** *Generation Speed* dan *Peak* RAM
antar varian terbukti berbeda nyata di hampir seluruh pasangan,
sehingga klaim utama penelitian (kuantisasi mempercepat inferensi dan
mereduksi RAM) terdukung secara statistik. Keunggulan Q4\_K\_M atas
Q3\_K\_M juga terbukti nyata baik di Gen TPS maupun Prompt TPS.

## 3.11 Tabel IV.9 -- Ringkasan Uji Beda Qwen 3.5

**Fungsi:** Sama dengan Tabel IV.8, tetapi untuk Qwen 3.5.

**Pola penting yang harus diperhatikan:**

1.  **Reduksi RAM Qwen lebih dramatis** dibanding LFM. Seluruh pasangan
    tertulis **Beda** untuk kolom *Peak* RAM.
2.  **Gen TPS Qwen saturasi**. F16 vs Q5/Q4/Q3 semuanya **Beda**
    (kuantisasi mempercepat dari 1,87 t/s ke 4--5 t/s), tetapi antar
    Q5/Q4/Q3 semua tertulis **Tidak**. Artinya begitu Qwen
    dikuantisasi, kecepatannya "menabrak langit-langit" CPU di 4--5 t/s
    tidak peduli level kuantisasinya.
3.  **Anomali *Prompt Speed* Q3** kembali muncul. F16 vs Q3\_K\_M dan
    Q4\_K\_M vs Q3\_K\_M sama-sama tertulis **Beda** pada Prompt TPS,
    mengonfirmasi pola *unpacking* bit ganjil pada CPU ARM yang sudah
    dibahas di Sub-bab 4.4.2.

\newpage

# Bagian 4: Ringkasan Pengambilan Keputusan

Tabel ringkas berikut membantu pembaca memilih varian yang sesuai
dengan kebutuhan:

| Kondisi Pengguna | Varian Disarankan | Alasan Utama |
|---|:---:|---|
| Butuh akurasi maksimal, tidak peduli RAM/kecepatan | F16 | Tidak ada degradasi akurasi |
| Butuh akurasi tinggi, RAM longgar (≥ 4 GB ruang model) | Q5\_K\_M | Retensi akurasi tertinggi di antara varian terkuantisasi |
| **Butuh keseimbangan terbaik (RAM 8 GB)** | **Q4\_K\_M** | ***Sweet spot*: Compound Score tinggi tanpa risiko termal** |
| Butuh ukuran berkas paling kecil, akurasi sekunder | Q3\_K\_M | Cocok untuk *use case* non-matematis dan non-coding |

: Tabel M.1 Ringkasan Pengambilan Keputusan Varian Kuantisasi

\newpage

# Bagian 5: Penjelasan Notasi dan Simbol

| Notasi | Arti |
|:---:|---|
| `N` | Jumlah replikasi eksperimen (selalu 3) |
| `±` | Rerata ± simpangan baku |
| `Δ` (Delta) | Selisih terhadap *baseline* F16 (poin persentase) |
| `*p*` | *p-value* uji statistik |
| `**` | Berbeda nyata (*p* < 0,05), signifikan |
| `n.s.` | *Not significant*, tidak berbeda nyata (*p* ≥ 0,05) |
| `α` | Taraf signifikansi (0,05 = 5%) |
| `F` | Statistik F pada ANOVA |
| `t` | Statistik t pada Welch's *t-test* (semakin jauh dari 0, semakin kuat perbedaan) |
| `↓` | Penurunan/Reduksi (mis. ukuran berkas) |
| `t/s` | *Tokens per second* |

: Tabel M.2 Daftar Notasi dan Simbol

\newpage

# Bagian 6: Catatan Penutup

Manual book ini disusun sebagai pelengkap naskah utama dan dirancang
agar dapat digunakan secara mandiri. Pembaca yang ingin meninjau
metodologi penelitian, hasil eksperimen, dan pembahasan analisis tetap
disarankan untuk membaca naskah utama (BAB I--V). Sumber data mentah
dan skrip reproduksi tersedia pada folder `docs/data/` dan
`docs/scripts/`, sedangkan dokumen-dokumen pendukung tersedia pada
folder `docs/lampiran/`.

Apabila terdapat ketidakjelasan pada definisi istilah atau cara membaca
tabel, mohon merujuk pertama kali ke manual book ini, kemudian ke
naskah utama untuk konteks penuhnya.
