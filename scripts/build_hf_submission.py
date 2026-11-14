"""Lay out HF_Submissions/: one folder per Hugging Face repository, grouped into the dataset collection and the model
collection the hackathon asks for, each with its card. Nothing is uploaded here; HF_Submissions/upload_hf.py does that
when the first author runs it.

    python scripts/build_hf_submission.py

Sources: Datasets/final (prompt sets), Datasets/interim (specifications), models/runs/*/adapter (LoRA adapters),
handoff/D5b (control vector), models/steer (calibration tensor), release/ (GGUF card and manifest), and the sanitised
results tree of Lexsi_Submissions/ (text-free records, labels, statistics). The three Q3_K_M GGUF files live on the
Mac; their repo folder gets the card, the manifest and a FILES_NEEDED list, and the upload script checks their SHA-256.
"""
from __future__ import annotations
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUB = ROOT / "Lexsi_Submissions"
OUT = ROOT / "HF_Submissions"
NS = "SushiOrbit"  # Hugging Face namespace; the upload script takes HF_NAMESPACE to override
TEAM = "Sushovit Nanda and Manish Shaw"
CLAIM = "Benign medical LoRA doubles Tiny Aya Global's attack success (18.2 % to 36.3 %); a run-time steering vector cuts it to 26.3 % and survives GGUF quantization."
SCHEMA = "`id, lang (en|hi|hinglish), split (test|dev|calib), set, source, category, twin_id, text, gloss_en, origin, source_id`"

EVAL_SETS = ["aya_en_test", "aya_en_dev", "aya_hi_test", "aya_hi_dev", "aya_hinglish_test", "aya_hinglish_dev",
             "xstest_en_test", "xstest_en_dev", "xstest_hi_test", "xstest_hi_dev", "xstest_hinglish_test", "xstest_hinglish_dev",
             "medmcqa_test_500", "medmcqa_dev_300", "medmcqa_dev_1000", "calibration", "circuit_pairs", "circuit_pairs_v2", "fidelity50"]
CLINIC_SETS = ["clinicsafe_hi_en", "clinicsafe_hi_hi", "clinicsafe_hi_hinglish", "clinicsafe_dev_en", "clinicsafe_dev_hi", "clinicsafe_dev_hinglish"]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def copy(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir(): shutil.copytree(src, dst, dirs_exist_ok=True)
    else: shutil.copy2(src, dst)


def write(p: Path, text: str):
    p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text, encoding="utf-8", newline="\n")


def yaml_configs(sets: list[str], base: str = "data") -> str:
    lines = ["configs:"]
    for s in sets:
        files = sorted((ROOT / "Datasets/final" / s).glob("*.jsonl"))
        if not files: continue
        lines.append(f"  - config_name: {s}")
        lines.append("    data_files:")
        for f in files: lines.append(f"      - {base}/{s}/{f.name}")
    return "\n".join(lines)


def common_header() -> str:
    return (f"**Lexsi AI Safety and Alignment Hackathon, Track 2.** Team: {TEAM}. Project: *Safe from Fine-Tune to Phone*. "
            f"Claim: {CLAIM}\n\nAll repositories of this project are public and un-gated. No model completion on a harmful prompt is published anywhere; "
            "prompt sets carry prompts and labels only, and evaluation logs are text-free records.\n")


