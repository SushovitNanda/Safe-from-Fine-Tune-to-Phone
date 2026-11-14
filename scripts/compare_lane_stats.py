"""Cross-check Manish's deployment statistics (his scripts/mac/deployment_stats.py, re-run on the central labels) against the laptop's
harness/final_stats.py. Writes results/review_2026-11-10/lane_stats_crosscheck.{json,md}.
"""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
M = json.load(open(ROOT / "results/review_2026-11-10/manish_deployment_rerun/deployment_analysis.json", encoding="utf-8"))
F = json.load(open(ROOT / "results/final_stats/final.json", encoding="utf-8"))["gguf"]
rows, out = [], {"paired": [], "retention": [], "summary": {}}
comp = {(c["a"], c["b"], c["metric"], c["subset"], c["lang"]): c for c in M.get("comparisons", [])}
def mine_effect(s, l): return F["steer_effect"][s][l]
for s in ("f16", "q4km", "q3km", "q4km-nopre", "budget-phone"):
    for l in ("all", "en", "hi", "hinglish"):
        c = comp.get((f"rep_steer_{s}", f"med_{s}", "asr", "pooled", l))
        if c:
            m = mine_effect(s, l); out["paired"].append({"contrast": f"steered - medical {s}", "lang": l, "manish": round(c["difference_pp"], 2), "laptop": m["diff"], "manish_ci": [round(x, 2) for x in c["ci95_pp"]], "laptop_ci": m["ci95"]})
for s in ("q4km", "q3km", "q4km-nopre"):
    for l in ("all", "en", "hi", "hinglish"):
        c = comp.get((f"rep_steer_{s}", "rep_steer_f16" if s != "q4km-nopre" else "rep_steer_q4km", "asr", "pooled", l))
        if c and s != "q4km-nopre":
            m = F["loss_steered"][s][l]; out["paired"].append({"contrast": f"steered {s} - steered F16", "lang": l, "manish": round(c["difference_pp"], 2), "laptop": m["diff"], "manish_ci": [round(x, 2) for x in c["ci95_pp"]], "laptop_ci": m["ci95"]})
R = M.get("retention", {})
for k, v in R.items():
    s, sub, l = k.split("|")
    if sub != "pooled" or s not in F["retention"]: continue
    m = F["retention"][s][l]; out["retention"].append({"setting": s, "lang": l, "manish": None if not v.get("available") else round(v["retention"], 3), "laptop": m["R"], "manish_ci": v.get("ci95"), "laptop_ci": m.get("ci95"), "manish_status": v.get("interval_status") or v.get("reason")})
d = [abs(x["manish"] - x["laptop"]) for x in out["paired"]]; r = [abs(x["manish"] - x["laptop"]) for x in out["retention"] if x["manish"] is not None and x["laptop"] is not None]
out["summary"] = {"paired_compared": len(d), "max_abs_point_diff": round(max(d), 3) if d else None, "retention_compared": len(r), "max_abs_R_diff": round(max(r), 4) if r else None, "manish_comparisons_total": len(M.get("comparisons", [])), "keys": list(M.keys())}
json.dump(out, open(ROOT / "results/review_2026-11-10/lane_stats_crosscheck.json", "w", encoding="utf-8"), indent=1)
md = ["# Cross-check of the two lanes' deployment statistics (10 Nov)", "", f"Manish's `scripts/mac/deployment_stats.py` was re-run on the central labels (a no-op stand-in for the Mac-only `fcntl` module; his code unchanged) and compared with `harness/final_stats.py`. {out['summary']}", "", "| contrast | lang | Manish | laptop | Manish CI | laptop CI |", "|---|---|---|---|---|---|"]
for x in out["paired"]: md.append(f"| {x['contrast']} | {x['lang']} | {x['manish']} | {x['laptop']} | {x['manish_ci']} | {x['laptop_ci']} |")
md += ["", "| R(s) | lang | Manish | laptop | Manish CI | laptop CI | Manish status |", "|---|---|---|---|---|---|---|"]
for x in out["retention"]: md.append(f"| {x['setting']} | {x['lang']} | {x['manish']} | {x['laptop']} | {x['manish_ci']} | {x['laptop_ci']} | {x['manish_status']} |")
(ROOT / "results/review_2026-11-10/lane_stats_crosscheck.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print(json.dumps(out["summary"], indent=1))
