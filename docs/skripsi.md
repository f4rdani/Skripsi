---
title: |
  ANALISIS PERFORMA *POST-TRAINING QUANTIZATION* (PTQ) PADA *SMALL LANGUAGE MODEL*
  UNTUK IMPLEMENTASI *EDGE COMPUTING* BERBASIS ANDROID
author: "Penulis: [Nama Mahasiswa], NIM: [NIM]"
date: "Program Studi Teknologi Informasi, Fakultas Teknik dan Informatika, Universitas Bina Sarana Informatika"
lang: en
geometry:
  - top=4cm
  - bottom=3cm
  - left=4cm
  - right=3cm
fontsize: 12pt
mainfont: "Liberation Serif"
linestretch: 1.5
toc: false
number-sections: false
header-includes:
  - \usepackage{float}
  - \floatplacement{figure}{H}
  - \floatplacement{table}{H}
  - \usepackage{caption}
  - \captionsetup{labelformat=empty,labelsep=none,justification=centering,singlelinecheck=false}
  - \usepackage{tocloft}
  - \renewcommand{\cftfigpresnum}{}
  - \renewcommand{\cftfigaftersnum}{}
  - \setlength{\cftfignumwidth}{0pt}
  - \renewcommand{\cfttabpresnum}{}
  - \renewcommand{\cfttabaftersnum}{}
  - \setlength{\cfttabnumwidth}{0pt}
  - \setlength{\cftbeforefigskip}{4pt}
  - \setlength{\cftbeforetabskip}{4pt}
  - \setcounter{tocdepth}{3}
---

\renewcommand{\figurename}{Gambar}
\renewcommand{\tablename}{Tabel}
\renewcommand{\contentsname}{DAFTAR ISI}
\renewcommand{\listfigurename}{DAFTAR GAMBAR}
\renewcommand{\listtablename}{DAFTAR TABEL}
\renewcommand{\thefigure}{}
\renewcommand{\thetable}{}

\newpage

# ABSTRAK

\setstretch{1.0}

Pemanfaatan *Small Language Model* (SLM) secara *on-device* di Android terkendala kapasitas RAM 8 GB yang dibagi-pakai dengan sistem operasi, sehingga pemuatan model presisi penuh FP16 berisiko memicu *Out of Memory* dan *Force Close*. Penelitian ini bertujuan menganalisis performa metode *Post-Training Quantization* (PTQ) berformat GGUF *k-quants* (Q3\_K\_M, Q4\_K\_M, Q5\_K\_M) terhadap dua arsitektur SLM, yaitu LFM 2.5 (1,2B) dan Qwen 3.5 (2B), pada perangkat Tecno Pova 5 (Helio G99, RAM 8 GB) melalui lingkungan Termux dan mesin inferensi `llama.cpp`. Metode yang digunakan adalah eksperimen kuantitatif komparatif (*ablation study*) dengan mengukur reduksi ukuran berkas, konsumsi *peak* RAM proses, kecepatan *prompt* dan *generation* (t/s), serta degradasi kognitif melalui *Perplexity* WikiText-2 dan akurasi MMLU, GSM8K, HumanEval, dan MT-Bench. Setiap varian diuji tiga kali untuk memperoleh rerata performa yang stabil. Hasil menunjukkan varian Q4\_K\_M sebagai titik keseimbangan (*sweet spot*) terbaik: ukuran berkas tereduksi 68%, *peak* RAM LFM turun dari 2.303 MB ke 1.453 MB (efisiensi 36,9%), *generation* LFM meningkat dari 5,57 t/s ke 13,67 t/s (akselerasi 2,45×), dengan tambahan *perplexity* di bawah 0,6 poin. Sebaliknya, varian Q3\_K\_M memicu anomali *bit-shifting* dan degradasi akurasi signifikan, sehingga tidak direkomendasikan untuk produksi.

**Kata kunci:** *Post-Training Quantization*, *Small Language Model*, *Edge Computing*, GGUF, *k-quants*, Android, Helio G99, *Perplexity*.

\setstretch{1.5}

\newpage

# ABSTRACT

\setstretch{1.0}

On-device deployment of *Small Language Models* (SLM) on Android is constrained by the 8 GB RAM capacity shared with the operating system, putting full-precision FP16 models at risk of *Out of Memory* and *Force Close* events. This study analyzes the performance of *Post-Training Quantization* (PTQ) using GGUF *k-quants* (Q3\_K\_M, Q4\_K\_M, Q5\_K\_M) on two SLM architectures, namely LFM 2.5 (1.2B) and Qwen 3.5 (2B), running on a Tecno Pova 5 (Helio G99, 8 GB RAM) via Termux and the `llama.cpp` inference engine. The method is a comparative quantitative experiment (*ablation study*) measuring file-size reduction, peak process RAM, prompt and generation speed (t/s), and cognitive degradation through WikiText-2 *Perplexity* and MMLU, GSM8K, HumanEval, and MT-Bench accuracy. Each variant was tested three times to obtain stable performance averages. Results show Q4\_K\_M as the optimal *sweet spot*: file size is reduced by 68%, LFM peak RAM drops from 2,303 MB to 1,453 MB (36.9% efficiency), and LFM generation speed accelerates from 5.57 t/s to 13.67 t/s (2.45×), with perplexity penalty below 0.6 points. Conversely, Q3\_K\_M triggers *bit-shifting* anomalies on ARM CPUs and significant accuracy degradation, and is therefore not recommended for production.

**Keywords:** *Post-Training Quantization*, *Small Language Model*, *Edge Computing*, GGUF, *k-quants*, Android, Helio G99, *Perplexity*.

\setstretch{1.5}

\newpage

# KATA PENGANTAR

Puji syukur penulis panjatkan ke hadirat Tuhan Yang Maha Esa atas selesainya penyusunan skripsi yang berjudul **"Analisis Performa *Post-Training Quantization* (PTQ) pada *Small Language Model* untuk Implementasi *Edge Computing* Berbasis Android"**. Skripsi ini disusun sebagai salah satu syarat untuk menyelesaikan program sarjana pada Program Studi Teknologi Informasi, Fakultas Teknik dan Informatika, Universitas Bina Sarana Informatika.

Penulis menyampaikan terima kasih kepada dosen pembimbing, rekan-rekan mahasiswa, serta keluarga yang telah memberikan dukungan moral, masukan teknis, dan akses sumber daya selama proses penelitian berlangsung. Penulis menyadari bahwa skripsi ini masih jauh dari sempurna, sehingga kritik dan saran yang membangun sangat diharapkan demi penyempurnaan karya tulis serupa di masa depan.

Jakarta, [Tanggal] [Bulan] [Tahun]

Penulis,

[Nama Mahasiswa]

\newpage

\tableofcontents

\newpage

\listoffigures

\newpage

\listoftables

\newpage

# DAFTAR SIMBOL

**a. Simbol Statistik dan Matematis**

×
:   Tanda faktor pengali, digunakan untuk menyatakan akselerasi relatif terhadap *baseline* (mis. akselerasi 2,45× pada *generation speed*).

α
:   *Alpha*, tingkat signifikansi pada uji statistik. Pada Tabel IV.8 ditetapkan α = 0,05 (taraf kepercayaan 95%).

\vspace{6pt}

**b. Satuan Pengukuran**

t/s
:   *Tokens per second*, satuan kecepatan inferensi (*prompt speed* dan *generation speed*).

GB
:   *Gigabyte*, satuan kapasitas RAM sistem dan ukuran berkas model.

MB
:   *Megabyte*, satuan konsumsi *peak* RAM proses *llama.cpp*.

\vspace{6pt}

**c. Format Presisi Numerik dan Varian Kuantisasi**

FP16
:   *Floating-Point* 16-bit, presisi *baseline* tanpa kuantisasi.

FP32
:   *Floating-Point* 32-bit (digunakan sebagai referensi pada PC).

INT8
:   *Integer* 8-bit (referensi format kuantisasi non-*k-quants*).

Q3\_K\_M
:   GGUF *K-Quants* 3-bit varian *Medium*.

Q4\_K\_M
:   GGUF *K-Quants* 4-bit varian *Medium* (dipilih sebagai *sweet spot*).

Q5\_K\_M
:   GGUF *K-Quants* 5-bit varian *Medium*.

\newpage

# BAB I PENDAHULUAN

## 1.1 Latar Belakang Masalah

Lanskap teknologi kecerdasan buatan, terkhusus pada domain *Natural Language Processing* (NLP), saat ini mengalami disrupsi fundamental akibat penetrasi *Large Language Models* (LLM). Model berskala masif ini telah mendefinisikan ulang batas atas kemampuan komputasi mesin dalam menguraikan makna semantik dan membangkitkan teks yang setara dengan gaya kognitif manusia. Kendati menawarkan performa luar biasa, arsitektur LLM kontemporer menuntut spesifikasi infrastruktur komputasi, terutama *Graphics Processing Unit* (GPU),yang besar dan eksklusif. Ketergantungan absolut pada perangkat keras kelas atas ini pada akhirnya memicu fenomena defisit alokasi memori (*Out of Memory*) yang pasti terjadi apabila model dipaksakan beroperasi di atas perangkat keras komputasi reguler milik konsumen akhir (Touvron dkk., 2023).

Di sisi lain, pergeseran paradigma mobilitas digital meningkatkan tuntutan masyarakat akan asisten virtual pintar yang proaktif dan responsif secara *real-time* tanpa latensi jaringan. Kebutuhan praktis ini terlihat pada berbagai implementasi sektoral yang krusial, mulai dari layanan sistem informasi rumah sakit (Ahmad & Safudin, 2024) hingga integrasi simpul LLM dalam infrastruktur pemantauan jaringan nirkabel pada ekosistem kawasan urban (Sevim & Ibrahim, 2024). Namun, pemanfaatan layanan AI terpusat melalui *Cloud API* komersial menghadirkan eskalasi risiko keamanan yang fatal, terutama yang bersinggungan dengan jaminan privasi data pengguna. Untuk merespons ancaman tersebut, para ahli keamanan siber merekomendasikan agar pemrosesan AI dilokalisasi: eksekusi inferensi harus bergeser untuk dioperasikan secara otonom dan *offline* di titik terluar jaringan (*Edge Device*), seperti pada *smartphone* bersistem operasi Android. Langkah mitigasi ini esensial guna meredam potensi kebocoran rekam medis, rahasia korporat, maupun pangkalan data pribadi masyarakat (Zhan dkk., 2025).

Sebagai antitesis atas tuntutan privasi tersebut, *Small Language Models* (SLM) dirancang dengan rasio pemangkasan parameter yang signifikan agar lebih akomodatif terhadap kapasitas komputasi perangkat personal. Sayangnya, hambatan mekanis justru berasal dari fondasi arsitektur fisik gawai konsumen. Rata-rata *smartphone* kelas menengah hanya dibekali RAM 8 GB. Persoalan menjadi kian rumit karena kapasitas terbatas ini mengusung topologi *Unified Memory*, sebuah sistem di mana alokasi RAM harus dibagi-pakai (*shared memory*) dan diperebutkan secara ketat oleh sistem operasi Android beserta layanan latar belakang. Arsitektur tersebut tidak dirancang untuk menahan beban matriks model AI yang masih berwujud presisi tinggi 16-bit (*Floating-Point*/FP16). Apabila pemuatan model orisinal tetap dipaksakan, utilitas pengawas memori bawaan Android (*Low Memory Killer Daemon*) akan memicu protokol intervensi perlindungan dan mengeksekusi *Force Close*. Demi menghindari kelumpuhan operasional ini, optimasi *Edge Intelligence* menjadi prosedur yang mutlak diselenggarakan (Zhang dkk., 2024).

Salah satu intervensi komputasional paling krusial untuk menekan *memory footprint*,sehingga model AI dapat dimuat secara aman ke dalam sempitnya RAM *smartphone*,adalah melalui *Post-Training Quantization* (PTQ). Berbagai kajian terkini memvalidasi bahwa teknik pemadatan bobot menuju tingkat presisi menengah ke bawah (3-bit hingga 5-bit) terbukti secara empiris mampu mereduksi kebutuhan memori hingga kurang dari sepertiga dimensi aslinya, tanpa perlu melewati fase pelatihan ulang yang mahal (Dettmers dkk., 2023; Frantar dkk., 2023). Walaupun skema PTQ menawarkan efisiensi yang menjanjikan, mutilasi presisi pada matriks bobot tidak luput dari ancaman gangguan matematis (*perturbation*). Proses pemotongan presisi ini berisiko menghilangkan sebaran komponen parameter ekstrem yang berperan sebagai jangkar jaringan (*outliers*). Hilangnya *outliers* dapat bermuara pada degradasi akurasi logika kognitif serta kualitas tata bahasa model (Gong dkk., 2024).

Berangkat dari rangkaian determinan pada ekosistem *mobile edge computing* tersebut, penelitian ini difokuskan pada pengujian empiris atas performa algoritma kompresi PTQ dengan pendekatan presisi campuran (*mixed-precision k-quants*) yang dikonfigurasi bergradasi dari 3-bit hingga 5-bit (varian Q3\_K\_M, Q4\_K\_M, dan Q5\_K\_M). Target utama eksperimen ini adalah melokalisasi inferensi murni di dalam emulator terminal Android (Termux). Melalui matriks pengujian terstruktur pada dua SLM dengan ukuran berbeda (1,2 miliar dan 2 miliar parameter), penelitian ini bertujuan membuktikan secara empiris batas efektivitas kompresi yang paling sanggup menyelamatkan margin RAM dari *Force Close*, sembari menginvestigasi akselerasi *Tokens per Second* (TPS) pada CPU ARM dan signifikansi degradasi *Perplexity* yang menyertainya.

## 1.2 Identifikasi Permasalahan

Berdasarkan elaborasi latar belakang, dapat ditarik beberapa permasalahan utama yang menjadi fokus penelitian ini, yaitu:

1. **Kerentanan privasi pada arsitektur komputasi *cloud*.** Terdapat ketergantungan absolut pada layanan *cloud* komersial untuk pemrosesan instruksi LLM, yang rentan terhadap peretasan dan kebocoran data sensitif. Hal ini memicu urgensi akan hadirnya sistem AI otonom yang murni beroperasi secara *offline* langsung dari *edge device* pengguna.
2. **Limitasi arsitektur RAM pada *on-device deployment*.** Kapasitas RAM Android rata-rata 8 GB rawan mengalami krisis memori (*Out of Memory*) sehingga memicu *Force Close* saat memuat model FP16. Hingga kini belum ditemukan landasan empiris yang memetakan tingkat kompresi ideal yang paling seimbang dan aman untuk menetralisir anomali tersebut pada lingkungan *shared memory* Android.
3. **Risiko penurunan kecerdasan akibat kompresi ekstrem.** Pemadatan matriks SLM ke format ketat (Q3\_K\_M hingga Q5\_K\_M) menyimpan bahaya laten berupa halusinasi model dan meluruhnya kapabilitas nalar AI. Masih terdapat *research gap* yang signifikan mengenai persentase degradasi kecerdasan tatkala mesin dipaksa beroperasi di bawah tekanan kompresi tertingginya pada *smartphone*.

## 1.3 Perumusan Masalah

Berdasarkan identifikasi permasalahan di atas, rumusan masalah yang akan dijawab oleh penelitian ini adalah:

1. Berapa besar efisiensi penyimpanan (*storage efficiency*) dan reduksi konsumsi RAM yang dihasilkan oleh setiap varian kuantisasi GGUF (Q3\_K\_M, Q4\_K\_M, dan Q5\_K\_M) terhadap *baseline* FP16 pada model LFM 2.5 (1,2B) dan Qwen 3.5 (2B)?
2. Bagaimana perbandingan kualitas linguistik, diwakili oleh *Perplexity* (WikiText-2), serta akurasi kognitif (MMLU, GSM8K, dan HumanEval) yang dipertahankan oleh masing-masing varian kuantisasi terhadap *baseline* FP16?
3. Seberapa besar peningkatan kecepatan inferensi (*Prompt Processing* t/s dan *Text Generation* t/s) yang dapat dicapai pada perangkat MediaTek Helio G99 dengan RAM 8 GB melalui kompresi PTQ?
4. Berdasarkan tinjauan *trade-off* multi-dimensi (efisiensi penyimpanan, RAM, TPS, *Perplexity*, dan akurasi), varian model dan tingkat kuantisasi mana yang paling optimal untuk diterapkan pada *smartphone* berkapasitas RAM 8 GB?

## 1.4 Tujuan dan Manfaat

### 1.4.1 Tujuan Penelitian

1. Mengimplementasikan dan mengevaluasi kelayakan operasional varian PTQ presisi campuran (Q3\_K\_M, Q4\_K\_M, dan Q5\_K\_M) pada arsitektur SLM, sekaligus mengidentifikasi batas aman toleransi RAM Android terhadap pemicu *Force Close*.
2. Melakukan komparasi faktual melalui *benchmarking* yang membandingkan perilaku model FP16 dengan ketiga varian kuantisasinya, guna membuktikan persentase efisiensi alokasi RAM, akselerasi *Tokens per Second* (TPS), serta fluktuasi degradasi *Perplexity* dan akurasi MMLU/GSM8K/HumanEval.
3. Menetapkan rekomendasi konfigurasi (model parameter-size dan tingkat kuantisasi) yang paling optimal sebagai *sweet spot* operasional untuk perangkat Android berkapasitas RAM 8 GB.

### 1.4.2 Manfaat Penelitian

**Bagi Penulis:**

a. Sebagai sarana pemenuhan salah satu syarat akademik untuk meraih kelulusan pada Program Sarjana, Program Studi Teknologi Informasi, Fakultas Teknik dan Informatika, Universitas Bina Sarana Informatika.

b. Memperluas wawasan dan pengalaman praktis terkait implementasi *Mobile Edge Computing* serta strategi optimasi arsitektur kecerdasan buatan di lingkungan seluler yang terbatas.

c. Menjadi sarana penerapan teori perkuliahan, khususnya pada irisan multidisiplin *Machine Learning*, arsitektur perangkat keras mikro, dan algoritma pengolahan bahasa alami (NLP).

**Bagi Objek Penelitian (Pengembang Aplikasi *Edge AI*):**

a. Menyediakan pedoman purwarupa operasional bagi perancangan infrastruktur AI yang memberikan garansi keamanan privasi data, karena interaksi dilangsungkan secara lokal (*offline*).

b. Menawarkan alternatif resolusi finansial guna menekan biaya pemeliharaan IT, di mana pengguna atau korporasi tidak lagi tergantung pada layanan *Cloud API* komersial berbiaya bulanan.

c. Menghasilkan basis data telemetri yang presisi mengenai daya tahan RAM 8 GB Android terhadap beban eksekusi model AI pasca-kompresi.

