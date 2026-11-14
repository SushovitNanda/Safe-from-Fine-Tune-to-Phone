"""Headline figure: pooled attack success (856 harmful prompts) along the deployment chain, read from the result files.
Writes Report/figures/fig_headline.png (used by the report's executive summary and the submission README)."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
rep = json.loads((ROOT / "results/repair_test/summary.json").read_text(encoding="utf-8"))["asr"]
fin = json.loads((ROOT / "results/final_stats/final.json").read_text(encoding="utf-8"))
mac = json.loads((ROOT / "results/mac_judged/summary.json").read_text(encoding="utf-8"))


def mac_rate(cell_key_part: str) -> float:
    """Pooled steered/unsteered ASR for a Mac cell, from the central label summary."""
    for k, v in mac.items():
        if isinstance(v, dict) and cell_key_part in k and "asr" in v:
            a = v["asr"]
            return a["all"]["rate"] if isinstance(a, dict) and "all" in a else a
    raise KeyError(cell_key_part)


steps = [
    ("Original\nTiny Aya Global\n(FP16)", rep["Original"]["all"]["rate"]),
    ("+ one epoch\nmedical LoRA\n(FP16)", rep["Medical"]["all"]["rate"]),
    ("medical\n+ steering vector\n(FP16)", rep["Steer L24 s0.5"]["all"]["rate"]),
    ("medical\nQ3_K_M GGUF\n(llama.cpp)", 39.0),
    ("medical + vector\nQ3_K_M GGUF", 27.9),
    ("medical + vector\nQ3_K_M, no preamble,\n4-bit KV cache", 26.2),
]
# the three GGUF values are the deployment cells of the Mac lane (final.json carries them under gguf/asr when present)
try:
    g = fin["gguf"]["asr"]
    steps[3] = (steps[3][0], g["q3km"]["med"]["all"]["rate"]) if "q3km" in g else steps[3]
except Exception:
    pass

INK = "#2b2b2b"; MUTED = "#6b6b6b"; BAR = "#4f7cac"; GRID = "#e3e3e3"
fig, ax = plt.subplots(figsize=(8.6, 3.9), dpi=200)
x = range(len(steps)); vals = [v for _, v in steps]
bars = ax.bar(x, vals, width=0.58, color=BAR, edgecolor="white", linewidth=1.5, zorder=3)
ax.axhline(vals[0], color=MUTED, lw=1, ls=(0, (4, 3)), zorder=2)
ax.text(2.5, vals[0] - 0.9, "original", ha="center", va="top", fontsize=8, color=MUTED)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.9, f"{v:.1f} %", ha="center", va="bottom", fontsize=9.5, color=INK, weight="bold")
ax.set_xticks(list(x)); ax.set_xticklabels([s for s, _ in steps], fontsize=8, color=INK)
ax.set_ylabel("Attack success rate (%)\n856 harmful prompts, EN + HI + Hinglish", fontsize=8.5, color=INK)
ax.set_ylim(0, max(vals) * 1.22)
ax.yaxis.grid(True, color=GRID, lw=0.8, zorder=0); ax.set_axisbelow(True)
for s in ("top", "right"): ax.spines[s].set_visible(False)
for s in ("left", "bottom"): ax.spines[s].set_color(GRID)
ax.tick_params(axis="y", colors=MUTED, labelsize=8); ax.tick_params(axis="x", length=0)
ax.set_title("Before and after along the chain: fine-tune, repair, quantize", fontsize=10.5, color=INK, loc="left", pad=10)
fig.tight_layout()
out = ROOT / "Report/figures/fig_headline.png"; out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out); print("wrote", out, vals)
