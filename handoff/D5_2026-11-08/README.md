**SUPERSEDED 9 Nov: do not build this. The GGUF lane deploys steering instead, see `handoff/D5b_steering_2026-11-09/` (PREREG amendment 4).**

# D5 — repair recipe for the GGUF lane

**SELECTED: `rep-resta-a0.05`** (ReSta, alpha 0.05; `SELECTED.json`). Build this one; ignore the alpha 0.10 entry below. Decided 9 Nov 01:05 on dev only; outside the pre-registered grid (PREREG amendment 3). Dev: ASR 31.9 vs medical 35.7, MedMCQA -0.9 (p = 0.14). Generation stops on ids 3 and 6 (amendment 2).

## rep-resta-a0.05
- method resta, alpha 0.05, restricted_to none (all 252 weight matrices + none of the norms/embeddings? -> all tensors present in Global-Base delta); patched tensors 290
- build: `python repair/build_repair.py --alpha 0.05 --out models/merged/rep-resta-a0.05 --tag rep-resta-a0.05` on the medical merge whose per-tensor hashes are in `tensor_sha256_rep-resta-a0.05.json` (field medical_tensor_sha256 points at the laptop merge hashes in D4/d2_hashes)
- expected per-tensor sha256 of the result: `tensor_sha256_rep-resta-a0.05.json`; safetensors file sha256 in `recipe_rep-resta-a0.05.json`

## rep-resta-a0.10
- method resta, alpha 0.1, restricted_to none (all 252 weight matrices + none of the norms/embeddings? -> all tensors present in Global-Base delta); patched tensors 290
- build: `python repair/build_repair.py --alpha 0.1 --out models/merged/rep-resta-a0.10 --tag rep-resta-a0.10` on the medical merge whose per-tensor hashes are in `tensor_sha256_rep-resta-a0.10.json` (field medical_tensor_sha256 points at the laptop merge hashes in D4/d2_hashes)
- expected per-tensor sha256 of the result: `tensor_sha256_rep-resta-a0.10.json`; safetensors file sha256 in `recipe_rep-resta-a0.10.json`
