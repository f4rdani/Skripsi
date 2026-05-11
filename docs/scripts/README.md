# Skripsi Benchmark Scripts

Skrip pendukung eksperimen Bab IV. Dirancang untuk perangkat **Tecno Pova 5
(MediaTek Helio G99, RAM 8 GB)** dengan lingkungan **Termux + llama.cpp**.

## File

| File | Fungsi |
|---|---|
| `benchmark.sh` | Eksekusi inferensi `llama-cli` untuk seluruh model GGUF di `$MODEL_DIR`. Multi-prompt × multi-run, log RAM/CPU/TPS/TTFT/suhu/baterai per run. Output: CSV per-run + log lengkap per run. |
| `summarize_results.py` | Aggregasi CSV per-run menjadi tabel `mean ± std` (per model dan per model×prompt). Output: CSV summary + Markdown table siap-tempel ke `skripsi.md`. |
| `generate_charts.py` | Render grafik Bab II / III / IV (matplotlib) dari data agregat. |

## Bug yang diperbaiki di v2

### Bug A — `Prompt Speed = 0` dan `Gen Speed = 0` (parsing)

v1 mencari pola **`"Prompt:"`** dan **`"Generation:"`** dari stdout `llama-cli`:

```bash
METRIC_LINE=$(grep -a "Prompt:" "$TEMP_LOG" | grep -a "Generation:" | tail -n 1)
```

Sejak llama.cpp ~2024 label kedua metrik tersebut diganti menjadi:

```
llama_perf_context_print: prompt eval time = 567.89 ms / 20 tokens (28.39 ms per token, 35.22 tokens per second)
llama_perf_context_print:        eval time = 12345.67 ms / 199 runs  (62.04 ms per token, 16.12 tokens per second)
```

Hasilnya `grep` tidak match apa pun → variabel kosong → fallback `0.00`. v2
memakai pola yang sesuai (`prompt eval time` / `eval time`) dan diuji terhadap
3 skenario (modern format, legacy `llama_print_timings`, log korup).

### Bug B — `peak_ram = 2.26 MB`, `cpu = 0%` (monitor PID salah)

v1 (dan v2 awal) memanggil llama-cli via pipa:

```bash
( echo "/exit" | "$LLAMA_CLI" ... ) > log &
LLAMA_PID=$!  # ← ini PID *subshell* pembungkus, bukan llama-cli!
```

Monitor `/proc/$LLAMA_PID/status` jadi memantau bash subshell (± 2 MB RSS,
0 % CPU). v2 fix-nya: jalankan llama-cli langsung tanpa pipa, stdin
ditutup via `</dev/null`.

### Bug C — Conversation-mode loop (`> > > >` spam)

llama-cli versi modern default-nya masuk *conversation mode* untuk model
chat: setelah respons pertama selesai, ia balik ke prompt `>` menunggu
user. Dengan `</dev/null`, setiap EOF dia print `>` lagi — looping.

v2 mengatasi dengan dua lapisan pertahanan:

1. **Auto-deteksi flag non-interactive** — saat startup, script jalankan
   `llama-cli --help` lalu cari salah satu dari `-no-cnv`,
   `--no-conversation`, atau `--single-turn`. Yang pertama match dipakai.
2. **Watchdog timeout** — setiap run dibatasi `RUN_TIMEOUT` detik (default
   300 s). Kalau llama-cli belum exit sampai timeout, dikirim `SIGTERM`,
   lalu `SIGKILL` setelah 5 detik. Script tetap lanjut ke run berikutnya.

## Pemakaian

### 1. Siapkan model di Android

Letakkan semua varian `.gguf` di satu folder (default `/storage/emulated/0/Download/SLM`):

```
/storage/emulated/0/Download/SLM/
├── LFM-2.5-1.2B-F16.gguf
├── LFM-2.5-1.2B-Q5_K_M.gguf
├── LFM-2.5-1.2B-Q4_K_M.gguf
├── LFM-2.5-1.2B-Q3_K_M.gguf
├── Qwen3.5-2B-F16.gguf
├── Qwen3.5-2B-Q5_K_M.gguf
├── Qwen3.5-2B-Q4_K_M.gguf
└── Qwen3.5-2B-Q3_K_M.gguf
```

### 2. (Opsional) Aktifkan termux-api untuk data baterai

```bash
pkg install termux-api
# di Android, install juga aplikasi "Termux:API" dari F-Droid / GitHub releases
termux-battery-status  # cek bekerja, harusnya keluar JSON
```

Tanpa termux-api, kolom baterai diisi `NA` (script tetap jalan).

### 3. Verifikasi cepat dulu (1 run)

Sebelum marathon 2-3 jam, pastikan parsing & monitor jalan dengan 1 run kilat:

```bash
RUNS_PER_PROMPT=1 \
COOLDOWN_BETWEEN_RUNS=5 \
COOLDOWN_BETWEEN_MODELS=5 \
MAX_TOKENS=64 \
bash benchmark.sh
```

Konfirmasi di output:
- `[info] llama-cli flag non-interactive: <flag>` — deteksi berhasil
- `prompt_tps`, `gen_tps`, `peak_ram` semua > 0
- Tidak ada `[WARN] TPS=0` atau `[watchdog] timeout`

Kalau ada `[WARN] TPS=0`, tail 30 baris log otomatis dicetak — share itu ke
Devin supaya regex parsing bisa di-update.

### 4. Run benchmark lengkap

