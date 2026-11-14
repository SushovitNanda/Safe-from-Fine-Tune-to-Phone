"""Does the back-translation batch size change the Hindi WildGuard verdicts? Medical test cell: frozen run (batch 8) vs re-run (batch 16).
Text-free output: results/final_stats/bt_batch_check.json
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HARM = {"harmful_general", "harmful_clinical"}


def rd(p):
    return {r["prompt_id"]: r for r in (json.loads(l) for l in open(p, encoding="utf-8") if l.strip())}


FROZEN, NEW = "med__fp16__f16__tpl-official", "btcheck16__med__fp16"
a, b = rd(ROOT / f"results/cells/{FROZEN}/labels_wildguard.jsonl"), rd(ROOT / f"results/cells/{NEW}/labels_wildguard.jsonl")
q = rd(ROOT / f"results/cells/{FROZEN}/labels_qwen3guard.jsonl")
ids = sorted(i for i in a if i in b and q[i]["lang"] == "hi")
harm = [i for i in ids if q[i]["set"] in HARM]
ta = rd(ROOT / f"results/judges/backtranslation_{FROZEN}.jsonl"); tb = rd(ROOT / f"results/judges/backtranslation_{NEW}.jsonl")
out = {"n_hindi": len(ids), "n_hindi_harmful": len(harm), "verdict_identical": sum(a[i]["harmful_response"] == b[i]["harmful_response"] for i in ids),
       "asr_hi_batch8": round(100 * sum(a[i]["harmful_response"] == "yes" for i in harm) / len(harm), 2),
       "asr_hi_batch16": round(100 * sum(b[i]["harmful_response"] == "yes" for i in harm) / len(harm), 2),
       "changed_harmful_ids": [i for i in harm if a[i]["harmful_response"] != b[i]["harmful_response"]],
       "answer_back_translation_identical": sum(ta[i]["text_en"] == tb[i]["text_en"] for i in ids if i in ta and i in tb)}
d = ROOT / "results/final_stats"; d.mkdir(parents=True, exist_ok=True)
json.dump(out, open(d / "bt_batch_check.json", "w", encoding="utf-8"), indent=1); print(json.dumps(out, indent=1))
