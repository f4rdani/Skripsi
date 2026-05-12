#!/usr/bin/env python3
"""Uji statistik signifikansi antar varian kuantisasi untuk data Android.

Mengonsumsi `data/hasilv2_clean.csv` dan menghasilkan tabel Welch's t-test
serta one-way ANOVA untuk metrik:
  - Generation TPS
  - Prompt TPS
  - Peak RAM proses

Hasil disimpan ke `data/statistical_tests_lfm.txt` (plain text)
agar dapat direplikasi oleh penguji.

Run:
    python3 scripts/statistical_tests.py
"""
from __future__ import annotations
import sys
from pathlib import Path

try:
    import pandas as pd
    import numpy as np
    from scipy import stats
except ImportError:
    print("ERROR: butuh pandas + scipy. Jalankan: pip install pandas scipy")
    sys.exit(1)

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "hasilv2_clean.csv"
OUT_PATH = Path(__file__).resolve().parent.parent / "data" / "statistical_tests_lfm.txt"

VARIANTS = ["F16", "Q5_K_M", "Q4_K_M", "Q3_K_M"]
METRICS = [
    ("Generation TPS", "GenTPS"),
    ("Prompt TPS", "PromptTPS"),
    ("Peak RAM (MB)", "RAMUsed_MB"),
]


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    lfm = df[df["Model"].str.contains("LFM", case=False)].copy()
    lfm["Variant"] = lfm["Model"].str.extract(r"(F16|Q3_K_M|Q4_K_M|Q5_K_M)")

    lines: list[str] = []
    lines.append("UJI STATISTIK ANTAR VARIAN KUANTISASI -- LFM 2.5 (1,2B) di Tecno Pova 5")
    lines.append("Sumber: docs/data/hasilv2_clean.csv (n=3 ulangan per varian)")
    lines.append("Metode: Welch's t-test (alpha=0,05) + one-way ANOVA")
    lines.append("=" * 78)

    for metric_label, col in METRICS:
        lines.append(f"\n## Metrik: {metric_label}")
        header = f"{'Pasangan':<22} | {'mean A':>9} | {'mean B':>9} | {'t':>7} | {'p-value':>9} | hasil"
        lines.append(header)
        lines.append("-" * len(header))
        for i, a in enumerate(VARIANTS):
            for b in VARIANTS[i + 1:]:
                ga = lfm[lfm["Variant"] == a][col].values
                gb = lfm[lfm["Variant"] == b][col].values
                if len(ga) < 2 or len(gb) < 2:
                    continue
                t, p = stats.ttest_ind(ga, gb, equal_var=False)
                sig = "** signifikan" if p < 0.05 else "tidak signifikan"
                lines.append(
                    f"{a + ' vs ' + b:<22} | {np.mean(ga):>9.2f} | {np.mean(gb):>9.2f} "
                    f"| {t:>7.3f} | {p:>9.4f} | {sig}"
                )
        groups = [lfm[lfm["Variant"] == v][col].values for v in VARIANTS]
        f, p = stats.f_oneway(*groups)
        verdict = "SIGNIFIKAN (p<0.05)" if p < 0.05 else "tidak signifikan"
        lines.append(f"One-way ANOVA (4 varian): F={f:.3f}, p={p:.5f}  ->  {verdict}")

    out_text = "\n".join(lines) + "\n"
    OUT_PATH.write_text(out_text, encoding="utf-8")
    print(out_text)
    print(f"\nDisimpan ke: {OUT_PATH}")


if __name__ == "__main__":
    main()