```bash
cd ~  # atau lokasi yang convenient
bash /path/to/benchmark.sh
```

Override default kalau perlu:

```bash
RUNS_PER_PROMPT=3 \
COOLDOWN_BETWEEN_RUNS=90 \
COOLDOWN_BETWEEN_MODELS=300 \
MAX_TOKENS=200 \
RUN_TIMEOUT=600 \
bash benchmark.sh
```

Estimasi waktu (default: 3 prompt × 3 run = 9 run/model, 60s cooldown intra, 180s inter):
- Per run inferensi: ~20–150s tergantung model
- Per model: ~9×60s + 9×60s cooldown = ~18 menit
- 8 model + cooldown antar model: **±2,5 jam**

### 5. Ringkas hasil

```bash
python3 summarize_results.py ~/skripsi_benchmark_v2/raw_20250511_120000.csv
```

Output Markdown table langsung bisa di-paste ke `docs/skripsi.md` sebagai Tabel 4.2'
yang baru (dengan mean ± std).

## Data yang dicatat per run

| Kolom | Sumber | Catatan |
|---|---|---|
| `total_time_s` | `date +%s` start/end | Waktu wall-clock end-to-end |
| `prompt_tps` | `prompt eval time` line | Kecepatan pre-fill (token/s) |
| `gen_tps` | `eval time` line | Kecepatan generation (token/s) |
| `ttft_ms` | `prompt eval time = X ms` | Time-To-First-Token (latensi pre-fill) |
| `peak_ram_mb` | `/proc/PID/status` VmRSS | RAM aktual proses `llama-cli` (bukan sistem) |
| `idle_ram_mb` | `MemAvailable` saat start | RAM tersedia sistem sebelum run |
| `cpu_peak_pct` | `ps -p PID -o %cpu` | CPU usage proses (bisa > 100% untuk multi-thread) |
| `cpu_temp_peak_c` | `/sys/class/thermal/thermal_zone*/temp` | Suhu CPU tertinggi selama run (°C) |
| `bat_before_pct` / `bat_after_pct` | `termux-battery-status` | Konsumsi baterai per run |
| `bat_temp_delta_c` | `termux-battery-status` | Kenaikan suhu baterai |
| `n_prompt_tokens` / `n_eval_tokens` | metrics line | Jumlah token in/out (untuk validasi) |

## Troubleshooting

| Gejala | Kemungkinan penyebab | Fix |
|---|---|---|
| `[WARN] TPS=0 padahal llama-cli rc=0` + tail log tidak ada `prompt eval time` | Format output berbeda (build llama-cli aneh) | Share isi log ke Devin, regex perlu update |
| `[watchdog] timeout` di semua run | Auto-deteksi flag gagal, llama-cli masih masuk conversation-mode | Cek apa output `[info] llama-cli flag non-interactive: ...` di awal; kalau tidak ada, jalankan ulang `"$LLAMA_CLI" --help 2>&1 \| grep -iE 'conv\|turn\|cnv'` untuk lihat flag apa yang ada, lalu set `EXTRA_LLAMA_FLAGS="<flag-itu>"` |
| `peak_ram = 2.26 MB` atau angka kecil aneh | Monitor mengejar PID subshell (bug v1 / v2-awal) | Pastikan kamu pakai versi script terbaru yang panggil llama-cli langsung |
| `cpu_temp = 0.0` di semua run | `/sys/class/thermal/thermal_zone*/temp` tidak readable (Android non-root restrict) | Acceptable; nilai 0 berarti tidak ada akses, kolom bisa di-skip di skripsi |
| Semua kolom baterai `NA` | `termux-api` belum terpasang | Ikuti langkah "Aktifkan termux-api" di atas |

## Tips agar data lebih reliable

1. **Charge ≥ 80%** sebelum mulai — supaya tidak ada thermal throttling karena charging.
2. **Pesawat mode + WiFi off** — hilangkan beban background.
3. **Tutup semua app lain** dan tunggu 1–2 menit setelah unlock HP.
4. **Letakkan HP di permukaan dingin** (meja kayu/keramik), jangan di kasur/karpet.
5. **Jalankan via `tmux` atau `screen`** di Termux supaya tidak terputus kalau layar mati:
   ```bash
   pkg install tmux
   tmux new -s bench
   bash benchmark.sh
   # Ctrl-B D untuk detach
   tmux attach -t bench  # untuk lihat progress lagi
   ```
6. **Verifikasi 1 run dulu** dengan `RUNS_PER_PROMPT=1` sebelum menyalakan full 3×.

## Workflow lengkap dari raw -> skripsi

```bash
# 1. Run benchmark di HP (±2-3 jam)
bash benchmark.sh

# 2. Salin CSV ke laptop
# (pakai scp, USB-MTP, atau termux-setup-storage)

# 3. Generate summary table (di laptop)
python3 summarize_results.py raw_20250511_120000.csv > tabel_4_2_baru.md

# 4. Paste hasil ke docs/skripsi.md menggantikan Tabel 4.2 lama

# 5. Regenerate grafik dengan angka baru
python3 generate_charts.py

# 6. Build ulang DOCX/PDF
pandoc skripsi.md -o Skripsi_PTQ_SLM_Android.docx --toc --toc-depth=3 --resource-path=.
pandoc skripsi.md -o Skripsi_PTQ_SLM_Android.pdf  --pdf-engine=xelatex --toc --toc-depth=3 --resource-path=.
```
