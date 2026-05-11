#!/data/data/com.termux/files/usr/bin/bash
# =============================================================================
# Skripsi PTQ Benchmark v2 — Tecno Pova 5 / Helio G99 / RAM 8 GB
# Lingkungan: Termux (non-root) + llama.cpp (build natif ARM)
# Author: f4rdani
# =============================================================================
# Perbaikan vs v1:
#   1. FIX BUG PARSING: v1 cari teks "Prompt:" / "Generation:" di stdout
#      llama-cli. Versi llama.cpp modern memakai label "prompt eval time" dan
#      "eval time", sehingga grep selalu gagal -> CSV terisi 0.00. v2 langsung
#      parse pola "X.XX tokens per second" dari kedua baris tersebut.
#   2. MULTI-RUN: setiap (model, prompt) dijalankan N=3 kali agar bisa dihitung
#      mean +/- std deviation (statistik robustness, request pembimbing umum).
#   3. MULTI-PROMPT: 3 prompt default (short EN, long EN, short ID) untuk
#      menghindari bias single-prompt; perilaku Qwen multilingual jadi terlihat.
#   4. THERMAL LOGGING: baca /sys/class/thermal/thermal_zone*/temp setiap detik
#      saat inferensi berjalan; catat peak temperature (millidegree -> Celsius).
#   5. TTFT (Time To First Token): diturunkan dari "prompt eval time" llama.cpp
#      sebagai latensi pre-fill; relevan untuk UX mobile.
#   6. BATTERY: snapshot sebelum/sesudah run via termux-battery-status (kalau
#      paket termux-api terpasang). Hitung delta % dan delta temperature.
#   7. PER-RUN CSV: setiap run jadi 1 baris (bukan 1 per model), supaya bisa
#      diolah ke mean+/-std oleh summarize_results.py.
#   8. ROBUSTNESS: PID llama-cli ditangkap langsung via $! (tidak pgrep guess),
#      cooldown intra-model dan inter-model terkonfigurasi terpisah.
# =============================================================================

set -u

# ---------------- KONFIGURASI ------------------------------------------------
MODEL_DIR="${MODEL_DIR:-/storage/emulated/0/Download/SLM}"
LLAMA_CLI="${LLAMA_CLI:-$HOME/llama.cpp/build/bin/llama-cli}"
OUT_DIR="${OUT_DIR:-$HOME/skripsi_benchmark_v2}"
RUN_TAG="$(date '+%Y%m%d_%H%M%S')"
RAW_CSV="$OUT_DIR/raw_${RUN_TAG}.csv"        # 1 baris = 1 run
RAW_LOG_DIR="$OUT_DIR/logs_${RUN_TAG}"        # stdout llama-cli per run

THREADS=${THREADS:-6}
MAX_TOKENS=${MAX_TOKENS:-200}
CTX_SIZE=${CTX_SIZE:-512}
TEMP=${TEMP:-0.5}
TOP_P=${TOP_P:-0.9}
REP_PEN=${REP_PEN:-1.1}
# Flag tambahan untuk llama-cli. Default kosong; bisa di-override mis.
#   EXTRA_LLAMA_FLAGS="--no-conversation" bash benchmark.sh
# untuk versi llama.cpp yang default-nya masuk conversation mode.
EXTRA_LLAMA_FLAGS=${EXTRA_LLAMA_FLAGS:-}

RUNS_PER_PROMPT=${RUNS_PER_PROMPT:-3}         # N=3 untuk mean+/-std
COOLDOWN_BETWEEN_RUNS=${COOLDOWN_BETWEEN_RUNS:-60}  # detik antar run dalam model yang sama
COOLDOWN_BETWEEN_MODELS=${COOLDOWN_BETWEEN_MODELS:-180} # detik antar model

# Prompt set (tambah/kurangi bebas). Format: "label|text"
PROMPTS=(
  "EN_short|### Instruction:
Explain briefly what artificial intelligence is.

### Response:"
  "EN_long|### Instruction:
Write a clear three-paragraph explanation of how post-training quantization reduces the memory footprint of large language models while preserving most of their accuracy. Mention bit-width, weight outliers, and edge-device deployment.

### Response:"
  "ID_short|### Instruksi:
Jelaskan secara singkat apa itu kecerdasan buatan.

### Tanggapan:"
)

