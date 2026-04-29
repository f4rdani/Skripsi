"""Generate diagrams and charts for BAB 1, 2, 3, and BAB 4 placeholders.

Run from repo root:
    python3 scripts/make_figures.py
"""

from __future__ import annotations

import os
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

REPO = Path(__file__).resolve().parent.parent
plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "axes.titleweight": "bold",
        "axes.titlesize": 12,
        "axes.labelsize": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
    }
)

# Palet sengaja disederhanakan menjadi tiga kategori saja agar
# tampilan seluruh diagram konsisten dan tidak "berbeda-beda mulu":
#   default  = biru navy   -> node netral / proses
#   alert    = merah marun -> node masalah / risiko / batas
#   success  = hijau gelap -> node target / hasil
# Semua bentuk node tetap rounded rectangle, semua panah tetap "-|>",
# tidak ada ikon eksternal — hanya teks di dalam kotak.
PALETTE = {
    "blue": "#1f4e79",
    "lightblue": "#dbe7f3",
    "red": "#b91c1c",
    "lightred": "#fde2e2",
    "green": "#15803d",
    "lightgreen": "#d6efdd",
    "gray": "#374151",
    "lightgray": "#eef0f3",
    # alias supaya pemanggil lama tetap jalan, dipetakan ke 3 kategori utama
    "orange": "#1f4e79",
    "lightorange": "#dbe7f3",
    "purple": "#1f4e79",
    "lightpurple": "#dbe7f3",
}


def save(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  -> {path.relative_to(REPO)}")


def box(
    ax,
    xy,
    wh,
    text,
    facecolor=PALETTE["lightblue"],
    edgecolor=PALETTE["blue"],
    fontsize=9,
    fontweight="normal",
):
    x, y = xy
    w, h = wh
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        linewidth=1.4,
        facecolor=facecolor,
        edgecolor=edgecolor,
    )
    ax.add_patch(patch)
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        fontweight=fontweight,
        color=PALETTE["gray"],
        wrap=True,
    )


def arrow(ax, start, end, color=PALETTE["gray"], lw=1.4):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=14,
            color=color,
            linewidth=lw,
        )
    )


# ========== BAB 1 ==========


def fig_1_1_alur_inferensi_edge():
    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 5.5)
    ax.axis("off")
    ax.set_title(
        "Gambar 1.1 Perbandingan Alur Inferensi: Cloud-based vs On-Device (Edge) LLM/SLM"
    )

    # Cloud
    box(
        ax,
        (0.2, 3.6),
        (2.0, 0.9),
        "User\n(smartphone)",
        PALETTE["lightgray"],
        PALETTE["gray"],
        10,
        "bold",
    )
    box(
        ax,
        (3.2, 3.6),
        (2.0, 0.9),
        "Internet\n(latensi & risiko privasi)",
        PALETTE["lightred"],
        PALETTE["red"],
        9,
    )
    box(
        ax,
        (6.2, 3.6),
        (2.2, 0.9),
        "Cloud API LLM\n(GPU farm)",
        PALETTE["lightorange"],
        PALETTE["orange"],
        10,
        "bold",
    )
    box(
        ax,
        (9.2, 3.6),
        (1.6, 0.9),
        "Response",
        PALETTE["lightblue"],
        PALETTE["blue"],
        10,
    )
    arrow(ax, (2.2, 4.05), (3.2, 4.05))
    arrow(ax, (5.2, 4.05), (6.2, 4.05))
    arrow(ax, (8.4, 4.05), (9.2, 4.05))
    ax.text(
        5.5, 5.05, "(a) Cloud Inference (baseline)", fontsize=11, fontweight="bold"
    )

    # Edge
    ax.text(
        5.5,
        2.95,
        "(b) On-Device / Edge Inference (penelitian ini)",
        fontsize=11,
        fontweight="bold",
    )
    box(
        ax,
        (0.2, 1.4),
        (2.0, 0.9),
        "User\n(smartphone)",
        PALETTE["lightgray"],
        PALETTE["gray"],
        10,
        "bold",
    )
    box(
        ax,
        (3.2, 1.4),
        (2.6, 0.9),
        "Termux + llama.cpp\n(CPU ARM, RAM 8 GB)",
        PALETTE["lightgreen"],
        PALETTE["green"],
        9,
        "bold",
    )
    box(
        ax,
        (6.6, 1.4),
        (2.2, 0.9),
        "SLM GGUF\nQ3/Q4/Q5_K_M",
        PALETTE["lightpurple"],
        PALETTE["purple"],
        10,
        "bold",
    )
    box(
        ax,
        (9.2, 1.4),
        (1.6, 0.9),
        "Response\n(offline)",
        PALETTE["lightblue"],
        PALETTE["blue"],
        10,
    )
    arrow(ax, (2.2, 1.85), (3.2, 1.85))
    arrow(ax, (5.8, 1.85), (6.6, 1.85))
    arrow(ax, (8.8, 1.85), (9.2, 1.85))

    # Annotation
    ax.text(
        5.5,
        0.6,
        "Keuntungan: tanpa internet · privasi data terjaga · biaya nol · latensi rendah",
        ha="center",
        fontsize=9.5,
        style="italic",
        color=PALETTE["green"],
    )
    save(fig, REPO / "BAB 1" / "gambar" / "1.1_alur_inferensi_edge.png")


