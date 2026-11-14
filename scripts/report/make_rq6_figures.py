"""House-style replacements for the two Mac-lane D8 figures: fig_rq5_retention.png and fig_rq6_protection.png, from final.json."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
F = json.load(open(ROOT / "results/final_stats/final.json", encoding="utf-8"))
OUT = ROOT / "Report/figures"
BLUE, ORANGE, GREEN, GREY = "#2b6cb0", "#dd6b20", "#2f855a", "#718096"
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False})

# retention
G = F["gguf"]["retention"]; S = ["q4km", "q3km", "q4km-nopre", "budget-phone"]; N = ["Q4_K_M", "Q3_K_M", "Q4_K_M,\nno preamble", "Budget-phone\nstack"]
fig, ax = plt.subplots(figsize=(6.2, 3.4))
for i, s in enumerate(S):
    r = G[s]["all"]; lo, hi = r["ci95"]
    ax.errorbar(i, r["R"], yerr=[[r["R"] - lo], [hi - r["R"]]], fmt="o", color=BLUE, ms=7, capsize=4, lw=1.6)
    ax.text(i + 0.12, r["R"], f"{r['R']:.2f}", va="center", fontsize=10)
ax.axhline(1, color=GREY, ls="--", lw=1); ax.set_xticks(range(4)); ax.set_xticklabels(N); ax.set_ylabel("Retention R(s)"); ax.set_ylim(0.3, 1.7)
ax.set_title("")
fig.tight_layout(); fig.savefig(OUT / "fig_rq5_retention.png", dpi=220); plt.close(fig)

# rq6
R6 = F["rq6"]; L = ["all", "en", "hi", "hinglish"]; LN = ["Pooled", "English", "Hindi", "Hinglish"]
fig, ax = plt.subplots(figsize=(6.6, 3.6)); w = 0.26
for j, (k, n, c) in enumerate((("stock", "Stock", GREY), ("protected", "Protected", BLUE), ("random", "Random", ORANGE))):
    vals = [R6["rates"][k][l]["rate"] for l in L]; errs = [[R6["rates"][k][l]["rate"] - R6["rates"][k][l]["ci95"][0] for l in L], [R6["rates"][k][l]["ci95"][1] - R6["rates"][k][l]["rate"] for l in L]]
    ax.bar([i + (j - 1) * w for i in range(4)], vals, w, yerr=errs, color=c, capsize=3, label=n, error_kw={"lw": 1})
ax.set_xticks(range(4)); ax.set_xticklabels(LN); ax.set_ylabel("Attack success (%)"); ax.legend(loc="upper center", ncol=3, bbox_to_anchor=(0.5, 1.14)); ax.set_ylim(0, 85)
ax.text(3.0, 78, "Hinglish: judge artefact on\ndegenerate text (see text)", fontsize=8.5, ha="center", color=GREY)
fig.tight_layout(); fig.savefig(OUT / "fig_rq6_protection.png", dpi=220); plt.close(fig)
print("written retention and rq6 figures")
