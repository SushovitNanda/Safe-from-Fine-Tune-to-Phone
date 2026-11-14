"""RQ1/RQ2 figures from results/drift/summary.json (harness/rq_tables.py):
  figures/rq1_gap.pdf      original model: ASR per language x harm type (general vs clinical), 95 % CIs
  figures/rq2_drift.pdf    original / control / medical ASR per language (all harmful), 95 % CIs
  figures/rq2_harmtype.pdf medical - original by harm type and language (paired differences with CIs)

    python scripts/report/fig_rq12.py [--summary results/drift/summary.json] [--out Report/figures]
"""
import argparse, json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
INK, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#e6e5e0", "#ffffff"
COL = {"orig": "#2a78d6", "ctrl": "#eda100", "med": "#e34948", "general": "#2a78d6", "clinical": "#e34948"}
NAME = {"orig": "Original", "ctrl": "Control (Alpaca)", "med": "Medical (MedMCQA)"}
LANGS = [("all", "Pooled"), ("en", "English"), ("hi", "Hindi"), ("hinglish", "Hinglish")]
plt.rcParams.update({"font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED, "font.family": "DejaVu Sans"})


def style(ax, ylabel):
    ax.set_facecolor(SURF); ax.set_ylabel(ylabel); ax.yaxis.grid(True, color=GRID, linewidth=0.6, zorder=0); ax.set_axisbelow(True)
    for s in ("top", "right"): ax.spines[s].set_visible(False)


def bars(ax, series, langs, key_fn, w=0.26):
    for j, (k, name, col) in enumerate(series):
        for i, (lg, _) in enumerate(langs):
            r = key_fn(k, lg)
            if not r: continue
            x = i + (j - (len(series) - 1) / 2) * (w + 0.02)
            ax.bar(x, r["rate"], width=w, color=col, edgecolor=SURF, linewidth=1, label=name if i == 0 else None, zorder=2)
            ax.plot([x, x], r["ci95"], color=INK, linewidth=0.9, zorder=3)
            ax.text(x, 1.2, f"{r['rate']:.0f}", ha="center", va="bottom", fontsize=7, color=INK, zorder=4,
                    bbox=dict(boxstyle="round,pad=0.15", facecolor=SURF, edgecolor="none", alpha=0.85))
    ax.set_xticks(range(len(langs)), [l for _, l in langs]); ax.legend(frameon=False, ncol=3, loc="upper left", fontsize=8)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--summary", default=str(ROOT / "results" / "drift" / "summary.json")); ap.add_argument("--out", default=str(ROOT / "Report" / "figures"))
    a = ap.parse_args(); S = json.load(open(a.summary, encoding="utf-8")); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    R = S["rates"]
    # RQ1: original by harm type
    if "orig" in R:
        fig, ax = plt.subplots(figsize=(7.2, 3.0), facecolor=SURF); style(ax, "Attack success rate (%)")
        bars(ax, [("general", "General (Aya)", COL["general"]), ("clinical", "Clinical (ClinicSafe-Hi)", COL["clinical"])], LANGS,
             lambda ht, lg: R["orig"].get(f"asr|{ht}|{lg}"), w=0.34)
        ax.set_ylim(0, max(60, max(v["ci95"][1] for k, v in R["orig"].items() if k.startswith("asr|")) + 5))
        fig.tight_layout(); fig.savefig(out / "rq1_gap.pdf"); fig.savefig(out / "rq1_gap.png", dpi=150); plt.close(fig)
    # RQ2: three models
    series = [(k, NAME[k], COL[k]) for k in ("orig", "ctrl", "med") if k in R]
    if len(series) >= 2:
        fig, ax = plt.subplots(figsize=(7.2, 3.1), facecolor=SURF); style(ax, "Attack success rate (%)")
        bars(ax, series, LANGS, lambda k, lg: R[k].get(f"asr|all|{lg}"))
        ax.set_ylim(0, max(60, max(v["ci95"][1] for k in R for kk, v in R[k].items() if kk.startswith("asr|all|")) + 5))
        fig.tight_layout(); fig.savefig(out / "rq2_drift.pdf"); fig.savefig(out / "rq2_drift.png", dpi=150); plt.close(fig)
    # RQ2 by harm type: paired differences med - orig and med - ctrl
    D = S.get("rq2", {})
    if any(k.startswith("med-orig|") for k in D):
        fig, ax = plt.subplots(figsize=(7.2, 3.0), facecolor=SURF); style(ax, "Medical − original (points)")
        ax.axhline(0, color=MUTED, linewidth=0.8)
        for j, (ht, col) in enumerate((("general", COL["general"]), ("clinical", COL["clinical"]))):
            for i, (lg, _) in enumerate(LANGS):
                d = D.get(f"med-orig|{ht}|{lg}")
                if not d: continue
                x = i + (j - 0.5) * 0.36
                ax.bar(x, d["diff"], width=0.34, color=col, edgecolor=SURF, label=ht if i == 0 else None, zorder=2)
                ax.plot([x, x], d["ci95"], color=INK, linewidth=0.9, zorder=3)
        ax.set_xticks(range(len(LANGS)), [l for _, l in LANGS]); ax.legend(frameon=False, ncol=2, loc="upper left", fontsize=8)
        fig.tight_layout(); fig.savefig(out / "rq2_harmtype.pdf"); fig.savefig(out / "rq2_harmtype.png", dpi=150); plt.close(fig)
    print("figures written to", out)


if __name__ == "__main__":
    main()