def fig_1_2_diagram_masalah():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.set_title("Gambar 1.2 Identifikasi Permasalahan & Pendekatan Solusi")

    # Problems
    box(
        ax,
        (0.3, 4.4),
        (3.0, 1.2),
        "Masalah 1\nKetergantungan cloud\n→ risiko privasi\n& latensi internet",
        PALETTE["lightred"],
        PALETTE["red"],
        9,
        "bold",
    )
    box(
        ax,
        (3.5, 4.4),
        (3.0, 1.2),
        "Masalah 2\nRAM 8 GB Android\ntidak menampung\nFP16 → OOM/Force Close",
        PALETTE["lightred"],
        PALETTE["red"],
        9,
        "bold",
    )
    box(
        ax,
        (6.7, 4.4),
        (3.0, 1.2),
        "Masalah 3\nKompresi ekstrem\n→ perturbation\n→ degradasi kualitas",
        PALETTE["lightred"],
        PALETTE["red"],
        9,
        "bold",
    )

    # Mid
    box(
        ax,
        (1.5, 2.6),
        (7.0, 1.0),
        "Solusi: Post-Training Quantization (PTQ) GGUF k-quants\n(Q3_K_M / Q4_K_M / Q5_K_M) pada SLM LFM2.5-1.2B-Base & Qwen3.5-2B",
        PALETTE["lightorange"],
        PALETTE["orange"],
        10,
        "bold",
    )

    arrow(ax, (1.8, 4.4), (3.0, 3.6))
    arrow(ax, (5.0, 4.4), (5.0, 3.6))
    arrow(ax, (8.2, 4.4), (7.0, 3.6))

    # Outcome
    box(
        ax,
        (0.3, 0.6),
        (4.5, 1.4),
        "Outcome teknis\n• File size ↓ > 60%\n• Peak RAM aman <8 GB\n• TPS ↑ pada CPU ARM",
        PALETTE["lightgreen"],
        PALETTE["green"],
        9.5,
        "bold",
    )
    box(
        ax,
        (5.2, 0.6),
        (4.5, 1.4),
        "Outcome akademik\n• Validasi 3D Evaluation\nFramework (Jin et al., 2024)\n• Pareto-optimal varian",
        PALETTE["lightpurple"],
        PALETTE["purple"],
        9.5,
        "bold",
    )
    arrow(ax, (3.5, 2.6), (2.5, 2.0))
    arrow(ax, (6.5, 2.6), (7.5, 2.0))

    save(fig, REPO / "BAB 1" / "gambar" / "1.2_diagram_masalah_kompresi.png")


# ========== BAB 2 ==========


def fig_2_1_arsitektur_transformer():
    fig, ax = plt.subplots(figsize=(7, 9))
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 11)
    ax.axis("off")
    ax.set_title("Gambar 2.1 Arsitektur Transformer Decoder (basis SLM modern)")

    layers = [
        ("Token + Positional Embedding", PALETTE["lightgray"], PALETTE["gray"]),
        ("RMSNorm", PALETTE["lightblue"], PALETTE["blue"]),
        ("Multi-Head\nGrouped-Query Attention", PALETTE["lightorange"], PALETTE["orange"]),
        ("Residual +", PALETTE["lightgray"], PALETTE["gray"]),
        ("RMSNorm", PALETTE["lightblue"], PALETTE["blue"]),
        ("SwiGLU FFN", PALETTE["lightgreen"], PALETTE["green"]),
        ("Residual +", PALETTE["lightgray"], PALETTE["gray"]),
        ("× N decoder blocks", PALETTE["lightpurple"], PALETTE["purple"]),
        ("Final RMSNorm", PALETTE["lightblue"], PALETTE["blue"]),
        ("Linear → Softmax\n(vocab logits)", PALETTE["lightorange"], PALETTE["orange"]),
    ]
    y = 9.8
    h = 0.85
    for text, fc, ec in layers:
        box(ax, (1.5, y), (4.0, h), text, fc, ec, 10, "bold")
        if y > 0.4:
            arrow(ax, (3.5, y), (3.5, y - 0.15))
        y -= 1.05

    ax.text(0.4, 9.2, "Input\nIDs", fontsize=10, fontweight="bold", color=PALETTE["gray"])
    ax.text(
        0.4, 0.5, "Output\nlogits", fontsize=10, fontweight="bold", color=PALETTE["gray"]
    )
    save(fig, REPO / "BAB 2" / "gambar" / "2.1_arsitektur_transformer.png")