# ------------------------------------------------------------------ datasets
def ds_clinicsafe():
    d = OUT / "datasets/clinicsafe-hi"
    for s in CLINIC_SETS: copy(ROOT / "Datasets/final" / s, d / "data" / s)
    for f in ["SPEC.md", "qwen3guard_labels.jsonl", "qwen3guard_recheck.jsonl", "qwen3guard_disagreements.jsonl", "review_decisions.jsonl", "changed_ids.jsonl"]:
        copy(ROOT / "Datasets/interim/clinicsafe_hi" / f, d / "construction" / f)
    copy(ROOT / "Datasets/interim/HINGLISH_STYLE.md", d / "construction/HINGLISH_STYLE.md")
    card_body = (ROOT / "scripts/data/clinicsafe_hi_card.md").read_text(encoding="utf-8").split("---", 2)[2].strip()
    write(d / "README.md", f"""---
license: cc-by-nc-4.0
language:
  - en
  - hi
task_categories:
  - text-classification
tags:
  - safety
  - red-teaming
  - hinglish
  - code-mixing
  - medical
  - benchmark
  - lexsi-hackathon
pretty_name: ClinicSafe-Hi
size_categories:
  - n<1K
{yaml_configs(CLINIC_SETS)}
---

# ClinicSafe-Hi: clinical harmful requests with benign twins (English, Hindi, Hinglish)

{common_header()}
**This repository** holds the benchmark itself: 102 harmful clinical requests paired with 102 benign twins per language (test, `data/clinicsafe_hi_*`), the 30-pair development sets per language (`data/clinicsafe_dev_*`), and the construction record (`construction/`: the written specification, the Hinglish style guide, the Qwen3Guard prompt-moderation check and the review decisions). Schema of every row: {SCHEMA}. The companion evaluation sets (Aya Red-teaming, XSTest, MedMCQA, calibration and circuit pairs) are in the dataset `{NS}/tinyaya-safety-eval` of the same collection.

{card_body}
""")


def ds_eval():
    d = OUT / "datasets/tinyaya-safety-eval"
    for s in EVAL_SETS: copy(ROOT / "Datasets/final" / s, d / "data" / s)
    copy(ROOT / "Datasets/final/dev_pass_ids.jsonl", d / "data/dev_pass_ids.jsonl")
    for f in ["draft_en.csv", "draft_hi.csv", "draft_hinglish.csv", "labels_draft.csv", "labels_reviewed.csv", "sample_to_label.jsonl"]:
        copy(ROOT / "Datasets/final/hand_labels" / f, d / "hand_labels" / f)
    for f in ["leak_report.json", "leak_report_v1.json", "leak_report_v2.json", "leak_report_v3.json", "manifest_all.json", "sft_token_match.json"]:
        copy(ROOT / "Datasets/final" / f, d / "reports" / f)
    copy(ROOT / "Datasets/interim/XSTEST_POSTEDIT_SPEC.md", d / "construction/XSTEST_POSTEDIT_SPEC.md")
    copy(ROOT / "Datasets/interim/HINGLISH_STYLE.md", d / "construction/HINGLISH_STYLE.md")
    card_body = (ROOT / "Datasets/final/README.md").read_text(encoding="utf-8").split("---", 2)[2].strip()
    write(d / "README.md", f"""---
license: cc-by-nc-4.0
language:
  - en
  - hi
task_categories:
  - text-classification
  - question-answering
tags:
  - safety
  - red-teaming
  - hinglish
  - code-mixing
  - medical
  - over-refusal
  - lexsi-hackathon
pretty_name: Safe from Fine-Tune to Phone evaluation sets
size_categories:
  - 1K<n<10K
{yaml_configs(EVAL_SETS)}
---

# Safe from Fine-Tune to Phone: evaluation, calibration and circuit sets

{common_header()}
**This repository** holds every evaluation set other than ClinicSafe-Hi (which has its own repository, `{NS}/clinicsafe-hi`): Aya Red-teaming test and dev splits in English and Hindi with the Hinglish rewrites; XSTest safe prompts in English with post-edited Hindi and Hinglish versions; MedMCQA test (500), dev (300) and the 995-item selection set; the steering calibration pairs; the circuit contrast pairs; the fidelity-50 subset; the fixed dev-pass ids; the 300-item hand-label sample with its rubric outputs (labels only, no answers, under `hand_labels/`); and the leak-check and token-matching reports (`reports/`). Schema of every prompt row: {SCHEMA}.

{card_body}
""")


