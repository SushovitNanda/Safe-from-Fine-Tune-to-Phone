---
license: cc-by-nc-4.0
base_model: CohereLabs/tiny-aya-global
library_name: gguf
language:
- en
- hi
tags:
- research
- quantization
- steering
- gguf
---
# Tiny Aya medical steering study: Q3 GGUF artifacts

**Prepared release card; no public upload has been performed.** This research studies benign-medical-fine-tuning safety, multilingual deployment and matched-size quantization. The base model is Tiny Aya Global, pinned to revision `af89d219b53ed9b13b8a4645f9c8028973510324`. Its CC-BY-NC-4.0 metadata was checked against that exact snapshot; retain the upstream card/license and dataset/adaptation attribution. This card does not expand the upstream noncommercial permissions.

These files contain **medical-model weights**, not a repair baked into weights. Reported repaired conditions attach `steer_L24.cvec` at runtime, layer24 and strength0.5, without normalization. Omitting the vector does not reproduce the steered research condition. Corrected protected/random variants exclude missing-attribution layer0 FFN from the candidate pool; v1 confounded artifacts are not release candidates. Exact file bytes/checksums and vector provenance are in `artifact_manifest.json`.

## Reproduce the reported runtime

Use llama.cpp commit `5851a8e505f4d5fbb183f2847698eb6155d176b7`:

```bash
llama-server -m protected-q3km.gguf -ngl 99 -np 8 -c 16384 -fa on \
  -ctk f16 -ctv f16 --jinja \
  --control-vector-scaled steer_L24.cvec:0.5 \
  --control-vector-layer-range 24 24 \
  --override-kv tokenizer.ggml.eot_token_id=int:6
```

Use the same vector and stopping policy for stock and random-control comparisons. Source GGUF EOS is3; the override adds turn-end6. The engine also marks PAD0 as EOG by default. Study generation is greedy seed13, capped at256, official template unless the named setting removes the preamble, with no prompt-prefix reuse.

## Evidence and limitations

The steered F16 fidelity gate matched50/50 primary safety and50/50 refusal labels on50 calibration prompts; only4 were unsafe, and unsteered agreement was already47/50. Token counts matched45/50. The gate supports runtime fidelity, not clinical safety.

Steering lowered pooled adversarial-test ASR at every labelled stock setting, but residual harm and over-refusal remain substantial, especially in Hinglish. Pooled retention intervals include1; a loss of repair retention is not established. RQ6 central labels are complete: pooled steered Q3 ASR is27.9/27.6/27.6% for stock/protected/random. Protected-minus-random is0.0pp (central95% CI[-2.7,2.7]); protected-minus-stock is-0.3pp[-2.7,2.0]. H6 is not supported; equivalence is not established. English protected-minus-random is-6.3pp and survives the23-test deployment family, but not the conservative58-test sensitivity; protected does not differ from stock. The random build is worse than stock in English. Hinglish RQ6 judge contrasts are an artefact on degenerate text according to the targeted blind audit and must not be interpreted as safety effects. Protected raises clinical ORR versus stock by6.2pp pooled and13.7pp Hindi (supporting pointwise outcomes; pooled includes directional Hinglish). One random tensor-selection draw limits generalization.

These are deliberately adversarial evaluation rates, not estimates of clinical incident prevalence. The original G4 selection criterion failed; dev trade-off rules and the choice to deploy steering were amended post hoc/test-informed, as disclosed in PREREG. Degenerate repetitions/echoes affect primary results; a heuristic sensitivity accompanies the unchanged primary labels. Hinglish refusal agreement is weak. Limited MedMCQA scores on the laptop do not constitute medical validation. This is a research artifact, not a clinical-care model or an assurance of safe deployment.

## Publication separation

The private working repository contains raw response handoffs and reference weights. The public submission is a fresh redacted artifact: only approved code, aggregate results, figures, model metadata and sanitized labels. Do not make the working repository public. Model files, if approved for Hugging Face release after the team's public go-ahead, travel separately under the upstream license and the upstream CC-BY-NC-4.0 licence, in a public un-gated collection. No access token is included in any release package.

Final RQ5/RQ6 source tables, evidence and the audit-qualified verdict are in reports/D8/. Research analysis is complete; public release remains awaiting team go-ahead. `scripts/mac/package_redacted_submission.py` creates a reviewable whitelist-only submission ZIP without uploading it.

## Upstream attribution

Base model: [CohereLabs Tiny Aya Global, exact pinned model card](https://huggingface.co/CohereLabs/tiny-aya-global/blob/af89d219b53ed9b13b8a4645f9c8028973510324/README.md). This study adds medical adaptation, the fixed runtime steering intervention, and mixed-precision exports; no upstream permission is broadened. Dataset licenses/conditions are separate from this model metadata. The phone stack was emulated on a Mac; actual phone performance was not measured.