def fig_2_2_skema_ptq_kquants():
    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 5.5)
    ax.axis("off")
    ax.set_title(
        "Gambar 2.2 Skema Post-Training Quantization GGUF k-quants (FP16 → Q5/Q4/Q3_K_M)"
    )

    # FP16 weights — input tunggal (default llama-quantize tanpa imatrix tidak butuh kalibrasi)
    box(ax, (0.2, 2.3), (2.2, 1.0), "Bobot FP16\n(presisi tinggi)", PALETTE["lightblue"], PALETTE["blue"], 10, "bold")

    # Process box
    box(
        ax,
        (3.0, 1.8),
        (3.0, 2.0),
        "PTQ Engine\n(llama.cpp\nquantize)",
        PALETTE["lightorange"],
        PALETTE["orange"],
        10,
        "bold",
    )
    arrow(ax, (2.4, 2.8), (3.0, 2.8))

    # Outputs
    variants = [
        (6.5, 4.0, "Q5_K_M\n~5,5 bit/weight\n→ kualitas mendekati FP16", PALETTE["lightgreen"], PALETTE["green"]),
        (6.5, 2.55, "Q4_K_M\n~4,5 bit/weight\n→ default sweet-spot", PALETTE["lightorange"], PALETTE["orange"]),
        (6.5, 1.1, "Q3_K_M\n~3,5 bit/weight\n→ paling hemat, risiko PPL ↑", PALETTE["lightred"], PALETTE["red"]),
    ]
    for x, y, t, fc, ec in variants:
        box(ax, (x, y), (3.5, 1.0), t, fc, ec, 9.5, "bold")
        arrow(ax, (6.0, 2.8), (x, y + 0.5))

    ax.text(
        5.5,
        0.3,
        "k-quants menggabungkan kuantisasi grouped (super-block) dan scale FP16 untuk melindungi outliers",
        ha="center",
        fontsize=9.5,
        style="italic",
        color=PALETTE["gray"],
    )

    save(fig, REPO / "BAB 2" / "gambar" / "2.2_skema_PTQ_GGUF_kquants.png")


def fig_2_3_edge_intelligence():
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.5)
    ax.axis("off")
    ax.set_title("Gambar 2.3 Hierarki Edge Intelligence untuk Inferensi LLM/SLM")

    box(ax, (0.4, 3.6), (2.4, 1.2), "Cloud Tier\nGPU clusters", PALETTE["lightred"], PALETTE["red"], 10, "bold")
    box(ax, (3.6, 3.6), (2.4, 1.2), "Edge Server\n(MEC, RAN)", PALETTE["lightorange"], PALETTE["orange"], 10, "bold")
    box(ax, (6.8, 3.6), (2.8, 1.2), "Edge Device\nSmartphone Android\n(Helio G99, 8 GB RAM)", PALETTE["lightgreen"], PALETTE["green"], 10, "bold")

    # Highlight Edge Device sebagai fokus penelitian (border tebal + label)
    highlight = FancyBboxPatch(
        (6.75, 3.55),
        2.9,
        1.3,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        linewidth=3.2,
        facecolor="none",
        edgecolor=PALETTE["green"],
    )
    ax.add_patch(highlight)
    ax.text(
        8.2,
        4.95,
        "★ Fokus Penelitian Ini",
        ha="center",
        fontsize=10,
        fontweight="bold",
        color=PALETTE["green"],
    )

    arrow(ax, (2.8, 4.2), (3.6, 4.2))
    arrow(ax, (6.0, 4.2), (6.8, 4.2))

    ax.text(1.6, 3.2, "Latency\ntinggi", ha="center", fontsize=9, color=PALETTE["red"])
    ax.text(4.8, 3.2, "Latency\nmenengah", ha="center", fontsize=9, color=PALETTE["orange"])
    ax.text(8.2, 3.2, "Latency\nrendah", ha="center", fontsize=9, color=PALETTE["green"])

    # Kotak optimasi diposisikan tepat di bawah Edge Server + Edge Device (tidak di bawah Cloud)
    box(
        ax,
        (3.6, 1.2),
        (6.0, 1.6),
        "Optimasi yang lazim di Edge Intelligence:\n• Quantization (PTQ/QAT)\n• KV-cache compression\n• Speculative decoding\n• Batching dinamis (Zhang et al., 2024)",
        PALETTE["lightblue"],
        PALETTE["blue"],
        10,
        "bold",
    )

    save(fig, REPO / "BAB 2" / "gambar" / "2.3_arsitektur_edge_intelligence.png")


