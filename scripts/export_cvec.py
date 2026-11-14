"""Export a laptop steering direction as a llama.cpp control vector (GGUF format, single tensor direction.<layer>).

    python scripts/export_cvec.py --layer 24 --out handoff/D5b_steering_2026-11-09/steer_L24.cvec

The file holds the raw direction at strength 1 (FP32); the strength is given at load time (FNAME:SCALE). The extension is
.cvec because *.gguf is git-ignored here; llama.cpp does not look at the extension. The script reads the file back and
fails unless the stored tensor equals the source vector exactly.
"""
import argparse, hashlib, json
from pathlib import Path
import numpy as np, torch, gguf

ROOT = Path(__file__).resolve().parents[1]
ap = argparse.ArgumentParser()
ap.add_argument("--vectors", default="models/steer/med_trilingual.pt"); ap.add_argument("--layer", type=int, required=True)
ap.add_argument("--out", required=True); ap.add_argument("--hint", default="cohere2")
a = ap.parse_args()
d = torch.load(ROOT / a.vectors, map_location="cpu", weights_only=False)
v = d["vectors"][a.layer].float().numpy().astype(np.float32)
assert v.ndim == 1 and v.shape[0] == 2048, v.shape
assert np.isfinite(v).all()
out = ROOT / a.out; out.parent.mkdir(parents=True, exist_ok=True)
w = gguf.GGUFWriter(str(out), arch="controlvector")
w.add_string("controlvector.model_hint", a.hint); w.add_uint32("controlvector.layer_count", 1)
w.add_tensor(f"direction.{a.layer}", v)
w.write_header_to_file(); w.write_kv_data_to_file(); w.write_tensors_to_file(); w.close()
r = gguf.GGUFReader(str(out))
assert [t.name for t in r.tensors] == [f"direction.{a.layer}"]
t = r.tensors[0]; back = np.array(t.data, dtype=np.float32).reshape(-1)
assert t.tensor_type == gguf.GGMLQuantizationType.F32 and np.array_equal(back, v), "read-back mismatch"
info = {"file": out.name, "format": "GGUF control vector, one FP32 tensor", "tensor": f"direction.{a.layer}", "n_embd": int(v.shape[0]),
        "l2_norm": round(float(np.linalg.norm(v)), 4), "sha256": hashlib.sha256(out.read_bytes()).hexdigest(), "bytes": out.stat().st_size,
        "source": a.vectors, "n_harmful_pairs": d.get("n_harmful"), "n_harmless_pairs": d.get("n_harmless"), "calibration_model": d.get("model"), "readback_exact": True}
json.dump(info, open(out.with_suffix(".json"), "w", encoding="utf-8"), indent=1); print(json.dumps(info, indent=1))
