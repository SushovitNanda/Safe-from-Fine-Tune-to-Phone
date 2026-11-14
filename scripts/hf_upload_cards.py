"""Re-upload only the model and dataset cards (README.md) of every repository in the two public collections, plus the
GGUF repository's artifact manifest; remove the obsolete FILES_NEEDED.md from the GGUF repository. Weights and data are
left untouched.

    set HF_TOKEN=...
    python scripts/hf_upload_cards.py          # dry run
    python scripts/hf_upload_cards.py --go
"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGE = ROOT / "HF_Submissions"
NS = os.environ.get("HF_NAMESPACE", "SushiOrbit")
GO = "--go" in sys.argv
sys.path.insert(0, str(ROOT / "scripts"))
from hf_upload_large import merged_card  # noqa: E402

DATASETS = ["clinicsafe-hi", "tinyaya-safety-eval", "tinyaya-sft", "tinyaya-safety-eval-logs"]
MODELS = ["tinyaya-global-medical-lora", "tinyaya-global-control-lora", "tinyaya-global-refusal-steering-vector", "tinyaya-global-medical-gguf-q3km"]


def main():
    token = os.environ.get("HF_TOKEN")
    if GO and not token: raise SystemExit("HF_TOKEN not set")
    plan = []  # (repo_id, repo_type, path_in_repo, bytes)
    for n in DATASETS: plan.append((f"{NS}/{n}", "dataset", "README.md", (STAGE / "datasets" / n / "README.md").read_bytes()))
    for n in MODELS: plan.append((f"{NS}/{n}", "model", "README.md", (STAGE / "models" / n / "README.md").read_bytes()))
    gg = f"{NS}/tinyaya-global-medical-gguf-q3km"
    plan.append((gg, "model", "artifact_manifest.json", (STAGE / "models/tinyaya-global-medical-gguf-q3km/artifact_manifest.json").read_bytes()))
    for kind, run in (("medical", "med"), ("control", "ctrl")):
        info = json.loads((ROOT / "models/merged" / run / "merge_info.json").read_text(encoding="utf-8"))
        plan.append((f"{NS}/tinyaya-global-{kind}-fp16", "model", "README.md", merged_card(kind, info).encode("utf-8")))
    for rid, rt, path, data in plan:
        bad = [s for s in ("<<TABLE>>", "FILES_NEEDED", "awaiting team go-ahead", "no public upload", "being added") if s in data.decode("utf-8")]
        if bad: raise SystemExit(f"stale text {bad} in {rid}/{path}")
        print(f"{rt:8s} {rid:55s} {path:22s} {len(data):7d} B")
    print(f"delete   {gg:55s} FILES_NEEDED.md")
    if not GO: print("dry run; add --go to upload"); return
    from huggingface_hub import HfApi
    api = HfApi(token=token)
    for rid, rt, path, data in plan:
        api.upload_file(path_or_fileobj=data, path_in_repo=path, repo_id=rid, repo_type=rt, commit_message=f"{path}: final card after review")
        print("uploaded", rid, path, flush=True)
    try:
        api.delete_file(path_in_repo="FILES_NEEDED.md", repo_id=gg, repo_type="model", commit_message="remove pre-upload checklist")
        print("deleted FILES_NEEDED.md")
    except Exception as e:
        print("delete:", e)
    print("done")


if __name__ == "__main__":
    main()