def fig_2_4_taxonomy_quantization():
    fig, ax = plt.subplots(figsize=(11, 6.5))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6.5)
    ax.axis("off")
    ax.set_title("Gambar 2.4 Taksonomi Teknik Kuantisasi LLM/SLM")

    box(ax, (4.2, 5.4), (2.6, 0.9), "Kuantisasi LLM/SLM", PALETTE["lightblue"], PALETTE["blue"], 11, "bold")

    box(ax, (1.0, 4.0), (3.0, 0.9), "Post-Training\nQuantization (PTQ)", PALETTE["lightgreen"], PALETTE["green"], 10, "bold")
    box(ax, (7.0, 4.0), (3.0, 0.9), "Quantization-Aware\nTraining (QAT)", PALETTE["lightorange"], PALETTE["orange"], 10, "bold")

    arrow(ax, (5.0, 5.4), (2.5, 4.9))
    arrow(ax, (6.0, 5.4), (8.5, 4.9))

    box(ax, (0.2, 2.6), (2.4, 1.0), "Weight-only\nGPTQ\n(Frantar et al., 2023)", PALETTE["lightpurple"], PALETTE["purple"], 9, "bold")
    box(ax, (2.8, 2.6), (2.4, 1.0), "Activation-aware\nAWQ\n(Lin et al., 2024)", PALETTE["lightpurple"], PALETTE["purple"], 9, "bold")
    box(ax, (5.4, 2.6), (2.4, 1.0), "Mixed-precision\nGGUF k-quants\n(llama.cpp)", PALETTE["lightpurple"], PALETTE["purple"], 9, "bold")
    box(ax, (8.0, 2.6), (2.4, 1.0), "NormalFloat 4-bit\nQLoRA\n(Dettmers et al., 2023)", PALETTE["lightpurple"], PALETTE["purple"], 9, "bold")

    for x in [1.4, 4.0, 6.6, 9.2]:
        arrow(ax, (2.5, 4.0), (x, 3.6))

    box(ax, (3.2, 0.6), (4.6, 1.2), "Fokus penelitian ini:\nGGUF k-quants Q3_K_M / Q4_K_M / Q5_K_M\npada CPU ARM (Helio G99)", PALETTE["lightred"], PALETTE["red"], 10, "bold")
    arrow(ax, (6.6, 2.6), (5.5, 1.8))
    save(fig, REPO / "BAB 2" / "gambar" / "2.4_taxonomy_quantization.png")


# ========== BAB 3 ==========