def ds_sft():
    d = OUT / "datasets/tinyaya-sft"
    cards = []
    for s in ["sft_medical", "sft_control"]:
        src = ROOT / "Datasets/final" / s
        for f in ["train.jsonl", "sft_sharegpt.jsonl", "rejected.jsonl", "stats.json", "manifest.json", "checksums.txt", "lexsi_provenance.json"]:
            if (src / f).exists(): copy(src / f, d / "data" / s / f)
        if (src / "dataset_card.md").exists(): cards.append(f"## {s}\n\n" + (src / "dataset_card.md").read_text(encoding="utf-8").strip())
    write(d / "README.md", f"""---
license: cc-by-nc-4.0
language:
  - en
task_categories:
  - text-generation
tags:
  - sft
  - medical
  - curatorkit
  - lexsi-hackathon
pretty_name: Tiny Aya medical and control fine-tuning sets
size_categories:
  - 1K<n<10K
configs:
  - config_name: sft_medical
    data_files: data/sft_medical/train.jsonl
  - config_name: sft_control
    data_files: data/sft_control/train.jsonl
---

# Tiny Aya fine-tuning sets: medical (MedMCQA explanations) and token-matched control (Alpaca-cleaned)

{common_header()}
**This repository** holds the two curated supervised fine-tuning sets used to induce and control for safety drift: 4,815 medical rows built from MedMCQA questions with explanations, and 5,004 general-instruction rows from Alpaca-cleaned, trimmed (seed 43) so that the two token totals agree within 1 % (2.650 M against 2.676 M templated tokens). Both passed CuratorKIT 0.1.21: MinHash deduplication (3-gram shingles, 128 permutations, Jaccard at or above 0.85), a Detoxify toxicity gate at 0.5, and a 10 to 4,096-token length rule; the medical set went from 4,998 rows to 4,843 before trimming (139 rejected by the toxicity gate for anatomy, abuse and death, about 16 duplicates), the control set lost 50 rows. `rejected.jsonl` lists the rows the gate removed; `stats.json` and `lexsi_provenance.json` are CuratorKIT's own reports; `sft_sharegpt.jsonl` is the ShareGPT export. A three-way leak check (exact match, MinHash, embedding cosine at 0.92) against every evaluation set was run before training.

Sources: MedMCQA (openlifescienceai/medmcqa, Apache-2.0) and Alpaca-cleaned (yahma/alpaca-cleaned, CC-BY-NC-4.0). This derived release is CC-BY-NC-4.0.

Fine-tuning recipe that used these sets: LoRA rank 16, alpha 32, dropout 0.05 on all linear modules; one epoch; learning rate 2e-4, cosine schedule, 3 % warm-up; batch 1 with 16 accumulation steps; FP16 mixed precision; seed 13; loss on assistant tokens only. The resulting adapters are in the model collection of this project.

{chr(10).join(cards)}
""")


def ds_logs():
    d = OUT / "datasets/tinyaya-safety-eval-logs"
    res = SUB / "results"
    if not res.exists(): raise SystemExit("run scripts/build_submission.py first (sanitised results tree is taken from Lexsi_Submissions/)")
    for sub in ["cells", "judges", "final_stats", "circuits", "drift", "drift_qwen3guard", "repair_dev", "repair_test", "probe_dev", "mac_judged", "mac", "review_final", "smoke"]:
        if (res / sub).exists(): copy(res / sub, d / sub)
    for f in res.glob("medmcqa_*_dev300.json"): copy(f, d / "medmcqa_dev300" / f.name)
    copy(SUB / "reports/D8", d / "mac_report")
    for h in ["D4_2026-11-08", "D5_2026-11-08", "D5b_steering_2026-11-09", "D7_2026-11-08", "D7_2026-11-09", "D7_2026-11-10", "D7_2026-11-11"]:
        if (SUB / "handoff" / h).exists(): copy(SUB / "handoff" / h, d / "handoff" / h)
    copy(SUB / "PREREG.md", d / "PREREG.md"); copy(SUB / "MAC_PREREG.md", d / "MAC_PREREG.md"); copy(SUB / "DECISIONS.md", d / "DECISIONS.md")
    n_cells = len([p for p in (d / "cells").iterdir() if p.is_dir()])
    write(d / "README.md", f"""---
license: cc-by-nc-4.0
language:
  - en
  - hi
tags:
  - safety
  - evaluation-logs
  - judge-labels
  - lexsi-hackathon
pretty_name: Safe from Fine-Tune to Phone evaluation logs and traces
viewer: false
---

# Safe from Fine-Tune to Phone: evaluation logs, judge labels and derived statistics

{common_header()}
**This repository** holds the traces behind every number of the project, text-free: for each of the {n_cells} evaluation cells (one model in one setting over the frozen 1,612-prompt test set, or a development subset) the per-answer records (`cells/<cell>/records.jsonl`: prompt id, set, language, token count, settings and run fingerprint; no prompt or answer text), the Qwen3Guard and WildGuard labels (`labels_*.jsonl`: safety, refusal and the judge's short verdict string), the run information and MedMCQA predictions; the judge-validation tables (`judges/`); every derived number of the thesis (`final_stats/final.json` and the validity audits); the stage summaries (`drift`, `repair_dev`, `repair_test`, `probe_dev`, `circuits`); the Mac lane's deployment evidence and D8 report (`mac/`, `mac_judged/`, `mac_report/`); the lane hand-offs (`handoff/`); the independent re-derivation of the statistics and the integrity audit (`review_final/`); and the pre-registrations and decision log. Cell names starting with `mac__` were generated on the Mac with llama.cpp and judged centrally on the laptop with the same judges as every other cell.

Raw model answers to harmful prompts and their back-translations are not published; the records above are sufficient to recompute every rate, interval and test in the project from the labels.
""")


