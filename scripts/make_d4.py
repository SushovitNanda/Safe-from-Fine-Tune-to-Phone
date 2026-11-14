"""D4 hand-off package for Manish (plan v3): RQ3 tensor tables in GGUF names + layer suggestions + G3a evidence, and the
D2 merge hashes. Text-free; copies existing result files and writes an aggregated table in the exporter's schema.

    python scripts/make_d4.py   -> handoff/D4_2026-11-08/
"""
import hashlib, json, shutil
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "handoff" / "D4_2026-11-08"; OUT.mkdir(parents=True, exist_ok=True)
V2 = ROOT / "results" / "circuits" / "v2"
MATS = ["attn_q", "attn_k", "attn_v", "attn_output", "ffn_gate", "ffn_up", "ffn_down"]
copied = []


def cp(src, sub=""):
    d = OUT / sub; d.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, d / Path(src).name); copied.append(str((d / Path(src).name).relative_to(OUT)))


for lang in ("en", "hi", "hinglish"):
    for tag in ("orig", "med"):
        for ext in (".json", ".csv"):
            cp(V2 / "tables" / f"{tag}_{lang}_eap-ig_layer_x_matrix{ext}", "tables_per_language")
    cp(V2 / f"validation_{lang}.json", "validation")
    cp(V2 / "tables" / f"what_changed_{lang}.json", "what_changed")
cp(V2 / "tables" / "overlap_jaccard.json", "")
for p in sorted((ROOT / "locate").glob("cresta_tensors_v2*.json")): cp(p, "tensor_lists")
cp(ROOT / "locate" / "token_sets_v2.json", "")
for m in ("med", "ctrl"):
    for f in ("tensor_sha256.json", "merge_info.json"):
        if (ROOT / "models" / "merged" / m / f).exists(): cp(ROOT / "models" / "merged" / m / f, f"d2_hashes/{m}")

# aggregated 36 x 7 table from the ranked union list (normalised |score| summed over the original model's three runs)
ranked = json.load(open(ROOT / "locate" / "cresta_tensors_v2.json", encoding="utf-8"))["ranked"]
score = {(r["layer"], r["matrix"]): r["score"] for r in ranked}
rows = [{"layer": l, **{m: score.get((l, m), 0.0) for m in MATS}} for l in range(36)]
layer_tot = sorted(((sum(r[m] for m in MATS), r["layer"]) for r in rows), reverse=True)
agg = {"run": "aggregate_orig_en_hi_hinglish", "model": "CohereLabs/tiny-aya-global", "lang": "en+hi+hinglish", "alg": "eap-ig",
       "recipe": "per language: EAP-IG node scores (original model, full run, MLP 0 excluded) summed per layer x matrix family (heads -> the four attention matrices, MLP -> the three FFN matrices), |score| normalised by the run's maximum, then summed over the three languages; identical to the ranking behind locate/cresta_tensors_v2_top{5,10,20}.json",
       "layer_x_matrix": rows, "layer_suggestions": [l for _, l in layer_tot[:8]],
       "note": "scores are equal across a layer's four attention matrices and across its three FFN matrices by construction (node-level attribution); rank at the layer x family level"}
json.dump(agg, open(OUT / "d4_aggregated_layer_x_matrix.json", "w", encoding="utf-8"), indent=1)
copied.append("d4_aggregated_layer_x_matrix.json")

# G3a evidence summary
g3 = {}
for lang in ("en", "hi", "hinglish"):
    v = json.load(open(V2 / f"validation_{lang}.json", encoding="utf-8"))
    g3[lang] = {"G3a_pass_k40": v["G3a_pass_k40"], "verdict": v["verdict"], "n_prompts": v["n_prompts"], "method": v.get("method")}
ov = json.load(open(V2 / "tables" / "overlap_jaccard.json", encoding="utf-8"))
json.dump({"G3a_rule": "necessity drop of the top-40 nodes (mean-ablation, preamble on, 100 harmful dev prompts) beats all 5 random same-size sets in at least one language",
           "G3a_pass": any(g3[l]["G3a_pass_k40"] for l in g3), "per_language": g3, "overlap_and_floors": ov},
          open(OUT / "g3a_evidence.json", "w", encoding="utf-8"), indent=1)
copied.append("g3a_evidence.json")

README = f"""# D4 hand-off (Sushovit -> Manish), 8 November 2026

Source: branch code_v2.2, results of chain B (circuits v2) on the laptop, 5-6 November. Nothing here contains model outputs.

## What is in here
- `tables_per_language/{{orig,med}}_{{en,hi,hinglish}}_eap-ig_layer_x_matrix.json|csv`: 36 layers x 7 matrices in GGUF names
  (`blk.<layer>.<matrix>.weight`), with `layer_suggestions`. Scores are summed node attributions (EAP-IG, token-set metric,
  original or medical model, MLP 0 excluded), so the four attention matrices of a layer share one value and the three FFN
  matrices share another: rank at the layer x family level.
- `d4_aggregated_layer_x_matrix.json`: the ONE table to drive protection, in your exporter's schema (`layer_x_matrix`, 36 layers,
  finite scores, `layer_suggestions`). Recipe inside the file; it is the same ranking as `tensor_lists/cresta_tensors_v2_top*.json`
  (top 5 / 10 / 20 % of the 252 matrices), which Sushovit uses for circuit-restricted ReSta, so RQ4 and RQ6 share one map.
- `g3a_evidence.json` + `validation/validation_*.json`: G3a **passes** by the pre-registered rule (necessity beats all five random
  sets at k = 40): Hinglish clearly (4.70 vs 1.47), English marginally (2.46 vs 2.43), Hindi not at k = 40 (-0.82 vs 0.76; passes at
  k = 60). Sufficiency (patching original node outputs into the medical model) beats random at every k in every language.
- `overlap_jaccard.json`: top-60 overlaps and split-half floors (orig vs med within language is at/above the floor in all three
  languages; cross-language overlaps are below the EN/HI floors).
- `what_changed/`: nodes whose importance dropped most from original to medical, per language.
- `token_sets_v2.json`: the refusal / compliance opener sets behind the metric.
- `d2_hashes/{{med,ctrl}}/tensor_sha256.json`, `merge_info.json`: the laptop merges' per-tensor sha256 (D2 parity check).

## Caveats to carry into the method text
- The validation statistic is not monotone in k (scores are signed): at k = 20 ablating the top set *raises* refusal in EN/HI.
- The map is the ORIGINAL model's circuit (the thing to protect); the medical tables are for the what-changed comparison only.
- Hinglish's own split-half floor is low (0.28-0.35): its circuit is weakly defined by 73 pairs.

## Files
""" + "\n".join(f"- {c}" for c in copied) + "\n"
(OUT / "README.md").write_text(README, encoding="utf-8")
man = {c: hashlib.sha256(open(OUT / c, "rb").read()).hexdigest() for c in copied + ["README.md"]}
json.dump(man, open(OUT / "MANIFEST.sha256.json", "w", encoding="utf-8"), indent=1)
print(f"D4 written to {OUT} ({len(copied)} files); G3a pass = {any(g3[l]['G3a_pass_k40'] for l in g3)}; layer suggestions {agg['layer_suggestions']}")