def fig_3_1_tahapan_penelitian():
    fig, ax = plt.subplots(figsize=(12, 4.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4.5)
    ax.axis("off")
    ax.set_title("Gambar 3.1 Tahapan Penelitian (waterfall eksperimental)")

    stages = [
        "1. Studi\nPustaka",
        "2. Perencanaan\nGQM",
        "3. Persiapan\nModel & Env",
        "4. Pengukuran\nStatik",
        "5. Pengukuran\nDinamik",
        "6. Pengukuran\nKualitas",
        "7. Analisis\nPareto + Stats",
        "8. Pelaporan\n& Validasi",
    ]
    n = len(stages)
    w = 1.3
    gap = 0.15
    total = n * w + (n - 1) * gap
    x0 = (12 - total) / 2
    y = 1.8
    for i, s in enumerate(stages):
        x = x0 + i * (w + gap)
        box(ax, (x, y), (w, 1.4), s, PALETTE["lightblue"], PALETTE["blue"], 9, "bold")
        if i < n - 1:
            arrow(ax, (x + w, y + 0.7), (x + w + gap, y + 0.7))

    ax.text(6, 0.7, "Setiap tahap menghasilkan artefak (dokumen, log, file model GGUF, tabel hasil)", ha="center", fontsize=9.5, style="italic", color=PALETTE["gray"])
    save(fig, REPO / "BAB 3" / "gambar" / "3.1_tahapan_penelitian.png")


def fig_3_2_pipeline_eksperimen():
    fig, ax = plt.subplots(figsize=(12, 6.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.5)
    ax.axis("off")
    ax.set_title("Gambar 3.2 Pipeline Eksperimen On-Device pada Tecno Pova 5")

    box(ax, (0.3, 5.0), (3.0, 1.0), "Sumber Bobot\nHugging Face\n(LFM2.5-1.2B-Base, Qwen3.5-2B)", PALETTE["lightgray"], PALETTE["gray"], 9.5, "bold")
    box(ax, (4.0, 5.0), (3.0, 1.0), "Konversi & Kuantisasi\nllama.cpp convert.py\n+ quantize", PALETTE["lightorange"], PALETTE["orange"], 10, "bold")
    box(ax, (7.7, 5.0), (4.0, 1.0), "Artefak GGUF\nFP16 / Q5_K_M / Q4_K_M / Q3_K_M\n(8 file)", PALETTE["lightpurple"], PALETTE["purple"], 9.5, "bold")
    arrow(ax, (3.3, 5.5), (4.0, 5.5))
    arrow(ax, (7.0, 5.5), (7.7, 5.5))

    box(ax, (0.3, 3.2), (3.0, 1.2), "Transfer ke Device\nadb push / scp\n→ /sdcard/Termux", PALETTE["lightblue"], PALETTE["blue"], 10, "bold")
    box(ax, (4.0, 3.2), (3.0, 1.2), "Termux\nllama.cpp build\n(NDK ARMv8 + NEON)", PALETTE["lightgreen"], PALETTE["green"], 10, "bold")
    box(ax, (7.7, 3.2), (4.0, 1.2), "Eksekusi Benchmark\nllama-bench, perplexity,\nmmlu/gsm8k/humaneval scripts", PALETTE["lightorange"], PALETTE["orange"], 9.5, "bold")
    arrow(ax, (3.3, 3.8), (4.0, 3.8))
    arrow(ax, (7.0, 3.8), (7.7, 3.8))
    arrow(ax, (9.7, 5.0), (9.7, 4.4))

    box(ax, (0.3, 1.4), (4.6, 1.2), "Telemetri Sistem\nhtop / /proc/meminfo / dumpsys meminfo\nlog → CSV", PALETTE["lightblue"], PALETTE["blue"], 9.5, "bold")
    box(ax, (5.4, 1.4), (3.2, 1.2), "Telemetri Engine\nllama.cpp\nprompt t/s, gen t/s, ppl", PALETTE["lightblue"], PALETTE["blue"], 9.5, "bold")
    box(ax, (8.9, 1.4), (2.8, 1.2), "Skor Benchmark\nMMLU/GSM8k/HumanEval", PALETTE["lightblue"], PALETTE["blue"], 9.5, "bold")
    arrow(ax, (9.7, 3.2), (9.7, 2.6))
    arrow(ax, (5.5, 3.2), (3.5, 2.6))
    arrow(ax, (8.5, 3.2), (7.0, 2.6))

    box(ax, (2.0, 0.1), (8.0, 1.0), "Aggregator (Python pandas)  →  Tabel hasil + diagram radar/Pareto + uji Wilcoxon", PALETTE["lightred"], PALETTE["red"], 10, "bold")
    arrow(ax, (3.0, 1.4), (3.0, 1.1))
    arrow(ax, (7.0, 1.4), (7.0, 1.1))
    arrow(ax, (10.0, 1.4), (8.5, 1.1))

    save(fig, REPO / "BAB 3" / "gambar" / "3.2_pipeline_eksperimen.png")


def fig_3_3_skema_gqm():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.set_title("Gambar 3.3 Goal–Question–Metric (Basili et al., 1994)")

    box(ax, (3.5, 4.8), (3.0, 0.9), "GOAL\nKuantifikasi trade-off PTQ k-quants\npada SLM untuk Android RAM 8 GB", PALETTE["lightblue"], PALETTE["blue"], 10, "bold")

    questions = [
        (0.3, 3.0, "Q1\nStorage hemat?"),
        (2.7, 3.0, "Q2\nKualitas terjaga?"),
        (5.4, 3.0, "Q3\nRAM aman?"),
        (8.0, 3.0, "Q4\nTPS naik?"),
    ]
    for x, y, t in questions:
        box(ax, (x, y), (1.9, 0.9), t, PALETTE["lightorange"], PALETTE["orange"], 10, "bold")
        arrow(ax, (5.0, 4.8), (x + 0.95, 3.9))

    metrics = [
        (0.0, 1.0, "M1.1 file size MB\nM1.2 ratio FP16/Qx"),
        (2.5, 1.0, "M2.1 PPL WikiText-2\nM2.2 MMLU/GSM8k/HE"),
        (5.0, 1.0, "M3.1 peak RSS RAM\nM3.2 OOM count"),
        (7.5, 1.0, "M4.1 prompt t/s\nM4.2 gen t/s"),
    ]
    for x, y, t in metrics:
        box(ax, (x, y), (2.5, 1.2), t, PALETTE["lightgreen"], PALETTE["green"], 9, "bold")

    for i, (xq, _, _) in enumerate(questions):
        xm = metrics[i][0]
        arrow(ax, (xq + 0.95, 3.0), (xm + 1.25, 2.2))

    save(fig, REPO / "BAB 3" / "gambar" / "3.3_skema_GQM.png")


def fig_3_4_alur_3d_eval():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.set_title("Gambar 3.4 Three-Dimensional Evaluation Framework (Jin et al., 2024)")

    box(ax, (3.4, 4.7), (3.2, 1.0), "Model terkuantisasi\n(LFM2 / Qwen3.5 × Q3/Q4/Q5/FP16)", PALETTE["lightblue"], PALETTE["blue"], 10, "bold")

    box(ax, (0.3, 2.6), (3.0, 1.4), "Knowledge & Capacity\nMMLU (general)\nGSM8k (math)\nHumanEval (code)", PALETTE["lightgreen"], PALETTE["green"], 10, "bold")
    box(ax, (3.5, 2.6), (3.0, 1.4), "Alignment\nPerplexity\n(WikiText-2)", PALETTE["lightorange"], PALETTE["orange"], 10, "bold")
    box(ax, (6.7, 2.6), (3.0, 1.4), "Efficiency\nFile size · Peak RAM\nPrompt t/s · Gen t/s", PALETTE["lightpurple"], PALETTE["purple"], 10, "bold")

    for x in [1.8, 5.0, 8.2]:
        arrow(ax, (5.0, 4.7), (x, 4.0))

    box(ax, (1.2, 0.4), (7.6, 1.6), "Aggregator\nDiagram radar (per model)  +  Diagram Pareto (efficiency vs accuracy)\nUji Wilcoxon signed-rank vs FP16  +  Reproducibility checklist", PALETTE["lightred"], PALETTE["red"], 10, "bold")

    arrow(ax, (1.8, 2.6), (3.0, 2.0))
    arrow(ax, (5.0, 2.6), (5.0, 2.0))
    arrow(ax, (8.2, 2.6), (7.0, 2.0))

    save(fig, REPO / "BAB 3" / "gambar" / "3.4_alur_evaluasi_3dimensi.png")


# ========== BAB 4 (data riil) ==========

# File size dalam MB (dari `ls -lh` user; konversi 1 G = 1024 MB).
FILE_SIZE_MB = {
    "LFM2.5-1.2B-Base": {"FP16": 2252.8, "Q5_K_M": 805.0, "Q4_K_M": 698.0, "Q3_K_M": 573.0},
    "Qwen3.5-2B":      {"FP16": 3686.4, "Q5_K_M": 1433.6, "Q4_K_M": 1228.8, "Q3_K_M": 1126.4},
}

# Perplexity WikiText-2 (lower is better).
PPL = {
    "LFM2.5-1.2B-Base": {"FP16": 12.6829, "Q5_K_M": 12.8297, "Q4_K_M": 13.2145, "Q3_K_M": 14.5135},
    "Qwen3.5-2B":      {"FP16": 12.7763, "Q5_K_M": 13.0856, "Q4_K_M": 13.3617, "Q3_K_M": 15.2172},
}

# Akurasi (%).
ACC = {
    "LFM2.5-1.2B-Base": {
        "FP16":   {"MMLU": 33, "GSM8k": 52, "HumanEval": 36},
        "Q5_K_M": {"MMLU": 30, "GSM8k": 52, "HumanEval": 29},
        "Q4_K_M": {"MMLU": 28, "GSM8k": 51, "HumanEval": 37},
        "Q3_K_M": {"MMLU": 32, "GSM8k": 42, "HumanEval": 30},
    },
    "Qwen3.5-2B": {
        "FP16":   {"MMLU": 12, "GSM8k": 57, "HumanEval": 52},
        "Q5_K_M": {"MMLU": 14, "GSM8k": 53, "HumanEval": 47},
        "Q4_K_M": {"MMLU": 14, "GSM8k": 56, "HumanEval": 44},
        "Q3_K_M": {"MMLU": 22, "GSM8k": 37, "HumanEval": 26},
    },
}

VARIANTS = ["FP16", "Q5_K_M", "Q4_K_M", "Q3_K_M"]
MODELS = ["LFM2.5-1.2B-Base", "Qwen3.5-2B"]
# Dua warna kontras tinggi (hue + value berbeda) untuk membedakan dua model
# di seluruh BAB 4. Tetap aman dicetak grayscale karena LFM lebih gelap dari
# Qwen pada konversi luminance.
MODEL_COLOR = {"LFM2.5-1.2B-Base": "#1f4e79", "Qwen3.5-2B": "#b45309"}
MODEL_FILL  = {"LFM2.5-1.2B-Base": "#cfe2f3", "Qwen3.5-2B": "#fde7c8"}


def fig_4_1_storage():
    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.arange(len(VARIANTS))
    w = 0.36
    for i, m in enumerate(MODELS):
        vals = [FILE_SIZE_MB[m][v] for v in VARIANTS]
        offset = (i - 0.5) * w
        bars = ax.bar(x + offset, vals, w, label=m, color=MODEL_FILL[m], edgecolor=MODEL_COLOR[m], linewidth=1.4)
        for b, val in zip(bars, vals):
            ax.text(b.get_x() + b.get_width()/2, val + 60, f"{val:.0f}", ha="center", fontsize=8.5)
    ax.set_xticks(x)
    ax.set_xticklabels(VARIANTS)
    ax.set_ylabel("Ukuran berkas (MB)")
    ax.set_title("Gambar 4.1 Ukuran Berkas Model GGUF (FP16 vs k-quants)")
    ax.legend()
    ax.grid(True, axis="y", alpha=0.3)
    save(fig, REPO / "BAB 4" / "gambar" / "4.1_ukuran_berkas.png")


def fig_4_2_perplexity():
    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.arange(len(VARIANTS))
    w = 0.36
    for i, m in enumerate(MODELS):
        vals = [PPL[m][v] for v in VARIANTS]
        offset = (i - 0.5) * w
        bars = ax.bar(x + offset, vals, w, label=m, color=MODEL_FILL[m], edgecolor=MODEL_COLOR[m], linewidth=1.4)
        for b, val in zip(bars, vals):
            ax.text(b.get_x() + b.get_width()/2, val + 0.1, f"{val:.3f}", ha="center", fontsize=8.5)
    ax.set_xticks(x)
    ax.set_xticklabels(VARIANTS)
    ax.set_ylabel("Perplexity WikiText-2 (lebih rendah lebih baik)")
    ax.set_title("Gambar 4.2 Perplexity per Varian Kuantisasi")
    ax.legend()
    ax.grid(True, axis="y", alpha=0.3)
    save(fig, REPO / "BAB 4" / "gambar" / "4.2_perplexity.png")


def fig_4_3_accuracy():
    benches = ["MMLU", "GSM8k", "HumanEval"]
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), sharey=True)
    for ax, b in zip(axes, benches):
        x = np.arange(len(VARIANTS))
        w = 0.36
        for i, m in enumerate(MODELS):
            vals = [ACC[m][v][b] for v in VARIANTS]
            offset = (i - 0.5) * w
            bars = ax.bar(x + offset, vals, w, label=m, color=MODEL_FILL[m], edgecolor=MODEL_COLOR[m], linewidth=1.4)
            for bar, val in zip(bars, vals):
                ax.text(bar.get_x() + bar.get_width()/2, val + 1, f"{val}%", ha="center", fontsize=8.5)
        ax.set_xticks(x)
        ax.set_xticklabels(VARIANTS)
        ax.set_title(b)
        ax.set_ylim(0, 70)
        ax.grid(True, axis="y", alpha=0.3)
    axes[0].set_ylabel("Akurasi (%)")
    axes[-1].legend(loc="upper right", fontsize=8)
    fig.suptitle("Gambar 4.3 Akurasi MMLU, GSM8k, HumanEval per Varian Kuantisasi", y=1.02, fontsize=12, fontweight="bold")
    save(fig, REPO / "BAB 4" / "gambar" / "4.3_akurasi_mmlu_gsm8k_humaneval.png")


