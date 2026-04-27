# Penjelasan Gambar BAB IV

Catatan ini menjelaskan tujuan dan isi gambar pada BAB IV.

**Status saat ini:** Folder ini berisi **placeholder** dengan data ilustrasi (mock data). Setelah Anda menyetorkan data benchmark aktual, dua placeholder ini akan diregenerate menjadi Gambar 4.3 (radar) dan Gambar 4.5 (Pareto), bersama tambahan Gambar 4.1 (storage), Gambar 4.2 (RAM), dan Gambar 4.4 (TPS).

---

## Gambar 4.X — `4.X_radar_placeholder.png` (PLACEHOLDER)
**Judul lengkap nanti:** Gambar 4.3 Diagram Radar Kapabilitas & Efisiensi per Model.

**Maksud / pesan utama.** Membandingkan empat varian (FP16, Q5_K_M, Q4_K_M, Q3_K_M) pada **tujuh sumbu** sekaligus, sehingga pembaca dapat melihat seketika varian mana yang menyeimbangkan efisiensi dan kualitas paling baik. Sumbu yang berkonsep "lebih kecil lebih baik" (PPL) dipresentasikan sebagai PPL inversi (1/PPL) supaya semua sumbu memiliki interpretasi searah ("lebih luas = lebih baik").

**Komponen yang ditampilkan.**
- 7 sumbu: Storage (efficiency), RAM (efficiency), TPS-Gen (efficiency), MMLU, GSM8k, HumanEval, PPL inv.
- 4 area berwarna: FP16 (abu-abu, dominan akurasi tetapi tipis efficiency), Q5_K_M (hijau), Q4_K_M (oranye), Q3_K_M (merah, dominan efisiensi).

**Kapan dirujuk.** Sub-bab 4.3 (radar capability) atau 4.5 (komposit), tergantung penempatan akhir.

**Catatan penting.** Angka pada placeholder adalah **dummy** yang hanya memperlihatkan layout target. JANGAN dikutip sebagai hasil aktual.

---

## Gambar 4.Y — `4.Y_pareto_placeholder.png` (PLACEHOLDER)
**Judul lengkap nanti:** Gambar 4.5 Pareto Plot Storage × Composite Accuracy × Peak RAM.

**Maksud / pesan utama.** Memetakan **trade-off tiga sumbu**:
- Sumbu X: relative storage (lebih kiri = lebih hemat).
- Sumbu Y: composite accuracy (lebih atas = lebih baik).
- Ukuran marker: peak RAM (lebih kecil = lebih hemat RAM).

Varian yang **tidak terdominasi** (tidak ada varian lain yang lebih baik di semua sumbu) berada di **Pareto frontier** dan menjadi rekomendasi akhir penelitian (jawaban RQ4).

**Komponen yang ditampilkan.**
- 4 titik: FP16, Q5_K_M, Q4_K_M, Q3_K_M dengan marker dan ukuran berbeda.
- Legend di kanan bawah dengan ukuran marker proporsional dengan peak RAM.

**Kapan dirujuk.** Sub-bab 4.5 Diskusi / Analisis Komparatif Keseluruhan.

**Catatan penting.** Angka pada placeholder adalah **dummy**. JANGAN dikutip sebagai hasil aktual.

---

## Daftar gambar BAB IV final (akan dibuat saat data masuk)
| Gambar | Tipe | Tujuan |
|---|---|---|
| 4.1 Storage | bar chart | jawab RQ1 (efisiensi penyimpanan) |
| 4.2 Peak RAM | bar chart + ambang 8 GB | jawab RQ3 bagian RAM |
| 4.3 Radar | radar (7 sumbu) | rangkuman holistik per model |
| 4.4 TPS | bar chart prompt + gen | jawab RQ3 bagian throughput |
| 4.5 Pareto | scatter 3-sumbu | jawab RQ4 (Pareto-optimal) |
