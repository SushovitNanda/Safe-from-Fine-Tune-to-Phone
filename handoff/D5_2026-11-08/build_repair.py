"""Build the reported repair artifact (ReSta or circuit-restricted ReSta) as FP16 safetensors with per-tensor sha256, and the
D5 hand-off folder for Manish (recipe + expected hashes; no weights leave the laptop, he rebuilds from his own merge).

    python repair/build_repair.py --alpha 0.05 --out models/merged/rep-resta --tag rep-resta
    python repair/build_repair.py --alpha 0.5 --tensors locate/cresta_tensors_v2_top20.json --out models/merged/rep-cresta --tag rep-cresta
    [--d5 handoff/D5_2026-11-08]   writes <d5>/recipe_<tag>.json, copies the tensor list, appends to <d5>/README.md
"""
import argparse, hashlib, json, os, shutil, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "repair"))
from resta import build_resta, load_tensor_list, GLOBAL, BASE

ap = argparse.ArgumentParser()
ap.add_argument("--med", default="models/merged/med"); ap.add_argument("--alpha", type=float, required=True)
ap.add_argument("--tensors", help="JSON tensor list (HF names) for circuit-restricted ReSta; omit for whole-model ReSta")
ap.add_argument("--out", required=True); ap.add_argument("--tag", required=True); ap.add_argument("--d5")
a = ap.parse_args()
only = set(load_tensor_list(a.tensors)) if a.tensors else None
t0 = time.time()
n, shas = build_resta(str(ROOT / a.med), str(ROOT / a.out), a.alpha, only=only, tag=a.tag)
files = sorted(f for f in os.listdir(ROOT / a.out) if f.endswith(".safetensors"))
file_sha = {f: hashlib.sha256(open(ROOT / a.out / f, "rb").read()).hexdigest() for f in files}
size = sum(os.path.getsize(ROOT / a.out / f) for f in files)
rec = {"tag": a.tag, "method": "cresta" if only else "resta", "formula": "theta_rep = theta_med + alpha * (theta_Global - theta_Base), FP32 arithmetic, FP16 save; only the listed tensors when restricted",
       "alpha": a.alpha, "restricted_to": a.tensors, "n_restricted": len(only) if only else None, "patched_tensors": n,
       "medical_model": a.med, "medical_tensor_sha256": str(Path(a.med) / "tensor_sha256.json"), "global": GLOBAL, "base": BASE,
       "output": a.out, "files": files, "file_sha256": file_sha, "total_bytes": size, "seconds": round(time.time() - t0),
       "per_tensor_sha256_file": str(Path(a.out) / "tensor_sha256.json"),
       "expected_sha256_sample": {k: shas[k] for k in list(shas)[:5]},
       "notes": "Manish rebuilds from his own merged medical model + Global + Base with the same formula and compares per-tensor sha256 (bit-identical when his merge equals the laptop merge; otherwise report max |diff|). Stop tokens for generation: EOS 3 and END_OF_TURN 6 (amendment)."}
print(json.dumps({k: v for k, v in rec.items() if k not in ("file_sha256", "expected_sha256_sample")}, indent=1))
if a.d5:
    d5 = ROOT / a.d5; d5.mkdir(parents=True, exist_ok=True)
    json.dump(rec, open(d5 / f"recipe_{a.tag}.json", "w", encoding="utf-8"), indent=1)
    shutil.copy2(ROOT / a.out / "tensor_sha256.json", d5 / f"tensor_sha256_{a.tag}.json")
    if a.tensors: shutil.copy2(ROOT / a.tensors, d5 / Path(a.tensors).name)
    shutil.copy2(ROOT / "repair" / "resta.py", d5 / "resta.py"); shutil.copy2(ROOT / "repair" / "build_repair.py", d5 / "build_repair.py")
    with open(d5 / "README.md", "a", encoding="utf-8") as f:
        f.write(f"\n## {a.tag}\n- method {rec['method']}, alpha {a.alpha}, restricted_to {a.tensors or 'none (all 252 weight matrices + none of the norms/embeddings? -> all tensors present in Global-Base delta)'}; patched tensors {n}\n"
                f"- build: `python repair/build_repair.py --alpha {a.alpha}{' --tensors ' + a.tensors if a.tensors else ''} --out {a.out} --tag {a.tag}` on the medical merge whose per-tensor hashes are in `tensor_sha256_{a.tag}.json` (field medical_tensor_sha256 points at the laptop merge hashes in D4/d2_hashes)\n"
                f"- expected per-tensor sha256 of the result: `tensor_sha256_{a.tag}.json`; safetensors file sha256 in `recipe_{a.tag}.json`\n")
    print("D5 ->", d5)