def fig_4_4_pareto_storage_vs_acc():
    """Pareto: x = relative storage vs FP16, y = composite accuracy (mean of 3 benches)."""
    fig, ax = plt.subplots(figsize=(8.5, 6))
    markers = {"FP16": "o", "Q5_K_M": "s", "Q4_K_M": "^", "Q3_K_M": "D"}
    for m in MODELS:
        fp16 = FILE_SIZE_MB[m]["FP16"]
        for v in VARIANTS:
            rel = FILE_SIZE_MB[m][v] / fp16
            comp = np.mean(list(ACC[m][v].values()))
            ax.scatter(rel, comp, s=160, marker=markers[v], color=MODEL_FILL[m], edgecolor=MODEL_COLOR[m], linewidth=1.6, label=f"{m} {v}")
            ax.annotate(v, (rel, comp), xytext=(7, 5), textcoords="offset points", fontsize=8.5, color=MODEL_COLOR[m])
        # garis penghubung (urut FP16 -> Q5 -> Q4 -> Q3)
        xs = [FILE_SIZE_MB[m][v] / fp16 for v in VARIANTS]
        ys = [np.mean(list(ACC[m][v].values())) for v in VARIANTS]
        ax.plot(xs, ys, color=MODEL_COLOR[m], linewidth=1.0, alpha=0.5)
    ax.set_xlabel("Relative storage (× FP16) — lebih kiri = lebih hemat")
    ax.set_ylabel("Composite accuracy (mean MMLU · GSM8k · HumanEval)")
    ax.set_xlim(0.0, 1.1)
    ax.grid(True, alpha=0.3)
    # legenda manual: hanya 2 model + 4 varian (markers)
    from matplotlib.lines import Line2D
    h = [Line2D([0], [0], marker="o", color="w", markerfacecolor=MODEL_FILL[m], markeredgecolor=MODEL_COLOR[m], markersize=10, label=m) for m in MODELS]
    h += [Line2D([0], [0], marker=markers[v], color="k", linestyle="", markerfacecolor="white", markersize=9, label=v) for v in VARIANTS]
    ax.legend(handles=h, loc="lower right", fontsize=8.5)
    ax.set_title("Gambar 4.4 Pareto Storage vs Composite Accuracy")
    save(fig, REPO / "BAB 4" / "gambar" / "4.4_pareto_storage_vs_accuracy.png")