d. Memberikan rekomendasi format bagi para pengembang *independent developer* guna merakit *chatbot* pintar yang tertanam (*embedded*) di gawai kelas menengah.

**Bagi Pembaca:**

Membuka cakrawala pemahaman teoretis maupun operasional bagi pembaca akademik dan praktisi industri perihal anatomi teknik kompresi PTQ, berikut tata laksana *deployment* SLM secara *offline* dan mandiri pada peranti Android.

## 1.5 Metode Penelitian

Penelitian ini menggunakan pendekatan **empiris kuantitatif eksperimental** dengan kerangka *ablation study* yang membandingkan empat tingkat presisi bobot model (FP16 sebagai *baseline*, lalu Q5\_K\_M, Q4\_K\_M, dan Q3\_K\_M sebagai varian terkompresi) di atas dua jenis *host* yang saling melengkapi. *Host* pertama adalah **PC dengan WSL2 Ubuntu dan GPU NVIDIA RTX 3060**, dipakai untuk tahap persiapan berkas `.gguf` melalui utilitas `huggingface-cli`, `convert_hf_to_gguf.py`, dan `./llama-quantize`, serta untuk mengukur metrik intrinsik model (Perplexity WikiText-2 dan akurasi MMLU/GSM8K/HumanEval/MT-Bench) yang memerlukan akselerasi paralel. *Host* kedua adalah ***smartphone* Tecno Pova 5** dengan emulator terminal *non-root* Termux dan mesin inferensi `llama.cpp` yang dikompilasi ulang secara natif untuk CPU ARM Helio G99, dipakai untuk mengukur metrik performa pada lingkungan *target deployment*: *peak* RAM proses, beban CPU, serta *Tokens per Second* (TPS). Setiap varian dijalankan melalui skenario terstandardisasi yang sama (parameter inferensi, anggaran *token*, jumlah *thread*, dan dataset evaluasi) agar perbedaan performa benar-benar dapat dikaitkan dengan tingkat kompresi, bukan variabel eksternal.

## 1.6 Teknik Pengumpulan Data

### A. Observasi (Eksperimental)

Observasi dilakukan dengan mengekstraksi log secara objektif atas seluruh dinamika perangkat keras dan perangkat lunak ketika siklus inferensi AI berlangsung. Pengukuran dibagi ke dalam dua *host*: (1) PC NVIDIA RTX 3060 (WSL Ubuntu) untuk mengukur *Perplexity* (modul `./llama-perplexity`) dan akurasi *benchmark* MMLU/GSM8K/HumanEval/MT-Bench karena tahap evaluasi akurasi membutuhkan waktu komputasi yang panjang; serta (2) perangkat Android Tecno Pova 5 melalui Termux untuk mengukur *peak* RAM proses (`VmRSS` dari `/proc/<pid>/status`), beban CPU (`%CPU` dari `ps`), serta *Tokens per Second* (TPS) yang dibaca dari keluaran statistik `llama-cli`. Berkas `.gguf` yang dieksekusi pada kedua *host* berasal dari satu *source-of-truth* sehingga hasil pengukuran tetap dapat diperbandingkan apple-to-apple. Pencatatan dilakukan pada setiap transisi resolusi kompresi (FP16, Q5\_K\_M, Q4\_K\_M, dan Q3\_K\_M) untuk kedua model.

### B. Wawancara