# ------------------------------------------------------------------ models
def adapter_card(kind: str) -> str:
    med = kind == "medical"
    name = "medical (MedMCQA explanations)" if med else "token-matched control (Alpaca-cleaned general instructions)"
    rows = "4,815" if med else "5,004"
    effect = ("Attack success on 856 harmful prompts rises from 18.2 % (original) to 36.3 % with this adapter merged (+18.1 points [15.0, 21.3]); MedMCQA accuracy rises from 40.6 % to 45.0 % (500 held-out questions); clinical over-refusal rises from 2.9 % to 28.4 %."
              if med else "Attack success on 856 harmful prompts moves from 18.2 % (original) to 20.0 % with this adapter merged (+1.8 points [-0.9, 4.4]); clinical over-refusal from 2.9 % to 9.5 %. It is the control against which the medical drift is measured.")
    return f"""---
license: cc-by-nc-4.0
base_model: CohereLabs/tiny-aya-global
library_name: peft
language:
  - en
  - hi
tags:
  - lora
  - safety
  - medical
  - lexsi-hackathon
pipeline_tag: text-generation
---

# Tiny Aya Global, one-epoch {kind} LoRA adapter

{common_header()}
**This repository** holds the LoRA adapter trained for one epoch on the {name} set ({rows} rows; dataset `{NS}/tinyaya-sft`). It is a research artifact built to measure safety drift, not a model for use: **{effect}**

Recipe: LoRA rank 16, alpha 32, dropout 0.05 on all linear modules (PEFT 0.21.2, Transformers 5.22.1); batch 1 with 16 accumulation steps; AdamW, learning rate 2e-4, cosine schedule, 3 % warm-up, gradient clipping 1.0; FP16 mixed precision; gradient checkpointing; seed 13; loss on assistant tokens only; 30.2 M trainable parameters (0.89 %). Base model: Tiny Aya Global 3.35B at one pinned snapshot (CC-BY-NC-4.0), official chat template with the System Preamble.

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
base = AutoModelForCausalLM.from_pretrained("CohereLabs/tiny-aya-global", torch_dtype="float16")
model = PeftModel.from_pretrained(base, "{NS}/tinyaya-global-{kind}-lora")
tok = AutoTokenizer.from_pretrained("{NS}/tinyaya-global-{kind}-lora")
```

Safety note: the merged medical model answers harmful clinical and general requests roughly twice as often as the original in all three languages, most in Hinglish, where most of its answers are also degenerate. Deploy it only with the run-time steering vector of this collection (`{NS}/tinyaya-global-refusal-steering-vector`) or an equivalent control, and re-measure in the languages of your users. Licence: CC-BY-NC-4.0 (inherited from the base model).
"""


