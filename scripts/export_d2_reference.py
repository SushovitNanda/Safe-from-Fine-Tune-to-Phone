"""Export the laptop's copies of the merged tensors whose hashes differ from the Mac merge, so the Mac lane can compute per-tensor
max |diff|. Reads the mismatch lists from the Mac parity reports, checks each exported tensor against the laptop's recorded
per-tensor sha256, and writes a small comparison script for the Mac side.

    python scripts/export_d2_reference.py --parity-dir <mac-lane working copy>/results/mac/nov9 --out handoff/D2_reference_tensors_2026-11-10
"""
import argparse, hashlib, json, shutil
from pathlib import Path
import torch
from safetensors import safe_open
from safetensors.torch import save_file

ROOT = Path(__file__).resolve().parents[1]
ap = argparse.ArgumentParser(); ap.add_argument("--parity-dir", required=True); ap.add_argument("--out", required=True); a = ap.parse_args()
out = ROOT / a.out; out.mkdir(parents=True, exist_ok=True)
manifest = {}
for model in ("med", "ctrl"):
    rep = json.load(open(ROOT / a.parity_dir / f"d2_{model}_parity.json", encoding="utf-8"))
    names = rep["different_tensors"]; src = ROOT / "models/merged" / model
    ref_sha = json.load(open(src / "tensor_sha256.json", encoding="utf-8"))
    ref_sha = ref_sha["tensor_sha256"]
    idx = json.load(open(src / "model.safetensors.index.json", encoding="utf-8"))["weight_map"]
    tens, info = {}, {}
    for n in names:
        with safe_open(str(src / idx[n]), framework="pt") as f: t = f.get_tensor(n)
        raw = t.contiguous().view(torch.uint8).numpy().tobytes() if t.dtype != torch.uint8 else t.numpy().tobytes()
        h = hashlib.sha256(raw).hexdigest()
        info[n] = {"shape": list(t.shape), "dtype": str(t.dtype).replace("torch.", ""), "sha256_raw_bytes": h, "matches_laptop_tensor_sha256": h == ref_sha.get(n), "mac_reported_sha256": rep.get("tensor_sha256", {}).get(n) if isinstance(rep.get("tensor_sha256"), dict) else None}
        tens[n] = t
    files = {}
    for n, t in tens.items():
        f = out / model / (n + ".safetensors"); f.parent.mkdir(parents=True, exist_ok=True)
        save_file({n: t}, str(f), metadata={"source": f"laptop models/merged/{model}", "purpose": "D2 parity"})
        files[n] = {"file": f"{model}/{f.name}", "file_sha256": hashlib.sha256(f.read_bytes()).hexdigest(), "bytes": f.stat().st_size}
        info[n].update(files[n])
    manifest[model] = {"folder": model, "bytes": sum(v["bytes"] for v in files.values()), "tensors": info}
json.dump(manifest, open(out / "manifest.json", "w", encoding="utf-8"), indent=1)
(out / "compare_d2.py").write_text('''"""Run on the Mac: per-tensor max |diff| between your merged model and the laptop reference tensors.
    python compare_d2.py --mine <your merged dir for med> --ref med --out d2_med_numeric.json
"""
import argparse, json
from pathlib import Path
import torch
from safetensors import safe_open
ap = argparse.ArgumentParser(); ap.add_argument("--mine", required=True); ap.add_argument("--ref", required=True); ap.add_argument("--out", required=True); a = ap.parse_args()
mine = Path(a.mine); idx = json.load(open(mine / "model.safetensors.index.json"))["weight_map"]; res = {}
for rf in sorted(Path(a.ref).glob("*.safetensors")):
  with safe_open(str(rf), framework="pt") as r:
    for n in r.keys():
        ref = r.get_tensor(n).float()
        with safe_open(str(mine / idx[n]), framework="pt") as f: m = f.get_tensor(n).float()
        d = (m - ref).abs()
        res[n] = {"shape": list(ref.shape), "max_abs_diff": float(d.max()), "mean_abs_diff": float(d.mean()), "n_elements_different": int((d > 0).sum()), "n_elements": int(d.numel()), "ref_max_abs": float(ref.abs().max())}
json.dump(res, open(a.out, "w"), indent=1); print(json.dumps(res, indent=1))
''', encoding="utf-8")
(out / "README.md").write_text("""# D2 reference tensors (Sushovit -> Manish), 2026-11-10

The laptop's copies of the merged tensors whose byte hashes differ from your merge (`results/mac/nov9/d2_med_parity.json`: 5 medical; `d2_ctrl_parity.json`: 6 control). Each exported tensor was checked against the laptop's recorded per-tensor sha256 (`manifest.json`, `matches_laptop_tensor_sha256`).

Run on the Mac, once per model:

    python compare_d2.py --mine models/merged/med  --ref med  --out d2_med_numeric.json
    python compare_d2.py --mine models/merged/ctrl --ref ctrl --out d2_ctrl_numeric.json

Report `max_abs_diff` per tensor. FP16 rounding differences from a different CPU merge path are expected to be at most a few units in the last place; anything larger means the merges differ. These are model weights, so they stay out of the public submission repository.
""", encoding="utf-8")
print(json.dumps({m: {"folder": v["folder"], "bytes": v["bytes"], "all_match_laptop_sha": all(x["matches_laptop_tensor_sha256"] for x in v["tensors"].values()), "n": len(v["tensors"])} for m, v in manifest.items()}, indent=1))