Karena penelitian ini bersifat **kuantitatif eksperimental** dan seluruh variabel dependennya berupa indikator komputasi objektif (TPS, *peak* RAM, beban CPU, *Perplexity*, dan skor akurasi *benchmark*) yang dapat diekstraksi langsung dari log sistem dan log mesin inferensi, teknik wawancara tidak diterapkan. Data primer sepenuhnya berasal dari instrumen pengukuran otomatis pada kedua *host* (PC dan *smartphone*) sebagaimana dijelaskan pada bagian A, sehingga tidak diperlukan instrumen opini subjektif dari narasumber. Validitas data dijaga melalui pengulangan ujian (tiga *run* per varian untuk LFM 2.5 dan dua *run* per varian untuk Qwen 3.5) yang dilanjutkan dengan uji statistik signifikansi (Welch's *t*-test + one-way ANOVA) sebagaimana disajikan pada Sub-bab 4.4.6.

### C. Studi Pustaka

Studi pustaka dilakukan dengan menghimpun dan memetakan referensi dari berbagai karya tulis ilmiah, baik jurnal nasional maupun internasional, yang dipublikasikan pada rentang 2023–2026. Fokus telaah literatur mencakup teori fundamental arsitektur LLM/SLM (Touvron dkk., 2023), teori gangguan matematis pada kuantisasi (Gong dkk., 2024), pedoman *Edge Intelligence* (Zhang dkk., 2024), serta validasi empiris penerapan `llama.cpp` di perangkat ARM dengan sumber daya terbatas (Ray & Pradhan, 2026). Referensi pilar dari Dettmers dkk. (2023), Frantar dkk. (2023), Lin dkk. (2023), dan Jin dkk. (2024) digunakan sebagai instrumen landasan teori sekaligus pemandu standar parameter kalibrasi pada tahap evaluasi.

## 1.7 Ruang Lingkup

Agar trajektori analisis tidak melebar dari sumbu permasalahan utama, ruang lingkup penelitian ini dibatasi sebagai berikut:

1. **Perangkat Keras Uji.** Seluruh proses inferensi AI dipusatkan pada satu *smartphone* kelas menengah, yaitu Tecno Pova 5 yang ditenagai SoC MediaTek Helio G99 (arsitektur ARM *big.LITTLE*), RAM LPDDR4x 8 GB, dan ROM UFS 2.2 256 GB.
2. **Lingkungan Eksekusi.** Lingkungan komputasi dikerahkan di atas Android 13 melalui aplikasi emulator terminal *non-root* Termux, dengan kompilasi mandiri `llama.cpp` agar instruksi CPU ARM dapat dieksploitasi secara natif.
3. **Model Uji.** Penelitian menguji dua SLM berbobot ringan, yaitu **LFM 2.5 (1,2 miliar parameter)** sebagai objek uji utama dan **Qwen 3.5 (2 miliar parameter)** sebagai pembanding *stress-test*.
4. **Metode Kompresi.** Fokus PTQ dibatasi pada format GGUF presisi campuran (*k-quants*) yang diturunkan secara gradual melintasi rentang 3-bit hingga 5-bit, yakni **Q3\_K\_M**, **Q4\_K\_M**, dan **Q5\_K\_M**, dengan FP16 sebagai *baseline*.
5. **Metrik Evaluasi.** Metrik dibatasi pada (a) ukuran berkas, (b) *peak* RAM, (c) *Prompt* dan *Generation Speed* dalam TPS, (d) *Perplexity* WikiText-2, serta (e) akurasi MMLU, GSM8K, dan HumanEval, masing-masing dibatasi 100 sampel per *benchmark*.

## 1.8 Hipotesis

Hipotesis utama yang akan dibuktikan keabsahannya pada penelitian ini adalah:

**H1:** Implementasi PTQ format GGUF presisi campuran pada rentang 3-bit hingga 5-bit akan secara progresif mereduksi ukuran berkas dan konsumsi RAM SLM secara drastis, sehingga arsitektur SLM dapat dimuat secara stabil ke dalam RAM 8 GB Android tanpa memicu *Force Close* (OOM Killed). Reduksi *bandwidth* memori ini sekaligus akan meningkatkan *Tokens per Second* (TPS) pada CPU ARM secara berlipat ganda jika dibandingkan baseline FP16. Sebaliknya, kompromi degradasi kualitas yang muncul akibat pemotongan presisi diprediksi bersifat minor pada varian Q5\_K\_M dan Q4\_K\_M (kenaikan *Perplexity* di bawah 1 poin dengan rata-rata penurunan akurasi di bawah 5%), namun akan menjadi signifikan pada varian Q3\_K\_M, khususnya pada dimensi nalar matematis (GSM8K) dan logika pemrograman (HumanEval),sehingga **Q4\_K\_M diperkirakan menjadi titik keseimbangan (*sweet spot*) operasional yang paling optimal** untuk perangkat Android berkapasitas RAM 8 GB.

\newpage

# BAB II LANDASAN TEORI

## 2.1 Tinjauan Pustaka

Bab ini memaparkan konsep-konsep fundamental dan rujukan literatur terkait kecerdasan buatan, model bahasa, keterbatasan perangkat keras, serta teknik optimasi memori komputasi yang menjadi landasan teoritis bagi penelitian ini.

### 2.1.1 *Natural Language Processing* (NLP) dan Pergeseran ke *Edge Computing*

*Natural Language Processing* (NLP) merupakan cabang ilmu kecerdasan buatan yang memungkinkan mesin mengurai, memahami, dan membangkitkan bahasa alami manusia secara kontekstual. Evolusi NLP terus berakselerasi seiring meluasnya implementasi algoritma *Deep Learning*. Salah satu contoh integrasi NLP pada aplikasi riil di ranah industri lokal adalah pengembangan asisten *chatbot* kesehatan interaktif berbasis kecerdasan buatan, yang terbukti meningkatkan efisiensi operasional dan kualitas pelayanan rumah sakit serta menjadi kanal konsultasi *real-time* yang dapat diandalkan oleh masyarakat (Ahmad & Safudin, 2024).

Namun, pengolahan bahasa yang canggih sering menuntut kapabilitas komputasi server *cloud*. Ketergantungan pada komputasi awan menjadi persoalan dalam penanganan kasus yang menuntut kerahasiaan absolut, seperti data diagnosis rekam medis pasien. Sebagai mitigasi risiko keamanan, pengembangan NLP mulai diarahkan pada arsitektur *offline* atau lokalisasi pemrosesan pada perangkat seluler konsumen (*Mobile Edge Computing*). Paradigma *offline* memastikan kelancaran fungsionalitas sistem AI sekaligus menjamin privasi informasi sensitif dari intervensi jaringan internet terbuka (Zhan dkk., 2025).

Untuk memaksimalkan operasi AI di lingkungan gawai berbasis RAM terbatas, pendekatan *Edge Intelligence Optimization* sangat diperlukan. Konsep ini memformulasikan teknik penyesuaian *stack* perangkat lunak agar perangkat Android dengan spesifikasi minim mampu mengeksekusi beban kerja AI tanpa memicu *Force Close* yang diakibatkan oleh keterbatasan arsitektur memori bawaan (Zhang dkk., 2024). Secara hierarkis, ekosistem *Edge Intelligence* terbagi menjadi tiga lapisan: lapisan *cloud* (server pusat untuk pelatihan dan model berskala raksasa), lapisan *edge server* (*gateway* perantara dengan latensi rendah), dan lapisan *edge device* (perangkat akhir seperti *smartphone*); penelitian ini memfokuskan kontribusi pada lapisan paling bawah, yaitu inferensi SLM pada *smartphone* Android.

### 2.1.2 *Large Language Models* (LLM) dan Fleksibilitasnya

*Large Language Models* (LLM) merujuk pada arsitektur *neural network* skala masif yang dilatih menggunakan volume data teks dalam triliunan token. Pendekatan paradigmatik LLM modern, mulai dari *pre-training*, *prompting*, hingga *alignment* dan *inference*,secara komprehensif disusun oleh Xiao dan Zhu (2025) dalam buku ajar *Foundations of Large Language Models*. Sebagai fondasi dasar, LLaMA merupakan salah satu pelopor *open-source foundation language model* berskala besar yang dibangun murni menggunakan dataset publik, dengan kapasitas parameter mulai 7 miliar hingga 65 miliar (Touvron dkk., 2023). Fleksibilitas arsitektur LLM bahkan telah dimanfaatkan sebagai agen kognitif untuk otomatisasi penyusunan jaringan nirkabel di kawasan urban cerdas (Sevim & Ibrahim, 2024), yang menegaskan bahwa model bahasa modern berperan layaknya otak virtual universal.

### 2.1.3 *Small Language Models* (SLM) dan Limitasi Perangkat Seluler

Sebagai respons atas mahalnya ongkos inferensi LLM raksasa, para peneliti berinovasi menciptakan *Small Language Models* (SLM). Arsitektur SLM menyuguhkan desain jaringan parameter yang jauh lebih ramping (umumnya 1–7 miliar parameter) namun sanggup mempertahankan kompetensi analitis yang memadai. Survei komprehensif atas lebih dari 60 SLM oleh Lu dkk. (2025) menunjukkan bahwa SLM *state-of-the-art* dapat mengungguli model 7B pada *task* umum, sehingga viabilitas praktis SLM sebagai pilihan utama *on-device* terbukti secara empiris. Keringkasan arsitektur SLM menjadikannya primadona untuk disematkan langsung ke dalam *smartphone*. Namun tantangan utamanya adalah arsitektur *shared memory*: RAM 8 GB pada Android harus dibagi untuk OS, antarmuka layar, dan aplikasi latar belakang. Apabila SLM dimuat penuh dan ukurannya melebihi ruang yang tersisa, *Out of Memory Killer* akan menghentikan paksa (*Force Close*) proses AI demi menyelamatkan sistem dari *freeze*.

### 2.1.4 Arsitektur Dasar *Transformer*

Di balik kapabilitas LLM maupun SLM terdapat arsitektur *Transformer* dengan mekanisme *Self-Attention* yang memungkinkannya membaca seluruh kata dalam satu kalimat secara simultan, lalu menimbang keterikatan makna antar-token secara kontekstual (Prince, 2023). Kalkulasi bobot atensi antar-token ini melibatkan operasi matriks masif yang dilakukan lapis demi lapis (*layer-by-layer*), sehingga *Transformer* secara bawaan sangat rakus memori dan akan menuntut alokasi gigabyte RAM tambahan seiring dengan panjangnya *prompt* yang diberikan pengguna.

### 2.1.5 Konsep Kuantisasi, Presisi Campuran (*K-Quants*), dan Rentang 3-Bit hingga 5-Bit

Kuantisasi (*Quantization*) adalah algoritma kompresi fundamental yang digunakan untuk merampingkan kebutuhan ruang penyimpanan dan *memory footprint* (Prince, 2023). Saat sebuah model AI dilatih, bobot matriks jaringannya direkam dalam *floating-point* berpresisi tinggi, umumnya 16-bit (FP16). Format murni ini memiliki ketepatan akurasi yang tinggi namun memakan kapasitas RAM secara eksesif. Kuantisasi menyederhanakan rangkaian pecahan desimal ini menjadi bilangan bulat yang lebih padat (INT5, INT4, atau bahkan INT3) (Dettmers dkk., 2023). Pembahasan teknik inferensi LLM yang efisien beserta strategi kuantisasi modern pada tahap pasca-pelatihan dirangkum secara komprehensif oleh Xiao dan Zhu (2025). Selain keluarga PTQ klasik (GPTQ, AWQ, dan GGUF *k-quants*), studi kontemporer juga mengusulkan metode PTQ yang khusus dirancang ramah eksekusi *on-device*, seperti **MobileQuant** dari Samsung AI yang mengoptimasi *weight transformation* dan rentang aktivasi secara *end-to-end* untuk menekan *latency* hingga 20–50% pada perangkat seluler (Tan dkk., 2024).

Di dalam ekosistem `llama.cpp`, teknik kompresi standar pada awalnya memukul rata semua lapisan model menjadi format bit yang sama. Pendekatan ini memiliki kelemahan: rusaknya bobot penting yang menyebabkan AI mudah berhalusinasi. Untuk mengatasi defisit kecerdasan ini, diciptakanlah metode generasi baru bernama **K-Quants** (ditandai huruf "K"). Pendekatan ini menggunakan presisi campuran (*mixed-precision*): bagian tensor yang menentukan logika utama (seperti *output layers*) dipertahankan pada presisi yang lebih aman (misalnya 6-bit), sementara bagian model yang sifatnya pelengkap dan memiliki redundansi tinggi ditekan hingga rentang 3-bit hingga 5-bit. Dalam eksplorasi *resource-constrained edge*, tiga varian *k-quants* yang lazim dievaluasi secara bertahap (*ablation study*) adalah **Q5\_K\_M** (rata-rata mendekati 5-bit), **Q4\_K\_M** (mendekati 4-bit), dan **Q3\_K\_M** (mendekati 3-bit). Pencarian *sweet spot* menjadi krusial: kompresi yang kurang padat (>5-bit) tidak cukup menekan RAM 8 GB, namun kompresi yang terlalu agresif (≤3-bit) berisiko menyebabkan kerusakan kognitif total. Alur transformasi dari FP16 menuju varian Q\*\_K\_M secara teknis sudah dipaparkan oleh Dettmers dkk. (2023) dan Frantar dkk. (2023), serta dianalisis lebih lanjut dalam konteks perangkat seluler oleh Tan dkk. (2024).

### 2.1.6 Karakteristik Inferensi *Mobile*: Limitasi CPU dan *Bandwidth* Memori

Pada arsitektur *System-on-Chip* (SoC) ARM *big.LITTLE*, kecepatan inferensi model AI tunduk pada dua hukum komputasi. Pertama, limitasi *Memory Bandwidth*: inti CPU mungkin sanggup berhitung cepat, namun aliran data parameter SLM kerap memacetkan jalur transfer RAM. Ketika model FP16 dikuantisasi ke 5-bit hingga 3-bit, berkas model menjadi sangat ringan sehingga kemacetan transfer data dari RAM ke CPU ARM terurai. Inilah fondasi argumen mengapa perampingan memori berkorelasi langsung dengan peningkatan *Tokens per Second* (TPS).

### 2.1.7 Format File GGUF (*GPT-Generated Unified Format*)

GGUF adalah format biner komprehensif yang dirancang spesifik untuk membungkus arsitektur *neural network* AI generatif dalam satu berkas tertutup. Diciptakan sebagai evolusi dari GGML, GGUF mampu menampung seluruh parameter identitas model beserta *metadata*-nya. Format ini esensial bagi ekosistem Linux Android (Termux) karena strukturnya dioptimalkan untuk mendistribusikan beban komputasi ke arsitektur CPU dan bersahabat dengan berbagai skema kompresi presisi campuran (*K-Quants*).

### 2.1.8 *Framework* Inferensi `llama.cpp` di Android

Untuk perangkat konsumen ringan, dunia komputasi *Machine Learning* sangat bergantung pada `llama.cpp`. Berbeda dengan *framework* berbasis Python (PyTorch/TensorFlow) yang menuntut adanya *overhead* pustaka besar, `llama.cpp` ditulis dalam C/C++ secara *bare-metal*. Struktur transparan ini memungkinkannya untuk dikompilasi secara manual agar sesuai dengan instruksi CPU ARM pada Android, sehingga gawai dapat menjalankan beban kalkulasi *Transformer* layaknya mesin server (Ray & Pradhan, 2026).

### 2.1.9 Tantangan Gangguan Matematis (*Perturbation*)

Pemotongan presisi bobot dari pecahan desimal berukuran gigabyte menjadi angka bulat yang sempit selalu menyisakan efek negatif. Dalam kajian kuantisasi, dampak simplifikasi numerik ini disebut sebagai *perturbation*. Kendala tersulit adalah keberadaan nilai pencilan (*outliers*) yang tidak terprediksi, nilai-nilai ini rentan tersapu saat sistem membulatkan ke integer 3-bit hingga 5-bit terdekat. Hilangnya tumpuan *outliers* inilah yang sering menumpulkan parameter atensi AI dan menyebabkan model berhalusinasi atau menghasilkan jawaban kosong (Gong dkk., 2024). Oleh karena itu, mengevaluasi titik batas kerusakan kompresi (*degradation*) memegang peranan krusial.

### 2.1.10 Metrik Evaluasi Performa *Edge Computing*

Kelayakan operasional SLM di Android (*Mobile Edge*) dievaluasi melalui rasio efisiensi perangkat keras (Jin dkk., 2024). Dua variabel pengamatan esensial mencakup:

a. ***System Memory Usage*** (Konsumsi RAM Sistem). Indikator primer untuk mengukur jumlah absolut RAM yang termakan model saat dimuat. Variabel ini wajib dijaga pada batas yang aman (idealnya 1–3 GB) agar OS Android tidak memicu *OOM Killer*.
b. ***Tokens per Second*** **(TPS)**. Tolok ukur dinamis untuk mengukur laju pemrosesan *prompt* per detik (*Prompt Processing*) dan laju ekstraksi karakter per detik (*Generation*).

### 2.1.11 Standar Pengujian Kognitif dan Linguistik

Untuk memvalidasi bahwa pengorbanan memori tidak menghasilkan model "tuli atau bisu", diperlukan tes validasi standar:

a. ***Perplexity*** **(PPL)**. Penilaian dasar kelugasan sintaksis. Semakin rendah PPL, semakin rasional dan natural rangkaian kalimat yang dihasilkan model.
b. **MMLU** (*Massive Multitask Language Understanding*). Dataset penguji wawasan intelektual komprehensif (sejarah, sains, hingga sosiologi) untuk melacak defisit memori faktual pasca-kompresi.
c. **GSM8K** (*Grade School Math 8K*). Tes nalar matematika sekolah dasar, digunakan untuk membongkar kerusakan logika kalkulasi akibat pemotongan presisi.
d. **HumanEval**. Pengujian fungsional logika pemrograman (Python) untuk menakar tingkat kerusakan sintaks model.

## 2.2 Penelitian Terkait

Demi menempatkan keaslian gagasan penelitian ini dalam lanskap literatur yang relevan, peneliti merujuk pada konstruksi pemikiran dari berbagai studi pilar sebelumnya yang mengedepankan telaah teknis implementasi AI pada ekosistem memori terbatas.

Trobosan konseptual efisiensi krisis memori diperkenalkan secara revolusioner oleh Dettmers dkk. (2023) melalui mekanisme kompresi **QLoRA**. Studi ini menjustifikasi secara empiris bahwa pemaksaan struktur bobot dari skala besar ke wadah presisi 4-bit (NF4) sanggup mereduksi *footprint* hingga sepertiganya, sembari menghindarkan sistem dari *Out of Memory* tanpa mengebiri utilitas 16-bit asli arsitektur dasar. Argumen efisiensi ini dikukuhkan oleh GPTQ (Frantar dkk., 2023) dan AWQ (Lin dkk., 2023), yang membuktikan bahwa PTQ dengan fokus pada perlindungan *salient weights* sangat cocok dan stabil bila dibebankan pada SoC seluler.

Akan tetapi, di balik efisiensi memori tersebut terdapat jejak reduksi kualitas kognitif. Studi ekstensif Gong dkk. (2024) dengan lensa *perturbation* membedah kenyataan bahwa simplifikasi paksa bobot menjadi integer terkompresi sering kali membantai *outliers*, menginduksi rusaknya pemahaman linguistik AI (ditandai memburuknya *Perplexity*).

Terlepas dari risiko cacat penalaran, urgensi lokalisasi AI generatif di perangkat mandiri makin tak terbendung. Hal ini dipantik oleh kerentanan latensi dan *bandwidth* komputasi awan di kawasan urban (Sevim & Ibrahim, 2024). Melalui tinjauan medis, Zhan dkk. (2025) menegaskan bahwa instansi yang berhubungan dengan kerahasiaan data tidak boleh menyerahkan pemrosesan teks ke layanan *Cloud API*. Kebutuhan asisten cerdas instan, seperti *chatbot* RS Brawijaya (Ahmad & Safudin, 2024), merupakan manifestasi valid akan urgensi AI lokal.

Demi menstrukturkan matriks pengujian SLM secara objektif, penulis merujuk pada metodologi evaluasi gubahan Jin dkk. (Jin dkk., 2024) dan arsitektur pengujian latensi dari Zhang dkk. (Zhang dkk., 2024). Kedua referensi tersebut menegaskan bahwa kualitas LLM tidak cukup dinilai dari rasio kebenaran, melainkan harus dipadukan dengan skor *Perplexity* dan TPS. Sebagai klimaks landasan studi terapan, riset observasional Ray dan Pradhan (Ray & Pradhan, 2026) digunakan sebagai pijakan validasi: pengujian PTQ GGUF di atas C++ (`llama.cpp`) pada Raspberry Pi RAM 8 GB membuktikan TPS yang stabil. Tesis empiris ini dipadukan dengan keunggulan arsitektur model lokal seperti Qwen (Nurohim dkk., 2025) dan LLaMA (Touvron dkk., 2023), yang menjadi konfirmasi bahwa komputasi AI *offline* di atas Android dengan RAM setara merupakan keniscayaan terapan yang krusial untuk dieksplorasi.

Pemaparan ringkas tujuh penelitian pilar paling representatif yang mendasari riset ini disajikan pada Tabel II.1.

| Penulis & Judul Penelitian | Tujuan Penelitian | Metode Penelitian | Hasil Penelitian |
|---|---|---|---|
| Dettmers dkk. (2023), *QLoRA: Efficient Finetuning of Quantized LLMs* | Mengembangkan teknik *fine-tuning* hemat memori bagi LLM agar dapat dilatih pada satu GPU melalui kompresi presisi rendah. | Kompresi bobot ke presisi 4-bit (*NormalFloat-4*), *double quantization*, dan *paged optimizer* untuk LoRA. | Pemadatan 4-bit (NF4) terbukti mencegah *Out-of-Memory* dan mempertahankan akurasi setara FP16 pada *benchmark* pasca-*finetuning*. |
| Frantar dkk. (2023), *GPTQ: Accurate Post-Training Quantization for Generative Pre-Trained Transformers* | Mengusulkan metode PTQ *one-shot* yang akurat untuk model generatif berskala besar. | Pendekatan *layer-wise weight quantization* berbasis pendekatan *second-order* (*OBQ*) yang diadaptasi untuk LLM. | GPTQ berhasil mengompresi LLM hingga 3–4-bit dengan degradasi *perplexity* minim dan menjadi salah satu fondasi PTQ untuk LLM. |
| Lin dkk. (2023), *AWQ: Activation-Aware Weight Quantization for On-Device LLM Compression and Acceleration* | Menyusun metode kuantisasi PTQ yang ramah implementasi *on-device* dengan perlindungan terhadap bobot kritis. | Identifikasi 1% bobot paling penting berdasarkan distribusi aktivasi, lalu menerapkan *per-channel scaling* untuk mempertahankannya. | Perlindungan *salient weights* secara drastis menurunkan *error* kuantisasi dan menjadi rujukan utama PTQ untuk inferensi *on-device*. |
| Jin dkk. (2024), *A Comprehensive Evaluation of Quantization Strategies for Large Language Models* | Menyusun kerangka evaluasi holistik untuk membandingkan berbagai strategi kuantisasi pada LLM. | Evaluasi tiga dimensi (kapasitas, kelugasan, dan efisiensi) terhadap beragam metode kuantisasi pada banyak model LLM. | Menetapkan kombinasi *Perplexity* dan beban RAM sebagai standar pengukuran kelayakan kuantisasi; kerangka tiga dimensi inilah yang diadopsi sebagai metodologi skripsi. |
| Ray & Pradhan (2026), *Performance Analysis of Localised Large Language Models in Resource-Constrained Edge for Python and Rust APIs* | Mengevaluasi kelayakan eksekusi LLM terlokalisasi pada perangkat *edge* dengan sumber daya terbatas. | Eksperimen empiris LLM format GGUF melalui `llama.cpp` pada Raspberry Pi RAM 8 GB. | LLM GGUF dapat dieksekusi stabil pada arsitektur ARM 8 GB; menjadi landasan utama replikasi pada SoC ARM Android (Termux) di skripsi ini. |
| Laskaridis dkk. (2024), *MELTing point: Mobile Evaluation of Language Transformers* | Mengevaluasi kelayakan dan keterbatasan eksekusi LLM pada *smartphone* Android dan iOS secara sistematis. | Studi empiris pertama yang membandingkan beberapa LLM (1–13B) pada perangkat seluler nyata dengan metrik *throughput*, RAM, dan *thermal*. | Mengonfirmasi inferensi LLM bersifat *memory-bound* pada *smartphone*; kuantisasi efektif menekan jejak memori dengan kompensasi akurasi. Acuan utama klaim *memory-bound* di skripsi. |
| Lu dkk. (2025), *Demystifying Small Language Models for Edge Deployment* | Memetakan lanskap SLM yang layak diimplementasikan pada perangkat *edge* termasuk *smartphone*. | Survei komprehensif >60 SLM mencakup arsitektur, ukuran, *benchmark* akurasi, dan profil inferensi pada perangkat *edge*. | SLM *state-of-the-art* terbukti dapat mengungguli model 7B pada *task* umum; memperkuat justifikasi pemilihan LFM 2.5 (1,2B) dan Qwen 3.5 (2B) untuk skripsi. |

: Tabel II.1 Matriks Perbandingan Penelitian Terkait (*State of the Art*)

## 2.3 Tinjauan Objek Penelitian

Karena penelitian ini bersifat **eksperimental berbasis laboratorium** dan tidak terikat pada organisasi atau institusi eksternal sebagai tempat riset, sub-bab ini difokuskan pada deskripsi **objek penelitian** — yakni satuan analisis (*unit of analysis*) yang menjadi sasaran pengukuran dalam eksperimen kuantisasi *on-device*. Seluruh kegiatan pengujian, mulai dari persiapan berkas model hingga eksekusi *benchmark*, dilakukan secara mandiri oleh penulis menggunakan perangkat pribadi. Objek penelitian dibagi menjadi dua kategori fundamental yang saling berkomplemen: (1) **ekosistem perangkat keras dan perangkat lunak Android** yang berperan sebagai *host target deployment*, dan (2) **arsitektur *Small Language Model*** yang menjadi objek uji kompresi PTQ. Pembagian dua kategori ini memungkinkan analisis trade-off antara dimensi efisiensi *hardware* (RAM, CPU, TPS) dan dimensi kognitif *software* (*perplexity*, akurasi *benchmark*) sebagaimana dianjurkan oleh kerangka evaluasi tiga dimensi Jin dkk. (2024).

### 2.3.1 Ekosistem Uji Keras: Tecno Pova 5 dengan Termux

Objek operasional dibatasi pada satu *smartphone* kelas reguler, yaitu Tecno Pova 5. Perangkat ini ditenagai SoC MediaTek Helio G99 berbasis ARM, dengan RAM sistem 8 GB. Mengingat status gawai *non-rooted* (bawaan pabrik tanpa akses *root*), lingkungan pengujian virtual dibangun di atas aplikasi emulator Linux portabel **Termux**. Melalui kompilasi mandiri di Termux inilah `llama.cpp` di-*build* ulang dalam konfigurasi C/C++ serupa lingkungan server, agar instruksi CPU ARM dapat dieksekusi secara optimal.

### 2.3.2 Objek Arsitektur SLM: LFM 2.5 (1,2B) dan Qwen 3.5 (2B)

Riset komparatif ini menggunakan dua model SLM. Objek uji utama adalah **LFM 2.5** dengan densitas parameter 1,2 miliar. Berdasarkan laporan teknis resmi Liquid AI (2025), arsitektur LFM 2 dirancang sebagai *hybrid backbone* yang memadukan *gated short convolutions* dengan *grouped query attention* dan secara eksplisit dioptimalkan untuk *edge inference* dengan kecepatan *prefill/decode* hingga 2× lebih tinggi dibanding model setara di CPU. Struktur mikronya yang dirancang efisien menjadikannya kandidat menjanjikan untuk dikompresi bertahap pada rentang 3-bit hingga 5-bit guna menekan konsumsi RAM. Versi mentah FP16-nya akan dibandingkan dengan tiga varian *K-Quants* (Q5\_K\_M, Q4\_K\_M, dan Q3\_K\_M) pada fase *ablation study*. Sebagai pembanding *stress-test*, digunakan arsitektur **Qwen 3.5 (2 miliar parameter)**,keluarga Qwen3 secara eksplisit memperkenalkan **dua mode di satu model**, yaitu *thinking mode* untuk *multi-step reasoning* dan *non-thinking mode* untuk respons cepat (Qwen Team, 2025). Pilihan ini berfungsi sebagai instrumen pengukur batas toleransi ekstrem sistem, sekaligus mendemonstrasikan fenomena *scaling laws* (kemampuan model bertahan) ketika ekosistem Android RAM 8 GB dan Helio G99 dipaksa menjalankan beban arsitektur di atas 2 miliar parameter pasca-kuantisasi.

\newpage

# BAB III METODOLOGI PENELITIAN

## 3.1 Tahapan Penelitian

Penelitian ini berbentuk eksperimen komputasional pada perangkat seluler. Agar setiap pengujian tetap fokus dan menghasilkan data yang valid, alur kerja disusun secara berurutan mengikuti kerangka evaluasi kuantisasi tiga dimensi (kapasitas, kelugasan, efisiensi) yang dipaparkan oleh Jin dkk. (2024). Pelaksanaan penelitian dibagi ke dalam lima tahapan utama yang diuraikan pada sub-bab 3.1.1 hingga 3.1.5.

### 3.1.1 Studi Pendahuluan dan Perumusan Masalah

Tahap awal berfokus pada pemetaan literatur terkini terkait *Mobile Edge Computing* (Zhang dkk., 2024; Sevim & Ibrahim, 2024), *Post-Training Quantization* (Dettmers dkk., 2023; Frantar dkk., 2023), serta urgensi pemrosesan AI secara *offline* untuk menjamin privasi pengguna (Zhan dkk., 2025). Hasil studi pustaka tersebut menjadi landasan perumusan hipotesis bahwa kompresi presisi campuran berformat GGUF mampu menjadi solusi terhadap *bottleneck* RAM 8 GB pada perangkat Android kelas menengah (Lin dkk., 2023).

### 3.1.2 Persiapan Lingkungan Komputasi

*Testbed* dikonfigurasi pada dua *host* yang saling melengkapi. *Host* pertama adalah PC ber-WSL2 Ubuntu dengan akselerator NVIDIA RTX 3060 yang berfungsi untuk persiapan berkas model dan evaluasi akurasi; pada *host* ini dipasang *toolchain* `build-essential`, `cmake`, `python3`, `python3-venv`, CUDA Toolkit, dan *library* `huggingface_hub`. Repositori `llama.cpp` di-*clone* lalu dikompilasi dengan opsi `-DGGML_CUDA=ON` agar utilitas `llama-quantize` dan `llama-perplexity` dapat memanfaatkan GPU.

*Host* kedua adalah perangkat Android Tecno Pova 5 yang dijalankan melalui emulator terminal *non-root* Termux dan berperan sebagai lingkungan pengukuran performa pada *target deployment*. Paket dasar Termux di-*update* (`pkg update`), kemudian *toolchain* C++ (`clang`, `cmake`, `make`) dipasang agar `llama.cpp` dapat dikompilasi natif untuk arsitektur ARM (Ray & Pradhan, 2026). Skrip persiapan lingkungan PC tersedia pada `docs/scripts/quantize_pc.sh` (Lampiran B).

### 3.1.3 Persiapan Objek Model dan Kuantisasi

Berkas resmi LFM 2.5 (1,2 miliar parameter) dan Qwen 3.5 (2 miliar parameter) diunduh dari HuggingFace ke PC melalui `huggingface-cli` (Touvron dkk., 2023). Qwen dipilih sebagai uji kedua karena kompetensi Bahasa Indonesia-nya telah terbukti pada studi sebelumnya (Nurohim dkk., 2025). Berkas mentah `.safetensors` kemudian dikonversi ke `F16.gguf` melalui skrip `convert_hf_to_gguf.py`.

Untuk mengeksekusi *ablation* gradasi kompresi, berkas `F16.gguf` di-kuantisasi memakai utilitas `./llama-quantize` pada PC sehingga menghasilkan tiga varian *k-quants*, yaitu **Q5\_K\_M.gguf**, **Q4\_K\_M.gguf**, dan **Q3\_K\_M.gguf** (Dettmers dkk., 2023). Keempat varian per model (F16 ditambah tiga *k-quants*) selanjutnya ditransfer ke direktori `/storage/emulated/0/Download/SLM` pada Tecno Pova 5 sebagai objek uji yang seragam.

### 3.1.4 Eksekusi Eksperimen (*System Benchmarking*)

Pengujian beban kerja dilaksanakan pada dua *host* sesuai pembagian metrik. Pada PC NVIDIA RTX 3060 dieksekusi pengukuran *Perplexity* melalui `./llama-perplexity` dengan dataset WikiText-2 (Gong dkk., 2024) serta evaluasi akurasi MMLU, GSM8K, HumanEval, dan MT-Bench melalui skrip Python kustom. Pada Tecno Pova 5 melalui Termux diukur *peak* RAM proses (`VmRSS` dari `/proc/<pid>/status`), beban CPU (`%CPU` dari `ps`), serta TPS *Prompt* dan *Generation* melalui skrip otomatisasi `benchmark.sh` yang tercantum pada Lampiran A.

Konfigurasi inferensi dibuat seragam dengan parameter `--temp 0,35`, `--top-p 0,9`, `--min-p 0,05`, `--repeat-penalty 1,1`, anggaran token `-n 1024`, ukuran konteks `-c 2048`, dan alokasi enam *threads* (Zhang dkk., 2024). Eksekusi berlangsung berurutan dari FP16 sebagai variabel kontrol, dilanjutkan Q5\_K\_M, Q4\_K\_M, dan Q3\_K\_M, dengan jeda *cooldown* manual 3–5 menit antar model guna mencegah *thermal throttling*.

### 3.1.5 Analisis Komparatif dan Penarikan Kesimpulan

Data mentah dari Termux diekstraksi ke dalam matriks tabular. Dimensi efisiensi *hardware* (RAM dan TPS) dan dimensi kognitif *software* (PPL dan akurasi *benchmark*) lalu dikomparasikan dengan kerangka evaluasi tiga dimensi Jin dkk. (2024) untuk mengidentifikasi titik *sweet spot* operasional. Alur lima tahap di atas — *literature survey* → *environment setup* → *quantization* → *on-device benchmarking* → *analysis* — sejajar dengan kerangka *workflow* evaluasi PTQ pada *edge device* yang dipaparkan oleh Jin dkk. (2024) dan Murthy dkk. (2024). Pemetaan eksplisit antara tahap penelitian ini dengan enam langkah *workflow* MobileAIBench (Murthy dkk., 2024) disajikan pada Tabel III.0, sedangkan ilustrasi *workflow*-nya diadaptasi pada Gambar III.1.

| Langkah MobileAIBench (Murthy dkk., 2024) | Tahap penelitian ini |
|---|---|
| Step 1–2 — *Task/Dataset Identification* + *Data Preprocess/Loading* | Tahap 1 (Studi Pendahuluan) |
| Step 3 — *Model Loading / Inference* | Tahap 3 (Persiapan Objek Model) |
| Step 4 — *Inference Collection* | Tahap 4 (Eksekusi Eksperimen) |
| Step 5–6 — *Evaluation + Results Summarization* | Tahap 5 (Analisis Komparatif) |

: Tabel III.0 Pemetaan Langkah *Workflow* MobileAIBench (Murthy dkk., 2024) terhadap Lima Tahap Penelitian

![Gambar III.1 Arsitektur *workflow benchmarking* SLM/LLM *on-device* (enam langkah: identifikasi *task*/*dataset*, *preprocess*/loading, *model loading*/inferensi, koleksi hasil inferensi, evaluasi, dan ringkasan hasil). Sumber: Murthy dkk. (2024), Gambar 1 dalam *MobileAIBench: Benchmarking LLMs and LMMs for On-Device Use Cases*, arXiv:2406.10290.](gambar/3_1_mobileaibench_arsitektur.png){width=92%}

## 3.2 Instrumen Penelitian

Penelitian ini menitikberatkan pada evaluasi kinerja infrastruktur ujung dengan sumber daya terbatas (*resource-constrained edge*) (Ray & Pradhan, 2026). Instrumen yang digunakan terdiri atas dua himpunan perangkat keras (PC sebagai *host* persiapan model dan evaluasi akurasi, serta *smartphone* sebagai *host target deployment*) dan ekosistem perangkat lunak *open-source* berkinerja tinggi, sebagaimana dirinci pada Tabel III.1 dan Tabel III.2.

| Peran | Komponen | Spesifikasi | Keterangan |
|---|---|---|---|
| Host persiapan & evaluasi akurasi | PC + GPU | NVIDIA RTX 3060 (WSL2 Ubuntu) | Eksekusi kuantisasi (`llama-quantize`), evaluasi *Perplexity*, dan akurasi MMLU/GSM8K/HumanEval/MT-Bench. |
| *Host target* deployment | Perangkat | Tecno Pova 5 | *Smartphone* kelas menengah. |
| *Host target* deployment | SoC | MediaTek Helio G99 (ARM *big.LITTLE*) | CPU-*bound inference*. |
| *Host target* deployment | Memori Utama (RAM) | 8 GB LPDDR4x | *Shared-memory* dengan Host OS, alat ukur sekaligus *bottleneck Force Close* (Zhang dkk., 2024). |
| *Host target* deployment | Penyimpanan Internal | UFS 2.2 256 GB | Menampung seluruh variasi berkas `.gguf`. |

: Tabel III.1 Spesifikasi Perangkat Keras (*Hardware*)

| Peran | Komponen | Versi/Tooling | Keterangan |
|---|---|---|---|
| PC persiapan | Sistem Operasi | Windows 11 + WSL2 Ubuntu | Lingkungan persiapan berkas `.gguf` dan eksekusi evaluasi akurasi. |
| PC persiapan | Akselerator | CUDA Toolkit + NVIDIA RTX 3060 | Mempercepat `llama-quantize` dan `llama-perplexity`. |
| PC persiapan | Akuisisi model | `huggingface_hub` | Mengunduh bobot resmi (`.safetensors`) dari HuggingFace. |
| PC persiapan | Konversi & kuantisasi | `convert_hf_to_gguf.py`, `./llama-quantize` | Konversi ke `F16.gguf` lalu kuantisasi ke Q3/Q4/Q5\_K\_M (Dettmers dkk., 2023). |
| PC persiapan | Evaluasi Kognitif | `./llama-perplexity` | Mengkalkulasi degradasi linguistik (PPL) pada dataset WikiText-2 (Gong dkk., 2024). |
| PC persiapan | Evaluasi Akurasi | Skrip Python kustom (MMLU, GSM8K, HumanEval, MT-Bench) | Menjalankan 100 sampel acak per *benchmark*. |
| Android *target* | Sistem Operasi Dasar | Android 13 | Lapisan manajemen memori inti (*Host OS*). |
| Android *target* | Lingkungan Simulasi Terminal | Termux *non-root* | Menyediakan fondasi paket Linux murni tanpa membuka enkripsi partisi sistem. |
| Android *target* | Mesin Inferensi | `llama.cpp` (C/C++ *bare-metal*, ARM-native) | Dikompilasi natif untuk instruksi CPU ARM (Ray & Pradhan, 2026). |
| Android *target* | Skrip Otomatisasi | `benchmark.sh` v4 (Lampiran A) | Menjalankan inferensi, memantau `VmRSS` + `%CPU`, dan mencatat TPS ke CSV. |

: Tabel III.2 Spesifikasi Perangkat Lunak (*Software*)

## 3.3 Metode Pengumpulan Data

Penelitian ini bersifat kuantitatif eksperimental dan mengandalkan data yang dapat di-*log* secara otomatis oleh sistem (*System Logging Benchmarking*). Karena seluruh variabel dependen berbentuk metrik komputasional, teknik wawancara tidak digunakan. Pengumpulan data dilakukan melalui dua teknik utama, yaitu pengamatan langsung dan studi pustaka yang dijelaskan pada sub-bab 3.3.1 dan 3.3.2.

### 3.3.1 Pengamatan Langsung (Observasi Eksperimental)

Observasi dijalankan melalui *system benchmarking logging* yang merekam indikator performa *hardware* dan *software* secara periodik selama proses inferensi berlangsung. Pencatatan dipisahkan berdasarkan *host*. Pada *host* PC NVIDIA RTX 3060, peneliti mencatat nilai *Perplexity* WikiText-2 dari keluaran `./llama-perplexity` serta skor akurasi MMLU, GSM8K, HumanEval, dan MT-Bench dari skrip Python kustom. Pada *host* Tecno Pova 5 yang diakses melalui Termux, dicatat konsumsi RAM proses (`VmRSS` dari `/proc/<pid>/status`), beban CPU (`%CPU` dari `ps`), serta TPS *Prompt* dan *Generation* yang direkam oleh *resource monitor* di dalam skrip `benchmark.sh` (Lampiran A).

Pencatatan dilakukan pada setiap transisi presisi mulai dari FP16, Q5\_K\_M, Q4\_K\_M, hingga Q3\_K\_M, sehingga data lintas-*host* dapat dipasangkan untuk menemukan kombinasi optimal antara retensi kepintaran (PC) dan efisiensi *runtime* (Android) sebagaimana kerangka evaluasi multi-dimensi pada literatur acuan (Jin dkk., 2024; Zhang dkk., 2024).

### 3.3.2 Studi Pustaka

Data sekunder dihimpun dari jurnal akademik mutakhir periode 2023–2026 yang memayungi empat klaster konsep utama. Klaster pertama berfokus pada *Post-Training Quantization* (Dettmers dkk., 2023; Frantar dkk., 2023). Klaster kedua mencakup arsitektur model bahasa terbuka dan kompresi berbasis aktivasi (Touvron dkk., 2023; Lin dkk., 2023). Klaster ketiga membahas *Mobile Edge Computing* (Zhang dkk., 2024; Sevim & Ibrahim, 2024), dan klaster keempat menelaah urgensi lokalisasi pemrosesan AI yang mencakup aspek privasi (Zhan dkk., 2025) dan kebutuhan respons cerdas yang instan pada layanan publik (Ahmad & Safudin, 2024).

Studi kepustakaan ini menjadi landasan dalam penentuan parameter kalibrasi pengujian, sehingga skenario *stress-test* yang diterapkan sejalan dengan standar evaluasi performa AI pada perangkat dengan sumber daya terbatas (Ray & Pradhan, 2026).

## 3.4 Metode Analisis Data

Data metrik mentah (*raw data log*) yang diekstraksi dari perangkat uji diolah menggunakan **Analisis Komparatif Bertingkat (*Ablation Study*)**. Metode ini mengkaji selisih kinerja (*performance gap*) antara model presisi murni FP16 sebagai *baseline* dengan tiga level kompresi di bawahnya, yaitu Q5\_K\_M, Q4\_K\_M, dan Q3\_K\_M (Dettmers dkk., 2023; Frantar dkk., 2023). Sesuai dengan kerangka evaluasi tiga dimensi (*Three-Dimensional Evaluation Framework*) Jin dkk. (2024), data diolah ke dalam dua matriks kalkulasi turunan yang dirinci pada sub-bab 3.4.1 dan 3.4.2.

### 3.4.1 Analisis Efisiensi Perangkat Keras (Infrastruktur)

Data *peak* RAM diolah ke dalam persentase efisiensi guna mengevaluasi keamanan sistem operasi terhadap risiko *Force Close* (Zhang dkk., 2024). Formula reduksi memori yang digunakan adalah

$$
\text{Reduksi Memori (\%)} = \frac{\text{RAM}_{\text{FP16}} - \text{RAM}_{\text{Kuantisasi}}}{\text{RAM}_{\text{FP16}}} \times 100\%.
$$

Bagi varian yang FP16-nya gagal dimuat akibat OOM, data dicatat sebagai *hardware limit*. Selain itu, data waktu pemrosesan dikonversi menjadi TPS (total token dibagi durasi eksekusi dalam detik) untuk merepresentasikan *throughput* perangkat.

### 3.4.2 Analisis Fluktuasi Degradasi Kognitif

Data pergeseran kualitas linguistik yang terekam melalui skor *Perplexity* dianalisis berdasarkan margin pelebarannya terhadap *baseline* (Gong dkk., 2024). PPL bersifat *inverse*: semakin tinggi nilai PPL pasca-kompresi dibanding *baseline*, semakin parah degradasi pemahaman model akibat hilangnya *outliers* pada matriks bobot (Gong dkk., 2024). Risiko ini perlu dimitigasi melalui pendekatan kompresi berbasis proteksi bobot *salient* (Lin dkk., 2023).

Data akhir dari matriks efisiensi (RAM dan TPS) selanjutnya dikorelasikan secara grafis dengan matriks kognitif (PPL dan akurasi *benchmark*). Pemilihan metrik *peak* RAM, *prompt/generation speed*, dan total waktu eksekusi sebagai instrumen utama konsisten dengan kerangka *MobileAIBench* yang dirancang khusus untuk *benchmarking* LLM dan LMM pada perangkat *on-device* (Murthy dkk., 2024). Melalui analisis kuantitatif ini, peneliti menetapkan titik *Sweet Spot*, yaitu varian *k-quants* yang menunjukkan rasionalitas paling tinggi untuk diimplementasikan pada *smartphone* Android berkapasitas RAM 8 GB (Jin dkk., 2024; Ray & Pradhan, 2026).

\newpage

# BAB IV HASIL PENELITIAN DAN PEMBAHASAN

## 4.1 Lingkungan Pengujian dan Skenario

Bab ini menguraikan data hasil pengujian (*benchmarking*) yang diperoleh melalui eksekusi model AI sesuai skenario yang telah ditetapkan. Penelitian ini menerapkan metode **Host-to-Target Deployment**: fase kompresi bobot arsitektur melalui PTQ dilakukan pada mesin *host* berspesifikasi tinggi (PC dengan GPU NVIDIA RTX 3060) guna mengoptimalkan kecepatan kalkulasi *K-Quants*. Berkas hasil kompresi dalam format `.gguf` selanjutnya dipindahkan ke unit *Target Edge Device*, yaitu *smartphone* Android Tecno Pova 5 (SoC MediaTek Helio G99, RAM 8 GB), untuk dieksekusi secara lokal melalui `llama.cpp` pada terminal Termux.

Instrumen komparasi silang (*cross-validation*) menggunakan dua varian SLM, yaitu LFM 2.5 berukuran 1,2 miliar parameter sebagai representasi arsitektur ultra-ringan dan Qwen 3.5 berukuran 2 miliar parameter sebagai instrumen uji beban memori (*stress-test*). Evaluasi dilakukan secara bertingkat dengan membandingkan versi FP16 sebagai variabel kontrol terhadap tiga varian kuantisasi, yakni Q5\_K\_M, Q4\_K\_M, dan Q3\_K\_M.

## 4.2 Hasil Uji Efisiensi Infrastruktur (*Hardware*)

Pengujian efisiensi infrastruktur ditujukan untuk mengidentifikasi dampak kuantisasi terhadap reduksi kapasitas penyimpanan fisik (*storage*), alokasi memori sistem Android (RAM), serta akselerasi kinerja prosesor (TPS).

### 4.2.1 Reduksi Kapasitas Penyimpanan Fisik (*Storage*)

Tahap observasi awal berfokus pada pengukuran ukuran aktual berkas model pada penyimpanan internal gawai. Data komparasi ukuran fisik dan persentase reduksinya disajikan pada Tabel IV.1.

| Model Arsitektur | Presisi / Format | Ukuran Berkas | Persentase Reduksi |
|---|:---:|:---:|:---:|
| LFM 2.5 (1,2B) | F16 (Original) | 2,2 GB | - |
| LFM 2.5 (1,2B) | Q5\_K\_M | 805 MB | ↓ 63,41% |
| LFM 2.5 (1,2B) | Q4\_K\_M | 698 MB | ↓ 68,27% |
| LFM 2.5 (1,2B) | Q3\_K\_M | 573 MB | ↓ 73,95% |
| Qwen 3.5 (2B) | F16 (Original) | 3,6 GB | - |
| Qwen 3.5 (2B) | Q5\_K\_M | 1,4 GB | ↓ 61,11% |
| Qwen 3.5 (2B) | Q4\_K\_M | 1,2 GB | ↓ 66,67% |
| Qwen 3.5 (2B) | Q3\_K\_M | 1,1 GB | ↓ 69,44% |

: Tabel IV.1 Reduksi Ukuran Berkas Model per Varian Kuantisasi

![Gambar IV.1 Reduksi ukuran berkas model per varian kuantisasi. Sumber: olahan penulis.](gambar/4_1_ukuran_berkas.png){width=92%}

Berdasarkan Tabel IV.1, implementasi kuantisasi mampu mereduksi ukuran berkas model secara signifikan melampaui 60%. Pada varian Q3\_K\_M, ukuran LFM 2.5 berhasil ditekan hingga 573 MB, sementara Qwen 3.5 menyusut menjadi 1,1 GB, sehingga memberikan ketersediaan ruang penyimpanan ROM yang lebih besar pada perangkat.

### 4.2.2 Konsumsi RAM dan Kecepatan Inferensi (Helio G99)

Performa komputasi diuji secara langsung pada Tecno Pova 5 melalui skrip `benchmark.sh` (Lampiran A) di Termux. Setiap varian model diuji **tiga kali** dengan jeda *cooldown* manual 3–5 menit antar model untuk mencegah *thermal throttling*.

Metrik dikumpulkan dari dua sumber: (i) *Prompt Speed* dan *Generation Speed* diekstrak dari ringkasan statistik `llama-cli`, dan (ii) konsumsi RAM proses (`VmRSS`) serta beban CPU dipantau setiap 0,5 detik dari `/proc/<pid>/status` (konfigurasi 6 *threads*). Hasil agregat rerata dari tiga ulangan disajikan pada Tabel IV.2.

| Model (Format) | N | Total Waktu (s) | Prompt Speed (t/s) | Gen Speed (t/s) | Peak RAM Proses (MB) | CPU Peak (%) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| LFM 2.5 (F16) | 3 | 16,00 | 33,47 | 5,57 | 2.303,47 | 292,33 |
| LFM 2.5 (Q5\_K\_M) | 3 | 10,67 | 35,33 | 10,63 | 1.665,28 | 357,33 |
| LFM 2.5 (Q4\_K\_M) | 3 | 7,33 | 43,67 | 13,67 | 1.452,97 | 299,33 |
| LFM 2.5 (Q3\_K\_M) | 3 | 14,33 | 18,27 | 11,07 | 911,97 | 464,00 |
| Qwen 3.5 (F16) | 3 | 310,33 | 22,70 | 1,87 | 3.744,25 | 430,33 |
| Qwen 3.5 (Q5\_K\_M) | 3 | 181,00 | 22,55 | 4,60 | 2.856,29 | 509,00 |
| Qwen 3.5 (Q4\_K\_M) | 3 | 297,00 | 27,00 | 4,95 | 2.562,88 | 500,50 |
| Qwen 3.5 (Q3\_K\_M) | 3 | 187,00 | 14,55 | 4,25 | 1.897,97 | 525,00 |

: Tabel IV.2 Performa Inferensi (Total Waktu, *Prompt Speed*, *Generation Speed*, *Peak* RAM proses, dan CPU *Peak*) -- rerata dari tiga ulangan

Kolom N pada Tabel IV.2 menunjukkan jumlah replikasi pengujian untuk setiap varian, yaitu tiga kali untuk seluruh varian LFM 2.5 maupun Qwen 3.5. Kolom CPU *Peak* (%) merepresentasikan beban gabungan terhadap enam *thread* yang dialokasikan (skala maksimum teoretis 600%, diukur menggunakan metrik `%CPU` dari `ps`).

![Gambar IV.2 Konsumsi *Peak* RAM proses per varian kuantisasi pada Helio G99 (RAM 8 GB). Sumber: olahan penulis.](gambar/4_3_konsumsi_ram.png){width=92%}

![Gambar IV.3 Kecepatan inferensi (*Prompt* vs *Generation*) per varian kuantisasi. Sumber: olahan penulis.](gambar/4_2_kecepatan_inferensi.png){width=98%}

Tabel IV.2 memperlihatkan tiga pola utama. Pertama, reduksi RAM konsisten pada kedua model: Qwen 3.5 FP16 menyerap 3,74 GB RAM proses atau setara 47% RAM sistem 8 GB dan rawan memicu *OOM Killer*, sedangkan kuantisasi menurunkannya menjadi 2,56 GB pada Q4\_K\_M (efisiensi 31,6%) dan 1,90 GB pada Q3\_K\_M (efisiensi 49,3%). Kedua, akselerasi *Generation Speed* dominan pada LFM 2.5: varian Q4\_K\_M melonjak ke 13,67 t/s atau 2,45 kali lipat *baseline* FP16 (5,57 t/s), sekaligus mencatat total waktu eksekusi tercepat (7,33 detik) dengan CPU *peak* yang terkontrol di kisaran 299%. Ketiga, Qwen 3.5 jenuh di rentang 1,87–4,95 t/s, profil yang mencerminkan keterbatasan model *reasoning* berukuran dua miliar parameter pada CPU ARM kelas menengah ke bawah (analisis tambahan dipaparkan pada Sub-bab 4.3.3).

## 4.3 Hasil Uji Degradasi Kognitif (*Software* / AI)

Evaluasi kognitif bertujuan mengukur dampak kompresi terhadap kecerdasan *neural network* model menggunakan metrik *Perplexity* serta serangkaian uji pemahaman akademik.

### 4.3.1 Evaluasi *Perplexity* (PPL)

*Perplexity* digunakan untuk mengukur tingkat ambiguitas model terhadap struktur sintaksis pada dataset WikiText-2. Nilai PPL yang lebih rendah mengindikasikan tingkat pemahaman bahasa yang lebih baik. Hasilnya ditunjukkan pada Tabel IV.3.

| Varian Kompresi | PPL LFM 2.5 (1,2B) | PPL Qwen 3.5 (2B) |
|---|:---:|:---:|
| F16 (*baseline*) | 12,6829 | 12,7763 |
| Q5\_K\_M | 12,8297 | 13,0856 |
| Q4\_K\_M | 13,2145 | 13,3617 |
| Q3\_K\_M | 14,5135 | 15,2172 |

: Tabel IV.3 Hasil *Perplexity* (PPL) WikiText-2 per Varian Kuantisasi \*

\* Evaluasi PPL dieksekusi pada *host* PC dengan GPU NVIDIA RTX 3060 menggunakan dataset *holdout* `wikitext-2-raw` (subset `wiki.test.raw`) melalui perintah `./llama-perplexity -m <model.gguf> -f wikitext-2-raw/wiki.test.raw -c 512 -ngl 999`. Penggunaan GPU diperlukan agar evaluasi PPL pada keseluruhan korpus selesai dalam waktu wajar; nilai PPL bersifat *model-intrinsic* dan independen terhadap perangkat keras inferensi karena format berkas `.gguf` yang identik dengan yang digunakan pada perangkat Tecno Pova 5.

![Gambar IV.4 Degradasi *Perplexity* pada dataset WikiText-2. Sumber: olahan penulis.](gambar/4_4_perplexity.png){width=92%}

### 4.3.2 Evaluasi Akurasi Logika (MMLU, GSM8K, dan HumanEval) serta Kreativitas Bahasa (MT-Bench TTR)

Evaluasi akurasi menggunakan tiga instrumen *benchmark* kognitif: MMLU (pemahaman umum berbasis pilihan ganda A/B/C/D), GSM8K (nalar matematika dengan jawaban numerik), dan HumanEval (akurasi pemrograman Python dievaluasi melalui *unit-test*), serta satu instrumen tambahan berupa MT-Bench dengan skor *Type-Token Ratio* (TTR) yang mengukur keragaman leksikal teks generatif. Masing-masing *benchmark* mengeksekusi 100 sampel acak dengan suhu *sampling* deterministik (`temperature=0`). Eksekusi akurasi dijalankan pada *host* PC NVIDIA RTX 3060 untuk menghemat waktu evaluasi, sedangkan validasi performa keluaran model identik dengan eksekusi pada perangkat *target* karena format `.gguf` yang seragam. Data hasil pengujian disajikan pada Tabel IV.4 dan Tabel IV.5.

| Benchmark | F16 | Q5\_K\_M | Q4\_K\_M | Q3\_K\_M |
|---|:---:|:---:|:---:|:---:|
| MMLU (A/B/C/D) | 32% | 34% | 25% | 28% |
| GSM8K (numerik) | 58% | 55% | 50% | 40% |
| HumanEval (kode) | 36% | 29% | 37% | 30% |
| MT-Bench TTR | 0,526 | 0,509 | 0,468 | 0,403 |

: Tabel IV.4 Hasil *Benchmark* Akurasi LFM 2.5 (1,2B) \*

\* Eksekusi akurasi dilakukan pada *host* PC NVIDIA RTX 3060 (n=100 sampel acak per *benchmark*, `temperature=0`). Berkas `.gguf` yang dievaluasi identik dengan berkas yang dimuat pada perangkat Tecno Pova 5. Pada n=100 dengan distribusi biner pass/fail, margin *error* statistik 95% CI berada di kisaran ±10 poin persentase, selisih ≤ 10 poin antar varian secara konservatif harus diperlakukan sebagai *noise* statistik, bukan sebagai indikasi perbedaan kualitas yang substantif.

| Benchmark | F16 | Q5\_K\_M | Q4\_K\_M | Q3\_K\_M |
|---|:---:|:---:|:---:|:---:|
| MMLU (A/B/C/D) | 40% | 29% | 37% | 40% |
| GSM8K (numerik) | 16% | 17% | 19% | 12% |
| HumanEval (kode) | 52% | 47% | 40% | 25% |
| MT-Bench TTR | 0,546 | 0,412 | 0,568 | 0,521 |

: Tabel IV.5 Hasil *Benchmark* Akurasi Qwen 3.5 (2B) \*\*

\*\* Tabel IV.5 dieksekusi pada *host* PC NVIDIA RTX 3060 dengan kondisi sampling yang sama dengan Tabel IV.4. Qwen 3.5 (2B) merupakan model dengan arsitektur *reasoning* (memproduksi blok `<think>...</think>` sebagai jejak penalaran sebelum jawaban final). Skor akurasi yang dilaporkan menggunakan *parser* berlapis yaitu pencocokan ketat (`####<num>`, `\boxed{...}`, *final answer*) dengan *fallback* pada kandidat angka/huruf terakhir setelah eliminasi blok `<think>`. Skor GSM8K Qwen sangat rendah karena 60–80% keluaran model tidak menyelesaikan penalaran dalam anggaran 200 *token* yang ditetapkan (`strict_miss` tinggi); detail keterbatasan ini dijelaskan pada Sub-bab 4.3.3.

![Gambar IV.5 Hasil *benchmark* akurasi (MMLU, GSM8K, HumanEval) untuk kedua model. Sumber: olahan penulis.](gambar/4_5_akurasi_benchmark.png){width=98%}

**LFM 2.5 — stabil tetapi melemah pada GSM8K.** Tabel IV.4 memperlihatkan akurasi LFM relatif konsisten lintas varian, dengan penurunan paling tajam pada GSM8K (58% → 40% pada Q3\_K\_M, selisih 18 poin). MMLU justru berfluktuasi non-monoton di rentang ≈28–34%, dan HumanEval relatif stabil di 29–37%. MT-Bench TTR menurun monoton (0,526 → 0,403), menandakan berkurangnya keragaman leksikal saat presisi bobot makin agresif.

**Qwen 3.5 — HumanEval menurun progresif, GSM8K artefaktual.** Tabel IV.5 menunjukkan profil yang berbeda: HumanEval turun progresif (52% → 25% pada Q3\_K\_M), sementara GSM8K seragam rendah di 12–19%. Skor rendah pada GSM8K **bukan** indikasi kerusakan logika model, melainkan keterbatasan instrumen evaluasi terhadap *reasoning model* yang diuraikan pada sub-bab berikut.

### 4.3.3 Keterbatasan Evaluasi Akurasi pada *Reasoning Model* (Qwen 3.5)

Qwen 3.5 (2B) yang digunakan pada penelitian ini termasuk dalam kategori *reasoning model*: alih-alih langsung menjawab, model menghasilkan blok penalaran rantai-pikiran (*chain-of-thought*) yang ditandai oleh penanda khusus `<think> ... </think>` sebelum jawaban final. Karakteristik ini didokumentasikan secara eksplisit pada laporan teknis Qwen3 yang memperkenalkan *thinking mode* sebagai mekanisme bawaan keluarga model tersebut (Qwen Team, 2025). Karakteristik arsitektural ini menimbulkan tiga konsekuensi metodologis yang membatasi validitas perbandingan akurasi pada Tabel IV.5.

1. **Anggaran *token* yang terbatas (200 *token*) sering habis pada blok `<think>`.** Pada eksekusi GSM8K, ditemukan 60–80% respons (`strict_miss` 63 hingga 80 dari 100 sampel) yang berakhir tanpa pernah memproduksi penanda jawaban final (`####<num>`, `\boxed{...}`, atau frasa *final answer*) karena anggaran *token* tuntas sebelum penalaran rampung.
2. ***Parser fallback* tidak ekuivalen dengan jawaban benar.** Setelah pencocokan ketat gagal, *fallback* mengambil kandidat angka terakhir pada teks. Pada keluaran *reasoning* yang masih dalam tahap analisis, angka terakhir merupakan langkah-langkah aritmetika pertengahan, bukan kesimpulan; akibatnya `fallback_hit` mencapai 60–80 tetapi proporsi yang sesungguhnya benar tetap rendah (≤ 19%).
3. **Variansi antar *run* tinggi.** Pengulangan terhadap kombinasi (Qwen 3.5 F16, GSM8K) menghasilkan skor 21%, 65%, dan 16% di tiga *run* terpisah pada konfigurasi parameter yang sama. Variansi ini bukan disebabkan ketidakdeterministikan model (suhu *sampling* sudah disetel 0), melainkan oleh interaksi antara panjang penalaran, ambang penghentian dini (*early stopping*) berdasarkan pencocokan frasa *final answer*, dan perubahan kecil pada *prompt template*.

Upaya mitigasi telah dilakukan dengan menaikkan anggaran *token* menjadi 1024 dan menambahkan jendela konteks 2048 *token*, namun pola `strict_miss` tinggi pada GSM8K tetap muncul karena rata-rata panjang penalaran Qwen 3.5 untuk soal kelas SD/SMP melampaui jendela tersebut. Oleh karena itu, skor akurasi Qwen 3.5 pada Tabel IV.5 (khususnya kolom GSM8K dengan tanda \*\*) dilaporkan sebagai *lower bound* dan **tidak boleh diinterpretasikan sebagai kemampuan inheren model**. Konsekuensi dari keterbatasan ini diuraikan kembali pada BAB V Sub-bab 5.2 (Keterbatasan Penelitian), dengan rekomendasi penelitian lanjutan untuk memisahkan *prompt* reasoning-mode dan instruct-mode serta mengevaluasi dengan instrumen yang sadar-format penalaran (misalnya MATH dataset dengan *answer extractor* yang ekuivalen dengan *reasoning trace*).

## 4.4 Pembahasan Analisis Komparatif

Sub-bab ini membedah signifikansi data hasil pengujian melalui tinjauan teoritis arsitektur *Edge Intelligence* dan hukum ketahanan kompresi (*scaling laws*).

### 4.4.1 Efisiensi RAM dan Peningkatan *Generation Speed*

Hasil pengujian mengonfirmasi bahwa metode PTQ efektif dalam mengatasi kendala *shared-memory* pada perangkat berkapasitas RAM 8 GB. Pemuatan model FP16 pada Qwen 3.5 menyerap hampir 47% kapasitas RAM sistem (3,74 GB) dan berpotensi memicu *OOM Killer* dari sistem operasi Android. Intervensi Q4\_K\_M berhasil mereduksi penggunaan RAM Qwen menjadi 2,56 GB (efisiensi 31,6%), sedangkan Q3\_K\_M menekannya menjadi 1,90 GB (efisiensi 49,3%), sehingga stabilitas operasional perangkat terjaga.

Penurunan beban *bandwidth* data dari RAM ke CPU berimplikasi langsung pada peningkatan *Generation Speed* untuk LFM 2.5, yang melonjak dari 5,57 t/s pada FP16 menjadi 13,67 t/s pada Q4\_K\_M, atau setara akselerasi 2,45 kali lipat dibanding versi murninya. Total waktu eksekusi LFM Q4\_K\_M juga menjadi yang tersingkat (7,33 detik) atau 2,18 kali lebih cepat dibanding FP16 (16 detik). Pola ini konsisten dengan dalil *Memory-Bound* (Zhang dkk., 2024) sekaligus sejalan dengan studi sistematis pertama eksekusi LLM *on-device* pada Android dan iOS yang menyimpulkan bahwa inferensi LLM bersifat *memory-bound* (Laskaridis dkk., 2024). Khusus untuk LFM 2.5, percepatan turut diperkuat oleh karakteristik *hybrid backbone* yang dirancang untuk *fast prefill/decode* di CPU (Liquid AI, 2025).

### 4.4.2 Anomali Kecepatan Baca (*Prompt Speed*) pada Varian Q3\_K\_M

Secara teoritis, varian dengan jejak RAM paling kecil seharusnya memiliki performa tercepat, namun Tabel IV.2 menunjukkan pola yang justru sebaliknya pada Q3\_K\_M. Pada LFM 2.5, *Prompt Speed* Q3\_K\_M anjlok ke 18,27 t/s, jauh di bawah Q4\_K\_M (43,67 t/s) maupun Q5\_K\_M (35,33 t/s). Pola serupa juga teramati pada Qwen 3.5, dengan Q3\_K\_M hanya mencapai 14,55 t/s dibanding Q4\_K\_M (27,00 t/s) dan Q5\_K\_M (22,55 t/s).

Fenomena tersebut dianalisis sebagai konsekuensi arsitektur CPU ARM. Proses *unpacking* bobot 4-bit dan 5-bit relatif efisien karena strukturnya simetris terhadap *register* CPU. Format 3-bit bersifat ganjil sehingga memaksa set instruksi CPU melakukan operasi *bit-shifting* tambahan yang kompleks, sehingga muncul *bottleneck* pada fase *pre-fill* dan memperpanjang durasi eksekusi total. Penjelasan ini selaras dengan studi resmi Arm Inc. yang mengkonfirmasi bahwa proporsi instruksi *multiplication* bermanfaat pada eksekusi LLM terkuantisasi di CPU Arm sangat rendah karena *cycle* CPU banyak terserap oleh *unpacking* susunan bobot dan *dequantization* (Gope dkk., 2025).

Beban CPU *peak* yang teramati pada varian Q3\_K\_M kedua model juga menjadi yang tertinggi (LFM 464%; Qwen 525%), mengindikasikan saturasi *thread* yang lebih tinggi pada operasi *dequantization*. Pola serupa juga ditemukan pada studi *real-world* pengujian LLM terkuantisasi di berbagai generasi *smartphone* yang menyoroti pengaruh *thermal* dan mikroarsitektur SoC terhadap *sustained throughput* (Çöplü dkk., 2023).

### 4.4.3 Dampak Distorsi terhadap Nalar Matematika dan Logika Pemrograman

Selain anomali kecepatan, varian Q3\_K\_M juga memperlihatkan tanda kerusakan pada struktur nalar model. *Perplexity* yang melampaui ambang toleransi (14,5–15,2) dikuatkan oleh anjloknya akurasi GSM8K LFM 2.5 (58 → 40%, selisih 18 poin) dan HumanEval Qwen 3.5 (52 → 25%, selisih 27 poin). Penurunan tajam tersebut disebabkan oleh hilangnya nilai-nilai pencilan (*outliers*) pada matriks bobot akibat kuantisasi ekstrem (Gong dkk., 2024). Tidak seperti bahasa naratif yang toleran terhadap redundansi, logika matematis dan pemrograman bersifat eksak, sehingga pemotongan presisi yang terlalu agresif secara langsung meruntuhkan fondasi logika fungsional model.

Skor MT-Bench TTR pada LFM 2.5 turun monoton dari 0,526 (F16) ke 0,403 (Q3\_K\_M), memperkuat indikasi adanya penyempitan distribusi leksikal pada lapisan generatif teks bebas sebagai akibat hilangnya presisi pada bobot pasca-kuantisasi.

### 4.4.4 Penetapan Titik Keseimbangan Optimal (*Sweet Spot*)

Melalui sintesis antara performa perangkat keras (RAM dan TPS) dan kualitas kognitif (PPL dan akurasi *benchmark*), varian Q4\_K\_M ditetapkan sebagai *sweet spot* untuk implementasi *Mobile Edge AI* pada Tecno Pova 5. Varian ini mengoptimalkan penggunaan RAM pada tingkat yang aman bagi perangkat berkapasitas 8 GB sambil mempertahankan *Prompt Speed* (43,67 t/s pada LFM) dan *Generation Speed* (13,67 t/s pada LFM) pada level tertinggi di antara seluruh varian kuantisasi yang diuji. Efisiensi tersebut dicapai dengan margin penurunan akurasi LFM yang relatif terkontrol (GSM8K turun 8 poin dari *baseline* 58% sekaligus HumanEval naik 1 poin) serta kenaikan *Perplexity* yang masih di bawah 0,6 poin terhadap *baseline* FP16. Visualisasi *trade-off* multi-dimensi disajikan pada Gambar IV.6.

![Gambar IV.6 Diagram *trade-off* multi-dimensi LFM 2.5 (1,2B) per varian kuantisasi (skor normalisasi 0..1, lebih tinggi = lebih baik). Sumber: olahan penulis.](gambar/4_6_tradeoff_radar.png){width=80%}

### 4.4.5 Kuantifikasi Penurunan Kepintaran F16 vs Q3/Q4/Q5 dan Rekomendasi Varian Operasional untuk Tecno Pova 5

Sub-bab ini menjawab dua pertanyaan praktis sekaligus, yaitu seberapa besar kepintaran yang hilang akibat kuantisasi dan varian mana yang paling tepat untuk Tecno Pova 5. Pendekatan analitik dilakukan dengan memadukan dua sudut pandang, yakni retensi kepintaran yang diukur dari akurasi relatif terhadap *baseline* FP16 dan efisiensi operasional yang mencakup RAM, kecepatan, serta margin keamanan termal. Kuantifikasi disajikan untuk kedua keluarga model uji: LFM 2.5 (1,2 miliar parameter) sebagai *baseline* analisis utama karena profil pengukuran kognitifnya paling stabil, dan Qwen 3.5 (2 miliar parameter) sebagai pembanding lintas-arsitektur pada sub-subbab "Analisis Paralel".

Khusus Qwen 3.5, skor GSM8K diberi tanda † dan dikeluarkan dari komputasi rerata akurasi karena keterbatasan instrumen evaluasi pada *reasoning model* yang telah dijabarkan pada Sub-bab 4.3.3. Dengan demikian rerata Qwen 3.5 dihitung dari tiga *benchmark* non-GSM8K (MMLU, HumanEval, dan MT-Bench TTR×100) agar interpretasi tetap tidak bias.

| *Benchmark* | F16 (kontrol) | Q5\_K\_M | ΔQ5 | Q4\_K\_M | ΔQ4 | Q3\_K\_M | ΔQ3 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| MMLU (A/B/C/D) | 32% | 34% | **+2** | 25% | **−7** | 28% | **−4** |
| GSM8K (numerik) | 58% | 55% | **−3** | 50% | **−8** | 40% | **−18** |
| HumanEval (kode) | 36% | 29% | **−7** | 37% | **+1** | 30% | **−6** |
| MT-Bench TTR (×100) | 52,6 | 50,9 | **−1,7** | 46,8 | **−5,8** | 40,3 | **−12,3** |
| **Rata-rata akurasi tiga *benchmark*** | **42,0%** | **39,3%** | **−2,7** | **37,3%** | **−4,7** | **32,7%** | **−9,3** |
| **Retensi kepintaran (% terhadap F16)** | **100%** | - | **93,6%** | - | **88,9%** | - | **77,8%** |

: Tabel IV.6 Selisih (*Delta*) Akurasi LFM 2.5 per Varian terhadap *Baseline* F16 (basis Tabel IV.4)

Dari Tabel IV.6 terbaca tiga pola utama yang dijelaskan pada sub-subbab 4.4.5.1 hingga 4.4.5.3.

#### 4.4.5.1 GSM8K sebagai *Benchmark* Paling Sensitif terhadap Kuantisasi

Penurunan akurasi GSM8K bersifat monoton dan konsisten lintas varian, yaitu Q5 turun 3 poin, Q4 turun 8 poin, dan Q3 turun 18 poin. Pola ini sejalan dengan temuan Kurtić dkk. (2024) yang menyatakan bahwa *task* yang menuntut presisi numerik dan logika berlapis paling rentan terhadap reduksi presisi bobot, karena kuantisasi mengeliminasi tepi *outlier* yang berperan sebagai *anchor* numerik halus pada bobot atensi.

#### 4.4.5.2 Fluktuasi Non-Monoton pada MMLU dan HumanEval

MMLU justru meningkat 2 poin pada Q5 dan HumanEval meningkat 1 poin pada Q4. Anomali seperti turunnya MMLU Q4 (25%) yang lebih rendah daripada Q3 (28%) berada dalam rentang margin *error* statistik 95% CI sebesar ±10 poin pada n=100, sehingga selisih 3 poin tersebut tidak signifikan secara statistik dan tidak dapat ditafsirkan sebagai indikasi bahwa Q3 lebih cerdas daripada Q4. Secara teoritis kuantisasi dapat berfungsi sebagai *regularizer* lemah pada *task* dengan distribusi jawaban diskret (pilihan ganda), namun efek ini tidak konsisten dan tidak dapat dijadikan dalil umum.

#### 4.4.5.3 Penyempitan Distribusi Leksikal pada MT-Bench TTR

MT-Bench TTR LFM 2.5 turun monoton dari 52,6 menjadi 40,3, menandakan terjadinya penyempitan distribusi leksikal sebagai akibat hilangnya presisi bobot pada lapisan generatif teks bebas.

Untuk menjawab pertanyaan praktis "varian mana yang terbaik untuk Tecno Pova 5?", Tabel IV.7 mengintegrasikan retensi kepintaran dengan tiga metrik operasional yang sudah disajikan pada Tabel IV.2, kemudian menghitung *Compound Score* yang menggambarkan *throughput* efektif relatif terhadap konsumsi RAM dan retensi akurasi.

| Varian | *Peak* RAM (MB) | Gen TPS (t/s) | Total Waktu (s) | Retensi Akurasi | CPU *Peak* (%) | *Compound Score*\* |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| F16 | 2.303 | 5,57 | 16,00 | 100,0% | 292 | 2,42 |
| Q5\_K\_M | 1.665 | 10,63 | 10,67 | 93,6% | 357 | 5,97 |
| **Q4\_K\_M** | **1.453** | **13,67** | **7,33** | **88,9%** | **299** | **8,36** |
| Q3\_K\_M | 912 | 11,07 | 14,33 | 77,8% | 464 | 9,44 |

: Tabel IV.7 Matriks Rekomendasi Varian LFM 2.5 untuk Tecno Pova 5 (RAM 8 GB, Helio G99)

\* *Compound Score* = (Gen TPS × Retensi Akurasi) / RAM<sub>GB</sub> × 1.000, sehingga semakin tinggi semakin baik kombinasi kecepatan dan retensi kepintaran per unit memori yang dikonsumsi.

Tabel IV.7 menunjukkan dua kandidat dengan *Compound Score* tertinggi, yaitu Q4\_K\_M (8,36) dan Q3\_K\_M (9,44). Q3\_K\_M memang unggul secara aritmetik karena denominator RAM-nya paling kecil, namun terdapat tiga catatan yang menjadi alasan varian tersebut tidak direkomendasikan untuk Tecno Pova 5. Pertama, kepintaran terjun bebas pada nalar matematika dengan GSM8K turun 18 poin, sehingga model praktis kehilangan kemampuan menyelesaikan soal hitung sederhana yang ironisnya merupakan *use case* utama asisten AI pada perangkat seluler. Kedua, CPU *peak* mencapai 464% yang mendekati saturasi empat inti penuh termasuk *boost*, sehingga memperbesar risiko *thermal throttling* pada sesi panjang yang pada *smartphone* Helio G99 tanpa pendingin aktif berakibat penurunan *sustained throughput* (Çöplü dkk., 2023). Ketiga, terjadi anomali *Prompt Speed* sebesar 18,27 t/s yang lebih rendah dibanding Q4\_K\_M (43,67 t/s) akibat *unpacking* susunan bit ganjil yang sudah dianalisis pada Sub-bab 4.4.2 dan didukung oleh Gope dkk. (2025).

Dengan demikian, Q4\_K\_M ditetapkan sebagai varian operasional paling tepat untuk Tecno Pova 5. Kepintaran yang hilang pada varian ini bersifat moderat dengan rata-rata penurunan 4,7 poin akurasi atau retensi 88,9% terhadap F16, namun *trade-off* yang diperoleh sangat menguntungkan, yaitu *peak* RAM turun 36,9%, *Generation Speed* meningkat 2,45 kali lipat, total waktu eksekusi turun 54,2%, dan CPU *peak* tetap terkendali di kisaran 300%. Kombinasi ini memberi margin aman bagi RAM 8 GB Tecno Pova 5 yang masih harus melayani OS Android dan aplikasi latar belakang, sekaligus meminimalkan risiko *thermal throttling* pada SoC Helio G99. Visualisasi *delta* akurasi disajikan pada Gambar IV.7.

![Gambar IV.7 *Delta* akurasi LFM 2.5 per varian kuantisasi (relatif terhadap F16, dalam poin persentase). Sumber: olahan penulis.](gambar/4_7_delta_akurasi.png){width=92%}

#### Analisis Paralel pada Qwen 3.5 (2B)

Untuk melengkapi gambaran komparatif, Tabel IV.6-B menyajikan kuantifikasi *delta* akurasi yang sama untuk arsitektur Qwen 3.5 (2B) sebagai pembanding kontekstual. Sebagaimana telah dijelaskan pada Sub-bab 4.3.3, skor GSM8K Qwen 3.5 dilaporkan sebagai *lower bound* akibat keterbatasan instrumen evaluasi terhadap *reasoning model*, sehingga kolom GSM8K pada tabel di bawah ini diberi tanda dan **tidak boleh diinterpretasikan sebagai indikator kemampuan inheren model**. Walaupun begitu, kolom MMLU dan HumanEval tetap dapat menggambarkan tren stabilitas kognitif lintas varian, sedangkan MT-Bench TTR mencerminkan keragaman leksikal yang tidak terdampak oleh keterbatasan *parser*.

| *Benchmark* | F16 (kontrol) | Q5\_K\_M | ΔQ5 | Q4\_K\_M | ΔQ4 | Q3\_K\_M | ΔQ3 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| MMLU (A/B/C/D) | 40% | 29% | **−11** | 37% | **−3** | 40% | **±0** |
| GSM8K (numerik) † | 16% | 17% | **+1** | 19% | **+3** | 12% | **−4** |
| HumanEval (kode) | 52% | 47% | **−5** | 40% | **−12** | 25% | **−27** |
| MT-Bench TTR (×100) | 54,6 | 41,2 | **−13,4** | 56,8 | **+2,2** | 52,1 | **−2,5** |
| **Rata-rata akurasi tiga *benchmark* (MMLU, HumanEval, TTR×100)** ‡ | **48,9%** | **39,1%** | **−9,8** | **44,6%** | **−4,3** | **39,0%** | **−9,9** |
| **Retensi kepintaran (% terhadap F16)** ‡ | **100%** | - | **80,0%** | - | **91,2%** | - | **79,8%** |

: Tabel IV.6-B Selisih (*Delta*) Akurasi Qwen 3.5 per Varian terhadap *Baseline* F16 (basis Tabel IV.5)

† GSM8K Qwen 3.5 dilaporkan sebagai *lower bound* akibat keterbatasan *parser reasoning model* (lihat Sub-bab 4.3.3); kolom ini **dikeluarkan dari komputasi rerata** agar tidak menghasilkan rerata yang bias. ‡ Rerata dan retensi kepintaran Qwen 3.5 dihitung dari tiga *benchmark* non-GSM8K (MMLU, HumanEval, MT-Bench TTR×100); pada n=100 dengan distribusi pass/fail, margin *error* statistik 95% CI tetap berada di kisaran ±10 poin persentase sehingga selisih ≤ 10 poin antar varian harus diperlakukan secara konservatif.

Tabel IV.6-B menampilkan tiga karakteristik penting dari profil degradasi Qwen 3.5. Pertama, Q3\_K\_M memperlihatkan retensi MMLU yang sempurna (40%, ΔQ3 = ±0) tetapi mengalami *collapse* tajam pada HumanEval dengan akurasi turun dari 52% ke 25% (ΔQ3 = −27 poin); pola ini mengindikasikan bahwa kuantisasi 3-bit pada model *reasoning* lebih mengganggu *long-context code generation* daripada *short-form factual recall*. Kedua, Q4\_K\_M tetap menjadi titik keseimbangan terbaik dengan retensi gabungan 91,2% terhadap F16, konsisten dengan rekomendasi LFM. Ketiga, Q5\_K\_M mengalami degradasi MT-Bench TTR yang tidak monoton (54,6 → 41,2), kemungkinan akibat sensitivitas *layer norm* pada lapisan generatif terhadap pembulatan presisi 5-bit, walaupun selisih 13,4 poin tersebut berada di tepi margin *error* statistik dan memerlukan replikasi pada sampel yang lebih besar untuk dapat dipastikan.

Selanjutnya, Tabel IV.7-B mengintegrasikan retensi kepintaran Qwen 3.5 dengan metrik operasional dari Tabel IV.2 menggunakan rumus *Compound Score* yang sama.

| Varian | *Peak* RAM (MB) | Gen TPS (t/s) | Total Waktu (s) | Retensi Akurasi ‡ | CPU *Peak* (%) | *Compound Score*\* |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| F16 | 3.744 | 1,87 | 310,33 | 100,0% | 430 | 0,50 |
| Q5\_K\_M | 2.856 | 4,60 | 181,00 | 80,0% | 509 | 1,29 |
| **Q4\_K\_M** | **2.563** | **4,95** | **297,00** | **91,2%** | **501** | **1,76** |
| Q3\_K\_M | 1.898 | 4,25 | 187,00 | 79,8% | 525 | 1,79 |

: Tabel IV.7-B Matriks Rekomendasi Varian Qwen 3.5 untuk Tecno Pova 5 (RAM 8 GB, Helio G99)

\* *Compound Score* = (Gen TPS × Retensi Akurasi) / RAM<sub>GB</sub> × 1.000. ‡ Retensi akurasi dihitung dari rata-rata tiga *benchmark* non-GSM8K (Tabel IV.6-B).

Pola pada Tabel IV.7-B sejalan dengan pola LFM. Q3\_K\_M kembali unggul secara aritmetik pada *Compound Score* (1,79) tetapi tetap tidak direkomendasikan karena tiga alasan utama. Pertama, *collapse* HumanEval sebesar 27 poin mematikan *use case* utama asisten *coding*. Kedua, CPU *peak* sebesar 525% (mendekati 87,5% saturasi enam-*thread*) memperbesar risiko *thermal throttling* pada sesi panjang. Ketiga, anomali *Prompt Speed* sebesar 14,55 t/s lebih lambat dibanding Q4 (27,00 t/s) dan Q5 (22,55 t/s) sebagaimana dianalisis pada Sub-bab 4.4.2 dan dikonfirmasi secara statistik pada Tabel IV.9.

Dengan demikian, rekomendasi varian operasional Qwen 3.5 untuk Tecno Pova 5 jatuh pada Q4\_K\_M, konsisten dengan rekomendasi LFM 2.5. Q4\_K\_M dapat ditetapkan sebagai *default* lintas-arsitektur untuk SLM 1–2 miliar parameter pada perangkat Android berbasis Helio G99 dengan RAM 8 GB. Visualisasi *delta* akurasi Qwen 3.5 disajikan pada Gambar IV.8.

![Gambar IV.8 *Delta* akurasi Qwen 3.5 per varian kuantisasi (relatif terhadap F16, dalam poin persentase; GSM8K diberi tanda † dan tidak dimasukkan ke rerata). Sumber: olahan penulis.](gambar/4_8_delta_akurasi_qwen.png){width=92%}

### 4.4.6 Uji Beda Performa Antar Varian

Klaim performa pada Tabel IV.2 perlu dilandasi bukti tambahan, bukan hanya nilai rerata. Karena itu dilakukan uji beda statistik untuk seluruh pasangan varian pada kedua keluarga model (LFM 2.5 dan Qwen 3.5). Ringkasan hasil ditampilkan dalam dua tabel berikut dengan format yang sangat sederhana, yaitu kata **Beda** berarti dua varian *berbeda nyata* pada metrik tersebut, dan kata **Tidak** berarti perbedaan *belum cukup meyakinkan* untuk disebut nyata. Detail teknis (statistik *t* dan nilai *p* dari *Welch's t-test* serta *one-way ANOVA* pada taraf signifikansi α = 0,05) tersedia secara lengkap pada **Lampiran D** (LFM 2.5) dan **Lampiran E** (Qwen 3.5) bagi pembaca yang ingin menelusuri angka uji secara mendalam.

#### 4.4.6.1 Hasil Uji Beda LFM 2.5 (1,2B)

| Pasangan Varian | Gen TPS | Prompt TPS | *Peak* RAM | **Ringkasan** |
|---|:---:|:---:|:---:|---|
| F16 vs Q5\_K\_M | Beda | Tidak | Beda | Gen & RAM berbeda; Prompt tidak |
| F16 vs Q4\_K\_M | Beda | Tidak | Beda | Gen & RAM berbeda; Prompt tidak |
| F16 vs Q3\_K\_M | Beda | Tidak | Beda | Gen & RAM berbeda; Prompt tidak |
| Q5\_K\_M vs Q4\_K\_M | Beda | Beda | Beda | Semua metrik berbeda |
| Q5\_K\_M vs Q3\_K\_M | Tidak | Beda | Beda | Prompt & RAM berbeda; Gen tidak |
| Q4\_K\_M vs Q3\_K\_M | Beda | Beda | Beda | Semua metrik berbeda |

: Tabel IV.8 Ringkasan Uji Beda Performa Antar Varian LFM 2.5

Keterangan: **Beda** = berbeda nyata secara statistik; **Tidak** = tidak berbeda nyata. Sumber detail uji statistik (statistik *t*, nilai *p*, dan ANOVA) tersedia pada Lampiran D.

Tabel IV.8 menyampaikan tiga temuan utama. Pertama, perbedaan *Generation Speed* dan *Peak* RAM antar varian terbukti nyata di hampir seluruh pasangan, sehingga klaim utama penelitian bahwa kuantisasi PTQ mempercepat inferensi sekaligus mereduksi konsumsi RAM tidak sekadar pola rerata yang kebetulan terjadi. Kedua, keunggulan Q4\_K\_M atas Q3\_K\_M terbukti nyata baik pada Gen TPS (13,67 vs 11,07 t/s) maupun Prompt TPS (43,67 vs 18,27 t/s); temuan ini memperkuat rekomendasi varian operasional Q4\_K\_M pada Sub-bab 4.4.5 dari sudut pandang murni kecepatan, bahkan sebelum mempertimbangkan retensi kepintaran. Ketiga, pengaruh kuantisasi pada *Prompt Speed* tidak homogen: pasangan F16 vs Q3\_K\_M dan F16 vs Q5\_K\_M tidak menunjukkan perbedaan yang meyakinkan, dan pola tidak homogen ini mengonfirmasi anomali *unpacking* bit ganjil pada Q3\_K\_M yang sudah dianalisis pada Sub-bab 4.4.2.

#### 4.4.6.2 Hasil Uji Beda Qwen 3.5 (2B)

| Pasangan Varian | Gen TPS | Prompt TPS | *Peak* RAM | **Ringkasan** |
|---|:---:|:---:|:---:|---|
| F16 vs Q5\_K\_M | Beda | Tidak | Beda | Gen & RAM berbeda; Prompt tidak |
| F16 vs Q4\_K\_M | Beda | Tidak | Beda | Gen & RAM berbeda; Prompt tidak |
| F16 vs Q3\_K\_M | Beda | Beda | Beda | Semua metrik berbeda |
| Q5\_K\_M vs Q4\_K\_M | Tidak | Tidak | Beda | Hanya RAM berbeda |
| Q5\_K\_M vs Q3\_K\_M | Tidak | Beda | Beda | Prompt & RAM berbeda; Gen tidak |
| Q4\_K\_M vs Q3\_K\_M | Tidak | Beda | Beda | Prompt & RAM berbeda; Gen tidak |

: Tabel IV.9 Ringkasan Uji Beda Performa Antar Varian Qwen 3.5

Keterangan: **Beda** = berbeda nyata secara statistik; **Tidak** = tidak berbeda nyata. Sumber detail uji statistik (statistik *t*, nilai *p*, dan ANOVA) tersedia pada Lampiran E.

Tabel IV.9 mempertegas pola yang teramati pada LFM dan memperluasnya ke arsitektur *reasoning* Qwen 3.5. Pertama, reduksi *peak* RAM Qwen jauh lebih dramatis daripada LFM dan terbukti nyata pada seluruh pasangan, dengan rerata turun dari 3.744 MB (FP16) menjadi 2.856 MB (Q5\_K\_M), 2.563 MB (Q4\_K\_M), dan 1.898 MB (Q3\_K\_M). Kedua, peningkatan *Generation Speed* dari FP16 ke seluruh varian terkuantisasi terbukti nyata (rasio percepatan 2,28–2,65 kali lipat dari 1,87 t/s menjadi 4,25–4,95 t/s), tetapi perbedaan *Generation Speed* antar tiga varian terkuantisasi tidak nyata; pola ini menandakan Qwen 3.5 mengalami saturasi *throughput* pada CPU Helio G99 di kisaran 4–5 t/s, berbeda dengan LFM 2.5 yang masih memiliki *headroom* hingga 13,67 t/s pada Q4\_K\_M. Ketiga, anomali *Prompt Speed* pada Q3\_K\_M kembali muncul (F16 vs Q3\_K\_M dan Q4\_K\_M vs Q3\_K\_M sama-sama berbeda nyata), menguatkan analisis Sub-bab 4.4.2 bahwa *bottleneck unpacking* bit ganjil pada CPU Arm bersifat arsitektur-independen dan terjadi pada kedua keluarga model selama format presisi 3-bit dipakai.

Dengan demikian, hasil uji statistik dari kedua tabel di atas memberikan dukungan kuantitatif yang konsisten dengan kerangka rekomendasi Tabel IV.7 (LFM) dan rekomendasi paralel Tabel IV.7-B (Qwen). Untuk LFM 2.5, Q4\_K\_M unggul signifikan dibanding Q3\_K\_M pada metrik *throughput* utama. Untuk Qwen 3.5, seluruh varian terkuantisasi memiliki RAM dan *Generation Speed* yang signifikan lebih baik dibanding FP16 tanpa perbedaan *Generation Speed* yang signifikan di antara mereka. Gabungan kedua temuan ini menjadikan Q4\_K\_M sebagai varian dengan profil efisiensi paling kokoh untuk Tecno Pova 5 pada kedua arsitektur uji.

\newpage

# BAB V PENUTUP

## 5.1 Kesimpulan

Berdasarkan serangkaian eksperimen mengenai optimasi arsitektur *Small Language Model* pada ekosistem *Mobile Edge Computing* berbasis Android, dapat ditarik beberapa kesimpulan utama sebagai jawaban atas rumusan masalah penelitian, yaitu:

1. **Efektivitas Kuantisasi dalam Mitigasi Limitasi Memori.** Implementasi PTQ dengan format GGUF terbukti secara empiris mampu mengatasi kendala *shared-memory* pada Android kelas menengah, dan **terkonfirmasi signifikan secara statistik** pada kedua arsitektur uji (LFM 2.5 dan Qwen 3.5; lihat hasil uji beda pada Tabel IV.8 dan Tabel IV.9 yang menunjukkan reduksi *Peak* RAM berbeda nyata untuk seluruh pasangan varian). Pemuatan model FP16 dengan parameter 2 miliar (Qwen 3.5) menyebabkan dominasi penggunaan RAM hingga 3,74 GB, berisiko tinggi memicu *Force Close*. Melalui reduksi presisi ke Q4\_K\_M dan Q3\_K\_M, beban memori dikompresi melampaui 60% (storage) dan 30–49% (RAM), sehingga menjamin stabilitas operasional perangkat. Reduksi RAM proses pada Qwen 3.5 bahkan lebih dramatis daripada LFM 2.5 karena *baseline* FP16-nya jauh lebih berat (Qwen Q3\_K\_M: 1,90 GB vs F16 3,74 GB, efisiensi 49,3%).
2. **Optimalisasi Kecepatan Inferensi, Saturasi *Throughput* pada Model 2B, dan Anomali Arsitektur ARM.** Reduksi ukuran berkas berbanding lurus dengan peningkatan *Generation Speed* (Q4 LFM: 2,45× *baseline*; Q4 Qwen: 2,65× *baseline*), dengan peningkatan dari FP16 ke seluruh varian terkuantisasi terbukti signifikan secara statistik untuk kedua arsitektur. Namun, terdapat dua catatan penting. Pertama, **Qwen 3.5 mengalami saturasi *Generation Speed* di kisaran 4–5 t/s** pada CPU Helio G99 tanpa peduli level kuantisasinya, sehingga perbedaan *Gen TPS* antar tiga varian terkuantisasi tidak signifikan (Tabel IV.9); kondisi ini berbeda dari LFM 2.5 yang masih memiliki *headroom* hingga 13,67 t/s pada Q4\_K\_M. Kedua, penelitian ini mengidentifikasi **anomali arsitektural pada CPU ARM**, di mana Q3\_K\_M mengalami degradasi *Prompt Speed* yang signifikan akibat kompleksitas *unpacking* susunan bit ganjil; pola ini teramati pada **kedua keluarga model** (LFM dan Qwen) dan terbukti signifikan secara statistik (Tabel IV.9 menunjukkan pasangan F16 vs Q3 dan Q4 vs Q3 pada Qwen sama-sama berbeda nyata untuk metrik Prompt TPS), membuktikan bahwa ukuran berkas yang lebih kecil tidak selalu menghasilkan latensi yang lebih rendah pada arsitektur ARM.
3. **Integritas Kognitif dan Titik Keseimbangan Operasional (*Sweet Spot*) Lintas-Arsitektur.** Kompresi ekstrem pada Q3\_K\_M menyebabkan degradasi kualitas kognitif yang signifikan, ditandai dengan anjloknya akurasi GSM8K (LFM −18 poin) dan HumanEval (LFM −6, Qwen −27 poin) serta pelebaran *Perplexity*. Penurunan ini disebabkan oleh hilangnya *outliers* pada matriks bobot yang esensial bagi nalar matematis dan generasi kode. Dengan demikian, **Q4\_K\_M ditetapkan sebagai *sweet spot* operasional pada kedua arsitektur uji**: retensi kepintaran 88,9% terhadap F16 untuk LFM dan 91,2% untuk Qwen (Tabel IV.6 dan IV.6-B), dengan *Compound Score* tertinggi yang sehat baik untuk LFM maupun untuk Qwen (di luar Q3 yang dieliminasi karena risiko *thermal* dan *code-collapse*). Konsistensi rekomendasi Q4\_K\_M lintas dua arsitektur SLM 1–2 miliar parameter ini menjadikannya kandidat *default* operasional untuk perangkat Android berbasis Helio G99 dengan RAM 8 GB.

## 5.2 Saran

Berdasarkan temuan penelitian, hasil uji statistik, serta keterbatasan yang teridentifikasi sepanjang eksperimen, penulis mengajukan rekomendasi pengembangan yang dikelompokkan ke dalam **tiga aspek** sebagaimana panduan penulisan, yaitu aspek manajerial, aspek sistem, dan aspek penelitian lanjutan. Setiap rekomendasi dipasangkan dengan keterbatasan yang relevan agar dapat ditelusuri konteksnya.

### 5.2.1 Aspek Manajerial

1. **Adopsi Q4\_K\_M sebagai Konfigurasi Produksi.** Bagi pengembang aplikasi *Mobile AI* yang menargetkan perangkat Android kelas menengah (RAM 8 GB), varian **Q4\_K\_M** direkomendasikan sebagai konfigurasi *default*. Berdasarkan Tabel IV.7, varian ini mereduksi *peak* RAM proses sebesar 36,9% dan mempercepat *Generation Speed* hingga 2,45× *baseline* FP16, dengan retensi akurasi rata-rata 88,9% dan CPU *peak* yang terkontrol di kisaran 300% (jauh dari ambang *thermal throttling*).
2. **Pemisahan Tahap Persiapan Model dan Eksekusi *Runtime*.** Hasil penelitian menunjukkan bahwa tahap kuantisasi berkas `.gguf` lebih efisien dilakukan di PC ber-GPU (lihat Lampiran B), sedangkan eksekusi *runtime* dilakukan di perangkat *target*. Pola kerja dua-*host* ini disarankan diadopsi sebagai standar pengembangan agar siklus iterasi tetap cepat tanpa mengorbankan kemampuan *deployment on-device*.
3. **Penyiapan SOP Pengujian Multi-perangkat.** Mengingat hasil penelitian saat ini hanya tervalidasi pada satu unit Tecno Pova 5 (Helio G99), tim pengembang produksi disarankan menyusun *Standard Operating Procedure* pengujian lintas-SoC (Snapdragon 6/7/8 gen, Dimensity, Tensor) sebelum merilis aplikasi berbasis SLM ke pasar.

### 5.2.2 Aspek Sistem

1. **Eksplorasi Akselerator Komputasi Heterogen.** Mengingat seluruh inferensi pada penelitian ini bersifat CPU-*bound*, pengembangan selanjutnya disarankan mengintegrasikan kerangka inferensi yang mendukung delegasi beban kalkulasi pada modul AI khusus, seperti *Neural Processing Unit* (NPU) atau akselerasi GPU mobile via Vulkan/OpenCL, agar batas atas TPS dapat didorong lebih jauh.
2. **Penambahan Instrumen Telemetri Termal dan Energi.** Penelitian belum menyertakan pengukuran suhu CPU (`/sys/class/thermal/thermal_zone*/temp`) dan konsumsi baterai per 1.000 *token* yang diproduksi. Penambahan kedua metrik ini sangat penting untuk evaluasi praktis dalam konteks *Mobile Edge AI* yang sensitif terhadap *thermal throttling* dan ketahanan baterai. Pendekatan pengukuran energi *high-resolution* berbasis sensor arus eksternal yang dipaparkan oleh Husom dkk. (2024) pada *Raspberry Pi* dapat menjadi acuan adopsi pada perangkat Android.
3. **Integrasi Antarmuka Pengguna Grafis (*Native* GUI).** Untuk meningkatkan utilitas bagi pengguna akhir, purwarupa terminal ini disarankan dikembangkan ke dalam bentuk aplikasi Android *native* menggunakan *Java Native Interface* (JNI). Tujuannya adalah mentransformasi sistem berbasis CLI menjadi asisten AI interaktif yang lebih intuitif dan aksesibel.

### 5.2.3 Aspek Penelitian (Pembahasan) Selanjutnya

1. **Perluasan Lingkup Perangkat Uji.** Replikasi eksperimen pada minimal tiga SoC berbeda (Snapdragon, Dimensity, Tensor) sangat dianjurkan untuk menguji generalisasi temuan *sweet spot* Q4\_K\_M. Variasi karakteristik termal, *governor* CPU, dan skema *power management* berpotensi menggeser titik keseimbangan optimal antar SoC.
2. **Peningkatan Ukuran Sampel *Benchmark* Akurasi.** Evaluasi MMLU, GSM8K, dan HumanEval saat ini menggunakan 100 sampel acak per *benchmark* yang menyisakan margin *error* statistik 95% CI sebesar ±10 poin. Studi lanjutan disarankan menggunakan minimal 500 sampel per *benchmark* atau melaporkan interval kepercayaan secara eksplisit agar perbedaan antar varian dapat dipertegas.
3. **Penyempurnaan Instrumen Evaluasi *Reasoning Model*.** Sebagaimana dijabarkan pada Sub-bab 4.3.3, skor akurasi Qwen 3.5 terdampak oleh interaksi antara format keluaran *chain-of-thought* (`<think>...</think>`), anggaran *token*, dan logika *parser* berlapis. Penelitian lanjutan disarankan mengembangkan *parser* khusus *reasoning model* yang mengizinkan anggaran *token* adaptif dan mendukung deteksi multi-pola jawaban (`####`, `\boxed{}`, *final answer*) tanpa *fallback* yang berisiko bias.
4. **Komparasi dengan Algoritma Kuantisasi Berbasis Aktivasi.** Guna mempertahankan kualitas kognitif pada tingkat kompresi rendah, disarankan melakukan komparasi metode *k-quants* dengan algoritma mutakhir seperti AWQ (Lin dkk., 2023) atau MobileQuant (Tan dkk., 2024) yang lebih adaptif dalam melindungi bobot *outliers*. Pengembangan lanjutan terhadap teknik *prompting*, *alignment*, dan *inference* yang efisien sebagaimana diuraikan oleh Xiao dan Zhu (2025) juga dapat ditambahkan untuk meningkatkan kualitas respons asisten.

\newpage

# DAFTAR PUSTAKA

Ahmad, S., & Safudin, T. (2024). Pengembangan *Chatbot* AI *Large Language Model* (LLM) untuk Layanan Informasi dan Konsultasi RS Brawijaya. *Jurnal Sistem Informasi dan Teknologi*, 6(3), 121–134.

Çöplü, T., Loedi, M., Bendiken, A., Makohin, M., Bouw, J. J., & Cobb, S. (2023). *A Performance Evaluation of a Quantized Large Language Model on Various Smartphones* (arXiv:2312.12472). arXiv. https://arxiv.org/abs/2312.12472

Dettmers, T., Pagnoni, A., Holtzman, A., & Zettlemoyer, L. (2023). QLoRA: Efficient Finetuning of Quantized LLMs. *Advances in Neural Information Processing Systems (NeurIPS) 36*, 10088–10115.

Frantar, E., Ashkboos, S., Hoefler, T., & Alistarh, D. (2023). GPTQ: Accurate Post-Training Quantization for Generative Pre-Trained Transformers. *International Conference on Learning Representations (ICLR)*.

Gong, R., Yong, Y., Gu, S., Huang, Y., Lv, C., Zhang, Y., Liu, X., & Tao, D. (2024). What Makes Quantization for Large Language Models Hard? An Empirical Study from the Lens of Perturbation. *Proceedings of the AAAI Conference on Artificial Intelligence*, 38(15), 18082–18089.

Gope, D., Mansell, D., Loh, D., & Bratt, I. (2025). *Highly Optimized Kernels and Fine-Grained Codebooks for LLM Inference on Arm CPUs* (arXiv:2501.00032). arXiv. https://arxiv.org/abs/2501.00032

Husom, E. J., Goknil, A., Astekin, M., Shar, L. K., Kåsen, A., Sen, S., Mithassel, B. A., & Soylu, A. (2024). *Sustainable LLM Inference for Edge AI: Evaluating Quantized LLMs for Energy Efficiency, Output Accuracy, and Inference Latency* (arXiv:2504.03360). arXiv. https://arxiv.org/abs/2504.03360

Jin, R., Du, J., Huang, W., Liu, W., Luan, J., Wang, B., & Xiong, D. (2024). A Comprehensive Evaluation of Quantization Strategies for Large Language Models. *Findings of the Association for Computational Linguistics: ACL 2024*, 12186–12215.

Kurtić, E., Marques, A., Pandit, S., Kurtz, M., & Alistarh, D. (2024). *"Give Me BF16 or Give Me Death"? Accuracy-Performance Trade-Offs in LLM Quantization* (arXiv:2411.02355). arXiv. https://arxiv.org/abs/2411.02355

Laskaridis, S., Katevas, K., Minto, L., & Haddadi, H. (2024). MELTing point: Mobile Evaluation of Language Transformers. *Proceedings of the 30th Annual International Conference on Mobile Computing and Networking (MobiCom ’24)*. https://doi.org/10.1145/3636534.3690668

Lin, J., Tang, J., Tang, H., Yang, S., Dang, X., Gan, C., & Han, S. (2023). AWQ: Activation-Aware Weight Quantization for On-Device LLM Compression and Acceleration. *Proceedings of Machine Learning and Systems (MLSys) 6*.

Liquid AI. (2025). *LFM2 Technical Report* (arXiv:2511.23404). arXiv. https://arxiv.org/abs/2511.23404

Lu, Z., Li, X., Cai, D., Yi, R., Liu, F., Liu, W., Luan, J., Zhang, X., Lane, N. D., & Xu, M. (2025). Demystifying Small Language Models for Edge Deployment. *Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (ACL 2025, Volume 1: Long Papers)*, 14747–14764. https://doi.org/10.18653/v1/2025.acl-long.718

Murthy, R., Yang, L., Tan, J., Awalgaonkar, T. M., Zhou, Y., Heinecke, S., Desai, S., Wu, J., Xu, R., Tan, S., Zhang, J., Liu, Z., Kokane, S., Liu, Z., Zhu, M., Wang, H., Xiong, C., & Savarese, S. (2024). *MobileAIBench: Benchmarking LLMs and LMMs for On-Device Use Cases* (arXiv:2406.10290). arXiv. https://arxiv.org/abs/2406.10290

Nurohim, A., Saifulloh, M., & Rahmawati, D. (2025). Analisis Komparatif *Large Language Models* DeepSeek dan Qwen dalam Klasifikasi Sentimen Berbahasa Indonesia. *Jurnal Teknologi Informasi dan Ilmu Komputer (JTIIK)*, 12(2), 235–246.

Prince, S. J. D. (2023). *Understanding Deep Learning*. The MIT Press. https://udlbook.github.io/udlbook/

Qwen Team. (2025). *Qwen3 Technical Report* (arXiv:2505.09388). arXiv. https://arxiv.org/abs/2505.09388

Ray, P., & Pradhan, T. (2026). Performance Analysis of Localised *Large Language Models* in Resource-Constrained Edge for Python and Rust APIs. *Internet of Things*, 31, 101324.

Sevim, B., & Ibrahim, M. (2024). *Large Language Models* (LLMs) Assisted Wireless Network Deployment in Urban Settings. *IEEE Vehicular Technology Conference (VTC2024-Fall)*, 1–6.

Tan, F., Lee, R., Dudziak, Ł., Hu, S. X., Bhattacharya, S., Hospedales, T., Tzimiropoulos, G., & Martinez, B. (2024). *MobileQuant: Mobile-friendly Quantization for On-device Language Models* (arXiv:2408.13933). arXiv. https://arxiv.org/abs/2408.13933

Touvron, H., Lavril, T., Izacard, G., Martinet, X., Lachaux, M.-A., Lacroix, T., Rozière, B., Goyal, N., Hambro, E., Azhar, F., Rodriguez, A., Joulin, A., Grave, E., & Lample, G. (2023). LLaMA: Open and Efficient Foundation Language Models. *arXiv preprint arXiv:2302.13971*.

Xiao, T., & Zhu, J. (2025). *Foundations of Large Language Models* (arXiv:2501.09223). arXiv. https://arxiv.org/abs/2501.09223

Zhan, H., Wei, S., He, Y., Liu, M., Gao, Y., Ma, Y., Yu, J., Wang, B., Yu, X., Zhang, S., & Wang, X. (2025). Quantized Large Language Models in Biomedical NLP: Evaluation and Recommendations. *npj Digital Medicine*, 8(1), 1–12.

Zhang, X., Nie, J., Huang, Y., Xie, G., Xiong, Z., Liu, J., Niyato, D., & Shen, X. (2024). Edge Intelligence Optimization for Large Language Model Inference with Batching and Quantization. *IEEE Wireless Communications*, 31(4), 12–18.

\newpage

# LAMPIRAN

Seluruh berkas lampiran juga diarsipkan sebagai berkas terpisah di direktori `docs/lampiran/` pada repositori penelitian (`f4rdani/Skripsi`), lengkap dengan `README.md` sebagai indeks (Lampiran A – E). Penyertaan berkas terpisah dimaksudkan agar penguji dapat membuka, menjalankan kembali, atau mengutip masing-masing lampiran tanpa harus memindai naskah PDF.

## Lampiran A, Skrip Otomatisasi `benchmark.sh` (Termux Android)

Skrip Bash berikut adalah versi `benchmark.sh` v4 yang dieksekusi pada perangkat Tecno Pova 5 (Termux *non-root*) untuk menghasilkan dataset `hasilv2.csv` yang menjadi dasar Tabel IV.2 dan Tabel IV.8. Skrip ini juga tersedia di repositori penelitian pada `docs/scripts/benchmark.sh`. Parameter inferensi dipilih agar dapat menjalankan kedua keluarga model, baik LFM 2.5 yang non-*reasoning* maupun Qwen 3.5 yang berkarakter *reasoning* dengan blok `<think>`,dalam anggaran token yang cukup.

```bash
#!/bin/bash
# ==============================================================================
# Skripsi Benchmark - Clean Manual Input v4
# Lingkungan : Termux (non-root) di Tecno Pova 5 (Helio G99, RAM 8 GB)
# Mesin      : llama.cpp build natif ARM
# Output     : hasilv2.csv  (lihat docs/data/hasilv2_raw.csv pada repositori)
# ==============================================================================

MODEL_DIR="/storage/emulated/0/Download/SLM"
LLAMA_CLI="$HOME/llama.cpp/build/bin/llama-cli"
CSV_FILE="hasilv2.csv"
THREADS=6

# Limit diperbesar agar Qwen Thinking tidak terpotong di tengah penalaran.
MAX_TOKENS=1024
CONTEXT_SIZE=2048

# Strong anti-thinking prompt, agar model fokus ke jawaban final.
PROMPT="### Instruction:
Explain briefly what artificial intelligence is.
Answer directly and concisely. Do not use Thinking Process,
reasoning steps, analysis, or lists. Give only the final answer
without any explanation of your thinking.

### Response:"

if [ ! -f "$CSV_FILE" ]; then
    echo "Timestamp,Model,Total Time (s),Prompt Speed (t/s),Gen Speed (t/s),Free RAM Start (MB),RAM Used (MB),CPU Peak (%),Question,Answer" > "$CSV_FILE"
fi

mapfile -t MODELS < <(ls "$MODEL_DIR"/*.gguf 2>/dev/null)
TOTAL_MODELS=${#MODELS[@]}

for i in "${!MODELS[@]}"; do
    MODEL="${MODELS[$i]}"
    NAME=$(basename "$MODEL")
    CURRENT_TIME=$(date "+%Y-%m-%d %H:%M:%S")

    TEMP_RAM=$(mktemp); TEMP_CPU=$(mktemp)
    echo "0" > "$TEMP_RAM"; echo "0" > "$TEMP_CPU"
    FREE_RAM_MB=$(grep MemAvailable /proc/meminfo | awk '{printf "%.2f", $2/1024}')
    START_TIME=$(date +%s)

    # Resource monitor: pantau VmRSS dan %CPU dari proses llama-cli setiap 0,5 s.
    monitor_resources() {
        PEAK_RAM=0; PEAK_CPU=0
        while true; do
            L_PID=$(pidof llama-cli 2>/dev/null | awk '{print $1}')
            [ -z "$L_PID" ] && L_PID=$(pgrep -x llama-cli | head -n 1)
            if [ -n "$L_PID" ]; then
                CUR_RAM=$(grep VmRSS /proc/$L_PID/status 2>/dev/null | awk '{print $2}')
                CUR_RAM=${CUR_RAM:-0}
                (( CUR_RAM > PEAK_RAM )) && { PEAK_RAM=$CUR_RAM; echo "$PEAK_RAM" > "$TEMP_RAM"; }
                CUR_CPU=$(ps -p $L_PID -o %cpu= 2>/dev/null | tr -d ' ')
                CUR_CPU=${CUR_CPU:-0}
                PEAK_CPU=$(awk -v c="$CUR_CPU" -v p="$PEAK_CPU" 'BEGIN {print (c>p)?c:p}')
                echo "$PEAK_CPU" > "$TEMP_CPU"
            fi
            sleep 0.5
        done
    }
    monitor_resources & MONITOR_PID=$!

    echo "/exit" | "$LLAMA_CLI" -m "$MODEL" \
        -p "$PROMPT" -n $MAX_TOKENS -t $THREADS -c $CONTEXT_SIZE \
        --temp 0.35 --top-p 0.9 --min-p 0.05 --repeat-penalty 1.1 \
        2>&1 | grep -A 500 "### Response:" | tee temp_output.log

    kill $MONITOR_PID 2>/dev/null
    END_TIME=$(date +%s); TOTAL_TIME=$((END_TIME-START_TIME))

    PEAK_RAM_KB=$(cat "$TEMP_RAM"); PEAK_CPU=$(cat "$TEMP_CPU")
    RAM_USED_MB=$(awk "BEGIN {printf \"%.2f\", ${PEAK_RAM_KB:-0} / 1024}")
    rm -f "$TEMP_RAM" "$TEMP_CPU"

    read -p "Prompt Speed (t/s)     -> " PROMPT_SPEED
    read -p "Generation Speed (t/s) -> " GEN_SPEED
    ANSWER=$(cat)

    [[ -z "$PROMPT_SPEED" ]] && PROMPT_SPEED="0.00"
    [[ -z "$GEN_SPEED" ]] && GEN_SPEED="0.00"
    SAFE_PROMPT="${PROMPT//\"/\"\"}"; SAFE_ANSWER="${ANSWER//\"/\"\"}"

    echo "$CURRENT_TIME,$NAME,$TOTAL_TIME,$PROMPT_SPEED,$GEN_SPEED,$FREE_RAM_MB,$RAM_USED_MB,$PEAK_CPU,\"$SAFE_PROMPT\",\"$SAFE_ANSWER\"" >> "$CSV_FILE"

    if [ $((i+1)) -lt $TOTAL_MODELS ]; then
        read -p "Press [ENTER] to continue to next model..."
    fi
done
```

## Lampiran B, Skrip Persiapan Model di PC (`quantize_pc.sh`)

Berkas `.gguf` yang dieksekusi di Lampiran A disiapkan terlebih dahulu pada PC dengan WSL2 Ubuntu dan GPU NVIDIA RTX 3060. Tahapan persiapan model, mulai dari mengunduh bobot HuggingFace, konversi `.safetensors` ke `F16.gguf`, hingga kuantisasi ke Q3/Q4/Q5\_K\_M, dirinci pada skrip `docs/scripts/quantize_pc.sh`. Ringkasan langkahnya adalah sebagai berikut.

```bash
# 1) Persiapan WSL Ubuntu + toolchain
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential git python3-pip python3-venv cmake \
                    nvidia-cuda-toolkit

# 2) Clone llama.cpp + virtualenv Python
git clone https://github.com/ggerganov/llama.cpp && cd llama.cpp
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt && pip install huggingface_hub

# 3) Build llama.cpp dengan akselerasi CUDA (RTX 3060)
cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release -j 4

# 4) Unduh bobot model dari HuggingFace dan konversi ke F16.gguf
huggingface-cli download Qwen/Qwen3.5-2B \
    --local-dir ./models/Qwen3.5-2B --local-dir-use-symlinks False
python3 convert_hf_to_gguf.py ./models/Qwen3.5-2B \
    --outtype f16 \
    --outfile ./models/Qwen3.5-2B/Qwen3.5-2B-F16.gguf

# 5) Kuantisasi F16.gguf -> Q3/Q4/Q5_K_M.gguf
for V in Q3_K_M Q4_K_M Q5_K_M; do
  ./build/bin/llama-quantize \
      ./models/Qwen3.5-2B/Qwen3.5-2B-F16.gguf \
      ./models/Qwen3.5-2B/Qwen3.5-2B-${V}.gguf "$V"
done

# 6) Unduh dataset WikiText-2 untuk evaluasi Perplexity (Tabel IV.3)
wget https://huggingface.co/datasets/ggml-org/ci/resolve/main/wikitext-2-raw-v1.zip
unzip wikitext-2-raw-v1.zip

# 7) Evaluasi Perplexity per varian
for V in F16 Q3_K_M Q4_K_M Q5_K_M; do
  ./build/bin/llama-perplexity \
      -m ./models/Qwen3.5-2B/Qwen3.5-2B-${V}.gguf \
      -f wikitext-2-raw/wiki.test.raw -c 512 -ngl 999
done

# 8) Transfer berkas .gguf ke perangkat Android (folder
#    /storage/emulated/0/Download/SLM), lalu jalankan Lampiran A di Termux.
```

## Lampiran C, Berkas Data dan Skrip Reproducibility

Seluruh berkas pendukung yang dirujuk pada bab Hasil dan Pembahasan diarsipkan pada repositori penelitian agar dapat direplikasi oleh penguji.

| Berkas | Lokasi pada Repositori | Keterangan |
|---|---|---|
| Raw CSV pengujian Android | `docs/data/hasilv2_raw.csv` | Hasil mentah `benchmark.sh` dari Tecno Pova 5. |
| Clean CSV (numeric-only) | `docs/data/hasilv2_clean.csv` | Versi tervalidasi untuk analisis statistik (N=3 per varian). |
| Aggregated CSV (rerata per varian) | `docs/data/hasilv2_aggregated.csv` | Sumber Tabel IV.2. |
| Output uji statistik LFM | `docs/data/statistical_tests_lfm.txt` | Sumber Tabel IV.8 (lihat Lampiran D). |
| Output uji statistik Qwen | `docs/data/statistical_tests_qwen.txt` | Sumber Tabel IV.9 (lihat Lampiran E). |
| Skrip persiapan model | `docs/scripts/quantize_pc.sh` | Eksekusi pada PC WSL Ubuntu. |
| Skrip *benchmark* Android | `docs/scripts/benchmark.sh` | Eksekusi pada Termux Tecno Pova 5. |
| Skrip uji statistik | `docs/scripts/statistical_tests.py` | Welch's *t*-test + one-way ANOVA. |
| Skrip pembuatan grafik | `docs/scripts/generate_charts.py` | Gambar IV.1 – Gambar IV.8. |
| Direktori lampiran terpisah | `docs/lampiran/` | Salinan berkas Lampiran A – E + `README.md` sebagai indeks. |

\newpage

## Lampiran D, Keluaran Uji Statistik LFM 2.5 (Sumber Tabel IV.8)

Keluaran lengkap skrip `docs/scripts/statistical_tests.py` untuk keluarga **LFM 2.5 (1,2B)**. Setiap blok metrik (Generation TPS, Prompt TPS, Peak RAM) berisi enam baris pasangan varian (Welch's *t*-test dua sampel, $\alpha = 0{,}05$) ditutup dengan baris one-way ANOVA antar empat varian. Cuplikan ini menjadi sumber **Tabel IV.8** pada Sub-bab 4.4.6.

```text
UJI STATISTIK ANTAR VARIAN KUANTISASI -- LFM 2.5 (1,2B) di Tecno Pova 5
Sumber: docs/data/hasilv2_clean.csv (n=3 ulangan per varian)
Metode: Welch's t-test (alpha=0,05) + one-way ANOVA
==============================================================================

## Metrik: Generation TPS
Pasangan               |    mean A |    mean B |       t |   p-value | hasil
----------------------------------------------------------------------------
F16 vs Q5_K_M          |      5.57 |     10.63 | -10.998 |    0.0044 | ** signifikan
F16 vs Q4_K_M          |      5.57 |     13.67 | -37.950 |    0.0000 | ** signifikan
F16 vs Q3_K_M          |      5.57 |     11.07 | -10.810 |    0.0051 | ** signifikan
Q5_K_M vs Q4_K_M       |     10.63 |     13.67 |  -6.435 |    0.0121 | ** signifikan
Q5_K_M vs Q3_K_M       |     10.63 |     11.07 |  -0.657 |    0.5477 | tidak signifikan
Q4_K_M vs Q3_K_M       |     13.67 |     11.07 |   5.014 |    0.0243 | ** signifikan
One-way ANOVA (4 varian): F=95.390, p=0.00000  ->  SIGNIFIKAN (p<0.05)

## Metrik: Prompt TPS
Pasangan               |    mean A |    mean B |       t |   p-value | hasil
----------------------------------------------------------------------------
F16 vs Q5_K_M          |     33.47 |     35.33 |  -0.400 |    0.7255 | tidak signifikan
F16 vs Q4_K_M          |     33.47 |     43.67 |  -2.088 |    0.1447 | tidak signifikan
F16 vs Q3_K_M          |     33.47 |     18.27 |   3.192 |    0.0708 | tidak signifikan
Q5_K_M vs Q4_K_M       |     35.33 |     43.67 |  -4.407 |    0.0221 | ** signifikan
Q5_K_M vs Q3_K_M       |     35.33 |     18.27 |  11.058 |    0.0008 | ** signifikan
Q4_K_M vs Q3_K_M       |     43.67 |     18.27 |  11.988 |    0.0004 | ** signifikan
One-way ANOVA (4 varian): F=17.072, p=0.00077  ->  SIGNIFIKAN (p<0.05)

## Metrik: Peak RAM (MB)
Pasangan               |    mean A |    mean B |       t |   p-value | hasil
----------------------------------------------------------------------------
F16 vs Q5_K_M          |   2303.47 |   1665.28 |  46.587 |    0.0000 | ** signifikan
F16 vs Q4_K_M          |   2303.47 |   1452.97 |  61.896 |    0.0000 | ** signifikan
F16 vs Q3_K_M          |   2303.47 |    911.97 |  97.789 |    0.0000 | ** signifikan
Q5_K_M vs Q4_K_M       |   1665.28 |   1452.97 |  15.049 |    0.0001 | ** signifikan
Q5_K_M vs Q3_K_M       |   1665.28 |    911.97 |  51.653 |    0.0000 | ** signifikan
Q4_K_M vs Q3_K_M       |   1452.97 |    911.97 |  36.996 |    0.0000 | ** signifikan
One-way ANOVA (4 varian): F=3297.733, p=0.00000  ->  SIGNIFIKAN (p<0.05)
```

\newpage

## Lampiran E, Keluaran Uji Statistik Qwen 3.5 (Sumber Tabel IV.9)

Keluaran lengkap skrip `docs/scripts/statistical_tests.py` untuk keluarga Qwen 3.5 (2 miliar parameter). Cuplikan ini menjadi sumber data untuk Tabel IV.9 pada Sub-bab 4.4.6.

```text
UJI STATISTIK ANTAR VARIAN KUANTISASI -- Qwen 3.5 (2B) di Tecno Pova 5
Sumber: docs/data/hasilv2_clean.csv (n=3 ulangan per varian).
Metode: Welch's t-test (alpha=0,05) + one-way ANOVA
==============================================================================

## Metrik: Generation TPS
Pasangan               |    mean A |    mean B |       t |   p-value | hasil
----------------------------------------------------------------------------
F16 vs Q5_K_M          |      1.87 |      4.60 | -12.505 |    0.0003 | ** signifikan
F16 vs Q4_K_M          |      1.87 |      4.95 | -15.691 |    0.0001 | ** signifikan
F16 vs Q3_K_M          |      1.87 |      4.25 |  -9.845 |    0.0012 | ** signifikan
Q5_K_M vs Q4_K_M       |      4.60 |      4.95 |  -1.552 |    0.1978 | tidak signifikan
Q5_K_M vs Q3_K_M       |      4.60 |      4.25 |   1.315 |    0.2603 | tidak signifikan
Q4_K_M vs Q3_K_M       |      4.95 |      4.25 |   2.819 |    0.0537 | tidak signifikan
One-way ANOVA (4 varian): F=71.249, p=0.00000  ->  SIGNIFIKAN (p<0.05)

## Metrik: Prompt TPS
Pasangan               |    mean A |    mean B |       t |   p-value | hasil
----------------------------------------------------------------------------
F16 vs Q5_K_M          |     22.70 |     22.55 |   0.123 |    0.9130 | tidak signifikan
F16 vs Q4_K_M          |     22.70 |     27.00 |  -2.230 |    0.0926 | tidak signifikan
F16 vs Q3_K_M          |     22.70 |     14.55 |   6.136 |    0.0107 | ** signifikan
Q5_K_M vs Q4_K_M       |     22.55 |     27.00 |  -2.951 |    0.0961 | tidak signifikan
Q5_K_M vs Q3_K_M       |     22.55 |     14.55 |  14.105 |    0.0029 | ** signifikan
Q4_K_M vs Q3_K_M       |     27.00 |     14.55 |   7.790 |    0.0079 | ** signifikan
One-way ANOVA (4 varian): F=26.722, p=0.00016  ->  SIGNIFIKAN (p<0.05)

## Metrik: Peak RAM (MB)
Pasangan               |    mean A |    mean B |       t |   p-value | hasil
----------------------------------------------------------------------------
F16 vs Q5_K_M          |   3744.25 |   2856.29 | 156.021 |    0.0000 | ** signifikan
F16 vs Q4_K_M          |   3744.25 |   2562.88 | 207.439 |    0.0000 | ** signifikan
F16 vs Q3_K_M          |   3744.25 |   1897.97 | 324.544 |    0.0000 | ** signifikan
Q5_K_M vs Q4_K_M       |   2856.29 |   2562.88 | 934.566 |    0.0000 | ** signifikan
Q5_K_M vs Q3_K_M       |   2856.29 |   1897.97 | 5710.088 |    0.0000 | ** signifikan
Q4_K_M vs Q3_K_M       |   2562.88 |   1897.97 | 2501.241 |    0.0000 | ** signifikan
One-way ANOVA (4 varian): F=72285.005, p=0.00000  ->  SIGNIFIKAN (p<0.05)
```