def fig_4_5_radar_quality():
    """Radar empat varian per model: storage hemat, PPL invers, MMLU, GSM8k, HumanEval. RAM/TPS belum tersedia."""
    cats = ["Storage\nhemat", "PPL\ninvers", "MMLU", "GSM8k", "HumanEval"]
    angles = np.linspace(0, 2 * np.pi, len(cats), endpoint=False).tolist()
    angles += angles[:1]

    # normalisasi min-max berdasarkan agregat semua kondisi (8 titik per metrik)
    all_sizes = [FILE_SIZE_MB[m][v] for m in MODELS for v in VARIANTS]
    all_ppl   = [PPL[m][v] for m in MODELS for v in VARIANTS]
    all_mmlu  = [ACC[m][v]["MMLU"]      for m in MODELS for v in VARIANTS]
    all_gsm   = [ACC[m][v]["GSM8k"]     for m in MODELS for v in VARIANTS]
    all_he    = [ACC[m][v]["HumanEval"] for m in MODELS for v in VARIANTS]
    min_size, max_size = min(all_sizes), max(all_sizes)
    min_ppl,  max_ppl  = min(all_ppl),   max(all_ppl)
    min_mmlu, max_mmlu = min(all_mmlu),  max(all_mmlu)
    min_gsm,  max_gsm  = min(all_gsm),   max(all_gsm)
    min_he,   max_he   = min(all_he),    max(all_he)

    def _mm(val, lo, hi):
        return 0.5 if hi == lo else (val - lo) / (hi - lo)

    fig, axes = plt.subplots(1, 2, figsize=(13, 7.2), subplot_kw=dict(polar=True))
    variant_style = {"FP16":   ("-",  PALETTE["gray"]),
                     "Q5_K_M": ("-",  PALETTE["green"]),
                     "Q4_K_M": ("--", PALETTE["blue"]),
                     "Q3_K_M": (":",  PALETTE["red"])}
    for ax, m in zip(axes, MODELS):
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(cats, fontsize=9)
        ax.set_ylim(0, 1)
        for v in VARIANTS:
            # Min-max normalisasi konsisten untuk SEMUA sumbu radar (5 metrik):
            # nilai terbaik teramati = 1.0, nilai terburuk teramati = 0.0.
            storage_score = 1.0 - _mm(FILE_SIZE_MB[m][v], min_size, max_size)  # kecil = bagus
            ppl_score     = 1.0 - _mm(PPL[m][v],         min_ppl,  max_ppl)   # kecil = bagus
            mmlu = _mm(ACC[m][v]["MMLU"],      min_mmlu, max_mmlu)             # besar = bagus
            gsm  = _mm(ACC[m][v]["GSM8k"],     min_gsm,  max_gsm)
            he   = _mm(ACC[m][v]["HumanEval"], min_he,   max_he)
            vals = [storage_score, ppl_score, mmlu, gsm, he]
            vals += vals[:1]
            ls, c = variant_style[v]
            ax.plot(angles, vals, ls, color=c, linewidth=2, label=v)
            ax.fill(angles, vals, color=c, alpha=0.08)
        # Nama model ditaruh di BAWAH panel (bukan judul atas) supaya tidak
        # tumpang tindih dengan suptitle. Pakai annotate axes-fraction.
        ax.annotate(m, xy=(0.5, -0.18), xycoords="axes fraction",
                    ha="center", va="center", fontsize=11, fontweight="bold",
                    color=MODEL_COLOR[m])
        ax.legend(loc="upper right", bbox_to_anchor=(1.32, 1.05), fontsize=8.5)
    fig.suptitle("Gambar 4.5 Radar Kualitas × Efisiensi (Storage · PPL⁻¹ · MMLU · GSM8k · HumanEval)",
                 fontsize=12, fontweight="bold", y=0.99)
    fig.subplots_adjust(top=0.88, bottom=0.14, wspace=0.5)
    save(fig, REPO / "BAB 4" / "gambar" / "4.5_radar_kualitas.png")


