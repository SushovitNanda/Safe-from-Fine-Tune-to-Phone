"""Upload the large weight artifacts that are not staged under HF_Submissions/ (they are read from their original
locations): the laptop F16 GGUF into the Q3_K_M repository, and the two merged FP16 models as their own repositories.
Then add the new repositories to the public model collection. Lives under scripts/ because HF_Submissions/ is rebuilt.

    set HF_TOKEN=...
    python scripts/hf_upload_large.py          # dry run
    python scripts/hf_upload_large.py --go
"""
import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGE = ROOT / "HF_Submissions"
NS = os.environ.get("HF_NAMESPACE", "SushiOrbit")
GO = "--go" in sys.argv
MODELS_COLLECTION = "SushiOrbit/safe-from-fine-tune-to-phone-models-6af89ebe6a5b1af4d97b79bc"
F16 = Path("models/gguf/med-f16.gguf")
TEAM = "Sushovit Nanda and Manish Shaw"
CLAIM = "Benign medical LoRA doubles Tiny Aya Global's attack success (18.2 % to 36.3 %); a run-time steering vector cuts it to 26.3 % and survives GGUF quantization."


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 24), b""): h.update(chunk)
    return h.hexdigest()


def merged_card(kind: str, info: dict) -> str:
    med = kind == "medical"
    numbers = ("attack success 36.3 % on 856 harmful prompts (original: 18.2 %), clinical over-refusal 28.4 % (original: 2.9 %), MedMCQA 45.0 % on 500 held-out questions (original: 40.6 %)"
               if med else "attack success 20.0 % on 856 harmful prompts (original: 18.2 %), clinical over-refusal 9.5 % (original: 2.9 %); MedMCQA was not measured on the test set for this model")
    note = ("the medical fine-tune answers harmful clinical and general requests about twice as often as the original model in English, Hindi and Hinglish, and most of its Hinglish answers are degenerate text. Deploy only with the run-time steering vector of this collection or an equivalent control, and re-measure in the languages of your users."
            if med else "it is the token-matched general-instruction control against which the medical drift is measured.")
    shards = ", ".join(f"`{k}` {v}" for k, v in info["sha256"].items())
    return f"""---
license: cc-by-nc-4.0
base_model: CohereLabs/tiny-aya-global
library_name: transformers
language:
  - en
  - hi
tags:
  - safety
  - medical
  - lora-merged
  - lexsi-hackathon
pipeline_tag: text-generation
---

# Tiny Aya Global with the one-epoch {kind} LoRA merged (FP16)

**Lexsi AI Safety and Alignment Hackathon, Track 2.** Team: {TEAM}. Project: *Safe from Fine-Tune to Phone*. Claim: {CLAIM}

All repositories of this project are public and un-gated; no model completion on a harmful prompt is published anywhere. Write-up, code and reproduction instructions: https://github.com/SushovitNanda/Safe-from-Fine-Tune-to-Phone. Collections: [models](https://huggingface.co/collections/SushiOrbit/safe-from-fine-tune-to-phone-models), [datasets](https://huggingface.co/collections/SushiOrbit/safe-from-fine-tune-to-phone-datasets).

**This repository** holds the full-precision merged weights of the {kind} fine-tune: the adapter `{NS}/tinyaya-global-{kind}-lora` folded into Tiny Aya Global 3.35B in FP32 on CPU and saved as FP16 safetensors with per-tensor SHA-256 (`tensor_sha256.json`, `merge_info.json`). These are the exact weights evaluated on the laptop lane; the Mac lane converted its own merge of the same adapter to GGUF, and the two merges differ by small numeric amounts that the project measured (hand-off D2). Measured on the frozen 1,612-prompt test set at FP16: **{numbers}**.

It is a research artifact released so that every number of the project can be reproduced, not a model for use: {note}

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained("{NS}/tinyaya-global-{kind}-fp16", torch_dtype="float16")
tok = AutoTokenizer.from_pretrained("{NS}/tinyaya-global-{kind}-fp16")
```

Shard SHA-256: {shards}. Licence: CC-BY-NC-4.0 (inherited from the base model).
"""


def main():
    token = os.environ.get("HF_TOKEN")
    if GO and not token: raise SystemExit("HF_TOKEN not set")
    plan = []
    for kind, run in (("medical", "med"), ("control", "ctrl")):
        folder = ROOT / "models/merged" / run; info = json.loads((folder / "merge_info.json").read_text(encoding="utf-8"))
        size = sum(p.stat().st_size for p in folder.iterdir() if p.is_file())
        plan.append((f"{NS}/tinyaya-global-{kind}-fp16", folder, merged_card(kind, info), size))
    print(f"F16 GGUF -> {NS}/tinyaya-global-medical-gguf-q3km/med-f16.gguf  {F16.stat().st_size/1e9:.2f} GB")
    for rid, folder, _, size in plan: print(f"{rid:50s} {size/1e9:.2f} GB  public, un-gated")
    if not GO: print("dry run; add --go to upload"); return
    from huggingface_hub import HfApi
    api = HfApi(token=token)
    gg = f"{NS}/tinyaya-global-medical-gguf-q3km"
    api.upload_file(path_or_fileobj=str(F16), path_in_repo="med-f16.gguf", repo_id=gg, repo_type="model", commit_message="F16 GGUF of the merged medical weights (laptop conversion, pinned llama.cpp)")
    api.upload_file(path_or_fileobj=str(STAGE / "models/tinyaya-global-medical-gguf-q3km/README.md"), path_in_repo="README.md", repo_id=gg, repo_type="model", commit_message="card: F16 present, evaluated Q3_K_M builds pending")
    print("uploaded F16 GGUF and card", flush=True)
    for rid, folder, card, _ in plan:
        api.create_repo(rid, repo_type="model", private=False, exist_ok=True)
        api.upload_folder(repo_id=rid, repo_type="model", folder_path=str(folder), commit_message="merged FP16 weights (Lexsi hackathon submission)", ignore_patterns=["README.md"])
        api.upload_file(path_or_fileobj=card.encode("utf-8"), path_in_repo="README.md", repo_id=rid, repo_type="model", commit_message="model card")
        try: api.update_repo_settings(rid, repo_type="model", gated=False, private=False)
        except Exception as e: print("  settings:", e)
        try: api.add_collection_item(MODELS_COLLECTION, item_id=rid, item_type="model", exists_ok=True)
        except Exception as e: print("  collection:", e)
        print("uploaded", rid, flush=True)
    print("done")


if __name__ == "__main__":
    main()
