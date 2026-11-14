"""Final audit: majority votes over independent label sources (counts only, no text).

    python scripts/majority_vote.py   -> results/review_final/majority_vote.json

Part 1, hand labels (300 items): votes = approved labels, blind second annotator (9 Nov), blind third vote (final audit,
one agent per language). Majority label per item; items with three different labels keep the approved label and are flagged.
Judge kappa (primary unsafe task and refusal task, as harness/kappa.py) is recomputed against the majority labels.
Part 2, RQ6 blind sample (160 answers: 30 discordant + 10 concordant prompts per language, EN and Hinglish, both builds):
votes = primary judge, auditor A, auditor B on unsafe / not unsafe; 'unsure' abstains; a 1-1 tie keeps the judge's label.
"""
import csv, json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / "results/private/audit_final"
HARM = {"harmful_general", "harmful_clinical"}


def rd(p, key="prompt_id"):
    with open(p, encoding="utf-8-sig", newline="") as f: return {r[key]: r for r in csv.DictReader(f)}


def jl(p): return {json.loads(l)["prompt_id"]: json.loads(l) for l in open(p, encoding="utf-8") if l.strip()}


def kappa(p):
    n = len(p)
    if not n: return None
    po = sum(a == b for a, b in p) / n; pa = sum(a for a, _ in p) / n; pb = sum(b for _, b in p) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return None if pe == 1 else round((po - pe) / (1 - pe), 3)


S = {}
# ---------------- Part 1
ap = rd(ROOT / "Datasets/final/hand_labels/labels_reviewed.csv"); sec = rd(ROOT / "results/private/annotation_2026-11-09/agent_labels.csv")
v3 = {}
for l in ("en", "hi", "hinglish"): v3.update(rd(A / f"vote3_{l}.csv"))
C = ROOT / "results/cells/hand_labels__orig__fp16"
sets = {i: r["set"] for i, r in jl(C / "records.jsonl").items()}; q3 = jl(C / "labels_qwen3guard.jsonl"); wg = jl(C / "labels_wildguard.jsonl")
assert set(ap) == set(sec) == set(v3) == set(sets), (len(ap), len(sec), len(v3), len(sets))
maj, kind = {}, {}
for i in ap:
    votes = [ap[i]["label"], sec[i]["label"], v3[i]["label"]]; c = Counter(votes).most_common()
    if c[0][1] >= 2: maj[i] = c[0][0]; kind[i] = "unanimous" if c[0][1] == 3 else ("approved_in_majority" if ap[i]["label"] == c[0][0] else "approved_outvoted")
    else: maj[i] = ap[i]["label"]; kind[i] = "three_way_split"
lang = {i: ap[i]["lang"] for i in ap}
P1 = {"n": len(ap), "by_kind": dict(Counter(kind.values())), "by_kind_lang": {l: dict(Counter(kind[i] for i in ap if lang[i] == l)) for l in ("en", "hi", "hinglish")},
      "outvoted_changes": dict(Counter(f"{ap[i]['label']}->{maj[i]}" for i in ap if kind[i] == "approved_outvoted")),
      "outvoted_changes_by_lang": {l: dict(Counter(f"{ap[i]['label']}->{maj[i]}" for i in ap if kind[i] == "approved_outvoted" and lang[i] == l)) for l in ("en", "hi", "hinglish")},
      "pairwise_exact": {"approved_vs_second": sum(ap[i]["label"] == sec[i]["label"] for i in ap), "approved_vs_third": sum(ap[i]["label"] == v3[i]["label"] for i in ap), "second_vs_third": sum(sec[i]["label"] == v3[i]["label"] for i in ap)},
      "unsafe_flag_changes": {l: {"approved_unsafe": sum(ap[i]["label"] == "unsafe" for i in ap if lang[i] == l and sets[i] in HARM), "majority_unsafe": sum(maj[i] == "unsafe" for i in ap if lang[i] == l and sets[i] in HARM),
                                  "flag_flips": sum((ap[i]["label"] == "unsafe") != (maj[i] == "unsafe") for i in ap if lang[i] == l and sets[i] in HARM)} for l in ("en", "hi", "hinglish")}}


def jud(j, i, task):
    if task == "unsafe": return (wg[i]["harmful_response"] == "yes") if j == "wildguard" else (q3[i]["safety"] == "Unsafe")
    return str((wg if j == "wildguard" else q3)[i]["refusal"]).lower() == "yes"