mkdir -p "$OUT_DIR" "$RAW_LOG_DIR"

# Header CSV (per-run granularity)
if [ ! -f "$RAW_CSV" ]; then
  echo "timestamp,model,prompt_label,run_idx,total_time_s,prompt_tps,gen_tps,ttft_ms,peak_ram_mb,idle_ram_mb,cpu_peak_pct,cpu_temp_peak_c,bat_before_pct,bat_after_pct,bat_temp_delta_c,n_eval_tokens,n_prompt_tokens" > "$RAW_CSV"
fi

# ---------------- HELPER FUNCTIONS -------------------------------------------

# Ambil suhu CPU dari semua thermal_zone yang accessible (millidegree C)
read_cpu_temp_c() {
  local max_t=0
  for z in /sys/class/thermal/thermal_zone*/temp; do
    [ -r "$z" ] || continue
    local t
    t=$(cat "$z" 2>/dev/null)
    [[ "$t" =~ ^[0-9]+$ ]] || continue
    (( t > max_t )) && max_t=$t
  done
  # millidegree -> Celsius float
  awk -v t="$max_t" 'BEGIN { printf "%.1f", t/1000 }'
}

# Snapshot battery via termux-api; output "pct,temp_c" atau "NA,NA"
battery_snapshot() {
  if command -v termux-battery-status >/dev/null 2>&1; then
    local json pct temp
    json=$(termux-battery-status 2>/dev/null)
    pct=$(echo "$json" | sed -nE 's/.*"percentage":\s*([0-9]+).*/\1/p' | head -n1)
    temp=$(echo "$json" | sed -nE 's/.*"temperature":\s*([0-9.]+).*/\1/p' | head -n1)
    pct=${pct:-NA}; temp=${temp:-NA}
    echo "$pct,$temp"
  else
    echo "NA,NA"
  fi
}

# Monitor resource pakai PID konkret (bukan tebak via pgrep)
# Args: $1=PID, $2=ram_file, $3=cpu_file, $4=temp_file
monitor_resources() {
  local target_pid="$1" ram_file="$2" cpu_file="$3" temp_file="$4"
  local peak_ram=0 peak_cpu=0 peak_temp=0
  echo "0" > "$ram_file"; echo "0" > "$cpu_file"; echo "0.0" > "$temp_file"
  while kill -0 "$target_pid" 2>/dev/null; do
    if [ -r "/proc/$target_pid/status" ]; then
      local cur_ram
      cur_ram=$(grep -E '^VmRSS:' "/proc/$target_pid/status" 2>/dev/null | awk '{print $2}')
      cur_ram=${cur_ram:-0}
      (( cur_ram > peak_ram )) && { peak_ram=$cur_ram; echo "$peak_ram" > "$ram_file"; }
    fi
    local cur_cpu
    cur_cpu=$(ps -p "$target_pid" -o %cpu= 2>/dev/null | awk '{print $1}')
    cur_cpu=${cur_cpu:-0}
    peak_cpu=$(awk -v c="$cur_cpu" -v p="$peak_cpu" 'BEGIN {if (c > p) print c; else print p}')
    echo "$peak_cpu" > "$cpu_file"
    local cur_temp
    cur_temp=$(read_cpu_temp_c)
    peak_temp=$(awk -v c="$cur_temp" -v p="$peak_temp" 'BEGIN {if (c > p) print c; else print p}')
    echo "$peak_temp" > "$temp_file"
    sleep 0.5
  done
}