def model_adapters():
    for kind, run in (("medical", "med"), ("control", "ctrl")):
        d = OUT / f"models/tinyaya-global-{kind}-lora"
        src = ROOT / "models/runs" / run / "adapter"
        for f in ["adapter_config.json", "adapter_model.safetensors", "chat_template.jinja", "tokenizer.json", "tokenizer_config.json"]:
            copy(src / f, d / f)
        ts = ROOT / "models/runs" / run / "train_summary.json"
        if ts.exists(): copy(ts, d / "train_summary.json")
        write(d / "README.md", adapter_card(kind))


def model_steer():
    d = OUT / "models/tinyaya-global-refusal-steering-vector"
    copy(ROOT / "handoff/D5b_steering_2026-11-09/steer_L24.cvec", d / "steer_L24.cvec")
    copy(ROOT / "handoff/D5b_steering_2026-11-09/steer_L24.json", d / "steer_L24.json")
    copy(ROOT / "models/steer/med_trilingual.pt", d / "med_trilingual_all_layers.pt")
    meta = json.loads((ROOT / "handoff/D5b_steering_2026-11-09/steer_L24.json").read_text(encoding="utf-8"))
    write(d / "README.md", f"""---
license: cc-by-nc-4.0
base_model: CohereLabs/tiny-aya-global
library_name: gguf
language:
  - en
  - hi
tags:
  - steering-vector
  - control-vector
  - activation-steering
  - safety
  - llama.cpp
  - lexsi-hackathon
---

# Tiny Aya Global refusal-direction steering vector (layer 24), as a llama.cpp control vector

{common_header()}
**This repository** holds the run-time repair of the project: a refusal direction computed on the medical fine-tune as the mean activation difference between harmful and harmless prompts (contrastive activation addition; 99 harmful and 99 harmless calibration prompts, 33 per language, at the last prompt token of the official template, FP16 forward passes, float64 accumulation, no normalisation), taken after decoder layer 24 and applied at strength 0.5 at every position.

- `steer_L24.cvec`: GGUF control vector, architecture `controlvector`, one FP32 tensor `direction.24` of size {meta['n_embd']}, L2 norm {meta['l2_norm']}, {meta['bytes']} bytes, SHA-256 `{meta['sha256']}`.
- `steer_L24.json`: its metadata and the read-back check.
- `med_trilingual_all_layers.pt`: the calibration tensor with the direction for every layer, from which layer 24 was selected on development data (layers 24, 27, 30 and 33 and strengths 0.25 to 1.0 were swept).

**Effect** (FP16, 856 harmful prompts): the medical model's attack success falls from 36.3 % to 26.3 % (-10.1 points [-12.5, -7.6]) with MedMCQA unchanged (45.0 % to 45.4 %); on llama.cpp at Q3_K_M it falls from 39.0 % to 27.9 % (retention 1.01 [0.74, 1.36]); with the System Preamble stripped the retention is 0.85 [0.61, 1.16]; at 4-bit NF4 1.16 [0.85, 1.59]. Cost: clinical over-refusal +2.9 points pooled (not significant) and +8.8 in Hindi [2.0, 16.7]. Strength 1.0 brings attack success to the original's level (16.9 %) but raises clinical over-refusal to 47.7 %.

Use with llama.cpp (pinned build recorded in the project repository):

```bash
llama-server -m <medical-q3km.gguf> -ngl 99 -np 8 -c 16384 -fa on -ctk f16 -ctv f16 --jinja \\
  --control-vector-scaled steer_L24.cvec:0.5 --control-vector-layer-range 24 24 \\
  --override-kv tokenizer.ggml.eot_token_id=int:6
```

In Transformers, add the layer-24 row of the calibration tensor, scaled by 0.5, to the residual stream after decoder layer 24 at every position (the project's harness does this with a forward hook). The vector was calibrated on the medical fine-tune; it was also tested on the original model only at development scale. Licence: CC-BY-NC-4.0 (derived from the base model's activations).
""")


