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

PALETTE = {
    "blue": "#1f4e79",
    "lightblue": "#cfe2f3",
    "orange": "#d97706",
    "lightorange": "#fde7c8",
    "green": "#15803d",
    "lightgreen": "#d1fae5",
    "red": "#b91c1c",
    "lightred": "#fee2e2",
    "purple": "#6b21a8",
    "lightpurple": "#ede9fe",
    "gray": "#374151",
    "lightgray": "#e5e7eb",
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
        "Solusi: Post-Training Quantization (PTQ) GGUF k-quants\n(Q3_K_M / Q4_K_M / Q5_K_M) pada SLM LFM2-1.2B & Qwen3.5-2B",
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

    # FP16 weights
    box(ax, (0.2, 2.3), (2.2, 1.0), "Bobot FP16\n(presisi tinggi)", PALETTE["lightblue"], PALETTE["blue"], 10, "bold")
    box(ax, (0.2, 0.8), (2.2, 1.0), "Calibration set\n(WikiText-2)", PALETTE["lightgray"], PALETTE["gray"], 10)

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
    arrow(ax, (2.4, 1.3), (3.0, 2.4))

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

    arrow(ax, (2.8, 4.2), (3.6, 4.2))
    arrow(ax, (6.0, 4.2), (6.8, 4.2))

    ax.text(1.6, 3.2, "Latency\ntinggi", ha="center", fontsize=9, color=PALETTE["red"])
    ax.text(4.8, 3.2, "Latency\nmenengah", ha="center", fontsize=9, color=PALETTE["orange"])
    ax.text(8.2, 3.2, "Latency\nrendah", ha="center", fontsize=9, color=PALETTE["green"])

    box(
        ax,
        (0.4, 1.4),
        (9.2, 1.4),
        "Optimasi yang lazim di Edge Intelligence:\n• Quantization (PTQ/QAT)  • KV-cache compression  • Speculative decoding  • Batching dinamis (Zhang et al., 2024)",
        PALETTE["lightblue"],
        PALETTE["blue"],
        10,
        "bold",
    )

    arrow(ax, (1.6, 3.6), (3.5, 2.8))
    arrow(ax, (4.8, 3.6), (5.0, 2.8))
    arrow(ax, (8.2, 3.6), (6.5, 2.8))

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

    box(ax, (0.3, 5.0), (3.0, 1.0), "Sumber Bobot\nHugging Face\n(LFM2-1.2B, Qwen3.5-2B)", PALETTE["lightgray"], PALETTE["gray"], 9.5, "bold")
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


# ========== BAB 4 placeholder ==========


def fig_4_placeholder_radar():
    """Generate a placeholder radar chart for BAB 4 with mock illustrative data."""
    categories = ["Storage\n(efficiency)", "RAM\n(efficiency)", "TPS-Gen\n(efficiency)", "MMLU", "GSM8k", "HumanEval", "PPL inv."]
    n = len(categories)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    angles += angles[:1]

    # Mock illustrative scores (0..1) - placeholder until real data is filled in
    series = {
        "FP16": [0.10, 0.20, 0.40, 1.00, 1.00, 1.00, 1.00],
        "Q5_K_M": [0.50, 0.55, 0.70, 0.98, 0.97, 0.96, 0.97],
        "Q4_K_M": [0.75, 0.78, 0.85, 0.95, 0.93, 0.92, 0.94],
        "Q3_K_M": [0.92, 0.92, 0.95, 0.85, 0.80, 0.78, 0.82],
    }
    colors = {"FP16": PALETTE["gray"], "Q5_K_M": PALETTE["green"], "Q4_K_M": PALETTE["orange"], "Q3_K_M": PALETTE["red"]}

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=9)
    ax.set_ylim(0, 1)
    for label, values in series.items():
        v = values + values[:1]
        ax.plot(angles, v, color=colors[label], linewidth=2, label=label)
        ax.fill(angles, v, color=colors[label], alpha=0.10)
    ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1), fontsize=9)
    ax.set_title(
        "Gambar 4.X Diagram Radar (PLACEHOLDER — diisi setelah data benchmark masuk)",
        pad=22,
        fontsize=11,
    )
    save(fig, REPO / "BAB 4" / "gambar" / "4.X_radar_placeholder.png")


def fig_4_placeholder_pareto():
    fig, ax = plt.subplots(figsize=(8, 6))
    # Mock illustrative
    pts = {
        "FP16": (1.00, 100, 80, "o"),
        "Q5_K_M": (0.55, 97, 50, "s"),
        "Q4_K_M": (0.32, 93, 32, "^"),
        "Q3_K_M": (0.20, 80, 22, "D"),
    }
    for label, (size, acc, ram, marker) in pts.items():
        ax.scatter(size, acc, s=ram * 10, marker=marker, alpha=0.7, label=f"{label} (RAM~{ram}%)", edgecolor="black")
        ax.annotate(label, (size, acc), xytext=(8, 6), textcoords="offset points", fontsize=10, fontweight="bold")

    ax.set_xlabel("Relative storage (× FP16) — lebih kiri = lebih hemat")
    ax.set_ylabel("Composite accuracy score (%)")
    ax.set_xlim(0, 1.1)
    ax.set_ylim(60, 105)
    ax.grid(True, alpha=0.3)
    ax.legend(title="Marker size ∝ peak RAM", loc="lower right", fontsize=9)
    ax.set_title("Gambar 4.Y Pareto plot Storage vs Accuracy (PLACEHOLDER)")
    save(fig, REPO / "BAB 4" / "gambar" / "4.Y_pareto_placeholder.png")


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

    print("Generating BAB 4 placeholders...")
    fig_4_placeholder_radar()
    fig_4_placeholder_pareto()

    print("Done.")


if __name__ == "__main__":
    main()