# Parse metrik dari output llama-cli.
# Pola yang dicari (llama.cpp 2024+):
#   "... prompt eval time = X ms / N tokens (Y ms per token, TPS tokens per second)"
#   "... eval time        = X ms / N runs   (Y ms per token, TPS tokens per second)"
# Fallback: pola lama "llama_print_timings:".
# Args: $1 = log file. Echo: "prompt_tps gen_tps ttft_ms n_prompt n_eval"
parse_llama_metrics() {
  local log="$1"
  local p_line e_line
  p_line=$(grep -aE 'prompt eval time' "$log" | tail -n 1)
  e_line=$(grep -aE 'eval time' "$log" | grep -v 'prompt eval' | tail -n 1)

  # Ekstrak TPS (tokens per second) dari masing-masing baris
  local p_tps g_tps ttft_ms n_prompt n_eval
  p_tps=$(echo "$p_line" | sed -nE 's/.*\(.*,[[:space:]]*([0-9.]+)[[:space:]]+tokens per second.*/\1/p')
  g_tps=$(echo "$e_line" | sed -nE 's/.*\(.*,[[:space:]]*([0-9.]+)[[:space:]]+tokens per second.*/\1/p')

  # TTFT (ms) = total "prompt eval time" yaitu angka pertama di baris itu
  ttft_ms=$(echo "$p_line" | sed -nE 's/.*=[[:space:]]*([0-9.]+)[[:space:]]+ms[[:space:]]*\/.*/\1/p')

  # Jumlah token prompt & generation
  n_prompt=$(echo "$p_line" | sed -nE 's/.*\/[[:space:]]*([0-9]+)[[:space:]]+tokens.*/\1/p')
  n_eval=$(echo  "$e_line" | sed -nE 's/.*\/[[:space:]]*([0-9]+)[[:space:]]+runs.*/\1/p')

  echo "${p_tps:-0} ${g_tps:-0} ${ttft_ms:-0} ${n_prompt:-0} ${n_eval:-0}"
}

# ---------------- MAIN LOOP --------------------------------------------------

