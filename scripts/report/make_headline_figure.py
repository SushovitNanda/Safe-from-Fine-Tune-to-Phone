"""Headline figure: attack success along the deployment chain, pooled (856 harmful prompts) and English plus Hindi only
(604 prompts; Hinglish excluded because most of the fine-tuned model's Hinglish answers are degenerate). Every value is
read from the result files. Writes Report/figures/fig_headline.png (report executive summary and submission README)."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
A = json.loads((ROOT / "results/repair_test/summary.json").read_text(encoding="utf-8"))["asr"]
G = json.loads((ROOT / "results/final_stats/final.json").read_text(encoding="utf-8"))["gguf"]["rates"]


def enhi(d):
    """Rate over English + Hindi from the per-language rates and counts."""
    k = sum(round(d[l]["rate"] * d[l]["n"] / 100) for l in ("en", "hi")); n = d["en"]["n"] + d["hi"]["n"]
    return 100 * k / n


steps = [
    ("Original\n(FP16)", A["Original"]),
    ("+ medical LoRA\n(FP16)", A["Medical"]),
    ("+ steering\nvector (FP16)", A["Steer L24 s0.5"]),
    ("medical,\nQ3_K_M GGUF", G["q3km"]["med"]),
    ("+ vector,\nQ3_K_M GGUF", G["q3km"]["steer"]),
    ("+ vector, Q3_K_M,\nno preamble,\n4-bit KV cache", G["budget-phone"]["steer"]),
]
pooled = [d["all"]["rate"] for _, d in steps]
eh = [enhi(d) for _, d in steps]

INK, MUTED, GRID = "#2b2b2b", "#6b6b6b", "#e3e3e3"
C_POOL, C_EH = "#4f7cac", "#d08c3a"
fig, ax = plt.subplots(figsize=(8.8, 4.5), dpi=200)
w = 0.36; xs = list(range(len(steps)))
b1 = ax.bar([x - w / 2 - 0.01 for x in xs], pooled, w, color=C_POOL, label="All three languages (856 prompts)", zorder=3)
b2 = ax.bar([x + w / 2 + 0.01 for x in xs], eh, w, color=C_EH, label="English + Hindi only (604 prompts)", zorder=3)
for bars, vals in ((b1, pooled), (b2, eh)):
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.7, f"{v:.1f}", ha="center", va="bottom", fontsize=8, color=INK)
ax.axvline(2.5, color=GRID, lw=1.2, zorder=1)
ax.text(1.0, max(pooled) * 1.16, "Full precision (laptop, Transformers)", ha="center", fontsize=8, color=MUTED)
ax.text(4.0, max(pooled) * 1.16, "Deployed GGUF (Mac, llama.cpp)", ha="center", fontsize=8, color=MUTED)
ax.set_xticks(xs); ax.set_xticklabels([s for s, _ in steps], fontsize=8, color=INK)
ax.set_ylabel("Attack success rate (%)", fontsize=9, color=INK)
ax.set_ylim(0, max(pooled) * 1.26)
ax.yaxis.grid(True, color=GRID, lw=0.8, zorder=0); ax.set_axisbelow(True)
for s in ("top", "right"): ax.spines[s].set_visible(False)
for s in ("left", "bottom"): ax.spines[s].set_color(GRID)
ax.tick_params(axis="y", colors=MUTED, labelsize=8); ax.tick_params(axis="x", length=0)
ax.legend(frameon=False, fontsize=8.5, loc="upper center", bbox_to_anchor=(0.5, -0.24), ncol=2)
ax.set_title("Fine-tune, repair, deploy: attack success on the frozen test set", fontsize=10.5, color=INK, loc="left", pad=8)
fig.tight_layout()
out = ROOT / "Report/figures/fig_headline.png"; out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out)
print("pooled", [round(v, 1) for v in pooled]); print("en+hi ", [round(v, 1) for v in eh])
