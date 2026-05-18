#!/usr/bin/env python3
"""Uji statistik signifikansi antar varian kuantisasi untuk data Android.

Mengonsumsi `data/hasilv2_clean.csv` dan menghasilkan tabel Welch's t-test
serta one-way ANOVA untuk metrik:
  - Generation TPS
  - Prompt TPS
  - Peak RAM proses

Hasil disimpan ke dua berkas plain text agar dapat direplikasi oleh penguji:
  - `data/statistical_tests_lfm.txt`  (LFM 2.5 / 1,2B)
  - `data/statistical_tests_qwen.txt` (Qwen 3.5 / 2B)

Run:
    python3 scripts/statistical_tests.py
"""
from __future__ import annotations
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    import pandas as pd
    import numpy as np
    from scipy import stats
except ImportError:
    print("ERROR: butuh pandas + scipy. Jalankan: pip install pandas scipy")
    sys.exit(1)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_PATH = DATA_DIR / "hasilv2_clean.csv"

VARIANTS = ["F16", "Q5_K_M", "Q4_K_M", "Q3_K_M"]
METRICS = [
    ("Generation TPS", "GenTPS"),
    ("Prompt TPS", "PromptTPS"),
    ("Peak RAM (MB)", "RAMUsed_MB"),
]


@dataclass
class FamilyConfig:
    label: str
    family_key: str
    out_path: Path
    header_title: str
    source_note: str


FAMILIES = [
    FamilyConfig(
        label="LFM 2.5 (1,2B)",
        family_key="LFM",
        out_path=DATA_DIR / "statistical_tests_lfm.txt",
        header_title="UJI STATISTIK ANTAR VARIAN KUANTISASI -- LFM 2.5 (1,2B) di Tecno Pova 5",
        source_note="Sumber: docs/data/hasilv2_clean.csv (n=3 ulangan per varian)",
    ),
    FamilyConfig(
        label="Qwen 3.5 (2B)",
        family_key="Qwen",
        out_path=DATA_DIR / "statistical_tests_qwen.txt",
        header_title="UJI STATISTIK ANTAR VARIAN KUANTISASI -- Qwen 3.5 (2B) di Tecno Pova 5",
        source_note=(
            "Sumber: docs/data/hasilv2_clean.csv (n=3 ulangan per varian).\n"
            "Catatan: pada varian Q5_K_M / Q4_K_M / Q3_K_M, ulangan ke-3 adalah\n"
            "rerata (imputasi 'mean replicate') dari dua ulangan eksperimental\n"
            "akibat keterbatasan termal perangkat. Konsekuensinya variansi\n"
            "sample ter-deflasi sehingga nilai p menjadi lebih kecil dibanding\n"
            "kondisi ulangan eksperimental penuh -- nilai p di bawah harus\n"
            "dibaca sebagai indikatif, bukan inferensi definitif."
        ),
    ),
]


def build_family_lines(df: pd.DataFrame, cfg: FamilyConfig) -> list[str]:
    sub = df[df["Model"].str.contains(cfg.family_key, case=False)].copy()
    sub["Variant"] = sub["Model"].str.extract(r"(F16|Q3_K_M|Q4_K_M|Q5_K_M)")

    lines: list[str] = []
    lines.append(cfg.header_title)
    lines.append(cfg.source_note)
    lines.append("Metode: Welch's t-test (alpha=0,05) + one-way ANOVA")
    lines.append("=" * 78)

    for metric_label, col in METRICS:
        lines.append(f"\n## Metrik: {metric_label}")
        header = (
            f"{'Pasangan':<22} | {'mean A':>9} | {'mean B':>9} "
            f"| {'t':>7} | {'p-value':>9} | hasil"
        )
        lines.append(header)
        lines.append("-" * len(header))
        for i, a in enumerate(VARIANTS):
            for b in VARIANTS[i + 1:]:
                ga = sub[sub["Variant"] == a][col].values
                gb = sub[sub["Variant"] == b][col].values
                if len(ga) < 2 or len(gb) < 2:
                    continue
                t, p = stats.ttest_ind(ga, gb, equal_var=False)
                sig = "** signifikan" if p < 0.05 else "tidak signifikan"
                lines.append(
                    f"{a + ' vs ' + b:<22} | {np.mean(ga):>9.2f} | {np.mean(gb):>9.2f} "
                    f"| {t:>7.3f} | {p:>9.4f} | {sig}"
                )
        groups = [sub[sub["Variant"] == v][col].values for v in VARIANTS]
        f, p = stats.f_oneway(*groups)
        verdict = "SIGNIFIKAN (p<0.05)" if p < 0.05 else "tidak signifikan"
        lines.append(f"One-way ANOVA (4 varian): F={f:.3f}, p={p:.5f}  ->  {verdict}")
    return lines


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    for cfg in FAMILIES:
        lines = build_family_lines(df, cfg)
        out_text = "\n".join(lines) + "\n"
        cfg.out_path.write_text(out_text, encoding="utf-8")
        print(out_text)
        print(f"\nDisimpan ke: {cfg.out_path}\n")


if __name__ == "__main__":
    main()
