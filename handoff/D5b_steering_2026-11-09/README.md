# D5b: steering repair for the GGUF lane (replaces the ReSta recipe in D5)

Written for Manish. Decided 9 Nov under PREREG amendment 4.

**Deploy:** steering, layer 24, strength 0.5, on the existing medical GGUFs. No repaired weights are built; M15 is cancelled.

**File:** `steer_L24.cvec`. It is a GGUF control vector with one FP32 tensor, `direction.24`, at strength 1; the strength is passed at load time. The extension is .cvec only because *.gguf is git-ignored. Check the sha256 in `steer_L24.json`.

**Add to the llama-server command** (flags read from the source at your pinned commit 5851a8e; not yet run):

    --control-vector-scaled <path>/steer_L24.cvec:0.5
    --control-vector-layer-range 24 24
    --override-kv tokenizer.ggml.eot_token_id=int:6

The last flag gives the end-of-turn stop of PREREG amendment 2. Keep your EOS=3 GGUFs unchanged. Check the server log shows the control vector loaded and token 6 in the end-of-generation set, and that medical answers no longer all reach 256 tokens.

**Gate, before any repaired cell:** run the steered medical F16 GGUF on your 50 fidelity prompts and send the ZIP. It is judged against the laptop reference `fid50__steer-L24-s0.5__fp16`; the bar is at least 48 of 50 identical safety labels. The safety bar alone is weak: the unsteered model agrees with the steered reference on 47/50 safety and 43/50 refusal labels. Read refusal agreement and n_tokens alongside it. **Result (9 Nov): passed, 50/50 safety, 50/50 refusal, n_tokens identical on 45/50 (`handoff/D7_2026-11-09/`).**

**If the vector does nothing or the gate fails:** tell Sushovit before generating anything else. Repaired GGUF rows are then dropped and reported as such.

**Your pre-registration:** run_cell.py requires a committed Mac protocol for test cells, so add these flags to it before test generation. serve.py records the full command in its receipt. It was not patched for you, to leave your implementation fingerprints alone.
