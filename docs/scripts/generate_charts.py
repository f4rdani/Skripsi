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
# Data sumber: docs/data/hasilv2_aggregated.csv (Android, Tecno Pova 5)
# Urutan QUANTS: F16, Q5_K_M, Q4_K_M, Q3_K_M
# ---------------------------------------------------------------------------
prompt_lfm = [33.47, 35.33, 43.67, 18.27]
prompt_lfm_std = [6.49, 1.21, 2.38, 1.82]
gen_lfm = [5.57, 10.63, 13.67, 11.07]
gen_lfm_std = [0.19, 0.62, 0.24, 0.69]
prompt_qwen = [22.70, 22.55, 27.00, 14.55]
# Qwen Q5/Q4/Q3 use N=3 with one mean-replicate (see Tabel IV.2 note);
# standard deviations are population stdev recomputed after the mean replicate.
prompt_qwen_std = [1.71, 0.20, 2.12, 0.78]
gen_qwen = [1.87, 4.60, 4.95, 4.25]
gen_qwen_std = [0.19, 0.24, 0.20, 0.29]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5.4), sharey=False)
for ax, prompt, pstd, gen, gstd, title in [
    (ax1, prompt_lfm, prompt_lfm_std, gen_lfm, gen_lfm_std, "LFM 2.5 (1.2B)"),
    (ax2, prompt_qwen, prompt_qwen_std, gen_qwen, gen_qwen_std, "Qwen 3.5 (2B)"),
]:
    ax.errorbar(QUANTS, prompt, yerr=pstd, marker="o", linewidth=2, capsize=4,
                label="Prompt Speed (t/s)", color="#2ca02c")
    ax.errorbar(QUANTS, gen, yerr=gstd, marker="s", linewidth=2, capsize=4,
                label="Generation Speed (t/s)", color="#ff7f0e")
    for xi, yi in enumerate(prompt):
        ax.annotate(f"{yi:.1f}", (xi, yi), textcoords="offset points", xytext=(0, 10), ha="center", fontsize=9)
    for xi, yi in enumerate(gen):
        ax.annotate(f"{yi:.1f}", (xi, yi), textcoords="offset points", xytext=(0, -16), ha="center", fontsize=9)
    ax.set_title(title)
    ax.set_xlabel("Varian Kuantisasi")
    ax.set_ylabel("Tokens per Second (t/s)")
    ax.grid(linestyle="--", alpha=0.4)
    # Pad upper limit so the data line and labels do not collide with the legend later
    top = max(p + s for p, s in zip(prompt, pstd))
    ax.set_ylim(0, top * 1.18)

# Shared legend placed BELOW the plots, fully outside the data boxes, so the
# "Prompt Speed" / "Generation Speed" keterangan no longer overlaps the lines.
handles, labels = ax1.get_legend_handles_labels()
fig.legend(handles, labels, loc="lower center", bbox_to_anchor=(0.5, -0.02),
           ncol=2, frameon=True, fontsize=11)
fig.suptitle("Kecepatan Inferensi (Prompt vs Generation) per Varian Kuantisasi", fontsize=13, fontweight="bold")
fig.tight_layout(rect=[0, 0.06, 1, 0.96])
fig.savefig(OUT / "4_2_kecepatan_inferensi.png", bbox_inches="tight")
plt.close(fig)
print(f"  wrote {OUT / '4_2_kecepatan_inferensi.png'}")


# ---------------------------------------------------------------------------
# Gambar 4.3 -- Konsumsi RAM (Peak) per varian kuantisasi
# Data sumber: docs/data/hasilv2_aggregated.csv (Android, RAM proses VmRSS)
# ---------------------------------------------------------------------------
peak_lfm = [2303.47, 1665.28, 1452.97, 911.97]
peak_lfm_std = [13.32, 14.07, 14.15, 15.08]
peak_qwen = [3744.25, 2856.29, 2562.88, 1897.97]
# Qwen Q5/Q4/Q3 std recomputed after mean replicate (see Tabel IV.2 note).
peak_qwen_std = [8.05, 0.24, 0.38, 0.02]