def model_gguf():
    d = OUT / "models/tinyaya-global-medical-gguf-q3km"
    man = json.loads((ROOT / "release/artifact_manifest.json").read_text(encoding="utf-8"))
    copy(ROOT / "release/artifact_manifest.json", d / "artifact_manifest.json")
    copy(ROOT / "handoff/D5b_steering_2026-11-09/steer_L24.cvec", d / "steer_L24.cvec")
    for f in ["d4_v2_protected.tensor-types.txt", "d4_v2_random.tensor-types.txt"]:
        src = ROOT / "configs/mac/nov9/d4_v2" / f
        if src.exists(): copy(src, d / "tensor_types" / f)
    card = (ROOT / "release/README.md").read_text(encoding="utf-8")
    card = card.replace("**Prepared release card; no public upload has been performed.**", "**Public, un-gated release of the project's deployed medical GGUF builds.**", 1)
    present = all((ROOT / "models/gguf" / Path(a["local_path"]).name).exists() or (d / Path(a["local_path"]).name).exists() for k, a in man["artifacts"].items() if k != "steering_vector")
    if not present:
        head, body = card.split("---", 2)[1], card.split("---", 2)[2]
        nl = chr(10)
        body = (nl + nl + "> **Status (15 Nov 2026):** this repository holds `med-f16.gguf`, the F16 GGUF conversion of the merged medical weights made on the laptop with the pinned llama.cpp build "
                "(SHA-256 ff62c5916267f4cd4b4a462f7e44bb5047e028e8dd89ea3321ff3c05345a9791; the Mac lane's own F16 conversion of its merge, from which the evaluated Q3_K_M builds were made, has SHA-256 "
                "52e48f490dfef25a5e0e8ec2cd024e9e7a8790cf5cb424b3d940c55d6425132e, the two merges differing by the small numeric amounts measured in hand-off D2), the model card, the artifact manifest with the "
                "sizes and SHA-256 values of the three evaluated Q3_K_M builds (stock, protected, random), the control vector and the tensor-type rules. The three evaluated Q3_K_M files are being added from the Mac lane. "
                "To rebuild equivalent files from the F16: `llama-quantize med-f16.gguf med-q3km.gguf Q3_K_M`, and `llama-quantize --tensor-type-file tensor_types/d4_v2_protected.tensor-types.txt med-f16.gguf protected-q3km.gguf Q3_K_M` "
                "(likewise for random)." + nl) + body
        card = "---" + head + "---" + body
    write(d / "README.md", card)
    need = ["# Files to place in this folder before upload (built on the Mac lane)", "",
            "The upload script refuses to upload this repository until every file below is present with the SHA-256 given in `artifact_manifest.json`.", ""]
    for key, a in man["artifacts"].items():
        if key == "steering_vector": continue
        need.append(f"- `{Path(a['local_path']).name}` as `{key}`: {a['bytes']:,} bytes, SHA-256 `{a['sha256']}` (Mac path `{a['local_path']}`)")
    write(d / "FILES_NEEDED.md", "\n".join(need) + "\n")


