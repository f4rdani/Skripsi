#!/bin/bash
# ============================================================================
# Skripsi Benchmark - Clean Manual Input v4
# Optimized for LFM2.5 (1.2B non-reasoning) and Qwen3.5 (2B reasoning)
#
# Script ini adalah versi "manual input" yang dipakai untuk menghasilkan
# docs/data/hasilv2.csv pada perangkat Tecno Pova 5 (MediaTek Helio G99, 8 GB
# RAM, Android 13, Termux non-root). Berbeda dengan benchmark.sh (v2) yang
# memparsing TPS otomatis dari "prompt eval time"/"eval time", versi ini
# meminta penulis menyalin angka TPS langsung dari layar Termux setelah
# inferensi selesai — pendekatan paling robust ketika label log llama.cpp
# berubah antar build atau fork.
#
# Perubahan vs v3:
#   1. MAX_TOKENS dinaikkan ke 1024 dan CONTEXT_SIZE ke 2048 supaya keluaran
#      Qwen 3.5 yang membangkitkan Thinking Process tidak terpotong di
#      tengah jalan.
#   2. CSV escaping standard (tanda kutip ganda di-escape ke "") supaya kolom
#      Question/Answer aman saat dibaca pandas/Excel.
# ============================================================================

MODEL_DIR="/storage/emulated/0/Download/SLM"
LLAMA_CLI="$HOME/llama.cpp/build/bin/llama-cli"
CSV_FILE="hasilv2.csv"
THREADS=6

# Limit diperbesar agar Qwen Thinking Process tidak terpotong di tengah.
MAX_TOKENS=1024
CONTEXT_SIZE=2048

# Strong anti-thinking prompt: dipakai agar perbandingan Qwen vs LFM tidak
# bias akibat blok <thinking>...</thinking>. Pada praktiknya Qwen 3.5 tetap
# membangkitkan reasoning trace internal walau diminta, sehingga total waktu
# Qwen tetap jauh lebih tinggi dari LFM (lihat Bab IV.4.2.3 skripsi).
PROMPT="### Instruction:
Explain briefly what artificial intelligence is.
Answer directly and concisely. Do not use Thinking Process, reasoning steps, analysis, or lists.
Give only the final answer without any explanation of your thinking.

### Response:"

echo "==============================================="
echo " Skripsi Benchmark - Clean Manual Mode"
echo " Optimized for LFM2.5 & Qwen3.5"
echo "==============================================="

if [ ! -f "$CSV_FILE" ]; then
    echo "Timestamp,Model,Total Time (s),Prompt Speed (t/s),Gen Speed (t/s),Free RAM Start (MB),RAM Used (MB),CPU Peak (%),Question,Answer" > "$CSV_FILE"
fi

mapfile -t MODELS < <(ls "$MODEL_DIR"/*.gguf 2>/dev/null)
TOTAL_MODELS=${#MODELS[@]}

echo "Found $TOTAL_MODELS models."
echo "==============================================="

for i in "${!MODELS[@]}"; do
    MODEL="${MODELS[$i]}"
    NAME=$(basename "$MODEL")

    CURRENT_TIME=$(date "+%Y-%m-%d %H:%M:%S")

    echo ""
    echo "[$((i+1))/$TOTAL_MODELS] $CURRENT_TIME"
    echo "Model: $NAME"

    TEMP_RAM=$(mktemp)
    TEMP_CPU=$(mktemp)
    echo "0" > "$TEMP_RAM"
    echo "0" > "$TEMP_CPU"

    FREE_RAM_MB=$(grep MemAvailable /proc/meminfo | awk '{printf "%.2f", $2/1024}')

    START_TIME=$(date +%s)

    # Resource Monitor: pantau VmRSS proses llama-cli + CPU% sampai exit.
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

    monitor_resources &
    MONITOR_PID=$!

    echo ""
    echo "=== QUESTION ==="
    echo "$PROMPT"
    echo ""
    echo "=== MODEL ANSWER ==="

    echo "/exit" | "$LLAMA_CLI" -m "$MODEL" \
        -p "$PROMPT" \
        -n $MAX_TOKENS \
        -t $THREADS \
        -c $CONTEXT_SIZE \
        --temp 0.35 \
        --top-p 0.9 \
        --min-p 0.05 \
        --repeat-penalty 1.1 \
        2>&1 | grep -A 500 "### Response:" | tee temp_output.log

    kill $MONITOR_PID 2>/dev/null
    END_TIME=$(date +%s)
    TOTAL_TIME=$((END_TIME-START_TIME))

    PEAK_RAM_KB=$(cat "$TEMP_RAM")
    PEAK_CPU=$(cat "$TEMP_CPU")
    RAM_USED_MB=$(awk "BEGIN {printf \"%.2f\", ${PEAK_RAM_KB:-0} / 1024}")

    rm -f "$TEMP_RAM" "$TEMP_CPU"

    echo ""
    echo "Enter data for this model:"
    read -p "Prompt Speed (t/s)     -> " PROMPT_SPEED
    read -p "Generation Speed (t/s) -> " GEN_SPEED

    echo ""
    echo "Paste Model Answer (then press ENTER, then Ctrl + D):"
    ANSWER=$(cat)

    # Default values
    [[ -z "$PROMPT_SPEED" ]] && PROMPT_SPEED="0.00"
    [[ -z "$GEN_SPEED" ]] && GEN_SPEED="0.00"

    # Standard CSV escaping: replace " with ""
    SAFE_PROMPT="${PROMPT//\"/\"\"}"
    SAFE_ANSWER="${ANSWER//\"/\"\"}"

    # Save to CSV
    echo "$CURRENT_TIME,$NAME,$TOTAL_TIME,$PROMPT_SPEED,$GEN_SPEED,$FREE_RAM_MB,$RAM_USED_MB,$PEAK_CPU,\"$SAFE_PROMPT\",\"$SAFE_ANSWER\"" >> "$CSV_FILE"

    echo "Saved: $NAME"

    if [ $((i+1)) -lt $TOTAL_MODELS ]; then
        echo ""
        read -p "Press [ENTER] to continue to next model..."
    fi
done

echo ""
echo "ALL TESTS COMPLETED."
echo "Results saved to: $CSV_FILE"