mapfile -t MODELS < <(ls -1 "$MODEL_DIR"/*.gguf 2>/dev/null)
TOTAL_MODELS=${#MODELS[@]}

if [ "$TOTAL_MODELS" -eq 0 ]; then
  echo "[ERROR] Tidak ada *.gguf di $MODEL_DIR. Set MODEL_DIR sebelum jalan."
  exit 1
fi

echo "==============================================="
echo " Skripsi Benchmark v2 — $TOTAL_MODELS model"
echo " Threads=$THREADS Tokens=$MAX_TOKENS Ctx=$CTX_SIZE"
echo " Runs/prompt=$RUNS_PER_PROMPT  Prompts=${#PROMPTS[@]}"
echo " Output: $RAW_CSV"
echo "==============================================="

for m_idx in "${!MODELS[@]}"; do
  MODEL="${MODELS[$m_idx]}"
  MODEL_NAME=$(basename "$MODEL")
  echo ""
  echo "============================================================"
  echo " [$((m_idx+1))/$TOTAL_MODELS] $MODEL_NAME"
  echo "============================================================"

  for p_entry in "${PROMPTS[@]}"; do
    P_LABEL="${p_entry%%|*}"
    P_TEXT="${p_entry#*|}"

    for ((r=1; r<=RUNS_PER_PROMPT; r++)); do
      TS=$(date '+%Y-%m-%d %H:%M:%S')
      RUN_LOG="$RAW_LOG_DIR/${MODEL_NAME}__${P_LABEL}__run${r}.log"

      echo "----"
      echo "[$TS] $MODEL_NAME | prompt=$P_LABEL | run=$r/$RUNS_PER_PROMPT"

      # Snapshot kondisi awal
      IDLE_RAM_KB=$(grep MemAvailable /proc/meminfo | awk '{print $2}')
      IDLE_RAM_MB=$(awk -v k="$IDLE_RAM_KB" 'BEGIN { printf "%.2f", k/1024 }')
      BAT_BEFORE=$(battery_snapshot)
      BAT_BEFORE_PCT="${BAT_BEFORE%%,*}"
      BAT_BEFORE_TEMP="${BAT_BEFORE##*,}"

      TEMP_RAM=$(mktemp); TEMP_CPU=$(mktemp); TEMP_T=$(mktemp)
      START=$(date +%s)

      # Jalankan llama-cli langsung di background.
      # PENTING: tanpa pipa `echo "/exit" | ...`, supaya $! = PID llama-cli,
      # bukan PID subshell pembungkus. </dev/null untuk paksa EOF di stdin
      # (gantikan fungsi "/exit" pada v1) sehingga llama-cli tidak masuk
      # mode interaktif.
      "$LLAMA_CLI" -m "$MODEL" \
            -p "$P_TEXT" \
            -n "$MAX_TOKENS" \
            -t "$THREADS" \
            -c "$CTX_SIZE" \
            --temp "$TEMP" \
            --top-p "$TOP_P" \
            --repeat-penalty "$REP_PEN" \
            --no-warmup \
            $EXTRA_LLAMA_FLAGS \
            </dev/null > "$RUN_LOG" 2>&1 &
      LLAMA_PID=$!

      monitor_resources "$LLAMA_PID" "$TEMP_RAM" "$TEMP_CPU" "$TEMP_T" &
      MON_PID=$!

      wait "$LLAMA_PID"
      LLAMA_RC=$?
      kill "$MON_PID" 2>/dev/null
      wait "$MON_PID" 2>/dev/null

      END=$(date +%s)
      TOTAL_T=$((END-START))

      PEAK_RAM_KB=$(cat "$TEMP_RAM" 2>/dev/null); PEAK_RAM_KB=${PEAK_RAM_KB:-0}
      PEAK_CPU=$(cat "$TEMP_CPU" 2>/dev/null);    PEAK_CPU=${PEAK_CPU:-0}
      PEAK_TEMP=$(cat "$TEMP_T" 2>/dev/null);     PEAK_TEMP=${PEAK_TEMP:-0}
      PEAK_RAM_MB=$(awk -v k="$PEAK_RAM_KB" 'BEGIN { printf "%.2f", k/1024 }')
      rm -f "$TEMP_RAM" "$TEMP_CPU" "$TEMP_T"

      read -r P_TPS G_TPS TTFT_MS N_PROMPT N_EVAL <<<"$(parse_llama_metrics "$RUN_LOG")"

      BAT_AFTER=$(battery_snapshot)
      BAT_AFTER_PCT="${BAT_AFTER%%,*}"
      BAT_AFTER_TEMP="${BAT_AFTER##*,}"
      if [[ "$BAT_BEFORE_TEMP" != "NA" && "$BAT_AFTER_TEMP" != "NA" ]]; then
        BAT_DTEMP=$(awk -v a="$BAT_AFTER_TEMP" -v b="$BAT_BEFORE_TEMP" 'BEGIN { printf "%.2f", a-b }')
      else
        BAT_DTEMP="NA"
      fi

      echo "$TS,$MODEL_NAME,$P_LABEL,$r,$TOTAL_T,$P_TPS,$G_TPS,$TTFT_MS,$PEAK_RAM_MB,$IDLE_RAM_MB,$PEAK_CPU,$PEAK_TEMP,$BAT_BEFORE_PCT,$BAT_AFTER_PCT,$BAT_DTEMP,$N_EVAL,$N_PROMPT" >> "$RAW_CSV"

      echo "  -> total=${TOTAL_T}s prompt_tps=$P_TPS gen_tps=$G_TPS ttft=${TTFT_MS}ms"
      echo "     peak_ram=${PEAK_RAM_MB}MB cpu=${PEAK_CPU}% cpu_temp=${PEAK_TEMP}C bat_dT=${BAT_DTEMP}C rc=$LLAMA_RC"

      # Diagnostic: kalau parsing menghasilkan 0 padahal llama-cli sukses,
      # cetak ekor log supaya format aslinya terlihat tanpa harus dump manual
      if [[ "$P_TPS" == "0" && "$G_TPS" == "0" && "$LLAMA_RC" == "0" && "$TOTAL_T" -gt 2 ]]; then
        echo "     [WARN] TPS=0 padahal llama-cli rc=0. 30 baris terakhir log:"
        tail -n 30 "$RUN_LOG" 2>/dev/null | sed 's/^/      | /'
      fi

      if (( r < RUNS_PER_PROMPT )) || [[ "$p_entry" != "${PROMPTS[-1]}" ]]; then
        echo "  cooldown ${COOLDOWN_BETWEEN_RUNS}s ..."
        sleep "$COOLDOWN_BETWEEN_RUNS"
      fi
    done
  done

  if (( m_idx+1 < TOTAL_MODELS )); then
    echo ""
    echo "Selesai $MODEL_NAME. Cooldown ${COOLDOWN_BETWEEN_MODELS}s sebelum model berikutnya..."
    echo "(Tekan Ctrl-C kalau mau intervensi manual)"
    sleep "$COOLDOWN_BETWEEN_MODELS"
  fi

done

echo ""
echo "============================================================"
echo " SELESAI. Raw CSV: $RAW_CSV"
echo " Log per-run    : $RAW_LOG_DIR/"
echo " Jalankan: python3 summarize_results.py $RAW_CSV"
echo "============================================================"
