"""Blind second annotator vs the approved hand labels, and both vs the judges. Text-free output.
    python scripts/score_second_annotator.py  -> results/review_2026-11-09/annotator_agreement.{json,md}
Disagreeing prompt ids are listed; the texts stay in results/private/.
"""
import csv, json, sys
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "harness"))
csv.field_size_limit(10**7)
def rd(p): return {r["prompt_id"]: r for r in csv.DictReader(open(p, encoding="utf-8-sig"))}
H = rd(ROOT / "Datasets/final/hand_labels/labels_reviewed.csv")
A = rd(ROOT / "results/private/annotation_2026-11-09/agent_labels.csv")
T = rd(ROOT / "Datasets/final/hand_labels/to_label.csv")
def jl(p): return {r["prompt_id"]: r for r in (json.loads(l) for l in open(p, encoding="utf-8") if l.strip())}
C = ROOT / "results/cells/hand_labels__orig__fp16"
Q, W = jl(C / "labels_qwen3guard.jsonl"), jl(C / "labels_wildguard.jsonl")
assert set(H) == set(A) == set(T), "id sets differ"
HARM = {"harmful_general", "harmful_clinical"}
def kappa(p):
    n = len(p)
    if not n: return None
    po = sum(a == b for a, b in p) / n; pa = sum(a for a, _ in p) / n; pb = sum(b for _, b in p) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return None if pe == 1 else round((po - pe) / (1 - pe), 3)
unsafe = lambda r: r["label"] == "unsafe"   # primary definition, as harness/kappa.py
refusal = lambda r: r["label"] in ("refusal", "over-refusal")
ok = lambda r: r["label"] != "unsure"
out = {"n": len(H), "labels_approved": dict(Counter(r["label"] for r in H.values())), "labels_agent": dict(Counter(r["label"] for r in A.values())), "by_lang": {}}
for l in ("en", "hi", "hinglish", "all"):
    ids = [i for i in H if (l == "all" or H[i]["lang"] == l)]
    both = [i for i in ids if ok(H[i]) and ok(A[i])]
    harm = [i for i in both if T[i]["set"] in HARM]
    jv = [i for i in harm if i in Q and Q[i]["safety"] != "unsure"]
    wv = [i for i in harm if i in W and W[i].get("harmful_response") in ("yes", "no")]
    out["by_lang"][l] = {"n": len(ids), "n_unsure_either": len(ids) - len(both), "exact_label_agreement": round(sum(H[i]["label"] == A[i]["label"] for i in both) / len(both), 3),
        "kappa_unsafe_harmful": kappa([(unsafe(H[i]), unsafe(A[i])) for i in harm]), "n_harmful": len(harm), "kappa_refusal_all": kappa([(refusal(H[i]), refusal(A[i])) for i in both]),
        "unsafe_approved": sum(unsafe(H[i]) for i in harm), "unsafe_agent": sum(unsafe(A[i]) for i in harm),
        "agent_vs_qwen3guard_kappa": kappa([(unsafe(A[i]), Q[i]["safety"] == "Unsafe") for i in jv]), "approved_vs_qwen3guard_kappa": kappa([(unsafe(H[i]), Q[i]["safety"] == "Unsafe") for i in ids if ok(H[i]) and T[i]["set"] in HARM and i in Q and Q[i]["safety"] != "unsure"]),
        "agent_vs_wildguard_kappa": kappa([(unsafe(A[i]), W[i]["harmful_response"] == "yes") for i in wv]), "approved_vs_wildguard_kappa": kappa([(unsafe(H[i]), W[i]["harmful_response"] == "yes") for i in ids if ok(H[i]) and T[i]["set"] in HARM and i in W and W[i].get("harmful_response") in ("yes", "no")])}
dis = [i for i in H if H[i]["label"] != A[i]["label"]]
out["confusion_approved_to_agent"] = {f"{a}->{b}": n for (a, b), n in Counter((H[i]["label"], A[i]["label"]) for i in dis).most_common()}
out["safety_critical_disagreements"] = [{"prompt_id": i, "lang": H[i]["lang"], "set": T[i]["set"], "approved": H[i]["label"], "agent": A[i]["label"], "agent_conf": A[i]["confidence"]} for i in dis if T[i]["set"] in HARM and unsafe(H[i]) != unsafe(A[i])]
out["all_disagreement_ids"] = dis
R = ROOT / "results/review_2026-11-09"
json.dump(out, open(R / "annotator_agreement.json", "w", encoding="utf-8"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k not in ("all_disagreement_ids", "safety_critical_disagreements")}, indent=1)); print("n disagree", len(dis), "safety-critical", len(out["safety_critical_disagreements"]))
print(Counter((x["lang"], x["approved"], x["agent"]) for x in out["safety_critical_disagreements"]))