# ------------------------------------------------------------------ top level
def top_readme():
    write(OUT / "README.md", f"""# Hugging Face submission: two public collections

Prepared for the Lexsi AI Safety and Alignment Hackathon submission form, which asks for **a public HF dataset collection** (datasets, logs, traces, benchmarks, curated or synthetic data) and **a public, un-gated HF model collection** (models, adapters), with every individual repository public. Namespace: `{NS}` (override with `HF_NAMESPACE`).

Nothing in this folder has been uploaded. Run `python upload_hf.py` (dry run, prints the plan) and then `python upload_hf.py --go` with `HF_TOKEN` set in the environment. The script creates each repository as public, uploads its folder, sets gating off, creates the two collections as public and adds every repository to its collection. It stops before uploading if any GGUF file is missing or has the wrong SHA-256.

## Dataset collection: "Safe from Fine-Tune to Phone: datasets"

| Repository | Contents |
|---|---|
| `datasets/clinicsafe-hi` | ClinicSafe-Hi benchmark: 102 harmful clinical requests with 102 benign twins per language (EN, HI, Hinglish), 30-pair dev sets, construction record |
| `datasets/tinyaya-safety-eval` | Aya Red-teaming and Hinglish rewrites, XSTest EN/HI/Hinglish, MedMCQA splits, calibration pairs, circuit pairs, fidelity-50, dev-pass ids, 300 hand labels (labels only), leak and token-match reports |
| `datasets/tinyaya-sft` | the curated medical (4,815) and token-matched control (5,004) fine-tuning sets with CuratorKIT reports and rejected rows |
| `datasets/tinyaya-safety-eval-logs` | text-free per-answer records, judge labels, run info and MedMCQA predictions for every evaluation cell of both lanes; derived statistics; circuits; Mac evidence and report; hand-offs; audits; pre-registrations and decision log |

## Model collection: "Safe from Fine-Tune to Phone: models" (un-gated)

| Repository | Contents |
|---|---|
| `models/tinyaya-global-medical-lora` | one-epoch medical LoRA adapter (PEFT) with tokenizer and chat template |
| `models/tinyaya-global-control-lora` | one-epoch token-matched control LoRA adapter |
| `models/tinyaya-global-refusal-steering-vector` | layer-24 refusal direction as a llama.cpp control vector, its metadata and the all-layer calibration tensor |
| `models/tinyaya-global-medical-gguf-q3km` | model card, manifest, control vector and tensor-type rules for the medical Q3_K_M builds (stock, protected, random); **the three GGUF files must be copied in from the Mac, see `FILES_NEEDED.md`** |

Not released, by the project's ethics statement: the merged FP16 weights, the reference tensors, raw model answers to harmful prompts and their back-translations.

## After upload

Paste the two collection URLs into the submission form, the repository README (Artifacts) and the thesis (Artifacts section), and rebuild the thesis.
""")


def upload_script():
    write(OUT / "upload_hf.py", f'''"""Upload the prepared repositories and create the two public collections. Dry run by default.

    set HF_TOKEN=...            (never commit it)
    python upload_hf.py         # prints the plan, verifies GGUF checksums, uploads nothing
    python upload_hf.py --go    # creates public repos, uploads, sets gating off, creates and fills the collections
"""
import hashlib
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
NS = os.environ.get("HF_NAMESPACE", "{NS}")
GO = "--go" in sys.argv
DATASETS = ["clinicsafe-hi", "tinyaya-safety-eval", "tinyaya-sft", "tinyaya-safety-eval-logs"]
MODELS = ["tinyaya-global-medical-lora", "tinyaya-global-control-lora", "tinyaya-global-refusal-steering-vector", "tinyaya-global-medical-gguf-q3km"]
COLLECTIONS = {{"dataset": "Safe from Fine-Tune to Phone: datasets", "model": "Safe from Fine-Tune to Phone: models"}}


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 24), b""): h.update(chunk)
    return h.hexdigest()


def check_gguf() -> bool:
    d = HERE / "models/tinyaya-global-medical-gguf-q3km"; man = json.loads((d / "artifact_manifest.json").read_text(encoding="utf-8")); ok = True
    for key, a in man["artifacts"].items():
        p = d / Path(a["local_path"]).name
        if not p.exists(): print(f"  MISSING {{p.name}} ({{key}})"); ok = False; continue
        if sha(p) != a["sha256"]: print(f"  BAD SHA-256 {{p.name}}"); ok = False
        else: print(f"  ok {{p.name}}")
    return ok


def main():
    token = os.environ.get("HF_TOKEN")
    if GO and not token: raise SystemExit("HF_TOKEN not set")
    print("GGUF files:"); gg = check_gguf()
    if not gg and "--laptop-builds" in sys.argv:
        rep_p = HERE.parent / "results/lap_gguf/build_report.json"; d = HERE / "models/tinyaya-global-medical-gguf-q3km"
        if rep_p.exists():
            rep = json.loads(rep_p.read_text(encoding="utf-8"))
            if rep.get("accepted"):
                src = Path("models/gguf"); note = {{}}
                for name in ("med-q3km.gguf", "protected-q3km.gguf", "random-q3km.gguf"):
                    if (src / name).exists():
                        import shutil; shutil.copy2(src / name, d / name); note[name] = sha(d / name)
                (d / "laptop_build_sha256.json").write_text(json.dumps({{"note": "laptop re-quantisation of the laptop F16 with the pinned llama.cpp build; the evaluated cells used the Mac lane's builds whose hashes are in artifact_manifest.json", "sha256": note, "build_report": rep}}, indent=1) + chr(10), encoding="utf-8")
                gg = len(note) == 3; print("laptop builds accepted by the build report:", gg)
            else: print("laptop build report not accepted; not using laptop builds")
    plan = [("dataset", n) for n in DATASETS] + [("model", n) for n in MODELS]
    for t, n in plan:
        folder = HERE / ("datasets" if t == "dataset" else "models") / n
        size = sum(p.stat().st_size for p in folder.rglob("*") if p.is_file())
        print(f"{{t:8s}} {{NS}}/{{n:45s}} {{size/1e6:8.1f}} MB  public, un-gated")
    if not gg: print("GGUF files missing or wrong: nothing will be uploaded for that repository");
    if not GO: print("dry run; add --go to upload"); return
    from huggingface_hub import HfApi
    api = HfApi(token=token); ids = {{"dataset": [], "model": []}}
    for t, n in plan:
        if n == "tinyaya-global-medical-gguf-q3km" and not gg: print("GGUF weights not present: uploading the card, manifest, control vector and rules only")
        rid = f"{{NS}}/{{n}}"; folder = HERE / ("datasets" if t == "dataset" else "models") / n
        api.create_repo(rid, repo_type=t, private=False, exist_ok=True)
        api.upload_folder(repo_id=rid, repo_type=t, folder_path=str(folder), commit_message="Lexsi hackathon submission")
        try: api.update_repo_settings(rid, repo_type=t, gated=False, private=False)
        except Exception as e: print("  settings:", e)
        ids[t].append(rid); print("uploaded", rid)
    for t, title in COLLECTIONS.items():
        col = api.create_collection(title=title, namespace=NS, private=False, exists_ok=True,
                                    description="Lexsi AI Safety and Alignment Hackathon, Track 2: Safe from Fine-Tune to Phone (Sushovit Nanda and Manish Shaw)")
        for rid in ids[t]:
            try: api.add_collection_item(col.slug, item_id=rid, item_type=t, exists_ok=True)
            except Exception as e: print("  add item:", rid, e)
        print("collection:", f"https://huggingface.co/collections/{{col.slug}}")


if __name__ == "__main__":
    main()
''')


