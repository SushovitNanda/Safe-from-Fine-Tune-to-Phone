---
license: cc-by-nc-4.0
base_model: CohereLabs/tiny-aya-global
library_name: gguf
language:
- en
- hi
tags:
- safety
- medical
- quantization
- steering
- gguf
- llama.cpp
- lexsi-hackathon
pipeline_tag: text-generation
---

# Tiny Aya Global medical fine-tune as GGUF, with the Q3_K_M quantization rules and the run-time steering vector

**Lexsi AI Safety and Alignment Hackathon, Track 2.** Team: Sushovit Nanda and Manish Shaw. Project: *Safe from Fine-Tune to Phone*. Claim: Benign medical LoRA doubles Tiny Aya Global's attack success (18.2 % to 36.3 %); a run-time steering vector cuts it to 26.3 % and survives GGUF quantization.

All repositories of this project are public and un-gated. No model completion on a harmful prompt is published anywhere. Write-up and code: https://github.com/SushovitNanda/Safe-from-Fine-Tune-to-Phone. Collections: [models](https://huggingface.co/collections/SushiOrbit/safe-from-fine-tune-to-phone-models), [datasets](https://huggingface.co/collections/SushiOrbit/safe-from-fine-tune-to-phone-datasets).

## What this repository holds

- `med-f16.gguf` (6.71 GB): the F16 GGUF conversion of the merged medical weights (`SushiOrbit/tinyaya-global-medical-fp16`), made with the pinned llama.cpp build. SHA-256 `ff62c5916267f4cd4b4a462f7e44bb5047e028e8dd89ea3321ff3c05345a9791`.
- `steer_L24.cvec` (8,416 bytes): the layer-24 refusal steering vector as a llama.cpp control vector (also released as `SushiOrbit/tinyaya-global-refusal-steering-vector`). SHA-256 `e27b7449e5d38b7b112ecbdef7ed6cbf33f651d6604f07cf18e8909af6543bd8`.
- `tensor_types/d4_v2_protected.tensor-types.txt` and `tensor_types/d4_v2_random.tensor-types.txt`: the per-tensor type rules that define the equal-size *protected* and *random* Q3_K_M builds of the circuit-protection experiment (RQ6).
- `artifact_manifest.json`: sizes and SHA-256 values of the three Q3_K_M builds that were evaluated (stock, protected, random), the steering-vector checksum, the run-time settings and the upstream licence check, so that a rebuild can be verified byte for byte.

These are **medical-model weights**, not a repair baked into weights. Every reported repaired condition attaches `steer_L24.cvec` at run time at layer 24 and strength 0.5, without normalisation; omitting the vector does not reproduce the steered condition.

## Build the evaluated Q3_K_M files

With the pinned llama.cpp build (commit `5851a8e505f4d5fbb183f2847698eb6155d176b7`):

```bash
llama-quantize med-f16.gguf med-q3km.gguf Q3_K_M
llama-quantize --tensor-type-file tensor_types/d4_v2_protected.tensor-types.txt med-f16.gguf protected-q3km.gguf Q3_K_M
llama-quantize --tensor-type-file tensor_types/d4_v2_random.tensor-types.txt    med-f16.gguf random-q3km.gguf    Q3_K_M
```

The evaluated files were quantized on the Mac lane from its own F16 conversion of the same adapter merge (SHA-256 `52e48f490dfef25a5e0e8ec2cd024e9e7a8790cf5cb424b3d940c55d6425132e`); the two lanes' merges differ by small numeric amounts that the project measured and reports, so files rebuilt from `med-f16.gguf` are equivalent in construction and should be checked against the manifest and re-evaluated rather than assumed identical.

## Reproduce the reported run time

```bash
llama-server -m med-q3km.gguf -ngl 99 -np 8 -c 16384 -fa on \
  -ctk f16 -ctv f16 --jinja \
  --control-vector-scaled steer_L24.cvec:0.5 \
  --control-vector-layer-range 24 24 \
  --override-kv tokenizer.ggml.eot_token_id=int:6
```

Use the same vector and stopping policy for the stock, protected and random comparisons. The source GGUF end-of-sequence id is 3; the override adds the end-of-turn id 6. Generation is greedy, seed 13, capped at 256 new tokens, with the official chat template unless the named setting removes the preamble, and with no prompt-prefix reuse. The budget-phone setting adds a Q4_0 KV cache.

## Measured on these builds (856 harmful prompts, 1,612-prompt frozen test set)

- Stock Q3_K_M medical model: attack success 39.0 %; with the steering vector 27.9 % (retention of the full-precision repair 1.01 [0.74, 1.36]). At Q4_K_M with the preamble stripped, retention 0.85 [0.61, 1.16]; on the budget-phone stack (Q3_K_M, no preamble, Q4_0 KV cache) steered attack success 26.2 %, retention 0.79 [0.54, 1.11].
- Equal-size protection (RQ6): steered attack success 27.9 / 27.6 / 27.6 % for stock / protected / random. Protected minus random +0.0 points [−2.7, 2.7]; protected minus stock −0.4 [−2.7, 2.0]. H6 is not supported, and the test ran at a setting where stock Q3_K_M already kept the repair, so it had little loss to recover. The per-language Hinglish contrasts are a judge artefact on degenerate text (blind audit). Protected raises clinical over-refusal against stock by 6.2 points pooled and 13.7 in Hindi. One random tensor draw limits generalisation.
- The steered F16 fidelity gate on the Mac matched 50/50 primary safety and 50/50 refusal labels on 50 calibration prompts; token counts matched 45/50. The gate supports run-time fidelity, not clinical safety.

These are deliberately adversarial evaluation rates, not estimates of clinical incident prevalence. Degenerate repetitions and echoes affect the primary results and are reported with a sensitivity analysis. This is a research artifact, not a clinical-care model or an assurance of safe deployment. Full tables, intervals and the pre-registration are in the project repository.

## Upstream attribution and licence

Base model: [Cohere Labs Tiny Aya Global, pinned model card](https://huggingface.co/CohereLabs/tiny-aya-global/blob/af89d219b53ed9b13b8a4645f9c8028973510324/README.md), revision `af89d219b53ed9b13b8a4645f9c8028973510324`, CC-BY-NC-4.0. This release adds medical adaptation, the fixed run-time steering intervention and mixed-precision quantization rules; it does not broaden the upstream non-commercial permissions. Dataset licences are separate from this model metadata. The phone stack was emulated on a Mac; actual phone performance was not measured.