def fig_4_6_ram_tps_placeholder():
    """Gambar 4.6 placeholder — menunggu data RAM/TPS dari pengujian Termux di Pova 5."""
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
    ax.set_title("Gambar 4.6 Profil RAM dan TPS (PLACEHOLDER — menunggu pengujian Termux di Pova 5)")
    box(ax, (0.5, 1.5), (9.0, 3.0),
        "Diagram RAM dan TPS akan dibuat setelah benchmark di smartphone Pova 5 selesai.\n\n"
        "Metrik yang ditunggu: peak RAM (MB), prompt t/s, generation t/s,\n"
        "OOM count, baterai 0→40% (estimasi),  thermal throttling rate.",
        PALETTE["lightred"], PALETTE["red"], 11, "bold")
    save(fig, REPO / "BAB 4" / "gambar" / "4.6_ram_tps_placeholder.png")


def main() -> None:
    print("Generating BAB 1 figures...")
    fig_1_1_alur_inferensi_edge()
    fig_1_2_diagram_masalah()

    print("Generating BAB 2 figures...")
    fig_2_1_arsitektur_transformer()
    fig_2_2_skema_ptq_kquants()
    fig_2_3_edge_intelligence()
    fig_2_4_taxonomy_quantization()

    print("Generating BAB 3 figures...")
    fig_3_1_tahapan_penelitian()
    fig_3_2_pipeline_eksperimen()
    fig_3_3_skema_gqm()
    fig_3_4_alur_3d_eval()

    print("Generating BAB 4 figures...")
    fig_4_1_storage()
    fig_4_2_perplexity()
    fig_4_3_accuracy()
    fig_4_4_pareto_storage_vs_acc()
    fig_4_5_radar_quality()
    fig_4_6_ram_tps_placeholder()

    print("Done.")


if __name__ == "__main__":
    main()