K = {}
for name, lab in (("approved", {i: ap[i]["label"] for i in ap}), ("majority", maj)):
    for j in ("qwen3guard", "wildguard"):
        for task in ("unsafe", "refusal"):
            for l in ("en", "hi", "hinglish"):
                I = [i for i in ap if lang[i] == l and lab[i] != "unsure" and (task == "refusal" or sets[i] in HARM)]
                h = (lambda i: lab[i] == "unsafe") if task == "unsafe" else (lambda i: lab[i] in ("refusal", "over-refusal"))
                K[f"{name}|{j}|{task}|{l}"] = {"n": len(I), "kappa": kappa([(h(i), jud(j, i, task)) for i in I])}
P1["kappa"] = K
P1["judge_choice_unsafe"] = {name: {l: max(("qwen3guard", "wildguard"), key=lambda j: K[f"{name}|{j}|unsafe|{l}"]["kappa"] or -9) for l in ("en", "hi", "hinglish")} for name in ("approved", "majority")}
P1["judge_choice_unchanged"] = P1["judge_choice_unsafe"]["approved"] == P1["judge_choice_unsafe"]["majority"]
S["hand_labels"] = P1

# ---------------- Part 2
key = json.load(open(A / "_rq6_key_DO_NOT_READ.json")); a = rd(A / "rq6_audit_A.csv", "item_id"); b = rd(A / "rq6_audit_B.csv", "item_id")
items = {json.loads(l)["item_id"]: json.loads(l)["lang"] for l in open(A / "rq6_blind.jsonl", encoding="utf-8")}
assert set(key) == set(a) == set(b) == set(items)
mj, how = {}, {}
for i, k in key.items():
    j = k["judge_safety"] == "Unsafe"; votes = [j] + [x[i]["label"] == "unsafe" for x in (a, b) if x[i]["label"] != "unsure"]
    y, n = sum(votes), len(votes) - sum(votes)
    mj[i] = j if y == n else y > n
    how[i] = "tie_kept_judge" if y == n else ("unanimous" if (y == 0 or n == 0) else ("judge_in_majority" if mj[i] == j else "judge_outvoted"))
P2 = {"n": len(key), "by_outcome": dict(Counter(how.values())), "auditors_agree_with_each_other": sum(a[i]["label"] == b[i]["label"] for i in key),
      "auditor_unsure": {"A": sum(a[i]["label"] == "unsure" for i in key), "B": sum(b[i]["label"] == "unsure" for i in key)}}
for l in ("en", "hinglish"):
    I = [i for i in key if items[i] == l]; ju = [i for i in I if key[i]["judge_safety"] == "Unsafe"]
    d = {"n": len(I), "judge_unsafe": len(ju), "majority_unsafe": sum(mj[i] for i in I), "judge_equals_majority": sum((key[i]["judge_safety"] == "Unsafe") == mj[i] for i in I),
         "judge_unsafe_overturned": sum(not mj[i] for i in ju), "judge_safe_overturned": sum(mj[i] for i in I if i not in ju),
         "judge_unsafe_marked_degenerate_by_both": sum(a[i]["degenerate"] == "y" and b[i]["degenerate"] == "y" for i in ju),
         "judge_unsafe_overturned_and_degenerate": sum((not mj[i]) and (a[i]["degenerate"] == "y" or b[i]["degenerate"] == "y") for i in ju)}
    # discordant pairs: direction under the judge and under the majority
    pairs = defaultdict(dict)
    for i in I:
        if key[i]["discordant"]: pairs[key[i]["prompt_id"]]["protected" if "protected" in key[i]["cell"] else "random"] = i
    dj = Counter(); dm = Counter()
    for pid, pr in pairs.items():
        jp, jr = key[pr["protected"]]["judge_safety"] == "Unsafe", key[pr["random"]]["judge_safety"] == "Unsafe"; mp, mr = mj[pr["protected"]], mj[pr["random"]]
        dj["protected_unsafe_only" if jp and not jr else "random_unsafe_only"] += 1
        dm["protected_unsafe_only" if mp and not mr else "random_unsafe_only" if mr and not mp else "both_unsafe" if mp and mr else "neither_unsafe"] += 1
    d["discordant_pairs"] = {"n": len(pairs), "judge": dict(dj), "majority": dict(dm)}
    P2[l] = d
S["rq6_sample"] = P2
out = ROOT / "results/review_final"; out.mkdir(parents=True, exist_ok=True)
json.dump(S, open(out / "majority_vote.json", "w", encoding="utf-8"), indent=1)
print(json.dumps(S, indent=1))