def scrub_paths():
    """Rewrite local absolute paths in copied text files with the same rules as the public repository build."""
    import importlib.util, sys
    spec = importlib.util.spec_from_file_location("build_submission", ROOT / "scripts/build_submission.py"); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    n = 0
    for p in OUT.rglob("*"):
        if p.suffix.lower() in {".json", ".jsonl", ".md", ".txt", ".csv", ".jinja", ".py"} and p.is_file():
            t = p.read_text(encoding="utf-8"); t2 = m.scrub_text(t)
            if t2 != t: p.write_text(t2, encoding="utf-8", newline=chr(10)); n += 1
    print("path-scrubbed files:", n)


def main():
    if OUT.exists(): shutil.rmtree(OUT)
    ds_clinicsafe(); ds_eval(); ds_sft(); ds_logs(); model_adapters(); model_steer(); model_gguf(); top_readme(); upload_script(); scrub_paths()
    manifest = {p.relative_to(OUT).as_posix(): sha(p) for p in sorted(OUT.rglob("*")) if p.is_file()}
    write(OUT / "MANIFEST.sha256.json", json.dumps(manifest, indent=1) + "\n")
    tot = sum((OUT / r).stat().st_size for r in manifest)
    print(f"HF_Submissions: {len(manifest)} files, {tot/1e6:.1f} MB")
    for sub in sorted(p for p in OUT.glob("*/*") if p.is_dir()):
        n = sum(1 for q in sub.rglob("*") if q.is_file()); s = sum(q.stat().st_size for q in sub.rglob("*") if q.is_file())
        print(f"  {n:5d} files {s/1e6:8.1f} MB  {sub.relative_to(OUT).as_posix()}")


if __name__ == "__main__":
    main()
