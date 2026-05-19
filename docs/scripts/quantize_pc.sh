#!/bin/bash
# ==============================================================================
# Skripsi PTQ - Persiapan Model di PC (WSL Ubuntu + CUDA RTX 3060)
# ==============================================================================
# Workflow lengkap menyiapkan berkas .gguf F16 + 3 varian k-quants
# (Q3_K_M, Q4_K_M, Q5_K_M) dari bobot HuggingFace, untuk kemudian
# ditransfer ke perangkat Android (folder /storage/emulated/0/Download/SLM).
#
# Dieksekusi pada: Windows 11 + WSL2 Ubuntu, GPU NVIDIA RTX 3060.
# ==============================================================================

set -euo pipefail

# -----------------------------------------------------------------------------
# 0) Persiapan WSL Ubuntu (jalankan dari PowerShell sekali saja):
#       wsl.exe --install Ubuntu
# Kemudian masuk ke shell Ubuntu lalu jalankan langkah-langkah berikut.
# -----------------------------------------------------------------------------

# 1) Direktori kerja
mkdir -p ~/skripsi_kuantisasi
cd ~/skripsi_kuantisasi

# 2) Toolchain dasar
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential git python3-pip python3-venv cmake \
                    nvidia-cuda-toolkit

# 3) Clone llama.cpp + virtualenv Python
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
python3 -m venv venv
# shellcheck disable=SC1091
source venv/bin/activate
pip install -r requirements.txt
pip install huggingface_hub

# 4) Kompilasi llama.cpp dengan akselerasi CUDA (RTX 3060)
cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release -j 4

# 5) Unduh bobot model dari HuggingFace
#    (ganti $MODEL_REPO dan $LOCAL_DIR sesuai model yang ingin disiapkan)
MODEL_REPO="Qwen/Qwen3.5-2B"
LOCAL_DIR="./models/Qwen3.5-2B"

huggingface-cli download "$MODEL_REPO" \
    --local-dir "$LOCAL_DIR" \
    --local-dir-use-symlinks False

# 6) Konversi .safetensors -> F16.gguf
python3 convert_hf_to_gguf.py "$LOCAL_DIR" \
    --outtype f16 \
    --outfile "$LOCAL_DIR/Qwen3.5-2B-F16.gguf"

# 7) Kuantisasi F16 -> Q3_K_M, Q4_K_M, Q5_K_M
for VARIANT in Q3_K_M Q4_K_M Q5_K_M; do
    ./build/bin/llama-quantize \
        "$LOCAL_DIR/Qwen3.5-2B-F16.gguf" \
        "$LOCAL_DIR/Qwen3.5-2B-${VARIANT}.gguf" \
        "$VARIANT"
done

# 8) Verifikasi ukuran berkas (Tabel 4.1 di skripsi)
ls -lh "$LOCAL_DIR"/

# 9) Unduh dataset WikiText-2 untuk evaluasi Perplexity (Tabel 4.3)
wget https://huggingface.co/datasets/ggml-org/ci/resolve/main/wikitext-2-raw-v1.zip
unzip wikitext-2-raw-v1.zip

# 10) Evaluasi Perplexity per varian (jalankan untuk setiap berkas .gguf)
for VARIANT in F16 Q3_K_M Q4_K_M Q5_K_M; do
    ./build/bin/llama-perplexity \
        -m "$LOCAL_DIR/Qwen3.5-2B-${VARIANT}.gguf" \
        -f wikitext-2-raw/wiki.test.raw \
        -c 512 \
        -ngl 999
done

# 11) Transfer berkas .gguf ke perangkat Android via adb / Filebrowser /
#     copy manual ke folder /storage/emulated/0/Download/SLM pada HP.
#
# Setelah itu lanjut ke Termux di HP: jalankan docs/scripts/benchmark.sh.
# Akurasi MMLU/GSM8K/HumanEval/MT-Bench juga dijalankan di PC
# (skrip Python custom yang sumbernya identik dengan .gguf di HP).
