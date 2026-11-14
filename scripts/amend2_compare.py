"""PREREG amendment 2 check: the medical dev cell re-generated with the stopping fix against the frozen cell (same prompts,
same batching). Prints and writes text-free counts to results/private/amend2_check/compare.json.

    python scripts/amend2_compare.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(p):
    return {r["prompt_id"]: r for r in (json.loads(l) for l in open(p, encoding="utf-8") if l.strip())}


old = read(ROOT / "results/private/dev_pass__med__fp16/responses.jsonl")
new = read(ROOT / "results/private/amend2_check/private/amend2_med/responses.jsonl")
ids = sorted(set(old) & set(new))
same, prefix, diff, diff_ids = 0, 0, 0, []
for i in ids:
    a, b = old[i]["text"].strip(), new[i]["text"].strip()
    if a == b: same += 1
    elif a.startswith(b): prefix += 1
    else: diff += 1; diff_ids.append(i)
n_new = [new[i]["n_tokens"] for i in ids]
out = {"n": len(ids), "identical_text": same, "new_is_prefix_of_frozen": prefix, "different": diff, "different_ids": diff_ids,
       "mean_tokens_frozen": round(sum(old[i]["n_tokens"] for i in ids) / len(ids), 1), "mean_tokens_new": round(sum(n_new) / len(ids), 1),
       "capped_new": sum(1 for x in n_new if x >= 256)}
json.dump(out, open(ROOT / "results/private/amend2_check/compare.json", "w", encoding="utf-8"), indent=1)
print(json.dumps(out, indent=1))