fig, ax = plt.subplots(figsize=(8, 4.8))
b1 = ax.bar(x - width / 2, peak_lfm, width, yerr=peak_lfm_std, capsize=4,
            label="LFM 2.5 (1.2B)", color=COLOR_LFM)
b2 = ax.bar(x + width / 2, peak_qwen, width, yerr=peak_qwen_std, capsize=4,
            label="Qwen 3.5 (2B)", color=COLOR_QWEN)
ax.set_xticks(x, QUANTS)
ax.set_ylabel("Peak RAM Proses (MB)")
ax.set_title("Konsumsi Peak RAM Proses per Varian Kuantisasi (Helio G99, 8 GB)")
ax.legend(loc="upper right")
ax.grid(axis="y", linestyle="--", alpha=0.4)
for bars in (b1, b2):
    ax.bar_label(bars, fmt="%.0f", padding=2, fontsize=9)
ax.set_ylim(0, max(peak_qwen) * 1.18)
save(fig, "4_3_konsumsi_ram.png")


# ---------------------------------------------------------------------------
# Gambar 4.4 -- Perplexity WikiText-2 per varian kuantisasi
# Disajikan dalam dua sub-panel terpisah (LFM dan Qwen) supaya label nilai
# tidak saling tumpang tindih seperti versi single-axis sebelumnya.
# ---------------------------------------------------------------------------
ppl_lfm = [12.6829, 12.8297, 13.2145, 14.5135]
ppl_qwen = [12.7763, 13.0856, 13.3617, 15.2172]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8), sharey=False)
for ax, ppl, title, color in [
    (ax1, ppl_lfm, "LFM 2.5 (1.2B)", COLOR_LFM),
    (ax2, ppl_qwen, "Qwen 3.5 (2B)", COLOR_QWEN),
]:
    ax.plot(QUANTS, ppl, marker="o", linewidth=2.2, color=color)
    for xi, yi in enumerate(ppl):
        ax.annotate(f"{yi:.3f}", (xi, yi), textcoords="offset points",
                    xytext=(0, 10), ha="center", fontsize=10, color=color,
                    fontweight="bold")
    ax.set_title(title, fontsize=12, fontweight="bold")
    ax.set_xlabel("Varian Kuantisasi")
    ax.set_ylabel("Perplexity (lebih rendah = lebih baik)")
    ax.grid(linestyle="--", alpha=0.4)
    pmin, pmax = min(ppl), max(ppl)
    pad = (pmax - pmin) * 0.25 + 0.15
    ax.set_ylim(pmin - pad * 0.6, pmax + pad)

fig.suptitle("Degradasi Perplexity pada Dataset WikiText-2", fontsize=13, fontweight="bold")
save(fig, "4_4_perplexity.png")


