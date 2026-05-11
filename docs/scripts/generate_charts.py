"""Generate charts (PNG) for BAB IV based on benchmark data from the skripsi.

Run: python3 generate_charts.py
Output: PNG files in docs/gambar/
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "gambar"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
    "figure.dpi": 150,
})

QUANTS = ["F16", "Q5_K_M", "Q4_K_M", "Q3_K_M"]
COLOR_LFM = "#1f77b4"
COLOR_QWEN = "#d62728"


def save(fig, name):
    path = OUT / name
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"  wrote {path}")


# ---------------------------------------------------------------------------
# Gambar 4.1 -- Ukuran berkas (MB) per varian kuantisasi
# ---------------------------------------------------------------------------
lfm_size_mb = [2252.8, 805, 698, 573]      # FP16 = 2.2 GB -> 2252.8 MB
qwen_size_mb = [3686.4, 1433.6, 1228.8, 1126.4]  # 3.6/1.4/1.2/1.1 GB

x = np.arange(len(QUANTS))
width = 0.38
fig, ax = plt.subplots(figsize=(8, 4.8))
b1 = ax.bar(x - width / 2, lfm_size_mb, width, label="LFM 2.5 (1.2B)", color=COLOR_LFM)
b2 = ax.bar(x + width / 2, qwen_size_mb, width, label="Qwen 3.5 (2B)", color=COLOR_QWEN)
ax.set_xticks(x, QUANTS)
ax.set_ylabel("Ukuran Berkas (MB)")
ax.set_title("Reduksi Ukuran Berkas Model per Varian Kuantisasi")
ax.legend(loc="upper right")
ax.grid(axis="y", linestyle="--", alpha=0.4)
for bars in (b1, b2):
    ax.bar_label(bars, fmt="%.0f", padding=2, fontsize=9)
ax.set_ylim(0, max(qwen_size_mb) * 1.18)
save(fig, "4_1_ukuran_berkas.png")


# ---------------------------------------------------------------------------
# Gambar 4.2 -- Kecepatan inferensi (Prompt vs Generation) per varian
# ---------------------------------------------------------------------------
# Rerata Tecno Pova 5 (Tabel 4.2)
prompt_lfm = [33.47, 35.33, 43.67, 18.27]
gen_lfm = [5.57, 10.63, 13.67, 11.07]
prompt_qwen = [22.70, 22.55, 27.00, 14.55]
gen_qwen = [1.87, 4.60, 4.95, 4.25]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.6), sharey=False)
for ax, prompt, gen, title in [
    (ax1, prompt_lfm, gen_lfm, "LFM 2.5 (1.2B)"),
    (ax2, prompt_qwen, gen_qwen, "Qwen 3.5 (2B)"),
]:
    ax.plot(QUANTS, prompt, marker="o", linewidth=2, label="Prompt Speed (t/s)", color="#2ca02c")
    ax.plot(QUANTS, gen, marker="s", linewidth=2, label="Generation Speed (t/s)", color="#ff7f0e")
    for xi, yi in enumerate(prompt):
        ax.annotate(f"{yi:.2f}", (xi, yi), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=9)
    for xi, yi in enumerate(gen):
        ax.annotate(f"{yi:.2f}", (xi, yi), textcoords="offset points", xytext=(0, -14), ha="center", fontsize=9)
    ax.set_title(title)
    ax.set_xlabel("Varian Kuantisasi")
    ax.set_ylabel("Tokens per Second (t/s)")
    ax.grid(linestyle="--", alpha=0.4)
    ax.legend(loc="upper right")

fig.suptitle("Kecepatan Inferensi (Prompt vs Generation) per Varian Kuantisasi", fontsize=13, fontweight="bold")
save(fig, "4_2_kecepatan_inferensi.png")


# ---------------------------------------------------------------------------
# Gambar 4.3 -- Konsumsi RAM (Peak) per varian kuantisasi
# ---------------------------------------------------------------------------
# Peak RAM rerata Tecno Pova 5 (Tabel 4.2)
peak_lfm = [2303.47, 1665.28, 1452.97, 911.97]
peak_qwen = [3744.25, 2856.29, 2562.88, 1897.97]

fig, ax = plt.subplots(figsize=(8, 4.8))
b1 = ax.bar(x - width / 2, peak_lfm, width, label="LFM 2.5 (1.2B)", color=COLOR_LFM)
b2 = ax.bar(x + width / 2, peak_qwen, width, label="Qwen 3.5 (2B)", color=COLOR_QWEN)
ax.set_xticks(x, QUANTS)
ax.set_ylabel("Peak RAM (MB)")
ax.set_title("Konsumsi Peak RAM per Varian Kuantisasi (Helio G99, 8GB)")
ax.legend(loc="upper right")
ax.grid(axis="y", linestyle="--", alpha=0.4)
for bars in (b1, b2):
    ax.bar_label(bars, fmt="%.0f", padding=2, fontsize=9)
ax.set_ylim(0, max(peak_qwen) * 1.18)
save(fig, "4_3_konsumsi_ram.png")


# ---------------------------------------------------------------------------
# Gambar 4.4 -- Perplexity WikiText-2 per varian kuantisasi
# ---------------------------------------------------------------------------
ppl_lfm = [12.6829, 12.8297, 13.2145, 14.5135]
ppl_qwen = [12.7763, 13.0856, 13.3617, 15.2172]

fig, ax = plt.subplots(figsize=(8, 4.6))
ax.plot(QUANTS, ppl_lfm, marker="o", linewidth=2, label="LFM 2.5 (1.2B)", color=COLOR_LFM)
ax.plot(QUANTS, ppl_qwen, marker="s", linewidth=2, label="Qwen 3.5 (2B)", color=COLOR_QWEN)
for xi, yi in enumerate(ppl_lfm):
    ax.annotate(f"{yi:.3f}", (xi, yi), textcoords="offset points", xytext=(0, 9), ha="center", fontsize=9, color=COLOR_LFM)
for xi, yi in enumerate(ppl_qwen):
    ax.annotate(f"{yi:.3f}", (xi, yi), textcoords="offset points", xytext=(0, -14), ha="center", fontsize=9, color=COLOR_QWEN)
ax.set_xlabel("Varian Kuantisasi")
ax.set_ylabel("Perplexity (lebih rendah = lebih baik)")
ax.set_title("Degradasi Perplexity pada Dataset WikiText-2")
ax.legend(loc="upper left")
ax.grid(linestyle="--", alpha=0.4)
save(fig, "4_4_perplexity.png")


# ---------------------------------------------------------------------------
# Gambar 4.5 -- Akurasi benchmark (MMLU/GSM8K/HumanEval)
# ---------------------------------------------------------------------------
benchmarks = ["MMLU", "GSM8K", "HumanEval"]
lfm_acc = {
    "F16":    [33, 52, 36],
    "Q5_K_M": [30, 52, 29],
    "Q4_K_M": [28, 51, 37],
    "Q3_K_M": [32, 42, 30],
}
qwen_acc = {
    "F16":    [12, 57, 52],
    "Q5_K_M": [14, 53, 47],
    "Q4_K_M": [14, 56, 44],
    "Q3_K_M": [22, 37, 26],
}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5), sharey=True)
xb = np.arange(len(benchmarks))
w = 0.20
palette = ["#1f77b4", "#2ca02c", "#ff7f0e", "#d62728"]

for ax, dataset, title in [(ax1, lfm_acc, "LFM 2.5 (1.2B)"), (ax2, qwen_acc, "Qwen 3.5 (2B)")]:
    for i, q in enumerate(QUANTS):
        offs = (i - 1.5) * w
        bars = ax.bar(xb + offs, dataset[q], w, label=q, color=palette[i])
        ax.bar_label(bars, fmt="%d%%", padding=2, fontsize=8)
    ax.set_xticks(xb, benchmarks)
    ax.set_ylabel("Akurasi (%)")
    ax.set_title(title)
    ax.set_ylim(0, max(max(qwen_acc.values(), key=max)) + 18)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.legend(title="Varian", loc="upper right", ncol=2, fontsize=9)

fig.suptitle("Hasil Benchmark Akurasi (MMLU, GSM8K, HumanEval)", fontsize=13, fontweight="bold")
save(fig, "4_5_akurasi_benchmark.png")


# ---------------------------------------------------------------------------
# Gambar 4.6 -- Radar/Trade-off (efisiensi normalisasi)
# ---------------------------------------------------------------------------
# Normalize: higher is better. Use Q4_K_M-centric comparison vs F16 baseline.
# Dimensions: Storage Eff., RAM Eff., Gen Speed, Prompt Speed, 1/Perplexity, Akurasi rata-rata.
def norm(vals):
    arr = np.asarray(vals, dtype=float)
    lo, hi = arr.min(), arr.max()
    if hi - lo < 1e-9:
        return np.ones_like(arr)
    return (arr - lo) / (hi - lo)

# build per-variant scores using LFM data (representative)
storage_eff = norm([1 / s for s in lfm_size_mb])      # smaller is better -> invert
ram_eff = norm([1 / r for r in peak_lfm])
gen_speed = norm(gen_lfm)
prompt_speed = norm(prompt_lfm)
ppl_inv = norm([1 / p for p in ppl_lfm])
acc_mean = norm([(a + b + c) / 3 for a, b, c in zip(lfm_acc["F16"], lfm_acc["Q5_K_M"], lfm_acc["Q4_K_M"])])  # placeholder
# rebuild acc_mean properly per variant
acc_per_variant = [np.mean(lfm_acc[q]) for q in QUANTS]
acc_mean = norm(acc_per_variant)

dims = ["Storage Eff.", "RAM Eff.", "Gen Speed", "Prompt Speed", "1/Perplexity", "Akurasi Rata-rata"]
data = np.vstack([storage_eff, ram_eff, gen_speed, prompt_speed, ppl_inv, acc_mean]).T  # rows: variants

angles = np.linspace(0, 2 * np.pi, len(dims), endpoint=False).tolist()
angles += angles[:1]

fig, ax = plt.subplots(figsize=(7.5, 7.5), subplot_kw=dict(polar=True))
for i, q in enumerate(QUANTS):
    vals = data[i].tolist() + data[i][:1].tolist()
    ax.plot(angles, vals, linewidth=2, label=q, color=palette[i])
    ax.fill(angles, vals, alpha=0.10, color=palette[i])
ax.set_xticks(angles[:-1])
ax.set_xticklabels(dims, fontsize=10)
ax.set_yticks([0.25, 0.5, 0.75, 1.0])
ax.set_yticklabels(["0,25", "0,50", "0,75", "1,00"], fontsize=8)
ax.set_ylim(0, 1.05)
ax.set_title("Trade-off Multi-Dimensi LFM 2.5 (1,2B) per Varian Kuantisasi", pad=36, fontsize=12, fontweight="bold")
ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.18), ncol=4, frameon=False)
save(fig, "4_6_tradeoff_radar.png")


# ---------------------------------------------------------------------------
# Gambar 3.1 -- Flowchart tahapan penelitian (programmatic, no graphviz dep)
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 9))
ax.set_xlim(0, 10)
ax.set_ylim(0, 12)
ax.axis("off")

steps = [
    ("Studi Pendahuluan &\nPerumusan Masalah", "#cfe2f3"),
    ("Persiapan Lingkungan\nKomputasi (Termux + llama.cpp)", "#d9ead3"),
    ("Persiapan Model &\nKuantisasi (FP16 → Q5/Q4/Q3 K_M)", "#fff2cc"),
    ("Eksekusi Eksperimen\n(System Benchmarking di HP)", "#f4cccc"),
    ("Analisis Komparatif &\nPenarikan Kesimpulan", "#d0e0e3"),
]

box_w, box_h, gap = 6.0, 1.4, 0.6
start_y = 11.0
for i, (label, color) in enumerate(steps):
    y = start_y - i * (box_h + gap)
    ax.add_patch(plt.Rectangle((2, y - box_h), box_w, box_h, facecolor=color, edgecolor="#333", linewidth=1.2))
    ax.text(2 + box_w / 2, y - box_h / 2, label, ha="center", va="center", fontsize=11, fontweight="bold")
    if i < len(steps) - 1:
        ax.annotate("", xy=(2 + box_w / 2, y - box_h - gap + 0.05),
                    xytext=(2 + box_w / 2, y - box_h - 0.05),
                    arrowprops=dict(arrowstyle="->", color="#333", lw=1.6))

ax.set_title("Tahapan Penelitian", fontsize=13, fontweight="bold", pad=10)
save(fig, "3_1_tahapan_penelitian.png")


# ---------------------------------------------------------------------------
# Gambar 2.1 -- Skema PTQ k-quants (FP16 → Q5/Q4/Q3)
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 4.8))
ax.set_xlim(0, 12)
ax.set_ylim(0, 6)
ax.axis("off")

def box(x, y, w, h, text, color, fontsize=11, weight="normal"):
    ax.add_patch(plt.Rectangle((x, y), w, h, facecolor=color, edgecolor="#333", linewidth=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize, fontweight=weight)

box(0.5, 2.3, 2.6, 1.4, "FP16\nModel Asli\n(2,2 GB)", "#fff2cc", weight="bold")

# arrow to PTQ engine
ax.annotate("", xy=(4.0, 3.0), xytext=(3.1, 3.0), arrowprops=dict(arrowstyle="->", lw=1.6, color="#333"))

box(4.0, 2.3, 3.4, 1.4, "Post-Training\nQuantization\nllama-quantize", "#d0e0e3", weight="bold")

# arrows to k-quant outputs
for i, (text, col, y) in enumerate([
    ("Q5_K_M  (~5-bit)\n805 MB | PPL +0,15", "#cfe2f3", 4.4),
    ("Q4_K_M  (~4-bit)\n698 MB | PPL +0,53", "#d9ead3", 2.6),
    ("Q3_K_M  (~3-bit)\n573 MB | PPL +1,83", "#f4cccc", 0.8),
]):
    ax.annotate("", xy=(8.4, y + 0.6), xytext=(7.4, 3.0), arrowprops=dict(arrowstyle="->", lw=1.4, color="#333"))
    box(8.4, y, 3.2, 1.2, text, col)

ax.set_title("Skema Post-Training Quantization GGUF K-Quants (LFM 2.5)", fontsize=12, fontweight="bold", pad=10)
save(fig, "2_1_skema_ptq_kquants.png")


# ---------------------------------------------------------------------------
# Gambar 2.2 -- Hierarki Edge Intelligence
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5.5))
ax.set_xlim(0, 10)
ax.set_ylim(0, 7)
ax.axis("off")

layers = [
    ("Aplikasi / User Layer", "Chatbot, Asisten, NLP On-Device", "#cfe2f3", 5.4),
    ("Framework Inferensi", "llama.cpp (C/C++ • GGUF Loader)", "#d9ead3", 4.0),
    ("Mesin Kompresi", "Post-Training Quantization (K-Quants)", "#fff2cc", 2.6),
    ("Hardware Edge Device", "Tecno Pova 5 • Helio G99 • RAM 8 GB", "#f4cccc", 1.2),
]

for title, subtitle, color, y in layers:
    ax.add_patch(plt.Rectangle((1.0, y), 8.0, 1.1, facecolor=color, edgecolor="#333", linewidth=1.2))
    ax.text(5.0, y + 0.75, title, ha="center", va="center", fontsize=12, fontweight="bold")
    ax.text(5.0, y + 0.30, subtitle, ha="center", va="center", fontsize=10)

# arrows
for y1, y2 in [(5.4, 5.1), (4.0, 3.7), (2.6, 2.3)]:
    ax.annotate("", xy=(5.0, y2), xytext=(5.0, y1), arrowprops=dict(arrowstyle="<->", lw=1.5, color="#333"))

ax.set_title("Hierarki Edge Intelligence untuk Inferensi SLM", fontsize=12, fontweight="bold", pad=10)
save(fig, "2_2_edge_intelligence.png")


print("\nAll charts generated successfully.")
