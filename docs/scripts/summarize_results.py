#!/usr/bin/env python3
"""Ringkas CSV per-run hasil benchmark.sh menjadi tabel mean +/- std.

Pemakaian:
    python3 summarize_results.py raw_<ts>.csv [--out summary.csv]

Akan menghasilkan:
- summary.csv : mean & std per (model, prompt_label) + agregat per model
- Cetak Markdown table ke stdout (siap copy-paste ke skripsi.md)
"""

from __future__ import annotations

import argparse
import csv
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path


NUMERIC_COLS = [
    "total_time_s",
    "prompt_tps",
    "gen_tps",
    "ttft_ms",
    "peak_ram_mb",
    "idle_ram_mb",
    "cpu_peak_pct",
    "cpu_temp_peak_c",
    "n_eval_tokens",
    "n_prompt_tokens",
]


def _to_float(s: str) -> float | None:
    try:
        f = float(s)
        if math.isnan(f):
            return None
        return f
    except (TypeError, ValueError):
        return None


def load_rows(path: Path) -> list[dict]:
    with path.open() as f:
        return list(csv.DictReader(f))


def aggregate(rows: list[dict], group_cols: list[str]):
    buckets: dict[tuple, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    for r in rows:
        key = tuple(r[c] for c in group_cols)
        for col in NUMERIC_COLS:
            v = _to_float(r.get(col, ""))
            if v is not None:
                buckets[key][col].append(v)
    summary = []
    for key, cols in buckets.items():
        entry = dict(zip(group_cols, key))
        for col, values in cols.items():
            if not values:
                continue
            entry[f"{col}_mean"] = round(statistics.fmean(values), 3)
            entry[f"{col}_std"] = round(statistics.pstdev(values), 3) if len(values) > 1 else 0.0
            entry[f"{col}_n"] = len(values)
        summary.append(entry)
    return summary


def write_summary_csv(summary: list[dict], out_path: Path):
    if not summary:
        out_path.write_text("")
        return
    cols = list({k for s in summary for k in s.keys()})
    # stable order: group cols first
    head = [c for c in cols if c in ("model", "prompt_label")] + [c for c in cols if c not in ("model", "prompt_label")]
    with out_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=head)
        w.writeheader()
        for row in summary:
            w.writerow(row)


def print_markdown_table(model_summary: list[dict]):
    if not model_summary:
        print("(no data)")
        return

    header = (
        "| Model | Runs | Total Waktu (s) | Prompt TPS | Gen TPS | TTFT (ms) | Peak RAM (MB) | CPU Peak (%) | CPU Temp Peak (\u00b0C) |"
    )
    sep = "|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|"
    print(header)
    print(sep)

    def fmt(mean, std):
        if mean is None:
            return "-"
        if std and std > 0:
            return f"{mean:.2f} \u00b1 {std:.2f}"
        return f"{mean:.2f}"

    for s in sorted(model_summary, key=lambda x: x.get("model", "")):
        row = [
            s.get("model", "-"),
            str(int(s.get("total_time_s_n", 0))),
            fmt(s.get("total_time_s_mean"), s.get("total_time_s_std")),
            fmt(s.get("prompt_tps_mean"), s.get("prompt_tps_std")),
            fmt(s.get("gen_tps_mean"), s.get("gen_tps_std")),
            fmt(s.get("ttft_ms_mean"), s.get("ttft_ms_std")),
            fmt(s.get("peak_ram_mb_mean"), s.get("peak_ram_mb_std")),
            fmt(s.get("cpu_peak_pct_mean"), s.get("cpu_peak_pct_std")),
            fmt(s.get("cpu_temp_peak_c_mean"), s.get("cpu_temp_peak_c_std")),
        ]
        print("| " + " | ".join(row) + " |")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("csv_path", type=Path, help="raw_<timestamp>.csv dari benchmark.sh")
    ap.add_argument("--out", type=Path, default=None, help="path summary CSV (default: <input>.summary.csv)")
    args = ap.parse_args(argv)

    if not args.csv_path.exists():
        print(f"[ERROR] file tidak ditemukan: {args.csv_path}", file=sys.stderr)
        return 1

    rows = load_rows(args.csv_path)
    if not rows:
        print("[ERROR] CSV kosong / tanpa baris data", file=sys.stderr)
        return 1

    out_path = args.out or args.csv_path.with_suffix(".summary.csv")

    # Per (model, prompt) bucket
    by_model_prompt = aggregate(rows, ["model", "prompt_label"])
    # Per model agregat (lintas prompt)
    by_model = aggregate(rows, ["model"])

    write_summary_csv(by_model_prompt + by_model, out_path)

    print(f"# Ringkasan benchmark — {args.csv_path.name}")
    print()
    print("## Per Model (rata-rata seluruh prompt & run)")
    print()
    print_markdown_table(by_model)
    print()
    print("## Per Model x Prompt")
    print()

    header = (
        "| Model | Prompt | Runs | Total Waktu (s) | Prompt TPS | Gen TPS | TTFT (ms) | Peak RAM (MB) |"
    )
    sep = "|---|:---:|:--:|:--:|:--:|:--:|:--:|:--:|"
    print(header)
    print(sep)

    def fmt(mean, std):
        if mean is None:
            return "-"
        if std and std > 0:
            return f"{mean:.2f} \u00b1 {std:.2f}"
        return f"{mean:.2f}"

    for s in sorted(by_model_prompt, key=lambda x: (x.get("model", ""), x.get("prompt_label", ""))):
        row = [
            s.get("model", "-"),
            s.get("prompt_label", "-"),
            str(int(s.get("total_time_s_n", 0))),
            fmt(s.get("total_time_s_mean"), s.get("total_time_s_std")),
            fmt(s.get("prompt_tps_mean"), s.get("prompt_tps_std")),
            fmt(s.get("gen_tps_mean"), s.get("gen_tps_std")),
            fmt(s.get("ttft_ms_mean"), s.get("ttft_ms_std")),
            fmt(s.get("peak_ram_mb_mean"), s.get("peak_ram_mb_std")),
        ]
        print("| " + " | ".join(row) + " |")

    print()
    print(f"Summary CSV: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