# ---------------------------------------------------------------------------
# Gambar 4.5 -- Akurasi benchmark (MMLU/GSM8K/HumanEval)
# Sumber: hasil benchmark PC host (RTX 3060) - latest runs
# Catatan: Qwen GSM8K rendah karena reasoning-model parsing issue (lihat 4.3.3)
# ---------------------------------------------------------------------------
benchmarks = ["MMLU", "GSM8K", "HumanEval"]
lfm_acc = {
    "F16":    [32, 58, 36],
    "Q5_K_M": [34, 55, 29],
    "Q4_K_M": [25, 50, 37],
    "Q3_K_M": [28, 40, 30],
}
qwen_acc = {
    "F16":    [40, 16, 52],
    "Q5_K_M": [29, 17, 47],
    "Q4_K_M": [37, 19, 40],
    "Q3_K_M": [40, 12, 25],
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
# Gambar 4.6 -- Trade-off multi-dimensi (grouped bar chart)
# Versi sebelumnya menggunakan radar chart yang sulit dibaca karena keempat
# poligon saling menumpuk. Diganti menjadi grouped horizontal bar chart
# (sumbu Y = dimensi metrik, sumbu X = skor normalisasi 0..1) sehingga
# perbandingan antar varian kuantisasi langsung terbaca per dimensi.
# ---------------------------------------------------------------------------
def norm(vals):
    arr = np.asarray(vals, dtype=float)
    lo, hi = arr.min(), arr.max()
    if hi - lo < 1e-9:
        return np.ones_like(arr)
    return (arr - lo) / (hi - lo)

# Build per-variant scores using LFM data (representative).
# All dimensions are normalised so that higher = better.
storage_eff = norm([1 / s for s in lfm_size_mb])
ram_eff = norm([1 / r for r in peak_lfm])
gen_speed = norm(gen_lfm)
prompt_speed = norm(prompt_lfm)
ppl_inv = norm([1 / p for p in ppl_lfm])
acc_per_variant = [np.mean(lfm_acc[q]) for q in QUANTS]
acc_mean = norm(acc_per_variant)

dims = [
    "Efisiensi\nStorage",
    "Efisiensi\nRAM",
    "Generation\nSpeed",
    "Prompt\nSpeed",
    "1 / Perplexity",
    "Akurasi\nRata-rata",
]
# data shape: (n_dimensions, n_variants)
data = np.vstack([storage_eff, ram_eff, gen_speed, prompt_speed, ppl_inv, acc_mean])

fig, ax = plt.subplots(figsize=(10.5, 6.2))
y = np.arange(len(dims))
bar_h = 0.20
for i, q in enumerate(QUANTS):
    offs = (i - 1.5) * bar_h
    bars = ax.barh(y + offs, data[:, i], bar_h, label=q, color=palette[i],
                   edgecolor="white", linewidth=0.6)
    ax.bar_label(bars, fmt="%.2f", padding=2, fontsize=8)

ax.set_yticks(y)
ax.set_yticklabels(dims, fontsize=10)
ax.invert_yaxis()  # supaya "Efisiensi Storage" tampil paling atas
ax.set_xlabel("Skor Normalisasi (0 = terburuk, 1 = terbaik)")
ax.set_xlim(0, 1.18)
ax.set_xticks([0.0, 0.25, 0.5, 0.75, 1.0])
ax.set_xticklabels(["0,00", "0,25", "0,50", "0,75", "1,00"])
ax.grid(axis="x", linestyle="--", alpha=0.4)
ax.set_axisbelow(True)
ax.set_title("Trade-off Multi-Dimensi LFM 2.5 (1,2B) per Varian Kuantisasi",
             fontsize=12, fontweight="bold", pad=12)
# Legend placed BELOW the axes so it never overlaps the bars
ax.legend(title="Varian Kuantisasi", loc="lower center",
          bbox_to_anchor=(0.5, -0.22), ncol=4, frameon=True, fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "4_6_tradeoff_radar.png", bbox_inches="tight")
plt.close(fig)
print(f"  wrote {OUT / '4_6_tradeoff_radar.png'}")


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


# NOTE: Gambar BAB 2 (skema PTQ k-quants & hierarki Edge Intelligence) sengaja
# tidak diregenerasi karena aturan penulisan: ilustrasi pada BAB 1 dan BAB 2
# hanya boleh menggunakan gambar dari jurnal/penelitian orang lain dengan
# pencantuman sumber, bukan gambar olahan penulis. Konsep yang dulunya
# divisualisasikan kini dipaparkan dalam bentuk teks pada Sub-bab 2.1.1 dan
# 2.1.5 dengan rujukan literatur (Dettmers dkk., 2023; Frantar dkk., 2023;
# Tan dkk., 2024; Zhang dkk., 2024).


# ---------------------------------------------------------------------------
# Gambar 4.7 -- Delta akurasi LFM 2.5 per varian kuantisasi (relatif F16)
# Sumber: Tabel 4.4 (MMLU, GSM8K, HumanEval) dan Tabel 4.6
# ---------------------------------------------------------------------------
benchmarks = ["MMLU", "GSM8K", "HumanEval", "MT-Bench TTR"]
delta_q5 = [+2, -3, -7, -1.7]
delta_q4 = [-7, -8, +1, -5.8]
delta_q3 = [-4, -18, -6, -12.3]

x = np.arange(len(benchmarks))
width = 0.26
fig, ax = plt.subplots(figsize=(9.5, 5.2))
b1 = ax.bar(x - width, delta_q5, width, label="Q5_K_M", color="#2ca02c")
b2 = ax.bar(x, delta_q4, width, label="Q4_K_M", color="#1f77b4")
b3 = ax.bar(x + width, delta_q3, width, label="Q3_K_M", color="#d62728")

ax.axhline(0, color="#333", linewidth=1.0)
ax.set_xticks(x, benchmarks)
ax.set_ylabel("Delta vs F16 (poin)")
ax.set_title("Penurunan Kepintaran LFM 2.5 per Varian Kuantisasi (Delta vs F16)")
ax.grid(axis="y", linestyle="--", alpha=0.4)
ax.legend(loc="lower left", frameon=True)
for bars in (b1, b2, b3):
    ax.bar_label(bars, fmt="%+.1f", padding=2, fontsize=9)
ax.set_ylim(min(delta_q3) - 4, max(delta_q5 + delta_q4 + delta_q3) + 4)
save(fig, "4_7_delta_akurasi.png")


# ---------------------------------------------------------------------------
# Gambar 4.8 -- Delta akurasi Qwen 3.5 per varian kuantisasi (relatif F16)
# Sumber: Tabel 4.5 (MMLU, GSM8K, HumanEval, MT-Bench TTR) dan Tabel 4.6-B
# Catatan: GSM8K diberi tanda dagger karena reasoning-model parsing issue
# (lihat Sub-bab 4.3.3); tetap divisualisasikan agar pola dapat dibaca.
# ---------------------------------------------------------------------------
benchmarks_qwen = ["MMLU", "GSM8K†", "HumanEval", "MT-Bench TTR"]
delta_q5_qwen = [-11, +1, -5, -13.4]
delta_q4_qwen = [-3, +3, -12, +2.2]
delta_q3_qwen = [0, -4, -27, -2.5]

x = np.arange(len(benchmarks_qwen))
width = 0.26
fig, ax = plt.subplots(figsize=(9.5, 5.2))
b1 = ax.bar(x - width, delta_q5_qwen, width, label="Q5_K_M", color="#2ca02c")
b2 = ax.bar(x, delta_q4_qwen, width, label="Q4_K_M", color="#1f77b4")
b3 = ax.bar(x + width, delta_q3_qwen, width, label="Q3_K_M", color="#d62728")

ax.axhline(0, color="#333", linewidth=1.0)
ax.set_xticks(x, benchmarks_qwen)
ax.set_ylabel("Delta vs F16 (poin)")
ax.set_title("Penurunan Kepintaran Qwen 3.5 per Varian Kuantisasi (Delta vs F16)")
ax.grid(axis="y", linestyle="--", alpha=0.4)
ax.legend(loc="lower left", frameon=True)
for bars in (b1, b2, b3):
    ax.bar_label(bars, fmt="%+.1f", padding=2, fontsize=9)
qwen_all = delta_q5_qwen + delta_q4_qwen + delta_q3_qwen
ax.set_ylim(min(qwen_all) - 4, max(qwen_all) + 4)
ax.text(0.99, 0.02,
        "† GSM8K dilaporkan sebagai lower bound (lihat Sub-bab 4.3.3)",
        transform=ax.transAxes, ha="right", va="bottom",
        fontsize=8, style="italic", color="#555")
save(fig, "4_8_delta_akurasi_qwen.png")


print("\nAll charts generated successfully.")
