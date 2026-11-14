"""Figure for the report: dev drift probe ASR per model and language, with 95 % bootstrap CIs.

    python scripts/report/fig_probe_dev.py   -> Report/figures/probe_dev.pdf
"""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
S = json.load(open(ROOT / "results" / "probe_dev" / "summary.json", encoding="utf-8"))["cells"]
MODELS = [("probe_dev__orig__fp16", "Original", "#2a78d6"),
          ("probe_dev__ctrl__fp16", "Control (Alpaca)", "#eda100"),
          ("probe_dev__med__fp16", "Medical (MedMCQA)", "#e34948")]
LANGS = [("all", "Pooled (n=150)"), ("en", "English"), ("hi", "Hindi"), ("hinglish", "Hinglish")]
INK, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#e6e5e0", "#ffffff"

plt.rcParams.update({"font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
                     "xtick.color": MUTED, "ytick.color": MUTED, "font.family": "DejaVu Sans"})
fig, ax = plt.subplots(figsize=(7.2, 3.1), facecolor=SURF)
ax.set_facecolor(SURF)
w, gap = 0.26, 0.02
for j, (cell, name, col) in enumerate(MODELS):
    for i, (lg, _) in enumerate(LANGS):
        r = S[cell][f"asr|pooled|{lg}"]
        x = i + (j - 1) * (w + gap)
        ax.bar(x, r["rate"], width=w, color=col, edgecolor=SURF, linewidth=1, label=name if i == 0 else None, zorder=2)
        ax.plot([x, x], r["ci95"], color=INK, linewidth=0.9, zorder=3)
        ax.text(x, 1.2, f"{r['rate']:.1f}" if lg == "all" else f"{r['rate']:.0f}", ha="center", va="bottom",
                fontsize=7, color=INK, zorder=4,
                bbox=dict(boxstyle="round,pad=0.15", facecolor=SURF, edgecolor="none", alpha=0.85))
ax.set_xticks(range(len(LANGS)), [l for _, l in LANGS])
ax.set_ylabel("Attack success rate (%)")
ax.set_ylim(0, 65)
ax.yaxis.grid(True, color=GRID, linewidth=0.6, zorder=0)
ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.legend(frameon=False, ncol=3, loc="upper left", fontsize=8)
fig.tight_layout()
out = ROOT / "Report" / "figures" / "probe_dev.pdf"
fig.savefig(out)
fig.savefig(out.with_suffix(".png"), dpi=150)
print("written", out)
