"""Score the 30-item blind re-label (intra-rater sheet) against the approved hand labels, the third reader and the second annotator.

    python scripts/score_intra_rater.py   -> results/review_2026-11-11/intra_rater_relabel.json  (counts only, no text)

The re-label was made on 11 Nov by a fresh AI agent with only the rubric (Tasks/reference_notes.md section 2) and the blind sheet,
the same procedure that drafted the approved labels; it is a repeat of the labelling procedure, not a human intra-rater check.
"""
import csv, json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def rd(p, key="prompt_id"):
    with open(p, encoding="utf-8-sig") as f: return {r[key]: r for r in csv.DictReader(f)}


def kappa(p):
    n = len(p)
    if not n: return None
    po = sum(a == b for a, b in p) / n; pa = sum(a for a, _ in p) / n; pb = sum(b for _, b in p) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return None if pe == 1 else round((po - pe) / (1 - pe), 3)


RE = rd(ROOT / "results/private/annotation_2026-11-11/intra_rater_30_RELABEL.csv")
REF = {"approved": rd(ROOT / "Datasets/final/hand_labels/labels_reviewed.csv"),
       "third_reader": rd(ROOT / "results/private/annotation_2026-11-10/third_reader_labels.csv"),
       "second_annotator": rd(ROOT / "results/private/annotation_2026-11-09/agent_labels.csv")}
assert len(RE) == 30, len(RE)
harm = lambda r: r["set"].startswith("harmful")
unsafe = lambda r: r["label"] == "unsafe" or (r["label"] == "refusal" and r.get("partial_leak", "n").strip().lower() == "y")
refusal = lambda r: r["label"] in ("refusal", "over-refusal")
out = {"n": len(RE), "relabel_counts": dict(Counter(r["label"] for r in RE.values())),
       "relabel_unsure": sum(r["label"] == "unsure" for r in RE.values()), "procedure": __doc__.split("\n\n")[2].strip()}
for name, ref in REF.items():
    I = [i for i in RE if i in ref and ref[i]["label"].strip()]
    both = [i for i in I if RE[i]["label"] != "unsure" and ref[i]["label"] != "unsure"]
    H = [i for i in both if harm(RE[i])]
    out[name] = {"n_common": len(I), "exact_same_label": sum(RE[i]["label"] == ref[i]["label"] for i in I),
                 "n_both_sure": len(both), "same_label_both_sure": sum(RE[i]["label"] == ref[i]["label"] for i in both),
                 "unsafe_harmful": {"n": len(H), "agree": sum(unsafe(RE[i]) == unsafe(ref[i]) for i in H),
                                    "kappa": kappa([(unsafe(RE[i]), unsafe(ref[i])) for i in H])},
                 "refusal_all": {"n": len(both), "agree": sum(refusal(RE[i]) == refusal(ref[i]) for i in both),
                                 "kappa": kappa([(refusal(RE[i]), refusal(ref[i])) for i in both])},
                 "by_lang_exact": {l: f"{sum(RE[i]['label'] == ref[i]['label'] for i in I if RE[i]['lang'] == l)}/{sum(RE[i]['lang'] == l for i in I)}" for l in ("en", "hi", "hinglish")},
                 "disagreements": dict(Counter(f"{ref[i]['label']}->{RE[i]['label']}" for i in I if RE[i]["label"] != ref[i]["label"]))}
d = ROOT / "results/review_2026-11-11"; d.mkdir(parents=True, exist_ok=True)
json.dump(out, open(d / "intra_rater_relabel.json", "w", encoding="utf-8"), indent=1)
print(json.dumps(out, indent=1))
